# Project progress

Updated: 3 November 2026 (America/Halifax).

## Current objective

Analyse the complete studio workflow and actions, and define a consistent process
across wizard stages, centre lessons, preview and code. Runtime changes are not
part of this analysis request.

## Design Workflow and button consistency audit (3 November 2026)

- Reviewed all twelve runtime wizard panes, sixteen centre sections, global/local
  project actions, beginner and inspector controls, colour repair and both sample
  pages. Read actual handlers and DOM reorganisation, not only static markup.
- Added `docs/WORKFLOW_REVIEW_2026-11-03.md` with a canonical twelve-stage process,
  centre mappings, a shared action/feedback contract, section-specific findings
  and an implementation sequence. Added the grouped runtime inventory in
  `docs/WORKFLOW_BUTTON_INVENTORY_2026-11-03.csv`: 379 groups / 1,567 button,
  internal-link and native-disclosure instances. Repeated token, contrast and
  specimen controls are grouped; conditional behaviour was also read in source.
- Isolated Chrome checks confirmed all twelve forward routes and their numeric
  return routes exist. Found naming/numbering ambiguity (Components vs colour
  roles, Layout vs Components, twelve stages vs sixteen centre numbers) and an
  Accessibility primary route to States rather than the contrast/review section.
- Confirmed action defects in the temporary profile: Deliver Show CSS leaves an
  already selected HTML tab active; restoring Basic's sitemap clears Advanced
  link mappings too; readiness ticks/status survive Reset. Clamp's copy action
  silently ignores rejected clipboard access, whereas the central copy action
  reports a fallback. Header/Deliver JSON exports also use different names and
  metadata. These findings are recorded, not fixed by this analysis-only task.
- Recommended one stage registry, twelve matching lesson identities with preview/
  overview/catalogue utilities outside stage numbering, consistent reveal/focus
  behaviour, explicit reset/export scopes and common studio action styling.
  Planning steps should inspect project data or relevant HTML rather than imply
  every planning field generates page CSS. Basic practice remains a shortcut path.
- Current checks: targeted runtime audit completed with no JavaScript errors,
  intercepted downloads and a simulated clipboard failure in isolated temporary
  Chrome profiles outside the sandbox. `python scripts/check_structure.py`
  passed (41 assets); `git diff --check` passed. The full browser suite was not
  rerun for documentation-only work. Earlier 1082/1082 and 38/38 results below
  remain historical. No user projects/storage were opened.
- Removed temporary audit helper/JSON; retained the inventory and ignored
  `.workflow-audit.log`. No runtime assets, existing user edits, sample snapshots,
  commits or deployments were changed by this review. Manual keyboard-only,
  screen-reader, cross-browser and learner trials were not performed.
- Next step: fix confirmed action/scope/progress defects first, then implement the
  shared stage/action definitions and validate the complete forward/return flow.

## Beginner path and connected workspace (3 November 2026)

- Added an opt-in First steps with Basic entry and four short exercises: action
  colour, reusable spacing, narrow layout and export/reopen. They select Basic,
  retain design values and route to existing source controls. Session progress
  is explicitly self-reported and is excluded from saved project data.
- Added sticky Build/Preview/Code/Beginner steps shortcuts, compacted the studio
  introduction, moved the longer three-exercise reference out of the inspector,
  and shortened repeated dock instructions. Code navigation retains the current
  language/study section and reveals the code area, including on narrow screens.
- Added Basic example connections: fixed element/selector/token mappings, actual
  rule text and theme-scoped declarations from the current CSS export, Configure
  source controls, and navigation to the matching rule in complete CSS. Section
  study choices update their related example. Formula tokens retain calc() text.
- Added optional one-shot preview selection. Primary actions and section/profile/
  FAQ/Grid/form/footer examples map to their appropriate study entries. Normal
  actions resume after selection, Escape (including inside the iframe), stopping
  selection or mode changes. An example selector provides a keyboard alternative.
- Added DSStudio.inspector.show() and an inspector refresh event rather than a
  new render wrapper. Reused exported CSS when reading catalogue values, cached
  unchanged study views and preserved normal copy/full-download paths. Updated
  affected asset query versions and documented state/API boundaries.
- Synchronized sticky offsets with measured workspace/header heights and fixed
  queued preview focus stealing focus after a subsequent Code/control jump.
  No teaching controls or UI state enter generated website files.
- Prepared `docs/LEARNER_TRIAL.md`: participant tasks, observation sheet and
  follow-up decision table. No learner sessions, analytics or messages occurred;
  actual participant observation remains outstanding.
- Current checks: `python scripts/check_structure.py` passed (41 assets) and
  `git diff --check` passed. First expanded `python scripts/browser_review.py`
  passed 1070/1080, no JavaScript errors: six former header-only offset assertions
  needed the workspace bar; four new checks required settled colour sampling,
  calc() expectations, normalized JSON comparison and focus investigation.
  Second full run passed 1078/1080 with no errors; remaining narrow-offset and
  queued-focus issues were corrected. Focused new-path harness passed **38/38**.
  Final full rerun passed **1082/1082**, with no JavaScript errors, in ignored
  `.learning-path-review.log`. Final FAQ/footer token mapping corrections were
  then checked by the focused harness: **38/38 passed**, no errors (ignored
  `.learning-path-focused.log`). All required checks passed.
- Increased the growing browser harness to a 90-second virtual budget and
  240-second process timeout, following the prior 120-second timeout during the
  product review. Assertions were retained/expanded; isolated Chrome profiles
  outside the sandbox do not use the user's stored projects.
- Inspected temporary 1440px initial/path/connection screenshots and 320px Code
  navigation. No page overflow or captured startup errors; compacting the entry
  restored some initial code visibility, and starting the first exercise showed
  its control, example and code together. Refreshed controls use studio styling.
  Removed temporary screenshot/diagnostic helpers and artifacts; no visual
  baselines were added.
- Manual keyboard-only, screen-reader, Firefox/Safari and real learner review
  remain unrun. No root sample snapshots, commits or deployments changed.
- Next step: run the prepared trial with learners and record anonymised findings
  before claiming learning effectiveness; complete manual accessibility and
  cross-browser review.

## Product and system analysis (3 November 2026)

- Reviewed the current implementation at `e9c05eb`, including the UI essentials
  showcase and newer sitemap/background controls, rather than assuming previous
  workshop/footer designs were still current. Read README, architecture, scope,
  historical audits, generator/state/inspector, planning/sitemap, token catalogue,
  persistence, layout and CI/deployment paths.
- Added `docs/PRODUCT_REVIEW_2026-11-03.md` with the decision -> preview -> code
  vision, strengths, concrete usability observations, planning/generation limits,
  recommendations and a prioritised next phase. Kept earlier reviews historical.
- Measured and inspected isolated Chrome views at 1440/1280/390 px and a 900 px
  studio height. Basic's code begins around y=947 at desktop startup; its Fluid
  preview is about 562 CSS px wide. At 1280 the inspector precedes the preview;
  at 390 its top is around y=3715 after the wizard. These are navigation/context
  costs, not assertions that controls are unreachable. Removed temporary visual
  helper/screenshots after review.
- Confirmed sitemap edits affect the plan/navigation rather than body sections;
  wireframe/prototype are bounded teaching artifacts. Noted differing Basic map
  filters and stale README references to a twelve-entry map/asymmetric checklist.
- Recommended clarifying the beginner path and scope, improving example-to-rule
  navigation and narrow-screen access, observing learners, then gating publishing
  and simplifying the shared update/generator contract. No runtime edits made.
- Current checks: `python scripts/check_structure.py` passed (39 assets).
  Standard `python scripts/browser_review.py` exceeded its 120-second process
  timeout without a final result. Reran the unchanged assertions/virtual-time
  budget alone with `python .system-analysis-run.py`, a temporary driver allowing
  240 seconds: **1045/1045 passed**, with no JavaScript errors (ignored output:
  `.system-analysis-review.log`). Removed the driver afterward. Final
  `git diff --check` passed. Earlier results below remain historical. Chrome
  used isolated temporary profiles outside the sandbox.
- No learner study, manual keyboard-only, screen-reader, Firefox/Safari review,
  user-storage access, commits or deployments. This is a source/product review
  with layout observations, not a complete accessibility or security audit.
- Next step: use the review to choose the next product iteration; learner
  testing should guide further expansion.

## Sitemap editor and webpage background (3 November 2026)

- Added Architecture controls to create/read/rename entries, choose a parent and
  existing-section destination, reorder siblings/groups, delete a branch, and
  undo the last edit. Retained the raw text editor in a disclosure and the full
  inventory restore action. Selected unmatched entries appear as Planned page
  in the footer, as explicitly requested; no placeholder body sections are added.
- Continued using the bounded two-level pages text; added validated per-sample
  pageLinks and showPlanned fields to planning data. Fixed-ID-only destination
  validation, escaped rendering, 64-entry limits and stale-undo invalidation
  cover imported data and editing edge cases. Rename preserves sibling order.
- Changes feed existing preview, inspector, artifact, project/JSON and export
  generators. Basic's optional planned view retains Home/Footer exclusions;
  Advanced's complete map and existing legacy aliases remain supported.
- Added Palette background picker/hex/reset for the current theme, reusing
  semanticOverrides rather than introducing another stored colour setting.
  Both samples and export use it; light/dark values are independent.
- Added one runtime module, refreshed affected asset versions, updated docs and
  browser regression checks. User root snapshots/scope file remain untouched.
- Initial `python scripts/browser_review.py` passed 1039/1039, including CRUD,
  persistence, preview/inspector, background and unsafe-target coverage. Added
  sibling-order, entry-limit, stale-undo and narrow-editor checks afterward.
  Final suite passed 1045/1045 with no interaction JavaScript errors using an
  isolated temporary Chrome profile outside the sandbox (ignored log:
  `.site-builder-review.log`). Structure check passed (39 assets), Python
  compilation and `git diff --check` passed.
- Visually reviewed light desktop Architecture/Palette and 320px Architecture
  screenshots; controls fit and wrap. Corrected the screenshot helper for
  Chrome's minimum window size by explicitly setting the iframe to 320px.
  Rechecked final Save button styling; removed temporary screenshots/helper. Manual
  keyboard-only, screen-reader and Firefox/Safari checks remain unrun.
- Next step: try the editor with a learner and complete manual accessibility
  and cross-browser review.

## Basic CSS simplification (3 November 2026)

- Consolidated repeated heading, link-target, flexible-child and form-control
  declarations. Removed obsolete form-section FAQ rules, unused demo-link
  styling and redundant sizing already supplied by the global box model/cards.
- Placed the shared page styles before section rules, retaining mobile nav
  precedence and section-labelled study excerpts. Moved sidebar heading styles
  beside that layout; refreshed outdated HTML comments and the Basic JS version.
- Basic's authored page layer fell from 115 to 107 blocks and 286 to 261
  declarations (counts include media-query blocks, exclude shared foundations
  and footer). Shared tokens/components remain to support studio controls and
  matching previews/exports. Advanced and the shared footer are unchanged.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. `python scripts/browser_review.py` passed 1021/1021 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.basic-css-cleanup-review.log`). No new tests added for this cleanup.
- Next step: review the simplified source with a learner. Manual visual, keyboard-only,
  screen-reader and cross-browser checks have not been rerun for this revision.

## Shared classic footer for Basic and Advanced (3 November 2026)

- Left-aligned the Sitemap title while retaining centred column groups and
  vertically stacked, centred sublinks. Moved all Basic footer layout rules into
  the shared CSS generator and consolidated both modes into one HTML template.
- Advanced now uses the same brand/navigation row, visible sitemap and bottom
  copyright/Back to top row. Retained its own navigation, tagline, copyright and
  complete planning map; Basic retains its filtered three-group map. Removed
  Advanced's Explore heading, redundant Sitemap shortcut and closed disclosure.
- Updated affected asset versions, README/architecture notes and browser
  assertions for visible maps, left-aligned titles and centred link groups in
  both modes across widths/themes and edited design-system settings.
- `python scripts/check_structure.py` passed (38 assets); `git diff --check`
  and Python compilation passed. Initial browser run passed 1016/1021: three
  stale Advanced footer selectors and two colour-dialog focus assertions failed.
  Corrected selectors; focus assertions passed on rerun without product changes.
  Final `python scripts/browser_review.py` passed 1021/1021 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.shared-classic-footer-review.log`). One fewer check reflects removing the
  redundant Advanced Sitemap shortcut navigation test.
- Next step: review the shared footer; watch for intermittent dialog-focus test
  failures. Manual visual, keyboard-only, screen-reader
  and cross-browser reviews have not been rerun for this revision.

## Centred links within Basic sitemap groups (3 November 2026)

- Centred each group heading and its vertically stacked child links within the
  existing centred sitemap columns. Basic-only styling; refreshed its JS query
  version and updated architecture notes and existing alignment assertions.
- `python scripts/check_structure.py` passed (38 assets), Python compilation
  and `git diff --check` passed. `python scripts/browser_review.py` passed
  1022/1022 with no interaction JavaScript errors using isolated Chrome outside
  the sandbox (ignored log: `.basic-footer-links-centred-review.log`).
- Next step: review the updated footer. Manual visual,
  accessibility and cross-browser reviews have not been rerun for this revision.

## Centred Basic footer sitemap (3 November 2026)

- Centred the Sitemap heading and constrained its responsive column grid to
  48rem with automatic inline margins. Groups are centred within their tracks;
  sublinks retain left alignment and vertical stacking.
- Scoped changes to Basic, refreshed its JS query version, documented the
  layout and added geometry/style assertions across existing themes and widths.
- `python scripts/check_structure.py` passed (38 assets) and `git diff --check`
  passed. `python scripts/browser_review.py` passed 1022/1022 with no interaction
  JavaScript errors using isolated Chrome outside the sandbox (ignored log:
  `.basic-footer-centred-review.log`). Python compilation also passed.
- Next step: review the centred footer. Manual visual/accessibility and
  cross-browser checks have not been rerun for this revision.

## Basic footer navigation and sitemap columns (3 November 2026)

- Added labelled main footer navigation beside the project brand/tagline,
  reusing Home, Components, Layouts and Forms from the header generator.
  The identity/navigation row stacks at the saved responsive cutoff.
- Sitemap parent groups use responsive Grid columns; each parent's sublinks
  stack vertically and align left. Retained the filtered three-group sitemap,
  stable destinations, copyright and Back to top.
- Scoped layout changes to Basic, refreshed both affected JS asset versions,
  and updated README/architecture descriptions. Root snapshots and the user's
  webd-UI-scope.md remain untouched.
- Updated browser assertions for navigation destinations/position, horizontal
  desktop parent columns and vertical sublinks across themes and screen widths.
  `python scripts/check_structure.py` passed (38 assets); `git diff --check`
  passed. `python scripts/browser_review.py` passed 1022/1022 using an isolated
  temporary Chrome profile outside the sandbox, with no interaction JavaScript
  errors (ignored log: `.basic-footer-columns-review.log`). Python compilation
  and final `git diff --check` passed too.
- Next step: review the revised footer with a learner. Manual visual,
  keyboard-only, screen-reader and cross-browser checks were not rerun for this
  revision; automated geometry checks do not establish full accessibility.

## Basic UI essentials showcase (3 November 2026)

- Implemented the agreed scope (also read the user-owned webd-UI-scope.md,
  left untouched): semantic header/nav/main/section/article/aside/footer,
  two-CTA hero, captioned image, content card, Grid card collection, Flexbox
  profile row, article/sidebar layout, ul/ol/dl, form controls and native FAQ.
  Kept the page compact with component labels and short explanations rather
  than long code recipes. Advanced's page and user root snapshots are unchanged.
- Reused four main sections and stable destinations; labels are now Home,
  Components, Layouts and Forms. Footer remains a single three-group navigation
  with horizontal/wrapping child links and no Home/Footer groups or duplicate
  Explore menu. Default inventory has sixteen entries; footer has fourteen.
- Added a fieldset/legend radio group with two labelled choices and one default,
  retaining native validation, labelled inputs/select/textarea, required demo
  checkbox and role=status feedback. FAQ moved into its component article.
  Existing preview capture/restore preserves radio and FAQ/control state.
- Added current mock-inventory migration alongside older complete inventories
  and expanded aliases, preserving stored planning data and old fixed-ID links.
  Refreshed four affected JS query versions, inspector labels/help and docs.
- Extended browser regression checks for component content, semantic grouping,
  radio defaults/state, responsive layouts, footer depth, and mock-plan migration.
  `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed, `python -m py_compile scripts/browser_review.py` passed.
- Browser review uses an isolated temporary Chrome profile outside the sandbox;
  the normal approval path accepted this session's runs. Initial run passed
  1020/1022 with no JavaScript errors. Corrected old assertions expecting
  aria-label rather than the existing aria-labelledby footer name, prohibiting
  the now-valid Form controls link text, and expecting four H2s instead of the
  hero H1 plus three section H2s. The intermediate rerun passed 1021/1022.
  Final `python scripts/browser_review.py` passed 1022/1022 with no interaction
  JavaScript errors (ignored log: `.basic-ui-essentials-review.log`). Structure
  verification, Python compilation and `git diff --check` also passed again.
- Visually inspected eight generated-page screenshots: light desktop hero,
  Components, Layouts, Forms and footer; dark 390px Components/footer; light
  320px form/footer. No clipping observed; parent/child footer links wrap and
  controls remain readable. Removed temporary screenshots after review.
  Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks remain
  unrun; automated checks do not establish full accessibility.
- Next step: review with a first-course learner and complete the manual checks above.

## Basic footer navigation limited to three groups (3 November 2026)

- Consolidated Basic's footer into one navigation block: Services (Website design,
  Content planning, Responsive websites), Resources (Project checklist, How we
  work, Useful terms) and Contact (Enquiry form, Common questions). Removed
  duplicate Explore navigation and Home/Footer sitemap groups. Kept identity,
  copyright, Back to top and horizontal/wrapping parent/child link layout.
- Added a parentIds rendering allowlist to the shared helper. Basic passes fixed
  Services/Resources/Contact target IDs; aliases still resolve safely, orphaned
  children are not promoted, and planning data/Advanced/header navigation remain
  intact. Refreshed three affected JavaScript query versions and docs.
- Updated browser expectations for the single navigation block, eleven rendered
  links, filtered custom/legacy maps and fallback brand navigation for empty maps.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed, `python -m py_compile scripts/browser_review.py`
  passed. Static source review confirmed exact group/child labels and a single
  footer nav with no Explore/Home/Footer groups; log is ignored
  `.basic-footer-groups-static.log`. These checks do not execute browser output.
- `python scripts/browser_review.py` was attempted, but sandboxed Chrome failed
  to start (GPU/access denied); no browser assertions ran. Earlier automatic
  approval-review usage-limit block has not been bypassed. Manual visual,
  accessibility and cross-browser checks remain unrun for this revision.
- Next step: inspect Basic footer and rerun the browser suite in working Chrome.

## Horizontal Basic footer navigation (3 November 2026)

- Changed Basic's footer Explore list from Grid to a horizontal, wrapping Flexbox
  row with shared spacing. Main links stay keyboard accessible and wrap on narrow
  screens. Refreshed the Basic generator asset query version and extended existing
  footer checks to assert row direction and wrapping.
- Inspected the active test.html snapshot and its companion tokens.css: its
  sample-nav is already horizontal Flexbox, so neither snapshot needed editing.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. `python scripts/browser_review.py` was attempted but sandboxed Chrome
  could not start (GPU process/access denied); no browser assertions ran. The
  earlier automatic approval-review usage-limit block is documented below and
  has not been bypassed. No manual visual/accessibility review was run.
- Next step: review the footer in a working browser and rerun the browser suite.

## Basic mock studio site (3 November 2026)

- Replaced Basic's tutorial/exercise copy and all code blocks with a short mock
  studio site: Home, Services, Resources and Contact. Retained semantic header,
  main, headed sections, articles, related aside, native hamburger/FAQ, two-CTA
  hero, Flexbox services, Grid resources and article/sidebar layout. Source
  comments and the inspector remain useful for beginners. Removed unused
  tutorial-specific styling and the example formatter helper.
- Retained the classic footer with shared main navigation. Expanded its default
  sitemap to thirteen parent/child links: Services and Resources have three
  children each, Contact has Enquiry form and Common questions. Home and Footer
  remain standalone even if a custom plan assigns children. Children remain
  horizontal/wrapping beneath their parent. Added a standaloneIds render option.
- Added stable contact-form ID; kept earlier content/control/FAQ IDs. Added
  current tutorial inventory migration alongside the prior workshop migration,
  preserving stored planning text and legacy destination aliases. Contact's
  real copy replaces technical field labels; static-demo notice and safe native
  validation remain. Preview feedback says no message was sent.
- Updated browser regression expectations for mock content, lack of on-page
  recipes, sitemap depth/grouping, legacy inventories, semantic layout and form
  state. Refreshed affected JS query versions, inspector labels/help and docs.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed; `python -m py_compile scripts/browser_review.py`
  passed. A read-only `python -` static review passed five checks: balanced mock
  HTML/semantic landmarks, unique IDs and static label/ARIA/link references,
  navigation/inventory targets, child counts 0/3/3/2/0, and absence of page
  tutorial recipes. This inspects templates, not executed browser output; log is
  ignored `.basic-mock-static-review.log`. `python scripts/browser_review.py` was attempted
  inside the sandbox but Chrome failed to start (GPU process/access-denied).
  No browser assertions ran for this revision. The previous turn's final
  escalated rerun was not executed: automatic approval review hit the account
  usage limit, not an unsafe-action determination. That check has not been
  bypassed. Current browser/visual/accessibility/cross-browser checks remain
  unverified; historical pass counts below do not establish this revision.
- Previous expanded-sitemap screenshots were inspected in the prior turn before
  its blocked final rerun, and are now obsolete for this copy change. Temporary
  screenshots are removed. No commits, deployments or new runtime dependencies.
- Next step: run `python scripts/browser_review.py` in a working local Chrome
  environment once approval review is available, and inspect light/dark layouts.

## Expanded sitemap and semantic HTML (3 November 2026)

- Expanded Basic's visible footer sitemap from five top-level links to eleven
  parent/child links for the default plan. Parent groups and their nested child
  lists use horizontal wrapping Flexbox rows. The classic Explore navigation,
  copyright and Back to top remain. The Architecture plan's existing filtering
  and layout are unchanged.
- Added a linksOnly sitemap rendering option: includes known children under
  known parents, omits unlinked planned entries and never promotes orphan
  children. Original planning data, aliases, custom/empty plans and Advanced's
  complete map behaviour remain intact. Existing top-level-only option remains.
- Reviewed and clarified the semantic tutorial: headed section for a topic,
  article for independent content, aside for related information, and div for
  layout wrappers. Expanded the existing escaped HTML example to include nav,
  article and aside; used a labelled article beside the labelled sidebar aside.
  Kept Flexbox/Grid independent of semantic element choice and all four main
  sections, stable destinations, native controls and shared design settings.
- Updated old footer-depth assertions and added both-theme child-row geometry
  checks at 320/390/768/1440px, semantic structure checks and mixed valid/unknown
  child filtering coverage. Refreshed three affected runtime query versions and
  updated README/architecture.
- `python scripts/check_structure.py` passed (38 assets), `git diff --check`
  passed. Initial full browser run passed 1019/1020 with no JavaScript errors.
  Its remaining old assertion expected every article under Grid to be a list
  card with an h3; scoped that check to the three list cards, leaving the new
  independent sidebar article correctly headed by h4. Final rerun/visual review
  pending. Desktop/light and 390px dark expanded-footer screenshots and the
  semantic lesson screenshot were inspected, but the final escalated rerun was
  rejected by automatic approval review's account usage limit and did not run.
  That tutorial revision is superseded by the mock-site changes above.
- Next step: see the current mock-site objective and its verification gap.

## Classic Basic footer and common UI patterns (3 November 2026)

- Restored a classic footer using Advanced's shared identity/navigation Grid:
  project identity, an Explore column with Hero/Flexbox/Grid & lists/Forms and
  Sitemap, then copyright and Back to top. Kept Basic's visible top-level
  sitemap and its separate Architecture-plan view filtering. Header, mobile
  menu and footer main links now share one safe authored navigation helper.
- Added live examples to existing Flexbox lesson cards: content card with a
  text link, avatar/text media object with a badge, and native FAQ disclosure.
  Added a main-content/sidebar Grid example below the list cards, stacking in
  source order at the saved cutoff. Kept the four main sections and plan IDs.
- Added optional labelled select/textarea controls to the native-validation
  practice form. New components use semantic roles, spacing and shared control
  styles. FAQ and optional control state survive live preview edits. Added one
  CSS recipe (nine examples total) and one practice task (six total).
- Added regression coverage for matching header/footer links, classic footer
  geometry, UI/sidebar containment across widths/themes, native FAQ/focus and
  preservation of FAQ/select/textarea state. Updated previous code/task counts.
  Refreshed affected runtime query versions, sample help and docs.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **1010/1010** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; ignored log `.basic-classic-components-review.log`.
  Initial full browser run passed 1008/1009 with no
  JavaScript errors; every new footer/component check passed. The existing
  colour-repair focus assertion intermittently fell back to the contrast summary.
  Review also identified that HTML indentation could insert spaces into an empty
  textarea. Protected textarea blocks alongside preformatted code and added an
  empty default-value regression assertion. The final browser rerun passed
  every check, including the existing focus assertion.
- Captured and inspected desktop/light footer/profile/FAQ/sidebar and exact-390px
  dark footer/form plus light sidebar screenshots. Layouts and controls fit;
  sidebar stacks below content. Manual keyboard-only, screen-reader, zoom and
  Firefox/Safari review remain unrun; automated checks do not establish full
  accessibility. Removed the temporary screenshots after inspection; no visual
  baselines added. No commits, deployments, new dependencies or root snapshots.
- Next step: try the beginner component examples and complete manual
  accessibility/cross-browser review.

## Basic sitemap plan groups (3 November 2026)

- Added a render-only filter to the Basic Architecture artifact: hides Forms
  and Footer parent groups, including case/spacing/hyphen variations and legacy
  Sign up/Signup aliases. Other groups retain their related second-level items.
  Child labels are not independently hidden. Empty/fully filtered plans have
  clear messages. All labels continue to be escaped.
- Scoped Flexbox styling to process-map--basic: parent groups flow left to right,
  related children sit below aligned to the same left edge, and groups wrap on
  narrow screens. Advanced's tree remains unchanged. Full editable/saved plans,
  generated page sections and Basic footer links are preserved.
- Updated former full-render count assumptions and added both-theme geometry
  checks at 320/768/1440px, alias/child/data preservation checks and a fully hidden
  plan case. Refreshed the affected JavaScript asset query version and architecture.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **998/998** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; log is ignored `.basic-plan-columns-review.log`.
  First full browser run passed 991/998 with no JavaScript errors:
  six new assertions incorrectly assumed stored default planning data had already
  been rewritten to Basic labels (resolution is intentionally pure). Corrected
  them to check the resolved editor and unchanged stored data. One existing
  contrast-review focus assertion also failed intermittently; the final run
  passed that check and all 998 assertions.
- Inspected desktop/light and exact-390px dark screenshots: three aligned groups
  on desktop, related items beneath each heading, and wrapping on phones. Manual
  keyboard-only, screen-reader and Firefox/Safari checks remain unrun. Earlier
  results below belong to earlier work. Temporary screenshots were removed;
  no visual baselines were added.
- Next step: review the Basic plan layout with a real project and complete
  manual accessibility/cross-browser checks.

## Studio light background shade (3 November 2026)

- Changed the studio body canvas from the shared light background #F3F6FA to
  a dedicated --studio-background token, #E8EDF3, for stronger separation from
  white panels. Dark mode continues to follow the existing --background role.
  Generated website backgrounds, semantic overrides, project data and exports
  retain their existing behaviour. Refreshed the base CSS asset query version.
- Final verification: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **990/990** with no JavaScript errors,
  and `git diff --check` passed. A focused isolated Chrome check passed 3/3:
  exact light canvas, retained dark canvas, and independent custom website
  backgrounds in preview/export. Logs are ignored `.studio-background-review.log`
  and `.studio-background-focused.log`. No new permanent tests were added for
  this small visual change.
- Manual visual, keyboard, screen-reader and cross-browser review were not run
  for this change; previous results below are historical.
- Next step: review the new studio shade visually.

## Basic top-level sitemap links (3 November 2026)

- Added an explicit topLevelLinksOnly rendering option to the shared sitemap
  helper. Basic uses it to render only known linked parent entries from the
  current Architecture plan; nested children and unlinked planned entries are
  omitted, and children are never promoted. Empty and wholly unlinked plans
  retain clear empty states. Imported labels still resolve only to fixed IDs.
- Changed Basic's sitemap to a compact wrapping link row and adjusted its tutorial
  copy. The default sample shows Hero, Flexbox, Grid & lists, Forms and Footer.
  The complete two-level plan, centre Architecture lesson, local/JSON project
  data and Advanced's default full sitemap remain intact. Existing aliases work.
- Updated regression checks for the rendered depth, legacy/custom plans,
  unknown/malicious labels, restoration, JSON round trips and exports. Added
  explicit checks that the shared full Basic map retains eleven entries while
  the footer shows five and that filtering never promotes a known child of an
  unknown parent. Refreshed three affected runtime query versions and docs.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **990/990** with no JavaScript
  errors, and `git diff --check` passed. Chrome used an isolated temporary
  profile outside the sandbox; output is in ignored
  `.basic-sitemap-filter-review.log`.
- Manual visual, keyboard-only, screen-reader and Firefox/Safari checks were not
  run for this change; earlier screenshots/results below belong to earlier work.
- Next step: review the simplified footer in Basic and complete manual
  accessibility/cross-browser checks.

## Basic component tutorial and visible footer sitemap (3 November 2026)

- Replaced workshop/promotional copy with component-specific lessons: Hero and
  header navigation, semantic HTML, Flexbox rows/columns, native responsive menu,
  CSS Grid, ul/ol/dl lists, and form labels/validation. Renamed navigation and
  CTA labels to match the components they reach. Kept the four-section structure,
  stable IDs, shared settings, native menu, illustration and paired section CTAs.
- Added eight escaped HTML/CSS code examples plus concrete practice tasks.
  Protected preformatted examples during HTML indentation, keeping their code
  whitespace and rendering markup as text. Examples preserve source whitespace and
  scroll locally with keyboard focus, keeping code identifiers intact.
  Native form tutorial requests sample data, explains exported GET behaviour and
  uses a practice acknowledgement rather than marketing consent. Preview success
  feedback describes validation; no processing backend or script was added.
- Replaced Basic's three-column promotional footer/Explore menu/dropdown with
  a compact identity/lesson row, one always-visible grouped sitemap and a utility
  row (Start again, Sitemap, Back to top). Uses shared safe sitemap generation;
  Basic-specific markup/style is separate from Advanced's existing presentation.
- Updated Basic's content inventory to tutorial labels, preserving old section
  and lesson labels as safe aliases. Exact previous complete Basic inventories
  resolve to the tutorial inventory without modifying saved planning data;
  custom and empty plans retain their established behaviour.
- Added browser regression coverage for tutorial headings/tasks, exact code
  example text/whitespace, inert escaped markup, visible footer navigation,
  preformatted-code containment, old complete-plan migration and custom aliases.
  Updated former Basic disclosure/footer geometry assertions while retaining
  Advanced native disclosure checks and shared foundation parity checks.
- Refreshed affected runtime asset query versions, inspector help, README and
  architecture. Final required checks: `python scripts/check_structure.py`
  passed (38 assets), `python scripts/browser_review.py` passed **988/988**
  with no JavaScript errors, and `git diff --check` passed. Chrome used isolated
  temporary profiles outside the sandbox. Logs are ignored
  `.basic-tutorial-review.log`, `.basic-tutorial-focus.log` and
  `.basic-tutorial-scroll.log`. First full browser run passed 985/986, including
  all tutorial/footer/compatibility checks, with no JavaScript errors. One
  existing colour-repair focus assertion failed in both full runs. A focused
  diagnostic rerun passed 143/143 with no JavaScript errors. Updated that test
  to await the native dialog close event (with a bounded timeout) before checking
  restored focus and added failure details. The next full run passed 986/986
  with no JavaScript errors. The first code-scrolling refinement run passed
  975/988: unwrapped form code exposed an auto-sized centred introduction wider
  than its narrow Grid track. Constrained the introduction to width:100% within
  its existing reading measure. A focused isolated Chrome check passed 3/3 at
  320/390/1440px, confirming no overflowing elements and working focused local
  code scrolling. Final expanded full run passed all 988 checks.
- Inspected desktop/light header/hero/Flexbox/Grid/footer and exact 320px light
  Grid plus 390px dark hero/form/footer screenshots. Visual review found an old
  decorative caption number wrapping vertically; removed it. Kept practice text
  left aligned. A final narrow screenshot showed natural hyphen breaks still
  split code identifiers, so switched code examples to preserved whitespace with
  keyboard-accessible local horizontal scrolling. Inspected the final 320px
  code-scrolling screenshot and corrected 390px dark caption/form screenshots.
  Added focus/scroll assertions in both themes. Also inspected the corrected
  320px dark form after its width fix. Removed all temporary screenshots after
  review; no visual baselines were added. Manual keyboard-only, screen-reader,
  zoom and Firefox/Safari checks
  remain unrun, so the suite does not establish full accessibility. Earlier results
  below belong to previous work; no commits/deployments or root snapshots changed.
- Next step: walk through the beginner exercises with a learner and complete
  manual accessibility/cross-browser review.

## Basic website structure review (3 November 2026)

- Reviewed the current generated Basic page against the requested structure.
  The existing illustrated hero already has two shared primary/secondary CTAs,
  and the footer already links to its expandable Architecture-driven sitemap.
- Added Basic's native details/summary hamburger with hamburger/close icons,
  visible Menu label and 48px control. Desktop and mobile links come from one
  fixed list. The saved stacking cutoff selects desktop/mobile navigation;
  exported pages need no scripts. The preview preserves menu state on live edits.
- Converted the whole Skills section to Flexbox, including the 5:7 introduction
  and vertically stacked lesson cards. Renamed feature-grid to skill-cards so
  the source reflects the layout being taught. Narrow screens stack both areas.
- Simplified Toolkit to equal-width auto-fit Grid cards using the saved card
  minimum and gap, removing the asymmetric first-card span and nested sizing
  expression. Retained stable IDs, list semantics, all section CTAs, illustration,
  demo form, shared tokens/components, footer structure and exports.
- Updated the inspector guide, section labels, sample help, README and architecture
  to describe Header navigation, Skills Flexbox and Toolkit Grid. Refreshed the
  affected Basic generator query version. Fixed teaching HTML indentation to
  recognise self-closing SVG paths introduced by the hamburger icon.
- Added browser coverage for native menu open/close, visible/hidden navigation,
  focus outline, target sizes and icon states in both themes at 320/390/768/1440px;
  preview navigation and retained open state; actual Flexbox-only Skills styles;
  equal-width Grid cards; standalone footer Sitemap navigation and disclosure.
  Updated prior Grid-based Skills assumptions and hidden-nav target-size checks.
- Final checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **980/980** with no JavaScript errors,
  and `git diff --check` passed. Chrome used an isolated temporary profile outside
  the sandbox; output is in ignored `.basic-structure-review.log`. The initial
  run passed 956/980; corrected obsolete asymmetric Grid/visible-nav test
  assumptions and restored the palette after the new live-menu test. The next
  run passed 975/980, including every Basic check, but existing sticky-header
  assertions measured stale ResizeObserver offsets. A rendering-frame wait
  stalled under headless virtual time, so replaced it with explicit resize-event
  delivery after layout before the existing geometry assertions. No studio
  runtime change was needed. The final rerun passed all 980 checks.
- Captured and inspected temporary desktop/light header/hero/Skills/Grid toolkit
  and exact-390px dark open-menu/footer screenshots. Removed temporary screenshots
  after review; no visual baselines were added. Manual keyboard-only, screen-reader, zoom and
  Firefox/Safari review have not been run; automated checks do not establish full
  accessibility. No commits, deployments, new dependencies or user root sample
  snapshots changed. Earlier results below belong to earlier work.
- Next step: try the Basic learning exercises and complete manual accessibility
  and Firefox/Safari review.

## Basic inspector learning guide (3 November 2026)

- Added a Basic-only Start here disclosure with three concrete exercises:
  edit the downloaded H1, change the live spacing unit, and compare the
  390/768/1280 px preview presets. Explicitly identifies the inspector as
  read-only and distinguishes downloaded edits from the generated live preview.
- Explained spacing custom properties and the progression from normal flow to
  Header Flexbox and Hero Grid, with Toolkit as an optional Grid challenge.
- Added authored SECTION comments to Basic HTML/CSS, indented generated HTML
  (including formerly compact cards, lists, forms and shared footer markup),
  and expanded page/footer CSS declarations onto separate lines. Shared design
  system foundations and the existing section compositions are preserved.
- Added a transient Basic section filter for Page basics, Header, Hero, Skills,
  Toolkit, Form and Footer. CSS excerpts include shared page/responsive rules
  and explain their dependency on complete tokens.css. Page basics includes live
  spacing token definitions so the spacing exercise shows the changed base value.
  Copy copies the visible excerpt; inspector/Deliver downloads always save the complete selected file.
  Advanced hides the learning controls and retains complete code. Async copy
  feedback checks the selected section as well as language/sample mode.
- Kept the selector visible below the scrolling guide. Stacked docks now grow
  with controls and use a bounded code viewport, avoiding clipped controls.
  Refreshed all three affected asset query versions; documented the architecture.
- Final required checks: `python scripts/check_structure.py` passed (38 assets),
  `python scripts/browser_review.py` passed **958/958** with no JavaScript
  errors, and `git diff --check` passed. Output is captured in ignored
  `.basic-learning-review.log`. First sandboxed Chrome attempt could not start;
  isolated-profile reruns outside the sandbox worked. The first full run was
  950/952: corrected a viewport-dependent spacing test assumption and a wrong
  test-only JSON function name. A subsequent 957/958 run exposed one test
  expecting a resolved spacing value instead of the exported calc() expression;
  corrected that assertion. The next 957/958 run passed every new check but
  intermittently failed the existing contrast-review focus assertion, which
  passed in earlier runs. The unchanged final rerun passed it and all 958
  checks; the intermittent focus-check failure remains recorded for follow-up.
- Captured and inspected temporary desktop/light and exact-390px iframe/dark
  screenshots with the guide expanded and Hero/HTML selected. Visual review
  prompted the guide/selector scrolling correction. Removed the temporary
  screenshots after inspecting the corrected layouts; no screenshot baselines.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain
  unrun; automated checks do not establish full accessibility. No runtime
  dependencies, commits, deployments or user root sample snapshots changed.
- Next step: try the exercises with a beginner and complete manual accessibility
  and cross-browser review; monitor the existing intermittent focus assertion.

## Basic section and footer layouts (3 November 2026)

- Replaced repetitive section grids with a framed/captioned two-column hero,
  a 5:7 editorial skills layout beside three stacked lessons, an asymmetric
  toolkit with a two-row checklist beside workflow/terms panels, and a centred
  sign-up introduction/form limited by the saved reading measure.
- Layouts use the existing semantic roles, spacing, card appearance, grid gap,
  card alignment and responsive cutoff. The toolkit also respects the saved
  minimum card width. Retained all four main sections, stable content IDs,
  primary/secondary CTAs, native validation and the offline illustration.
- Redesigned only Basic's footer presentation: logo/project identity, vertical
  shortcuts and a suggested next-step column; a separate bordered expandable
  sitemap; copyright and Back to top below. Mobile stacks the areas and uses
  two-column shortcuts. Shared footer generation/sitemap validation remain;
  Advanced keeps its existing two-column presentation.
- Updated sample help, README, architecture and affected asset query versions.
  Updated former three-column assumptions in browser checks, added section/footer
  geometry coverage in both themes at 320/390/768/1440 px, and assertions that
  form width follows default and edited/imported reading measure. Existing tests
  continue to cover wizard/preview/inspector/export parity and sitemap behaviour.
- Current checks: `python scripts/check_structure.py` passed (38 assets),
  `git diff --check` passed. Initial expanded `python scripts/browser_review.py`
  passed **915/915**, with no JavaScript errors. Visual review then exposed an
  undefined form-width token; corrected it to `--reading-measure`, added explicit
  form-width checks. The next run passed 915/919 with no JavaScript errors; the
  four new assertions accidentally compared the form to small eyebrow text, so
  their `ch` values used different font metrics. A focused isolated Chrome check
  confirmed the correct form token/width. Corrected the selector to compare body
  text. Final full rerun passed **919/919**, with no JavaScript errors, captured
  in ignored `.basic-layout-review.log`. All three required checks passed. Chrome
  used an isolated temporary profile outside the sandbox, with no access to the
  user's saved projects.
- Captured and inspected temporary light desktop hero/skills/toolkit/footer and
  exact-390px dark sign-up/footer screenshots, including refreshed screenshots
  after the form-width correction. Removed temporary screenshot/diagnostic helpers
  and artifacts; no visual baselines were added.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review were not
  run; automated tests do not establish full accessibility. No commits,
  deployments, runtime dependencies or user root sample snapshots changed.
- Next step: try the revised layouts with a real project and complete manual
  accessibility/cross-browser review.

## Basic page engagement and sitemap feedback (3 November 2026)

- Reworked the existing four sections around a beginner website workshop:
  an outcome-led hero, three practical skill cards, a project toolkit and a
  clearly labelled demo sign-up. Retained existing IDs, inventories, native form
  validation, offline illustration and the shared foundation/component generator.
- Added primary/secondary CTA pairs to all four sections, contextual fragment
  destinations and direct links from skill cards to toolkit cards. Shared button
  classes retain wizard variant colours, size, dimensions and mobile width.
  Action rows wrap with the defined spacing tokens; the form status is announced.
- Investigated the reported sitemap button: the existing handler restored custom
  and empty plans in the prior browser suite, but had no visible feedback when
  the map already matched and the footer remained collapsed. Added applied versus
  already-complete confirmation, section/topic counts, expansion of the centre
  map and a review link. Feedback clears after plan/sample changes. The action
  changes the plan, while existing content destinations remain fixed and safe.
- Added browser coverage for every CTA destination, primary/secondary settings
  in both themes, mobile full-width/focus, row spacing/containment, and sitemap
  restoration/repeated clicks/feedback in both modes. Existing tests cover live
  typography, grid, shared foundations, copy/downloads, forms, storage and exports.
- Current checks: `python scripts/check_structure.py` passed (38 assets) and
  `git diff --check` passed. The first `python scripts/browser_review.py` run
  encountered Windows console encoding while printing a CTA arrow in a test
  name. Changed test names to use ASCII destination IDs. Final expanded suite
  passed **899/899**, with no captured JavaScript errors, outside the sandbox
  using an isolated temporary Chrome profile. Output is captured in ignored
  `.basic-engagement-review.log`. All three required checks passed.
- Captured and inspected temporary desktop/light and exact-390px mobile/light
  hero screenshots plus dark mobile toolkit/sign-up screenshots. Visual review
  caught an undefined action-gap token; corrected it and added a computed-gap
  assertion. Removed the temporary screenshot helper and artifacts afterward;
  no visual baselines were added.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari checks were not
  run; automated tests do not establish full accessibility. No commits,
  deployments, runtime dependencies or root sample snapshots changed.
- Next step: try the revised Basic journey with a real project and complete
  manual accessibility/cross-browser checks.

## Responsive preview cleanup (3 November 2026)

- Removed `See the system working together` from the preview's generated lesson
  list and `Download this responsive website` from the preview markup. The live
  viewport now follows the theme/width controls. Other centre lessons remain.
- Removed the card's unused stylesheet, code-shortcut handlers, status-node update
  and sample-description update. Inspector/Deliver downloads still use the same
  generators; generated sample pages and saved project data are unchanged.
- Refreshed affected JavaScript query versions, updated README/architecture notes
  and adjusted browser coverage for fifteen lessons plus the preview, absence of
  the removed sections and retained download behaviour.
- Current checks: `python scripts/check_structure.py` passed (38 assets);
  `git diff --check` passed. The first `python scripts/browser_review.py` attempt
  failed because the sandbox blocked access to Chrome's temporary profile.
  The first full run outside the sandbox passed 866/867 with no JavaScript
  errors; its remaining assertion referenced the removed sample-description node.
  Updated that obsolete assertion; final full rerun passed **867/867**, with no
  JavaScript errors, using the isolated-profile harness. Output is captured in
  ignored `.preview-cleanup-review.log`. All three required checks passed.
- Manual visual, keyboard, screen-reader and cross-browser checks were not run;
  automated checks do not establish full accessibility. Earlier results below
  belong to prior sessions. No commits, deployments or root snapshots changed.
- Next step: review the simplified preview in the UI and complete manual checks.

## Completed in this session

- Reviewed all 13 current JavaScript modules, relevant CSS/HTML, repository
  checks, architecture and publishing workflows.
- Added `AGENTS.md` and this handoff file for progress across sessions/computers.
- Fixed OKLCH conversion unnecessarily reducing valid saturated colours because
  of floating-point error at the sRGB boundary; wheel warnings share the tolerance.
- Validated browser-local library entries so a damaged entry cannot interrupt
  startup or prevent recovery of other valid projects.
- Corrected responsive specimen font sizes to include container padding/border
  when translating content-box `cqi` measurements into device viewport widths.
- Expanded browser checks for OKLCH, preview/readout agreement, exports, library
  operations, malformed storage, actual file-input imports, clipboard failure,
  advanced states and editor round trips. Made CSS transition measurements
  deterministic under Chrome's virtual clock and included failure details.

See `docs/AUDIT_BASELINE_2026-10-19.md` for evidence and remaining coverage gaps.

## Inspector feature completed

- Added CSS/HTML language tabs, keyboard navigation and matching copy/download
  actions to the live inspector, keeping the centre export tabs independent.
- Replaced exported `--example-*` fixed reference colours with `--brand-*`, including
  token catalogue descriptions and CSV exports. Reference values remain fixed.
- Added the registered `sample-homepage` module: a responsive header/navigation,
  hero, about image, services, resource table, FAQs, sample form, footer and broad
  component gallery, all using the shared CSS and selected settings.
- Embedded two palette-coloured SVG illustrations, so exported `index.html` only
  needs its companion `tokens.css`. The static enquiry form has no delivery backend.
- Removed the button module's old HTML append wrapper; the full page now renders
  selected button size, mobile full-width and interaction state itself.
- Reviewed desktop, 390px mobile, dark-theme and HTML-inspector screenshots in
  isolated headless Chrome profiles. No screenshot comparison baseline was added.

## Verification

- `python scripts/check_structure.py`: 30 referenced assets verified.
- `python scripts/browser_review.py`: **544/544 passed** in headless Chrome on
  Windows; no captured startup or interaction JavaScript errors.
- `python scripts/button_states_review.py`: **12/12 passed** (5 reduced-motion,
  7 forced-colour checks), repeated against the Web Design Field Guide sample.
- `python scripts/font_cdn_review.py`: **9/9 passed** using real Google font
  stylesheet/font downloads and standalone exported HTML, repeated for the field guide.
- `git diff --check`: passed.

## Themes and linked responsive preview completed

- Added inspector/preview Page theme selectors sharing the existing saved
  `state.theme`; global toggles, guided controls, import and reset stay synchronized.
- Moved the responsive preview to the first centre-pane position, open by default
  in Fluid mode. Updated displayed section/nav numbering while preserving IDs.
- Added the registered `responsive-preview` module after the sample generator.
  Its iframe renders the actual generated page at Fluid/375/768/1280 px, using
  exported viewport typography and media queries rather than a separate demo.
- Batched preview updates; retained scroll, user-entered form values, choices,
  open FAQs and focus during live changes. Navigation stays in the sample and
  sample submission is intercepted after native validation without sending data.
- Replaced the old cqi preview styling with iframe layout and viewport readouts.
  Exported files and illustration generation continue to use their existing sources.
- Verified real iframe viewport sizes and reflow, theme persistence, preview/export
  agreement, navigation, retained browsing state and safe CSS text insertion.
- Visually reviewed top Fluid preview, dark phone preview and narrow studio UI
  screenshots. User-created `test.html` and `tokens.css` were left untouched.

## Responsive hamburger completed

- Added native `details`/`summary` mobile navigation at 48rem/768 px and below,
  with desktop navigation generated from the same link array.
- Embedded hamburger and close SVG paths use `currentColor` tied to `--accent`,
  with a minimum 44 px control. No CDN or scripts are needed.
- Both the downloaded sample and live preview support opening/closing the menu.
  The preview preserves its open state through accent/theme changes, and menu
  links use the existing in-preview section navigation.
- Added regression checks for both themes at 320/768/1440 px, actual closed/open
  navigation visibility, focusability, live colours and long project names.
- Visually reviewed exported mobile closed/open, dark open and desktop headers.
  User-created `test.html` and `tokens.css` remain untouched; fresh inspector
  downloads include the header changes.

## Header logo and title completed

- Replaced the decorative diamond with a square “Logo” placeholder beside the
  project name. The placeholder is decorative to assistive technology; the
  project name remains the brand link's accessible name.
- Logo dimensions/text scale with viewport width; colours follow primary/on-primary
  roles and corners use the shared radius. The title uses H2 size, heading leading,
  weight and tracking, with wrapping that preserves space for the mobile menu.
- Verified both themes at 320/768/1440 px, contained logo text, long-name wrapping,
  live project-title updates and heading-scale changes. All 237 browser checks pass.
- User-created `test.html` and `tokens.css` remain untouched. Fresh HTML/CSS
  downloads include the updated header.

## Mobile menu style refinement completed

- Removed the toggle border and filled background. The “Menu” label now uses
  `--text`; only the hamburger/close SVG uses `--accent` in both themes.
- Preserved the native disclosure, 44 px target and standard focus outline.
- Updated existing browser checks to verify the label, icon, transparent background
  and absent border at mobile/tablet widths. No new test cases were needed.
- User-created `test.html` and `tokens.css` remain untouched; fresh exports use
  these defaults.

## Full-width studio layout completed

- Removed the 1500 px shell cap and aligned top-bar/workspace gutters.
- Fixed desktop controls at 310 px and the inspector at 380 px using studio-only
  CSS properties; the centre absorbs the remaining width, including ultrawide screens.
- Kept desktop sticky panes. The inspector stacks at 1280 px and below; all panes
  stack at 900 px and below. Generated sample-page layout is unaffected.
- Verified pane widths, complete centre expansion and no horizontal page overflow
  at 1281/1440/1920/2560/3440 px, plus stacking at 1280/900 px and existing mobile
  checks. All 245 browser checks pass; the structure checker verifies 23 assets.
- User-created `test.html` and `tokens.css` remain untouched.

## 390 px preview preset completed

- Changed the preview phone button, CSS dimensions and viewport/typography
  readouts from 375 to 390 px. Updated the existing exact-viewport browser checks.
- Retained 320 px checks for both the studio and generated sample. W3C's reflow
  guidance uses 320 CSS px as the narrow-width reference for vertically scrolling
  content: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html (verified this session).
- Typography's existing 375 px specimen and fluid minimum remain independent of
  the preview preset; existing project typography settings are unchanged.
- User-created `test.html` and `tokens.css` remain untouched.

## CSS/HTML generation and spacing review completed

- Confirmed the 8 px spacing / 12-column grid approach against IBM and Bootstrap
  primary documentation. It is a design convention; 4 px fine spacing remains
  useful, and font/border/focus sizes follow their own requirements.
- Added the exported spacing scale; replaced ad hoc page spacing with token steps.
  Hero/split rows use 6 + 6 spans, cards use 4 + 4 + 4, and narrow layouts collapse.
  Container queries retain the existing card minimum-width and gap controls.
- New projects use 24 px card gaps, 48 px minimum controls/buttons and 8/16 px
  button padding. Imported custom dimensions are preserved without snapping.
- Removed duplicate button overrides, corrected footer and field-label spacing,
  and fixed ordinary selects incorrectly matching read-only input styling.
- Made CSS theme export read-only, halved palette resolutions per HTML export,
  cached embedded illustration encodings, and skipped unchanged code-text updates.
- Added 16 regression checks. Final browser run: 261/261 passed, including both
  themes, grid geometry, actual spacing values, saved dimensions and six widths
  from 320 to 1440 px; no captured JavaScript errors.
- Reviewed desktop/phone headers and content, service/resource layouts, contact
  form and dark components/footer screenshots. Removed the temporary screenshot
  helper. User-created `test.html` and `tokens.css` remain untouched.
- Refreshed affected script cache versions and documented the design choices in
  `docs/GENERATION_REVIEW_2026-10-19.md`. Structure check: 23 assets; diff check passed.

## Section action pairs completed

- Added one filled primary and one outlined secondary action to each main section.
  Hero/about actions stay with their text, and services/resources/components
  actions follow section content with a token-based 24 px default gap.
- Used contextual destinations: services to contact/resources, resources to
  contact/components, and components to contact/home. Header navigation and action
  pairs together reach every main section.
- Paired the contact form's existing sample-submit action with a services link.
  Kept service-card text actions and component state demonstrations separate.
- All pairs share button colours, size and mobile full-width settings. Navigation
  remains usable when the component gallery demonstrates loading/disabled states.
- Added 21 browser checks for action hierarchy, destinations, settings, responsive
  wrapping in both themes, and all 11 actual preview anchor interactions.
  Final suite: 282/282 passed; no captured startup/interaction JavaScript errors.
- Visually reviewed desktop service actions, 390 px about/contact action pairs,
  and dark resource actions. Responsive wrapping and spacing remained consistent.
- Structure check: 23 assets; diff check passed. Updated the sample script cache
  version. User-created `test.html` and `tokens.css` remain untouched.

## Optional font sources and CDN learning completed

- Added the registered `font-sources` module and Typography studio controls for
  System/Google sources, independent heading/body families and additional weights.
  Curated Inter, Source Sans 3 and Literata metadata/API syntax were verified with
  primary Google sources. System fonts remain offline by default.
- Generated HTML now includes CDN/preconnect links in Google mode; CSS exports
  heading/body tokens and a compatible `--font-ui` alias. Specimens, component
  previews and the actual sample page share these selections.
- Validated IDs/weights on import, preserved legacy system-font projects and saved
  font settings through existing JSON/local-project flows. No imported URLs or CSS.
- Added loading/failure/retry feedback, stale-callback protection and preservation
  of managed font nodes through unrelated edits and preview HTML refreshes.
- Added a preview-only fallback toggle that leaves exports/saved settings intact,
  plus teaching examples for links, weights, swap loading, CORS and fallback stacks.
- Added 22 deterministic regressions (304/304 final suite) and the separate optional
  real-CDN check (9/9 passed, all three families plus standalone export). No captured
  JavaScript errors. Existing button-weight import validation remains in place.
- Visually reviewed real-font desktop/phone controls, teaching examples, light/dark
  sample pages and fallback comparison; no horizontal overflow in captured views.
- Updated runtime cache versions, README/contributor/security/architecture notes
  for the authorized optional font network requests. See
  `docs/FONT_SOURCES_2026-10-19.md` for state shape, references and verification.
- Structure check: 25 assets; diff check passed. User-created `test.html` and
  `tokens.css` remain untouched. No commits, pushes or deployments were made.

## Secondary custom-colour preview fix completed

- Reproduced the user's Secondary action/custom base colour issue. The live
  stylesheet was updating, but visible secondary calls to action were using the
  independently edited Outline variant. The targeted pre-fix check failed.
- Mapped all six section action pairs, including hero and contact, to the wizard's
  Primary/Secondary variants. The component gallery still demonstrates Outline.
  Secondary custom colours now appear on the corresponding page actions.
- Added nine regressions for both themes, all section pairs, repeated custom-colour
  edits without palette changes, wizard/preview agreement, primary independence
  and generated exports. Final regular suite: 313/313 passed; no captured errors.
- Re-ran actual Google font integration checks: 9/9 passed. Updated the generated
  sample's asset cache version and current README/architecture/changelog wording.
- Visually confirmed the custom secondary colour on the 390 px light hero and
  1280 px dark hero, with the primary action retaining its independent colour.
- Structure check: 25 assets; diff check passed. User-created `test.html` and
  `tokens.css` remain untouched.

## Guided button contrast review completed

- Added the registered `button-contrast` module to step 5. All five variants have
  seven selectable states and separate Light/Dark outcomes: 70 combinations.
  Per-variant counts and a live summary make required problems easy to find.
- Reused the full inventory's results through `contrast:updated`; removed the
  wizard's separate selected-sample ratio calculation. Selected details show the
  lowest audited text, focus/selection and conditional-boundary ratios. Loading
  opacity is included, and disabled controls are explicitly exempt.
- Added direct actions into the existing colour-repair dialog, including shared
  ring colours and related-effect previews before Apply. Choosing a review state
  synchronizes the variant/state selectors and specimen without changing colours.
  Applied edits use existing preview/export/project-save paths.
- Preserved review nodes and open disclosures during refreshes. Dialog Apply and
  Cancel return focus to their opener when available. No new colour schema or
  automatic changes to the user's palette were introduced.
- Added 23 browser regressions: all combinations agree with the full inventory;
  bad text, loading opacity and focus failures are detected; editing, cancellation,
  saves/imports, exports and responsive-preview CSS stay synchronized. Confirmed
  both theme layouts at 320 px and visually reviewed desktop/390 px phone views.
- Final regular suite: **336/336 passed**, with no captured startup/interaction
  errors. The harness now captures missing resources and caught module errors,
  excluding intentional failed-font fixtures. Increased its virtual-time allowance
  to 30 seconds for the expanded interaction sequence.
- Structure check: **26 assets**; diff check passed. Updated affected asset query
  versions and README/architecture/changelog guidance. User-created `test.html`
  and `tokens.css` remain untouched. No commits, pushes or deployments were made.
- This makes contrast problems reviewable and editable; custom colours can still
  be below target. Conditional boundaries and inactive exemptions are not counted
  as required failures. Browser tests do not establish full accessibility.

## Default button state best practices completed

- Added the registered `button-state-practices` module before core startup. Its
  shared CSS generator supplies studio specimens, State Explorer, component CSS
  downloads and the responsive/generated page with consistent non-colour cues.
- Default hover underlines the label; pressed states add an inset appearance;
  selected toggles show CSS-drawn checkmarks plus existing rings. Off/on export
  examples keep identical labels and reserve identical checkmark space.
- Busy examples show a progress indicator and Processing label at full opacity.
  Removed the matrix-only 0.8 opacity that could make otherwise readable defaults
  fail. Updated contrast calculations and the guided review to match. Kept native
  disabled exemptions and operable busy text checks distinct.
- Adjusted the new-project button focus colour from #B45309 to warm #B86C20, which
  meets the 3:1 target on every named light/dark host in the button inventory.
  Fresh defaults meet all required button text/focus/selection checks across both
  themes. Imported custom colours and palette anchors remain editable/preserved.
- Retained keyboard focus outlines independently of pressed cues. Added a
  forced-colour pressed outline fallback that preserves real keyboard focus.
  Progress stops for platform reduced motion and the saved Reduce demo animations
  setting; its static indicator and text remain visible.
- Added nearby disabled/busy explanations, a step-5 best-practices guide and
  export comments distinguishing CSS states from application behaviour. Static
  examples still need application logic for actions, toggling, workflow status
  announcements and duplicate-submission protection in a real product.
- Added 33 regular regressions and a repeatable media-preference script. Final
  checks: **369/369** regular browser tests and **12/12** actual reduced-motion /
  forced-colour tests passed; no captured runtime errors. Structure: **27 assets**;
  diff check passed. Visual review covered desktop selected variants and 390 px
  dark selected / light loading exported examples, including wrapping and icons.
- Updated affected runtime asset query versions and README/contributor/architecture/
  changelog notes. User-created `test.html` and `tokens.css` remain untouched;
  re-export HTML/CSS to update those manual snapshots. No commits, pushes or
  deployments were made. Broader manual screen-reader / Firefox / Safari coverage
  remains open; these checks do not establish complete accessibility conformance.

## Guided Brand Palette and Main Palette completed

- Added the registered `brand-palette` module and scoped CSS. The six-step builder
  now introduces Brand Palette references before Main Palette role assignment in
  step 2; the introduction explains that sequence.
- Every Primary UI colour, Supporting colour and Accent colour dropdown offers
  the full named Brand Palette with HEX values. Existing custom pickers remain,
  and guided/advanced changes synchronize matching selections or Custom.
- Added optional name/colour editing and add/remove controls for up to 24 brand
  references. A selection copies HEX into a UI role: subsequent reference edits
  or removal preserve existing role colours until the user chooses again. Editor
  nodes and focus remain stable during updates; the last colour cannot be removed.
- Stored the normalized palette in project state, local saves and JSON. Existing
  projects without it receive starter references without overwriting their UI
  colours. New/reset projects retain the existing 11 starter colours/token IDs.
- Core reference swatches, legacy accent choices, exported `--brand-*` tokens,
  token catalogue and contrast candidates now read the same project palette.
  Display-name changes preserve token IDs. Candidate labels include token IDs so
  duplicate or ramp-like names cannot collide with generated-ramp repair targets.
- Import validation bounds palette/name sizes, accepts only safe unique IDs and
  HEX values, and renders untrusted names as text/escaped markup. Added regressions
  for malformed colours/IDs, duplicate names, HTML injection and palette limits.
- Added 21 browser regressions. Final suite: **390/390 passed** with no captured
  runtime errors; structure: **29 assets**; diff check passed. Covered both themes
  at 320 px and visually reviewed desktop and 390 px phone palette/editor views.
  Broader manual keyboard/screen-reader and Firefox/Safari review remains open.
- Updated runtime query versions, README/security/architecture/changelog and this
  handoff. User-created `test.html` and `tokens.css` remain untouched; exports are
  the source for refreshing those snapshots. No commits, pushes or deployments.

## Brand Colour Palette interaction cleanup completed

- Renamed the centre section to **2. Brand Colour Palette**. Inspected the old
  handlers and ran a focused pre-change browser check: Primary/Accent buttons
  updated their roles, but Supporting had no action and cards had no visible
  assignment feedback. The colour blocks were passive divs, so clicking the
  swatch colour itself did nothing.
- Replaced group-dependent actions with one unified grid: choose Primary UI,
  Supporting or Accent, then click any full swatch card. Role selection alone is
  view-only. The colour, label and usage footer all activate the same native button.
- Added Current Main Palette summaries, explicit Set-as action labels, per-card
  role usage, current-role highlighting and live confirmation. Applying a swatch
  updates existing role inputs, guided choices, preview, CSS and active local save.
  Cards update by token ID to retain keyboard focus; usage text also describes the
  button for assistive technology. Names continue to be rendered as plain text.
- Removed the section's misleading Restore example defaults control, which reset
  the whole project. Edit Brand Palette now opens step 2, expands its editor and
  focuses the first name control without changing project data. Global reset is
  unchanged. Palette references and independent Main Palette assignments retain
  their existing copy-and-apply behaviour.
- Moved swatch rendering/assignment into the brand module; core's renderBrand
  delegates to it. Removed artificial primary/accent restrictions from the display,
  clarified reference/ramp/semantic/component guidance, enlarged action text and
  adjusted mobile spacing/focus styling.
- Added 20 regressions. Final regular suite: **410/410 passed**, no captured
  runtime errors. Verified all three role actions, colour-block/footer clicks,
  independent assignments, live feedback, focus, editor navigation and both themes
  at 320 px. Visually reviewed desktop and 390 px dark-phone summaries/cards.
  Structure: **29 assets**; diff check passed. Broader manual screen-reader and
  Firefox/Safari testing remains open.
- Updated affected cache versions, README/architecture/changelog and this handoff.
  User-created `test.html` and `tokens.css` remain untouched. No commits, pushes or
  deployments were made.

## Header navigation state practices completed

- Scoped generated header navigation styles separately from ordinary links:
  plain at rest, underlined on hover, thicker underline while pressed, and the
  shared button focus colour/width with a 3 px outline offset for keyboard focus.
  Desktop and native mobile menus share these rules in both themes. Existing
  footer/body link settings remain independent. No extra scripts are needed in
  the exported page.
- Added 14 regressions covering exported/live-preview defaults with the general
  underline setting enabled/disabled, both themes at 320/1440 px, unchanged hover
  geometry, pressed cues and real DOM focus-visible styling. Pointer pseudo-state
  cascade checks use equal-specificity class substitution in headless Chrome;
  interactive pointer/touch review remains part of the open manual checks.
- Current checks: **424/424 browser checks**, **29 referenced assets**, and
  `git diff --check` passed. Refreshed the sample generator cache version.
  User-created `test.html` and `tokens.css` remain untouched.

## Footer navigation and startup disclosures completed

- Generated footer navigation now reads Home, About, Resources, Contact in that
  order, linking to the corresponding sections in both export and live preview.
- Removed remaining default-open studio disclosures from the guided state guide,
  button review, dynamically built variant reviews and advanced interaction
  settings. Only the Responsive page preview starts expanded. Subsequent user
  toggles and section-navigation shortcuts retain their existing behaviour.
  The sample page's own FAQ is independent of studio accordion defaults.
- Added six checks for all studio disclosure defaults, matching exported/live
  footer links and all four working preview destinations. The button-review test
  explicitly opens its parent disclosure before testing its interactions.
- Current verification: **430/430 browser checks**, no captured runtime errors,
  **29 referenced assets**, and `git diff --check` passed. Bumped changed runtime
  cache versions. User `test.html` and `tokens.css` snapshots remain untouched.

## Guided semantic colour editor

- Added Semantic colour roles beneath the preview theme selector in wizard step
  4 (Components). All 18 existing roles have readable labels, CSS token names,
  purpose text, a colour swatch, current HEX/theme and generated/custom status.
- Reused the contrast-preview/edit dialog and shared reset operation. Apply
  changes only the active preview theme; Cancel preserves project data and
  returns focus. Reset removes only the selected override. Both editor entry
  points refresh through the existing contrast-update path, including palette
  edits, imported/saved projects and project reset. Component-specific button
  overrides remain separate and the role descriptions explain that distinction.
- Added 15 regressions for role availability, light/dark previews, cancellation,
  focus return, overrides, CSS/live page/local saves, editor agreement, JSON
  imports, selected reset and 320 px layout. Initial test failures exposed test
  fixture assumptions: the wizard listens to input events and multiple saved
  projects already exist. Corrected those tests to use the active project and
  the existing wizard event contract.
- Updated README, architecture, changelog and the colour-repair cache version.
  User `test.html` and `tokens.css` snapshots remain untouched.
- Final verification: **445/445 browser checks passed**, no captured runtime
  errors; structure check verified **29 assets** and `git diff --check` passed.
  Interactive screen-reader and cross-browser review remains open below.

## Teaching workspace and complete token configuration

- Audited catalogue declarations against configuration sources. The previous
  wizard left font loading, responsive typography, readability, layout and
  interaction settings scattered across labs and the legacy parameter panel.
  Heading line-height was fixed. See
  `docs/TOKEN_CONFIGURATION_2026-10-20.md` for the family-by-family map.
- Expanded to eight wizard steps, preserving existing steps 1–5 and adding
  Layout and Accessibility before Deliver. Navigation no longer implies that
  earlier decisions/checks are complete. New `studio-learning` module moves
  existing configuration nodes after initialization, preserving IDs, handlers,
  validation and save paths. Hidden compatibility nodes keep older bindings.
- Added a lesson to each of the eleven centre sections: explanation, token
  relationship, practice and wizard shortcut. Each wizard step links back to
  a related lesson. Interactive experiments, specimen comparisons, calculator
  viewport and contrast repairs remain available; no duplicate demo state.
- Added Configure source to every catalogue row, with direct/derived/alias
  guidance. Routes reveal and focus the wizard control, select the correct
  semantic/button theme and button variant, and locate brand colours by stable
  ID. Derived scales update their foundation; no arbitrary CSS override layer.
  Corrected category labels for typography, layout, motion and control tokens.
- Made heading line-height a validated, persisted foundation (1–1.6, default
  1.18). Studio specimens, preview, CSS, JSON and local saves share the value.
  Old projects retain the default. Constant body text and the base-sized type
  step route to base size, since changing only the ratio would not update them.
- The existing 445-check suite passed after the initial reorganization. Added
  catalogue coverage, focused navigation, eight-step flow, line-height, save/
  import, teaching-link and expanded narrow-layout regressions. These exposed
  hidden catalogue labels extending beyond the table scroll area; replaced
  them with accessible button labels. A focused Chrome check then fit at 320 px.
- Updated README, architecture, changelog and affected cache versions. The user
  snapshots `test.html` and `tokens.css` remain untouched.
- Final checks: **474/474 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and `git diff --check` passed. The 29 new
  regressions cover all token mappings, representative focus routes, persisted
  line-height, expanded light/dark wizard steps at 320 px and lesson navigation.
  Also removed native range-input side margins that caused 2 px of overflow in
  expanded typography. Visually reviewed the desktop teaching layout and 390 px
  typography wizard in isolated Chrome screenshots. No screenshot baseline was
  added; interactive assistive-technology and cross-browser checks remain open.

## Follow-up audit and Colour systems startup

- Repeated the source/workflow and functional review after the teaching/wizard
  changes. Detailed scope, fixes and remaining limitations are recorded in
  `docs/AUDIT_2026-10-20.md`.
- Only **3. Colour systems** now starts expanded. Other centre sections and
  wizard disclosures start collapsed. Fluid preview updates while hidden, and
  reopening preserves its document, selected settings and measured viewport.
  Direct URL fragments and user disclosure toggles retain existing navigation.
- Fixed mismatched teaching specimens: one `SPACING_STEPS` definition now feeds
  exported CSS and the spacing chart (removing non-exported space-3 and showing
  all exported steps); type ladder line-height follows heading/body settings;
  heading specimens and ladder follow the configured heading weight. Body rows
  retain weight 400. Refreshed core-state's cache version.
- Desktop and dark-phone visual review exposed fixed scroll margins hiding
  mobile lesson headings below the wrapped header. Section offsets now follow
  measured header/navigation heights via resize observation. Added visible-heading
  checks at 320, 390 and 1440 px and refreshed layout/accordion cache versions.
- Accessibility and real-font fixtures now reveal the preview they exercise
  rather than depending on the startup disclosure. Main suite coverage adds
  collapsed-preview lifecycle, chart/export agreement, typography synchronization,
  spacing updates and section navigation. User snapshots remain untouched.
- Final audit verification: **484/484 main**, **12/12 accessibility-mode** and
  **9/9 live-font checks passed**, no captured runtime errors; structure verified
  **30 assets** and diff check passed. No commits or deployments were performed.

## Responsive preview startup restored

Latest startup preference supersedes the Colour systems default recorded in the
follow-up audit: only Responsive page preview now starts expanded in Fluid mode.
Updated startup assertions and retained collapsed-preview lifecycle checks by
explicitly closing it within that test fixture. README/architecture reflect the
current default; the preceding audit remains a historical record.
The navigation geometry fixture now disables smooth scrolling and browser scroll
anchoring during viewport measurements, avoiding interference from the preceding
animated lesson jump. Application scrolling behaviour is unchanged.
Verification for this preference change: **484/484 browser checks passed**, no
captured runtime errors; structure verified **30 assets** and diff check passed.
The optional media/font results above are from the preceding audit, not rerun for
this HTML startup-default change.

## Minor Third default

- Changed the foundation ratio from 1.25 to 1.2; the existing preset matching
  selects Minor Third in both wizard and calculator. Updated CSS/HTML fallback
  values, explanatory default examples and affected asset query versions.
- Startup, New project, Reset and imports without a ratio use Minor Third.
  Explicit saved ratios, including Major Third 1.25, remain unchanged.
- Added five regressions for initial synchronization/export, reset, new projects,
  old explicit ratios and missing-ratio imports. Updated default ladder checks
  to expect 19.2 px / 1.2 rem above the 16 px base. User snapshots were not edited.
- Verification: **489/489 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and `git diff --check` passed. Optional media
  and live-font checks remain the preceding audit's results, not rerun here.

## Resource-table link states

- Extended the existing generated header-link selectors to include the resource
  table. All three Explore links are plain by default, underline on hover, use a
  stronger underline while pressed and share the button keyboard focus ring.
  Generated exports and the responsive page preview consume the same CSS.
- Added 14 regressions for all three links, both general underline settings,
  light/dark themes and 320/1440 px widths: default decoration, unchanged hover
  geometry, pressed cue and real focus-visible outline. Pointer-state cascade
  checks use equal-specificity class substitution, as in the existing nav tests.
- Refreshed the sample generator asset version and documentation. Resource hrefs
  retain their existing section destinations; user snapshots were not edited.
- Verification: **503/503 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Optional media/font
  checks remain the preceding audit's results, not rerun for these link styles.

## Wizard navigation/content division

- Added a 2 px theme-aware divider below the eight step buttons, with 16 px
  padding above the divider and 24 px separation before the selected step content.
  It applies across all wizard steps and uses the existing border token.
- Refreshed the wizard stylesheet cache version. No new tests were added for this
  presentation-only change; the existing browser suite is used for regressions.
- Verification: **503/503 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Visually reviewed the
  divider on a light desktop and a dark 390 px phone layout in isolated Chrome.
  Optional media/font checks were not repeated for this spacing/divider change.

## Persistent section menu above the preview

- Moved the existing 1–11 menu and Expand/Collapse controls to the start of the
  centre pane, before Responsive page preview. The preview remains the first
  learning section and the only expanded disclosure on startup.
- Kept the menu sticky at every breakpoint, including phones, and positioned it
  using the measured app-header height. The same measurement includes the menu
  when calculating section scroll offsets so destination headings stay visible.
  Horizontal overflow remains inside the menu; link targets are at least 44 px
  tall and retain native keyboard/fragment navigation.
- Extended checks for startup order, sticky/header geometry, heading visibility,
  horizontal overflow and reaching the last menu item with keyboard focus across
  320, 390, 768, 1280, 1440 and 2560 px. Refreshed affected asset cache versions.
- Verification: **518/518 browser checks passed**, no captured runtime errors;
  structure verified **30 assets** and diff check passed. Visually reviewed the
  desktop preview and a scrolled dark-phone lesson with the menu pinned below
  the header. Optional media/font checks remain the earlier audit results.

## Web Design Field Guide sample

- Replaced the generic service-site content with a coherent web design tutorial:
  welcoming hero, semantic-structure introduction, six lesson cards, Grid and
  type/colour workshops, field notes, review checklist, practice question form
  and interface/state lab. Header now labels the existing services anchor Lessons;
  footer stays Home/About/Resources/Contact. Stable IDs preserve preview behaviour.
- Drew self-contained palette-aware SVG browser and grid illustrations. Kept the
  bounded illustration cache, adding border colour to its key. No new assets or
  runtime network dependencies; existing optional Google Fonts behaviour remains.
- Added a twelve-track grid exercise (8/4 and 4/4/4 spans), a matching native
  CSS-recipe disclosure and tablet-stacked example/notes composition. The demo
  becomes one column at 48rem and consumes the saved grid-gap token. Six lesson
  cards retain the existing minimum-width/container-query grid controls.
- Added live base/ratio/leading readouts and semantic palette swatches/HEX values.
  Lessons link to real page examples. All eight main sections retain wizard-driven
  Primary/Secondary action pairs; the form remains an explicitly static practice.
- Updated browser expectations for eight sections, added tutorial content, grid
  bounds/spans at eight widths, live readout/gap and lesson-destination coverage.
  Existing layout, theme, footer, state, form preservation and resource-link tests
  remain. Updated generator cache version, README, architecture and changelog.
  User snapshots `test.html` and `tokens.css` remain untouched.

- Final verification: **544/544 browser**, **12/12 accessibility-mode** and
  **9/9 real-font checks passed**, with no captured runtime errors. Structure
  verified **30 assets** and diff check passed. Visually reviewed the exported
  desktop hero, six-card lesson board and grid workshop, plus the dark 390 px
  stacked grid. The CSS recipe includes all demonstrated spans and the narrow
  media rule. No screenshot comparison baseline or deployment was added.

## OKLCH role reset and Flexbox lesson (21 October 2026)

- Added "Reset selected role to default" beside the OKLCH Apply/Load controls.
  It restores only the selected Primary/Supporting/Accent starter anchor, reloads
  the wheel and uses the same control, preview, export and save path as Apply.
  Load continues to discard an unapplied experiment; nearby help explains both.
  Brand reference edits and other role assignments are preserved.
- Expanded the existing layout workshop with Flexbox topic wrapping, fixed-marker /
  flexible-text rows, main/cross-axis explanations and column card interiors.
  A comparison table explains normal flow, Grid and Flexbox, including nesting.
  The displayed Flexbox recipe and generated CSS share one source. Lesson 02,
  the practice-form topic and HTML description now include Flexbox.
- Kept existing section IDs and eight main sections. Existing previews and HTML/CSS
  downloads receive the lesson automatically. Refreshed both changed JS asset
  versions; user snapshots `test.html` and `tokens.css` were not edited.
- Added 18 browser checks for all three role resets, repeat resets, state/control /
  preview/export/save agreement, shared recipe/gap and Flexbox geometry at
  320/390/768/1280/1440 px in both themes.
- Commands run: `python scripts/check_structure.py` (**30 assets verified**),
  `python scripts/browser_review.py` (**562/562 passed**, no captured errors),
  and `git diff --check` (passed). Chrome initially could not create a temporary
  profile in the sandbox; the suite succeeded with elevated execution using its
  isolated profile. Intermediate runs caught test-file encoding changes, corrected
  before the final pass. No product failures remained.
- Ran temporary Python/local-server/headless-Chrome screenshot helpers and inspected
  the light desktop and exact 390 px dark Flexbox lesson. The attempted colour-panel
  screenshots did not reach the expanded panel; visual review of the reset control
  remains a manual gap. Automated studio checks still pass at 320 px.
- Optional real-font and accessibility-mode suites were not rerun; their preceding
  results are historical. Manual keyboard/screen-reader, Firefox/Safari and real
  pointer/touch checks remain open. No commits, pushes or deployments were made.
- Next step: manually review the reset controls in the expanded Colour lesson,
  then continue the broader verification/CI work listed below.

## Project planning before palette (21 October 2026)

- Expanded the wizard to eleven stages: Project Brief, Information Architecture,
  Wireframing, Prototyping, Palette, Typography, Components, Buttons, Layout,
  Accessibility and Deliver. Added four corresponding centre lessons after the
  responsive-preview hub and before palette; the menu now has fifteen lessons.
  Kept the preview as the only initially expanded centre section and preserved
  existing control/section IDs. Updated all numeric wizard routes and shortcuts.
- Added the registered `design-process` module and studio stylesheet. Planning
  records audience, main task, scope, success signal, constraints, a two-level
  content map, split/stack wireframe arrangement, hierarchy notes, prototype task
  and observations. The brief/map feed the wireframe and linked Discover, Choose
  and Review screens. Native fragment navigation works in the studio, sandboxed
  preview and static exported page; the prototype has no application backend.
- Planning uses shared state, Apply/render/autosave and existing JSON/local-project
  flows. Imported values are type/length/enum validated; architecture is limited
  to twelve entries, two levels and 64-character labels. Empty drafts stay empty.
  Plan text is escaped. Older projects receive fresh starter planning data without
  changing their explicit palette. UI edits do not mutate defaults. Reuse unchanged
  artifact nodes to preserve focus through unrelated design changes.
- Updated the generated field guide with a Process destination, shared planning
  artifacts, ten ordered lesson cards, related form topics and workflow guidance.
  Nine main sections retain Primary/Secondary action pairs. The sample remains a
  teaching field guide; planning data does not generate a finished custom website.
  Updated delivery guidance and the eight-item self-assessment, source routing,
  runtime cache versions, README, architecture and changelog. User snapshots
  `test.html` and `tokens.css` were not edited.
- Added planning regressions for stage order and reciprocal navigation, local
  autosave/project switching, JSON and actual file-input imports, legacy/malformed
  data, length bounds, safe rendering, default/reset independence, prototype
  links/focus, shared inspector/export/preview content and both themes at
  320/390/768/1440 px. Existing layout/state/library/font-fixture checks remain.
- Final commands: `python scripts/check_structure.py` (**32 assets verified**),
  `python scripts/browser_review.py` (**615/615 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Browser runs used elevated execution
  for isolated temporary Chrome profiles. Increased the virtual-time budget to
  45 seconds and process timeout to 90 seconds for the longer interaction suite.
- Intermediate checks exposed harness issues rather than remaining product
  failures: stale section/action counts, a 1440 px test iframe affecting narrow
  studio measurements, and file I/O outlasting a fixed virtual wait. Updated
  expectations, resized the test iframe and waited for file-input cleanup.
  Focused temporary-harness checks also passed **2/2** for direct 390 px startup.
- Ran temporary local-server/headless-Chrome screenshot helpers. Visually reviewed
  the desktop brief/editor, light desktop wireframe/prototype/lesson board and
  exact 390 px dark exported wireframe/prototype. The attempted mobile studio
  screenshot captured before initialization; it is not visual-review evidence.
  Automated direct-mobile initialization and narrow planning-editor checks pass.
- Optional real-font and accessibility-mode suites were not rerun; previous
  results above remain historical. Manual keyboard, screen-reader, zoom, complete
  mobile-studio visual review and Firefox/Safari checks remain open. No commits,
  pushes, deployments, runtime dependencies or new network requests were added.
- Next step: walk through the planning flow with a real project/audience, review
  the mobile studio and keyboard/screen-reader experience, then continue CI work.

## Explicit standalone website downloads (21 October 2026)

- Added a clear download card above the responsive page viewport with separate
  HTML (`index.html`) and complete CSS (`tokens.css`) actions, plus View HTML/CSS
  shortcuts into the existing live code panel. Added the HTML action to Deliver
  and moved its CSS action to the shared handler, correcting the old stylesheet
  filename mismatch. Both files can now be saved together without renaming.
- Added the registered `website-export` module and studio-only stylesheet. All
  downloads evaluate the existing generators at click time; the sample, preview,
  inspector and files remain one source of truth. Export/view actions do not
  alter saved project data. Feedback says a download was requested rather than
  claiming the browser saved a file successfully.
- Explained the included header/mobile menu, hero, images, cards, Grid/Flexbox,
  forms, table, FAQs, component states and footer. Included same-folder/open-file
  instructions and existing static-form / optional-font behaviour. Updated
  README, architecture, changelog, delivery guidance and the affected asset query
  version. No generated snapshot overwrites: `test.html` and `tokens.css` remain
  user-owned files.
- Added 20 browser checks, including every explicit action's filename/MIME/exact
  contents, code selection/reveal/focus and unchanged settings. Loaded captured
  HTML using a separate Blob stylesheet, with no injected style or script nodes,
  and verified components, 320/768/1440 px reflow and native mobile-menu/FAQ/form
  validation behaviour in both themes.
- Commands run: `python scripts/check_structure.py` (**34 assets verified**),
  `python scripts/browser_review.py` (**635/635 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Chrome used elevated execution for
  its isolated temporary profile. No browser-suite failures in this session.
- Temporary local-server/headless-Chrome screenshots were captured and inspected
  for the light desktop and exact 390 px dark download card. Applied the existing
  ghost-button class after visual review for consistent studio controls; that
  presentation-only adjustment was checked structurally, without rerunning the
  already passing full suite.
- Actual browser download/save-dialog permissions and manual keyboard/screen-reader,
  zoom and cross-browser checks remain open. Previous optional font/media results
  are historical and were not repeated. No new runtime dependencies, network
  requests, commits, pushes or deployments were introduced.
- Next step: use both download buttons in an interactive browser, save the pair
  into one folder and confirm the local file workflow on the target computer.

## Basic / Advanced Inspector samples (21 October 2026)

- Added independent Advanced/Basic tabs above the existing CSS/HTML tabs, with
  Arrow/Home/End navigation, one tab stop per group and labelled nested panels.
  Advanced remains the startup/reset/legacy-project default and retains its exact
  generated HTML/CSS. The Basic sample is intentionally smaller and uses its own
  complete stylesheet instead of shipping unused Advanced gallery/workshop CSS.
- Added the registered `basic-homepage` module after the Advanced generator and
  before the responsive preview, plus studio-only mode-control CSS. Basic includes
  logo/wrapping navigation, hero, three generated Grid cards, a labelled static
  sign-up form with required name/email/consent and a footer with navigation and
  a real Back to top destination. It includes a skip link and visible focus styles.
  Exported HTML has no scripts, inline styles or runtime libraries.
- Basic HTML/CSS share current project name/theme, font settings, type scale,
  leading/tracking/heading weight, semantic colours, radius, grid gap/card minimum
  and focus width. Advanced state demonstrations/planning artifacts stay in the
  Advanced sample. Imports escape project text and validate the saved `sampleMode`
  enum; missing/invalid modes use Advanced. Selection travels through JSON/local
  saves and all existing code, copy, preview and download paths.
- Preview refreshes preserve form state within a mode and start fresh when switching
  samples, preventing unrelated input/focus/scroll state from crossing modes.
  Basic preview submissions use native validation and display static-demo feedback
  without navigation or an account backend. The exported static form returns to
  the page using native GET behaviour; help instructs using sample details.
- Updated Inspector notes and download-card descriptions, README, architecture,
  changelog and affected runtime cache versions. Asynchronous clipboard feedback
  now verifies both selected mode and language before reporting success/failure.
  User snapshots `test.html` and `tokens.css` remain untouched.
- Added 40 browser checks for mode defaults/keyboard controls, exact Advanced
  preservation, Basic semantic structure and safe rendering, persistence/imports,
  selected code/copy/download agreement, live settings, form validation and
  preservation, clean mode transitions and external-stylesheet rendering. Checked
  Basic reflow at 320/390/768/1440 px in both themes, real native Back to top links,
  visible skip links and focus outlines.
- Commands run: `python scripts/check_structure.py` (**36 assets verified**),
  `python scripts/browser_review.py` (**675/675 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). Chrome used elevated execution with
  isolated temporary profiles. The suite passed on its first run for this change.
- Ran temporary local-server/headless-Chrome screenshot helpers and inspected the
  light desktop Basic page, exact 390 px dark header/hero/Grid/form/footer and the
  desktop Inspector with Basic/HTML selected. No visual baseline was added.
- Actual browser download/save-dialog behaviour, manual keyboard/screen-reader/zoom
  reviews and Firefox/Safari remain open. Previous optional real-font and media
  suite results are historical; those suites were not rerun. No dependencies,
  new network requests, commits, pushes or deployments were introduced.
- Next step: try the Basic file pair and keyboard journey in an interactive browser,
  then continue the manual accessibility and CI work below.

## Responsive phase, brief training and Basic lists/sitemap (21 October 2026)

- Added phase 10, Responsive, between Layout and Accessibility: twelve wizard
  phases and sixteen centre lessons. Moved grid minimum/gap/alignment controls
  into this phase, updated token/lesson routes and retained stable section IDs.
  Added five validated project settings for narrow cutoff, wide spacing start,
  page maximum and standard/wide gutters, with 768/1024/1152/16/32 defaults.
- Both samples, exported styles, Advanced Grid recipe and planning wireframes
  consume these shared decisions. Three page tokens route to Responsive and are
  classified as Layout. Breakpoints export as literal rem media-query lengths;
  variable-based container lengths remain separate. Preview presets, fluid type
  bounds, studio pane widths and component-specific button settings stay separate.
- New lesson explains content-led breakpoints, containers, wrapping, flexible
  images and boundary checks, with a current recipe and real iframe matchMedia
  readout. Ordered/bounded imports and 1px slider increments preserve exact valid
  lengths. UI changes use existing Apply/render/autosave and JSON/local flows.
- Replaced the prefilled Project Brief lesson with five plain-language questions
  and a fill-in sentence. New brief fields start empty with prompts. Imported
  answers remain available in an optional Your draft brief disclosure. Guidance
  follows web.dev media-query and GOV.UK user-needs primary sources, linked from
  the lessons and README.
- Basic now has four main sections: hero, features, lists and static sign-up.
  The lists section demonstrates titled ul/ol/dl examples side by side when space
  permits and stacks at narrow widths. Header/footer navigation includes Lists.
- Clarified that Architecture's Pages and content groups is the sitemap plan.
  Its existing two-level parser now also supplies Basic's footer sitemap. Known
  built-section labels become actual fragment links; other entries are escaped
  text with Planned page markers. Empty plans show an explicit empty state while
  ordinary footer navigation continues to reach every built section. Architecture
  edits update the centre map, footer, Inspector and downloaded HTML together.
- Preserved preview disclosure state by stable IDs/summary keys rather than array
  position, preventing the first added brief draft from transferring a FAQ's open
  state to a different disclosure. Added a regression for draft insertion.
- Commands run: `python scripts/check_structure.py` (**38 assets verified**),
  `python scripts/browser_review.py` (**736/736 passed**, no captured JavaScript
  errors), and `git diff --check` (passed). A focused temporary browser harness
  passed **1/1** after the final page-token classification refinement. Chrome used
  elevated execution with isolated temporary profiles. Increased suite allowances
  to 60 seconds virtual time / 120 seconds process time for the longer sequence.
- Current browser coverage includes both themes/modes immediately below/at/above
  custom cutoffs, gutters/page width, exact import values, malformed data, save /
  round trips / reset, brief instructions and preserved drafts, list semantics,
  responsive geometry, sitemap live edits/empty state/safe text and valid links.
  The first expanded run was 733/734: its security assertion expected a literal
  greater-than character that the documented hierarchy delimiter consumes. Corrected
  the assertion while retaining DOM-injection and destination safety checks.
- Ran temporary local-server/headless-Chrome screenshot helpers; inspected the
  desktop Responsive editor/lesson, simple brief guide, desktop list cards and
  exact 390 px dark footer sitemap. No visual-comparison baseline was added.
- Intermediate work was committed by the user as `62924b5` while this task was in
  progress. The final checks above validate the completed work, including later
  local changes. No commits, pushes or deployments were made by this assistant.
  User snapshots `test.html` and `tokens.css` remain untouched.
- Previous optional media/real-font checks remain historical and were not rerun.
  Manual screen-reader, keyboard/zoom, Firefox/Safari and actual download-dialog
  checks remain open. No new runtime dependencies or network requests were added.
- Next step: try a real Architecture plan and both exported samples, then complete
  the manual accessibility and CI work below.

## Complete sample content maps (21 October 2026)

- Replaced the six-entry starter with complete Basic (11 entries) and Advanced
  (38 entries) inventories. Maps include all main sections and article groups: Basic cards/lists and
  Advanced planning stages, ten lessons, layout/visual workshops, resources and
  components. Added fixed destination IDs and an Advanced footer sitemap.
- Architecture, wireframe/prototype topic labels, both footer maps and generated
  HTML resolve the same selected-sample plan. Untouched complete maps follow the
  mode; the exact old starter upgrades automatically. Custom/empty maps remain
  unchanged across mode switches and JSON round trips. The explicit restore
  button replaces a custom map with the current sample inventory.
- Kept destinations restricted to fixed IDs and escaped unknown labels. Raised
  limits to 64 entries / 8,400 characters (two levels, 64 characters per label).
  Updated training copy, README, architecture notes, changelog and asset versions.
- Added browser regressions for complete destination coverage in both modes,
  matching editor/centre/footer maps, custom preservation/round trips, restore,
  legacy starter upgrades and the expanded parser bound. Existing responsive
  checks now run against the populated Basic sitemap.
- Current verification: `python scripts/check_structure.py` passed (38 assets);
  `git diff --check` passed (existing CRLF normalization notices only).
  First browser run completed at 778/781, including duplicate table-ID and
  complete-map coverage failures. Split the layout-comparison/resource-library
  IDs and included the layout-comparison entry. The second run passed 781/782;
  its remaining assertion still expected the old four-link footer. Updated that
  assertion to check the five footer shortcuts separately from the full sitemap.
  Final `python scripts/browser_review.py` passed **782/782**, with no
  interaction JavaScript errors. All three required checks passed on the final
  implementation; browser checks used an isolated temporary Chrome profile.
- Manual visual, keyboard, screen-reader and Firefox/Safari checks were not run
  for this change. Earlier visual checks above belong to the previous task.
- Next step: review the complete maps with real training content and complete
  the manual accessibility/cross-browser checks. No commits or deployments made.

## Shared sample system and footer review (21 October 2026)

- Confirmed Basic maintained a separate, partial token/CSS generator and fixed
  body/heading sizes, spacing, reading measure, control sizes and card appearance.
  Added `sample-system.js` to capture the existing shared foundation/component
  generator before the sample layouts, with common button classes/footer output.
  Script order remains dependency-safe; there are no new runtime dependencies.
- Both samples now use the same generated ramps, semantic/theme roles, fluid
  typography and spacing tokens, reading width, card borders/shadow/opacity,
  control dimensions/focus, grid alignment and Button Design settings. Basic's
  HTML stays simple. It now uses shared `ds-button` classes and labelled `.input`
  controls; its layout CSS consumes tokens rather than overriding system values.
  General link focus also follows the saved focus width in both exports.
- Replaced duplicate footer implementations with shared identity/Explore rows,
  a closed native expandable sitemap and a copyright/Back to top row. Added
  Advanced's `#top` destination. The full maps and custom plans remain intact;
  shorter footer links remain visible. Rows use the saved responsive cutoff,
  gutters, type, borders and spacing. Footer link weight is now shared too.
- Added regressions comparing actual computed Basic/Advanced styles under default
  and edited/imported settings in both themes, standalone and live preview;
  covered custom button colours/dimensions, footer disclosure and all footer
  target sizes/overflow at 320, 390 and 1440 px. Updated prior assertions for the
  shared system CSS and expandable sitemap. Updated asset versions and docs.
- Current checks: `python scripts/check_structure.py` passed (39 assets),
  `git diff --check` passed (existing CRLF normalization notices only).
  Initial expanded `python scripts/browser_review.py` passed **804/804**, no
  interaction errors. The final run, including the footer weight adjustment and
  custom button colour assertions, also passed **804/804**, with no interaction
  JavaScript errors.
- `python scripts/button_states_review.py` passed **5/5 reduced-motion** and
  **7/7 forced-colour** checks using isolated temporary Chrome profiles.
- Generated and visually inspected temporary screenshots for both modes: 1440 px
  light desktop and exact 390 px dark phone. Footer identity, links, disclosure
  and bottom rows fit; final link-weight consistency was corrected afterward.
  Screenshots are temporary local artifacts, not committed visual baselines.
- Manual keyboard-only, screen-reader, zoom and Firefox/Safari review remain open;
  passing the automated suite does not establish full accessibility. Root user
  snapshots `tokens.css` and `test.html` were not edited. No commits/deployments.
- Next step: review with real training content and complete the manual
  accessibility/cross-browser checks.

## Header navigation consistency (21 October 2026)

- Confirmed Basic header links inherited normal body weight/general underlining,
  while Advanced explicitly used weight 600 and plain links at rest.
- Moved Advanced's header navigation text, hover/pressed underlines and component
  focus ring into shared sample foundation CSS, targeting both headers. Advanced
  resource-table styles remain separate. Basic keeps its wrapping layout and
  Advanced keeps its native mobile menu; text treatment now has one source.
- Refreshed sample-system/sample-homepage asset versions. Added browser checks
  comparing navigation fonts/decoration across modes, both themes, default and
  edited/imported settings, live previews and standalone exports, including
  visible links and focus rings at 320, 390 and 1440 px.
- Current checks: `python scripts/check_structure.py` passed (39 assets) and
  `git diff --check` passed (existing CRLF normalization notices only).
  Required `python scripts/browser_review.py` passed **852/852**, with no
  interaction JavaScript errors, using an isolated temporary Chrome profile.
- No button component rules changed; prior reduced-motion/forced-colour results
  above are historical for this task. Manual keyboard-only, screen-reader and
  cross-browser review were not performed for this small text-style change.
  User root snapshots remain untouched. No commits or deployments.
- Next step: verify navigation in the user's preview and complete the manual
  accessibility/cross-browser review.

## Website-project brief lesson (21 October 2026)

- Replaced the generic user-needs guide with seven website-project prompts:
  purpose/main action, audience, first-release pages/features and exclusions,
  content and its owner, design/technical/accessibility requirements, delivery
  (deadline, budget/time, handover, approval and maintenance), and a success check.
- Added a fill-in template and a clearly labelled static cafe website example.
  The example explains three pages, no online ordering, owner-supplied content,
  branding, phone/keyboard use, delivery and a visitor task. It does not fill in
  or overwrite a learner's saved answers. Unknowns can be marked to confirm.
- Reviewed the old GOV.UK user-needs page, Smashing Magazine's website-planning
  guide (Ben Seigel, needs assessment/client brief) and Figma's design-brief guide.
  The lesson now stands alone and links to Smashing Magazine as optional website
  planning reading. No remote content is loaded into the runtime.
- Updated stage introduction/practice, wizard labels/placeholders/scope help,
  generated Advanced lesson, README, architecture notes, changelog and asset
  version. Existing audience/goal/scope/success/constraints data and limits remain.
- `python scripts/check_structure.py` passed (39 assets); `git diff --check`
  passed (existing CRLF notices only). Full `python scripts/browser_review.py`
  passed **853/853**, with no interaction JavaScript errors.
- After final wording/label corrections, ran a temporary focused harness through
  the same browser runner: **7/7** passed for seven prompts, accent/apostrophe
  rendering, wizard labels, source replacement, saved-field preservation,
  matching Advanced export and the lesson at 320 px. Added the final wording
  assertion to the tracked regression suite afterward; that extra assertion was
  covered by the focused run, not the earlier 853-check full run.
- Manual keyboard/screen-reader, visual screenshot and cross-browser reviews were
  not run for this lesson change. Previous screenshot results remain historical.
  No root snapshots, commits, deployments or runtime dependencies were changed.
- Next step: try writing a brief for a real small website with the revised guide.

## Seven-field brief wizard alignment (21 October 2026)

- Replaced the five combined brief editors with seven numbered fields in the
  approved lesson order: Purpose, Audience, Pages and features, Content, Design
  and requirements, Delivery, Success. Labels and full question text now match
  the centre lesson exactly. Updated guidance and completion prompts accordingly.
- Added one `briefFields` definition for field keys, labels, prompts and limits.
  It generates the wizard, lesson checklist and saved draft, preventing separate
  wording/order from drifting again. Added spacing for the generated editor group
  and refreshed affected JS/CSS query versions.
- Added Content and Delivery to normalized project planning data (empty defaults,
  string-only values, 1,200-character bounds). Kept original goal/audience/scope/
  constraints/success keys. Legacy combined notes remain in their original fields;
  no guessed splitting or automatic overwrite. Shared state makes new answers
  follow JSON, local projects, the centre draft, Advanced preview and HTML export.
- Extended existing autosave, project-switch/file-import and JSON round-trip tests
  with Content/Delivery values. Added parity/order/prompt checks, legacy combined
  note preservation, new field limits/type validation, escaping and reset checks.
  Draft assertions now select a named field rather than assuming Audience is first.
- Current verification: `python scripts/check_structure.py` passed (39 assets),
  `git diff --check` passed (CRLF normalization notices only). Required browser
  suite is running; final result pending.
- Captured and inspected temporary 1440 px/390 px screenshots. Desktop Purpose,
  Audience and Pages/features editors have readable spacing; the narrow wizard
  introduction/navigation fits. These are temporary checks, not screenshot baselines.
- Manual keyboard/screen-reader, full form visual and cross-browser review remain
  open. No network dependencies, root snapshots, commits or deployments changed.
- Next step: record browser results and try a complete brief in the aligned wizard.

## Basic hero image (23 October 2026)

- Added Advanced's embedded 960 x 720 SVG illustration to the Basic hero through
  the shared `DSStudio.samples.illustration` helper. Its bounded cache and current
  palette/theme roles are reused; no network requests or extra export files.
- Basic uses two equal Grid columns with the saved gap, stacking text before the
  image at the saved responsive cutoff. Added descriptive alt text, intrinsic
  dimensions, fluid image sizing and the shared corner radius. Updated sample
  descriptions, architecture notes and affected JavaScript cache versions.
- Added 12 regressions for shared image/inspector/export agreement, live palette
  edits, standalone image loading in both themes and hero geometry at
  320/390/768/1440 px. Updated the hostile-project assertion to allow only the
  intended embedded image while still rejecting injected markup/event handlers.
- First browser attempt was blocked by sandbox access to Chrome's temporary
  profile; reran outside the sandbox using the existing isolated-profile harness.
  First full result: **871/872**, no captured JavaScript errors. All new hero
  checks passed. The failure was an older brief-escaping assertion selecting the
  first field after the seven-field reorder; corrected it to select Audience by
  its field name. Final full rerun: **872/872 passed**, with no captured
  JavaScript errors.
- `python scripts/check_structure.py`: **39 assets verified**.
  `git diff --check`: passed. Browser output captured in the ignored temporary
  `.basic-hero-review.log` while running; no root sample snapshots were edited.
- Manual visual, keyboard, screen-reader and cross-browser checks were not run
  for this change; automated tests do not establish full accessibility.
- Next step: review the Basic hero in the UI and complete manual browser checks.

## Open work / next session

1. Add the browser suite to CI and gate Pages publishing on validation. Current
   CI only checks structure; deployment is a separate workflow.
2. Complete manual keyboard, screen-reader, zoom and visual review; test Firefox
   and Safari. Automated interaction checks do not replace these checks.
3. Review browser download permissions, successful clipboard access and real
   pointer/touch wheel dragging in an interactive browser.
4. Keep the shared-global/module migration as architecture debt; no refactor was
   attempted during this audit.

No commits, pushes or deployments were made in this session.
The older `PROJECT_AUDIT_2026-10-19.md` records a previous, smaller test baseline.
