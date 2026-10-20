# Design System Studio

Dependency-free browser application using HTML, CSS and classic deferred JavaScript.
There is no build step. Keep the runtime local and free of network dependencies.

## Session handoff

- Read `docs/PROGRESS.md` at the start of work. Consult the linked audit and
  `docs/ARCHITECTURE.md` when relevant to the task.
- After meaningful work, update `docs/PROGRESS.md` with completed changes,
  decisions, commands actually run, results, unresolved issues and the next step.
- Keep historical audit results distinct from checks run in the current session.
  Do not mark planned or untested work complete.
- These notes travel between computers when committed and pushed with the code.
  Do not assume access to earlier chats or another computer's browser storage.

## Implementation and verification

- Follow `CONTRIBUTING.md`. Preserve script load order in `index.html` and the
  relationship between shared state, live previews, saved projects and exports.
- Treat imported JSON and browser storage as untrusted data. Validate values;
  never execute imported content or insert unescaped user strings into HTML.
- For functional changes, run `python scripts/check_structure.py`,
  `python scripts/browser_review.py` and `git diff --check`.
- Browser checks need Chrome/Chromium or Edge; `CHROME_BIN` can select the binary.
  They use an isolated temporary profile, not the user's saved projects.
- Add regression coverage for confirmed bugs. Report browser and manual-testing
  gaps explicitly; passing this suite does not establish full accessibility.
- Refresh the affected asset query versions in `index.html` when changing runtime
  assets, so previously deployed browser caches can pick up fixes.
