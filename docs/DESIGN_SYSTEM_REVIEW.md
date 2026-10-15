# Design System Review & Recommendations

Review of the V4.1 single-file build (3,776 lines, ~163 KB) before modularisation.

## What works well

- **Layered model**: Foundation -> Semantic -> Component tokens, with a live CSS export that stays in sync with the preview.
- **Modern CSS**: fluid type with `clamp()` and container query units (`cqi`) so previews respond to the simulated device, OKLCH colour exploration.
- **Accessibility intent**: contrast-aware defaults (the focus colour was already corrected for 3:1 non-text contrast), labelled state simulations, `aria-labelledby` sections, skip-friendly landmarks, `prefers-reduced-motion` handling.
- **Safe data handling**: imports are validated JSON and never executed; storage failures are tolerated.
- **Pedagogy**: guided journey and progressive disclosure.

## Findings (measured on the split source)

| Area | Observation | Recommendation |
|---|---|---|
| Structure | 7 `<style>` and 8 `<script>` blocks, layered "V2.5 ... V4.1" patches | Done: split into `src/css` and `src/js`. Next: merge overrides into their owning module |
| Globals / patching | `htmlExport` is reassigned by a later script | Replace with `DSStudio` `exportCss()` contributions |
| Hard-coded colour | ~158 raw hex values vs ~75 custom property declarations | Move remaining literals into tokens; keep brand hex only in a brand preset |
| Dark mode | Manual `data-theme` toggle; no `prefers-color-scheme` rule | Default `data-theme` from `matchMedia`, persist user choice |
| `!important` | 7 uses | Remove through layer ordering; adopt `@layer reset, tokens, base, components, utilities` |
| Inline styles | 12 `style=""` attributes | Replace with classes (also enables a strict CSP) |
| `innerHTML` | 14 uses | Audit each for user-controlled data (imported JSON, project names); prefer `textContent`/DOM construction |
| Naming | Mixed prefixes (`bd-`, `demo-`, `ds-`, `studio-`) | Adopt one convention, e.g. `ds-` for exported output, `studio-` for app chrome |
| Token format | Custom state object | Export W3C Design Tokens (DTCG) JSON for Style Dictionary / Figma interop |
| Fonts | Greycliff is licensed and unavailable | Keep system fallback stack; document how to supply a licensed font |
| Quality gates | None | CI structure check (added), then Playwright accessibility smoke tests (axe), Stylelint, ESLint |
| Content | Brand-specific (NSCC) text mixed into the generic tool | Move brand data to `presets/nscc.json` and ship a neutral default |

## Roadmap

1. Migrate feature scripts to `DSStudio.register`; remove `htmlExport` monkey-patch.
2. Cascade layers and token clean-up; `prefers-color-scheme` support.
3. Convert to ES modules; add Vite only if bundling is needed.
4. Preset system (`presets/*.json`) and DTCG / Tailwind / SCSS export modules.
5. Automated a11y and visual regression tests in CI.
6. GitHub Pages deployment (workflow included).
