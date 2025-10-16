import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer
import uuid


def build_index(questions):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    client = chromadb.PersistentClient(path="./chroma_db")

# Create or load a collection
    collection = client.get_or_create_collection(name="stackoverflow_qa")


    # Suppose we already fetched StackOverflow Q&A from your API
    # questions = [
    #     {"question_id": 1, "title": "How to reverse a list in Python?", "body": "I want to reverse a list efficiently."},
    #     {"question_id": 2, "title": "Difference between list and tuple in Python", "body": "When should I use one over the other?"}
    # ]

    # Create embeddings
    for item in questions:
        text = item['title'] + " " + item.get('body', '') 
        embedding = model.encode(text).tolist()

        collection.add(
            documents=[text],
            embeddings=[embedding],
            ids=[str(uuid.uuid4())],
            metadatas=[{
                "question_title": item['title']
            }]
        )


    print("✅ Index built and saved!")