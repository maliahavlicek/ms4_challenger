from django.shortcuts import render
from .models import Challenge
from django.contrib.auth.decorators import login_required


@login_required
def all_challenges(request):
    """Show Challenges page to user"""
    try:
        owned_challenges = Challenge.objects.get(owner=request.user.id)
    except Challenge.DoesNotExist:
        owned_challenges = []
    try:
        member_challenges = Challenge.objects.get(members=request.user.id)
    except Challenge.DoesNotExist:
        member_challenges = []
    return render(request, "challenges.html", {"owned_challenges": owned_challenges,"member_challenges": member_challenges })
