import time
from tokenization import create_json_output, get_unique_words
    
from radicalization import *

import json
from collections import defaultdict

# Load knowledge_table.json and tokenized_docs_count.json
with open('outputs\knowledge_table.json', 'r') as kt_file:
    knowledge_table = json.load(kt_file)

with open('tokenized_docs_count.json', 'r') as docs_file:
    tokenized_docs = json.load(docs_file)

# Create a mapping from words to radicals
word_to_radical = {}
for entry in knowledge_table:
    radical = entry["radical"]
    for word in entry["words"]:
        word_to_radical[word] = radical

# Initialize a dictionary to store radicalized documents with counts
radicalized_docs = defaultdict(lambda: defaultdict(int))

# Replace tokens with radicals and count appearances
for doc_name, word_counts in tokenized_docs.items():
    for word, count in word_counts.items():
        if word in word_to_radical:
            radical = word_to_radical[word]
            radicalized_docs[doc_name][radical] += count
        else:
            # If the word doesn't have a corresponding radical, skip or include as is
            continue

# Convert defaultdict to a regular dictionary for saving
radicalized_docs = {doc: dict(counts) for doc, counts in radicalized_docs.items()}

# Save the radicalized document counts to a new JSON file
output_file_path = 'radicalized_docs_count.json'
with open(output_file_path, 'w', encoding='utf-8') as output_file:
    json.dump(radicalized_docs, output_file, indent=4, ensure_ascii=False)

def ponderate_tf_idf(json_file, output_file):
    """
    Ponderate the given JSON file with TF-IDF weights.

    Args:
        json_file (str): Path to the JSON file containing radicalized word counts per document.
        output_file (str): Path to save the ponderated JSON file with TF-IDF weights.

    Returns:
        None
    """
    # Load the radicalized document counts
    with open(json_file, 'r') as file:
        radicalized_docs = json.load(file)

    # Calculate document frequencies (DF) for each radical
    doc_count = len(radicalized_docs)
    doc_frequencies = defaultdict(int)
    for doc, radicals in radicalized_docs.items():
        for radical in radicals:
            doc_frequencies[radical] += 1

    # Calculate TF-IDF for each radical in each document
    tf_idf_docs = {}
    for doc, radicals in radicalized_docs.items():
        tf_idf_docs[doc] = {}
        total_terms = sum(radicals.values())
        for radical, count in radicals.items():
            # Term Frequency (TF)
            tf = count / total_terms
            # Inverse Document Frequency (IDF)
            idf = math.log(doc_count / (1 + doc_frequencies[radical]))
            # TF-IDF
            tf_idf_docs[doc][radical] = tf * idf

    # Save the ponderated JSON file
    with open(output_file, 'w', encoding='utf-8') as output_file:
        json.dump(tf_idf_docs, output_file, indent=4, ensure_ascii=False)

    print(f"Ponderated JSON with TF-IDF weights saved to: {output_file.name}")

