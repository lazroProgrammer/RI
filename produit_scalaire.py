import json
import math
from collections import defaultdict
from radicalization import *

def produit_scalaire():

    with open("ponderated_docs.json", 'r') as tf_idf_f:
        tf_idf_docs = json.load(tf_idf_f)

    with open("radicalized_query.json", 'r') as query_f:
        query = json.load(query_f)

    # calculate the query's TF-IDF weights
    query_tf_idf = {}
    total_query_terms = sum(query.values())
    for radical, count in query.items():
        query_tf_idf[radical] = count 

    # compute similarity scores between the query and each document
    scores = defaultdict(float)
    for radical, terms_weights in tf_idf_docs.items():
        if radical in query_tf_idf:
            for doc, tf_idf_weight in terms_weights.items():
                scores[doc] += query_tf_idf[radical] * tf_idf_weight

    
    with open("outputs/score.json", 'w', encoding='utf-8') as output_f:
        json.dump(scores, output_f, indent=4, ensure_ascii=False)

    print(f"Similarity scores saved to: score.json")
    return scores

def sort_scores():
    
    with open("outputs/score.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    with open("outputs/sorted_score.json", 'w', encoding='utf-8') as sorted_file:
        json.dump(sorted_data, sorted_file, indent=4, ensure_ascii=False)
