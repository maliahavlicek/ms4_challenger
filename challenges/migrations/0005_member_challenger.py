# Generated by Django 3.0.5 on 2020-05-10 22:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0004_member'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='challenger',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='challenges.Challenge'),
        ),
    ]
