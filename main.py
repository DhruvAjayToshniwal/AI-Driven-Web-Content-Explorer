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

def generate_query(history, new_question, combined_text):
    history_text = "\n\n".join([f"Q: {q}\nA: {a}" for q, a in history])
    final_query = f"""You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
    I will also give you a history of the conversation that the user may have had with you. You could refer the history and see if the user is asking a follow up question.
    If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
    If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.

    Context: {combined_text}
    
    History: {history_text}
    
    Question about context: {new_question}"""
    return final_query

def main():
    # Initialize components
    train_data = load_data("train.jsonl")
    MODEL = init_openai(os.getenv("OPENAI_API_KEY"))
    vector_db = InCodeVectorDB()
    create_and_index_embeddings(train_data, MODEL, vector_db)

    conversation_history = []

    while True:
        user_query = input("Enter your query (or type 'exit' to quit): ")
        if user_query.lower() == 'exit':
            break

        # Vectorize the query
        query_embedding = vectorize_input(user_query, MODEL)

        # Search for similar entries
        similar_ids = [result[0] for result in vector_db.search(query_embedding, top_k=3)]
        
        # Retrieve relevant data from train.jsonl
        relevant_entries = retrieve_data_from_jsonl(similar_ids)
        combined_text = ' '.join([entry['text'] for entry in relevant_entries])

        # Formulate the query for OpenAI, including conversation history
        final_query = generate_query(conversation_history, user_query, combined_text)
        
        # Send to OpenAI using GPT-3.5 Turbo
        response = openai.Completion.create(engine="text-davinci-003", prompt=final_query, max_tokens=500)
        answer = response.choices[0].text.strip()

        print("Response from OpenAI:", answer)

        # Update conversation history
        conversation_history.append((user_query, answer))

if __name__ == "__main__":
    main()
