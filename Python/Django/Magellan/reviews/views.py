#### Django-Specific / Default Packages ####
from django.shortcuts import render
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from .services.data_aggregator import get_filtered_data
from .services.get_feedback import get_feedback
import json





def index(request):
    return render(request, 'reviews/index.html', {'title': 'Dashboard'} )



def feedback_page(request):
    # Get filter parameters from the GET request
    date = request.GET.get('date')
    credit_type = request.GET.get('credit_type')
    sentiment_category = request.GET.get('sentiment_category')
    dominant_topic = request.GET.get('dominant_topic')

    # Retrieve ordered and filtered feedback
    feedback = get_feedback(
        date=date, 
        credit_type=credit_type, 
        sentiment_category=sentiment_category, 
        dominant_topic=dominant_topic,
        order_by_field='id', 
        descending=True
    )

    # Set up pagination: 5 reviews per page
    paginator = Paginator(feedback, 5)
    page_number = request.GET.get('page', 1)
    feedback = paginator.get_page(page_number)

    # Pass filter parameters to the template for pagination links
    context = {
        'feedback': feedback,
        'date': date,
        'credit_type': credit_type,
        'sentiment_category': sentiment_category,
        'dominant_topic': dominant_topic,
        'title' : 'Feedback'
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

    # Render only the filtered feedback items
    return render(request, 'reviews/feedback_list.html', {'feedback': page_obj})




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


