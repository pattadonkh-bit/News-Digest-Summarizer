from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import os
import nltk

# โมดูลภายในโปรเจกต์
from fetch_module import fetch_top_headlines
from summarizer_module import summarize_text
from db_module import init_db, insert_article, get_latest_articles

# -----------------------------
# แก้ไข NLTK Error: ตรวจสอบและดาวน์โหลด NLTK resources
# ต้องมั่นใจว่ามีการดาวน์โหลด 'punkt' และ 'stopwords' ซึ่งจำเป็นต่อ summarizer_module.py
# -----------------------------
def download_nltk_resources():
    """ตรวจสอบและดาวน์โหลด 'punkt' และ 'stopwords'"""
    try:
        nltk.data.find('tokenizers/punkt')
    except nltk.downloader.DownloadError:
        print("Downloading 'punkt' for NLTK...")
        nltk.download('punkt', quiet=True)
    except LookupError:
        print("Downloading 'punkt' for NLTK...")
        nltk.download('punkt', quiet=True)
        
    try:
        nltk.data.find('corpora/stopwords')
    except nltk.downloader.DownloadError:
        print("Downloading 'stopwords' for NLTK...")
        nltk.download('stopwords', quiet=True)
    except LookupError:
        print("Downloading 'stopwords' for NLTK...")
        nltk.download('stopwords', quiet=True)
        
# เรียกใช้ฟังก์ชันดาวน์โหลดก่อนเริ่มแอป
download_nltk_resources()


# โหลดตัวแปรจาก .env
load_dotenv()

# สร้าง Flask app
app = Flask(__name__)
# ใช้ OS random bytes เป็น secret key สำหรับการใช้งานจริง
app.secret_key = os.urandom(24) if not os.getenv("FLASK_SECRET_KEY") else os.getenv("FLASK_SECRET_KEY")

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
    # ดึงบทความล่าสุด 15 บทความจากฐานข้อมูล
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
    if not API_KEY or API_KEY == "YOUR_NEWSAPI_KEY_HERE":
        flash("Missing or invalid NEWSAPI_KEY in .env file. Please update it.", "error")
        return redirect(url_for("index"))

    try:
        # ใช้ flash message เพื่อแสดงสถานะการทำงาน
        flash(f"Fetching latest {category} news...", "info")

        # ดึงข่าวจาก API
        articles = fetch_top_headlines(API_KEY, category=category, country=country, page_size=10)

        # สรุปข่าวและบันทึกลง DB
        summarized_count = 0
        for art in articles:
            # รวม Title, Description, และ Content เข้าด้วยกันสำหรับสรุป
            text = " ".join(filter(None, [art.get("title", ""), art.get("description", ""), art.get("content", "")]))
            
            summary = ""
            try:
                # ลองสรุปข้อความ
                summary = summarize_text(text)
            except Exception as e:
                # จัดการข้อผิดพลาดในการสรุปและบันทึกข้อความผิดพลาดลงใน summary
                summary = f"**เกิดข้อผิดพลาดในการสรุปข่าว:** {e}. (Original Error: NLTK resource missing or text too short/invalid for summarization.)"

            insert_article(DB_PATH, art, category, summary)
            summarized_count += 1

        flash(f"Fetched and summarized {summarized_count} articles!", "success")
        
    except Exception as e:
        flash(f"Error fetching articles: {e}", "error")

    return redirect(url_for("index"))

# -----------------------------
# หน้า digest แยกตาม category
# -----------------------------
@app.route("/digest/<category>")
def digest(category):
    # ดึงบทความ 20 บทความล่าสุดสำหรับหมวดหมู่นี้
    articles = get_latest_articles(DB_PATH, limit=20, category=category)
    return render_template("digest_template.html", title=f"{category.title()} Digest", articles=articles)

# -----------------------------
# จุดเริ่มต้นของแอป
# -----------------------------
if __name__ == "__main__":
    # ใช้ host="0.0.0.0" เพื่อให้สามารถเข้าถึงจากภายนอกได้ในสภาพแวดล้อม container
    app.run(debug=True, host="0.0.0.0", port=5000)
