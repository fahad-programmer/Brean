from django.shortcuts import render
from django.http import request


# Create your views here.
def Home(request):
    return render(request, 'home/index.html')


def Search(request):
    return render(request, 'page/search.html')
