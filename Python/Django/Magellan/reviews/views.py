#### Django-Specific / Default Packages ####
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
# from .services.data_aggregator import get_review_count_by_date
from .services.data_aggregator import get_filtered_data
from .services.get_feedback import get_feedback
import json




def index(request):
    return render(request, 'reviews/index.html', {'title': 'Dashboard'} )


def feedback_page(request):
     # Retrieve all reviews (without filters)
    feedback = get_feedback()
    # Set up pagination: 5 reviews per page (change as desired)
    paginator = Paginator(feedback, 5)
    page_number = request.GET.get('page')
    feedback = paginator.get_page(page_number)
    # Return context
    context = {
        'feedback': feedback
    }
    return render(request, 'reviews/feedback.html', context)


def filter_feedback(request):
    date = request.GET.get('date')
    credit_type = request.GET.get('credit_type')
    sentiment_category = request.GET.get('sentiment_category')
    dominant_topic = request.GET.get('dominant_topic')

    # Retrieve filtered reviews
    reviews_queryset = get_feedback(date, credit_type, sentiment_category, dominant_topic)
    
    # Pagination
    paginator = Paginator(reviews_queryset, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Prepare JSON response with relevant fields
    feedback_data = [
        {
            'product': item.product,
            'rating_int': item.rating_int,
            'sentiment_category': item.sentiment_category,
            'dominant_topic': item.dominant_topic,
            'date': item.date.strftime('%Y-%m-%d')
        }
        for item in page_obj
    ]
    return JsonResponse({'feedback_data': feedback_data})


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
    filtered_data['average_rating_by_date'] = {str(k): v for k, v in filtered_data['average_rating_by_date'].items()}
    filtered_data['average_sentiment_by_date'] = {str(k): v for k, v in filtered_data['average_sentiment_by_date'].items()}
    return JsonResponse(filtered_data)


