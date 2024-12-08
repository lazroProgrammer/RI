import json
from radicalization import *

word_count=23074

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
    with open('outputs/resulting_radicals/grouped_by_radicalized_radicals.json','r') as radicals_file:
        radical_dict= json.load(radicals_file)
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
        

    
def test():
    # find_missed_words('grouped_by_radicals.json')
    find_missed_words('outputs/knowledge_table.json')
    # print(find_missed_words('grouped_by_radicals.json'))
    # find_missed_words('grouped_words_by_two.json')
    # print(find_missed_words('grouped_words_by_two.json'))
    one_radical_per_term()    