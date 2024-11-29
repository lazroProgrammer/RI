how the algorithm works:
    1- tokenization:
        - tokenize accoarding to whitespaces while eliminate all special caracters excluding the "-" that is between caracters or numbers.
    2- radicalization:
        - it construct for each word a bigram and groups them.
        - it calculates similarity between each elements of a group and get a list of radicals. (similarity is checked from the start of the bigram, if the bigram1(n) != bigram2(n) it calculates the similarity of the resulted set with the dice algorithm (75%))
        - it combines radicals onto their smaller radical that :
            1. has a length bigger than 3. (to balance between eliminating a bit of ambiguity and to not sabotage the search algorithm)
            2. are similar by the 75% in their start
        - construct a knowledge table that has for each radical the corresponding words.
    3- ponderation tf*idf:
     (;<)
    4- search element: 
     (idk how tbh)