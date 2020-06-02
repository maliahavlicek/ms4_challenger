from django.shortcuts import render, redirect, reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from accounts.forms import UserLoginForm, UserRegistrationFrom, ProfileForm, UserUpdateForm
from checkout.models import Order
from .models import Profile

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
            # login user automatically
            user = auth.authenticate(username=request.POST['username'],
                                     password=request.POST['password1'])

            if user:
                # first time need to create a profile and set up service_level as Free and add order
                product = user.profile.get_product_level()
                profile = Profile.objects.get(user=user)
                profile.product_level = product
                profile.save()

                # create order for free product
                Order.objects.create(
                    user=user,
                    product=product,
                    total=product.price,
                    payment_status='payment_collected',
                )

                # auto login newly created user
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
    orders = Order.objects.filter(user=request.user, payment_status='payment_collected').order_by('-date_created')
    return render(request, 'profile.html', {'orders': orders, })


@login_required
def update_profile(request):
    """Update profile page"""
    profile_form = ProfileForm(instance=request.user.profile)

    if request.method == "POST":
        if 'cancel' in request.POST:
            return redirect(reverse('profile'))
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            # don't stomp on product level, purposely not in form so user can't hack a change
            profile_form.product_level = request.user.profile.get_product_level()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect(reverse('profile'))
        else:
            # use initial to retain user entered values on invalid form
            initial = {}
            if 'profile_pic' in profile_form.cleaned_data:
                initial['profile_pic'] = profile_form.cleaned_data['profile_pic']
            if 'tags' in profile_form.cleaned_data:
                initial['tags'] = profile_form.cleaned_data['tags']
            if 'birth_date' in profile_form.cleaned_data:
                initial['birth_date'] = profile_form.cleaned_data['birth_date']
            profile_form = ProfileForm(request.POST, request.FILES, initial=initial)

    return render(request, "profile_update.html", {'profile_form': profile_form})


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
                    form.fields['username'].default_error_messages = {
                        'required': 'That email address is already in use.'}
                    form.fields['username'].error_messages = {'required': 'That email address is already in use.'}
                    messages.error(request, f'That email is already in use.')
                return render(request, 'user_update.html', {'form': form})

    else:

        form = UserUpdateForm(instance=request.user)

    return render(request, 'user_update.html', {'form': form})
