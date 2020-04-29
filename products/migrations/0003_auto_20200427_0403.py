# Generated by Django 3.0.5 on 2020-04-27 04:03

import django.core.validators
from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0003_auto_20200427_0403'),
        ('products', '0002_auto_20200427_0147'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=254)),
                ('price', models.DecimalField(decimal_places=2, default=10.0, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1500)])),
                ('features', multiselectfield.db.fields.MultiSelectField(choices=[('group_emails', 'Group Emails'), ('peer_ratings', 'Peer Ratings'), ('submission_image', 'Uploading and Sharing Image Files'), ('submission_audio', 'Uploading and Sharing Audio Files'), ('submission_video', 'Uploading and Sharing Video Files'), ('accounts_observers', 'Observer Accounts'), ('accounts_managers', 'Multipler Manger Accounts')], max_length=113)),
                ('description', models.TextField(max_length=200)),
                ('image', models.ImageField(upload_to='images/products')),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]
