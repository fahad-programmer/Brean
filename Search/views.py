from django.shortcuts import render
from django.http import request



# Create your views here.
def Home(request):
    return render(request, template_name='home/index.html')