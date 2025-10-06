# report_module.py
import os
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")

def generate_html_report(articles, out_path: str = "daily_digest.html", title: str = None):
    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
    template = env.get_template("digest_template.html")
    rendered = template.render(
        title=title or f"Daily Digest — {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}",
        generated_at=datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC"),
        articles=articles
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(rendered)
    return out_path
