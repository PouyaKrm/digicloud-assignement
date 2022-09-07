from django.urls import path

from feed_subscription import views

urlpatterns = [
    path('subscription/', views.FeedSubscriptionAPI.as_view()),
    path('subscription/<int:subscription_id>/', views.FeedSubscriptionRetrieveAPI.as_view()),
]
