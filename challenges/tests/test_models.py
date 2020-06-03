from django.test import TestCase
from django.utils import timezone

from challenges.models import Challenge
from submissions.models import Entry
from django.core.management import call_command
from datetime import timedelta
import time
from django.contrib.auth.models import User


class TestChallenge(TestCase):
    """
    Test Challenge Model
    """

    @classmethod
    def setUpTestData(cls):
        # set up db, order matters because of Many to Many Relationships

        # set up 3 base products from json
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

    def test_challenge_model(self):
        """
        tests for challenges/models.py
        """
        # pull a closed challenge from DB with 4 members and 4 submissions
        challenge = Challenge.objects.get(pk=78)
        # verify challenge is closed
        self.assertTrue(challenge.is_closed())
        # verify 4 members
        self.assertEquals(len(challenge.get_submissions()), 4)
        # verify 4 submissions
        self.assertEquals(len(challenge.get_submissions()), 4)
        # verify name is in string representation of challenge object
        self.assertTrue(challenge.name in str(challenge))
        # verify image name is in string representation of challenge object
        self.assertTrue(challenge.example_image.name in str(challenge))

        """
        Create a Challenge
        """
        user1 = User.objects.get(pk=1)
        product = user1.profile.get_product_level()
        orig_challenge_count = len(user1.profile.get_owned_challenges())
        self.assertTrue(product.name, 'Free')
        submission_types = ['submission_image']
        if 'submission_audio' in product.features:
            submission_types.append('submission_audio')
        if 'submission_video' in product.features:
            submission_types.append('submission_video')
        challenge = Challenge.objects.create(
            owner=user1,
            name='test challenge 1 name',
            description='test challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now(),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=product.max_members_per_challenge,
            video_time_limit=product.video_length_in_seconds,
            submission_storage_cap=product.max_submission_size_in_MB,
            submission_types=submission_types,
        )
        # verify no submissions
        self.assertEquals(len(challenge.get_submissions()), 0)
        # verify no members
        self.assertEquals(len(challenge.get_members()), 0)
        # verify challenge is opened
        self.assertFalse(challenge.is_closed())
        # verify name is in string representation of challenge object
        self.assertTrue(challenge.name in str(challenge))
        # verify image name is in string representation of challenge object
        self.assertTrue(challenge.example_image.name in str(challenge))
        # verify video name is in string representation of challenge object
        self.assertTrue(str(challenge.example_video) in str(challenge))

        # db may be slow, so let's wait a bit in a controlled manner
        tries = 0
        while tries < 5:
            time.sleep(.5)
            user1 = User.objects.get(pk=1)
            new_count = len(user1.profile.get_owned_challenges())
            tries += 1
            if new_count == orig_challenge_count + 1:
                tries = 5

        # verify owner is as expected
        user1 = User.objects.get(pk=1)
        self.assertEquals(challenge.owner.email, 'testing_1@test.com')
        self.assertEqual(orig_challenge_count + 1, len(user1.profile.get_owned_challenges()))

        """
        Update the challenge
        """
        challenge_id = challenge.id
        vid_name_part = str(challenge.example_video)
        challenge.example_video = ''
        challenge.save()
        challenge = Challenge.objects.get(id=challenge_id)
        # verify video name is in string representation of challenge object
        self.assertFalse(vid_name_part in str(challenge))

        """
        Delete the challenge
        """
        challenge.delete()
        # verify challenge is not in database anymore
        challenge = list(Challenge.objects.filter(id=challenge_id))
        self.assertEquals(len(challenge), 0)
