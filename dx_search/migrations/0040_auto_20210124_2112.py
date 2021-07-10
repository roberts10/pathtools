# Generated by Django 2.1.2 on 2021-01-24 21:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0039_auto_20200224_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case_set',
            name='create_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 21, 12, 20, 663468), verbose_name='Creation Timestamp'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_datetime',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 21, 12, 20, 665336), verbose_name='Request Timestamp'),
        ),
        migrations.AlterField(
            model_name='download_request',
            name='request_type',
            field=models.CharField(choices=[('IRB', 'Research with IRB'), ('Case_Finding', 'Not Research / Case_Finding')], default='IRB', max_length=20, verbose_name='Request Type'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_password_change',
            field=models.DateTimeField(default=datetime.datetime(2021, 1, 24, 21, 12, 20, 662188), verbose_name='Last Password Change'),
        ),
    ]