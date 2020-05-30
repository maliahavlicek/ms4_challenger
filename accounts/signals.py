from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


def customer_profile(sender, instance, created, **kwargs):
    """ when a user is created, a customer_profile is auto created"""
    if created:
        group = Group.objects.get(name='profile')
        instance.groups.add(group)
        # need to set up product level
        instance.profile.get_product_level()


post_save.connect(customer_profile, sender=User)
