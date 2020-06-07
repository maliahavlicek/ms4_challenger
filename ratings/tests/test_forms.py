from django.test import TestCase
from ratings.forms import CreateRatingForm
from django.contrib.auth.models import User
from submissions.models import Entry
from challenges.models import Challenge
from django.core.management import call_command


class TestCreateRatingForm(TestCase):
    """
    Test Create Rating Form
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

    def test_make_payment_form_success(self):
        # ensure success can happen
        form = CreateRatingForm({
            'rating': 3,
            'entry': 1,
            'reviewer': 1,
        })
        self.assertTrue(form.is_valid())