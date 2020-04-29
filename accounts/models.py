from django.db import models
from products.models import ServiceLevel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Tag(models.Model):
    """
    Used to help profile user for newer products or ads
    """
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name


class Profile(models.Model):
    """
    Extend User to have the profile fields and self tagging
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default="profile1.png", upload_to='images/products')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    product_level = models.ForeignKey(ServiceLevel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()