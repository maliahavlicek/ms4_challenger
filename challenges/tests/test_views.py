from datetime import timedelta
from django.test import TestCase, Client, RequestFactory
from with_asserts.mixin import AssertHTMLMixin
from django.contrib.auth.models import User
from django.core.management import call_command
from challenges.views import all_challenges
from challenges.forms import CreateChallengeForm, UpdateChallengeForm
from challenges.models import Challenge
from products.models import ServiceLevel
from checkout.models import Order
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from django.utils import timezone
import lxml.html
import json


class TestAllChallengesView(TestCase):
    # setup objects for testing

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

        # every test needs access to the request factory
        self.factory = RequestFactory()

        # create a users
        for i in range(1, 2):
            User.objects.create_user(
                username=f'testing_{i}',
                email=f'testing_{i}@test.com',
                password='Tester_1234!'
            )
        self.user1 = User.objects.get(username='testing_1')
        # simulate user profile getting setup
        self.user1.profile.get_product_level()
        self.client = Client()

    def test_all_challenges_new_user(self):
        # create  an instance of request by getting the home page
        request = self.factory.get('/')
        # middleware isn't supported so simulate loge din user by setting request.user manually
        request.user = self.user1

        # now go to challenges page
        page = all_challenges(request)
        self.assertTemplateUsed('challenges.html')
        self.assertContains(page, 'You belong to 0 challenges.')
        self.assertContains(page, 'You are the Master of 0')
        self.assertContains(page, '/challenges/create/')


class TestCreateChallengeView(TestCase):
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@email.com', password="testing_1234"
        )
        # tie Free product to user
        self.user.profile.get_product_level()

        self.user2 = User.objects.create_user(
            username='testuser2', email='test2@email.com', password="testing_1234"
        )
        self.user2.profile.get_product_level()
        # simulate ordering 2nd tier product
        product = ServiceLevel.objects.get(pk=2)
        self.user2 = order(product, self.user2)

        self.user3 = User.objects.create_user(
            username='testuser3', email='test3@email.com', password="testing_1234"
        )
        self.user3.profile.get_product_level()
        # simulate ordering 2rd tier product
        product = ServiceLevel.objects.get(pk=3)
        self.user3 = order(product, self.user3)

        # img_file
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

        self.client = Client()

    def test_loaded_template(self):
        self.client.login(username='testuser', password="testing_1234")
        response = self.client.get('/challenges/create/')
        templates = response.templates
        names = get_names(templates)

        self.assertIn('base.html', str(names))
        self.assertIn('navigation.html', str(names))
        self.assertIn('create_challenge.html', str(names))

    def test_form_choices_free_tier(self):
        self.client.login(username='testuser', password="testing_1234")
        response = self.client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)
        choices = form.fields['submission_types'].choices
        self.assertNotIn(('video', 'Video'), choices)
        self.assertNotIn(('audio', 'Audio'), choices)
        self.assertIn(('image', 'Image'), choices)

    def test_form_choices_medium_tier(self):
        self.client.login(username=self.user2.username, password="testing_1234")
        response = self.client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)
        choices = form.fields['submission_types'].choices
        self.assertNotIn(('video', 'Video'), choices)
        self.assertIn(('audio', 'Audio'), choices)
        self.assertIn(('image', 'Image'), choices)

    def test_form_choices_high_tier(self):
        client = Client()
        client.login(username=self.user3.username, password="testing_1234")

        response = client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)
        choices = form.fields['submission_types'].choices
        self.assertIn(('video', 'Video'), choices)
        self.assertIn(('audio', 'Audio'), choices)
        self.assertIn(('image', 'Image'), choices)

    def test_create_free_tier(self):
        self.client.login(username='testuser', password="testing_1234")
        response = self.client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)
        response = self.client.post('/challenges/create/', {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date(),
            'members': [{"first_name": "first name", "last_name": "last name", "email": "email@email.com", "user": ""}],
            'submission_types': ['image'],
            'example_image': self.img_file
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'You are the Master of 1')
        self.assertContains(response, 'Challenge 5 Name')
        self.assertContains(response, "Your challenge: Challenge 5 Name was successfully created.")
        self.assertContains(response, "update your member list if you want people to participate")

    def test_create_medium_tier(self):
        self.client.login(username=self.user2.username, password="testing_1234")
        response = self.client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)

        response = self.client.post('/challenges/create/', {
            'name': 'Challenge Medium name',
            'description': 'Challenge Medium description',
            'start_date': (timezone.now() - timedelta(days=5)).date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"malia.havlicek@gmail.com","user":""}]',
            'submission_types': ['image', 'audio'],
            'example_image': self.img_file,
            'example_video': self.vid_file,
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'You are the Master of 1')
        self.assertContains(response, 'Challenge Medium name')
        self.assertContains(response, "Your challenge: Challenge Medium Name was successfully created")
        self.assertContains(response, "an invite has been sent to the members")

    def test_create_with_auto_create_user(self):
        self.client.login(username=self.user2.username, password="testing_1234")
        response = self.client.get('/challenges/create/')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)

        response = self.client.post('/challenges/create/', {
            'name': 'Challenge Medium name',
            'description': 'Challenge Medium description',
            'start_date': (timezone.now() - timedelta(days=5)).date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"new_user1@test.com","user":""}]',
            'submission_types': ['image', 'audio'],
            'example_image': self.img_file,
            'example_video': '',
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('challenges.html')
        self.assertContains(response, 'You are the Master of 1')
        self.assertContains(response, 'Challenge Medium name')
        self.assertContains(response, "Your challenge: Challenge Medium Name was successfully created")
        self.assertContains(response, "an invite has been sent to the members")
        self.assertEqual(1, User.objects.filter(email='new_user1@test.com').count())


class TestCreateChallengeLimits(TestCase):
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

        # load challenges from json, assuming user 1 is master of 5 challenges [the limit]
        call_command('loaddata', 'challenges/fixtures/challenge_views.json', verbosity=0)

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

    def test_create_get_stopped_cannot_exceed_limit(self):
        # cannot start to add a 6th challenge from get /challenges/create/
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.get('/challenges/create/', follow=True)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response,
                            'You are at your limit for challenges, please delete one before creating a new one')

    def test_create_post_stopped_cannot_exceed_limit(self):
        # cannot start to add a 6th challenge from post /challenges/create/
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.post('/challenges/create/', {
            'name': 'Challenge Medium name',
            'description': 'Challenge Medium description',
            'start_date': (timezone.now() - timedelta(days=5)).date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"malia.havlicek@gmail.com","user":""}]',
            'submission_types': ['image', 'audio'],
            'example_image': self.img_file,
            'example_video': self.vid_file,
        }, follow=True)
        # user redirected to challenges page
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response,
                            'You are at your limit for challenges, please delete one before creating a new one')

        self.assertTemplateUsed('challenges.html')

    def test_create_fails_image_file_too_big(self):
        # cannot create challenge because image file is too large
        self.client.login(username='testuser_2', password="testing_1234")
        user = auth.get_user(self.client)

        # img_file
        with open(
                "challenges/fixtures/image_22MB.png",
                "rb",
        ) as f:
            img_content = f.read()
        img_file = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        response = self.client.post('/challenges/create/', {
            'name': 'Challenge HUGE image File Name',
            'description': 'Challenge HUGE image File description',
            'start_date': (timezone.now() - timedelta(days=5)).date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"malia.havlicek@gmail.com","user":""}]',
            'submission_types': ['image'],
            'example_image': img_file,
        }, follow=True)
        # user stays on page, with error about file size
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('create_challenge.html')
        self.assertContains(response, 'Please keep file size under 10.0 MB.')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)

    def test_create_fails_video_file_too_big(self):
        # cannot create challenge because video file is too large
        self.client.login(username='testuser_2', password="testing_1234")
        user = auth.get_user(self.client)

        # vid_file
        with open(
                "challenges/fixtures/challenge_vid_53MB.mov",
                "rb",
        ) as f:
            vd_content = f.read()
        vid_file = SimpleUploadedFile(
            "challenge.mov", vd_content, content_type="video/quicktime"
        )

        response = self.client.post('/challenges/create/', {
            'name': 'Challenge HUGE image File Name',
            'description': 'Challenge HUGE image File description',
            'start_date': (timezone.now() - timedelta(days=5)).date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"malia.havlicek@gmail.com","user":""}]',
            'submission_types': ['image'],
            'example_image': self.img_file,
            'example_video': vid_file,
        }, follow=True)
        # user stays on page, with error about file size
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('create_challenge.html')
        self.assertContains(response, 'Please keep file size under 50.0 MB.')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)

    def test_delete_allows_to_create(self):
        # verify challenge create can happen if user deletes a challenge
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)

        # delete
        challenge = Challenge.objects.get(pk=1)
        response = self.client.get('/challenges/delete/1/', follow=True)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response,
                            challenge.name.title() + " has been deleted. A cancellation email has been sent to the members.")
        self.assertTemplateUsed('challenges.html')

        # go to create
        response = self.client.get('/challenges/create/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('create_challenge.html')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, CreateChallengeForm)


class TestUpdateChallengeViews(TestCase, AssertHTMLMixin):
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        # create 1 user
        for i in range(1, 2):
            user = User.objects.create_user(
                username=f'testuser_{i}', email=f'testuser_{i}t@email.com', password="testing_1234"
            )
            # tie Free product to each user
            user.profile.get_product_level()

        # load challenges from json, assuming user 1 is master of 5 challenges [the limit]
        call_command('loaddata', 'challenges/fixtures/challenge_views.json', verbosity=0)

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

    def test_update_challenge_prepopulated(self):
        # update challenge form loads with data prepopulated
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.get('/challenges/update/1/', follow=True)
        challenge = Challenge.objects.get(id=1)

        # correct status code, template, form
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('update_challenge.html')
        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEquals(form_type, UpdateChallengeForm)

        # verify population
        self.assertContains(response, challenge.name)
        self.assertContains(response, challenge.example_image.url)
        self.assertContains(response, challenge.description)
        self.assertContains(response, challenge.start_date.strftime('%Y-%m-%d'))
        self.assertContains(response, challenge.end_date.strftime('%Y-%m-%d'))
        for m in challenge.get_members():
            u = User.objects.get(id=m.id)
            self.assertContains(response, u.email)

        for index, t in enumerate(challenge.submission_types):
            with self.assertHTML(response) as html:
                self.assertIsInstance(html, lxml.html.HtmlElement)
            # li in div_id_submissions should match order of challenge.submission_types
            with self.assertHTML(response, '#div_id_submission_types li') as elms:
                self.assertEqual(elms[index].text, t)

    def test_update_challenge_name_only(self):
        # update challenge with just a name change
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        orig = Challenge.objects.get(id=1)
        orig_members = orig.get_members()

        # change name and end date so it's valid
        response = self.client.post('/challenges/update/1/', {
            'name': 'Challenge 1 New Name',
            'description': orig.description,
            'start_date': orig.start_date.date(),
            'end_date': timezone.now().date(),
            'members': members_json_string(orig_members),
            'submission_types': orig.submission_types,
            'example_image': orig.example_image.file,
        }, follow=True)
        # verify successful update and new name is in response
        updated = Challenge.objects.get(id=1)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertContains(response, updated.name.title())
        self.assertTemplateUsed('challenges.html')

        # verify updated challenge is as expected
        self.assertNotEqual(orig.name, updated.name)
        self.assertNotEqual(orig.end_date, updated.end_date)
        self.assertEqual(orig.description, updated.description)
        # due to file storage path differs from json location so just check file size
        self.assertEqual(orig.example_image.file.size, updated.example_image.file.size)
        self.assertEqual(orig.start_date, updated.start_date)
        self.assertEqual(orig.submission_types, updated.submission_types)
        self.assertEqual(members_json_string(orig_members), members_json_string(updated.get_members()))

    def test_update_challenge_change_everything(self):
        # update challenge form loads with data prepopulated
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        orig = Challenge.objects.get(id=1)
        orig_members = orig.get_members()

        # load up new example image
        with open(
                "challenges/fixtures/Paper_Plane-512.png",
                "rb",
        ) as f:
            img_content = f.read()
        img_file = SimpleUploadedFile(
            "plane.png", img_content, content_type="image/png"
        )

        # load up new example video
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            vid_content = f.read()
        vid_file = SimpleUploadedFile(
            "challenge_vid.mp4", vid_content, content_type="video/mp4"
        )

        # change everything but the submission types
        response = self.client.post('/challenges/update/1/', {
            'name': 'Challenge 1 New Name',
            'description': orig.description + " new",
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date(),
            'members': '[{"first_name":"","last_name":"","email":"new_user3@test.com","user":""}]',
            'submission_types': orig.submission_types,
            'example_image': img_file,
            'example_video': vid_file,
        }, follow=True)
        # verify successful update and new name is in response
        updated = Challenge.objects.get(id=1)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertContains(response, updated.name.title())
        self.assertTemplateUsed('challenges.html')

        # verify updated challenge is as expected
        self.assertNotEqual(orig.name, updated.name)
        self.assertNotEqual(orig.end_date, updated.end_date)
        self.assertNotEqual(orig.description, updated.description)
        # due to file storage path differs from json location so just check file size
        self.assertNotEqual(orig.example_image.file.size, updated.example_image.file.size)
        self.assertNotEqual(orig.start_date, updated.start_date)
        self.assertEqual(orig.submission_types, updated.submission_types)
        self.assertNotEqual(members_json_string(orig_members), members_json_string(updated.get_members()))
        self.assertNotEqual(orig.example_video, updated.example_video)

    def test_update_challenge_with_example_vid_change_name(self):
        # update challenge with example video, name only this was giving a 500 error at one point in development
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        orig = Challenge.objects.get(id=5)
        orig_members = orig.get_members()

        # change name and end date so it's valid
        response = self.client.post('/challenges/update/1/', {
            'name': 'Challenge 1 New Name',
            'description': orig.description,
            'start_date': orig.start_date.date(),
            'end_date': timezone.now().date(),
            'members': members_json_string(orig_members),
            'submission_types': orig.submission_types,
            'example_image': orig.example_image.file,
            'example_video': orig.example_video.file,
        }, follow=True)
        # verify successful update and new name is in response
        updated = Challenge.objects.get(id=1)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertContains(response, updated.name.title())
        self.assertTemplateUsed('challenges.html')

        # verify updated challenge is as expected
        self.assertNotEqual(orig.name, updated.name)
        self.assertNotEqual(orig.end_date, updated.end_date)
        self.assertEqual(orig.description, updated.description)
        # due to file storage path differs from json location so just check file size
        self.assertEqual(orig.example_image.file.size, updated.example_image.file.size)
        self.assertEqual(orig.example_video.file.size, updated.example_video.file.size)
        self.assertEqual(orig.submission_types, updated.submission_types)
        self.assertEqual(members_json_string(orig_members), members_json_string(updated.get_members()))


# Helper functions
def get_names(templates):
    names = []
    for t in templates:
        names.append(t.name)
    return names


# simulate an order, pass back user
def order(product, user):
    Order.objects.create(
        user=user,
        product=product,
        total=product.price,
        payment_status='payment_collected'
    )
    # update profile with new product
    profile = Profile.objects.get(user=user)
    profile.product_level = product
    profile.save()
    user = User.objects.get(id=user.id)
    return user


def members_json_string(members):
    #output of create or update is json object stingified
    # ex) '[{"first_name":"","last_name":"","email":"malia.havlicek@gmail.com","user":""}]'
    j_string =[]
    for u in members:
        item = {
            'first_name': u.first_name,
            'last_name': u.last_name,
            'email': u.email,
            'user': ""
        }
        j_string.append(item)
    return json.dumps(j_string)