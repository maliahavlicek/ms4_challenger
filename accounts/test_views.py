from django.test import TestCase, Client
from django.shortcuts import get_object_or_404
from .models import Profile, User
from products.models import ServiceLevel
from django.urls import reverse


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

    # test that unauthenticated redirects
    def test_unauthenticated_redirects(self):
        # has to login before checking out
        page = self.client.get("/checkout/1/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/checkout/1/')

        # has to login before seeing profile
        page = self.client.get("/accounts/profile/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/')

        # has to login before updating profile
        page = self.client.get("/accounts/profile/update/")
        self.assertEqual(page.status_code, 302)
        self.assertRedirects(page, '/accounts/login/?next=/accounts/profile/update/')

