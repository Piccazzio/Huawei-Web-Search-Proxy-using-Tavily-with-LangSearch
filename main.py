import requests
import time
import hashlib
from datetime import datetime, timedelta
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()

TAVILY_URL = "https://api.tavily.com/search"
MONTHLY_LIMIT = 1000


request_count = 0

def get_next_month_reset():
    now = datetime.now()

    next_month = now.replace(day=28) + timedelta(days=4)

    first_day_next_month = next_month.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )

    return first_day_next_month.timestamp()


reset_timestamp = get_next_month_reset()


CACHE_TTL = 60 * 60 * 24  
cache = {}


def normalize_query(query: str):
    return query.strip().lower()


def cache_key(query: str):
    return hashlib.md5(query.encode()).hexdigest()


def is_cache_valid(entry):
    return time.time() - entry["timestamp"] < CACHE_TTL


def check_quota():
    global request_count, reset_timestamp

    now = datetime.now().timestamp()

    if now > reset_timestamp:
        request_count = 0
        reset_timestamp = get_next_month_reset()

    if request_count >= MONTHLY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Monthly Tavily quota exceeded (1000 requests)"
        )

    request_count += 1


def transform_to_langsearch(tavily_json):
    query = tavily_json.get("query", "")
    results = tavily_json.get("results", [])

    values = []

    for i, r in enumerate(results):
        values.append({
            "id": f"https://api.langsearch.com/v1/#WebPages.{i+1}",
            "name": r.get("title"),
            "url": r.get("url"),
            "displayUrl": r.get("url"),
            "snippet": r.get("content"),
            "summary": r.get("content"),
            "datePublished": None,
            "dateLastCrawled": None
        })

    return {
        "code": 200,
        "msg": None,
        "data": {
            "_type": "SearchResponse",
            "queryContext": {
                "originalQuery": query
            },
            "webPages": {
                "webSearchUrl": f"https://langsearch.com/search?q={query}",
                "totalEstimatedMatches": len(values),
                "value": values
            }
        }
    }


@app.post("/search")
async def search(request: Request):

    body = await request.json()
    query = body.get("query")

    if not query:
        raise HTTPException(status_code=400, detail="Missing query")

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    normalized = normalize_query(query)
    key = cache_key(normalized)

    if key in cache and is_cache_valid(cache[key]):
        return cache[key]["data"]

    check_quota()

    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }

    response = requests.post(
        TAVILY_URL,
        headers=headers,
        json={"query": query},
        timeout=10
    )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Tavily error: {response.text}"
        )

    tavily_json = response.json()

    transformed = transform_to_langsearch(tavily_json)

    cache[key] = {
        "timestamp": time.time(),
        "data": transformed
    }

    return transformed


@app.get("/health")
def health():
    return {
        "status": "ok",
        "requests_used": request_count,
        "monthly_limit": MONTHLY_LIMIT,
        "remaining": MONTHLY_LIMIT - request_count,
        "reset_at": datetime.fromtimestamp(reset_timestamp).isoformat(),
        "cache_entries": len(cache)
    }