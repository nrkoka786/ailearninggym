#!/usr/bin/env python3
"""Prepare a publication PR only after explicit human verification. Never merge/deploy."""
import argparse
from datetime import date
import html
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET

DOMAIN = "https://ailearninggym.com"
def escape(s): return html.escape(str(s), quote=True)
def prepare(site, draft, slug, dry_run=False):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
        raise ValueError("Unsafe slug")
    data = json.loads((draft / "review.json").read_text(encoding="utf-8"))
    if data.get("status") != "HUMAN_REVIEW_REQUIRED":
        raise ValueError("Only reviewed draft schema supported")
    for field in ("title", "description", "sections", "faq", "example_prompts", "sources"):
        if not data.get(field): raise ValueError("Missing: " + field)
    if len(data["description"]) > 155: raise ValueError("Description exceeds 155 characters")
    words = sum(len(p.split()) for s in data["sections"] for p in s["paragraphs"])
    words += sum(len(x["answer"].split()) for x in data["faq"])
    if words < 900: raise ValueError(f"Article too short ({words} instructional words)")
    if len(data["faq"]) < 4 or len(data["example_prompts"]) < 3:
        raise ValueError("Missing FAQs or prompts")
    if not any("example" in s["heading"].lower() for s in data["sections"]):
        raise ValueError("Worked example missing")
    if len(data["sources"]) < 2: raise ValueError("Insufficient sources")
    # Editor must choose/verify sources; no automatic factual verification.
    from urllib.parse import urlparse
    for s in data["sources"]:
        parsed = urlparse(s["url"])
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Invalid source URL")
    target = site / "blog" / slug / "index.html"
    if target.exists(): raise ValueError("Article already exists; refusing overwrite")
    canonical = DOMAIN + "/blog/" + slug + "/"
    # Only the allowlisted learning-path URL becomes HTML; all other text is escaped.
    contextual_path = "/learning-paths/how-to-fact-check-ai-answers/"
    def render_paragraph(paragraph):
        pieces = str(paragraph).split(contextual_path)
        safe = escape(pieces[0])
        for part in pieces[1:]:
            safe += '<a href="' + contextual_path + '">How to Fact-Check AI Answers</a>' + escape(part)
        return "<p>" + safe + "</p>"
    sections = []
    for sec in data["sections"]:
        sections.append("<section><h2>" + escape(sec["heading"]) + "</h2>")
        sections += [render_paragraph(p) for p in sec["paragraphs"]]
        sections.append("</section>")
    sections.append("<section><h2>Copyable prompts</h2>")
    for p in data["example_prompts"]:
        sections.append("<h3>" + escape(p["label"]) + "</h3><pre><code>" + escape(p["prompt"]) + "</code></pre>")
    sections.append("</section><section><h2>Frequently asked questions</h2>")
    for f in data["faq"]:
        sections.append("<h3>" + escape(f["question"]) + "</h3><p>" + escape(f["answer"]) + "</p>")
    sections.append("</section>")
    # Do not automatically claim source verification or treat links as citations.
    sections.append("<section><h2>Further reading</h2><ul>")
    for source in data["sources"]:
        sections.append('<li><a rel="noopener noreferrer" href="' + escape(source["url"]) + '">' + escape(source["label"]) + "</a></li>")
    sections.append("</ul></section>")
    # Internal links must be selected by editor; use only paths verified in site checkout.
    paths = ["/learning-paths/how-to-fact-check-ai-answers/"]
    links = [p for p in paths if (site / p.lstrip("/") / "index.html").is_file()]
    if not links: raise ValueError("Expected existing related learning path not found")
    sections.append('<aside class="related"><h2>Related learning</h2><ul>')
    sections += ['<li><a href="' + escape(p) + '">How to Fact-Check AI Answers</a></li>' for p in links]
    sections.append("</ul></aside>")
    title = escape(data["title"])
    page = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>' + title + ' | AI Learning Gym</title>'
            '<meta name="description" content="' + escape(data["description"]) + '">'
            '<link rel="canonical" href="' + escape(canonical) + '">'
            '<style>body{margin:0;background:#fff;color:#172033;font:18px/1.72 system-ui,sans-serif}'
            'header{border-bottom:1px solid #d9e2ee;padding:18px 24px}'
            'header a,main{max-width:750px;margin:auto;display:block}'
            'main{padding:48px 24px 64px}h1,h2,h3{line-height:1.3;color:#101827}'
            'h1{font-size:clamp(2rem,5vw,3rem)}h2{margin-top:2em}'
            'a{color:#155bb5}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f3f7fb;padding:1rem}'
            '.related{margin-top:3rem;padding:1rem;border:1px solid #d9e2ee;border-radius:8px}'
            '</style></head><body><header><a href="/">AI Learning Gym</a></header>'
            '<main><article><h1>' + title + '</h1>' + "\n".join(sections) + '</article></main></body></html>\n')
    if dry_run:
        sitemap = site / "sitemap.xml"
        ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        tree = ET.parse(sitemap)
        if any(n.text == canonical for n in tree.getroot().iter(ns + "loc")):
            raise ValueError("Sitemap already contains URL")
        print(f"DRY RUN PASS: {slug}; {words} instructional words; no files written")
        return
    target.parent.mkdir(parents=True, exist_ok=False)
    target.write_text(page, encoding="utf-8")
    sitemap = site / "sitemap.xml"
    # Preserve the site's existing sitemap bytes and ordering, appending one URL.
    # XML parsing is for validation only; ElementTree serialization would reformat
    # every existing entry and make the publication PR difficult to audit.
    sitemap_text = sitemap.read_text(encoding="utf-8")
    tree = ET.fromstring(sitemap_text)
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    if any(n.text == canonical for n in tree.iter(ns + "loc")):
        raise ValueError("Sitemap already contains URL")
    closing = "</urlset>"
    if sitemap_text.count(closing) != 1:
        raise ValueError("Unexpected sitemap closing tag")
    entry = ("  <url><loc>" + escape(canonical) + "</loc><lastmod>"
             + date.today().isoformat() + "</lastmod></url>\n")
    sitemap.write_text(sitemap_text.replace(closing, entry + closing), encoding="utf-8")
    print("Prepared publication files; publication still requires PR review and merge")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--site",required=True)
    p.add_argument("--draft",required=True)
    p.add_argument("--slug",required=True)
    p.add_argument("--dry-run", action="store_true", help="Validate only; no files written")
    a=p.parse_args()
    prepare(Path(a.site).resolve(),Path(a.draft).resolve(),a.slug, dry_run=a.dry_run)

if __name__=="__main__": main()
