from django.test import TestCase
from django.utils import timezone

from .forms import CreateChallengeForm, UpdateChallengeForm
from datetime import timedelta
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class TestCreateChallengeForm(TestCase):
    """
    Test CreateChallengeForm
    """

    def test_create_error_start_after_end(self):
        # start date is after end date
        submission_choices = [('image', 'Image')]
        form = CreateChallengeForm(submission_choices,{
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() + timedelta(days=5),
            'end_date': timezone.now(),
            'example_image': 'challenges/fixtures/challenge_vid.mp4',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['end_date'], [u'End Date must come after Start Date.'])

    def test_create_error_past_end_date(self):
        # end date in past error
        submission_choices = [('image', 'Image')]
        form = CreateChallengeForm(submission_choices,{
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': (timezone.now() - timedelta(days=5)),
            'end_date': (timezone.now() - timedelta(days=5)),
            'example_image': 'challenges/fixtures/challenge_vid.mp4',
            'submission_types': ['image'],
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['end_date'], [u'End Date cannot be in the past.'])
        self.assertEqual(form.errors['example_image'], [u'This field is required.'])

    def test_create_valid_no_members(self):
        # valid form
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        img = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        data = {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': (timezone.now() - timedelta(days=5)),
            'end_date': timezone.now(),
            'members': [{"first_name": "first name", "last_name": "last name", "email": "email@email.com", "user": ""}],
            'submission_types': ['image'],
        }
        file_data = {
            'example_image': img
        }
        submission_choices = [('image', 'Image')]
        form = CreateChallengeForm(submission_choices, data, file_data)
        self.assertTrue(form.is_valid())

    def test_create_invalid_bad_file_type(self):
        # bad file type for image
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            img_content = f.read()
        img = SimpleUploadedFile(
            "challenge.mp4", img_content, content_type="video/mp4"
        )

        data = {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() + timedelta(days=5),
            'end_date': timezone.now(),
            'members': '',
        }
        file_data = {
            'example_image': img
        }
        submission_choices = [('image', 'Image')]
        form = CreateChallengeForm(submission_choices, data, file_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['example_image'],
                         [u'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'])


# Create your tests here.
class TestUpdateChallengeForm(TestCase):
    """
    Test Update Challenge Form
    """

    def test_challenge_update_form_bad_date(self):
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        img = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        data = {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() + timedelta(days=5),
            'end_date': timezone.now(),
            'members': [{"first_name": "first name", "last_name": "last name", "email": "email@email.com", "user": ""}],
        }
        file_data = {
            'example_image': img
        }
        form = UpdateChallengeForm(data, file_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['end_date'], [u'End Date must come after Start Date.'])

    def test_create_invalid_bad_file_type(self):
        # bad file type for image
        with open(
                "challenges/fixtures/challenge_vid.mp4",
                "rb",
        ) as f:
            img_content = f.read()
        img = SimpleUploadedFile(
            "challenge.mp4", img_content, content_type="video/mp4"
        )

        data = {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() + timedelta(days=5),
            'end_date': timezone.now(),
            'members': '',
        }
        file_data = {
            'example_image': img
        }
        form = UpdateChallengeForm(data, file_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['example_image'],
                         [u'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'])

    def test_update_error_past_end_date(self):
        # end date in past error
        form = UpdateChallengeForm({
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() - timedelta(days=5),
            'end_date': timezone.now() - timedelta(days=5),
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['end_date'], [u'End Date cannot be in the past.'])
        self.assertEqual(form.errors['example_image'], [u'This field is required.'])

    def test_challenge_update_form_valid(self):
        with open(
                "challenges/fixtures/challenge_img.jpg",
                "rb",
        ) as f:
            img_content = f.read()
        img = SimpleUploadedFile(
            "challenge.jpg", img_content, content_type="image/jpg"
        )

        data = {
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': timezone.now() - timedelta(days=5),
            'end_date': timezone.now(),
            'members': [{"first_name": "first name", "last_name": "last name", "email": "email@email.com", "user": ""}],
        }
        file_data = {
            'example_image': img
        }
        form = UpdateChallengeForm(data, file_data)
        self.assertTrue(form.is_valid())

