from django.test import TestCase
from products.models import ServiceLevel
from django.core.management import call_command


# Create Tests for Product Models

class TestProductModel(TestCase):
    """
    Test Product model
    """

    @classmethod
    def setUp(self):
        # set up 3 base products from json
        call_command('loaddata', 'products/fixtures/servicelevel.json', verbosity=0)

    def test_str(self):
        test_name = ServiceLevel(
            name='A product',
            price=1.00,
            description='Test Product description',
            max_number_of_challenges=10,
            max_members_per_challenge=2,
            video_length_in_seconds=0,
            max_submission_size_in_MB=200,
        )
        self.assertEqual(str(test_name), 'A product')

    def test_get_product_features(self):
        prod = ServiceLevel.objects.get(id=1)
        features = prod.get_features_display_list()
        expected = ['Group Emails', 'Peer Ratings', 'Share Image Files']
        self.assertEquals(len(features), len(expected))

    def test_default_price(self):
        # expect failure if trying to create an order without an owner
        test_name = ServiceLevel(
            name='A product',
            description='Test Product description',
            max_number_of_challenges=10,
            max_members_per_challenge=2,
            video_length_in_seconds=0,
            max_submission_size_in_MB=200,
        )
        test_name.save()
        prod = ServiceLevel.objects.filter(name='A product').first()
        self.assertEqual(prod.price, 10)


