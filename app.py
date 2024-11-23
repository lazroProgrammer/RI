from tokenization import create_json_output


def main():
    with open('result.json', 'w', encoding='utf-8') as json_file:
        json_file.write(create_json_output())
    
if __name__ == "__main__":
    main()
