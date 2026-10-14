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
def prepare(site, draft, slug):
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
    sections = []
    for sec in data["sections"]:
        sections.append("<section><h2>" + escape(sec["heading"]) + "</h2>")
        sections += ["<p>" + escape(p) + "</p>" for p in sec["paragraphs"]]
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
    page = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>""" + title + """ | AI Learning Gym</title>
<meta name="description" content="""" + escape(data["description"]) + """">
<link rel="canonical" href="""" + escape(canonical) + """">
<style>
:root{--ink:#172033;--muted:#5e687a;--link:#155bb5;--border:#d9e2ee;--soft:#f3f7fb}
*{box-sizing:border-box}body{margin:0;background:#fff;color:var(--ink);font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;font-size:18px;line-height:1.72}
a{color:var(--link)}.site-header{border-bottom:1px solid var(--border)}.site-header-inner,main{max-width:750px;margin:auto;padding:18px 24px}
main{padding-top:48px;padding-bottom:64px}h1,h2,h3{line-height:1.3;color:#101827}h1{font-size:clamp(2rem,5vw,3rem)}
h2{margin-top:2em}p{margin-bottom:1.2em}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:var(--soft);padding:1rem;border-radius:8px}
.related{margin-top:3rem;padding:1rem;border:1px solid var(--border);border-radius:8px}
</style></head><body><header class="site-header"><div class="site-header-inner"><a href="/">AI Learning Gym</a></div></header>
<main><article><h1>""" + title + "</h1>" + "\n".join(sections) + "</article></main></body></html>\n"
    target.parent.mkdir(parents=True, exist_ok=False)
    target.write_text(page, encoding="utf-8")
    sitemap = site / "sitemap.xml"
    ET.register_namespace("", "http://www.sitemaps.org/schemas/sitemap/0.9")
    tree = ET.parse(sitemap)
    root = tree.getroot()
    ns = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
    if any(n.text == canonical for n in root.iter(ns + "loc")):
        raise ValueError("Sitemap already contains URL")
    entry = ET.SubElement(root, ns + "url")
    ET.SubElement(entry, ns + "loc").text = canonical
    ET.SubElement(entry, ns + "lastmod").text = date.today().isoformat()
    ET.indent(tree, space="  ")
    tree.write(sitemap, encoding="utf-8", xml_declaration=True)
    print("Prepared publication files; publication still requires PR review and merge")

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--site",required=True)
    p.add_argument("--draft",required=True)
    p.add_argument("--slug",required=True)
    a=p.parse_args()
    prepare(Path(a.site).resolve(),Path(a.draft).resolve(),a.slug)

if __name__=="__main__": main()
