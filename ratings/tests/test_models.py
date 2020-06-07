from django.test import TestCase
from ratings.models import Rating, RatingInput, TotalTrophies
from django.contrib.auth.models import User


# Create Tests for Ratings Models

class TestRatingModel(TestCase):
    """
    Test Rating models
    """

    @classmethod
    def setUp(self):
        # create 4 users
        for i in range(1, 5):
            user = User(
                username=f'testing_{i}',
                email=f'testing_{i}@test.com',
                password='Tester_1234!'
            )
            user.save()
        self.user1 = User.objects.get(username='testing_1')

    def test_rating_str(self):
        # test that rating model string is what you expect
        test_name = Rating(
            reviewer=self.user1,
            rating=3
        )

        self.assertEqual(str(test_name), "{0} by {1}".format(test_name.rating, self.user1.username))

    def test_rating_input_str(self):
        # test that rating input model string is what you expect
        test_name = RatingInput(
            reviewer=self.user1.id,
            rating=3,
            entry_id=1,
        )
        self.assertEqual(str(test_name), str(test_name.rating))

    def test_trophies_str(self):
        # test that rating input model string is what you expect
        test_name = TotalTrophies(
            trophies=2.33,
            entry_id=1,
        )
        self.assertEqual(str(test_name), str(test_name.trophies))
