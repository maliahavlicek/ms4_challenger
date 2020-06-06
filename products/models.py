from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from multiselectfield import MultiSelectField

PRODUCT_INCLUDED_FEATURES_CHOICES = [
    ('group_emails', 'Group Emails'),
    ('peer_ratings', 'Peer Ratings'),
    ('submission_image', 'Share Image Files'),
    ('submission_audio', 'Share Audio Files'),
    ('submission_video', 'Share Video Files'),
    ('accounts_observers', 'Observer Accounts'),
    ('accounts_managers', 'Multiple Manager Accounts'),
]


# Create your models here.
class ServiceLevel(models.Model):
    """
    Products for Challenger App are subscription based, will be expanded for annual and monthly costs in future
    """
    name = models.CharField(max_length=254, default='')
    price = models.DecimalField(max_digits=6, decimal_places=2,
                                validators=[
                                    MinValueValidator(0.00),
                                    MaxValueValidator(1500.00)
                                ],
                                default=10.00)
    features = MultiSelectField(choices=PRODUCT_INCLUDED_FEATURES_CHOICES)
    description = models.TextField(max_length=200)
    max_members_per_challenge = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    max_number_of_challenges = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    video_length_in_seconds = models.PositiveIntegerField(validators=[MaxValueValidator(300)])
    max_submission_size_in_MB = models.PositiveIntegerField(validators=[MaxValueValidator(10000)])
    image = models.ImageField(upload_to='images/products', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_features_display_list(self):
        feature_list = []
        d = dict(PRODUCT_INCLUDED_FEATURES_CHOICES)
        for feature in self.features:
            if feature in d:
                feature_list.append(d[feature])
            else:
                feature_list.append(feature)
        return feature_list
