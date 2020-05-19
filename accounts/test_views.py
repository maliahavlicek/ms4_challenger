from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from .models import Profile, User
from products.models import ServiceLevel
from django.urls import reverse
from django.contrib import auth


class TestAccountViews(TestCase):
    def setUp(self):
        self.client = Client()
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
