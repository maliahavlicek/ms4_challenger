from django import forms
from datetime import datetime

year = int(datetime.now().strftime("%Y"))


class MakePaymentForm(forms.Form):
    """
    Input for Strip Payment Collection
    Default Expiration Year Range to current Year
    """
    MONTH_CHOICES = [(i, i) for i in range(1, 12)]
    YEAR_CHOICES = [(i, i) for i in range(year, year+20)]

    credit_card_number = forms.CharField(label='Credit Card Number', required=False)
    ccv = forms.CharField(label="Security Code", required=False)
    expiry_month = forms.ChoiceField(choices=MONTH_CHOICES, required=False)
    expiry_year = forms.ChoiceField(choices=YEAR_CHOICES, required=False)
    stripe_id = forms.CharField(widget=forms.HiddenInput)

