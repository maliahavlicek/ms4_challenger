# Generated by Django 3.0.5 on 2020-05-17 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0006_entry'),
        ('challenges', '0010_challenge_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='challenge',
            name='submissions',
            field=models.ManyToManyField(to='submissions.Entry'),
        ),
    ]
