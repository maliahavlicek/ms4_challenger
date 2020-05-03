from django.urls import path
from .views import all_challenges, create_challenge

urlpatterns = [
    path('', all_challenges, name='challenges'),
    path('create/', create_challenge, name='create_challenge')
]