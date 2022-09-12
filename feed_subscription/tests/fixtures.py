from typing import List

from base_app.tests import *
from feed_subscription.models import FeedChannel, Article


@pytest.fixture
def create_channel(db):
    def create(*args, user: ApplicationUser, rss_link: str = None, delete=False):
        title = fake.pystr()
        link = rss_link
        if rss_link is None:
            link = fake.uri()
        return FeedChannel.objects.create(user=user, title=title, rss_link=link, deleted=delete)

    return create


@pytest.fixture
def channel(user, create_channel) -> FeedChannel:
    return create_channel(user=user)


@pytest.fixture
def create_articles(channel):

    def create(*args, favorite=False, bookmark=False) -> List[Article]:
        for i in range(20):
            title = fake.pystr()
            description = fake.pystr()
            link = fake.uri()
            Article.objects.create(
                title=title,
                description=description,
                link=link,
                is_favorite=favorite,
                is_bookmarked=bookmark,
                channel=channel
            )
        return Article.objects.all()

    return create


@pytest.fixture
def articles(create_articles):
    return create_articles()
