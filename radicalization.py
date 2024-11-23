import json
import string
from tokenization import get_unique_words
from collections import defaultdict
def generate_bigramme(string):
    return [string[i:i+2] for i in range(len(string)-1)]

def compare_and_match_bigrams(list1, list2):
    # gives the common bigram part
    result = []
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            result.append(list1[i])
    return result

def compose_word_from_bigram(list1):
    word= list1[0]
    for bigram in list1[1:]:
        word += bigram[1]
    return word

def calculate_percentage(list1, list2):
    # calculate bigram similarity 
    print(len(compare_and_match_bigrams(list1,list2)*2),"/",len(list1),"+",len(list2))
    return len(compare_and_match_bigrams(list1,list2)*2) / (len(list1) + len(list2))

def create_word_bigrams_json():
    # words to bigrams json
    unique_words = get_unique_words('result.json')

    bigrams_dict = {word: generate_bigramme(word) for word in unique_words}

    with open("bigrams.json", 'w') as file:
        json.dump(bigrams_dict, file, indent=4)
        
def find_words_starting_with(json_file, start_char):
    words = get_unique_words(json_file)

    matching_words = [word for word in words if word.lower().startswith(start_char)]

    return matching_words

def get_allowed_characters():
    chars = string.ascii_lowercase + string.digits  
    return sorted(chars)

import json

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

def same_radical(word1, word2):
    bigramme1= generate_bigramme(word1)
    bigramme2= generate_bigramme(word2)
    percentage= calculate_percentage(bigramme1, bigramme2)
    if(calculate_percentage(bigramme1, bigramme2) >0.75):
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
                # if(not(len(word1)*3 <= len(word2))):
                    
                radical = same_radical(word1, word2)
                if radical:
                    visited.add((word1, word2))  # Mark the pair as processed
                    radicals.append({"radical": radical, "words": [word1, word2]})

    # Save the result to a JSON file
    with open('grouped_by_radicals_with_duplicates.json', 'w') as outfile:
        json.dump(radicals, outfile, indent=4)

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
        {"radical": radical, "words": sorted(list(words))}
        for radical, words in merged_radicals.items()
    ]

    # Save the result to the output file
    with open(output_file, 'w') as outfile:
        json.dump(result, outfile, indent=4)

    print(f"Merged radicals saved to {output_file}")