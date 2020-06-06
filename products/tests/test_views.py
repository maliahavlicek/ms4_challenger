from django.test import TestCase, Client, RequestFactory
from with_asserts.mixin import AssertHTMLMixin
from django.contrib.auth.models import User
from products.models import ServiceLevel
from checkout.models import Order
from accounts.models import Profile
from django.core.management import call_command


class TestProductsView(TestCase, AssertHTMLMixin):
    # setup objects for testing

    @classmethod
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

    # test that unauthenticated user can get to products page
    def test_get_product_page(self):
        page = self.client.get("/products/")
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed(page, 'products.html')
        # verify Free Product is present and user has checkout button
        self.assertContains(page, '/checkout/1/')
        self.assertContains(page, 'Register')
        self.assertContains(page, 'Login')
        self.assertNotContains(page, 'My Account')
        self.assertNotContains(page, 'Currently Owned')

    def test_user_owns_free(self):
        # logged in user with free product should see mixture of checkout buttons
        self.client.login(username='testuser', password="testing_1234")
        page = self.client.get('/products/')
        # no checkout button for free product
        self.assertContains(page, 'Currently Owned')
        # 2 checkout buttons for medium  and high product
        with self.assertHTML(page, '.btn.btn-default') as elms:
            self.assertEqual(len(elms), 2)

    def test_user_owns_medium(self):
        # logged in user with medium product should see mixture of included, recap and 1 checkout button
        self.client.login(username=self.user2.username, password="testing_1234")
        page = self.client.get('/products/')
        # included text for free
        self.assertContains(page, 'Included with Blast Off')
        # no checkout button for owned product
        self.assertContains(page, 'Currently Owned')
        # 1 checkout buttons for medium  and high product
        with self.assertHTML(page, '.btn.btn-default') as elms:
            self.assertEqual(len(elms), 1)

    def test_user_owns_high(self):
        self.client.login(username=self.user3.username, password="testing_1234")
        page = self.client.get('/products/')
        # included text for free
        self.assertContains(page, 'Included with Interstellar')
        # no checkout button for owned product
        self.assertContains(page, 'Currently Owned')
        # 0 checkout buttons for high product
        self.assertNotContains(page, 'Checkout')


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
