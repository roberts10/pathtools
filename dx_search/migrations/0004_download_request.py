# Generated by Django 2.1.2 on 2019-03-03 20:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dx_search', '0003_auto_20190219_0404'),
    ]

    operations = [
        migrations.CreateModel(
            name='Download_Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=256)),
                ('datetime', models.DateTimeField(default=datetime.datetime(2019, 3, 3, 20, 30, 2, 709635))),
                ('accession_number', models.BooleanField(verbose_name='Accession Number')),
                ('date', models.BooleanField(verbose_name='Accession Date')),
                ('staff', models.BooleanField(verbose_name='Assigned Staff')),
                ('MRN', models.BooleanField(verbose_name='Patient MRN')),
                ('DOB', models.BooleanField(verbose_name='Patient DOB')),
                ('age', models.BooleanField(verbose_name='Patient Age')),
                ('sex', models.BooleanField(verbose_name='Patient Sex')),
                ('first_name', models.BooleanField(default=None, verbose_name='Patient First Name')),
                ('last_name', models.BooleanField(default=None, verbose_name='Patient Last Name')),
                ('text', models.BooleanField(default=None, verbose_name='Diagnostic Text')),
                ('IRB_number', models.CharField(max_length=128)),
            ],
        ),
    ]