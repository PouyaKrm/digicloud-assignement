from feed_subscription.models import FeedSubscription
from feed_subscription.selectors import try_get_subscription_by_id, try_get_subscription_by_rss_link, \
    get_existing_subscription_by_id
from users.models import ApplicationUser


def subscribe_to_feed(*args, user: ApplicationUser, rss_link: str) -> FeedSubscription:
    feed = try_get_subscription_by_rss_link(user=user, rss_link=rss_link)
    if feed is not None and feed.deleted:
        feed.deleted = False
        feed.save()
        return feed
    elif feed is not None:
        return feed
    return FeedSubscription.objects.create(user=user, rss_link=rss_link)


def delete_subscription(*args, user: ApplicationUser, subscription_id: int) -> FeedSubscription:
    sub = get_existing_subscription_by_id(user=user, subscription_id=subscription_id)
    sub.deleted = True
    sub.save()
    return sub



