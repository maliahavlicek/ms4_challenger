from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import User
from .models import Challenge
from submissions.models import Entry
from django.core.management import call_command
from .views import all_challenges, create_challenge
from .forms import CreateChallengeForm, UpdateChallengeForm
from products.models import ServiceLevel
from checkout.models import Order
from accounts.models import Profile


class TestChallengeViews(TestCase):
    # setup objects for testing

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

        # every test needs access to the request factory
        self.factory = RequestFactory()

        # create 4 users
        for i in range(1, 5):
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
