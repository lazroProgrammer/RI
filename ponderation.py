import time
from tokenization import create_json_output, get_unique_words
import math 
    
from radicalization import *

import json
from collections import defaultdict


def ponderate_tf_idf():

    with open("radicalized_docs_count.json", 'r') as file:
        radicalized_docs = json.load(file)

  
    doc_count = len(radicalized_docs)
    doc_frequencies = defaultdict(int)
    for doc, radicals in radicalized_docs.items():
        for radical in radicals:
            doc_frequencies[radical] += 1

   
    tf_idf_docs = {}
    for doc, radicals in radicalized_docs.items():
        tf_idf_docs[doc] = {}

        for radical,tf  in radicals.items(): 
            
            idf = math.log(doc_count / (1 + doc_frequencies[radical]))

            tf_idf_docs[doc][radical] = tf * idf

    
    with open("ponderated_docs.json", 'w', encoding='utf-8') as output_file:
        json.dump(tf_idf_docs, output_file, indent=4, ensure_ascii=False)




