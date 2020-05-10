from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateChallengeForm, UpdateChallengeForm, MemberForm, BaseMemberFormSet
from django.contrib import messages
from .models import Challenge
from django.forms import formset_factory
from django.contrib.auth.models import User


@login_required
def all_challenges(request):
    """Show Challenges page to user"""
    owned_product = request.user.profile.get_product_level()
    owned_challenges = request.user.profile.get_owned_challenges()
    member_challenges = request.user.profile.get_member_challenges()
    return render(request, "challenges.html", {
        "owned_challenges": owned_challenges,
        "member_challenges": member_challenges,
        'owned_product': owned_product
    })


@login_required
def create_challenge(request):
    """Create Challenge page"""
    owned_product = request.user.profile.get_product_level()
    owned_challenges = request.user.profile.get_owned_challenges()
    MembersFormset = formset_factory(MemberForm, formset=BaseMemberFormSet, extra=owned_product.max_members_per_challenge)
    ChallengeFormset = formset_factory(CreateChallengeForm)

    if owned_challenges and len(owned_challenges) == owned_product.max_number_of_challenges:
        # check if user is at challenge limit for product_level
        messages.warning(request, "You are at your limit for challenges, please delete one before creating a new one.")
        return redirect(reverse('challenges'))

    elif request.method == 'POST':
        challenge_formset = ChallengeFormset(request.POST, request.FILES, prefix='challenge')
        members_formset = MembersFormset(request.POST, prefix='members')
        if challenge_formset.is_valid() and members_formset.is_valid():
            # create the challenge object
            submission_types = ['submission_image']
            if 'submission_audio' in owned_product.features:
                submission_types.append('submission_audio')
            if 'submission_video' in owned_product.features:
                submission_types.append('submission_video')

            challenge = Challenge.objects.create(
                owner=request.user,
                name=challenge_formset.data['name'],
                description=challenge_formset.data['description'],
                start_date=challenge_formset.data['start_date'],
                end_date=challenge_formset.data['end_date'],
                member_limit=owned_product.max_members_per_challenge,
                video_time_limit=owned_product.video_length_in_seconds,
                submission_storage_cap=owned_product.max_submission_size_in_MB,
                submission_types=submission_types,
            )

            if 'example_image' in request.FILES:
                challenge.example_image = request.FILES['example_image']
            if 'example_video' in request.FILES:
                challenge.example_video = request.FILES['example_video']

            challenge.save()
            # now need to see if we have a member or not, if not create a fakish one
            for item in members_formset:
                user = User.objects.get(email=item.data['member'])

            return redirect(reverse('challenges'))
    else:
        challenge_formset = CreateChallengeForm()
        # need to pull out user's account info and set some defaults for the form
        challenge_formset = ChallengeFormset(prefix='challenge')
        member_formset = MembersFormset(prefix='members')

    return render(request, "create_challenge.html", {
        "owned_challenges": owned_challenges,
        'owned_product': owned_product,
        'challenge_form': challenge_formset,
        'members': member_formset,
    })


@login_required
def delete_challenge(request, id):
    """
    Delete a challenge
    """
    user = request.user
    challenge = Challenge.objects.get(id=id)
    if challenge.owner == user:
        Challenge.objects.filter(id=id).delete()
    else:
        messages.warning(request, "Only the challenge master can delete a challenge.")

    return redirect(reverse('challenges'))


@login_required
def update_challenge(request, id):
    """
    Update a challenge
    """
    user = request.user
    challenge = Challenge.objects.get(id=id)
    if challenge.owner == user:
        # user could have upgraded or downgraded, so when updating, get latest owned product
        owned_product = request.user.profile.get_product_level()
        challenge_form = UpdateChallengeForm(initial={
            'name': challenge.name,
            'description': challenge.description,
            'start_date': challenge.start_date,
            'end_date': challenge.end_date,
            'example_image': challenge.example_image,
            'example_video': challenge.example_video,
        })
        if request.method == 'POST':
            challenge_form = UpdateChallengeForm(request.POST, request.FILES)
            if 'cancel' in  request.POST:
                return redirect(reverse('challenges'))
            elif challenge_form.is_valid():
                challenge.name = challenge_form.data['name']
                challenge.description = challenge_form.data['description']
                challenge.start_date = challenge_form.data['start_date']
                challenge.end_date = challenge_form.data['end_date']
                challenge.member_limit = owned_product.max_members_per_challenge
                challenge.video_time_limit = owned_product.video_length_in_seconds
                challenge.submission_storage_cap = owned_product.max_submission_size_in_MB
                submission_types = ['submission_image']
                if 'submission_audio' in owned_product.features:
                    submission_types.append('submission_audio')
                if 'submission_video' in owned_product.features:
                    submission_types.append('submission_video')
                challenge.submission_types = submission_types

                if 'example_image' in request.FILES:
                    challenge.example_image = request.FILES['example_image']
                if 'example_video' in request.FILES:
                    challenge.example_video = request.FILES['example_video']

                challenge.save()
                return redirect(reverse('challenges'))

        return render(request, "update_challenge.html", {
            'owned_product': owned_product,
            'challenge_form': challenge_form,
            'challenge': challenge,
        })
    else:
        messages.warning(request, "Only the challenge master can update a challenge.")

    return redirect(reverse('challenges'))
