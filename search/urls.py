from django.urls import path, include
from .views import do_search

urlpatterns = [
    path('', do_search, name='search')
    ]