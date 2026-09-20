# AI Learning Gym — Phase 4

Phase 4 strengthens the site's indexable learning content, editorial transparency, internal linking, and evidence of ongoing maintenance.

## Added

- Public Learning Paths hub at `/learning-paths/`
- Three complete, indexable courses:
  - ChatGPT for Complete Beginners
  - Write Better Emails Using AI
  - Create Social-Media Posts Using AI
- Original explanations, worked comparisons, safety guidance, knowledge checks, and practice projects
- Course structured data, canonical URLs, unique titles, and meta descriptions
- AI Learning Gym Editorial Team bylines and review dates
- Editorial Standards page
- Site and Curriculum Updates page
- Stronger links from the homepage, About page, blog, HTML sitemap, and XML sitemap

## Important separation

Public course pages are indexable and explain the complete skill. Personalized dashboards and lesson sessions remain `noindex` because they depend on browser-local learner state.

## Acceptance test

1. Open `/learning-paths/` and confirm all three course cards work.
2. Open every course page and confirm its personalized-path button opens `/learn/` with the goal prefilled.
3. Confirm bylines link to `/editorial-standards.html`.
4. Confirm `/updates.html` lists Phases 1–4.
5. Confirm the homepage course cards now open the public courses.
6. Submit the updated `/sitemap.xml` in Google Search Console after deployment.
