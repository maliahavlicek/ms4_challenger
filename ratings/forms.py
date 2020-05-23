from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import RatingInput


class CreateRatingForm(forms.Form):
    CHOICES = [('1', 'nice'), ('2', 'good'), ('3', 'great')]
    rating = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES)
    entry = forms.HiddenInput()
    reviewer = forms.HiddenInput()

    class Meta:
        model = RatingInput
        fields = [
            'rating',
            'reviewer',
            'entry',
        ]



