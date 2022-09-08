from typing import List, Union, Optional

import requests
from bs4 import BeautifulSoup, ResultSet

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import Article


class ChannelData:
    def __init__(self, title, description, link):
        self.title = title
        self.description = description
        self.link = link


class ArticleData:
    def __init__(self, title, description, link, pub_date):
        self.title = title
        self.description = description
        self.link = link
        self.pub_date = pub_date


def get_articles(rss_link: str) -> List[ArticleData]:
    try:
        r = requests.get(rss_link)
        if not r.status_code == 200:
            raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_CHANNEL_DATA)
        soup = BeautifulSoup(r.content, features="xml")
        articles = soup.findAll('item')
        result = []
        for a in articles:
            title = _find_field_or_none('title', a)
            link = _find_field_or_none('link', a)
            description = _find_field_or_none('description', a)
            pub_date = _find_field_or_none('pubDate', a)
            article = ArticleData(title=title, link=link, description=description, pub_date=pub_date)
            result.append(article)
        return result
    except (requests.RequestException, AttributeError) as e:
        raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_ARTICLES, e)


def get_channel_data(rss_link: str) -> ChannelData:
    try:
        r = requests.get(rss_link)
        if not r.status_code == 200:
            raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_CHANNEL_DATA)
        soup = BeautifulSoup(r.content, features="xml")
        title = _find_field_or_none('title', soup)
        link = _find_field_or_none('link', soup)
        description = _find_field_or_none('description', soup)
        return ChannelData(title, description, link)
    except (requests.RequestException, AttributeError) as e:
        raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_CHANNEL_DATA, e)


def _find_field_or_none(key: str, result_set: Union[ResultSet, BeautifulSoup]) -> Optional:
    result = result_set.find(key)
    if result is not None:
        return result.text
    return None


