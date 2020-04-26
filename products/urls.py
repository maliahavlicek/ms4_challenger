from django.urls import path, include
from .views import all_products

urlpatterns = [
    path('', all_products, name='products'),
]
