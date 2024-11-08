#### Django-Specific / Default Packages ####
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from .services.data_aggregator import get_review_count_by_date
from .services.data_aggregator import get_filtered_data
import json




def index(request):
    return render(request, 'reviews/index.html', {'title': 'Dashboard'} )


def filter_data(request):
    """Handles AJAX requests for filtered data."""
    # Get filter parameters from the request
    date = request.GET.get('date')
    credit_type = request.GET.get('credit_type')
    sentiment_category = request.GET.get('sentiment_category')
    dominant_topic = request.GET.get('dominant_topic')

    # Call your data aggregation function with filters
    filtered_data = get_filtered_data(date, credit_type, sentiment_category, dominant_topic)

    # Convert to JSON serializable format if needed
    filtered_data['total_reviews_by_date'] = {str(k): v for k, v in filtered_data['total_reviews_by_date'].items()}

    return JsonResponse(filtered_data)





# def index(request):
#     total_review_count_data = get_review_count_by_date()

#     context = {
#         'title': 'Dashboard',
#         'total_review_count_data' : json.dumps(total_review_count_data)
#     }

#     return render(request, 'reviews/index.html', context)


