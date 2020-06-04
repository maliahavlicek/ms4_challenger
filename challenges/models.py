from django.db import models

# Create your models here.
from django.db import models
from products.models import ServiceLevel
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from submissions.models import Entry
from datetime import datetime, date
import pytz

utc = pytz.UTC

SUBMISSION_TYPE_CHOICES = [('image', 'Image'), ('audio', 'audio'), ('video', 'video')]


class Challenge(models.Model):
    """
    Challenges are associated to the user that creates them and are created within the product level
    of their account profile. If the product that is associated with the account is null.
    Default to Free settings:
       - Price : 0
       - Group Emails - Allowed
       - Peer Ratings - Allowed
       - Uploading Images - Allowed
       - Uploading Audio Files - Not Allowed
       - Uploading Video Files - Not Allowed
       - Observer Accounts - Not Allowed
       - Multiple Manager Accounts - Not Allowed
       - Max members per challenge: 5
       - Max number of challengers: 5
       - Max Video Length: 0
       - Max Submission Size: 500 MB
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    name = models.CharField(max_length=254, default='')
    description = models.TextField(max_length=1000)
    example_image = models.ImageField(upload_to='challenges/images')
    example_video = models.FileField(upload_to='challenges/videos', null=True, blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    member_limit = models.PositiveIntegerField()
    video_time_limit = models.PositiveIntegerField()
    submission_storage_cap = models.PositiveIntegerField()
    submission_types = MultiSelectField(choices=SUBMISSION_TYPE_CHOICES)
    members = models.ManyToManyField(User)
    submissions = models.ManyToManyField(Entry)

    def __str__(self):
        stringy = self.name
        if self.example_image:
            stringy += " - Image: " + str(self.example_image)
        if self.example_video:
            stringy += " - Video: " + str(self.example_video)

        return stringy

    def get_members(self):
        """model function to return list of members"""
        try:
            members = list(self.members.all())
        except:
            members = []
        return members

    def get_submissions(self):
        """model function to return submissions"""
        try:
            submissions = list(self.submissions.all())
        except:
            submissions = []
        return submissions

    def is_closed(self):
        """model function to return if end_date has passed"""
        if self.end_date.date() < utc.localize(datetime.today()).date():
            return True
        else:
            return False


class Member(models.Model):
    """ this model is used via javascript and associated forms, but never entered in the database"""
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.EmailField()
    challenger = models.ForeignKey(Challenge, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.email
