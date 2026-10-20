# CSS/HTML generation review

Reviewed 19 October 2026. Covers the live inspector, downloaded sample page and
linked responsive preview. The user's `test.html` and `tokens.css` snapshots were
not changed; fresh downloads contain these improvements.

## Spacing and grid approach

An 8-point spacing rhythm and a 12-column grid are compatible design conventions:
spacing sets distances, while the grid sets alignment and proportions. They are
not a requirement of CSS or an accessibility guarantee. IBM's
[2x Grid](https://www.ibm.com/design/language/2x-grid/) describes an 8 px mini unit
for product/web design; [Bootstrap's grid](https://getbootstrap.com/docs/5.3/layout/grid/)
documents a responsive 12-column system. These primary sources were checked during
the review.

The studio keeps its existing default 4 px spacing foundation. Major spacing uses
8, 16, 24, 32, 48, 64 and 80 px; 4 px remains available for fine details such as
badge padding, help text and definition-list labels. Fonts, line heights, borders,
focus outlines, and user-selected button size variants keep their own rules.
Imported custom values are not rounded or migrated.

| Generated layout | Default behavior |
| --- | --- |
| Container | 72rem maximum including gutters; 16 px narrow / 32 px desktop gutters |
| Hero and split sections | 12 tracks, 6 + 6 spans; one column at 48rem and below |
| Card rows | 12 tracks with 4 + 4 + 4 spans; two/one columns as content space narrows |
| Card gutters/padding | 24 px / 24 px |
| Section padding | 32 px narrow, 48 px medium, 64 px desktop |
| Hero padding | 48 px narrow, 80 px desktop |
| Buttons and inputs | 48 px default minimum height; button padding 8 px / 16 px |
| Footer | One 32 px padding layer, removing the former doubled padding and extra gap |

Named container queries calculate card breakpoints from the selected card minimum
width and gap, keeping those controls functional. Text remains fluid and columns
may have fractional pixel widths; neither needs to be forced to multiples of eight.
Custom spacing units and component dimensions intentionally change the default rhythm.

## Generator findings and changes

- Added a reusable spacing token scale and replaced ad hoc layout padding, gaps
  and margins with tokens and discrete responsive steps.
- Consolidated duplicated card/grid declarations. Shared component rules own real
  button states; sample rules supply only the selected-state demonstration.
- Excluded button anchors from ordinary-link colour styling, removing the need
  for repeated button foreground and hover/active overrides.
- Changed input read-only matching to `[readonly]`: `:read-only` also matched
  ordinary selects. Kept disabled and invalid states available.
- Corrected adjacent field-label spacing and trailing content margins.
- Removed temporary writes to the active theme during CSS export.
- Resolved the palette once for each HTML export, rather than once for each image.
  Instrumented Chrome runs measured four palette calls for two HTML exports before
  the change and two afterward. CSS export still reads both palettes.
- Cached up to eight encoded illustration variants using all SVG colour inputs
  and the illustration type as the key. Palette/theme edits still produce new images.
- Retained both code panels' text nodes when export content is unchanged, avoiding
  needless DOM replacement and preserving text selections during those refreshes.

The added spacing/grid rules increase the unminified stylesheet slightly. The
optimization targets consistent layout, simpler styling and repeated live-update
work rather than file compression. No framework or runtime dependency was added.

## Verification

- `python scripts/check_structure.py`: 23 referenced assets verified.
- `python scripts/browser_review.py`: 261/261 checks passed in isolated headless
  Chrome, including the existing 245 checks and 16 new regressions; no captured
  startup/interaction JavaScript errors.
- New checks cover 12-track geometry; 8 px spacing; footer/select styling; link and
  button state colours in both themes; 320/390/600/768/1280/1440 px reflow; large
  custom card gaps/minimums; imported dimensions; read-only export behavior; and
  unchanged inspector text nodes.
- Reviewed screenshots of desktop and 390 px phone headers/hero, desktop services
  and resources, phone contact form, and dark component gallery/footer. Temporary
  screenshot tooling was removed after review.
- `git diff --check`: passed.

Firefox, Safari, interactive pointer/touch behavior, zoom and assistive-technology
review remain manual coverage gaps. Pointer-state CSS regression checks substitute
classes of equal specificity to resolve the cascade; they do not emulate a real
pointer. No full accessibility compliance claim is made.
