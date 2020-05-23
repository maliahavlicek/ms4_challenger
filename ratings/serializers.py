from rest_framework import serializers
from .models import RatingInput, TotalTrophies


class RatingsInputSerializer(serializers.ModelSerializer):
    """
    package up rating input for rest_framework ajax transport
    """
    class Meta:
        model = RatingInput
        fields = '__all__'


class TotalTrophiesSerializer(serializers.ModelSerializer):
    """
    package up TotalTrophy for rest_framework ajax transport
    """
    class Meta:
        model = TotalTrophies
        fields = '__all__'
