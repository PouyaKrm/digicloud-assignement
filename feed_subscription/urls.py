from django.urls import path

from feed_subscription import views

urlpatterns = [
    path('channels/', views.ChannelSubscriptionAPI.as_view()),
    path('channels/<int:subscription_id>/', views.ChannelRetrieveAPI.as_view()),
    path('channels/update/', views.UpdateUserChannels.as_view()),
]
