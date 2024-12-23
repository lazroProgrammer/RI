from tokenization import tokenize_files, get_unique_words 
from radicalization import *
import json
from collections import defaultdict
def word_to_rad() :
    # produces all indexes of the docs with radicals instead of words and their counts
    with open('outputs/knowledge_table.json', 'r') as kt_file:
        knowledge_table = json.load(kt_file)

    with open("outputs/words/indexed_docs.json", 'r') as docs_file:
        tokenized_docs = json.load(docs_file)

    word_to_radical = {}
    for entry in knowledge_table:
        radical = entry["radical"]
        for word in entry["words"]:
            word_to_radical[word] = radical

    # format it to {"doc":{"radical": count}}
    radicalized_docs = defaultdict(lambda: defaultdict(int))

    # replace tokens with radicals and count appearances
    for doc_name, word_counts in tokenized_docs.items():
        for word, count in word_counts.items():
            if word in word_to_radical:
                radical = word_to_radical[word]
                radicalized_docs[doc_name][radical] += count
            else:
                # if the word doesn't have a corresponding radical skip 
                continue

    # convert defaultdict to a regular dictionary for saving
    radicalized_docs = {doc: dict(counts) for doc, counts in radicalized_docs.items()}

    with open('radicalized_docs_count.json', 'w', encoding='utf-8') as output_file:
        json.dump(radicalized_docs, output_file, indent=4, ensure_ascii=False)

def transform_doc_word_counts():
    with open("radicalized_docs_count.json", 'r') as file:
        radicalized_docs = json.load(file)

    fichier_inverse = defaultdict(lambda: {"nb_docs": 0, "docs": {}})
    
    for doc, word_counts in radicalized_docs.items():
        for word, count in word_counts.items():
            if word not in fichier_inverse:
                fichier_inverse[word] = {"nb_docs": 0, "docs": {}}
            fichier_inverse[word]["docs"][doc] = count
            fichier_inverse[word]["nb_docs"] += 1

    transformed_output = [{"word": word, "nb_docs": data["nb_docs"], "docs": data["docs"]} for word, data in fichier_inverse.items()]

    with open("fichier_inverse.json", 'w', encoding='utf-8') as output_file:
        json.dump(transformed_output, output_file, indent=4, ensure_ascii=False)
