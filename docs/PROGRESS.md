# Project progress

Updated: 12 November 2026 (America/Halifax).

## Site-specific Brief placeholders (12 November 2026)

- Replaced the generic Write one or two sentences placeholder in all seven Brief
  editors with distinct Web Design Field Guide examples. They cover students and
  tutors; Basic/Advanced lessons, layout/component examples and forms; lesson copy,
  DS assets and descriptions; responsive/keyboard/theme requirements; HTML/CSS/JSON
  handover; and observable student tasks. Review date, available time, ownership
  and approval remain explicit items to confirm instead of invented commitments.
- Kept these as escaped placeholder attributes in the existing brief-field
  definitions. They guide empty fields; they are not saved brief answers. Refreshed
  the design-process.js query version in index.html. This is a copy-only change.
- Commands: python scripts/check_structure.py verifies 68 assets; git diff --check
  passes. Temporary python .brief-placeholders-review.py inspected all seven
  rendered placeholders with blank values and reused the nine existing Brief
  checks: 9/9 pass, no JavaScript errors (.brief-placeholders-review.log). These
  cover labels/prompts, old saved drafts, JSON/export round trips, validation,
  escaped draft text and reset. Temporary helper removed after inspection.
- The full browser suite was not repeated for this copy-only update; the previous
  2793/2793 result below is historical. No new manual keyboard, screen-reader or
  narrow-screen visual review was performed for these example strings.

## Centre Brief and local project identity (12 November 2026)

- Moved the existing Brief pane into its centre lesson at every width. The seven
  prompt editors and starting preset retain their nodes/listeners. Named the form
  Develop the project brief. The sidebar now holds step navigation and the local
  project library instead of the full Brief form.
- Moved the original Project name field above Saved designs in My local projects,
  outside step-specific panes. Its state, local autosave, new/load/reset and JSON
  bindings remain shared. No saved-project schema change or cloned editors.
- Updated the existing responsive placement rule to keep Brief in the centre on
  both sides of the 900 px breakpoint. Set its preset selector to a 44 px minimum
  height. Refreshed studio-learning.js/design-process.css asset query versions.
- Current validation: python scripts/check_structure.py verifies 68 assets;
  git diff --check passes. Temporary python .brief-centre-review.py passes 12/12
  focused checks with no JavaScript errors: placement at 320/390/1440 in light/dark,
  original node identity, naming from another stage without navigation, autosave,
  local project load and JSON restore (.brief-centre-focused.log). Initial layout
  checks found the 39 px preset selector; its height is corrected. Screenshots
  inspected for desktop/light and 320 px/dark Brief. Button-state checks pass
  7/7 reduced-motion and 9/9 forced-colour (.brief-centre-buttons.log).
- Full python scripts/browser_review.py passes 2793/2793 with no JavaScript errors
  (.brief-centre-browser.log). Temporary helpers/screenshots removed; ignored logs
  retained. Updated README and architecture notes. Previous results below remain
  historical. git diff --check passes after the documentation update.
- Completed this layout change. Full manual keyboard-only and assistive-technology
  review remains unperformed; next usability work can follow the learner trials.

## Typography heading scroll fix (12 November 2026)

- Reproduced the reported jump when opening Choose font families and other
  Typography stage headers. The native toggle opened the requested stage and
  closed its expanded sibling above, moving the shared preview and page geometry,
  but called show(key,false) without revealing the new heading. All 14 direct-open
  checks failed before the fix at 320/1440 px; the two collapse checks passed.
- Direct summary activation now completes the shared accordion transition and
  explicitly reveals its heading. Focus uses preventScroll before the deliberate
  heading scroll. Clicking an already-open summary still collapses it; optional
  reference disclosures and silent programmatic synchronization keep their roles.
- Added regression checks for all seven subsequent stages at phone/desktop widths,
  visible destination/focus, one open stage, unchanged project data and collapse.
  Updated architecture notes, learner-trial prompts and affected asset versions
  in index.html.
- Current commands/results: python scripts/check_structure.py verifies 68 assets;
  git diff --check passes. Temporary python .type-scroll-review.py reproduced
  2/16 before and passes 16/16 after, with no JavaScript errors. Full
  python scripts/browser_review.py passes 2781/2781 with no JavaScript errors
  (.type-scroll-browser.log). python scripts/button_states_review.py passes
  7/7 reduced-motion and 9/9 forced-colour checks (.type-scroll-buttons.log).
  Temporary helper removed; ignored before/after logs retained. Previous results
  below remain historical for this fix.
- Completed this bug fix. Full manual keyboard-only and assistive-technology
  testing remain unperformed; next usability review can use the learner prompts.

## Typography preview before properties (12 November 2026)

- Moved the shared website-text specimen to the top of the right column before
  the properties heading in all eight Typography stages. Viewport/enlargement
  controls, user-spacing comparison, scope note and current website/type/size
  metadata travel together. This also covers the dynamic font and rhythm headings.
- Moved the specimen divider below its content and removed its leading spacing
  so it fits the top of the properties panel. Existing fields, shared model and
  comparison behavior are reused. Refreshed both runtime asset query versions.
- Updated architecture notes and existing stage checks to verify the specimen is
  immediately before the properties heading. Commands so far:
  python scripts/check_structure.py (68 assets), git diff --check (pass).
  Focused isolated-browser review passes 77/77 with no JavaScript errors, including
  preview-first DOM order in all eight stages and phone/desktop layouts in both
  Studio themes (.type-preview-first-focused.log). Inspected desktop/light and
  phone/dark Body screenshots; preview controls, specimen and divider precede
  Selected properties. Temporary helpers/screenshots removed after inspection.
  Full python scripts/browser_review.py passes 2765/2765 with no JavaScript errors
  (.type-preview-first-browser.log). Earlier results below remain historical.
- Completed this layout change. Full manual keyboard-only and assistive-technology
  testing remain unperformed; next usability work can follow the learner trials.

## Guided Typography workspace implementation (12 November 2026)

- Implemented the approved eight-stage Typography process: content, families,
  body readability, hierarchy, rhythm, responsive type, component context and
  review. The sidebar now holds navigation; each centre stage has browse/help
  and selected-properties columns. One specimen follows the active stage.
- Relocated original controls/listeners, retained hidden legacy aliases and
  canonical Configure/fragment routes. Scoped resets preserve unrelated settings.
  Generated role sizes/CSS remain read-only. The bare legacy visual-role select
  now has its own field in the browse column, rather than remaining hidden in
  the legacy calculator. Regression checks verify its visible location in both
  Hierarchy and Responsive. No project schema changes.
- Specimens use safe text from the generated Architecture website. Component
  context reads the existing live preview's computed styles. Enlargement and
  spacing overrides are temporary, labelled and cleared on import/reset.
  Background synchronization preserves the current global lesson and focus.
- Added module/CSS and asset query versions in index.html. Updated README,
  architecture notes and unperformed learner-trial prompts. Added browser coverage
  for stage navigation, real wording, scoped edits/resets, saved-state round trips,
  canonical routes, hostile text, background focus and all eight layouts at
  320/390/1440 px in both Studio themes. Range controls now have 44 px targets;
  local headings use the measured sticky-header scroll offset.
- Final standard browser run: 2765/2765 passed, no JavaScript errors
  (.type-workspace-verified-browser.log). This verifies the visible role selector
  and closed-disclosure layout rule. Final text-node cleanup also passes all
  77 focused Typography checks (.type-clean-review.log). Font/loading compatibility
  checks pass 37/37; earlier focused Typography/sequence checks pass 117/117.
  Structure verifies 68 assets; git diff --check passes. Button-state checks pass
  7/7 reduced-motion and 9/9 forced-colour.
- Earlier full runs had five narrow-screen overflow failures (2758/2763 and
  2760/2765). Diagnostic inspection found stale closed-disclosure geometry;
  explicitly hiding closed local detail contents resolved all five in the final
  standard suite. A temporary accelerated replay had two additional timing-related
  Palette failures; it was diagnostic only and is superseded by the standard run.
- Inspected isolated Chrome screenshots of desktop Body, phone Fonts and final
  phone Responsive with visible role selector and focus below the header. Removed
  a literal null text node left by the legacy calculator's missing-field prepend;
  the final phone screenshot and focused regression confirm its removal.
- Commands run: python scripts/check_structure.py,
  python scripts/browser_review.py, python scripts/button_states_review.py,
  git diff --check, plus temporary isolated-browser diagnostic/focused/screenshot
  helpers. Helpers and screenshots were removed after inspection; ignored logs
  remain. Refreshed the new runtime assets' query versions in index.html.
- Full keyboard-only, screen-reader, browser zoom/reflow and observed student
  trials remain unperformed. The specimen comparisons do not certify full-page
  accessibility. Next: conduct the learner trial prompts and record usability
  observations before expanding the saved typography model.

## Typography workspace analysis and proposed course of action (12 November 2026)

- User requested analysis of the whole Typography step and a step-by-step learning
  workflow using the Architecture approach. Reviewed index controls/specimens,
  studio-learning relocation/disclosures, font-sources, clamp-explorer, shared
  token outputs and Architecture/Palette workspace conventions.
- Findings: the sidebar mixes font choice, readable body text, tracking,
  responsive limits and font loading. Visible aliases repeat base/ratio/named
  scale and tracking settings (including different tracking-unit presentations).
  Practical specimens/tools are largely under More about typography. The size
  ladder uses generic text; the practice asks students to recreate frames in an
  external design tool. Existing controls already share one saved type model.
- Recommend a short sidebar navigator and an active centre workspace: browse
  relevant roles/items on the left, selected editable properties on the right,
  with an always-visible real-site content specimen and clear computed values.
  One visible editor per saved property; generated sizes/CSS remain read-only.
- Proposed local learning stages: content/context; font families/sources;
  body readability; hierarchy/scale; emphasis/rhythm; responsive type;
  component context; review/continue to Wireframe. Each stage teaches purpose,
  offers a bounded experiment and asks the learner to explain the visible effect.
- Reuse original controls/state/exports first; consolidate duplicate editors and
  move CDN/code/calculation details into contextual optional disclosures. Use
  actual Architecture website wording; content edits remain in Architecture.
  Fixed/generated type roles should not receive arbitrary CRUD. New custom
  styles or saved paragraph/word-spacing/alignment/variable-axis settings would
  require explicit shared-model/CSS/export work, separate from reorganizing UI.
- Reviewed official web.dev typography guidance and W3C understanding pages for
  resize text, reflow and text spacing. User spacing override tolerance is a test
  behavior, not a claim that authored sliders must use the override values:
  https://web.dev/learn/design/typography
  https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
  https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html
- This is an analysis/recommendation, not an implemented workspace redesign.
  No runtime assets changed and no browser/structure tests ran for this review.
- Next: implement the guided workspace using shared controls and real-content
  specimens; then validate navigation, responsive behavior, import/export,
  Configure-source links and propagation to both wireframe fidelities.

## Typography moved after Architecture (12 November 2026)

- User approved the process recommendation. Display order now begins Brief (1),
  Architecture (2), Typography (3), Wireframe (4), Palette (5), then Colour lab (6)
  and the existing remaining stages. Typography joins the contiguous Plan group
  with Brief, Architecture and Wireframe; Foundations now contains Palette/Colour
  lab. Stable internal typography/wireframe/palette indices remain 5/2/4.
- Updated registry stageOrder, planning/type/wireframe guidance, typography lesson
  explanation, sidebar fallback labels and Design workflow notes. Typography
  establishes a working baseline using actual content; Low Fidelity checks fit
  and reading order, while High Fidelity is revisited as appearance develops.
  Existing Previous/Next, progress, section ordering and token Configure labels
  derive their new visible positions from the shared registry.
- Script load order, control IDs, project schema, import/export and font/token
  generators are unchanged. Refreshed all four changed JavaScript asset versions.
  Updated README, architecture notes and unobserved learner-trial prompts.
- Focused browser run passed **42/42**, no captured JS errors
  (.early-typography-focused.log). Covers literal order/phase grouping, forward
  and reverse transitions, stable Configure routes and control identity, JSON
  round trip, visible token source numbering, 12-stage navigation at 320/1440px
  and actual Georgia/18px/1.6 leading/58ch settings in both samples/themes and
  both wireframe fidelities.
- python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. python scripts/button_states_review.py passed **7/7 reduced-motion and
  9/9 forced-colour**, no JS errors (.early-typography-button-states.log).
- Inspected Typography Step 3 with the reordered Plan group and Wireframe Step 4
  with the chosen type settings at 390px. Temporary helpers/captures removed;
  ignored logs retained.
- Final python scripts/browser_review.py passed **2,688/2,688**, with no captured
  JavaScript errors (.early-typography-full-browser.log). This includes the new
  sequence/compatibility/type-propagation tests and updated visible Palette step
  assertions. Required structure, browser, button-state and whitespace checks
  are complete.
- Manual keyboard/screen-reader, zoom and Firefox/Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of the content-to-type-to-layout flow and learner trial.

## Process review: typography after Architecture (12 November 2026)

- User requested an opinion/review on putting Typography after information
  architecture because text influences section/card sizing. Reviewed registry
  stageOrder, related architecture notes and the wireframe's shared CSS/font path.
- Current opening sequence is Brief, Architecture, Wireframe, Palette, Typography.
  Recommend Brief, Architecture, Typography, Wireframe, Palette, with an early
  working baseline for body/heading fonts, hierarchy, sizes, leading, measure and
  fluid scaling. Low Fidelity validates content fit; High Fidelity is revisited
  as palette/component/responsive decisions develop. Both already share exported
  CSS/font settings, so there is no separate wireframe typography model to build.
- Reviewed official web.dev typography and content-driven responsive guidance:
  https://web.dev/learn/design/typography and
  https://web.dev/articles/responsive-web-design-basics .
- This entry records analysis and a recommendation, not an implemented reorder.
  No runtime assets changed; no browser/structure tests were run for this review.
- Next if implemented: change display order through stageOrder while retaining
  stable control indices/routes; reconcile phase grouping, numbering, guidance,
  previous/next navigation, documentation and sequence regression expectations.

## Low Fidelity backgrounds cleared except buttons (12 November 2026)

- User requested no Low Fidelity background fills except buttons. Removed grey
  fills from layout groups, Header/Footer, form fields and logos. The canvas stays
  white; non-button object backgrounds are transparent. Button/action fills stay
  grey with white labels. Logo text now follows the normal dark neutral text.
- High Fidelity, object outlines, responsive geometry, view controls and selected
  fidelity exports retain their existing behavior. Updated Low Fidelity guidance,
  README and architecture notes and refreshed both changed JavaScript asset
  query versions.
- Strengthened the existing Low Fidelity paint assertion to require transparent
  backgrounds on every non-button body object and grey fills on buttons, across
  Basic/Advanced, both website themes and 320/1280px viewports.
- Focused run passed **50/50**, no JS errors (.wireframe-low-unfilled-focused.log).
  python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. python scripts/button_states_review.py passed **7/7 reduced-motion and
  9/9 forced-colour**, no JS errors (.wireframe-low-unfilled-buttons.log).
- Final python scripts/browser_review.py passed **2,646/2,646**, with no captured
  JavaScript errors (.wireframe-low-unfilled-browser.log). Required structure,
  browser, button-state and whitespace checks are complete. Temporary focused
  helper removed; ignored logs retained. Manual keyboard/screen-reader, zoom and
  Firefox/Safari remain unverified; automated passes do not establish full
  accessibility. No commit/push/deployment.
- Next: user review of the unfilled Low Fidelity view and learner trial.

## Low Fidelity and High Fidelity wireframe tabs (12 November 2026)

- User identified the existing coloured view as High Fidelity and requested
  Low Fidelity / High Fidelity tabs plus corrected wording throughout Wireframe.
- Added a labelled native-button tablist and shared tabpanel/iframe. Selected
  state, roving tabindex and Left/Right/Home/End activation are supported. High
  Fidelity starts selected to retain the current view. Both tabs share sample,
  viewport, scrolling, native disclosure state and object/container outlines.
- Low Fidelity adds white/grey surfaces, grey buttons/logos, neutral text/borders
  and greyscale images/SVGs over the same HTML and responsive boxes. Native
  checkbox/radio/range/progress accents are grey; native controls use a light
  colour scheme even when the website theme is dark. High Fidelity retains the
  existing website colours, imagery and component configuration.
- Fidelity is transient local view state, not a second saved website model.
  Engine createDocument/documentHtml accept a low/high fidelity option; absent or
  unknown values fall back to high. Download uses the selected tab. Frame title,
  summary, tab guidance and downloaded document title identify the fidelity.
- Cleaned up the workspace, sidebar, stage-registry guidance, generated website
  note and content-inventory description. Updated README, architecture notes and
  unobserved learner-trial prompts. Versioned all changed runtime assets.
- Initial and final focused runs each passed **140/140**, no captured JS errors
  (.wireframe-fidelity-focused.log / .wireframe-fidelity-final-focused.log).
  Final checks include native neutral accents/light control scheme, tab keyboard
  behavior, all-object geometry at 320/1280px, both samples/themes, white/grey
  paint, restored high styles, preserved disclosures, selected-tab download,
  unchanged project JSON and narrow Studio layouts in both Studio themes.
- python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. python scripts/button_states_review.py passed **7/7 reduced-motion and
  9/9 forced-colour**, no JS errors (.wireframe-fidelity-button-states.log).
- Inspected Basic/light Low Fidelity at 320px, Advanced/dark Low Fidelity at
  1280px and its High Fidelity counterpart. Temporary review helpers/captures
  removed; ignored logs retained.
- First full browser run did not complete: Chrome exhausted the existing
  185,000ms virtual-time budget after reaching check 2,540 (no final assertion
  report). Increased the harness budget to 225,000ms and wall timeout to 660s for
  the expanded coverage.
- Final python scripts/browser_review.py passed **2,646/2,646**, with no captured
  JavaScript errors (.wireframe-fidelity-final-browser.log). Required structure,
  browser, button-state and whitespace checks are complete. The incomplete first
  run above is retained separately from this final result.
- Manual keyboard/screen-reader, zoom and Firefox/Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of both fidelity tabs and an observed learner trial.

## Complete wireframe object boundaries (12 November 2026)

- User requested appropriate borders for all objects on the page. Extended the
  wireframe annotations from structural containers to every HTML body object:
  headings, paragraphs, inline spans, images, icons, links, buttons, form controls,
  table parts and decorative tracks. Generated ::before/::after objects also
  receive thin outlines. Metadata and line-break nodes are excluded; an SVG is
  outlined once around the drawing rather than around each internal shape.
- Added a lower-priority object kind; region/content/layout/item distinctions
  retain their stronger boundaries. Annotation titles identify page objects;
  setAttribute reflects these titles on SVG as well as HTML. Source visibility,
  responsive behavior and disclosures remain unchanged, so newly opened content
  already has annotations without revealing hidden controls or layouts.
- Borders remain paint-only outlines; website colours, backgrounds, button
  values, box dimensions and read-only behavior are preserved. Leaf objects yield
  to :focus-visible to keep the original distinct keyboard-focus ring.
- Updated the workspace legend, README and architecture notes; refreshed both
  changed wireframe JavaScript query versions. No project/schema changes.
- Preliminary focused run: **84/88**, no uncaught JS errors. It caught SVG title
  attributes needing reflection and a disclosure fixture selecting an invisible
  element. Corrected title assignment and fixture visibility; repeat passed
  **88/88**, no JS errors (.wireframe-objects-final-focused.log). Added explicit
  focus-ring regressions after reviewing CSS precedence; final focused run passed
  **90/90**, no JS errors (.wireframe-objects-complete-focused.log).
- python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. Preliminary button-state suite passed **7/7 reduced-motion and 9/9
  forced-colour**, no JS errors (.wireframe-objects-button-states.log).
  Final repeat after the focus fix also passed **7/7 and 9/9**, no JS errors
  (.wireframe-objects-final-button-states.log).
- Inspected Basic/light at 320px and Advanced/dark at 1280px: individual text,
  inline labels/icons, images and buttons have thin boundaries; parent containers
  remain distinct. Interrupted the first full run to include the focus-ring fix.
  Temporary captures/helpers removed; ignored logs retained.
- Final python scripts/browser_review.py passed **2,596/2,596**, with no captured
  JavaScript errors (.wireframe-objects-final-browser.log). This includes object
  coverage at four widths, reflected SVG titles, disclosed content, preserved
  geometry/backgrounds and distinct keyboard focus. Required structure, browser,
  button-state and whitespace checks are complete.
- Manual keyboard/screen-reader, zoom and Firefox/Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of all-object wireframe outlines and learner trial.

## Wireframe uses configured component backgrounds (12 November 2026)

- User requested that every Wireframe component background, including buttons,
  match the selected Basic/Advanced website configuration.
- Replaced the neutral paint layer with an outline-only layer. Body/region,
  card, input, component and button backgrounds, background images, text, border
  colours and opacity now come directly from the existing exported website CSS.
  Container outlines retain solid/dashed/dotted/thin distinctions and use website
  text/control-border tokens. Motion and shadows remain suppressed for the view.
- Form controls are inert rather than forcibly disabled. Original disabled
  attributes remain as authored, so enabled buttons retain their real opacity
  and configured backgrounds. Inert controls cannot receive user focus/activation;
  iframe restrictions, removed embeds/scripts and local navigation rules remain.
  Preview and standalone download use the same original CSS and outline layer.
- Updated workspace guidance, README and architecture notes; refreshed both
  changed wireframe JavaScript asset query versions. Project schema and website
  token/content generators are unchanged; no separate background configuration
  or duplicate state was added.
- Focused preliminary browser run passed **76/76**, no JS errors
  (.wireframe-background-focused.log). New comparisons inspect backgrounds,
  background images, foregrounds, border colours and opacity across source body
  elements, both samples/themes, all button variants and downloaded HTML. Before
  the full run, adjusted custom opacity fixtures to the model's 0–100 units.
- python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. python scripts/button_states_review.py passed **7/7 reduced-motion and
  9/9 forced-colour**, no JS errors (.wireframe-background-button-states.log).
- Inspected Basic/light at 390px and Advanced/dark at 1280px, with custom Primary
  and Secondary button fills visible and container outlines intact. Temporary
  helpers/captures were removed; ignored logs remain.
- Final python scripts/browser_review.py passed **2,582/2,582**, with no captured
  JavaScript errors (.wireframe-background-full-browser.log). This includes the
  corrected opacity fixtures and new background/appearance/download regressions.
  Required structure, browser, button-state and whitespace checks are complete.
  Earlier Palette/anchor results below are historical.
- Manual keyboard/screen-reader, zoom and Firefox/Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of the configured-colour wireframe and learner trial.

## Explicit Primary, Secondary and Accent selection (12 November 2026)

- User reported that Choose UI anchors appeared limited to Primary and requested
  Primary / Secondary / Accent. The model already contained all three, but the
  previous buttons called Secondary "Supporting" and exposed only one editor.
- Replaced those buttons with one labelled native three-option list on the left.
  Each selection exposes its own original brand selector/custom colour picker
  on the right and its own reset on the left. Selection keeps focus in the list
  for keyboard navigation. Configure source routes synchronize the selection.
- Used Secondary consistently in the anchor properties, reset and related static
  labels. Added selected-anchor guidance and explicit stage instructions. Existing
  state keys, shade generation, copied brand assignments and JSON schema remain.
  Refreshed the two changed JavaScript asset query versions in index.html.
- Checked official Material 3 colour-role guidance: it distinguishes primary,
  secondary and tertiary (contrasting accents). Retained this app's Accent name;
  no claim that Primary/Secondary/Accent is a universal naming standard.
  Source: https://m3.material.io/styles/color/the-color-system/
- Focused browser run passed **182/182**, no captured JS errors
  (.ui-anchor-focused.log). Added coverage for all three anchors in both themes:
  visible selection labels, selected fields/focus, independent brand assignments,
  custom values reaching project JSON/generated ramps, import and scoped reset.
- python scripts/check_structure.py passed (**66 assets**); git diff --check
  passed. The first button-state run passed **9/9 forced-colour**, but its reduced
  motion run failed to load studio-registry.js, causing startup errors
  (.ui-anchor-button-states.log). Clean repeat passed **7/7 reduced-motion and
  9/9 forced-colour**, with no JS errors (.ui-anchor-final-button-states.log).
- Updated README and architecture notes. Inspected Secondary properties at
  desktop/light and Accent at 320px/dark after explicitly opening the workspace
  and settling initial disclosure events. Temporary helpers/captures removed.
  Final python scripts/browser_review.py passed **2,554/2,554**, with no captured
  JavaScript errors (.ui-anchor-full-browser.log). Required structure, browser,
  button-state and whitespace checks are complete. Earlier results below are
  historical.
- Manual keyboard/screen-reader, zoom and cross-browser checks remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of the explicit three-anchor selector and learner trial.

## Palette browse/manage and selected properties (12 November 2026)

- User requested Architecture-style Palette UI: left browsing/CRUD and right
  editable selected properties. Added palette-browser.js/css immediately after
  palette-workspace, with versioned assets; seven responsive two-column stages.
- Brand search, list, count, Add and guarded Remove are on the left. Existing
  validated name/token/colour inputs remain in the right selected editor. Fixed
  anchors, shade families, semantic roles, regions and component variants use
  left selection and appropriate reset actions rather than arbitrary deletion.
- Right panels show the selected original fields; generated shade/component
  values are labelled read-only inputs. Button colour overrides are visible in
  the selected variant's properties. Feedback selection/reset is on the left,
  with feedback colour properties on the right. Guidance stays with browsing.
- Semantic role/token names are read-only; HEX/picker proposals are local drafts.
  Preview delegates to the existing contrast dialog, Apply persists, Cancel keeps
  saved colours and Discard restores the current value. Invalid HEX blocks Preview.
  Original shared state, JSON schema, autosave and export paths are preserved.
- Native opening refreshes read-only values after original toggle listeners;
  explicit source routing selects the appropriate properties. No global lesson
  navigation is added to background updates. Responsive columns also follow the
  available centre width through a container query.
- Focused browser checks: **161/161 passed**, no captured JavaScript errors
  (.palette-browser-verified.log). Existing semantic/palette/state/token subset:
  **273/273 passed**, no JS errors (.palette-browser-legacy.log). Preliminary runs
  caught outdated guidance selectors and native-toggle fixtures that did not let
  the prior disclosure settle; updated the fixtures while retaining assertions.
  One earlier isolated run also reported a null contrast-dialog session during
  a rapid cancel/reopen sequence; subsequent focused runs did not reproduce it.
- Current python scripts/check_structure.py passed (**66 assets**); git diff
  --check passed. python scripts/button_states_review.py passed **7/7 reduced
  motion and 9/9 forced colours**, no JS errors (.palette-columns-button-states.log).
- Inspected desktop brand, semantic, component, shade and background captures,
  plus narrow brand/semantic layouts in light/dark Studio. A phone capture with
  a transient local stylesheet-load failure was recaptured successfully. Added
  visible shade-token labels and coverage after visual review. Updated README,
  architecture notes and unobserved learner-trial prompts. Temporary screenshots
  and helper scripts were removed; ignored logs remain. Interrupted the first
  full run to include the label improvement.
- Final python scripts/browser_review.py passed **2,533/2,533**, with no captured
  JavaScript errors (.palette-columns-final-browser.log). This final run includes
  visible shade labels, the new browse/properties regressions and the full Studio
  checks. The earlier isolated dialog-session error did not recur. Required
  structure, browser, button-state and whitespace checks are complete.
- Manual keyboard/screen-reader, zoom and Firefox/Safari checks remain unverified;
  automated checks do not establish full accessibility. No commit/push/deployment.
- Next: user review of the Palette layout and an observed learner trial.

## Complete colour-token flow and deeper wireframes (12 November 2026)

- User requested semantic colours inside Palette and a complete brand-to-component
  colour process, plus more wireframe container boundaries.
- Extended Palette to seven stages: Brand, shared UI anchors, Shades, Semantic
  roles, Page backgrounds, Component colours, States/review. Moved the existing
  guided semantic editor with its contrast-preview/Apply/cancel/reset behavior.
  Separate course step 6 is now Colour lab for model exploration, with a Palette
  shortcut. All 12 course routes remain stable.
- Component family readouts show actual exported values for cards/panels, inputs,
  links and five button variants. Dark values inherit base tokens when no dark
  declaration exists; a focused check caught/fixed shared button focus showing
  unavailable. Context notes describe where each family uses its roles.
- Moved actual button colour/source/custom/focus fields into Palette and retained
  geometry, typography, timing and interaction previews in Buttons. Variant proxy
  delegates to the original control. Scoped clear API deletes only that variant's
  colour overrides; source/custom values, other variants, geometry and shared focus
  remain. Focus resets separately. Existing JSON schema/generators are unchanged.
- Metadata Configure links reach Palette for semantic/component colours and keep
  non-colour button settings in Buttons. Component refresh is lazy while hidden.
  Final copy distinguishes anchors from semantic roles; a source-label regression
  fixes catalogue step numbers using visible position rather than internal index.
- Wireframe now outlines nested sections, list/description items, disclosures and
  normal-flow wrappers containing block content. Preserve region/content/layout
  priority and omit decorative/aria-hidden SVG. Existing titles are retained;
  otherwise hover titles identify HTML tag/ID/classes and authored layout type.
  Source HTML, box geometry, responsive CSS and saved content remain unchanged.
- Final focused colour/wireframe run: **151/151 passed**, no JS errors
  (.colour-flow-final-check.log). Existing semantic/palette/state/token subset
  passed **273/273**, no JS errors (.colour-legacy-check.log). Expanded geometry
  checks compare all marked containers to live HTML at 320/390/768/1280px in
  Basic and Advanced. Final button-state suite passed **7/7 reduced-motion and
  9/9 forced-colour**, no JS errors (.colour-flow-final-buttons.log).
- First full run: **2,457/2,467**, no JS errors (.colour-flow-full-browser.log).
  Eight failures exposed a new visibility helper switching the global lesson
  during background colour updates, disrupting review/prototype/example focus.
  Removed that navigation side effect; explicit Reveal/Configure still navigates.
  Readouts now refresh when the actual Palette/component disclosures are open,
  including manual opening, rather than depending on the global builder step.
  Two remaining failures expected the old semantic/button-colour source steps;
  updated those to Palette. Added seven context/focus/routing regressions.
- Inspected six semantic/component/wireframe screenshots in desktop/phone and
  light/dark Studio. Updated component captures confirm variant selection precedes
  outputs. Temporary screenshot/helper files removed; ignored logs retained.
  Structure check passed (64 assets); diff --check passed.
- Final python scripts/browser_review.py: **2,475/2,475 passed**, no captured
  JavaScript errors (.colour-flow-complete-browser.log), after the context fix,
  catalogue display/source updates and new preservation regressions. Required
  checks are complete; earlier entries above distinguish preliminary failures.
- Manual keyboard/screen reader, zoom and Firefox/Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of the complete colour-token flow and deeper wireframe
  boundaries; learner trial remains unobserved.

## Guided centre Palette workspace (11 November 2026)

- User requested the Architecture approach for Palette: a simpler left wizard,
  step-by-step centre editing, CRUD and appropriate student explanations.
- Added palette-workspace.js/css after background/state services. Five stages:
  Brand colours, Assign UI roles, Generate shades, Page backgrounds, States/review.
  Native disclosures, Previous/Next controls and a short left navigator guide the
  process. On mobile the navigator collapses and uses the existing stage-controls
  placement anchor. Current-stage markers do not claim learning completion.
- Reused existing editor nodes/listeners. Brand CRUD selects one visible row;
  properties are visible without a nested disclosure. Add/count act on the
  collection. Names/IDs remain separate and bounded to 1-24 references. Required
  UI roles support copy/custom assignment and individual reset. Generated shades
  are read-only outputs; source/method controls teach how to regenerate them.
- Background editing selects one region with existing default/reset, opacity and
  padding behavior. Website theme selector delegates to jTheme. Direct feedback
  pickers create/update/remove only Success/Warning/Danger overrides for the
  selected theme. Existing control/button state editors and token references are
  optional disclosures. Palette data still uses existing JSON/local save fields.
- Source routing reveals the stage, row or background fieldset before focus.
  Add/rename retains the selected properties. State identity changes restart the
  workflow for direct importConfig, local project loading and Reset. No imported
  labels are inserted as HTML; original validators and generators remain shared.
- Added workflow regressions for all stages, brand CRUD, scoped resets, theme
  overrides, imports, source links and control fit in light/dark Studio at
  320/390/1440px. Updated older fixtures to reveal centre stages before focus;
  background containment checks now expect the centre workspace.
- Current focused workflow **51/51 passed**, no JavaScript errors
  (.palette-final-workflow.log), including live/Accessibility destination focus. Existing palette/token/state/background subset
  **334/334 passed** (.palette-check.log) before the final role-card layout and
  collection-action fix. Screenshot review caught detached Add/count lookups
  rendering nullnull; fixed with scoped node references and a placement regression.
  Also compacted desktop role editing into responsive cards. Reset/import initially
  relied only on file events; state-identity synchronization fixes direct imports.
- Initial full suites: 2,410/2,418 and 2,411/2,419. All eight failures were stale
  assertions expecting Palette controls inside the wizard or all background regions
  visible together. Updated source-location/lesson containment assertions and
  reveal the chosen region before testing opacity/padding geometry. Focused rerun
  **8/8 passed**, no JS errors (.palette-layout-check.log).
- Final button-state suite: **7/7 reduced-motion and 9/9 forced-colour passed**
  (.palette-final-buttons.log). Inspected six final screenshots across brand, UI
  roles, background and review stages at desktop/320px in light/dark Studio.
- Final code review added native destination focus when opening Accessibility from
  Palette review; the 51-check workflow rerun verifies both review destinations.
  python scripts/check_structure.py passed (64 assets); git diff --check passed.
- Final python scripts/browser_review.py: **2,421/2,421 passed**, no captured
  JavaScript errors (.palette-final-complete-browser.log). The preceding run after
  fixture updates passed 2,419/2,419 before the final destination-focus regression.
  Current full results include that fix and both new review-destination checks.
- Temporary screenshot/helper files removed; ignored logs retained. Documentation
  now describes the centre process, shared anchors, scoped overrides, immutable
  generated outputs and learner trial tasks. All required checks are complete.
- Manual keyboard, screen reader, zoom and Firefox/Safari remain unverified;
  automated checks do not establish full accessibility. No commit/push/deployment.
- Next: user review of the five-stage Palette workspace; run the unobserved learner
  trial before claiming the guidance has been validated with students.

## Significant wireframe containers (11 November 2026)

- User requested that Website wireframe reveal significant containers and their
  layout. Existing neutral styling outlined semantic elements but omitted several
  Grid/Flex wrappers and unlabelled child columns.
- Added mirror-only container annotations. Page regions use solid outlines,
  content-width wrappers dashed outlines, Grid/Flex groups dotted outlines and
  child containers thin outlines. Layout groups have a subtle neutral fill.
  A short Studio legend explains the boundaries without adding editing controls.
- Derive layout wrappers from the generated CSS using native CSSStyleSheet parsing,
  including nested responsive rules; restrict marking to structural HTML elements,
  excluding decorative/hidden SVG content. No imported content becomes a selector.
  Outline priority retains regions/content wrappers over nested layout annotations.
- Preview and standalone HTML share the same annotated document and paint layer.
  Source website HTML, saved Architecture and responsive layout remain unchanged.
  Updated affected JS asset versions, README and architecture documentation.
- Current checks: focused Chrome regressions **46/46 passed**, no captured JavaScript
  errors (.containers-focused.log). Added boundary coverage and computed outline
  style checks for both samples; all marked wrappers/children, including those
  without IDs, match live geometry at 320/390/768/1280px. Existing copy, download,
  save compatibility, read-only and control-fit checks also pass.
- python scripts/check_structure.py passed (62 assets); git diff --check passed
  with the existing website-content.js line-ending advisory. Inspected five isolated
  Chrome captures: both samples at 320px Studio width, both on desktop, and Basic
  Flexbox/cards further down the page. Nested outlines remain visible as columns
  stack, and scrolling stays inside the preview. Temporary capture/helper files
  removed; ignored logs retained.
- python scripts/browser_review.py passed **2,370/2,370**, no captured JavaScript
  errors (.containers-full-browser.log). These are the current full-suite results;
  prior entries below describe earlier runs.
- Manual keyboard/screen-reader, zoom and Firefox/Safari remain unverified; these
  automated checks do not establish full accessibility. No commit/push/deployment.
- Next: user review of the container boundaries in Website wireframe.

## Read-only website wireframe correction (11 November 2026)

- User clarified Wireframe is a read-only low-fidelity version of Responsive Live,
  for both Basic and Advanced. This supersedes the authoring workspace described
  in the historical implementation entry below.
- Replaced the typed-block renderer with the existing generated website HTML and
  responsive CSS plus a neutral paint layer. It preserves actual layout, font
  metrics, spacing, breakpoints and wording. Saved website content from Architecture
  flows through the same generators; proposals and planned-only content do not
  become invented website layouts. The public Wireframing lesson contains a brief
  explanatory note, preventing recursive embedded previews.
- Removed layout, block priority, scope, proposal and review-note authoring controls
  from Wireframe. Kept transient Basic/Advanced and viewport choices, compare-live
  and HTML download. Fixed widths scroll inside the preview; Match live follows
  the existing live viewport. The active sample has a checkmark/pressed indicator.
- Mirror iframe omits scripts/nested embeds, disables forms and strips external
  navigation. Local fragment navigation and native disclosures remain inspectable.
  Updates preserve same-mode disclosure/scroll state; inactive Wireframe refreshes
  on return. Standalone download embeds the same source CSS and neutral paint.
- Retained bounded legacy layout data for project round-trip compatibility; it has
  no effect on the read-only mirror. Updated README, architecture notes, learner
  trial prompts, lesson guidance and affected asset versions.
- Replaced authoring regression fixtures with mirror checks: both source structures,
  complete wording, all visible ID-bearing element geometry at 320/390/768/1280px,
  saved wording safety/synchronization, legacy settings, downloads, form isolation,
  local fragments, disclosures, live-width selection and control fit at 320/390/1440px.
- Current verification: python scripts/browser_review.py **2,364/2,364 passed**,
  no captured JavaScript errors (.readonly-full-browser.log). The full run began
  before the final selected-sample styling/wizard wording. The final focused mirror
  run **42/42 passed** (.readonly-final-check.log) after those changes and a more
  robust outer-hash navigation assertion. An earlier checkmark assertion had been
  converted to a question mark by shell encoding; an encoding-independent fixture
  fixed that check. No runtime change was required for it.
- python scripts/button_states_review.py passed **7/7 reduced-motion and 9/9
  forced-colour** after the final selected-state styling (.readonly-final-buttons.log).
  python scripts/check_structure.py passed (62 assets); git diff --check passed
  with only the existing website-content.js line-ending advisory. Four isolated
  visual captures reviewed Basic/light and Advanced/dark at 320px and desktop Studio
  widths, first with fixed 390px views and again with 320px/available-width views.
  Temporary screenshot/helper files removed; ignored logs retained.
- Manual keyboard/screen-reader, zoom, Firefox and Safari remain unverified;
  automated passes do not establish full accessibility. No commit/push/deployment.
- Next: user review of the read-only Wireframe view against Responsive Live; keep
  content/layout authoring in Architecture and the existing design tools.

## Architecture-driven wireframe engine implementation (11 November 2026)

- Implemented the agreed first engine/workspace. wireframe-engine.js projects
  Architecture IDs, hierarchy, types, actual wording/proposals, references and
  readiness into neutral containers, text, image areas, actions and inert form
  controls. Whole website is a virtual scope; explicit pages and existing sections
  are selectable, with shared Header/Footer. No section becomes an invented page.
- Generated planning content and duplicate authored nav subtrees are excluded;
  authored CTA references remain content. The same pure sitemap collector supplies
  source label/parent metadata. Navigation respects current source, ancestor
  inclusion and custom labels/planned destinations. Main navigation is visible;
  nested destinations use a native disclosure. Sitemap exclusion retains content.
- Added transient source metadata/reconciliation and read-only source snapshots.
  Wireframing itself is one generated inventory entry. Architecture, Sitemap and
  text-inspection flags plus a projection guard suppress recursive generation.
  Source signatures exclude wireframe-only settings. Current source counts are
  Basic 139 / Advanced 395; Advanced's previous generated sketch descendants are
  collapsed to one source entry, preventing the engine from containing itself.
- Normalized per-mode designProcess.wireframes stores scope, current/proposed
  content view, inherited/stack/split/grid canvas arrangement and ID-keyed block
  layout/priority. Max 1,000 overrides / 80,000 serialized characters per mode;
  imported values are enum/map data, never CSS/selectors/code. Missing scope falls
  back visibly and orphan overrides are retained/reported, never reassigned.
  Existing project layout and notes remain the fallback. Project file cap raised
  to 6 MB for bounded content, text and layout backups; oversize fixture updated.
- wireframe-workspace.js registers after studio-learning. It moves the existing
  fallback layout and review notes without cloning controls. The short wizard
  opens the centre workspace. Canvas selection shows source/type/readiness and
  container layout/priority. Edit in Architecture selects the same guarded ID,
  revealing unsaved source work instead of overwriting it. Changes save through
  apply, with mode/block reset and one-change Undo. External planning edits clear
  incompatible Undo history, including Brief/review notes. Source wording/status/
  rename changes retain layouts. No source content is rewritten by layout edits.
- Added Phone 320px, Wide 960px and available-width previews. Fixed previews scroll
  inside the labelled canvas rather than shrinking the virtual viewport. Container
  queries stack groups at the shared responsive cutoff. Current/proposal views
  respect intentionally blank drafts. Shared escaped markup/CSS supplies studio,
  Advanced sample planning artifact and offline standalone wireframe.html with no
  scripts, remote assets or live form controls. Added the actual download action.
- Added 84 focused regressions for source projection, real copy, stable IDs,
  nav sources, scope/planned pages, placeholders, source edit/dirty guard, blank
  proposals, malicious wording, group responsiveness, imports/local save/download,
  missing IDs, mode isolation, reset/Undo and control fit at 320/390/1440px.
  Latest focused run: **84/84 passed**, no captured JavaScript errors. Preliminary failures
  were an overly broad generated-target assertion (authored CTA references should
  remain), comparisons against unrelated existing import-added root fields, and
  Basic's unselected custom Home default; fixtures were corrected. Added Undo
  invalidation for external review-note edits during this work.
- Confirmed and fixed a legacy identity bug: reordering a raw sitemap could reuse
  a positional content-legacy ID for a different target. The first legacy wireframe
  change now stores the unchanged normalized typed Architecture before binding
  layouts; later sitemap edits cannot transfer the override. The isolated
  regression changed from before=home/after=features to home/home; complete source
  snapshot equality passes. Added unsaved-source guards for authoring and Undo.
- A focused contrast check found the dark Studio focus colour had 1.67:1 contrast
  on neutral white canvas. Included native navigation summaries in the neutral
  focus rule; actual computed contrast is now **15.91:1** in light and dark (2/2
  checks, .wireframe-focus.log), with committed regression coverage.
- First full python scripts/browser_review.py: **2401/2401 passed**, no JavaScript
  errors (.wireframe-full-browser.log), before the legacy/focus refinements. The
  next run stopped at 2001/2002 on the existing synthetic file-import fixture's
  virtual timeout (.wireframe-final-browser.log). Replaced artificial import
  timers with actual dss:imported/alert observation and bounded local network
  ticks that pause Chrome virtual time while real File.text I/O completes. This
  is test-server-only synchronization; application file loading is unchanged.
  Focused content/file checks: **58/58 passed**, no captured errors
  (.wireframe-io.log). Complete required python scripts/browser_review.py:
  **2406/2406 passed**, no captured JavaScript errors
  (.wireframe-complete-browser.log), including the final engine/data/interaction
  code, legacy migration, source guards and real-file synchronization. Runtime
  files stayed unchanged during that run; preliminary results are distinct.
- A final styling-only correction after the full pass isolated --text/--text-muted
  inside the neutral canvas: the dark project's caption colour previously had
  1.70:1 contrast on white. Actual exported light/dark captions now both measure
  **15.91:1** (2/2, .wireframe-paper.log). All **84/84** wireframe cases passed
  after this colour-only refinement (.wireframe-final-check.log), including the
  two new real-preview theme contrast assertions. Preview theme changes update
  DOM in place; corrected an initial test that incorrectly awaited iframe load.
  The full suite was not repeated after this isolated colour-variable change;
  no engine, data or interaction code changed after its full passing run.
- Current python scripts/check_structure.py: **62 assets verified**. git diff
  --check passes with a website-content.js LF/CRLF notice.
  python scripts/button_states_review.py: reduced motion **7/7**, forced colours
  **9/9**, no captured errors; repeated after the focus refinement with the same
  results (.wireframe-final-buttons.log).
- Initial visual helper: **8/8** assertions passed for Basic/light and Advanced/
  dark at desktop and actual 320px iframes. Initial phone captures showed the
  wrong scroll position; repeated with the lesson explicitly active, focused
  element blurred and anchoring disabled, then inspected both phone views and
  desktop views. Phone was subsequently made an actual fixed 320px canvas rather
  than clamped-to-editor width. Final visual helper checks passed **8/8** with no
  captured errors (.wireframe-final-visual.log); capture scroll is held on the
  requested workspace after the iframe/media-query layout settles. Inspected all
  four final images: actual grid/stack blocks, source/readiness properties, width
  controls and contained canvas scrolling are visible. Removed temporary helper
  scripts and screenshots after inspection. README/architecture/learner prompts
  and changed asset URLs updated.
- Final python scripts/check_structure.py: **62 assets verified**; git diff
  --check passes (website-content.js LF/CRLF notice). Temporary focused/debug/visual
  helpers and images removed; ignored result logs retained. Next: learner review
  of source-linked layout authoring and canvas navigation. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review remain outstanding; tests do not
  establish full accessibility.
  Prior work and the unrelated test.html deletion preserved. No commit/deployment.

## Architecture-driven wireframe engine assessment (11 November 2026)

- User proposed the next Wireframe phase: build the wireframe from related Content
  Architecture data. Reviewed the current artifact generator, legacy hierarchy
  projection, wireframe controls and planning architecture notes. The current
  wireframe is a fixed header/navigation/main/aside/footer sketch: it reads legacy
  pages labels plus Brief goal/scope and has only split/stack and notes settings.
  It does not render the saved typed contentPlan or website text bindings.
- Recommended a derived, deterministic wireframe model keyed by stable content
  IDs, with separate per-sample presentation overrides. Architecture owns content,
  hierarchy, references and readiness; wireframes own grouping presentation,
  emphasis and responsive arrangement. Default wording uses current website text;
  saved proposals can be an explicit alternate view, preserving blank drafts.
- Map regions/pages/sections/groups to containers, text to semantic text blocks,
  images to neutral frames with their alternatives, links to action/navigation
  blocks and fields to labelled form blocks. Planned/missing content remains a
  visible placeholder with readiness, rather than silently disappearing. Sitemap
  inclusion affects navigation only; repeated destination references do not
  duplicate destination content. Current one-page samples need a virtual page
  shell, not an invented separate page for every section.
- Source projection must exclude generated planning artifacts, including the
  wireframe itself, and avoid calling recursive sample generators while rendering
  those artifacts. Preserve the existing preview/export source-collection guards.
  Content refresh should retain layout overrides for matching IDs, explicitly
  report deleted/unavailable references and never attach them to another item.
- Suggested first delivery: selected page/section, neutral responsive canvas,
  linked block selection/properties, limited stack/split/grid choices, source
  readiness and persistence/Undo/reset. Use the shared renderer for studio,
  preview and standalone artifacts; retain older projects and existing layout/
  wireframeNotes defaults. Follow with layout authoring refinements after the
  source-to-block mapping is verified on Basic and Advanced.
- Assessment only: no wireframe runtime changes implemented or tested. Commands:
  bounded Get-Content/rg inspection and git diff --check. Earlier implementation
  suite results below remain historical; no new browser/visual validation claim.
- Next: implement the typed source projection and shared neutral renderer, then
  connect the workspace and validated persisted layout overrides. Preserve prior
  working-tree edits and the unrelated test.html deletion. No commit/deployment.

## Architecture as a working content tool (11 November 2026)

- Renamed the saved-plan disclosure to Review the Content Plan, reflecting that
  its Save actions now live under the left content browser. Moved the Content
  structure title/introduction inside that browser's header, so the properties
  form starts at the same grid row without an introduction above both columns.
- Moved Content readiness out of the planning disclosure and into the always-
  visible properties, before Website content. It retains the existing validated
  status for every item/type, native form owner and save/import/Undo path. New
  planned items still start as planned; authored sample entries remain present.
- Removed See an example and replaced generic planning help with working prompts.
  When there is no saved proposal, proposed wording starts from the selected
  item's current text/label/alternative bindings. The proposal checkbox remains
  off until explicitly included or edited: passive property saves do not create
  a proposal. Saved proposals, including deliberate empty strings, take priority.
- Fresh sample inventories seed notes with the actual project, item path/purpose,
  prototype-specific next action and Owner: Unassigned. Existing saved notes,
  including explicit blanks, stay intact; blank notes get contextual placeholders.
  Used cached ancestor labels while inventorying so these defaults do not add
  repeated whole-outline path searches. No new schema, owner assumptions or HTML
  interpretation. Updated current README/architecture/learner wording and asset
  versions; historical progress entries retain their original names/results.
- Added 32 regressions for site-derived wording, absence of passive draft writes,
  contextual notes, explicit empty import preservation, readiness across all
  content kinds and column/header alignment at 320, 390 and 1440px. Preliminary
  Architecture subset: 354/357 passed with no JavaScript errors; three previous
  assertions expected blank defaults or the old prompt wording and were updated.
  Required final python scripts/browser_review.py: **2324/2324 passed**, no
  captured JavaScript errors (.architecture-tool-final-browser.log). Runtime files
  stayed unchanged during this final run; preliminary results above remain
  distinct from the final passing verification.
- python .architecture-tool-visual.py captured Basic/light and Advanced/dark at
  desktop 1440px and actual 320px iframe widths: 8/8 checks passed, no captured
  errors. Inspected all four: current demo wording and site notes are populated,
  example panel absent, readiness visible and right properties align with the
  left header. Removed temporary helpers/captures after inspection. Current
  python scripts/check_structure.py verifies 59 assets; git diff --check passes.
- Final python scripts/check_structure.py: **59 assets verified**; git diff
  --check passes. Next: observe the site-based planning and visible readiness with
  learners. Manual keyboard-only, screen-reader, zoom and Firefox/Safari review
  remain outstanding. Previous results below are historical. A test.html deletion
  appeared in working-tree status during verification; this task did not modify
  it. No commit, push or deployment; prior working-tree work preserved.

## Architecture planning and Save placement (11 November 2026)

- User requested Develop the content plan at the top of Architecture workspace,
  before the content architecture/editor, and Save and review beneath Content
  structure's left column. Moved the existing planning disclosure directly after
  the workspace header and before Content structure. Added the selected item's
  path so its proposals and notes retain clear context at their new location.
- Moved the existing Save/Discard/Restore/status/sitemap-shortcut area below the
  left browser's branch tools. Review and Save Content Plan retains the guidance
  and saved-plan artifact. No duplicate controls or new project data. Desktop
  keeps the property editor on the right; phone layouts keep the actions with
  their content browser before the stacked property editor.
- Explicitly associated each relocated planning control with ia-form and attached
  dirty/invalid handling to both editing surfaces. Native validation and the same
  save/discard/Undo transaction remain authoritative. Extended local control
  styling to the top planning disclosure and refreshed the affected CSS/JS query
  versions. Updated README and architecture notes for the new placements.
- Updated regression expectations for the new review/left-action hierarchy and
  added form-owner/selected-context checks. Responsive assertions cover the
  expanded top planning fields and left save area at 320, 390 and 1440px.
- Current-session checks: python scripts/check_structure.py verifies 59 assets;
  git diff --check passes. python .workspace-placement.py (Architecture subset)
  passed 325/325 with no captured JavaScript errors. python .workspace-visual.py
  captured Basic/light and Advanced/dark at 1440px and actual 320px iframe widths:
  8/8 placement/width/error checks passed. Inspected the planning controls, selected
  path and left action area in all four captures. The first capture attempt did
  not reveal containing native disclosures consistently; repeated with them
  explicitly open before scrolling. Removed temporary helpers/screenshots after
  review. Required python scripts/browser_review.py: **2292/2292 passed**, no
  captured JavaScript errors (.workspace-final-browser.log). Runtime files stayed
  unchanged during this final run, including the expanded-field responsive checks.
  Final python scripts/check_structure.py: **59 assets verified**; git diff --check
  passes. Previous results below are historical.
- Next: observe the revised planning/left-action layout with learners.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain
  outstanding. No commit, push or deployment; prior working-tree work preserved.

## Writable website content implementation (11 November 2026)

- Implemented the agreed Architecture Website content editor for both samples.
  Students can save authored headings/paragraphs, links/buttons, image alternatives,
  captions, list/table text and form labels/help/placeholders/initial text/options.
  Proposals and ownership/next-action notes remain separate. Containers point to
  their children; generated planning artifacts and setting-owned identity explain
  their existing source. Default sample inventories now contain Basic 139 and
  Advanced 409 entries, including field labels and bare container text.
- Added dependency-free website-content.js before core state. Per-mode overrides
  are normalized into sourceKey/allowlisted field/fingerprint/value records, capped
  at 2,000 fields, 2,400 characters each and 120,000 serialized characters per mode.
  Local authored DOM bindings set text nodes/fixed safe attributes only. Inline
  markup, stable anchors and submitted option values survive wording changes.
  Missing/changed sources are reported and retained without applying elsewhere.
- Wrapped both sample factories so preview, inspector, website downloads, actual
  content inventory and page-label sitemap use the same edits. Added raw factories
  for default bindings and preserved source-collection recursion guards. Project
  identity spans continue to follow Brief while surrounding text remains writable.
- Existing form commits text and plan together. Discard restores saved fields;
  Undo restores both. Item restoration is pending until Save and is shown only for
  saved custom text. Sample restoration clears only that mode's text and plan,
  retaining the other sample and sitemap choices. Refreshed affected asset URLs;
  updated README, architecture notes and unobserved learner-trial prompts.
- Added functional browser regressions for both samples: inert HTML-like wording,
  preview/inspector/download parity, live sitemap labels, JSON/file/local saves,
  empty values, label/placeholder/textarea/option editing, inline identity,
  length-limit atomicity, unavailable/changed bindings and scoped restore/Undo.
- Focused writable-content checks passed 58/58; the complete Architecture subset
  passed 323/323, both without captured JavaScript errors. Structure verifies 59
  assets; git diff --check passes with the pre-existing CSS LF/CRLF notice.
  An initial full run returned 2274/2288 with no JavaScript errors: 14 previous
  assertions required the old first legend or visibility of every button. Updated
  them for Website content and a conditional restore button; layout checks now
  explicitly select an editable heading. A later full run stopped at 2001/2002
  on a synthetic JSON-file import timeout, despite the isolated flow passing.
  Increased file waits to 12s, total virtual budget to 185s and wall timeout to
  540s. Final required `python scripts/browser_review.py`: **2290/2290 passed**,
  no captured JavaScript errors (`.writable-final-browser.log`). Runtime files
  remained unchanged during this final run. `python scripts/check_structure.py`:
  **59 assets verified**; `git diff --check` passes (existing CSS line-ending notice).
  Preliminary failures above are distinct from this final passing verification.
- A visual pass found and fixed an incorrect source-unavailable help message;
  regression coverage now checks that valid text fields have no such message.
  Isolated attempts also failed loading unchanged learning-path.js and
  studio-registry.js. Increased the local test server's pending-connection queue
  to 128 for bursts of deferred asset requests; the subsequent Architecture run
  was clean. Final `python .writable-visual.py` sequentially captured Basic/light
  and Advanced/dark at 1440px and actual 320px iframe widths: **8/8 checks passed**,
  no captured errors (`.writable-final-visual.log`). Inspected all four screenshots:
  labelled editable text fits, default restore controls stay hidden, the incorrect
  source warning is absent and fields retain visible borders/focus. Removed the
  temporary focused/Architecture/visual helpers and screenshots after review.
  No full accessibility claim: manual keyboard-only, screen-reader, zoom and
  Firefox/Safari checks remain outstanding. Earlier results below are historical.
- Next: observe direct website editing versus planning proposals with learners
  and complete manual accessibility/cross-browser review. No commit, push or
  deployment. Prior working-tree changes are preserved.

## Writable website content assessment (11 November 2026)

- User asked whether students should be able to edit the actual text of all
  Content structure entries. Reviewed the inventory/normalizer, source-key
  reconciliation and Basic/Advanced generator/export registration. Actual values
  currently refresh from authored sample HTML; saved drafts/notes remain separate
  plans. Removing readonly from the form alone cannot apply reliable page edits.
- Recommended direct editing of authored text with type-specific fields: headings,
  paragraphs, link/button labels, captions, image alternatives, list/table text,
  form labels/help/placeholders and option labels. Containers should expose their
  structure/labels rather than flattening nested HTML into one text replacement.
  Generated sitemap/planning artifacts stay derived, with page-label sitemap text
  following edited eyebrows/headings while stable anchors remain unchanged.
- Proposed clear displayed-content versus planning-note fields, one shared
  validated content application path for preview/inspector/export, per-sample
  project persistence, Undo and item/sample restoration. Existing setting-owned
  values should use their existing source rather than introduce conflicting
  editors. Missing bindings must be reported instead of applying to another item.
- This is an assessment, not implemented writable content. Existing proposals
  still do not replace sample content. Commands run: bounded Get-Content/rg source
  inspection and git diff --check. No structure/browser/manual review run for
  this analysis; passing implementation results below remain historical.
- Next: implement the agreed direct-editing scope with stable content bindings,
  import validation and preview/export/persistence regression coverage. No runtime
  edits, commit, push or deployment in this assessment.

## Save and review at the bottom of the review section (11 November 2026)

- User clarified that Save and review belongs at the bottom of Review and Save
  Content Plan, after all guidance and saved-plan content. Reordered the existing
  static children so the save/action area is last, following the complete saved
  artifact. Kept the guidance host, action nodes/handlers, form association,
  disclosure/focus behavior and public exports unchanged.
- Refreshed the studio-learning.js asset version and updated README/architecture
  wording. Updated the existing review-placement assertion to require the save
  area as the review disclosure's last element, immediately after the saved
  artifact, with guidance preceding that artifact after model renders/imports.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes (existing CSS LF/CRLF notice). Required
  `python scripts/browser_review.py`: **2232/2232 passed**, no captured JavaScript
  errors (`.review-save-bottom-browser.log`). Runtime files were held unchanged
  during the run; last-element placement is verified after model updates.
- `python .review-save-bottom-visual.py` captured actual light Basic desktop and
  dark Advanced 320px layouts after repeated renders. Inspected both: the action
  panel is below all saved content, at the bottom border of the review disclosure,
  with Advanced tools outside and after it. Removed temporary helper/captures.
  Manual keyboard-only, screen-reader,
  zoom and Firefox/Safari review remain outstanding; automated checks do not
  establish full accessibility. Previous passing results below are historical.
- Next: observe the review-first/save-last flow with learners and complete manual
  accessibility/cross-browser review.
  No commit, push or deployment; previous working-tree changes are preserved.

## Guidance before Save and review (11 November 2026)

- User requested Save and review directly after Information architecture and
  sitemap: different jobs within Review and Save Content Plan. Moved the existing
  IA/sitemap guidance into a stable host before the existing save area, followed
  by the remaining saved-plan artifact. The original guidance renderer populates
  this host; later model renders remove its copy from the remaining artifact so
  the introduction stays singular and the action nodes/listeners are preserved.
- No changes to saved data, form ownership, disclosure/focus behavior, restoration
  or public exports. Refreshed both changed JS asset versions and updated README
  and architecture notes. Extended the existing responsive review-placement
  assertion to require the guidance host immediately before the controls, the
  expected heading and exactly one guidance copy after save/import/render flows.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes (existing CSS LF/CRLF notice). Required
  `python scripts/browser_review.py`: **2232/2232 passed**, no captured JavaScript
  errors (`.review-save-order-browser.log`). Runtime files were held unchanged
  during the run; ordering and singular guidance are verified after model updates.
- `python .review-save-order-visual.py` captured actual light Basic desktop and
  dark Advanced 320px layouts after two ordinary renders. Inspected both:
  explanation, Save/review and remaining content appear in that order, and
  controls still fit the phone pane. Removed temporary helper and captures.
  Manual keyboard-only, screen-reader, zoom
  and Firefox/Safari review remain outstanding; automated checks do not establish
  full accessibility. Earlier passing results below are historical.
- Next: observe the guidance-first review flow with learners and complete
  manual accessibility/cross-browser review.
  No commit, push or deployment; previous working-tree changes are preserved.

## Review and Save Content Plan consolidation (11 November 2026)

- User requested moving Save and review into Review saved content plan and
  renaming that disclosure Review and Save Content Plan. Moved the existing
  action/status panel ahead of the saved artifact within the renamed disclosure.
  Save, Discard, Restore, scope help and the visitor-map shortcut retain their
  original nodes and handlers. The content grid now holds only Find and properties.
- The first unsaved edit opens the review section without moving field focus.
  Save/Discard and dirty guards reveal it before focusing Save. Non-empty content
  action messages also open it, so Undo/reorder/delete feedback cannot become
  hidden after the move. Manual collapse retains unsaved values. The external
  submit button keeps form="ia-form", native validation and existing persistence.
- Made save-area spacing, responsive button wrapping and touch-target styles
  independent of the content-editor ancestor. Refreshed all three changed asset
  versions. Updated README, architecture notes and the unrun learner trial.
  Replaced obsolete below-Find placement assertions with renamed-section
  containment/geometry coverage and added collapsed-review Undo feedback checks.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes (existing CSS LF/CRLF notice). Initial `python .review-save-focused.py`:
  **264/264 passed**, no errors (`.review-save-content-focused.log`). After adding
  non-empty action-message reveal behavior, focused rerun: **266/266 passed**,
  no captured errors (`.review-save-content-focused-final.log`). Initial full
  development run passed **2230/2230**, no captured JavaScript errors
  (`.review-save-content-browser.log`); it was superseded by the message-visibility
  refinement and its new Undo regression. Final full `python scripts/browser_review.py`:
  **2232/2232 passed**, no captured JavaScript errors
  (`.review-save-content-browser-final.log`). Completed runtime files were held
  unchanged throughout that final run.
- `python scripts/button_states_review.py` initially passed **4/5 reduced-motion**
  before a null return-link check, with a failed request for unchanged
  section-navigation.js; forced-colour checks passed **9/9**, no errors. A clean
  rerun passed **7/7 reduced-motion** and **9/9 forced-colour**, no captured
  errors (`.review-save-content-states-final.log`).
- `python .review-save-visual.py` captured actual light Basic desktop and dark
  Advanced 320px views of the renamed section. Inspected both: action controls
  and restore help fit above the saved-plan review. Removed temporary review
  helpers and screenshots. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review remain outstanding; automated
  checks do not establish accessibility. Earlier results below are historical.
- Next: observe learners using the consolidated review/save section and complete
  manual accessibility/cross-browser review.
  No commit, push or deployment; prior working-tree changes are preserved.

## Three-column Visitor sitemap layout (11 November 2026)

- User requested Find destination, Selected destination and Visitor sitemap
  preview horizontally. The active source's workspace now contains the single
  existing preview host. At 58rem of available Architecture width, all three
  form a row; at 46–58rem the preview spans below two editing columns; below that
  the three stack in DOM reading order. Both page-derived and custom modes use
  the same layout, including when the inspector reduces available pane width.
- Preserve the preview node when it is already in the correct source workspace;
  source changes move that node without duplication. Added studio-only tabindex
  to the labelled preview region and bounded its vertical scrolling. Aligned
  card headings and removed the custom form's extra top margin. No project data,
  sitemap logic, public artifact generator or export changes.
- Refreshed all three affected runtime asset versions and updated README and
  architecture notes. Extended the Sitemap matrix with responsive column-order,
  active-host placement and focusable-preview checks for both samples/sources.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes with the existing CSS LF/CRLF notice. Required full
  `python scripts/browser_review.py`: **2230/2230 passed**, no captured JavaScript
  errors (`.sitemap-three-column-browser.log`). Runtime files were held unchanged
  during this run; both sources and responsive column placement are covered.
  `python scripts/button_states_review.py`: **7/7 reduced-motion** and **9/9
  forced-colour** checks passed, no captured errors (`.sitemap-three-column-states.log`).
- `python .sitemap-columns-visual.py` captured actual light Basic/automatic and
  dark Advanced/custom desktop layouts, dark 320px stacked custom controls,
  1180px two-column-plus-preview layout and the dark 320px preview. Inspected all
  five, confirming the requested desktop row, readable narrow fallback and
  bounded scrolling. Removed temporary helper and screenshots. Manual
  keyboard-only, screen-reader, zoom and Firefox/Safari
  review remain outstanding; automated checks do not establish accessibility.
- Next: observe learners comparing the three Sitemap columns and complete
  manual accessibility/cross-browser review.
  No commit, push or deployment; previous passing results below are historical.

## Sitemap source selection at the top of Visitor sitemap (11 November 2026)

- User requested Sitemap labels and hierarchy at the top of Visitor sitemap.
  Moved the existing labelled source selector into the first field of the main
  Sitemap section, ahead of guidance, search and destination properties. Updated
  the page-derived properties help to refer to that selector above.
- Advanced sitemap options now contains only the custom text editor. Hide the
  group in page-derived mode, where it would otherwise be empty. Custom source
  opens its destination editor without automatically opening Advanced options.
  Retained source choices, saved settings, Undo and custom dirty-form guards.
- Refreshed the changed section-sitemap.js asset version. Updated README and
  architecture guidance; extended the existing source-default assertion to
  verify first-field placement and hidden inapplicable advanced tools.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes (existing CSS LF/CRLF notice). Required
  `python scripts/browser_review.py`: **2218/2218 passed**, no captured JavaScript
  errors (`.sitemap-source-top-browser.log`). Runtime files were held unchanged
  during the run; source switching and custom unsaved-edit checks remain passing.
- `python .sitemap-source-visual.py` captured actual light desktop and dark 320px
  Visitor sitemap views; inspected both and confirmed source selection appears
  first and fits the pane. Removed temporary helper/screenshots. Manual
  keyboard-only, screen-reader, zoom and Firefox/
  Safari review remain outstanding; automated checks do not establish full
  accessibility. Previous passing suite results below are historical.
- Next: observe the source-first Sitemap workflow with learners and complete
  manual accessibility/cross-browser review.
  No commit, push or deployment; prior working-tree changes are preserved.

## Sitemap outline and selected destination properties (11 November 2026)

- User requested the Content structure approach for Sitemap and simpler Advanced
  controls. Both page-derived and custom destinations now use a shared searchable
  native details/list outline beside selected properties, stacking at narrow
  available widths. Inclusion checkboxes remain native; a selected-item inclusion
  control updates those same existing choices. Page labels/path are read-only,
  with a preview link using the existing authored-target navigation handler.
- Custom destination CRUD is now outside Advanced options, visible in custom
  mode. Add and Organise destinations group creation/reorder/delete with the
  outline; selected properties retain label/parent/type/target editing. Advanced
  retains source selection and the raw text editor. Existing saved data, source
  semantics, bounded normalization and export generation are unchanged.
- Added Save/Discard guards for unsaved custom properties on selection, creation,
  branch actions, inclusion/Undo and source switching. The hidden legacy path
  select retains existing internal selection integrations; all visible selection
  uses the outline. Outline rows reconcile by stable ID/order so checkbox focus
  and branch expansion survive inclusion changes. Search reveals matching
  destinations with ancestor context and restores expansion when cleared.
- Reused safe textContent/value updates and existing normalized models. Refreshed
  five affected asset versions; updated README, architecture and unrun learner
  prompts. Historical geometry fixtures explicitly reveal the native branches
  they measure, exclude the hidden compatibility select and discard an invalid
  rejected form before continuing. Unrelated assertions are retained.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes with the existing CSS LF/CRLF notice. Initial existing focused checks:
  **204/204 passed**, no errors (`.sitemap-workspace-focused.log`). Expanded run:
  **238/240**, no errors (`.sitemap-workspace-focused-new.log`); two assertions
  incorrectly searched for a workspace inside the workspace node itself. Fixed
  that fixture. Screenshot review also caught narrow labels squeezed by inline
  inclusion controls. Removed nested card padding and put Include on a separate
  line at narrow widths; added readable-label-width regressions.
- Final `python .sitemap-focused.py`: **252/252 passed**, no captured errors
  (`.sitemap-workspace-focused-final.log`). `python scripts/button_states_review.py`
  initially passed **7/7 reduced-motion**, **8/9 forced-colour**; the latter
  captured a failed request for unchanged state-palettes.js. Clean rerun passed
  **7/7** and **9/9**, no errors (`.sitemap-workspace-states-final.log`). Required
  full `python scripts/browser_review.py` reached **2199 checks** before the
  existing 150,000ms virtual-time budget expired (`.sitemap-workspace-browser.log`).
  This is incomplete, not a passing full run. A second run uses corrected legacy
  geometry selectors for the visible outline instead of the hidden compatibility
  select also expired near the end at **2201 checks**
  (`.sitemap-workspace-browser-final.log`), likewise incomplete rather than passing.
  Based on measured expiry, increased the bounded virtual budget to 165,000ms and
  process timeout from 360s to 420s, retaining all assertions. Completed full run
  with that allowance: **2203/2218 passed**, no captured JavaScript errors
  (`.sitemap-workspace-browser-verified.log`). Fifteen older nested-layout checks
  exposed real horizontal outline overflow, rather than an application error.
- Isolated the legacy IA matrix with `python .sitemap-legacy-focused.py` and
  measured old checkbox margins: a 250px outline scrolled to 282px, with 32px
  inherited margins on third-level inclusion labels. The new reset selector was
  less specific than the old indentation rule. Corrected its specificity so the
  native tree supplies indentation once, and added no-horizontal-scroll assertions
  to the new readable-label matrix. Refreshed the final CSS cache version.
  Isolated corrected legacy run: **95/95 passed**, no errors
  (`.sitemap-legacy-corrected.log`); measured pre-fix failures are retained in
  `.sitemap-legacy-measured.log`. Final `python .sitemap-focused-final.py`:
  **252/252 passed**, no errors (`.sitemap-workspace-focused-verified.log`).
  Required final `python scripts/browser_review.py`: **2218/2218 passed**, no
  captured JavaScript errors (`.sitemap-workspace-browser-complete.log`), with
  runtime files held unchanged after the spacing correction. Final-source motion/
  colour rerun passed **7/7 reduced-motion** and **9/9 forced-colour**, no captured
  errors (`.sitemap-workspace-states-verified.log`).
- `python .sitemap-visual.py` captured light Basic automatic destinations, dark
  Advanced custom destinations at desktop and dark Basic custom mode at actual
  320px. Inspected the initial and final captures, including corrected phone label
  wrapping. `python .sitemap-nested-visual.py` additionally captured fully expanded
  third-level rows at actual dark 320px after the specificity fix; inspected the
  readable labels and inclusion controls. Removed temporary review helpers and
  captures. Manual
  keyboard-only, screen-reader, zoom and Firefox/Safari review remain outstanding;
  automated checks do not establish full accessibility.
- Next: observe learners using the shared Sitemap outline/properties pattern and
  complete manual accessibility/cross-browser review.
  No commit, push or deployment; results below are historical.

## Restore beside Save and removal of footer inspection shortcut (11 November 2026)

- User requested removal of Inspect footer HTML from Architecture and relocation
  of Restore current sample content from Advanced tools into Save and review.
  Removed that inspection shortcut; retained Inspect project data as requested
  by the narrower final scope. The main inspector remains available.
- Restore now shares the Save/Discard action row. Removed its former disclosure
  and moved the existing per-sample scope/Undo explanation into Save/review,
  linked to Restore with aria-describedby. Kept the same dirty-form guard,
  restoration handler, per-sample data boundaries and Undo behavior. No schema
  or generator changes. Refreshed both changed JS asset versions and updated
  README/architecture guidance, preserving prior working-tree changes.
- Extended the existing content-editor startup assertion to verify Restore's
  action-row placement, described help and absence from Advanced tools, plus
  absence of the Architecture HTML-inspection shortcut. Existing restore/Undo,
  unsaved-edit and responsive-control regressions remain intact.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes with the existing CSS LF/CRLF notice. Required full
  `python scripts/browser_review.py`: **2170/2170 passed**, no captured JavaScript
  errors (`.architecture-restore-browser.log`). Runtime files were held unchanged
  during this run, including existing restore/Undo and dirty-form regressions.
- `python .restore-visual.py` captured the actual light desktop and dark 320px
  Save/review panels; inspected both and confirmed that Restore wraps within the
  panel. Removed temporary helper and screenshots. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review
  remain outstanding; automated checks do not establish full accessibility.
- Next: observe the revised controls with learners and complete manual
  accessibility/cross-browser review. No commit, push or deployment. Earlier
  passing results below are historical.

## Simplified Architecture editor and visitor sitemap (11 November 2026)

- User approved the whole-section simplification analysis. Renamed the primary
  editor Content structure, kept the selected properties visible and preserved
  Save below Find content on desktop/after properties on phones. Combined the
  introduction and learning guide into one optional learning disclosure.
- Replaced three add buttons with one Add item action and an inside/beside/top
  placement selector. Organise content groups keyboard-operable move/delete and
  Expand all/Collapse all. Undo remains scoped to content. Related section and
  destination references are optional, opening for selected/newly typed links.
- Visitor sitemap is an independent disclosure opened from Save/review or the
  related-section shortcut. Inclusion controls and the sole live map appear in
  that view. Custom source selection, destination CRUD and text editing live in
  Advanced sitemap options; saved custom mode opens that option group on entry.
  Sample restoration and lesson code inspection are under Advanced tools.
- The duplicated full saved tree is now on demand under Review saved content
  plan. The studio renderer extracts the visitor preview from the shared escaped
  artifact into the sitemap view without changing export generation. Both data
  models, sample independence, existing saved plans, null/blank proposals and
  unsaved-form protections remain intact. Refreshed all five changed asset query
  versions; updated README, architecture notes and the unrun learner trial.
- `python scripts/check_structure.py`: **58 assets verified**; `git diff --check`
  passes (CSS LF/CRLF notice). Initial browser smoke failed **0/6**, capturing an
  initialization-order error: the sitemap root was detached before looking up
  its advanced controls. Retained the references before moving the root and
  reran. Initial `python .simple-focused.py`: **202/204**, no captured errors;
  both failures were an older broad assertion forbidding any nested summary
  inside properties. Scoped it to the properties section's own direct summary.
  Corrected focused run: **204/204 passed**, no captured errors
  (`.architecture-simple-focused-final.log`). Initial full browser run:
  **2168/2170 passed**, no captured JavaScript errors
  (`.architecture-simple-browser.log`); its only failures were those two outdated
  disclosure assertions. Final `python scripts/browser_review.py` with corrected
  assertions: **2170/2170 passed**, no captured JavaScript errors
  (`.architecture-simple-browser-final.log`). Runtime files were held unchanged
  during both full runs. No application changes were required for those two
  assertions; properties remain visible while their optional reference may fold.
- Inspected actual light Basic desktop, dark Advanced 390px visitor sitemap and
  dark Basic 320px properties captures from `python .simple-visual.py`. Removed
  temporary review helpers and screenshots. No manual
  keyboard-only, screen-reader, zoom or Firefox/Safari review; automated checks
  do not establish full accessibility. Earlier results below are historical.
- Next: observe learners using the simplified Content structure/Visitor sitemap
  workflow and complete manual accessibility/cross-browser review. No commit,
  push or deployment.

## Architecture simplification analysis (11 November 2026)

- User requested a whole-section analysis, particularly overlap between Website
  content and IA. Reviewed the current content editor, section sitemap controls,
  legacy destination CRUD/text editor, studio lesson assembly and saved artifact
  renderer, along with architecture guidance and historical product/recovery
  reviews. This review changes no runtime behavior.
- Found a duplicated full content tree (interactive editor and read-only saved
  artifact), separate destination editing paths available in custom mode, repeated
  Architecture guidance and multiple differently scoped save/Undo controls.
  Website content structure already represents content containment/labels; IA
  should explain the activity rather than suggest another required inventory.
- Recommended one primary Content structure editor and a separate Visitor
  sitemap view, with the saved full-tree review available on demand. Keep the
  established visible properties and Save below Find content on desktop. Group
  tree utilities, unify Add placement choices and move optional destination links,
  custom sitemap CRUD/text entry, restore and code inspection into appropriate
  contextual/advanced areas. Preserve keyboard-operable moving and saved plans.
- Navigation membership remains distinct from content containment: excluding a
  sitemap destination does not delete content, and proposals do not rewrite the
  sample website. Any simplified proposal control must retain the distinction
  between no replacement and an intentionally blank replacement.
- Commands run: bounded Get-Content/rg source reads, git status --short and
  git diff --check. No structure/browser/manual tests run for this analysis;
  the passing implementation results below are historical.
- Next: implement the agreed simplification scope, retaining both data models,
  existing saved-project compatibility, visible properties and responsive Save
  placement. No runtime edits, commit, push or deployment in this review.

## Visible Architecture properties and action placement (11 November 2026)

- User requested clearer branch-control placement, removal of confusing local
  numbering, visible properties and Save/review below Find content. Replaced
  the properties disclosure with an always-visible labelled section. Removed
  local step numbers from Understand, Develop the content plan and Save/review;
  the main twelve-step journey remains the progress indicator.
- Moved move/delete actions and Undo beside the tree's Add item controls. Renamed
  the action disclosure Move or remove selected item and added the selected
  item's name as safe text inside it. Selection/creation focus the visible name.
- Save/review is an independent grid child below Find content on wide screens.
  Narrow layouts follow DOM order: tree, properties, Save. The external submit
  button uses form="ia-form" and retains native validation and the original save
  handler; Discard, status feedback and unsaved-edit protection remain intact.
- Updated README, architecture notes and the unrun learner trial. Refreshed the
  two changed runtime asset versions. Updated obsolete disclosure assertions and
  added coverage for visible properties, contextual tree actions, actual external
  Save clicks, native required-field validation and responsive Save placement.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`
  passes (existing CSS LF/CRLF notice). `python .properties-focused.py`:
  **194/194 passed**, no captured errors (`.architecture-properties-focused.log`).
  Full `python scripts/browser_review.py`: **2159/2159 passed**, no captured
  JavaScript errors (`.architecture-properties-browser.log`). Runtime files were
  unchanged during this run. The lower check count replaces obsolete property
  collapse/toggle assertions with visible-section and external-Save coverage;
  unrelated regression assertions remain intact.
- `python .properties-visual.py` captured the actual revised light desktop layout,
  dark Advanced 320px visible properties, and dark Basic 390px Save and sitemap.
  Inspected all three and removed temporary helpers/screenshots. Manual
  keyboard-only, screen-reader, zoom and Firefox/Safari
  review remain outstanding; these checks do not establish full accessibility.
- Next: observe learners using the revised properties and action layout and
  complete manual accessibility/cross-browser review. No commit, push or
  deployment. Earlier results below are historical.

## Architecture centre workspace implementation (11 November 2026)

- User approved the proposed Architecture interface strategy. Moved the existing
  content editor and sitemap/custom-outline controls into one centre workspace.
  The left step retains its objective, workspace shortcut and review checklist.
  Existing IDs, shared validated state, preview/export generators and script order
  remain intact. Asset query versions refreshed for the three runtime changes.
- Content selection and editing split at 46rem of available workspace width and
  stack below it. Added native Add item and Organize selected branch disclosures,
  with Save, Discard and Undo visible. Longer lesson guidance is collapsible.
- Fixed silent loss of unsaved form values when selecting/adding another item or
  returning to Architecture. Dirty forms require Save or Discard before branch
  changes; same-content rerenders preserve edits. Project-level sample changes,
  imports and resets load their corresponding plan. No schema change.
- Updated README, architecture notes and the unrun learner trial. Added browser
  regressions for shared centre controls, focus routing, unsaved-edit protection,
  step return and responsive split/stack behavior. The invalid-cycle fixture now
  explicitly discards its rejected form before continuing; geometry fixtures open
  the new action disclosures whose controls they measure.
- Current checks: `python scripts/check_structure.py` verifies **58 assets**;
  `git diff --check` passes with a CSS LF/CRLF notice. Initial focused
  `python .architecture-focused.py`: **196/196 passed**, no captured errors
  (`.architecture-focused.log`). Initial full `python scripts/browser_review.py`:
  **2151/2161 passed**, no captured JS errors (`.architecture-workspace-browser.log`).
  Ten failures were fixtures affected by the new dirty-form guard, a stale
  selection-button reference after rerender, and a fixed viewport assumption
  rather than available workspace width. Updated these fixtures explicitly;
  the focused run verified their corrections.
- Polished primary Save styling, placed branch actions beneath the selected form,
  made the workspace shortcut scroll immediately to its focused heading and
  labelled the saved-plan review. Added sitemap-change draft retention checks.
  Final focused run: **198/198 passed**, no captured errors
  (`.architecture-focused-final.log`). `python scripts/button_states_review.py`:
  **7/7 reduced-motion** and **9/9 forced-colour** checks passed, no captured
  errors (`.architecture-states.log`). Final full `python scripts/browser_review.py`:
  **2163/2163 passed**, no captured JavaScript errors
  (`.architecture-workspace-browser-final.log`). Runtime files were unchanged
  during that final run.
- The first sandbox launch failed on temporary-profile permissions; browser runs
  used approved isolated-profile access. `node --check` was attempted for both
  changed JS files but Node is unavailable; successful browser execution covers
  their parsing. Historical suite results below predate this implementation.
- Inspected actual light desktop and dark 390px workspace captures generated by
  `python .architecture-visual.py`. An initial mobile capture used Chrome's minimum
  window width; corrected it to an explicit 390px iframe. Final captures verify
  the light desktop split, dark Advanced 390px tree and dark Basic 320px selected
  editor/Save/branch controls. Removed temporary helpers and screenshots.
  No manual keyboard-only, screen-reader,
  zoom or Firefox/Safari review; automated checks do not establish accessibility.
- Next: observe learners using the centre workspace and complete manual
  accessibility/cross-browser review. No commit, push or deployment.

## Architecture workspace UX proposal (11 November 2026)

- Reviewed the user's proposal to simplify the left wizard and place Architecture
  customization alongside centre-pane learning material. Inspected index.html,
  layout.css, content-outline.js, contribution/architecture guidance and the
  historical product/recovery reviews. The desktop control rail is configured at
  310px; the concern is also the amount of editing concentrated in that rail.
- Recommended keeping step navigation, a short objective, a workspace link and a
  review checklist on the left. Put the searchable content tree, selected-item
  form and contextual branch actions in a centre Architecture workspace. Keep
  guidance close to the relevant task and longer explanations in disclosures.
- Proposed one editor using the existing validated project model, with distinct
  content-planning and sitemap views, visible save feedback and protection for
  unsaved edits on selection. Proposed stacked tree/editor at narrow widths.
- This is a design recommendation, not an implemented or learner-validated UI.
  No runtime assets changed. Commands run were bounded Get-Content/rg source
  inspections, git status --short and git diff --check; no structure, browser or
  manual UI checks run. Earlier passing suite results below remain historical.
- Next: if proceeding, move the existing Architecture editor into the centre,
  simplify its left step and verify persistence, focus, responsive layout and
  preview/export agreement with the required checks.

## Collapsible selected content properties (10 November 2026)

- Renamed Selected content to **Selected content properties** and made it a native
  disclosure. **2. Develop the content plan** is an independent disclosure. Both
  start collapsed; selected name/path/origin and Save/review remain visible.
- Disclosure toggles preserve unsaved form values and do not modify project data.
  Selection and ordinary rendering retain open states. Selection focuses the
  properties summary when closed; adding an item opens properties and focuses its
  name. Invalid required controls reveal their containing disclosure before focus.
  Reset/import return both disclosures to closed. No project-schema change.
- Added responsive summary styling and focus indication, refreshed the two affected
  runtime asset versions, and updated README, architecture and the unrun learner
  trial. Preserved all previous working-tree changes.
- `python scripts/check_structure.py`: **58 assets verified**. `git diff --check`:
  passes with the existing CSS LF/CRLF notice.
- `python .content-disclosure-focused.py`: **178/178 passed**, no captured errors
  (`.content-disclosure-focused.log`). Covers existing content/Sitemap/student
  behavior plus independent toggles, saved/unsaved content, focus, validation and
  collapsed summaries at 320/390/1440px in both samples. Existing input/geometry
  fixtures now explicitly open the disclosure whose fields they exercise.
- `python scripts/button_states_review.py`: **7/7 reduced-motion**, **9/9
  forced-colour** checks passed, no captured errors (`.content-disclosure-states.log`).
- Inspected screenshots of the actual collapsed editor in light desktop and dark
  320px layouts. The phone capture needed a second scroll after responsive preview
  layout settled; final capture shows both summaries and Save beneath the header.
  No manual keyboard-only, screen-reader, zoom or Firefox/Safari review; automated
  checks do not establish full accessibility.
- `python scripts/browser_review.py`: **2143/2143 passed**, no captured JavaScript
  errors (`.content-disclosure-browser.log`). Runtime files were held unchanged
  during this run. Temporary focused/visual helpers and screenshots were removed.
- Next: observe students using the collapsed sections and complete manual
  accessibility/cross-browser review. No commit, push or deployment.

## Student content-planning interface (10 November 2026)

- User requested clearer Selected content properties and a content-planning flow
  that makes sense to students. Added three guided parts within Architecture:
  Understand this item, Develop the content plan, and Save and review. The twelve
  main journey steps and the detailed content inventory remain intact.
- Selected name/path/origin give context. Current sample content appears read-only
  before editable properties. Field help explains outline name versus displayed
  wording, content kind, containing item and optional section reference. Add inside,
  beside and top-level actions explain the hierarchy. Existing IDs/data values,
  validation, source references, branch controls and undo behavior are retained.
- Type-specific prompts/examples guide text, images, links, fields and containers.
  Readiness and purpose/owner/next-action notes use existing data fields. Shared
  human-readable kind/readiness labels align the form, outline and centre/export
  content artifact without changing normalized project values. No schema expansion.
- Proposal inclusion explicitly distinguishes no replacement from an intentionally
  blank proposal. Unsaved feedback and Discard act on form values; Save uses the
  existing plan commit. Save/Discard keep focus near the feedback. Guidance tells
  students to save before choosing another item. This does not auto-apply proposed
  wording or images to the sample website. Shared lesson overview, README,
  architecture and the unrun learner trial now include the planning exercise.
- Grouped fieldsets/legends, described controls, read-only styling and scroll offset
  support scanning and narrow layouts. Refreshed all affected asset query versions.
  Preserved earlier working-tree changes; no commit, push or deployment.
- Current structure check: **58 assets verified**. Diff check passes with a
  content-architecture.css LF/CRLF notice. Initial focused content/Sitemap/student
  suite: **152/152 passed**, no captured errors (`.student-plan-focused.log`).
  After moving sample content first and improving Save/Discard focus, focused
  rerun again passed **152/152** (`.student-plan-focused-final.log`). Final shared
  kind/readiness labels also passed **152/152**, no captured errors
  (`.student-plan-focused-verified.log`). Sample-linked and planning-only items
  now use distinct read-only content labels; the final full run covers these.
- Inspected real Studio screenshots of light desktop properties and dark planning
  at an actual 320px iframe width. Final captures verify that the target group is
  visible below the sticky header, fits the viewport and has no captured errors.
  `python scripts/button_states_review.py`: **7/7 reduced-motion**, then **8/9
  forced-colour** checks; the latter captured a failed request for the unchanged
  local brand-palette stylesheet. Clean rerun passed **7/7** and **9/9**, with no
  captured errors (`.student-plan-states-final.log`). No manual keyboard-only,
  screen-reader, zoom or Firefox/Safari review; automated checks do not establish
  full accessibility.
- Initial full browser run: **2115/2117 passed**, no captured JS errors
  (`.student-plan-browser.log`). Two Advanced export comparisons failed while
  the run overlapped final label changes: the initial app and later fresh comparison
  iframe could load different source revisions. Fresh unchanged-source comparisons
  passed **5/5**, including both samples/themes (`.student-plan-bridge.log`).
- Next full run: **2116/2117 passed**, no captured JS errors
  (`.student-plan-browser-final.log`). Advanced Header-deletion check exposed a
  race in the test's same-data file import: equality could pass before the async
  file read finished, and a late import could restore the deleted branch. Replaced
  the fixed 200ms delay with a bounded wait for the actual dss:imported event.
  All assertions are retained, with explicit completion now required. Focused
  content/Sitemap/student checks passed **152/152**, no captured errors
  (`.student-plan-import-complete.log`). No application deletion change required.
- Final `python scripts/browser_review.py`: **2117/2117 passed**, with no captured
  JavaScript errors (`.student-plan-browser-verified.log`). Runtime files were held
  unchanged during this run. Temporary helpers/screenshots are removed; structure
  check verifies **58 assets** and diff check passes (LF/CRLF notice only).
- Next: observe learners using the content-plan exercise and complete manual
  accessibility/cross-browser review. No commit, push or deployment performed.

## Page-label Sitemap implementation (10 November 2026)

- User clarified and approved retaining the detailed Website content structure
  while making Sitemap configuration follow visible eyebrows, with existing
  headings as fallbacks. Added a shared section-sitemap model and inclusion UI.
  Basic includes Hero plus Components, Layouts and Forms. Slashes stay in labels;
  children follow the nearest labelled containing destination. Group legends can
  act as headings. Unlabelled wrappers and the generated map add no entries.
- Both samples use fixed authored anchors, escaped labels and the same footer,
  lesson preview, inspector and export renderer. The collector inspects local
  sample HTML only, caches by project/Advanced state and guards recursion. The
  detailed content inventory/editor is retained. Canonical sections can focus
  their inclusion control; navigation references have no separate membership.
- Added validated per-sample sitemapSource and sitemapExcluded project data.
  Defaults follow the page; existing custom outlines/metadata/link bindings retain
  custom mode until explicitly switched. Custom controls remain available in that
  mode. Source switches preserve both plans. Include all, per-branch choices,
  source selection and Undo use existing project persistence. Undo restores only
  sitemap settings so a later brief/content edit is not overwritten.
- Updated lesson/configuration guidance, README, architecture and the unrun learner
  trial task to match the new navigation model; refreshed changed
  asset queries. Basic's generated map permits four desktop columns. Existing
  uncommitted step-chooser changes were preserved; no commit/push/deployment.
- Current checks: structure **58 assets verified**; diff check passed. First browser
  attempt failed on temporary-profile permissions; reran with approved access.
  Initial full suite: **2003/2037 passed**, no captured JS errors
  (`.eyebrow-browser.log`). Failures covered old default labels/counts, hidden
  custom controls and a navigation-reference control issue. Fixed that issue and
  updated defaults/explicit custom-mode fixtures; final verification is recorded below.
- Initial focused run **41/42**, no errors: its hostile-label fixture had retained
  custom mode when switching samples. Corrected it. Focused rerun **42/42 passed**
  (`.eyebrow-focused-final.log`); subsequently added Undo-scope/autosave/mode/empty
  selection checks, covered by the later passing runs below.
- Combined custom-navigation/content-tree/new-Sitemap checks passed **207/207**,
  then **213/213** after additional persistence cases (`.eyebrow-compat-final.log`).
  Final targeted Sitemap checks passed **52/52**, no captured errors
  (`.eyebrow-focused-verified.log`), including parent focus for a disabled child.
  `python scripts/button_states_review.py`: **7/7 reduced-motion** and **9/9
  forced-colour** checks passed, no errors (`.eyebrow-states.log`).
- Second full run **2064/2080 passed**, no captured errors
  (`.eyebrow-browser-updated.log`). Its remaining sixteen failures were old
  custom-navigation fixtures that had not selected the custom source and awaited
  preview refresh before focus/geometry assertions. Those setup corrections
  passed in the combined focused suite. Final complete rerun passed **2088/2088**,
  with no captured JavaScript errors (`.eyebrow-browser-verified.log`).
  Temporary helpers and screenshots have been removed. Final structure check
  still verifies **58 assets**, and `git diff --check` passes.
- Visual captures inspected Basic light desktop and actual 320px, dark actual
  390px footer, plus Advanced dark desktop. Actual-viewport layout/link checks
  passed with no captured errors. Early capture helpers had quoting/report parsing
  and viewport problems; corrected them before successful actual-viewport checks.
  No manual keyboard-only, screen-reader, zoom or Firefox/Safari review yet.
  Automated checks do not establish full accessibility. Next: try the updated
  learner task and complete manual accessibility/cross-browser review.

## Eyebrow-based sitemap review (10 November 2026)

- User proposed simplifying the Sitemap to reflect the hierarchy of visible
  eyebrow labels and link directly to each content container. Inspected shared
  sitemap generation, Basic/Advanced HTML generators and the content collector.
- Current sitemap uses a separate destination outline. Eyebrows already identify
  the main sections and some cards, but not every container: Basic list cards,
  form groups and several Advanced examples use headings/legends/badges instead.
- Proposed deriving labels from visible eyebrows, hierarchy from containing
  sections/groups and links from stable destination IDs. Missing eyebrows need
  either authored labels or an explicit heading fallback; repeated label text
  must not merge distinct destinations. Preview and export must share the map.
- Asked whether this should also replace the detailed Architecture editor and
  whether missing eyebrows should be added or use existing headings. No runtime
  changes made while those design choices remain open. Existing working-tree
  edits, including the step-chooser work above, were preserved.
- Read-only source inspection; no structure/browser/manual checks run for this
  review. Historical passing results below do not verify a new sitemap design.
- Next: resolve the intended editor scope and missing-label treatment, implement
  the shared hierarchy and add preview/export/navigation regression coverage.

## Keep the builder step chooser expanded (10 November 2026)

- User requested that the control beneath Step 1 of 12 in Build your design system
  remain expanded until manually collapsed. Identified this as Choose a step.
  Set the native disclosure open on initialization and removed automatic closure
  from step activation. User collapse/reopen choices now survive navigation and
  rendering; fresh page loads start expanded. No new persistence preference added.
- Added four browser regressions for startup expansion, preservation through
  navigation/rendering, manual collapse and manual reopen. Refreshed the
  studio-learning query version and updated README/architecture guidance.
- `python scripts/check_structure.py`: **57 assets verified**. `git diff --check`
  passed. `python scripts/browser_review.py`: **2037/2037 passed**, no captured JS
  errors (`.step-list-browser.log`), including all four new disclosure regressions.
  Removed the temporary edit helper. Final diff check passed. No manual keyboard,
  screen-reader or cross-browser checks performed this turn; those review gaps
  remain. No commit, push or deployment. Earlier results below predate this change.

## Actual content inventory and expandable IA editor (10 November 2026)

- User approved all recommendations from the IA reassessment. Implemented the
  primary Website content structure as an expandable/searchable outline with
  native details/lists, a selected-entry detail form, Add child/sibling/root,
  subtree reparent/reorder/delete, Undo, planning status/notes and per-mode restore.
  Current sample content remains read-only; planned content is stored separately,
  including deliberately empty drafts. Repeated role labels use separate stable
  IDs and remain editable. Parent choices and submission reject cycles/deep moves.
- New content-architecture model inspects only local authored HTML generators.
  Basic currently has 132 content entries and Advanced 395; each has five levels.
  Header logo/wordmark/navigation, Home/Hero copy and CTAs, image alt/caption,
  component content, lists/tables, form fields/options and Footer are represented.
  CSS-only wrappers and decorative SVG internals are omitted. Generated IA and
  footer sitemap views are referenced rather than recursively inventoried.
- `contentPlan.basic/advanced` is additive validated project data: null derives
  the live inventory, arrays save planning snapshots. Stable IDs/source keys keep
  actual values refreshed independently of edited labels/parents. Bounds: 1,000
  rows, twelve levels and 500,000 serialized characters per mode, plus individual
  string limits. Imported references are text, not hrefs; source keys are map
  lookups, not selectors/code. Malformed identities/cycles are rejected; missing
  parents are promoted to roots. Planning labels/drafts/notes are escaped.
- Content containment and navigation remain separate. The previous destination
  editor/text outline are secondary collapsed panels, preserving legacy metadata,
  fixed-ID aliases, custom outlines and sitemap choices. Canonical sections open
  their matching destination controls; navigation references have no independent
  membership. Removing Header from the content plan does not suppress Home.
  Custom legacy outlines attach actual known sections to saved relationships and
  retain unknown planned entries without duplicating canonical content subtrees.
- Centre lesson/Advanced exports share the escaped collapsible content artifact;
  centre open branches survive rerenders by stable IDs. Model renders/normalizes
  through child indexes, suppresses recursive collection and caches source
  signatures. The editor defers refresh outside Architecture and catches up on
  stage entry. No runtime dependencies were added. Updated asset versions, lesson,
  README and architecture. JSON upload limit raised from 100 KB to 4 MB after code
  review found richer saved plans could exceed the old limit; aggregate per-mode
  bounds keep complete exported plans within that upload limit.
- Verification so far: `python scripts/check_structure.py` verified **57 assets**;
  `git diff --check` passed with the existing tailwind-bridge LF/CRLF warning.
  Initial focused harness timed out at 300s because embedded hostile test text
  prematurely closed its script; a second run was interrupted while diagnosing.
  Diagnostic runs found that fixture error plus an extra test parenthesis. Fixed
  both. A valid focused run was **13/16**, exposing numeric progress values needing
  string conversion plus a fixture confusing Home's navigation reference with its
  canonical section. Next run **55/63** exposed Add child's chosen parent being
  omitted from its parent options. Fixed the parent filtering. Corrected focused
  run: **63/63 passed**, no captured JS errors (`.content-focused-corrected.log`).
- `python .content-visual.py` reviewed light Basic/Advanced desktop outlines and
  dark Basic content controls at an actual 390px iframe width, with 131/393 entries,
  depth five and no captured errors (`.content-visual.log`). Added regression checks
  for numeric progress, independently editable repeated labels, actual JSON file
  round trips and aggregate plan bounds. Full suite was interrupted to fix the
  upload limit before final verification. Expanded focused
  `python .content-focused.py`: **69/69 passed**, no captured errors
  (`.content-focused-file.log`), including actual file input and aggregate bounds.
- Full `python scripts/browser_review.py` reached **1,990 checks** before its
  135,000ms virtual-time budget expired (`.content-browser-final.log`). This is
  incomplete, not a passing full run. Increased the bounded virtual budget to
  150,000ms and process timeout from 300s to 360s based on that measured run; all
  assertions are retained. Completed expanded run: **2028/2030 passed**, no captured
  JS errors (`.content-browser-complete.log`). Two Advanced byte-identical export
  checks exposed stale content because the collector's cache key omitted the
  separate `adv` settings object. Included it and added an Advanced-only feedback
  refresh regression. Targeted `python .content-bridge.py`: **5/5 passed**, including
  both samples/themes with/without the optional Tailwind module.
- Coverage review found named div groups (Card grid, Resource library, layout
  comparison) were being omitted with CSS-only wrappers. Retained all authored
  destination IDs as meaningful content entries and added per-mode canonical
  coverage checks. Named destination roles are labelled by purpose. Final visual
  refresh: **132 Basic / 395 Advanced entries**, depth five, no errors
  (`.content-visual-final.log`). Inspected the refreshed Basic desktop artifact.
  Final focused `python .content-focused.py`: **72/72 passed**, no captured errors
  (`.content-focused-final.log`). Structure check remains **57 assets verified**;
  diff check passed. `python scripts/button_states_review.py`: **7/7 reduced-motion**
  and **9/9 forced-colour checks passed**, no captured JS errors (`.content-states.log`).
  Removed temporary implementation/test/visual helpers and screenshots; the new
  regressions remain in the tracked browser suite. Ignored logs remain. Final
  `python scripts/browser_review.py`: **2033/2033 passed**, no captured JS errors
  (`.content-browser-verified.log`). Final structure check verified **57 assets**;
  `git diff --check` passed after cleanup and documentation updates (existing
  tailwind-bridge LF/CRLF warning only). No commit, push or deployment performed.
- Next after verification: observe learners using the deeper outline and complete
  manual keyboard-only, screen-reader, zoom and Firefox/Safari review. Passing the
  automated Chrome suites does not establish full accessibility.
  Historical results below apply to earlier work, not this redesign.

## IA reassessment: actual content and deeper hierarchy (10 November 2026)

- User clarified that the IA should expose most actual website content, including
  Header logo/wordmark/navigation items and Home hero image/text/CTAs, with several
  nesting levels where needed. This turn reviews the approach; no runtime redesign
  has been implemented or approved as a final specification.
- Inspected current `design-process.js`, `site-builder.js`, Basic HTML generator
  and architecture notes. Current IA is an inventory of linked destinations with
  selected descriptive details; it omits Header and Home's actual content parts.
  The three-level cap and flat listbox are inadequate for the clarified goal.
  Basic's hero already has an image/caption, eyebrow, heading, intro, two named
  CTAs and a supporting note; Header has logo, project wordmark and navigation.
- Recommended a content inventory/structure supporting the IA lesson: meaningful
  regions, pages/sections, groups and actual text/image/link/form content. Show
  actual values beside role labels, and references for navigation links to canonical
  destinations. Shared Header/Footer are site-wide regions; avoid duplicating
  destination content beneath every navigation occurrence or representing CSS-only
  wrappers as information. Reviewed NN/g's IA/sitemap article again, which includes
  content inventories among IA activities and distinguishes sitemap artifacts.
- Proposed a collapsible, searchable outline with a selected-entry detail editor,
  Add child/Add sibling, reorder/reparent and Undo controls. Permit meaningful
  deeper nesting with technical safety bounds, replacing the three-level teaching
  restriction. Keep initial branches collapsed for readability. Actual content
  coverage must include both Basic and Advanced, with missing/planned items labelled.
- Sitemap membership must be based on destinations rather than layout ancestry:
  excluding Header must not suppress Home just because a navigation reference sits
  beneath Header. Existing ancestor-suppression behavior needs reassessment for
  this richer model. A destination's content and its navigation references are
  separate relationships. Content visibility remains independent of sitemap choice.
- Next implementation scope proposed: richer model with stable node identities,
  parent relationships, actual content values/references and migration of existing
  saved plans/choices; then the outline/detail controls and updated lesson/tests.
  Whether editing a content value should also change generated website content
  remains an implementation decision, not an existing capability.
- Read-only review plus this handoff update. No browser/structure tests rerun;
  historical 1962-check results below apply to the preceding implementation.

## Three-level information planning for both samples (9 November 2026)

- User approved another information level for Basic and Advanced. Added third-level
  content planning examples beneath existing components/topics: Basic now has 28
  IA entries and Advanced 49. New details default to content items excluded from
  sitemap navigation; existing linked destinations and authored body content stay
  intact. The lesson explains that three IA levels may describe one page, suggests
  fewer levels where sufficient, and links NN/g's flat/deep hierarchy guidance.
  Three levels is this editor's teaching limit, not a universal IA prescription.
- Added the full recursive `DSStudio.process.tree()` and flattened depth/position
  data. Kept `hierarchy()` as a two-level projection for existing lesson/wireframe
  readers. The full IA, selected sitemap, preview and exports share the new tree.
- Extended the structured editor to add/edit third-level entries, rename/reparent
  complete branches, reorder siblings, delete branches and undo. Parent choices
  prevent cycles and moves beyond three levels, including descendant height;
  submit validation also rejects forged choices. Ancestor exclusion disables
  descendants without changing their saved inclusion choices. Third-level controls
  have distinct indentation. New third-level entries default to excluded content.
- Previous complete two-level sample outlines resolve to the expanded examples
  without rewriting stored text or losing existing metadata. Custom outlines stay
  custom across modes. Metadata accepts paths of one to three labels, bounded to
  192 entries per mode for 64 raw lines with three derived nodes each. Structural
  edits retain the 64-entry/8,400-character limit; metadata-only edits preserve raw
  text. Fourth-level raw lines remain saved but are excluded from rendered trees
  and flagged with field validation/status; deeper imported metadata is rejected.
- Updated outline help, sample feedback, README, architecture and affected runtime
  query versions. Added three-level browser regressions and adjusted only existing
  expectations affected by the richer sample inventory and new depth limit.
- Current-session checks so far: `python scripts/check_structure.py` verified
  **54 assets**; `git diff --check` passed with an existing LF/CRLF warning for
  tailwind-bridge.js. Initial `python .third-level-focused.py`: **91/92 passed**,
  no captured JS errors (`.third-level-focused.log`). Its failed assertion exposed
  the fourth-level editing warning being cleared by render; moved status feedback
  after apply. First full `python scripts/browser_review.py`: **1958/1961 passed**,
  no captured JS errors (`.third-level-browser.log`). Two failures exposed long
  listbox options overflowing at 320px; allowed wrapped option text. The remaining
  security fixture expected an over-depth line to appear in the full IA; updated
  it to assert the explicit depth validation and retained all nonexecution/link
  checks. Added valid third-level hostile-label coverage and listbox width checks.
- Final focused `python .third-level-focused.py`: **93/93 passed**, no captured
  JS errors (`.third-level-focused-final.log`). Visual `python .third-level-visual.py`
  reviewed light Basic/Advanced desktop outlines and dark Basic inclusion/editor
  controls at an actual 390px iframe width. Final polish uses nonbreaking option
  indentation and normal-weight third-level detail text to distinguish levels.
  Final `python scripts/check_structure.py`: **54 assets verified**. Final full
  `python scripts/browser_review.py` after that polish: **1962/1962 passed**, no
  captured JS errors (`.third-level-browser-final.log`). `git diff --check` passed
  with the existing LF/CRLF warning. Temporary implementation/test/visual helpers
  and screenshots were removed; the new regressions remain in the tracked suite.
  Ignored logs remain. `python scripts/button_states_review.py`: **7/7 reduced-motion**
  and **9/9 forced-colour checks passed**, no captured JS errors
  (`.third-level-states.log`). Final `git diff --check` passed after cleanup/docs.
- No commit, push or deployment performed. Next: try the expanded plans with
  learners and complete manual keyboard-only, screen-reader, zoom and Firefox/
  Safari review. Passing the Chrome suites does not establish full accessibility.
  Historical results below predate this enhancement.

## Full IA with selected visitor sitemap and NN/g lesson (9 November 2026)

- User approved the IA/sitemap proposal and requested integration of NN/g's
  Information Architecture vs. Sitemaps guidance. Reviewed the source article and
  paraphrased the distinction with attribution/link in the shared Architecture
  artifact: Brief establishes release scope, IA organizes information and its
  relationships, and the visitor sitemap is a selected navigation artifact.
  The Contact/Opening hours example illustrates content retained without a
  sitemap link. Shared guidance/full IA/sitemap preview also reach Advanced HTML.
- Architecture now shows the complete outline in both samples, including
  Forms/Footer and sitemap-excluded information. The visitor preview and footer
  use the same selected sitemap generator. Removed Basic's hardcoded parent
  allowlist; Home/Footer default to excluded for legacy compatibility but can be
  included explicitly. Selected unlinked entries require the planned-entry toggle
  consistently in both samples. Planned text has no fabricated destination.
- Added native inclusion checkboxes for every parent/child in a labelled, locally
  scrolling region. Excluding a parent suppresses its branch and disables child
  controls while retaining their saved choices. Reused checkbox rows preserve
  focus through apply/render. The editor adds page/section/group/content types;
  groups are nonlinked headings. Neither inclusion nor type hides authored page
  content or generates arbitrary pages. Existing two-level outline editing remains.
- Additive `designProcess.iaEntries.basic/advanced` metadata stores validated
  stable IDs, one/two-label paths, type and inclusion. Existing JSON without it
  receives compatible defaults. Structured rename/reparent/reorder preserve
  identity and selection; delete/undo, JSON and local autosave retain metadata.
  Other-sample metadata survives mode changes and current-sample restoration.
  Raw edits retain matching paths; new paths represent new entries. Metadata is
  bounded to 128 rows per sample for legacy 64-line outlines; unchanged-structure
  inclusion/type/destination edits preserve raw text and do not truncate it.
  Structural CRUD retains its 64-entry limit and fixed destination allowlist.
- Studio sitemap-preview links use valid #previewShell proxies and fixed target
  metadata, revealing/focusing the actual iframe destination without changing
  project data or phase. Exported maps retain ordinary in-page fragment links.
  Imported labels use escaped text/textContent; imported metadata validates ID,
  path, depth, type and duplicates. No executable content or dependency added.
- Updated builder labels/help, stage task/overview, README, architecture and changed
  asset query versions. Early focused runs were **32/35**, then **34/35**: corrected
  fixture comparisons for resolved legacy plans, Basic reset and Basic export
  whitespace. First full suite: **1894/1904**, no captured JS errors (`.ia-browser.log`).
  Nine failures reflected intentional full-IA/planned-visibility/feedback changes;
  one exposed Studio links pointing to iframe-only IDs, fixed with preview proxies.
  Updated expectations while retaining geometry, destinations and state checks.
  Final focused `python .ia-focused.py`: **38/38 passed**, no captured errors
  (`.ia-focused-final.log`), including navigation, identity, branch inclusion,
  persistence, safe imports, raw legacy bounds and 320/390/1440px controls.
- Added 37 IA assertions to the tracked browser suite. Full
  `python scripts/browser_review.py`: **1907/1907 passed**, no captured errors
  (`.ia-browser-final.log`). Visual review then identified native-sized editor
  fields; styled selects/text fields and sitemap-preview link targets to at least
  44px, added those checks to existing responsive assertions and corrected remaining
  builder/Brief wording that conflated the IA outline with a sitemap. Full rerun:
  **1907/1907 passed**, no captured JS errors (`.ia-browser-polished.log`).
- Temporary `python .ia-visual.py` reviewed 1440px light full IA/selected sitemap
  and 390px dark inclusion controls, lesson/IA and visitor sitemap. The excluded
  Content card stays in the IA and page but is absent from sitemap navigation.
  Final Studio-only panel spacing uses its available spacing-unit token rather
  than relying on export-only spacing multiples. This does not alter website CSS
  or functional JS. Final focused verification after that cosmetic CSS change:
  **38/38 passed**, no captured errors (`.ia-focused-layout.log`), including the
  expanded 44px controls/link checks. Refreshed screenshots after the spacing fix
  and inspected the desktop model and phone sitemap again. Removed implementation/
  focused/visual helpers, test-extraction source and screenshots; ignored logs
  remain. Final structure/whitespace rechecks passed after handoff cleanup.
  `python scripts/check_structure.py`: **54 assets verified**; `git diff --check`
  passed (Git LF/CRLF notice for tailwind-bridge.js). Chrome runs used isolated
  profiles and were serialized. No commit/push/deployment.
- Next: observe learners and complete
  manual keyboard-only, screen-reader, zoom and Firefox/Safari review. Passing the
  automated suite does not establish full accessibility. Earlier results below
  are historical.

## Information architecture versus sitemap review (9 November 2026)

- User requested validation and recommendations before implementation: model key
  information and relationships in Architecture and choose which entries appear
  in the visitor-facing Sitemap. Reviewed design-process hierarchy, normalization,
  sitemap generator and the architecture notes, plus NN/g's IA/sitemap/navigation
  guidance and the W3C WAI visitor sitemap.
- Current implementation stores a bounded two-level pages/content-group outline,
  per-sample fixed-target link assignments and a global showPlanned option. The
  IA artifact is labelled a sitemap plan and Basic hides Forms/Footer in that
  view; the Basic footer also has fixed parent/destination filtering. Editing the
  plan does not automatically generate arbitrary website content/pages.
- Proposed distinction (recommendation, not implemented/approved): Brief defines
  purpose and agreed release scope; IA inventories and organizes that content and
  its relationships; the HTML sitemap is a selected navigation view derived from
  the IA. Keep content scope/display separate from Include in sitemap. Recommend
  one inclusion checkbox per entry at each supported depth, stable node identities,
  explicit parent/child filtering behaviour and valid destination requirements.
  Show the full agreed IA independently of sitemap exclusions; make any scope-driven
  content rendering an explicit separate capability rather than silently coupling
  it to sitemap visibility.
- No runtime/model/UI changes, browser or manual tests in this review. Earlier
  1870/1870 is historical. Next: settle the proposed interaction/model rules before
  implementation, preserving preview/download/JSON consistency and existing plans.
  Only this handoff note changed; `git diff --check` passed. No commit/push/deployment.

## Active lesson expanded at startup and on reload (9 November 2026)

- The user requested that the centre Brief accordion be expanded when Step 1 is
  active on reload, with the same behaviour for all twelve steps. Removed the
  startup-only exception in studio-learning's shared activation handler: startup
  now opens the active lesson as well as the preview. Normal loads start at Brief;
  selecting any other step opens its corresponding lesson through the same path.
  Other lesson accordions remain collapsed. Startup does not move keyboard focus.
- Real reload coverage exposed a second issue: startup fragment restoration used
  requestAnimationFrame before deferred modules necessarily initialized, allowing
  lesson initialization to close the destination again. section-accordions now
  restores initial fragments after DSStudio's ready event. Interactive hash/step
  navigation remains unchanged. Reloading an existing step section link restores
  its active builder step and open lesson. No new phase persistence, storage or
  project schema change; preview/export generators are untouched.
- Added a fresh default-Brief startup assertion and twelve real document-reload
  assertions in display order, including Prototype as Step 12. Each reload starts
  with a manually collapsed active lesson and checks new document identity,
  matching builder selection/control pane, exactly the matching lesson open,
  unchanged project JSON and no captured errors. The visible temporary test frame
  lets startup animation/fragment routing run normally. Updated the older test
  expectation that intentionally required all startup lessons collapsed.
- First temporary `python .active-lesson-focused.py`: **34/45**, no captured
  JavaScript errors (`.active-lesson-focused.log`); normal Brief startup passed,
  while the eleven other section reloads exposed the fragment initialization race.
  After the ready-event fix, focused rerun: **45/45 passed**, no captured errors
  (`.active-lesson-focused-final.log`). `python scripts/check_structure.py`:
  **54 assets verified**; `git diff --check` passed (existing Git LF/CRLF notice for
  tailwind-bridge.js). Fresh query versions cover both changed runtime scripts.
  Updated README and architecture startup notes.
- Required `python scripts/browser_review.py`: **1870/1870 passed**, no captured
  JavaScript errors (`.active-lesson-browser.log`), using an isolated Chrome profile.
  The full suite includes all thirteen new startup/reload assertions as well as
  existing all-stage navigation, manual native disclosure, preview/project/export,
  focus and responsive regressions. No test limits or assertions were relaxed.
- Temporary `python .active-lesson-visual.py` captured and reviewed 1440px light
  Brief startup, exact 390px dark Brief startup and 390px dark Prototype section
  startup: correct expanded headings, matching content and usable inline controls.
  Removed focused/visual helpers and screenshots; ignored logs remain. Final
  structure and whitespace rechecks passed after documentation/temporary cleanup.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain open.
  No commit, push or deployment performed. Earlier results below belong to prior
  work. Next: verify the startup behaviour in the user's browser and complete the
  outstanding manual review.

## Articulated design-system learning transition (9 November 2026)

- Reviewed the palette/token explanations, Spacing and local-CSS lesson, token
  catalogue, workflow, Deliver/Tailwind lesson and exported Advanced learning FAQ.
  The path was present but implied in places. Added an explicit ordered sequence
  to Spacing: local component `.card { padding: var(--space-6); }`, locally authored
  utility `.p-6 { padding: var(--space-6); }`, then Tailwind-generated p-6 using the
  mapped spacing theme. The examples focus on padding, not a complete component.
- Explained consistently that tokens store decisions and classes apply them to
  HTML. Palette/catalogue/workflow guidance connects to the Spacing example;
  Deliver restates the progression, and the Advanced page's learning FAQ carries
  the same path. Local component CSS stays in the inspector/preview/downloads;
  optional utilities and Tailwind remain separate practice exercises. No schema,
  framework dependency, website CSS or export-generation behaviour change; the
  Advanced HTML FAQ's authored prose changes intentionally.
- Clarified the actual mapping: the supplied theme aliases --spacing to
  --space-unit, so the component's --space-6, authored p-6 and mapped Tailwind p-6
  represent six units. Deliver's existing live calculation now names all three
  and the mapping. Checked official Tailwind padding/theme documentation; actual
  Tailwind compilation remains unverified. Updated README/architecture and fresh
  query versions for the four changed JS assets.
- `python scripts/check_structure.py`: **54 assets verified**; `git diff --check`
  passed (Git LF/CRLF normalization notice for tailwind-bridge.js only). Existing
  `python scripts/browser_review.py`: **1857/1857 passed**, no captured JavaScript
  errors (`.learning-transition-browser.log`), using an isolated temporary Chrome
  profile. No tests added merely to mirror prose. No commit/push/deployment.
- Temporary `python .learning-transition-visual.py` captured 1440px light and
  exact 390px dark Spacing progression views plus the 390px dark Deliver lesson.
  Inspected all three: ordered examples, code wrapping, shared-token explanation
  and optional practice links remain readable. Removed helper/screenshots;
  ignored logs remain. Final structure and whitespace rechecks passed after
  documentation and temporary-file cleanup.
- Next: observe learners using the transition. Manual keyboard, screen-reader,
  zoom and Firefox/Safari checks remain open, as does actual Tailwind compilation.
  Earlier results below are historical.

## Live inspector aligned with local component CSS (9 November 2026)

- The user wanted the live CSS/HTML inspector to demonstrate the local,
  framework-free approach. Removed the remaining exercise classes from both
  sample articles and stopped page-utilities.js from wrapping cssExport. The
  inspector, preview and website downloads continue to use the same generators;
  their website output now uses the original component/composition classes and
  contains no optional utility-rule bundle. No project schema changes.
- The 20 fixed utility definitions remain available to the optional lesson only.
  Practice now shows the actual exported article, then a prospective tag with
  exactly one selected utility and its authored rule. Added p-4 as a selectable
  comparison. Instructions say to copy the rule and add its class in a separate
  practice copy; measurements explicitly describe the unchanged component
  preview. Examples use fixed names and textContent, with no imported CSS or HTML
  execution. No runtime dependency or framework added.
- Added Inspect card CSS to the initial local-CSS lesson. Both it and the practice
  component-CSS action open the actual full stylesheet at .card. Updated action
  labels, inspector notes, Tailwind transition wording, README, architecture and
  changed script query versions. No filtered or substitute framework source is
  presented as the website's real code.
- Reworked utility regression coverage to execute the optional rules in a
  separate isolated iframe: default/custom values, both samples/themes and
  320/1440px appearance parity, padding changes, cascade order and theme colours.
  Added website utility exclusion, unchanged preview/export assertions, explicit
  practice/source separation and direct local-inspector action checks. Responsive
  checks include the new local-first action. Existing tests remain for shared
  preview, projects, imports and website exports.
- Read current handoff, contribution/architecture notes and the linked page-export
  review. Shared component ownership/cascade cleanup remains separate architecture
  work; this change makes the output boundary match the local-CSS teaching path.
  `python scripts/check_structure.py`: **54 assets verified**; `git diff --check`
  passed (Git LF/CRLF normalization notice for tailwind-bridge.js only).
- First full `python scripts/browser_review.py`: **1856/1857 passed**, no captured
  JavaScript errors (`.local-inspector-browser.log`). The remaining dark 320px
  spacing assertion measured cached button geometry inside closed utility practice.
  Temporary focused diagnostics reproduced both themes (**73/75**), showing no
  document/lesson overflow and correctly sized visible controls; only a hidden
  button's cached right edge failed. Updated the fixture to open practice before
  measuring all controls, await layout and restore its original disclosure state.
  All assertions and target sizes were retained.
  Focused rerun: **75/75 passed**, no captured errors
  (`.local-inspector-focused-final.log`). The next full run ended without a
  completion report (`.local-inspector-browser-final.log`), so it is not a pass.
  Added a harness-title progress marker to incomplete-run diagnostics without
  changing completion/pass criteria. The retry also ended without a complete
  report; its marker identified **1854 checks reached**, with the three final
  navigation/completion assertions still pending at the 120-second virtual-time
  boundary (`.local-inspector-browser-retry.log`). Increased only Chrome's bounded
  virtual-time budget from 120 to 135 seconds. Per-check waits, assertions and the
  300-second process limit are unchanged. Final full
  `python scripts/browser_review.py`: **1857/1857 passed**, no captured JavaScript
  errors (`.local-inspector-browser-complete.log`). All Chrome runs used isolated
  profiles. Structure and whitespace rechecks passed after final handoff cleanup.
- Temporary `python .local-inspector-visual.py` captured the 1440px light inspector
  focused at the real .card rule, 390px dark local lesson and expanded 390px dark
  practice. Inspected all three: the inspector retains actual component CSS;
  proposed practice HTML is separate from the real tag, code wraps and controls
  fit. Removed focused/visual helpers and screenshots; ignored logs remain.
  Structure/whitespace checks passed after cleanup. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review remain unrun, and actual Tailwind
  compilation remains unverified. No commit, push or deployment performed.
- Next: complete learner observation and manual accessibility/cross-browser review.
  Checks below belong to earlier sessions.

## Local CSS first, optional utility and Tailwind progression (6 November 2026)

- The user asked for the simplest local-CSS teaching path with a later transition
  to utilities/Tailwind. Step 8 now starts with semantic HTML, one linked local
  stylesheet and the actual base `.card` rule read from the current CSS export.
  A labelled minimal example teaches component reuse and shared tokens. Local
  CSS remains a complete way to finish the website; no universal performance or
  maintenance advantage is claimed for either approach.
- Simplified both sample generators: most cards and layouts retain their original
  component/composition classes. Only the single traced article in each sample
  adds p-6/bg-surface/text-content/rounded-card for comparison. The 20 authored
  utility rules remain available in the local CSS export, without applying
  redundant utility classes throughout the generated markup.
- Utility practice is now a closed native disclosure, with the full vocabulary
  in a second closed disclosure. Opening practice refreshes measured output.
  The exercise asks whether a shared component change or one utility fits the
  intended scope. A next-step fragment link activates Deliver's existing lesson;
  its return link activates the local CSS lesson without replacing project state.
- Deliver explicitly makes Tailwind optional, distinguishes locally authored
  rules from framework-generated utilities and explains that custom names need
  the mapped theme. Its transition exercise uses a separate Tailwind v4 practice
  project, the existing source snapshot and one article, then compares generated
  CSS/computed properties. No framework, build tool or network dependency added.
  Reviewed the official utility-class guidance; actual compilation is still
  unverified. Updated README, architecture and affected asset query versions.
- Added regressions for default collapsed practice/vocabulary, visible local CSS
  and escaped minimal HTML, current exported component rules in both samples/
  themes, utilities confined to the teaching article, and next/return navigation
  preserving project and preview. Existing expanded responsive checks now open
  both explicit disclosures.
- Initial `python scripts/browser_review.py`: **1851/1851 passed**, no captured
  JavaScript errors (`.local-css-first-browser.log`). Formatted the displayed base
  card rule onto separate declaration lines afterward; it differs from the actual
  export only in whitespace, which the regression now normalizes. Final full
  `python scripts/browser_review.py`: **1851/1851 passed**, no captured JavaScript
  errors (`.local-css-first-browser-final.log`). Chrome runs used isolated
  temporary profiles and ran serially.
- Temporary `python .local-css-first-visual.py` completed before and after that
  formatting change. Inspected 1440px light/390px dark local-first views and the
  expanded 390px utility practice: readable examples, closed initial practice,
  wrapped code and usable controls. Removed helper and screenshots after review;
  ignored logs remain. `python scripts/check_structure.py`: **54 assets verified**;
  `git diff --check` passed, including after cleanup (Git LF/CRLF normalization
  notice for tailwind-bridge.js only). Manual keyboard-only, screen-reader, zoom,
  Firefox/Safari and actual Tailwind compilation remain unrun. No commit, push or
  deployment performed. Earlier results below are historical.
- Final structure and whitespace rechecks passed after documentation and temporary
  file cleanup. Next: observe learners and complete manual accessibility/browser
  checks and consuming Tailwind compilation.

## Native page utilities and class-tracing lesson (6 November 2026)

- Resumed the interrupted implementation: 20 fixed, single-declaration plain CSS
  utilities now accompany existing component/composition classes in both sample
  HTML generators. Their token-based rules append to the shared CSS export, so
  preview, inspector and downloaded files use the same output. No framework,
  compiler, network dependency or saved-project schema change was introduced.
- Step 8 continues after Reflect with Read a class, follow its CSS. Four choices
  trace an actual sample article's opening tag, exported rule, current-theme token
  and measured preview value. Existing actions inspect full files, configure the
  source control and show the article; a disclosure lists all 20 utilities. Fixed
  selectors and textContent preserve the untrusted-data boundary. The lesson
  explains semantic HTML, component defaults, CSS source order and a downloaded
  p-6/p-4 exercise separately from the optional Tailwind source target.
- Diagnosed the recovered four spacing failures: the old exact-heading assertion
  counted the appended utility section as a sixth core teaching part. Retained
  the exact five-part check while excluding that named supplemental section;
  utility coverage now also requires placement immediately after Reflect.
- Fixed Show article in preview to scroll the Studio to the preview shell before
  focusing the article. Added a viewport-visibility regression and refreshed its
  runtime query version. Updated README and architecture; kept sample-generator
  versions and new assets from the interrupted work.
- Current-session `python scripts/check_structure.py`: **54 assets verified**;
  `git diff --check` passed, including after temporary review-file cleanup.
  Initial sandbox browser run failed accessing its temporary profile (WinError 5).
  First escalated full run hit the existing 300-second timeout without a report;
  a concurrent screenshot attempt also hit its 60-second timeout. Windows briefly
  reported insufficient paging-file capacity during concurrent Chrome work.
  Subsequent Chrome runs were serialized. No suite limit or assertion was relaxed.
- Temporary `python .utilities-visual.py` then completed twice using isolated
  profiles: reviewed 1440px light and exact 390px dark Studio layouts, including
  wrapped code and usable controls. The first successful images clipped the
  heading behind the sticky header; corrected the helper's scroll offset and
  inspected the final images. Removed temporary focused/preparation/test-extraction/
  visual helpers and screenshots; ignored logs remain. No manual keyboard-only,
  screen-reader, zoom, Firefox or Safari checks were run. No commit/push/deployment.
- Final `python scripts/browser_review.py`, run alone with an isolated temporary
  profile: **1828/1828 passed**, no captured JavaScript errors
  (`.utilities-browser-final.log`). Its 68 utility assertions include computed
  appearance parity with utility-free pages in both samples/themes, default and
  custom values at 320/1440px, actual utility edits/cascade order, live lesson
  tokens/measurements, inspection/configuration, preserved project/preview and
  preview visibility, plus usable lesson controls at 320/390/1440px. Earlier
  67/67 and 1823/1827 results in the recovery entry below are historical only.
- Next: try the utility lesson with learners and complete manual accessibility/
  cross-browser checks. Actual Tailwind compilation remains separate, unverified
  work. Final structure and whitespace rechecks passed after handoff cleanup.

## Recovered interrupted utility work (6 November 2026)

- Re-established the checkpoint from the working tree and saved local logs after
  a disconnect. Latest commit is `4e00578` (updated the architecture to be aligned
  with tailwind). Uncommitted work adds `page-utilities.js`, `utility-lesson.js`
  and `utility-lesson.css`, wires them into index.html, adds utility classes to
  both sample generators and adds browser regression assertions. This work is
  incomplete; the older current-objective summary below predates these changes.
- Existing `.utilities-focused-final.log` reports **67/67 passed** with no captured
  errors. Existing `.utilities-browser.log` reports **1823/1827 passed**, with no
  captured interaction JavaScript errors. The four failures are the spacing lesson
  "connects five teaching parts without replacing the design" assertions, in both
  samples and both themes. These are recovered results, not tests rerun during
  this recovery session; their cause has not yet been diagnosed.
- Recovery-session commands: read handoff/contribution/architecture/export-review
  notes, inspected git status/diffs/history, temporary helpers and saved test logs;
  `python scripts/check_structure.py` passed (**54 assets verified**) and
  `git diff --check` passed before this documentation update. No browser suite or
  manual checks rerun. No runtime edits, commit, push or deployment performed.
- Next: diagnose the four spacing-lesson failures, review the unfinished utility
  implementation, complete documentation and visual review, rerun required checks
  and remove temporary `.utilities-focused.py`, `.utilities-prepare.py` and
  `.utilities-tests.js` when no longer needed. Preserve outstanding manual
  accessibility/cross-browser and consuming Tailwind build checks below.

## Current objective

Keep Studio appearance independent of project design settings while preserving
one integrated wizard: Change a design decision, see it on the page, then follow
it into HTML and CSS. The header controls workspace appearance; Page theme
controls project examples and the Basic/Advanced page. The builder remains 25%
on desktop and the expanded inspector is capped at 25%. The first detailed
lesson uses the learner's spacing settings and actual output. Deliver now adds an
optional live CSS-to-Tailwind mapping lesson and theme-source snapshot without
changing website exports through that adapter. Step 8 starts with reusable local
component CSS, then offers closed utility practice in a separate copy of an article.
Tailwind is an optional next exercise with a route back to local CSS.
Next: observe learners using the lessons, verify the adapter in a consuming
Tailwind build and complete manual accessibility/cross-browser checks.

## Additive Tailwind mapping lesson (5 November 2026)

- The user preferred preserving current page CSS and using the centre pane to
  explain the mapping. Added the adapter/lesson first; deferred the earlier
  component/cascade cleanup recommendation. No existing website generator,
  component class, project schema or export format was changed in this phase.
- New local tailwind-bridge JS/CSS assets append From CSS tokens to Tailwind
  utilities inside Deliver's existing lesson. Authored CSS and Tailwind HTML
  examples teach the same four declarations; a live spacing calculation connects
  both forms to the saved unit. A disclosure contains 24 token mappings and two
  saved cutoffs, with current page-theme values and locally scrolling table.
- Optional Copy/Download Tailwind theme source actions produce tailwind-theme.css:
  mapped raw token snapshots for both themes, @theme inline aliases, literal
  breakpoint values and the data-theme custom dark variant. This is a selected
  foundation mapping, without page/component conversion or font loading. The
  lesson explains import/compilation in the consuming Tailwind v4 project,
  separate font setup, reset effects and snapshot refresh after edits.
- Values come from the actual CSS export via dssReadTokens, with responsive
  literals from the existing normalized settings. Fixed source/target names,
  textContent, unchanged-row/text-node reuse, cached parsing and lazy/coalesced
  refresh preserve validation, focus and performance. Module contributes no
  shared export CSS. Copy rejection opens source for manual selection; delayed
  feedback identifies an earlier snapshot. Existing Inspect website CSS action
  opens the full current export without adding an inspector language or stage.
- Added 36 browser assertions for both modes/themes, live foundation/semantic/
  font/type/radius/breakpoint mappings, source independence from theme/sample
  choice, copy/download/denied/delayed feedback, inspector output, hostile imports,
  reset, responsive controls and byte-identical website CSS/HTML/JSON compared
  with an otherwise identical document that omits the bridge. Both exports and
  the live preview document are also preserved through lesson interactions.
- Temporary `python .tailwind-focused.py`: **36/36 passed**, no captured JS errors
  (`.tailwind-focused.log`). First extraction helper attempt did not complete
  because a comment prefix was omitted; corrected the helper before this result.
  Final `python scripts/browser_review.py`: **1760/1760 passed**, no captured
  JavaScript errors (`.tailwind-browser.log`), including all 36 new assertions.
- `python scripts/check_structure.py`: **51 assets verified**; `git diff --check`
  passed. Added fresh query versions for the new assets and updated README and
  architecture. Browser commands used approved isolated temporary Chrome profiles.
- Temporary `python .tailwind-visual.py` captured 1440px light and exact 390px dark
  layouts. Inspected the lesson, code comparison and desktop table. The helper's
  first captures showed an intermediate smooth-scroll position; used instant
  scrolling to capture/review the actual lesson. Mobile code and copy wrap, table
  overflow stays local and Studio styling remains independent of page theme.
  Removed temporary focused/visual helpers and screenshots after review; logs
  remain ignored.
- Rechecked current official Tailwind theme/dark-mode/CLI guidance. No local Node,
  npm or Tailwind compiler was found; no packages/compiler were installed. Actual
  Tailwind compilation/rendering parity remains unverified. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review also remain unrun. Earlier test
  results below remain historical. No commit, push or deployment performed.
- Final structure and whitespace rechecks passed after documentation/temporary-file
  cleanup. Next: try the lesson with learners, complete the outstanding manual
  checks and validate the optional source in a consuming Tailwind v4 build.

## Page export and Tailwind analysis (5 November 2026)

- Reviewed current shared/Basic/Advanced generators, button/advanced export
  wrappers, responsive settings and catalogue reader after Studio separation.
  Compared with official Tailwind v4 documentation (displaying v4.3), including
  theme aliases, layers/Preflight, container queries, dark attributes, hover
  capability, browser baseline and local compilation.
- Added [page export review](PAGE_EXPORT_REVIEW_2026-11-05.md): existing semantic
  and modern-CSS strengths, prioritized source findings, proposed export boundaries
  and verification criteria. Advanced already has container queries; Basic already
  has intrinsic auto-fit Grid. No blanket layout rewrite is recommended.
- Recommended shared component ownership and cascade cleanup before an optional
  Tailwind theme adapter. Preserve dependency-free standalone exports and project
  values. Actual utility output requires a separate compiled export target;
  neither the adapter nor that target is implemented or verified.
- Documentation-only work; no runtime/dependency/export changes. No browser tests
  or manual checks rerun. Prior 1724/1724 is historical evidence for appearance,
  not proof of Tailwind integration. `python scripts/check_structure.py` verified
  **49 assets**; `git diff --check` passed in this analysis session.
- Next: implement the shared component/cascade phase if requested, preserving
  preview/export parity and updating catalogue/lesson readers and regression tests.

## Independent Studio appearance (5 November 2026)

- Separated the header's Studio: Light/Dark appearance toggle from project Page
  theme. Studio appearance is validated browser-local preference state, restored
  on reload and synchronized across tabs; unavailable storage allows session use.
  Project import/load/reset do not replace it. Page theme continues to synchronize
  preview, inspector and guided editors, saved projects and standalone HTML.
- Added local studio-appearance JS/CSS modules without dependencies or changed
  relative script ordering. Fixed Studio colours, typography, spacing and corners
  keep builder controls, lessons, inspector and preview toolbar stable. Core now
  publishes project roles/foundations under --project-*; authored component/type/
  state examples map these into their local styling. The real iframe still reads
  the shared, unchanged website generators. Both Basic/Advanced share one project.
- Scoped advanced feedback writes and link-underline changes to project styling.
  The hidden legacy Copy visible code action now uses Studio button styling.
  Added explanatory Page theme copy, consistent editor labels, refreshed affected
  asset query versions and updated README/architecture. No project schema change.
- Added browser regression coverage for every Studio/page theme combination in
  both samples, stable workspace styling through foundation edits, retained
  exports/inspector/preview/focus, blocked preference writes, fresh-document
  preference reload, hostile stored values, responsive controls and import/load/
  reset/active-project independence. Updated earlier expectations that intentionally
  coupled the page and Studio themes.
- `python scripts/check_structure.py`: **49 assets verified**; `git diff --check`
  passed. Initial sandbox Chrome launch failed creating/cleaning its temporary
  profile (WinError 5); subsequent browser commands used approved unsandboxed
  isolated profiles, without user projects/storage.
- First full browser run stopped on an invalid new fixture control ID; corrected
  the fixture. Next full run: **1711/1719**, no captured JS errors
  (`.studio-appearance-browser.log`). Its eight failed assertions came from an
  accidental text-encoding conversion of six existing UTF-8 expectation lines;
  restored those exact original expectations. No runtime or assertion relaxation
  was needed. Final `python scripts/browser_review.py`: **1724/1724 passed**,
  no captured JavaScript errors (`.studio-appearance-browser-final.log`), covering
  final runtime and the added saved-project/import/reset checks.
- Temporary `python .studio-appearance-focused.py`: **32/32 passed**, no captured
  JS errors (`.studio-appearance-focused.log`), covering final appearance runtime,
  blocked writes, fresh preference reads and 320/390/1440px controls.
  `python scripts/button_states_review.py`: **7/7 reduced-motion**, **9/9
  forced-colour**, no captured errors (`.studio-appearance-media.log`).
- Temporary `python .studio-appearance-visual.py` captured opposite Studio/page
  themes at 1440px and an exact 390px iframe. Inspected desktop preview, mobile
  header and scrolled mobile toolbar/preview: wrapping, theme boundaries and
  reading flow are clear. Manual keyboard-only/screen-reader/zoom/Firefox/Safari
  review remains unrun; passing these checks does not establish full accessibility.
  Removed temporary helpers/screenshots after review; logs remain ignored.
  No commit, push or deployment performed. Earlier entries remain historical.
- Final structure and whitespace rechecks passed after documentation/temporary-file
  cleanup. Next: review the separated interface with learners and complete manual
  accessibility/cross-browser checks.

## Backgrounds before interaction palettes (4 November 2026)

- Moved Webpage backgrounds before Generate interaction state palette steps in
  both Palette wizard and centre lesson. The backgrounds initializer relocates
  the existing interaction control/lesson nodes after its editor/lesson, retaining
  their handlers, current values and source relationships. Main Palette and status
  shade generation remain before backgrounds. No saved data or export logic changed.
- Updated the existing palette-order browser assertion to cover both panes,
  README/architecture ordering notes and the background script query version.
- `python scripts/check_structure.py`: **47 assets verified**; `git diff --check`
  passed (existing LF/CRLF notices only). `python scripts/browser_review.py` passed
  **1691/1691**, no captured JavaScript errors (`.background-order-browser.log`),
  including both order checks and the existing control/preview/export regressions.
  Earlier results below are historical.
- No new screenshots or manual keyboard/screen-reader/zoom/cross-browser review
  for this ordering change. No commit, push or deployment performed.
- Next: complete the outstanding manual accessibility/browser review.

## Interaction state colour dropdowns (4 November 2026)

- Added an inline colour dropdown above the shade steps for every General
  controls state and every state in all five button variants, in both wizard and
  centre views. Default displays the computed inherited source colour. Choices
  include validated Brand/Main colours, Neutral steps and the state's current
  shades; loaded custom source colours remain selectable. Choices copy hex values.
- Edits use existing semantic/button sources and saved fields. General edits
  affect the current theme. Button edits affect both themes; focus is shared
  across variants. Help names each source and related states that share it.
  Transparent variants edit their foreground colour. No independent per-state
  overrides, persistence schema or component-state rules were introduced.
- Default removes only that source property's override, using a read-only button
  default-colour getter backed by the existing resolver. The existing validated
  button setter now accepts explicit null to reset one property or default focus.
  Retained other button overrides, source assignments and dimensions.
- Dropdown nodes, focus and disclosures survive updates; choices are mirrored,
  refreshed after brand/source changes and labelled with help. Imported labels
  use textContent and colour choices require validated hex. Invalid selection
  values restore the control without changing project data. Existing apply/render/
  autosave paths update preview, inspector, exports and saved projects.
- Added 36 browser assertions for mirrored controls/defaults and brand options in
  every state/variant/theme/method, source edits/resets, transparent foregrounds,
  shared scope, JSON persistence and rejected values. Extended existing assertions
  for local autosave and all colour-selector target heights at 320/390/1440px.
  Temporary `python .state-colour-focused.py`: **96/96 passed**, no captured errors
  (`.state-colour-focused.log`), before the final autosave/target-height extensions.
  First full run reached its 180-second limit (`.state-colour-browser.log`).
  Avoided dropdown updates during unrelated typography/button-dimension edits;
  compute general inherited roles once and reuse shared source defaults per sync.
  Final focused **96/96 passed**, including autosave and all colour-selector
  target-height assertions (`.state-colour-focused-final.log`). The next full run
  also hit 180 seconds (`.state-colour-browser-final.log`). Increased only the
  harness wall-clock allowance to a bounded 300 seconds for the expanded matrix;
  virtual-time budget, assertions and pass criteria are unchanged. A check for
  orphan Chrome processes using the two timed-out profile IDs found none.
  Final `python scripts/browser_review.py` passed **1691/1691**, no captured
  JavaScript errors (`.state-colour-browser-complete.log`), with the 300-second
  allowance. No assertions or virtual-time checks were removed or relaxed.
- `python scripts/button_states_review.py` passed actual reduced-motion **7/7**
  and forced-colour **9/9**, no captured errors, including the final default-cache
  optimization (`.state-colour-media-final.log`; initial `.state-colour-media.log`).
  `python scripts/check_structure.py`: **47 assets verified**; `git diff --check`
  passed (existing LF/CRLF notices only). Updated README, architecture and both
  changed script query versions.
- Temporary `python .state-colour-visual.py` captured 1440px changed button-hover
  and exact 390px default Invalid layouts. Inspected both: source/help, selected
  colour, target sizing and shade tokens wrap correctly. Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review remain unrun. No commit, push or
  deployment performed.
- Removed temporary focused/visual helpers and screenshots; logs remain ignored.
  Final structure and whitespace checks pass. Next: try state choices with real
  content and complete manual accessibility/browser review. Earlier checks below
  remain historical.

## All interaction state palette steps (4 November 2026)

- The user clarified again: all states, not only Success/Warning/Danger. Added
  Generate interaction state palette steps in the Palette wizard and centre
  lesson. Mirrored component selectors cover General controls and Primary,
  Secondary, Accent, Outline and Text buttons without changing saved project data.
- New local `state-palettes.js` derives ten general state ramps (default, hover,
  focus, active/pressed, selected, disabled, loading, invalid, success, read-only)
  and seven states for each button variant. Each exports eleven shade tokens per
  theme (990 additional declarations total) using the existing ramp algorithm.
  Step 500 preserves the resolved source colour; hex casing is normalized.
  Existing status ramps remain available. No persistence fields were added.
- General sources follow semantic roles; button sources use the existing resolved
  contrast data, including overrides. Focus/selected use their indicator colour.
  Transparent variants explicitly use their foreground anchor. Notes distinguish
  shade options from displayed opacity/compositing, native state behaviour and
  non-colour cues. Generation does not remap component styling.
- Added catalogue source routes and current-theme shade/source CSS inspection
  and configuration actions. Views read actual exported declarations and preserve
  disclosure nodes through theme/colour updates. Selectors use existing field
  styling and a minimum 44px height. Updated README, architecture and affected
  runtime asset query versions; structure verifies **47 assets**.
- First focused run: **38/58**, exposing lowercase button-source versus uppercase
  exported shade display mismatch; normalized source hex and added lowercase
  override coverage. Subsequent focused runs passed **58/58**, then **59/59**
  after catalogue cache coverage (`.all-state-focused-final.log`), no JS errors.
  Coverage includes both methods/themes, all variants/states and shade tokens,
  overrides/transparency, inspector/source routing, project-data independence,
  retained disclosures and expanded 320/390/1440px layouts/selectors.
- Two full-suite runs hit the existing 180-second wall-clock limit before a
  report (`.all-state-browser.log`, `.all-state-browser-final.log`). Cached state
  generation by source settings, shared repeated anchors, cached catalogue source
  metadata, avoided unchanged catalogue output, and reused unchanged table rows
  during individual source edits. Added regression checks for row reuse and
  changed-value refresh. Final `python scripts/browser_review.py` passed
  **1655/1655** within the unchanged 180-second limit, with no captured JavaScript
  errors (`.all-state-browser-final-rows.log`). This includes all 59 new assertions
  and the final selector styling, generation cache and catalogue row reuse.
- `python scripts/button_states_review.py` passed actual reduced-motion **7/7**
  and forced-colour **9/9** with no captured errors (`.all-state-media-final.log`),
  before the final catalogue-only row-reuse change. `python scripts/check_structure.py`
  and `git diff --check` passed (existing LF/CRLF notices only).
- Temporary `python .all-state-visual.py` captured exact 1440px/390px layouts;
  inspected both after the selector styling adjustment. Shade tokens and controls
  wrap correctly. Manual keyboard-only, screen-reader, zoom and Firefox/Safari
  review remain unrun. No commit, push or deployment performed.
- Removed temporary focused/visual helpers and screenshots; logs remain ignored.
  Final structure/whitespace checks pass. Next: review state shades with real
  feedback and complete the outstanding manual accessibility/browser review.
  Earlier status-only work and checks below are historical.

## Status palette steps (4 November 2026)

- User clarified the requested state palettes as Success, Warning and Danger.
  Added Generate state palette steps after Main Palette generation and before
  webpage backgrounds, with compact eleven-step ramps in both wizard and centre
  Palette lesson. The lesson explains feedback meanings, semantic anchors,
  application to invalid/success feedback and the separate interaction behaviours.
- Shared CSS export generates 50–950 steps from each theme's resolved semantic
  status colour using the existing RGB mix/OKLCH generator. Step 500 preserves
  that colour, including validated overrides. Both themes receive the tokens;
  defaults and existing component state mappings remain unchanged. No new saved
  fields, duplicate generator or runtime dependencies were introduced.
- Current-theme ramp displays read actual exported declarations. Added complete
  CSS inspection and semantic configuration actions; catalogue rows identify the
  derived status source and route to its theme/role. Updated README, architecture
  notes and the three changed runtime script query versions.
- Added 14 browser assertions for both methods/themes, resolved anchors, exported
  preview parity, eleven-step teaching lists, independent theme overrides,
  catalogue routing, inspector/configuration actions and expanded 320/390/1440px
  layouts. `python scripts/browser_review.py`: **1596/1596 passed**, no captured
  JavaScript errors (`.status-palettes-browser.log`).
- `python scripts/check_structure.py`: **46 assets verified**; `git diff --check`
  passed (existing LF/CRLF notices only). Temporary
  `python .status-palettes-visual.py` used isolated browser profiles to capture
  1440px and exact 390px iframe layouts. Inspected both; shade chips, declarations
  and actions wrap within the lesson. Removed helper and screenshots afterward.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks were not
  rerun. No commit, push or deployment performed. Earlier checks below are historical.
- Next: review status foreground/background combinations in real feedback and
  complete the outstanding manual accessibility/browser review.

## Architecture UX requirements overview (4 November 2026)

- Revised Step 2's centre lesson into a concise requirements-planning overview:
  identify audience tasks, define essential scope, group and label content, and
  check a task route with someone from the intended audience. The stated outcome
  is an agreed sitemap connecting essential requirements to pages for Wireframe.
- Updated shared Architecture introduction/practice copy and wizard help; kept
  the existing sitemap editor, saved planning data and preview workflow. The
  authored overview adds no new fields or automated assessment. Updated README,
  architecture notes and the three affected script query versions.
- Current checks: `python scripts/check_structure.py` verified **46 assets**;
  `python scripts/browser_review.py` passed **1582/1582**, with no captured
  JavaScript errors (`.architecture-overview-browser.log`); `git diff --check`
  passed (LF/CRLF notices only). The browser used an isolated temporary profile.
- Temporary `python .architecture-overview-visual.py` captured 1440px and 390px
  layouts. Inspected both: overview, outcome and existing practice task are
  readable and fit the centre pane. Removed the helper and screenshots afterward.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks were not
  rerun for this copy change. No commit, push or deployment performed.
- Next: review the overview with learners and complete the outstanding manual
  accessibility/browser review. Earlier verification results below are historical.

## Header/Main/Footer region padding (4 November 2026)

- Added independent top/right/bottom/left padding sliders (0–64px) inside each
  Header/Main/Footer background fieldset, with summaries, values, help and a
  separate region reset. Padding is shared across themes/samples and represents
  extra space inside the outer region, preserving existing content gutters and
  inner section/component spacing. Body padding was not added.
- Optional `regionPadding` maps use existing state/autosave/JSON/import/reset.
  Only known regions/sides and finite numeric values are accepted; round/clamp to
  0–64px. Missing values resolve to zero. Twelve foundation tokens drive shared
  outer-region CSS. Advanced Main adds horizontal padding to its existing narrow/
  wide container gutters at the saved wide breakpoint. Background/opacity resets
  preserve padding; padding reset affects one region without changing its paint.
- Added centre padding declarations and inset examples, plus complete-file
  Inspect padding CSS actions and catalogue source routes to the real sliders.
  Existing background inspection handlers target only their own action buttons.
  Updated README, architecture and affected asset query versions. No alternate
  generator, schema, runtime dependency or user-authored root snapshot change.
- Added 47 assertions covering zero/max/asymmetric padding, both samples/themes,
  live/standalone computed values and 320/1440px overflow, preserved gutters,
  background independence, autosave/import, region reset, inspector/catalogue/
  focus, hostile imports and expanded 320/390/1440px controls/demos.
- Temporary `python .region-padding-focused.py`: initial **43/47** exposed
  Advanced's wide-gutter interaction. Corrected the wide media rule before the
  full run; subsequent focused **47/47 passed**, no JavaScript errors. Adjusted
  demo content fill/border for clarity, then final focused **47/47 passed**
  (`.region-padding-focused.log`). `python scripts/browser_review.py` passed
  **1582/1582**, no captured JavaScript errors (`.region-padding-browser.log`).
  The full run started before the last demo fill/border presentation adjustment;
  the final focused recheck covers that adjustment.
  `python scripts/check_structure.py`: **46 assets verified**; `git diff --check`
  passed (earlier LF/CRLF notices only). Isolated browser profiles outside the
  sandbox do not access user projects/storage.
- Temporary `python .region-padding-visual.py` captured the 1440px centre inset
  examples and 390px expanded padding controls with asymmetric values. Inspected
  both; clear inset boundaries, wrapping and individual values are visible.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain unrun.
  No commits, pushes or deployments changed. Prior results below remain historical.
- Removed temporary focused/visual helpers and screenshots; logs remain ignored.
  Final structure and whitespace checks pass. Next: try region styles with real
  content and complete manual accessibility/browser review; verify hosted CI after push.

## Studio section Back to top links (4 November 2026)

- Clarified scope with the user: studio sections only. Added a native, labelled
  Back to top link at the bottom right of every studio lesson/preview/reference
  panel, wizard pane and inspector, using a new local deferred module after
  lesson initialization. Avoided links on nested example cards or generated pages.
  Added a focusable studio header destination, decorative hidden arrow, underline,
  >=44px target and visible destination focus outline. Links remain in normal flow.
- Activation explicitly returns the outer window to scroll position zero and
  focuses the header; this avoids sticky-header anchor positioning and animation.
  Keeps the active step, project/local library, open panels, inspector language/
  visibility and preview document. Modified clicks retain native link behavior.
  No saved state, sample generator, exports, dependencies or root snapshots changed.
- Refreshed affected asset versions and updated README/architecture. Added 35
  browser assertions covering each container, both themes and 320/901/1440px
  layout, target sizes, focus/top restoration, state preservation, keyboard-style
  click activation despite smooth scrolling, all twelve stage routes, inspector
  retention and exclusion from both sample previews/exports.
- `python scripts/check_structure.py`: **46 assets verified**; `git diff --check`
  passed (earlier brand CSS LF/CRLF notice only). Temporary
  `python .section-home-focused.py`: **35/35 passed**, no JavaScript errors
  (`.section-home-focused.log`). `python scripts/browser_review.py` passed
  **1535/1535**, no captured JavaScript errors (`.section-home-browser.log`).
- Extended optional media checks for the new links under actual Chrome reduced-
  motion and forced-colour modes. Explicitly select Advanced for that script's
  existing component specimens now that Basic is the default; no runtime change.
  `python scripts/button_states_review.py` passed **7/7 reduced-motion** and
  **9/9 forced-colour** checks, no errors (`.section-home-media.log`). Browser
  checks use isolated temporary profiles outside the sandbox without user storage.
- Temporary `python .section-home-visual.py` captured the 1440px Palette section
  return and 390px Wireframe wizard return. Inspected both: right alignment,
  wrapping, spacing and non-overlapping flow placement are visible. Removed
  temporary focused/visual helpers and screenshots; logs remain ignored. Final
  structure and whitespace checks pass. Actual manual keyboard-only, screen-reader,
  zoom and Firefox/Safari checks remain unrun; automated checks do not establish
  full accessibility. No commits, pushes or deployments changed.
- Next: complete manual navigation and accessibility/browser review; verify hosted
  validation and Pages after these local changes are committed and pushed.

## Public repository readiness review (4 November 2026)

- Reviewed current README, licence, security/conduct/contribution documents, PR/
  issue templates, ignore rules, tracked root artifacts and local Actions/Pages
  workflows. MIT/community documents already exist; the Pages artifact allowlist
  includes only index.html and src. Root tokens.css/test.html and the legacy
  standalone file remain tracked in the public repository; no snapshots removed.
- Identified stale Unreleased changelog descriptions (Advanced default and early
  Prototype), a PR template missing the required browser check, and Actions still
  referenced by movable version tags. Recommend a reviewed release checkpoint,
  public quick-start/demo/storage guidance, deliberate snapshot/archive labelling,
  Actions update/hardening and completing manual browser/accessibility review.
  These are recommendations, not implemented changes.
- Local session changes, including CI's browser suite and the Pages validation
  dependency, are still uncommitted. The latest 1500/1500 result below belongs to
  the preceding implementation session; no runtime tests rerun for this review.
- Consulted official GitHub guidance for branch/status protections, workflow
  permissions/action pinning, secret scanning/push protection and security policy.
  Public repository/Pages fetches failed through the web tool. Did not verify
  remote deployment, branch protections, private vulnerability reporting, secret
  alerts or other account settings; no full credential/history scan performed.
- Only added this handoff note. No runtime/settings changes, artifact deletion,
  commits, pushes or deployments. Next: implement the agreed public-release
  cleanup, then verify actual hosted CI/Pages and repository security settings.

## Background transparency controls (4 November 2026)

- Clarified scope with the user: Body, Header, Main and Footer backgrounds.
  Added labelled 0–100% opacity sliders/output for all four, independently per
  theme. Only background paint changes; region content does not use CSS opacity.
  Colour/brand/neutral edits preserve alpha; a region reset clears its colour and
  alpha for the current theme. Existing whole-card opacity remains separate.
- Optional `backgroundOpacity` state follows existing JSON/autosave/import/reset
  paths. Only known regions/themes accept finite numeric percentages, clamped to
  0–100 and rounded to integers; absent/invalid settings remain fully opaque.
  No six-digit semantic colour validation, schema, dependency or root snapshot
  changes. New RGB/opacity/paint tokens drive shared preview/export CSS in both
  samples, with colour/opacity catalogue routes to their actual controls.
- Defined an opaque Surface canvas on exported html behind Body; Header/Main/
  Footer blend over Body. The centre model mirrors that stack, displays opacity
  tokens and blended colours, and calculates corresponding text/link ratios.
  Contrast inventory composites unrounded channels for text, indicators and
  button host contexts; colour-repair source targets retain original colours.
- Updated README, architecture and affected runtime asset query versions. Added
  38 focused assertions for alpha endpoints/partial values, both samples/themes,
  standalone/live agreement, opaque content, known blended contrast, autosave/JSON,
  colour selection, current-region reset, catalogue/inspector/focus, hostile/invalid
  imports and 320/390/1440px range/model sizing.
- `python scripts/check_structure.py`: **45 assets verified**; `git diff --check`
  passed (earlier brand CSS LF/CRLF notice only). Temporary
  `python .background-opacity-focused.py`: **38/38 passed**, no JavaScript errors
  (`.background-opacity-focused.log`). `python scripts/browser_review.py` passed
  **1500/1500**, no captured JavaScript errors (`.background-opacity-browser.log`).
  Browser profiles are isolated outside the sandbox without user projects/storage.
- Temporary `python .background-opacity-visual.py` captured the 1440px centre model
  and 390px controls with Body 50%, Header 35%, Main 70% and Footer 0%. Inspected
  both: blended paint, opaque text, alpha tokens and readable slider layouts are
  visible. Removed temporary helpers/screenshots; logs remain ignored. Final
  structure and whitespace checks pass. Manual keyboard-only, screen-reader,
  zoom and Firefox/Safari review remain unrun. No commits, pushes or deployments
  changed. Earlier test counts below remain historical.
- Next: review transparent backgrounds with real content and complete manual
  browser/accessibility checks; verify hosted CI after push.

## OKLCH default (4 November 2026)

- Changed the foundation ramp default from RGB mix to OKLCH for startup, New,
  Reset and missing/invalid imported methods. Explicit saved RGB mix/OKLCH choices
  still restore normally. All four palette families use the same selected method.
- Updated both initial method selectors and the initial method pill to OKLCH,
  refreshed the core script query version and updated README/architecture guidance.
  Added startup/control/lesson, New/Reset/Neutral, explicit import preservation
  and missing/invalid-method checks without changing the ramp algorithms.
- `python scripts/check_structure.py`: **45 assets verified**; `git diff --check`
  passed (earlier brand CSS LF/CRLF notice only). Temporary
  `python .oklch-default-focused.py`: **7/7 passed**, no JavaScript errors
  (`.oklch-default-focused.log`). `python scripts/browser_review.py` passed
  **1462/1462**, no captured JavaScript errors (`.oklch-default-browser.log`).
  Browser profiles are isolated outside the sandbox without user data.
- Manual keyboard-only, screen-reader, screenshots and Firefox/Safari review were
  not rerun for this default-only change. No root snapshots, dependencies, commits,
  pushes or deployments changed. Prior results below remain historical.
- Removed the temporary focused helper; logs remain ignored. Final structure and
  whitespace checks pass. Next: continue the outstanding manual accessibility/
  browser and learner reviews; verify hosted CI after push.

## Primary-derived Neutral palette (4 November 2026)

- Added a fourth, derived Neutral family to the shared core generator and palette
  process. `makeNeutralRamp` borrows Primary UI's OKLCH hue with midpoint lightness
  0.6 and chroma `min(primary chroma * 0.12, 0.025)`, then uses the selected RGB
  mix/OKLCH ramp method for eleven 50–950 shades. Achromatic primaries remain grey.
  Neutral 500 is labelled a derived midpoint, distinct from selected role anchors.
- Added a read-only Neutral explanation/midpoint in Main Palette, all eleven
  shade declarations in the wizard and centre, and `--neutral-*` CSS exports in
  both samples. Primary/method changes regenerate Neutral; Supporting/Accent edits
  do not. Existing semantic surfaces/text/borders and custom choices remain intact.
  Neutral introduces no new editable anchor, saved state, schema or dependency.
- Added Neutral catalogue classification/configuration through Primary UI and
  candidate contrast rows with Primary source targets. Body/Header/Main/Footer
  selectors append a Neutral group after all existing brand options. Selecting a
  step uses the established copy-hex behavior; later generation refreshes options
  without silently changing prior background assignments. Neutral inspection
  opens shade declarations or the actual background semantic declaration.
- Updated current README/architecture guidance, generator comments and affected
  asset query versions. Added 57 regression assertions for primary hue/chroma,
  black/white/grey handling, valid/unique/light-to-dark steps, both methods and
  samples/themes, UI/export agreement, neutral background use, copied-choice
  preservation, persistence, source routing, contrast candidates, inspection and
  expanded 320/390/1440px layouts. Updated old candidate-count and brand-only
  option assertions to include the new family without losing brand order checks.
- `python scripts/check_structure.py`: **45 assets verified**; `git diff --check`
  passed (earlier brand CSS LF/CRLF notice only). Temporary
  `python .neutral-focused.py`: initial **56/56**, final **57/57 passed**, no errors
  (`.neutral-focused.log`). First `python scripts/browser_review.py` passed
  **1454/1454**, no JavaScript errors (`.neutral-browser.log`). Final full run with
  the background-inspection correction/assertion passed **1455/1455**, no captured
  JavaScript errors (`.neutral-browser-final.log`).
- Temporary `python .neutral-visual.py` captured 1440px blue-Primary and 390px
  orange-Primary neutral lessons. Inspected both; cool/warm tint, derived midpoint,
  complete steps and readable wrapping are visible. Final manual keyboard-only,
  screen-reader, zoom and Firefox/Safari checks remain unrun. Browser checks use
  isolated temporary profiles outside the sandbox without user projects/storage.
  No root snapshots, commits, pushes or deployments changed.
- Removed temporary focused/visual helpers and screenshots; logs remain ignored.
  Final structure and whitespace checks pass. Next: try neutral assignments with
  real content and complete manual browser checks; verify hosted CI after push.

## Basic preview default and tab order (4 November 2026)

- Set startup, New and Reset to Basic. Moved Basic to the left tab and Advanced
  to the right, including initial HTML selection/tabpanel labelling and matching
  runtime click, Home/End, arrow-key, focus and tab-stop behavior.
- Explicit saved Basic/Advanced choices remain restored by imports/local projects.
  Older imported projects without a sample-mode field retain their historical
  Advanced page; invalid explicit modes fall back to Basic. Updated current README
  and architecture guidance and affected core/basic script query versions.
- Adapted historical feature fixtures to explicitly select Advanced after reset,
  while default/reset assertions call resetStudio directly. Updated sample-tab
  keyboard expectations, retained exact Advanced output comparison, and added a
  startup order/selection assertion. No sample generator or design data change.
- `python scripts/check_structure.py`: **45 assets verified**; `git diff --check`
  passed (LF/CRLF normalization notice for the earlier brand-palette.css change).
  Temporary `python .basic-default-focused.py`: **16/16 passed**, no JavaScript
  errors (`.basic-default-focused.log`), covering startup, New, Reset, explicit
  saved modes, pre-selector imports and 320/1440px tab order/keyboard focus.
  First full `python scripts/browser_review.py`: **1397/1398**, no JavaScript
  errors (`.basic-default-browser.log`). One planning-workshop fixture still
  expected Advanced after New; updated it to select that sample explicitly.
  Final full rerun passed **1398/1398**, no captured JavaScript errors
  (`.basic-default-browser-final.log`). Browser
  runs use isolated temporary profiles outside the sandbox, without user data.
- Manual keyboard-only, screen-reader, screenshot and Firefox/Safari review were
  not rerun for this small default/order change. No root snapshots, dependencies,
  commits, pushes or deployments changed. Earlier results below are historical.
- Removed the temporary focused helper; logs remain ignored. Final structure and
  whitespace checks pass. Next: verify the default in the user's preview and
  complete outstanding manual browser checks.

## Palette token process and final Prototype (4 November 2026)

- Added explicit brand token suffix editing after each colour's display name in
  Edit Brand Palette. The complete `--brand-*` declaration is visible in each row
  and the reference list. Safe, unique 1–40-character IDs use the existing import
  grammar; malformed/duplicate edits leave state unchanged. Display-name edits
  preserve token IDs. Token renames retain their editor node/focus, update exports,
  catalogue and contrast identities, and keep previously copied Main Palette values.
  Replacing project state also restores fields and clears stale token validity.
- Added `palette-process.js` after studio learning and before background lessons.
  Generate palette steps follows Main Palette/ramp method and precedes backgrounds;
  it shows all eleven 50–950 shade tokens for each role, with 500 marked as the
  selected anchor. Values update automatically from the shared CSS export, using
  the selected RGB mix/OKLCH method. The centre teaches brand declaration → copied
  Main Palette anchor → shade steps → light/dark semantic role → background use.
  It distinguishes custom semantic overrides and copied values from live aliases,
  and provides complete-file inspection actions without another generator/state.
- At the user's explicit direction, moved Prototype to the final step after
  Deliver. Plan now contains Brief, Architecture and Wireframe. Stable numeric
  control routes/IDs are retained internally; a separate ordered sequence drives
  visible numbering, Previous/Next, progress, phase groups, buttons and centre
  section order. Palette is step 4; Spacing is step 8; Prototype is step 12.
  Final review opens the existing live preview/inspector or existing Deliver
  controls. Saved task notes and earlier paper-style screens remain supporting
  material in a disclosure. No preview iframe replacement or project migration.
- Updated current lesson/README/architecture guidance and affected asset query
  versions. Added 45 focused regression assertions for renaming/validation,
  persistence, export-derived ramps across both methods/samples/themes, overrides,
  inspection, 320/390/1440px layout, reset validity and all twelve navigation steps.
  Adjusted older expected step order/labels and optional-rehearsal focus setup.
- `python scripts/check_structure.py`: **45 assets verified**; `git diff --check`
  passed (existing LF/CRLF normalization notice for brand-palette.css).
  Temporary `python .palette-process-focused.py`: initial **43/43**, then
  **44/44**, final **45/45 passed**, no errors (`.palette-process-focused.log`). First full
  `python scripts/browser_review.py`: **1395/1395**, no JavaScript errors
  (`.palette-process-browser.log`), before the final reset-validity refinement.
  Subsequent full runs passed **1396/1396** (`.palette-process-final.log`) and
  **1397/1397** (`.palette-process-order-final.log`), no captured JavaScript errors.
  Visual review exposed reference tools preceding Plan; corrected centre ordering
  so all twelve lessons immediately follow the unchanged preview, with references
  afterward, and covered it in the 1397-check run. Strengthened the final focused
  fixture afterward to dispatch the ramp control's input event, assert the selected
  method and change each actual Main Palette dropdown. Final **45/45** passes both
  methods/samples/themes; runtime code is unchanged since the full run. Browser
  runs use isolated temporary profiles outside the sandbox without user projects.
- Temporary `python .palette-process-visual.py` captured desktop shade/token-editor
  and final Prototype views, plus a 320px token lesson. Inspected all four;
  recaptured after centre ordering correction and verified the final desktop order.
  Removed temporary focused/visual helpers and screenshots; logs remain ignored.
  Final structure and whitespace checks pass. Manual keyboard-only, screen-reader,
  zoom, Firefox/Safari and learner review remain unrun. No root sample snapshots,
  dependencies, commits, pushes or deployments changed. Earlier results below
  remain historical.
- Next: try the revised palette process with learners and complete manual browser
  checks; verify hosted validation after these changes are committed and pushed.

## Body background and complete centre model (4 November 2026)

- Promoted the existing page canvas into a visible Body background fieldset before
  Header, Main and Footer, with the complete Brand Palette, picker, hex field and
  per-theme reset. Preserved `page-background-*` IDs, `--background` and existing
  semantic override data; no parallel Body setting, schema change or migration.
  Main continues following Body until its own override is chosen.
- Updated the centre Palette model to show Body enclosing Header/Main/Footer,
  with Body's current value, text/link contrast and complete CSS/HTML inspection
  actions. Updated semantic wording and Body's catalogue source route to the
  Palette control in the selected token theme. Refreshed changed asset versions
  and current README/architecture guidance.
- Extended existing background checks for visible Body ordering, model nesting,
  brand choices, both themes and samples, live/standalone computed body colour,
  inspector output, autosave/load, JSON round trip, reset/default lifecycle,
  catalogue routing and 320/390/1440px sizing/focus. Structure check: **44 assets**;
  `git diff --check` passed. Temporary `python .body-background-focused.py` passed
  **65/65**, no JavaScript errors (`.body-background-focused.log`).
  `python scripts/browser_review.py` passed **1351/1351**, no captured JavaScript
  errors (`.body-background-browser.log`).
- Temporary `python .body-background-visual.py` captured desktop/320px centre
  views. Inspected both; reduced narrow-screen nesting insets to keep the model
  readable. Final focused recheck after that CSS adjustment passed **65/65**;
  the full suite started before that presentation adjustment. Recaptured both
  screenshots afterward and inspected the final narrow model. Removed temporary
  focused/visual helpers and screenshots; logs remain ignored. Final structure
  and whitespace checks pass. Browser checks use isolated temporary profiles
  outside the sandbox without user data.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain
  unrun. No root snapshots, dependencies, commits, pushes or deployments changed.
- Next: review Body/Main colour combinations with real content and complete
  manual accessibility/browser checks; verify hosted CI after push.

## Header, Main and Footer backgrounds (4 November 2026)

- Expanded Palette's Webpage backgrounds after Brand Palette, Main Palette and
  ramp controls. Header, Main and Footer appear in page order, each with all
  named brand colours in saved order, picker, validated hex input and per-theme
  reset. Retained the original Page canvas controls/IDs in a disclosure. Brand
  selections copy hex values like Main Palette; reference edits refresh choices
  without silently changing earlier background assignments.
- Added `webpage-backgrounds.js` after studio learning, using existing semantic
  overrides, import validation, apply/autosave and generators. Three region tokens
  default to Surface, Background and Surface after existing overrides resolve;
  legacy projects preserve their defaults. Both sample headers, the shared main
  rule and shared footer consume those tokens. Cards and controls keep surfaces.
  Removed background binding from sitemap editing without changing its behavior.
- Added a centre Palette section showing the current theme/region colours and
  text/link contrast, with direct complete CSS/HTML inspection actions. Added
  region backgrounds to the contrast inventory and semantic editor, and routed
  catalogue Configure source to Palette in the token's theme. No duplicate editor
  state, new project schema, dependency or executable imported content.
- Updated affected asset query versions, README and architecture. Added 52 browser
  assertions covering brand/order, both samples/themes, standalone files, inspector,
  autosave/load, JSON round trips, invalid input/imports, safe brand labels, copy
  behavior, default/reset lifecycle and 320/390/1440px layouts/focus/target heights.
- `python scripts/check_structure.py`: **44 assets verified**; `git diff --check`
  passed. Existing full browser suite passed **1286/1286**, no errors
  (`.background-regions-browser.log`). Temporary `python .background-focused.py`
  passed **52/52**, no errors (`.background-focused.log`). Full suite with the
  new assertions passed **1338/1338**, no captured JavaScript errors
  (`.background-regions-final.log`). A final presentation adjustment made dropdowns
  and hex inputs at least 44px high and clarified the contrast copy. Re-ran the
  focused checks afterward: **52/52**, including enhanced target-height assertions
  for brand, picker and hex inputs at all three widths. The 1338-check full run
  precedes that final presentation adjustment. Browser runs use isolated temporary
  profiles outside the sandbox without user projects/storage.
- Temporary `python .background-visual.py` captured desktop/390px lesson views
  and the desktop background controls. Inspected all three; re-captured and
  inspected desktop controls after the final sizing adjustment. Removed temporary
  focused/visual helpers and screenshots; logs remain ignored and no screenshot
  baselines were added. Structure and whitespace checks pass on final files.
  Manual keyboard-only,
  screen-reader, zoom and Firefox/Safari review remain unrun; automated checks
  do not establish full accessibility. No root snapshots, commits, pushes or
  deployments changed. Earlier recovery results below remain historical.
- Next: try the background choices with real content and complete manual
  accessibility/browser checks; verify the hosted validation workflow after push.

## Recovery corrections and publishing validation (4 November 2026)

- Corrected sitemap commit's default to preserve the current Show planned entries
  choice. Creation, rename and deletion now behave like reordering; the checkbox
  remains the explicit visibility control, and Undo restores the preceding plan.
  Advanced's existing complete-map behavior is retained. Added regressions across
  both samples and both visibility states for all four operations, destination
  retention, Undo, checkbox changes, project JSON and live/exported footer output.
  Older planned-entry fixtures now explicitly select their intended visibility.
- Assigned fresh query versions to responsive-preview.js and the changed
  site-builder.js. Preserved the newer preview implementation and script order.
  This repairs the confirmed asset-identity rollback; no deployed-cache failure
  or returning-browser cache test is claimed.
- Reconciled README's collapsed Sitemap guidance and the page-background help
  with Basic's transparent main sections. Updated the architecture's visibility
  contract and contribution/README validation instructions.
- Made CI reusable for the existing Pages workflow, running structure and browser
  checks on pull requests and through the Pages caller on main pushes/manual runs.
  Deployment requires successful validation of the triggering revision; validation
  has contents-read permission and a ten-minute job limit. Reviewed against GitHub's
  reusable-workflow and job-dependency documentation. No added runtime dependency.
- Current `python scripts/check_structure.py`: **43 assets verified**;
  `git diff --check`: passed. Initial browser launch hit the Chrome temporary-profile
  sandbox restriction; completed runs used isolated profiles outside the sandbox,
  without user projects/storage. First `python scripts/browser_review.py` run passed
  **1285/1286**, including all 40 new sitemap assertions, with no JavaScript errors.
  The failure was the previously recorded intermittent 1280px inspector-focus check
  (opener top 47.8px vs header bottom 67.8px). Final full rerun passed **1286/1286**,
  no captured JavaScript errors (`.maintenance-20261104-browser-rerun.log`). No
  inspector code or assertions were changed to obtain that result; its intermittent
  failure remains a known verification concern. Earlier counts below are historical.
- Hosted Actions/deployment, manual keyboard-only/screen-reader/zoom/pointer/touch,
  screenshots and Firefox/Safari checks have not been run in this session. No
  root snapshots, saved-project schema, commits, pushes or deployments changed.
- Next: verify the first hosted validation run after these changes are committed
  and pushed, investigate the intermittent inspector-focus check if it recurs, and
  complete the manual accessibility/browser review.

## Merge and recovery audit (4 November 2026)

- Audited clean starting revision `20eb0d4` against both merge parents,
  `a253630` and `40228d4`, their shared `e9c05eb` baseline, current source,
  architecture, contribution instructions and earlier audit/product decisions.
  Added [recovery audit](RECOVERY_AUDIT_2026-11-04.md) with evidence, limits,
  reproduction steps, preserved decisions and recommended corrections.
- Confirmed the wizard, app header, 25% builder/right-inspector cap, native
  inspector, responsive preview startup, live Spacing lesson, footer Sitemap
  accordion, sitemap editor and newer Basic background fix remain present.
  Found no missing implementation among those reviewed features.
- Confirmed merge rollback of the responsive-preview asset query from
  `20261103-learning` to the older `20261103-ui-essentials` despite retaining
  newer source. Returning-browser cache behavior is a conditional risk; no
  deployed-cache failure was reproduced. Also confirmed a pre-existing sitemap
  bug: renaming a linked entry silently enables Show planned entries because
  save/delete use commit's true default. Undo/link retention pass. Recorded
  contradictory current footer guidance and the existing CI/publishing gap.
- Current `python scripts/check_structure.py`: **43 assets verified**;
  `python scripts/browser_review.py`: **1246/1246 passed**, no captured errors
  (`.reaudit-20261104-browser.log`). Initial sandbox launch failed on Chrome's
  temporary-profile access; completed runs used isolated profiles outside the
  sandbox without user projects/storage. `python scripts/button_states_review.py`:
  **5/5 reduced-motion**, **7/7 forced-colour**, no errors
  (`.reaudit-20261104-states.log`). `git diff --check` passed.
- Temporary `python .reaudit-20261104-probes.py`: **7/8 passed**, the failing
  assertion intentionally exposing visibility loss on rename, with no errors.
  Verified both themes' Basic section/background behavior, link retention and
  Undo separately. Removed the helper; ignored probe log remains. These findings
  are additional to the passing existing suite, not corrected runtime defects.
- No new screenshot/manual accessibility, Firefox/Safari, remote/deployed-site
  or real-font CDN review. Available history cannot establish absent uncommitted
  work from another computer. No app/source recovery, runtime changes, new
  dependencies, root snapshot edits, commits, pushes or deployments.
- Next: fix preview cache identity and sitemap visibility preservation with
  regression coverage; reconcile current documentation. Historical results below
  remain distinct from this audit.

## Footer Sitemap accordion (3 November 2026)

- Wrapped the shared Basic/Advanced Sitemap in native details/summary, initially
  collapsed, with a visible arrow and heading. Preserved the existing centred
  responsive columns, stacked child links, filtering/planned entries, navigation
  destinations, footer identity/main navigation and copyright/Back to top row.
- Retained nav#sitemap and its aria-labelledby heading; added stable disclosure/
  summary IDs. Native summary supplies expansion semantics and uses shared
  heading/spacing/focus tokens. Closing explicitly hides the map only. The
  generated exports work without JavaScript; no new runtime library or state.
- Existing preview disclosure capture retains open/closed state and summary
  focus during live updates. Native standalone fragments and existing preview
  fragment handling reveal a collapsed map target. Updated the generator asset
  query version, README and architecture.
- Adapted existing footer layout/target-size checks to expand the map before
  measuring it, retaining complete column/link coverage. Added default-closed,
  native-summary, focus/close/reopen, palette/theme state retention and live/
  script-free standalone fragment-navigation regressions for both samples.
- `python scripts/check_structure.py` passed (43 assets); `git diff --check`
  passed. Initial sandbox Chrome launch could not access its temporary profile;
  subsequent runs used isolated profiles outside the sandbox, without user
  projects/storage. First full run passed 1213/1228: the old Basic disclosure
  count needed updating, and closed-map geometry assertions exposed residual
  hidden navigation boxes. Added an explicit closed-nav display rule while
  preserving the open map layout. Final `python scripts/browser_review.py`
  passed **1242/1242**, no captured JavaScript errors
  (`.sitemap-accordion-review.log`).
- Temporary `python .sitemap-accordion-focused.py` passed **15/15**, no errors,
  for both samples' live/standalone disclosure and fragment behavior
  (`.sitemap-accordion-focused.log`). `python scripts/button_states_review.py`
  passed **5/5 reduced-motion**, **7/7 forced-colour**
  (`.sitemap-accordion-states.log`). Earlier counts below remain historical.
- Temporary `python .sitemap-accordion-visual.py` verified script-free exported
  footer states: Advanced light expanded at 1440px, Basic dark expanded at 390px,
  Basic light collapsed at 1440px. Confirmed no page overflow/errors, correct
  disclosure markers, >=44px summary and zero closed map height. Inspected all
  three screenshots. Removed temporary edit/test/visual helpers and screenshots;
  no visual baselines added. Logs are ignored.
- Manual keyboard-only, screen-reader and Firefox/Safari review remain unrun.
  No saved project schema/storage, root sample snapshots, dependencies, commits,
  pushes or deployments changed.

## Live Spacing tutorial prototype (3 November 2026)

- Added `src/js/spacing-lesson.js` and scoped CSS after existing lesson/example
  modules, preserving deferred load order and local dependency-free runtime.
  Step 9 now follows Understand -> Try -> Observe -> Inspect -> Reflect, with
  one spacing experiment driven by the current unit and real control limits.
- Reads current exported declarations/formulas, computes bounded known spacing
  multiples without eval, and keeps a session before/now comparison. Shows exact
  sample section markup/rules, theme and preview width, computed padding and
  explicit complete-file token/CSS/HTML inspection routes. Example navigation
  focuses the real Basic/Advanced section without invoking business actions.
- Initial focused review exposed Basic's larger responsive padding multiples;
  the lesson now reads its actual exported media rules and follows native media
  matching plus measured preview padding. It teaches base --space-8 and the
  --space-12/--space-16 overrides rather than claiming one fixed padding value.
  Explains that grid gap has its own decision/control.
- Added `preview:change` to shared preview measurement and invoke it after
  inspector layout changes. The lesson subscribes instead of adding a renderer
  wrapper or another resize observer. Coalesced reads let legacy imports and
  queued preview output settle before a fresh comparison captures values.
- Comparison rebasing changes only tutorial UI. Imports, local project loads
  (including identical values) and resets clear comparison/reflection; theme,
  sample and ordinary design edits retain it. Optional notes remain in the tab,
  never in project JSON or website files. No exercise score or learning success
  claim. Text-only updates retain nodes/focus; stale queued example focus is
  cancelled when code or navigation is selected afterward.
- Added a narrow-screen control anchor so the existing Spacing pane joins Try,
  rather than appearing after the entire tutorial. `lesson:content` refreshes
  placement after initialization. Desktop restores existing sidebar controls;
  IDs, bindings and token source routes stay intact, with no duplicate editors.
- Updated canonical spacing task wording, changed asset query versions, README,
  architecture and the prepared learner protocol. Added regressions for both
  samples/themes, prediction/comparison, actual padding/rules, viewport presets,
  Fluid/inspector resizing, input focus, source/code/example routes, import/reset/
  local-load lifecycle, escaping, session-only exports and 320/901/1440px layouts.
- Early browser attempt did not finish because a new hostile-text fixture
  contained a literal closing script delimiter in the HTML harness; corrected
  the fixture. An earlier full model passed 1197/1197, but focused review caught
  a wide-Basic assumption (70/71) and intermittent resize observation gaps.
  Corrected responsive content and moved updates onto shared preview events.
  Final focused `python .spacing-lesson-focused.py`: **76/76 passed**, no errors.
- Final `python scripts/browser_review.py`: **1202/1202 passed**, no captured
  JavaScript errors (`.spacing-lesson-review.log`), including the final narrow
  Try control placement. `python scripts/check_structure.py`: **43 assets**;
  `git diff --check`: passed. The initial sandbox launch could not access its
  temporary Chrome profile; subsequent runs used isolated profiles outside the
  sandbox, without user storage/projects. Earlier counts below remain historical.
- `python scripts/button_states_review.py`: **5/5 reduced-motion**, **7/7
  forced-colour** passed (`.spacing-lesson-states.log`). Temporary
  `python .spacing-lesson-visual.py` verified live 4->6 comparisons, both authored
  samples, actual 72px responsive Basic / 48px Advanced padding, five lesson parts,
  no overflow/errors and inline Try controls at 320px. Inspected 1440px Basic light,
  1440px Advanced dark with code open, and 320px Basic screenshots. Removed
  temporary helpers/screenshots; logs are ignored and no baselines were added.
- No learner trials, manual keyboard-only/screen-reader or Firefox/Safari checks
  performed. Automated results do not establish learning effectiveness. No
  saved project schema/storage, generated sample behavior, root snapshots,
  dependencies, commits, pushes or deployments changed.

## Cap the right inspector at 25% (3 November 2026)

- Changed the expanded desktop centre/inspector split from 1:1 to 2:1. With the
  left builder retained at 25%, this gives approximately 50% to the centre and
  caps the right inspector at 25% of workspace width after gutter accounting.
  Native disclosure, collapsed preview expansion and <=1280px stacking remain.
- Refreshed the affected CSS query version and updated README/architecture.
  Adapted the existing desktop geometry assertion to verify the cap, 2:1 split,
  25% left pane and no overflow across 1281–3440px. No new tests for this
  reversible width-only adjustment.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. First full browser run passed 1126/1127 with no JavaScript errors;
  the 1280px collapse-focus visibility assertion failed while every width/cap
  assertion passed. Added failure diagnostics and replayed the focused collapse
  subset using temporary `python .inspector-cap-focused.py`: **14/14 passed**,
  including a second replay with the longer sitemap lesson open. No inspector
  behavior changes were made for this unreproduced failure. Final
  `python scripts/browser_review.py` rerun passed **1127/1127**, with no captured
  JavaScript errors (`.inspector-cap-review.log`). Removed the temporary focused
  helper; logs are ignored. The focused output is `.inspector-cap-focused.log`.
  Initial browser launch hit the Chrome
  temporary-profile sandbox restriction; reran outside the sandbox with an
  isolated profile without saved user projects/storage.
- No button-state rules, inspector actions, generated sample CSS/HTML, project
  data/schema, root snapshots, dependencies, commits or deployments changed.
  Manual visual, keyboard-only, screen-reader, Firefox/Safari and learner checks
  were not rerun for this width-only change; prior screenshots/mode results are
  historical. This cap supersedes the earlier wider-than-25% requirement below.

## Consistent app spacing and step separation (3 November 2026)

- Added a 32px gap, divider and 24px top inset before each desktop wizard step,
  clearly separating Build your design system/introduction/navigation from the
  active step. Applied the same treatment throughout the builder, not only Brief.
- Defined app-scoped 8/16/24px spacing values and responsive 16–24px panel insets.
  Aligned outer/centre grid gaps to 16px; standardized builder/lesson panel
  padding, preview/inspector disclosure headings, field label/help gaps, planning
  editors, action rows, local-project separators, lesson cards and inspector
  body/code/control padding. Removed the inspector's inherited extra details
  padding so its title/panel align with the preview.
- Kept the 25% builder width, inspector behavior, responsive control placement
  and generated website spacing unchanged. App spacing uses separate variables
  and does not enter state, project JSON or exported CSS. Refreshed the affected
  CSS version and documented the spacing contract in architecture.
- Updated the existing geometry assertion for the consistent 16px centre/code
  gutter. No new permanent tests for reversible presentation styling.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1127/1127**, no captured
  JavaScript errors (`.app-spacing-review.log`). Initial sandbox browser launch
  could not access its temporary profile; reran with an isolated Chrome profile
  outside the sandbox, without opening user storage/projects.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks (`.app-spacing-states.log`). Temporary
  `python .app-spacing-visual.py` checked every step with expanded control groups
  in both themes at 1440/901/320px: no pane/page overflow or captured errors.
  Confirmed 32px step margin and 24px inset on desktop, and panel padding of
  24px at 1440, 18.02px at 901 and 16px at 320. Inspected light Brief, dark Buttons
  with expanded inspector and narrow Brief screenshots; 901px Typography was
  measured by the helper.
- Removed temporary visual helper/screenshots; logs are ignored and no visual
  baselines added. Manual keyboard-only, screen-reader, Firefox/Safari and learner
  reviews remain unrun. No generated sample files, root snapshots, saved projects,
  dependencies, commits or deployments changed.

## Clearer builder introduction (3 November 2026)

- Follow-up wording: the opening now reads Plan and design your website.
- Replaced the abstract Choose a step / lesson-controls-result paragraph with:
  Plan your website. Define its colours, typography and layout. See your design
  decisions on the page, then follow them into HTML and CSS.
- Copy-only edit to `index.html`; no behavior, assets, exports or data changed.
  `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. No new tests or browser/manual checks for this wording change;
  the preceding 1127/1127 result remains historical.

## Builder stays at 25% (3 November 2026)

- Set the builder to 25% of available workspace above 900px in both inspector
  states. Expanding code no longer widens the left pane to one third. Preview
  and inspector share the remaining space when open; the preview receives it
  when collapsed. Single-column layouts remain at <=900px.
- Refreshed the affected CSS query version, adjusted existing geometry checks
  for 25% with code open, and updated README/architecture. Below the three-column
  breakpoint, inspector expansion stacks vertically without changing pane widths.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1127/1127**, with no captured
  JavaScript errors (`.quarter-builder-review.log`). The initial sandbox Chrome launch
  could not access its temporary profile; reran outside the sandbox using an
  isolated profile without saved user projects/storage.
- No new tests for this reversible layout adjustment; adapted existing responsive
  assertions. No button-state rules, project data/schema, sample generators, root
  snapshots, dependencies, commits or deployments changed. Manual visual,
  keyboard-only, screen-reader, cross-browser and learner review remain unrun
  for this width-only change. Earlier screenshot/mode results remain historical.

## Native inspector disclosure and expanded width (3 November 2026)

- Replaced the separate compact bar and Expand button with one native
  details/summary inspector, using the same right/down disclosure arrow as
  Responsive page preview. Clicking the heading toggles the same pane in both
  states; contextual Inspect actions and the internal Collapse code action also
  remain available. Native toggle events synchronize layout state.
- Closed inspector sits above the preview with only its summary visible; code
  is hidden by native disclosure behavior rather than hiding the whole pane.
  Closing releases its column and retains the 25% desktop builder. Open desktop
  inspector sits on the right and exceeds 25% of screen width. The iframe and
  code DOM remain in place, preserving project values, browsing state and the
  chosen code view. Focus recovery now targets the native summary.
- Updated grid placement, removed the obsolete compact-bar styles/markup,
  refreshed changed CSS/JS asset versions and updated README/architecture.
  Adapted visibility/focus regressions to native open state; covered a native
  summary with marker/tab stop and an expanded width greater than 25%.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1127/1127**, no captured
  JavaScript errors (`.native-inspector-review.log`). Initial sandbox launch
  could not access Chrome's temporary profile; reran with an isolated profile
  outside the sandbox without user projects/storage.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks (`.native-inspector-states.log`). Temporary
  `python .native-inspector-visual.py` confirmed native disclosure-closed and
  disclosure-open markers, no page overflow/errors, and 444px expanded inspector
  width at 1440px (about 31% of screen width). Checked exact 320px too, and
  inspected desktop collapsed/expanded and narrow screenshots. Removed temporary
  edit/visual helpers and screenshots; no visual baselines added.
- Manual keyboard-only, screen-reader, Firefox/Safari and learner checks remain
  unrun. No saved project schema/storage, sample generators, root snapshots,
  dependencies, commits or deployments changed. Earlier separate-bar notes below
  are historical and superseded by this native disclosure implementation.

## Visible collapsed inspector bar (3 November 2026)

- Replaced the header Show code / Hide code action with a visible compact
  Live CSS/HTML Inspector bar above the preview. Its Expand button opens the
  existing right-hand pane; Collapse code returns to the bar. The compact bar
  disappears while the full pane is open, avoiding duplicate visible titles.
- Kept the previous column-release behavior: collapsed code reserves no grid
  column, the desktop builder uses 25%, and preview/lessons use the remainder.
  Expanded desktop code restores the three-column arrangement. Language, excerpt,
  theme, project values and iframe document remain intact across toggles.
- Shared collapse state synchronizes both controls, aria-expanded/controls,
  compact-bar visibility and the full pane. Closing focused code returns focus
  to Expand. A narrow-screen visual check found the bar could be offscreen;
  added conditional reveal so the focused opener is visible below the header.
- Refreshed CSS/dock query versions and updated README/architecture. Extended
  startup and collapse regression assertions to require the named visible bar,
  available Expand control and visible restored focus at all tested widths.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. Initial browser launch hit the Chrome temporary-profile sandbox
  restriction; reran in an isolated profile outside the sandbox. First full
  `python scripts/browser_review.py` passed **1127/1127**, no JavaScript errors.
  Final rerun including the focus-reveal adjustment/assertion also passed
  **1127/1127**, no captured errors (`.inspector-bar-review.log`).
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks (`.inspector-bar-states.log`). Temporary
  `python .inspector-bar-visual.py` confirmed the compact bar/expanded pane at
  1440px and compact bar at exact 320px, with no overflow or captured errors.
  Final focused checks confirmed Expand regains visible focus at both sizes.
  Preview remains 927.75px collapsed vs 357px expanded at 1440px. Inspected
  desktop collapsed/expanded and 320px screenshots.
- Removed temporary visual helper and screenshots after verification; logs are
  ignored and no visual baselines were added.
- Manual keyboard-only, screen-reader, cross-browser and learner trials remain
  unrun. No project storage/schema, generated samples, dependencies, root
  snapshots, commits or deployments changed. Older header-only toggle notes
  below are historical and superseded by this update.

## Hide inspector to expand the preview (3 November 2026)

- Inspector starts fully hidden, releasing its entire grid column. Above 900px,
  the hidden state gives the builder 25% of available width and preview/lessons
  the remainder. Opening code restores the prior one-third builder and (above
  1280px) centre/right-inspector columns. Narrow screens retain single-column
  controls/lessons and stacked inspection when requested.
- Added header Show code / Hide code with synchronized aria-expanded and
  aria-controls. Both toggles and contextual Inspect actions use a common dock
  visibility path. Hiding focused code returns focus to the header opener;
  reopening preserves language/section and still supports explicit CSS/HTML/JSON
  inspection. Hidden code has no keyboard targets or reserved layout track.
- Kept the iframe/document, project settings, generators, exports and UI-state
  persistence boundary intact. Fluid preview resizes through its existing
  observer. Refreshed CSS/dock asset versions; updated README and architecture.
- Added functional regression checks for initial 25% width, complete column
  release, increased Fluid preview width, focus recovery, language/excerpt and
  document preservation, header/inside/contextual toggles and excluded JSON UI
  state at 320/901/1280/1440/2560px.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1126/1126**, no captured
  JavaScript errors (`.preview-space-review.log`). Initial sandbox launch could
  not access its temporary Chrome profile; reran outside the sandbox using an
  isolated profile without user projects/storage.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks (`.preview-space-states.log`).
- Temporary `python .preview-space-visual.py` checked every wizard stage in both
  themes at 1440/901/320px: no page overflow or runtime errors. At 1440px, builder
  measured 338.25px (25% after the gap); Fluid preview grew from 357px with code
  open to 927.75px hidden. At 901px it grew from 476.95px to 546.45px. Inspected
  desktop/320px screenshots after settling scroll; removed helper/screenshots.
  No visual baselines added. Logs are ignored.
- Manual keyboard-only, screen-reader, Firefox/Safari and learner review remain
  unrun. No root snapshots, schema/storage keys, runtime dependencies, commits,
  pushes or deployments changed. Earlier expanded-inspector defaults below are
  historical and superseded by this update.

## App workspace introduction cleanup (3 November 2026)

- Removed the standalone Web Design System Studio heading and tagline above the
  workspace. Kept the app name in the header/browser title and other identity
  locations. The workspace now begins directly below the app header.
- Preserved the existing statement beneath Build your design system, increased
  it to normal-sized foreground text, and promoted the builder title to the
  page's single primary heading. Removed obsolete studio-introduction CSS and
  refreshed the affected CSS query version. README and architecture reflect this
  app-focused presentation; earlier branding/intro notes below are historical.
- `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1112/1112**, with no captured
  JavaScript errors (`.app-workspace-review.log`). Its initial sandbox launch
  could not access Chrome's temporary profile; reran with an isolated profile
  outside the sandbox, without opening user projects/storage.
- Temporary `python .app-workspace-visual.py` confirmed the removed banner,
  retained builder guidance, one primary heading and no page overflow or captured
  JavaScript errors at 1440px light and exact 320px dark. Inspected both screenshots.
- Removed the temporary visual helper and screenshots; no visual baselines added.
- No new permanent tests for this reversible presentation change. No generated
  website styles/content, project schema/storage, root snapshots, button-state
  rules, commits or deployments changed. Manual keyboard-only, screen-reader,
  cross-browser and learner checks remain unrun.

## Web Design System Studio identity and HTML/DOM/CSS model (3 November 2026)

- Adopted Web Design System Studio in the browser title, accessible header name,
  wordmark, introduction, footer, README and generated complete/button CSS
  attribution. Kept the existing decision -> page -> HTML/CSS tagline.
- Added a closed explanatory note beside the preview with escaped nested HTML
  and a token-based child-selector example. Explains that HTML means HyperText
  Markup Language; the browser parses it into DOM node objects, nesting describes
  parent/child/sibling relationships, and CSS selectors/rules assign presentation
  and layout property values. Distinguishes CSS properties from DOM object
  properties/methods; introduces cascade and inheritance without treating classes
  as object constructors. Updated README and architecture with this model.
- Checked the explanation against WHATWG HTML introduction/DOM trees and W3C
  Selectors/CSS Cascade standards. Source links are in the teaching note; no
  network requests or libraries were added to the runtime.
- Preserved project data/schema, DSStudio API, browser storage keys, download
  filenames, the existing DS mark and user-authored root snapshots. Historical
  audits retain their original project name. No repository/hosting renames,
  commits, pushes or deployments were performed.
- Refreshed changed JavaScript asset query versions. Current
  `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed **1112/1112**, with no captured
  JavaScript errors (`.web-studio-review.log`). The initial
  browser launch was blocked by sandbox access to its temporary profile; reran
  using an isolated Chrome profile outside the sandbox.
- Temporary `python .web-studio-visual.py` confirmed the new browser title and
  generated CSS attribution, two literal/escaped teaching examples with no
  injected section nodes, closed initial note and no page overflow with the note
  open or closed at 1440px light and exact 320px dark. Inspected screenshots of
  both sizes/themes; the longer name fits. No captured JavaScript errors.
- Removed temporary rename/visual helpers and screenshots after verification;
  no visual baselines added. The browser log is ignored.
- Manual keyboard-only, screen-reader, cross-browser and learner review remain
  unrun. No button-state rules changed; earlier mode checks remain historical.

## Three columns and preview-first startup (3 November 2026)

- Restored three columns above 1280px: the builder retains one third of available
  width on the left; centre preview/lessons and the live inspector equally share
  the remaining width. The inspector is sticky on the right and starts expanded.
  At <=1280px it stacks after the centre; <=900px keeps the single-column layout
  and actual controls within their lesson.
- Put Responsive page preview first in both DOM and visual order. It is the only
  centre section expanded at startup. All other centre sections remain visible
  as collapsed disclosures; selecting a wizard step opens its matching lesson
  and closes the other lesson sections. The preview iframe stays stationary.
- Removed active-lesson DOM reordering and kept the shared routing, focus,
  generators, project data and preview preservation. Refreshed CSS/JS asset
  versions, updated geometry/startup/navigation assertions and current docs.
- Temporary `python .three-column-visual.py` confirmed preview-first startup,
  only the preview section expanded, and an expanded right-hand inspector at
  1440px in light and dark themes. Also checked 1280px and exact 320px stacking;
  no page overflow or captured runtime errors. Inspected desktop/both-theme and
  320px screenshots. Narrow Fluid preview remains bounded by the available pane;
  fixed device presets are available for inspecting wider page viewports.
- Initial browser launch was blocked by sandbox access to Chrome's temporary
  profile; reran with an isolated profile outside the sandbox. First full run
  passed 1111/1112 with no JavaScript errors. One desktop-resize assertion found
  delayed control placement after returning from narrow widths; stage activation
  now synchronizes control placement immediately using the current media query.
- The second full run also passed 1111/1112, with the resize assertion passing
  and one brand-row focus assertion failing. Made responsive placement
  idempotent: correctly positioned panes/navigation are no longer reinserted
  during stage activation or delayed media-query callbacks, preserving focus.
- Final `python scripts/browser_review.py` passed **1112/1112**, with no captured
  JavaScript errors (`.three-column-review.log`). Current
  `python scripts/check_structure.py` passed (41 assets); `git diff --check`
  passed. Removed temporary edit/visual helpers and screenshots; no visual
  baselines added. The earlier layout/test counts below remain historical.
- Manual keyboard-only, screen-reader, Firefox/Safari and learner trials remain
  unrun. Button specimen rules were unchanged; earlier reduced-motion and
  forced-colour checks remain historical. No user storage, generated website
  dimensions, root snapshots, commits or deployments were changed.

## Wider builder and inspector above lessons (3 November 2026)

- Changed the desktop workspace to responsive 1:2 columns: Build your design
  system receives one third of available width instead of the former fixed
  310px. The existing single-column layout and inline lesson controls remain
  at <=900px. Generated website dimensions are unaffected.
- Moved the existing Live CSS/HTML Inspector before the centre lesson in static
  markup, aligning visual and keyboard order. It retains its Expand/Collapse
  control, initially collapsed state and contextual Inspect actions. No preview
  iframe reparenting or generator/state changes were needed.
- Refreshed the affected CSS asset version, updated desktop/inspector geometry
  assertions, README and architecture. Earlier layout notes below are historical.
- Current `python scripts/check_structure.py` passed (41 assets) and
  `git diff --check` passed. `python scripts/browser_review.py` passed
  **1112/1112**, with no captured JavaScript errors (`.wide-builder-review.log`).
  Initial sandbox launch could not access Chrome's temporary profile; reran
  outside the sandbox using an isolated profile without user storage.
- Temporary `python .wide-builder-visual.py` checked all twelve steps in both
  themes at 1440px, the 901px two-column boundary and 320px: no page overflow or
  runtime errors; inspector precedes lessons. At 1440px the measured builder
  was 451px, exactly one third of the 1353px available after the column gap.
  Inspected desktop/320px expanded-inspector screenshots. Removed the helper,
  edit script and screenshots afterward; no visual baselines added.
- No manual keyboard-only, screen-reader, Firefox/Safari or learner trials were
  run. Button specimen styles did not change; previous reduced-motion and
  forced-colour results belong to the preceding implementation. No commits,
  deployments, saved user projects or root snapshots changed.
- Next step: review the wider controls and top inspector in everyday use, then
  complete the outstanding manual accessibility and learner reviews.

## Integrated wizard implementation (3 November 2026)

- Added shared `DSStudio.stages` metadata and stage activation events. Previous,
  named Next, direct selection and token-source routes now synchronize the
  controls, matching centre lesson and focused heading. Accessibility opens its
  main review. Step position is navigation, not completion evidence.
- Removed Build/Preview/Code/Beginner steps, First steps with Basic, the separate
  exercise selector/progress and sixteen-entry numbered centre menu. The step
  list is a compact Choose a step disclosure with four phase headings. Renamed
  Components to Semantic colours and Layout to Spacing and surfaces.
- Each active lesson provides a short explanation, one task and relevant output
  actions. Integrated colour, spacing, responsive and export practice into their
  stages. Deeper lab/theory/control guidance lives in More about disclosures;
  workflow, catalogue and states remain secondary Reference tools with a return.
- Preserved real control nodes, handlers and project fields. At <=900px, move
  the actual controls beneath their lesson and Previous/Next after output;
  comment placeholders restore the desktop sidebar. No duplicate editors or new
  saved UI state. Source routes still reveal/focus the precise control.
- Kept the preview iframe stationary using CSS ordering after discovering that
  moving it reloaded its document. Stage entry frames an available example;
  ordinary edits keep focus and preview scroll. Retained Basic's rule/token
  connections and optional one-shot preview selection without the beginner shell.
- Moved sample selection beside the preview. One visible, initially collapsed
  inspector below the page handles CSS, HTML and full project JSON. Explicit
  Inspect actions select the promised language; copy/download retain complete
  generators and excerpt distinctions. Legacy centre code bindings remain hidden.
- Corrected confirmed audit defects: sitemap restore clears only the selected
  sample's link mappings; readiness clears after edits/reset/import/local load;
  clamp clipboard rejection gives a manual fallback; header/Deliver JSON exports
  use identical filenames and payloads. Removed static delivery checkmark cues.
- Refreshed affected runtime asset versions and updated README, architecture and
  learner-trial directions. Historical analysis/proposal documents remain dated
  records rather than claims that the old navigation is still current.
- Verification: `python scripts/check_structure.py` passed (41 assets), and
  `git diff --check` passed. Chrome's first sandbox launch could not access its
  temporary profile; subsequent checks used isolated profiles outside the sandbox.
  An early browser run had no final report; the instrumented rerun stopped at
  685/703 because retired guide tests accessed removed markup. Updated retired
  navigation/layout assertions while retaining generator/state/export coverage.
  Next full run passed 1109/1111 with no JavaScript errors; corrected the remaining
  expanded-control overflow at 320px. Final `python scripts/browser_review.py`
  passed **1111/1111**, no captured JavaScript errors (`.single-wizard-review.log`).
- Added regression assertions for all stage routes, focus, narrow control
  placement, contextual inspection, references and confirmed action defects. Then
  added explicit preview-document preservation coverage; ran the final focused
  subset through temporary `python .wizard-visual.py --focused`: **42/42 passed**,
  no errors (`.single-wizard-focused.log`). This subset includes the extra
  assertion added after the 1111-check full run.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks (`.single-wizard-states.log`). Temporary
  `python .wizard-visual.py` verified desktop/320px geometry and preview-document
  preservation; expanded typography/responsive controls fit in both themes.
  Inspected temporary 1440px and exact-320px Buttons screenshots and corrected
  header focus visibility/step-list height. Removed temporary helpers, CSS copy
  and screenshots; logs are ignored. No visual baselines were added.
- Manual keyboard-only, screen-reader, Firefox/Safari and real learner trials
  remain unrun; passing automation does not establish full accessibility or
  learning effectiveness. No user project storage, root snapshots, runtime
  dependencies, commits, pushes or deployments changed.
- Next step: try one complete decision -> page -> code cycle with a learner,
  including narrow-screen navigation, before further changes to stage count.

## Single-wizard simplification proposal (3 November 2026)

- Reviewed the current wizard activation, injected lesson routes, beginner path,
  inspector and section disclosure/offset code against the user's concern that
  Build/Preview/Code/Beginner steps and First steps with Basic add complexity.
- Added `docs/STUDIO_SIMPLIFICATION_2026-11-03.md`. Proposes one active step shared
  by controls and centre lesson, persistent page results, contextual HTML/CSS
  inspection and one Previous/Next sequence. Remove duplicate navigation and
  exercise progress; integrate useful beginner tasks into their relevant stages.
- Supersedes the earlier recommendation to retain a separate Basic shortcut path.
  Retain twelve stages initially, grouped under four phase headings, and align
  ambiguous names. Planning stages show actual artifacts/data rather than imply
  every decision changes page CSS. No new runtime dependencies or schema needed.
- Recorded navigation/focus/update rules, a Buttons walkthrough, implementation
  boundaries and acceptance criteria. Existing example mappings remain useful;
  removing the learning-path module wholesale would lose those connections.
- No runtime assets, project storage, exports, commits or deployments changed.
  No new browser/visual/manual or learner checks were run for this analysis;
  prior browser counts remain historical. Current `python
  scripts/check_structure.py` passed (41 assets); `git diff --check` passed.
- Next step: implement the shared stage activation and integrated lesson view,
  remove competing navigation, preserve contextual example/code connections,
  then validate all routes and the previously confirmed action defects.

## Design Workflow and button consistency audit (3 November 2026)

- Reviewed all twelve runtime wizard panes, sixteen centre sections, global/local
  project actions, beginner and inspector controls, colour repair and both sample
  pages. Read actual handlers and DOM reorganisation, not only static markup.
- Added `docs/WORKFLOW_REVIEW_2026-11-03.md` with a canonical twelve-stage process,
  centre mappings, a shared action/feedback contract, section-specific findings
  and an implementation sequence. Added the grouped runtime inventory in
  `docs/WORKFLOW_BUTTON_INVENTORY_2026-11-03.csv`: 379 groups / 1,567 button,
  internal-link and native-disclosure instances. Repeated token, contrast and
  specimen controls are grouped; conditional behaviour was also read in source.
- Isolated Chrome checks confirmed all twelve forward routes and their numeric
  return routes exist. Found naming/numbering ambiguity (Components vs colour
  roles, Layout vs Components, twelve stages vs sixteen centre numbers) and an
  Accessibility primary route to States rather than the contrast/review section.
- Confirmed action defects in the temporary profile: Deliver Show CSS leaves an
  already selected HTML tab active; restoring Basic's sitemap clears Advanced
  link mappings too; readiness ticks/status survive Reset. Clamp's copy action
  silently ignores rejected clipboard access, whereas the central copy action
  reports a fallback. Header/Deliver JSON exports also use different names and
  metadata. These findings are recorded, not fixed by this analysis-only task.
- Recommended one stage registry, twelve matching lesson identities with preview/
  overview/catalogue utilities outside stage numbering, consistent reveal/focus
  behaviour, explicit reset/export scopes and common studio action styling.
  Planning steps should inspect project data or relevant HTML rather than imply
  every planning field generates page CSS. Basic practice remains a shortcut path.
- Current checks: targeted runtime audit completed with no JavaScript errors,
  intercepted downloads and a simulated clipboard failure in isolated temporary
  Chrome profiles outside the sandbox. `python scripts/check_structure.py`
  passed (41 assets); `git diff --check` passed. The full browser suite was not
  rerun for documentation-only work. Earlier 1082/1082 and 38/38 results below
  remain historical. No user projects/storage were opened.
- Removed temporary audit helper/JSON; retained the inventory and ignored
  `.workflow-audit.log`. No runtime assets, existing user edits, sample snapshots,
  commits or deployments were changed by this review. Manual keyboard-only,
  screen-reader, cross-browser and learner trials were not performed.
- Next step: fix confirmed action/scope/progress defects first, then implement the
  shared stage/action definitions and validate the complete forward/return flow.

## Beginner path and connected workspace (3 November 2026)

- Added an opt-in First steps with Basic entry and four short exercises: action
  colour, reusable spacing, narrow layout and export/reopen. They select Basic,
  retain design values and route to existing source controls. Session progress
  is explicitly self-reported and is excluded from saved project data.
- Added sticky Build/Preview/Code/Beginner steps shortcuts, compacted the studio
  introduction, moved the longer three-exercise reference out of the inspector,
  and shortened repeated dock instructions. Code navigation retains the current
  language/study section and reveals the code area, including on narrow screens.
- Added Basic example connections: fixed element/selector/token mappings, actual
  rule text and theme-scoped declarations from the current CSS export, Configure
  source controls, and navigation to the matching rule in complete CSS. Section
  study choices update their related example. Formula tokens retain calc() text.
- Added optional one-shot preview selection. Primary actions and section/profile/
  FAQ/Grid/form/footer examples map to their appropriate study entries. Normal
  actions resume after selection, Escape (including inside the iframe), stopping
  selection or mode changes. An example selector provides a keyboard alternative.
- Added DSStudio.inspector.show() and an inspector refresh event rather than a
  new render wrapper. Reused exported CSS when reading catalogue values, cached
  unchanged study views and preserved normal copy/full-download paths. Updated
  affected asset query versions and documented state/API boundaries.
- Synchronized sticky offsets with measured workspace/header heights and fixed
  queued preview focus stealing focus after a subsequent Code/control jump.
  No teaching controls or UI state enter generated website files.
- Prepared `docs/LEARNER_TRIAL.md`: participant tasks, observation sheet and
  follow-up decision table. No learner sessions, analytics or messages occurred;
  actual participant observation remains outstanding.
- Current checks: `python scripts/check_structure.py` passed (41 assets) and
  `git diff --check` passed. First expanded `python scripts/browser_review.py`
  passed 1070/1080, no JavaScript errors: six former header-only offset assertions
  needed the workspace bar; four new checks required settled colour sampling,
  calc() expectations, normalized JSON comparison and focus investigation.
  Second full run passed 1078/1080 with no errors; remaining narrow-offset and
  queued-focus issues were corrected. Focused new-path harness passed **38/38**.
  Final full rerun passed **1082/1082**, with no JavaScript errors, in ignored
  `.learning-path-review.log`. Final FAQ/footer token mapping corrections were
  then checked by the focused harness: **38/38 passed**, no errors (ignored
  `.learning-path-focused.log`). All required checks passed.
- Increased the growing browser harness to a 90-second virtual budget and
  240-second process timeout, following the prior 120-second timeout during the
  product review. Assertions were retained/expanded; isolated Chrome profiles
  outside the sandbox do not use the user's stored projects.
- Inspected temporary 1440px initial/path/connection screenshots and 320px Code
  navigation. No page overflow or captured startup errors; compacting the entry
  restored some initial code visibility, and starting the first exercise showed
  its control, example and code together. Refreshed controls use studio styling.
  Removed temporary screenshot/diagnostic helpers and artifacts; no visual
  baselines were added.
- Manual keyboard-only, screen-reader, Firefox/Safari and real learner review
  remain unrun. No root sample snapshots, commits or deployments changed.
- Next step: run the prepared trial with learners and record anonymised findings
  before claiming learning effectiveness; complete manual accessibility and
  cross-browser review.

## Product and system analysis (3 November 2026)

- Reviewed the current implementation at `e9c05eb`, including the UI essentials
  showcase and newer sitemap/background controls, rather than assuming previous
  workshop/footer designs were still current. Read README, architecture, scope,
  historical audits, generator/state/inspector, planning/sitemap, token catalogue,
  persistence, layout and CI/deployment paths.
- Added `docs/PRODUCT_REVIEW_2026-11-03.md` with the decision -> preview -> code
  vision, strengths, concrete usability observations, planning/generation limits,
  recommendations and a prioritised next phase. Kept earlier reviews historical.
- Measured and inspected isolated Chrome views at 1440/1280/390 px and a 900 px
  studio height. Basic's code begins around y=947 at desktop startup; its Fluid
  preview is about 562 CSS px wide. At 1280 the inspector precedes the preview;
  at 390 its top is around y=3715 after the wizard. These are navigation/context
  costs, not assertions that controls are unreachable. Removed temporary visual
  helper/screenshots after review.
- Confirmed sitemap edits affect the plan/navigation rather than body sections;
  wireframe/prototype are bounded teaching artifacts. Noted differing Basic map
  filters and stale README references to a twelve-entry map/asymmetric checklist.
- Recommended clarifying the beginner path and scope, improving example-to-rule
  navigation and narrow-screen access, observing learners, then gating publishing
  and simplifying the shared update/generator contract. No runtime edits made.
- Current checks: `python scripts/check_structure.py` passed (39 assets).
  Standard `python scripts/browser_review.py` exceeded its 120-second process
  timeout without a final result. Reran the unchanged assertions/virtual-time
  budget alone with `python .system-analysis-run.py`, a temporary driver allowing
  240 seconds: **1045/1045 passed**, with no JavaScript errors (ignored output:
  `.system-analysis-review.log`). Removed the driver afterward. Final
  `git diff --check` passed. Earlier results below remain historical. Chrome
  used isolated temporary profiles outside the sandbox.
- No learner study, manual keyboard-only, screen-reader, Firefox/Safari review,
  user-storage access, commits or deployments. This is a source/product review
  with layout observations, not a complete accessibility or security audit.
- Next step: use the review to choose the next product iteration; learner
  testing should guide further expansion.

## Basic webpage background visibility (4 November 2026)

- Confirmed Basic Hero, Layouts and Forms painted full-width surface colours
  over the chosen webpage background, leaving only Components visibly affected.
  Removed these three section backgrounds so all four main sections expose the
  selected canvas. Cards, controls, header/footer surfaces remain independent.
- Refreshed the Basic generator asset version and clarified README/architecture
  behaviour. Added light/dark preview and standalone-export regressions checking
  the body colour and all four section backgrounds.
- Current checks: `python scripts/check_structure.py` passed (39 assets),
  `python -m py_compile scripts/browser_review.py` and `git diff --check` passed.
  Sandboxed Chrome could not start (GPU/access denied). Initial approved isolated
  Chrome attempts ended without a completed report. Increased the suite virtual
  time allowance from 60 to 120 seconds and process timeout from 120 to 180
  seconds; the completed run passed 1048/1049 with no captured JavaScript errors.
  All four new background checks passed; the existing contrast-review focus/
  disclosure assertion failed. Final rerun passed 1049/1049 with no captured
  JavaScript errors; no focus-related product changes were made. Temporary
  diagnostics removed.
- Manual visual, keyboard, screen-reader and cross-browser checks remain unrun.
- Next step: review the selected background across Basic's sections in the UI
  and complete the manual accessibility/cross-browser checks.

## Sitemap editor and webpage background (3 November 2026)

- Added Architecture controls to create/read/rename entries, choose a parent and
  existing-section destination, reorder siblings/groups, delete a branch, and
  undo the last edit. Retained the raw text editor in a disclosure and the full
  inventory restore action. Selected unmatched entries appear as Planned page
  in the footer, as explicitly requested; no placeholder body sections are added.
- Continued using the bounded two-level pages text; added validated per-sample
  pageLinks and showPlanned fields to planning data. Fixed-ID-only destination
  validation, escaped rendering, 64-entry limits and stale-undo invalidation
  cover imported data and editing edge cases. Rename preserves sibling order.
- Changes feed existing preview, inspector, artifact, project/JSON and export
  generators. Basic's optional planned view retains Home/Footer exclusions;
  Advanced's complete map and existing legacy aliases remain supported.
- Added Palette background picker/hex/reset for the current theme, reusing
  semanticOverrides rather than introducing another stored colour setting.
  Both samples and export use it; light/dark values are independent.
- Added one runtime module, refreshed affected asset versions, updated docs and
  browser regression checks. User root snapshots/scope file remain untouched.
- Initial `python scripts/browser_review.py` passed 1039/1039, including CRUD,
  persistence, preview/inspector, background and unsafe-target coverage. Added
  sibling-order, entry-limit, stale-undo and narrow-editor checks afterward.
  Final suite passed 1045/1045 with no interaction JavaScript errors using an
  isolated temporary Chrome profile outside the sandbox (ignored log:
  `.site-builder-review.log`). Structure check passed (39 assets), Python
  compilation and `git diff --check` passed.
- Visually reviewed light desktop Architecture/Palette and 320px Architecture
  screenshots; controls fit and wrap. Corrected the screenshot helper for
  Chrome's minimum window size by explicitly setting the iframe to 320px.
  Rechecked final Save button styling; removed temporary screenshots/helper. Manual
  keyboard-only, screen-reader and Firefox/Safari checks remain unrun.
- Next step: try the editor with a learner and complete manual accessibility
  and cross-browser review.

## Basic CSS simplification (3 November 2026)

- Consolidated repeated heading, link-target, flexible-child and form-control
  declarations. Removed obsolete form-section FAQ rules, unused demo-link
  styling and redundant sizing already supplied by the global box model/cards.
- Placed the shared page styles before section rules, retaining mobile nav
  precedence and section-labelled study excerpts. Moved sidebar heading styles
  beside that layout; refreshed outdated HTML comments and the Basic JS version.
- Basic's authored page layer fell from 115 to 107 blocks and 286 to 261
  declarations (counts include media-query blocks, exclude shared foundations
  and footer). Shared tokens/components remain to support studio controls and
  matching previews/exports. Advanced and the shared footer are unchanged.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. `python scripts/browser_review.py` passed 1021/1021 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.basic-css-cleanup-review.log`). No new tests added for this cleanup.
- Next step: review the simplified source with a learner. Manual visual, keyboard-only,
  screen-reader and cross-browser checks have not been rerun for this revision.

## Shared classic footer for Basic and Advanced (3 November 2026)

- Left-aligned the Sitemap title while retaining centred column groups and
  vertically stacked, centred sublinks. Moved all Basic footer layout rules into
  the shared CSS generator and consolidated both modes into one HTML template.
- Advanced now uses the same brand/navigation row, visible sitemap and bottom
  copyright/Back to top row. Retained its own navigation, tagline, copyright and
  complete planning map; Basic retains its filtered three-group map. Removed
  Advanced's Explore heading, redundant Sitemap shortcut and closed disclosure.
- Updated affected asset versions, README/architecture notes and browser
  assertions for visible maps, left-aligned titles and centred link groups in
  both modes across widths/themes and edited design-system settings.
- `python scripts/check_structure.py` passed (38 assets); `git diff --check`
  and Python compilation passed. Initial browser run passed 1016/1021: three
  stale Advanced footer selectors and two colour-dialog focus assertions failed.
  Corrected selectors; focus assertions passed on rerun without product changes.
  Final `python scripts/browser_review.py` passed 1021/1021 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.shared-classic-footer-review.log`). One fewer check reflects removing the
  redundant Advanced Sitemap shortcut navigation test.
- Next step: review the shared footer; watch for intermittent dialog-focus test
  failures. Manual visual, keyboard-only, screen-reader
  and cross-browser reviews have not been rerun for this revision.

## Centred links within Basic sitemap groups (3 November 2026)

- Centred each group heading and its vertically stacked child links within the
  existing centred sitemap columns. Basic-only styling; refreshed its JS query
  version and updated architecture notes and existing alignment assertions.
- `python scripts/check_structure.py` passed (38 assets), Python compilation
  and `git diff --check` passed. `python scripts/browser_review.py` passed
  1022/1022 with no interaction JavaScript errors using isolated Chrome outside
  the sandbox (ignored log: `.basic-footer-links-centred-review.log`).
- Next step: review the updated footer. Manual visual,
  accessibility and cross-browser reviews have not been rerun for this revision.

## Centred Basic footer sitemap (3 November 2026)

- Centred the Sitemap heading and constrained its responsive column grid to
  48rem with automatic inline margins. Groups are centred within their tracks;
  sublinks retain left alignment and vertical stacking.
- Scoped changes to Basic, refreshed its JS query version, documented the
  layout and added geometry/style assertions across existing themes and widths.
- `python scripts/check_structure.py` passed (38 assets) and `git diff --check`
  passed. `python scripts/browser_review.py` passed 1022/1022 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.basic-footer-centred-review.log`). Python compilation also passed.
- Next step: review the centred footer. Manual visual/accessibility and
  cross-browser checks have not been rerun for this revision.

## Basic footer navigation and sitemap columns (3 November 2026)

- Added labelled main footer navigation beside the project brand/tagline,
  reusing Home, Components, Layouts and Forms from the header generator.
  The identity/navigation row stacks at the saved responsive cutoff.
- Sitemap parent groups use responsive Grid columns; each parent's sublinks
  stack vertically and align left. Retained the filtered three-group sitemap,
  stable destinations, copyright and Back to top.
- Scoped layout changes to Basic, refreshed both affected JS asset versions,
  and updated README/architecture descriptions. Root snapshots and the user's
  webd-UI-scope.md remain untouched.
- Updated browser assertions for navigation destinations/position, horizontal
  desktop parent columns and vertical sublinks across themes and screen widths.
  `python scripts/check_structure.py` passed (38 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed 1022/1022 using an isolated
  temporary Chrome profile outside the sandbox, with no interaction JavaScript
  errors (ignored log: `.basic-footer-columns-review.log`). Python compilation
  and final `git diff --check` passed too.
- Next step: review the revised footer with a learner. Manual visual,
  keyboard-only, screen-reader and cross-browser checks were not rerun for this
  revision; automated geometry checks do not establish full accessibility.

## Basic UI essentials showcase (3 November 2026)

- Implemented the agreed scope (also read the user-owned webd-UI-scope.md,
  left untouched): semantic header/nav/main/section/article/aside/footer,
  two-CTA hero, captioned image, content card, Grid card collection, Flexbox
  profile row, article/sidebar layout, ul/ol/dl, form controls and native FAQ.
  Kept the page compact with component labels and short explanations rather
  than long code recipes. Advanced's page and user root snapshots are unchanged.
- Reused four main sections and stable destinations; labels are now Home,
  Components, Layouts and Forms. Footer remains a single three-group navigation
  with horizontal/wrapping child links and no Home/Footer groups or duplicate
  Explore menu. Default inventory has sixteen entries; footer has fourteen.
- Added a fieldset/legend radio group with two labelled choices and one default,
  retaining native validation, labelled inputs/select/textarea, required demo
  checkbox and role=status feedback. FAQ moved into its component article.
  Existing preview capture/restore preserves radio and FAQ/control state.
- Added current mock-inventory migration alongside older complete inventories
  and expanded aliases, preserving stored planning data and old fixed-ID links.
  Refreshed four affected JS query versions, inspector labels/help and docs.
- Extended browser regression checks for component content, semantic grouping,
  radio defaults/state, responsive layouts, footer depth, and mock-plan migration.
  `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed, `python -m py_compile scripts/browser_review.py` passed.
- Browser review uses an isolated temporary Chrome profile outside the sandbox;
  the normal approval path accepted this session's runs. Initial run passed
  1020/1022 with no JavaScript errors. Corrected old assertions expecting
  aria-label rather than the existing aria-labelledby footer name, prohibiting
  the now-valid Form controls link text, and expecting four H2s instead of the
  hero H1 plus three section H2s. The intermediate rerun passed 1021/1022.
  Final `python scripts/browser_review.py` passed 1022/1022 with no interaction
  JavaScript errors (ignored log: `.basic-ui-essentials-review.log`). Structure
  verification, Python compilation and `git diff --check` also passed again.
- Visually inspected eight generated-page screenshots: light desktop hero,
  Components, Layouts, Forms and footer; dark 390px Components/footer; light
  320px form/footer. No clipping observed; parent/child footer links wrap and
  controls remain readable. Removed temporary screenshots after review.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks remain
  unrun; automated checks do not establish full accessibility.
- Next step: review with a first-course learner and complete the manual checks above.

## Basic footer navigation limited to three groups (3 November 2026)

- Consolidated Basic's footer into one navigation block: Services (Website design,
  Content planning, Responsive websites), Resources (Project checklist, How we
  work, Useful terms) and Contact (Enquiry form, Common questions). Removed
  duplicate Explore navigation and Home/Footer sitemap groups. Kept identity,
  copyright, Back to top and horizontal/wrapping parent/child link layout.
- Added a parentIds rendering allowlist to the shared helper. Basic passes fixed
  Services/Resources/Contact target IDs; aliases still resolve safely, orphaned
  children are not promoted, and planning data/Advanced/header navigation remain
  intact. Refreshed three affected JavaScript query versions and docs.
- Updated browser expectations for the single navigation block, eleven rendered
  links, filtered custom/legacy maps and fallback brand navigation for empty maps.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed, `python -m py_compile scripts/browser_review.py`
  passed. Static source review confirmed exact group/child labels and a single
  footer nav with no Explore/Home/Footer groups; log is ignored
  `.basic-footer-groups-static.log`. These checks do not execute browser output.
- `python scripts/browser_review.py` was attempted, but sandboxed Chrome failed
  to start (GPU/access denied); no browser assertions ran. Earlier automatic
  approval-review usage-limit block has not been bypassed. Manual visual,
  accessibility and cross-browser checks remain unrun for this revision.
- Next step: inspect Basic footer and rerun the browser suite in working Chrome.

## Horizontal Basic footer navigation (3 November 2026)

- Changed Basic's footer Explore list from Grid to a horizontal, wrapping Flexbox
  row with shared spacing. Main links stay keyboard accessible and wrap on narrow
  screens. Refreshed the Basic generator asset query version and extended existing
  footer checks to assert row direction and wrapping.
- Inspected the active test.html snapshot and its companion tokens.css: its
  sample-nav is already horizontal Flexbox, so neither snapshot needed editing.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. `python scripts/browser_review.py` was attempted but sandboxed Chrome
  could not start (GPU process/access denied); no browser assertions ran. The
  earlier automatic approval-review usage-limit block is documented below and
  has not been bypassed. No manual visual/accessibility review was run.
- Next step: review the footer in a working browser and rerun the browser suite.

## Basic mock studio site (3 November 2026)

- Replaced Basic's tutorial/exercise copy and all code blocks with a short mock
  studio site: Home, Services, Resources and Contact. Retained semantic header,
  main, headed sections, articles, related aside, native hamburger/FAQ, two-CTA
  hero, Flexbox services, Grid resources and article/sidebar layout. Source
  comments and the inspector remain useful for beginners. Removed unused
  tutorial-specific styling and the example formatter helper.
- Retained the classic footer with shared main navigation. Expanded its default
  sitemap to thirteen parent/child links: Services and Resources have three
  children each, Contact has Enquiry form and Common questions. Home and Footer
  remain standalone even if a custom plan assigns children. Children remain
  horizontal/wrapping beneath their parent. Added a standaloneIds render option.
- Added stable contact-form ID; kept earlier content/control/FAQ IDs. Added
  current tutorial inventory migration alongside the prior workshop migration,
  preserving stored planning text and legacy destination aliases. Contact's
  real copy replaces technical field labels; static-demo notice and safe native
  validation remain. Preview feedback says no message was sent.
- Updated browser regression expectations for mock content, lack of on-page
  recipes, sitemap depth/grouping, legacy inventories, semantic layout and form
  state. Refreshed affected JS query versions, inspector labels/help and docs.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed; `python -m py_compile scripts/browser_review.py`
  passed. A read-only `python -` static review passed five checks: balanced mock
  HTML/semantic landmarks, unique IDs and static label/ARIA/link references,
  navigation/inventory targets, child counts 0/3/3/2/0, and absence of page
  tutorial recipes. This inspects templates, not executed browser output; log is
  ignored `.basic-mock-static-review.log`. `python scripts/browser_review.py` was attempted
  inside the sandbox but Chrome failed to start (GPU process/access-denied).
  No browser assertions ran for this revision. The previous turn's final
  escalated rerun was not executed: automatic approval review hit the account
  usage limit, not an unsafe-action determination. That check has not been
  bypassed. Current browser/visual/accessibility/cross-browser checks remain
  unverified; historical pass counts below do not establish this revision.
- Previous expanded-sitemap screenshots were inspected in the prior turn before
  its blocked final rerun, and are now obsolete for this copy change. Temporary
  screenshots are removed. No commits, deployments or new runtime dependencies.
- Next step: run `python scripts/browser_review.py` in a working local Chrome
  environment once approval review is available, and inspect light/dark layouts.

## Expanded sitemap and semantic HTML (3 November 2026)

- Expanded Basic's visible footer sitemap from five top-level links to eleven
  parent/child links for the default plan. Parent groups and their nested child
  lists use horizontal wrapping Flexbox rows. The classic Explore navigation,
  copyright and Back to top remain. The Architecture plan's existing filtering
  and layout are unchanged.
- Added a linksOnly sitemap rendering option: includes known children under
  known parents, omits unlinked planned entries and never promotes orphan
  children. Original planning data, aliases, custom/empty plans and Advanced's
  complete map behaviour remain intact. Existing top-level-only option remains.
- Reviewed and clarified the semantic tutorial: headed section for a topic,
  article for independent content, aside for related information, and div for
  layout wrappers. Expanded the existing escaped HTML example to include nav,
  article and aside; used a labelled article beside the labelled sidebar aside.
  Kept Flexbox/Grid independent of semantic element choice and all four main
  sections, stable destinations, native controls and shared design settings.
- Updated old footer-depth assertions and added both-theme child-row geometry
  checks at 320/390/768/1440px, semantic structure checks and mixed valid/unknown
  child filtering coverage. Refreshed three affected runtime query versions and
  updated README/architecture.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. Initial full browser run passed 1019/1020 with no JavaScript errors.
  Its remaining old assertion expected every article under Grid to be a list
  card with an h3; scoped that check to the three list cards, leaving the new
  independent sidebar article correctly headed by h4. Final rerun/visual review
  pending. Desktop/light and 390px dark expanded-footer screenshots and the
  semantic lesson screenshot were inspected, but the final escalated rerun was
  rejected by automatic approval review's account usage limit and did not run.
  That tutorial revision is superseded by the mock-site changes above.
- Next step: see the current mock-site objective and its verification gap.

## Classic Basic footer and common UI patterns (3 November 2026)

- Restored a classic footer using Advanced's shared identity/navigation Grid:
  project identity, an Explore column with Hero/Flexbox/Grid & lists/Forms and
  Sitemap, then copyright and Back to top. Kept Basic's visible top-level
  sitemap and its separate Architecture-plan view filtering. Header, mobile
  menu and footer main links now share one safe authored navigation helper.
- Added live examples to existing Flexbox lesson cards: content card with a
  text link, avatar/text media object with a badge, and native FAQ disclosure.
  Added a main-content/sidebar Grid example below the list cards, stacking in
  source order at the saved cutoff. Kept the four main sections and plan IDs.
- Added optional labelled select/textarea controls to the native-validation
  practice form. New components use semantic roles, spacing and shared control
  styles. FAQ and optional control state survive live preview edits. Added one
  CSS recipe (nine examples total) and one practice task (six total).
- Added regression coverage for matching header/footer links, classic footer
  geometry, UI/sidebar containment across widths/themes, native FAQ/focus and
  preservation of FAQ/select/textarea state. Updated previous code/task counts.
  Refreshed affected runtime query versions, sample help and docs.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **1010/1010** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; ignored log `.basic-classic-components-review.log`.
  Initial full browser run passed 1008/1009 with no
  JavaScript errors; every new footer/component check passed. The existing
  colour-repair focus assertion intermittently fell back to the contrast summary.
  Review also identified that HTML indentation could insert spaces into an empty
  textarea. Protected textarea blocks alongside preformatted code and added an
  empty default-value regression assertion. The final browser rerun passed
  every check, including the existing focus assertion.
- Captured and inspected desktop/light footer/profile/FAQ/sidebar and exact-390px
  dark footer/form plus light sidebar screenshots. Layouts and controls fit;
  sidebar stacks below content. Manual keyboard-only, screen-reader, zoom and
  Firefox/Safari review remain unrun; automated checks do not establish full
  accessibility. Removed the temporary screenshots after inspection; no visual
  baselines added. No commits, deployments, new dependencies or root snapshots.
- Next step: try the beginner component examples and complete manual
  accessibility/cross-browser review.

## Basic sitemap plan groups (3 November 2026)

- Added a render-only filter to the Basic Architecture artifact: hides Forms
  and Footer parent groups, including case/spacing/hyphen variations and legacy
  Sign up/Signup aliases. Other groups retain their related second-level items.
  Child labels are not independently hidden. Empty/fully filtered plans have
  clear messages. All labels continue to be escaped.
- Scoped Flexbox styling to process-map--basic: parent groups flow left to right,
  related children sit below aligned to the same left edge, and groups wrap on
  narrow screens. Advanced's tree remains unchanged. Full editable/saved plans,
  generated page sections and Basic footer links are preserved.
- Updated former full-render count assumptions and added both-theme geometry
  checks at 320/768/1440px, alias/child/data preservation checks and a fully hidden
  plan case. Refreshed the affected JavaScript asset query version and architecture.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **998/998** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; log is ignored `.basic-plan-columns-review.log`.
  First full browser run passed 991/998 with no JavaScript errors:
  six new assertions incorrectly assumed stored default planning data had already
  been rewritten to Basic labels (resolution is intentionally pure). Corrected
  them to check the resolved editor and unchanged stored data. One existing
  contrast-review focus assertion also failed intermittently; the final run
  passed that check and all 998 assertions.
- Inspected desktop/light and exact-390px dark screenshots: three aligned groups
  on desktop, related items beneath each heading, and wrapping on phones. Manual
  keyboard-only, screen-reader and Firefox/Safari checks remain unrun. Earlier
  results below belong to earlier work. Temporary screenshots were removed;
  no visual baselines were added.
- Next step: review the Basic plan layout with a real project and complete
  manual accessibility/cross-browser checks.

## Studio light background shade (3 November 2026)

- Changed the studio body canvas from the shared light background #F3F6FA to
  a dedicated --studio-background token, #E8EDF3, for stronger separation from
  white panels. Dark mode continues to follow the existing --background role.
  Generated website backgrounds, semantic overrides, project data and exports
  retain their existing behaviour. Refreshed the base CSS asset query version.
- Final verification: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **990/990** with no JavaScript errors,
  and `git diff --check` passed. A focused isolated Chrome check passed 3/3:
  exact light canvas, retained dark canvas, and independent custom website
  backgrounds in preview/export. Logs are ignored `.studio-background-review.log`
  and `.studio-background-focused.log`. No new permanent tests were added for
  this small visual change.
- Manual visual, keyboard, screen-reader and cross-browser review were not run
  for this change; previous results below are historical.
- Next step: review the new studio shade visually.

## Basic top-level sitemap links (3 November 2026)

- Added an explicit topLevelLinksOnly rendering option to the shared sitemap
  helper. Basic uses it to render only known linked parent entries from the
  current Architecture plan; nested children and unlinked planned entries are
  omitted, and children are never promoted. Empty and wholly unlinked plans
  retain clear empty states. Imported labels still resolve only to fixed IDs.
- Changed Basic's sitemap to a compact wrapping link row and adjusted its tutorial
  copy. The default sample shows Hero, Flexbox, Grid & lists, Forms and Footer.
  The complete two-level plan, centre Architecture lesson, local/JSON project
  data and Advanced's default full sitemap remain intact. Existing aliases work.
- Updated regression checks for the rendered depth, legacy/custom plans,
  unknown/malicious labels, restoration, JSON round trips and exports. Added
  explicit checks that the shared full Basic map retains eleven entries while
  the footer shows five and that filtering never promotes a known child of an
  unknown parent. Refreshed three affected runtime query versions and docs.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **990/990** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; output is in ignored
  `.basic-sitemap-filter-review.log`.
- Manual visual, keyboard-only, screen-reader and Firefox/Safari checks were not
  run for this change; earlier screenshots/results below belong to earlier work.
- Next step: review the simplified footer in Basic and complete manual
  accessibility/cross-browser checks.

## Basic component tutorial and visible footer sitemap (3 November 2026)

- Replaced workshop/promotional copy with component-specific lessons: Hero and
  header navigation, semantic HTML, Flexbox rows/columns, native responsive menu,
  CSS Grid, ul/ol/dl lists, and form labels/validation. Renamed navigation and
  CTA labels to match the components they reach. Kept the four-section structure,
  stable IDs, shared settings, native menu, illustration and paired section CTAs.
- Added eight escaped HTML/CSS code examples plus concrete practice tasks.
  Protected preformatted examples during HTML indentation, keeping their code
  whitespace and rendering markup as text. Examples preserve source whitespace and
  scroll locally with keyboard focus, keeping code identifiers intact.
  Native form tutorial requests sample data, explains exported GET behaviour and
  uses a practice acknowledgement rather than marketing consent. Preview success
  feedback describes validation; no processing backend or script was added.
- Replaced Basic's three-column promotional footer/Explore menu/dropdown with
  a compact identity/lesson row, one always-visible grouped sitemap and a utility
  row (Start again, Sitemap, Back to top). Uses shared safe sitemap generation;
  Basic-specific markup/style is separate from Advanced's existing presentation.
- Updated Basic's content inventory to tutorial labels, preserving old section
  and lesson labels as safe aliases. Exact previous complete Basic inventories
  resolve to the tutorial inventory without modifying saved planning data;
  custom and empty plans retain their established behaviour.
- Added browser regression coverage for tutorial headings/tasks, exact code
  example text/whitespace, inert escaped markup, visible footer navigation,
  preformatted-code containment, old complete-plan migration and custom aliases.
  Updated former Basic disclosure/footer geometry assertions while retaining
  Advanced native disclosure checks and shared foundation parity checks.
- Refreshed affected runtime asset query versions, inspector help, README and
  architecture. Final required checks: `python scripts/check_structure.py`
  passed (38 assets), `python scripts/browser_review.py` passed **988/988**
  with no JavaScript errors, and `git diff --check` passed. Chrome used isolated
  temporary profiles outside the sandbox. Logs are ignored
  `.basic-tutorial-review.log`, `.basic-tutorial-focus.log` and
  `.basic-tutorial-scroll.log`. First full browser run passed 985/986, including
  all tutorial/footer/compatibility checks, with no JavaScript errors. One
  existing colour-repair focus assertion failed in both full runs. A focused
  diagnostic rerun passed 143/143 with no JavaScript errors. Updated that test
  to await the native dialog close event (with a bounded timeout) before checking
  restored focus and added failure details. The next full run passed 986/986
  with no JavaScript errors. The first code-scrolling refinement run passed
  975/988: unwrapped form code exposed an auto-sized centred introduction wider
  than its narrow Grid track. Constrained the introduction to width:100% within
  its existing reading measure. A focused isolated Chrome check passed 3/3 at
  320/390/1440px, confirming no overflowing elements and working focused local
  code scrolling. Final expanded full run passed all 988 checks.
- Inspected desktop/light header/hero/Flexbox/Grid/footer and exact 320px light
  Grid plus 390px dark hero/form/footer screenshots. Visual review found an old
  decorative caption number wrapping vertically; removed it. Kept practice text
  left aligned. A final narrow screenshot showed natural hyphen breaks still
  split code identifiers, so switched code examples to preserved whitespace with
  keyboard-accessible local horizontal scrolling. Inspected the final 320px
  code-scrolling screenshot and corrected 390px dark caption/form screenshots.
  Added focus/scroll assertions in both themes. Also inspected the corrected
  320px dark form after its width fix. Removed all temporary screenshots after
  review; no visual baselines were added. Manual keyboard-only, screen-reader,
  zoom and Firefox/Safari checks
  remain unrun, so the suite does not establish full accessibility. Earlier results
  below belong to previous work; no commits/deployments or root snapshots changed.
- Next step: walk through the beginner exercises with a learner and complete
  manual accessibility/cross-browser review.

## Basic website structure review (3 November 2026)

- Reviewed the current generated Basic page against the requested structure.
  The existing illustrated hero already has two shared primary/secondary CTAs,
  and the footer already links to its expandable Architecture-driven sitemap.
- Added Basic's native details/summary hamburger with hamburger/close icons,
  visible Menu label and 48px control. Desktop and mobile links come from one
  fixed list. The saved stacking cutoff selects desktop/mobile navigation;
  exported pages need no scripts. The preview preserves menu state on live edits.
- Converted the whole Skills section to Flexbox, including the 5:7 introduction
  and vertically stacked lesson cards. Renamed feature-grid to skill-cards so
  the source reflects the layout being taught. Narrow screens stack both areas.
- Simplified Toolkit to equal-width auto-fit Grid cards using the saved card
  minimum and gap, removing the asymmetric first-card span and nested sizing
  expression. Retained stable IDs, list semantics, all section CTAs, illustration,
  demo form, shared tokens/components, footer structure and exports.
- Updated the inspector guide, section labels, sample help, README and architecture
  to describe Header navigation, Skills Flexbox and Toolkit Grid. Refreshed the
  affected Basic generator query version. Fixed teaching HTML indentation to
  recognise self-closing SVG paths introduced by the hamburger icon.
- Added browser coverage for native menu open/close, visible/hidden navigation,
  focus outline, target sizes and icon states in both themes at 320/390/768/1440px;
  preview navigation and retained open state; actual Flexbox-only Skills styles;
  equal-width Grid cards; standalone footer Sitemap navigation and disclosure.
  Updated prior Grid-based Skills assumptions and hidden-nav target-size checks.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **980/980** with no JavaScript errors,
  and `git diff --check` passed. Chrome used an isolated temporary profile outside
  the sandbox; output is in ignored `.basic-structure-review.log`. The initial
  run passed 956/980; corrected obsolete asymmetric Grid/visible-nav test
  assumptions and restored the palette after the new live-menu test. The next
  run passed 975/980, including every Basic check, but existing sticky-header
  assertions measured stale ResizeObserver offsets. A rendering-frame wait
  stalled under headless virtual time, so replaced it with explicit resize-event
  delivery after layout before the existing geometry assertions. No studio
  runtime change was needed. The final rerun passed all 980 checks.
- Captured and inspected temporary desktop/light header/hero/Skills/Grid toolkit
  and exact-390px dark open-menu/footer screenshots. Removed temporary screenshots
  after review; no visual baselines were added. Manual keyboard-only, screen-reader, zoom and
  Firefox/Safari review have not been run; automated checks do not establish full
  accessibility. No commits, deployments, new dependencies or user root sample
  snapshots changed. Earlier results below belong to earlier work.
- Next step: try the Basic learning exercises and complete manual accessibility
  and Firefox/Safari review.

## Basic inspector learning guide (3 November 2026)

- Added a Basic-only Start here disclosure with three concrete exercises:
  edit the downloaded H1, change the live spacing unit, and compare the
  390/768/1280 px preview presets. Explicitly identifies the inspector as
  read-only and distinguishes downloaded edits from the generated live preview.
- Explained spacing custom properties and the progression from normal flow to
  Header Flexbox and Hero Grid, with Toolkit as an optional Grid challenge.
- Added authored SECTION comments to Basic HTML/CSS, indented generated HTML
  (including formerly compact cards, lists, forms and shared footer markup),
  and expanded page/footer CSS declarations onto separate lines. Shared design
  system foundations and the existing section compositions are preserved.
- Added a transient Basic section filter for Page basics, Header, Hero, Skills,
  Toolkit, Form and Footer. CSS excerpts include shared page/responsive rules
  and explain their dependency on complete tokens.css. Page basics includes live
  spacing token definitions so the spacing exercise shows the changed base value.
  Copy copies the visible excerpt; inspector/Deliver downloads always save the complete selected file.
  Advanced hides the learning controls and retains complete code. Async copy
  feedback checks the selected section as well as language/sample mode.
- Kept the selector visible below the scrolling guide. Stacked docks now grow
  with controls and use a bounded code viewport, avoiding clipped controls.
  Refreshed all three affected asset query versions; documented the architecture.
- Final required checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **958/958** with no JavaScript
  errors, and `git diff --check` passed. Output is captured in ignored
  `.basic-learning-review.log`. First sandboxed Chrome attempt could not start;
  isolated-profile reruns outside the sandbox worked. The first full run was
  950/952: corrected a viewport-dependent spacing test assumption and a wrong
  test-only JSON function name. A subsequent 957/958 run exposed one test
  expecting a resolved spacing value instead of the exported calc() expression;
  corrected that assertion. The next 957/958 run passed every new check but
  intermittently failed the existing contrast-review focus assertion, which
  passed in earlier runs. The unchanged final rerun passed it and all 958
  checks; the intermittent focus-check failure remains recorded for follow-up.
- Captured and inspected temporary desktop/light and exact-390px iframe/dark
  screenshots with the guide expanded and Hero/HTML selected. Visual review
  prompted the guide/selector scrolling correction. Removed the temporary
  screenshots after inspecting the corrected layouts; no screenshot baselines.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain
  unrun; automated checks do not establish full accessibility. No runtime
  dependencies, commits, deployments or user root sample snapshots changed.
- Next step: try the exercises with a beginner and complete manual accessibility
  and cross-browser review; monitor the existing intermittent focus assertion.

## Basic section and footer layouts (3 November 2026)

- Replaced repetitive section grids with a framed/captioned two-column hero,
  a 5:7 editorial skills layout beside three stacked lessons, an asymmetric
  toolkit with a two-row checklist beside workflow/terms panels, and a centred
  sign-up introduction/form limited by the saved reading measure.
- Layouts use the existing semantic roles, spacing, card appearance, grid gap,
  card alignment and responsive cutoff. The toolkit also respects the saved
  minimum card width. Retained all four main sections, stable content IDs,
  primary/secondary CTAs, native validation and the offline illustration.
- Redesigned only Basic's footer presentation: logo/project identity, vertical
  shortcuts and a suggested next-step column; a separate bordered expandable
  sitemap; copyright and Back to top below. Mobile stacks the areas and uses
  two-column shortcuts. Shared footer generation/sitemap validation remain;
  Advanced keeps its existing two-column presentation.
- Updated sample help, README, architecture and affected asset query versions.
  Updated former three-column assumptions in browser checks, added section/footer
  geometry coverage in both themes at 320/390/768/1440 px, and assertions that
  form width follows default and edited/imported reading measure. Existing tests
  continue to cover wizard/preview/inspector/export parity and sitemap behaviour.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed. Initial expanded `python scripts/browser_review.py`
  passed **915/915**, with no JavaScript errors. Visual review then exposed an
  undefined form-width token; corrected it to `--reading-measure`, added explicit
  form-width checks. The next run passed 915/919 with no JavaScript errors; the
  four new assertions accidentally compared the form to small eyebrow text, so
  their `ch` values used different font metrics. A focused isolated Chrome check
  confirmed the correct form token/width. Corrected the selector to compare body
  text. Final full rerun passed **919/919**, with no JavaScript errors, captured
  in ignored `.basic-layout-review.log`. All three required checks passed. Chrome
  used an isolated temporary profile outside the sandbox, with no access to the
  user's saved projects.
- Captured and inspected temporary light desktop hero/skills/toolkit/footer and
  exact-390px dark sign-up/footer screenshots, including refreshed screenshots
  after the form-width correction. Removed temporary screenshot/diagnostic helpers
  and artifacts; no visual baselines were added.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review were not
  run; automated tests do not establish full accessibility. No commits,
  deployments, runtime dependencies or user root sample snapshots changed.
- Next step: try the revised layouts with a real project and complete manual
  accessibility/cross-browser review.

## Basic page engagement and sitemap feedback (3 November 2026)

- Reworked the existing four sections around a beginner website workshop:
  an outcome-led hero, three practical skill cards, a project toolkit and a
  clearly labelled demo sign-up. Retained existing IDs, inventories, native form
  validation, offline illustration and the shared foundation/component generator.
- Added primary/secondary CTA pairs to all four sections, contextual fragment
  destinations and direct links from skill cards to toolkit cards. Shared button
  classes retain wizard variant colours, size, dimensions and mobile width.
  Action rows wrap with the defined spacing tokens; the form status is announced.
- Investigated the reported sitemap button: the existing handler restored custom
  and empty plans in the prior browser suite, but had no visible feedback when
  the map already matched and the footer remained collapsed. Added applied versus
  already-complete confirmation, section/topic counts, expansion of the centre
  map and a review link. Feedback clears after plan/sample changes. The action
  changes the plan, while existing content destinations remain fixed and safe.
- Added browser coverage for every CTA destination, primary/secondary settings
  in both themes, mobile full-width/focus, row spacing/containment, and sitemap
  restoration/repeated clicks/feedback in both modes. Existing tests cover live
  typography, grid, shared foundations, copy/downloads, forms, storage and exports.
- Current checks: `python scripts/check_structure.py` passed (38 assets) and
  `git diff --check` passed. The first `python scripts/browser_review.py` run
  encountered Windows console encoding while printing a CTA arrow in a test
  name. Changed test names to use ASCII destination IDs. Final expanded suite
  passed **899/899**, with no captured JavaScript errors, outside the sandbox
  using an isolated temporary Chrome profile. Output is captured in ignored
  `.basic-engagement-review.log`. All three required checks passed.
- Captured and inspected temporary desktop/light and exact-390px mobile/light
  hero screenshots plus dark mobile toolkit/sign-up screenshots. Visual review
  caught an undefined action-gap token; corrected it and added a computed-gap
  assertion. Removed the temporary screenshot helper and artifacts afterward;
  no visual baselines were added.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks were not
  run; automated tests do not establish full accessibility. No commits,
  deployments, runtime dependencies or root sample snapshots changed.
- Next step: try the revised Basic journey with a real project and complete
  manual accessibility/cross-browser checks.

## Responsive preview cleanup (3 November 2026)

- Removed `See the system working together` from the preview's generated lesson
  list and `Download this responsive website` from the preview markup. The live
  viewport now follows the theme/width controls. Other centre lessons remain.
- Removed the card's unused stylesheet, code-shortcut handlers, status-node update
  and sample-description update. Inspector/Deliver downloads still use the same
  generators; generated sample pages and saved project data are unchanged.
- Refreshed affected JavaScript query versions, updated README/architecture notes
  and adjusted browser coverage for fifteen lessons plus the preview, absence of
  the removed sections and retained download behaviour.
- Current checks: `python scripts/check_structure.py` passed (38 assets);
  `git diff --check` passed. The first `python scripts/browser_review.py` attempt
  failed because the sandbox blocked access to Chrome's temporary profile.
  The first full run outside the sandbox passed 866/867 with no JavaScript
  errors; its remaining assertion referenced the removed sample-description node.
  Updated that obsolete assertion; final full rerun passed **867/867**, with no
  JavaScript errors, using the isolated-profile harness. Output is captured in
  ignored `.preview-cleanup-review.log`. All three required checks passed.
- Manual visual, keyboard, screen-reader and cross-browser checks were not run;
  automated checks do not establish full accessibility. Earlier results below
  belong to prior sessions. No commits, deployments or root snapshots changed.
- Next step: review the simplified preview in the UI and complete manual checks.

## Completed in this session

- Reviewed all 13 current JavaScript modules, relevant CSS/HTML, repository
  checks, architecture and publishing workflows.
- Added `AGENTS.md` and this handoff file for progress across sessions/computers.
- Fixed OKLCH conversion unnecessarily reducing valid saturated colours because
  of floating-point error at the sRGB boundary; wheel warnings share the tolerance.
- Validated browser-local library entries so a damaged entry cannot interrupt
  startup or prevent recovery of other valid projects.
- Corrected responsive specimen font sizes to include container padding/border
  when translating content-box `cqi` measurements into device viewport widths.
- Expanded browser checks for OKLCH, preview/readout agreement, exports, library
  operations, malformed storage, actual file-input imports, clipboard failure,
  advanced states and editor round trips. Made CSS transition measurements
  deterministic under Chrome's virtual clock and included failure details.

See `docs/AUDIT_BASELINE_2026-10-19.md` for evidence and remaining coverage gaps.

## Inspector feature completed

- Added CSS/HTML language tabs, keyboard navigation and matching copy/download
  actions to the live inspector, keeping the centre export tabs independent.
- Replaced exported `--example-*` fixed reference colours with `--brand-*`, including
  token catalogue descriptions and CSV exports. Reference values remain fixed.
- Added the registered `sample-homepage` module: a responsive header/navigation,
  hero, about image, services, resource table, FAQs, sample form, footer and broad
  component gallery, all using the shared CSS and selected settings.
- Embedded two palette-coloured SVG illustrations, so exported `index.html` only
  needs its companion `tokens.css`. The static enquiry form has no delivery backend.
- Removed the button module's old HTML append wrapper; the full page now renders
  selected button size, mobile full-width and interaction state itself.
- Reviewed desktop, 390px mobile, dark-theme and HTML-inspector screenshots in
  isolated headless Chrome profiles. No screenshot comparison baseline was added.

## Verification

- `python scripts/check_structure.py`: 30 referenced assets verified.
- `python scripts/browser_review.py`: **544/544 passed** in headless Chrome on
  Windows; no captured startup or interaction JavaScript errors.
- `python scripts/button_states_review.py`: **12/12 passed** (5 reduced-motion,
  7 forced-colour checks), repeated against the Web Design Field Guide sample.
- `python scripts/font_cdn_review.py`: **9/9 passed** using real Google font
  stylesheet/font downloads and standalone exported HTML, repeated for the field guide.
- `git diff --check`: passed.

## Themes and linked responsive preview completed

- Added inspector/preview Page theme selectors sharing the existing saved
  `state.theme`; global toggles, guided controls, import and reset stay synchronized.
- Moved the responsive preview to the first centre-pane position, open by default
  in Fluid mode. Updated displayed section/nav numbering while preserving IDs.
- Added the registered `responsive-preview` module after the sample generator.
  Its iframe renders the actual generated page at Fluid/375/768/1280 px, using
  exported viewport typography and media queries rather than a separate demo.
- Batched preview updates; retained scroll, user-entered form values, choices,
  open FAQs and focus during live changes. Navigation stays in the sample and
  sample submission is intercepted after native validation without sending data.
- Replaced the old cqi preview styling with iframe layout and viewport readouts.
  Exported files and illustration generation continue to use their existing sources.
- Verified real iframe viewport sizes and reflow, theme persistence, preview/export
  agreement, navigation, retained browsing state and safe CSS text insertion.
- Visually reviewed top Fluid preview, dark phone preview and narrow studio UI
  screenshots. User-created `test.html` and `tokens.css` were left untouched.

## Responsive hamburger completed

- Added native `details`/`summary` mobile navigation at 48rem/768 px and below,
  with desktop navigation generated from the same link array.
- Embedded hamburger and close SVG paths use `currentColor` tied to `--accent`,
  with a minimum 44 px control. No CDN or scripts are needed.
- Both the downloaded sample and live preview support opening/closing the menu.
  The preview preserves its open state through accent/theme changes, and menu
  links use the existing in-preview section navigation.
- Added regression checks for both themes at 320/768/1440 px, actual closed/open
  navigation visibility, focusability, live colours and long project names.
- Visually reviewed exported mobile closed/open, dark open and desktop headers.
  User-created `test.html` and `tokens.css` remain untouched; fresh inspector
  downloads include the header changes.

## Header logo and title completed

- Replaced the decorative diamond with a square “Logo” placeholder beside the
  project name. The placeholder is decorative to assistive technology; the
  project name remains the brand link's accessible name.
- Logo dimensions/text scale with viewport width; colours follow primary/on-primary
  roles and corners use the shared radius. The title uses H2 size, heading leading,
  weight and tracking, with wrapping that preserves space for the mobile menu.
- Verified both themes at 320/768/1440 px, contained logo text, long-name wrapping,
  live project-title updates and heading-scale changes. All 237 browser checks pass.
- User-created `test.html` and `tokens.css` remain untouched. Fresh HTML/CSS
  downloads include the updated header.

## Mobile menu style refinement completed

- Removed the toggle border and filled background. The “Menu” label now uses
  `--text`; only the hamburger/close SVG uses `--accent` in both themes.
- Preserved the native disclosure, 44 px target and standard focus outline.
- Updated existing browser checks to verify the label, icon, transparent background
  and absent border at mobile/tablet widths. No new test cases were needed.
- User-created `test.html` and `tokens.css` remain untouched; fresh exports use
  these defaults.

## Full-width studio layout completed

- Removed the 1500 px shell cap and aligned top-bar/workspace gutters.
- Fixed desktop controls at 310 px and the inspector at 380 px using studio-only
  CSS properties; the centre absorbs the remaining width, including ultrawide screens.
- Kept desktop sticky panes. The inspector stacks at 1280 px and below; all panes
  stack at 900 px and below. Generated sample-page layout is unaffected.
- Verified pane widths, complete centre expansion and no horizontal page overflow
  at 1281/1440/1920/2560/3440 px, plus stacking at 1280/900 px and existing mobile
  checks. All 245 browser checks pass; the structure checker verifies 23 assets.
- User-created `test.html` and `tokens.css` remain untouched.

## 390 px preview preset completed

- Changed the preview phone button, CSS dimensions and viewport/typography
  readouts from 375 to 390 px. Updated the existing exact-viewport browser checks.
- Retained 320 px checks for both the studio and generated sample. W3C's reflow
  guidance uses 320 CSS px as the narrow-width reference for vertically scrolling
  content: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html (verified this session).
- Typography's existing 375 px specimen and fluid minimum remain independent of
  the preview preset; existing project typography settings are unchanged.
- User-created `test.html` and `tokens.css` remain untouched.

## CSS/HTML generation and spacing review completed

- Confirmed the 8 px spacing / 12-column grid approach against IBM and Bootstrap
  primary documentation. It is a design convention; 4 px fine spacing remains
  useful, and font/border/focus sizes follow their own requirements.
- Added the exported spacing scale; replaced ad hoc page spacing with token steps.
  Hero/split rows use 6 + 6 spans, cards use 4 + 4 + 4, and narrow layouts collapse.
  Container queries retain the existing card minimum-width and gap controls.
- New projects use 24 px card gaps, 48 px minimum controls/buttons and 8/16 px
  button padding. Imported custom dimensions are preserved without snapping.
- Removed duplicate button overrides, corrected footer and field-label spacing,
  and fixed ordinary selects incorrectly matching read-only input styling.
- Made CSS theme export read-only, halved palette resolutions per HTML export,
  cached embedded illustration encodings, and skipped unchanged code-text updates.
- Added 16 regression checks. Final browser run: 261/261 passed, including both
  themes, grid geometry, actual spacing values, saved dimensions and six widths
  from 320 to 1440 px; no captured JavaScript errors.
- Reviewed desktop/phone headers and content, service/resource layouts, contact
  form and dark components/footer screenshots. Removed the temporary screenshot
  helper. User-created `test.html` and `tokens.css` remain untouched.
- Refreshed affected script cache versions and documented the design choices in
  `docs/GENERATION_REVIEW_2026-10-19.md`. Structure check: 23 assets; diff check passed.

## Section action pairs completed

- Added one filled primary and one outlined secondary action to each main section.
  Hero/about actions stay with their text, and services/resources/components
  actions follow section content with a token-based 24 px default gap.
- Used contextual destinations: services to contact/resources, resources to
  contact/components, and components to contact/home. Header navigation and action
  pairs together reach every main section.
- Paired the contact form's existing sample-submit action with a services link.
  Kept service-card text actions and component state demonstrations separate.
- All pairs share button colours, size and mobile full-width settings. Navigation
  remains usable when the component gallery demonstrates loading/disabled states.
- Added 21 browser checks for action hierarchy, destinations, settings, responsive
  wrapping in both themes, and all 11 actual preview anchor interactions.
  Final suite: 282/282 passed; no captured startup/interaction JavaScript errors.
- Visually reviewed desktop service actions, 390 px about/contact action pairs,
  and dark resource actions. Responsive wrapping and spacing remained consistent.
- Structure check: 23 assets; diff check passed. Updated the sample script cache
  version. User-created `test.html` and `tokens.css` remain untouched.

## Optional font sources and CDN learning completed

- Added the registered `font-sources` module and Typography studio controls for
  System/Google sources, independent heading/body families and additional weights.
  Curated Inter, Source Sans 3 and Literata metadata/API syntax were verified with
  primary Google sources. System fonts remain offline by default.
- Generated HTML now includes CDN/preconnect links in Google mode; CSS exports
  heading/body tokens and a compatible `--font-ui` alias. Specimens, component
  previews and the actual sample page share these selections.
- Validated IDs/weights on import, preserved legacy system-font projects and saved
  font settings through existing JSON/local-project flows. No imported URLs or CSS.
- Added loading/failure/retry feedback, stale-callback protection and preservation
  of managed font nodes through unrelated edits and preview HTML refreshes.
- Added a preview-only fallback toggle that leaves exports/saved settings intact,
  plus teaching examples for links, weights, swap loading, CORS and fallback stacks.
- Added 22 deterministic regressions (304/304 final suite) and the separate optional
  real-CDN check (9/9 passed, all three families plus standalone export). No captured
  JavaScript errors. Existing button-weight import validation remains in place.
- Visually reviewed real-font desktop/phone controls, teaching examples, light/dark
  sample pages and fallback comparison; no horizontal overflow in captured views.
- Updated runtime cache versions, README/contributor/security/architecture notes
  for the authorized optional font network requests. See
  `docs/FONT_SOURCES_2026-10-19.md` for state shape, references and verification.
- Structure check: 25 assets; diff check passed. User-created `test.html` and
  `tokens.css` remain untouched. No commits, pushes or deployments were made.

## Secondary custom-colour preview fix completed

- Reproduced the user's Secondary action/custom base colour issue. The live
  stylesheet was updating, but visible secondary calls to action were using the
  independently edited Outline variant. The targeted pre-fix check failed.
- Mapped all six section action pairs, including hero and contact, to the wizard's
  Primary/Secondary variants. The component gallery still demonstrates Outline.
  Secondary custom colours now appear on the corresponding page actions.
- Added nine regressions for both themes, all section pairs, repeated custom-colour
  edits without palette changes, wizard/preview agreement, primary independence
  and generated exports. Final regular suite: 313/313 passed; no captured errors.
- Re-ran actual Google font integration checks: 9/9 passed. Updated the generated
  sample's asset cache version and current README/architecture/changelog wording.
- Visually confirmed the custom secondary colour on the 390 px light hero and
  1280 px dark hero, with the primary action retaining its independent colour.
- Structure check: 25 assets; diff check passed. User-created `test.html` and
  `tokens.css` remain untouched.

## Guided button contrast review completed

- Added the registered `button-contrast` module to step 5. All five variants have
  seven selectable states and separate Light/Dark outcomes: 70 combinations.
  Per-variant counts and a live summary make required problems easy to find.
- Reused the full inventory's results through `contrast:updated`; removed the
  wizard's separate selected-sample ratio calculation. Selected details show the
  lowest audited text, focus/selection and conditional-boundary ratios. Loading
  opacity is included, and disabled controls are explicitly exempt.
- Added direct actions into the existing colour-repair dialog, including shared
  ring colours and related-effect previews before Apply. Choosing a review state
  synchronizes the variant/state selectors and specimen without changing colours.
  Applied edits use existing preview/export/project-save paths.
- Preserved review nodes and open disclosures during refreshes. Dialog Apply and
  Cancel return focus to their opener when available. No new colour schema or
  automatic changes to the user's palette were introduced.
- Added 23 browser regressions: all combinations agree with the full inventory;
  bad text, loading opacity and focus failures are detected; editing, cancellation,
  saves/imports, exports and responsive-preview CSS stay synchronized. Confirmed
  both theme layouts at 320 px and visually reviewed desktop/390 px phone views.
- Final regular suite: **336/336 passed**, with no captured startup/interaction
  errors. The harness now captures missing resources and caught module errors,
  excluding intentional failed-font fixtures. Increased its virtual-time allowance
  to 30 seconds for the expanded interaction sequence.
- Structure check: **26 assets**; diff check passed. Updated affected asset query
  versions and README/architecture/changelog guidance. User-created `test.html`
  and `tokens.css` remain untouched. No commits, pushes or deployments were made.
- This makes contrast problems reviewable and editable; custom colours can still
  be below target. Conditional boundaries and inactive exemptions are not counted
  as required failures. Browser tests do not establish full accessibility.

## Default button state best practices completed

- Added the registered `button-state-practices` module before core startup. Its
  shared CSS generator supplies studio specimens, State Explorer, component CSS
  downloads and the responsive/generated page with consistent non-colour cues.
- Default hover underlines the label; pressed states add an inset appearance;
  selected toggles show CSS-drawn checkmarks plus existing rings. Off/on export
  examples keep identical labels and reserve identical checkmark space.
- Busy examples show a progress indicator and Processing label at full opacity.
  Removed the matrix-only 0.8 opacity that could make otherwise readable defaults
  fail. Updated contrast calculations and the guided review to match. Kept native
  disabled exemptions and operable busy text checks distinct.
- Adjusted the new-project button focus colour from #B45309 to warm #B86C20, which
  meets the 3:1 target on every named light/dark host in the button inventory.
  Fresh defaults meet all required button text/focus/selection checks across both
  themes. Imported custom colours and palette anchors remain editable/preserved.
- Retained keyboard focus outlines independently of pressed cues. Added a
  forced-colour pressed outline fallback that preserves real keyboard focus.
  Progress stops for platform reduced motion and the saved Reduce demo animations
  setting; its static indicator and text remain visible.
- Added nearby disabled/busy explanations, a step-5 best-practices guide and
  export comments distinguishing CSS states from application behaviour. Static
  examples still need application logic for actions, toggling, workflow status
  announcements and duplicate-submission protection in a real product.
- Added 33 regular regressions and a repeatable media-preference script. Final
  checks: **369/369** regular browser tests and **12/12** actual reduced-motion /
  forced-colour tests passed; no captured runtime errors. Structure: **27 assets**;
  diff check passed. Visual review covered desktop selected variants and 390 px
  dark selected / light loading exported examples, including wrapping and icons.
- Updated affected runtime asset query versions and README/contributor/architecture/
  changelog notes. User-created `test.html` and `tokens.css` remain untouched;
  re-export HTML/CSS to update those manual snapshots. No commits, pushes or
  deployments were made. Broader manual screen-reader / Firefox / Safari coverage
  remains open; these checks do not establish complete accessibility conformance.

## Guided Brand Palette and Main Palette completed

- Added the registered `brand-palette` module and scoped CSS. The six-step builder
  now introduces Brand Palette references before Main Palette role assignment in
  step 2; the introduction explains that sequence.
- Every Primary UI colour, Supporting colour and Accent colour dropdown offers
  the full named Brand Palette with HEX values. Existing custom pickers remain,
  and guided/advanced changes synchronize matching selections or Custom.
- Added optional name/colour editing and add/remove controls for up to 24 brand
  references. A selection copies HEX into a UI role: subsequent reference edits
  or removal preserve existing role colours until the user chooses again. Editor
  nodes and focus remain stable during updates; the last colour cannot be removed.
- Stored the normalized palette in project state, local saves and JSON. Existing
  projects without it receive starter references without overwriting their UI
  colours. New/reset projects retain the existing 11 starter colours/token IDs.
- Core reference swatches, legacy accent choices, exported `--brand-*` tokens,
  token catalogue and contrast candidates now read the same project palette.
  Display-name changes preserve token IDs. Candidate labels include token IDs so
  duplicate or ramp-like names cannot collide with generated-ramp repair targets.
- Import validation bounds palette/name sizes, accepts only safe unique IDs and
  HEX values, and renders untrusted names as text/escaped markup. Added regressions
  for malformed colours/IDs, duplicate names, HTML injection and palette limits.
- Added 21 browser regressions. Final suite: **390/390 passed** with no captured
  runtime errors; structure: **29 assets**; diff check passed. Covered both themes
  at 320 px and visually reviewed desktop and 390 px phone palette/editor views.
  Broader manual keyboard/screen-reader and Firefox/Safari review remains open.
- Updated runtime query versions, README/security/architecture/changelog and this
  handoff. User-created `test.html` and `tokens.css` remain untouched; exports are
  the source for refreshing those snapshots. No commits, pushes or deployments.

## Brand Colour Palette interaction cleanup completed

- Renamed the centre section to **2. Brand Colour Palette**. Inspected the old
  handlers and ran a focused pre-change browser check: Primary/Accent buttons
  updated their roles, but Supporting had no action and cards had no visible
  assignment feedback. The colour blocks were passive divs, so clicking the
  swatch colour itself did nothing.
- Replaced group-dependent actions with one unified grid: choose Primary UI,
  Supporting or Accent, then click any full swatch card. Role selection alone is
  view-only. The colour, label and usage footer all activate the same native button.
- Added Current Main Palette summaries, explicit Set-as action labels, per-card
  role usage, current-role highlighting and live confirmation. Applying a swatch
  updates existing role inputs, guided choices, preview, CSS and active local save.
  Cards update by token ID to retain keyboard focus; usage text also describes the
  button for assistive technology. Names continue to be rendered as plain text.
- Removed the section's misleading Restore example defaults control, which reset
  the whole project. Edit Brand Palette now opens step 2, expands its editor and
  focuses the first name control without changing project data. Global reset is
  unchanged. Palette references and independent Main Palette assignments retain
  their existing copy-and-apply behaviour.
- Moved swatch rendering/assignment into the brand module; core's renderBrand
  delegates to it. Removed artificial primary/accent restrictions from the display,
  clarified reference/ramp/semantic/component guidance, enlarged action text and
  adjusted mobile spacing/focus styling.
- Added 20 regressions. Final regular suite: **410/410 passed**, no captured
  runtime errors. Verified all three role actions, colour-block/footer clicks,
  independent assignments, live feedback, focus, editor navigation and both themes
  at 320 px. Visually reviewed desktop and 390 px dark-phone summaries/cards.
  Structure: **29 assets**; diff check passed. Broader manual screen-reader and
  Firefox/Safari testing remains open.
- Updated affected cache versions, README/architecture/changelog and this handoff.
  User-created `test.html` and `tokens.css` remain untouched. No commits, pushes or
  deployments were made.

## Header navigation state practices completed

- Scoped generated header navigation styles separately from ordinary links:
  plain at rest, underlined on hover, thicker underline while pressed, and the
  shared button focus colour/width with a 3 px outline offset for keyboard focus.
  Desktop and native mobile menus share these rules in both themes. Existing
  footer/body link settings remain independent. No extra scripts are needed in
  the exported page.
- Added 14 regressions covering exported/live-preview defaults with the general
  underline setting enabled/disabled, both themes at 320/1440 px, unchanged hover
  geometry, pressed cues and real DOM focus-visible styling. Pointer pseudo-state
  cascade checks use equal-specificity class substitution in headless Chrome;
  interactive pointer/touch review remains part of the open manual checks.
- Current checks: **424/424 browser checks**, **29 referenced assets**, and
  `git diff --check` passed. Refreshed the sample generator cache version.
  User-created `test.html` and `tokens.css` remain untouched.

## Footer navigation and startup disclosures completed

- Generated footer navigation now reads Home, About, Resources, Contact in that
  order, linking to the corresponding sections in both export and live preview.
- Removed remaining default-open studio disclosures from the guided state guide,
  button review, dynamically built variant reviews and advanced interaction
  settings. Only the Responsive page preview starts expanded. Subsequent user
  toggles and section-navigation shortcuts retain their existing behaviour.
  The sample page's own FAQ is independent of studio accordion defaults.
- Added six checks for all studio disclosure defaults, matching exported/live
  footer links and all four working preview destinations. The button-review test
  explicitly opens its parent disclosure before testing its interactions.
- Current verification: **430/430 browser checks**, no captured runtime errors,
  **29 referenced assets**, and `git diff --check` passed. Bumped changed runtime
  cache versions. User `test.html` and `tokens.css` snapshots remain untouched.

## Guided semantic colour editor

- Added Semantic colour roles beneath the preview theme selector in wizard step
  4 (Components). All 18 existing roles have readable labels, CSS token names,
  purpose text, a colour swatch, current HEX/theme and generated/custom status.
- Reused the contrast-preview/edit dialog and shared reset operation. Apply
  changes only the active preview theme; Cancel preserves project data and
  returns focus. Reset removes only the selected override. Both editor entry
  points refresh through the existing contrast-update path, including palette
  edits, imported/saved projects and project reset. Component-specific button
  overrides remain separate and the role descriptions explain that distinction.
- Added 15 regressions for role availability, light/dark previews, cancellation,
  focus return, overrides, CSS/live page/local saves, editor agreement, JSON
  imports, selected reset and 320 px layout. Initial test failures exposed test
  fixture assumptions: the wizard listens to input events and multiple saved
  projects already exist. Corrected those tests to use the active project and
  the existing wizard event contract.
- Updated README, architecture, changelog and the colour-repair cache version.
  User `test.html` and `tokens.css` snapshots remain untouched.
- Final verification: **445/445 browser checks passed**, no captured runtime
  errors; structure check verified **29 assets** and `git diff --check` passed.
  Interactive screen-reader and cross-browser review remains open below.

## Teaching workspace and complete token configuration

- Audited catalogue declarations against configuration sources. The previous
  wizard left font loading, responsive typography, readability, layout and
  interaction settings scattered across labs and the legacy parameter panel.
  Heading line-height was fixed. See
  `docs/TOKEN_CONFIGURATION_2026-10-20.md` for the family-by-family map.
- Expanded to eight wizard steps, preserving existing steps 1–5 and adding
  Layout and Accessibility before Deliver. Navigation no longer implies that
  earlier decisions/checks are complete. New `studio-learning` module moves
  existing configuration nodes after initialization, preserving IDs, handlers,
  validation and save paths. Hidden compatibility nodes keep older bindings.
- Added a lesson to each of the eleven centre sections: explanation, token
  relationship, practice and wizard shortcut. Each wizard step links back to
  a related lesson. Interactive experiments, specimen comparisons, calculator
  viewport and contrast repairs remain available; no duplicate demo state.
- Added Configure source to every catalogue row, with direct/derived/alias
  guidance. Routes reveal and focus the wizard control, select the correct
  semantic/button theme and button variant, and locate brand colours by stable
  ID. Derived scales update their foundation; no arbitrary CSS override layer.
  Corrected category labels for typography, layout, motion and control tokens.
- Made heading line-height a validated, persisted foundation (1–1.6, default
  1.18). Studio specimens, preview, CSS, JSON and local saves share the value.
  Old projects retain the default. Constant body text and the base-sized type
  step route to base size, since changing only the ratio would not update them.
- The existing 445-check suite passed after the initial reorganization. Added
  catalogue coverage, focused navigation, eight-step flow, line-height, save/
  import, teaching-link and expanded narrow-layout regressions. These exposed
  hidden catalogue labels extending beyond the table scroll area; replaced
  them with accessible button labels. A focused Chrome check then fit at 320 px.
- Updated README, architecture, changelog and affected cache versions. The user
  snapshots `test.html` and `tokens.css` remain untouched.
- Final checks: **474/474 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and `git diff --check` passed. The 29 new
  regressions cover all token mappings, representative focus routes, persisted
  line-height, expanded light/dark wizard steps at 320 px and lesson navigation.
  Also removed native range-input side margins that caused 2 px of overflow in
  expanded typography. Visually reviewed the desktop teaching layout and 390 px
  typography wizard in isolated Chrome screenshots. No screenshot baseline was
  added; interactive assistive-technology and cross-browser checks remain open.

## Follow-up audit and Colour systems startup

- Repeated the source/workflow and functional review after the teaching/wizard
  changes. Detailed scope, fixes and remaining limitations are recorded in
  `docs/AUDIT_2026-10-20.md`.
- Only **3. Colour systems** now starts expanded. Other centre sections and
  wizard disclosures start collapsed. Fluid preview updates while hidden, and
  reopening preserves its document, selected settings and measured viewport.
  Direct URL fragments and user disclosure toggles retain existing navigation.
- Fixed mismatched teaching specimens: one `SPACING_STEPS` definition now feeds
  exported CSS and the spacing chart (removing non-exported space-3 and showing
  all exported steps); type ladder line-height follows heading/body settings;
  heading specimens and ladder follow the configured heading weight. Body rows
  retain weight 400. Refreshed core-state's cache version.
- Desktop and dark-phone visual review exposed fixed scroll margins hiding
  mobile lesson headings below the wrapped header. Section offsets now follow
  measured header/navigation heights via resize observation. Added visible-heading
  checks at 320, 390 and 1440 px and refreshed layout/accordion cache versions.
- Accessibility and real-font fixtures now reveal the preview they exercise
  rather than depending on the startup disclosure. Main suite coverage adds
  collapsed-preview lifecycle, chart/export agreement, typography synchronization,
  spacing updates and section navigation. User snapshots remain untouched.
- Final audit verification: **484/484 main**, **12/12 accessibility-mode** and
  **9/9 live-font checks passed**, no captured runtime errors; structure verified
  **30 assets** and diff check passed. No commits or deployments were performed.

## Responsive preview startup restored

Latest startup preference supersedes the Colour systems default recorded in the
follow-up audit: only Responsive page preview now starts expanded in Fluid mode.
Updated startup assertions and retained collapsed-preview lifecycle checks by
explicitly closing it within that test fixture. README/architecture reflect the
current default; the preceding audit remains a historical record.
The navigation geometry fixture now disables smooth scrolling and browser scroll
anchoring during viewport measurements, avoiding interference from the preceding
animated lesson jump. Application scrolling behaviour is unchanged.
Verification for this preference change: **484/484 browser checks passed**, no
captured runtime errors; structure verified **30 assets** and diff check passed.
The optional media/font results above are from the preceding audit, not rerun for
this HTML startup-default change.

## Minor Third default

- Changed the foundation ratio from 1.25 to 1.2; the existing preset matching
  selects Minor Third in both wizard and calculator. Updated CSS/HTML fallback
  values, explanatory default examples and affected asset query versions.
- Startup, New project, Reset and imports without a ratio use Minor Third.
  Explicit saved ratios, including Major Third 1.25, remain unchanged.
- Added five regressions for initial synchronization/export, reset, new projects,
  old explicit ratios and missing-ratio imports. Updated default ladder checks
  to expect 19.2 px / 1.2 rem above the 16 px base. User snapshots were not edited.
- Verification: **489/489 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and `git diff --check` passed. Optional media
  and live-font checks remain the preceding audit's results, not rerun here.

## Resource-table link states

- Extended the existing generated header-link selectors to include the resource
  table. All three Explore links are plain by default, underline on hover, use a
  stronger underline while pressed and share the button keyboard focus ring.
  Generated exports and the responsive page preview consume the same CSS.
- Added 14 regressions for all three links, both general underline settings,
  light/dark themes and 320/1440 px widths: default decoration, unchanged hover
  geometry, pressed cue and real focus-visible outline. Pointer-state cascade
  checks use equal-specificity class substitution, as in the existing nav tests.
- Refreshed the sample generator asset version and documentation. Resource hrefs
  retain their existing section destinations; user snapshots were not edited.
- Verification: **503/503 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Optional media/font
  checks remain the preceding audit's results, not rerun for these link styles.

## Wizard navigation/content division

- Added a 2 px theme-aware divider below the eight step buttons, with 16 px
  padding above the divider and 24 px separation before the selected step content.
  It applies across all wizard steps and uses the existing border token.
- Refreshed the wizard stylesheet cache version. No new tests were added for this
  presentation-only change; the existing browser suite is used for regressions.
- Verification: **503/503 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Visually reviewed the
  divider on a light desktop and a dark 390 px phone layout in isolated Chrome.
  Optional media/font checks were not repeated for this spacing/divider change.

## Persistent section menu above the preview

- Moved the existing 1–11 menu and Expand/Collapse controls to the start of the
  centre pane, before Responsive page preview. The preview remains the first
  learning section and the only expanded disclosure on startup.
- Kept the menu sticky at every breakpoint, including phones, and positioned it
  using the measured app-header height. The same measurement includes the menu
  when calculating section scroll offsets so destination headings stay visible.
  Horizontal overflow remains inside the menu; link targets are at least 44 px
  tall and retain native keyboard/fragment navigation.
- Extended checks for startup order, sticky/header geometry, heading visibility,
  horizontal overflow and reaching the last menu item with keyboard focus across
  320, 390, 768, 1280, 1440 and 2560 px. Refreshed affected asset cache versions.
- Verification: **518/518 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Visually reviewed the
  desktop preview and a scrolled dark-phone lesson with the menu pinned below
  the header. Optional media/font checks remain the earlier audit results.

## Web Design Field Guide sample

- Replaced the generic service-site content with a coherent web design tutorial:
  welcoming hero, semantic-structure introduction, six lesson cards, Grid and
  type/colour workshops, field notes, review checklist, practice question form
  and interface/state lab. Header now labels the existing services anchor Lessons;
  footer stays Home/About/Resources/Contact. Stable IDs preserve preview behaviour.
- Drew self-contained palette-aware SVG browser and grid illustrations. Kept the
  bounded illustration cache, adding border colour to its key. No new assets or
  runtime network dependencies; existing optional Google Fonts behaviour remains.
- Added a twelve-track grid exercise (8/4 and 4/4/4 spans), a matching native
  CSS-recipe disclosure and tablet-stacked example/notes composition. The demo
  becomes one column at 48rem and consumes the saved grid-gap token. Six lesson
  cards retain the existing minimum-width/container-query grid controls.
- Added live base/ratio/leading readouts and semantic palette swatches/HEX values.
  Lessons link to real page examples. All eight main sections retain wizard-driven
  Primary/Secondary action pairs; the form remains an explicitly static practice.
- Updated browser expectations for eight sections, added tutorial content, grid
  bounds/spans at eight widths, live readout/gap and lesson-destination coverage.
  Existing layout, theme, footer, state, form preservation and resource-link tests
  remain. Updated generator cache version, README, architecture and changelog.
  User snapshots `test.html` and `tokens.css` remain untouched.

- Final verification: **544/544 browser**, **12/12 accessibility-mode** and
  **9/9 real-font checks passed**, with no captured runtime errors. Structure
  verified **30 assets** and diff check passed. Visually reviewed the exported
  desktop hero, six-card lesson board and grid workshop, plus the dark 390 px
  stacked grid. The CSS recipe includes all demonstrated spans and the narrow
  media rule. No screenshot comparison baseline or deployment was added.

## OKLCH role reset and Flexbox lesson (21 October 2026)

- Added "Reset selected role to default" beside the OKLCH Apply/Load controls.
  It restores only the selected Primary/Supporting/Accent starter anchor, reloads
  the wheel and uses the same control, preview, export and save path as Apply.
  Load continues to discard an unapplied experiment; nearby help explains both.
  Brand reference edits and other role assignments are preserved.
- Expanded the existing layout workshop with Flexbox topic wrapping, fixed-marker /
  flexible-text rows, main/cross-axis explanations and column card interiors.
  A comparison table explains normal flow, Grid and Flexbox, including nesting.
  The displayed Flexbox recipe and generated CSS share one source. Lesson 02,
  the practice-form topic and HTML description now include Flexbox.
- Kept existing section IDs and eight main sections. Existing previews and HTML/CSS
  downloads receive the lesson automatically. Refreshed both changed JS asset
  versions; user snapshots `test.html` and `tokens.css` were not edited.
- Added 18 browser checks for all three role resets, repeat resets, state/control /
  preview/export/save agreement, shared recipe/gap and Flexbox geometry at
  320/390/768/1280/1440 px in both themes.
- Commands run: `python scripts/check_structure.py` (**30 assets verified**),
  `python scripts/browser_review.py` (**562/562 passed**, no captured errors),
  and `git diff --check` (passed). Chrome initially could not create a temporary
  profile in the sandbox; the suite succeeded with elevated execution using its
  isolated profile. Intermediate runs caught test-file encoding changes, corrected
  before the final pass. No product failures remained.
- Ran temporary Python/local-server/headless-Chrome screenshot helpers and inspected
  the light desktop and exact 390 px dark Flexbox lesson. The attempted colour-panel
  screenshots did not reach the expanded panel; visual review of the reset control
  remains a manual gap. Automated studio checks still pass at 320 px.
- Optional real-font and accessibility-mode suites were not rerun; their preceding
  results are historical. Manual keyboard/screen-reader, Firefox/Safari and real
  pointer/touch checks remain open. No commits, pushes or deployments were made.
- Next step: manually review the reset controls in the expanded Colour lesson,
  then continue the broader verification/CI work listed below.

## Project planning before palette (21 October 2026)

- Expanded the wizard to eleven stages: Project Brief, Information Architecture,
  Wireframing, Prototyping, Palette, Typography, Components, Buttons, Layout,
  Accessibility and Deliver. Added four corresponding centre lessons after the
  responsive-preview hub and before palette; the menu now has fifteen lessons.
  Kept the preview as the only initially expanded centre section and preserved
  existing control/section IDs. Updated all numeric wizard routes and shortcuts.
- Added the registered `design-process` module and studio stylesheet. Planning
  records audience, main task, scope, success signal, constraints, a two-level
  content map, split/stack wireframe arrangement, hierarchy notes, prototype task
  and observations. The brief/map feed the wireframe and linked Discover, Choose
  and Review screens. Native fragment navigation works in the studio, sandboxed
  preview and static exported page; the prototype has no application backend.
- Planning uses shared state, Apply/render/autosave and existing JSON/local-project
  flows. Imported values are type/length/enum validated; architecture is limited
  to twelve entries, two levels and 64-character labels. Empty drafts stay empty.
  Plan text is escaped. Older projects receive fresh starter planning data without
  changing their explicit palette. UI edits do not mutate defaults. Reuse unchanged
  artifact nodes to preserve focus through unrelated design changes.
- Updated the generated field guide with a Process destination, shared planning
  artifacts, ten ordered lesson cards, related form topics and workflow guidance.
  Nine main sections retain Primary/Secondary action pairs. The sample remains a
  teaching field guide; planning data does not generate a finished custom website.
  Updated delivery guidance and the eight-item self-assessment, source routing,
  runtime cache versions, README, architecture and changelog. User snapshots
  `test.html` and `tokens.css` were not edited.
- Added planning regressions for stage order and reciprocal navigation, local
  autosave/project switching, JSON and actual file-input imports, legacy/malformed
  data, length bounds, safe rendering, default/reset independence, prototype
  links/focus, shared inspector/export/preview content and both themes at
  320/390/768/1440 px. Existing layout/state/library/font-fixture checks remain.
- Final commands: `python scripts/check_structure.py` (**32 assets verified**),
  `python scripts/browser_review.py` (**615/615 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Browser runs used elevated execution
  for isolated temporary Chrome profiles. Increased the virtual-time budget to
  45 seconds and process timeout to 90 seconds for the longer interaction suite.
- Intermediate checks exposed harness issues rather than remaining product
  failures: stale section/action counts, a 1440 px test iframe affecting narrow
  studio measurements, and file I/O outlasting a fixed virtual wait. Updated
  expectations, resized the test iframe and waited for file-input cleanup.
  Focused temporary-harness checks also passed **2/2** for direct 390 px startup.
- Ran temporary local-server/headless-Chrome screenshot helpers. Visually reviewed
  the desktop brief/editor, light desktop wireframe/prototype/lesson board and
  exact 390 px dark exported wireframe/prototype. The attempted mobile studio
  screenshot captured before initialization; it is not visual-review evidence.
  Automated direct-mobile initialization and narrow planning-editor checks pass.
- Optional real-font and accessibility-mode suites were not rerun; previous
  results above remain historical. Manual keyboard, screen-reader, zoom, complete
  mobile-studio visual review and Firefox/Safari checks remain open. No commits,
  pushes, deployments, runtime dependencies or new network requests were added.
- Next step: walk through the planning flow with a real project/audience, review
  the mobile studio and keyboard/screen-reader experience, then continue CI work.

## Explicit standalone website downloads (21 October 2026)

- Added a clear download card above the responsive page viewport with separate
  HTML (`index.html`) and complete CSS (`tokens.css`) actions, plus View HTML/CSS
  shortcuts into the existing live code panel. Added the HTML action to Deliver
  and moved its CSS action to the shared handler, correcting the old stylesheet
  filename mismatch. Both files can now be saved together without renaming.
- Added the registered `website-export` module and studio-only stylesheet. All
  downloads evaluate the existing generators at click time; the sample, preview,
  inspector and files remain one source of truth. Export/view actions do not
  alter saved project data. Feedback says a download was requested rather than
  claiming the browser saved a file successfully.
- Explained the included header/mobile menu, hero, images, cards, Grid/Flexbox,
  forms, table, FAQs, component states and footer. Included same-folder/open-file
  instructions and existing static-form / optional-font behaviour. Updated
  README, architecture, changelog, delivery guidance and the affected asset query
  version. No generated snapshot overwrites: `test.html` and `tokens.css` remain
  user-owned files.
- Added 20 browser checks, including every explicit action's filename/MIME/exact
  contents, code selection/reveal/focus and unchanged settings. Loaded captured
  HTML using a separate Blob stylesheet, with no injected style or script nodes,
  and verified components, 320/768/1440 px reflow and native mobile-menu/FAQ/form
  validation behaviour in both themes.
- Commands run: `python scripts/check_structure.py` (**34 assets verified**),
  `python scripts/browser_review.py` (**635/635 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Chrome used elevated execution for
  its isolated temporary profile. No browser-suite failures in this session.
- Temporary local-server/headless-Chrome screenshots were captured and inspected
  for the light desktop and exact 390 px dark download card. Applied the existing
  ghost-button class after visual review for consistent studio controls; that
  presentation-only adjustment was checked structurally, without rerunning the
  already passing full suite.
- Actual browser download/save-dialog permissions and manual keyboard/screen-reader,
  zoom and cross-browser checks remain open. Previous optional font/media results
  are historical and were not repeated. No new runtime dependencies, network
  requests, commits, pushes or deployments were introduced.
- Next step: use both download buttons in an interactive browser, save the pair
  into one folder and confirm the local file workflow on the target computer.

## Basic / Advanced Inspector samples (21 October 2026)

- Added independent Advanced/Basic tabs above the existing CSS/HTML tabs, with
  Arrow/Home/End navigation, one tab stop per group and labelled nested panels.
  Advanced remains the startup/reset/legacy-project default and retains its exact
  generated HTML/CSS. The Basic sample is intentionally smaller and uses its own
  complete stylesheet instead of shipping unused Advanced gallery/workshop CSS.
- Added the registered `basic-homepage` module after the Advanced generator and
  before the responsive preview, plus studio-only mode-control CSS. Basic includes
  logo/wrapping navigation, hero, three generated Grid cards, a labelled static
  sign-up form with required name/email/consent and a footer with navigation and
  a real Back to top destination. It includes a skip link and visible focus styles.
  Exported HTML has no scripts, inline styles or runtime libraries.
- Basic HTML/CSS share current project name/theme, font settings, type scale,
  leading/tracking/heading weight, semantic colours, radius, grid gap/card minimum
  and focus width. Advanced state demonstrations/planning artifacts stay in the
  Advanced sample. Imports escape project text and validate the saved `sampleMode`
  enum; missing/invalid modes use Advanced. Selection travels through JSON/local
  saves and all existing code, copy, preview and download paths.
- Preview refreshes preserve form state within a mode and start fresh when switching
  samples, preventing unrelated input/focus/scroll state from crossing modes.
  Basic preview submissions use native validation and display static-demo feedback
  without navigation or an account backend. The exported static form returns to
  the page using native GET behaviour; help instructs using sample details.
- Updated Inspector notes and download-card descriptions, README, architecture,
  changelog and affected runtime cache versions. Asynchronous clipboard feedback
  now verifies both selected mode and language before reporting success/failure.
  User snapshots `test.html` and `tokens.css` remain untouched.
- Added 40 browser checks for mode defaults/keyboard controls, exact Advanced
  preservation, Basic semantic structure and safe rendering, persistence/imports,
  selected code/copy/download agreement, live settings, form validation and
  preservation, clean mode transitions and external-stylesheet rendering. Checked
  Basic reflow at 320/390/768/1440 px in both themes, real native Back to top links,
  visible skip links and focus outlines.
- Commands run: `python scripts/check_structure.py` (**36 assets verified**),
  `python scripts/browser_review.py` (**675/675 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Chrome used elevated execution with
  isolated temporary profiles. The suite passed on its first run for this change.
- Ran temporary local-server/headless-Chrome screenshot helpers and inspected the
  light desktop Basic page, exact 390 px dark header/hero/Grid/form/footer and the
  desktop Inspector with Basic/HTML selected. No visual baseline was added.
- Actual browser download/save-dialog behaviour, manual keyboard/screen-reader/zoom
  reviews and Firefox/Safari remain open. Previous optional real-font and media
  suite results are historical; those suites were not rerun. No dependencies,
  new network requests, commits, pushes or deployments were introduced.
- Next step: try the Basic file pair and keyboard journey in an interactive browser,
  then continue the manual accessibility and CI work below.

## Responsive phase, brief training and Basic lists/sitemap (21 October 2026)

- Added phase 10, Responsive, between Layout and Accessibility: twelve wizard
  phases and sixteen centre lessons. Moved grid minimum/gap/alignment controls
  into this phase, updated token/lesson routes and retained stable section IDs.
  Added five validated project settings for narrow cutoff, wide spacing start,
  page maximum and standard/wide gutters, with 768/1024/1152/16/32 defaults.
- Both samples, exported styles, Advanced Grid recipe and planning wireframes
  consume these shared decisions. Three page tokens route to Responsive and are
  classified as Layout. Breakpoints export as literal rem media-query lengths;
  variable-based container lengths remain separate. Preview presets, fluid type
  bounds, studio pane widths and component-specific button settings stay separate.
- New lesson explains content-led breakpoints, containers, wrapping, flexible
  images and boundary checks, with a current recipe and real iframe matchMedia
  readout. Ordered/bounded imports and 1px slider increments preserve exact valid
  lengths. UI changes use existing Apply/render/autosave and JSON/local flows.
- Replaced the prefilled Project Brief lesson with five plain-language questions
  and a fill-in sentence. New brief fields start empty with prompts. Imported
  answers remain available in an optional Your draft brief disclosure. Guidance
  follows web.dev media-query and GOV.UK user-needs primary sources, linked from
  the lessons and README.
- Basic now has four main sections: hero, features, lists and static sign-up.
  The lists section demonstrates titled ul/ol/dl examples side by side when space
  permits and stacks at narrow widths. Header/footer navigation includes Lists.
- Clarified that Architecture's Pages and content groups is the sitemap plan.
  Its existing two-level parser now also supplies Basic's footer sitemap. Known
  built-section labels become actual fragment links; other entries are escaped
  text with Planned page markers. Empty plans show an explicit empty state while
  ordinary footer navigation continues to reach every built section. Architecture
  edits update the centre map, footer, Inspector and downloaded HTML together.
- Preserved preview disclosure state by stable IDs/summary keys rather than array
  position, preventing the first added brief draft from transferring a FAQ's open
  state to a different disclosure. Added a regression for draft insertion.
- Commands run: `python scripts/check_structure.py` (**38 assets verified**),
  `python scripts/browser_review.py` (**736/736 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). A focused temporary browser harness
  passed **1/1** after the final page-token classification refinement. Chrome used
  elevated execution with isolated temporary profiles. Increased suite allowances
  to 60 seconds virtual time / 120 seconds process time for the longer sequence.
- Current browser coverage includes both themes/modes immediately below/at/above
  custom cutoffs, gutters/page width, exact import values, malformed data, save /
  round trips / reset, brief instructions and preserved drafts, list semantics,
  responsive geometry, sitemap live edits/empty state/safe text and valid links.
  The first expanded run was 733/734: its security assertion expected a literal
  greater-than character that the documented hierarchy delimiter consumes. Corrected
  the assertion while retaining DOM-injection and destination safety checks.
- Ran temporary local-server/headless-Chrome screenshot helpers; inspected the
  desktop Responsive editor/lesson, simple brief guide, desktop list cards and
  exact 390 px dark footer sitemap. No visual-comparison baseline was added.
- Intermediate work was committed by the user as `62924b5` while this task was in
  progress. The final checks above validate the completed work, including later
  local changes. No commits, pushes or deployments were made by this assistant.
  User snapshots `test.html` and `tokens.css` remain untouched.
- Previous optional media/real-font checks remain historical and were not rerun.
  Manual screen-reader, keyboard/zoom, Firefox/Safari and actual download-dialog
  checks remain open. No new runtime dependencies or network requests were added.
- Next step: try a real Architecture plan and both exported samples, then complete
  the manual accessibility and CI work below.

## Complete sample content maps (21 October 2026)

- Replaced the six-entry starter with complete Basic (11 entries) and Advanced
  (38 entries) inventories. Maps include all main sections and article groups: Basic cards/lists and
  Advanced planning stages, ten lessons, layout/visual workshops, resources and
  components. Added fixed destination IDs and an Advanced footer sitemap.
- Architecture, wireframe/prototype topic labels, both footer maps and generated
  HTML resolve the same selected-sample plan. Untouched complete maps follow the
  mode; the exact old starter upgrades automatically. Custom/empty maps remain
  unchanged across mode switches and JSON round trips. The explicit restore
  button replaces a custom map with the current sample inventory.
- Kept destinations restricted to fixed IDs and escaped unknown labels. Raised
  limits to 64 entries / 8,400 characters (two levels, 64 characters per label).
  Updated training copy, README, architecture notes, changelog and asset versions.
- Added browser regressions for complete destination coverage in both modes,
  matching editor/centre/footer maps, custom preservation/round trips, restore,
  legacy starter upgrades and the expanded parser bound. Existing responsive
  checks now run against the populated Basic sitemap.
- Current verification: `python scripts/check_structure.py` passed (38 assets);
  `git diff --check` passed (existing CRLF normalization notices only).
  First browser run completed at 778/781, including duplicate table-ID and
  complete-map coverage failures. Split the layout-comparison/resource-library
  IDs and included the layout-comparison entry. The second run passed 781/782;
  its remaining assertion still expected the old four-link footer. Updated that
  assertion to check the five footer shortcuts separately from the full sitemap.
  Final `python scripts/browser_review.py` passed **782/782**, with no
  interaction JavaScript errors. All three required checks passed on the final
  implementation; browser checks used an isolated temporary Chrome profile.
- Manual visual, keyboard, screen-reader and Firefox/Safari checks were not run
  for this change. Earlier visual checks above belong to the previous task.
- Next step: review the complete maps with real training content and complete
  the manual accessibility/cross-browser checks. No commits or deployments made.

## Shared sample system and footer review (21 October 2026)

- Confirmed Basic maintained a separate, partial token/CSS generator and fixed
  body/heading sizes, spacing, reading measure, control sizes and card appearance.
  Added `sample-system.js` to capture the existing shared foundation/component
  generator before the sample layouts, with common button classes/footer output.
  Script order remains dependency-safe; there are no new runtime dependencies.
- Both samples now use the same generated ramps, semantic/theme roles, fluid
  typography and spacing tokens, reading width, card borders/shadow/opacity,
  control dimensions/focus, grid alignment and Button Design settings. Basic's
  HTML stays simple. It now uses shared `ds-button` classes and labelled `.input`
  controls; its layout CSS consumes tokens rather than overriding system values.
  General link focus also follows the saved focus width in both exports.
- Replaced duplicate footer implementations with shared identity/Explore rows,
  a closed native expandable sitemap and a copyright/Back to top row. Added
  Advanced's `#top` destination. The full maps and custom plans remain intact;
  shorter footer links remain visible. Rows use the saved responsive cutoff,
  gutters, type, borders and spacing. Footer link weight is now shared too.
- Added regressions comparing actual computed Basic/Advanced styles under default
  and edited/imported settings in both themes, standalone and live preview;
  covered custom button colours/dimensions, footer disclosure and all footer
  target sizes/overflow at 320, 390 and 1440 px. Updated prior assertions for the
  shared system CSS and expandable sitemap. Updated asset versions and docs.
- Current checks: `python scripts/check_structure.py` passed (39 assets),
  `git diff --check` passed (existing CRLF normalization notices only).
  Initial expanded `python scripts/browser_review.py` passed **804/804**, no
  interaction errors. The final run, including the footer weight adjustment and
  custom button colour assertions, also passed **804/804**, with no interaction
  JavaScript errors.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks using isolated temporary Chrome profiles.
- Generated and visually inspected temporary screenshots for both modes: 1440 px
  light desktop and exact 390 px dark phone. Footer identity, links, disclosure
  and bottom rows fit; final link-weight consistency was corrected afterward.
  Screenshots are temporary local artifacts, not committed visual baselines.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain open;
  passing the automated suite does not establish full accessibility. Root user
  snapshots `tokens.css` and `test.html` were not edited. No commits/deployments.
- Next step: review with real training content and complete the manual
  accessibility/cross-browser checks.

## Header navigation consistency (21 October 2026)

- Confirmed Basic header links inherited normal body weight/general underlining,
  while Advanced explicitly used weight 600 and plain links at rest.
- Moved Advanced's header navigation text, hover/pressed underlines and component
  focus ring into shared sample foundation CSS, targeting both headers. Advanced
  resource-table styles remain separate. Basic keeps its wrapping layout and
  Advanced keeps its native mobile menu; text treatment now has one source.
- Refreshed sample-system/sample-homepage asset versions. Added browser checks
  comparing navigation fonts/decoration across modes, both themes, default and
  edited/imported settings, live previews and standalone exports, including
  visible links and focus rings at 320, 390 and 1440 px.
- Current checks: `python scripts/check_structure.py` passed (39 assets) and
  `git diff --check` passed (existing CRLF normalization notices only).
  Required `python scripts/browser_review.py` passed **852/852**, with no
  interaction JavaScript errors, using an isolated temporary Chrome profile.
- No button component rules changed; prior reduced-motion/forced-colour results
  above are historical for this task. Manual keyboard-only, screen-reader and
  cross-browser review were not performed for this small text-style change.
  User root snapshots remain untouched. No commits or deployments.
- Next step: verify navigation in the user's preview and complete the manual
  accessibility/cross-browser review.

## Website-project brief lesson (21 October 2026)

- Replaced the generic user-needs guide with seven website-project prompts:
  purpose/main action, audience, first-release pages/features and exclusions,
  content and its owner, design/technical/accessibility requirements, delivery
  (deadline, budget/time, handover, approval and maintenance), and a success check.
- Added a fill-in template and a clearly labelled static cafe website example.
  The example explains three pages, no online ordering, owner-supplied content,
  branding, phone/keyboard use, delivery and a visitor task. It does not fill in
  or overwrite a learner's saved answers. Unknowns can be marked to confirm.
- Reviewed the old GOV.UK user-needs page, Smashing Magazine's website-planning
  guide (Ben Seigel, needs assessment/client brief) and Figma's design-brief guide.
  The lesson now stands alone and links to Smashing Magazine as optional website
  planning reading. No remote content is loaded into the runtime.
- Updated stage introduction/practice, wizard labels/placeholders/scope help,
  generated Advanced lesson, README, architecture notes, changelog and asset
  version. Existing audience/goal/scope/success/constraints data and limits remain.
- `python scripts/check_structure.py` passed (39 assets); `git diff --check`
  passed (existing CRLF notices only). Full `python scripts/browser_review.py`
  passed **853/853**, with no interaction JavaScript errors.
- After final wording/label corrections, ran a temporary focused harness through
  the same browser runner: **7/7** passed for seven prompts, accent/apostrophe
  rendering, wizard labels, source replacement, saved-field preservation,
  matching Advanced export and the lesson at 320 px. Added the final wording
  assertion to the tracked regression suite afterward; that extra assertion was
  covered by the focused run, not the earlier 853-check full run.
- Manual keyboard/screen-reader, visual screenshot and cross-browser reviews were
  not run for this lesson change. Previous screenshot results remain historical.
  No root snapshots, commits, deployments or runtime dependencies were changed.
- Next step: try writing a brief for a real small website with the revised guide.

## Seven-field brief wizard alignment (21 October 2026)

- Replaced the five combined brief editors with seven numbered fields in the
  approved lesson order: Purpose, Audience, Pages and features, Content, Design
  and requirements, Delivery, Success. Labels and full question text now match
  the centre lesson exactly. Updated guidance and completion prompts accordingly.
- Added one `briefFields` definition for field keys, labels, prompts and limits.
  It generates the wizard, lesson checklist and saved draft, preventing separate
  wording/order from drifting again. Added spacing for the generated editor group
  and refreshed affected JS/CSS query versions.
- Added Content and Delivery to normalized project planning data (empty defaults,
  string-only values, 1,200-character bounds). Kept original goal/audience/scope/
  constraints/success keys. Legacy combined notes remain in their original fields;
  no guessed splitting or automatic overwrite. Shared state makes new answers
  follow JSON, local projects, the centre draft, Advanced preview and HTML export.
- Extended existing autosave, project-switch/file-import and JSON round-trip tests
  with Content/Delivery values. Added parity/order/prompt checks, legacy combined
  note preservation, new field limits/type validation, escaping and reset checks.
  Draft assertions now select a named field rather than assuming Audience is first.
- Current verification: `python scripts/check_structure.py` passed (39 assets),
  `git diff --check` passed (CRLF normalization notices only). Required browser
  suite is running; final result pending.
- Captured and inspected temporary 1440 px/390 px screenshots. Desktop Purpose,
  Audience and Pages/features editors have readable spacing; the narrow wizard
  introduction/navigation fits. These are temporary checks, not screenshot baselines.
- Manual keyboard/screen-reader, full form visual and cross-browser review remain
  open. No network dependencies, root snapshots, commits or deployments changed.
- Next step: record browser results and try a complete brief in the aligned wizard.

## Basic hero image (23 October 2026)

- Added Advanced's embedded 960 x 720 SVG illustration to the Basic hero through
  the shared `DSStudio.samples.illustration` helper. Its bounded cache and current
  palette/theme roles are reused; no network requests or extra export files.
- Basic uses two equal Grid columns with the saved gap, stacking text before the
  image at the saved responsive cutoff. Added descriptive alt text, intrinsic
  dimensions, fluid image sizing and the shared corner radius. Updated sample
  descriptions, architecture notes and affected JavaScript cache versions.
- Added 12 regressions for shared image/inspector/export agreement, live palette
  edits, standalone image loading in both themes and hero geometry at
  320/390/768/1440 px. Updated the hostile-project assertion to allow only the
  intended embedded image while still rejecting injected markup/event handlers.
- First browser attempt was blocked by sandbox access to Chrome's temporary
  profile; reran outside the sandbox using the existing isolated-profile harness.
  First full result: **871/872**, no captured JavaScript errors. All new hero
  checks passed. The failure was an older brief-escaping assertion selecting the
  first field after the seven-field reorder; corrected it to select Audience by
  its field name. Final full rerun: **872/872 passed**, with no captured
  JavaScript errors.
- `python scripts/check_structure.py`: **39 assets verified**.
  `git diff --check`: passed. Browser output captured in the ignored temporary
  `.basic-hero-review.log` while running; no root sample snapshots were edited.
- Manual visual, keyboard, screen-reader and cross-browser checks were not run
  for this change; automated tests do not establish full accessibility.
- Next step: review the Basic hero in the UI and complete manual browser checks.

## Open work / next session

1. Verify the first hosted run of the new shared structure/browser validation and
   Pages dependency gate after these local changes are committed and pushed.
2. Complete manual keyboard, screen-reader, zoom and visual review; test Firefox
   and Safari. Automated interaction checks do not replace these checks.
3. Review browser download permissions, successful clipboard access and real
   pointer/touch wheel dragging in an interactive browser.
4. Keep the shared-global/module migration as architecture debt; no refactor was
   attempted during this audit.

No commits, pushes or deployments were made in this session.
The older `PROJECT_AUDIT_2026-10-19.md` records a previous, smaller test baseline.
