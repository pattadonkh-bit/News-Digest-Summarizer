# 📰 News Digest & Summarizer (Final Submission)

## Overview
A Flask-based app that fetches top headlines via **NewsAPI**, auto-summarizes them using **Sumy (LexRank)**, and saves them to **SQLite**.  
Users can view daily news digests directly in the web interface.

---

## 🧠 Features
- Fetch news by category (Tech, Science, Sports)
- Auto summarization with Sumy
- Store and query in SQLite
- HTML dashboard for daily digest
- Ready for Docker deployment

---

## 🧰 Tech Stack
| Component | Technology |
|------------|-------------|
| Backend | Flask |
| Summarizer | Sumy (LexRank) |
| Database | SQLite |
| API | NewsAPI |
| Deployment | Docker + docker-compose |

---

## ⚙️ Environment Setup (Local)
1. Clone repo  
   ```bash
   git clone https://github.com/yourusername/news-digest-summarizer.git
   cd news-digest-summarizer
