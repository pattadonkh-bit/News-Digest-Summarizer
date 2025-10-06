import requests

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"

def fetch_top_headlines(api_key: str, category: str = "technology", country: str = "us", page_size: int = 20):
    """
    ดึงข่าวจาก NewsAPI โดยใช้ category, country, และจำนวนข่าวที่ต้องการ
    จะคืนค่าเป็น list ของ dict ที่มี key: title, description, content, source, published_at, url
    """
    headers = {"Authorization": api_key}
    params = {"category": category, "country": country, "pageSize": page_size}

    try:
        resp = requests.get(NEWSAPI_URL, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        # ตรวจสอบว่ามี articles จริงไหม
        if "articles" not in data:
            print("Warning: No articles found in response.")
            return []

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

    except requests.exceptions.RequestException as e:
        print(f"[fetch_top_headlines] Network or API error: {e}")
        return []
    except Exception as e:
        print(f"[fetch_top_headlines] Unexpected error: {e}")
        return []
