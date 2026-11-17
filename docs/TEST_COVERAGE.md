# Test coverage and validation ownership

The application has no build step or runtime network dependency. Run
`python scripts/review_suites.py` for the complete offline check set, followed by
`git diff --check`. The catalogue runs structure checks, runner contracts and all
21 browser suites in independent processes. It finishes every command and returns
nonzero if any command failed. `--list` prints commands; `--matrix` prints the CI
browser matrix without importing suites or launching Chrome.

Browser runs use separate local servers and temporary profiles. They never use
the user's browser profile or saved projects. `CHROME_BIN` can select Chrome,
Chromium or Edge. The runner rejects failed assertions, captured JavaScript
errors, nonzero browser exits, malformed/empty reports and incomplete harnesses.

## Suite ownership

Accordion follow-up: the documentation-only handoff run 44073640483 catches an
intermittent native alignment failure (144/145) and blocks deployment. A focused
late-growth reproduction fails 0/1 before, passes 1/1 after. The consistency suite
now deliberately grows preceding content after opening and adds four manual
wheel-cancellation cases: 149/149 focused checks pass with empty errors. A fresh
complete catalogue and exact-head hosted validation are pending. The preceding
publication evidence below describes its own verified revision.

Final release validation, 17 November 2026:
[CI run 44071416209](https://github.com/davis-boudreau/webdesignstudio/actions/runs/44071416209)
passes all 23 jobs on its first attempt for exact feature head d063847: checks,
all 21 browser suites and the required gate. PR #3 is merged as f71bdbf.
[Pages run 44072502110](https://github.com/davis-boudreau/webdesignstudio/actions/runs/44072502110)
passes all 24 validation/deployment jobs on its first attempt. The 4,153-assertion
inventory, 12 runner contracts and 84 assets are validated. Uncached public index
and asset comparisons match the merged Git bytes, 85/85 checks, with Pages built
and HTTPS enforced. This final handoff changes documentation only. Earlier failed
runs and focused corrections below retain their own results; no full manual
accessibility or cross-browser audit is implied.

17 November 2026 consistency work adds interaction_consistency_review.py: native
accordion alignment and cancellation in nested scrollers at 320/1440px and both
Studio appearances; generated CSS and component selection across eight added
learning views; native input/change theme sequences; per-theme colour overrides;
local save, downloaded JSON and reimport; brand proposals, shade families and
component highlights. Focused result: 144/144 with empty errors. Existing learning
checks pass 114/114; structure verifies 84 assets and runner contracts pass 12/12.
The selection-preservation extension passes 145/145. The complete local catalogue
finishes 21/23 commands: Typography has a local script-load failure (clean rerun
184/184), and Palette measures stale closed-disclosure geometry (843/844).
Opening the actual Neutral view/reference and requiring both to be visible
corrects that fixture; Palette then passes 844/844. Every other suite passes.
The final successful suite inventory is 4,153 assertions across 21 browser suites
(22 launches), plus 12 runner contracts and 84 assets. Hosted CI subsequently
validates the final exact head as above; the local catalogue was not repeated
after focused fixes.
These results are separate from the dated prior validation below. Screenshots
are visual checks, not a complete accessibility audit.

Typography selector correction, 16 November 2026: two additional learning checks
dispatch native select input followed by change and verify actual specimen text
colours, selected theme and preserved draft/Studio appearance in both directions.
Before the correction, 113/114 pass; after it, 114/114 pass. The full catalogue
finishes 21/22 commands because responsive preview captures a local
section-accordions.js resource-load error (155/157); its unchanged isolated rerun
passes 157/157 with empty errors. All other suites pass. The assertion inventory
with that clean rerun is 4,008. The following baseline describes the earlier run.

The local shared-learning-preview feature adds learning_previews_review.py to the
catalogue. It owns exact saved/candidate stylesheet parity, all four CSS quick
views, shared website themes in both sample modes at 320/1440px, independent safe
teaching content, draft/storage/export isolation, local ARIA references, snapshot
purity, font loading/fallback inside isolated documents and readable editing
annotations with transparent project colours. Its 112 checks use local font
fixtures. Current-session local validation passes all 22/22 catalogue commands:
4,006 browser assertions across 20 suites (21 browser launches), 12 runner
contracts and 83 assets, with empty captured browser error lists. Export fixtures
are unchanged. Existing owner
suites retain their assertions, with new document lookups, deliberate independent
copy expectations and browser subpixel comparisons against rounded size readouts.

Final feature release validation, 16 November 2026:
[CI run 43960139274](https://github.com/davis-boudreau/webdesignstudio/actions/runs/43960139274)
passes all 21 jobs on its first attempt for feature head 07a19c4: checks, all 19
offline browser suites and the required structure gate. The current assertion
inventory is 3,894, with 12 runner contracts and 81 assets. PR #2 is merged as
8729662. [Pages run 43961315128](https://github.com/davis-boudreau/webdesignstudio/actions/runs/43961315128)
passes all 22 validation/deployment jobs on its first attempt. Uncached public
index/asset comparisons match the merged Git bytes, 82/82 checks
(.release-publication-verified.log). Pages reports built, workflow publishing and
HTTPS enforced. No new manual accessibility or live-browser interaction review
is implied. Earlier failures, local focused checks and historical baselines below
describe their own revisions. This release handoff changes documentation only.

A subsequent preview focus probe reproduced a lost programmatic hero target after
HTML replacement (1/2 before, 2/2 after): temporary tabindex=-1 was missing from
the replacement node. The restoration fix preserves that temporary target and
restores focus only if the iframe held focus, preventing Studio editor focus from
being taken. Eight new responsive-preview cases cover both samples/themes, live
target restoration, unchanged exported tabindex and retained Studio focus (157
cases; catalogue inventory 3,894). Final local responsive preview passes 157/157,
integration 279/279 and shared actions 234/234, with empty captured errors;
structure verifies 81 assets and diff checking passes. Final hosted revalidation
passes all 21 jobs as recorded above. The preceding alignment revision's run
43957756291 succeeded on its
unchanged failed-jobs retry after a 278/279 integration result; it does not validate
this later focus correction. See PROGRESS for separate before/after evidence.

The subsequent hosted release run 43955275407 found a real light-320px preview
alignment failure in shared property actions (230/231); all 18 other browser
suites passed and the required gate blocked merge. The scroll correction adds
three property-action regressions (234 total): late sticky-header overlap in both
themes with preserved focus/model/storage/document/drafts, and cancellation when
focus moves elsewhere. A focused before/after reproduction is 4/5 then 5/5;
these checks overlap the tracked suite. Final local shared actions passes 234/234
and navigation 158/158, plus integration 279/279, with empty errors. Structure
passes 81 assets and diff checking passes; final hosted revalidation passes as
recorded above.
These three new assertions bring the catalogue inventory to 3,886;
the dated 3,883-assertion audit below describes the preceding revision.

Current audit, 16 November 2026: the complete catalogue finished 20/21 commands
(.audit-2026-11-16-checks.log). Its sole failing suite was Contrast (87/90): the
fixture opened the inner saved review while its new outer Buttons reference
disclosure remained collapsed. A one-line fixture correction reveals that ancestor
through buttonWorkspace.revealControl; all assertions and runtime code remain
unchanged. Final python scripts/contrast_review.py passes 90/90 with empty errors
(.audit-2026-11-16-contrast-final.log). Together these final results cover all 19
offline browser suites, 3,883 passing assertions and 20 empty captured-error
reports, plus 12 runner contracts and 81 structure assets. Integration passes
279/279; export byte fixtures pass unchanged (98/98). Structure and git diff
--check were rechecked successfully. This is a full run plus focused correction/
rerun, not a new single 21/21 invocation or assertion-name Counter audit. Manual
accessibility, Firefox/Safari, browser/OS permissions and learner observation
remain open. The historical table and dated results below retain their own counts.

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

The Content Plan report adds 37 content-tree assertions (238 total): complete
numbered containment hierarchy and twelve-level support, sample/project and
readiness totals, current/proposed/empty/missing content, escaped hostile text and
plain references, standalone HTML download, unsaved-form and storage isolation,
Save/Undo, stable DOM on unrelated styling, explicit empty plans and light/dark
layout/targets at 320/390/1440px. The previous Studio inventory-layout assertion
now checks the complete report while retaining the Advanced export's nested-map
expectation. Both report styles and downloads use shared authored helpers.

Current content-tree 238, integration 279, planning 76 and export pipeline 98
pass (691 assertions; empty error reports), with 74 structure assets and clean
whitespace checks. Export byte fixtures are unchanged. A focused 37-check report
harness also passes after the final heading-size refinement. Initial failures
caught a dropped report stylesheet on artifact refresh; the refresh now retains
report CSS. Earlier full-catalogue counts remain historical; manual accessibility
and other browsers are not established by these checks.

Shared colour-selector previews add 52 Palette assertions (672 total), covering
Body/Header/Main/Footer brand/neutral lists, semantic choices and visible roles,
UI anchors, button sources, dynamic state choices, actual swatch colours, original
native control identity/focus, pointer cancellation, keyboard browsing/type-ahead,
disabled options, dismissal, draft/Save/Discard/contrast boundaries, imports,
hide/show, queued feature updates and light/dark geometry at 320/390/1440px.
A viewport-fixed edge fixture checks available popup space. A toggle fixture
reproduced a late native-value update leaving stale swatches; settled refresh
fixes it. Original non-colour selectors and export bytes are unchanged.

Current focused suites pass Palette 672, shared properties 231, integration 279,
navigation 158, view updates 16 and export pipeline 98 (1,454 assertions, empty
error reports). The final swatch-only matrix also passes 53 checks. Structure now
checks 76 assets; whitespace checks pass. This is a focused run, not a repeated
full catalogue. A desktop open-menu capture was inspected; manual keyboard/touch,
screen-reader, other-browser and live-CDN review remain outstanding.

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

## Colour sources and grouped Brief verification (15 November 2026)

Palette coverage now includes None/default choices for page regions, semantic
proposals, anchors, button sources and state assignments; staged reference edits;
source following and CSS variable output; both-theme import/save behavior;
removed-token fallbacks; feedback-state cache invalidation; hostile references and
display names; all valid brand suffixes; and omission of empty source metadata.
The focused new matrix passes 71/71 (.brief-colours-sources-final.log); it overlaps
the full Palette suite and must not be added to its assertion count.

Planning adds two assertions for the three labelled Brief groups and guidance
that leaves saved data and drafts untouched: 78/78 pass. The final integration
run passes 279/279, shared actions 231/231 and export pipeline 98/98; structure
passes with 76 assets and git diff --check passes. Final full Palette coverage
passes 742/742 (.brief-colours-palette-complete.log). These five focused suites
pass 1,428 assertions with empty captured-error reports; the separate 71-check
matrix overlaps Palette. Earlier full-catalogue results remain historical.
Manual keyboard/touch, screen-reader, other-browser and live-CDN testing remain
outside this session's verification.

## Confirmed transparent None (15 November 2026)

The user's clarification supersedes the earlier None/default interpretation.
Palette now distinguishes transparent paint from Use default, while raw HEX and
source references continue generating shades. New coverage owns both-theme
Save/Discard/import, live paint, native None toggles, transparent foreground/focus
contrast, retained button anchors, browser Canvas compositing and standalone
Basic/Advanced regions/cards/buttons. The final focused matrix passes 77/77 (.transparent-focused-labels-verified.log);
it overlaps the expanded full Palette suite. Strengthened default restoration to
assert immediate live-CSS synchronization after transparent-only edits.

Current shared-actions checks pass 231/231, exports 98/98 and reduced-motion /
forced-colour checks 7/7 + 9/9. Default export byte fixtures are unchanged. Final
sequential full Palette passes 818/818 and integration 279/279, bringing these five
focused suites to 1,442 assertions. The separate 77-check matrix overlaps Palette.
Concurrent runs each hit an existing scroll/focus assertion once; sequential runs
pass with empty captured-error reports. Parallel timing remains an observed gap. Added diagnostics to an existing
Typography journey assertion without weakening its checks. Manual keyboard/touch,
screen-reader and other-browser testing remain pending.

## Clamp lesson (15 November 2026)

Typography adds twelve checks for the initially collapsed calculation disclosure,
non-mutating expansion, proposed limit/slope/offset/rem values, the eight fluid/
constant/fixed role cases and equal-heading guidance. The focused Typography
suite passes 184/184 (.clamp-lesson-typography.log), with empty captured errors.
Integration passes 279/279 (.clamp-lesson-browser.log); these two suites total
463 assertions with empty captured errors. Structure verifies 76 assets and
git diff --check passes. Expanded-lesson visual checks pass 4/4 at 320/390px in
light/dark (.clamp-lesson-visual.log). The desktop screenshot is
work/reviews/clamp-calculation-lesson.png. Manual keyboard/screen-reader and
other-browser review remain pending; older suite totals are historical.

## Page background learning workspace (15 November 2026)

Palette adds a focused learning-page matrix for control/preview/action placement,
clickable region labels, theme-wide multi-region drafts, token references, alpha
and transparency, actual extra padding, Save/Discard, theme isolation, unrelated
saved updates, invalid fields, safe project wording, saved-page focus and 320/
390/1440px light/dark layouts. The final focused matrix passes 30/30
(.background-learning-focused-verified.log), including transparent diagnostic
contrast and a Custom HEX selection that previously displayed the None label.
These assertions overlap the full Palette suite and are not added to its count.
Final broad runs pass Palette 847/847, shared actions 231/231, integration 279/279
and export pipeline 98/98: 1,455 assertions with empty captured-error reports.
Structure verifies 77 assets and git diff --check passes. Inspected
work/reviews/background-learning-workspace.png; the final visual smoke passes 1/1
(.background-learning-visual-final.log). Manual keyboard/touch, screen-reader and
other-browser review remain pending. See PROGRESS for exact log paths.

## Body padding across page views (15 November 2026)

The focused Body matrix passes 43/43 (.body-padding-focused-verified.log),
overlapping the final spacing suite. It checks exact draft insets, reset/discard,
four independent sides, token navigation, JSON validation, Basic/Advanced pages,
both themes and low/high wireframes, including live frames and 64px at 320px.
Final spacing passes 265/265 (.body-padding-spacing-final.log), integration
279/279 (.body-padding-browser-final.log) and exports 98/98
(.body-padding-export.log): 642 assertions with empty captured-error reports.
The intentionally refreshed export baseline adds 259 bytes to CSS/shared CSS in
all 16 cases for the four Body tokens and rule; HTML hashes are unchanged.
Structure verifies 77 assets and git diff --check passes. Inspected
work/reviews/body-padding-linked.png; the final visual smoke passes 1/1 with
empty errors (.body-padding-visual-final.log). The full wireframe suite was not
rerun; the focused matrix covers the affected geometry. Manual keyboard/touch,
screen-reader and other-browser review remain pending.

## Unified Buttons workspace (15 November 2026)

Components adds regressions for detached geometry/colour proposals, full-matrix
and theme parity, proposed contrast, variant switching, latest shared focus,
transparent focus replacement, combined Save/Discard, unrelated Palette drafts,
JSON/live CSS, reset followed by a new edit, transparent None, narrow full-width
buttons, all seven CSS lessons, focus retention, contextual/matrix selection,
responsive-preview routing, control height, responsive layout and project import.
The final component run passes 98/98 (.button-workspace-components-complete.log),
with empty captured errors. Shared actions pass 231/231
(.button-workspace-actions.log), exercising the actual workspace action bar.
Palette passes 848/848 (.button-workspace-palette-verified.log), including the
new invalid-background-draft reset regression and updated Buttons token routes.
Its focused sizing/reset matrix passes 18/18 and overlaps the broad suite.
Palette and shared actions ran before the final shared-focus paint-clear cleanup;
the final component run covers that cleanup and its cross-variant regression.
Final integration passes 279/279 (.button-workspace-browser-verified.log), exports
98/98 (.button-workspace-exports.log) and media modes 7/7 + 9/9
(.button-workspace-media.log), all with empty captured errors. The six affected
suites total 1,570 assertions; focused/visual runs are not added. Integration also
checks ownership of derived button-state shade tokens, with diagnostics naming
misrouted tokens. Export byte fixtures remain unchanged for this work.
Structure verifies 79 assets and diff checking passes. Inspected the desktop screenshot
work/reviews/button-learning-workspace.png; the final visual smoke passes 1/1
with empty errors (.button-workspace-visual-final.log). These are affected suites,
not a complete repeated 19-suite catalogue. Trusted keyboard/touch, screen-reader
and other-browser testing remain pending.

## Five-variant Button learning preview (15 November 2026)

Components now verifies all five visible action labels, each variant's editor
route/current indication and draft preservation, plus wrapping in both website
themes at 320/390/1440px. The complete component suite passes 109/109 with empty
captured errors (.button-variants-components.log). Required integration passes
279/279 with empty errors (.button-variants-browser.log): 388 assertions across
both suites. Visual smoke passes 1/1 (.button-variants-visual.log); the refreshed
work/reviews/button-learning-workspace.png shows all five variants together.
Structure verifies 79 assets and diff checking passes. Saved models
and export generation are unchanged; earlier export/media results are historical.
Manual keyboard/touch, screen-reader and other-browser review remain pending.

## Contextual Buttons CSS lessons (15 November 2026)

Components verifies every Size/spacing, Shape/type, Colour/token and State/behaviour
control against its short teaching topic, proposed token value and explanation.
Checks include both size multipliers, all colour overrides/source/custom/focus,
focus width, timing, mobile opt-in, transparent paint, all seven states, balanced
CSS blocks with reduced-motion rules, focus-only topic changes, saved-output
isolation and Save/Discard parity. Light/dark colour scope and transparent tokens
are explicit. Final Components passes 149/149 with empty captured errors
(.button-css-components-final.log). Integration passes 279/279
(.button-css-browser.log) and exports 98/98 (.button-css-exports.log), all with
empty captured errors: 526 assertions across these three affected suites.
Export fixtures remain unchanged. Visual smoke passes 1/1 (.button-css-visual-final.log);
the screenshot is work/reviews/button-css-lesson.png.
Structure verifies 79 assets and diff checking passes. Earlier full Palette/media
results are historical; manual keyboard/touch, screen-reader and other-browser
review remain pending.

## Spacing and surfaces learning workspace (15 November 2026)

The new focused matrix passes 46/46 (.spacing-workspace-focused.log), overlapping
the expanded Spacing suite. It covers normalized draft geometry/surfaces,
computed padding/margins, independent grid gap, ladder arithmetic, guides and
selection, one Save/Discard boundary, unrelated Palette drafts, Accessibility
height ownership, JSON, both samples/themes at 320/390/1440px, responsive preview,
token navigation and project replacement. Additional checks cover independent
button geometry/saved size classes and the Surface colour source link.

The initial full Spacing result was 292/310 with empty captured errors; 18 assertions
still required the previous lesson/control/utility placement. Updated fixtures
open the actual disclosures and assert the new owners without dropping their
arithmetic, layout, focus or saved-output checks. Final Spacing passes 313/313
(.spacing-workspace-spacing-final.log) with empty captured errors.
Shared actions pass 231/231, Components 149/149, required integration 279/279 and
exports 98/98, all with empty captured errors (.spacing-workspace-actions.log,
-components.log, -browser.log and -exports.log). Export fixtures remain unchanged.
These five affected suites total 1,070 passing assertions; focused checks overlap
Spacing and are not added. Visual smoke passes 1/1 (.spacing-workspace-visual.log);
inspected work/reviews/spacing-learning-workspace.png, with contextual CSS placed
before the complete ladder. Structure verifies 81 assets and diff checking passes.
Manual accessibility/other-browser review remains pending; these affected suites
do not constitute a full catalogue run.

## Buttons website theme and elevation (15 November 2026)

The focused feature matrix passes 47/47 (.button-elevation-focused-final.log),
overlapping Components. It verifies default flat appearance, per-variant proposals,
light/dark synchronization and token values, Studio independence, draft retention,
combined Save/Discard, JSON round trip, seven states in both themes, standalone
Basic/Advanced styles, combined pressed/toggle layers, actual focus, token routes,
None removal, narrow controls and strict/legacy import validation. Components also
checks loading a locally saved project and readable teaching instructions outside
the dark website sample. Final Components passes 197/197
(.button-theme-shadow-components-final.log); final integration passes 279/279
(.button-theme-shadow-browser-final.log), both with empty captured errors.
Model passes 14/14 (-model.log), media modes 9/9 + 11/11 (-media.log) and shared
actions 231/231 (-actions.log). The media suite enables elevation before checking
actual reduced-motion and forced-colour rendering, outlines and checkmarks.

Initial exports passed 97/98 with matching byte fixtures but a failed local load
of unchanged clamp-explorer.js. Confirmed its presence and reran without changing
source/fixtures: exports pass 98/98 with empty errors
(.button-theme-shadow-exports-final.log). Other named broad logs share the prefix
.button-theme-shadow. The initial visual check exposed Studio-coloured instruction
text inside a dark project sample; moved instructions to the Studio surface and
added a contrast regression. Final Light/Dark visual checks pass 4/4
(.button-theme-shadow-visual-final.log), including instruction contrast. Captures:
work/reviews/button-theme-elevation-light.png and button-theme-elevation-dark.png.
The six affected suites total 839 passing assertions; focused/visual checks are
not added to that count. Structure
verifies 81 assets and diff checking passes. Manual focus/shadow visibility,
keyboard/touch, screen-reader and other-browser review remain pending; a full
catalogue rerun was not performed.


## Unified semantic colours and backgrounds (15 November 2026)

Final Palette passes 844/844 (.semantic-workspace-palette-final.log), required
integration 279/279 (-browser.log) and shared actions 231/231 (-actions.log), all
with empty captured errors. Log names share the .semantic-workspace prefix.
These affected suites total 1,354 assertions; the full catalogue was not repeated.
Palette includes placement of the learning sample, six visible stages, all 21
selectable roles, detached colour/None/token proposals, invalid HEX, Discard and
region-to-role synchronization. Existing background paint, alpha, padding, theme,
Save/storage/export-isolation and responsive controls remain covered. The first
palette run passed 830/842 before correcting obsolete layout/visibility fixtures
and the compatibility route's disclosure handling; final coverage supersedes it.

Light/Dark visual review passes 4/4 each (.semantic-workspace-visual.log) for sample
placement, desktop columns, theme/role availability and viewport fit. Inspected
work/reviews/semantic-learning-light.png and semantic-learning-dark.png. These
visual checks overlap and are not added to the broad count. Structure verifies
81 assets; diff checking passes. No project schema or export fixture changes were
needed for this UI refactor. Trusted keyboard/touch, screen-reader and other-browser
manual testing remain open; these checks do not establish full accessibility.
