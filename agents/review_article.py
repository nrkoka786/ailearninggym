#!/usr/bin/env python3
"""Agent 2: read-only editorial/SEO checks. Reports findings; never approves/publishes."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
from urllib.parse import urlparse
import urllib.request
import urllib.error

ROOT = Path.cwd() if (Path.cwd() / "agent_drafts").is_dir() else Path(__file__).resolve().parents[1]
class Extract(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.headings, self.title = [], [], []
        self.in_title = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a": self.links.append(a.get("href", ""))
        if tag in ("h1", "h2", "h3"): self.headings.append(tag)
        if tag == "title": self.in_title = True
    def handle_endtag(self, tag):
        if tag == "title": self.in_title = False
    def handle_data(self, data):
        if self.in_title: self.title.append(data)

def verify_url(url):
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        return "INVALID"
    if parsed.hostname in ("localhost",) or parsed.hostname.endswith((".local", ".internal")):
        return "SKIPPED"
    # Only check whether the URL resolves, not whether it supports article claims.
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "AILearningGymEditorialReview/1.0"})
        with urllib.request.urlopen(req, timeout=8) as res:
            return "REACHABLE" if res.status < 400 else "HTTP_" + str(res.status)
    except urllib.error.HTTPError as exc:
        return "HTTP_" + str(exc.code)
    except (urllib.error.URLError, TimeoutError, ValueError):
        return "UNVERIFIED"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True, help="Relative path to draft folder")
    parser.add_argument("--output", default="agent2-review.md")
    args = parser.parse_args()
    folder = (ROOT / args.draft).resolve()
    if not folder.is_relative_to((ROOT / "agent_drafts").resolve()) or not folder.is_dir():
        raise SystemExit("Draft path must be an existing agent_drafts subdirectory")
    doc = json.loads((folder / "review.json").read_text(encoding="utf-8"))
    markup = (folder / "preview.html").read_text(encoding="utf-8")
    parser_html = Extract()
    parser_html.feed(markup)
    findings = []
    def flag(level, message): findings.append((level, message))
    if doc.get("status") != "HUMAN_REVIEW_REQUIRED": flag("BLOCK", "Human-review guardrail missing")
    if 'name="robots" content="noindex,nofollow"' not in markup: flag("BLOCK", "Draft missing noindex")
    if len(doc.get("description", "")) > 155 or not doc.get("description"): flag("FIX", "Meta description missing or too long")
    if parser_html.headings.count("h1") != 1: flag("FIX", "Expected exactly one H1")
    words = sum(len(p.split()) for s in doc.get("sections", []) for p in s.get("paragraphs", []))
    words += sum(len(x.get("answer", "").split()) for x in doc.get("faq", []))
    if words < 900: flag("FIX", f"Only {words} instructional words; assess depth and usefulness (not filler)")
    if len(doc.get("example_prompts", [])) < 3: flag("FIX", "Fewer than 3 reusable prompts")
    if len(doc.get("faq", [])) < 4: flag("FIX", "Fewer than 4 FAQ answers")
    if not any("example" in x.get("heading", "").lower() for x in doc.get("sections", [])):
        flag("REVIEW", "No clearly labeled worked example")
    links = [x for x in parser_html.links if x.startswith("/") and not x.startswith("//") and x != "/"]
    if not links: flag("FIX", "No contextual internal links in article")
    sources = doc.get("sources", [])
    if len(sources) < 2: flag("FIX", "Fewer than two proposed sources")
    statuses = [(x.get("url", ""), verify_url(x.get("url", ""))) for x in sources]
    if any(s != "REACHABLE" for _, s in statuses): flag("REVIEW", "One or more source URLs could not be reached")
    flag("REVIEW", "Source relevance, specific claim support and factual accuracy require human verification")
    flag("REVIEW", "Check originality, search intent, duplication, and compatibility with existing site design")
    title = doc.get("title", "")
    report = [
        "# Agent 2 — SEO and editorial review", "",
        f"**Article:** {title}", f"**Draft:** {args.draft}", "",
        "**Decision: NEEDS HUMAN REVIEW — NOT APPROVED FOR PUBLICATION**", "",
        f"Instructional words (excluding prompts): **{words}**", "",
        "## Findings", ""
    ]
    report += [f"- **{level}:** {message}" for level, message in findings]
    report += ["", "## Proposed source URL checks", "",
               "Reachable means the URL responded; it does **not** verify a claim.", ""]
    report += [f"- {url} — {status}" for url, status in statuses]
    report += ["", "## Editorial release gate", "",
               "An editor must verify claims against primary sources, choose accurate in-article citations, "
               "add relevant existing-site internal links, and approve a separately prepared publication PR.",
               "This report cannot approve publication.", ""]
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(report), encoding="utf-8")
    print(f"Agent 2 report written to {out}; {len(findings)} findings; no publication")
if __name__ == "__main__":
    main()
