"""Revise a review-only article with up to two Gemini calls."""
import argparse
import json
from pathlib import Path
from generate_draft import request_gemini, render

def word_count(article):
    return sum(len(p.split()) for s in article["sections"] for p in s["paragraphs"])

def revise(article):
    attempts = []
    for number in range(2):
        if word_count(article) >= 900 and len(article.get("faq", [])) >= 4:
            break
        instruction = "Return a complete JSON article with the same schema, 900+ substantive words, four FAQs, three useful prompts, and a worked example. Do not invent evidence. Proposed source links need human verification. Article: "
        updated, usage = request_gemini(instruction + json.dumps(article))
        article = updated
        attempts.append({"attempt": number + 1, "usage": usage})
    return article, attempts

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    source = Path(args.draft)
    original = json.loads((source / "review.json").read_text())
    if original.get("status") != "HUMAN_REVIEW_REQUIRED":
        raise ValueError("Draft requires human review status")
    article, attempts = revise(original)
    if not all(article.get(k) for k in ("title", "description", "sections", "faq", "example_prompts", "sources")):
        raise ValueError("Revision lacks required content")
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=False)
    article["status"] = "HUMAN_REVIEW_REQUIRED"
    article["revision_history"] = attempts
    article["quality_metrics"] = {"instructional_word_count": word_count(article), "source_links_verified": False}
    (output / "preview.html").write_text(render(article, source.name))
    (output / "review.json").write_text(json.dumps(article, indent=2))
    (output / "revision-report.md").write_text("Revision attempts: " + str(len(attempts)) + "\nHuman editorial verification still required.\n")

if __name__ == "__main__":
    main()
