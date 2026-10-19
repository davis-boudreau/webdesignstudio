# Project review — 19 October 2026

Reviewed the current `index.html`, all nine JavaScript files, all seven stylesheets,
project documentation, structure checker, and GitHub Actions workflows. Runtime
checks used headless Chrome, an isolated temporary profile, and a local server.
The legacy single-file build remains a historical reference; the functional fixes
below apply to the current modular application.

## Errors found and corrected

| Finding | Effect | Correction |
|---|---|---|
| Responsive typography settings were absent from project JSON | Custom viewport boundaries and mobile heading factors could not be restored from a backup | Include and validate `clampConfig` in JSON exports and browser-local projects |
| Reset left responsive typography settings intact | A supposedly new/default project retained the previous project's typography configuration | Reset clamp settings with the other foundation values; importing an older project supplies defaults |
| Autosave did not cover every editor or ran before updates | Advanced select/checkbox changes, clamp changes, and some palette actions could leave saved projects behind the visible interface | Save after state updates; use the shared project serializer for browser-local saves |
| Import/reset could save intermediate values over the active project | Switching or resetting could alter the project being left | Suspend autosave while importing; detach the active saved project before resetting |
| Numeric select import treated heading weight as a range | A saved heading weight became `NaN`, which propagated into CSS | Validate numeric select values against their options; use range bounds only where present |
| Exported examples dropped selected settings | HTML always opened in light mode and omitted the chosen button size; card opacity and grid alignment were not applied | Preserve theme and button-size classes; consume opacity and alignment tokens in exported CSS |
| Button colour exports depended on the currently active theme | Transparent button text could be exported using the wrong theme's foreground choices | Export explicit light and dark button token blocks |
| An inherited object property was accepted as a button variant | Malformed imported variants such as `__proto__` could cause later rendering errors | Accept only the variant map's own properties |
| Code tabs lacked the expected keyboard and panel relationships | Arrow-key navigation, managed tab stops, and active panel labelling were missing | Add Arrow/Home/End navigation, tab stops, `aria-controls`, and active-panel labelling |
| Default button focus colour had weak contrast against white | The previous orange measured 2.88:1 against white | Use a default measuring 5.02:1 against white and 3.18:1 against the default dark surface |

Also added a skip link, connected the advanced input's help text, exposed its
loading state with `aria-busy`, and corrected the outdated section-count copy.
Asset version parameters were refreshed so deployed browser assets can update.

## Verification

`python scripts/browser_review.py`: **43 checks passed**, with no captured startup
or interaction JavaScript errors. Coverage includes:

- Live CSS/export agreement and neutral CSS, JSON, and HTML output.
- RGB and OKLCH ramp anchors and valid HEX colours, plus known contrast ratios.
- Theme synchronization, selected fonts, responsive typography round trips, and reset.
- Autosave for advanced controls and clamp settings; protection of saved projects during import/reset.
- Button and heading-weight round trips; bounded imports and malformed variant fallback.
- Theme and size preservation in exported HTML; computed card opacity and grid alignment.
- Keyboard operation and labelling of code tabs; loading button semantics.
- Page overflow at 320, 390, 768, and 1440 px; exact 375, 768, and 1280 px preview widths.
- Unique HTML IDs, existing label targets, and working internal anchor targets.

`python scripts/check_structure.py`: **16 assets verified**. The checker now
handles versioned URLs and catches duplicate IDs, broken internal anchors, and
institution-specific references in the current page/source files.

`git diff --check` and Python script compilation also pass. Stylesheet opening
and closing brace counts were balanced.

These are targeted regression checks, not a full accessibility certification or
an exhaustive security assessment. Firefox, Safari, assistive technologies,
browser download/clipboard permissions, storage quota failures, and every
possible custom palette remain outside the automated coverage. No production
deployment was performed as part of this review.

## Recommended next steps

1. **Gate publishing on validation.** CI currently runs the structure check, but
   the Pages deployment is a separate workflow and does not depend on its
   success. Run required validation in the deployment path before uploading the
   artifact. Add the browser suite to CI with a configured Chrome executable.
2. **Finish the module migration.** The registry exists, but current features
   still wrap shared globals such as `apply`, `renderCode`, and `importConfig`.
   Centralize state changes, import/export contributions, and change events.
   This would make the save-order bugs found here less likely to return.
3. **Expand accessibility checks.** Add an automated accessibility engine and
   manual screen-reader, keyboard, and zoom checks. Include generated pages and
   custom colours, focus indicators, disabled states, and both themes. The
   current contrast readouts cover selected pairs, not every rendered state.
4. **Test additional browsers.** Verify Safari and Firefox, especially container
   units in typography previews, canvas pointer input, clipboard behavior, and
   project storage. Add image comparisons for mobile and desktop layouts if
   visual regressions become frequent.
5. **Reduce repeated work during slider input.** Shared wrappers can render CSS,
   tables, button matrices, and previews multiple times for one change. Profile
   those paths, then batch visual updates per animation frame and debounce
   local storage writes where appropriate.
6. **Clarify project persistence in the interface.** Mark unsaved projects and
   distinguish browser-local saves from downloaded backups. Consider updating
   the saved-project list name when the project title changes and validating
   stored project entries before listing them.
7. **Unify release metadata.** The interface says V4.1 while some internal schema
   and code comments refer to earlier versions. Document the schema separately
   from the app version and use a consistent release identifier for asset
   caching. Keep the legacy build explicitly archival.

The dependency-free runtime and the shared CSS generator are useful strengths:
the live inspector, CSS downloads, and token catalogue already read the same
generator. Preserve that relationship when adding features.
