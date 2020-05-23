from django.db import models
from ratings.models import Rating
from django.contrib.auth.models import User
from django.db.models import Avg


class Entry(models.Model):
    """
    Model to hold Submission/Entry for a  Challenge
    """
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    image_file = models.FileField(upload_to="submissions/image/", null=True, blank=True)
    audio_file = models.FileField(upload_to="submissions/audio/", null=True, blank=True)
    video_file = models.FileField(upload_to="submissions/video/", null=True, blank=True)
    title = models.CharField(max_length=300)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    ratings = models.ManyToManyField(Rating)

    def get_rating(self):
        """model function to return aggregate average of trophies awarded by peers"""
        try:
            if self.ratings:
                rating = self.ratings.all().aggregate(trophies=Avg('rating'))
                rating = rating['trophies']
            else:
                rating = 0
        except:
            rating = 0
        return rating
