from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, UserForm, ProfileForm
from accounts.models import Profile
from datetime import datetime


# Create your views here.
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out.')
    return redirect(reverse('index'))


def login(request):
    """Render login page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in")
                return redirect(reverse('index'))
            else:
                login_form.add_error(None, "Username/email and password not valid.")
    else:
        login_form = UserLoginForm()

    return render(request, 'login.html', {"login_form": login_form})


def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        return redirect(reverse('index'))

    if request.method == "POST":
        registration_form = UserRegistrationFrom(request.POST)
        if registration_form.is_valid():
            registration_form.save()
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])
            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully registered.")
                return redirect(reverse('index'))
            else:
                messages.error(request, 'Unable to register your account at this time')

    else:
        registration_form = UserRegistrationFrom()

    return render(request, 'registration.html', {"registration_form": registration_form})


@login_required
def user_profile(request):
    """The user's profile page"""
    user = User.objects.get(email=request.user.email)
    profile = Profile.objects.get(user=user)
    return render(request, 'profile.html', {"user": user, "profile": profile})


@login_required
def update_profile(request):
    user = request.user
    profile = request.user.profile
    profile_form = ProfileForm(instance=profile)
    user_form = UserForm(instance=user)

    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('profile'))

    return render(request, "profile_update.html",
                  {'user_form': user_form, 'profile_form': profile_form})
