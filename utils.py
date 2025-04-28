import re
import numpy as np
from numpy.linalg import norm

def preprocess(text):
    clean_text = re.sub(r'[^a-z0-9\s]', '', text.lower())
    return clean_text.split()

def cosine_similarity(a, b):
    return np.dot(a, b) / (norm(a) * norm(b))

def query_to_vector(query, word_list, word_to_index):
    query_words = preprocess(query)
    vector = np.zeros(len(word_list))
    for word in query_words:
        if word in word_to_index:
            idx = word_to_index[word]
            vector[idx] += 1
    return vector

def transform_query(query_vec, U_k, S_k):
    S_k_inv = np.linalg.inv(S_k)
    return np.dot(np.dot(query_vec, U_k), S_k_inv)
