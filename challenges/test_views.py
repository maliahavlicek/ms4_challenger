from datetime import timedelta

from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from django.core.management import call_command
from .views import all_challenges
from .forms import CreateChallengeForm, UpdateChallengeForm
from products.models import ServiceLevel
from checkout.models import Order
from accounts.models import Profile
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib import auth
from django.utils import timezone


class TestChallengeViews(TestCase):
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


class TestCreateChallenge(TestCase):
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


class TestCreateLimits(TestCase):
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

    def test_create_get_stops_cannot_exceed_limit_stops(self):
        # cannot start to add a 6th challenge from get /challenges/create/
        self.client.login(username='testuser_1', password="testing_1234")
        user = auth.get_user(self.client)
        response = self.client.get('/challenges/create/', follow=True)
        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response,
                            'You are at your limit for challenges, please delete one before creating a new one')

    def create_post_stops_cannot_exceed_limit_stops(self):
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

        self.assertRedirects(response, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertContains(response,
                            'You are at your limit for challenges, please delete one before creating a new one')

        form = response.context['challenge_form']
        form_type = type(form)
        self.assertEqual(form_type, UpdateChallengeForm)


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
