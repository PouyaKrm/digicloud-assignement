# Generated by Django 3.2 on 2022-09-09 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed_subscription', '0005_auto_20220908_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedchannel',
            name='last_update',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
