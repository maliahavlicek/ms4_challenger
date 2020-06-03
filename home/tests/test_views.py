from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.core.management import call_command
from home.views import index


class TestHomeViews(TestCase):
    # setup objects for testing

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

        # every test needs access to the request factory
        self.factory = RequestFactory()

        # create user
        self.user1 = User.objects.create_user(
            username='testing_{1',
            email='testing_1@test.com',
            password='Tester_1234!'
        )

    def test_index_view(self):
        """
        Test authenticated and unauthenticated view of home page
        """
        # create  an instance of request by getting the home page
        request = self.factory.get('/')
        self.assertTemplateUsed('index.html')
        home_page = index(request)
        self.assertContains(home_page, 'Bring the next level of competition')
        # verify has expected unauthenticated navigation
        self.assertContains(home_page, 'Login')
        self.assertContains(home_page, 'Register')
        self.assertNotContains(home_page, 'My Account')

        # middleware isn't supported so  simulate loge din user by setting request.user manually
        request.user = self.user1
        home_page = index(request)
        self.assertTemplateUsed('index.html')
        self.assertNotContains(home_page, 'Login')
        self.assertContains(home_page, 'Challenges')
        self.assertContains(home_page, 'My Account')

    def test_404_view(self):
        """
        Test authenticated and unauthenticated view of home page
        """
        request = self.factory.get('/IdoNotExist/')
        self.assertTemplateUsed('404.html')
