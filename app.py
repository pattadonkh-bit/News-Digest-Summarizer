from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
import nltk

# ตรวจสอบและดาวน์โหลด punkt tokenizer สำหรับ NLTK
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

# โมดูลภายในโปรเจกต์
from fetch_module import fetch_top_headlines
from summarizer_module import summarize_text
from db_module import init_db, insert_article, get_latest_articles

# โหลดตัวแปรจาก .env
load_dotenv()

# สร้าง Flask app
app = Flask(__name__)
app.secret_key = "newsdigest-secret"

# โหลดค่าคงที่จาก .env
API_KEY = os.getenv("NEWSAPI_KEY")
DB_PATH = os.getenv("DB_PATH", "./db/news.db")

# ตรวจสอบและสร้างโฟลเดอร์ฐานข้อมูลหากยังไม่มี
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
init_db(DB_PATH)

# -----------------------------
# ROUTE หลัก
# -----------------------------
@app.route("/")
def index():
    articles = get_latest_articles(DB_PATH, limit=15)
    return render_template("index.html", articles=articles)

# -----------------------------
# ดึงข่าว + สรุปข่าว
# -----------------------------
@app.route("/fetch", methods=["POST"])
def fetch():
    category = request.form.get("category", "technology")
    country = request.form.get("country", "us")

    # ตรวจสอบ API key
    if not API_KEY:
        flash("Missing NEWSAPI_KEY in .env file", "error")
        return redirect(url_for("index"))

    try:
        flash(f"Fetching latest {category} news...", "info")

        # ดึงข่าวจาก API
        articles = fetch_top_headlines(API_KEY, category=category, country=country, page_size=10)

        # สรุปข่าวและบันทึกลง DB
        for art in articles:
            text = " ".join(filter(None, [art.get("title"), art.get("description"), art.get("content")]))
            try:
                summary = summarize_text(text)
            except Exception as e:
                summary = f"(summarization error: {e})"

            insert_article(DB_PATH, art, category, summary)

        flash(f"Fetched and summarized {len(articles)} articles!", "success")
    except Exception as e:
        flash(f"Error fetching articles: {e}", "error")

    return redirect(url_for("index"))

# -----------------------------
# หน้า digest แยกตาม category
# -----------------------------
@app.route("/digest/<category>")
def digest(category):
    articles = get_latest_articles(DB_PATH, limit=20, category=category)
    return render_template("digest_template.html", title=f"{category.title()} Digest", articles=articles)

# -----------------------------
# จุดเริ่มต้นของแอป
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
