from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import FeedChannel
from users.models import ApplicationUser


def channel_exists(*args, user: ApplicationUser, rss_link: str) -> bool:
    return FeedChannel.objects.filter(user=user, rss_link=rss_link, deleted=False).exists()


def get_existing_channel_by_id(*args, user: ApplicationUser, subscription_id: int) -> FeedChannel:
    try:
        return FeedChannel.objects.get(id=subscription_id, user=user, deleted=False)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def get_channel_by_id(*args, user: ApplicationUser, subscription_id: int) -> FeedChannel:
    try:
        return FeedChannel.objects.get(id=subscription_id, user=user)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def try_get_channel_by_id(*args, user: ApplicationUser, subscription_id: int) -> Optional[FeedChannel]:
    try:
        return FeedChannel.objects.get(id=subscription_id, user=user)
    except ObjectDoesNotExist:
        return None


def try_get_channel_by_rss_link(*args, user: ApplicationUser, rss_link: str) -> Optional[FeedChannel]:
    try:
        return FeedChannel.objects.get(rss_link=rss_link, user=user)
    except ObjectDoesNotExist:
        return None


def get_user_existing_channels(*args, user: ApplicationUser):
    return FeedChannel.objects.filter(user=user, deleted=False)
