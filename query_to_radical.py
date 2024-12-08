import json
from collections import defaultdict

def query_to_rad():
   
    with open('outputs/knowledge_table.json', 'r', encoding='utf-8') as kt_file:
        knowledge_table = json.load(kt_file)

    with open("input_file.json", 'r', encoding='utf-8') as input_fil:
        tokenized_words = json.load(input_fil)

    # create a mapping from words to radicals
    word_to_radical = {}
    for entry in knowledge_table:
        radical = entry["radical"]
        for word in entry["words"]:
            word_to_radical[word] = radical

    radicalized_words = defaultdict(int)

    # replace tokens with radicals and count appearances
    for word, count in tokenized_words.items():
        if word in word_to_radical:
            radical = word_to_radical[word]
            radicalized_words[radical] += count
        else:
            
            continue

    
    radicalized_words = dict(radicalized_words)

    
    with open("radicalized_query.json", 'w', encoding='utf-8') as output_fil:
        json.dump(radicalized_words, output_fil, indent=4, ensure_ascii=False)

    print(f"Radicalized query saved to: radicalized_query.json")
