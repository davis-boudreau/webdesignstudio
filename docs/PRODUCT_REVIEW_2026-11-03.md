# Design System Studio: product and system review

Reviewed 3 November 2026, starting at `e9c05eb`. This review examines the current
repository, including the Basic UI essentials showcase, inspector study excerpts,
sitemap editor and theme-specific webpage background. Earlier workshop layouts
and audits are historical. No application behaviour was changed for this review.

## The vision

The tool's strongest purpose is to help a learner understand how design decisions
become reusable rules, how those rules shape a real page, and how that page is
implemented in HTML and CSS. Its distinguishing experience is a visible loop:

**Make a decision -> observe the page -> inspect the rule -> test another context.**

The left wizard, centre preview/lessons and right inspector are three views of
the same work. A learner should finish with both usable files and an explanation
of why the design works. That is a more useful direction than adding controls
without making their consequences easier to understand.

This interpretation matches `webd-UI-scope.md`: semantic HTML, normal flow,
Flexbox, Grid, native controls and accessible interaction before more elaborate
widgets. Basic now expresses that scope substantially better than the earlier
fictional workshop landing page. Advanced provides a broader field guide using
the same foundations.

## What is working

- **A credible decision-to-code connection.** Basic and Advanced select the public
  HTML/CSS generators; preview, inspectors and downloads consume those generators.
  Basic excerpts are derived from complete output, rather than maintained as
  independent teaching examples. Copy/excerpt versus complete-download behaviour
  is explicitly explained in the UI.
- **Useful token relationships.** Brand references, interface roles and component
  values have distinct jobs. The catalogue can take a learner back to a setting's
  source, including derived values. This makes the system explainable rather
  than merely configurable.
- **A contextual preview.** A real iframe exercises generated viewport rules;
  isolated component swatches alone would not expose navigation crowding,
  wrapping, reading order or form layout. Shared Basic/Advanced foundations allow
  different compositions to demonstrate the same design decisions.
- **A coherent beginner specimen.** Basic includes meaningful landmarks, cards,
  profile layout, native disclosure, lists, Grid, article/aside and grouped form
  controls. It supports the agreed scope without requiring a framework or backend.
- **Responsible boundaries.** Planned sitemap items are distinguished from real
  destinations. Imported values are bounded and validated, and labels are escaped.
  Demo forms describe their limitations. System fonts work locally; optional
  curated Google Fonts are a separate, documented network choice.
- **Substantial regression coverage.** The suite exercises saved projects, imports,
  corrupted storage, unsafe content, responsive geometry, themes, component states
  and export agreement. That is an important asset to preserve as the tool grows.

## Where the product is less clear

### 1. The learning loop is connected technically but expensive to see

In an isolated 1440 x 900 studio viewport, with Basic selected and its guided
exercise disclosure closed, the inspector code starts at approximately y=947.
There is no code in the initial visible viewport. The workspace begins around
y=323, and the Fluid sample viewport is approximately 562 CSS px wide. A desktop
browser therefore initially shows the sample's narrow navigation, which is valid
responsive behaviour but can surprise a beginner.

At 1280 px the inspector is placed before the preview. At 390 px, its top is
approximately y=3715 because the wizard precedes the right-hand workspace. These
are measurements of the tested initial states, not proof that controls are
unreachable: scrolling and the inspector's own scrolling work. They do show that
the core cause/effect comparison requires substantial navigation.

**Recommendation:** reduce introductory space after first use and provide clear
Build / Preview / Code access on narrow screens. On desktop, prioritise useful
preview and code space over repeated instructions. Make the distinction between
the studio window and the sample viewport immediately understandable. Evaluate
this before adding more controls to either side pane.

### 2. Three product roles compete for attention

The app is simultaneously a design-system editor, a web-development course and
a planning workspace. Twelve wizard stages, sixteen centre destinations and
independent sample/language/study-section choices are defensible individually,
but together require a learner to understand the tool before using it.

Advanced is currently the default. That preserves existing project behaviour,
but it is not the smallest starting point for the beginner scope.

**Recommendation:** keep a deliberate beginner path, with Basic selected for a
new beginner session while preserving saved projects. Consider language such as
Essentials and Full field guide to explain the sample choice. Offer a short
first-success exercise before requiring the complete planning sequence; keep the
full twelve-stage journey available for a project-based lesson.

### 3. Planning and page generation have different powers

The sitemap editor changes the map, relationships and safe destinations. It does
not add, rename or reorder authored body sections. The wireframe illustrates a
structural choice, while the prototype is a fixed Discover / Choose / Review
exercise. They are valuable planning artifacts, but they are not a general page
builder or a prototype of every learner's actual site.

There is also intentional view filtering: Basic's centre Architecture artifact
omits Forms/Footer groups, while its footer omits Home/Footer groups. Notes
explain this, but different maps can look inconsistent to a learner.

**Recommendation:** label planning artifacts by what they affect, and show one
clear distinction between an existing section and a planned page. Explain view
filters beside each map. Treat body-content editing or section assembly as an
explicit future product decision, rather than an implied consequence of sitemap
CRUD. A site builder would introduce a separate content model and substantially
expand validation, accessibility, migration and export responsibilities.

### 4. Generated code can be readable without being easy to learn

Section comments and study excerpts improve Basic considerably. Complete CSS
still includes the shared foundation/component system, and excerpts depend on
that complete stylesheet. The UI correctly says so. The remaining opportunity is
navigation from a visible example to its exact rule and source control.

**Recommendation:** connect a selected example to its HTML, relevant CSS and
controlling token. Show changed declarations or a small explanation after an
edit. Preserve complete files for downloads and dependency information for
excerpts. Avoid introducing an editable code pane until the desired relationship
between authored code and generated state is defined.

Also distinguish a live dependency from a copied value. Selecting a brand swatch
copies its HEX into an interface role; editing the brand reference later does
not automatically rebind that role. The current documentation explains this,
but a dependency view should make that behaviour visible. Equal values are not
necessarily aliases, and this matters to the learner's mental model of a system.

### 5. The design system needs reasons as well as values

The current tool is strong at foundations, semantic roles and component output.
The brief and review notes introduce purpose, but there is less support for
recording why a particular scale, spacing rule, role assignment or component
variant was chosen and when it should be used.

**Recommendation:** use existing lessons and project notes to capture a small
number of decisions and usage rules. A learner should be able to explain why a
secondary action differs from a primary action, not just produce two colours.
Avoid implying that exported tokens alone constitute a complete organisational
design system.

## Engineering and maintenance

The runtime is appropriately local and dependency-free. A framework rewrite is
not necessary to improve this product. The principal technical risk is the chain
of wrappers around `apply`, `renderCode`, `cssExport` and `htmlExport`, whose
behaviour depends on module order. The registry exists, but its CSS contribution
API is not the actual assembly path. The catalogue also reconstructs metadata by
parsing CSS lines and interpreting token names.

Incrementally establish an explicit state/update contract and generator API,
then move token/source metadata into shared definitions. Preserve output parity
with the existing regression suite during that work. This is supporting work for
reliability, rather than a prerequisite for every small UI improvement.

CI currently runs the structure check only. Pages deployment is a separate
workflow and does not depend on browser verification. Browser regressions should
gate publishing. A small, intentional set of visual checks should complement
geometry checks; passing the current suite does not establish classroom usability,
complete accessibility or Firefox/Safari compatibility.

Documentation is beginning to drift. For example, README still describes an
asymmetric tall checklist and a twelve-entry map, while the current Basic page
uses equal Grid list cards and the bounded editor supports 64 entries. Preserve
historical reviews, but keep one current product description aligned with the UI.

## Recommended order of work

| Order | Focus | Observable result |
| --- | --- | --- |
| 1 | Clarify the beginner path and planning boundaries | A learner can identify what each edit changes and what files they will receive. |
| 2 | Improve preview/code access and example-to-rule navigation | A learner can change a setting, see the result and find its rule without losing context. |
| 3 | Observe a small learner trial | Test whether learners can explain and repeat the workflow, not merely click through it. |
| 4 | Gate publishing and simplify update/generator contracts | Regressions are caught before release and new features need fewer cross-module patches. |

For a learner trial, ask participants to change a primary action colour, explain
its token relationship, adjust spacing/type, inspect a mobile layout, edit one
sitemap entry, and export/reopen the complete page. Observe where they hesitate,
whether they understand the read-only inspector, and whether they mistake a
planned item for a generated page. Include keyboard use in this evaluation.

## Verification for this review

- Source review: README, current progress/architecture, the user-owned UI scope,
  historical design/audit notes, UI markup/styles, generator/state/inspector,
  sitemap/planning, token catalogue, persistence and CI/deployment paths.
- Current `python scripts/check_structure.py`: 39 assets verified.
- Fresh `python scripts/browser_review.py`: the normal run exceeded its
  120-second process timeout without a completed report. An isolated rerun of
  the same harness, using `python .system-analysis-run.py` (a temporary driver
  allowing 240 seconds), passed **1045/1045**, with no captured JavaScript errors.
  The virtual-time budget and assertions were unchanged. The driver was removed
  afterward; output is in ignored `.system-analysis-review.log`. The earlier
  1045/1045 result in PROGRESS belongs to the previous implementation session.
- Current `git diff --check`: passed.
- Isolated Chrome screenshots/measurements: Advanced at 1440 px; Basic at 1440,
  1280 and 390 px, each using a 900 px studio viewport height. Screenshots support
  initial-layout observations only, not a full interaction or accessibility audit.
- No runtime edits, user-storage access, commits, deployment or learner study.

Assessment: the tool has a coherent educational vision and a well-tested
functional foundation. Its next major improvement should make the existing
decision-to-result-to-code loop clearer, rather than broaden the feature list.
