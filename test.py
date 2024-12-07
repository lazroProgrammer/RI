import json
from radicalization import *

word_count=23074
with open('outputs/resulting_radicals/grouped_by_radicalized_radicals.json','r') as radicals_file:
    radical_dict= json.load(radicals_file)
def one_radical_per_term():
# first it was 1931, second one is 1900, third 208, fourth 4
    to_eliminate_count=0
    with open('outputs/words/bigrams.json', 'r') as file:
        words_to_bigram= json.load(file)
    radical_count_per_word={key : len(radical_per_word(key)) for key in words_to_bigram.keys()}
    for key, count in radical_count_per_word.items():
        if count > 1:
            to_eliminate_count += count-1
            
    print(to_eliminate_count,"word duplications left")
    with open("outputs/radicals/radicals_count.json", 'w') as outfile:
        json.dump(radical_count_per_word, outfile, indent=4)        

def radical_per_word(word):
    return [
    entry['radical']
    for entry in radical_dict
    if word in entry['words']
]

def test_bigrams():
    if same_radical("affect","effect"):
        print("test failed")
    else:
        print("test succeded")
        
def find_missed_words(merged_file):
    # load the merged radicals JSON
    with open(merged_file, 'r') as file:
        merged_data = json.load(file)
    with open('outputs/words/bigrams.json') as file:
        words_list=json.load(file)
        
    words_list= words_list.keys()
    # flatten all words in the merged JSON into a single set
    merged_words = set()

    # check if merged_data is a dictionary-based format
    if isinstance(merged_data, dict):
        for words in merged_data.values():
            merged_words.update(words)

    # if merged_data is a list of dictionaries, handle that format
    elif isinstance(merged_data, list):
        for entry in merged_data:
            merged_words.update(entry["words"])
    # find words that are not in the merged JSON
    missed_words = [word for word in words_list if word not in merged_words]
    print("there are",len(missed_words),"missed words out of", len(words_list))
    with open("missed_words.json","w") as file:
        json.dump(missed_words,file,indent=4, sort_keys=True)
    return missed_words
    
def main():
    # find_missed_words('grouped_by_radicals.json')
    find_missed_words('outputs/knowledge_table.json')
    # print(find_missed_words('grouped_by_radicals.json'))
    # find_missed_words('grouped_words_by_two.json')
    # print(find_missed_words('grouped_words_by_two.json'))
    one_radical_per_term()    
if __name__ == "__main__":
    main()