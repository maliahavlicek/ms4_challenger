# Generated by Django 3.0.5 on 2020-04-27 01:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('individual', 'Individual'), ('corporate', 'Corporate')], default='individual', max_length=50),
        ),
        migrations.AddField(
            model_name='product',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='price_lifetime',
            field=models.DecimalField(decimal_places=2, default=10.0, max_digits=6, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1500)]),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='images/products'),
        ),
    ]
