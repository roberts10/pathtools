# Generated by Django 2.1.2 on 2019-03-18 18:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0019_auto_20190318_1841'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='download_request',
            name='datetime',
        ),
        migrations.AddField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 18, 18, 44, 8, 936841), verbose_name='Request Timestamp'),
        ),
    ]
