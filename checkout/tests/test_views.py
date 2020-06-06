from django.test import TestCase, Client, RequestFactory
from with_asserts.mixin import AssertHTMLMixin
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.management import call_command
from checkout.models import Order
from checkout.forms import MakePaymentForm
from products.models import ServiceLevel
from django.utils import timezone
import lxml.html
from ms4_challenger.settings import STRIPE_SECRET


class TestCheckoutView(TestCase, AssertHTMLMixin):
    """
    Test MakePayment Form
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', email='test@email.com', password="testing_1234"
        )

        self.year = int(timezone.now().strftime("%Y")) + 1
        self.month = int(timezone.now().strftime("%m"))

        self.client = Client()

    def test_unauthenticated_checkout_redirects(self):
        # user is redirected to login before checking out
        page = self.client.post("/checkout/1/")
        self.assertRedirects(page, '/accounts/login/?next=/checkout/1/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

    def test_checkout_fee_goes_to_profile(self):
        # free product doesn't need to collect payment
        self.client.login(username='testuser', password="testing_1234")
        page = self.client.post("/checkout/1/", follow=True)
        self.assertRedirects(page, '/accounts/profile/', status_code=302, target_status_code=200,
                             msg_prefix='', fetch_redirect_response=True)

        with self.assertHTML(page, '.alert.alert-success.alert-dismissible') as (elm,):
            self.assertIsInstance(elm, lxml.html.HtmlElement)
        self.assertContains(page, 'Your service level has been changed.')

        self.assertContains(page, 'Free')
        order = Order.objects.filter(id=self.user.pk).order_by('-date_created').first()
        self.assertEqual(order.product.name, 'Free')

    def test_checkout_medium_requires_payment(self):
        # free product doesn't need to collect payment
        self.client.login(username='testuser', password="testing_1234")
        page = self.client.post("/checkout/2/", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed('checkout.html')
        form = page.context['payment_form']
        form_type = type(form)
        self.assertEqual(form_type, MakePaymentForm)
        product = ServiceLevel.objects.get(id=2)
        self.assertContains(page, product.name)

    def test_checkout_top_requires_payment(self):
        # free product doesn't need to collect payment
        self.client.login(username='testuser', password="testing_1234")
        page = self.client.post("/checkout/3/", follow=True)
        self.assertEqual(page.status_code, 200)
        self.assertTemplateUsed('checkout.html')
        form = page.context['payment_form']
        form_type = type(form)
        self.assertEqual(form_type, MakePaymentForm)
        product = ServiceLevel.objects.get(id=3)
        self.assertContains(page, product.name)


