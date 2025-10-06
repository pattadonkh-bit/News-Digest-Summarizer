import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    content TEXT,
    source TEXT,
    url TEXT UNIQUE,
    published_at TEXT,
    category TEXT,
    summary TEXT,
    created_at TEXT DEFAULT (datetime('now'))
);
"""

def init_db(db_path: str):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(SCHEMA)
    conn.commit()
    conn.close()

def insert_article(db_path: str, article: dict, category: str, summary: str = None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO articles (title, description, content, source, url, published_at, category, summary)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        article.get("title"),
        article.get("description"),
        article.get("content"),
        article.get("source"),
        article.get("url"),
        article.get("published_at"),
        category,
        summary
    ))
    conn.commit()
    conn.close()

def get_latest_articles(db_path: str, limit: int = 20, category: str = None):
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    if category:
        cur.execute("SELECT title, source, published_at, summary, url, category FROM articles WHERE category = ? ORDER BY published_at DESC LIMIT ?", (category, limit))
    else:
        cur.execute("SELECT title, source, published_at, summary, url, category FROM articles ORDER BY published_at DESC LIMIT ?", (limit,))
    rows = cur.fetchall()
    conn.close()
    return rows
