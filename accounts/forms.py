from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class DateInput(forms.DateInput):
    input_type = 'date'


class UserLoginForm(forms.Form):
    """ Form to be used by login """
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Email or Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def __init__(self, * args, **kwargs):
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

        if not password1 or not password2:
            raise forms.ValidationError('Please confirm your password')

        if password1 != password2:
            raise forms.ValidationError('Passwords must match')

        return password2

    def __init__(self, * args, **kwargs):
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
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(widget=DateInput)

    class Meta:
        model = Profile
        fields = [
            'profile_pic',
            'birth_date',
            'tags',
        ]
