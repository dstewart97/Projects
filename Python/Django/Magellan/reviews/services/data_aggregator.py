import pandas as pd
from reviews.models import ReviewData


def get_review_count_by_date():
    # Fetch data
    queryset = ReviewData.objects.all().values() 
    df = pd.DataFrame(list(queryset))
    review_count_by_date_df = df.groupby('date').size().reset_index(name = 'total_reviews')
    review_count_by_date_df = review_count_by_date_df.sort_values('date')
    review_count_by_date_df['date'] = review_count_by_date_df['date'].dt.strftime('%Y-%m-%d')
    final_review_count_data = review_count_by_date_df.set_index('date')['total_reviews'].to_dict()
    return final_review_count_data