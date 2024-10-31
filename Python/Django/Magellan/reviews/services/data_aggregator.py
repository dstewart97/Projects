import pandas as pd
from reviews.models import ReviewData


def get_sentiment_distribution():
    # Fetch data
    queryset = ReviewData.objects.all().values() 
    df = pd.DataFrame(list(queryset))
    sentiment_counts = df['sentiment_category'].value_counts().to_dict
    return sentiment_counts