from django.shortcuts import render
from .models import ServiceLevel


# Create your views here.
def all_products(request):
    products = ServiceLevel.objects.all()
    owned_product = False
    if request.user.profile.product_level:
        owned_product = request.user.profile.product_level
    return render(request, "products.html", {"products": products, 'owned_product': owned_product})
