import json

import pytest
from django.urls import reverse

from base_app.tests import *
from .fixtures import *
from feed_subscription.models import FeedChannel

pytestmark = pytest.mark.integration


def test__user_channels_get(api_client_authenticated):
    url = reverse('user_channels')
    response = api_client_authenticated.get(url)
    assert response.status_code == 200


def test__create_channel(api_client_authenticated):
    url = reverse("user_channels")
    rss_link = fake.url()
    data = {'title': fake.pystr(), "rss_link": rss_link}

    response = api_client_authenticated.post(url, data)

    assert response.status_code == 200
    assert FeedChannel.objects.filter(rss_link=rss_link).exists()


def test__delete_single_channel(api_client_authenticated, channel):
    url = reverse("retrieve_channel", kwargs={"subscription_id": channel.id})

    response = api_client_authenticated.delete(url)

    assert response.status_code == 200
    assert not FeedChannel.objects.filter(id=channel.id).exists()


def test__user_channels_update(api_client_authenticated):
    url = reverse("user_channels_update")

    response = api_client_authenticated.post(url)

    assert response.status_code == 200


def test__fetch_articles(articles, api_client_authenticated):
    channel_id = articles[0].channel.id
    url = reverse("articles", kwargs={"channel_id": channel_id})

    response = api_client_authenticated.get(url)

    assert response.status_code == 200
    result = response.data
    assert len(result) == len(articles)


def test__article_favorite(articles, api_client_authenticated):
    article = articles[0]
    favorite_before = article.is_favorite
    url = reverse("article_favorite", kwargs={"article_id": article.id})

    response = api_client_authenticated.put(url)

    assert response.status_code == 200
    favorite_after = response.data["is_favorite"]
    assert favorite_after == (not favorite_before)


def test__article_bookmark(articles, api_client_authenticated):
    article = articles[0]
    bookmark_before = article.is_bookmarked
    url = reverse("article_bookmark", kwargs={"article_id": article.id})

    response = api_client_authenticated.put(url)

    assert response.status_code == 200
    bookmark_after = response.data["is_bookmarked"]
    assert bookmark_after == (not bookmark_before)



