from base_app.error_codes import ApplicationErrorException
from .fixtures import *
from ..selectors import channel_exists, try_get_channel_by_id, \
    get_all_articles_by_channel_id, get_article_by_id

pytestmark = pytest.mark.unit


def test__channel_exists(channel):
    exist = channel_exists(user=channel.user, rss_link=channel.rss_link)
    assert exist


def test__try_get_channel_by_id__returns_none(channel):
    found = try_get_channel_by_id(user=channel.user, channel_id=-1)
    assert found is None


def test__try_get_channel_by_id__success(channel):
    found = try_get_channel_by_id(user=channel.user, channel_id=channel.id)
    assert found is not None
    assert found.id == channel.id


get_all_articles_by_channel_id__test_data = [
    (False, False),
    (True, False),
    (True, True)
]


@pytest.mark.parametrize("favorite, bookmark", get_all_articles_by_channel_id__test_data)
def test__get_all_articles_by_channel_id(create_articles, user, channel, favorite, bookmark):
    articles = create_articles(favorite=True)
    result = get_all_articles_by_channel_id(user=user, channel_id=channel.id, favorite=favorite, bookmark=bookmark)
    count = len(articles)
    ids = list(map(lambda e: e.id, articles))
    assert result.count() == count
    assert result.filter(id__in=ids).count() == count


def test__get_article_by_id__throws(user):
    with pytest.raises(ApplicationErrorException):
        get_article_by_id(user=user, article_id=-1)


def test__test__get_article_by_id__success(user, articles):
    a = articles[0]
    article = get_article_by_id(user=user, article_id=a.id)
    assert article is not None
    assert article.id == a.id
