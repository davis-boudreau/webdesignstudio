# Architecture

## Wizard configuration and centre lessons

`studio-learning.js` registers last and reorganizes existing control nodes after
the other modules initialize. It preserves their IDs, event handlers and state
paths while placing font, responsive, layout and accessibility settings inside
the eleven-step wizard. Hidden compatibility nodes retain legacy module bindings.
The main pane adds fifteen lessons with token relationships, exercises and
configuration shortcuts. Interactive comparison and experiment controls remain.

The journey exposes `dssShowWizardStep()` for catalogue/lesson navigation and
derives its progress from eleven explicit step labels. Navigation alone does not
mark previous steps complete. Each wizard step links to a related centre lesson;
startup expands only Responsive page preview.

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
| Features | `design-process`, `brand-palette`, `button-state-practices`, `font-sources`, `css-dock`, `advanced-params`, `journey-library`, `button-design`, `sample-homepage`, `basic-homepage`, `responsive-preview`, `website-export`, `oklch-lab`, `token-catalogue`, `clamp-explorer`, `contrast-audit`, `colour-repair`, `button-contrast`, `typography-controls`, `section-accordions` | One user-facing capability each |

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
plain text audience/goal/scope/success/constraints, a multiline two-level page map,
`split`/`stack` wireframe arrangement, wireframe notes, prototype task and notes.
Imports bound text lengths and accept only the two arrangements; missing or invalid
planning objects receive starter data. Empty draft strings remain empty. No plan
text becomes executable markup, a URL, a CSS declaration or a token.

The eleven wizard stages are Brief, Architecture, Wireframe, Prototype, Palette,
Typography, Components, Buttons, Layout, Accessibility and Deliver. Existing control
and centre IDs remain stable; numeric wizard indices and token-source routes move
by three after the old first stage. Four new native centre disclosures follow the
preview hub, bringing the centre navigation to fifteen lessons. Startup still
expands only the responsive preview; navigation does not imply task completion.

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

## Live CSS/HTML Inspector and sample page

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

The studio chrome uses the full window width. `layout.css` sets fixed desktop
tracks through `--studio-controls-width` (310px) and `--studio-inspector-width`
(380px), with the centre consuming the remaining space via `minmax(0, 1fr)`.
Shell gutters also align the top bar with the workspace. At 1280px and below,
the inspector stacks above the centre; at 900px and below, the left pane stacks
as well. Existing sticky behaviour remains on desktop. These layout rules apply
to the studio and do not change the generated sample site's container width.

`css-dock.js` selects `cssExport()` or `htmlExport()` for its shared code panel,
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

The generated container includes its gutters in a 72rem maximum border-box width.
Gutters are 16 px on narrow screens and 32 px from 64rem at defaults. Hero/split
rows use 12 tracks with children spanning six; card rows span four per card.
The generated sample is a Web Design Field Guide: ten lesson cards, a layout
workshop, typography/semantic-palette exercises, resource checklists, practice
question form and the component/state gallery. Existing section/form IDs remain
stable, including `services` for the Lessons destination. Browser/wireframe SVGs
replace the generic landscape illustrations and remain embedded/palette-aware.

The named `sample-content` inline-size container lets card rows switch to two/one
columns using thresholds calculated from `adv.columns` and `adv.gap`. Split rows
stack at 48rem. Responsive layouts therefore retain the existing card controls.
The new `grid-lab` workshop demonstrates twelve tracks with 8/4 and 4/4/4 spans;
the demo uses `--grid-gap` and becomes one column at 48rem. The outer 8/4
example/notes layout stacks at 64rem. A native disclosure exposes the matching
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

## Basic and Advanced sample modes

`state.sampleMode` is a validated `advanced` / `basic` enum, defaulting to Advanced
for existing projects, startup, New and Reset. It participates in the existing
project JSON and local save/load flows. Invalid imported modes fall back to
Advanced. No separate palette or project state is introduced for Basic.

`basic-homepage.js` registers after the Advanced sample generator and before the
responsive-preview module. Its initializer captures the full Advanced HTML/CSS
functions and wraps the existing public generators to select the current mode.
Advanced output is unchanged. Basic produces a small semantic HTML page and a
complete dedicated stylesheet with a subset of shared foundation/semantic tokens,
rather than including the Advanced gallery, workshops or unused component CSS.
The token catalogue continues to read the selected CSS generator.

Basic renders header/logo/wrapping nav, hero, three Grid cards, a native-validation
sign-up form and footer with a real Back to top fragment. It uses the current
project name, theme, curated/system font settings, scale/leading/tracking, heading
weight, radius, semantic palette, grid gap/card minimum and focus width. Other
advanced component simulations do not turn Basic navigation/forms into state demos.
Imported project text is escaped. The static form has no sign-up backend; the
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
HTML/CSS actions sit above the responsive viewport and in Deliver. Both read the
current `htmlExport()` / `cssExport()` at click time, so there is no parallel sample
or cached export snapshot. Files are always named `index.html` and `tokens.css`,
matching the existing relative stylesheet link. Deliver's CSS action previously
used `design-system-tokens.css`; it now uses the shared handler and matching name.
JSON export filenames and project data are unchanged.

The preview card's View HTML/CSS actions select the existing centre inspector's
language tab, reveal it and focus its code panel. Downloads remain two separate
user actions. Shared visible feedback says a download was requested and explains
how to save the pair; the application does not claim browser/OS saving succeeded.
`website-export.css` styles only studio controls and is not needed by the sample.
The static page retains its native menu/disclosures, embedded illustrations and
form demonstration. Google font links remain conditional on the saved font source.

The browser suite captures each file action and verifies exact contents and MIME
types, source shortcuts and unchanged settings. It also loads the captured HTML
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
