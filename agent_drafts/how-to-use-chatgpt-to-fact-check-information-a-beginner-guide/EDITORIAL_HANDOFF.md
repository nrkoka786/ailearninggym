# First article — editorial handoff

**Status: UNPUBLISHED; NOT APPROVED FOR PUBLICATION**

- Title: How to Use ChatGPT to Fact-Check Information: A Beginner Guide
- Draft directory: `agent_drafts/how-to-use-chatgpt-to-fact-check-information-a-beginner-guide`
- Instructional word count (sections + FAQ answers): **1,172**
- Worked example: explicitly fictional recycling ordinance; **not presented as a real event**
- Added: five-question verification checklist, evidence log, source/context checks, fourth reusable prompt, fifth FAQ
- Existing `preview.html` is a **noindex draft preview**, not a live website article

## Outstanding editorial gates
1. Specific official sources now replace the broad homepages: OpenAI's accuracy/limitations and search guidance, and the Library of Congress primary-sources guide. Check each page directly and confirm it supports the article's corresponding claim before approving publication.
2. Run Agent #2 against this exact branch and slug; address flagged issues.
3. Run Agent #3 dry-run against this exact branch and slug; confirm structural PASS.
4. A contextual internal link now appears in the draft preview, but the Agent 3 publication renderer currently escapes paragraph text and will not convert this plain-text URL to a clickable link. Fix or review the publication renderer before release. Review overlap with the existing "How to Fact-Check AI Answers" learning path, and verify that the new guide adds distinct practical value.
5. Verify on-brand HTML and live navigation before preparing a publication PR.
6. Only after those checks, the editor can authorize Agent #3 to create a **separate draft publication PR**; merging that future publication PR would publish to GitHub Pages.

**Do not merge this editorial draft PR into main.** It contains review-only files.
