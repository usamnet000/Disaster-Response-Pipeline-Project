from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import WhitespaceTokenizer 
import re

def tokenize(text):
    """
    Remove capitalization and special characters and lemmatize texts
    """    

    # get tokens from text
    tokens = WhitespaceTokenizer().tokenize(text)
    lemmatizer = WordNetLemmatizer()
    
    # clean tokens
    processed_tokens = []
    for token in tokens:
        token = lemmatizer.lemmatize(token).lower().strip('!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')
        token = re.sub(r'\[[^.,;:]]*\]', '', token)
        
        # add token to compiled list if not empty
        if token != '':
            processed_tokens.append(token)
        
    return processed_tokens

class StartingVerbExtractor(BaseEstimator, TransformerMixin):
    """
    Starting Verb Extractor class
    
    This class extract the starting verb of a sentence,
    creating a new feature for the ML classifier
    """

    def starting_verb(self, text):
        sentence_list = nltk.sent_tokenize(text)
        for sentence in sentence_list:
            pos_tags = nltk.pos_tag(tokenize(sentence))
            first_word, first_tag = pos_tags[0]
            if first_tag in ['VB', 'VBP'] or first_word == 'RT':
                return True
        return False

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X_tagged = pd.Series(X).apply(self.starting_verb)
        return pd.DataFrame(X_tagged)
