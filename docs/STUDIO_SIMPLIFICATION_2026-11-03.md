# One wizard, connected lessons

Analysis: 3 November 2026. Proposal only; application behaviour is unchanged.

## Product direction

Keep the studio promise:

> Change a design decision, see it on the page, then follow it into HTML and CSS.

Make **Build your design system** the single guided journey. The centre lesson
belongs to the selected wizard step. Learners should not have to navigate to a
second curriculum to understand the control they are using.

This revises the earlier workflow review's recommendation to retain a separate
Basic shortcut path. The user's current preference is to simplify that structure.

## What creates the friction

Source review confirms three parallel navigation structures: twelve builder
steps, sixteen numbered centre sections, and four opt-in beginner exercises.
Build/Preview/Code/Beginner steps adds another set of navigation choices.

`journey-library.js` changes the active control pane in `showStep()`, but does not
select its lesson. `studio-learning.js` appends Explore the centre lesson buttons
and return-to-wizard buttons. The learner must connect two independently navigated
areas. Several names differ between them, and Accessibility opens the state lab
rather than the main accessibility review.

`learning-path.js` helps connect settings, examples and actual exported rules,
but introduces another task selector, progress counter and set of navigation
actions. First steps also changes the sample to Basic and opens other areas.
Useful teaching mechanisms have become a separate journey.

The centre is currently a long reference library. Startup opens only the page
preview, so the initial Brief step does not begin with its lesson visible.
At narrow widths, independent stacks make travel between the control, lesson,
preview and code especially expensive. These are source-based observations and
earlier recorded layout findings; no new visual or learner trial was run here.

## Proposed workspace

One shared heading identifies the active step, for example **Step 8 of 12:
Buttons**. Under it, show the current lesson and its controls together as one
workspace. At wide widths, the controls can remain on the left and the lesson
and page preview in the centre; their identity and navigation are shared.

Use the same short lesson structure at every step:

1. One sentence explaining the decision and why it matters.
2. One task using the visible controls.
3. What to look for in the page or planning artifact.
4. A precise connection to the relevant generated output.

Show the live page beside or immediately below the active learning area. Place
one code inspector beneath the page, collapsed initially, with explicit Inspect
CSS and Inspect HTML actions where relevant. Opening code should reveal the
matching rule or markup and explain any shared dependencies. Complete files
remain available in that inspector and in Deliver.

On narrow screens, order content within the active step: short explanation,
controls, result, relevant output, Previous/Next. Longer theory and experiments
go in a More about this decision disclosure within that step. Avoid placing a
whole library between the current control and its result.

Do not replace the removed bar with another global tab bar. The preview and code
are results of the active decision, directly reachable within its workspace.

## Remove, integrate and retain

| Existing surface | Proposed treatment |
| --- | --- |
| Build / Preview / Code / Beginner steps bar | Remove; use the wizard and local result/output actions |
| First steps with Basic entry | Remove; start directly in the normal wizard |
| Beginner exercise selector and tried counter | Remove; integrate their tasks into Buttons, Spacing, Responsive and Deliver |
| Sixteen numbered centre links | Remove as a second curriculum; the wizard selects the lesson |
| Explore lesson / Configure in wizard pairs | Remove for the current step; lesson and controls are already together |
| Expand all / Collapse all centre sections | Remove from the guided workspace |
| Long repeated control guidance | Consolidate into the active lesson; keep essential field help beside controls |
| Example-to-token-to-rule connections | Retain as contextual teaching; remove the separate exercise shell |
| Preview click selection | Keep as optional inspection inside the preview, outside the main task sequence |
| Basic / Advanced | Retain as sample choices near the preview; neither starts a separate learning journey |
| Workflow overview | Fold into a short introduction and the wizard step list |
| Token catalogue | Keep as a secondary reference disclosure/tool, with precise source routes |
| Separate centre export and dock code views | Consolidate HTML/CSS inspection; Deliver handles handover and project JSON |
| Project save/load/reset | Keep as global project actions with clear scope |

An inspectable token elsewhere can still navigate to its source. That action
must select both the source step and its lesson, then focus the exact control.
It should not open an unrelated second learning context.

## Wizard organisation

Retain twelve underlying steps for the first implementation. Removing navigation
duplication is a clearer initial change than simultaneously merging lessons and
rewriting stored/token routes. Group the visible step list into four phases;
these are headings, not another navigation control:

| Phase | Steps, using matching control and lesson names |
| --- | --- |
| Plan | Brief; Architecture; Wireframe; Prototype |
| Foundations | Palette; Typography; Semantic colours |
| Apply | Buttons; Spacing and surfaces; Responsive layout |
| Review and deliver | Accessibility; Deliver |

Replace the ambiguous Components and Layout names. Allow direct selection of
any step, so experienced users can skip planning without choosing another mode.
Previous and Next move the entire workspace. Label Next with the destination,
such as Next: Typography. Step position expresses location, not completion.

Keep planning concise but honest: a brief updates project data; Architecture
updates the sitemap/footer; wireframe and prototype update teaching artifacts.
Use the relevant artifact or project data instead of claiming every step changes
page CSS. Whether planning should later be compressed into fewer steps remains
a learner-testing question, not a requirement of this proposal.

## Example: Buttons

**Decision:** Make the main action easy to recognise and read.

**Try:** Change the primary button background using the adjacent control.

The page stays visible at its primary action. Changes update it immediately,
without scrolling, changing focus or requiring an Apply button for a setting
that already updates live. The lesson asks the learner to check the label's
contrast and keyboard focus.

**Follow into code:** Inspect CSS opens the actual `.ds-button--primary` rule
and the current `--button-primary-bg` declaration. Inspect HTML shows the button
or link that consumes that class. Explain shared rules and theme scope rather
than implying the displayed fragment is a standalone stylesheet.

State specimens and deeper colour experiments remain available under supporting
details. Next: Spacing and surfaces selects that step's controls and lesson.
There is no Open control / Show example / Inspect output exercise dashboard.

## Navigation and update rules

- Every entry point selects the same active step and matching lesson.
- A deliberate step change focuses the new shared step heading. It must not
  automatically open code or change design values, sample, theme or variant.
- Ordinary edits update output without moving keyboard focus or resetting the
  user's page/code scroll. An explicit Inspect action may reveal and focus code.
- Choose a representative preview target when entering a step, with a safe page
  fallback if that sample has no direct example. Ordinary edits retain position.
- Returning from a reference preserves the current lesson; choosing Configure
  source deliberately switches to that source's step.
- Preserve draft values when moving between steps. No required exercises,
  automatic completion ticks or new project-data schema are needed.
- Keep temporary colour-repair Apply/Cancel semantics and bounded import
  validation; simplification of navigation must preserve those contracts.

## Implementation and acceptance

First define one stage registry containing stable ID, label, existing control
pane, primary lesson, example target and output connections. Route Next,
Previous, direct selection and token-source navigation through one activation
function. Preserve existing DOM controls, handlers, generators and project data.

Then couple the active lesson and controls, integrate the four useful beginner
tasks, remove duplicate navigation/progress surfaces, and consolidate inspection.
Do not delete `learning-path.js` wholesale: its example mappings and output
connections need extracting or relocating. Remove its obsolete event bindings,
markup and sticky-offset dependencies together. Refresh changed asset versions.

Include the prior audit's confirmed Show CSS, sitemap restore scope, reset
readiness and clipboard feedback defects in the implementation regression work;
those findings remain unresolved by this analysis.

Acceptance should establish that all twelve steps display the correct matching
lesson, every navigation route stays synchronized, edits persist across steps,
and inspection selects the promised language and relevant actual output. Check
both samples and themes, 320px layouts, keyboard focus and unchanged complete
exports. Run the required structure/browser/diff checks after runtime changes.

Observe learners changing one decision, identifying its page effect, and finding
its implementation without coaching. Compare navigation detours and whether they
can explain the connection. The proposal is a design hypothesis, not evidence
of improved learning or accessibility.
