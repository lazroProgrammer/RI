from tokenization import *
from query_to_radical import *
from produit_scalaire import *
import json


def tokenrad(query):
    tokenauery=process_query(query)
    with open("input_file.json", 'w', encoding='utf-8') as input_file:
            json.dump(tokenauery, input_file, indent=4, ensure_ascii=False)

    query_to_rad()
    calculate_similarity()
    

tokenrad("hello aldjelfa enjoyers allied with adrar to do a flip againstn the allied algerians")



