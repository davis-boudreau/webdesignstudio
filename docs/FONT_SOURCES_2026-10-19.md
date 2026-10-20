# Optional Google Fonts and learning controls

Implemented 19 October 2026. System fonts remain the offline default. The user
authorized optional CDN fonts after reviewing the proposed font-source, separate
heading/body, export, learning-panel and fallback-comparison features.

## Learner workflow

Open **Typography studio → Fonts and CDN integration** (also linked from the
guided Typography step). Select System fonts or Google Fonts. System mode uses
the existing body-font control and an independent system heading choice. Google
mode offers Inter, Source Sans 3 and Literata for body/headings; headings can also
follow the body choice.

Select additional weights as needed. The page's required 400/600/700 weights,
advanced heading weight and validated button weight remain included. The sample's
italic body cite adds italic 400. A shared heading/body family is requested once.
The regular button importer continues to accept its existing 400/500/600/700 set.

Specimens, button demonstrations and the generated home page use these choices.
Studio labels and controls keep their installed font. The loading status reports
loading, loaded, failure or fallback comparison; Retry reloads the studio and
preview font links. Failed web-font requests leave system fallbacks available.

**Show fallback fonts in previews** omits web fonts from specimen/preview stacks
and removes managed font links. It is a comparison setting, not a project setting:
the saved configuration and exported HTML/CSS keep the chosen web fonts. Import
and reset clear comparison. Requests already in progress may still finish.

The learning disclosure explains the stylesheet/font-file requests, weights,
`preconnect`, `crossorigin`, `display=swap`, fallback stacks and possible reflow.
Its live HTML and CSS examples follow the same sources as the inspector. Downloads
include ordinary HTML links and font tokens and need no JavaScript font loader.
Google font files are externally hosted; downloaded pages use fallbacks offline.

## State and implementation

```json
{
  "font": "Arial, Helvetica, sans-serif",
  "fontSettings": {
    "source": "google",
    "body": "inter",
    "heading": "literata",
    "systemHeading": "same",
    "weights": [400, 600, 700]
  }
}
```

`font-sources.js` defines `DSStudio.fonts` before core state is evaluated, then
registers its UI/loader module. Core import validates font settings before applying
state. The previous installed `font` field remains compatible with older projects;
missing font settings mean system mode. New properties travel through the existing
JSON/local-project serialization. Unknown IDs, sources, system choices and weights
are discarded; imported data cannot specify font URLs, CSS or scripts.

Exports define `--font-body` and `--font-heading`; `--font-ui` aliases the body token.
Heading rules and the sample project title use the heading family. CDN requests
use HTTPS Google CSS2 URLs built from the curated catalogue, sorted styles, selected
weights and `display=swap`. HTML escapes URL ampersands and provides preconnects
to `fonts.googleapis.com` and `fonts.gstatic.com`, with anonymous CORS for font-file
preconnection. No catalogue API key or remote script is required.

Managed links use a URL/document record. Unrelated edits retain link nodes; source
changes clear old links/timeouts and invalidate callbacks. Loading checks actual
font faces; stylesheet/font errors and a 12-second timeout offer Retry. The preview
keeps its own managed links across HTML refreshes, adding fallback CSS only to its
existing style node. The downloaded files are unaffected by comparison.

## Verified primary references

- [Google Fonts CSS2 API](https://developers.google.com/fonts/docs/css2): family
  requests, styles/weights, sorting and `display` parameter.
- [Inter metadata](https://raw.githubusercontent.com/google/fonts/main/ofl/inter/METADATA.pb):
  normal/italic faces, weight range 100–900, SIL Open Font License.
- [Source Sans 3 metadata](https://raw.githubusercontent.com/google/fonts/main/ofl/sourcesans3/METADATA.pb):
  normal/italic faces, weight range 200–900, SIL Open Font License.
- [Literata metadata](https://raw.githubusercontent.com/google/fonts/main/ofl/literata/METADATA.pb):
  normal/italic faces, weight range 200–900, SIL Open Font License.

These references were checked during implementation. No font binaries were added
to the repository; each font's licence is available from the Google Fonts catalogue.

## Verification

- `python scripts/check_structure.py`: 25 referenced assets verified.
- `python scripts/browser_review.py`: 304/304 checks passed, including the previous
  282 checks and 22 font regressions; no captured JavaScript errors. Font loading,
  errors and retry use local CSS/font-face fixtures rather than network availability.
- `python scripts/font_cdn_review.py`: 9/9 checks passed with actual Google CDN
  stylesheets/font downloads, all three curated families, responsive sample and
  standalone export, and fallback comparison; no captured JavaScript errors.
- Reviewed real-font desktop/390 px controls and teaching notes, light/dark sample
  pages and the phone fallback comparison. Captured pages had no horizontal overflow.
- `git diff --check`: passed.

The retry regression explicitly loads the offscreen iframe face: browsers may
defer unused/offscreen font rendering. The regular fixtures verify behavior, while
the live check and screenshots separately verify the actual fonts. Firefox/Safari,
screen-reader behavior and broader manual accessibility review remain coverage gaps.
User-created `test.html` and `tokens.css` snapshots were left untouched.
