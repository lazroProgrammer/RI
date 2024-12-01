import json
import math
from collections import defaultdict
from radicalization import *

def calculate_similarity():

    with open("ponderated_docs.json", 'r') as tf_idf_f:
        tf_idf_docs = json.load(tf_idf_f)

    # Load the radicalized query JSON file
    with open("radicalized_query.json", 'r') as query_f:
        query = json.load(query_f)

    # Calculate the query's TF-IDF weights
    query_tf_idf = {}
    total_query_terms = sum(query.values())
    for radical, count in query.items():
        query_tf_idf[radical] = count 

    # Compute similarity scores (dot product) between the query and each document
    similarity_scores = {}
    for doc, tf_idf_weights in tf_idf_docs.items():
        # Dot product calculation
        dot_product = sum(
            query_tf_idf.get(radical, 0) * tf_idf_weights.get(radical, 0)
            for radical in query_tf_idf
        )
        similarity_scores[doc] = dot_product

    # Save similarity scores to a JSON file
    with open("outputs/score.json", 'w', encoding='utf-8') as output_f:
        json.dump(similarity_scores, output_f, indent=4, ensure_ascii=False)

    print(f"Similarity scores saved to: score.json")
    return similarity_scores
