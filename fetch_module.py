import requests

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

def fetch_top_headlines(api_key: str, category: str = "technology", country: str = "us", page_size: int = 20):
    headers = {"Authorization": api_key}
    params = {"category": category, "country": country, "pageSize": page_size}
    resp = requests.get(NEWSAPI_URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    data = resp.json()

    articles = []
    for a in data.get("articles", []):
        articles.append({
            "title": a.get("title"),
            "description": a.get("description") or "",
            "content": a.get("content") or "",
            "source": (a.get("source") or {}).get("name"),
            "published_at": a.get("publishedAt"),
            "url": a.get("url")
        })
    return articles
