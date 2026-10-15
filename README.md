# Design System Studio

A dependency-free, browser-based studio for building accessible design systems: brand palettes, OKLCH colour exploration, fluid typography (`clamp()`) calculator, button component designer, state explorer, and exportable CSS / tokens / HTML.

No build step, no framework, no network calls. Everything runs locally and stays in your browser.

## Quick start

```bash
git clone https://github.com/davis-boudreau/webdesignstudio.git
cd webdesignstudio
python -m http.server 8080      # or: npx serve .
```

Open <http://localhost:8080>. Opening `index.html` directly via `file://` also works.

## Project layout

```text
index.html            Markup only (no inline CSS/JS)
src/css/              Stylesheets, loaded in order (tokens -> layout -> features)
src/js/               Classic scripts, loaded in order; studio-registry.js first
docs/                 Architecture, design-system review, roadmap
scripts/              Repository checks
legacy/               Original single-file V4.1 build, kept for reference
```

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how to add a feature module and
[docs/DESIGN_SYSTEM_REVIEW.md](docs/DESIGN_SYSTEM_REVIEW.md) for the analysis and recommendations.

## Development

```bash
python scripts/check_structure.py   # verifies index.html <-> src/ consistency
```

See [CONTRIBUTING.md](CONTRIBUTING.md). Please follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Licence

[MIT](LICENSE). The NSCC brand colours referenced in the studio belong to their owner and are used as a reference example only; Greycliff is a licensed font, so Arial is the bundled fallback.
