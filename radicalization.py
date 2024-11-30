import json
import string
from tokenization import get_unique_words
from test import *
from collections import defaultdict

with open("outputs/words/bigrams.json") as file:
    words_bigrams=json.load(file)
with open("outputs/radicals/radicals_bigram.json") as file2:
    radicals_bigram=json.load(file2)
    
def write_json(name, data):
    with open(name, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)
        
def generate_bigramme(string):
    return [string[i:i+2] for i in range(len(string)-1)]

def compare_and_match_bigrams(list1, list2):
    # gives the common bigram part
    result = []
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            result.append(list1[i])
        else:
            break
    return result

def compose_word_from_bigram(list1):
    # bigram to word
    word= list1[0]
    for bigram in list1[1:]:
        word += bigram[1]
    return word

def calculate_percentage(list1, list2):
    # calculate bigram similarity 
    return len(compare_and_match_bigrams(list1,list2)*2) / (len(list1) + len(list2))

def create_word_bigrams_json(list: list[str], output):
    # words to bigrams dictionary

    bigrams_dict = {word: generate_bigramme(word) for word in list}
    write_json(output,bigrams_dict)
        
def find_words_starting_with(input_json_file, start_char):
    words = get_unique_words(input_json_file)
    matching_words = [word for word in words if word.lower().startswith(start_char)]
    return matching_words

def same_radical(word1, word2, isWord):
    # if the two words are simmilar, it gives the radical
    # else it gives none
    if isWord:
        bigramme1=words_bigrams[word1]
        bigramme2=words_bigrams[word2]
    else:
        bigramme1= radicals_bigram[word1]
        bigramme2= radicals_bigram[word2]
    percentage= calculate_percentage(bigramme1, bigramme2)
    if(percentage >0.75):
        return compose_word_from_bigram(compare_and_match_bigrams(bigramme1, bigramme2))
    else:
        return None
    
def group_by_radicals_with_duplicates(input_json_file):
    # groupes words that have a radical two by two
    with open(input_json_file, 'r') as file:
        data = json.load(file)  

    radicals = []

    for char, words in data.items():
        # memoizing
        visited = set()  
        for i, word1 in enumerate(words):
            for word2 in words[i + 1:]:
                if (word1, word2) in visited or (word2, word1) in visited:
                    continue  # Skip already processed pairs
                    
                radical = same_radical(word1, word2,True)
                if radical:
                    visited.add((word1, word2))  # add it to the memo
                    radicals.append({"radical": radical, "words": [word1, word2]})

    write_json('outputs/grouped_by_radicals_with_duplicates.json',radicals) 

def grouped_words_by_two(input_json_file):
    # group words by the first bigram (to make the algorithm faster)
    bigram_groups = {}

    words = get_unique_words(input_json_file)

    # Process each word in the dataset
    for word in words:
        if len(word) > 1:  # word needs to be 2 or bigger to process it
            bigram = word[:2].lower()  # get the first 2 characters
            if bigram not in bigram_groups:
                bigram_groups[bigram] = []
            bigram_groups[bigram].append(word)

    # Remove duplicate words in each bigram group
    for bigram in bigram_groups:
        bigram_groups[bigram] = list(set(bigram_groups[bigram]))

    write_json('outputs/grouped_words_by_two.json', bigram_groups)
        

def merge_radicals(input_file, output_file):
    # merge words that have the same radical 
    
    with open(input_file, 'r') as infile: # here it's the grouped_by_radicals.json
        data = json.load(infile)

    # Use a dictionary to group words by radical
    merged_radicals = defaultdict(set)

    # Process each entry to merge words by radical
    for entry in data:
        radical = entry["radical"]
        words = entry["words"]
        merged_radicals[radical].update(words)

    # Convert the result back to a list of dictionaries
    result = [
        {"radical": radical, "words": sorted(list(merged_radicals[radical]))}
        for radical in sorted(merged_radicals.keys())
    ]

    write_json(output_file, result)
    
def radicals_bigrams():
    #bigrams of the all radicals (before elimination)
    with open("outputs/grouped_by_radicals.json","r") as file:
        radicals_dict=json.load(file)
    radicals=[entry["radical"] for entry in radicals_dict]
    create_word_bigrams_json(radicals,"outputs/radicals_bigram.json")
    
def radicals_grouping():
    # groups radicals that have more than a 75% similarity level two by two
    with open("outputs/radicals_bigram.json","r") as file:
        radicals_to_bigrams= json.load(file)
        # memoizing
        visited = set()
        radicalized_radicals=[]
        radicals = list(radicals_to_bigrams.keys()) 
        # print(len(list1))
    for i, radical1 in enumerate(radicals):
        for radical2 in radicals[i + 1:]:
            if (radical1, radical2) in visited or (radical2, radical1) in visited:
                    continue  # Skip already processed pairs
            # if len(radical1)>=4 & len(radical2)>=4:                    
            radical = same_radical(radical1, radical2, False)
            if radical:
                visited.add((radical1, radical2))  # Mark the pair as processed
                radicalized_radicals.append({"radical": radical, "radicals": [radical1, radical2]})
    write_json("outputs/radicalized_radicals.json", radicalized_radicals)
    
def merge_radicals_of_radicals(input_file, output_file):
    # merge the radicalized radicals
    # same job as the mergeRadicals(), different inputfile format 
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    merged_radicals = defaultdict(set)

    for entry in data:
        radical = entry["radical"]
        words = entry["radicals"]
        merged_radicals[radical].update(words)

    result = [
        {"radical": radical, "radicals": sorted(list(merged_radicals[radical]))}
        for radical in sorted(merged_radicals.keys())
    ]

    write_json(output_file, result)
 
def remove_radicalized_radicals():
    # group each radical group with the smallest common radical

    with open("outputs/non_duplicated_radicalized_radicals.json") as file:
        radic_dict= json.load(file)
    radical_map = {}

    for entry in radic_dict:
        radical = entry["radical"]
        radicals = set(entry["radicals"])  # get unique radicals

        # add radical to the radical group 
        radicals.add(radical)
            # if the radical is included in the map it puts the 
        if radical in radical_map:
            # just to make sure it doesn't slip
            radical_map[radical].update(radicals)  # Adds the radicals to the set 
        else:
            found = False
            # see if the radical is already in a group corresponding to some radical
            for key in list(radical_map.keys()):
                if radical in radical_map[key] or key in radicals:
                    radical_map[key].update(radicals)
                    found = True
                    break
                #if it's not found, add it to the radical_map
            if not found:
                radical_map[radical] = radicals

    # Format the json
    result= [
        {"radical": key, "radicals": sorted(list(radicals))}
        for key, radicals in radical_map.items()
    ]
    write_json("outputs/merged_radicals_groups.json",result)
    
def merge_radicals_and_words(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        words_data = json.load(f1)
        radicalized_data = json.load(f2)

    # Build a map of radicals to words from File 1
    words_by_radical = {
        entry["radical"]: set(entry["words"]) for entry in words_data
    }

    # Helper function to recursively gather all connected radicals
    def gather_radicals(radical, radical_map, visited=None):
        if visited is None:
            visited = set()
        if radical in visited:
            return set()  # Avoid cycles
        visited.add(radical)
        result = set([radical])
        if radical in radical_map:
            for related in radical_map[radical]:
                result.update(gather_radicals(related, radical_map, visited))
        return result

    # Build a map of radical relationships from File 2
    radical_relationships = {
        entry["radical"]: entry["radicals"] for entry in radicalized_data
    }

    # Process relationships to resolve all groups
    resolved_radicals = {}
    for radical in radical_relationships:
        if radical not in resolved_radicals:
            all_related = gather_radicals(radical, radical_relationships)
            for r in all_related:
                resolved_radicals[r] = all_related

    # Merge words based on resolved radical groups
    merged_data = {}
    for group in resolved_radicals.values():
        main_radical = min(group)  # Use the lexicographically smallest radical
        combined_words = set()
        for radical in group:
            if radical in words_by_radical:
                combined_words.update(words_by_radical.pop(radical))
        if main_radical not in merged_data:
            merged_data[main_radical] = set()
        merged_data[main_radical].update(combined_words)

    # Add remaining standalone radicals from File 1
    for radical, words in words_by_radical.items():
        if radical not in merged_data:
            merged_data[radical] = words

    # Convert the merged data to the required JSON structure
    output_data = [
        {"radical": radical, "words": sorted(words)} for radical, words in merged_data.items()
    ]
    write_json("outputs/resulting_radicals/grouped_by_radicalized_radicals.json",output_data)
def knowledge_table(radicals_file, missing_words):
    with open(radicals_file) as file:
        radicals_dict= json.load(file)
    new_entries = []

    for word in missing_words:
        if not any(entry["radical"] == word for entry in radicals_dict):
            new_entries.append({
                "radical": word, 
                "words": [word]   
            })

    # If there are new entries, append them to the original list
    if new_entries:
        radicals_dict.extend(new_entries)
        print(f"Added {len(new_entries)} new entries.")
    else:
        print("No new words to add.")

    write_json("outputs/knowledge_table.json", radicals_dict)
      
    
def radicalize_from_texts():
    # group_by_radicals_with_duplicates("outputs/grouped_words_by_two.json")
    # merge_radicals("outputs/grouped_by_radicals_with_duplicates.json", "outputs/grouped_by_radicals.json")
    # radicals_bigrams()
    # radicals_grouping()
    # merge_radicals_of_radicals("outputs/radicalized_radicals.json","outputs/non_duplicated_radicalized_radicals.json")
    # remove_radicalized_radicals()
    # merge_radicals_and_words("outputs/grouped_by_radicals.json","outputs/non_duplicated_radicalized_radicals.json")
    knowledge_table("outputs/resulting_radicals/grouped_by_radicalized_radicals.json",find_missed_words('grouped_by_radicals.json'))