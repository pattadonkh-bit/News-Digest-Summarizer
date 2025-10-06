# tests/test_report.py
import os
from report_module import generate_html_report

def test_generate_report(tmp_path):
    articles = [
        ("Title 1", "Source A", "2025-10-06T08:00:00Z", "Summary 1", "http://example.com/1", "technology"),
        ("Title 2", "Source B", "2025-10-06T07:00:00Z", "Summary 2", "http://example.com/2", "technology"),
    ]
    out = tmp_path / "digest.html"
    path = generate_html_report(articles, out_path=str(out), title="Test Digest")
    assert os.path.exists(path)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Test Digest" in content
    assert "Title 1" in content
