from django.test import TestCase
from .forms import CreateChallengeForm, UpdateChallengeForm
from datetime import datetime, timedelta, date
from django.core.files.uploadedfile import SimpleUploadedFile


# Create your tests here.
class TestCreateChallengeForm(TestCase):
    """
    Test CreateChallengeForm
    """

    def test_create_error_start_after_end(self):
        # start date is after end date
        form = CreateChallengeForm({
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': (datetime.now() + timedelta(days=5)).date(),
            'end_date': date.today(),
            'example_image': 'challenges/fixtures/challenge_vid.mp4',
        })
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['end_date'], [u'End Date must come after Start Date.'])

    def test_create_error_past_end_date(self):
        # end date in past error
        form = CreateChallengeForm({
            'name': 'Challenge 5 name',
            'description': 'Challenge 5 description',
            'start_date': (datetime.now() - timedelta(days=5)).date(),
            'end_date': (datetime.now() - timedelta(days=5)).date(),
            'example_image': 'challenges/fixtures/challenge_vid.mp4',
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
            'start_date': (datetime.now() - timedelta(days=5)).date(),
            'end_date': date.today(),
            'members': [{"first_name":"first name","last_name":"last name","email":"email@email.com","user":""}],
        }
        file_data = {
            'example_image': img
        }
        form = CreateChallengeForm(data, file_data)
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
            'start_date': (datetime.now() - timedelta(days=5)).date(),
            'end_date': date.today(),
            'members': '',
        }
        file_data = {
            'example_image': img
        }
        form = CreateChallengeForm(data, file_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['example_image'],
                         [u'Upload a valid image. The file you uploaded was either not an image or a corrupted image.'])
