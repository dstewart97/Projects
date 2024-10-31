import pandas as pd
from reviews.utils.scrapper import ReviewScrapper
from reviews.utils.cleaner import ReviewCleaner
from reviews.utils.sentiment_topic import SentimentTopicAnalyzer
from reviews.models import ReviewData




class Magellan:
    def __init__(self):
        pass

    def run_scraper(self):
        scraper = ReviewScrapper(driver_path = r'C:\Users\dstewart\OneDrive - CreditOne Bank\Desktop\Python\msedgedriver.exe')
        product_dict = {
            'good_credit' : ['chaseunitedbusiness']
        }
        scraper.scrape_reviews(product_dict)
        raw_data = scraper.data
        scraper.close_driver()
        return raw_data

    def clean_data(self, raw_data):
        cleaner = ReviewCleaner()
        cleaned_data = cleaner.run_all_cleaning(raw_data)
        return cleaned_data
    
    def perform_analysis(self, cleaned_data):
        sentiment_analyzer = SentimentTopicAnalyzer()
        final_data = sentiment_analyzer.process_reviews(cleaned_data)
        return final_data
    
    def select_final_columns(self, df):
        final_columns = [
            'Date', 'Product', 'Credit_Type', 'Rating', 'Rating_Int', 'Title', 'Verified_Customer', 'Body', 'Helpful', 'Not_Helpful', 'Comment', 'Sentiment_Category', 'Sentiment_Scale', 'Dominant_Topic', 'Topic1', 'Topic2'
        ]
        return df[final_columns]
    
    def load_to_database(self, final_data):
        for index, row in final_data.iterrows():
                for index, row in final_data.iterrows():
                    review_instance = ReviewData(
                            date = row['Date'],
                            product = row['Product'],
                            credit_type = row['Credit_Type'],
                            rating = row['Rating'],
                            rating_int = row['Rating_Int'],
                            title = row['Title'],
                            verified_customer = row['Verified_Customer'],
                            body = row['Body'],
                            helpful = row['Helpful'],
                            not_helpful = row['Not_Helpful'],
                            comment = row['Comment'],
                            sentiment_category = row['Sentiment_Category'],
                            dominant_topic = row['Dominant_Topic'],
                            topic1 = row['Topic1'],
                            topic2 = row['Topic2']
                    )
                    review_instance.save()
                            

    def final_review_processing(self):
        raw_data = self.run_scraper()
        cleaned_data = self.clean_data(raw_data)
        analyzed_data = self.perform_analysis(cleaned_data)
        final_data = self.select_final_columns(analyzed_data)
        self.load_to_database(final_data)
        return final_data
    


