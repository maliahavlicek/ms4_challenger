from django import forms
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





if input.isnumeric()