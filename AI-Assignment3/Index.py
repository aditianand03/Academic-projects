#!/usr/bin/env python
# coding: utf-8

# In[29]:

from nltk.corpus import wordnet

import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
from bs4 import BeautifulSoup
# Create lemmatizer
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import sqlite3

import pandas as pd
import numpy as np
import tensorflow as tf


# In[79]:


import argparse
parser = argparse.ArgumentParser(description='Indexing Script.')
parser.add_argument('--raw-data',type=str,required=True, help='Path to the input text file.')
args = parser.parse_args()
connec = sqlite3.connect(args.raw_data)


# In[78]:


data = pd.read_sql("select * from tvmaze", connec)

genres = pd.read_sql("select * from tvmaze_genre", connec)
#genres = pd.DataFrame(genres)
genre_mapping = genres.groupby('tvmaze_id')['genre'].apply(list).to_dict()


# In[31]:


data['genre'] = data['tvmaze_id'].map(genre_mapping)


# In[46]:


df = data[["tvmaze_id",'description', 'genre',"showname"]]
df = df.dropna().reset_index(drop=True)


# In[48]:


df


# In[49]:


# Function to remove specific HTML tags
def remove_html_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()

# Apply the function to the 'df.description' column
df['description'] = df['description'].apply(remove_html_tags)


# In[1]:


df = df.dropna().reset_index(drop=True)


# In[53]:


df


# In[ ]:


def lemmatize_text(text):
    lemmatizer = WordNetLemmatizer()
    tokens = nltk.word_tokenize(text)
    lemmatized_tokens = [lemmatizer.lemmatize(word, wordnet.VERB) for word in tokens]
    return ' '.join(lemmatized_tokens)


df['description'] = df['description'].apply(lemmatize_text)

import pickle
with open("lemmatize.pkl", "wb") as file:
    pickle.dump(df,file)

