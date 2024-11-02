import pandas as pd
from reviews.models import ReviewData


# def get_review_count_by_date():
#     # Fetch data
#     queryset = ReviewData.objects.all().values() 
#     df = pd.DataFrame(list(queryset))
#     review_count_by_date_df = df.groupby('date').size().reset_index(name = 'total_reviews')
#     review_count_by_date_df = review_count_by_date_df.sort_values('date')
#     review_count_by_date_df['date'] = review_count_by_date_df['date'].dt.strftime('%Y-%m-%d')
#     final_review_count_data = review_count_by_date_df.set_index('date')['total_reviews'].to_dict()
#     return final_review_count_data


def get_filtered_data(date = None, credit_type=None, sentiment_category=None, dominant_topic=None):
    # Query the Review model with filters
    queryset = ReviewData.objects.all()
    
    if date:
        queryset = queryset.filter(date=date)
    if credit_type:
        queryset = queryset.filter(credit_type=credit_type)
    if sentiment_category:
        queryset = queryset.filter(sentiment_category=sentiment_category)
    if dominant_topic:
        queryset = queryset.filter(dominant_topic=dominant_topic)

    # Convert to DataFrame and aggregate
    df = pd.DataFrame.from_records(queryset.values('date'))
    df['date'] = pd.to_datetime(df['date'])
    total_reviews_by_date = df.groupby(df['date'].dt.to_period("Q")).size().to_dict()

    return {'total_reviews_by_date': total_reviews_by_date}
