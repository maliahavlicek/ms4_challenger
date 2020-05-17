from django.urls import path
from .views import all_submissions, create_submission, update_submission

urlpatterns = [
    path('<str:challenge_id>', all_submissions, name='submissions'),
    path('create/<str:challenge_id>', create_submission, name='create_submission'),
    path('update/<str:challenge_id>/', update_submission, name='update_submission'),
]
