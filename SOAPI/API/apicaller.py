from fastapi import FastAPI
import requests

app = FastAPI(title="StackOverflow Secure QA API")

# Base Stack Exchange API URL
STACK_API = "https://api.stackexchange.com/2.3"

@app.get("/stackoverflow/accepted")
def get_stackoverflow_accepted():
    """
    Fetch latest Stack Overflow questions that have accepted answers,
    along with their accepted answer body.
    """
    # Step 1: Get recent questions
    questions_url = f"{STACK_API}/questions"
    params = {
        "order": "desc",
        "sort": "activity",          # could be "votes" or "creation"
        "pagesize": 100,              # top 50
        "site": "stackoverflow",
        "filter": "withbody"         # get full question text
    }
    results = []    

    while len(results) < 50:
        res = requests.get(questions_url, params=params)
        data = res.json()

        if "items" not in data:
            return {"error": "Failed to fetch questions", "details": data}

        # Step 2: Loop through questions that have accepted answers
        for q in data["items"]:
            accepted_id = q.get("accepted_answer_id")
            if not accepted_id:
                continue  # skip questions without accepted answer

            # Step 3: Fetch accepted answer details
            answer_url = f"{STACK_API}/answers/{accepted_id}"
            ans_params = {
                "order": "desc",
                "sort": "activity",
                "site": "stackoverflow",
                "filter": "withbody"      # get answer text
            }
            ans_res = requests.get(answer_url, params=ans_params)
            ans_data = ans_res.json()

            if "items" not in ans_data or not ans_data["items"]:
                continue

            answer = ans_data["items"][0]

            # Step 4: Construct a clean record for RAG
            results.append({
                # "question_id": q["question_id"],
                "question_title": q["title"],
                "question_body": q.get("body", ""),
                # "question_score": q.get("score", 0),
                # "answer_id": accepted_id,
                "answer_body": answer.get("body", ""),
                # "answer_score": answer.get("score", 0),
                # "link": q["link"]
            })

    return {"count": len(results), "qa_pairs": results}
