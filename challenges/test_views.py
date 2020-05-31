from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser, User
from .models import Challenge
from submissions.models import Entry
from django.core.management import call_command
from products.models import ServiceLevel
from accounts.models import Tag
from datetime import datetime, timedelta
from home.views import index
from .views import all_challenges


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

    def test_all_challenges(self):
        # create  an instance of request by getting the home page
        request = self.factory.get('/')
        # middleware isn't supported so simulate loge din user by setting request.user manually
        request.user = self.user1

        # now go to challenges page
        page = all_challenges(request)
        self.assertTemplateUsed('challenges.html')
        self.assertContains(page, 'You belong to 0 challenges.')
