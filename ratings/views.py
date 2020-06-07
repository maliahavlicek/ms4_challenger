from submissions.models import Entry
from rest_framework.decorators import api_view
from .serializers import RatingsInputSerializer, TotalTrophiesSerializer
from rest_framework.response import Response
from .models import Rating
from django.contrib.auth.models import User
from datetime import datetime
import pytz

utc = pytz.UTC


@api_view(['post'])
def send(request):
    """
    Create or update a rating if input form is valid and user is really allowed to rate given entry
    """
    serializer = RatingsInputSerializer(data=request.data)
    if serializer.is_valid():
        entry = Entry.objects.get(id=serializer.data['entry_id'])
        challenge = entry.challenge_set.first()
        members = challenge.get_members()
        # need to make sure user belongs to challenge entry is part of
        user = User.objects.filter(id=serializer.data['reviewer']).first()
        if user in members or challenge.owner == user:
            # check if entry has a rating by the reviewer
            if entry.ratings.count() > 0 and entry.ratings.filter(reviewer=user).count() > 0:
                # updating
                rating = entry.ratings.get(reviewer=user)
                rating.rating = serializer.data['rating']
                rating.updated_date = utc.localize(datetime.today())
                rating.save()
            else:
                # creating
                rating = Rating.objects.create(
                    reviewer=user,
                    rating=serializer.data['rating'],
                )
                entry.ratings.add(rating)

        # calculate the total trophies
        aggregated_rating = entry.get_rating()
        trophy_serializer = TotalTrophiesSerializer(data={'trophies': aggregated_rating, 'entry_id': str(entry.pk)})
        if trophy_serializer.is_valid():
            return Response(trophy_serializer.data)

    return Response(serializer.data)
