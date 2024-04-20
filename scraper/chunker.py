import os
import hashlib
import json
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
import tiktoken

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

def process_html_file(file_path):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )

    documents = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:  # Add encoding parameter here
            soup = BeautifulSoup(f, 'html.parser')

        text_content = soup.get_text(separator='\n', strip=True)
        m = hashlib.md5()
        m.update(file_path.encode('utf-8'))
        uid = m.hexdigest()[:12]

        chunks = text_splitter.split_text(text_content)
        for i, chunk in enumerate(chunks):
            documents.append({'id': f'{uid}-{i}', 'text': chunk, 'source': file_path})

        os.remove(file_path)
    except Exception as e:
        print(f"Error processing file {os.path.basename(file_path)}: {e}")
    return documents

def process_html_files_parallel(folder_path):
    if not os.path.exists(folder_path):
        print(f"Directory not found: {folder_path}")
        return  # Exit the function if the directory does not exist

    html_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.html')]

    if not html_files:
        print("No HTML files found. Exiting.")
        return

    documents = []
    for file in html_files:
        processed_docs = process_html_file(file)
        documents.extend(processed_docs)

    if documents:
        with open('train.jsonl', 'w') as f:
            for doc in documents:
                f.write(json.dumps(doc) + '\n')
    else:
        print("No documents to write to train.jsonl.")


if __name__ == "__main__":
    folder_path = "websites"
    process_html_files_parallel(folder_path)
