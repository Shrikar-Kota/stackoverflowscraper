from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle

def build_index(questions):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Suppose we already fetched StackOverflow Q&A from your API
    # questions = [
    #     {"question_id": 1, "title": "How to reverse a list in Python?", "body": "I want to reverse a list efficiently."},
    #     {"question_id": 2, "title": "Difference between list and tuple in Python", "body": "When should I use one over the other?"}
    # ]

    # Create embeddings
    texts = [q["title"] + " " + q["body"] for q in questions]
    embeddings = model.encode(texts, show_progress_bar=True)

    # Convert to numpy array
    embeddings = np.array(embeddings).astype("float32")

    # Create FAISS index
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and metadata
    faiss.write_index(index, "stackoverflow.index")
    with open("questions.pkl", "wb") as f:
        pickle.dump(questions, f)

    print("✅ Index built and saved!")