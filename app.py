from flask import Flask, render_template, request, redirect, url_for, flash
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer
import requests
import sqlite3
import nltk

# ✅ ดาวน์โหลด punkt ถ้ายังไม่มี
nltk.download("punkt", quiet=True)

app = Flask(__name__)
app.secret_key = "supersecretkey"

# === Summarization Function ===
def summarize_text(text: str, sentence_count: int = 2) -> str:
    text = (text or "").strip()
    if not text:
        return ""
    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentence_count)
        return " ".join(str(s) for s in summary_sentences)
    except Exception as e:
        return f"(summarization error: {e})"

# === Database Setup ===
def init_db():
    with sqlite3.connect("news.db") as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            source TEXT,
            published_at TEXT,
            summary TEXT,
            url TEXT,
            category TEXT
        )""")
init_db()

# === Routes ===
@app.route("/")
def index():
    with sqlite3.connect("news.db") as conn:
        cur = conn.cursor()
        cur.execute("SELECT title, source, published_at, summary, url, category FROM articles ORDER BY id DESC LIMIT 10")
        articles = cur.fetchall()
    return render_template("index.html", articles=articles)

@app.route("/fetch", methods=["POST"])
def fetch():
    category = request.form.get("category", "technology")
    country = request.form.get("country", "us")
    flash(f"Fetching latest {category} news...", "info")

    API_KEY = "YOUR_NEWSAPI_KEY"
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country={country}&apiKey={API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        flash("Failed to fetch news.", "error")
        return redirect(url_for("index"))

    articles = data.get("articles", [])
    summarized_articles = []
    with sqlite3.connect("news.db") as conn:
        for a in articles:
            title = a.get("title", "No title")
            source = a["source"]["name"]
            published_at = a.get("publishedAt", "")
            content = a.get("content", "") or a.get("description", "")
            summary = summarize_text(content)
            url_ = a.get("url", "#")
            conn.execute(
                "INSERT INTO articles (title, source, published_at, summary, url, category) VALUES (?, ?, ?, ?, ?, ?)",
                (title, source, published_at, summary, url_, category)
            )
            summarized_articles.append((title, source, published_at, summary, url_, category))
        conn.commit()

    flash(f"Fetched and summarized {len(summarized_articles)} articles!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)