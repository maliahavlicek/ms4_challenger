from django.urls import path
from .views import all_challenges, create_challenge, delete_challenge, update_challenge, add_member

urlpatterns = [
    path('', all_challenges, name='challenges'),
    path('create/', create_challenge, name='create_challenge'),
    path('delete/<str:id>/', delete_challenge, name='delete_challenge'),
    path('update/<str:id>/', update_challenge, name='update_challenge'),
    path('add_member/', add_member, name='add_member'),
]