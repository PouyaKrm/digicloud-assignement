import requests
from bs4 import BeautifulSoup
from django.db import transaction

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import FeedChannel
from feed_subscription.selectors import try_get_channel_by_id, try_get_channel_by_rss_link, \
    get_existing_channel_by_id
from users.models import ApplicationUser


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
        return channel


def delete_channel(*args, user: ApplicationUser, subscription_id: int) -> FeedChannel:
    sub = get_existing_channel_by_id(user=user, subscription_id=subscription_id)
    sub.deleted = True
    sub.save()
    return sub


def get_channel_data(rss_link: str):
    try:
        r = requests.get(rss_link)
        if not r.status_code == 200:
            raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_CHANNEL_DATA)
        soup = BeautifulSoup(r.content, features="xml")
        title = soup.find('title').text
        link = soup.find('link').text
        description = soup.find('description').text
        return ChannelData(title, description, link)
    except (requests.RequestException, AttributeError) as e:
        raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_CHANNEL_DATA, e)


def _check_feed(rss_link):
    try:
        r = requests.get(rss_link)
        if r.status_code == 200:
            # print(r.content)
            soup = BeautifulSoup(r.content, features="xml")
            articles = soup.findAll('item')
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                description = a.find('description')
                # published = a.find('pubDate')
                article = {
                    'title': title,
                    'link': link,
                    # 'published': published
                }
                print(article)
    except Exception as e:
        raise e


class ChannelData:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link