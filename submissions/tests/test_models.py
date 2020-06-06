from django.test import TestCase
from django.utils import timezone
from challenges.models import Challenge
from submissions.models import Entry
from django.contrib.auth.models import User
from django.core.management import call_command
from datetime import timedelta


class TestEntryModel(TestCase):
    """
    Test Entry model
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        # create user

        user = User.objects.create_user(
            username="testing_1",
            email='tes1@test.com',
            password='Tester_1234!'
        )
        # simulate ordering free tier product
        user.profile.get_product_level()

        # create challenge

        challenge = Challenge.objects.create(
            owner=user,
            name='test challenge 1 name',
            description='test challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now(),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user.profile.product_level.max_members_per_challenge,
            video_time_limit=user.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user.profile.product_level.max_submission_size_in_MB,
            submission_types='image',

        )

        # set up challenge_member_relationship
        challenge.members.add(user)

    def test_entry_model_creates(self):
        """
        tests for submissions/model.py
        """
        user = User.objects.get(pk=1)

        member_challenges = user.profile.get_member_challenges()

        challenge = member_challenges.first()
        orig_submissions = challenge.submissions.count()

        submission = Entry.objects.create(
            user=user,
            image_file='submissions/fixtures/entry_img_1.jpg',
            title='submission_1',
        )
        challenge.submissions.add(submission)
        challenge = Challenge.objects.get(id=challenge.id)
        self.assertEqual(orig_submissions + 1, challenge.submissions.count())

    def test_entry_rating_initial_zero(self):
        """
        tests for submissions/model.py
        """
        user = User.objects.get(pk=1)

        member_challenges = user.profile.get_member_challenges()

        challenge = member_challenges.first()
        orig_submissions = challenge.submissions.count()

        submission = Entry.objects.create(
            user=user,
            image_file='submissions/fixtures/entry_img_1.jpg',
            title='submission_1',
        )
        challenge.submissions.add(submission)
        challenge = Challenge.objects.get(id=challenge.id)
        self.assertEqual(orig_submissions + 1, challenge.submissions.count())

        self.assertEqual(None, submission.get_rating())


