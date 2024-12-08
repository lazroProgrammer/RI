import json
import os
import re
from pathlib import Path
from collections import Counter


def tokenize(content):
    # remove special characters (keep only letters, numbers, and spaces)
    cleaned_content = re.sub(r'[^\w\s-]|(?<!\w)-|-(?!\w)', '', content)
    
    # split the content into words by spaces
    words = cleaned_content.lower().split()
    return words

def eliminateEmptyWords(tokenized_list: list[str]):
    with open('empty_words.txt', 'r') as file:
        remove_set = {line.strip() for line in file if line.strip() != ""}
    # print(remove_set)
    # filter out lines that are in the remove_set
    filtered_lines = [word for word in tokenized_list if word not in remove_set]
    
    # write to the output file or return the list
    
    return filtered_lines


def get_file_names(folder_path):
    # create a Path object for the folder
    folder = Path(folder_path)
    # use glob to list all files (ignoring directories)
    files = [f.name for f in folder.iterdir() if f.is_file()]
    return files

def process_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        
    words = eliminateEmptyWords(tokenize(content))
    token_count = Counter(words)
    return dict(token_count)



def process_query(query):
    words = eliminateEmptyWords(tokenize(query))
    token_count = Counter(words)
    return dict(token_count)

def tokenize_files():
    result = {}
    files = get_file_names('Collection_TIME')

    for file in files:
        file_path = os.path.join('Collection_TIME', file)
        result[file] = process_file(file_path)

    json_output = json.dumps(result, indent=4)
    with open("outputs/words/indexed_docs.json", 'w', encoding='utf-8') as json_file:
        json_file.write(json_output)

def get_unique_words(json_file):
    unique_words = set()

    with open(json_file, 'r') as file:
        data = json.load(file)  

    for word_list in data.values():
        unique_words.update(word_list)  # add words to the set

    return sorted(unique_words)

