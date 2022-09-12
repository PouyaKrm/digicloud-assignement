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
 get_user_channels, get_channel_by_id, get_article_by_id, \
    get_user_channels_id_in
from users.models import ApplicationUser
from users.selectors import get_user_by_id
from utils.scraper import get_articles


def subscribe_to_channel(*args, user: ApplicationUser, rss_link: str, title: str) -> FeedChannel:
    channel = try_get_channel_by_rss_link(user=user, rss_link=rss_link)
    if channel is not None:
        channel.title = title
    else:
        channel = FeedChannel(user=user, rss_link=rss_link, title=title)
    channel.save()
    update_all_user_channels.delay(user.id)
    return channel


def delete_channel(*args, user: ApplicationUser, channel_id: int) -> FeedChannel:
    sub = get_channel_by_id(user=user, channel_id=channel_id)
    sub.delete()
    # sub.save()
    return sub


def delete_articles(*args, channel_id: int):
    Article.objects.filter(channel_id=channel_id, is_favorite=False, is_bookmarked=False).delete()


@shared_task
def update_all_user_channels(user_id: int):
    updating = is_user_channels_updating(user_id=user_id)
    print(updating)
    if updating:
        return
    set_user_channels_updating(user_id=user_id, insert=True)
    try:
        user = ApplicationUser.objects.get(id=user_id)
        channel_ids = get_user_channels(user=user).values_list('id', flat=True)
        channel_ids = list(channel_ids)
        _update_channels(user_id=user_id, channel_ids=channel_ids)
    finally:
        set_user_channels_updating(user_id=user_id, insert=False)


@shared_task
def update_user_channel(user_id: int, channel_id: int):
    updating = is_user_channel_updating(user_id=user_id, channel_id=channel_id)
    if updating:
        return
    try:
        set_user_channel_updating(user_id=user_id, channel_id=channel_id, insert=True)
        _update_channels(user_id=user_id, channel_ids=[channel_id])
    finally:
        set_user_channel_updating(user_id=user_id, channel_id=channel_id, insert=False)


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
    print(result_list is None)
    if result_list is None:
        return []

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


def _update_channels(user_id, channel_ids: List[int]):
    user = ApplicationUser.objects.get(id=user_id)
    channels = get_user_channels_id_in(user=user, channel_ids=channel_ids)
    if channels.count() == 0:
        return
    g = group(get_ar.s(c.rss_link, c.id) for c in channels)
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


@shared_task
@backoff.on_exception(backoff.expo, ApplicationErrorException, max_tries=2, raise_on_giveup=False)
def _fetch_articles_task(rss_link: str, channel_id):
    result = get_articles(rss_link=rss_link)
    articles = [{**a} for a in result]
    return {'articles': articles, 'channel_id': channel_id}

