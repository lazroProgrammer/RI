from tokenization import create_json_output
from radicalization import get_pairs, compare_and_match_bigrams, calculate_percentage

def main():
    # create_json_output()
    list1= get_pairs("diverse")
    list2= get_pairs("diversity")
    print(list1)
    print(list2)
    print(compare_and_match_bigrams(list1, list2))
    print("percentage:", calculate_percentage(list1, list2))
    
    
if __name__ == "__main__":
    main()
