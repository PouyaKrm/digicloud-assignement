from django.db import models

# Create your models here.
from base_app.models import BaseModel
from users.models import ApplicationUser


class FeedChannel(BaseModel):
    user = models.ForeignKey(ApplicationUser, related_name="user", related_query_name="user", on_delete=models.PROTECT)
    rss_link = models.URLField()
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        unique_together = ["user", "rss_link"]
        ordering = ['-create_date']
        db_table = "feed_channel"


class Feed(BaseModel):
    channel = models.ForeignKey(FeedChannel, related_name="feeds", related_query_name="feeds", on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    link = models.URLField()
    pub_date = models.DateTimeField(null=True, blank=True)
    media_type = models.TextField(null=True, blank=True)
    media_url = models.URLField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    is_favorite = models.BooleanField(default=False)

    class Meta:
        db_table = "feeds"
        ordering = ['-create_date']


