from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
# from .forms import CreateSubmissionForm, UpdateSubmissionForm
from django.contrib import messages
from .models import Submission
from challenges.models import Challenge
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives, EmailMessage
from ms4_challenger.settings import EMAIL_HOST_USER, DEFAULT_DOMAIN
from datetime import datetime, date
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


# Create your views here.
@login_required
def create_submission(request, challenge_id):
    """Show Submissions for a particular challenge to user"""
    challenge = Challenge.objects.get(id=challenge_id)
    members = challenge.get_members()
    # need to make sure user belongs to challenge
    user = request.user
    if user not in members:
        messages.warning(request, "Only a member can create an entry for this challenge.")
        return redirect(reverse('challenges'))

    # make sure now falls within submission window (between start and end date)
    if challenge.start_date > utc.localize(datetime.today()):
        messages.warning(request, challenge.name.title() + ": hasn't started yet.")
        return redirect(reverse('challenges'))

    if challenge.end_date < utc.localize(datetime.today()):
        messages.warning(request, challenge.name.title() + ": has already closed.")
        return redirect(reverse('challenges'))

    # make sure user hasn't already submitted something
    submissions = challenge.get_submissions()
    if request.user in submissions:
        messages.warning(request, challenge.name.title() + ": You already submitted an entry to this challenge.")
        return redirect(reverse('challenges'))

    return render(request, "create_submission.html", {
        "challenge": challenge,
    })
