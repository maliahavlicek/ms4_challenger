# Generated by Django 3.0.5 on 2020-05-17 18:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0008_remove_challenge_submissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='challenge',
            name='name',
        ),
    ]
