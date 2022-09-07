from base_app.serializers import BaseModelSerializer
from feed_subscription.models import FeedChannel


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
