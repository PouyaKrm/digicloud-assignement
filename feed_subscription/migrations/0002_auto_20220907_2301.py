# Generated by Django 3.2 on 2022-09-07 18:31

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed_subscription', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FeedSubscription',
            new_name='FeedChannel',
        ),
        migrations.AlterModelTable(
            name='feedchannel',
            table='feed_channel',
        ),
    ]