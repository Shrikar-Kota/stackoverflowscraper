from openai import OpenAI

client = OpenAI()

@router.post("/answer")
def generate_secure_answer(query: str):
    query_embedding = embedder.embed(query)
    context = searcher.search(query_embedding, top_k=5)
    
    prompt = f"""
    You are a helpful, security-aware coding assistant.
    Use the following verified StackOverflow content:
    {context}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"answer": response.choices[0].message["content"]}
