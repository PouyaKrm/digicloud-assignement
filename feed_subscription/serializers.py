from base_app.serializers import BaseModelSerializer
from feed_subscription.models import FeedSubscription


class FeedSubscriptionReadOnlySerializer(BaseModelSerializer):

    class Meta:
        model = FeedSubscription
        fields = [
            'id',
            'rss_link',
            'title',
            'description'
        ]
