import time
from tokenization import create_json_output, get_unique_words
    
from radicalization import *


    

def main():
    create_json_output()
    list1= generate_bigramme("astonished")
    list2= generate_bigramme("astonishing")
    print(list1)
    print(list2)
    print(compare_and_match_bigrams(list1, list2))
    print("percentage:", calculate_percentage(list1, list2))
    
    # create_word_bigrams_json()
    
    # print(get_allowed_characters())
    # grouped_words_by_starting_caracter("indexed_docs.json")
    # print(compose_word_from_bigram(compare_and_match_bigrams(list1, list2)))
    # grouped_words_by_two("indexed_docs.json")
    start_time = time.time()
    radicalize_from_texts()
    # radicals_bigrams()
    # radicals_grouping()
    # group_by_radicals_with_duplicates("grouped_words_by_two.json")
    # merge_radicals("grouped_by_radicals_with_duplicates.json", "grouped_by_radicals.json")
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
if __name__ == "__main__":
    main()
