# Generated by Django 2.1.2 on 2019-05-30 23:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0030_auto_20190527_1718'),
    ]

    operations = [
        migrations.AddField(
            model_name='download_request',
            name='new',
            field=models.BooleanField(default=True, verbose_name='New'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='pending',
            field=models.BooleanField(default=False, verbose_name='Pending'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 5, 30, 23, 11, 40, 482522), verbose_name='Request Timestamp'),
        ),
    ]
