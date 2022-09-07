from django.contrib import admin

# Register your models here.
from feed_subscription.models import FeedSubscription

admin.site.register(FeedSubscription)
