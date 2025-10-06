# tests/test_fetch.py
import os
import pytest
from fetch_module import fetch_top_headlines

@pytest.mark.skipif(not os.getenv("NEWSAPI_KEY"), reason="Need NEWSAPI_KEY for integration test")
def test_fetch_top_headlines_basic():
    api_key = os.getenv("NEWSAPI_KEY")
    results = fetch_top_headlines(api_key, category="technology", country="us", page_size=5)
    assert isinstance(results, list)
    assert len(results) <= 5
    for r in results:
        assert "title" in r
        assert "url" in r
