from openai import OpenAI

client = OpenAI(api_key="#####")

def generate_consolidated_answer(user_query, answers):
    """
    user_query: str — the original user question
    answers: list of dicts [{"answer_id": ..., "body": ...}, ...]
    """
    # Combine answer bodies (you can truncate to keep under token limits)
    combined_text = "\n\n".join(
        [f"Answer {a['answer_id']}:\n{a['body']}" for a in answers]
    )

    prompt = f"""
        You are a helpful and security-conscious AI assistant. 
        Summarize the key ideas from the following Stack Overflow answers to provide a single clear, concise explanation. 
        Preserve any important examples or code snippets, and note if answers disagree.

        User query:
        {user_query}

        Stack Overflow answers:
        {combined_text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )

    return response.choices[0].message.content