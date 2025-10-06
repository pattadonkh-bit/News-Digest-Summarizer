import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

# ตรวจสอบและดาวน์โหลด punkt tokenizer ถ้ายังไม่มี
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def summarize_text(text: str, sentence_count: int = 2) -> str:
    """
    สรุปข้อความภาษาอังกฤษโดยใช้ LexRank summarizer จาก Sumy
    ปลอดภัยจาก LookupError และรองรับข้อความว่าง
    """
    text = (text or "").strip()
    if not text:
        return "(no content)"

    try:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LexRankSummarizer()
        summary_sentences = summarizer(parser.document, sentence_count)
        summary = " ".join(str(s) for s in summary_sentences)
        return summary or "(summary empty)"
    except Exception as e:
        # กัน error จาก NLTK หรือ Sumy
        return f"(summarization error: {e})"
