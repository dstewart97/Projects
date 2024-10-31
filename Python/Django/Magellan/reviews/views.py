#### Django-Specific / Default Packages ####
from django.shortcuts import render
from django.http import HttpResponse



def index(request):
    return render(request, 'reviews/index.html', {'title': 'Dashboard'} )
