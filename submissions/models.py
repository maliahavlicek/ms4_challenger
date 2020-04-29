from django.db import models
from challenges.models import Challenge
from ratings.models import Rating
from django.contrib.auth.models import User


# Create your models here.
class Submission(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenge_owner')
    file = models.FileField(upload_to="submissions/")
    ratings = models.ManyToManyField(Rating)
