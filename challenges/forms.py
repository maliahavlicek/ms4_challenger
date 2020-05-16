from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from .models import Challenge
from accounts.forms import DateInput
from datetime import date


class DatetimeInput(forms.DateInput):
    input_type = 'datetime'


class CreateChallengeForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    example_image = forms.ImageField(label="Example Image", required=False)
    example_video = forms.FileField(label="Example Video", required=False)
    members = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Challenge
        fields = [
            'name',
            'description',
            'start_date,'
            'end_date',
            'example_image',
            'example_video',
            'members'
        ]

    def clean_end_date(self):
        """custom validation for end_date"""
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError('End Date must come after Start Date.')

        if end_date < date.today():
            raise forms.ValidationError('End Date cannot be in the past.')

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
            Row(
                HTML('<div class="form-group col-md-12 mb-0"><label>Members</label><div id="member_list"></div></div>'),
                css_class='form-row'),
            Row(
                HTML(
                    '<div class="form-group col-md-12 mb-0"><div class="form-group"><div class id="member_list_errors"><span id="error_member_list"></span></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="first_name" type="text" max_length="50" placeholder="First Name"/></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="last_name" type="text" max_length="50" placeholder="Last Name"/></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-4 mb-0"><div class="form-group"><div class><input class="form-control" id="email" type="email" placeholder="Email"/>'
                     '<span id="error_email"></span></div></div></div>'),
                HTML('<div class="form-group member-entry col-md-2 mb-0"><div class="form-group"><div class><a onclick="add_member();" id="add_member" class="form-control btn btn-primary">Add Member</a></div></div></div>'),
                css_class='form-row'
            ),
            Row(Column('members'), css_class='form-row'),
            Row(HTML(
                '<input type="hidden" id="max_members" value="{{owned_product.max_members_per_challenge}}" />'
            ), css_class='form-row'),
            Submit('submit', 'Create Challenge'),
            Submit('cancel', 'Cancel', css_class='btn-cancel')
        )


class UpdateChallengeForm(CreateChallengeForm):
    """
    Update is basically the Create challenge form with different submit button name
    """
    name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
    example_image = forms.ImageField(label="Example Image", required=False)
    example_video = forms.FileField(label="Example Video", required=False)
    members = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Challenge
        fields = [
            'name',
            'description',
            'start_date,'
            'end_date',
            'example_image',
            'example_video',
            'members'
        ]

    def clean_end_date(self):
        """custom validation for end_date"""
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if end_date < start_date:
            raise forms.ValidationError('End Date must come after Start Date.')

        if end_date < date.today():
            raise forms.ValidationError('End Date cannot be in the past.')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('name', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('example_image', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0"><img class="img-preview" src="{{challenge.example_image.url}}" /></div>'),
                css_class='form-row'
            ),
            Row(
                Column('example_video', css_class='form-group col-md-4 mb-0'),
                HTML(
                    '{%if challenge.example_video %}<div class="form-group col-md-6 mb-0"><video class="vd-preview" controls><source src="{{challenge.example_video.url}}" type= "video/mp4" />Your browser does not support mp4 videos</video></div>{% endif %}'),
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
            Row(
                HTML('<div class="form-group col-md-12 mb-0"><label>Members</label><div id="member_list"></div></div>'),
                css_class='form-row'),
            Row(
                HTML(
                    '<div class="form-group col-md-12 mb-0"><div class="form-group"><div class id="member_list_errors"><span id="error_member_list"></span></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="first_name" type="text" max_length="50" placeholder="First Name"/></div></div></div>'),
                HTML(
                    '<div class="form-group  member-entry col-md-3 mb-0"><div class="form-group"><div class><input class="form-control" id="last_name" type="text" max_length="50" placeholder="Last Name"/></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-4 mb-0"><div class="form-group"><div class><input class="form-control" id="email" type="email" placeholder="Email"/>'
                    '<span id="error_email"></span></div></div></div>'),
                HTML(
                    '<div class="form-group member-entry col-md-2 mb-0"><div class="form-group"><div class><a onclick="add_member();" id="add_member" class="form-control btn btn-primary">Add Member</a></div></div></div>'),
                css_class='form-row'
            ),
            Row(HTML(
                '<input type="hidden" id="max_members" value="{{owned_product.max_members_per_challenge}}" />'
            ), css_class='form-row'),
            Row(Column('members'), css_class='form-row'),
            Submit('submit', 'Save Changes'),
            Submit('cancel', 'Cancel', css_class='btn btn-cancel')
        )
