#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sqlite3
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import TextVectorization, Embedding, Dense, GlobalAveragePooling1D, Input
from sklearn.model_selection import train_test_split
import argparse


# In[2]:


parser = argparse.ArgumentParser(description='Training script.')
parser.add_argument('--training-data', type=str, required=True, help='Path to the training data sqlite file.')
args = parser.parse_args()


connect = sqlite3.connect(args.training_data)

data = pd.read_sql("select * from tvmaze", connect)



# In[ ]:


data_1 = pd.read_sql("select * from tvmaze_genre", connect)





# In[5]:


genres = pd.read_sql("select * from tvmaze_genre", connect)

genre_mapping = genres.groupby('tvmaze_id')['genre'].apply(list).to_dict()


# In[6]:


data['genre'] = data['tvmaze_id'].map(genre_mapping)


# In[7]:


data


# In[8]:


df = data[['description', 'genre']]
df = df.dropna().reset_index(drop=True)


# In[9]:


from bs4 import BeautifulSoup
def remove_tags(text):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.get_text()


# In[10]:


df['description'] = df['description'].apply(remove_tags)


# In[14]:


genre = genres['genre'].unique().tolist()
genre


# In[57]:


df['genre'][200]


# In[15]:


import numpy as np
target = np.zeros((df.shape[0], len(genre)))
target.shape


# In[20]:


forward_lookup_of_categories = {c:i for (i,c) in enumerate(genre)}
forward_lookup_of_categories


# In[21]:


for i, cs in zip(df.index, df.genre):
    for c in cs:
        category_number = forward_lookup_of_categories[c]
        target[i, category_number]= 1


# In[22]:


from sklearn.model_selection import train_test_split
train_val_X, test_X, train_val_y, test_y = train_test_split(df.description, target, test_size = 0.2)
train_X, validaton_X, train_y, validation_y = train_test_split(train_val_X, train_val_y, test_size=0.2)


# In[37]:


max_tokens = 10000
output_sequence_length = 200
embedding_dim = 64


# In[38]:


vectorizer = TextVectorization(max_tokens = max_tokens, output_sequence_length = output_sequence_length)
vectorizer.adapt(train_X)


# In[39]:


inputs = Input(shape=(1,), dtype = tf.string)


# In[40]:


vectorized = vectorizer(inputs)




# In[42]:


embedded = Embedding(max_tokens+1, embedding_dim)(vectorized)


# In[43]:


averaged = GlobalAveragePooling1D()(embedded)


# In[44]:


layer = Dense(64, activation = 'relu')(averaged)
output = Dense(len(genre), activation = 'softmax')(layer)


# In[45]:


model = Model(inputs = [inputs], outputs = [output])


# In[46]:


model.compile(loss = 'binary_crossentropy', metrics = ['accuracy'], optimizer= 'adam')


# In[47]:


model.summary()


# In[48]:


import keras.callbacks
callback = keras.callbacks.EarlyStopping(monitor='val_loss', patience=20, restore_best_weights = True)


# In[49]:


history=model.fit(train_X, train_y,
                 validation_data=(validaton_X, validation_y), epochs=100, callbacks=callback)


# In[50]:


model.evaluate(test_X,test_y)


# In[53]:


test_df = pd.DataFrame(data=model.predict(test_X),columns=genre)
test_df


# In[54]:


model.save('model')


# In[55]:


import pickle
with open('genres.pkl', 'wb') as f:
    f.write(pickle.dumps(forward_lookup_of_categories))


# In[ ]:




