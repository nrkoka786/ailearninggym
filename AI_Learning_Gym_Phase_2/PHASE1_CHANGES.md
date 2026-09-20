# AI Learning Gym — Phase 1 Changes

## Purpose

Phase 1 repositions AI Learning Gym from a general utility directory to a practical AI-learning website, while preserving every existing tool.

## What changed

- Rebuilt the homepage around the question: **“What do you want to learn with AI?”**
- Added the active-learning method: **Learn, Show Me, Try It, Test Me, Ask AI**.
- Featured three initial learning-path concepts:
  - ChatGPT for Complete Beginners
  - Write Better Emails Using AI
  - Create Social-Media Posts Using AI
- Elevated the Prompt Builder, Token Counter, and Image Prompt Generator as learning-support tools.
- Moved general utilities into a secondary Free Tools section.
- Updated the About page to explain the learning mission and methodology.
- Removed visible AdSense units from all pages while retaining the AdSense ownership-verification loader.
- Replaced broken `/logo.png` references with the existing `/AI_Learning_Gym_Logo.jpg` asset.
- Added a self-referencing canonical URL to every HTML page.
- Added homepage Open Graph metadata and WebSite/Organization structured data.
- Added About, Contact, Privacy, and Terms pages to `sitemap.xml`.

## Important behavior in Phase 1

The homepage goal field currently introduces the learning concept and moves visitors to the initial learning paths. It does not call an AI model yet. Secure AI curriculum generation, adaptive questions, user accounts, and saved progress belong to Phase 2.

## Deployment

Upload the contents of this folder to the root of the existing GitHub repository, replacing matching files. Do not upload the enclosing `ailearninggym-phase1` folder as an extra directory.

After GitHub Pages deploys:

1. Open the homepage on desktop and mobile.
2. Test the three featured AI tools and several general tools.
3. Confirm `https://ailearninggym.com/ads.txt` still loads.
4. Confirm `https://ailearninggym.com/sitemap.xml` loads.
5. Request indexing of the homepage and About page in Google Search Console.

Do not request a new AdSense review immediately. Complete the working AI-learning MVP and establish genuine user activity first.
