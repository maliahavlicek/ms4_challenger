from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateChallengeForm


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
    if request.method == 'POST':
        challenge_form = CreateChallengeForm(request.POST, request.FILES)
        if challenge_form.is_valid():
            # need to stuff into model instead
            return redirect(reverse('challenges'))
    else:
        challenge_form = CreateChallengeForm()

    return render(request, "create_challenge.html", {
        "owned_challenges": owned_challenges,
        'owned_product': owned_product,
        'challenge_form': challenge_form,
    })
