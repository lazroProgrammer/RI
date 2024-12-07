import time
from tokenization import create_json_output, get_unique_words
import math 
    
from radicalization import *

import json
from collections import defaultdict


def ponderate_tf_idf():

    with open("transformed_word_to_docs.json", 'r') as file:
        radicalized_docs = json.load(file)
    with open("outputs/words/indexed_docs.json") as file1:
        doc_count=len(json.load(file1))
    
    tf_idf_docs = defaultdict(lambda: defaultdict(float))
    for node in radicalized_docs: 
        radical = node["word"]
        nb_docs = node["nb_docs"]
        idf = math.log(doc_count / (1 + nb_docs))
        for doc, count in node["docs"].items():
            tf = count
            tf_idf_docs[radical][doc] = tf * idf
    
    with open("ponderated_docs.json", 'w', encoding='utf-8') as output_file:
        json.dump(tf_idf_docs, output_file, indent=4, ensure_ascii=False)


ponderate_tf_idf()

