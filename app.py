import time
from test import test
from tokenization import tokenize_files
from radicalization import *
from ponderation import *
from word_to_radical import *


    

def main():
    tokenize_files()
    # list1= generate_bigramme("astonished")
    # list2= generate_bigramme("astonishing")
    # print(list1)
    # print(list2)
    # print(compare_and_match_bigrams(list1, list2))
    # print("percentage:", calculate_percentage(list1, list2))

    create_word_bigrams_json(get_unique_words("outputs/words/indexed_docs.json"),"outputs/words/bigrams.json")
    
    # print(compose_word_from_bigram(compare_and_match_bigrams(list1, list2)))
    # grouped_words_by_two("indexed_docs.json")
    start_time = time.time()
    radicalize_from_texts()
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Execution time: {execution_time:.2f} seconds")
    test()
    word_to_rad()
    transform_doc_word_counts()
    ponderate_tf_idf()
    
if __name__ == "__main__":
    main()
