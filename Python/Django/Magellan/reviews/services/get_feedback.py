from reviews.models import ReviewData

def get_feedback(date=None, credit_type=None, sentiment_category=None, dominant_topic=None, order_by_field = 'id', descending = False):
    queryset = ReviewData.objects.all()

    if date:
        queryset = queryset.filter(date=date)
    if credit_type:
        queryset = queryset.filter(credit_type=credit_type)
    if sentiment_category:
        queryset = queryset.filter(sentiment_category=sentiment_category)
    if dominant_topic:
        queryset = queryset.filter(dominant_topic=dominant_topic)

    # Add ordering
    if descending:
        order_by_field = f'-{order_by_field}' # Prefix with "-" for descending order
    queryset = queryset.order_by(order_by_field)

    return queryset