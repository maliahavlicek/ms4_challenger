from django.test import TestCase
from django.utils import timezone
from challenges.models import Challenge
from submissions.models import Entry
import unittest
from django.contrib.auth.models import User
from products.models import ServiceLevel
from django.core.management import call_command

from submissions.forms import CreateEntryForm
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class TestCreateChallengeForm(TestCase):
    """
    Test CreateChallengeForm
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

        # create audio challenge
        challenge1 = Challenge.objects.create(
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
            submission_types='audio',

        )

        # preload some files
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        self.img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        # aud_file
        with open(
                "challenges/fixtures/test_audio.mp3",
                "rb",
        ) as f:
            audio_content = f.read()
        self.aud_file = SimpleUploadedFile(
            "challenge.mp3", audio_content, content_type="audio/mp3"
        )

        # vid_file
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            img_content = f.read()
        self.vid_file = SimpleUploadedFile(
            "challenge.mp4", img_content, content_type="video/mp4"
        )

        # set up challenge_member_relationship
        challenge1.members.add(user)
        self.challenge1 = challenge1

    def test_create_success_audio_file(self):
        types = self.challenge1.submission_types
        form = CreateEntryForm(types,
                               {
                                   'submission_size_limit': self.challenge1.submission_storage_cap,
                                   'submission_time_limit': self.challenge1.video_time_limit,
                                   'title': "title",
                               }, {
                                   'audio_file': self.aud_file,
                               })
        self.assertTrue(form.is_valid())

    def test_create_error_audio_file_content_type(self):
        types = self.challenge1.submission_types
        tmp_file = self.img_file
        tmp_file.name = "test.mp3"
        form = CreateEntryForm(types,
                               {
                                   'submission_size_limit': self.challenge1.submission_storage_cap,
                                   'submission_time_limit': self.challenge1.video_time_limit,
                                   'title': "title",
                               }, {
                                   'audio_file': tmp_file,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['audio_file'][0], 'Unsupported file type, expecting audio/mp3 or audio/mpeg.')

    def test_create_error_audio_file_extension(self):
        types = self.challenge1.submission_types
        tmp_file = self.img_file
        tmp_file.content_type = "audio/mp3"
        form = CreateEntryForm(types,
                               {
                                   'submission_size_limit': self.challenge1.submission_storage_cap,
                                   'submission_time_limit': self.challenge1.video_time_limit,
                                   'title': "title",
                               }, {
                                   'audio_file': tmp_file,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['audio_file'][0], 'Unacceptable file extension, expecting .mp3')

    def test_create_error_audio_file_size(self):
        types = self.challenge1.submission_types
        with open(
                "submissions/fixtures/entry_large.mp3",
                "rb",
        ) as f:
            audio_content = f.read()
        aud_file = SimpleUploadedFile(
            "challenge.mp3", audio_content, content_type="audio/mp3"
        )
        form = CreateEntryForm(types,
                               {
                                   'submission_size_limit': self.challenge1.submission_storage_cap,
                                   'submission_time_limit': self.challenge1.video_time_limit,
                                   'title': "title",
                               }, {
                                   'audio_file': aud_file,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['audio_file'][0], 'Please keep file size under 5.0 MB. Current size 8.4 MB.')

    def test_create_success_video_file(self):
        form = CreateEntryForm('video',
                               {
                                   'submission_size_limit': 10,
                                   'submission_time_limit': 300,
                                   'title': "title",
                               }, {
                                   'video_file': self.vid_file,
                               })
        self.assertTrue(form.is_valid())

    def test_create_error_video_file_content_type(self):
        temp = self.vid_file
        temp.content_type = "audio/mp3"
        form = CreateEntryForm('video',
                               {
                                   'submission_size_limit': 10,
                                   'submission_time_limit': 300,
                                   'title': "title",
                               }, {
                                   'video_file': temp,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['video_file'][0], 'Unsupported file type, expecting video/mp4 or video/quicktime.')

    def test_create_error_video_file_extension(self):
        temp = self.vid_file
        temp.name = "file.mp3"
        form = CreateEntryForm('video',
                               {
                                   'submission_size_limit': 10,
                                   'submission_time_limit': 300,
                                   'title': "title",
                               }, {
                                   'video_file': temp,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['video_file'][0], 'Unacceptable file extension, expecting .mp4 or .mov')

    def test_create_error_video_file_size(self):
        types = self.challenge1.submission_types
        temp = self.vid_file
        form = CreateEntryForm('video',
                               {
                                   'submission_size_limit': 5,
                                   'submission_time_limit': 300,
                                   'title': "title",
                               }, {
                                   'video_file': temp,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['video_file'][0], 'Please keep file size under 5.0 MB. Current size 6.6 MB.')

    def test_create_success_image_file(self):
        form = CreateEntryForm('image',
                               {
                                   'submission_size_limit': 10,
                                   'submission_time_limit': 300,
                                   'title': "title",
                               }, {
                                   'image_file': self.img_file,
                               })
        self.assertTrue(form.is_valid())

    def test_create_error_image_file_size(self):
        with open(
                "submissions/fixtures/image_5.1_mb.png",
                "rb",
        ) as f:
            img_content = f.read()
        img_file = SimpleUploadedFile(
            "challenge.mp3", img_content, content_type="image/png"
        )
        form = CreateEntryForm('image',
                               {
                                   'submission_size_limit': 5,
                                   'submission_time_limit': 0,
                                   'title': "title",
                               }, {
                                   'image_file': img_file,
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['image_file'][0], 'Please keep file size under 5.0 MB. Current size 5.1 MB.')

    def test_create_error_no_file(self):
        form = CreateEntryForm('image',
                               {
                                   'submission_size_limit': 5,
                                   'submission_time_limit': 0,
                                   'title': "title",
                               })
        self.assertFalse(form.is_valid())
        self.assertTrue(form.errors['__all__'][0], 'You must upload a file for your entry.')
        pass
