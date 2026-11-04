# Architecture

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
import events also cover identical values. Updates coalesce through two microtasks
so legacy import wrappers and the queued preview renderer settle before reading
new values. Unchanged text nodes stay intact, preserving selection and focus.

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
focuses its heading on deliberate navigation. Startup expands only the preview;
navigation never marks completion. The step list is a collapsed Choose a step
disclosure. Numeric indices and existing control/lesson IDs remain compatible.

At 900px and below, existing control panes move directly after their lesson.
Comment placeholders restore them to the sidebar at wider widths; IDs, bindings
and values are unchanged. Previous/Next moves after the output on narrow screens.
The preview iframe never moves: it remains first in the centre above the lessons,
preserving its browsing context. Other sections remain visible as collapsed
disclosures. `DSStudio.activateLesson` lets existing fragment and laboratory
routes select a collapsed lesson before revealing the target.
Ordinary edits preserve control focus and do not invoke stage navigation.

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
| Core | `src/js/studio-registry.js`, `core-state.js` | Registry/events, state, CSS and HTML export |
| Features | `responsive-design`, `design-process`, `brand-palette`, `button-state-practices`, `font-sources`, `css-dock`, `advanced-params`, `journey-library`, `button-design`, `sample-homepage`, `basic-homepage`, `responsive-preview`, `website-export`, `oklch-lab`, `token-catalogue`, `clamp-explorer`, `contrast-audit`, `colour-repair`, `button-contrast`, `typography-controls`, `section-accordions` | One user-facing capability each |

Load order is the order in `index.html`. Scripts are `defer`red; `DSStudio.start()` runs on `DOMContentLoaded`.

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
     },
     exportCss() { return '/* contributed to Export CSS */'; }
   });
   ```
3. Add the `<link>` / `<script defer>` tags to `index.html` and the markup section. The current export generator does not yet call `DSStudio.collectCss()`; exporting a registered module's CSS requires integrating that hook first.
4. Run `python scripts/check_structure.py` and `python scripts/browser_review.py`.

## Known debt (migration path)

Feature scripts still share globals (notably `cssExport` is wrapped by advanced and button modules). Migrating each to `DSStudio.register` and replacing wrappers with `exportCss()` contributions remains a roadmap item. Converting to native ES modules (`<script type="module">`) is the natural next step once globals are gone; a bundler such as Vite can be added then without changing the module shape.

## Project planning workflow

`design-process.js` loads after the registry/font helpers and before core state.
Its `DSStudio.process` API provides fresh defaults, normalization, a bounded
sitemap parser, shared artifact HTML and artifact CSS. `state.designProcess` holds
plain text goal/audience/scope/content/constraints/delivery/success, a multiline
two-level page map,
`split`/`stack` wireframe arrangement, wireframe notes, prototype task and notes.
Imports bound text lengths and accept only the two arrangements; missing or invalid
planning objects receive starter data. Empty draft strings remain empty. No plan
text becomes executable markup, a URL, a CSS declaration or a token.

`site-builder.js` registers after the existing feature modules and before studio
learning. It provides a two-level CRUD editor in Architecture, backed by the same
`designProcess.pages` text and bounded parser. `pageLinks.basic/advanced` store
label-to-fixed-ID mappings (empty string means planned); normalization accepts
only that sample's inventory IDs and at most 64 bounded labels per mode.
`showPlanned` is a validated boolean, default false for legacy plans. CRUD saves
enable planned items in Basic's footer while retaining its Home/Footer exclusion;
Advanced already displays the complete map. Existing label aliases still work.
Relationships affect the map/footer, not the authored body-section structure.
Rename preserves child order and assigned destinations; parent deletion removes
its children. A one-change in-memory undo is cleared by external edits/imports,
reset and mode changes. Text edits and complete-inventory restoration remain.

The same module binds Palette's background picker/hex/reset directly to validated
`semanticOverrides[theme].background`; no second background setting is stored.
Both generators, preview, contrast review, inspector and project flows use that
semantic role. Basic main sections are transparent so the selected canvas remains
visible throughout the page; cards, controls, header and footer retain surface roles.
Partial invalid hex input does not change state. All controls use
the shared apply/render/autosave paths and labels render through DOM text APIs.

The twelve wizard stages are Brief, Architecture, Wireframe, Prototype, Palette,
Typography, Semantic colours, Buttons, Spacing and surfaces, Responsive layout,
Accessibility and Deliver. Existing control and centre IDs remain stable; the
shared stage registry keeps their routes aligned. Planning artifacts appear in
the selected lesson; other stage sections are hidden until selected.

The module's initializer binds planning inputs through the existing `apply()` /
`renderCode()` / autosave paths. It wraps the CSS generator for shared artifact
styles and the renderer for synchronized controls/lessons. Markup caches preserve
unchanged artifact nodes and focus through unrelated palette changes. Editing
replaces the planning object rather than mutating defaults. Existing JSON, local
project save/load/import/reset and New flows include this optional data; the JSON
schema version stays 2 because earlier loaders can ignore the new field.

The static sample adds a planning section, Process navigation and four lesson
cards before the design-system lessons. Studio and sample call the same artifact
helpers with distinct ID prefixes. Wireframes inherit brief/map content; prototype
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
read-only; download complete files to edit their content. The hero demonstrates
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

The registered module adds step-5 editing and full-brand dropdowns for all three
Main Palette roles. Selections copy HEX values through the existing core inputs;
they are independent assignments rather than persistent bindings to reference IDs.
Picker/advanced/OKLCH changes synchronize the matching option or Custom choice.
Reference edits update saved data, exports, the catalogue and contrast candidates
without changing role assignments. The centre swatch display and the legacy
accent picker read the same project palette. Editor nodes stay stable
across updates; names are rendered as text and escaped in reference markup.
Contrast candidate identities include the brand token ID to distinguish duplicate
names and prevent them being mistaken for generated-ramp anchor controls.

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
Settings changes refresh the active language through the existing `renderCode` hook.
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

`responsive-preview.js` initializes after the sample generator and batches
`renderCode` updates into one microtask. It renders the same generated HTML and CSS
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

Basic includes titled unordered/ordered/description list examples. Its equal-width auto-fit card grid uses the saved minimum
and gap rules, adding columns as space permits without manual row spans. Both samples
have a footer Sitemap navigation generated by `DSStudio.process.sitemapHtml()`.
Both samples share one classic footer template and its complete CSS in
`sample-system.js`. Main navigation sits beside the brand and the sitemap is
always visible below it. Advanced keeps its full map; Basic shows only Components,
Layouts and Forms and their known child links. It has no separate Explore
menu, Home/Footer navigation groups or sitemap disclosure. The helper call uses
linksOnly plus a fixed parentIds allowlist. Parent groups occupy responsive Grid
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
In Basic, unlinked entries and children of omitted parents are not promoted. Planning data remains unchanged;
empty filtered maps explain that no linked sections are available. Copyright and
Back to top form the bottom row, and both headers expose `#top`.
The Basic Architecture plan artifact has its own view filter: Forms (including
legacy Sign up/Signup labels) and Footer parent groups are hidden, while all
other parents retain their children. The `.process-map--basic` list lays out
parent groups left to right with children below, wrapping to available width.
Filtering is render-only: the planning editor, saved JSON, page sections and
footer links retain their full inventory. Advanced keeps its original tree.
If filtering removes every group, the artifact explains the empty view.

The shared, fixed inventories in `design-process.js` map all major sections and
content groups, including each Basic card/list and Advanced lesson/workshop.
Stable authored IDs identify these destinations; imported labels never become URLs.
Matching ignores case, spacing and hyphens. Basic accepts its former section
and lesson labels as aliases for stable IDs. Its inventory names Home, Components, Layouts, Forms and Footer. The exact previous complete Basic plan
resolves to the new inventory without rewriting stored data; custom plans keep
their authored labels and legacy destinations.
In the full map, unknown labels remain escaped text marked Planned page; Basic
filters them from its footer. Empty maps remain explicit.

`samplePages(mode)` generates the complete two-level plan. `currentPlan()` resolves
an untouched canonical Basic/Advanced inventory or the exact legacy six-entry
starter to the selected sample's inventory. It leaves custom plans unchanged,
including empty plans. Resolution is pure: stored planning data is preserved;
preview, editor, centre artifacts and HTML exports all use the resolved plan.
The restore button explicitly replaces custom entries with the selected inventory.
It reports applied/already-complete status with section/topic counts and expands
the centre Architecture map without moving keyboard focus. Feedback clears on
planning edits, sample changes or imports with a different plan. Restoring the plan does not generate new pages or change either footer
presentation.
The parser allows 64 entries, two levels and 64 characters per label; the text
field/normalizer cap input at 8,400 characters. Footer links use only fixed IDs.
JSON/local project flows retain custom edits. Main navigation remains a shorter
selection of destinations rather than duplicating the entire content inventory.

Basic footer sitemap is one block with Components, Layouts
and Forms and their known children. The helper's parentIds allowlist is
['features','lists','signup']; Home/Footer and all other parent targets are
omitted without promoting their children or rewriting planning data.
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

The current inventory has sixteen entries, with fourteen links in Basic's
three-group footer. The previous thirteen-entry mock inventory is recognised
alongside older complete inventories, and resolves without changing stored
planning text. Its previous section/topic names remain fixed-ID aliases. Radio
choices, FAQ state and other form values participate in preview capture/restore.

## Basic and Advanced sample modes

`state.sampleMode` is a validated `advanced` / `basic` enum, defaulting to Advanced
for existing projects, startup, New and Reset. It participates in the existing
project JSON and local save/load flows. Invalid imported modes fall back to
Advanced. No separate palette or project state is introduced for Basic.

`sample-system.js` registers before both sample generators. It captures the
shared foundation/component CSS generator after planning styles initialize and
provides common button classes, header navigation text/state styles, footer HTML
and footer CSS. Header links use Advanced's semibold/plain-at-rest treatment in
both modes, independently of general link underlining. Both modes therefore
export the same foundation ramps, semantic roles, typography, spacing, responsive
settings, card/control appearance and Button Design rules. Basic adds its simple
page layout; Advanced adds its gallery/workshop layout. Basic no longer recreates
a partial set of tokens or hard-codes body/heading sizes, spacing, measure,
control dimensions, border widths or card effects. Global link focus follows the
saved focus width, while buttons retain their component focus settings.

`basic-homepage.js` registers after the Advanced generator and before the preview.
It wraps the public HTML/CSS functions to select the current mode; all inspector,
copy, preview and download paths continue through those functions. Basic renders
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

The responsive renderer preserves forms/disclosures/focus/scroll through same-mode
updates and starts a fresh browsing session when mode changes, so unrelated form
values do not cross between samples. Both modes remain static, script-free exports
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
`dssSelectButtonState()` synchronizes the private button editor settings, controls,
previews and autosave. Review DOM nodes remain stable across refreshes to preserve
disclosures and keyboard focus. The repair dialog returns focus to its opener,
falling back to the full-report summary if that element is no longer available.

The report models named solid-colour contexts and state samples. It does not
scan every rendered element, determine whether a boundary is necessary, or
validate focus geometry, announcements or arbitrary background layers. New state
styles need matching report coverage and browser regression checks.

## Typography and section navigation

`font-sources.js` loads after the registry and before core state. Its registered
module initializes after all deferred scripts have evaluated. The shared
`DSStudio.fonts` API normalizes `state.fontSettings`, resolves heading/body stacks,
builds CSS2 requests and supplies the exact links used by the HTML generator and
learning panel. Core import validates settings before applying state. Legacy
`state.font` remains the installed body stack; older JSON imports stay in system
mode. Google mode uses curated Inter, Source Sans 3 and Literata IDs with known
weight choices, never imported URLs or CSS. Heading and body font tokens export
separately; `--font-ui` aliases the body token for existing components.

The source module updates controls and specimen variables through `renderCode`,
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
configured in Fluid mode and initially expanded. All other centre sections and
wizard disclosures start collapsed. Section IDs stay stable
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
