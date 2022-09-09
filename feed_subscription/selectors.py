from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import FeedChannel, Article
from users.models import ApplicationUser


def channel_exists(*args, user: ApplicationUser, rss_link: str) -> bool:
    return FeedChannel.objects.filter(user=user, rss_link=rss_link, deleted=False).exists()


def get_existing_channel_by_id(*args, user: ApplicationUser, channel_id: int) -> FeedChannel:
    try:
        return FeedChannel.objects.get(id=channel_id, user=user, deleted=False)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def get_channel_by_id(*args, user: ApplicationUser, channel_id: int) -> FeedChannel:
    try:
        return FeedChannel.objects.get(id=channel_id, user=user)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def try_get_channel_by_id(*args, user: ApplicationUser, channel_id: int) -> Optional[FeedChannel]:
    try:
        return FeedChannel.objects.get(id=channel_id, user=user)
    except ObjectDoesNotExist:
        return None


def try_get_channel_by_rss_link(*args, user: ApplicationUser, rss_link: str) -> Optional[FeedChannel]:
    try:
        return FeedChannel.objects.get(rss_link=rss_link, user=user)
    except ObjectDoesNotExist:
        return None


def get_user_existing_channels(*args, user: ApplicationUser):
    return FeedChannel.objects.filter(user=user, deleted=False)


def get_all_articles_by_channel_id(*args, user: ApplicationUser, channel_id: int, favorite=False, bookmark=False):
    q = Article.objects.filter(channel__user=user, channel_id=channel_id)
    if favorite:
        q = q.filter(is_favorite=True)
    elif bookmark:
        q = q.filter(is_bookmarked=True)
    return q


def get_article_by_id(*args, user: ApplicationUser, article_id: int) -> Article:
    try:
        return Article.objects.get(channel__user=user, id=article_id)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)
