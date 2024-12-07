import streamlit as st
import json
import os
from tokenization import *
from query_to_radical import *
from produit_scalaire import *
import json

def processQuery_and_class_docs(query):
    tokenauery=process_query(query)
    with open("input_file.json", 'w', encoding='utf-8') as input_file:
            json.dump(tokenauery, input_file, indent=4, ensure_ascii=False)
    query_to_rad()
    produit_scalaire()
    sort_scores()

def search(query):
    processQuery_and_class_docs(query)
    with open("outputs/sorted_score.json") as file:
        documents = json.load(file)
    return [doc for doc, score in documents.items() if score>0]


def display_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content= file.read()
        return content
    except Exception as e:
        return f"Error reading file: {e}"
def extract_preview(content, num_words=24):
    paragraphs = content.split()
    preview = " ".join(paragraphs[:num_words])
    return preview if preview else ""

def interface():    
    query_params = st.query_params
    file_param = query_params.get("file", [None])

    if isinstance(file_param, str) and file_param:
        file_path = os.path.join("Collection_TIME", file_param)
        title = os.path.splitext(file_param)[0]
        st.write(f"## {title}")
        st.write("### Document Content")
        content = display_file_content(file_path)
        st.text(content)
        st.stop()
    else:    
        st.title("The Next GOOGLE ENGINE")
        query = st.text_input("",help="Enter your request")
        search_button = st.button("Search")

        if search_button and query:
            results = search(query)
            if results:
                for doc in results:
                    file_path = os.path.join("Collection_TIME", doc)
                    content = display_file_content(file_path)
                    preview = extract_preview(content)
                    file_url = f"?file={doc}"
                    st.markdown(
                    f'<a href="{file_url}" style="font-size: 24px;">{doc}</a>',
                    unsafe_allow_html=True)
                    st.text(preview + "...")
                    st.markdown(f'<hr>'
                        ,unsafe_allow_html=True)
            else:
                st.write("No results found.")
interface()
