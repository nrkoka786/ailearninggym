"""Deterministic editorial checks. No claims of factual verification."""
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlparse

STOP = set("about after again against also because before being could every from have into more most other over should their there these those through under using very what when where which while with would your this that than they them then were will".split())

def tokens(text):
    return set(w for w in re.findall(r"[a-z]{3,}", text.lower()) if w not in STOP)

class PageText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.title = []
        self.h1 = []
        self.current = None
        self.ignore = 0
    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"): self.ignore += 1
        if tag in ("title", "h1"): self.current = tag
    def handle_endtag(self, tag):
        if tag in ("script", "style") and self.ignore: self.ignore -= 1
        if tag == self.current: self.current = None
    def handle_data(self, data):
        if self.ignore: return
        if self.current == "title": self.title.append(data)
        if self.current == "h1": self.h1.append(data)

def inventory(site_root):
    root = Path(site_root)
    if not root.is_dir(): return []
    found = []
    for page in root.rglob("*.html"):
        rel = page.relative_to(root)
        if any(part.startswith(".") or part in ("agent_drafts", "node_modules", "agents") for part in rel.parts):
            continue
        if len(found) >= 1000: break
        try:
            parser = PageText()
            parser.feed(page.read_text(encoding="utf-8"))
            title = " ".join(parser.h1 or parser.title).strip()
        except (UnicodeError, OSError): continue
        if not title: continue
        url = "/" + str(rel).replace("\\", "/")
        if url.endswith("/index.html"): url = url[:-10]
        found.append({"path": url, "title": title})
    return found

def recommend_links(doc, pages, limit=5):
    subject = tokens(doc.get("title", "") + " " + doc.get("target_keyword", ""))
    scored = []
    for p in pages:
        overlap = len(subject & tokens(p["title"]))
        if overlap >= 2:
            scored.append((overlap, p))
    scored.sort(key=lambda x: (-x[0], x[1]["path"]))
    return [dict(p, shared_keywords=score) for score,p in scored[:limit]]

def content_warnings(doc):
    notes = []
    sections = doc.get("sections", [])
    paras = [p for s in sections for p in s.get("paragraphs", [])]
    if not any("example" in s.get("heading", "").lower() for s in sections):
        notes.append("No clearly labeled worked example")
    example = next((s for s in sections if "example" in s.get("heading", "").lower()), None)
    if example and any(term in " ".join(example.get("paragraphs", [])).lower() for term in ("imagine", "hypothetical", "[city", "[insert")):
        notes.append("Worked example appears hypothetical or contains placeholders; request a documented demonstration")
    if paras and len(set(p.strip().lower() for p in paras)) < len(paras):
        notes.append("Exact repeated paragraphs detected")
    if not doc.get("sources"):
        notes.append("No proposed sources")
    if any(urlparse(x.get("url","")).path in ("", "/") for x in doc.get("sources", [])):
        notes.append("One or more sources link only to a homepage rather than specific evidence")
    return notes
