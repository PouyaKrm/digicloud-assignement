from django.urls import path

from feed_subscription import views
from feed_subscription.views import ArticlesAPIView

urlpatterns = [
    path('channels/', views.ChannelSubscriptionAPI.as_view()),
    path('channels/<int:subscription_id>/', views.ChannelRetrieveAPI.as_view()),
    path('channels/update/', views.UpdateUserChannelsAPIView.as_view()),
    path('channels/<int:channel_id>/articles/', ArticlesAPIView.as_view()),
    path('articles/<int:article_id>/favorite/', views.ToggleFavoriteArticleAPIView.as_view()),
    path('articles/<int:article_id>/bookmark/', views.ToggleBookmarkArticleAPIView.as_view()),
]
