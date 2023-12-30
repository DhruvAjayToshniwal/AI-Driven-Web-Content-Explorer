import jsonlines
import openai
from dotenv import load_dotenv
import os
from vectorizer import InCodeVectorDB, load_data, init_openai, create_and_index_embeddings, vectorize_input

load_dotenv()

def retrieve_data_from_jsonl(ids, file_path="train.jsonl"):
    relevant_data = []
    with jsonlines.open(file_path) as f:
        for item in f:
            if item["id"] in ids:
                relevant_data.append(item)
    return relevant_data

def main(query):
    # Initialize components
    train_data = load_data("train.jsonl")
    MODEL = init_openai(os.getenv("OPENAI_API_KEY"))
    vector_db = InCodeVectorDB()
    create_and_index_embeddings(train_data, MODEL, vector_db)

    # Vectorize the query
    query_embedding = vectorize_input(query, MODEL)

    # Search for similar entries
    similar_ids = [result[0] for result in vector_db.search(query_embedding, top_k=3)]
    
    # Retrieve relevant data from train.jsonl
    relevant_entries = retrieve_data_from_jsonl(similar_ids)

    # Formulate the query for OpenAI
    combined_text = ' '.join([entry['text'] for entry in relevant_entries])

    final_query = f"""You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.

Context: {combined_text} 

Question about context: {query}"""
    
    # Send to OpenAI using GPT-3.5 Turbo
    response = openai.Completion.create(engine="text-davinci-003", prompt=final_query, max_tokens=500)
    return response.choices[0].text.strip()

if __name__ == "__main__":
    user_query = input("Enter your query:")
    response = main(user_query)
    print("Response from OpenAI:", response)
