from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import FeedSubscription
from users.models import ApplicationUser


def subscription_exists(*args, user: ApplicationUser, rss_link: str) -> bool:
    return FeedSubscription.objects.filter(user=user, rss_link=rss_link, deleted=False).exists()


def get_existing_subscription_by_id(*args, user: ApplicationUser, subscription_id: int) -> FeedSubscription:
    try:
        return FeedSubscription.objects.get(id=subscription_id, user=user, deleted=False)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def get_subscription_by_id(*args, user: ApplicationUser, subscription_id: int) -> FeedSubscription:
    try:
        return FeedSubscription.objects.get(id=subscription_id, user=user)
    except ObjectDoesNotExist:
        raise ApplicationErrorException(ErrorCodes.RECORD_NOT_FOUND)


def try_get_subscription_by_id(*args, user: ApplicationUser, subscription_id: int) -> Optional[FeedSubscription]:
    try:
        return FeedSubscription.objects.get(id=subscription_id, user=user)
    except ObjectDoesNotExist:
        return None


def try_get_subscription_by_rss_link(*args,  user: ApplicationUser, rss_link: str) -> Optional[FeedSubscription]:
    try:
        return FeedSubscription.objects.get(rss_link=rss_link, user=user)
    except ObjectDoesNotExist:
        return None


def get_user_existing_subscriptions(*args, user: ApplicationUser):
    return FeedSubscription.objects.filter(user=user, deleted=False)
