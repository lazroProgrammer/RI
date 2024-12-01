import json

def sort_json():
    
    
    with open("outputs/score.json", 'r', encoding='utf-8') as file:
        data = json.load(file)

    sorted_data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))

    with open("outputs/sorted_score.json", 'w', encoding='utf-8') as sorted_file:
        json.dump(sorted_data, sorted_file, indent=4, ensure_ascii=False)
