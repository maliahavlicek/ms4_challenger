from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, ProfileForm, UserUpdateForm
from checkout.models import Order

from django.contrib.auth.models import User


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
            # if no next_page then go to challenges list page as that is the expected highest volume page
            return redirect(reverse('challenges'))
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
                    # if no next_page then go to challenges list page
                    return redirect(reverse('challenges'))
            else:
                login_form.add_error(None, "Username/email and password not valid.")
    else:
        login_form = UserLoginForm(initial={'next': next_page})

    return render(request, 'login.html', {"login_form": login_form})


def registration(request):
    """Render the registration page"""
    if request.user.is_authenticated:
        # logged in users can't go to registration page, send them back to challenges page
        messages.error(request, 'You are already a registered user.')
        return redirect(reverse('challenges'))

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
        if 'cancel' in request.POST:
            return redirect(reverse('profile'))
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('profile'))

    orders = Order.objects.filter(customer=request.user, payment_status='payment_collected').order_by('-date_created')

    return render(request, "profile_update.html", {'profile_form': profile_form, 'order': orders, })


@login_required
def update_user(request):
    """
    Renders user's info as a form to update their information.
    """

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)

        if 'cancel' in request.POST:
            return redirect(reverse('profile'))

        if form.is_valid():
            user = request.user
            username = form.data['username']
            email = form.data['email']
            if User.objects.filter(username=username).exclude(id=user.id).count() == 0 and User.objects.filter(
                    email=email).exclude(id=user.id).count() == 0:
                user = User.objects.get(id=user.id)
                user.username = username
                user.email = email
                user.first_name = form.data['first_name']
                user.last_name = form.data['last_name']
                user.save()
                messages.success(request, f'Your user info has been updated.')
                return redirect('profile')
            else:
                if User.objects.filter(username=username).exclude(id=user.id).count() > 0:
                    form.fields['username'].default_error_messages = {'required': 'That username is already in use.'}
                    form.fields['username'].error_messages = {'required': 'That username is already in use.'}
                    messages.error(request, f'That user name is already in use.')
                if User.objects.filter(email=email).exclude(id=user.id).count() > 0:
                    form.fields['username'].default_error_messages ={'required': 'That email address is already in use.'}
                    form.fields['username'].error_messages ={'required': 'That email address is already in use.'}
                    messages.error(request, f'That email is already in use.')
                return render(request, 'user_update.html', {'form': form})

    else:

        form = UserUpdateForm(instance=request.user)

    return render(request, 'user_update.html', {'form': form})
