# Generated by Django 3.0.5 on 2020-05-09 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('challenges', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='challenge',
            name='example_image',
            field=models.ImageField(blank=True, null=True, upload_to='challenges/images'),
        ),
    ]
