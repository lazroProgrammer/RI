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

# Print the output file path for confirmation
print(f"Radicalized document counts saved to: {output_file_path}")

