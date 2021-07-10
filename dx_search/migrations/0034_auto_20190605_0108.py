# Generated by Django 2.1.2 on 2019-06-05 01:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0033_auto_20190604_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='download_request',
            name='notes',
            field=models.TextField(default='this is the notes section', verbose_name='Notes'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 6, 5, 1, 8, 21, 542514), verbose_name='Request Timestamp'),
        ),
    ]