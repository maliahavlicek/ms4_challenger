"""
/checkout URL Configuration
"""
from django.urls import path
from .views import checkout

urlpatterns = [
    path('<str:pk>/', checkout, name='checkout'),
]
