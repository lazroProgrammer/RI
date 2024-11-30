import time
from tokenization import create_json_output, get_unique_words
    
from radicalization import *

with open('outputs\knowledge_table.json','r') as radicals_js:
    data= json.load(radicals_js)

radicals = [entry["radical"] for entry in data]

with open('outputs/bobo.json','w') as rad:
    json.dump(radicals,rad, indent=4,sort_keys=True)
