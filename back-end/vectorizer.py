import numpy as np
import jsonlines
import openai

class InCodeVectorDB:
    def __init__(self):
        self.vectors = []
        self.ids = []

    def add_vector(self, vec_id, vector):
        self.ids.append(vec_id)
        self.vectors.append(vector)

    def search(self, query_vector, top_k=1):
        vectors = np.array(self.vectors)
        query_vector = np.array(query_vector)

        distances = np.linalg.norm(vectors - query_vector, axis=1)

        nearest_indices = np.argsort(distances)[:top_k]

        return [(self.ids[i], distances[i]) for i in nearest_indices]

def load_data(file_path):
    data = []
    try:
        with jsonlines.open(file_path) as f:
            for item in f:
                data.append(item)
    except jsonlines.jsonlines.Error as e:
        print(f"Error loading data: {e}")
    return data

def init_openai(api_key):
    openai.api_key = api_key
    return "text-embedding-ada-002"

def create_and_index_embeddings(data, model, db):
    if not data:
        print("No data to process for embeddings.")
        return
    for item in data:
        text = item["text"]
        try:
            res = openai.Embedding.create(input=text, engine=model)
            embedding = res["data"][0]["embedding"]
            db.add_vector(item["id"], embedding)
        except Exception as e:
            print(f"Failed to create embedding for {text}: {e}")

def vectorize_input(query, model):
    res = openai.Embedding.create(input=query, engine=model)
    return res["data"][0]["embedding"]
