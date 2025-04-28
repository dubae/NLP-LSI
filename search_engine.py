from utils import query_to_vector, transform_query, cosine_similarity

def recommend_top_k(query_text, word_list, word_to_index, U_k, S_k, reduced_docs, file_list, k):
    query_vec = query_to_vector(query_text, word_list, word_to_index)
    query_vec_reduced = transform_query(query_vec, U_k, S_k)

    similarities = []

    for idx, doc_vec in enumerate(reduced_docs):
        sim = cosine_similarity(query_vec_reduced, doc_vec)
        similarities.append((file_list[idx], sim))

    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:k]
