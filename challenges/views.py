from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import CreateChallengeForm, UpdateChallengeForm
from django.contrib import messages
from .models import Challenge
from django.contrib.auth.models import User
import json
from .password import random_string
from django.core.mail import EmailMultiAlternatives, EmailMessage
from ms4_challenger.settings import EMAIL_HOST_USER, DEFAULT_DOMAIN
from datetime import datetime, date
from pytz import timezone


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
    challenge_form = CreateChallengeForm()

    if owned_challenges and len(owned_challenges) == owned_product.max_number_of_challenges:
        # check if user is at challenge limit for product_level
        messages.warning(request, "You are at your limit for challenges, please delete one before creating a new one.")
        return redirect(reverse('challenges'))

    elif request.method == 'POST':
        challenge_form = CreateChallengeForm(request.POST, request.FILES)
        if 'cancel' in request.POST:
            return redirect(reverse('challenges'))
        if challenge_form.is_valid():
            # create the challenge object
            submission_types = ['submission_image']
            if 'submission_audio' in owned_product.features:
                submission_types.append('submission_audio')
            if 'submission_video' in owned_product.features:
                submission_types.append('submission_video')

            challenge = Challenge.objects.create(
                owner=request.user,
                name=challenge_form.data['name'],
                description=challenge_form.data['description'],
                start_date=challenge_form.data['start_date'],
                end_date=challenge_form.data['end_date'],
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
            # see if we have a member or not, if not create a one and flag for special treatment if auto created
            try:
                members = json.loads(challenge_form.data['members'])
            except:
                members = []

            member_status = []
            for member in members:
                user1 = User.objects.filter(email=member['email'])
                if user1:
                    user1 = user1[0]
                    challenge.members.add(user1)
                    member_status.append({
                        'user': user1.pk,
                        'status': 'existing',
                    })
                else:
                    # create a user
                    passwd = random_string(4, 4)
                    user1 = User.objects.create(
                        email=member['email'],
                        username=member['email'],
                        password=passwd,
                        first_name=member['first_name'],
                        last_name=member['last_name'],
                    )

                    challenge.members.add(user1)
                    member_status.append({
                        'user': user1.pk,
                        'status': 'new',
                    })
            # send email to challenge members
            challenge_initial_email(member_status, challenge)
            # let user know the challenge was created
            if len(member_status) > 0:
                messages.success(request,
                                 "Your challenge: " + challenge.name.title + " was successfully created and an invite has been sent to the members.")
            else:
                messages.success(request,
                                 "Your challenge: " + challenge.name.title + " was successfully created. Don't forget to update your member list if you want people to participate.")

            return redirect(reverse('challenges'))
    else:
        # need to pull out user's account info and set some defaults for the form
        challenge_forms = CreateChallengeForm()

    # first time create a challenge
    return render(request, "create_challenge.html", {
        "owned_challenges": owned_challenges,
        'owned_product': owned_product,
        'challenge_form': challenge_form,
    })


@login_required
def delete_challenge(request, id):
    """
    Delete a challenge
    """
    user = request.user
    challenge = Challenge.objects.get(id=id)
    if challenge.owner == user:
        members = []
        message = challenge.name.title() + "Has been deleted. \n\tA cancellation email has been sent to the following users:"
        for member in members:
            members.append({'user': member})
            user1 = User.objects.filter(id=member)
            message += '\t' + user1[0].email
        challenge_canceled_email(members, challenge)
        Challenge.objects.filter(id=id).delete()
        messages.success(request, message)
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
        member_data = list(challenge.members.all().values('email', 'first_name', 'last_name'))
        orig_members = json.dumps(member_data)

        challenge_form = UpdateChallengeForm(initial={
            'name': challenge.name,
            'description': challenge.description,
            'start_date': challenge.start_date,
            'end_date': challenge.end_date,
            'example_image': challenge.example_image,
            'example_video': challenge.example_video,
            'members': orig_members,
        })
        if request.method == 'POST':
            challenge_form = UpdateChallengeForm(request.POST, request.FILES)
            if 'cancel' in request.POST:
                return redirect(reverse('challenges'))
            elif challenge_form.is_valid():
                change_matrix = {}
                if challenge.name != challenge_form.data['name']:
                    challenge.name = challenge_form.data['name']
                    change_matrix['name'] = True
                if challenge.description != challenge_form.data['description']:
                    challenge.description = challenge_form.data['description']
                    change_matrix['description'] = True
                if challenge.start_date.strftime('%Y-%m-%d') != challenge_form.data['start_date']:
                    challenge.start_date = challenge_form.data['start_date']
                    change_matrix['start_date'] = True
                if challenge.end_date.strftime('%Y-%m-%d') != challenge_form.data['end_date']:
                    challenge.end_date = challenge_form.data['end_date']
                    change_matrix['end_date'] = True
                challenge.video_time_limit = owned_product.video_length_in_seconds
                challenge.submission_storage_cap = owned_product.max_submission_size_in_MB
                submission_types = ['submission_image']
                if 'submission_audio' in owned_product.features:
                    submission_types.append('submission_audio')
                if 'submission_video' in owned_product.features:
                    submission_types.append('submission_video')
                challenge.submission_types = submission_types

                if 'example_image' in request.FILES:
                    if challenge.example_image != request.FILES['example_image']:
                        challenge.example_image = request.FILES['example_image']
                        change_matrix['example_image'] = True
                if 'example_video' in request.FILES:
                    if challenge.example_video != request.FILES['example_video']:
                        challenge.example_video = request.FILES['example_video']
                        change_matrix['example_video'] = True

                challenge.save()
                # save and pull item from db because input dates are strings but get updated to datetime objects when saved
                challenge = Challenge.objects.get(id=id)
                # need to email updates to members
                # see if we have a member or not, if not create a one and flag for special treatment if auto created
                try:
                    members = json.loads(challenge_form.data['members'])
                except:
                    members = []

                member_status = []
                for member in members:
                    user1 = User.objects.filter(email=member['email'])
                    if user1:
                        user1 = user1[0]
                        # see if user is in existing member list or new to challenge
                        if not any(d['email'] == member['email'] for d in member_data):
                            status = 'existing'
                            challenge.members.add(user1)
                        else:
                            status = 'existing-already-in-challenge'
                        member_status.append({
                            'user': user1.pk,
                            'status': status,
                        })
                    else:
                        # create a user
                        passwd = random_string(4, 4)
                        user1 = User.objects.create(
                            email=member['email'],
                            username=member['email'],
                            password=passwd,
                            first_name=member['first_name'],
                            last_name=member['last_name'],
                        )

                        challenge.members.add(user1)
                        member_status.append({
                            'user': user1.pk,
                            'status': 'new',
                        })
                # now need to check if any members were dropped
                for old_member in member_data:
                    if not any(d['email'] == old_member['email'] for d in members):
                        user1 = User.objects.filter(email=old_member['email'])
                        member_status.append({
                            'user': user1[0].pk,
                            'status': 'out'
                        })
                        challenge.members.remove(user1[0].pk)
                # send emails to challenge members
                message = challenge_update_email_builder(member_status, challenge, change_matrix)
                messages.success(request, message)
                return redirect(reverse('challenges'))

        return render(request, "update_challenge.html", {
            'owned_product': owned_product,
            'challenge_form': challenge_form,
            'challenge': challenge,
        })
    else:
        messages.warning(request, "Only the challenge master can update a challenge.")

    return redirect(reverse('challenges'))


def challenge_update_email_builder(member_status, challenge, change_matrix):
    """
    Send emails to users when a challenge is updated
    """
    # First loop through member_status to determine what email gets sent to each member
    new_to_challenge = []
    already_in_challenge = []
    out = []
    for member in member_status:
        # if no changes in matrix, that means only members were changed, or user didn't update and clicked save so don't send out.
        if member['status'] == 'existing-already-in-challenge':
            if change_matrix:
                already_in_challenge.append(member)
        elif member['status'] == "out":
            out.append(member)
        else:
            new_to_challenge.append(member)

    if len(already_in_challenge) + len(new_to_challenge) + len(out) == 0:
        message = "You didn't make any updates"
    else:
        message = "The following emails were sent:"
        # Send out email to distinct groups
        if len(already_in_challenge) > 0:
            challenge_update_email(already_in_challenge, challenge, change_matrix)
            message += '\n\tUpdate Challenge To:'
            for member in already_in_challenge:
                user = User.objects.get(pk=member['user'])
                message += '\n\t\t' + user.email
        if len(new_to_challenge) > 0:
            challenge_initial_email(new_to_challenge, challenge)
            message += '\n\tChallenge Invite To:'
            for member in new_to_challenge:
                user = User.objects.get(pk=member['user'])
                message += '\n\t\t' + user.email
        if len(out) > 0:
            challenge_canceled_email(out, challenge)
            message += '\n\tChallenge Cancelled To:'
            for member in out:
                user = User.objects.get(pk=member['user'])
                message += '\n\t\t' + user.email
    return message


def challenge_canceled_email(members, challenge):
    from_email = EMAIL_HOST_USER
    # email subject.
    subject = "Challenge Cancelled: " + challenge.name.title() + " On " + datetime.strftime(challenge.start_date,
                                                                                          '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        subject += " until " + datetime.strftime(challenge.end_date, '%m/%d/%Y')

    # build text version of email body
    msg_text = "Hello!\n\nThe challenge master of " + challenge.name.title() + " has terminated the challenge."
    msg_text += '\n\n\tChallenge Name: ' + challenge.name.title()
    msg_text += '\n\n\tDate: ' + datetime.strftime(challenge.start_date, '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        msg_text += ' until ' + datetime.strftime(challenge.end_date, '%m/%d/%Y')
    msg_text += '\n\n\tDETAILS: ' + challenge.description
    msg_text +="\n\nYour account is still active and you can still set up your own challenges and view other active ones at <" + DEFAULT_DOMAIN + "/challenges/>."
    msg_text += '\n\nHave Fun and Challenger on!'

    # build out HTML version of email body
    msg_html = '<div style="font-size: 16px; width:100%; margin: 20px;"><p>Hello!</p><p>The challenge master of ' + challenge.name.title() + ' has terminated the challenge.</p>'
    msg_html += '<p>Date: ' + datetime.strftime(challenge.start_date, '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        msg_html += ' until ' + datetime.strftime(challenge.end_date, '%m/%d/%Y')

    msg_html += '</p><p>Your account is still active and you can still set up your own challenges and view other active ones at ' + DEFAULT_DOMAIN + "/challenges/.</p>"
    msg_html += '<p>Have Fun and Challenger on!</p>'

    # create list of recipients
    to = []
    for member in members:
        user = User.objects.get(pk=member['user'])
        to.append(user.email)

    # send email out
    msg = EmailMultiAlternatives(subject, msg_text, from_email, to)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
    return True


def challenge_update_email(members, challenge, change_matrix):
    from_email = EMAIL_HOST_USER
    # email subject.
    subject = "Updated Challenge: " + challenge.name.title() + " On " + datetime.strftime(challenge.start_date,
                                                                                          '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        subject += " until " + datetime.strftime(challenge.end_date, '%m/%d/%Y')

    # build text version of email body
    msg_text = "Hello!\n\nThe challenge master of " + challenge.name.title() + " has updated the game plan."
    msg_html = '<div style="font-size: 16px; width:100%; margin: 20px;"><p>Hello!</p><p>The challenge master of ' + challenge.name.title() + ' has updated the game plan.</p>'
    msg_text += '\n\nThe challenge details are below:'
    msg_html += '<p>The updated information is below <span style="color:red; font-weight: bold;">(changes in red)</span></p>'
    msg_text += '\n\n\tChallenge Name: ' + challenge.name.title()
    msg_text += '\n\n\tDate: ' + datetime.strftime(challenge.start_date, '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        msg_text += ' until ' + datetime.strftime(challenge.end_date, '%m/%d/%Y')
    msg_text += '\n\n\tDETAILS: ' + challenge.description
    if challenge.example_image:
        msg_text += '\n\n\tEXAMPLE IMAGE: <' + challenge.example_image.url + ">"
    if challenge.example_video:
        msg_text += '\n\n\tEXAMPLE VIDEO: <' + challenge.example_video.url + ">"
    msg_text += '\n\nFor more details, visit us at <' + DEFAULT_DOMAIN + "/challenges/ and click the submit button for " + challenge.name.title() + ">."
    msg_text += '\n\nHave Fun and Challenger on!'

    # build HTML version of email body
    msg_html += '<ul>Challenge Name: '
    if "name" in change_matrix:
        msg_html += '<strong style="color:red;">' + challenge.name.title() + '</strong>'
    else:
        msg_html += challenge.name.title()
    if "start_date" in change_matrix or "end_date" in change_matrix:
        msg_html += '<li style="color:red"><strong>DATE: </strong>' + datetime.strftime(challenge.start_date,
                                                                                        '%m/%d/%Y')
    else:
        msg_html += '<li><strong>DATE: </strong>' + datetime.strftime(challenge.start_date, '%m/%d/%Y')
    if challenge.start_date != challenge.end_date:
        msg_html += ' until ' + datetime.strftime(challenge.end_date, '%m/%d/%Y')
    msg_html += '</li>'
    if "description" in change_matrix:
        msg_html += '<li style="color:red"><strong>DETAILS: </strong>' + challenge.description + '</li>'
    else:
        msg_html += '<li><strong>DETAILS: </strong>' + challenge.description + '</li>'
    if challenge.example_image:
        if "example_image" in change_matrix:
            msg_html += "<li style='color:red;'><strong>EXAMPLE IMAGE: </strong><div style='height: 150px; width: 150px; margin: 20px auto; display:inline-block; background: url(" + challenge.example_image.url + ");background-size:contain; background-repeat:no-repeat;'></div></li>"
        else:
            msg_html += "<li'><strong>EXAMPLE IMAGE: </strong><div style='height: 150px; width: 150px; margin: 20px auto; display:inline-block; background: url(" + challenge.example_image.url + ");background-size:contain; background-repeat:no-repeat;'></div></li>"
    if challenge.example_video:
        if "example_video" in change_matrix:
            msg_html += "<li style='color:red;'><strong>VIDEO: </strong><video width='400' controls><source src='" + challenge.example_video.url + "' type='video/mp4'>Your browser does not support the video tag./video></li>"
        else:
            msg_html += "<li'><strong>VIDEO: </strong><video width='400' controls><source src='" + challenge.example_video.url + "' type='video/mp4'>Your browser does not support the video tag./video></li>"

    msg_html += '</ul><p>For more details, visit us at ' + DEFAULT_DOMAIN + "/challenges/ and click the submit button for " + challenge.name.title() + ".</p>"
    msg_html += '<p>Have Fun and Challenger on!</p>'

    # create list of recipients
    to = []
    for member in members:
        user = User.objects.get(pk=member['user'])
        to.append(user.email)

    # send email out
    msg = EmailMultiAlternatives(subject, msg_text, from_email, to)
    msg.attach_alternative(msg_html, "text/html")
    msg.send()
    return True


def challenge_initial_email(members, challenge):
    """
    Send email to users inviting them to the challenge
    """
    from_email = EMAIL_HOST_USER

    # new to Challenger Welcome Email for auto created users, send them a welcome message with password [status=new]
    new_subject = "Welcome to Challenger!"
    new_msg_greeting = "Hello!\n\nYou have been declared a member in friendly competition hosted on our website. Since you have not yet been invited to our forum, we have auto created an account for you."
    new_closing = "\n\nDon't worry, you can change your email once you login. The details about the challenge you've been invited to will follow shortly.\n\nHave Fun and Challenger on!"
    to = []
    # loop through members and build list of users to get Join a challege email and send of welcome message
    for member in members:
        user = User.objects.get(pk=member['user'])
        to.append(user.email)
        if member['status'] == "new":
            # if user is new, send them welcome email
            new_content = "\n\nYour username is: " + user.username
            new_content += "\n\n Your password is: " + user.password
            new_msg = new_msg_greeting + new_content + new_closing
            msg = EmailMessage(new_subject, new_msg, from_email, [user.email])
            msg.send()

    # Build You've been added to a Challenge Email [status !=new, 'existing']
    subject = "Congrats! You've been added to " + challenge.name.title() + " on Challenger!"
    text_content = 'Hello!\n\nThe gauntlet has been tossed!'
    html_content = '<div style="font-size: 16px; width:100%; margin: 20px;"><p>Hello!</p><p>The gauntlet has been tossed!'

    if challenge.start_date == challenge.end_date:
        date_msg = "On " + datetime.strftime(challenge.start_date, '%m/%d/%Y') + " only"
    else:
        date_msg = "From " + datetime.strftime(challenge.start_date, '%m/%d/%Y') + " until " + datetime.strftime(
            challenge.end_date, '%m/%d/%Y')
    date_msg += ", you can go to " + DEFAULT_DOMAIN + "/challenges/ and click the submit button for " + challenge.name.title() + "."

    text_content += "\n\n" + date_msg
    html_content += "<p>" + date_msg + "</p>"

    if challenge.example_image:
        html_content += "<div style='height: 150px; width: 150px; margin: 20px auto; display:inline-block; background: url(" + challenge.example_image.url + ");background-size:contain; background-repeat:no-repeat;'></div>"
    text_content += "\n\nDETAILS:\n" + challenge.description
    html_content += "<p>DETAILS</p><p>" + challenge.description + "</p>"

    closing_msg = "Have Fun and Challenger on!"

    text_content += "\n\n" + closing_msg
    html_content += "<p>" + closing_msg + "</p></div>"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return True
