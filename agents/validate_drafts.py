#!/usr/bin/env python3
"""Minimal deterministic checks for generated review-only files."""
import json
from pathlib import Path
from html.parser import HTMLParser

class Parser(HTMLParser):
    pass

root = Path(__file__).resolve().parents[1] / "agent_drafts"
items = list(root.glob("*/review.json"))
if not items:
    raise SystemExit("No generated draft to validate")
for metadata in items:
    doc = json.loads(metadata.read_text(encoding="utf-8"))
    if doc.get("status") != "HUMAN_REVIEW_REQUIRED":
        raise SystemExit("Draft missing human-review guardrail")
    preview = metadata.with_name("preview.html")
    if not preview.exists():
        raise SystemExit("Missing preview")
    html = preview.read_text(encoding="utf-8")
    if 'name="robots" content="noindex,nofollow"' not in html:
        raise SystemExit("Draft preview must be noindex")
    Parser().feed(html)
    if "<h2>Copyable prompts</h2>" not in html or "<h2>Frequently asked questions</h2>" not in html:
        raise SystemExit("Missing practical tutorial sections")
    if len(doc.get("example_prompts", [])) < 3 or len(doc.get("faq", [])) < 4:
        raise SystemExit("Missing example prompts or FAQs")
    if doc.get("quality_metrics", {}).get("instructional_word_count", 0) < 700:
        raise SystemExit("Draft is too short")
    if doc.get("quality_metrics", {}).get("source_links_verified") is not False:
        raise SystemExit("Sources must remain unverified pending editorial review")
    if len(doc.get("sections", [])) < 4 or len(doc.get("sources", [])) < 2:
        raise SystemExit("Incomplete draft")
print("Validated", len(items), "review-only draft(s)")
