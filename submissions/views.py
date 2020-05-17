from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateFreeEntryForm, CreateBlastOffEntryForm, CreateInterstellarEntryForm
from django.contrib import messages
from .models import Entry
from challenges.models import Challenge
from datetime import datetime
import pytz

utc = pytz.UTC


# Create your views here.
@login_required
def all_submissions(request, challenge_id):
    """Show Submissions for a particular challenge to user"""
    challenge = Challenge.objects.get(id=challenge_id)
    members = challenge.get_members()
    # need to make sure user belongs to challenge
    user = request.user
    if user.pk not in members:
        messages.warning(request, "Only a member or the challenge master can see the submissions to a challenge.")
        return redirect(reverse('challenges'))

    submissions = challenge.get_submissions()
    return render(request, "submissions.html", {
        "challenge": challenge,
        "submissions": submissions,
    })


@login_required
def create_submission(request, challenge_id):
    """Show Submission Entry for a particular challenge to user"""
    challenge = Challenge.objects.get(id=challenge_id)
    members = challenge.get_members()
    # need to make sure user belongs to challenge
    user = request.user

    # see if user already has a submission
    try:
        entry = Entry.objects.get(challenge=challenge, user=request.user)
        messages.warning(request, challenge.name.title() + ": You already submitted an entry to this challenge.")
        return redirect(reverse('challenges'))
    except:
        # do nothing this is what we expect
        pass

    if user not in members:
        messages.warning(request, "Only a member can create an entry for this challenge.")
        return redirect(reverse('challenges'))

    # make sure now falls within submission window (between start and end date)
    if challenge.start_date.date() > utc.localize(datetime.today()).date():
        messages.warning(request, challenge.name.title() + ": hasn't started yet.")
        return redirect(reverse('challenges'))

    if challenge.end_date.date() < utc.localize(datetime.today()).date():
        messages.warning(request, challenge.name.title() + ": has already closed.")
        return redirect(reverse('challenges'))

    # see what type of submission is allowed and choose correct form
    types = challenge.submission_types
    if 'submission_video' in types:
        form = CreateInterstellarEntryForm()
    elif 'submission_audio' in types:
        form = CreateBlastOffEntryForm()
    else:
        form = CreateFreeEntryForm()

    # see if user posted something
    if request.method == 'POST':
        # see what type of submission is allowed and set correct form
        if 'submission_video' in types:
            form = CreateInterstellarEntryForm(request.POST, request.FILES)
        elif 'submission_audio' in types:
            form = CreateBlastOffEntryForm(request.POST, request.FILES)
        else:
            form = CreateFreeEntryForm(request.POST, request.FILES)
        # see if user is canceling
        if 'cancel' in request.POST:
            return redirect(reverse('challenges'))
        elif form.is_valid():
            # create entry
            entry = Entry.objects.create(
                user=request.user,
                title=form.data['title'],
            )
            # all forms must have at least 1 file uploaded, so add that in
            if 'submission_video' in request.FILES:
                entry.submission_video = request.FILES['submission_video']
            if 'submission_audio' in request.FILES:
                entry.submission_audio = request.FILES['submission_audio']
            if 'submission_image' in request.FILES:
                entry.submission_image = request.FILES['submission_image']
            # save entry with file
            entry.save()
            # add submission to challenge
            challenge.submissions.add(entry)

            # send flow to challenges list page
            return redirect(reverse('challenges'))


    return render(request, "create_submission.html", {
        "challenge": challenge,
        "form": form,
    })


@login_required
def update_submission(request, challenge_id):
    """Show Prepopulated Submission Entry form for a particular challenge to user"""
    challenge = Challenge.objects.get(id=challenge_id)
    # see if user already has a submission
    try:
        entry = Entry.objects.get(challenge=challenge, user=request.user)
    except:
        messages.warning(request, "You have not yet submitted an entry for this challenge.")
        return redirect(reverse('challenges'))

    if not entry:
        messages.warning(request, "You have not yet submitted an entry for this challenge.")
        return redirect(reverse('challenges'))

    # make sure now falls within submission window (between start and end date)
    if challenge.start_date.date() > utc.localize(datetime.today()).date():
        messages.warning(request, challenge.name.title() + ": hasn't started yet.")
        return redirect(reverse('challenges'))

    if challenge.end_date.date() < utc.localize(datetime.today()).date():
        messages.warning(request, challenge.name.title() + ": has already closed.")
        return redirect(reverse('challenges'))

    # see what type of submission is allowed and choose correct form
    types = challenge.submission_types
    if 'submission_video' in types:
        form = CreateInterstellarEntryForm()
    elif 'submission_audio' in types:
        form = CreateBlastOffEntryForm()
    else:
        form = CreateFreeEntryForm()

    # see if user posted something
    if request.method == 'POST':
        # see what type of submission is allowed and set correct form
        if 'submission_video' in types:
            form = CreateInterstellarEntryForm(request.POST, request.FILES)
        elif 'submission_audio' in types:
            form = CreateBlastOffEntryForm(request.POST, request.FILES)
        else:
            form = CreateFreeEntryForm(request.POST, request.FILES)
        # see if user is canceling
        if 'cancel' in request.POST:
            return redirect(reverse('challenges'))
        elif form.is_valid():
            # create entry
            entry = Entry.objects.create(
                user=request.user,
                title=form.data['title'],
            )
            # all forms must have at least 1 file uploaded, so add that in
            if 'submission_video' in request.FILES:
                entry.submission_video = request.FILES['submission_video']
            if 'submission_audio' in request.FILES:
                entry.submission_audio = request.FILES['submission_audio']
            if 'submission_image' in request.FILES:
                entry.submission_image = request.FILES['submission_image']
            # save entry with file
            entry.save()
            # add submission to challenge
            challenge.submissions.add(entry)

            # send flow to challenges list page
            return redirect(reverse('challenges'))

    return render(request, "update_submission.html", {
        "challenge": challenge,
        "form": form,
    })
