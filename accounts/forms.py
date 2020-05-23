from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.safestring import mark_safe

from .models import Profile, Tag
from datetime import date
from multiselectfield import MultiSelectField



class DateInput(forms.DateInput):
    input_type = 'date'


class UserLoginForm(forms.Form):
    """ Form to be used by login """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email or Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    next = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('next')
            ),
            Submit('submit', 'Login')
        )


class UserRegistrationFrom(UserCreationForm):
    """Form used to register a new user"""
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'you@example.com'
    }))

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'username'
    }))

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    password2 = forms.CharField(
        label="Password Confirmation",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if User.objects.filter(email=email).exclude(username=username):
            raise forms.ValidationError('That email address is already registered.')

        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if password1 != password2:
            raise forms.ValidationError('Passwords must match.')

        if username in password2:
            raise forms.ValidationError('Your username cannot be part of your password.')

        if email in password2:
            raise forms.ValidationError('Your email cannot be part of your password.')

        return password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('password1', css_class='form-group col-md-6 mb-0'),
                Column('password2', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Register')
        )


class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, required=False)
    last_name = forms.CharField(max_length=50, required=False)
    email = forms.EmailField()
    username = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DateInput)
    profile_pic = forms.ImageField(label="Profile Picture")
    tags = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=((c.pk, mark_safe(c.name)) for c in Tag.objects.all()),
        required=False,
        label="Interests")


    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Don't really care if usr is leap year or not, +-2 days does not really matter if usr can sign up or not
        num_years = int((date.today() - birth_date).days / 365)

        # birthdate should be in past
        if birth_date > date.today():
            raise forms.ValidationError('Please enter a valid birth date.')

        # user has to be 10 years or older
        if num_years < 10:
            raise forms.ValidationError('You must be 10 years or older to use this platform.')

        return birth_date

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('profile_pic', css_class='form-group col-md-6 mb-0'),
                HTML(
                    '<div class="form-group col-md-6 mb-0">'
                    '<img class="profile-pic profile-outline"'
                    'src="{{ request.user.profile.profile_pic.url }}"/></div>'
                ),
                css_class='form-row'
            ),
            Row(
                HTML(
                    '<div class="form-group col-md-6 mb-0">'
                    '<div id="div_id_tags" class="form-group">'
                    '<label for="" class="">Interests</label>'
                    '<div class="">'
                    '{% for value, text in profile_form.tags.field.choices %}'
                    '<div class="field multi_select_form_field checkbox_select_multiple">'
                    '<label class="" for="id_tags_{{ forloop.counter0 }}">'
                    '<input type="checkbox" class="" name="tags" id="id_tags_{{ forloop.counter0 }}" value="{{value}}" {% if value in request.user.profile.get_tags_values %} checked="checked"{% endif %}>'
                    '{{ text }}</label>'
                    '</div>'
                    '{% endfor %}'
                    '</div>'
                    '</div>'
                    '</div>'
                ),
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
                css_class='form-row',

            ),
            Submit('submit', 'Save Changes'),
            Submit('cancel', 'Cancel', css_class='btn btn-cancel')
        )

