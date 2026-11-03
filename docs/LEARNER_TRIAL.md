# Learner trial: first design-system project

Status: ready to run. No participants have been observed yet.

## Purpose

Find out whether a beginner can connect a control, a visible example and its
generated rule, then export and reopen a small website. The product's four
exercises support the trial; clicking "I tried this" is self-report, not proof
that a task was understood or completed.

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
| Open First steps with Basic and change the primary action colour. | Can they identify the actual action control and compare it with the preview? Do they review text contrast? | The primary action changes; they find its component colour token and can explain its purpose. |
| Make the page spacing more generous. Explain why several gaps change. | Do they find Layout, use the spacing unit and connect it to derived values? | The preview and rule agree; the learner distinguishes the base unit from a multiple. |
| Check the hero at a phone width. Explain what changes the column layout. | Can they reach the preview and code without losing context? Do they confuse presets with saved breakpoints? | They compare 390 px/Fluid and locate the hero rule and responsive override. |
| Study a component of your choice and find its rule and controlling tokens. | Do the example selector, optional preview selection and Configure actions make sense? | They connect a real element to an exact rule, token value and source control. |
| Rename a sitemap entry and explain the result. | Do they expect a new page or a renamed body heading? Can they locate its footer link or planned status? | They correctly explain that Architecture changes the plan/navigation and does not generate a body section. |
| Export the website and reopen it outside the studio. Save a project backup too. | Do they distinguish complete files from excerpts and website files from project JSON? | index.html and tokens.css work together locally; JSON restores the design in an isolated studio profile. |

Ask the learner to use keyboard navigation for part of the session. Separately
record focus/scroll problems, inaccessible controls, crowded layouts and unclear
labels. This trial does not replace a dedicated accessibility review.

## Observation sheet

Participant code: ______  Date: ______  Experience: ______

Viewport/device: ______  Browser: ______  Input method: ______

| Task | Independent / helped / incomplete | Time or hesitation | Learner's explanation | Tool issue / next change |
| --- | --- | --- | --- | --- |
| Action colour | | | | |
| Spacing | | | | |
| Responsive hero | | | | |
| Component connection | | | | |
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
