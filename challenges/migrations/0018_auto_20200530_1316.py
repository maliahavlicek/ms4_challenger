# Generated by Django 3.0.5 on 2020-05-30 19:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0017_auto_20200530_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='end_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 30, 13, 16, 0, 283435)),
        ),
        migrations.AlterField(
            model_name='challenge',
            name='start_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 5, 30, 13, 16, 0, 283411)),
        ),
    ]
