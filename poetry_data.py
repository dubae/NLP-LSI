import os
import numpy as np
from utils import preprocess

def load_poetry_data(folder_path):
    file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.txt')])

    word_set = set()
    documents = []

    for filename in file_list:
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            text = f.read()
            words = preprocess(text)
            documents.append(words)
            word_set.update(words)

    word_list = sorted(list(word_set))

    word_to_index = {word: idx for idx, word in enumerate(word_list)}
    doc_to_index = {doc: idx for idx, doc in enumerate(file_list)}

    matrix = np.zeros((len(word_list), len(file_list)), dtype=int)

    for doc_idx, words in enumerate(documents):
        for word in words:
            word_idx = word_to_index[word]
            matrix[word_idx, doc_idx] += 1

    # SVD
    U, S, Vt = np.linalg.svd(matrix, full_matrices=False)

    k = 2
    U_k = U[:, :k]
    S_k = np.diag(S[:k])
    Vt_k = Vt[:k, :]

    reduced_docs = Vt_k.T

    return file_list, word_list, word_to_index, doc_to_index, U_k, S_k, reduced_docs
