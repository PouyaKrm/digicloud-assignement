from unittest.mock import call

import pytest

from base_app.error_codes import ApplicationErrorException, ErrorCodes
from base_app.tests import *
from .fixtures import *
from feed_subscription.models import FeedChannel
from feed_subscription.services import subscribe_to_channel, delete_channel, delete_articles, _fetch_articles_task, \
    update_all_user_channels, update_user_channel, _update_channels

pytestmark = pytest.mark.unit


def mock__update_all_user_channels(mocker):
    return mocker.patch('feed_subscription.services.update_all_user_channels')


def mock__get_articles(mocker):
    return mocker.patch('feed_subscription.services.get_articles')


def mock__is_user_channels_updating(mocker):
    return mocker.patch('feed_subscription.services.is_user_channels_updating')


def mock__set_user_channels_updating(mocker):
    return mocker.patch('feed_subscription.services.set_user_channels_updating')


def mock__is_user_channel_updating(mocker, return_value=False):
    return mocker.patch('feed_subscription.services.is_user_channel_updating', return_value=return_value)


def mock__set_user_channel_updating(mocker):
    return mocker.patch('feed_subscription.services.set_user_channel_updating')


def mock__get_user_by_id(mocker):
    return mocker.patch('feed_subscription.services.get_user_by_id')


def mock__try_get_channel_by_id(mocker):
    return mocker.patch('feed_subscription.services.try_get_channel_by_id')


def mock___update_channels(mocker):
    return mocker.patch('feed_subscription.services._update_channels')


def mock___delete_articles(mocker):
    return mocker.patch('feed_subscription.services.delete_articles')


def mock__group(mocker, channels):
    return_vl = []
    articles = []
    for c in channels:
        for i in range(10):
            article = {'title': 'title', 'description': 'description', 'link': 'link'}
            articles.append(article)
        return_vl.append({'articles': articles, 'channel_id': c.id})

    class Test:
        def get(self):
            return return_vl

    return mocker.patch('feed_subscription.services.group', return_value=Test), articles


def mock___create_articles_from_task_result(mocker, articles=None):
    def side_effect_fn(result_list, channel_id):
        ar = []
        for a in result_list:
            a = Article(
                title=a.get('title'),
                description=a.get('description'),
                link=a.get('link'),
                channel_id=channel_id,
            )
            ar.append(a)

    mock = mocker.patch('feed_subscription.services._create_articles_from_task_result')
    if articles is None:
        mock.side_effect = side_effect_fn
    else:
        mock.return_value = articles
    return mock


@pytest.mark.parametrize("deleted", [False, True])
def test__test__subscribe_to_channel__channel_already_created(mocker, create_channel, user, deleted):
    channel = create_channel(user=user, deleted=deleted)
    mocked_task = mock__update_all_user_channels(mocker)

    result = subscribe_to_channel(user=user, rss_link=channel.rss_link, title=channel.title)

    mocked_task.delay.assert_called_with(user.id)
    assert result.title


def test__subscribe_to_channel(mocker, user):
    title = fake.pystr()
    link = fake.uri()

    mocked_task = mock__update_all_user_channels(mocker)

    channel = subscribe_to_channel(user=user, rss_link=link, title=title)

    mocked_task.delay.assert_called_with(user.id)
    found = FeedChannel.objects.filter(id=channel.id, rss_link=link, title=title)
    assert found.exists()


def test__delete_channel(channel):
    delete_channel(user=channel.user, channel_id=channel.id)
    assert channel.deleted


def test__delete_articles(articles):
    a = articles[0]
    ids = list(map(lambda e: e.id, articles))

    delete_articles(channel_id=a.channel.id)

    exist = Article.objects.filter(id__in=ids).exists()
    assert not exist


def test__fetch_articles_task__fails(mocker, channel):
    mock = mock__get_articles(mocker)
    mock.side_effect = ApplicationErrorException(ErrorCodes.FAILED_TO_FETCH_ARTICLES)
    rss_link = channel.rss_link

    result = _fetch_articles_task(rss_link=rss_link, channel_id=channel.id)

    mock.assert_has_calls([call(rss_link=rss_link), call(rss_link=rss_link)], any_order=True)
    assert result is None


def test__update_all_user_channels__already_updating(mocker, user):
    mock_updating = mock__is_user_channels_updating(mocker)
    mock_updating.return_value = True

    update_all_user_channels(user_id=user.id)

    mock_set_user_channels = mock__set_user_channels_updating(mocker)
    mock_updating.assert_called_once_with(user_id=user.id)
    mock_set_user_channels.assert_not_called()


def test__update_all_user_channels(mocker, channel):
    mock_updating = mock__is_user_channels_updating(mocker)
    mock_updating.return_value = False
    set_updating_mock = mock__set_user_channels_updating(mocker)
    mock_update_channel = mock___update_channels(mocker)

    update_all_user_channels(user_id=channel.user.id)

    mock_update_channel.assert_called_once_with(user_id=channel.user.id, channel_ids=[channel.id])
    assert set_updating_mock.call_count == 2


def test___update_channels(mocker, channel):
    group_mock = mock__group(mocker, [channel])
    mock_delete_articles = mock___delete_articles(mocker)

    _update_channels(user_id=channel.user.id, channel_ids=[channel.id])

    group_mock[0].assert_called_once()
    mock_delete_articles.assert_called_once_with(channel_id=channel.id)


def test__update_user_channel__already_updating(channel, mocker):
    mock_updating = mock__is_user_channel_updating(mocker, True)
    mock_get_user = mock__get_user_by_id(mocker)

    update_user_channel(user_id=channel.user.id, channel_id=channel.id)

    mock_updating.assert_called_once_with(user_id=channel.user.id, channel_id=channel.user.id)
    mock_get_user.assert_not_called()


def test__update_user_channel(channel, mocker):
    user_id = channel.user.id
    channel_id = channel.id
    mock_updating = mock__is_user_channel_updating(mocker)
    mock_set_updating = mock__set_user_channel_updating(mocker)
    mock_update_channel = mock___update_channels(mocker)

    update_user_channel(user_id=user_id, channel_id=channel_id)

    mock_updating.assert_called_once_with(user_id=user_id, channel_id=channel_id)
    assert mock_set_updating.call_count == 2
    mock_update_channel.assert_called_once_with(user_id=user_id, channel_ids=[channel_id])
