# Web Design System Studio

A dependency-free, browser-based studio for building accessible design systems: brand palettes, OKLCH colour exploration, fluid typography (`clamp()`) calculator, button component designer, state explorer, and exportable CSS / tokens / HTML.

No build step or framework. System fonts work offline by default. Optional Google
Fonts mode loads stylesheets and fonts from Google's CDN; project files and
browser-saved projects stay local.

**Change a design decision, see it on the page, then follow it into HTML and CSS.**

An open-source workshop for understanding how semantic HTML, design decisions
and CSS work together. The browser parses HTML into a DOM tree of node objects;
element nesting establishes parent, child and sibling relationships. CSS
selectors match elements and rules assign property values that control their
presentation and layout. The cascade and inheritance determine the resulting
styles. Design tokens give reusable names to values used by those rules.

For example, a section can contain a heading and a paragraph. Those two children
are siblings; `.card > p` selects paragraph children of an element labelled
`class="card"`. In `color: var(--text)`, `color` is the property and the token
supplies its value. The preview's **How HTML, the DOM and CSS work together**
note explains this relationship alongside the live inspector.

Start in **Build your design system**. One twelve-step wizard selects both the
controls and their matching centre lesson. Each step explains a decision, offers
one task and connects its result to actual output. Use **Previous step** and the
named **Next** action, or open **Choose a step** to jump directly. Planning,
foundations, application and review are phases of this same journey.
The app opens directly into the workspace; its introduction lives beneath
Build your design system, with the project name retained in the app header.
Studio lesson panels, wizard panes and the inspector end with a right-aligned
**Back to top** link. It returns keyboard focus to the studio header while keeping
the current step, project and preview intact. These links stay out of generated websites.

New projects and Reset select **Basic**, shown in the left preview tab; **Advanced**
is on the right. Saved sample choices are restored when loading projects.
The page preview stays visible while you work. **Basic / Advanced** chooses the
sample beside it. **Inspect CSS**, **Inspect HTML** and planning's **Inspect
project data** open the live inspector and select the relevant output. It starts
collapsed to a visible **Live CSS/HTML Inspector** heading above the preview.
Click its disclosure arrow or heading to expand/collapse, just like Responsive
page preview. The expanded right-hand inspector uses at most 25% of the desktop workspace; collapsing
releases its column.
reopening preserves the language and section. Both code files and project JSON
remain complete downloads. Deeper theory and labs
are under **More about…**, with the workflow, catalogue and states available in
**Reference tools**. Navigation records your place, not completion.

Above 900 px, the builder uses 25% of available workspace in both inspector
states. With code collapsed, the preview/lessons use the rest. Opening code above
1280 px restores three columns: approximately 25% builder, 50% centre and 25%
inspector after accounting for gutters.
The centre starts with
**Responsive page preview** expanded at the top and all other sections collapsed.
Choosing a wizard step opens its lesson below the preview. At 1280 px and below,
the inspector stacks after the centre. At 900 px and below, the actual controls
join the selected lesson beneath its explanation. Previous/Next follows the output. The
preview iframe is retained across stage changes, preserving its document and
browsing state. Ordinary edits update results without moving keyboard focus.

In Basic, **Example, rule and tokens** connects examples to exported rules and
live token declarations. Configure selects the token's source step and control.
**Find rule in CSS** opens the complete stylesheet including shared rules. The
optional **Select in preview** mode inspects one example click, then restores
normal actions; Escape and switching samples also cancel selection.

**Step 8: Spacing and surfaces** includes the first tutorial driven by your own
design: Understand, Try, Observe, Inspect and Reflect. It compares a session
starting point with current exported spacing values, shows the actual sample
section and links to complete HTML/CSS. Basic's responsive overrides are included:
its section padding can use eight, twelve or sixteen units depending on preview
width. Grid gap is explained as a separate setting. On narrow screens, the real
spacing controls appear within Try. Comparison history and optional reflection
notes stay in this tab; resetting or loading a project clears them, and they do
not enter saved project JSON or website exports. No completion score is inferred.

The learner trial is prepared in [LEARNER_TRIAL.md](docs/LEARNER_TRIAL.md).
No participant trial has been run yet.

The inspector offers independent **CSS / HTML / Project JSON** language tabs.
Advanced keeps the full field guide.
Basic is a compact UI essentials showcase for a first web-development course.
Home introduces a two-CTA hero and captioned responsive image. Components uses
Flexbox to demonstrate content cards, an avatar/text profile row and a native
FAQ. Layouts demonstrates a responsive card Grid, unordered/ordered/description
lists and a semantic article/aside split. Forms includes labelled fields,
select/textarea, a fieldset/legend radio group, checkbox, native validation and
announced demo feedback. Short labels explain each example without long code
recipes. The inspector provides the full, commented HTML/CSS.
The footer places horizontal main navigation beside the brand. Its sitemap
arranges Components, Layouts and Forms in columns with related links stacked
vertically below each parent; Home/Footer sitemap groups are omitted. Both areas
reflow on narrow screens. Previous complete Basic inventories resolve to the showcase inventory
without overwriting saved planning data, and legacy labels remain safe aliases.
Advanced uses the same classic footer layout with its own main navigation and
complete sitemap. Both have a left-aligned Sitemap title and centred link groups.
The Sitemap heading is a native accordion, initially collapsed. Select its arrow
or heading to reveal the same column layout; footer navigation and Back to top
remain visible. The disclosure also works in downloaded pages without JavaScript.

The selected sample drives the live preview, code panels, copy actions and all
HTML/CSS downloads. Save the matching `index.html` and `tokens.css` together.
The mode travels with project JSON and local saves; older projects and Reset use
Advanced. The Basic form demonstrates browser validation and has no sign-up
service. Basic and Advanced use the same generated design system: colours,
fluid type,
spacing, reading width, corners, card appearance, controls, buttons and responsive
settings. Basic keeps a simpler page layout; planning workshops and state
demonstrations belong to Advanced. Changing modes starts a fresh preview
browsing session.

**Architecture is the sitemap plan.** In **Build your design system → Architecture**, select an entry to edit
its label, parent or existing-section destination. Add/delete entries, move them
within their level and undo the last change. Planned items can appear in the
footer without a link; editing does not create new content sections. The text
editor remains available for bulk edits. The plan updates the responsive preview,
live HTML inspector, exports and saved projects.

**Palette → Webpage backgrounds** follows the Brand and Main Palettes. Choose
Body, Header, Main and Footer backgrounds from every Brand Palette colour, a generated
Neutral step, a custom
picker or hex value. Choices copy the hex value and are saved independently for
light and dark themes. Header and Footer default to Surface; Main follows the
Body background until overridden. Reset each region to follow its default again.
Body is the outer canvas containing Header, Main and Footer. The centre model
shows this nesting, including Body's current colour, contrast and inspection actions.
Each region also has **background opacity**, from 0% transparent to 100% solid,
saved separately for light and dark themes. This changes background paint while
text and controls stay opaque. Body blends over an opaque Surface canvas; Header,
Main and Footer blend over Body. The centre model and contrast checks use those
blended colours. A background reset restores both its colour and full opacity
for the current theme. Older projects default to fully opaque backgrounds.
Header, Main and Footer also offer **Padding** controls for independent top,
right, bottom and left insets, from 0–64 px. Padding is shared across themes and
samples, and adds space around existing content gutters and section spacing.
The centre pane shows the tokens and an inset example. **Reset padding** restores
that region's zero extra padding without changing its background or opacity.
Basic's main sections remain transparent so the Main background shows through;
cards and controls retain their surface colours. The centre Palette lesson shows
the current region colours, text/link contrast and direct CSS/HTML inspector actions.

The starter maps all sections and content
groups in the selected Basic or Advanced sample, including cards, lessons and
workshop topics. Both sample footers use this map, with links to existing content.
The footer Sitemap accordion starts collapsed; identity, key links and Back to top stay readily available.
The original six-entry starter upgrades automatically. Complete sample maps
follow mode changes; custom edits are preserved. **Use complete Basic/Advanced
sitemap** restores the selected inventory, confirms section/topic counts and
opens the centre map for review. Repeated clicks confirm when it is already
complete. Browse **Sitemap** in the preview footer for its links. Use `Parent > Child` for two levels,
up to 64 entries and 64 characters per label. New, unbuilt entries are marked
**Planned page**. This is a single-page content map: main navigation can show a
shorter selection of key destinations. Basic's lists demonstrate `ul`, `ol` and
`dl`, with a tall checklist beside workflow/terms panels when space allows.
Sections stack on smaller screens; shared gap, card minimum, reading width and
responsive settings continue to drive the exported layouts.

The **Project brief** lesson teaches seven website-specific basics: purpose,
audience, pages/features, content, design requirements, delivery and success.
A fill-in template and a small café example show how to write a short brief. The
wizard uses the same seven numbered fields, labels and prompts, in the same
order as the lesson. Content and Delivery have their own saved fields. Older
combined notes are preserved in Pages and features / Design and requirements;
separate them into the new fields as needed. Answers remain under **Your draft
brief** and are never replaced by the example.

The **Responsive** phase follows Layout. Choose the narrow stacking cutoff, wide
spacing start, maximum page width and standard/wide side gutters; these apply to
both samples and their exports. Card minimum/gap controls now live in this phase.
The corresponding lesson shows the current rules and preview media-query state.
The wide start stays at least 160px after the narrow cutoff. Gutters are independent
of the spacing unit. Typography limits and accessibility settings stay in their
own phases. Preview presets are fixed test widths, not saved breakpoints.

Choose breakpoints when content needs to change, following
[web.dev's responsive-design guidance](https://web.dev/learn/design/media-queries).
The brief lesson includes optional further reading from
[Smashing Magazine's website-planning guide](https://www.smashingmagazine.com/2018/02/comprehensive-website-planning-guide-part1/).


The **Live CSS/HTML Inspector** switches between generated styles and a complete
Web Design Field Guide home page. Both update with your selections. Copy or
download the selected tab; save `index.html` and `tokens.css` together to view the page. Its illustrations
are embedded and follow your palette. The static sample includes navigation,
browser/grid illustrations, ten lesson cards, saved project-planning artifacts,
a responsive Grid/Flexbox workshop with an inspectable CSS recipe, live type/palette examples, resource checklists, FAQs
and a practice question form. The interface lab includes button variants,
feedback and progress controls. The form has no message delivery.
Project brand colour tokens use the `--brand-*` prefix.

To download the responsive static website, use the **Live CSS/HTML Inspector**
or the **Deliver** wizard step:

1. In the inspector, select **HTML**, then **Download index.html**.
2. Select **CSS**, then **Download tokens.css**.
3. Save both files in one folder and open `index.html` in a browser.

The CSS file includes tokens, components and responsive page rules. The inspector
shows the matching live source for the selected language.
Downloads use the same generators as the preview and reflect current settings.
The static menu and FAQ disclosures need no JavaScript. Images are embedded;
system fonts work offline. Optional Google Fonts still require their CDN. Forms
are demonstrations with no message delivery.


The wizard configures the system through twelve steps: Brief, Architecture,
Wireframe, Palette, Typography, Semantic colours, Buttons,
Spacing and surfaces, Responsive layout, Accessibility, Deliver and Prototype.
Font sources, responsive type limits, readability, grid rules, surfaces and
interaction settings are part of the wizard. The **main pane teaches** with
component examples, token relationships and practice tasks. Selecting a step
opens its matching lesson automatically, with contextual inspection actions.
Interactive labs remain available for experiments and contrast review.

Brief, Architecture and Wireframe come before palette design. Record the audience,
main task, scope, success signal and constraints in the brief.
Use Architecture's short UX planning overview to identify tasks, define scope,
group and label content, and check a route with the intended audience. Its outcome
is an agreed sitemap connecting essential requirements to pages for the wireframe.
Write a content map with up to 64
entries (`Lessons > Layout` creates a child), compare split/stacked wireframes,
and compare the hierarchy before styling. Prototype is the final review step:
use the finished live page and exported HTML/CSS to test your task, themes and
responsive layout. Earlier Discover, Choose and Review rehearsal screens remain
available in its supporting disclosure. Task notes remain saved project data.

Planning fields travel in local saves, project JSON and the HTML sample. Older
projects receive editable starter planning data. The sample remains a teaching
field guide rather than automatically becoming your finished website. Exported
planning artifacts and prototype links work locally without JavaScript.


Every row in the **Design token catalogue** includes **Configure source**, which
opens and focuses the relevant wizard control. Theme roles select the matching
theme; button colours also select their variant. Derived ramps, type sizes,
spacing multiples and aliases are labelled and configured through their source
decisions. They stay consistent rather than becoming independent overrides.
Heading line-height is now configurable and saved with the project.
New projects and Reset use **Minor Third · 1.2** as the named type scale.
Saved/imported projects retain their explicitly chosen ratio.

See [the teaching and token-configuration review](docs/TOKEN_CONFIGURATION_2026-10-20.md)
for the complete coverage map and the reasoning behind this organization.

In **Palette (step 4)**, keep named brand references separate
from the interface roles. Start with the example colours, or edit names/HEX
values, assign unique token suffixes and add/remove colours in **Edit Brand Palette**
(up to 24). Each declaration shows the complete `--brand-*` token name and hex.
Display-name edits preserve token names; token-name edits update CSS and the catalogue.
Each Main
Palette role—Primary UI colour, Supporting colour and Accent colour—has a dropdown
containing the complete Brand Palette plus a custom colour picker.

Choosing a brand swatch copies its HEX into the selected role. Editing or removing
that reference later keeps the current UI colour; choose the updated swatch again
to apply it. Brand colours and roles travel with local projects and JSON exports.
The reference display, `--brand-*` tokens, catalogue and contrast candidates use
the project's palette. Renaming a colour preserves its token ID. Imported older
projects receive the starter brand references while retaining their UI colours.

**Generate palette steps**, after Main Palette, displays all eleven generated
50–950 shade tokens for Primary, Supporting, Accent and Neutral; 500 preserves each chosen
anchor for the first three. Neutral borrows the Primary UI hue at reduced chroma
and generates its own grey midpoint, so it follows Primary without a separate
colour assignment. Its `--neutral-50` through `--neutral-950` tokens update with
Primary and the selected RGB mix/OKLCH method. They also appear in the catalogue,
contrast candidates and all four background selectors. Existing semantic and
background choices stay unchanged until you select a new value. The centre
lesson reads the actual exported CSS to show brand declarations, shade tokens and
light/dark semantic roles, including custom overrides and inspection actions.

OKLCH is the default for new projects and Reset; saved method choices are preserved.

**Generate state palette steps** extends this process to Success, Warning and
Danger. Each has eleven theme-specific shade tokens, such as `--success-50`
through `--success-950`; step 500 preserves the resolved semantic colour.
Change its colour in Semantic colours or change the ramp method to regenerate
the steps. The wizard and centre lesson show the current theme's exported values,
with CSS inspection and configuration links. Both themes appear in exported CSS
and the catalogue. Existing component state mappings retain their semantic
colours; choose shade pairs deliberately and use text or icons alongside feedback.

**Generate interaction state palette steps** covers every State Explorer state:
Default, Hover, Focus-visible, Active/pressed, Selected, Disabled, Loading, Invalid,
Valid/success and Read-only. Choose General controls or any of the five button
variants to see its state ramps in the wizard and centre lesson. All ramps export
eleven steps per theme, with step 500 preserving the resolved state colour.
Their catalogue sources and inspector actions lead to the existing semantic or
button colour controls. Transparent buttons use their foreground as the ramp
anchor and say so. Disabled opacity, selected/focus rings, progress indicators and
native behaviour remain part of the state design; shade generation does not
automatically remap component styling. The component selector is a view preference
and does not change project data.

Webpage backgrounds comes before Generate interaction state palette steps in
both the wizard and centre lesson.

Every interaction state ramp also has a colour dropdown, starting with its
computed **Default** colour. Choose a Brand colour, Main Palette colour, Neutral
step or shade from the state's current ramp; choices copy a hex value into its
existing source. Default removes that source override. The wizard and centre
dropdowns mirror each other, retain focus and update previews, inspection and
saved projects. General colours apply to the current theme; button colours apply
to both themes, and button focus is shared across variants. Help names the source
and related states affected by a shared edit. Transparent variants edit their
foreground source. Existing custom colours remain selectable after loading a project.

The centre-pane **Palette** shows current Main Palette assignments.
Choose **the UI role to change**, then click any swatch card to set Primary UI,
Supporting or Accent colour. Each card names its action and lists the roles using
that colour; a status message confirms the result. The preview, guided dropdowns,
CSS and active local save update together. **Edit Brand Palette** opens the step-4
editor and keeps project settings intact.

In wizard step **6**, **Semantic colour roles** shows all theme roles with readable
names, CSS tokens, a colour swatch and current HEX/status. Choose the preview theme
and role, then **Preview / edit role colour** to review contrast effects before
applying. **Use generated colour** removes that role's custom override. Changes
update the preview, CSS and saved project; Light and Dark remain independent.

Each main section pairs the button designer's Primary and Secondary variants,
using contextual links between services, resources, contact and the component
gallery. The contact form pairs its sample submission with a link back to services.
Cards retain quieter text actions. All action pairs follow the button designer's
colours, size and optional mobile full-width setting.
Editing Secondary action's custom base colour updates those secondary page links.
Outline is a separate variant demonstrated in the component gallery.

In **5. Design button variants and states**, expand **Review all variants and
states** to check Primary, Secondary, Accent, Outline and Text in all seven states.
Light and Dark results use the same contrast inventory as the full report.
Choose a state, then edit its text/background or shared ring colour. The editor
previews related effects before Apply; changes update the wizard, responsive page,
saved project and exported CSS. Required text/indicator failures, conditional
boundaries and disabled exemptions remain distinct. A contrast result does not
replace keyboard and accessibility testing.

Default button states communicate through shape and text as well as colour:
hover underlines, visible focus outlines, an inset pressed appearance, selected
checkmarks, and a progress indicator with “Processing…” text. Busy samples retain
full opacity; progress animation stops with reduced motion or the studio's
Reduce demo animations setting. Disabled examples
include nearby explanations. The default warm focus colour is checked against
both themes; saved custom focus colours remain editable.

The studio specimens, State Explorer and exported buttons share these cues.
Step 8 explains the state best practices. Toggle examples keep their label between
off/on and use `aria-pressed`; application code must implement the toggle action.
Loading workflows also need duplicate-action protection and status announcements.
The generated home page remains a static demonstration.
Header navigation and resource-table links share the same states: plain at rest,
underlined on hover, a stronger underline while pressed, and a visible keyboard
focus ring. These rules are shared by the responsive preview and exported CSS.

The generated page uses a responsive 12-column grid: six-column halves for hero
and split sections, four-column cards on wide screens, then two or one card per
row as space allows. Card breakpoints use the selected minimum width and gap.
The tutorial workshop demonstrates an 8/4 main/aside split and three equal cards,
then switches to a single-column flow on phones. Its outer example/notes layout
stacks on tablets. Lesson links navigate to real examples on the same page;
type and colour readouts reflect the current wizard selections in each theme.
Default spacing follows an 8 px rhythm with 4 px fine spacing, 24 px gutters and
card padding, and 48 px minimum controls. The existing 4 px foundation unit drives
spacing tokens; saved custom spacing and component dimensions remain editable.
Fonts, borders and focus indicators keep their own sizing rules.

In **Typography studio → Fonts and CDN integration**, choose System fonts or Google
Fonts, then select separate heading/body families. The curated web fonts are Inter,
Source Sans 3 and Literata. Choose additional weights; weights used by the page stay
included. Font choices and weights travel with project JSON and local saves.

**Show fallback fonts in previews** compares wrapping and component dimensions
without changing saved selections or exports. Loading status and a retry action
help distinguish a loaded web font from its fallback. The learning panel shows
the actual HTML stylesheet/preconnect links and CSS font tokens, with explanations
of weights, `display=swap`, `crossorigin` and fallback stacks. The inspector and
downloads use those same sources. Google font files remain hosted externally;
the exported page needs a connection to use them.

The responsive preview opens at the top of the centre pane and renders that same
generated page. Start in Fluid mode, or choose 390, 768 or 1280 px to test a device
width. Browse its navigation and scroll within the page. Light/Dark selectors in
the preview and inspector share the saved project theme; HTML starts in that theme
and CSS includes both. Preview edits retain scroll position, open FAQs and entered
sample form values. Form submissions in the preview are kept local and not sent.
The 390 px preset is a phone checkpoint, not a minimum supported width. Browser
checks also cover 320 CSS px, the narrow-width reference for vertically scrolling
content in [WCAG reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html).

At 768 px and below, the sample header switches to a native Menu disclosure with
an embedded hamburger/close icon. The toggle is borderless with a transparent
background and a normal `--text` “Menu” label; only the icon uses `--accent`,
updating with your palette and theme. The desktop links
remain visible at wider sizes. The menu requires no JavaScript or CDN; optional
web fonts are independent of the menu behavior.
The header pairs a responsive “Logo” placeholder with the project name. The title
uses the selected H2 typography; the logo uses primary/on-primary colours and
the selected corner radius.

## Quick start

```bash
git clone https://github.com/davis-boudreau/webdesignstudio.git
cd webdesignstudio
python -m http.server 8080      # or: npx serve .
```

Open <http://localhost:8080>. Opening `index.html` directly via `file://` also works.

## Project layout

```text
index.html            Markup only (no inline CSS/JS)
src/css/              Stylesheets, loaded in order (tokens -> layout -> features)
src/js/               Classic scripts, loaded in order; studio-registry.js first
docs/                 Architecture, design-system review, roadmap
scripts/              Repository checks
legacy/               Original single-file V4.1 build, kept for reference
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how to add a feature module and
[docs/DESIGN_SYSTEM_REVIEW.md](docs/DESIGN_SYSTEM_REVIEW.md) for the analysis and recommendations.

## Development

```bash
python scripts/check_structure.py   # verifies index.html <-> src/ consistency
python scripts/browser_review.py    # Chrome smoke tests using an isolated temporary profile
python scripts/button_states_review.py # optional: actual reduced-motion and forced-colour modes
python scripts/font_cdn_review.py   # optional: actual Google Fonts downloads and exported-page check
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

For the current handoff and verification baseline, see [Project progress](docs/PROGRESS.md).
[AGENTS.md](AGENTS.md) describes how Codex should maintain these notes across sessions.
See the [CSS/HTML generation review](docs/GENERATION_REVIEW_2026-10-19.md) for grid,
spacing and optimization decisions.

Browser checks require Chrome/Chromium or Edge. Set `CHROME_BIN` if the executable
is not detected automatically. The tests run against a temporary local server.
The regular suite uses local font-face fixtures for deterministic loading/failure
checks; the separate CDN check requires an internet connection.

CI runs structure and browser checks for pull requests and pushes to main through
the reusable validation workflow. Pages publishing, including manual runs, uses
the same validation and waits for it to pass before deploying the checked revision.
GitHub-hosted Ubuntu runners supply Chrome; the application gains no runtime dependencies.

## Licence

[MIT](LICENSE). The studio includes an illustrative example palette and uses locally available system fonts by default.
