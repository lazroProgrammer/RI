import re
def tokenize(file_name):
    # Read the content of the file
    with open(file_name, 'r') as file:
        content = file.read()

    # Remove special characters (keep only letters, numbers, and spaces)
    cleaned_content = re.sub(r'[^\w\s-]|(?<!\w)-|-(?!\w)', '', content)
    
    # Split the content into words by spaces
    words = cleaned_content.lower().split()
    
    return words
def eliminateEmptyWords(tokenized_list: list[str]):
    with open('empty_words.txt', 'r') as file:
        remove_set = {line.strip() for line in file if line.strip() != ""}
    # print(remove_set)
    # Filter out lines that are in the remove_set
    filtered_lines = [word for word in tokenized_list if word not in remove_set]
    
    # Write to the output file or return the list
    
    return filtered_lines
