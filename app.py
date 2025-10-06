from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os

from fetch_module import fetch_top_headlines
from summarizer_module import summarize_text
from db_module import init_db, insert_article, get_latest_articles

load_dotenv()

app = Flask(__name__)
app.secret_key = "newsdigest-secret"

API_KEY = os.getenv("NEWSAPI_KEY")
DB_PATH = os.getenv("DB_PATH", "./db/news.db")

# Initialize DB
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
init_db(DB_PATH)


@app.route("/")
def index():
    articles = get_latest_articles(DB_PATH, limit=15)
    return render_template("index.html", articles=articles)


@app.route("/fetch", methods=["POST"])
def fetch():
    category = request.form.get("category", "technology")
    country = request.form.get("country", "us")
    if not API_KEY:
        flash("Missing NEWSAPI_KEY in .env", "error")
        return redirect(url_for("index"))

    flash(f"Fetching latest {category} news...", "info")
    articles = fetch_top_headlines(API_KEY, category=category, country=country, page_size=10)
    for art in articles:
        text = " ".join(filter(None, [art.get("title"), art.get("description"), art.get("content")]))
        summary = summarize_text(text)
        insert_article(DB_PATH, art, category, summary)

    flash(f"Fetched and summarized {len(articles)} articles!", "success")
    return redirect(url_for("index"))


@app.route("/digest/<category>")
def digest(category):
    articles = get_latest_articles(DB_PATH, limit=20, category=category)
    return render_template("digest_template.html", title=f"{category.title()} Digest", articles=articles)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
