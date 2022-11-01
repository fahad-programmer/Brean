from django.shortcuts import render_to_response
from django.http import request

from .form import form

# Create your views here.
def Home(request):
    return render_to_response('home/index.html')