from django.contrib import admin

# Register your models here.
from feed_subscription.models import FeedChannel, Article


class FeedChannelModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'last_update']
    list_display_links = ['id', 'title', 'user', 'last_update']


class ArticleAdminModel(admin.ModelAdmin):
    list_display = ['title', 'channel']
    list_display_links = ['title', 'channel']


admin.site.register(FeedChannel, FeedChannelModelAdmin)
admin.site.register(Article, ArticleAdminModel)
