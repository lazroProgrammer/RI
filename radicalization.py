def get_pairs(string):
    return [string[i:i+2] for i in range(len(string)-1)]

def compare_and_match_bigrams(list1, list2):
    result = []
    for i in range(min(len(list1), len(list2))):
        if list1[i] == list2[i]:
            result.append(list1[i])
    return result

def calculate_percentage(list1, list2):
    print(len(compare_and_match_bigrams(list1,list2)*2),"/",len(list1),"+",len(list2))
    return len(compare_and_match_bigrams(list1,list2)*2) / (len(list1) + len(list2))