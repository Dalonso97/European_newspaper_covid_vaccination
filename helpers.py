
import os
import selenium
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from PIL import Image
import io
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import ElementClickInterceptedException
import pandas as pd
import seaborn as sns
import dateparser
import matplotlib.pyplot as plt

import re

import spacy 
from spacy import displacy

# Importing TextBlob
from textblob import TextBlob

#Function that gives us sentiment classification using textblob
def sentiment_scores_tb(sentence):
    result = TextBlob(sentence).sentiment.polarity
    time.sleep(1)
    # decide sentiment as positive, negative and neutral
    if result >= 0.5 :
        return "Positive"

    elif result <= - 0.05 :
        return "Negative"

    else :
        return "Neutral"


    # import SentimentIntensityAnalyzer class
# from vaderSentiment.vaderSentiment module.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def sentiment_scores_VADER(sentence):
    # Create a SentimentIntensityAnalyzer object.
    time.sleep(2)
    analyzer = SentimentIntensityAnalyzer()

    # polarity_scores method of SentimentIntensityAnalyzer
    # object gives a sentiment dictionary.
    # which contains pos, neg, neu, and compound scores.
    sentiment_dict = analyzer.polarity_scores(sentence)

    # decide sentiment as positive, negative and neutral
    if sentiment_dict['compound'] >= 0.05 :
        return "Positive"

    elif sentiment_dict['compound'] <= - 0.05 :
        return "Negative"

    else :
        return "Neutral"

#Function that return a dataframe with the entities of the articles
def ner(list_of_text, model_language): 
    entities = []
    labels = []
    nlp = spacy.load(model_language)
    for i in list_of_text:
        doc = nlp(i)
        for ent in doc.ents:
            entities.append(ent.text)
            labels.append(ent.label_)

    df_ner = pd.DataFrame({'Entity':entities,'Label':labels})
    return df_ner

# Clean function in order to eliminate characters like \n or \n\n after scraping
def preprocessor(text):
#     text = str(text).lower()
    
#     text = re.sub('https?://\S+|www\.\S+', '', text)
#     text = re.sub('<.*?>+', '', text)
#     text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n\n', '', text)
    text = re.sub('\'','', text)
    text = re.sub('\n', '', text)
    text = re.sub('   ', '', text)
    text = re.sub('\xa0', '', text)
    text = re.sub('\xad', '', text)
    text = re.sub('\ufeff', '', text)
    text = re.sub('\u2009', '', text)
    text = re.sub('\u200b', '', text)
    
#     text = re.sub('\w*\d\w*', '', text)
    return text
    