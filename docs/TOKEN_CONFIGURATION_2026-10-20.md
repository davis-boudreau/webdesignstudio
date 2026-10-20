# Teaching and configuration review

20 October 2026, America/Halifax.

The previous six-step wizard covered the common foundations but left font
sources and responsive typography in the centre, and layout, motion, readability
and surface settings under a separate advanced panel. The catalogue described
values without identifying how to configure them. Heading line-height was fixed
at 1.18. This made it difficult to follow a decision through the system.

The expanded wizard has eight steps. Existing step numbers 1–5 stay stable;
Layout and Accessibility precede Deliver, which is now step 8.

| Step | Configuration responsibilities | Centre learning examples |
| --- | --- | --- |
| 1 Project | Audience, project name, saved starting point | Design workflow and integrated page |
| 2 Palette | Named brand references, three Main Palette anchors, ramp method | Brand assignments and generated ramps |
| 3 Typography | Body/heading families, font source/weights, base, ratio, line-height, tracking, reading measure and responsive bounds | Specimens, ladder, CDN examples and clamp graph |
| 4 Components | Preview theme and all semantic colour roles | Semantic swatches and component examples |
| 5 Buttons | Variant sources/overrides, dimensions, weights, focus and motion | Theme comparison, native controls and state matrix |
| 6 Layout | Spacing unit, corners, borders, elevation, opacity, card minimum, grid gap/alignment | Spacing scale, surfaces and responsive page |
| 7 Accessibility | Control height, focus width, simulated state, link underlines, motion and reduced motion | State explorer and contrast report |
| 8 Deliver | Readiness review and project/CSS export | Export examples and token catalogue |

The centre is a teaching workspace: each existing section begins with an
explanation, token relationship, practice exercise and configuration shortcut.
Interactive experiments such as the colour wheel, comparison controls and
contrast repairs remain available. They use the same state rather than a second
demonstration project. Wizard steps link back to their centre lesson. Step
navigation no longer marks earlier steps complete merely because they were
passed; readiness checks remain explicitly self-reported.

## Catalogue coverage

Every generated token row has a configuration-source mapping and a Configure
source action. The action opens the relevant wizard step, reveals nested
settings and focuses a control. Semantic and button colour rows select the
appropriate theme; button rows also select their variant. Brand references
focus the matching colour by stable token ID.

| Token family | Editable source |
| --- | --- |
| `--brand-*` | Matching Brand Palette colour |
| `--primary-*`, `--secondary-*`, `--accent-*` ramps | Main Palette anchor and ramp method |
| Semantic colours, including dark declarations | Theme-specific semantic role and optional override |
| Font families and `--font-ui` | Font source and heading/body choices; UI is a body-font alias |
| Type steps and body/small text | Base size and ratio |
| Display/H1/H2 fluid sizes | Base, ratio and responsive limits |
| Leading, tracking, heading weight and reading measure | Corresponding typography setting |
| Spacing scale | Spacing unit; numbered tokens remain derived multiples |
| Radius, borders, opacity and elevation | Corresponding layout setting |
| Grid tokens | Card minimum, gap and alignment |
| Control height and focus width | Interaction settings |
| Motion duration and progress-animation name | Duration and reduced-motion settings |
| Button dimensions, font weight, focus and motion | Shared button component settings |
| Button variant source/background/text/border/state colours | Matching variant source or override |

Derived tokens are configured through their sources rather than given arbitrary
independent overrides. This preserves scales and aliases and avoids a second
CSS override system. For example, changing the spacing unit updates every
numbered spacing token. The body-sized scale step responds to the base size,
even though changing the ratio alone would leave it unchanged.

Heading line-height is now a validated project foundation (`headingLeading`,
1–1.6, default 1.18), used by studio specimens, previews, exports and JSON/local
projects. Older projects retain the existing default.

## Implementation and limits

`studio-learning.js` moves existing control DOM nodes once after module
initialization, preserving IDs, handlers, validation and serialization. Hidden
compatibility controls continue to support existing imports and module bindings.
The token catalogue still reads the actual CSS generator, not a second value
list. Browser regression coverage asserts that each generated row maps to a
control inside the expected wizard step; new token families must extend that
mapping. No free-form CSS from imported projects is executed.

The structural wizard reorganization does not add new components or imply that
automated contrast checks establish complete accessibility. Keyboard,
screen-reader and cross-browser review still need human evaluation.
