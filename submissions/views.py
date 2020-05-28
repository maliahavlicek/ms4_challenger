from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateEntryForm
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
    if user not in members and challenge.owner != user:
        messages.warning(request, "Only a member or the challenge master can see the submissions to a challenge.")
        return redirect(reverse('challenges'))

    submissions = challenge.get_submissions()
    return render(request, "submissions.html", {
        "challenge": challenge,
        "submissions": submissions,
        "choices": [('1', 'nice'), ('2', 'good'), ('3', 'great')],
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
    form = CreateEntryForm(types, initial={
        'submission_size_limit': challenge.submission_storage_cap,
        'submission_time_limit': challenge.video_time_limit
    })

    # see if user posted something
    if request.method == 'POST':
        # see what type of submission is allowed and set correct form
        form = CreateEntryForm(types, request.POST, request.FILES)
        # see if user is canceling
        if 'cancel' in request.POST:
            return redirect(reverse('challenges'))
        elif form.is_valid():

            # create entry
            entry = Entry.objects.create(
                user=request.user,
                title=form.data['title'],
            )
            # add in the files that were uploaded by challenge member
            if 'video_file' in request.FILES:
                entry.video_file = request.FILES['video_file']
            if 'audio_file' in request.FILES:
                entry.audio_file = request.FILES['audio_file']
            if 'image_file' in request.FILES:
                entry.image_file = request.FILES['image_file']
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

    # see what type of submission is allowed and choose correct form and preload expect file(s)
    types = challenge.submission_types
    initial = {
        'title': entry.title,
        'submission_size_limit': challenge.submission_storage_cap,
        'submission_time_limit': challenge.video_time_limit
    }

    if 'VIDEO' in (name.upper() for name in types):
        # video file is an option for an entries, but when updating, it's not going to be in the form unless user is changing it out, restore to original if not in request
        if entry.video_file and 'video_file' not in request.FILES.keys() and entry.video_file.file:
            request.FILES.appendlist('video_file', entry.video_file.file)
            initial['video_file'] = entry.video_file
    if 'AUDIO' in (name.upper() for name in types):
        # audio_file is an option when updating, but it's not going to be in the form unless user is changing it out, restore to original if not in request
        if entry.audio_file and 'audio_file' not in request.FILES.keys() and entry.audio_file.file:
            request.FILES.appendlist('audio_file', entry.audio_file.file)
            initial['audio_file'] = entry.audio_file

    if 'IMAGE' in (name.upper() for name in types):
        # image_file is an option updating, but it's not going to be in the form unless user is changing it out, restore to original if not in request
        if entry.image_file and 'image_file' not in request.FILES.keys() and entry.image_file.file:
            request.FILES.appendlist('image_file', entry.image_file.file)
            initial['image_file'] = entry.image_file
    form = CreateEntryForm(types, initial=initial)

    if request.method == 'POST':
        # see what type of submission is allowed and set correct form
        form = CreateEntryForm(types, request.POST, request.FILES)

        # see if user is canceling
        if 'cancel' in request.POST:
            return redirect(reverse('challenges'))
        elif form.is_valid():
            # update entry
            entry.title = form.data['title']
            entry.date_created = utc.localize(datetime.today())
            # all forms must have at least 1 file uploaded, so add that in
            if 'video_file' in request.FILES:
                entry.video_file = request.FILES['video_file']
            if 'audio_file' in request.FILES:
                entry.audio_file = request.FILES['audio_file']
            if 'image_file' in request.FILES:
                entry.image_file = request.FILES['image_file']
            # save entry so changes commit to DB
            entry.save()

            # send flow to challenges list page
            return redirect(reverse('challenges'))

    return render(request, "update_submission.html", {
        "challenge": challenge,
        "form": form,
        'entry': entry,
    })


@login_required
def delete_submission(request, id):
    """User Deletes a Submission Entry form for a particular challenge"""
    entry = Entry.objects.get(id=id)
    # see if user is owner
    if request.user == entry.user:
        Entry.objects.filter(id=id).delete()
        messages.success(request, "Delete Success: You removed the " + entry.title.title() + " entry.")
    else:
        messages.warning(request, "Delete Denied: You are not the owner of the " + entry.title.title() + " entry.")

    return redirect(reverse('challenges'))
