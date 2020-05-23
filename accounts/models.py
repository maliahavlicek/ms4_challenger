from django.db import models
from products.models import ServiceLevel
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from challenges.models import Challenge


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
    profile_pic = models.ImageField(default="profile1.png", upload_to='images/profiles')
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    tags = models.ManyToManyField(Tag)
    product_level = models.ForeignKey(ServiceLevel, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.email

    def get_owned_challenges(self):
        # get challenges user owns
        try:
            owned_challenges = Challenge.objects.filter(owner=self.user).order_by('-start_date', 'name')
        except Challenge.DoesNotExist:
            owned_challenges = None
        return owned_challenges

    def get_member_challenges(self):
        # get challenges that user is a member of
        try:
            member_challenges = Challenge.objects.filter(members=self.user).order_by('-start_date', 'name')
        except Challenge.DoesNotExist:
            member_challenges = None
        return member_challenges

    def get_product_level(self):
        # get owned product
        if self.product_level:
            owned_product = ServiceLevel.objects.get(name=self.product_level)
        else:
            # default to Free product
            try:
                owned_product = ServiceLevel.objects.get(name='Free')
            except ServiceLevel.DoesNotExist:
                # if no Free product in DB, create it
                owned_product = ServiceLevel.objects.create(
                    name="Free",
                    price="0.00",
                    features="group_emails,peer_ratings,submission_image",
                    description="Our Free Tier is perfect for a small group that wants to challenge each other. Throw the gauntlet down and see who comes up with the best response.",
                    max_members_per_challenge=5,
                    max_number_of_challenges=5,
                    video_length_in_seconds=0,
                    max_submission_size_in_MB=500,
                    image="images/products/hot-air-balloon.png",
                )
        return owned_product

    def get_tags(self):
        """model function to return tags/interests"""
        try:
            tags = list(self.tags.all())
        except:
            tags = []
        return tags

    def get_tags_values(self):
        """model function to return tags/interests"""
        try:
            tags = list(self.tags.all().values('pk'))
            tags = [d['pk'] for d in tags if 'pk' in d]
        except:
            tags = []
        return tags

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()
