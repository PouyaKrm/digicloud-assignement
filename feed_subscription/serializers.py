from base_app.serializers import BaseModelSerializer
from feed_subscription.models import FeedChannel, Article


class FeedSubscriptionReadOnlySerializer(BaseModelSerializer):

    class Meta:
        model = FeedChannel
        fields = [
            'id',
            'rss_link',
            'title',
            'description',
            'link',
        ]


class ArticleReadOnlySerializer(BaseModelSerializer):

    class Meta:
        model = Article
        fields = [
            'id',
            'title',
            'description',
            'link',
            'pub_date',
            'is_read',
            'is_favorite',
            'is_bookmarked',
        ]
