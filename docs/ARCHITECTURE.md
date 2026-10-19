# Architecture

## Principles

1. **Zero build, zero runtime dependencies.** Plain HTML, CSS and classic scripts. Contributors need only a browser and a static server.
2. **One source of truth.** Foundation values live in a single state object; CSS preview, export, token catalogue and clamp explorer all derive from it.
3. **Feature modules over a shared core.** The intended extension API is `DSStudio`; existing features still share globals while migration is pending.
4. **Imported data is data.** JSON import is validated and never executed.

## Layers

| Layer | Files | Responsibility |
|---|---|---|
| Markup | `index.html` | Sections, landmarks, asset manifest |
| Tokens & base | `src/css/base-tokens.css`, `layout.css` | `:root` custom properties, themes, page layout |
| Core | `src/js/studio-registry.js`, `core-state.js` | Registry/events, state, CSS and HTML export |
| Features | `css-dock`, `advanced-params`, `journey-library`, `button-design`, `oklch-lab`, `token-catalogue`, `clamp-explorer`, `contrast-audit` | One user-facing capability each |

Load order is the order in `index.html`. Scripts are `defer`red; `DSStudio.start()` runs on `DOMContentLoaded`.

## Adding a feature module

1. Create `src/css/my-feature.css` and `src/js/my-feature.js`.
2. Register the module:

   ```js
   'use strict';
   DSStudio.register({
     id: 'my-feature',
     title: 'My feature',
     init({ studio }) {
       // bind to DOM, subscribe: studio.on('ready', ...)
     },
     exportCss() { return '/* contributed to Export CSS */'; }
   });
   ```
3. Add the `<link>` / `<script defer>` tags to `index.html` and the markup section. The current export generator does not yet call `DSStudio.collectCss()`; exporting a registered module's CSS requires integrating that hook first.
4. Run `python scripts/check_structure.py` and `python scripts/browser_review.py`.

## Known debt (migration path)

Feature scripts still share globals (notably `htmlExport` is wrapped by `button-design.js`). Migrating each to `DSStudio.register` and replacing the monkey-patch with `exportCss()` contributions is the first roadmap item. Converting to native ES modules (`<script type="module">`) is the natural next step once globals are gone; a bundler such as Vite can be added then without changing the module shape.

## Contrast inventory

`contrast-audit.js` uses `palette(theme)` and the button editor's read-only
`dssGetButtonContrastData()` snapshot to evaluate both themes without switching
the active project. Core, advanced and button changes schedule one refresh per
event turn. Text, conditional non-text checks, inactive exemptions and exploratory
swatch candidates remain distinct. Alpha/brightness calculations use unrounded
sRGB channels for ratios; displayed samples use the nearest HEX values.

The report models named solid-colour contexts and state samples. It does not
scan every rendered element, determine whether a boundary is necessary, or
validate focus geometry, announcements or arbitrary background layers. New state
styles need matching report coverage and browser regression checks.

## Future extension points

- Export formats as modules (W3C Design Tokens JSON, Tailwind config, SCSS, Style Dictionary).
- Component editors beyond buttons (inputs, cards, alerts) using the same state/preview/export contract.
- Theme packs (brand palettes as JSON files in `presets/`).
