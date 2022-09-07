from django.urls import path

from feed_subscription import views

urlpatterns = [
    path('subscription/', views.ChannelSubscriptionAPI.as_view()),
    path('subscription/<int:subscription_id>/', views.ChannelRetrieveAPI.as_view()),
]
