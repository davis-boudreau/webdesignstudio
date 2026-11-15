# Test coverage and validation ownership

The application has no build step or runtime network dependency. Run
`python scripts/review_suites.py` for the complete offline check set, followed by
`git diff --check`. The catalogue runs structure checks, runner contracts and all
19 browser suites in independent processes. It finishes every command and returns
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
The table preserves that completed baseline. On 14 November a publication run
exposed a delayed colour-repair close-event race. Three deterministic regressions
were added to `contrast_review.py` (now 90 checks), bringing the current suite's
assertion inventory to 3,108. These cases failed before the runtime fix and pass
locally after it; the publication workflow validates the updated suite as usual.
The local semantic-colour dropdown feature adds 21 Palette checks (596 total).
All 18 offline browser suites passed on that feature branch with 3,129 assertions,
plus 12 runner contracts and 71 structure assets. The new choices are compared
independently with palette/state generator values, including both themes and
Preview/Apply persistence boundaries. This feature has not been published.
The subsequent local Brand Save/Discard and focused-preview change adds 24 Palette
checks (620 total), bringing the full passing inventory to 3,153. All 18 suites
pass with 19 empty error reports, alongside 12 runner contracts and 71 assets.
Coverage includes draft isolation from exports/storage, scoped Discard, atomic
Save, duplicate suffix validation, replacement and preview focus/layout in both
themes at 320/390/1440px. The latest Counter audit retains all 2,793 original
occurrences with zero missing (.brand-final-coverage.log). These local changes
remain unpublished; manual keyboard/screen-reader and other-browser checks have
not been performed.

The shared property-control extension registers `property_actions_review.py` in
the catalogue and adds 231 independent assertions. All 19 offline browser suites
pass locally: 3,384 assertions, 20 empty captured-error reports, plus 12 runner
contracts and 74 assets. The property suite checks drafts against model/CSS/HTML/
storage, scoped commits/discards, concurrent changes, source conflicts, project
replacement, validation, legacy display compatibility, deferred font requests,
semantic review, and source-aware preview/layout in both themes at 320/390/1440px.
The final Counter audit (.property-final-coverage.log) retains every original
2,793 assertion occurrence. Existing committed-edit fixtures explicitly Save;
two rejected-outline assertions now require unchanged saved structure/HTML.
The historical table below remains unchanged. The extension is unpublished;
manual accessibility, additional browsers and the optional live-font command
remain untested in this session. See [the property audit](PROPERTY_CONTROLS_AUDIT.md).

A subsequent Typography process review adds 124 raw-draft and stage-action cases
to `typography_review.py` (309 checks). These reproduced disappearing named-scale
proposals, font reset using the committed source and stale fallback comparison
after a shared source Save. The fixes pass the focused Typography suite 309/309,
integration 279/279 and shared property controls 231/231, with no captured errors.
The new coverage exercises all eight Typography stages at 320/390/1440px in both
themes, including draft preservation and preview focus. These focused results do
not replace the historical full-catalogue counts above. Font loads use local
fixtures; manual accessibility, additional browsers and live font delivery remain
unchecked.

The hierarchy ladder layout adds 15 Typography cases (324 total), checking the
accordion/control order, one visible ladder, all eight labelled sizes, saved/draft
boundaries, enlargement/user spacing, both themes at 320/390/1440px, stage return
and Configure routing. Focused checks pass 324/324, integration 279/279 and shared
property actions 231/231, with no captured errors. This focused run preserves the
historical full-catalogue counts above; no new full run or manual accessibility
review is implied.

The steps 1-3 property-disclosure follow-up adds 31 Typography cases (355 total),
covering default collapse, enlargement/control order, unchanged single specimens,
draft retention/Discard, Configure focus and both themes at 320/390/1440px. Focused
checks pass Typography 355/355, integration 279/279 and shared controls 231/231,
with empty captured-error reports. No full catalogue or manual accessibility run
was repeated for this layout change.

Typography level highlighting adds 62 cases (417 Typography checks): each of the
five current options selects exactly its row, exposes a non-colour selection cue,
preserves focus/model/exports/storage/document and fits both themes at
320/390/1440px. Leave/return checks clear and restore the selection appropriately.
Focused runs pass Typography 417/417, integration 279/279 and shared controls
231/231 with no captured errors. These results do not imply a new full catalogue
or manual accessibility review.

The adopted six-stage workflow retires 42 generated cases for the removed rhythm
and context stages, updates their ownership/navigation expectations, and adds 22
merge regressions. Typography now passes 397 checks, covering exact order and
numbering, merged component/review UI, independent body/heading Save/Discard/Reset
and canonical/legacy routes. The affected Typography, shared-control, integration,
navigation, view-update, wireframe and export-pipeline suites pass 1,331 assertions
with no captured errors; export byte fixtures are unchanged. This focused run is
not a new full catalogue or assertion-name Counter audit. Historical counts above
describe their recorded revisions; manual accessibility and other browsers remain
unchecked for this change.

The unified Typography learning workspace replaces the sequential-stage layout
and per-stage actions. Its 118 current checks retain core scale/codec/font cases
and cover live detached drafts, atomic Save/Discard, both persistent previews,
all eight selected levels, pointer/keyboard selection, comparisons, Configure
routes, proposed font loading/failure/stale callbacks, scoped resets, inert/blank
Architecture wording and real introduction/card selection in both sample modes.
Layout checks cover light/dark at 320/390/768/1440px. Assertions specific to retired
moving specimens, sequential navigation and independent stage Save bars have
been superseded; the lower count does not represent lost core model coverage.
All 19 current offline browser suites pass after targeted fixes/reruns: 3,317
assertions, 20 empty error reports, 12 runner contracts and 74 structure assets.
The final report is `.unified-type-validation-summary.log`. The first navigation
run found removed lesson/inspector hooks; restored hooks pass its final 158 checks.
Export byte fixtures pass unchanged. These are current local results; the table
below preserves its historical baseline. Desktop screenshot inspection was
performed; manual accessibility, other browsers and live CDN remain unchecked.

The compact learning-sample follow-up adds 20 Typography assertions (138 total):
all eight labelled roles remain visible at their actual draft sizes, each selects
and highlights its exact example, the header fills the sample width independently
of 40/85ch reading measure, and H3/H4 share a row with compact default height.
Current focused results pass Typography 138, shared controls 231, integration
279 and view updates 16 (664 assertions, no captured errors). Earlier full-catalogue counts above
remain historical; this does not imply a new complete-catalogue or manual
accessibility run.

Removing the superseded Typography review group adds 14 assertions (152 total),
covering the five-topic interface, inline readouts for all eight selected roles,
button-editor shortcut/focus and legacy review/context routes. View-update checks
now use the visible sample button and verify inline weight readouts. Focused
Typography 152, navigation 158, view updates 16 and integration 279 pass (605
assertions; no captured errors). The first integration run had one preview-example
selection failure; a diagnostic-preserving rerun passed without a related runtime
change. This is a focused run, not new full-catalogue or accessibility validation.

The shared CSS/calculation panel adds 14 Typography assertions (166 total):
placement outside settings groups, unnumbered headings, detached draft size CSS
and endpoints, viewport changes retaining proposed limits, Copy CSS without a
commit, Discard restoration, all eight actual exported size-token declarations
and continued visibility. Current focused checks pass Typography 166, integration
279, shared controls 231 and export pipeline 98 (774 assertions; empty error
reports). Export bytes remain unchanged. Earlier full-catalogue counts above
remain historical; this is not a complete-catalogue or accessibility rerun.

The Responsive typography reorder updates the placement/collapse expectations
and adds explicit viewport-slider ownership coverage (Typography 167 checks).
Explore the viewport owns its width control and graph; Generated CSS and the
calculation is last in Responsive typography. Typography 167 and integration
279 pass (446 assertions, no captured errors), with 74 structure assets and clean
whitespace checks. These focused results supersede placement expectations for
the preceding layout; no full-catalogue or manual accessibility rerun is implied.

Making Learning preview collapsible adds five assertions (Typography 172 total)
and revises the global CSS placement/collapse expectations. Coverage includes
native disclosure semantics, CSS/ladder visibility while collapsed, continued
draft CSS updates without saving, safe reopening and legacy routes. Current
Typography 172, integration 279 and view updates 16 pass (467 assertions, empty
error reports), with 74 structure assets and clean whitespace checks. Earlier
placement/full-catalogue results remain historical; manual accessibility and
other-browser testing were not repeated.

Wireframe's Low Fidelity default adds three startup regressions (155 Wireframe
checks): selected-tab semantics, the initial low-fidelity document, and a default
low-fidelity download without project/CSS changes. High-fidelity paint fixtures
still select that view explicitly. Wireframe 155 and integration 279 pass (434
assertions, no captured errors), with 74 structure assets and clean whitespace
checks. Engine programmatic defaults and website exports remain unchanged. This
is a focused run; historical full-catalogue counts above are unchanged.

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
gate. The final PR revision `8bbbdac` also passed all 20 jobs in
[CI run 43592914240](https://github.com/davis-boudreau/webdesignstudio/actions/runs/43592914240).
After user approval, [PR #1](https://github.com/davis-boudreau/webdesignstudio/pull/1)
was merged as `9b1d1c7`. [Pages run 43594084678](https://github.com/davis-boudreau/webdesignstudio/actions/runs/43594084678)
passed all 21 validation/deployment jobs and published the site. Uncached HTTP
checks confirmed that public index.html and all 71 referenced assets matched
committed Git bytes (72/72 checks). Repository Pages publishing is now configured
as `build_type: workflow`, matching the validation-gated Actions deployment.
Local Bash checks exercised all 16 success/failure/cancelled/skipped combinations
of gate prerequisites: only `success/success` passes. A failing command piped through
`tee` also retains its exit status and writes the diagnostic log under `pipefail`.

`python scripts/font_cdn_review.py` is an optional external-service smoke check;
the offline typography suite uses deterministic local font fixtures. It is not
part of CI. Manual keyboard/screen-reader/zoom/reflow, additional-browser reviews
and browser/OS file-chooser, download and clipboard permission behavior remain
outside this automated baseline. Passing these checks does not establish full
accessibility or successful browser/OS file saving.
