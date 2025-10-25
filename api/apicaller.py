from fastapi import APIRouter, Query
import requests
import time

from service import embedder, searcher

router = APIRouter()

# Base Stack Exchange API URL
STACK_API = "https://api.stackexchange.com/2.3"

@router.get("/accepted")
def get_stackoverflow_accepted(query: str = Query(..., description="User's search query, e.g. 'python keyerror'"),):
    """
    Fetch latest Stack Overflow questions that have accepted answers,
    along with their accepted answer body.
    """
    # Step 1: Get recent questions
    page_number = 1
    questions_url = f"{STACK_API}/search/advanced"
    params = {
        "fromdate" : int(time.time()-63072000),
        "todate" :int(time.time()),
        "order": "desc",
        "sort": "relevance",          # could be "votes" or "creation"
        "pagesize": 100,              # top 50
        "site": "stackoverflow",
        "filter": "withbody",         # get full question text
        "q": query,
        "accepted": True
    }
    results = []    
    answer_set = set()

    while len(results) < 50:
        params["page"] = page_number
        res = requests.get(questions_url, params=params)
        data = res.json()
        print(data)
        
        for q in data["items"]:
            accepted_id = q.get("accepted_answer_id")
            if accepted_id in answer_set:
                continue
            answer_set.add(accepted_id)
            results.append({
                "question_id": q["question_id"],
                "title": q["title"],
                "body": q.get("body", ""),
                "answer_id": accepted_id,
            })
        page_number += 1
        if "items" not in data or not data["has_more"]:
            break
    print(results)

    embedder.build_index(results)
    results = searcher.load_index(query)
    return {"count": len(results), "qa_pairs": results}