import os
import openai
import jsonlines
import pinecone

# Pinecone setup
pinecone_api_key = ''
pinecone.init(api_key=pinecone_api_key, environment='')

# Initialize Pinecone Index
index_name = ""
embedding_dimension = 1536
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=embedding_dimension)
index = pinecone.Index(index_name)

# Function to initialize OpenAI API
def init_openai(api_key):
    openai.api_key = api_key
    return "text-embedding-ada-002"

# Function to create embeddings and populate the Pinecone database
def create_and_index_embeddings(file_path, model):
    with jsonlines.open(file_path) as f:
        for item in f:
            text = item["text"]
            res = openai.Embedding.create(input=text, engine=model)
            embedding = res["data"][0]["embedding"]
            index.upsert(vectors={item["id"]: embedding})

# Function to vectorize a single input query
def vectorize_input(query, model):
    res = openai.Embedding.create(input=query, engine=model)
    return res["data"][0]["embedding"]

# Function to search in Pinecone Index
def search(query_vector, top_k=1):
    query_results = index.query([query_vector.tolist()], top_k=top_k)
    return [(match["id"], match["score"]) for match in query_results["matches"]]