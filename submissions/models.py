from django.db import models
from ratings.models import Rating
from django.contrib.auth.models import User

class Entry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_file = models.FileField(upload_to="submissions/image/", null=True, blank=True)
    audio_file = models.FileField(upload_to="submissions/audio/", null=True, blank=True)
    video_file = models.FileField(upload_to="submissions/video/", null=True, blank=True)
    title = models.CharField(max_length=300)