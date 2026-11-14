# Architecture

## Validation and publishing

`scripts/browser_runner.py` owns Chrome discovery, the loopback HTTP server,
test-only error instrumentation, local font/File-I/O fixtures, temporary profile,
DOM report parsing and cleanup. Suites call `run_review(harness, chrome_flags=(),
virtual_time_budget=225000, timeout=660)` with explicit inputs; there is no shared
mutable harness or subprocess replacement. Each call creates a separate server
and profile. Failed assertions, captured JavaScript errors, nonzero browser exit
codes, malformed/empty reports and incomplete harnesses fail validation.

`browser_review.py` retains combined integration journeys and its command entry point.
Project-model, project-library, navigation, planning, content-tree, sitemap,
wireframe, palette, contrast, components, typography, spacing, responsive-preview,
standalone-export, view-update, export-pipeline,
button-media and optional live-font suites own their HTML and initialize the app
independently through the same runner.
`browser_runner_review.py` tests the runner contract with standard-library mocks
and real loopback requests, without launching Chrome. CI runs it before the Chrome
suites. `project_library_review.py` owns the detailed local-library and JSON
validation/file-picker checks formerly embedded in the integration harness. It
adds independent Basic/Advanced fixtures for fresh-document recovery, complete
snapshots, exports, invalid-file autosave retention, successful-file detachment
and reset confirmation. The integration suite retains a save/edit/New/load/JSON
download/file-import path across editors, preview and exports. Feature-specific
persistence checks stay with their owning focused suites. Shared teaching,
inspector, token-routing, website-editing and Tailwind bridge contracts remain
in integration alongside the combined journeys.

`navigation_review.py` owns startup/step selection, fragment reloads, native
disclosures, lesson/control focus, responsive placement, inspector collapse and
Studio return-link checks. It initializes its own app and reload document; it
does not inherit Studio appearance, feature editor values or inspector setup
from another suite. It also exercises repeated 900/901 px breakpoint crossings,
original editor nodes/listeners, live hash routes and malformed/missing fragments.
The integration suite keeps a Brief-to-Typography-to-Deliver learner journey
covering edits, focus, preview identity, inspector output and website downloads.
Feature-specific routing remains alongside its owning feature checks.

`planning_review.py` owns shared planning-field persistence/validation/escaping,
the seven-field Brief guide and centre editors, supporting paper-prototype links
and planning-artifact layout checks. Its own fixtures start with explicit sample,
stage and viewport state. It also checks placeholder guidance stays outside saved
answers, original editor nodes/focus during escaped field edits, and Basic/Advanced
local-load/JSON-file round trips. Basic retains planning in Studio/project data;
Advanced renders the planning artifacts in its website. Integration retains one
shared-planning save/download/file-import/sample-switch path through editors,
preview and exports.

`content_tree_review.py` owns content inventory identities, branch operations,
Save/Discard/Undo, proposal-versus-website boundaries, normalization limits,
restoration and dirty-form protections. Its fixtures own sample, stage, viewport,
real local saves and JSON-file import setup; content-to-sitemap boundary checks
remain with these fixtures, while sitemap CRUD stays separate. Additional checks
cover identical-file replacement with a dirty editor, clearing incompatible Undo,
editor identity, protecting the previous local save after import, and New with
unsaved proposals. Integration retains a content-edit/save/Discard/Undo/JSON-file
journey across the editor, persistence and unchanged actual website content.

`sitemap_review.py` owns custom-destination CRUD and hierarchy, inclusion and
planned-entry visibility, legacy compatibility/validation, page-derived labels,
source switching, restore/Undo and responsive editor-layout checks. Its fixtures
explicitly establish sample, stage, viewport, Studio appearance and inspector
state. Additional Basic/Advanced cases exercise file import over dirty edits,
source Undo with later Brief changes, saved-project protection and New. Integration
retains a rename/save/Discard/Undo/download/file-import path across editor,
storage, preview and inspector. Shared footer styling, native disclosures and
standalone-page layout checks remain with preview/export fixtures.

`wireframe_review.py` owns read-only mirror structure, geometry/paint parity,
container annotations, inert controls, navigation/disclosures, viewport choices,
legacy compatibility, fidelity tabs and downloads. Its fixtures initialize sample,
stage, viewport and High Fidelity independently. Additional Basic/Advanced cases
cover inactive JSON-file replacement, current text/type on lesson entry, original
frame/document identity, view preferences staying outside JSON/autosave, live
comparison, downloaded fidelities and loading the previous local project.
Integration retains Architecture editing through wireframe rendering, local-view
changes, both fidelity downloads and live comparison. The early Typography and
course-order matrices now live in the independent Typography suite.

`palette_review.py`, `contrast_review.py` and `components_review.py` own the
colour-source/background, contrast inventory/repair and component-state matrices.
Each initializes its own model, viewport, inspector and lesson, with real local
projects wherever persistence is asserted. Palette's candidate checks call the
read-only contrast API without importing the contrast suite. Shared standalone
system comparisons now live in the standalone-export suite.
Integration retains an anchor/edit/autosave, reviewed semantic fix, component
override/button export and combined JSON-file restore journey. Its Studio
appearance persistence helper selects the actual chosen saved project, rather
than relying on the first entry in storage.

`typography_review.py` owns system/local-fixture fonts, font validation and retry,
scales, tracking, leading, specimen rendering, guided stages, comparison-only
controls and the early Typography/course-order/wireframe bridge. Font requests
use the runner's local fixtures; real CDN validation remains optional and separate.
`spacing_review.py` owns region padding, token chart arithmetic, spacing lesson
comparisons, reflection/session boundaries and optional plain-CSS practice.
Both initialize their own sample, viewport, Studio appearance, lesson, inspector
and fluid preview. Integration keeps a combined font/spacing edit, local autosave,
comparison/inspection, website download, JSON-file restore and sample-switch
journey. Shared responsive layout and standalone export matrices now have their
own focused suites.

`responsive_preview_review.py` owns fixed/fluid viewport sizing, workspace reflow,
live browsing/form/disclosure state, page-theme synchronization, safe preview
rendering and responsive control validation, persistence and breakpoint matrices.
`standalone_exports_review.py` owns Basic/Advanced markup and sample switching,
linked HTML/CSS downloads, inspector/file parity, rendered layout, system-style
parity and native navigation, forms and disclosures. Each suite starts its groups
with explicit model, viewport, Studio appearance, lesson and inspector settings;
the Advanced markup fixture explicitly selects its tested button size and width.
Integration retains Basic/Advanced source edits through local autosave, a mobile
preview with entered form data, separate HTML/CSS downloads rendered at configured
cutoffs and JSON-file restoration protecting the saved project library.

`.github/workflows/ci.yml` runs the dependency-free structure and isolated-profile
Chrome browser checks on pull requests and exposes the same job via `workflow_call`.
`scripts/review_suites.py` is the single offline browser catalogue for CI, local
full-check execution and import-safety checks. Runner contracts ensure every
review file is registered exactly once, with live-font validation classified
separately. `--matrix` prints JSON without importing or starting any browser suite;
the default command runs all local checks in independent sequential processes,
continues after failures and returns a failing status if any command failed.
CI runs structure and runner checks first, then a matrix of all 18 offline browser
suites, including actual reduced-motion/forced-colour modes. It keeps at most
three jobs active, does not cancel remaining jobs after a failure and retains
failed-suite logs for seven days. Each browser job has a 25-minute limit so the
two-launch media suite can use both 660-second runner budgets. This replaces the
old ten-minute limit shared by all suites. Live Google Fonts downloads remain an
optional external-service check. [Test coverage](TEST_COVERAGE.md) records suite
ownership, baseline reconciliation and explicit manual/hosted-CI gaps.
The existing `structure` job name is retained as an unconditional final gate over
the checks job and complete browser matrix. A failed or skipped prerequisite
fails that gate, preserving the meaning of the existing required-check context.
`.github/workflows/pages.yml` calls it for main pushes and manual publishing, with
the deployment job requiring successful validation through `needs: validate`.
Both checkouts use the triggering revision. Validation receives only read access
to repository contents; the deployment retains Pages and identity-token permissions.
No application build step or runtime dependency is introduced. This follows
[GitHub's reusable workflow model](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows).

## Project identity and teaching model

The public name is Web Design System Studio. The header, page title,
footer, README and generated CSS attribution use it. Existing `DSStudio` APIs,
DOM IDs, local-storage keys, JSON format and download filenames remain compatible.
Historical audits and user-authored root sample snapshots retain their names.
The workspace starts directly below the app header, without a separate branded
hero/title or tagline. Build your design system is its primary heading, followed
by the existing step/lesson/inspection guidance in normal foreground text.

The preview includes a closed, static HTML/DOM/CSS introduction: HTML is parsed
into node objects; valid nesting establishes tree relationships; CSS selectors
match elements and declarations assign presentation/layout property values.
It distinguishes CSS properties from DOM object properties and methods, with
escaped HTML and a token-based CSS example. No imported content is executed.
The explanation follows the WHATWG HTML/DOM and W3C Selectors/Cascade standards.

## Studio appearance and project styling

`studio-appearance.js` loads after the registry and before core state. It owns the
root `data-theme` and `color-scheme`, the header toggle and the validated local
`dss-studio-appearance` preference (light/dark, default light). Blocked storage
falls back to session operation. Cross-tab storage changes refresh appearance
without invoking project apply/render/autosave. This preference is outside state,
project JSON and website exports; project reset/import/load leave it alone.

`studio-appearance.css` defines fixed `--studio-*` colour tokens with light/dark
values and aliases the existing UI role names to them. Studio foundation values
remain the fixed defaults in `base-tokens.css`. Core `apply()` writes project
roles/foundations as `--project-*` variables and root `data-project-theme` instead
of replacing Studio values. The advanced feedback writer uses the same prefix;
its link underline setting is scoped to project examples. Demo-only advanced and
font variables continue to supply their existing specimens.

Authored `.project-preview` regions and the button/type/state specimen selectors
map project variables into local role names, font size, leading, tracking and
native control colour scheme. Lesson prose, captions around typography samples,
readouts, navigation, controls and code panels retain Studio styling. Swatch and
background illustrations retain their explicit validated paint values. The real
page remains isolated in its iframe and uses the unchanged export generators.
`state.theme` remains the shared project choice for the preview, inspector and
guided editor, persisted with projects and emitted into standalone HTML. Both
sample modes continue to share one project; CSS still exports both themes.

## Local CSS first and optional page utilities

`page-utilities.js` exposes a fixed 20-rule vocabulary for lesson examples only.
It does not register an export contributor or wrap `cssExport()`. Neither sample
adds its exercise utility classes to exported HTML. The live inspector, preview
and downloaded website therefore share the same component HTML and local CSS,
with normalized project tokens supplying values. The vocabulary covers Flexbox/
Grid, spacing, theme colours, corners and fonts. No imported names, selectors or
declarations are accepted, and there is no framework, compiler, network dependency
or project-schema change.

The optional exercise instructs learners to append a selected rule to a practice
copy of the local stylesheet and add its class in the copied HTML. Equal-specificity
conflicts use stylesheet order; HTML class order has no effect. Higher-specificity
component rules still apply. These rules are a bounded teaching vocabulary, not
a general Tailwind implementation or a new cascade-layer contract.

`utility-lesson.js` initializes after `spacing-lesson.js` and appends a labelled
section after its five teaching parts. Its stylesheet affects Studio teaching UI
only. The initial view teaches semantic HTML, a linked local stylesheet and the
base `.card` rule read directly from the current CSS export. A minimal example
is labelled separately from the complete page. Local CSS is the course's starting
approach, with reusable component rules and shared tokens; it remains a complete
route to a finished website.

The lesson explicitly orders the learning transition: local component
`.card { padding: var(--space-6); }`, locally authored utility
`.p-6 { padding: var(--space-6); }`, then Tailwind-generated `p-6` in a separate
practice project. It explains that tokens hold decisions and classes apply them
to HTML. The supplied Tailwind source maps `--spacing` to `--space-unit`, retaining
the same six-unit spacing decision. Palette/token guidance, the catalogue,
workflow, Deliver and the exported Advanced learning FAQ reinforce that sequence;
they do not introduce a framework dependency into the website.

A closed native disclosure introduces optional utility practice, keeping the
20-class vocabulary in a second closed disclosure. Five class choices (including
both p-6 and p-4) connect an authored practice rule to a current-theme source token.
Separate code panels show the actual exported article and a prospective practice
tag with only the selected utility added. Measurements explicitly describe the
unchanged component preview, before the exercise. Reads use fixed IDs and the
shared token parser; project/output strings enter via
textContent. Token parsing is cached by exported CSS and unchanged text nodes
survive refresh. Stage/preview/disclosure events refresh the visible lesson.
The initial Inspect card CSS action opens the real full stylesheet at `.card`.
Practice inspection actions also open the real component HTML/CSS, never a
substitute exercise export. Existing configuration routes retain shared state;
the preview action focuses the article without changing project data. Selection
is session UI only. Opening utility practice refreshes measurements. The vocabulary
table scrolls locally on narrow screens. An ordinary fragment link leads to the
Tailwind section in Deliver; its return link leads back to this local CSS lesson.
Existing section navigation activates the corresponding stage without changing
project values or replacing the preview document.

## Tailwind mapping lesson and optional source target

`tailwind-bridge.js` registers after the learning/spacing lessons and before
section return links. It appends a section inside Deliver's existing centre
lesson, retaining the twelve stages and existing inspector languages. Scoped
`tailwind-bridge.css` styles that teaching UI only. This module leaves the existing
HTML/CSS generators, website classes, project schema and preview document unchanged.

The introduction makes the framework exercise optional and connects locally
authored utilities with Tailwind-generated utilities. It directs students to a
separate practice project, the mapped theme and one article, then asks them to
compare generated rules and computed properties before extending the example.
Custom utility names need that theme mapping. No full website conversion or
automatic migration is offered, and local CSS remains a valid finished result.

The module reads actual CSS export declarations through `dssReadTokens`, keeping
last definitions per light/base and dark scope. A fixed map traces 24 source
variables into Tailwind v4 names, plus two saved responsive cutoff values. The
source includes mapped raw tokens in a theme layer, `@theme inline` aliases,
literal breakpoint declarations and an attribute-based custom dark variant.
It is a self-contained foundation snapshot without page component rules, font
requests or automatic HTML conversion. Distinct aliases avoid self-references
and the existing text-colour/font-size namespace ambiguity. Tailwind defaults
remain available alongside mapped theme names.

`DSStudio.tailwind.source()` reads the latest settings without mutating project
state. Its output is excluded from the registry's shared CSS export. Copy and
`tailwind-theme.css` download actions use current source, retain the website
inspector and explain compilation in the consuming project's Tailwind v4 build.
Font files/links remain the consuming project's responsibility. Copy failure
opens the source for manual selection; delayed feedback identifies an earlier
snapshot if settings changed during the clipboard request.

Display refreshes use the shared lesson-phase scheduler after output updates and run while
Deliver is open; opening it and explicit source actions refresh immediately.
Parsing is cached by unchanged exported CSS. Table rows and unchanged source
text nodes survive updates. Project values use textContent, with no CSS evaluation
or arbitrary imported token names/selectors. The table scrolls locally at narrow
widths with a labelled focusable region. No Tailwind code executes in the Studio.

This additive lesson/source phase precedes the component/cascade cleanup proposed
in the page export review, following the user's preference to preserve existing
page CSS. Compilation and utility/component integration are separate verification
work; mapping-source checks alone do not establish full Tailwind rendering parity.

## Wizard configuration and centre lessons

`spacing-lesson.js` registers after studio learning/example connections, with
`spacing-lesson.css` scoped to its single lesson. It replaces the short Spacing
lesson with authored Understand/Try/Observe/Inspect/Reflect content populated from
the current exports. It reads base token declarations via `dssReadTokens`, resolves
only pixel values or the generator's fixed spacing multiplication syntax, and
shows literal formulas rather than evaluating CSS or executing project data.
All dynamic output enters through textContent; fixed section IDs select the
actual opening HTML tag and CSS rules in Basic/Advanced. Basic's padding overrides
are collected from the exported responsive section and matched with native
matchMedia. The explanation also reports measured preview padding. This is a
bounded reader for the authored samples, not a general CSS cascade interpreter.

Its before/now comparison starts on lesson entry, can be rebased explicitly, and
remains private session UI state with optional reflection text. Replacing the
core state object on import/local load/reset invalidates both; explicit reset/
import events also cover identical values. Updates use the shared lesson phase,
after pending preview jobs, rather than nested microtasks to guess when the
preview has settled. Unchanged text nodes stay intact, preserving selection and focus.

`syncResponsivePreview()` emits `preview:change` after measurement/readout updates;
inspector layout changes call that same measurement function. The lesson listens
to this and `inspector:change`, stage/disclosure entry and iframe load. It needs
no extra render wrapper or independent resize observer. Preset, window and
inspector width changes update the applicable padding rule without changing the
comparison. Inspect actions keep complete-file generation and explicit language.
Queued example selection is invalidated by subsequent navigation/code focus.

An optional fixed `[data-stage-controls]` anchor in an authored lesson tells
studio learning where its real control pane belongs on narrow screens. The
`lesson:content` event refreshes placement after content initializes. For Spacing,
the controls join Try; desktop restores the original sidebar placeholder. Control
IDs, source routes and listeners are preserved, with no duplicate editors.

App spacing is scoped to `.layout` in `learning-path.css`: 8px for small gaps,
16px for normal gaps, 24px between groups and responsive 16–24px panel insets.
Desktop wizard panes have a 32px gap, divider and 24px inset before each step,
separating the builder introduction/navigation from editing. Fields, planning
editors, summaries, lesson cards and inspector controls reuse that rhythm.
These app-only values do not enter generated website CSS or saved design data.

`studio-learning.js` reorganizes existing control nodes after
the other modules initialize. It preserves their IDs, event handlers and state
paths while placing font, responsive, layout and accessibility settings inside
the twelve-step wizard. Hidden compatibility nodes retain legacy module bindings.
The centre presents the current short lesson, its task and contextual output
actions; deeper material lives in More about disclosures. Workflow, catalogue
and states remain secondary references rather than a second numbered curriculum.

`DSStudio.stages` in `studio-registry.js` defines the twelve stable stage IDs,
labels, phases, lesson IDs, tasks and CSS declaration targets. The existing
`dssShowWizardStep(n, focus)` updates controls, location and `DSStudio.activeStage`,
then emits `stage:change`. `studio-learning.js` selects the matching lesson and
focuses its heading on deliberate navigation. Startup expands the active lesson
(Brief on a normal load) as well as the preview, without moving focus. Reloading
a step's section fragment activates and opens that lesson after the registry's
`ready` event, so early fragment scrolling cannot be undone by lesson initialization.
The same activation
path opens matching lessons for all twelve steps; navigation never marks
completion. The Choose a step disclosure starts expanded. Step selection and
rerendering preserve its native open/collapsed state until the user changes it;
a fresh page load starts expanded again. Numeric indices and existing
control/lesson IDs remain compatible.
`stageOrder` and `orderedStages` define display order independently of the stable
internal indices. `position` supplies visible numbers. Previous/Next, progress,
step buttons, phase groups and centre section order follow that sequence. Prototype
is last, after Deliver; Plan contains Brief, Architecture, Typography and Wireframe.
The opening display order is `[0,1,5,2,4]`: Brief, Architecture, Typography (Step 3),
Wireframe (Step 4), Palette (Step 5). Stable typography/wireframe/palette indices
remain 5/2/4, so saved view routes and Configure links retain their targets. Script
load order is unchanged. Typography establishes a working baseline from actual
content; the wireframe validates its wrapping and spatial effects before palette
refinement. The final Prototype
review actions open the existing preview and inspector or route to Deliver without
replacing the iframe or project. Earlier task sketches remain in a disclosure.

The Brief control pane (`#brief-editor`) stays directly after its centre lesson
at every width. It retains the seven original prompt fields and starting preset.
Project name (`#jProject`) belongs to My local projects outside step-specific
panes, sharing the original state, autosave, load/reset and export bindings.
Other control panes move after their lesson at 900px and below.
Comment placeholders restore those panes to the sidebar at wider widths; IDs, bindings
and values are unchanged. Previous/Next moves after the output on narrow screens.
Architecture's full editor stays in its centre workspace at every width; only
its short guidance/shortcut pane participates in the sidebar relocation.
The preview iframe never moves: it remains first in the centre above the lessons,
preserving its browsing context. Other sections remain visible as collapsed
disclosures. `DSStudio.activateLesson` lets existing fragment and laboratory
routes select a collapsed lesson before revealing the target.
Ordinary edits preserve control focus and do not invoke stage navigation.

`section-navigation.js` initializes after the lessons, background/spacing modules
and control placement. It appends one flow-layout, right-aligned return link to
each `.studio-section > .panel`, wizard pane and inspector. It does not add links
to nested cards or sample generators. Native anchors target the focusable studio
banner `#studio-home`; unmodified activation explicitly scrolls the outer studio
window to zero and focuses the banner without scrolling, since a sticky banner
alone cannot reliably represent the document start. It always returns instantly,
including under reduced-motion preferences, and preserves stage, disclosures,
project/library data, inspector state and iframe identity. Modified clicks retain
native link behavior. Links have text, decorative arrows, underlines and at least
44px targets; the focused destination has an inset outline. Studio-only CSS and
the module add no saved state or generated CSS/HTML. Node placement survives the
existing narrow-screen control moves and text-only lesson refreshes.

`learning-path.js` now supplies contextual example connections only. Its former
beginner task selector, progress, entry button and workspace bar are removed.
The four useful tasks are in Buttons, Spacing, Responsive and Deliver. Basic and
Advanced remain sample choices beside the page; navigation does not switch them.
The selected example and picking flag are session UI state, excluded from project
JSON and generated files. A step change selects its example and frames a matching
page target where available without moving keyboard focus.

`DSStudio.inspector.show()` selects output in the inspector to the right of the centre,
preserving language/section by default. Explicit callers select complete CSS,
HTML or project JSON and an optional search string. JSON always uses the complete
project generator. Legacy centre code controls remain hidden to preserve existing
core bindings; the visible centre output actions all use the shared inspector.
The inspector is one native `details` element with a `summary` heading, matching
the preview's disclosure arrow in open and closed states. It starts collapsed
above the preview, with its code body hidden by the browser and its column
released. `setCollapsed` synchronizes the native open property, dock/workspace
classes and the optional internal Collapse code control. Native toggle events
update the same path; contextual Inspect actions open it through the existing
API. Collapsing with focus inside returns focus to its summary and brings it into view.
Visibility stays transient and is excluded from project JSON. Sample
tabs label the preview panel, separately
from the inspector's three language tabs. Sticky offsets now use the header alone.

Readiness acknowledgements clear after project changes, reset, imports or local
project loads, including loading identical data. Practice progress was removed.
Header and Deliver project JSON downloads share filename and payload policy.

The inspector emits `inspector:change` after refresh. The new module subscribes
instead of adding another render wrapper. Fixed example metadata maps authored
element IDs/selectors to tokens; rule text and theme-scoped declaration values
come from the current export/catalogue. Configure uses `dssConfigureToken()`.
Study-section changes update the corresponding example. Formula tokens retain
their exported `calc()` expressions rather than pretending to be resolved pixels.

Preview selection is explicitly enabled, Basic-only and consumed once. The
preview's existing click handler emits `preview:example` for fixed example IDs
instead of executing that click's normal action. Escape in the preview emits a
cancel event; parent Escape, stopping selection and mode changes also cancel it.
The example selector supplies a keyboard alternative. No teaching controls,
scripts or selection state are added to exported pages.

`docs/LEARNER_TRIAL.md` contains the unrun participant protocol and observation
sheet. Automated checks are not learner-study results. The growing browser suite
has a 90-second virtual-time budget and a
240-second process timeout; the prior standard timeout was exhausted during the
product review even though its unchanged rerun passed.

`token-catalogue.js` reads actual exported declarations through `dssReadTokens()`.
Its `dssTokenSource(row)` maps each row to a wizard step/control and records
whether it is direct, derived or an alias. `dssConfigureToken()` reveals the
source, choosing the theme/variant for scoped colours. Derived ramps, scales and
aliases edit their source. Coverage tests require every generated row to have a
source inside the expected wizard pane. See
`docs/TOKEN_CONFIGURATION_2026-10-20.md` for the complete family map.

`state.headingLeading` is a validated foundation (1–1.6, default 1.18), shared by
studio typography, generated CSS, preview and saved projects. Older imports use
the existing default. No arbitrary imported CSS overrides were introduced.

## Principles

1. **Zero build, no runtime libraries.** Plain HTML, CSS and classic scripts. System-font mode is offline; optional curated Google Fonts load external font assets. Contributors need only a browser and a static server.
2. **One source of truth.** Foundation values live in a single state object; CSS preview, export, token catalogue and clamp explorer all derive from it.
3. **Feature modules over a shared core.** The intended extension API is `DSStudio`; existing features still share globals while migration is pending.
4. **Imported data is data.** JSON import is validated and never executed.

## Layers

| Layer | Files | Responsibility |
|---|---|---|
| Markup | `index.html` | Sections, landmarks, asset manifest |
| Tokens & base | `src/css/base-tokens.css`, `layout.css` | `:root` custom properties, themes, page layout |
| Core | `src/js/studio-registry.js`, `export-pipeline.js`, `view-updates.js`, `project-model.js`, `core-state.js` | Registry/events, export assembly, view scheduling, pure project codec, state/DOM adapters |
| Features | `responsive-design`, `design-process`, `brand-palette`, `button-state-practices`, `font-sources`, `css-dock`, `advanced-params`, `journey-library`, `button-design`, `sample-homepage`, `basic-homepage`, `responsive-preview`, `website-export`, `oklch-lab`, `token-catalogue`, `clamp-explorer`, `contrast-audit`, `colour-repair`, `button-contrast`, `typography-controls`, `section-accordions` | One user-facing capability each |

Load order is the order in `index.html`. Scripts are `defer`red; `DSStudio.start()` runs on `DOMContentLoaded`. Export and view services load after the registry and before core/features.

## Adding a feature module

1. Create `src/css/my-feature.css` and `src/js/my-feature.js`.
2. Register the module:

   ```js
   'use strict';
   DSStudio.register({
     id: 'my-feature',
     title: 'My feature',
     init({ studio }) {
       // bind to DOM, subscribe: studio.on('ready', ...)
       // Optional website styles, separate from the Studio UI stylesheet:
       studio.exports.registerCss({
         id: 'my-feature', stage: 'components', order: 30,
         generate() { return '\n/* website component styles */\n'; }
       });
     }
   });
   ```
3. Add the `<link>` / `<script defer>` tags to `index.html` and the markup section. Register website CSS explicitly in the appropriate export stage; Studio-only styles do not belong in website exports.
4. Run the checks listed in CONTRIBUTING, including focused export checks for generated-output changes.

## Known debt (migration path)

Feature scripts still share model/calculation globals and some navigation/palette
adapters. Core view and export entry points are now stable; features use lifecycle
subscriptions and explicit export contributors. Further module isolation, finer
view dependencies and CSS rule ownership remain work. Native ES modules are a
later option once globals are isolated; no bundler or runtime library is required.

## Ordered website export pipeline

`export-pipeline.js` provides `DSStudio.exports` before core state evaluates.
Core retains the stable public `cssExport()` and `htmlExport()` functions, which
delegate using the current validated sample mode. No feature captures or replaces
either function. The structure checker rejects reassignment and checks the
registry/pipeline/core script order.

Shared CSS contributors have an authored `id`, `stage`, numeric `order` and
`generate()` callback. The pipeline sorts by the following stages, then order,
then lexical id (without locale collation); registration order does not define the cascade.

| Stage | Current contributors |
| --- | --- |
| `foundation` | Core ramps, semantic roles, typography, spacing and base components |
| `components` | Advanced component rules (10), then button rules (20) |
| `states` | General and button state shade ramps |
| `planning` | Shared planning artifact styles |
| `layout` | Shared region padding, navigation and focus rules |

`sharedCss()` assembles exactly those fragments. `DSStudio.samples.foundationCss`
remains its compatibility alias: the historical name includes shared component,
state, planning and layout CSS as well as raw foundations. Selected page CSS is
excluded, so Basic never captures an Advanced page stylesheet. Each sample
registers its own CSS and edited HTML renderers through `registerSample()`.
Basic keeps its readable page/footer formatting; Advanced keeps its own page
CSS followed by the shared footer generator. The pipeline concatenates raw
fragments without inserting, removing or reformatting separators.

The tiny core fallback sample is for initialization only. Until Basic registers,
Advanced supplies the same intermediate startup fallback as before. Only Basic
and Advanced are accepted as output modes; fallback is not a saved/user choice.
The actual-content inventory continues to use `advancedSourceHtml/basicSourceHtml`
and `advancedHtml/basicHtml` directly. Website text validation/escaping and the
same raw export APIs remain shared by previews, inspectors and downloads.

Registration rejects invalid/duplicate contributors and samples. Generation
checks string results and propagates errors instead of returning a partial file.
Recursion guards recover in `finally`. Removal handles cannot remove a later
registration that reused an id. `describe()` returns detached metadata;
`create()` provides an independent pipeline for focused tests or future targets.
Callbacks are authored code only; imported JSON supplies no registrations,
selectors, ordering rules or executable content.

The legacy `DSStudio.collectCss()` helper is retained for compatibility as a
standalone module-fragment collector. It is not called by the website pipeline;
an `exportCss` property on a UI module does not append website styles. Use explicit
contributors to avoid a second, implicit assembly path.

`scripts/fixtures/export_baseline.json` contains SHA-256/byte-count snapshots
captured from the wrapper implementation before migration. The export suite
checks CSS, HTML and shared CSS across 16 cases (both samples/themes, custom
tokens/components, Google font markup and edited text), plus pipeline contracts.
Only intentionally reviewed output changes should use
`python scripts/export_pipeline_review.py --capture` to replace that baseline.
This phase preserves generated bytes and cascade behavior; it does not
consolidate overlapping component selectors or introduce cascade layers.

## View lifecycle and scheduled updates

Core owns the stable `apply`, `renderType` and `renderCode` functions. Features
subscribe to explicit events instead of replacing those functions. The structure
checker rejects reassignment of these three entry points and checks that the
registry, scheduler and core appear in the required order.

| Event | Synchronous contract |
| --- | --- |
| `foundation:before` | Synchronize legacy tracking before foundation/export reads. |
| `type:updated` | Core type specimens are updated; synchronize clamp controls. |
| `output:prepare` | Prepare the actual-content inventory before artifact/export reads. |
| `output:controls` | Synchronize font, sample-mode and responsive controls. |
| `output:artifacts` | Refresh cached planning artifacts before code/inspector reads. |
| `output:updated` | Core code is current; refresh inspectors/editors and invalidate background views. |
| `foundation:updated` | Foundation apply is complete; synchronize guided fields, buttons and local autosave. |

These events preserve immediate control bindings, editor dirty/undo guards and
local save behavior. A callback must not call the same lifecycle entry point it
observes. Export generation remains synchronous and reads the current model;
copy/download actions do not wait for a rendered preview.

`DSStudio.views.subscribe({id, phase, events, run})` registers an authored task and
returns `{schedule, dispose}`. Repeated invalidations of a pending task coalesce
into one microtask update. The `preview` phase runs the responsive document and
active wireframe first; the `lesson` phase then refreshes Typography, Spacing,
utility and Tailwind views. Each task keeps its existing visibility guards.
Typography listens to preview measurements as well as type/output/foundation
changes, so component specimens read the latest computed styles. Project-sync
and explicit local navigation still refresh its controls immediately.

Tasks read the current model when they run; pending work never retains a project
snapshot that could outlive import/reset. Preview-triggered lesson invalidation
joins the same flush. Invalidating an earlier/already-run task defers it to a new
flush rather than recursively rendering. Disposal cancels pending work and event
subscriptions, and errors are reported without blocking unrelated views.
`DSStudio.views.flush()` provides a synchronous drain of the current phases when
a caller specifically needs it; it does not recursively drain new earlier-phase
work. Normal interaction uses the queued scheduler.

This batches work within a JavaScript turn, not across separate slider events or
animation frames. Inspectors, control synchronization and persistence remain
synchronous. Contrast's existing coalescer and focus/navigation continuations
remain separate. Export assembly uses the pipeline above; navigation adapters
remain separate work.
No performance or full accessibility claim follows from batching alone.

`python scripts/view_updates_review.py` independently checks phase ordering,
coalescing, disposal, error isolation, current-state reads, synchronous exports
and the Typography component-context regression. CI runs it before the full
browser integration suite.

## Project codec and replacement lifecycle

`project-model.js` loads after the data services and before core state. Its
`DSStudio.project` API creates fresh defaults, normalizes imported data and
produces detached snapshots or project JSON without touching the DOM, storage,
active state or render functions. Feature data normalizers remain the owners of
their bounded planning, font, brand and responsive structures. Advanced control
ranges and enums now have data definitions; imports no longer read live controls.
Numeric UI bounds consume those definitions and regression checks compare the
authored enum choices with the same rules.

`core-state.js` retains `importConfig`, `resetStudio`, `projectJson` and the new
`projectSnapshot` adapters. Import validates the complete project before replacing
`state` and `clampConfig`. The `project:install` event is exclusively for installing
model references or clearing session flags: it must not render, save or navigate.
Advanced and button editors retain their familiar local variables as references
to `state.advanced` and `state.buttonDesign`. Font fallback comparison clears in
this phase. Only after all references are installed does `project:sync` refresh
controls/views, followed by reset notifications when applicable and `apply()`.
Button rendering no longer copies settings into saved state.

`DSStudio.isReplacingProject()` stays true throughout synchronous replacement,
including observers, and clears in `finally`. Local autosave checks this guard
instead of wrapping import. Browser-local saves consume detached snapshots
directly; JSON inspector/downloads use the same codec. The library still owns
active-project identity and detaches it on New/reset and file-import completion.
Existing `dss:reset`/`dss:imported` UI notifications retain their meanings.

The JSON schema remains 2.9 and the storage key is unchanged. Legacy sample-mode
and tracking migration remains based on field presence, preserving historical
files whose schema labels did not track every added field. This is not a new
version-dispatch policy. Background views and export assembly use the services
above; finer update dependencies and remaining render-time legacy tracking
synchronization are subsequent work.

`python scripts/project_model_review.py` runs a short, independent scenario through
the existing isolated Chrome runner. It checks complete models during every
import/reset render, rendering purity for button settings, DOM-free data handling,
legacy/malformed data, detached objects, failed normalization and autosave guards.
CI runs it alongside the full integration suite; no Node or runtime library is
required.

## Project planning workflow

### Content structure workspace

Content structure is the primary Architecture editor; IA names the organising
activity rather than a second required inventory. `studio-learning.js` provides
one combined introduction/learning disclosure and wraps the duplicate full saved
artifact in `#architecture-saved-review`, named Review the Content Plan and
initially closed. It also contains the existing content Save/Discard/Restore area
and its status feedback. `#architecture-sitemap`
is a separate native disclosure, opened by Review visitor sitemap or an item's
destination shortcut. Its inclusion controls and sole live visitor preview stay
together. `design-process.js` extracts that preview from the existing escaped
studio artifact into `#architecture-sitemap-preview`; exports continue to consume
the complete original artifact renderer. The saved review retains the full
content tree and guidance, without duplicating the studio visitor preview.

Add uses `#ia-add-placement` and one `#ia-add` button, replacing the three previous
add-button IDs while retaining inside/beside/top-level behavior and depth bounds.
Organise content includes keyboard-operable reorder/delete and tree expansion
utilities. Core properties remain visible; the optional related section/reference
and destination shortcut live in `#ia-related-section`, opening for link items.
Proposal inclusion retains the original null versus intentionally empty behavior.
Restore current sample content shares Save/review's action row with Save and
Discard. Its nearby scope/Undo help is connected with aria-describedby. The
original dirty-form guard, per-sample restoration and Undo handler are unchanged.
Advanced tools retains project-data inspection. The Architecture-specific Inspect
footer HTML shortcut is removed; the main inspector still supports footer HTML.
Source selection is the first field in Visitor sitemap. Advanced sitemap options
contains only the text editor and is hidden for page-derived navigation, where
there are no applicable advanced controls. Selecting a custom plan opens its
destination editor without automatically opening Advanced options. The custom destination
editor is now outside Advanced options and visible when custom source is active.

`section-sitemap.js` exposes `createOutline`, a shared native details/list renderer
for both page-derived and custom destinations. It reconciles stable IDs and moves
rows only when their position changes, preserving checkbox focus and branch open
state. Search reveals matching destinations and ancestors; clearing it restores
the pre-search expansion. Names use textContent; sources remain the existing
validated page inventory and custom destination model. The two sources share the
same responsive outline/properties presentation while keeping their data rules.
The single preview host follows the active source's workspace without recreation.
At 58rem of available Architecture width, its grid uses Find destination,
Selected destination and Visitor sitemap preview columns. At 46–58rem the
preview spans below the two editing columns; below that all three stack in DOM
order. The studio-only preview region is focusable with bounded vertical scrolling;
the complete shared export artifact is unchanged. Ordinary renders do not move
an already correctly placed preview host, preserving focus and scroll.

Page-derived properties show a read-only label/path, immediate inclusion and an
authored-target preview link through the existing delegated preview handler.
Custom properties retain label/parent/type/target editing and immediate inclusion.
`site-builder.js` adds Save/Discard protection for dirty custom forms on selection,
creation, reorder/delete, inclusion and Undo. `DSStudio.sitemapEditor.canLeave`
also guards source switching; imports, resets and sample switches load their
corresponding forms. The old path select is hidden as an internal compatibility
bridge for existing selection routes; user-facing selection uses the outline.
No project-schema, sitemap generation or export changes are introduced.

Architecture uses a centre-pane workspace rather than a full CRUD form in the
left wizard. `studio-learning.js` moves the existing content editor, section
sitemap controls and legacy custom/text editors into `#architecture-workspace`,
before the saved planning artifact. These nodes retain their original IDs,
listeners and shared project state; the short wizard pane retains its objective,
workspace shortcut and review checklist at every breakpoint. The content tree
and selected form use a container-query split at 46rem of workspace width and
stack below that width, including when the code inspector reduces available room.
Longer Architecture guidance, Add item choices and branch actions use native
disclosures. Save, Discard and content Undo remain outside those action disclosures.
The property editor stays visible without a disclosure or local step numbers.
Move/remove controls and Undo live with the content tree. The content grid contains
the tree/browser with Save and review beneath its branch tools, beside the
property form. Develop the content plan leads the Architecture workspace directly
after its header and before Content structure. Its controls explicitly associate
with ia-form; both editing surfaces handle dirty state and invalid fields.
A selected-item path keeps the top planning disclosure's context clear. Review
and Save Content Plan retains the IA/sitemap guidance and complete saved artifact.
The guidance has its own stable host, populated by the existing
artifact renderer, so later model renders retain this order without replacing
the action nodes or adding a duplicate introduction. Exports keep the original
complete artifact. Its external submit button keeps
`form="ia-form"` so native validation and the existing handler remain authoritative.
The first unsaved edit opens the review disclosure without moving field focus.
Save, Discard and dirty-form guards reveal it before focusing Save. Manually
collapsing it preserves form values and project data; ordinary rendering retains
its disclosure state. Save-area styles are independent of the content-editor
ancestor so moved actions keep their responsive wrapping and touch targets.

The content editor guards selection, creation, move/delete, Undo and restoration
while its form is dirty, announces Save or discard and focuses Save. Same-content
refreshes and returning to the step preserve the form. Successful saves or Discard
clear the guard. A changed sample/content snapshot, reset or import loads the
corresponding form; unsaved forms are not persisted as project data. Sitemap-only
changes preserve unsaved content forms. No project schema or export editor is added.

The primary Architecture control is now the content outline, distinct from the
visitor sitemap's destination hierarchy described below. `content-architecture.js`
loads after `design-process.js` and before core state so the shared normalizer can
validate additive `designProcess.contentPlan.basic/advanced` data. A null mode
means use the current sample inventory; an array is a saved content planning
snapshot, including an intentionally empty array.

`sample-homepage.js` and `basic-homepage.js` expose their local authored generators
as `DSStudio.samples.advancedHtml/basicHtml`. The content model parses these inert
strings with DOMParser and visits semantic regions/groups/content, omitting CSS
wrappers, scripts, styles and decorative SVG internals. It captures headings,
paragraphs, CTAs and fragment references, figures/alternative text/captions,
lists/terms/tables, form controls/options and shared Header/Footer content. Header
logo/wordmark and Home/Hero are explicit. Numeric progress values become strings.
Default Basic has 139 entries and Advanced 395, with five levels in each.

The IA lesson within the Advanced sample is represented as a generated planning
view, and the footer sitemap as generated destinations. Their recursive contents
are not inventoried, preventing the content model from containing itself. The
collector suppresses content-map generation during source inspection, caches each
mode's source signature including the separate Advanced settings object, and uses parent/child indexes for rendering/normalization.
The UI defers refresh while Architecture is inactive and catches up on stage entry.

Content records have stable `content-*` IDs, parentId, label, type
(region/page/section/group/text/image/link/field), actual value, textual source
reference, sourceKey, nullable draft, planning status and notes. Destination
references use that sample's fixed-ID allowlist. Source keys associate saved
records with current actual values independently of edited labels/parents. A
missing source is identified in the selected-entry editor. New source items are
available through explicit sample restoration rather than silently undoing a
learner's deliberate deletions.

Imported rows are bounded to 1,000 per mode and twelve levels; cycles/duplicate IDs
are rejected, missing parents are promoted to roots, and valid rows are ordered by
parent/sibling relationships. Label/value/reference/notes lengths are bounded to
120/2,400/1,000/1,200 characters. Draft is null or a bounded string; empty draft is
distinct from no draft. Content is always escaped or set with textContent/value.
Each mode's normalized plan is also bounded to 500,000 serialized characters;
structural edits that exceed the budget are rejected rather than partially saved.
Project JSON uploads accept up to 6 MB so bounded content plans, text and layout edits can round-trip through
the real file picker; this replaces the token-only application's 100 KB limit.
Imported source keys are map lookups, never selectors or executable code. Imported
references are displayed as text, never assigned to href or fetched. No imported
HTML is passed to the collector or inserted into the document.

For old projects without contentPlan, the model inventories actual sample content.
Complete sample outlines keep their existing destination metadata. Custom outlines
are incorporated into the content plan with `content-legacy-ia-N` identities;
matching canonical sections retain their actual child content, while unknown
entries remain planned. Aliases and explicit pageLinks resolve through the same
`DSStudio.process.destinationId()` helper as sitemap output. Repeated references to
a claimed destination become links rather than duplicate destination subtrees.

`content-outline.js` initializes after site-builder and before studio-learning. It
replaces the primary flat IA interaction with native nested details/lists and
selection buttons, search with ancestor context, expand/collapse, a labelled detail
form, child/sibling/root creation, subtree reparent/reorder/delete and one-change
Undo. IDs preserve identity with repeated labels, rename and moves. Parent options
omit descendants and moves beyond the depth bound; submit revalidates forged
choices. Website content edits authored text; draft text/status/notes plan changes
separately. Per-mode snapshots persist via existing JSON/local
flows. Restoration affects only the current mode and can be undone. Mode changes,
reset/import and external planning changes clear incompatible Undo history.

The selected-item form shows Website content and Understand this item beside the
browser. Develop the content plan is above Content structure; Save and review is
below the left browser. They share native form ownership. The editor identifies
the selected name, path and origin, presents a saved-content summary before
editable properties, and explains each kind of content. Type-specific prompts and
prompts guide proposed wording, image briefs, link text, control instructions or
container requirements. Purpose/owner/next action remain notes. The proposal checkbox still preserves
the null/empty-string distinction. Unsaved feedback and Discard operate on form
values only; Save uses the existing validated commit and Undo flow. Saving or
discarding keeps focus on Save. Students are instructed to save before selection.
Native fieldsets with legends or aria-labelledby and aria-describedby connect
the controls and help. Selected content properties is an always-visible section.
Develop the content plan is a native disclosure, initially closed and reset to
closed after reset/import. Ordinary rendering preserves its open state;
toggling it leaves form values and project data intact. Selection and adding an
item focus the visible name field. Invalid controls inside the planning disclosure
reveal it before browser validation focuses them. The
Architecture overview adds content planning within the existing twelve steps.

Content structure's h3 and introductory paragraph live in the left browser's
header, keeping the right form aligned to the top of the two-column grid.
Content readiness is an always-visible field directly after the properties
heading and before Website content. It uses the existing validated status field
for all content kinds and remains part of ia-form. The review disclosure is now
named Review the Content Plan; its Save actions remain beneath the left browser.

With no saved draft, planning fields show current authored wording from the
selected item's text/alt/label bindings (bounded to 2,400 characters). The Include
proposal checkbox stays off, preserving null versus explicit empty proposals and
preventing passive saves from promoting current wording to a proposal. Saved
drafts always win, including empty strings. Fresh inventories seed existing notes
with site/item purpose, an explicitly unassigned owner and an item-specific review
action. Existing saved notes, including blanks, are preserved; a contextual
placeholder is available for blank notes. No new schema or generic example panel.

`website-content.js` loads after the content inventory and before core state. It
adds normalized `designProcess.websiteContent.{basic,advanced}` arrays (empty for
old projects). Each record contains a local sourceKey, allowlisted field,
fingerprint and plain-text value. The inventory's optional entry callback exposes
local DOM nodes to a binding registry; labels and bare container text also receive
inventory entries. Text-node aliases share one canonical binding, so a control's
label and its separate label entry cannot acquire conflicting overrides.
Fingerprint mismatches or absent sources are retained/reported and never applied
to a different node. Fields are limited to 2,000 per mode, 2,400 characters each
and 120,000 serialized characters per mode; UI saves reject overflow atomically.

Basic/Advanced register raw `*SourceHtml` factories and shared edited `*Html`
factories. Preview, inspector, copy/download and source-derived sitemap labels
use the edited factories. With no overrides, authored HTML is returned directly.
Overrides resolve against locally parsed authored DOM; imported strings are
assigned only to text nodes or fixed safe attributes, then serialized. They are
never parsed as markup, selectors, URLs or script. Inline elements and anchors
remain intact. Relabeling an option adds its original implicit value explicitly
when necessary, preserving form submission semantics. Containers do not flatten
their children; generated planning artifacts stay derived. Project-owned spans
retain Brief identity while surrounding authored wording remains editable.

The existing form transaction commits website text and plan together. Discard
changes only form values; Undo restores both. Item restoration prepares defaults
until Save, and sample restoration clears only the active mode's overrides and
content plan. Mode changes, reset/import and external changes clear incompatible
Undo history. Save before sample switches, reset or imports.

The old destination editor and raw text outline are secondary collapsed panels,
shown only for the custom Sitemap source. Canonical sections focus their matching
page-section inclusion checkbox, or open the custom destination controls when that
source is selected; navigation references cannot set independent membership. Deleting or moving Header in the
content plan never suppresses Home. Sitemap ancestor suppression applies inside the selected navigation source,
independently from saved content-plan containment.

The centre lesson and Advanced HTML share an escaped, collapsible full-content
artifact. Open centre branches survive rerender by stable content IDs. The legacy
destination outline is a separate optional disclosure beside the visitor sitemap
preview. Exported artifact CSS is supplied by design-process; Studio control CSS is
`content-architecture.css`. Existing token, CSS inspector, live page and export
generation remain shared and dependency-free.

### Read-only responsive wireframes

`wireframe-engine.js` loads after content/text services and before core state.
It parses the locally generated `htmlExport()` and embeds `cssExport()` plus local
font CSS. High Fidelity retains configured backgrounds, background
images, text, borders and opacity, including button variants and website themes.
It removes motion and shadows without changing layout rules, font metrics,
spacing or breakpoints. Annotation colours use the website's text/control-border
tokens; layout groups receive no extra background fill.
Low Fidelity adds a neutral paint layer before the shared outlines: a white
canvas, transparent non-button objects and logos, grey button fills,
neutral text/borders/native control accents and
greyscale images/SVGs. It uses a light native colour scheme even for a dark
website theme. Box dimensions, type metrics, content and source visibility stay
the same. `createDocument({preview,fidelity})` and `documentHtml({fidelity})` accept
low/high; absent or unknown fidelity values fall back to high.
Basic and Advanced therefore retain the live website's structure and actual copy.
Container annotations mark page regions and content-width wrappers. A constructed
CSSStyleSheet parses only locally generated CSS; walking style/media rules finds
structural Grid/Flex wrappers and their child containers without a per-sample
class list. Imported strings never become selectors. The annotations are confined
to the mirror/download; they do not alter source HTML or Architecture. Solid,
dashed, dotted and thin inset outlines distinguish the levels without changing
borders, padding, positioning or font metrics. A Studio legend explains them.
Nested sections, disclosures, list items, description values and normal-flow div
wrappers with block content receive thin outlines. Every other HTML body object
is marked with the lower-priority object kind, including text elements, inline
spans, controls, table parts, images and decorative tracks. Non-rendering metadata
and line-break nodes are excluded; SVGs get one outer boundary, without outlining
their internal drawing shapes. Generated ::before/::after objects also get thin
outlines. Native hidden, responsive and disclosure behavior remains unchanged.
Leaf-object outlines yield to the website's :focus-visible rule, retaining the
distinct keyboard ring while a link is focused.
Existing region/content/layout/item priority remains above object annotations.
Native title attributes identify authored tag/ID/classes and layout type without
adding nodes or changing containing blocks. Titles use setAttribute for both HTML
and SVG reflection; existing title attributes are preserved.


Website content saved through Architecture flows through the existing generators;
proposals and planned-only entries do not invent a different website layout.

The mirror removes executable/nested embeds, makes website form controls inert and
removes non-fragment navigation. The workspace iframe has only allow-same-origin,
without scripts or forms. Its parent handles local fragments with getElementById,
opens ancestor disclosures, and prevents form submission. Imported text is escaped
by the existing website generators; it is never interpreted as a template or CSS.
Inert controls cannot receive user focus or activation; their original disabled
attributes remain unchanged, preserving the configured enabled/disabled appearance
instead of artificially dimming every button. Local links and details remain
inspectable. The downloaded HTML uses the same inert controls and outline layer.
The Advanced website's Wireframing lesson contains a short explanatory note rather
than embedding the mirror inside itself. It remains one generated inventory entry.

`wireframe-workspace.js` registers after studio-learning. It replaces the Studio
wireframe artifact with the read-only iframe and Basic/Advanced, viewport, compare
and download controls. Low Fidelity / High Fidelity use a labelled tablist and a
shared labelled tabpanel/iframe, with selected state, roving tabindex and automatic
activation on Left/Right/Home/End. High Fidelity starts selected to retain the
existing view. Fidelity is local view state, shared across Basic/Advanced and
theme changes; it is not a second saved website model. The download uses the
selected fidelity, and frame titles, guidance and summary identify it. The wizard
opens this view. Render changes refresh the
mirror only while Wireframe is active, or explicitly requested; unchanged HTML
preserves nodes. Same-mode updates retain scroll and disclosure state. The
workspace uses the existing sample mode controls and font synchronization.
Match live preview, 320/390/768/1280px and available-width choices are transient.
Fixed widths scroll within the labelled region instead of shrinking breakpoints.
Standalone wireframe.html embeds the same source styles and outline layer,
plus neutral paint when Low Fidelity is selected.

Legacy `designProcess.wireframes` and earlier layout/review-note fields remain
bounded, validated project data for compatibility, but no longer control the
read-only view. No separate wireframe content/layout model is authored. The JSON
upload cap remains 6,000,000 bytes. Legacy per-mode overrides are capped at 1,000
rows and 80,000 serialized characters; IDs/enums never become selectors or code.

### Destination planning and compatibility


`design-process.js` loads after the registry/font helpers and before core state.
Its `DSStudio.process` API provides fresh defaults, normalization, a bounded
sitemap parser, shared artifact HTML and artifact CSS. `state.designProcess` holds
plain text goal/audience/scope/content/constraints/delivery/success, a multiline
three-level destination outline plus per-mode content planning snapshots,
`split`/`stack` wireframe arrangement, wireframe notes, prototype task and notes.
Imports bound text lengths and accept only the two arrangements; missing or invalid
planning objects receive starter data. Empty draft strings remain empty. No plan
text becomes executable markup, a URL, a CSS declaration or a token.

`site-builder.js` registers after the existing feature modules and before studio
learning. It provides the secondary three-level sitemap CRUD editor in Architecture, backed by the same
`designProcess.pages` text and bounded parser. `pageLinks.basic/advanced` store
label-to-fixed-ID mappings (empty string means planned); normalization accepts
only that sample's inventory IDs and at most 64 bounded labels per mode.
`showPlanned` is a validated boolean, default false, now applied consistently to
selected unlinked entries in both samples. Existing label aliases still work.
`iaEntries.basic/advanced` store stable `ia-N` identities, one/two/three-label paths,
page/section/group/content types and boolean `includeInSitemap` values. Invalid or
duplicate IDs/paths, excessive depth and non-string labels are rejected. Each
sample's metadata is capped at 192 rows (the maximum derived from 64 outline lines);
the structured editor continues to bound structural changes to 64 entries.
Metadata-only changes preserve raw outlines with up to 192 derived nodes.
`tree()` exposes the full recursive outline; `hierarchy()` keeps its two-level
projection for existing wireframe/lesson readers. `entries()` adds depth and index
positions to flattened records. Depth, positions and parent IDs are derived from
the outline rather than persisted in metadata.

`DSStudio.process.entries()` reconciles the outline with metadata by path, retaining
matched identities and assigning bounded fresh IDs to new paths. Structured rename
and reparent update paths while preserving IDs, types and inclusion. Reordering
retains IDs. Bulk text edits retain matching paths; a newly typed path is a new
entry. The saved destination outline remains visible independently of sitemap selection. Legacy plans
without metadata default first/second-level entries to selected except Basic
Home/Footer, which can be included explicitly. New third-level content details
default to excluded. Each sample retains its own choices.

The labelled, locally scrolling inclusion region has one native checkbox per entry.
Excluding an ancestor disables descendant controls without changing saved choices.
Unchanged rows/inputs survive updates to retain focus. Groups are nonlinked headings
when they have eligible children; missing destinations remain labelled text when
enabled, never fabricated links. Undo restores the complete preceding plan.
Relationships affect the map/footer, not the authored body-section structure.
Rename and reparent preserve the full descendant subtree, identities, choices and
assigned destinations. Parent choices exclude cycles and moves deeper than three
levels, including subtree height. Reorder moves whole sibling branches; deletion
removes the complete selected branch. A one-change in-memory undo is cleared by external edits/imports,
reset and mode changes. Text edits and complete-inventory restoration remain.

`webpage-backgrounds.js` initializes after studio learning, binding Palette's
Body/Header/Main/Footer controls, with Body first and visible alongside the others. They follow
Brand Palette and Main Palette in the wizard. Every selector offers all validated
brand references in saved order and copies the selected hex, matching Main Palette
semantics; later reference edits do not silently recolour existing choices.
The theme-specific `header-background`, `main-background`, `footer-background`
semantic overrides share existing import validation, state, autosave and exports.
Missing overrides resolve from the current Surface, Background and Surface roles,
respectively, after those roles' own overrides. Older projects preserve their look.
Body retains the existing `background` override, `--background` token and original
`page-background-*` control IDs. No new Body setting or migration is needed.
Both sample headers and the shared footer consume the corresponding region tokens;
shared foundation CSS paints the main element. Basic's main sections stay transparent
and cards/controls keep their separate surfaces. The centre Palette lesson shows
Body as an outer canvas enclosing Header/Main/Footer, and all four resolved colours
and text/link contrast with complete CSS/HTML inspector
routes; it adds no duplicate control state. Catalogue routes select the correct theme
and Palette field. Contrast inventory includes the three backgrounds. Partial invalid
hex input does not change state. All controls use shared apply/render/autosave paths;
imported names become text/Option nodes and only validated hex enters colour styles.

Background transparency stores optional `backgroundOpacity[light|dark]` percentage
maps with only `body`, `header`, `main` and `footer` keys. Imports accept finite
numbers, clamp to 0–100 and round to integer percentages; missing/invalid values
default to 100%. It uses existing project JSON/autosave/import/reset paths without
a schema change or alpha inside the six-digit semantic hex roles.
Each region exports RGB channels, opacity and a derived `*-background-paint` token.
Body uses that paint over an explicitly opaque `html` Surface canvas; Header/Main/
Footer use their paints over Body. Text/controls retain independent opacity and
the existing whole-card `--surface-opacity` feature stays separate. Changing a
colour preserves alpha; a region reset clears both its current-theme colour and
alpha. Catalogue sources route RGB channels to the colour picker and opacity/
paint to the opacity slider in the correct theme.
`backgroundLayers()` composites unrounded sRGB channels against the same known
canvas/parent stack. The contrast audit uses those channels for text/links,
indicators and button host backgrounds; source colour repair targets stay the
original validated semantic colours. The centre nested model paints actual alpha
and shows its percentage, alpha token, blended hex and text/link ratios. It uses
rounded hex for its readable ratio display; audit ratios use unrounded channels.

Optional `regionPadding[header|main|footer][top|right|bottom|left]` stores shared
layout insets as integer pixel values (0–64px), independently of theme/sample.
Imports accept only finite numbers, round/clamp to these bounds and ignore unknown
regions/sides. Missing values resolve to zero extra padding, preserving existing
layouts and background settings. Twelve `--*-padding-*` foundation tokens drive
the outer header/main/footer boxes. Advanced main keeps its existing narrow/wide
container gutter in addition to the selected left/right padding; its media rule
uses the saved responsive wide cutoff. Header/Footer inner spacing stays intact.
Webpage backgrounds includes per-region disclosure controls, summaries, reset and
centre inset/token examples. Padding reset affects one region only; background
reset keeps padding. Catalogue/inspection routes use the same controls and complete
CSS export. Layout values use existing JSON/autosave/import/reset without a new
schema, independent generator or imported CSS execution.

The twelve wizard stages are Brief, Architecture, Typography, Wireframe, Palette,
Colour lab, Buttons, Spacing and surfaces, Responsive layout,
Accessibility, Deliver and Prototype. Existing control and centre IDs remain stable; the
shared stage registry keeps their routes aligned. Planning artifacts appear in
the selected lesson; other stage sections are hidden until selected.

The module's initializer binds planning inputs through the existing `apply()` /
`renderCode()` / autosave paths. The centre Architecture lesson provides a brief
UX requirements-planning overview: identify audience tasks, define essential
scope/content and ownership/accessibility/dependencies in the brief, group and
label content, then check a task route with an intended user. Its stated outcome
is an agreed IA and selected visitor sitemap ready to guide Wireframe. Studio
learning combines the overview and content-planning exercise in one optional
learning disclosure after a concise introduction; it adds no planning fields or
automated validation of the learner's decisions.
The planning module registers shared artifact styles in the planning export
stage and subscribes to `output:artifacts` for synchronized controls/lessons. Markup caches preserve
unchanged artifact nodes and focus through unrelated palette changes. Editing
replaces the planning object rather than mutating defaults. Existing JSON, local
project save/load/import/reset and New flows include this optional data; the JSON
schema version stays 2 because earlier loaders can ignore the new field.

The static sample adds a planning section, Process navigation and four lesson
cards before the design-system lessons. Studio and sample call the same artifact
helpers with distinct ID prefixes. Wireframes mirror the generated website through wireframe-engine.js; prototype
screens link Discover, Choose and Review with native fragments, with no application
backend or script requirement. The sandboxed live preview uses its existing
fragment handler. Planning data describes a project; it does not rewrite the
field guide's main navigation or generate a finished custom website.

The studio body uses the separate `--studio-background` canvas token:
`#E8EDF3` in light mode, with dark mode continuing to follow `--background`.
The generated website palette, previews, semantic overrides and exports keep
their existing background roles; the studio-only token is not exported.

## Live CSS/HTML Inspector and sample page

Basic teaching tasks are integrated into the wizard. The inspector remains
read-only; edit authored text through Architecture or download complete files
for further HTML changes. The hero demonstrates
a two-column Grid layout, with Flexbox, Grid and form examples further down.
Generated Basic HTML is indented and its page CSS uses one declaration per line;
authored SECTION comments label Page basics, Header, Hero, Skills, Toolkit, Form
and Footer. Formatting operates on escaped generated strings without execution.
Preformatted lesson examples and textarea elements are protected while the
surrounding HTML is indented, preserving their internal whitespace and keeping
empty textareas empty; examples render as escaped text.
They preserve all source whitespace and scroll locally on narrow screens,
keeping identifiers intact without creating horizontal page overflow. A tab
stop on each code block provides keyboard access to horizontal scrolling.

The Basic-only section selector is transient inspector view state, independent
of project JSON and preview rendering. `DSStudio.samples.basicExcerpt()` selects
authored section comments; CSS excerpts also include shared page rules and
responsive queries, and explicitly require the full foundation/component CSS.
Page basics also shows the live spacing token definitions for its exercise.
Copy uses visible code; inspector downloads and Deliver always use complete
exports. Advanced hides the section filter and shows complete files. Returning to
Basic restores the view selection. Clipboard feedback checks mode, language and
section after awaiting the clipboard. The inspector keeps a bounded code viewport.

`brand-palette.js` loads after the registry and before core state. Its defaults
factory uses the core's example seed when `DEFAULT` is constructed. Each project
stores `brandPalette` entries `{id, name, hex, group}`: unique safe token IDs,
40-character names, six-digit HEX values and primary/accent reference groups.
Normalization accepts 1–24 valid entries and supplies starter references for
missing/empty/invalid older data. New projects keep the existing `--brand-*` IDs.

The registered module creates step-4 editing and full-brand dropdowns for all three
Main Palette roles. Selections copy HEX values through the existing core inputs;
they are independent assignments rather than persistent bindings to reference IDs.
Picker/advanced/OKLCH changes synchronize the matching option or Custom choice.
Reference edits update saved data, exports, the catalogue and contrast candidates
without changing role assignments. The centre swatch display and the legacy
accent picker read the same project palette. Editor nodes stay stable
across updates; names are rendered as text and escaped in reference markup.
Contrast candidate identities include the brand token ID to distinguish duplicate
names and prevent them being mistaken for generated-ramp anchor controls.
The editor exposes the ID as a token suffix after `--brand-`, validates uniqueness
and the existing safe-ID grammar before committing, and displays the full CSS
declaration. Display-name edits do not rename tokens. Token renames reuse the
editor node, update catalogue/contrast references and preserve copied UI colours.
Replacing project state restores field values and clears stale input validity.

### Guided Palette workspace

`palette-browser.js` initializes immediately after palette-workspace. Each of
the seven stages has a left browse/manage column and a right selected-properties
form, stacking when the available width is narrow. It moves the original controls
and delegates to their existing listeners; it adds no persisted model. Brand
search and selection preserve the selected editor, and Add/Remove use the existing
validated CRUD. Fixed anchors, semantic roles, regions and component families can
be selected and reset where supported rather than created or deleted.
Generated shade/component values appear in labelled read-only input fields.
Semantic name/token fields are read-only; proposed HEX and picker fields keep a
local draft until the existing contrast dialog previews and applies it. Cancel
keeps the saved value, and Discard restores the current value. Other edits retain
their existing immediate-update behavior. Native disclosure reopening refreshes
generated fields after the original workspace's toggle handlers finish.

The anchor stage uses one labelled native three-option list, Primary / Secondary /
Accent, rather than the previous role buttons that called Secondary "Supporting".
Changing selection retains focus in the list for keyboard navigation and exposes
only that anchor's original brand/custom fields and scoped reset. Configure routes
also synchronize the list. Selection remains transient; anchor values continue
through the existing shared model, generated ramps, autosave and JSON import/export.

`palette-workspace.js` registers after palette-process, state-palettes and
webpage-backgrounds, before spacing/utility lessons. It moves their existing
controls into seven native details stages inside the centre Palette panel:
brand references, shared UI anchors, shade generation, semantic roles, page
backgrounds, component colours and states/review. The existing guided semantic
selector and its contrast dialog are reused. Colour lab remains a separate
model-exploration step, with a link to Palette.
Only one main stage opens at a time; each has its explanation and Previous/Next
navigation. The wizard keeps a short guide/current-stage navigator. Its mobile
navigation collapses by default, and the existing stage-controls anchor places
it below the workspace header without cloning controls or losing listeners.

Brand editing keeps one selected existing row visible, using existing safe-ID
validation, add/remove bounds and project persistence. Selected properties are
a visible section, not another disclosure. Collection actions/counts remain
outside that section. Role pickers update through their original bindings;
reset copies only the relevant DEFAULT anchor. Generated shade tokens remain
read-only outputs of those anchors/method. Background selection shows one
existing region fieldset; reset keeps its original override/inheritance behavior.
The new theme selector delegates to jTheme. Feedback pickers write only one
validated existing semantic override for the selected theme; reset removes it.
Advanced state editors and token teaching views remain in optional disclosures.

The component stage uses a family selector and actual dssReadTokens output for
cards/panels, inputs/feedback, links and buttons. Dark values fall back to base
when a token is shared (notably button focus). Context names roles used by family
variants; it does not claim all selectors use every listed role. Component source
links and token catalogue metadata route colour settings to Palette (index 4),
while button geometry/behavior retain their existing step. Visible source labels
use stage.position rather than the internal step index.

Button variant selection proxies the original bdVariant control. Existing source,
custom and eight colour fields move once into Palette; all bindings persist.
button-design.js adds dssResetButtonColourOverrides, clearing only one validated
variant's overrides before rendering/autosaving. Chosen source/custom values,
other variants, geometry and shared focus remain. Focus has a separate reset.
Component readouts refresh on renderCode, entry and manual disclosure opening
only when Palette and its component stage are open, avoiding hidden CSS parsing.
The local visibility helper never changes the global lesson during background
updates; explicit Reveal/Configure handles navigation, preserving other lesson
nodes and focus.

The module subscribes to foundation updates so visible selection, theme
and source summaries stay synchronized. State identity replacement resets the
local process to brand references for direct importConfig, local load and reset,
not only file-import events. Stage/region/brand choices are transient; no schema
or colour generator is added. Existing copy-by-value relationships remain.
Source Configure/reveal routes open the stage, select the source row/region and
open ancestor disclosures before focus. Existing editor nodes remain stable.
Imported names use Option/textContent, never interpolated markup.

`palette-process.js` initializes after studio learning and before backgrounds.
It shows eleven shade declarations for each Main Palette role immediately after
the ramp-method control, and a centre Brand → Main Palette → shades → semantic
explanation before background application. It reads `dssReadTokens()` from the
actual shared CSS export, including both theme values and semantic overrides;
it does not add another colour generator, saved state or automatic brand binding.
Anchor 500 is explicitly identified. Text updates retain existing nodes/disclosures;
all imported display names use textContent and validated colours only paint chips.

Success, Warning and Danger also expose eleven shade tokens in each theme block.
The shared CSS generator applies `makeRamp()` to each resolved semantic colour,
including validated theme overrides; step 500 equals that colour. There is no
separate persisted status anchor, automatic remapping of component states or
additional colour algorithm. The palette module reads those exported declarations
for compact wizard and centre status ramps, preserving disclosure nodes across
theme/method/override updates. Configure actions and catalogue source routes reach
the matching theme's semantic editor. Existing feedback continues to use its
semantic colour, with non-colour interaction cues and native behaviour unchanged.

`state-palettes.js` loads after `palette-process.js` and contributes to the shared
states export stage. It derives ten General controls state ramps from resolved semantic
roles, plus seven state ramps for each of the five button variants from
`dssGetButtonContrastData()`. Sources follow the actual component rules: e.g.
hover/pressed use their specific backgrounds, focus/selected use the ring colour,
and disabled/loading reuse the base colour alongside their non-colour cues.
Transparent button backgrounds use the foreground colour as an explicitly labelled
anchor; the ramps do not represent an alpha-composited disabled/transparent paint.
Each state exports eleven steps per theme, using the existing ramp generator;
source hex casing is normalized. Status ramps remain separately available.

The module caches generated declarations by method/source settings and reuses
ramps for repeated anchors. A cached metadata lookup supplies catalogue routes
without recomputing colours for each table row. Wizard/centre component selectors
mirror an ephemeral view choice, never project data. The views read actual exported
tokens on render, retain disclosures through colour/theme updates and provide
shade/source inspection and existing source configuration. No component rules,
native semantics or persistence schema are replaced by these shade options.
The catalogue reuses unchanged CSS/search output and resolves a row's source once
when rendering. It also reuses rows whose escaped markup is unchanged, updating
affected rows instead of reconstructing the entire catalogue for each source edit.

Each interaction ramp includes a labelled colour selector in both mirrored views.
Default reads the inherited source with only that property's override removed;
Brand/Main/Neutral/current-ramp choices copy validated hex values to the existing
semantic or button property. No separate state-colour overrides are persisted.
General controls use current-theme semantic overrides and the normal apply/save
path. Button edits use the existing setter, now accepting explicit `null` to
remove one property override (or restore the default focus colour). A read-only
default-colour getter uses the same button colour resolver with that override
removed. Shared sources, cross-theme button settings, global button focus and
transparent foreground anchors are explained beside each selector.

Choice lists use textContent for imported brand labels and only validated colours.
Existing custom source colours receive a current-value option. Lists update when
brand/default/source values change, retaining select/disclosure nodes and focus.
Malformed selection values restore the control without changing project data.
Dropdown synchronization ignores unrelated typography and button dimensions.
General inherited colours are resolved once per sync from base semantic roles;
sources shared by multiple state rows reuse the same computed default.
After creating its lesson, the backgrounds module moves the existing interaction
controls and lesson after the background editor/lesson. This establishes the same
surface-before-interaction order in both panes while retaining all bound nodes.

`makeNeutralRamp(primary, method)` is part of the core colour generator. It borrows
Primary UI's OKLCH hue, sets midpoint lightness to 0.6 and reduces midpoint chroma
to `min(primary chroma * 0.12, 0.025)`. Achromatic sources remain grey. The existing
RGB mix/OKLCH ramp generator supplies eleven steps from that derived midpoint.
OKLCH is the foundation default for startup, New, Reset and missing/invalid
imported methods. Explicit saved `mix` and `oklch` values remain unchanged.
`palette().n` and `--neutral-50` through `--neutral-950` share that one result;
there is no editable neutral anchor or extra persisted state. Neutral 500 is
labelled a derived midpoint, while the three chosen anchors retain their meaning.
The catalogue routes neutral shades to Primary UI; contrast candidates include
all neutral steps and use Primary as their source target. Background selectors
append a Neutral optgroup after all brand references, with the same copy-hex
semantics. Primary/method edits refresh those options but preserve earlier choices.
Default semantic surfaces/text/borders remain unchanged; neutral steps are
available for deliberate assignment and actual foreground/background review.

The centre Brand Colour Palette uses one unified swatch grid and a view-only
target-role selector. Each entire swatch is a native button that copies its HEX
through the same validated assignment helper as the guided dropdowns. Current
role summaries, per-card usage labels and status feedback make the result visible.
The renderer updates existing cards by token ID so applying a colour retains
keyboard focus. It runs on every project refresh, including manual role edits,
import and reset. Its Edit shortcut opens/focuses the guided editor instead of
resetting project data. Core `renderBrand()` delegates to this module's renderer.

The studio chrome uses the full window width. `learning-path.css` overrides the
older fixed-track rules with a desktop three-column layout above 1280px. The
builder takes 25% of available width in either inspector state. Centre and
inspector split the remainder 2:1 after their gap, capping the inspector at 25%
of the desktop workspace and giving the centre approximately 50%. The inspector
precedes `main` in DOM order; explicit grid placement
puts it above the preview when closed and to the right when open, with sticky
positioning on desktop. Its native disclosure heading stays available.
The outer layout stays a 1:3 grid above 900px whether code is open or closed.
With code collapsed, `is-inspector-collapsed` switches `studio-right` to a single
track. The closed inspector body takes
no space and supplies no keyboard targets; its visible compact bar spans the
remaining workspace above the preview. The iframe is not moved or replaced;
its existing resize observer updates Fluid width while retaining browsing state.
At <=1280px the inspector stacks below the centre. At <=900px the entire layout
stacks and controls join their lesson. The preview remains first and expanded
on startup, with other centre sections collapsed; stage activation opens its
matching lesson without moving nodes. Shell gutters align the top bar with the
workspace. These rules do not affect generated website container widths.

`css-dock.js` selects `cssExport()`, `htmlExport()` or `projectJson()` for its code panel,
copy action and download. Its language tabs use arrow/Home/End keys, managed tab
stops and panel labelling; selection is independent of the centre export tabs.
Settings changes refresh the active language through `output:updated`.
Its Page theme selector and the preview's selector share `state.theme` with the
guided builder/global toggle, autosave and JSON import. Both theme blocks remain
in CSS; HTML uses the chosen initial theme and matching illustrations.

`sample-homepage.js` registers with `DSStudio` after the button module. During
startup it installs the complete HTML generator and appends sample component/layout
CSS to the existing stylesheet generator. Every HTML export therefore uses the same
page. The page reads current shared state, advanced settings and serialized button
settings, including theme, size, full-width and selected state. Embedded SVG images
use resolved palette colours; no remote images or extra asset downloads are needed.

Every main section, including the planning workshop, has a `sample-section-actions` pair. Shared generation keeps
the primary/secondary classes, selected size and mobile full-width behavior aligned;
destinations and labels follow each section's context. Hero/about pairs sit in
their text columns; services/resources/components pairs follow the section content
with a 24 px default top margin. The contact pair uses the existing native submit
button and an anchor back to services. Service cards keep text actions and the
component gallery keeps its state demonstrations. Demonstration loading/disabled
states do not disable section navigation. All navigation destinations are fragments
that work in downloaded HTML and the existing live-preview navigation handler.
The secondary links use `ds-button--secondary`, including the hero and contact
form, so Secondary wizard colour/source edits reach their visible page actions.
The independently editable Outline variant remains in the component gallery.

The header generates desktop and mobile link lists from one array. At 48rem and
below, a native `details`/`summary` disclosure replaces the desktop navigation.
The summary's inline SVG switches between hamburger and close paths using the
disclosure's open state. The SVG's `currentColor` inherits `--accent` while the
“Menu” label uses `--text`. The toggle has no border and a transparent background;
the normal keyboard focus outline remains. The native control works in downloaded static
HTML and the script-disabled preview, whose existing disclosure preservation also
retains the menu state during live palette/theme edits.

The header brand link pairs an aria-hidden “Logo” placeholder with a separate
project-title span, preserving the project name as the link's accessible name.
The square logo uses spacing tokens for 48 px on narrow screens and 64 px on
desktop at the default spacing unit, and uses
primary/on-primary colours and the shared radius. The title consumes `--text-h2`,
heading leading and tracking, and can wrap beside the mobile menu.

The generated container includes its gutters in a configurable maximum border-box width (72rem by default).
Gutters are 16 px on narrow screens and 32 px from 64rem at defaults. Hero/split
rows use 12 tracks with children spanning six; card rows span four per card.
The generated sample is a Web Design Field Guide: ten lesson cards, a layout
workshop, typography/semantic-palette exercises, resource checklists, practice
question form and the component/state gallery. Existing section/form IDs remain
stable, including `services` for the Lessons destination. Browser/wireframe SVGs
replace the generic landscape illustrations and remain embedded/palette-aware.

The named `sample-content` inline-size container lets card rows switch to two/one
columns using thresholds calculated from `adv.columns` and `adv.gap`. Split rows
stack at the configured narrow cutoff (48rem by default). Responsive layouts therefore retain the existing card controls.
The new `grid-lab` workshop demonstrates twelve tracks with 8/4 and 4/4/4 spans;
the demo uses `--grid-gap` and becomes one column at the narrow cutoff. The outer 8/4
example/notes layout stacks at the wide cutoff (64rem by default). A native disclosure exposes the matching
CSS recipe. `type-lab` renders base/ratio/leading readouts and a nested
`colour-lab` renders resolved semantic role values and swatches, so changing
wizard settings updates both explanation and rendered styles through exports.

The same layout workshop includes `flex-lab`: wrapping topic rows, a fixed marker
beside growing/shrinking text, and a normal-flow/Grid/Flexbox comparison. The
`flexRecipe` constant supplies both the inspectable recipe and exported CSS.
Lesson cards use its column layout with an auto top margin on the final action,
inside the existing Grid. Flex rows consume the saved grid gap and spacing tokens;
no additional settings, scripts or network calls are needed by the exported page.

`oklch-lab.js` keeps uncommitted exploration separate from foundation state. Load
reloads the current selected role; Reset selected role to default commits that
role's `DEFAULT` anchor through the same helper as Apply, then reloads the wheel.
The other anchors and project brand references are preserved.

The default 4 px foundation unit provides 8 px spacing steps plus 4 px fine
adjustments. Section padding changes in discrete token steps; typography remains
fluid. New defaults use 24 px card gaps and 48 px minimum button/control heights.
Imported dimensions are preserved rather than snapped to the spacing scale.
Fonts, borders, focus outlines and scaled button size variants remain independent.

Core CSS generation reads `palette('light')` and `palette('dark')` without changing
`state.theme`. The sample generator resolves its palette once per HTML export and
reuses embedded SVG encodings through an eight-entry cache keyed by their resolved
colours and illustration type. Component CSS owns real button states; the sample
adds only selected-state simulations. Both code panels retain their text nodes
when the generated string is unchanged, preserving selections during such updates.

Save `index.html` beside `tokens.css`. The HTML stays static: native navigation,
disclosures and form controls work without JavaScript, and the practice question form
has no delivery backend. Fixed reference palette values now export as `--brand-*`;
the catalogue and CSV use the same names. Existing consumers of `--example-*` must
update their references when adopting the new CSS export.

`responsive-preview.js` initializes after the sample generator and subscribes to
output updates through the shared preview phase. It renders the same generated HTML and CSS
inside `previewPage`, a sandboxed iframe with scripts/top navigation disabled and
same-origin DOM access/native form validation enabled. The exported CSS is inserted
as a style text node; the external tokens.css link is removed in the preview only.
The downloadable files are unchanged by browsing the preview.

CSS-only changes update the existing style node. HTML changes replace the document's
head/body contents while preserving the iframe, form values, checked choices, FAQ
states, focus and scroll position. Parent-owned event handlers keep fragment
navigation within the generated page, reveal linked FAQs and prevent sample form
submission from navigating or sending data. The document's own viewport controls
its media queries and vw typography at 390/768/1280 px or the actual Fluid width.

## Responsive design phase and training brief

`responsive-design.js` loads before core state to supply `DSStudio.responsive`.
`state.responsiveDesign` stores nominal-pixel `stack`, `wide`, `maxWidth`, `gutter`
and `wideGutter` values. Defaults are 768/1024/1152/16/32. Imports accept finite
numbers, bound and round them, and keep `wide >= stack + 160`; malformed or missing
objects receive fresh defaults. Sliders use 1px increments so valid imported values
remain representable without browser range-step rounding. UI mutations replace
objects and do not mutate defaults.

The new wizard phase is index 9, after Layout; Accessibility and Deliver move to
10/11. Grid minimum/gap/alignment controls move from Layout to Responsive. Catalogue
routes follow these controls and the three new page tokens. The new centre lesson
is `responsiveDesign`; existing anchors remain stable and numbering is refreshed.

Both generators use the same page width/gutter tokens and literal `rem` media-query
lengths (nominal pixels / 16). CSS variables cannot supply media-query conditions.
Advanced's split/header/Grid workshop cutoffs and wide styling, Basic's header/form
stacking/wide gutters, and planning wireframes follow the saved cutoffs. Responsive
page controls do not change studio pane breakpoints, fixed preview presets, fluid
font limits or the independently configured mobile button behaviour. Card wrapping
still follows container/card constraints rather than a universal page breakpoint.
The lesson uses the actual iframe `matchMedia()` results and `innerWidth`, so its
readout follows CSS even with scrollbar/default-font differences.

The Project Brief artifact teaches seven website-project prompts: purpose,
audience, pages/features, content, design requirements, delivery and success.
It includes a fill-in template and a static café example, plus optional website
planning reading from Smashing Magazine. The shared `briefFields` definition generates the seven numbered wizard fields,
the lesson checklist and saved-draft labels in the same order. Content and Delivery
are additive string fields (1,200 characters each); the original goal/audience/
scope/constraints/success keys remain. Legacy combined notes are kept verbatim
within their original bounds; new fields default empty rather than guessing how
to split text. Normalization validates types/lengths for all seven fields.
New default brief answers are empty, with prompt placeholders in the wizard.
Existing answers are normalized/preserved and shown in an optional draft disclosure.
Shared artifacts carry this guide into Advanced exports. Preview disclosures are
preserved by stable ID/summary keys rather than array index: inserting a draft
must not shift the saved open state of a FAQ or mobile menu.

## Architecture-linked sitemap and Basic lists

`section-sitemap.js` derives the default navigation from local sample HTML and
fixed, authored destination IDs. It takes an owned eyebrow before an owned
heading (or group legend), never borrowing a nested container's label. Unlabelled
wrappers are omitted, children attach to the nearest labelled ancestor and slash
text remains intact. Basic includes Hero and its three main content sections.
Generated IA/sitemap contents and Footer are not recursively inventoried here.
The detailed `content-architecture.js` inventory and planning tree stay intact.

`designProcess.sitemapSource.basic/advanced` accepts auto, sections or custom.
Auto uses page labels for the complete sample and preserves older custom outlines,
metadata and link bindings. Explicit source changes preserve those saved plans.
`sitemapExcluded.basic/advanced` holds deduplicated fixed destination IDs, bounded
to 192 input values and validated against the sample inventory. Excluding a
parent suppresses its subtree without changing child choices or authored content.
The section configuration provides per-sample restore and Undo. Source/exclusions
persist through the existing project JSON and autosave pipeline.

The collector's per-mode signature includes project state and Advanced settings,
excluding content planning data that does not change the actual page. A recursion
guard omits the generated map during collection. Labels are escaped for markup;
control labels use textContent. Imported strings never become selectors or URLs.
Both Sitemap sources use the shared footer/lesson renderer and existing Studio
preview proxies; exported links are ordinary fixed-ID fragments with no script.
The source selector shows the old custom editor only when that source is active.

The following legacy destination rules apply to the **custom** source:

Basic includes titled unordered/ordered/description list examples. Its equal-width auto-fit card grid uses the saved minimum
and gap rules, adding columns as space permits without manual row spans. Both samples
have a footer Sitemap navigation generated by `DSStudio.process.sitemapHtml()`.
Both samples share one classic footer template and its CSS in `sample-system.js`.
Both call `sitemapHtml({linksOnly:true})`; no fixed Basic parent allowlist remains.
For custom plans, per-entry inclusion, branch suppression, type and valid destinations determine
what appears. Basic defaults to omitting Home/Footer but explicit choices override
that default. Selected unlinked entries require showPlanned in either sample.
Parent groups occupy responsive Grid
columns, with child links stacked vertically in semantic nested lists.
The Sitemap heading is left-aligned. The capped-width column grid is centred,
with each group's heading and vertically stacked sublinks centred in its column.
The map is wrapped in native `details#footer-sitemap`, initially closed, with
`summary#sitemap-toggle` containing the existing `#sitemap-title` heading. The
inner `nav#sitemap` and its aria-labelledby relationship/destinations are retained.
The expanded list markup, grid and child alignment are unchanged. The closed
state explicitly hides only the inner navigation, avoiding residual map geometry;
the main footer navigation and bottom row stay visible. Summary size/focus reuse
the shared spacing, heading weight and button focus tokens. Native fragments to
the inner map reveal the ancestor in standalone exports; preview fragment
handling already opens ancestor disclosures. Existing keyed preview capture
preserves open/closed state and summary focus during palette/theme updates,
without storing the disclosure in project JSON or adding exported scripts.
Unselected entries and children of omitted parents are not promoted. Planning data remains unchanged;
empty filtered maps explain how to review inclusion and destinations. Copyright and
Back to top form the bottom row, and both headers expose `#top`.
Both samples' Architecture artifacts show the complete IA, including Forms/Footer
and information excluded from the sitemap. The `.process-map--basic` list retains
wrapping horizontal groups; Advanced retains its tree. A separate visitor sitemap
preview uses the same generator as the footer. Shared guidance distinguishes Brief
scope, IA organization and visitor navigation, with a Contact/Opening hours example
and a link to NN/g's Information Architecture vs. Sitemaps. This shared artifact also
appears in Advanced standalone exports. Neither inclusion nor type removes authored
website content or creates arbitrary pages.

The shared, fixed inventories in `design-process.js` map all major sections and
content groups, including each Basic card/list and Advanced lesson/workshop.
Stable authored IDs identify these destinations; imported labels never become URLs.
Matching ignores case, spacing and hyphens. Basic accepts its former section
and lesson labels as aliases for stable IDs. Its inventory names Home, Components, Layouts, Forms and Footer. The exact previous complete Basic plan
resolves to the new inventory without rewriting stored data; custom plans keep
their authored labels and legacy destinations.
The IA retains unknown labels as escaped text. The sitemap includes them as labelled
planned destinations only when selected and showPlanned is enabled. Empty maps remain explicit.

`samplePages(mode)` generates the three-level destination starter.
It does not represent the full actual-content inventory. `currentPlan()` resolves
an untouched canonical Basic/Advanced inventory, the previous complete two-level
inventories, or the exact legacy six-entry
starter to the selected sample's inventory. It leaves custom plans unchanged,
including empty plans. Resolution is pure: stored planning data is preserved;
preview, editor, centre artifacts and HTML exports all use the resolved plan.
The restore button replaces custom entries with the selected inventory and resets
that sample's destination/type/inclusion metadata, preserving the other sample's metadata.
It reports applied/already-complete status with section/topic counts and expands
the centre Architecture map without moving keyboard focus. Feedback clears on
planning edits, sample changes or imports with a different plan. Restoring the plan does not generate new pages or change either footer
presentation.
The parser allows 64 nonempty lines, three levels and 64 characters per label; the text
field/normalizer cap input at 8,400 characters. Fourth-level raw lines are retained
in saved text, flagged with native field validation and an editing status, and
excluded from rendered trees; imported metadata deeper than three is rejected.
Footer links use only fixed IDs.
JSON/local project flows retain custom edits. Main navigation remains a shorter
selection of destinations rather than duplicating the entire content inventory.

The default Basic footer Sitemap has four section groups labelled by the Hero,
Components, Layouts and Forms eyebrows. It contains twelve links, including
heading/legend fallbacks for labelled children. The custom source preserves the
previous Components/Layouts/Forms groups and optional Home/Footer choices.
Excluded parents suppress their branches in either source; child choices remain.
The identity row also has a labelled Footer navigation with the same Home,
Components, Layouts and Forms links as the header. It sits to the right on wide
screens and beneath the brand at the saved stacking cutoff; links wrap as needed.
Site identity/copyright/Back to top remain. Advanced uses the same layout with
Home, About, Resources and Contact navigation and its own tagline/copyright.

The current Basic page is a UI essentials showcase, implementing the agreed
beginner component scope. Header/main/footer navigation and section labels use
Home, Components, Layouts and Forms. Components combines real article cards,
a Flexbox avatar/text row and native FAQ. Layouts includes a card Grid, ul/ol/dl
examples and a headed section containing a labelled article/aside split. Forms
adds fieldset/legend radio grouping to labelled inputs, select, textarea and
checkbox controls, with native validation and live demo feedback. Semantic
landmarks, one H1, skip link and source reading order remain intact. Layouts
stack at the saved cutoff; no tab/modal/carousel scripts are added.

The Basic destination starter has 28 saved-outline entries: sixteen linked
sections/groups plus twelve descriptive entries retained for custom-plan
compatibility. That custom starter retains fourteen footer links; the default
page-label Sitemap uses twelve links in four groups. Advanced has
49 destination-outline entries: 38 linked entries plus eleven descriptive entries. These third-level
examples plan actual information within existing components; no extra pages,
anchors or body content are generated. Both samples start the new content details
excluded from sitemap navigation. The secondary destination editor retains its three-level bound; the primary
actual-content outline supports deeper structures. The lesson encourages fewer
levels where sufficient and cites NN/g's flat/deep hierarchy guidance without
presenting a universal depth rule. The previous thirteen-entry mock inventory is recognised
alongside older complete inventories, and resolves without changing stored
planning text. Its previous section/topic names remain fixed-ID aliases. Radio
choices, FAQ state and other form values participate in preview capture/restore.

## Basic and Advanced sample modes

`state.sampleMode` is a validated `advanced` / `basic` enum, defaulting to Basic
for startup, New and Reset. Basic is the left tab and Advanced the right; keyboard
Home/End and arrow navigation follow that order. Explicit saved choices are restored
through the existing JSON and local save/load flows. Legacy imports without a mode
retain Advanced, while invalid explicit modes fall back to Basic. No separate
palette or project state is introduced for Basic.

`sample-system.js` registers before both sample generators. It contributes shared
layout CSS, exposes the shared pipeline through the foundationCss compatibility
alias and provides common button classes, header navigation text/state styles, footer HTML
and footer CSS. Header links use Advanced's semibold/plain-at-rest treatment in
both modes, independently of general link underlining. Both modes therefore
export the same foundation ramps, semantic roles, typography, spacing, responsive
settings, card/control appearance and Button Design rules. Basic adds its simple
page layout; Advanced adds its gallery/workshop layout. Basic no longer recreates
a partial set of tokens or hard-codes body/heading sizes, spacing, measure,
control dimensions, border widths or card effects. Global link focus follows the
saved focus width, while buttons retain their component focus settings.

`basic-homepage.js` registers its CSS and edited HTML renderers after the Advanced
sample and before the preview. The stable public HTML/CSS entry points select
the current sample; inspector, copy, preview and download paths use those same functions. Basic renders
a four-section component showcase: an illustrated hero, Flexbox content cards
with a profile row and native FAQ, Grid cards with semantic lists and an
article/aside supporting layout, and a centred form with grouped choices.
Copy is concise, with working examples and short component explanations.
The page keeps semantic landmarks, one H1, labelled sections, articles and aside,
accessible native navigation and form labels, and static-demo feedback. It shares
all design-system typography, spacing, colour, component and button settings.
The framed hero and Flexbox composition stack at the saved narrow cutoff;
the card Grid uses the saved card minimum and gap, and the article/aside
split stacks in source order. The form respects --reading-measure.
Header desktop/mobile/footer links share an authored list. Basic keeps its
classic identity, grouped sitemap and copyright/Back to top row. Advanced keeps
its tutorial content and uses the same shared footer layout.
Every main section has a primary/secondary CTA pair with contextual
fragment destinations; the form pairs native submit with a layouts link. Content
cards also link to related examples. All CTA classes
come from the shared button helper, including variant, size and mobile width.
Simple Flexbox action rows wrap with token-based gaps; no new runtime or backend
is introduced. The two samples use the
same heading sizes at each hierarchy level and the same saved button size/mobile
width classes. Advanced interaction simulations remain gallery demonstrations;
Basic keeps usable native form controls and ordinary page actions.
Basic's page CSS places shared rules before the individual sections so local
rules remain easy to follow and mobile navigation overrides retain precedence.
Identical link targets, flexible-child sizing and form-control rules are grouped;
obsolete form FAQ styles and repeated declarations are removed. The full export
still includes shared foundation/component CSS to preserve studio settings.
Advanced exposes its cached SVG generator as `DSStudio.samples.illustration`;
Basic reuses it with the active palette roles. The hero uses two equal Grid
columns, stacking text before the image at the saved responsive stack cutoff.
Image dimensions reserve its 4:3 ratio; the exported data URL needs no extra file
or network request.
Imported project text is escaped. The static form has no processing backend; the
preview intercepts its submission and announces that no account was created.

Mode controls are an ARIA tab group with Arrow/Home/End navigation, roving tab
stops and a labelled shared panel containing the independent CSS/HTML tabs.
`basic-homepage.css` styles only this studio wrapper. All code/copy/download
surfaces continue to call the same generators, including the explicit website
file actions. Inspector copy feedback verifies both mode and language after an
asynchronous clipboard result, avoiding feedback for a subsequently selected mode.

The responsive renderer preserves forms/disclosures/focus/scroll through ordinary
same-mode edits. A sample change or project installation starts a fresh browsing
session, including identical JSON imports, local loads, reset and New. The
project-install listener invalidates the prior output and mode before scheduled
rendering, so coalesced sample changes cannot retain another project's form values.
The iframe document remains in place. Both modes remain static, script-free exports
and share the existing optional font-link and preview-only fallback behaviour.

## Standalone website download actions

`website-export.js` initializes after the sample/preview modules. Its explicit
HTML/CSS actions sit in Deliver; the Live CSS/HTML Inspector also downloads
the selected language. Both read the current `htmlExport()` / `cssExport()` at
click time, so there is no parallel sample or cached export snapshot. Files are always named `index.html` and `tokens.css`,
matching the existing relative stylesheet link. Deliver's CSS action previously
used `design-system-tokens.css`; it now uses the shared handler and matching name.
JSON export filenames and project data are unchanged.

Downloads remain two separate user actions. Announced feedback says a download
was requested and explains how to save the pair; the application does not claim
browser/OS saving succeeded. The responsive preview omits the introductory lesson
and duplicate download card so its viewport follows the preview controls.
The static page retains its native menu/disclosures, embedded illustrations and
form demonstration. Google font links remain conditional on the saved font source.

The browser suite captures each file action and verifies exact contents and MIME
types and unchanged settings. It also loads the captured HTML
with a separate Blob stylesheet (rather than inline CSS), then checks component
presence, reflow and native menu/FAQ behaviour in both themes. Actual download
permission/save-dialog behaviour remains a manual browser check.

## Contrast inventory

`button-state-practices.js` loads after the registry and before the core. Its
`DSStudio.buttonStates.css()` helper defines the non-colour state cues once:
hover underlines, inset pressed styling, CSS-drawn selected checkmarks and busy
progress indicators. Its registered initializer installs the studio rules with
state-simulation selectors; the button CSS generator uses the same helper for
real `.ds-button` and legacy `.button` states. Existing component focus rules
continue to own outlines. Reduced-motion and forced-colour rules retain visible
feedback without requiring animation or box shadows. Off/on toggle examples
reserve the same icon space and keep identical labels.
The `--button-progress-animation` token also follows the saved advanced Reduce
demo animations setting; the platform reduced-motion query always takes priority.
`scripts/button_states_review.py` uses isolated Chrome profiles to verify actual
reduced-motion and forced-colour preferences, including keyboard focus while a
pressed-state simulation is present.

Busy buttons keep full opacity in specimens and exports. Native disabled samples
keep the inactive exemption, while the lab's operable busy sample is still tested
as normal text. The static home page blocks its busy example with `disabled` and
includes nearby guidance; applications must implement actual workflow changes,
toggle interactions and status announcements. No script is added to exported HTML.

`contrast-audit.js` uses `palette(theme)` and the button editor's read-only
`dssGetButtonContrastData()` snapshot to evaluate both themes without switching
the active project. Core, advanced and button changes schedule one refresh per
event turn. Text, conditional non-text checks, inactive exemptions and exploratory
swatch candidates remain distinct. Alpha/brightness calculations use unrounded
sRGB channels for ratios; displayed samples use the nearest HEX values.

The report separates required pairs, conditional checks, potential colour uses
and inactive exemptions. Conditional boundaries and unused feedback text do not
inflate the required-problem count. `colour-repair.js` calls the pure
`collect({foundation, buttonSettings})` path with copied settings to compare
candidate colours without updating the studio, storage or exports. Suggestions
rank new required problems first, then the selected pair's target and resolved
problems. Apply checks the project revision before committing; Cancel discards
the preview. Changes across both themes remain visible in the comparison.

Semantic overrides live in `state.semanticOverrides.light/dark`, accept only
known HEX-valued roles on import, and flow through preview and export via
`resolvedSemanticRoles()`. `--control-border` follows `--border` until explicitly
overridden, allowing input boundaries to differ from decorative separators.
The step-7 guided semantic editor uses the active preview theme and the same
role list, colour-repair dialog and reset operation as the centre editor.
`dssSyncSemanticEditor()` refreshes both entry points after contrast updates,
imports and resets; it preserves each role selection. Guided edits show a
swatch, HEX value, purpose and generated/custom status without duplicating state.
Button previews accept copied settings and foundation values; the commit API
updates the selected variant's actual settings and existing controls.

The registered `button-contrast` module adds the step-8 review for all five button
variants and seven states, with both theme results. It consumes the inventory's
`contrast:updated` event and read-only snapshot instead of duplicating contrast
calculations. Each state/theme result aggregates required text and indicator
pairs; conditional boundaries and inactive exemptions stay separate. Selected
details show the lowest ratio for each text/indicator category across audited
contexts and open the existing colour-repair dialog for that exact pair.
`dssSelectButtonState()` synchronizes the shared button settings, controls,
previews and autosave. Review DOM nodes remain stable across refreshes to preserve
disclosures and keyboard focus. The repair dialog returns focus to its opener,
falling back to the full-report summary if that element is no longer available.

The report models named solid-colour contexts and state samples. It does not
scan every rendered element, determine whether a boundary is necessary, or
validate focus geometry, announcements or arbitrary background layers. New state
styles need matching report coverage and browser regression checks.

## Typography and section navigation

`typography-workspace.js` initializes after palette-browser. It relocates original
controls into eight local native disclosures with browse/properties columns and
moves a single real-content specimen to the top of the active stage's right
column, before the properties heading and editable fields. Preview controls,
comparison scope and current website/size metadata travel with that specimen
across all eight stages.
`typography-workspace.css` stacks columns on narrow containers, keeps code/specimen
overflow local and gives controls 44 px targets. Closed local disclosures explicitly
hide non-summary children to keep deferred content out of layout. The original bare
clamp-role select receives a dedicated field shared by Hierarchy and Responsive.
The sidebar holds navigation.
Generated scale roles are fixed; no new saved type schema is introduced.

Original control nodes and listeners remain authoritative. Hidden legacy aliases
retain import/binding compatibility; Configure and fragment routes reveal the
canonical visible editor and its selected family. `revealControl()` only opens
local disclosures; background synchronization never activates another lesson.
Direct stage-summary activation handles the accordion transition before focusing
without implicit browser scrolling and explicitly revealing the new heading.
Closing an open summary retains native collapse behavior. Programmatic toggle
synchronization remains local and silent, so background edits do not navigate.
Scoped resets dispatch the original controls. Explicit lifecycle subscriptions
and a lesson-phase specimen task retain existing state, preview, font-loading,
export and project contracts while avoiding repeated background synchronization.

Specimens parse generated HTML with DOMParser and insert wording through
textContent/value. Component context reads computed styles from the existing live
preview iframe. No additional font-loading document is created. Enlargement and
user-spacing comparisons are memory-only and clear on state replacement. Expensive
specimen rendering runs only while its lesson and local disclosure are open.


`font-sources.js` loads after the registry and before core state. Its registered
module initializes after all deferred scripts have evaluated. The shared
`DSStudio.fonts` API normalizes `state.fontSettings`, resolves heading/body stacks,
builds CSS2 requests and supplies the exact links used by the HTML generator and
learning panel. Core import validates settings before applying state. Legacy
`state.font` remains the installed body stack; older JSON imports stay in system
mode. Google mode uses curated Inter, Source Sans 3 and Literata IDs with known
weight choices, never imported URLs or CSS. Heading and body font tokens export
separately; `--font-ui` aliases the body token for existing components.

The source module updates controls and specimen variables through `output:controls`,
which also catches advanced/button-weight changes. Required page weights remain
included alongside selected additional weights; italic body 400 covers the sample
cite. A shared family is requested once. Managed links are keyed by URL/document,
so unrelated edits preserve their nodes. Loading status checks real font faces,
handles stylesheet/font failure and ignores stale callbacks after source changes.
Retry rebuilds managed links in both studio and preview documents.

Fallback comparison is an in-memory view setting. It removes managed font links
and changes only specimen/preview font stacks; JSON, downloaded CSS and HTML keep
the selected families. Import/reset clear comparison. The responsive iframe strips
font links from parsed HTML, preserves managed nodes through HTML edits, applies
the preview-only CSS fragment and synchronizes its own font links independently.
The download retains ordinary preconnect/stylesheet links and works without a
JavaScript loader. Studio labels/controls keep their existing installed font;
project specimens, button demonstrations and the generated page use project fonts.

`browser_review.py` exercises loading/error/retry with local CSS/font-face fixtures.
`font_cdn_review.py` is an optional network check for actual CDN stylesheets/font
files, responsive preview, standalone export and fallback comparison. The font
catalogue and API syntax were verified against Google's metadata and CSS2 guide;
see [font feature notes](FONT_SOURCES_2026-10-19.md).

Typography uses `state.ratio` for the named/custom modular scale and
`clampConfig.mobileFactor` for a separate heading-size percentage. Tracking is
stored in `state.headingTracking` / `bodyTracking` as em values. Import accepts
older `advanced.tracking` hundredths; that advanced field remains synchronized
for compatibility. Specimens and the size ladder show nominal PX/REM values
using a 16px root, while exports retain relative fluid sizes and em spacing.

The centre pane uses native `details` wrappers with the original section IDs.
`dssRevealSection()` opens destinations for shortcuts; fragment navigation opens
closed ancestors. The sticky section menu and expand/collapse controls precede
the responsive preview, which remains the first centre learning section,
configured in Fluid mode and initially expanded. The active step's centre lesson
also starts expanded; other centre lessons and optional wizard disclosures start
collapsed. Section IDs stay stable
while displayed numbers follow the new order. A direct fragment link opens its
destination. Opening/resizing the responsive section refreshes its width readout.
Section scroll margins follow measured header/navigation heights rather than a
fixed desktop offset, preserving heading visibility when the mobile header wraps.
The same measured header height positions the section menu below the topbar on
all breakpoints. The menu keeps horizontal overflow local and exposes links with
at least 44 px height; native keyboard focus scrolls offscreen items into view.

## Future extension points

- Export formats as modules (W3C Design Tokens JSON, Tailwind config, SCSS, Style Dictionary).
- Component editors beyond buttons (inputs, cards, alerts) using the same state/preview/export contract.
- Theme packs (brand palettes as JSON files in `presets/`).
