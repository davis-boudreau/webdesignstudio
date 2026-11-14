# Test coverage and validation ownership

The application has no build step or runtime network dependency. Run
`python scripts/review_suites.py` for the complete offline check set, followed by
`git diff --check`. The catalogue runs structure checks, runner contracts and all
18 browser suites in independent processes. It finishes every command and returns
nonzero if any command failed. `--list` prints commands; `--matrix` prints the CI
browser matrix without importing suites or launching Chrome.

Browser runs use separate local servers and temporary profiles. They never use
the user's browser profile or saved projects. `CHROME_BIN` can select Chrome,
Chromium or Edge. The runner rejects failed assertions, captured JavaScript
errors, nonzero browser exits, malformed/empty reports and incomplete harnesses.

## Suite ownership

Counts below are from the completed full catalogue run on 13 November 2026:
20/20 commands passed (`.final-all-checks.log`), with no captured JavaScript errors
in all 19 browser launches. The current-run audit is `.final-coverage.log`.
Counts are assertion occurrences, including loop cases and repeated names;
they are not line/branch coverage or accessibility conformance measurements.

| Suite (`scripts/`) | Checks | Owns |
| --- | ---: | --- |
| `project_model_review.py` | 14 | Normalization, complete replacement, observer ordering and save isolation |
| `project_library_review.py` | 49 | Local save/load, autosave, reset, JSON validation/migration and file replacement |
| `navigation_review.py` | 158 | Routes, fragments, disclosures, focus and responsive editor placement |
| `planning_review.py` | 76 | Shared planning, Brief fields, safe text and prototype artifacts |
| `content_tree_review.py` | 201 | Inventory, branch edits, Save/Discard/Undo and dirty-form boundaries |
| `sitemap_review.py` | 305 | Destinations, hierarchy, inclusion, source selection and compatibility |
| `wireframe_review.py` | 152 | Read-only mirror, geometry/paint, fidelity, local views and downloads |
| `palette_review.py` | 575 | Brand/UI anchors, ramps, semantic tokens, neutral paint, backgrounds and opacity |
| `contrast_review.py` | 87 | Inventory, filters/CSV, reviewed repair and guided button review |
| `components_review.py` | 57 | State cues, overrides, configuration round trips and secondary actions |
| `typography_review.py` | 185 | Fonts, validation/retry, scales, rhythm, specimens and guided stages |
| `spacing_review.py` | 223 | Region padding, token arithmetic, comparisons and optional CSS practice |
| `responsive_preview_review.py` | 149 | Viewports, browsing state, project replacement, themes and breakpoint decisions |
| `standalone_exports_review.py` | 465 | Basic/Advanced website files, linked CSS, native interactions, layout and parity |
| `view_updates_review.py` | 16 | Scheduling, phase order, coalescing and subscription lifecycle |
| `export_pipeline_review.py` | 98 | Contributor order, purity, recovery and reviewed CSS/HTML hashes |
| `browser_review.py` | 279 | Combined edits/save/preview/download/file-restore journeys and shared contracts |
| `button_states_review.py` | 16 | Actual reduced-motion (7) and forced-colour (9) browser modes |
| **Browser total** | **3,105** | 18 commands; the media command launches two independent browsers |

Structure checks separately verify 71 referenced assets, IDs/anchors, script
ordering and prohibited shared-entry-point reassignment. Runner/catalogue contract
tests currently pass 12 tests using standard-library mocks and real loopback
requests, without Chrome. They also detect missing/duplicate suite registration,
suite import side effects and lost failure status in the full-check command.

Integration intentionally retains Studio appearance separation, shared inspector
and token routing, teaching/example selection, authored website editing and the
optional Tailwind source bridge alongside the combined learner journeys. Focused
suites own their fixtures and never import or patch the integration harness.

## Refactor coverage audit

The original 13 November architecture-review browser log passed 2,793 checks
(`.architecture-review-browser.log`). A `collections.Counter` comparison with
the latest completed focused/integration logs accounts for every original name
occurrence, including duplicates: zero missing occurrences. Additional checks
cover codec/replacement ordering, view/export contracts, focused fixture isolation
and regressions discovered during extraction. In particular, project imports,
loads, reset and New clear preview browsing state while ordinary edits retain it.

The final current-run comparison also accounts for all 2,793 original occurrences
across the 3,105 passing browser assertions, with zero missing occurrences.
Historical and current logs are local, ignored diagnostic artifacts; they are not
required by CI or available in a fresh checkout. This document preserves the
reviewed findings. Future counts may change
as fixtures expand; CI validates behavior rather than a fixed assertion total.

## CI and remaining review gaps

CI runs structure and runner checks first, then the catalogue-driven browser
matrix. At most three jobs run concurrently; failure does not cancel other suites.
Each browser job has 25 minutes, accommodating two 660-second launches in the
media suite. Failed-suite logs are retained for seven days. The Pages deployment
depends on the complete reusable CI workflow for the same triggering revision.
The existing `structure` check remains a final gate over the checks job and the
entire browser matrix. It runs even when a prerequisite failed or was skipped,
and succeeds only when both prerequisites succeeded.

Both workflows passed [actionlint 1.7.7](https://github.com/rhysd/actionlint/releases/tag/v1.7.7)
in this session using the official Windows
release with its published SHA256 verified. The lint command disabled optional
external ShellCheck/Pyflakes integrations. The 13 November cleanup did not trigger
hosted Actions or a Pages deploy. On 14 November,
[CI run 43592435409](https://github.com/davis-boudreau/webdesignstudio/actions/runs/43592435409)
passed all 20 jobs for refactor commit `cb7a956`, including the final required
gate. [Draft PR #1](https://github.com/davis-boudreau/webdesignstudio/pull/1) shows
the latest revision's status. No merge or Pages deployment was performed.
Local Bash checks exercised all 16 success/failure/cancelled/skipped combinations
of gate prerequisites: only `success/success` passes. A failing command piped through
`tee` also retains its exit status and writes the diagnostic log under `pipefail`.

`python scripts/font_cdn_review.py` is an optional external-service smoke check;
the offline typography suite uses deterministic local font fixtures. It is not
part of CI. Manual keyboard/screen-reader/zoom/reflow, additional-browser reviews
and browser/OS file-chooser, download and clipboard permission behavior remain
outside this automated baseline. Passing these checks does not establish full
accessibility or successful browser/OS file saving.
