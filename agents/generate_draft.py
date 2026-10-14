#!/usr/bin/env python3
"""Generate a review-only SEO article draft with Gemini. No publication or ad interaction."""
import argparse
import html
import json
import os
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
MAX_OUTPUT_TOKENS = 3500
BLOCKED = {"index", "blog", "learn", "learning-paths"}

def slugify(value):
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    if not slug or slug in BLOCKED or len(slug) > 75:
        raise ValueError("Invalid article slug")
    return slug

def request_gemini(prompt):
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("Missing GEMINI_API_KEY GitHub Actions secret")
    endpoint = "https://generativelanguage.googleapis.com/v1beta/models/" + MODEL + ":generateContent"
    payload = {"contents": [{"parts": [{"text": prompt}]}],
               "generationConfig": {"responseMimeType": "application/json",
                                    "maxOutputTokens": MAX_OUTPUT_TOKENS, "temperature": 0.4}}
    req = urllib.request.Request(endpoint, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=90) as response:
            result = json.load(response)
    except urllib.error.HTTPError as exc:
        raise RuntimeError(f"Gemini API HTTP {exc.code}; check key, quota and model") from exc
    text = "".join(p.get("text", "") for c in result.get("candidates", [])
                   for p in c.get("content", {}).get("parts", []))
    if not text:
        raise RuntimeError("Gemini returned no text; no draft created")
    return json.loads(text), result.get("usageMetadata", {})

def render(doc, slug):
    title = html.escape(doc["title"])
    description = html.escape(doc["description"])
    sections = doc["sections"]
    body = []
    for section in sections:
        body.append("<section><h2>" + html.escape(section["heading"]) + "</h2>")
        for paragraph in section["paragraphs"]:
            body.append("<p>" + html.escape(paragraph) + "</p>")
        body.append("</section>")
    # Sources are proposed reading links, NOT verified evidence.
    sources = "".join('<li><a rel="noopener noreferrer" href="' + html.escape(s["url"], quote=True) +
                      '">' + html.escape(s["label"]) + "</a></li>" for s in doc["sources"])
    canonical = "https://ailearninggym.com/blog/" + slug + "/"
    return """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>""" + title + """ | AI Learning Gym</title>
<meta name="description" content='""" + description.replace("'", "&#39;") + """'>
<link rel="canonical" href='""" + canonical + """'>
<meta name="robots" content="noindex,nofollow">
<style>body{font:17px/1.7 system-ui,sans-serif;max-width:780px;margin:3rem auto;padding:0 1rem;color:#17263a}h1,h2{line-height:1.3}a{color:#1763a3}.notice{padding:1rem;background:#fff4d6;border:1px solid #e9c978}</style>
</head><body><nav><a href="/">AI Learning Gym</a> / Draft preview</nav>
<p class="notice"><strong>UNPUBLISHED DRAFT — human review required.</strong> Sources and claims are not independently verified. Do not deploy this page as-is.</p>
<main><h1>""" + title + "</h1><p>" + description + "</p>" + "\n".join(body) + """<section><h2>Sources to verify</h2><ul>""" + sources + """</ul></section></main></body></html>"""

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--topic", required=True)
    args = parser.parse_args()
    topic = args.topic.strip()
    if not (12 <= len(topic) <= 130):
        raise ValueError("Topic must contain 12–130 characters")
    existing = [p.parent.name for p in (ROOT / "blog").glob("*/index.html")]
    prompt = f"""You are drafting an ORIGINAL, beginner-friendly educational article for AI Learning Gym.
Topic: {topic}
Existing article slugs (avoid duplicate intent): {json.dumps(existing)}
Return JSON object ONLY with keys:
title (string), description (string <= 155 chars), target_keyword (string),
search_intent (string), seo_rationale (string), sections (array of 4-7 objects each with
heading string and paragraphs array of 2-4 substantive strings), sources (array of
2-5 objects with label and url, only official authoritative URLs you know).
Be specific, educational and cautious. No invented statistics, rankings, quotes,
pricing, release dates, or first-hand testing claims. Never suggest artificial ad traffic.
If a fact requires verification, say so. No markdown or HTML in fields."""
    doc, usage = request_gemini(prompt)
    required = ["title", "description", "target_keyword", "search_intent",
                "seo_rationale", "sections", "sources"]
    if any(not doc.get(k) for k in required):
        raise ValueError("Gemini draft missing required fields")
    if not (4 <= len(doc["sections"]) <= 7) or not (2 <= len(doc["sources"]) <= 5):
        raise ValueError("Draft failed section/source count validation")
    if len(doc["description"]) > 155:
        raise ValueError("Meta description too long")
    for s in doc["sources"]:
        if not isinstance(s["url"], str) or not s["url"].startswith("https://"):
            raise ValueError("Source URL must use HTTPS")
    slug = slugify(doc["title"])
    if slug in existing:
        raise ValueError("Draft duplicates existing article slug")
    output = ROOT / "agent_drafts" / slug
    if output.exists():
        raise ValueError("Draft already exists; refusing overwrite")
    output.mkdir(parents=True)
    (output / "preview.html").write_text(render(doc, slug), encoding="utf-8")
    (output / "review.json").write_text(json.dumps({"topic": topic, **doc,
        "usage": usage, "status": "HUMAN_REVIEW_REQUIRED"}, indent=2) + "\n", encoding="utf-8")
    print("Generated review-only draft:", output.relative_to(ROOT))
    print("Gemini usage:", json.dumps(usage))

if __name__ == "__main__":
    main()
