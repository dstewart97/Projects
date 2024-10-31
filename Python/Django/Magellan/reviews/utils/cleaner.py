import re
import pandas as pd

class ReviewCleaner:
    def __init__(self):
        pass

    
    def clean_helpful_columns(self, df):
        pattern = re.compile(r"(\d+)\s+(\d+)\s+(\d+)")
        # Iterate through each row
        for index, row in df.iterrows():
            # Check if columns contain pattern
            for column in ['Helpful', 'Not_Helpful', 'Comment']:
                match = pattern.search(str(row[column]))
                if match:
                    df.at[index, 'Helpful'] = int(match.group(1))
                    df.at[index, 'Not_Helpful'] = int(match.group(2))
                    df.at[index, 'Comment'] = int(match.group(3))
        return df
    
    
    def deduplicate_data(self, df):
        df = df.drop_duplicates(subset = df.columns.difference(['Credit_Type']))
        return df
    
    
    def fill_missing_verified_customer(self, df):
        df['Verified_Customer'] = df['Verified_Customer'].apply(lambda x: 'Not verified' if x!= 'Verified cardholder' else x)
        return df

    
    def convert_to_date(self, df, column_name):
        df[column_name] = pd.to_datetime(df[column_name])
        return df
    

    def convert_to_int(self, df, columns):
        for column in columns:
            df[column] = pd.to_numeric(df[column], errors = 'coerce').fillna(0).astype(int)
        return df
    
    
    def extract_rating_as_int(self, df, column_name, new_column_name):
        df[new_column_name] = df[column_name].apply(lambda x: int(float(re.search(r'(\d\.\d)', x).group(1))))
        return df
    
    
    
    def run_all_cleaning(self, df):
        df = self.clean_helpful_columns(df)
        df = self.deduplicate_data(df)
        df = self.fill_missing_verified_customer(df)
        df = self.convert_to_date(df, 'Date')
        df = self.convert_to_int(df, ['Helpful', 'Not_Helpful', 'Comment'])
        df = self.extract_rating_as_int(df, 'Rating', 'Rating_Int')
        return df
