# Generated by Django 3.0.5 on 2020-04-27 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(default='profile1.png', upload_to='images/products'),
        ),
    ]