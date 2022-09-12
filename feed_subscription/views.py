import re

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
from feed_subscription.selectors import channel_exists, get_user_channels, get_channel_by_id, \
    get_article_by_id, get_all_articles_by_channel_id
from feed_subscription.serializers import FeedSubscriptionReadOnlySerializer, ArticleReadOnlySerializer
from feed_subscription.services import subscribe_to_channel, delete_channel, update_user_channel, update_all_user_channels, \
    toggle_article_bookmark_by_article_id, toggle_article_favorite_by_article_id


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
        query_set = get_user_channels(user=request.user)
        result = paginator.paginate_queryset(query_set, request)
        sr = FeedSubscriptionReadOnlySerializer(result, many=True, request=request)
        return paginator.get_paginated_response(sr.data)


class ChannelRetrieveAPI(APIView):
    def delete(self, request, subscription_id):
        sub = delete_channel(user=request.user, channel_id=subscription_id)
        sr = FeedSubscriptionReadOnlySerializer(sub, request=request)
        return ok(sr.data)


class UpdateUserChannelsAPIView(APIView):
    def post(self, request: Request):
        user_id = request.user.id
        channel_id = request.query_params.get('channel_id')
        if channel_id is not None and re.match(r'^\d+$', channel_id):
            channel = get_channel_by_id(user=request.user, channel_id=int(channel_id))
            update_user_channel.delay(user_id, int(channel.id))
        else:
            update_all_user_channels.delay(user_id)
        return ok({"message": gettext("updating channels")})


class ArticlesAPIView(APIView):

    def get(self, request: Request, channel_id: int):
        filter_like = request.query_params.get('favorite') is not None
        filter_bookmark = request.query_params.get('bookmark') is not None
        paginator = BasePageNumberPagination()
        query_set = get_all_articles_by_channel_id(user=request.user,
                                                   channel_id=channel_id,
                                                   favorite=filter_like,
                                                   bookmark=filter_bookmark
                                                   )
        result = paginator.paginate_queryset(query_set, request)
        sr = ArticleReadOnlySerializer(result, many=True, request=request)
        return ok(sr.data)


class ToggleFavoriteArticleAPIView(APIView):

    def put(self, request: Request, article_id: int):
        ar = toggle_article_favorite_by_article_id(user=request.user, article_id=article_id)
        sr = ArticleReadOnlySerializer(ar)
        return ok(sr.data)


class ToggleBookmarkArticleAPIView(APIView):
    def put(self, request: Request, article_id: int):
        ar = toggle_article_bookmark_by_article_id(user=request.user, article_id=article_id)
        sr = ArticleReadOnlySerializer(ar)
        return ok(sr.data)
