from tokenization import tokenize, eliminateEmptyWords


def main():
    file_name = "Collection_TIME/017.txt"
    print(
    eliminateEmptyWords(tokenize(file_name))
          )

if __name__ == "__main__":
    main()
