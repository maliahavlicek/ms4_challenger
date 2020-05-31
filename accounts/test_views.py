from django.test import TestCase
from .models import User
from products.models import ServiceLevel
from django.contrib import auth
from .models import Tag
from datetime import datetime, timedelta
import time


class TestAccountViews(TestCase):
    # setup objects for testing

    @classmethod
    def setUp(cls):
        product = ServiceLevel(
            name='Free',
            price=0.00,
            features=['group_emails', 'peer_ratings', 'submission_image'],
            description='Our Free Tier is perfect for a small group that wants to challenge each other. Throw the gauntlet down and see who comes up with the best response.',
            max_members_per_challenge=5,
            max_number_of_challenges=5,
            video_length_in_seconds=0,
            max_submission_size_in_MB=500,
            image='/images/products/hot-air-balloon.png'
        )
        product.save()

        # create a couple of tags
        Tag.objects.create(
            name='Sports',
        )
        Tag.objects.create(
            name='Music',
        )

        User.objects.create(
            username='alreadyUsed',
            email='alreadyUsed@test.com',
            password="testing_1234",
        )

    # test home page can be hit and that user is not logged in
    def test_get_home_page(self):
        page = self.client.get("/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Register')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')

    # test that unauthenticated user can get to products page
    def test_get_product_page(self):
        page = self.client.get("/products/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'products.html')
        # verify Free Product is present and user has checkout button
        self.assertContains(page, '/checkout/1/')

    # test that unauthenticated redirects with expected parameters
    def test_unauthenticated_redirects(self):
        # user is redirected to login before checking out
        page = self.client.get("/checkout/1/")
        self.assertRedirects(page, '/accounts/login/?next=/checkout/1/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # post invalid input and verify next page is still in response and was posted
        page = self.client.post('/accounts/login/?next=/checkout/1/', {
            'email': 'testing_1@test.com',
            'username': 'testing_1',
            'password1': 'test_pass_1',
            'password2': 'test_pass_1',
            'next': '/checkout/1/'
        }, follow=True)
        self.assertEquals(page.wsgi_request.POST['next'], '/checkout/1/')
        self.assertContains(page, '<input type="hidden" name="next" value="/checkout/1/" id="id_next">')

        # has to login before seeing profile
        page = self.client.get("/accounts/profile/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/')

        # has to login before updating profile
        page = self.client.get("/accounts/profile/update/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/update/')

        # has to login before getting to challenges
        page = self.client.get("/challenges/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/challenges/')

    # test unauthenticated user can access key pages
    def test_authenticated_redirects(self):
        # first register a user with too similar of password, user remains on registration page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'username': 'test_1',
            'password1': 'test_pass_1',
            'password2': 'test_pass_1'
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'registration.html')
        self.assertContains(page, 'The password is too similar to the username')

        # register user with good credentials, user moves to home page
        page = self.client.post('/accounts/register/', {
            'email': 'testing@test.com',
            'username': 'this_is_test_1',
            'password1': 'tester_pw_1',
            'password2': 'tester_pw_1'
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'You have successfully registered.')
        self.assertContains(page, 'Products')
        self.assertContains(page, 'Challenges')
        self.assertContains(page, 'My Account')

        # check user has profile
        user = auth.get_user(self.client)
        self.assertEqual(user.profile.product_level, ServiceLevel.objects.first())

        # login user with email, expectation that they will go to update profile page
        page = self.client.get('/accounts/login/?next=/accounts/profile/update/', {
            'username': 'testing@test.com',
            'password': 'tester_pw_1',
            'next': '/accounts/profile/update/',
        }, follow=True)
        self.assertRedirects(page, '/accounts/profile/update/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertTemplateUsed(page, 'profile_update.html')
        self.assertContains(page, 'Update Profile')
        user = auth.get_user(self.client)
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, 'this_is_test_1')

        # post to profile with too young of birthday
        page = self.client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() - timedelta(days=3000)).date(),
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'You must be 10 years or older to use this platform.')

        # post to profile with future birth date
        page = self.client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() + timedelta(days=3)).date(),
            # {"model": "accounts.tag", "pk": 3, "fields": {"name": "Languages"}},
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'Please enter a valid birth date.')
        self.assertTemplateUsed(page, 'profile_update.html')

        # post to profile with all necessary data
        page = self.client.post('/accounts/profile/update/', {
            'profile_pic': 'accounts/fixtures/profile2.png',
            'birth_date': (datetime.now() - timedelta(days=3653)).date(),
            'tags': [],
        }, follow=True)
        self.assertContains(page, 'Your profile was successfully updated!')

        self.assertTemplateUsed(page, 'profile.html')


        # logout user, should go to home page, no user in session
        page = self.client.post('/accounts/logout/', follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)
        self.assertNotEqual(user.username, 'this_is_test_1')

        # attempt to login with bad password
        page = self.client.post('/accounts/login/', {
            'username': 'testing@test.com',
            'password': 'tester_pw_1111',
        }, follow=True)
        self.assertContains(page, "Username/email and password not valid.")

        # login user with email, no next parameter, expectation is user goes to challenges page
        page = self.client.post('/accounts/login/', {
            'username': 'testing@test.com',
            'password': 'tester_pw_1',
        }, follow=True)

        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertTemplateUsed(page, 'challenges.html')
        self.assertContains(page, 'Challenges')
        self.assertContains(page, 'You have successfully logged in')
        user = auth.get_user(self.client)

        # authenticated user if tries to go to login page goes back to challenges page
        page = self.client.get('/accounts/login/', follow=True)
        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)
        self.assertTemplateUsed(page, 'challenges.html')

        # user that is authenticated tries to go to register page should be redirected to challenges page
        page = self.client.get('/accounts/register/', follow=True)
        self.assertRedirects(page, '/challenges/', status_code=302, target_status_code=200, msg_prefix='',
                             fetch_redirect_response=True)
        self.assertContains(page, 'You are already a registered user')
        self.assertTemplateUsed(page, 'challenges.html')

        # logout
        page = self.client.post('/accounts/logout/', follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'index.html')
        self.assertNotIn('_auth_user_id', self.client.session)

        # post login with a redirect to a next page
        page = self.client.get('/accounts/profile/', follow=True)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        page = self.client.post('/accounts/login/?next=/accounts/profile/', {
            'username': 'testing@test.com',
            'password': 'tester_pw_1',
            'next': '/accounts/profile',
        }, follow=True)
        self.assertTemplateUsed('profile.html')

    def test_update_user(self):
        # user is redirected to login before updating user info
        page = self.client.get("/accounts/user/update/", follow=True)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/user/update/', status_code=302,
                             target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        # register a user
        page = self.client.post('/accounts/register/', {
            'email': 'test1_user_1@test1.com',
            'username': 'username1',
            'password1': 'testing_1234',
            'password2': 'testing_1234',
        }, follow=True)
        # verify user is on expected page
        self.assertTemplateUsed('You have successfully registered.')

        user = auth.get_user(self.client)

        # go to update user page
        page = self.client.get('/accounts/user/update/')

        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        # verify username is on page
        self.assertContains(page, "username1")
        self.assertEqual('username1', user.username)
        # verify email is on page
        self.assertContains(page, "test1_user_1@test1.com")
        self.assertEqual('test1_user_1@test1.com', user.email)

        # update first name
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': user.username,
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        self.assertEqual(page.status_code, 200)

        # verify user goes to profile page
        self.assertTemplateUsed('profile.html')
        self.assertContains(page, 'Account Overview')
        # verify user's first name was updated
        self.assertContains(page, "test1_user_1@test1.com")
        self.assertContains(page, "joe")

        # try to take over AlreadyUser username
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': "alreadyUsed",
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        self.assertContains(page, 'A user with that username already exists.')

        # try to take over AlreadyUser email
        page = self.client.post('/accounts/user/update/', {
            'username': user.username,
            'email': "alreadyUsed@test.com",
            'first_name': "joe",
            'last_name': '',
        }, follow=True)
        # verify user is on expected page
        self.assertTemplateUsed('user_update.html')
        self.assertContains(page, 'Updating User Info')
        self.assertContains(page, 'That email is already in use.')

        # update last name
        page = self.client.post('/accounts/user/update/', {
            'email': user.email,
            'username': user.username,
            'first_name': "joe",
            'last_name': 'cool',
        }, follow=True)
        self.assertEqual(page.status_code, 200)
        # verify user goes to profile page
        self.assertTemplateUsed('profile.html')
        self.assertContains(page, 'Account Overview')
        # verify user's first name was updated
        self.assertContains(page, "test1_user_1@test1.com")
        self.assertContains(page, "joe")
        self.assertContains(page, "cool")
        self.assertContains(page, "username1")

        user = auth.get_user(self.client)
        self.assertEqual('test1_user_1@test1.com', user.email)
        self.assertEqual('username1', user.username)
        self.assertEqual(user.first_name, "joe")
        self.assertEquals(user.last_name, "cool")



