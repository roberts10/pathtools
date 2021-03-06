# Generated by Django 2.1.2 on 2019-08-05 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0035_auto_20190731_0134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download_request',
            name='IRB_number',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='IRB_number (not required for case-finding requests)'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='collection_sheet',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='IRB approved data collection sheet (not required for case-finding requests)'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 5, 15, 53, 20, 718492), verbose_name='Request Timestamp'),
        ),
    ]
