# Merge and application recovery audit

4 November 2026, America/Halifax. Audited revision: `20eb0d4`.

## Conclusion

The recent interface and tutorial work is present in the merged source. No
missing wizard, inspector, spacing tutorial or footer accordion implementation
was found in the reviewed changes. One preview asset cache version was rolled
back by the merge. A separate sitemap visibility bug predates the merge, and
some documentation still describes superseded behavior.

The existing suite passes, but a focused audit probe reproduces the sitemap bug.
Passing the existing suite does not clear these findings. This audit changes
documentation only; it does not restore files or change runtime behavior.

## History and comparison

The working tree was clean at the start. `20eb0d4` merges:

- `a253630`: the 4 November Basic background visibility fix, based on `e9c05eb`.
- `40228d4`: architecture/tutorial work after `8c91ac9`, also based on `e9c05eb`.

Compared with `40228d4`, the merge changes six files: README, architecture,
progress, index, browser review and the Basic generator. The three Basic section
background removals and four associated light/dark preview/export checks survive.
The changed index also reverts the responsive preview query version, and the
browser runner combines a longer virtual-time budget with a shorter process
timeout. The latter completed successfully in this session; it is not recorded
as a reproduced failure.

The non-ancestor refs found by `git log --all --not HEAD` are October 15/16 agent
checkpoints, not another November feature branch. This review cannot establish
the contents of uncommitted work on another computer, browser storage, or code
that is absent from this repository's available history. No remote fetch or
deployed-site inspection was performed.

## Findings, in priority order

### 1. Preview script cache version was rolled back in the merge

Location: `index.html:2079`; implementation: `src/js/responsive-preview.js:16`.

`40228d4` references `responsive-preview.js?v=20261103-learning`. The merge
references `v=20261103-ui-essentials`, the query used before example selection
and Escape cancellation were added. The script's new implementation remains
intact, but its URL now reuses an older asset identity.

A returning browser may reuse the older script, depending on caching and
revalidation, while loading the newer learning UI. In that case Select in preview
and Escape cancellation may appear to have been overwritten. This is a confirmed
version rollback and a conditional cache risk, not a reproduced deployed-cache
failure. The isolated-profile suite always exercises the current file bytes.

Recommended correction: give the preview script a fresh query version and add a
merge/release check that changed runtime assets receive fresh version identities.
Do not restore the older script implementation.

### 2. Ordinary sitemap edits override the hide-planned choice

Location: `src/js/site-builder.js:65`, `:101` and `:109`.

`commit()` defaults `showPlanned` to true. Save and delete omit that argument,
whereas reorder passes the current value. Consequently, renaming an existing
linked entry checks Show planned entries even when the user left it unchecked.
Existing planned entries can unexpectedly appear in the footer; the changed
setting also enters saved project data.

Reproduction in an isolated profile:

1. Select Basic, then Architecture. Confirm Show planned entries is unchecked.
2. Select an existing child entry, rename it, and choose Save entry.
3. The checkbox and `state.designProcess.showPlanned` both become true.
4. Undo restores the original name and false visibility setting.

The focused probe reproduced this failure with no JavaScript errors. Link
destination preservation and Undo passed. `git diff e9c05eb HEAD --
src/js/site-builder.js` is empty: this bug predates the merge and is not evidence
of overwritten source.

Recommended correction: preserve the current visibility unless the checkbox
itself changes it. Add regression coverage for rename, creation, deletion,
reordering and Undo under both checkbox states before accepting the correction.

### 3. Current documentation contains conflicting instructions

`README.md:92` correctly says the Sitemap accordion starts collapsed, while
`:122` says the footer map is always visible. `index.html:133` describes section
surfaces keeping their colors without explaining that Basic's main sections now
expose the page canvas; README and architecture describe the newer behavior.
Historical product/workflow reviews also describe the older interface, but are
dated analyses rather than current behavior contracts.

Recommended correction: reconcile the current README and field help while
retaining historical audit results and explicitly superseded decisions.

### 4. Previously identified release-validation gap remains

`.github/workflows/ci.yml` runs the structure check only. The independent Pages
workflow publishes without requiring the browser suite. Neither protects against
the sitemap interaction bug or reuse of an old asset query. This is existing
maintenance debt, not a newly introduced merge regression.

## Preserved decisions checked

| Decision | Current evidence |
| --- | --- |
| One twelve-stage wizard with integrated lessons | Registry, stage routing and existing browser assertions pass; extra Build/Preview/Code/Beginner navigation remains removed |
| App header without a separate branded hero | Current index retains Build your design system and Plan and design your website guidance |
| Desktop builder at 25%; expanded inspector capped at 25% | Current learning-path CSS and responsive geometry assertions pass |
| Native collapsible inspector; preview initially expanded | Startup, collapse/reopen, focus recovery and document-preservation assertions pass |
| Live spacing tutorial | Five lesson parts, actual responsive padding, controls, inspection routes and comparison lifecycle assertions pass |
| Shared footer Sitemap accordion | Both samples start closed; grid, focus, live updates and script-free fragment/export assertions pass |
| Sitemap editor and theme-specific webpage background | CRUD, validation, persistence and light/dark Basic background assertions pass, subject to finding 2 |
| Shared project, preview, inspector and export paths | Existing import/storage/round-trip/export and hostile-data checks pass; no parallel generator or replacement state was introduced by this audit |

## Checks run in this session

- `python scripts/check_structure.py`: **43 assets verified**.
- `python scripts/browser_review.py`: **1246/1246 passed**, no captured JavaScript
  errors. Output: ignored `.reaudit-20261104-browser.log`.
- `python scripts/button_states_review.py`: **5/5 reduced-motion**, **7/7
  forced-colour**, no captured errors. Output: ignored
  `.reaudit-20261104-states.log`.
- Temporary `python .reaudit-20261104-probes.py`: **7/8 passed**, with the expected
  failing visibility-preservation assertion confirming finding 2; no captured
  errors. Both themes' Basic backgrounds, link retention and Undo passed. Output:
  ignored `.reaudit-20261104-probes.log`. Removed the temporary helper afterward.
- `git diff --check`: passed.

Initial sandbox browser launch failed on temporary-profile access. Completed
browser runs used isolated profiles outside the sandbox and did not open the
user's projects or normal browser storage. Older audit counts remain historical.

No new screenshot inspection, manual keyboard-only/screen-reader review,
interactive zoom/touch review, Firefox/Safari tests or live Google font checks
were run. The suite's local font fixtures do not verify external CDN availability.
No source recovery, runtime fix, root sample edit, dependency, commit, push or
deployment was performed. Next: correct findings 1 and 2 with regression coverage,
then reconcile current guidance and address the existing release-validation gap.
