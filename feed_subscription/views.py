from django.shortcuts import render

# Create your views here.
from django.utils.translation import gettext
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.request import Request
from rest_framework.views import APIView

from base_app.http_helpers import ok
from base_app.pginations import BasePageNumberPagination
from base_app.serializers import BaseSerializer
from feed_subscription.selectors import channel_exists, get_user_existing_channels
from feed_subscription.serializers import FeedSubscriptionReadOnlySerializer
from feed_subscription.services import subscribe_to_channel, delete_channel, update_channel, update_all_user_channels


class ChannelSubscriptionAPI(APIView):
    class FeedSubscriptionSerializer(BaseSerializer):
        rss_link = serializers.URLField()
        title = serializers.CharField(max_length=80)


        def validate_rss_link(self, value):
            # exist = subscription_exists(user=self.request.user, rss_link=value)
            # if exist:
            #     raise ValidationError(gettext("Already subscribed"))
            return value

    class Meta:
        fields = [
            'rss_link',
            'title',
        ]

    def post(self, request: Request):
        sr = self.FeedSubscriptionSerializer(request=request, data=request.data)
        sr.is_valid(True)
        sub = subscribe_to_channel(user=request.user, **sr.validated_data)
        sr = FeedSubscriptionReadOnlySerializer(sub, request=request)
        return ok(sr.data)

    def get(self, request):
        paginator = BasePageNumberPagination()
        query_set = get_user_existing_channels(user=request.user)
        result = paginator.paginate_queryset(query_set, request)
        sr = FeedSubscriptionReadOnlySerializer(result, many=True, request=request)
        return paginator.get_paginated_response(sr.data)


class ChannelRetrieveAPI(APIView):
    def delete(self, request, subscription_id):
        sub = delete_channel(user=request.user, subscription_id=subscription_id)
        sr = FeedSubscriptionReadOnlySerializer(sub, request=request)
        return ok(sr.data)


class UpdateUserChannels(APIView):
    def post(self, request: Request):
        user_id = request.user.id
        channel_id = request.query_params.get('channel_id')
        if channel_id is not None:
            update_channel.delay(user_id, int(channel_id))
        else:
            update_all_user_channels.delay(user_id)
        return ok({"message": gettext("updating channels")})



