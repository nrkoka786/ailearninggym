"""Safety checks for Agent 3 dry-run."""
import json
import tempfile
import unittest
from pathlib import Path
from prepare_publication import prepare

class DryRunSafety(unittest.TestCase):
    def test_short_article_does_not_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            site = root / "site"
            draft = root / "draft"
            site.mkdir()
            draft.mkdir()
            (draft / "review.json").write_text(json.dumps({
                "status":"HUMAN_REVIEW_REQUIRED",
                "title":"Short article",
                "description":"Test",
                "sections":[{"heading":"Worked example","paragraphs":["Too short."]}],
                "faq":[{"question":"Why?","answer":"Because."}]*4,
                "example_prompts":[{"label":"Prompt","prompt":"Try"}]*3,
                "sources":[{"label":"Source","url":"https://example.com/a"},
                           {"label":"Other","url":"https://example.org/b"}]
            }))
            with self.assertRaisesRegex(ValueError,"Article too short"):
                prepare(site,draft,"test-article",dry_run=True)
            self.assertFalse((site / "blog").exists())
    def test_invalid_slug_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            with self.assertRaisesRegex(ValueError,"Unsafe slug"):
                prepare(root,root,"../unsafe",dry_run=True)

if __name__=="__main__":
    unittest.main()
