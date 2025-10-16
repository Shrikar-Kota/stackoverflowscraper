from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

# Load index and data
def load_index(user_query, k=5):  
    model = SentenceTransformer('all-MiniLM-L6-v2')
    index = faiss.read_index("stackoverflow.index")
    with open("questions.pkl", "rb") as f:
        questions = pickle.load(f)

    query_vector = model.encode([user_query]).astype("float32")
    distances, indices = index.search(query_vector, k)
    results = [questions[i] for i in indices[0]]
    return results
