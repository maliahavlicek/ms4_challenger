# Generated by Django 3.0.5 on 2020-05-17 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0009_remove_challenge_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='name',
            field=models.CharField(default='', max_length=254),
        ),
    ]