#!/usr/bin/env python
# coding: utf-8

# In[20]:
import argparse

parser = argparse.ArgumentParser(description='classify script.')
parser.add_argument('--input-file', type=str, required=True,
help='Path to the input text file.')
parser.add_argument('--encoding', type=str, default="utf-8",
help="Text encoding of the input file. Default is utf-8.")
parser.add_argument("--output-json-file", type=str, required=True,
help="Filename for the output JSON file.")
parser.add_argument("--explanation-output-dir", type=str, required=True,
    help="Directory for the explanation outputs.")


args = parser.parse_args()

file_path = args.input_file
with open(file_path, "r") as file:
    content = file.read()


# In[11]:




# In[12]:


import keras.models
import pandas as pd
classify_model = keras.models.load_model('model')


# In[13]:


import pickle
category_lookup = pickle.loads(open('genres.pkl', 'rb').read())
category_lookup


# In[23]:






# In[22]:


prediction = classify_model.predict([content])
prediction_frame = pd.DataFrame(data=prediction, columns=category_lookup.keys())
prediction_frame


# In[24]:


top_n = 3  # Get the top 3 values

# Use apply to find the top n values and their indices for each row
top_3_values = prediction_frame.apply(lambda row: row.nlargest(top_n), axis=1)

print(top_3_values)


# In[25]:


top_n_indices = top_3_values.columns.tolist()
print(top_n_indices)


# In[35]:


import json



with open(args.output_json_file, 'w') as json_file:
    json.dump(top_n_indices, json_file, indent=4)


# In[ ]:




