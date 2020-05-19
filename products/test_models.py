from django.test import TestCase
from .models import ServiceLevel


# Create your tests here.

class ProductTests(TestCase):
    """
    Here we'll define the tests that we'll run against our
    Product model
    """

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
