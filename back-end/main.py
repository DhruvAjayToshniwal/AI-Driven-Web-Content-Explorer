import jsonlines
import openai
from dotenv import load_dotenv
import os
from vectorizer import InCodeVectorDB, load_data, init_openai, create_and_index_embeddings, vectorize_input
import requests

load_dotenv()
output_file = "output.txt"

def get_last_query_and_model(file_path="last_query.txt"):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            model_choice = lines[-1].strip()
            query = ''.join(lines[:-1]).strip()
            return query, model_choice
    except FileNotFoundError:
        return "", ""

def retrieve_data_from_jsonl(ids, file_path="train.jsonl"):
    relevant_data = []
    with jsonlines.open(file_path) as f:
        for item in f:
            if item["id"] in ids:
                relevant_data.append(item)
    return relevant_data

def generate_query(history, new_question, combined_text):
    history_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    final_query = f"""You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
    I will also give you a history of the conversation that the user may have had with you. You could refer to the history and see if the user is asking a follow-up question.
    If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.

    Context: {combined_text}
    
    History: {history_text}
    
    Question about context: {new_question}"""
    return final_query

def main():
    train_data = load_data("train.jsonl")
    MODEL = init_openai(os.getenv("OPENAI_API_KEY"))
    vector_db = InCodeVectorDB()
    create_and_index_embeddings(train_data, MODEL, vector_db)

    last_search_query, model_choice = get_last_query_and_model()
    conversation_history = []

    first_question = last_search_query
    conversation_history.append((first_question, "Search query"))

    process_question(first_question, MODEL, model_choice, vector_db, conversation_history)

def process_question(question, model, model_choice, vector_db, conversation_history):
    query_embedding = vectorize_input(question, model)
    if not vector_db.vectors:
        print("No embeddings in database; please check data loading and embedding creation.")
        return "Error: No embeddings available."

    similar_ids = [result[0] for result in vector_db.search(query_embedding, top_k=3)]
    relevant_entries = retrieve_data_from_jsonl(similar_ids)
    combined_text = ' '.join([entry['text'] for entry in relevant_entries])
    final_query = generate_query(conversation_history, question, combined_text)

    if model_choice.lower() == 'llama3':
        response = requests.post('http://localhost:11434/api/chat', json={
            "model": "llama3",
            "messages": [{"role": "user", "content": final_query}],
            "stream": False
        })
        answer = response.json()['message']['content'].strip()
    else:
        response = openai.Completion.create(engine="gpt-3.5-turbo-instruct", prompt=final_query, max_tokens=500)
        answer = response.choices[0].text.strip()
    print("Response from AI", answer)

    conversation_history.append((question, answer))

    with open(output_file, 'w') as file:
        file.write(answer)

if __name__ == "__main__":
    main()
