# tests/test_summarize.py
from summarizer_module import summarize_text

def test_summarize_short_text():
    text = "This is a short paragraph. It contains a few sentences. The summarizer should return something shorter."
    s = summarize_text(text, sentence_count=1)
    assert isinstance(s, str)
    assert len(s) > 0
