import chromadb




# Load index and data
def load_index(user_query, k=5):  
    client = chromadb.PersistentClient(path="./chroma_db")

# Retrieve the same collection
    collection = client.get_collection("stackoverflow_qa")

    results = collection.query(query_texts=["how to fix keyerror in python"], n_results=k)
    return results


    # model = SentenceTransformer('all-MiniLM-L6-v2')
    # index = faiss.read_index("stackoverflow.index")
    # with open("questions.pkl", "rb") as f:
    #     questions = pickle.load(f)

    # query_vector = model.encode([user_query]).astype("float32")
    # distances, indices = index.search(query_vector, k)
    # results = [questions[i] for i in indices[0]]
    # return results
