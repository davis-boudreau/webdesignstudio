# Baseline audit — 19 October 2026

Starting revision: `6163ada` (`improved UX/UI`). This audit establishes a new
baseline on the replacement computer; the earlier project audit remains historical.

## Scope

Read all 13 current JavaScript modules, relevant HTML and stylesheets, both
repository check scripts, architecture/contribution documentation and CI/Pages
workflows. Ran the existing checks before making fixes, then extended browser
coverage around less-tested functionality and confirmed regressions.

The initial structure check verified 21 assets. The initial Chrome run passed
110/112 browser checks with no captured application JavaScript errors. Its two
preview-width failures came from CSS transitions not advancing with the headless
browser's virtual timer. Explicitly finishing the transition in the test confirms
the final widths without changing application animation behaviour.

## Confirmed defects corrected

| Defect | Impact | Fix and evidence |
| --- | --- | --- |
| OKLCH round trips reduced chroma for valid red and green anchors | Applying an unchanged saturated colour could alter it | Allow small matrix round-off at the sRGB boundary, shared by HEX conversion and wheel gamut checks; regression checks for RGB primaries, black, white and the example blue |
| Null or malformed saved-library entries reached sorting/rendering | One damaged entry could interrupt library startup and later initialization in that script | Validate entry metadata and configuration shape before listing; load a fresh frame with mixed corrupt/valid storage and recover the valid project |
| Responsive typography used the content-box width while the device/readout included padding and border | Actual tablet/desktop heading sizes disagreed with displayed values | Compensate for the container inset in preview-only clamp expressions; compare computed heading sizes against the shared formula at 375, 768 and 1280 px |

Only affected runtime asset query versions were refreshed. No feature work or
architecture migration was included.

## Coverage

Final verification: `python scripts/browser_review.py` passed **159/159 checks**
with no captured application JavaScript errors. `python scripts/check_structure.py`
verified **21 assets**, and `git diff --check` passed.

- Foundation palettes and RGB/OKLCH ramps, semantic roles, themes, typography,
  presets, letter spacing, fluid limits and reset/import round trips.
- Page overflow at 320, 390, 768 and 1440 px; fixed device preview dimensions and
  computed typography; accordions, shortcuts, guided steps and code dock toggling.
- Advanced state semantics, button settings, native disabled/busy/read-only/
  invalid attributes, selected toggle semantics and editor persistence.
- Contrast report coverage, filtering, sorting and CSV; repair preview isolation,
  suggestions, Apply/Cancel, semantic overrides and stale-revision protection.
- Local save/load, switching autosave targets, confirmed/cancelled deletion,
  malformed entries and simulated storage quota failure.
- Actual JSON file-input change handlers with valid, malformed and oversized
  files; escaped project text and bounded imported configuration.
- Export handler filenames/content for CSS/JSON/HTML/button CSS, filtered token
  CSV and displayed-code agreement. Generated HTML is rendered in a frame for
  selected computed-style checks. Download routing checks intercept the shared
  download function; they do not verify operating-system download completion.
- Clipboard rejection fallback. Success depends on interactive browser permissions.
- Startup/interaction exceptions and unhandled promise rejections are collected
  from the application. The corrupted-storage fixture checks its own error list.

## Remaining findings and limits

1. CI runs only the structure check. Pages publishing does not depend on CI
   success. Add browser validation to CI and require checks in the deployment path.
2. Global function wrappers remain coupled across modules. The registry exists,
   but export contributors are not yet integrated; migration remains a separate task.
3. The contrast inventory models named contexts; it does not scan every rendered
   element or establish accessibility conformance. Screen readers, actual keyboard
   traversal, zoom, focus visibility/geometry and visual inspection remain manual.
4. This session exercises headless Chrome on Windows. Firefox, Safari, real touch/
   pointer capture, browser download completion and successful clipboard permissions
   remain unverified. No visual screenshot comparison was performed.
5. Corrupt library entries are skipped when reading storage. A later successful
   save persists the valid library; this is recovery of valid entries, not repair
   of arbitrary damaged project data.

Tests use a temporary profile and local server. No normal browser projects were
opened. No production deployment was performed.
