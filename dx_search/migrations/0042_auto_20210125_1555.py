# Generated by Django 2.1.2 on 2021-01-25 15:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0041_auto_20210124_2114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case_set',
            name='create_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 25, 15, 55, 44, 841913), verbose_name='Creation Timestamp'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='IRB_number',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='IRB_number (not required for non-research requests)'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='collection_sheet',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='IRB approved data collection sheet (not required for non-research requests)'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 25, 15, 55, 44, 846277), verbose_name='Request Timestamp'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_type',
            field=models.CharField(choices=[('IRB', 'Research with IRB'), ('Case_Finding', 'Not Research (Case-Findings)')], default='IRB', max_length=20, verbose_name='Request Type'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_password_change',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 25, 15, 55, 44, 840591), verbose_name='Last Password Change'),
        ),
    ]