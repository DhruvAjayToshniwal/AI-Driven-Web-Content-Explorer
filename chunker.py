import os
import hashlib
import json
import multiprocessing
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from tqdm.auto import tqdm
import tiktoken

def tiktoken_len(text):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    tokens = tokenizer.encode(text, disallowed_special=())
    return len(tokens)

def process_html_file(file_path):
    tokenizer = tiktoken.get_encoding('cl100k_base')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=400,
        chunk_overlap=20,
        length_function=tiktoken_len,
        separators=['\n\n', '\n', ' ', '']
    )

    documents = []
    try:
        with open(file_path, 'r') as f:
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

    print(f"Processed {len(documents)} chunks from {os.path.basename(file_path)}")  # Debugging line
    return documents

def process_html_files_parallel(folder_path):
    html_files = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.html')]
    print(f"Found {len(html_files)} HTML files.")  # Debugging line

    if not html_files:
        print("No HTML files found. Exiting.")
        return

    full_html_files = [os.path.abspath(file) for file in html_files]
    with multiprocessing.Pool() as pool:
        results = pool.map(process_html_file, full_html_files)
    
    documents = [doc for sublist in results for doc in sublist]
    print(f"Generated {len(documents)} documents.")  # Debugging line

    with open('train.jsonl', 'w') as f:
        for doc in documents:
            f.write(json.dumps(doc) + '\n')


if __name__ == "__main__":
    folder_path = "websites"
    process_html_files_parallel(folder_path)
