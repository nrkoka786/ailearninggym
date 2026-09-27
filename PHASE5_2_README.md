# AI Learning Gym Phase 5.2 maintenance patch

Upload the contents of this ZIP to the root of the GitHub repository, preserving the folders and replacing matching files. Do not upload the enclosing `phase52_patch` folder.

## Included improvements

- Corrected the About page's tool list so it no longer promises tools that do not exist.
- Rewrote the Terms page in clear language and updated its review date.
- Simplified the Contact page language.
- Added unique meta descriptions to Terms, Contact, and Privacy.
- Corrected duplicate H1 headings on eight blog posts, three AI explainer pages, and the Markdown Editor.
- Added lazy loading and accessible titles to the three YouTube embeds.
- Replaced fast-decaying model and price claims in the ChatGPT, Claude, and Grok guides with dated guidance and official-source links.

## Deliberately unchanged

- `sitemap.xml`: the live blog index and sitemap already contain the same nine blog posts. No URLs are missing.
- `/my-learning/`: this private, browser-specific progress page already uses `noindex,follow`, so it should remain outside the XML sitemap.
- Homepage tool cards: these are already normal crawlable `<a href>` links.

## AdSense consent setup (dashboard action, not a repository file)

Before serving personalized ads broadly, configure Google's certified consent-management messages in AdSense:

1. Open AdSense and go to **Privacy & messaging**.
2. Create or enable the **European regulations** message using a Google-certified CMP.
3. Configure the **US state regulations** message as appropriate.
4. Preview the messages, publish them, and test in an incognito browser or with Google's privacy-message testing tools.

Do not add a homemade cookie banner that merely hides ads; consent signals need to be handled through a compliant CMP.

## Deployment check

After GitHub Pages deploys, open the About, Terms, Contact, Privacy, Markdown Editor, three AI explainer pages, and two or three blog posts. Then confirm that YouTube videos still load when scrolled into view.
