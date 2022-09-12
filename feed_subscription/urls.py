from django.urls import path

from feed_subscription import views
from feed_subscription.views import ArticlesAPIView

urlpatterns = [
    path('channels/', views.ChannelSubscriptionAPI.as_view(), name="user_channels"),
    path('channels/<int:subscription_id>/', views.ChannelRetrieveAPI.as_view(), name="retrieve_channel"),
    path('channels/update/', views.UpdateUserChannelsAPIView.as_view(), name="user_channels_update"),
    path('channels/<int:channel_id>/articles/', ArticlesAPIView.as_view(), name="articles"),
    path('articles/<int:article_id>/favorite/', views.ToggleFavoriteArticleAPIView.as_view(), name="article_favorite"),
    path('articles/<int:article_id>/bookmark/', views.ToggleBookmarkArticleAPIView.as_view(), name="article_bookmark"),
]
