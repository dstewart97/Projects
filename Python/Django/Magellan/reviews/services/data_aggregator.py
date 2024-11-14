import pandas as pd
import matplotlib.cm as cm
import numpy as np
from reviews.models import ReviewData


# Function to generate a unique color for each point
def get_unique_colors(num_colors):
    return [cm.Paired(i / num_colors) for i in range(num_colors)]

# Define color mapping function for sentiment categories
def getColorForCategory(category):
    colors = {
        'Extremely Positive': 'rgba(27, 94, 32, 0.8)',
        'Very Positive': 'rgba(46, 125, 50, 0.8)',
        'Positive': 'rgba(76, 175, 80, 0.8)',
        'Neutral': 'rgba(158, 158, 158, 0.8)',
        'Negative': 'rgba(239, 83, 80, 0.8)',
        'Very Negative': 'rgba(198, 40, 40, 0.8)',
        'Extremely Negative': 'rgba(183, 28, 28, 0.8)',
    }
    return colors.get(category, 'rgba(0, 0, 0, 0.5)')  # Default color


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
    df = pd.DataFrame.from_records(queryset.values('date', 'product', 'rating_int', 'sentiment_category', 'dominant_topic'))
    df['date'] = pd.to_datetime(df['date'])

    ## Top 3 Chart -- Left
    # Calculate total reviews by date
    total_reviews_by_date = df.groupby(df['date'].dt.to_period("Q")).size().to_dict()


    ## Top 3 Chart -- Middle
    # Calculate average rating by date, handing missing values
    average_rating_by_date = (
        df.groupby(df['date'].dt.to_period("Q"))['rating_int'].mean().dropna().to_dict()
    )

    ## Top 3 Chart -- Right
    # Calculate average sentiment by mapping category to int
    sentiment_mapping = {
        'Extremely Positive' : 7,
        'Very Positive' : 6,
        'Positive' : 5,
        'Neutral' : 4,
        'Negative' : 3,
        'Very Negative' : 2,
        'Extremely Negative' : 1

    }
    df['sentiment_score'] = df['sentiment_category'].map(sentiment_mapping)
    average_sentiment_by_date = (
        df.groupby(df['date'].dt.to_period('Q'))['sentiment_score'].mean().dropna().to_dict()
    )

    ## Stacked VBar
    # Calculate count of dominant topic by sentiment 
    stacked_data = (
        df.groupby(['dominant_topic', 'sentiment_category']).size().unstack(fill_value=0)
    )
    # Define order for sentiment category
    sentiment_order = [
        'Extremely Positive',
        'Very Positive',
        'Positive',
        'Neutral',
        'Negative',
        'Very Negative',
        'Extremely Negative'
    ]
    # Reindex columns to follow spefici order
    stacked_data = stacked_data.reindex(columns=sentiment_order, fill_value=0)
    # Prepare data for Javascript
    dominantTopicSentimentlabels = stacked_data.index.tolist()
    dominantTopicSentimentdatasets = []
    for sentiment in stacked_data.columns:
        dominantTopicSentimentdatasets.append({
            'label' : sentiment,
            'data' : stacked_data[sentiment].to_list(),
            'backgroundColor' : getColorForCategory(sentiment)
        })


    ## Scatter Plot
    # Calculate the average sentiment and rating per product
    scatter_data = df.groupby('product').agg(
        average_sentiment = ('sentiment_score', 'mean'),
        average_rating = ('rating_int', 'mean')
    ).reset_index()
    # Prepare data for javascript
    scatterProducts = scatter_data['product'].tolist()
    scatterAverageSentiments = scatter_data['average_sentiment'].tolist()
    scatterAverageRatings = scatter_data['average_rating'].tolist()
    # Generate unique colors for each product
    num_products = len(scatterProducts)
    product_colors = get_unique_colors(num_products)
    # Combined into dataset
    scatter_plot_data = {
        'products' : scatterProducts,
        'average_sentiments' : scatterAverageSentiments,
        'average_ratings' : scatterAverageRatings,
        'colors' : [f'rgba({int(c[0]*255)}, {int(c[1]*255)}, {int(c[2]*255)}, 1)' for c in product_colors]
    }


    ## Return final datasets to pass to javascript
    return {
        'total_reviews_by_date': total_reviews_by_date,
        'average_rating_by_date' : average_rating_by_date,
        'average_sentiment_by_date' : average_sentiment_by_date,
        'dominantTopicSentimentlabels' : dominantTopicSentimentlabels,
        'dominantTopicSentimentdatasets' : dominantTopicSentimentdatasets,
        'scatter_plot_data' : scatter_plot_data,
        }
