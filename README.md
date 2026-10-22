# Design System Studio

A dependency-free, browser-based studio for building accessible design systems: brand palettes, OKLCH colour exploration, fluid typography (`clamp()`) calculator, button component designer, state explorer, and exportable CSS / tokens / HTML.

No build step or framework. System fonts work offline by default. Optional Google
Fonts mode loads stylesheets and fonts from Google's CDN; project files and
browser-saved projects stay local.

The studio fills the window. On desktop, the controls stay 310 px wide and the
inspector stays 380 px wide while the centre pane takes the remaining space.
The inspector stacks at 1280 px and below; all panes stack at 900 px and below.
On a normal load, only **1. Responsive page preview** is expanded in the centre
pane, in Fluid mode. All other centre sections start collapsed. The preview stays
synchronized with wizard edits even when you collapse it.
The **1–16 section menu** sits above the responsive preview and stays pinned below
the app header while you browse the centre lessons, including on phones. Scroll
the menu horizontally when needed; keyboard focus reveals offscreen links.

The **Live CSS/HTML Inspector** has **Advanced / Basic** sample tabs above its
independent **CSS / HTML** language tabs. Advanced keeps the full field guide.
Basic provides a minimal responsive homepage: logo and wrapping navigation, hero,
three CSS Grid cards, a three-column lists lesson, a labelled static sign-up form
and a footer with Back to top and an Architecture-driven sitemap.
Its shorter, commented CSS teaches Flexbox, Grid, spacing, typography and focus.

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

**Architecture is the sitemap plan.** The starter maps all sections and content
groups in the selected Basic or Advanced sample, including cards, lessons and
workshop topics. Both sample footers use this map, with links to existing content.
The full map
is expandable; identity, key links and Back to top stay readily available.
The original six-entry starter upgrades automatically. Complete sample maps
follow mode changes; custom edits are preserved. **Use complete Basic/Advanced
sitemap** restores the selected inventory. Use `Parent > Child` for two levels,
up to 64 entries and 64 characters per label. New, unbuilt entries are marked
**Planned page**. This is a single-page content map: main navigation can show a
shorter selection of key destinations. Basic's lists demonstrate `ul`, `ol` and
`dl`, with three titled cards side by side when space allows.

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

To download the responsive static website, use **Download this responsive website**
above the preview, or the **Deliver** wizard step:

1. Select **Download HTML (index.html)**.
2. Select **Download CSS (tokens.css)**.
3. Save both files in one folder and open `index.html` in a browser.

The CSS file includes tokens, components and responsive page rules. **View HTML
code** and **View CSS code** open the matching live source under Inspect and export.
Downloads use the same generators as the preview and reflect current settings.
The static menu and FAQ disclosures need no JavaScript. Images are embedded;
system fonts work offline. Optional Google Fonts still require their CDN. Forms
are demonstrations with no message delivery.


The **left pane configures** the system through twelve wizard steps: Project Brief,
Information Architecture, Wireframing, Prototyping, Palette, Typography, Components,
Buttons, Layout, Responsive, Accessibility and Deliver.
Font sources, responsive type limits, readability, grid rules, surfaces and
interaction settings are part of the wizard. The **main pane teaches** with
component examples, token relationships and practice exercises; each section
links to its wizard settings, and each step links back to a centre lesson.
Interactive labs remain available for experiments and contrast review.

The four planning lessons come before palette design. Record audience, main task,
scope, success signal and constraints. Write a content map with up to twelve
entries (`Lessons > Layout` creates a child), compare split/stacked wireframes,
and follow a linked Discover, Choose and Review prototype. Save observations and
revise before styling. The prototype is a low-detail navigation exercise with no
submission backend. The brief and architecture feed the wireframe and prototype;
they are project notes, not generated CSS tokens.

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

In **2. Brand Palette and Main Palette**, keep named brand references separate
from the interface roles. Start with the example colours, or edit names/HEX
values and add/remove colours in **Edit Brand Palette** (up to 24). Each Main
Palette role—Primary UI colour, Supporting colour and Accent colour—has a dropdown
containing the complete Brand Palette plus a custom colour picker.

Choosing a brand swatch copies its HEX into the selected role. Editing or removing
that reference later keeps the current UI colour; choose the updated swatch again
to apply it. Brand colours and roles travel with local projects and JSON exports.
The reference display, `--brand-*` tokens, catalogue and contrast candidates use
the project's palette. Renaming a colour preserves its token ID. Imported older
projects receive the starter brand references while retaining their UI colours.

The centre-pane **2. Brand Colour Palette** shows current Main Palette assignments.
Choose **the UI role to change**, then click any swatch card to set Primary UI,
Supporting or Accent colour. Each card names its action and lists the roles using
that colour; a status message confirms the result. The preview, guided dropdowns,
CSS and active local save update together. **Edit Brand Palette** opens the step-5
editor and keeps project settings intact.

In wizard step **4**, **Semantic colour roles** shows all theme roles with readable
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

## Licence

[MIT](LICENSE). The studio includes an illustrative example palette and uses locally available system fonts by default.
