# Generated by Django 3.2 on 2022-09-07 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed_subscription', '0002_auto_20220907_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedchannel',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
