from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Rating(models.Model):
    rating = models.IntegerChoices('rating', 'GOOD OUSTSANDING STELLER')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
