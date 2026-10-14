# Agent 2 — SEO and editorial reviewer (pilot)

Run manually from **Actions → Agent 2 SEO editorial review** on main.
For test PR #8 use branch `agent/draft-38627569942-1` and slug
`how-to-use-chatgpt-to-fact-check-information-a-beginner-guide`.

The job checks metadata, draft noindex guardrail, structural completeness,
instructional depth, copyable prompts, FAQs, presence of internal links,
and whether proposed source URLs respond. It uploads a Markdown review
report as a GitHub Actions artifact.

**Important limitations:** URL reachability is not factual verification.
This agent does not browse or evaluate source content, establish search
volume, perform plagiarism checks, or independently certify article
accuracy. Human editorial verification and explicit approval remain
mandatory. The workflow has read-only repository permissions; it does not
modify PRs, deploy content, or touch AdSense or sitemap files.
