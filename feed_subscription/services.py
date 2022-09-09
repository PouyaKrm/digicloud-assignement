from typing import List, Optional

import backoff
from celery import shared_task, group
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.cache import is_user_channels_updating, is_user_channel_updating, set_user_channels_updating, \
    set_user_channel_updating
from feed_subscription.models import FeedChannel, Article
from feed_subscription.selectors import try_get_channel_by_id, try_get_channel_by_rss_link, \
    get_existing_channel_by_id, get_user_existing_channels, get_channel_by_id, get_article_by_id
from users.models import ApplicationUser
from users.selectors import get_user_by_id
from utils.scraper import get_articles, get_channel_data


def subscribe_to_channel(*args, user: ApplicationUser, rss_link: str, title: str) -> FeedChannel:
    with transaction.atomic():
        channel = try_get_channel_by_rss_link(user=user, rss_link=rss_link)
        if channel is not None and channel.deleted:
            channel.deleted = False
        elif channel is None:
            channel = FeedChannel(user=user, rss_link=rss_link)
        channel.title = title
        channel.save()
    update_all_user_channels.delay(user.id)
    return channel


def delete_channel(*args, user: ApplicationUser, subscription_id: int) -> FeedChannel:
    sub = get_existing_channel_by_id(user=user, channel_id=subscription_id)
    sub.deleted = True
    sub.save()
    return sub


def delete_articles(*args, channel_id: int):
    Article.objects.filter(channel_id=channel_id, is_favorite=False, is_bookmarked=False).delete()


@shared_task
@backoff.on_exception(backoff.expo, ApplicationErrorException, max_tries=2, raise_on_giveup=False)
def fetch_articles_task(rss_link: str, channel_id):
    result = get_articles(rss_link=rss_link)
    articles = [{'title': a.title, 'description': a.description, 'link': a.link} for a in result]
    return {'articles': articles, 'channel_id': channel_id}


@shared_task
def update_all_user_channels(user_id: int):
    updating = is_user_channels_updating(user_id=user_id)
    print(updating)
    if updating:
        return
    set_user_channels_updating(user_id=user_id, insert=True)
    try:
        user = ApplicationUser.objects.get(id=user_id)
        channels = get_user_existing_channels(user=user)
        g = group(fetch_articles_task.s(c.rss_link, c.id) for c in channels)
        result = g().get()
        Article.objects.filter(channel__in=channels).delete()
        articles = []
        for r in result:
            if r is None:
                continue
            ar = _create_articles_from_task_result(result_list=r.get('articles'), channel_id=r.get('channel_id'))
            delete_articles(channel_id=r.get("channel_id"))
            articles.extend(ar)
        Article.objects.bulk_create(articles)
        channels.update(last_update=timezone.now())
    finally:
        set_user_channels_updating(user_id=user_id, insert=False)


@shared_task
def update_channel(user_id: int, chanel_id: int):
    updating = is_user_channel_updating(user_id=user_id, channel_id=chanel_id)
    print(updating)
    if updating:
        return
    user = get_user_by_id(user_id=user_id)
    channel = try_get_channel_by_id(user=user, channel_id=chanel_id)
    if channel is None:
        return
    set_user_channel_updating(user_id=user_id, channel_id=chanel_id, insert=True)
    try:
        channel = get_channel_by_id(user=user, channel_id=chanel_id)
        result = fetch_articles_task.delay(channel.rss_link, chanel_id).get()
        if result is None:
            return
        articles = _create_articles_from_task_result(result.get('articles'), channel_id=channel.id)
        if articles is not None and len(articles) > 0:
            delete_articles(channel_id=channel.id)
            Article.objects.bulk_create(articles)
        channel.last_update = timezone.now()
        channel.save()
    finally:
        set_user_channel_updating(user_id=user_id, channel_id=chanel_id, insert=False)


def toggle_article_favorite_by_article_id(*args, user: ApplicationUser, article_id: int) -> Article:
    article = get_article_by_id(user=user, article_id=article_id)
    article.is_favorite = not article.is_favorite
    article.save()
    return article


def toggle_article_bookmark_by_article_id(*args, user: ApplicationUser, article_id: int) -> Article:
    article = get_article_by_id(user=user, article_id=article_id)
    article.is_bookmarked = not article.is_bookmarked
    article.save()
    return article


def _create_articles_from_task_result(result_list: List[dict], channel_id: int, **kwargs) -> Optional[List[Article]]:
    articles = []
    if result_list is None:
        return None
    for a in result_list:
        a = Article(
            title=a.get('title'),
            description=a.get('description'),
            link=a.get('link'),
            channel_id=channel_id,
            **kwargs
        )
        articles.append(a)
    return articles
