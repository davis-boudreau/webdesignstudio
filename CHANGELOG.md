# Changelog

## [Unreleased]

### Changed
- Aligned the brief wizard with the approved seven-question lesson using one shared definition for order, labels, prompts and saved drafts. Added dedicated Content/Delivery fields while retaining legacy notes and project round trips.
- Reworked Project Brief around seven website-project basics, a fill-in template and a café example; replaced the general GOV.UK source with optional website-planning reading and aligned wizard prompts without changing saved fields.
- Matched Basic header navigation to Advanced: shared semibold text, plain links at rest, hover/pressed underlines and focus rings in both preview and exported CSS.
- Unified Basic and Advanced foundation/component exports so Basic follows the saved system typography, spacing, cards, controls and buttons. Redesigned both footers with shared responsive identity/navigation rows, an expandable sitemap and Back to top.
- Replaced the six-entry starter sitemap with complete Basic/Advanced content inventories, shared by Architecture and both sample footers. Preserved custom plans, upgraded the old starter, added a restore action and expanded the safe entry limit to 64.
- Added a Responsive phase and centre lesson for content-led breakpoints, page width and gutters across both samples; moved grid controls into the phase and kept saved values validated/exported. Simplified Project Brief into a five-question guide with an optional preserved draft.
- Added three titled semantic list examples to Basic and linked its footer sitemap to the Architecture plan, with working links only for built sections and explicit Planned page labels for other entries.
- Added independent Advanced/Basic sample tabs to the Live CSS/HTML Inspector. Basic supplies a compact responsive header/nav/logo, hero, Grid cards, static sign-up and footer/Back to top with its own commented CSS. The selected mode follows preview/code/downloads and is validated/persisted with projects; Advanced stays the default.
- Added explicit separate HTML/CSS website download actions above the responsive preview and in Deliver, with matching code shortcuts. Deliver now downloads `tokens.css` to match the generated HTML's stylesheet link. Both files share the live preview generators.
- Added project brief, information architecture, wireframing and prototyping before palette design: eleven wizard stages, fifteen centre lessons, validated saved planning data, shared live/exported artifacts and a ten-lesson HTML field guide. Updated navigation, token-source routes and learning shortcuts; older projects receive starter planning data.
- Reimagined the generated home page as a Web Design Field Guide: six navigable lesson cards, responsive CSS Grid workshop/recipe, live typography and palette exercises, tutorial resources and practice form, with palette-aware browser/grid illustrations. Preserved themes, wizard-driven components and existing navigation/form IDs.
- Moved the 1–11 section navigation and visibility controls above the responsive preview. The menu stays sticky beneath the measured app header at every breakpoint, with horizontally scrollable links and larger targets.
- Added a full-width divider and extra spacing below the wizard step buttons to separate navigation from the selected step's configuration content.
- Applied the established header-link states to all three resource-table links: plain at rest, underlined on hover, stronger underline while pressed, and the shared keyboard focus ring in generated CSS and the responsive preview.
- Changed the default named type scale to Minor Third (1.2) for startup, new projects and reset; preserved explicit saved/imported ratios and updated the default scale examples.
- Corrected teaching examples found in the follow-up audit: the spacing chart now uses the exported spacing scale, typography ladder line-height follows heading/body settings, and heading specimens/ladder follow the selected weight.
- Made section navigation scroll offsets follow the actual sticky header height so wrapped phone headers do not cover lesson headings.
- Set startup to expand only 1. Responsive page preview in Fluid mode; other centre sections start collapsed. Preview updates continue while it is closed. Refreshed startup and preview lifecycle checks.
- Expanded the configuration wizard to eight steps with dedicated Layout and Accessibility stages. Moved font sources, responsive type limits, readability and advanced settings into the wizard; added centre-pane lessons, exercises and two-way configuration/learning shortcuts. Step navigation no longer implies completed checks.
- Set the sample footer navigation to Home, About, Resources and Contact. All studio disclosures now start collapsed except the Responsive page preview, including the guided button reviews and advanced interaction settings.
- Updated sample header navigation to be plain at rest, underlined on hover, and more strongly underlined while pressed, with the shared button keyboard focus ring in desktop/mobile menus and responsive previews.
- Renamed the centre palette to Brand Colour Palette and clarified swatch actions: choose any UI role, click a full swatch card, and see current assignments plus confirmation. Added Supporting assignments for every swatch, retained focus during updates, and replaced the whole-project reset shortcut with navigation to the Brand Palette editor.
- Updated default button state practices with hover underlines, inset pressed cues, selected checkmarks and progress indicators shared by studio specimens and exported components. Busy text now stays at full opacity; the default button focus colour meets the named light/dark context targets. Added nearby disabled-state explanations and guided state/semantics advice.
- Fixed sample-page secondary actions using the Outline variant: hero, section and contact secondary links now follow the wizard's Secondary settings, including custom base colour.
- Standardized generated-page spacing with an 8 px rhythm and 4 px fine spacing; added responsive 12-column layouts, consistent gutters, and corrected footer/field spacing. New projects use 24 px card gaps and 48 px minimum controls; imported custom dimensions remain intact.
- Simplified generated button/link styles, cached palette illustrations, avoided unchanged code-panel replacements, and made CSS theme generation read-only. Corrected read-only input styling so ordinary selects retain their normal surface.
- Changed the responsive page preview's phone preset from 375 to 390 px, including viewport sizing and readouts; retained 320 px narrow-layout checks and existing typography bounds.
- Removed the studio's 1500 px width cap. Desktop controls/inspector panes now have fixed widths while the centre expands with the viewport; responsive stacking remains at narrower widths.
- Made the sample mobile menu toggle borderless and transparent, with a default text-colour “Menu” label and accent colour limited to its hamburger/close icon.
- Corrected OKLCH gamut-boundary round trips, recovered valid library entries when browser storage contains malformed projects, and aligned responsive preview typography with device-width readouts.
- Expanded browser audit coverage and added repository instructions/progress notes for session handoffs.
- Split the single-file V4.1 build into `index.html`, `src/css/*` and `src/js/*`.
- Added `DSStudio` registry as the module extension point.

### Added
- Configuration-source actions and direct/derived/alias guidance for every catalogue token, including theme/variant-aware routing. Added persisted, validated heading line-height and a teaching/token coverage review.
- Added Semantic colour roles to wizard step 4: all role names/tokens, purpose, swatch, current HEX and override status, with theme-specific contrast previews, edit/apply/cancel and restore-generated actions shared with the centre editor.
- Guided Brand Palette editor and Main Palette role dropdowns: name/edit/add/remove up to 24 project brand colours and choose any brand swatch for Primary, Supporting or Accent UI roles. Preserved custom pickers, separate role assignments, local saves/JSON compatibility, dynamic brand exports/reference displays and safe contrast identities.
- Guided button contrast review for every variant/state in both themes, with selected-state ratios, focus/selection indicators, inactive exemptions and direct colour-repair actions. Results share the full contrast inventory and update live previews, saves and exports; dialog actions return focus to their entry point.
- Optional Google Fonts with separate heading/body families, weight selection, saved settings, generated CDN links/font tokens, live loading/retry status and a preview-only fallback comparison. Added guided learning examples and separate deterministic/live-CDN browser checks; system fonts remain the offline default.
- Contextual primary/secondary action pairs throughout the generated home page, with working section destinations, a contact-form action pair and responsive wrapping tied to button settings.
- Responsive header logo container labelled “Logo”, paired with the project name using the shared heading typography and theme colours in the generated page and live preview.
- Responsive sample header with a native hamburger/close menu at 768 px and below. Embedded SVG icons follow the semantic accent colour in both themes and work in exported HTML and the live preview without JavaScript or remote assets.
- Shared Light/Dark theme selectors in the inspector and responsive preview. The preview now opens first in the centre pane, rendering the generated home page in Fluid or fixed device viewports with local navigation and preserved browsing state.
- Live CSS/HTML Inspector with keyboard-accessible tabs and matching copy/download actions; a responsive static home page with embedded palette illustrations, navigation, hero, service cards, resources, FAQs, forms and component states. Renamed exported fixed reference tokens from `--example-*` to `--brand-*`.
- Named type-scale presets, PX/REM specimen and ladder values, shared heading/body em letter spacing with legacy-project migration, and collapsible centre sections with navigation-aware expansion.
- Contrast repair actions with theme-specific semantic colour editing, separate control borders, non-mutating suggestions, related-pair comparisons, explicit Apply/Cancel, and persisted overrides.
- Filterable contrast inventory covering both themes, button and form states, focus/selection indicators, opacity and swatch candidates, with grouped sorting and CSV export.
- README, LICENSE (MIT), architecture and design-system review docs, CI and Pages workflows, issue/PR templates.

## 4.1.0
- Original single-file release (preserved in `legacy/`).
