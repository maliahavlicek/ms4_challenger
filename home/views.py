from django.shortcuts import render


def index(request):
    """Return the index.html file"""
    return render(request, 'index.html')


def test_coverage(request):
    """show test coverage main file"""
    return render(request, 'test_coverage/index.html')