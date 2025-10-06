FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ✅ Fix NLTK LookupError
RUN python -m nltk.downloader punkt stopwords

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 10000

CMD ["flask", "run", "--port=10000"]