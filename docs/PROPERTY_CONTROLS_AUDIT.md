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
| Palette: page backgrounds | Theme/region drafts for colour, opacity, padding and scoped resets |
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
| Buttons | Scoped size, dimensions, shape, weight, focus width, timing and mobile-width drafts; variant/state browsing stays immediate |
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
