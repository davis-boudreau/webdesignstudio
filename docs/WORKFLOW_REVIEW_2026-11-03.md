# Design Workflow and action consistency review

Reviewed 3 November 2026 against the current working tree, including the new
learning path and example connections. This review adds documentation and an
inventory; it does not change application behaviour or replace prior edits.

## Recommended process

Use one twelve-stage project journey, arranged into four phases:

**Plan (1-4) -> Define and apply the system (5-9) -> Evaluate (10-11) -> Deliver (12).**

Within each stage use the same learning loop:

**Configure -> View lesson -> Check example -> Inspect output -> Record/review -> Next step.**

Accessibility is considered during every stage, with a dedicated evaluation stage
before delivery. Stages can be revisited; Next is navigation, not evidence that
work is complete. The Basic beginner path is a short practice route through this
same journey, rather than a second definition of the design process.

The three panes should express one active context. Selecting a stage identifies
its controls, primary lesson and relevant output. Preview, token catalogue,
workflow overview and project library remain utilities available throughout.

## Scope and evidence

- Reviewed all twelve runtime wizard panes, all sixteen centre sections, global
  and local project actions, inspector/study controls, colour-repair actions and
  the Basic/Advanced sample CTAs, forms and state demonstrations.
- Inspected handlers and generated templates, including controls moved into the
  wizard by `studio-learning.js`. Static placement in index.html alone does not
  describe the current UI.
- An isolated Chrome audit recorded **379 groups representing 1,567 rendered
  buttons, internal links and native disclosure controls**, including repeated catalogue/contrast/specimen
  actions and both sample pages. See
  [the button inventory](WORKFLOW_BUTTON_INVENTORY_2026-11-03.csv).
- The inventory groups repeated controls by owner, identifier and label. It
  distinguishes hidden ancestors and disclosures; it is not a complete computed
  visibility or accessibility assessment. Conditional handlers and states were
  reviewed in source; not every possible configuration was exercised.
- Targeted runtime checks verified all twelve forward lesson routes, Show CSS,
  reset/readiness behaviour, cross-sample sitemap restore, export names/payloads
  and clipboard-failure feedback. No JavaScript errors were captured.

## Canonical stage matrix

The order can remain stable. Labels and responsibilities need reconciliation.
The numbers below should be shared by the wizard, centre lessons and overview.

| Stage | Recommended name and responsibility | Primary centre content | Output/evidence to inspect |
| --- | --- | --- | --- |
| 1 | Brief: audience, purpose, content, requirements, delivery and success | Project brief | Saved draft/project data; a clear visitor task |
| 2 | Architecture: entries, parents, destinations and planned content | Information architecture | Project data and footer HTML; distinguish planned entries from existing sections |
| 3 | Wireframe: hierarchy and a structural arrangement | Wireframing | Sketch and saved layout/notes; this choice does not rebuild the Basic page |
| 4 | Prototype: rehearse a task and record observations | Prototyping | Linked exercise and project notes; revisit the brief/map when necessary |
| 5 | Palette: brand references, main colours, ramps and canvas background | Brand palette, with the colour wheel as a supporting lab | Brand/main colour declarations and a themed page example |
| 6 | Typography: fonts, hierarchy, measure and responsive type | Typography studio | Heading/body example and generated typography CSS |
| 7 | Semantic roles and themes: purpose-based colours and overrides | Semantic colour roles; currently inside Colour systems | Active-theme role declarations, surfaces, text and controls |
| 8 | Buttons: variants, dimensions, colour sources and states | Button laboratory | A real action plus labelled state specimens; component CSS |
| 9 | Spacing and surfaces: unit, corners, borders, shadow and opacity | Spacing, surfaces and component examples | Computed spacing/card appearance and the corresponding CSS |
| 10 | Responsive layout: cutoffs, gutters, page width and card constraints | Responsive design, linked to the page preview | Reflow at/around cutoffs; distinguish test presets from saved rules |
| 11 | Accessibility and interaction review | Accessibility quick checks; state explorer as a supporting lab | Contrast findings, native keyboard/control behaviour and human observations |
| 12 | Review and deliver: evidence, usage notes, backup and implementation | Review/export content | Complete HTML/CSS, project JSON, reopened files and known limits |

Stage 7 currently says Components, although its remaining visible controls are
mainly theme/semantic colours. Its introduction still discusses spacing/radius
controls that initialization moves to stage 9. Stage 9 says Layout although
responsive grid settings are in stage 10. The proposed labels describe actual
responsibilities without adding another stage or implying a general page builder.

Planning stages should offer **Inspect project data** when JSON is their actual
output. Architecture can additionally inspect the footer HTML. Presenting CSS as
the output of every planning decision would misrepresent their effect, especially
in Basic, where the planning exercises are not authored body sections.

## Current centre-pane map

| Current centre section | Current relationship | Recommended treatment |
| --- | --- | --- |
| 1 Responsive page preview | Shared generated page; width/theme controls | Persistent unnumbered Preview utility |
| 2 Project brief | Wizard 1, correct return route | Stage 1 lesson |
| 3 Information architecture | Wizard 2, correct return route | Stage 2 lesson |
| 4 Wireframing | Wizard 3, correct return route | Stage 3 lesson |
| 5 Prototyping | Wizard 4, correct return route | Stage 4 lesson |
| 6 Brand Colour Palette | Wizard 5, correct return route | Stage 5 lesson |
| 7 Colour systems | Wizard 7, although main-colour wheel actions concern Palette | Separate primary semantic-role content from the supporting Palette experiment; name each route explicitly |
| 8 Typography studio | Wizard 6, correct return route | Stage 6 lesson |
| 9 Button design laboratory | Wizard 8, correct return route | Stage 8 lesson |
| 10 Spacing, surfaces and component states | Wizard 9; menu abbreviation is Components | Stage 9 lesson, with the same Spacing and surfaces label |
| 11 Responsive design | Wizard 10, correct return route | Stage 10 lesson |
| 12 Component state explorer | Current primary target of wizard 11 | Supporting lab for stage 11, not its only review destination |
| 13 Accessibility quick checks | Returns to wizard 11 but is not its primary Explore destination | Primary stage 11 lesson |
| 14 Inspect and export | Wizard 12; duplicates the live HTML/CSS inspector | Stage 12 review/delivery workspace; keep project JSON inspection here, with explicit links to live HTML/CSS |
| 15 Design workflow | Whole process, but generic Configure returns to wizard 1 | Unnumbered process overview; Resume current stage and explicit Start at Brief actions |
| 16 Design token catalogue | Whole-system utility; generic Configure returns to wizard 12 | Unnumbered token utility; individual Configure source actions retain their precise routes |

All twelve current Explore routes point to existing sections and all primary
return shortcuts point back to the originating numeric stage. The important
problems are the labels, choice of primary target and multiple numbering systems,
rather than missing target elements.

The left stage selector should be the authoritative process numbering. Centre
navigation can group lessons under those stages and list supporting tools without
giving them competing stage numbers. The overview should derive its sequence from
the same definition rather than maintaining a separate eight-item summary.

## Action contract for the whole studio

| Action family | Consistent labels | Behaviour and scope |
| --- | --- | --- |
| Stage navigation | Previous step / Next step; named stage buttons | Update active stage/context; preserve design values; focus the new stage heading; never mark completion automatically |
| Forward learning link | View [lesson name] | Open the matching centre lesson and focus its heading; retain a clear return to the source stage |
| Return/configuration link | Configure [setting or stage] | Open the actual source; select the necessary theme/variant explicitly; focus the relevant control |
| Preview navigation | Show [example] | Reveal and focus the actual example without submitting a form or modifying design values |
| Code navigation | Inspect CSS / Inspect HTML / Inspect project data | Explicitly select the stated output; reveal and focus it; generic Code retains the user's last inspector view |
| Immediate edit | Context-specific input, Use [colour], Save sitemap entry | Update the shared model, preview/output and active-project autosave; announce the result where useful |
| Draft preview/commit | Preview colour -> Apply colour / Cancel | Keep project data unchanged until Apply; return focus after close; retain stale-revision checks |
| Restore/reset | Restore generated [role], Restore [sample] sitemap, Reset current design | State the exact scope. Clearing an override differs from restoring an example value. Preserve unrelated mode/project data |
| Local persistence | Save project locally / Open saved project / New project / Delete saved project | Distinguish browser-local persistence from portable files; retain appropriate confirmation for deleting a saved project |
| Portable project data | Download project JSON / Load project JSON | One schema, payload policy and filename convention across entry points |
| Copy/download | Copy CSS, Copy HTML, Copy excerpt, Download index.html, Download tokens.css | State whether output is a complete file or excerpt; report success/failure honestly; keep component-only and CSV outputs explicitly scoped |
| Example picking | Select in preview / Stop selecting | Explicit opt-in, one-shot selection, Escape cancellation and a keyboard selector; keep normal actions restored |
| Review/progress | Exercises tried this session / Review this project | Keep practice progress distinct from project review evidence and automated checks |

Use links for page destinations and buttons for operations or interactive pane
changes. Button-looking links in the sample pages correctly navigate; they should
not be converted to form/action buttons merely for visual uniformity.

## Findings requiring correction

| Priority | Evidence | Recommended correction |
| --- | --- | --- |
| High | Deliver's Show CSS reveals the centre export panel while its HTML tab remains selected. Runtime audit: HTML selected=true, CSS selected=false. | Route an explicit Inspect CSS action to complete CSS through the inspector API; select the promised language and focus the code. |
| High | Use complete Basic sitemap clears both basic and advanced pageLinks. A stored Advanced Custom -> about mapping was removed by a Basic restore. | Restore the selected mode's map/link scope, preserving the other mode's custom mappings. Expose replacement/undo behaviour clearly. |
| High | A checked readiness item remains checked after Reset, with 1 of 8 checks completed still displayed. | Clear project-readiness acknowledgements when starting/resetting/loading another project; clearly invalidate review evidence after relevant edits. Session practice progress can remain separately labelled. |
| High | Components/Colour systems and Layout/Components use different names for the same routes; twelve wizard stages coexist with sixteen numbered centre entries. | Adopt the canonical stage names and primary-lesson mapping above. Keep utilities outside stage numbering. |
| Medium | Accessibility's primary Explore link opens only the state explorer. | Open Accessibility quick checks first; offer Test component states as a specific supporting action. |
| Medium | Show step/Back/Next changes panes without explicitly focusing the new heading; generic Explore scrolls without explicitly focusing its destination. Token Configure and workspace shortcuts already focus targets. | Share a navigation contract for revealing, scrolling and focusing destinations, with synchronized active-stage context. |
| Medium | Header/centre JSON downloads use design-system-studio.json; Deliver uses design-system-project.json and adds preset=custom. | Choose one portable project export entry point/payload convention and reuse it. This is an inconsistency, not evidence that imports currently fail. |
| Medium | Clamp Copy CSS silently catches clipboard failure; central Copy visible code reports an actionable fallback. Both were tested with a rejected clipboard promise. | Use the same success/failure feedback policy for all copy actions, while keeping their output scope explicit. |
| Medium | Static checkmarks in the Deliver journey summary resemble completion evidence, while Next and readiness are separate mechanisms. | Use a neutral inventory of topics or genuinely data-backed review indicators. Avoid displaying unearned completion cues. |
| Medium | The workflow overview has a generic Configure step 1 button; catalogue has Configure step 12 even though individual tokens belong elsewhere. | Use Resume workflow and Find token source, respectively; retain precise row-level Configure actions. |
| Medium | Studio utility controls mix .ghost, demo-btn, native-looking local buttons and feature-specific rules. | Define one studio action base with primary, secondary/quiet and destructive treatments. Keep specimen buttons governed by the edited design system. |

None of these findings requires replacing the shared generators or adding a
framework. Several existing behaviours are good patterns to reuse: precise token
source routes, reversible colour previews, one-shot example selection, named file
downloads and guarded project imports.

## Coverage of section-specific buttons

- **Brief, wireframe and prototype:** field edits are immediate; View lesson and
  Configure should form a consistent pair. Prototype fragment links navigate the
  teaching screens and should not imply a working sign-up service.
- **Architecture:** distinguish New entry (draft), Save sitemap entry (commit),
  Move up/down, Delete entry/group, Undo last sitemap change and Restore complete
  [sample] sitemap. Keep disabled boundary actions and group counts. A restore
  that replaces custom work needs clear scope and an appropriate recovery path.
- **Palette/colour:** retain Add/remove brand colour, Choose role/use swatch,
  background restore, wheel Load current colour, Apply main colour and Restore
  example main colour. These affect different data layers; labels must identify
  brand reference, main anchor, semantic override and current theme.
- **Typography:** retain Retry font loading, Restore responsive type limits and
  Copy type CSS. Retry is conditional; reset concerns only type interpolation
  limits; the copied fragment needs the same feedback standard as other copies.
- **Semantic roles:** use Preview role colour and Restore generated role colour.
  The repair dialog's candidates preview a value; Apply commits it and Cancel
  abandons it. Hidden compatibility controls need not become primary workflow.
- **Buttons:** keep View button laboratory, Copy button CSS and Download button
  CSS explicitly component-scoped. State tiles and laboratory specimens demonstrate
  appearance/native semantics; lack of a business action is not itself a defect.
- **Spacing/surfaces and state explorer:** distinguish specimen buttons from real
  navigation. Simulated loading/disabled/selected states must remain labelled and
  should not disable the studio's own navigation or export actions.
- **Responsive preview:** width buttons choose inspection viewports; theme controls
  share the current theme. They do not change saved breakpoints. Preserve visible
  pressed state and distinguish Fluid from fixed presets.
- **Accessibility:** filter/sort/search are review controls. Edit this colour must
  open the shared preview/apply flow; Download filtered contrast CSV should continue
  to describe its filtered scope rather than implying a complete audit export.
- **Inspect/export and catalogue:** retain complete-file output, explicit excerpt
  copy, project JSON and filtered token CSV. The central and dock inspectors should
  have a clear division of responsibilities and unambiguous language selection.
- **Project library/global controls:** Reset current design, New project, Delete
  saved project, Save locally and Download JSON are distinct operations. Their
  labels, confirmation/recovery and feedback should consistently explain scope.
- **Beginner controls:** keep the four exercises as shortcuts into the canonical
  stages. Open control, Show example and Inspect output must use those same route
  helpers. I tried this records practice, not project readiness or validation.

## Sample-page CTAs

Basic already has a coherent internal sequence:

**Home -> Components -> Layouts -> Forms -> Footer/navigation.**

Each main section offers a primary/secondary pair; component links provide more
specific destinations. Submit demo form performs native validation and displays
demo feedback in the studio. Back to layouts is navigation. The mobile header and
FAQ use native details/summary rather than JavaScript action buttons.

Advanced is a fuller field guide: hero/about introduce lessons, process and layout
exercises lead to resources/components, and contact provides the demonstration
form. Its section CTAs need labels meaningful to that content, not identical text
to Basic. Consistency should apply to primary/secondary hierarchy, destination
clarity, focus, responsive targets and demo-state labelling.

The sample pages are learning specimens, separate from the studio's own process
navigation. A sample link should browse its page, while a studio Inspect action
should open a rule/control. Optional example-picking mode explicitly switches the
next preview click to inspection and then restores normal behaviour.

## Implementation sequence

1. Correct the confirmed action/feedback/scope defects: Show CSS, cross-mode
   sitemap restore, readiness lifecycle and silent clipboard failure. Add outcome
   regressions for these before changing the information architecture.
2. Define a shared stage registry with stable IDs, one label, control pane, primary
   lesson, supporting labs and relevant output. Generate wizard labels, centre
   routes, overview and stage-specific shortcuts from that definition. Preserve
   existing DOM IDs/import compatibility where practical.
3. Consolidate navigation helpers and studio button presentation. Test forward and
   return paths, focus/scroll offsets, unchanged design values and explicit
   theme/variant selection. Keep sample component styling independent.
4. Walk through the resulting complete journey and Basic shortcut route with
   learners using LEARNER_TRIAL.md. Check whether they can predict each action and
   explain the relationship between controls, lessons, page and output.

## Verification and limits

The targeted audit ran in a temporary Chrome profile with downloads intercepted
in memory. All twelve forward/return numeric mappings existed and no captured
JavaScript errors occurred. The confirmed defects above concern action semantics,
scope and feedback, even though the previous general regression suite passed.

Current `python scripts/check_structure.py`: 41 referenced assets verified.
Current `git diff --check`: passed. The full browser regression suite was not
rerun for this documentation-only review; its earlier 1082/1082 and focused 38/38
results remain historical. No learner trial, manual keyboard-only/screen-reader
review, cross-browser testing, runtime edits, commits or deployment occurred.
