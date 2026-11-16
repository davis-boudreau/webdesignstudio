# Property control audit

14 November 2026. Local implementation; publication and manual accessibility
review are separate. Current check results belong in PROGRESS.md.

The common control is **Save / Discard / Responsive page preview**. Save commits
the area's staged properties; Discard clears only that area's draft. Preview
shows committed project values, preserves drafts, closes other centre sections
and workspace disclosures, keeps the source section/stage open, and focuses and
scrolls to the existing responsive preview. It does not rebuild the preview or
change project settings. Buttons wrap and have a minimum 44px height.

| Area | Control and boundary |
| --- | --- |
| Palette: Brand colours | Shared action bar; existing validated per-colour drafts and atomic save |
| Palette: UI anchors | Draft colour/brand assignments and resets; copied references remain independent |
| Palette: shade generation | Draft shared generation method; calculated shade values remain read-only |
| Palette: semantic roles | Shared bar reuses existing proposal/discard; Save opens contrast review, Apply confirms; Cancel leaves the saved role unchanged |
| Palette: feedback shade sources | Scoped draft/save/discard for optional editable state-source selectors |
| Palette: page backgrounds | Theme-wide region drafts; left controls update a local learning page; one shared bar saves/discards all current-theme regions; padding remains shared |
| Palette: component colours | Variant drafts for source, custom colour, state overrides and reset; shared focus remains a shared model property |
| Palette: states/review | Theme/feedback-role drafts; review instructions are read-only |
| Brief | Draft brief fields, saved together; existing saved brief remains the preview/export source |
| Architecture: content properties | Shared bar reuses existing form Save/Discard, validation and dirty-selection guard |
| Architecture: custom destination properties | Shared bar reuses existing form Save/Discard and dirty-selection guard |
| Architecture: raw destination outline | Scoped draft/save/discard; existing outline normalization still applies |
| Typography: families | Shared Typography draft; curated proposed fonts load only in learning previews |
| Typography: body readability | Shared draft for size, leading, measure and body tracking |
| Typography: hierarchy | Shared scale/heading draft; persistent realistic sample and complete labelled ladder |
| Typography: responsive limits | Shared draft for limits/mobile factor and viewport exploration; global CSS/calculation panel below the collapsible Learning preview; specimen width remains a comparison |
| Typography: content / inline inspection | Read-only source selection and computed text details beside the sample; one workspace-wide action bar |
| Buttons | Combined geometry and multi-variant colour drafts; proposed samples, contrast and CSS; variant/state browsing stays immediate |
| Spacing and surfaces | Scoped unit, radius, surface and component-dimension drafts |
| Responsive layout | Scoped breakpoints, gutters, grid size/gap/alignment drafts; coupled breakpoint validation preserved |
| Accessibility and interaction | Scoped focus, motion, underline and simulated-state properties; contrast repairs keep their existing reviewed Apply/Cancel |
| Prototype | Scoped task/observation drafts and shared preview |
| Colour lab | Shared bar reuses explicit colour Apply as Save; Discard reloads saved coordinates without resetting the project |
| Wireframe / Deliver | Preview-only shared bars; fidelity, view width, file downloads, copy and export filters remain direct operations |

## Typography process review

Five collapsible topics share one control pane and one Typography draft. The
realistic sample and eight-role ladder stay together and immediately show
normalized proposed values. One Save commits all Typography edits; Discard
restores them together. The actual responsive page, JSON, storage and exports
retain saved values until Save. Preview keeps the main Typography section,
closes local disclosures and focuses the saved page.

Body and heading resets stage only their owned settings; heading reset preserves
ratio. Font reset targets the selected family and proposed source. Curated Google
draft fonts use separate learning links with fallback/retry and stale-callback
protection. Discard removes these links without touching saved fonts. System
mode makes no font requests. Selection, enlargement, spacing and viewport remain
view state. Configure and legacy routes reveal the original owning control.
Selected-text computed properties are inline with the preview; the button-edit
shortcut sits beside the sample button. The former Test and review group and
redundant component selector are removed. Comparisons stay above the preview;
Accessibility retains the broader review. Legacy routes reveal inline details.
Current validation results are recorded in PROGRESS.md.

## Deliberately direct operations

Browsing/search, role/region/variant/theme selection, preview widths, specimen
comparisons, inspector/token filters and local appearance are navigation or view
state. They do not need Save/Discard. Generated token declarations have no fake
Save action. Collection commands (add/remove/reorder, sitemap membership/source,
restore/import/new/reset, sample-outline application) retain their explicit
commands and existing undo/dirty guards. Project-library Save/Load and JSON/file
downloads retain their existing meaning. Property resets in the new draft scopes
stage values for Save; they do not serve as Discard.
The semantic role's existing **Use generated** command remains an explicit reset;
its custom-colour proposal still uses the reviewed Save/Apply flow.

## Implementation boundary

`property-actions.js` owns button construction and source-aware preview navigation.
`property-editors.js` binds an explicit catalogue of controls to trusted model
paths. Capture listeners intercept only registered property input/change events;
feature-owned forms, navigation and comparisons retain their original handlers.
Drafts are transient and keyed by scope/context. Save validates controls, normalizes
a detached candidate through the project codec, and merges only edited paths into
the current model, preserving unrelated edits and shared object identities.
It then uses the existing render/autosave lifecycle. External source changes
invalidate conflicting drafts; complete project replacement clears all drafts.
No schema or export-format change is required.

## Inline colour preview audit

The common colour selector previews each palette colour with a thumbnail and
keeps its name, HEX or token visible. Coverage: all four webpage background
palettes; brand/UI assignments; semantic proposal choices and visible role lists;
button colour sources; Colour lab roles; feedback roles; and dynamic state-source
palettes. Existing colour inputs and brand/shade swatch buttons already preview
their colours. Unrelated region, method, font and component selectors remain native.

The original select and its input/change path stay authoritative. Pointer/keyboard
selection stages the same properties; Save/Discard and reviewed semantic Apply
retain their boundaries. Menu browsing/dismissal and swatch refresh do not save.
Only validated HEX values paint thumbnails; imported labels remain plain text.
Current validation results and manual-review gaps are recorded in PROGRESS.md.

## Colour defaults, transparency and sources (15 November 2026)

The user's confirmed meaning is None = transparent paint. Use default is a
separate choice. Required brand-entry HEX values and shade anchors remain valid;
optional paint flags control transparency without corrupting ramp generation.
Role-to-edit lists remain navigation rather than colour assignments.

| Area | None | Use default / source handling |
| --- | --- | --- |
| Main Palette / accent | Transparent associated action paint; retain anchor HEX | Restore starter anchor and opaque paint |
| Page regions | Transparent region background; preserve content opacity | Remove override and transparency; restore inherited/generated paint |
| Semantic proposals | Save transparent role paint | Restore generated role; brand/foundation proposals retain token links |
| General state colours | Transparent semantic paint; retain source ramp | Restore semantic source default |
| Button source | Transparent background states and border | Restore source, clear variant colour overrides/paint flags |
| Button properties / focus | Transparent selected property via nearby None control | Existing reset or a real colour restores paint |

Flags share Save/Discard boundaries; semantic explicit-colour proposals still use
contrast review. Native colour inputs retain a valid HEX fallback and expose a
labelled None toggle with draft-aware pressed state. None uses a checkerboard;
Use default previews the actual generated colour. Contrast/exports consume the
same validated paint flags. Brand source metadata is assigned from validated IDs
and authored shade steps, never inferred from editable display names.

## Typography calculation lesson (15 November 2026)

Generated CSS and Copy CSS remain outside an initially closed native disclosure.
Learn the clamp calculation uses four dynamic steps and stays open during draft
changes. Expansion is view state, with no Save/Discard or project mutation.
Fixed-px roles explain their actual rule; equal bounds explicitly explain the
constant size. The original shared Typography controls retain their scope.

## Background learning page (15 November 2026)

The small Body/Header/Main/Footer page follows a normalized current-theme draft,
with clickable region labels, padding and paint-only opacity. The original shared
action bar sits below controls and preview. Changing the selected region is view
state; Save/Discard applies to all pending regions in the current theme. Shared
padding retains its existing model paths. The saved responsive-page action keeps
the draft and focuses the existing saved website. Selected-region draft CSS and
contrast are separate from optional saved diagnostics. No duplicate action bar or
replacement form controls were introduced.

## Body inset controls (15 November 2026)

Body now has the same four-sided padding disclosure/reset as the other regions.
It creates the outer page frame; Header/Main/Footer padding stays inside those
regions. All use the shared regionPadding map and Save/Discard scope. The learning
page uses exact proposed Body values; full pages and both wireframe fidelities
use the saved CSS. Resets/default buttons reflect draft values as well as saved
values, preserving independent paint/opacity edits when resetting padding.

## Unified Buttons controls

Buttons now has one workspace bar that saves/discards geometry and all proposed
variant colours together. Learning samples, comparisons, CSS and contrast use
those combined drafts. Shared geometry, focus and behaviour are labelled separately
from variant colour overrides. Palette routes to the original colour controls in
Buttons; the records are shared, not copied into a second editor. Palette's own
component actions retain their existing selected-context boundary for its optional
state-source controls. Responsive page preview preserves all drafts and displays
the saved website. Complete references and the saved contrast audit are collapsed.

## Spacing workspace and control-height ownership

Spacing/surfaces reuses one original action bar with its normalized draft. Unit,
base radius, card/field borders, elevation and whole-component opacity update the
local learning page; Save commits those properties and Discard restores them.
Light/Dark is the shared website theme. Local selection/guides/width and token
selection are comparison tools. Archived inspection lessons show saved output.
Control height belongs to Accessibility for display, token navigation and Save;
it is no longer committed by the Spacing scope. Other source links preserve
Palette, Responsive and Buttons boundaries instead of duplicating their editors.

## Buttons theme and elevation

The nearby Website theme selector controls the shared website theme and preserves
button drafts; Studio appearance remains independent. Elevation is a validated
None/Subtle/Medium choice for the selected variant, shared across website themes
through theme-specific resolved shadow tokens. It participates in the existing
combined Save/Discard boundary, project storage and exports. Radius/border/weight
remain shared; elevation and colour overrides are per variant. None removes the
optional variant elevation; clearing colours does not reset elevation. Pressed and
selected cues are composed with depth, while keyboard focus retains its own outline.


## Unified semantic colour workspace

Assign semantic colours now owns the visible background workflow as well as all
other semantic roles. The six-stage navigation omits Apply page backgrounds;
legacy background entry routes reveal the merged stage and region disclosure.
Role controls and their original review actions sit left of the learning sample.
Original region controls/actions retain their current-theme draft boundary in the
same left pane. Selected semantic colour Save still reviews one proposal, while
region Save commits that scope's paint/opacity/padding proposals. Neither commits
the other's unrelated edits. Padding remains shared between themes and website
views. The learning sample composes both proposals into a detached state; full
website previews and exports retain saved values until their corresponding Save.
None is transparent paint; generated reset removes a custom role assignment;
valid foundation token sources remain references. All original control IDs and
project formats are preserved. Current results are in PROGRESS and TEST_COVERAGE.
