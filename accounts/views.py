from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, ProfileForm


# Create your views here.
@login_required
def logout(request):
    """Log the user out"""
    auth.logout(request)
    messages.success(request, 'You have successfully been logged out.')
    return redirect(reverse('index'))


def login(request):
    """Render login page"""
    next_page = None
    if request.method == 'GET' and 'next' in request.GET:
        next_page = request.GET['next']
    elif request.method == 'POST' and 'next' in request.POST:
        next_page = request.POST['next']
    if request.user.is_authenticated:
        if next_page:
            # allow next parameter to be used when user attempts to short cut to a login required page
            return redirect(next_page)
        else:
            # if no next_page then go to products list page
            return redirect(reverse('products'))
    if request.method == "POST":
        login_form = UserLoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

            if user:
                auth.login(user=user, request=request)
                messages.success(request, "You have successfully logged in")

                if next_page:
                    # allow next parameter to be used when user attempts to short cut to a login required page
                    return redirect(next_page)
                else:
                    # if no next_page then go to products list page
                    return redirect(reverse('products'))
            else:
                login_form.add_error(None, "Username/email and password not valid.")
    else:
        login_form = UserLoginForm(initial={'next': next_page})

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
    return render(request, 'profile.html')


@login_required
def update_profile(request):
    """Update profile page"""
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('profile'))

    return render(request, "profile_update.html",
                  {'profile_form': profile_form})


