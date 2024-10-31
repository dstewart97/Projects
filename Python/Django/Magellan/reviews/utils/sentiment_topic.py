from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import pandas as pd
import re


class SentimentTopicAnalyzer:
    def __init__(self):
        self.topic_keywords = {
            'fees' : ['annual fee', 'fees', 'late fee', 'service fee', 'penalty', 'over balance', 'payment fee', 'yearly fee', 'membership fee', 'overdue', 'over due', 'missed payment', 'atm fee', 'fine', 'charge', 'hidden fee', 'surprise charge', 'hidden fees', 'unexpected fees', 'unexpected charge', 'unexpected fee'],

            'customer_service' : ['customer service', 'representative', 'agent', 'support', 'helpdesk', 'rude', 'unhelpful', 'bad service', 'terrible experience', 'friendly', 'helpful', 'excellent service', 'quick response', 'long wait', 'hold time', 'automated service', 'call center'],

            'account' : ['blocked', 'suspended', 'frozen', 'can\'t access', 'closed account', 'initial setup', 'easy setup', 'hard to open', 'cancelled', 'closed', 'cancel'],

            'interest_rate' : ['interest rate', 'APR', 'rate', 'finance charge', 'residual interest', 'variable interest', 'interest charge', 'variable'],

            'rewards_benefits' : ['rewards', 'points', 'cashback', 'cash back', 'percent back', 'miles', 'rewards point', 'earn points', 'redeem points', 'travel miles', 'flight miles', 'airline rewards', 'bonus points', 'signup bonus', 'sign-up bonus', 'intro offer', 'introductory offer', 'gas rewards', 'dining rewards', 'groceries', 'travel rewards', 'retail rewards', 'intro rate', 'introductory rate', 'promotional offer', 'promotional', 'promotion', 'limited offer', 'denied rewards'],

            'credit_limit' : ['credit limit', 'increase', 'decrease', 'limit', 'credit line', 'spending limit', 'available credit', 'credit line increase', 'cli', 'higher limit', 'limit raised', 'line raised', 'limit reducction', 'credit lowered'],

            'billing_payments' : ['statement', 'billing', 'monthly bill', 'payment due', 'due date', 'payment deadline', 'autopay', 'automatic payment', 'scheduled payment', 'minimum payment', 'partial payment', 'overpayment', 'extra payment', 'paid too much', 'online payment', 'pay on app'],
            
            'credit_building' : ['credit repair', 'rebuilding credit', 'improve credit', 'secured card', 'deposit required', 'credit builder', 'credit utilization', 'debt ratio'],

            'balance_transfer' : ['easy trasnfer', 'seamless transfer', 'trasnfer approval', 'balance transfer', 'low interest transfer', 'transfer a balance'],

            'card_design' : ['metal card', 'premium design', 'premium card', 'color', 'card material', 'card customization', 'custom card', 'card design', 'card choice'],

            'application_process' : ['instant approval', 'easy apply', 'pre-approved', 'accepted', 'easy approval', 'application declined', 'application denied', 'hard inquiry', 'soft inquiry', 'credit pull', 'credit check'],

            'mobile_app_online' : ['mobile app', 'app', 'online account', 'manage account', 'website', 'home page', 'apple store', 'app store']
        }
        self.analyzer = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))


    def concatenate_text(self, df):
        df['Text'] = df['Title'].fillna("").str.lower() + ' ' + df['Body'].fillna("").str.lower()
        return df

    def get_and_classify_sentiment(self, text):
        if isinstance(text, float):
            text = str("")
        scores = self.analyzer.polarity_scores(text)
        if scores['compound'] >= 0.98:
            return 'Extremely Positive'
        elif 0.95 <= scores['compound'] < 0.98:
            return 'Very Positive'
        elif 0.8 <= scores['compound'] < 0.95:
            return 'Positive'
        elif -0.1 < scores['compound'] < 0.8:
            return 'Neutral'
        elif -0.4 <= scores['compound'] <= -0.1:
            return 'Negative'
        elif -0.7 <= scores['compound'] < -0.4:
            return 'Very Negative'
        else:  
            return 'Extremely Negative'
        
    def convert_sentiment_to_scale(self, sentiment):
        sentiment_mapping = {
            'Extremely Positive' : 7,
            'Very Positive' : 6,
            'Positive' : 5,
            'Neutral' : 4,
            'Negative' : 3,
            'Very Negative': 2,
            'Extremely Negative' : 1
        }
        return sentiment_mapping.get(sentiment, None)
            
    def assign_topics(self, text):
        text_lower = text.lower()
        matched_topics = []

        # Check for short comments
        if len(text_lower.split()) <= 5:
            matched_topics.append('short')

        for topic, keywords in self.topic_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                matched_topics.append(topic)
        
        if 'credit_limit' not in matched_topics: 
            dollar_amount_pattern = r'\b\$?\d{1,5}(?:,?\d{3})\b'
            if re.search(dollar_amount_pattern, text):
                matched_topics.append('credit_limit') 

        if not matched_topics:
            return ['other']
        
        return matched_topics
    
    def find_dominant_topic(self, matched_topics):
        if matched_topics:
            counter = Counter(matched_topics)
            # Return the topic with the highest count
            return counter.most_common(1)[0][0]
        else:
            return 'other'
    
    def expand_topics(self, df):
        # Create individual topic columns
        max_topics = df['Assigned_Topics'].apply(len).max()  # Find the maximum number of topics in any rows
        for i in range(max_topics):
            df[f'Topic{i+1}'] = df['Assigned_Topics'].apply(lambda x: x[i] if i < len(x) else None)

        # Create the Dominant_Topic column
        df['Dominant_Topic'] = df['Assigned_Topics'].apply(self.find_dominant_topic)

        return df


    def process_reviews(self, df):
        df = self.concatenate_text(df)
        df['Sentiment_Category'] = df['Text'].apply(self.get_and_classify_sentiment)
        df['Sentiment_Scale'] = df['Sentiment_Category'].apply(self.convert_sentiment_to_scale)
        df['Assigned_Topics'] = df['Text'].apply(self.assign_topics)
        df = self.expand_topics(df)
        return df