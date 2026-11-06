# Generated page HTML/CSS and Tailwind alignment review

5 November 2026, America/Halifax. Scope: current working-tree generators after
Studio appearance separation; Basic and Advanced page exports only.

## Conclusion

The independent page is a good foundation for modern, reusable HTML/CSS. Keep
semantic HTML and a dependency-free standalone export. First improve the shared
CSS cascade and component ownership, then add an optional Tailwind v4 theme
adapter generated from the same project settings. Actual Tailwind utility output
is a separate export target requiring compilation; it is not implemented here.
"Perfect" should mean defined, verified output requirements, not feature count.

## Existing strengths

- Basic has landmarks, one H1, labelled sections, article/aside/list examples,
  native details/summary navigation and FAQ, labelled inputs, fieldset/legend,
  autocomplete and native validation. Advanced retains its semantic field guide.
- Shared foundations, semantic light/dark roles, component/state tokens and the
  same HTML/CSS generators serve preview, inspector and downloaded files.
- Both use Grid/Flexbox, flexible gaps, minmax/min constraints, fluid rem/vw clamp
  typography and logical spacing in many places. Advanced already uses a named
  inline-size container and container queries, aspect-ratio and text-wrap: balance.
  Basic's auto-fit Grid is already appropriate; it need not copy every Advanced feature.
- Focus-visible, disabled/busy/selected cues, reduced-motion and forced-colour
  handling are present. Their presence is not a complete accessibility audit.
- OKLCH ramp calculation happens in JavaScript and produces HEX tokens. This is
  distinct from exporting CSS oklch() values. HEX is not an interoperability flaw.

## Prioritized findings and proposed changes

| Priority | Source evidence | Consequence and proposed direction |
| --- | --- | --- |
| 1 | core-state.js cssExport, advanced-params.js export wrapper, button-design.js buttonCSS and Basic action helper | Multiple .button/.ds-button and .card declarations accumulate; Basic actions carry both button classes. Establish one owner for component geometry, states and focus, with compatibility aliases only where needed. |
| 1 | No @layer declarations in the shared/page generators; Basic emits global h1/h2/h3, p, nav, label, small rules | Integration relies on source order and specificity. Introduce an explicit layer contract and keep page composition separate from reusable components. Scope rules intended only for a sample. This is an integration concern, not a reproduced Tailwind runtime failure. |
| 1 | Existing tokens use --primary, --space-unit, --font-body, --radius-base; no Tailwind adapter | Add an optional v4 theme adapter with --color-* semantic aliases, --spacing, --font-*, --text-*, --radius-* and project breakpoint literals. Use @theme inline for variable references, avoiding a self-reference when a source name already occupies a Tailwind namespace. |
| 2 | basic-homepage.js uses both min-width and max-width at the saved stack value; Advanced mixes wide/narrow directions too | Both sides match at the exact cutoff. Define documented boundary ownership and use coherent mobile-first ranges. Preserve the current boundary behavior or document/test an intentional change. |
| 2 | Ordinary :hover rules in navigation, components and shared state helper | Consider @media (hover: hover) for real hover styling, matching Tailwind's convention. Keep teaching simulation selectors operable independently of device hover capability. |
| 2 | Physical padding-left/right in Advanced main gutter calculations; physical top/left and margin-bottom elsewhere | Expand logical properties for direction-aware layouts, without mechanically changing all width/height declarations. Verify RTL and writing-mode requirements explicitly. |
| 2 | Advanced explicitly sets light/dark color-scheme; shared CSS declares dark but Basic has no explicit light scheme | Make native control theme behavior explicit and shared for both samples. Consider :user-invalid for actual form feedback separately from authored aria-invalid demonstrations. |
| 3 | Full shared exports include all interaction shade ramps and teaching styles | Preserve the full design-system export; consider a separate lean website export only after measuring size and defining which tokens must remain public. |

## Recommended export architecture

1. One validated project model supplies resolved tokens and reusable components.
2. Standalone target continues to produce browser-ready index.html and tokens.css.
3. Optional Tailwind target produces theme source for a consuming project's local
   Tailwind compiler. No CDN or browser compiler is needed in the Studio.
4. Use the common layer order `theme, base, components, utilities`; place page
   composition deliberately (for example within components). Avoid unlayered
   ordinary component rules that outrank layered utilities.
5. Map semantic roles to utilities such as bg-surface, text-content, bg-primary and
   text-on-primary. Keep --text (the existing colour role) distinct from Tailwind
   --text-* font-size tokens. Existing --space-4 and p-4 share the saved unit.
6. Emit literal breakpoint values into Tailwind theme source; CSS var() cannot
   supply media-query conditions. Do not silently adopt Tailwind default cutoffs.
7. Preserve data-theme="dark"; a Tailwind custom dark variant can target the same
   attribute. Semantic utilities can also change via the underlying role values.
8. Treat Tailwind Preflight as a conscious integration choice: its heading, list,
   margin and border resets may alter teaching examples. Do not merge two resets
   without comparing resulting styles. Audit the shared .container name too.

Tailwind alignment means matching tokens, responsive intent and state behavior.
Changing class names alone does not produce a Tailwind implementation. The first
implementation phase should be the shared component/cascade cleanup; the adapter
and any utility-first HTML output follow separately.

## Verification required before claiming the new target works

- Locally validate generated HTML and CSS syntax and retain semantic checks.
- Compare iframe, downloaded stylesheet and any compiled Tailwind fixture for
  the same project values in both modes/themes. Include overridden semantic roles.
- Test utility overrides against component layers and intentional Preflight use.
- Test saved breakpoints immediately below, exactly at and above each boundary;
  exercise container thresholds independently of the viewport.
- Test native menu/FAQ, labels, focus, reflow, long content and text resizing.
  Run keyboard, screen-reader, reduced-motion, forced-colour and cross-browser
  checks, with a documented browser baseline and progressive enhancements.
- Preserve imported-data validation, local project persistence, inspector source
  routes and current exports. The token catalogue currently recognizes literal
  :root/[data-theme="dark"] text blocks; update readers and teaching excerpts
  deliberately when introducing layers or changing generated selectors.
- The official Tailwind v4 compatibility page lists Chrome 111, Safari 16.4 and
  Firefox 128 as its baseline; any newer CSS feature needs its own support check.

## Sources consulted

Official sources checked on 5 November 2026; Tailwind docs displayed v4.3.

- [Theme variables and variable-reference aliases](https://tailwindcss.com/docs/theme)
- [Preflight and layer imports](https://tailwindcss.com/docs/preflight)
- [Responsive design and container queries](https://tailwindcss.com/docs/responsive-design)
- [Attribute-based dark mode](https://tailwindcss.com/docs/dark-mode)
- [Hover and other state variants](https://tailwindcss.com/docs/hover-focus-and-other-states)
- [Compatibility and browser baseline](https://tailwindcss.com/docs/compatibility)
- [Local Tailwind CLI compilation](https://tailwindcss.com/docs/installation/tailwind-cli)
- [CSS cascade layers](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@layer)

## Current-session evidence and limits

This is source analysis and official-documentation comparison. No Tailwind
compiler, HTML validator, browser probe or manual accessibility review was run
for this analysis. The earlier 1724/1724 browser result belongs to the Studio
appearance change and does not establish Tailwind compatibility. No application
runtime, dependencies, exported snapshots, commits or deployment changed.
