from datetime import timedelta
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.management import call_command
from submissions.forms import CreateEntryForm
from challenges.models import Challenge
from submissions.models import Entry
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from django.urls import reverse
from django.utils import timezone
from submissions.views import create_submission, update_submission, delete_submission


class TestCreateEntryAccess(TestCase):
    """
    Testing Access to Create Submission get method
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 4 users
        for i in range(1, 5):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

        # create a challenge under user2 that's currently open with user 1, no submissions
        user1 = User.objects.get(username='testuser_1')
        user2 = User.objects.get(username='testuser_2')
        challenge1 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 1 name',
            description='test user 2 challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='audio',
        )
        challenge1.members.add(user1)
        self.challenge1 = challenge1

        # create a challenge under user2 that's currently open with user 1, user 1 has submission
        challenge2 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 2 name',
            description='test user 2 challenge 2 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge2.members.add(user1)
        challenge2.members.add(user2)
        self.challenge2 = challenge2

        # create user1 submission to challenge 2
        submission1 = Entry.objects.create(
            user=user1,
            image_file='submissions/fixtures/entry_img_1.jpg',
            title='submission_1',
        )
        challenge2.submissions.add(submission1)
        self.submission1 = submission1

        # create a challenge that has a future start date that user 1 belongs to
        challenge3 = Challenge.objects.create(
            owner=user2,
            name='test user3 challenge 3 name',
            description='test user 3 challenge 3 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=(timezone.now() + timedelta(days=5)),
            end_date=(timezone.now() + timedelta(days=6)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge3.members.add(user1)
        self.challenge3 = challenge3

        # create a challenge that has dates in past that user 1 belongs to
        challenge4 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 4 name',
            description='test user 2 challenge 4 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=(timezone.now() - timedelta(days=5)),
            end_date=(timezone.now() - timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge4.members.add(user1)
        self.challenge4 = challenge4

        # img_file
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        self.img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
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
        self.client = Client()

    def test_create_denied_needs_login(self):
        # have to be logged in to create an entry
        challenge = Challenge.objects.all().first()
        url = reverse(create_submission, args=[challenge.id])
        page = self.client.get(url)
        expected_redirect = '/accounts/login/?next=/submissions/create/' + str(challenge.id) + '/'
        self.assertRedirects(page, expected_redirect)

    def test_create_denied_if_closed(self):
        # can't submit to a challenge if it's ended
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge4
        url = reverse(create_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = challenge.name.title() + ": has already closed."
        self.assertContains(response, expected_msg)

    def test_create_denied_if_future(self):
        # can't submit to a challenge if it's not open yet
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge3
        url = reverse(create_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = challenge.name.title() + ": has not started yet."
        self.assertContains(response, expected_msg)

    def test_create_denied_not_member(self):
        # have to be a member to submit an entry
        self.client.login(username='testuser_2', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge1
        url = reverse(create_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = "Only a member can create an entry for this challenge."
        self.assertContains(response, expected_msg)

    def test_create_denied_if_already_submitted(self):
        # users should be using resubmit not create to update
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge2
        url = reverse(create_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = challenge.name.title() + ": You already submitted an entry to this challenge."
        self.assertContains(response, expected_msg)

    def test_create_success(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge1
        url = reverse(create_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('create_submission.html')
        form = response.context['form']
        form_type = type(form)
        self.assertEqual(form_type, CreateEntryForm)

        # verify form is pre-populated with challenge instructions
        self.assertContains(response, challenge.name.title())
        self.assertContains(response, challenge.example_image.url)
        self.assertContains(response, challenge.description)


class TestCreateEntry(TestCase):
    """
    Testing Access to Create Submission get method
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 2 users
        for i in range(1, 3):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

        # create a challenge that only has image
        user1 = User.objects.get(username='testuser_1')
        user2 = User.objects.get(username='testuser_2')
        challenge1 = Challenge.objects.create(
            owner=user2,
            name='test challenge 1 name',
            description='test challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge1.members.add(user1)
        challenge1.members.add(user2)
        self.challenge1 = challenge1

        # create a challenge that only has audio
        challenge2 = Challenge.objects.create(
            owner=user2,
            name='test challenge 2 name',
            description='test challenge 2 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user1.profile.product_level.max_members_per_challenge,
            video_time_limit=user1.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user1.profile.product_level.max_submission_size_in_MB,
            submission_types='audio',
        )
        challenge2.members.add(user1)
        self.challenge2 = challenge2

        # create a challenge that only has video
        challenge3 = Challenge.objects.create(
            owner=user2,
            name='test challenge 2 name',
            description='test challenge 2 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user1.profile.product_level.max_members_per_challenge,
            video_time_limit=user1.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user1.profile.product_level.max_submission_size_in_MB,
            submission_types='video',
        )
        challenge3.members.add(user1)
        self.challenge3 = challenge3

    def test_create_image_entry(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge1
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        response = self.client.post('/submissions/create/1/', {
            'title': 'image entry name',
            'image_file': img_file,
            'submission_size_limit': self.challenge1.submission_storage_cap,
            'submission_time_limit': self.challenge1.video_time_limit,
        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'image entry name'.title())
        self.assertContains(response, "You added an entry to: " + challenge.name.title())

    def test_create_audio_entry(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge2
        with open(
                "challenges/fixtures/test_audio.mp3",
                "rb",
        ) as f:
            audio_content = f.read()
        aud_file = SimpleUploadedFile(
            "challenge.mp3", audio_content, content_type="audio/mp3"
        )

        response = self.client.post('/submissions/create/2/', {
            'title': 'audio entry name',
            'audio_file': aud_file,
            'submission_size_limit': self.challenge1.submission_storage_cap,
            'submission_time_limit': self.challenge1.video_time_limit,
        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'audio entry name'.title())
        self.assertContains(response, "You added an entry to: " + challenge.name.title())

    def test_create_video_entry(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge3
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            vid_content = f.read()
        vid_file = SimpleUploadedFile(
            "challenge.mp4", vid_content, content_type="video/mp4"
        )

        response = self.client.post('/submissions/create/3/', {
            'title': 'video entry name',
            'video_file': vid_file,
            'submission_size_limit': 7,
            'submission_time_limit': self.challenge1.video_time_limit,
        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'video entry name'.title())
        self.assertContains(response, "You added an entry to: " + challenge.name.title())

    def test_create_delete(self):
        # create an entry then delete it
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge3
        orig_submissions = len(challenge.get_submissions())
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            vid_content = f.read()
        vid_file = SimpleUploadedFile(
            "challenge.mp4", vid_content, content_type="video/mp4"
        )

        response = self.client.post('/submissions/create/3/', {
            'title': 'video entry name',
            'video_file': vid_file,
            'submission_size_limit': 7,
            'submission_time_limit': self.challenge1.video_time_limit,
        }, follow=True)
        # make sure count went up when added
        self.assertEqual(int(orig_submissions + 1), len(challenge.get_submissions()))

        # now delete that entry
        entry = Entry.objects.filter(challenge=challenge, user=user).first()
        url = reverse(delete_submission, args=[entry.id])
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertEqual(orig_submissions, len(challenge.get_submissions()))


class TestUpdateEntryAccess(TestCase):
    """
    Testing Updating Submissions Access
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 4 users
        for i in range(1, 5):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

        # create a challenge under user2 that's currently open with user 1, no submissions
        user1 = User.objects.get(username='testuser_1')
        user2 = User.objects.get(username='testuser_2')
        challenge1 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 1 name',
            description='test user 2 challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=1),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='audio',
        )
        challenge1.members.add(user1)
        self.challenge1 = challenge1

        # create a challenge under user2 that's currently open with user 1, user 1 has submission
        challenge2 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 2 name',
            description='test user 2 challenge 2 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge2.members.add(user1)
        challenge2.members.add(user2)
        self.challenge2 = challenge2

        # create user1 submission to challenge 2
        submission2 = Entry.objects.create(
            user=user1,
            image_file='submissions/fixtures/entry_img_1.jpg',
            title='submission_2',
        )
        challenge2.submissions.add(submission2)
        self.submission2 = submission2

        # create a challenge that has a future start date that user 1 belongs to
        challenge3 = Challenge.objects.create(
            owner=user2,
            name='test user3 challenge 3 name',
            description='test user 3 challenge 3 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=(timezone.now() - timedelta(days=5)),
            end_date=(timezone.now() + timedelta(days=6)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge3.members.add(user1)
        self.challenge3 = challenge3

        # create a challenge that has dates in past that user 1 belongs to with a submission
        challenge4 = Challenge.objects.create(
            owner=user2,
            name='test user 2 challenge 4 name',
            description='test user 2 challenge 4 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=(timezone.now() - timedelta(days=5)),
            end_date=(timezone.now() - timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge4.members.add(user1)
        # create user1 submission to challenge 2
        submission4 = Entry.objects.create(
            user=user1,
            image_file='submissions/fixtures/entry_img_1.jpg',
            title='submission_4',
        )
        challenge4.submissions.add(submission4)
        self.submission4 = submission4
        self.challenge4 = challenge4

        # img_file
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        self.img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
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
        self.client = Client()

    def test_update_denied_needs_login(self):
        # have to be logged in to create an entry
        challenge = Challenge.objects.all().first()
        url = reverse(update_submission, args=[challenge.id])
        page = self.client.get(url)
        expected_redirect = '/accounts/login/?next=/submissions/update/' + str(challenge.id) + '/'
        self.assertRedirects(page, expected_redirect)

    def test_update_denied_if_closed(self):
        # can't submit to a challenge if it's ended
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge4
        url = reverse(update_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = challenge.name.title() + ": has already closed."
        self.assertContains(response, expected_msg)

    def test_update_denied_if_no_submission(self):
        # can't update a entry if no submission
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge3
        url = reverse(update_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = "You have not yet submitted an entry for this challenge."
        self.assertContains(response, expected_msg)

    def test_update_denied_not_member(self):
        # have to be a member to submit an entry
        self.client.login(username='testuser_3', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge1
        url = reverse(update_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        expected_msg = "Only a member can update an entry for this challenge."
        self.assertContains(response, expected_msg)

    def test_update_access_success(self):
        # Update a submission during the proper entry window
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        challenge = self.challenge2
        submission = self.submission2
        url = reverse(update_submission, args=[challenge.id])
        response = self.client.get(url, follow=True)

        # correct status code, template, form, challenge
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('update_submission.html')
        form = response.context['form']
        form_type = type(form)
        self.assertEqual(form_type, CreateEntryForm)

        # verify form recaps challenge instructions
        self.assertContains(response, challenge.name.title())
        self.assertContains(response, challenge.example_image.url)
        self.assertContains(response, challenge.description)

        # verify form is pre-populated with entry values
        submission = self.submission2
        self.assertContains(response, submission.title)
        self.assertContains(response, submission.image_file.url)


class TestUpdateEntry(TestCase):
    """
    Testing Updating Entries
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 2 users
        for i in range(1, 3):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

    def test_update_image_entry_title_only(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)

        challenge = Challenge.objects.create(
            owner=user,
            name='test challenge 1 name',
            description='test challenge 1 description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user.profile.product_level.max_members_per_challenge,
            video_time_limit=user.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge.members.add(user)
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )
        submission1 = Entry.objects.create(
            user=user,
            title='Image Submission',
            image_file=img_file
        )
        challenge.submissions.add(submission1)

        response = self.client.post('/submissions/update/1/', {
            'title': 'New image entry name',
            'submission_size_limit': 5,
            'submission_time_limit': 0,

        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'New image entry name'.title())
        self.assertContains(response, "You updated your entry for: " + challenge.name.title())

    def test_update_audio_entry_title_only(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        # create a challenge that only has audio
        challenge = Challenge.objects.create(
            owner=user,
            name='test audio name',
            description='test audio description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user.profile.product_level.max_members_per_challenge,
            video_time_limit=user.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user.profile.product_level.max_submission_size_in_MB,
            submission_types='audio',
        )
        challenge.members.add(user)

        with open(
                "challenges/fixtures/test_audio.mp3",
                "rb",
        ) as f:
            audio_content = f.read()
        aud_file = SimpleUploadedFile(
            "challenge.mp3", audio_content, content_type="audio/mp3"
        )
        submission = Entry.objects.create(
            user=user,
            title='audio Submission',
            audio_file=aud_file
        )
        challenge.submissions.add(submission)

        response = self.client.post('/submissions/update/1/', {
            'title': 'updated audio entry name',
            'submission_size_limit': 5,
            'submission_time_limit': 30,
        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'updated audio entry name'.title())
        self.assertContains(response, "You updated your entry for: " + challenge.name.title())

    def test_update_video_entry(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)

        # create a challenge that only has video
        challenge = Challenge.objects.create(
            owner=user,
            name='test video name',
            description='test video description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=5),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user.profile.product_level.max_members_per_challenge,
            video_time_limit=user.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user.profile.product_level.max_submission_size_in_MB,
            submission_types='video',
        )
        challenge.members.add(user)

        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            vid_content = f.read()
        vid_file = SimpleUploadedFile(
            "challenge.mp4", vid_content, content_type="video/mp4"
        )
        submission3 = Entry.objects.create(
            user=user,
            title='Video Submission',
            video_file=vid_file
        )
        challenge.submissions.add(submission3)

        response = self.client.post('/submissions/update/1/', {
            'title': 'updated video entry name',
            'submission_size_limit': 7,
            'submission_time_limit': 300,
        }, follow=True)

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'updated video entry name'.title())
        self.assertContains(response, "You updated your entry for: " + challenge.name.title())


class TestAllEntries(TestCase):
    """
    Tests for All Entries View
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 4 users
        for i in range(1, 4):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

        # create a challenge under user2 that's currently open with user 1, no submissions
        user1 = User.objects.get(username='testuser_1')
        user2 = User.objects.get(username='testuser_2')
        user3 = User.objects.get(username='testuser_3')
        challenge1 = Challenge.objects.create(
            owner=user1,
            name='test user 1 owner, user 2 and user 3 as members',
            description='test description',
            example_image="challenges/fixtures/challenge_img.jpg",
            example_video="challenges/fixtures/challenge_vid.mp4",
            start_date=timezone.now() - timedelta(days=1),
            end_date=(timezone.now() + timedelta(days=5)),
            member_limit=user2.profile.product_level.max_members_per_challenge,
            video_time_limit=user2.profile.product_level.video_length_in_seconds,
            submission_storage_cap=user2.profile.product_level.max_submission_size_in_MB,
            submission_types='image',
        )
        challenge1.members.add(user2)
        challenge1.members.add(user3)
        self.challenge1 = challenge1

        submission2 = Entry.objects.create(
            user=user2,
            title='Image Submission for user 2',
            image_file='submissions/fixtures/entry_img_2.jpg'
        )
        challenge1.submissions.add(submission2)

        submission3 = Entry.objects.create(
            user=user3,
            title='Image Submission for user 3',
            image_file='submissions/fixtures/entry_img_3.jpg'
        )
        challenge1.submissions.add(submission3)

    def test_open_owner_can_see_entries(self):
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.get('/submissions/1/', follow=True)
        self.assertTemplateUsed(response, 'submissions.html')
        self.assertContains(response, 'Entries for:')

    def test_open_member_cannot_see_entries(self):
        self.client.login(username='testuser_2', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.get('/submissions/1/', follow=True)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response, 'You will be able to see all entries once the challenge closes.')

    def test_unauthenticated_cannot_see_entries(self):
        # need to be logged in to see all entries page
        response = self.client.get('/submissions/1/', follow=True)
        expected_redirect = '/accounts/login/?next=/submissions/1/'
        self.assertRedirects(response, expected_redirect)



