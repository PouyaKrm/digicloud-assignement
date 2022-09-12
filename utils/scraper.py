from typing import List, Union, Optional

import backoff
import requests
from bs4 import BeautifulSoup, ResultSet
from celery import shared_task

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from feed_subscription.models import Article


@shared_task
def get_articles(rss_link: str) -> List[dict]:
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
            article = {'title': title, 'description': description, 'link': link}
            result.append(article)
        return result
    except (requests.RequestException, AttributeError) as e:
        raise ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_ARTICLES, e)


def _find_field_or_none(key: str, result_set: Union[ResultSet, BeautifulSoup]) -> Optional:
    result = result_set.find(key)
    if result is not None:
        return result.text
    return None



