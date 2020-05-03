from django.db import models

# Create your models here.
from django.db import models
from products.models import ServiceLevel
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from django.core.validators import MaxValueValidator, MinValueValidator

SUBMISSION_TYPE_CHOICES = [('iamge', 'Image'), ('audio', 'audio'), ('video', 'video')]


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
    example_image = models.ImageField(upload_to='challenges/videos', null=True, blank=True)
    example_video = models.FileField(upload_to='challenges/videos', null=True, blank=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    member_limit = models.PositiveIntegerField()
    video_time_limit = models.PositiveIntegerField()
    submission_storage_cap = models.PositiveIntegerField()
    submission_types = MultiSelectField(choices=SUBMISSION_TYPE_CHOICES)
    members = models.ManyToManyField(User,)

