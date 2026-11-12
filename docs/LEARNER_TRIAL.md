# Learner trial: first design-system project

Status: ready to run. No participants have been observed yet.

## Purpose

Find out whether a beginner can connect a control, a visible example and its
generated rule, then export and reopen a small website. The integrated wizard
tasks support the trial; navigation and readiness
acknowledgements are not proof that a task was understood or completed.

## Session setup

- Use a fresh browser profile and a sample project, not someone's saved work.
- Start with a 20-30 minute session. Record an anonymous participant code,
  viewport/device, input method and previous HTML/CSS experience.
- Explain that this evaluates the tool, not the participant. Ask them to think
  aloud. Let them explore before giving instructions or pointing to controls.
- Ask permission before recording a session. Written observations are enough;
  the app has no trial analytics or automatic submission.
- Read each task as a goal. Do not initially give the navigation route. Record
  help when it is needed, including what prompted it.

## Tasks and evidence

| Task to give the learner | What to observe | Completion evidence |
| --- | --- | --- |
| Select the Basic sample and change the primary action colour. | Can they identify the actual action control and compare it with the preview? Do they review text contrast? | The primary action changes; they find its component colour token and can explain its purpose. |
| Make the page spacing more generous. Explain why several gaps change. | Do they use the live Spacing lesson's prediction, before/now comparison, page observation and code connections? Can they distinguish the independent grid gap and Basic's responsive padding multiples? | The preview and active rule agree; the learner explains the foundation/multiple relationship and why viewport width can change the applied multiple. |
| Check the hero at a phone width. Explain what changes the column layout. | Can they reach the preview and code without losing context? Do they confuse presets with saved breakpoints? | They compare 390 px/Fluid and locate the hero rule and responsive override. |
| Study a component of your choice and find its rule and controlling tokens. | Do the example selector, optional preview selection and Configure actions make sense? | They connect a real element to an exact rule, token value and source control. |
| Select the Hero heading and develop a content plan for your audience. Save it and explain what changed. | Can they read the visible Selected content properties, open Develop the content plan and collapse the plan without losing edits? Can they find the actions in Review the Content Plan and understand when that section opens? Can they distinguish an item's outline name from its wording, current content from a proposal, and saved from unsaved edits? Do the example and purpose/owner/next-action prompts help? | Their saved proposal, readiness and notes appear in the outline; the sample heading stays unchanged. They can discard a later unsaved edit and find the saved plan again. |
| Use the Sitemap to find the profile-row example. Exclude its link, then restore it. Explain what changed. | Do they match the visible eyebrow to its Sitemap label and understand the nesting? Can they distinguish Sitemap inclusion from the detailed Website content structure? | The link reaches Flexbox / Profile row; exclusion removes only its navigation link, and restoration brings it back. The example and detailed content remain available throughout. |
| Export the website and reopen it outside the studio. Save a project backup too. | Do they distinguish complete files from excerpts and website files from project JSON? | index.html and tokens.css work together locally; JSON restores the design in an isolated studio profile. |

For someone continuing an older project, optionally ask them to switch between
Page eyebrows and headings and Custom destination plan. Check that they understand
which labels each source uses and can recover their saved custom plan.

For Architecture, observe whether the learner reaches the centre workspace from
the short wizard step and can use its tree and selected-item form together. Ask
them to leave a note unsaved and select another item: can they understand the
Save or discard message and continue? Check Add item placement and Organise content
discovery, the visible property fields and the Review the Content Plan actions. Return
to the step with an unsaved note and repeat at a phone width. Can they reopen
Review the Content Plan after manually collapsing it?
These are trial prompts; no learner observation has yet validated the workspace.

Ask the learner to edit a heading in Website content, save it and locate it in
the website preview and HTML inspector. Then write a different proposal in Develop
the content plan: can they explain which words appear on the page? Try an image
alternative, form label and option wording. Ask them to discard an unsaved edit,
restore the selected item's text, Undo, and save/reopen a project JSON file. Check
whether container and generated-content guidance makes the editable scope clear.
Repeat at a phone width; record any crowding caused by multiple inline text fields.

Ask whether Content structure feels like one organising task. Can the learner
open Review visitor sitemap, change an inclusion choice and explain the adjacent
map? Can they find the optional saved-plan review and Advanced tools without
mistaking them for required extra inventories? For links, observe whether the
automatically revealed related-section reference is helpful.

In Visitor sitemap, ask the learner to search for a nested destination, select it
and explain its location and inclusion. Can they preview an excluded destination
and understand why its content is still present? In custom mode, ask them to edit
a label, attempt another selection, then save or discard and continue. Observe
whether the matching outline/properties pattern reduces the need for help at
desktop and phone widths. These tasks have not yet been observed with learners.

Ask the learner to use keyboard navigation for part of the session. Separately
record focus/scroll problems, inaccessible controls, crowded layouts and unclear
labels. This trial does not replace a dedicated accessibility review.

For the read-only Wireframe workspace, compare Basic and Advanced at phone and
desktop widths, then use Compare with live website. Can the learner recognise the
same content and responsive layout beneath the neutral treatment? Save website
wording in Architecture and return to Wireframe: does the matching text update?
Check native disclosures, local navigation and scrolling within a fixed viewport.
Can they distinguish the read-only wireframe HTML download from finished website
files? These are unobserved trial prompts; record keyboard and navigation problems.

For the guided Palette workspace, ask the learner to add a named brand colour,
change its token suffix, assign it to an interface role and then remove the brand
reference. Can they explain why the copied UI colour remains? Ask them to inspect
the generated shades, choose a page region, create and clear a background override,
and edit Warning in one website theme. Can they distinguish shared anchors from
theme-specific overrides and explain why a shade number does not prove contrast?
Try reopening a stage, a catalogue Configure link and project JSON. Record help
needed, scrolling and keyboard/focus issues at phone and desktop widths. These
prompts remain unobserved; stage navigation is not evidence of understanding.

For the two-column Palette editor, find a brand colour in the left list, add one,
edit its right-hand properties and remove it from the left. Try a search with no
results. Select an anchor, shade family, semantic role, background region and
component variant; can the learner locate the corresponding properties? Propose
a semantic HEX value, preview it, cancel, discard and then apply a proposal.
Observe whether generated read-only fields and fixed roles are understood.
Repeat with keyboard-only input and a narrow viewport; record scrolling and
focus problems. These learner observations have not yet been performed.

For the complete colour-token flow, ask the learner to explain how a brand
reference differs from a shared UI anchor and a theme-specific semantic role.
Edit Surface through a component's source link, preview contrast and return to
Cards. Choose a button variant, change its source and text override, then clear
only that variant's overrides. Observe whether they understand shared focus and
theme scope. In Wireframe, ask them to identify a nested content/list group and
its Grid/Flex parent at desktop and phone widths. These tasks are unobserved.

## Observation sheet

Participant code: ______  Date: ______  Experience: ______

Viewport/device: ______  Browser: ______  Input method: ______

| Task | Independent / helped / incomplete | Time or hesitation | Learner's explanation | Tool issue / next change |
| --- | --- | --- | --- | --- |
| Action colour | | | | |
| Spacing | | | | |
| Responsive hero | | | | |
| Component connection | | | | |
| Content plan | | | | |
| Sitemap | | | | |
| Export/reopen/restore | | | | |

Closing questions:

1. What connects a control, a token and a CSS rule?
2. What is the difference between the preview width and a breakpoint?
3. What would you change in downloaded HTML, and what would you change here?
4. Where did you lose your place or expect something different?

## Turning observations into changes

Keep observed behaviour separate from facilitator interpretations. Prioritise
failures to complete a task, mistaken mental models and keyboard blockers before
cosmetic preferences. Record the proposed change and repeat the affected task
afterwards. Do not treat a small trial as proof of general learning effectiveness.

| Observation | Evidence / participant code | Proposed change | How to check it | Result |
| --- | --- | --- | --- | --- |
| Pending learner sessions | | | | |

Keep raw participant records outside version control. Commit anonymised findings
and resulting product decisions only when there is appropriate permission.
