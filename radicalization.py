import json
import string
from tokenization import get_unique_words
from collections import defaultdict

with open("bigrams.json") as file:
    words_bigrams=json.load(file)
with open("radicals_bigram.json") as file2:
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
    word= list1[0]
    for bigram in list1[1:]:
        word += bigram[1]
    return word

def calculate_percentage(list1, list2):
    # calculate bigram similarity 
    
    return len(compare_and_match_bigrams(list1,list2)*2) / (len(list1) + len(list2))

def create_word_bigrams_json(list: list[str], output):
    # words to bigrams json
    # unique_words = get_unique_words('indexed_docs.json')

    bigrams_dict = {word: generate_bigramme(word) for word in list}

    write_json(output,bigrams_dict)
        
def find_words_starting_with(json_file, start_char):
    words = get_unique_words(json_file)

    matching_words = [word for word in words if word.lower().startswith(start_char)]

    return matching_words

def get_allowed_characters():
    chars = string.ascii_lowercase + string.digits  
    return sorted(chars)

def grouped_words_by_starting_caracter(json_file):
    allowed_characters = get_allowed_characters() 
    words_grouped = {char: [] for char in allowed_characters}
    data = get_unique_words(json_file)

    for word in data:
        first_char = word[0].lower()
        if first_char in words_grouped:
            words_grouped[first_char].append(word)

    with open('grouped_words.json', 'w') as outfile:
        json.dump(words_grouped, outfile, indent=4, sort_keys=True)

    print("Grouped words saved to 'grouped_words.json'")

def same_radical(word1, word2, isWord):
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
    
def group_by_radicals_with_duplicates(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)  # Load JSON file

    radicals = []  # To store lists of words grouped by radicals

    for char, words in data.items():
        visited = set()  # To avoid reprocessing the same word pairs
        for i, word1 in enumerate(words):
            for word2 in words[i + 1:]:
                if (word1, word2) in visited or (word2, word1) in visited:
                    continue  # Skip already processed pairs
                    
                radical = same_radical(word1, word2,True)
                if radical:
                    visited.add((word1, word2))  # Mark the pair as processed
                    radicals.append({"radical": radical, "words": [word1, word2]})

    # Save the result to a JSON file
    write_json('grouped_by_radicals_with_duplicates.json',radicals) 

def grouped_words_by_two(json_file):
    bigram_groups = {}

    # Get unique words from the JSON file
    words = get_unique_words(json_file)

    # Process each word in the dataset
    for word in words:
        if len(word) > 1:  # Only consider words with at least two characters
            bigram = word[:2].lower()  # Extract the first two characters (bigram)
            if bigram not in bigram_groups:
                bigram_groups[bigram] = []  # Initialize a new group for this bigram
            bigram_groups[bigram].append(word)  # Add the word to the bigram's group

    # Remove duplicate words in each bigram group
    for bigram in bigram_groups:
        bigram_groups[bigram] = list(set(bigram_groups[bigram]))

    with open('grouped_words_by_two.json', 'w') as outfile:
        json.dump(bigram_groups, outfile, indent=4, sort_keys=True)

def grouped_words_by_two_using_json(bigram_json_file):
    with open(bigram_json_file, 'r') as infile:
        bigram_data = json.load(infile)

    # Output dictionary for optimized grouping
    optimized_groups = {}

    # Process each bigram and its associated words
    for bigram, words in bigram_data.items():
        unique_words = list(set(words))  # Remove duplicates
        optimized_groups[bigram] = sorted(unique_words)  # Sort words for consistency

    # Write the output to a JSON file
    with open('optimized_grouped_words_by_two.json', 'w') as outfile:
        json.dump(optimized_groups, outfile, indent=4, sort_keys=True)
        

def merge_radicals(input_file, output_file):
    """
    Merges entries with duplicate radicals in a list of dictionaries, combining their word lists.

    Args:
        input_file (str): Path to the input JSON file.
        output_file (str): Path to save the merged JSON output.

    Returns:
        None: The merged JSON is saved to `output_file`.
    """
    # Load the input JSON
    with open(input_file, 'r') as infile:
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

    # Save the result to the output file
    write_json(output_file, result)

    print(f"Merged radicals saved to {output_file}")
    
def radicals_bigrams():
    with open("grouped_by_radicals.json","r") as file:
        radicals_dict=json.load(file)
    radicals=[entry["radical"] for entry in radicals_dict]
    create_word_bigrams_json(radicals,"radicals_bigram.json")
    
def radicals_grouping():
    with open("radicals_bigram.json","r") as file:
        radicals_to_bigrams= json.load(file)
        visited = set()
        radicals=[]
        list1 = list(radicals_to_bigrams.keys())
        # print(len(list1))
    for i, radical1 in enumerate(list1):
        for radical2 in list1[i + 1:]:
            if (radical1, radical2) in visited or (radical2, radical1) in visited:
                    continue  # Skip already processed pairs
            # if len(radical1)>=4 & len(radical2)>=4:                    
            radical = same_radical(radical1, radical2, False)
            if radical:
                visited.add((radical1, radical2))  # Mark the pair as processed
                radicals.append({"radical": radical, "radicals": [radical1, radical2]})
    write_json("radicalized_radicals.json", radicals)
def merge_radicals_of_radicals(input_file, output_file):
    with open(input_file, 'r') as infile:
        data = json.load(infile)

    # Use a dictionary to group words by radical
    merged_radicals = defaultdict(set)

    # Process each entry to merge words by radical
    for entry in data:
        radical = entry["radical"]
        words = entry["radicals"]
        merged_radicals[radical].update(words)

    # Convert the result back to a list of dictionaries
    result = [
        {"radical": radical, "radicals": sorted(list(merged_radicals[radical]))}
        for radical in sorted(merged_radicals.keys())
    ]

    # Save the result to the output file
    write_json(output_file, result)

    print(f"Merged radicals saved to {output_file}")
 
def remove_radicalized_radicals():
    with open("non_duplicated_radicalized_radicals.json") as file:
        radic_dict= json.load(file)
    radical_map = {}

    for entry in radic_dict:
        radical = entry["radical"]
        radicals = set(entry["radicals"])  # Use a set to avoid duplicates

        # Ensure the radical itself is included in the set
        radicals.add(radical)

        if radical in radical_map:
            radical_map[radical].update(radicals)  # Add to existing radical
        else:
            # Check if any existing radical overlaps with the current radicals
            found = False
            for key in list(radical_map.keys()):  # Use list to avoid runtime errors
                if radical in radical_map[key] or key in radicals:
                    radical_map[key].update(radicals)
                    found = True
                    break
            if not found:
                radical_map[radical] = radicals

    # Reconstruct the JSON
    result= [
        {"radical": key, "radicals": sorted(list(radicals))}
        for key, radicals in radical_map.items()
    ]
    write_json("merged_radicals_groups.json",result)
    
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
    write_json("grouped_by_radicalized_radicals.json",output_data)
    
def radicalize_from_texts():
    group_by_radicals_with_duplicates("grouped_words_by_two.json")
    merge_radicals("grouped_by_radicals_with_duplicates.json", "grouped_by_radicals.json")
    radicals_bigrams()
    radicals_grouping()
    merge_radicals_of_radicals("radicalized_radicals.json","non_duplicated_radicalized_radicals.json")
    remove_radicalized_radicals()
    merge_radicals_and_words("grouped_by_radicals.json","non_duplicated_radicalized_radicals.json")