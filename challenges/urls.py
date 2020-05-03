from django.urls import path
from .views import all_challenges

urlpatterns = [
    path('', all_challenges, name='challenges'),
]