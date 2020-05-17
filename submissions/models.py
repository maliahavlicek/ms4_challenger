from django.db import models
from ratings.models import Rating
from django.contrib.auth.models import User


# Create your models here.
class Submission(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_owner')
    image_file = models.FileField(upload_to="submissions/image/", null=True, blank=True)
    audio_file = models.FileField(upload_to="submissions/audio/", null=True, blank=True)
    video_file = models.FileField(upload_to="submissions/video/", null=True, blank=True)
    ratings = models.ManyToManyField(Rating)
