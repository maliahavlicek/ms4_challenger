import unittest
from django.test import TestCase
from django.contrib.auth.models import User
from products.models import ServiceLevel
from checkout.models import Order
from django.core.management import call_command


class TestOrderModel(TestCase):
    """
    Test Order Model
    """

    @classmethod
    def setUpTestData(cls):
        # set up db, order matters because of Many to Many Relationships

        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

        # create 4 users
        for i in range(1, 5):
            user = User(
                username=f'testing_{i}',
                email=f'testing_{i}@test.com',
                password='Tester_1234!'
            )
            user.save()

    @unittest.expectedFailure
    def test_cannot_create_without_user(self):
        # expect failure if trying to create an order without an owner
        product = ServiceLevel.objects.get(pk=1)
        order = Order.objects.create(
            payment_status="payment_collected",
            total=product.price,
            product=product
        )

    def test_order_str_method(self):
        # expect failure if trying to create an order without an owner
        product = ServiceLevel.objects.get(pk=1)
        user = User.objects.get(pk=1)
        order = Order.objects.create(
            payment_status="payment_collected",
            total=product.price,
            product=product,
            user=user,
        )
        self.assertEquals(str(order), user.username + " " + product.name + " @ " + str(product.price))

    def test_order_negative_price_zeros(self):
        # expect failure if trying to create an order without an owner
        product = ServiceLevel.objects.get(pk=1)
        user = User.objects.get(pk=1)
        order = Order.objects.create(
            payment_status="payment_collected",
            total=product.price * -1,
            product=product,
            user=user,
        )
        self.assertEqual(str(order), user.username + " " + product.name + " @ 0.00")

    def test_create(self):
        # expect failure if trying to create an order without an owner
        product = ServiceLevel.objects.get(pk=1)
        user = User.objects.get(pk=1)
        num_orders = Order.objects.filter(user=user).count()
        Order.objects.create(
            payment_status="payment_collected",
            total=product.price,
            product=product,
            user=user,
        )
        user = User.objects.get(pk=1)
        self.assertEqual(num_orders + 1, Order.objects.filter(user=user).count())
