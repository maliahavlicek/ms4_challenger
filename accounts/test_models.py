from django.test import TestCase
from .models import Profile, User, Tag


class TestTagModel(TestCase):
    """
    test tag model
    """

    def test_create_tag(self):
        # creation test
        item = Tag(name='art')
        item.save()
        self.assertEqual(item.name, 'art')


class TestProfileModel(TestCase):
    """
    Test auto creation of Profile from User
    """

    def test_profile(self):
        # create user
        user = User(
            username='testing',
            email='testing@test.com',
            password='Tester_1234!'
        )
        user.save()
        self.assertEqual(user.username, 'testing')

        # verify that profile was auto created
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, 'testing')

        # verify updating user, updates profile
        user.username = 'updated user'
        user.save()
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user.username, 'updated user')

