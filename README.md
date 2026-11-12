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
named **Next** action, or use **Choose a step** to jump directly. The step list starts expanded and
keeps your open/collapsed choice while switching steps. Planning,
foundations, application and review are phases of this same journey.
The app opens directly into the workspace; its introduction lives beneath
Build your design system, with the project name retained in the app header.
Studio lesson panels, wizard panes and the inspector end with a right-aligned
**Back to top** link. It returns keyboard focus to the studio header while keeping
the current step, project and preview intact. These links stay out of generated websites.

**Studio: Light / Dark** in the header changes only the editing workspace. Its
appearance is a local browser preference, independent of the project. **Page
theme** in Responsive page preview changes the generated page, design examples
and theme-specific colour editors. The inspector's Page theme control uses that
same project setting. You can design a light page in a dark Studio, or the reverse.
Project colours, font size, spacing and corners leave lesson text, editing controls
and inspector styling stable. Component and typography specimens retain project
styling. Studio appearance stays out of saved project JSON and website exports;
project reset/import/load preserve the browser preference.

In **Deliver**, the centre lesson **From CSS tokens to Tailwind utilities** traces
current project values into Tailwind v4 theme names and example utilities. Compare
component CSS with utility HTML for the same four properties, then expand the
live mapping table or theme source. Spacing, colours, fonts, type, separate card/
button radii and saved breakpoint values follow the existing project settings.

**Copy/Download Tailwind theme source** produces an optional `tailwind-theme.css`
snapshot containing the mapped source tokens for both themes and their aliases.
Import it after Tailwind in a consuming Tailwind v4 project and compile there.
Fonts need their installed families or separately loaded font files. The source
maps selected foundations; it does not convert the page's component classes or
implement all states. The Studio keeps its dependency-free runtime and existing
website HTML/CSS exports. No Tailwind compiler or stylesheet runs in the preview.
Re-download the snapshot after edits. The lesson links to official setup guidance.

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
The centre starts with **Responsive page preview** expanded at the top and the
active step's lesson expanded below it: **Brief** on a normal page load. The same
behaviour applies to all twelve steps, including reloading a step's section link.
Other lesson accordions start collapsed. Choosing a wizard step opens its matching
lesson below the preview. At 1280 px and below,
the inspector stacks after the centre. At 900 px and below, the actual controls
join the selected lesson beneath its explanation. Previous/Next follows the output. The
preview iframe is retained across stage changes, preserving its document and
browsing state. Ordinary edits update results without moving keyboard focus.
Architecture keeps its editing workspace in the centre at every screen size.

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

The same step continues with **Read a class, follow its CSS**, starting with
semantic HTML, one linked local stylesheet and the actual exported `.card` rule.
Sample cards reuse component classes. This is the starting approach for the
course: shared rules and tokens keep related styles together. Students can build
and export the whole website with local CSS; no framework transition is required.

The learning transition follows one spacing decision through three forms:

1. **Local component:** `.card { padding: var(--space-6); }`
2. **Local utility:** `.p-6 { padding: var(--space-6); }`
3. **Tailwind:** generates `p-6` using the mapped spacing theme.

A token stores the decision; a class applies it to HTML. The supplied theme maps
Tailwind's `--spacing` to the project's `--space-unit`, so all three examples use
six spacing units. The utility and Tailwind exercises use separate practice
copies, with Tailwind setup and compilation required for the third step. This
progression also connects the palette/token explanations, catalogue, workflow,
Deliver lesson and the exported Advanced page's learning FAQ.

**Inspect card CSS** opens the actual local stylesheet at `.card`. The inspector,
responsive preview and website downloads share the same component HTML/CSS.
Exercise utilities and framework theme source are excluded from those files.

The closed **Next: try one local utility class** disclosure shows a separate
practice version of a sample article. Select a class to see its proposed HTML,
authored rule and current source token. The measurement describes the original
component preview, before applying a utility. Copy the rule to the end of a
practice copy of `tokens.css`, then add the class in that copy's HTML. Compare
`p-6` and `p-4` one at a time, and explain why other cards keep their padding.
An optional nested disclosure lists 20 lesson examples. They are not automatically
added to the website stylesheet. Conflicting utilities follow CSS order and
specificity, regardless of their order in the HTML class attribute.

An optional next-step link leads to Deliver's Tailwind comparison, with a return
link. The exercise uses a separate Tailwind practice project, the mapped theme
source and one article. Students compare generated CSS and computed properties
before extending the example. Local utilities are authored CSS; Tailwind generates
utilities from its theme. Familiar names need the corresponding CSS in each
project, including the theme aliases for custom names. See the official
[utility-class explanation](https://tailwindcss.com/docs/styling-with-utility-classes).
The [padding reference](https://tailwindcss.com/docs/padding) explains how
Tailwind's numeric padding utilities use the spacing theme.

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
uses the four visible section eyebrows, including the Hero, as linked column
headings with related card/section links below them. Existing headings provide
fallback labels. Both areas reflow on narrow screens. Previous complete Basic inventories resolve to the showcase inventory
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

**Information Architecture and Sitemap have different jobs.** The Brief agrees the
release scope. Architecture organizes the full content structure, labels and
relationships, including information inside pages. The visitor sitemap is a
selected navigation view. The lesson includes a Contact/Opening hours example and
[NN/g's IA/sitemap guidance](https://www.nngroup.com/articles/information-architecture-sitemaps/).

In **Build your design system → Architecture**, choose **Open Architecture
workspace** to work in the centre pane. The left step keeps the objective and
review checklist. The workspace places the content outline beside the selected
item on wide screens and stacks them on smaller screens. Add item uses one action
with an inside, beside or top-level placement choice. Organise content groups
move/delete and Expand all / Collapse all; Undo stays with these tree
controls. **Develop the content plan** leads the Architecture workspace, before
Content structure, and identifies the selected item it applies to. **Save and
review** sits beneath the left content browser, grouping Save, Discard, Restore
and their status feedback. **Review the Content Plan** retains the guidance
and saved-plan review separately. It opens on the first unsaved
edit; saving, discarding or an unsaved-edit warning reveals it before focusing
Save. The main content editor keeps Find content and visible properties together.
Review visitor sitemap opens the inclusion choices and their live map together.
Restore retains its scope and Undo guidance. Advanced tools
retains project-data inspection. Sitemap labels and hierarchy is the first control
in Visitor sitemap. Advanced sitemap options holds text editing in custom mode;
the custom destination editor is available in the main Sitemap
view when that source is active.
Longer explanations share About content structure and navigation.

The main control is an expandable,
searchable **Content structure**. It shows meaningful containers and the
actual sample content: Header logo/wordmark/navigation, Home's Hero heading,
paragraphs, image/alternative text/caption and CTAs, component content, lists,
tables, form fields/options and Footer. Basic currently has 139 entries and
Advanced 395; both samples contain five levels of content. CSS-only wrappers are
omitted. Navigation links reference their destinations instead of duplicating
the destination's content. Header and Footer are shared regions.

Expand individual branches, search content or use the Organise content utilities.
Select an entry to inspect its current content and destination reference, change
its planning label/type/parent, write planned content and notes, and set a planning
status. Add child/sibling/top-level entries, move sibling branches, reparent or
delete a branch, and undo the last content change. The content editor supports up
to twelve levels and 1,000 entries as safety bounds, not recommended IA depths.
Repeated role labels, such as Paragraph, have distinct identities and are editable.

The workspace starts with **Develop the content plan**. In Content structure,
**Website content** and **Understand this item** sit beside the content browser;
**Save and review** sits below that browser. The selected
name, location and sample/planning origin provide context. Read the sample content
first, then inspect the item's name, kind, containing item and optional related
section. Plain-language help explains what each property means.

**Selected content properties** stays visible, including the current sample
content, outline name, kind and containing item. **Develop the content plan** is
an optional disclosure, initially closed. Collapsing it keeps unsaved edits.
These headings have no local step numbers; the main wizard tracks the journey.
Selection and adding an item focus the visible name field. The optional Related
website section disclosure opens for links; its section reference and sitemap
shortcut remain available for other content when needed.

Content structure's title and introduction sit inside its left browser. The
properties pane begins alongside that browser, with **Content readiness** always
visible near the top for every item/type. New content starts as Still to create;
existing demo content starts as Available in the sample.

**Proposed wording** starts from the selected demo item's current website copy,
unless you have already saved a proposal. This starting text stays outside the
saved proposal until you edit it or select Include this proposal. Explicitly blank
saved proposals remain blank. Fresh demo notes describe the item's purpose and
next review action in this site, with Owner: Unassigned. Saved notes, including
intentional blanks, are retained; blank notes get a site-specific placeholder.
The planning panel contains working fields without a separate example panel.

Planning prompts adapt to text, images, links, form controls and
containers. Propose wording or describe the required asset, record content
readiness, and note the purpose, owner and next action. **Include this proposal in
the saved plan** distinguishes no replacement from an intentionally blank proposal.
The form marks unsaved edits; **Discard unsaved edits** restores the saved item.
Selection, creation and branch actions keep unsaved edits in place until you save
or discard them. Navigating away and returning to Architecture also retains that
form while the sample content is unchanged. Reset, import and changing samples
load their corresponding plan; save before those project-level actions.
Choose **Save content plan** before selecting another item, then review the
proposal in the outline or centre lesson. Save and Discard retain focus near the
feedback. These are guided parts of Architecture, within the existing twelve-step
journey.

**Website content and planned content are separate.** Website content edits the
actual headings, paragraphs, link/button wording, image alternatives, list/table
text, captions and form labels, help, placeholders, initial text and options.
Save applies these words to the preview, HTML inspector and website downloads.
Inline formatting, link destinations and submitted option values are preserved.
Containers guide you to their children; generated plans/sitemaps and project
identity explain their existing source controls. No HTML editing is required.

Planned wording (including an explicitly empty draft) and notes remain separate
proposals. They do not replace website text or create pages. Both types of edits
persist per sample in project JSON and saved projects. **Use original text for
this item** prepares a restoration for Save; Discard cancels it. **Restore current
sample content** resets that sample's website text and content plan together.
Undo recovers the previous text and plan. The other sample and sitemap choices
are retained. Unavailable or changed text bindings are reported and retained in
the project without applying them to another item.

**Sitemap configuration** defaults to **Page eyebrows and headings**. Each link
uses the section's visible eyebrow text (including slashes), or its existing
heading when there is no eyebrow. Nested links follow the actual page containers.
Basic starts with HTML & CSS essentials, Components / Flexbox, Layouts / CSS Grid
and Forms / Labels & controls. The Hero is included. Labelled cards and content
groups appear beneath their sections; a group legend can supply a heading.
Unlabelled wrappers and the generated Sitemap itself do not add entries.

Choose which sections appear using the inclusion checkboxes. Excluding a parent
suppresses its branch while retaining child choices. **Include all sections**
restores this sample's choices; **Undo sitemap configuration** reverses the last
change. Labels and nesting follow the page automatically. These choices survive
project JSON, local autosave and mode switches. The lesson preview, footer,
HTML inspector and downloaded HTML share the same map and real section anchors.
Selecting a matching section in the content tree offers **Configure this sitemap
section** to focus its inclusion control. Content planning edits never remove
sections from the actual website or this map.

**Custom destination plan** preserves the previous destination editor, text
outline, label bindings, planned entries and three-level navigation bounds.
Both sources now use a searchable, expandable destination outline beside selected
properties. With enough available pane width, Find destination, Selected
destination and Visitor sitemap preview form three columns. Medium panes put
the preview below the two editing columns; narrow panes stack all three in that
reading order. The preview is keyboard-focusable and scrolls within its panel.
Search shows matching destinations with
their containing branches. Outline Include checkboxes and the selected item's
Include control update the same navigation choices. Page-derived labels and
nesting remain read-only; Preview this destination reaches the actual sample
section even when its navigation link is excluded.

Custom mode exposes label, parent, type and destination fields in its selected
properties panel. Add destination and Organise destinations keep creation and
keyboard-operable move/delete actions with the outline. Save destination and
Discard unsaved edits protect changes before selection, branch actions or source
switching. Native inclusion controls preserve inherited exclusions, and Undo
retains the existing per-source behavior. The raw text editor remains advanced.

Older custom outlines retain their navigation until explicitly switched to page
labels; switching sources does not discard either plan's settings. Custom plans
can include unlinked group headings and selected planned entries; their previous
Home/Footer defaults remain compatible. Existing custom outlines still attach
known section content and retain unknown planned entries in the detailed content
plan. Saved content identities survive rename, move and import.

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

Both Sitemap sources link to the selected sample's existing section anchors.
The footer Sitemap accordion starts collapsed while identity, key links and Back to top remain readily available.
Older complete outlines upgrade automatically. Complete destination maps follow
mode changes; custom edits are preserved. **Use complete Basic/Advanced destination
outline** restores that sample's destination plan, leaving the full content plan
unchanged. The optional custom sitemap text editor uses `Parent > Child > Detail` for
three navigation levels, up to 64 nonempty lines and 64 characters per label.

The full content structure above it can describe several levels within one page,
such as Home → Hero → Hero image → Image → Alternative text. Use only the depth
needed to understand content and relationships. Basic's lists demonstrate `ul`,
`ol` and `dl`; layouts continue to use the shared responsive design tokens.

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
Typography, Wireframe, Palette, Colour lab, Buttons,
Spacing and surfaces, Responsive layout, Accessibility, Deliver and Prototype.
Font sources, responsive type limits, readability, grid rules, surfaces and
interaction settings are part of the wizard. The **main pane teaches** with
component examples, token relationships and practice tasks. Selecting a step
opens its matching lesson automatically, with contextual inspection actions.
Architecture also provides the content and sitemap editing workspace in this pane.
Interactive labs remain available for experiments and contrast review.

Brief, Architecture, Typography and Wireframe come before palette design. Record the audience,
main task, scope, success signal and constraints in the brief.
Use Architecture's short UX planning overview to identify tasks, define scope,
group and label content, and check a route with the intended audience. Its outcome
is an agreed information architecture and selected visitor sitemap. In **Typography
(step 3)**, set a working baseline for body/heading fonts, hierarchy, line heights,
reading measure and fluid heading sizes using the site content. In **Wireframe
(step 4)**, check wrapping, reading order and the space needed by sections/cards.
Refine typography as the layout develops; revisit High Fidelity after palette and
component choices. Both wireframe views share the website's type settings.
The **Wireframe workspace** has **Low Fidelity** and **High Fidelity** tabs for
the Basic or Advanced website. High Fidelity is the initial view and retains
configured backgrounds, button colours and imagery for the selected website
theme. Low Fidelity uses a white canvas with unfilled objects and logos, grey
button fills and greyscale imagery to focus on structure and content. Both read-only views use the same
generated HTML, typography and responsive layout as the live website.
Solid outlines show page
regions, dashed outlines show content-width containers, dotted outlines show
Grid/Flex groups and thin outlines show every individual page object and nested
group: headings, paragraphs, inline text, links, buttons, controls, images, icons
and table cells. Each SVG drawing gets one outer boundary. Hidden content follows
the website's responsive and disclosure rules. Hover a boundary to inspect its
HTML identity and layout type. These boundaries
preserve actual spacing and dimensions, including in the HTML download. Saved website wording
from Architecture appears automatically; proposals remain planning data until
applied to website content. Layout and content are edited in their existing tools.

Choose Match live preview, 320, 390, 768 or 1280 pixels, or Available width.
Fixed-width views scroll inside the workspace. Sample and viewport controls choose
what to inspect; they do not save a separate wireframe layout. Form controls are read-only;
local navigation and native disclosures remain inspectable. **Download wireframe
HTML** exports the selected fidelity with embedded styles and container outlines.
Switch tabs with Left/Right arrows or Home/End. Fidelity and viewport choices do
not change saved website settings; tab changes retain scroll and open disclosures.

The optional sitemap text outline still accepts up to 64 three-level entries
(`Lessons > Layout` creates a child). Prototype is the final review step:
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

In **Palette (step 5)**, use the centre **Palette workspace**. The left column is
now a short guide and stage navigator. Work through **Brand colours → UI anchors → Shades → Semantic roles → Page backgrounds
→ Component colours → States and review**, with an
explanation and Previous/Next actions at each stage. Stages can be reopened to
revise a decision; the current-stage marker is navigation, not a completion grade.

Inside each stage, browse and manage items on the left, then view the selected
item's properties on the right. The columns stack on narrow screens. Brand
colours have search, Add and Remove controls; fixed roles and generated families
offer selection and appropriate reset actions. Generated token values use
read-only form fields. Semantic properties offer a HEX field and colour picker
for a proposal: Preview checks its effects, Apply saves it, and Discard restores
the current value.

In **2. Choose UI anchors**, the left list explicitly offers **Primary, Secondary
and Accent**. Each has its own brand selector, custom colour picker and reset
action. Switching anchors keeps the other two colours; all three travel with
saved projects and JSON and generate their respective shade families.

Create up to 24 named brand references, choose one to view its properties, edit
its name/HEX/token suffix, or remove it. Keep at least one reference. Selected
properties stay visible; other rows remain available in the selector. Display
names and token suffixes are separate. Main Palette roles offer the complete
brand list, a custom picker and a reset to their starter assignments. Required
roles and generated shade steps are edited through their sources, rather than
deleted. Direct edits apply immediately through the existing generators;
semantic proposals wait for Apply in the contrast preview.

Choose the website theme at the top. UI anchors are shared; background and
semantic overrides apply to the selected theme. Background editing
shows one chosen region at a time; Use default removes its override. Semantic roles include text, surfaces, borders, actions, focus and feedback. Their
existing contrast preview, Apply and reset controls now live in Palette. Review
keeps feedback selection on the left and its colour properties on the right.
Detailed control/button state customizations and token references are optional
disclosures. Save JSON or your local project to keep the decisions.

The component stage shows resolved exported tokens for cards/panels, inputs,
links and buttons. Edit source opens the appropriate Palette role or component
control. Select a button variant before its source, custom value or state colour
overrides. Clear overrides affects that variant only; it retains its source and
other variants. Shared button focus resets separately. Button colour settings
apply to both themes; semantic overrides remain theme-specific. Base declarations
also apply in dark theme when no dark override exists. The Buttons step keeps
geometry, typography, timing and interaction previews, with a link to Palette.

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
Change its colour in States and review or Semantic colours, or change the ramp
method to regenerate the steps. The workspace shows the current theme's exported values,
with CSS inspection and configuration links. Both themes appear in exported CSS
and the catalogue. Existing component state mappings retain their semantic
colours; choose shade pairs deliberately and use text or icons alongside feedback.

**Generate interaction state palette steps** covers every State Explorer state:
Default, Hover, Focus-visible, Active/pressed, Selected, Disabled, Loading, Invalid,
Valid/success and Read-only. Choose General controls or any of the five button
variants to see its state ramps in the workspace. All ramps export
eleven steps per theme, with step 500 preserving the resolved state colour.
Their catalogue sources and inspector actions lead to the existing semantic or
button colour controls. Transparent buttons use their foreground as the ramp
anchor and say so. Disabled opacity, selected/focus rings, progress indicators and
native behaviour remain part of the state design; shade generation does not
automatically remap component styling. The component selector is a view preference
and does not change project data.

Page backgrounds precedes States and review in the guided workspace.

Every interaction state ramp also has a colour dropdown, starting with its
computed **Default** colour. Choose a Brand colour, Main Palette colour, Neutral
step or shade from the state's current ramp; choices copy a hex value into its
existing source. Default removes that source override. The compact and reference
dropdowns mirror each other, retain focus and update previews, inspection and
saved projects. General colours apply to the current theme; button colours apply
to both themes, and button focus is shared across variants. Help names the source
and related states affected by a shared edit. Transparent variants edit their
foreground source. Existing custom colours remain selectable after loading a project.

The UI roles stage also offers an optional swatch-card view. Choose the role to
change, then click a brand card to apply its value. Each card names the action
and shows which roles use it. Its Edit Brand Palette shortcut opens the selected
colour editor; token catalogue Configure actions open the appropriate stage,
brand row or background region before focusing the source control.

**Assign semantic colours** is part of Palette, after generated shade families.
Choose a role and website theme, preview contrast effects, then Apply or cancel.
Use generated removes only that role's override for that theme. The separate
**Colour lab (step 6)** remains for RGB/HSL/OKLCH exploration, with a shortcut to
Palette. Catalogue source labels use the visible course step, not an internal index.

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
