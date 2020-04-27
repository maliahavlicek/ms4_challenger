from django.shortcuts import render
from products.models import ServiceLevel


# Create your views here.
def do_search(request):
    products = ServiceLevel.objects.filter(name__icontains=request.GET['q'])
    return render(request, 'products.html', {'products': products})
