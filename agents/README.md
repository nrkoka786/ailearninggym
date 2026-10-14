# AILearningGym autonomous growth agents — pilot

## Goal
Improve useful organic search traffic and AdSense revenue while preserving the existing static HTML website, GitHub Pages deployment, analytics, and advertising configuration.

## Approved decisions
- Model provider: Google Gemini API (cost-efficient Flash model; exact model ID configurable).
- First 30 days: every new article requires human approval.
- Target output: three SEO-informed article proposals per week, subject to verified data and quality.
- Publish through pull requests; never write generated content directly to main.
- Keep initial Gemini API spending target at $15/month; enforce explicit run limits and track usage.
- Never click ads or generate artificial traffic.
- Do not change AdSense scripts, security settings, or paid services autonomously.

## Planned pipeline
1. Research: identify gaps and opportunities using existing content and, once authorized, Google Search Console data.
2. Draft: produce evidence-backed beginner-focused content with source URLs and SEO rationale.
3. Validate: check factual support, originality risks, internal links, metadata, sitemap and HTML structure.
4. Review: create a pull request containing an article preview and change summary; require human approval.
5. Publish: merge only after approval and successful tests; verify the public URL and sitemap.
6. Monitor: inspect indexing status, impressions, clicks and engagement; report issues and opportunities.

## Secrets and integrations still needed
- GitHub Actions secret `GEMINI_API_KEY` (never commit or paste the key into chat).
- Google Search Console and GA4 authorization for data-driven prioritization.
- Verify GitHub notification delivery and preview workflow before scheduling jobs.

## Rollout gates
- Phase 1: implement manual-trigger draft generation, validations, and a test pull request.
- Phase 2: validate notifications, previews, costs, and human approvals for 30 days.
- Phase 3: consider automatic publication only after a documented quality and reliability review.

This document is a planning baseline, not an enabled automation. No scheduled jobs or API calls are activated by this file.
