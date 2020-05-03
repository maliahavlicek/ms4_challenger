from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from .models import Challenge
from accounts.forms import DateInput


class DatetimeInput(forms.DateInput):
    input_type = 'datetime'


class CreateChallengeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    example_image = forms.ImageField(label="Example Image", required=False)
    example_video = forms.FileField(label="Example Video", required=False)

    class Meta:
        model = Challenge
        fields = (
            'name',
            'description',
            'start_date,'
            'end_date',
            'example_image',
            'example_video',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-4 mb-0'),
                Column('example_image', css_class='form-group col-md-4 mb-0'),
                Column('example_video', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('description', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('start_date', css_class='form-group col-md-6 mb-0'),
                Column('end_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Create Challenge')
        )

