# AI Learning Gym — Phase 3

Phase 3 turns generated paths into usable, interactive lessons while keeping the experience browser-based and free to operate.

## Added

- Interactive lesson runner at `/lesson/`
- Five lesson stages: Learn, Show Me, Try It, Test Me, and Ask AI
- Original lesson content for ChatGPT foundations, AI email writing, and AI social-media writing
- Practice-answer saving in the visitor's browser
- Knowledge-check scoring and corrective review after an incorrect answer
- Module completion and automatic next-lesson navigation
- Dashboard lesson links, scores, and progress persistence
- Goal-prefilled homepage links for all three featured paths
- Updated privacy disclosure for practice responses, scores, and Ask AI prompts

## Acceptance test

1. Open the home page and enter `Help me write better emails with ChatGPT`.
2. Complete the five path-builder questions and save the path.
3. On My Learning, select **Open lesson** for module 1.
4. Open each lesson tab, save a practice response, and answer the knowledge check.
5. Confirm an incorrect answer shows a focused review and a correct answer records 100%.
6. Mark the lesson complete and confirm module 2 opens.
7. Return to My Learning and confirm progress and the score remain after refreshing.

The Ask AI feature intentionally copies a coaching prompt for use in the learner's preferred AI tool. It does not call a paid API in this phase.
