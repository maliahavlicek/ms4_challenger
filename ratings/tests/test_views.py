from django.contrib.auth.models import User
from submissions.models import Entry
from challenges.models import Challenge
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from decimal import *

getcontext().prec = 2


class RatingsTests(APITestCase):
    """
    Test Ratings API
    """

    @classmethod
    def setUpTestData(self):
        # load base 3 products
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

        # create 4 users
        for i in range(1, 5):
            user = User(
                username=f'testing_{i}',
                email=f'testing_{i}@test.com',
                password='Tester_1234!'
            )
            user.save()

        # load challenges from json, assuming user 1 is master
        call_command('loaddata', 'challenges/fixtures/challenges.json', verbosity=0)

        # set up challenge_member relationships
        challenge = Challenge.objects.get(pk=78)
        for i in range(1, 5):
            user = User.objects.get(pk=i)
            challenge.members.add(user)
            submission = Entry.objects.create(
                user=user,
                image_file=f'sumbissions/fixtures/entry_img_{i}.jpg',
                title=f'testing_{i} entry for {challenge.name}',
            )
            challenge.submissions.add(submission)

    def test_rating_submit(self):
        # ensure user can create a rating
        url = reverse('send')
        data = {
            'entry_id': 1,
            'reviewer': 1,
            'rating': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #
        self.assertEqual(response.data, {'trophies': '1.00', 'entry_id': '1'})

    def test_rating_error_if_not_member(self):
        # ensure user can create a rating
        url = reverse('send')
        data = {
            'entry_id': 1,
            'reviewer': 5,
            'rating': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # expect input back if error
        self.assertEqual(response.data, data)

    def test_user_changes_rating(self):
        # ensure user can create change their
        url = reverse('send')
        data = {
            'entry_id': 1,
            'reviewer': 1,
            'rating': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'trophies': '1.00', 'entry_id': '1'})
        # change mind and re-submit
        data = {
            'entry_id': 1,
            'reviewer': 1,
            'rating': 3,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {'trophies': '3.00', 'entry_id': '1'})

    def test_user_aggregate_rating(self):
        # get aggregate once 2 users have rated same entry
        url = reverse('send')
        data = {
            'entry_id': 1,
            'reviewer': 1,
            'rating': 1,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'trophies': '1.00', 'entry_id': '1'})
        # next user submits
        data = {
            'entry_id': 1,
            'reviewer': 2,
            'rating': 2,
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.data, {'trophies': '1.50', 'entry_id': '1'})
