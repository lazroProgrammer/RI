how the algorithm works:
    1- tokenization:
        - tokenize accoarding to whitespaces while eliminate all special caracters excluding the "-" that is between caracters or numbers.
    2- radicalization:
        - it construct for each word a bigram and groups them by the starting caracter (for now).
        - it calculate similarity between each elements of a group
        - construct a knowledge table that has for each radical the corresponding words.
    3- ponderation tf*idf:
     (;<)
    4- search element: 
     (idk how tbh)