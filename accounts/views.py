from django.contrib.auth.models import User
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, UserForm, ProfileForm
from accounts.models import Profile


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
                login_form.add_error(None, "user name and password not valid.")
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
    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = User.objects.get(email=request.user.email)
            user.last_name = user_form.data['last_name']
            user.email = user_form.data['email']
            user.first_name = user_form.data['first_name']
            user.save()
            profile = Profile.objects.get(user=user)
            profile.profile_pic = profile_form.data['profile_pic']
            profile.birth_date = profile_form.data['birth_date']
            profile.save()
            messages.success(request, 'Your profile was successfully updated!')
            redirect(reverse('profile'))

    else:
        user = User.objects.get(email=request.user.email)
        profile = Profile.objects.get(user=user)
        user_form = UserForm(initial={
            'last_name': user.last_name,
            'first_name': user.first_name,
            'email': user.email
        })
        profile_form = ProfileForm(initial={
            'profile_pic': profile.profile_pic,
            'birth_date': profile.birth_date,
        })

        return render(request, "profile_update.html",
                      {'user_form': user_form, 'profile_form': profile_form})
