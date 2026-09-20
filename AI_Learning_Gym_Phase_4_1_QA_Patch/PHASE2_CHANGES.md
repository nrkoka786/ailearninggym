# AI Learning Gym — Phase 2 MVP

## What Phase 2 adds

- A working `/learn/` Learning Path Builder.
- Five one-at-a-time questions covering:
  - the learner's goal;
  - prior AI experience;
  - desired outcome;
  - available time;
  - preferred learning style.
- Goal recognition for email, social media, AI images, coding, model comparison, AI foundations, and general productivity.
- Course scope selection: Quick Skill, Focused Skill, Skill Path, or Deep Path.
- A personalized curriculum preview with modules and Learn, Show Me, Try It, Test Me, and Ask AI activities.
- A `/my-learning/` dashboard with module checkboxes and completion percentage.
- Browser-only saving with no account, database, or AI API expense.
- Updated homepage links, site map, XML sitemap, and privacy disclosure.

## Privacy and cost behavior

The learner's answers, generated path, and progress remain in browser local storage. This version does not transmit questionnaire answers to an external model. The My Learning page is marked `noindex` because its content is personal and generated inside the visitor's browser.

## Suggested acceptance test

1. On the homepage, enter: `Help me write better emails with ChatGPT`.
2. Confirm the goal appears in the first questionnaire field.
3. Complete all five questions.
4. Confirm an email learning path appears.
5. Click **Start this path**.
6. Mark two modules complete and refresh the page.
7. Confirm the completed modules and percentage remain saved.
8. Test **Reset progress** and **Delete this path**.

## Next iteration after real-user testing

The next iteration can add actual lesson content, exercises, scoring, feedback, optional login/synchronization, and secure AI-generated adaptation. Those additions should follow observation of how visitors use this no-cost MVP.
