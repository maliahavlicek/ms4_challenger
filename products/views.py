from django.shortcuts import render
from .models import ServiceLevel


# Create your views here.
def all_products(request):
    products = ServiceLevel.objects.all()
    return render(request, "products.html", {"products": products})