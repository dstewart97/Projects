from reviews.models import ReviewData

def get_feedback(date=None, credit_type=None, sentiment_category=None, dominant_topic=None):
    queryset = ReviewData.objects.all()

    if date:
        queryset = queryset.filter(date=date)
    if credit_type:
        queryset = queryset.filter(credit_type=credit_type)
    if sentiment_category:
        queryset = queryset.filter(sentiment_category=sentiment_category)
    if dominant_topic:
        queryset = queryset.filter(dominant_topic=dominant_topic)

    return queryset