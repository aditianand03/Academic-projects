#!/usr/bin/env python
# coding: utf-8

# In[15]:


import argparse
parser = argparse.ArgumentParser(description='search script.')
parser.add_argument("--input-file", type=str, required=True,
help="Path to the input text file.")
parser.add_argument("--encoding", type=str, default="utf-8",
help="Text encoding of the input file. Default is utf-8.")
parser.add_argument("--output-json-file", type=str, required=True,
help="Filename for the output JSON file.")

args = parser.parse_args()


# In[16]:


file_path = args.input_file
with open(file_path, "r") as file:
    content = file.read()


# In[11]:

import pickle
with open("lemmatize.pkl", "rb") as file:
    data_2 = pickle.load(file)
import pandas as pd
from rank_bm25 import BM25Okapi
tokenized_docs = [doc.lower().split() for doc in data_2['description']]
bm25_obj = BM25Okapi(tokenized_docs)
def bm25_search(query, top_n=3):
    query_tokens = query.lower().split()
    scores = bm25_obj.get_scores(query_tokens)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_n]
    top_results = data_2.loc[top_indices, ['tvmaze_id', 'showname']]
    return top_results


query = content

search_results = bm25_search(query, top_n=1)

print("Search Results:")
print(search_results)


# In[12]:


import json

search_results_output = search_results.columns.tolist()
print(search_results_output)

with open(args.output_json_file, 'w') as json_file:
    json.dump(search_results_output, json_file, indent=4)

