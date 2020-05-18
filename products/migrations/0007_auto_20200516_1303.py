# Generated by Django 3.0.5 on 2020-05-16 19:03

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200502_1808'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicelevel',
            name='features',
            field=multiselectfield.db.fields.MultiSelectField(choices=[('group_emails', 'Group Emails'), ('peer_ratings', 'Peer Ratings'), ('submission_image', 'Share Image Files'), ('submission_audio', 'Share Audio Files'), ('submission_video', 'Share Video Files'), ('accounts_observers', 'Observer Accounts'), ('accounts_managers', 'Multiple Manger Accounts')], max_length=113),
        ),
    ]