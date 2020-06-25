"""
PREPROCESSING DATA
Disaster Response Pipeline Project
Udacity - Data Science Nanodegree

Sample Script Execution:
> python process_data.py disaster_messages.csv disaster_categories.csv DisasterResponse.db

Arguments:
    1) CSV file containing messages (disaster_messages.csv)
    2) CSV file containing categories (disaster_categories.csv)
    3) SQLite destination database (DisasterResponse.db)
"""

import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
 
def load_data(messages_filepath, categories_filepath):
    """
    Load Data function
    
    Arguments:
        messages_filepath -> path to messages csv file
        categories_filepath -> path to categories csv file
    Output:
        messages, categories -> Loaded dasa as Pandas DataFrame
    """
    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    return messages,categories

def clean_data(messages,categories):
    """
    Clean Data function
    
    Arguments:
        messages, categories -> raw data Pandas DataFrame
    Outputs:
        df -> clean data Pandas DataFrame
    """

    # dropping ALL duplicte values 
    messages.drop_duplicates(subset ="id", keep = False, inplace = True)
    categories.drop_duplicates(subset ="id", keep = False, inplace = True)  

    # Dummy the genre categorical variables
    messages = pd.concat([messages.drop('genre', axis=1), pd.get_dummies(messages['genre'], prefix='genre', prefix_sep='_')], axis=1)

    # Split categories into separate category columns
    ids = categories.id.values
    categories = categories['categories'].str.split(pat=';',expand=True)
    data = list()
    # select the index row of the categories dataframe 
    for i in range(categories.shape[0]):
        # convert each cell in row to dict
        row = dict((j[:-2], j[-1:]) for j in categories.iloc[i,:]) 
        data.append(row)
    categories = pd.DataFrame.from_dict(data)
    
    categories['id'] = ids
    categories.set_index('id')

    # Merge datasets
    df = pd.merge(left=messages, right=categories, left_index=True, right_index=True, on = ['id'], how='left')
    df  = df.dropna()# Drop any row with a missing value
    # convert column from string to int
    for column in df.iloc[:,3:].columns:
        df[column] = df[column].astype(np.int)
    df['related'][df['related']==2]=1
    return df

def save_data(df, database_filename):
    """
    Save Data function
    
    Arguments:
        df -> Clean data Pandas DataFrame
        database_filename -> database file (.db) destination path
    """
    engine = create_engine('sqlite:///'+ database_filename)
    df.to_sql('merged', engine, index=False,if_exists='replace')
    pass  


def main():
    """
    Main Data Processing function
    
    This function implement the ETL pipeline:
        1) Data extraction from .csv
        2) Data cleaning and pre-processing
        3) Data loading to SQLite database
    """
    print(sys.argv)
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        messages ,categories = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(messages,categories)
        
        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)
        
        print('Cleaned data saved to database!')
    
    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()