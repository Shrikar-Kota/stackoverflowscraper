context = searcher.search(query_embedding, top_k=5)

prompt = f"""
You are a secure coding assistant. Use the following StackOverflow answers as reference.
Don't hallucinate or provide unverified info.

Context:
{context}

User Query:
{query}

Generate a concise and secure solution.
"""
