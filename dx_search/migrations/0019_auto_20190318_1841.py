# Generated by Django 2.1.2 on 2019-03-18 18:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0018_auto_20190316_2331'),
    ]

    operations = [
        migrations.AddField(
            model_name='download_request',
            name='execute_user',
            field=models.CharField(default=False, max_length=256, verbose_name='Executed By'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 3, 18, 18, 41, 0, 13390), verbose_name='Request Timestamp'),
        ),
    ]
