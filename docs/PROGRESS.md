# Project progress

Updated: 20 October 2026 (America/Halifax).

## Current objective

Start with only **1. Responsive page preview** expanded in the centre pane;
keep all other centre sections collapsed.
The initial audit began at commit
`6163ada` (`improved UX/UI`) with a clean working tree; its changes are still local.

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
- `python scripts/browser_review.py`: **484/484 passed** in headless Chrome on
  Windows; no captured startup or interaction JavaScript errors.
- `python scripts/button_states_review.py`: **12/12 passed** (5 reduced-motion,
  7 forced-colour checks), repeated against the final follow-up audit code.
- `python scripts/font_cdn_review.py`: **9/9 passed** using real Google font
  stylesheet/font downloads and standalone exported HTML, repeated in this audit.
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

## Open work / next session

1. Add the browser suite to CI and gate Pages publishing on validation. Current
   CI only checks structure; deployment is a separate workflow.
2. Complete manual keyboard, screen-reader, zoom and visual review; test Firefox
   and Safari. Automated interaction checks do not replace these checks.
3. Review browser download permissions, successful clipboard access and real
   pointer/touch wheel dragging in an interactive browser.
4. Keep the shared-global/module migration as architecture debt; no refactor was
   attempted during this audit.

No commits, pushes or deployments were made in this session.
The older `PROJECT_AUDIT_2026-10-19.md` records a previous, smaller test baseline.
