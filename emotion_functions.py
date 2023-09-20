import pandas as pd
import numpy as np
import matplotlib 
import matplotlib.pyplot as plt
from transformers import RobertaTokenizerFast, TFRobertaForSequenceClassification, pipeline

tokenizer = RobertaTokenizerFast.from_pretrained("arpanghoshal/EmoRoBERTa")
model = TFRobertaForSequenceClassification.from_pretrained("arpanghoshal/EmoRoBERTa")

emotion = pipeline('sentiment-analysis', 
                    model='arpanghoshal/EmoRoBERTa')

def get_emotion_label(text): 
    return(emotion(text)[0]['label'])

def autopct(pct): # only show the label when it's > 10%
    return ('%.2f' % pct) if pct > 1 else ''

def emotion_analysis(subset):
    subset['emotion_transformers_1']=subset['Title_en'].apply(get_emotion_label)
    
#     my_labels = subset['emotion_transformers_1'].unique()
#     ax = subset['emotion_transformers_1'].value_counts().plot(kind='pie', figsize=(28,12), autopct=autopct, labels=None)
#     ax.axes.get_yaxis().set_visible(False)
#     plt.legend(labels=my_labels)