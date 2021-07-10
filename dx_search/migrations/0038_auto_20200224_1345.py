# Generated by Django 2.1.2 on 2020-02-24 13:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0037_auto_20200103_2346'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='research_status',
            new_name='analyst_status',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_search',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='role',
        ),
        migrations.AddField(
            model_name='profile',
            name='last_password_change',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 13, 44, 58, 332407), verbose_name='Last Password Change'),
        ),
        migrations.AlterField(
            model_name='case_set',
            name='create_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 13, 44, 58, 333806), verbose_name='Creation Timestamp'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 24, 13, 44, 58, 335895), verbose_name='Request Timestamp'),
        ),
    ]