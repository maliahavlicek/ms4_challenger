from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Rating(models.Model):
    """
    Model to hold Peer Reviews for Challenge Entries
    """
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(3)], null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now_add=True)


# Create your models here.
class RatingInput(models.Model):
    """
    Model to help serialize Peer Reviews Inputs
    """
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(3)], null=True, blank=True)
    reviewer = models.PositiveIntegerField()
    entry_id = models.PositiveIntegerField()


class TotalTrophies(models.Model):
    """
    Model to help serialize ajax response to inputted Ratings
    """
    trophies = models.DecimalField(validators=[MinValueValidator(0), MaxValueValidator(10000)], max_digits=5, decimal_places=2)
    entry_id = models.CharField(max_length=32)