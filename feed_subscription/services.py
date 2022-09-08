from typing import List, Optional, Union

import requests
from bs4 import BeautifulSoup, ResultSet
from django.db import transaction

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import FeedChannel, Article
from feed_subscription.selectors import try_get_channel_by_id, try_get_channel_by_rss_link, \
    get_existing_channel_by_id
from users.models import ApplicationUser
from utils.scraper import get_articles, get_channel_data


def subscribe_to_channel(*args, user: ApplicationUser, rss_link: str) -> FeedChannel:
    with transaction.atomic():
        channel = try_get_channel_by_rss_link(user=user, rss_link=rss_link)
        if channel is not None and channel.deleted:
            channel.deleted = False
            channel.save()
        elif channel is None:
            channel = FeedChannel.objects.create(user=user, rss_link=rss_link)
        channel_data = get_channel_data(rss_link)
        channel.title = channel_data.title
        channel.description = channel_data.description
        channel.link = channel_data.link
        channel.save()
        result = get_articles(rss_link=rss_link)
        print(result)
        return channel


def delete_channel(*args, user: ApplicationUser, subscription_id: int) -> FeedChannel:
    sub = get_existing_channel_by_id(user=user, subscription_id=subscription_id)
    sub.deleted = True
    sub.save()
    return sub


