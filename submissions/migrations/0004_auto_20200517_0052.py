# Generated by Django 3.0.5 on 2020-05-17 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submissions', '0003_auto_20200517_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='submissions/audio/'),
        ),
        migrations.AddField(
            model_name='submission',
            name='video_file',
            field=models.FileField(blank=True, null=True, upload_to='submissions/video/'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='image_file',
            field=models.FileField(upload_to='submissions/image/'),
        ),
    ]
