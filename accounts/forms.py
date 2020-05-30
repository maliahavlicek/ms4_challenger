from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.safestring import mark_safe

from .models import Profile, Tag
from datetime import date


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

    def clean(self):
        # Make sure email isn't already in system
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).count() > 0:
            self.add_error('email', 'That email address is already registered.')
        # Make sure user name isn't already in system
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            self.add_error('email', 'That username is already registered.')

        # make sure passwords match up and don't contain username or email
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if password1 != password2:
            self.add_error('password2', 'Passwords must match.')

        if username in password2:
            self.add_error('password2', 'Your username cannot be part of your password.')

        if email in password2:
            self.add_error('password2', 'Your email cannot be part of your password.')

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


class ProfileForm(forms.ModelForm):
    """
    Collect Updated Profile Info From User
    """
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

    def clean(self):
        birth_date = self.cleaned_data.get('birth_date')

        # Don't really care if usr is leap year or not, +-2 days does not really matter if usr can sign up or not
        num_years = int((date.today() - birth_date).days / 365)

        # birthdate should be in past
        if birth_date > date.today():
            self.add_error('birth_date', 'Please enter a valid birth date.')

        # user has to be 10 years or older
        if num_years < 10:
            self.add_error('birth_date', 'You must be 10 years or older to use this platform.')

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


class UserUpdateForm(UserChangeForm):
    """ Form to update User info username and email """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]

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
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Save Changes'),
            Submit('cancel', 'Cancel', css_class='btn btn-cancel')
        )
