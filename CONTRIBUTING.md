# Contributing

Thanks for helping! The project has no build step.

1. Fork and clone, then serve locally: `python -m http.server 8080`.
2. Create a branch: `git checkout -b feat/my-change`.
3. Keep changes focused. New features should be a module (see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).
4. Run the checks below. Manually test in light and dark themes, keyboard-only, and at 320 px width.
5. Open a pull request describing the change and, for UI work, include screenshots.

```bash
python scripts/review_suites.py
git diff --check
```

The catalogue command runs structure checks, runner contracts and all 18 offline
browser suites in separate processes, then returns nonzero if any check failed.
It continues after failures so the summary reports every suite. Use
`python scripts/review_suites.py --list` to see the individual commands; each suite
can also be run directly. [Test coverage](docs/TEST_COVERAGE.md) maps suite ownership
and records the reviewed baseline.

## Standards

- Accessible by default: WCAG 2.2 AA contrast, visible focus, labelled controls.
- No runtime libraries. Keep system-font mode offline; optional Google Fonts
  requests must use the curated catalogue and Google CSS/font hosts only.
- Never execute imported content; avoid `innerHTML` with untrusted data.
- Use CSS custom properties rather than literal colours.
- Commit messages: imperative mood (`Add OKLCH gamut warning`).

The full catalogue and CI include `python scripts/button_states_review.py` to
check actual Chrome reduced-motion and forced-colour modes. Run it directly for
a focused button-state check. Keep hover, pressed,
selected, busy and disabled cues understandable without relying on colour alone.

Focused browser suites import `run_review` from `scripts/browser_runner.py` and
pass their own harness HTML, with `chrome_flags` for media-mode checks. Do not
import the integration suite or replace runner globals. Runner contract tests
use only Python's standard library; Chrome suites require Chrome/Chromium or Edge
(`CHROME_BIN` can select the executable). Every run uses a fresh temporary profile.

Pull requests run structure/runner checks before a catalogue-driven browser matrix
in CI. Up to three jobs run at once; a failed suite does not cancel the rest. Each
browser job has a 25-minute limit (the media suite launches two browsers) and
uploads its failure log for seven days. Pushes to main and manual Pages runs call
the same complete validation workflow before publishing; every required job must
succeed for that revision before deployment can start. The existing `structure`
check name is retained as a final gate requiring both checks and the entire
browser matrix to succeed, including when earlier jobs fail or are skipped.
The live Google Fonts
check remains optional because it requires the external service.
