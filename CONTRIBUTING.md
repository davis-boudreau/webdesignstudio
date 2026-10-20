# Contributing

Thanks for helping! The project has no build step.

1. Fork and clone, then serve locally: `python -m http.server 8080`.
2. Create a branch: `git checkout -b feat/my-change`.
3. Keep changes focused. New features should be a module (see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)).
4. Run `python scripts/check_structure.py` and manually test in light and dark themes, keyboard-only, and at 320 px width.
5. Open a pull request describing the change and, for UI work, include screenshots.

## Standards

- Accessible by default: WCAG 2.2 AA contrast, visible focus, labelled controls.
- No runtime libraries. Keep system-font mode offline; optional Google Fonts
  requests must use the curated catalogue and Google CSS/font hosts only.
- Never execute imported content; avoid `innerHTML` with untrusted data.
- Use CSS custom properties rather than literal colours.
- Commit messages: imperative mood (`Add OKLCH gamut warning`).

For button state changes, also run `python scripts/button_states_review.py` to
check actual Chrome reduced-motion and forced-colour modes. Keep hover, pressed,
selected, busy and disabled cues understandable without relying on colour alone.
