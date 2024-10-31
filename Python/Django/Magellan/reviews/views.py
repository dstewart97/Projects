#### Django-Specific / Default Packages ####
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .services.data_aggregator import get_review_count_by_date
import json




# def index(request):
#     return render(request, 'reviews/index.html', {'title': 'Dashboard'} )

def index(request):
    total_review_count_data = get_review_count_by_date()

    context = {
        'title': 'Dashboard',
        'total_review_count_data' : json.dumps(total_review_count_data)
    }

    return render(request, 'reviews/index.html', context)

