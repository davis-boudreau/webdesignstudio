'use strict';
/* A static, self-contained HTML specimen using the same exports as the studio.
   Embedded SVG images follow the selected theme and palette without network calls. */
(() => {
  // The teaching recipe and exported styles share the same source.
  const flexRecipe = `.sample-flex-row {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: var(--grid-gap);
}
.sample-flex-tags {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}
.sample-flex-media {
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: var(--grid-gap);
}
.sample-flex-marker { flex: 0 0 var(--space-12); }
.sample-flex-copy { flex: 1 1 12rem; min-width: 0; }
.sample-flex-stack {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.sample-flex-stack > .ds-button { margin-top: auto; }`;
  // A bounded cache avoids repeatedly encoding unchanged SVGs during live edits.
  const illustrations = new Map();
  function illustration(r, detail = false) {
    const key = JSON.stringify([detail, r.primary, r.secondary, r.accent, r.surface, r['surface-muted'], r.text, r.border]);
    if (illustrations.has(key)) return illustrations.get(key);
    const columns = Array.from({ length: 12 }, (_, i) => `<rect x="${96 + i * 64}" y="174" width="52" height="414" rx="6" fill="${r.primary}" opacity=".1"/>`).join('');
    const scene = detail ? `
  <rect x="56" y="56" width="848" height="608" rx="28" fill="${r.surface}" stroke="${r.border}" stroke-width="2"/>
  <text x="96" y="126" fill="${r.text}" font-family="Arial, sans-serif" font-size="30" font-weight="700">A little structure. A lot of possibility.</text>
  ${columns}
  <rect x="96" y="198" width="372" height="152" rx="12" fill="${r.primary}"/>
  <rect x="492" y="198" width="372" height="152" rx="12" fill="${r.secondary}"/>
  <rect x="96" y="374" width="240" height="128" rx="12" fill="${r.accent}"/>
  <rect x="360" y="374" width="240" height="128" rx="12" fill="${r.primary}"/>
  <rect x="624" y="374" width="240" height="128" rx="12" fill="${r.secondary}"/>
  <path d="M96 548H864" stroke="${r.text}" stroke-width="8" stroke-linecap="round" opacity=".25"/>
  <text x="96" y="626" fill="${r.text}" font-family="Arial, sans-serif" font-size="26">12 tracks / flexible spans / one shared rhythm</text>` : `
  <circle cx="818" cy="114" r="100" fill="${r.accent}" opacity=".55"/>
  <rect x="56" y="64" width="848" height="592" rx="28" fill="${r.surface}" stroke="${r.border}" stroke-width="2"/>
  <path d="M58 126H902" stroke="${r.border}" stroke-width="2"/>
  <circle cx="94" cy="96" r="9" fill="${r.primary}"/>
  <circle cx="124" cy="96" r="9" fill="${r.secondary}"/>
  <circle cx="154" cy="96" r="9" fill="${r.accent}"/>
  <rect x="96" y="166" width="48" height="40" rx="8" fill="${r.primary}"/>
  <path d="M168 186H346M678 186H734M762 186H852" stroke="${r.text}" stroke-width="10" stroke-linecap="round" opacity=".55"/>
  <rect x="96" y="246" width="768" height="238" rx="16" fill="${r['surface-muted']}"/>
  <path d="M128 290H380M128 328H346" stroke="${r.primary}" stroke-width="20" stroke-linecap="round"/>
  <path d="M128 372H394M128 398H350" stroke="${r.text}" stroke-width="9" stroke-linecap="round" opacity=".45"/>
  <rect x="128" y="430" width="126" height="24" rx="6" fill="${r.primary}"/>
  <rect x="274" y="430" width="108" height="24" rx="6" fill="${r.secondary}"/>
  <rect x="512" y="274" width="316" height="180" rx="12" fill="${r.surface}"/>
  <rect x="536" y="298" width="124" height="132" rx="8" fill="${r.primary}"/>
  <rect x="676" y="298" width="128" height="56" rx="8" fill="${r.accent}"/>
  <rect x="676" y="370" width="128" height="60" rx="8" fill="${r.secondary}"/>
  ${[96, 360, 624].map((x, i) => `<rect x="${x}" y="512" width="240" height="98" rx="12" fill="${r['surface-muted']}"/><rect x="${x + 20}" y="532" width="32" height="32" rx="8" fill="${[r.primary, r.secondary, r.accent][i]}"/><path d="M${x + 72} 546H${x + 214}" stroke="${r.text}" stroke-width="9" stroke-linecap="round" opacity=".45"/>`).join('')}`;
    const source = 'data:image/svg+xml;charset=utf-8,' + encodeURIComponent(
      `<svg xmlns="http://www.w3.org/2000/svg" width="960" height="720" viewBox="0 0 960 720"><rect width="960" height="720" fill="${r['surface-muted']}"/>${scene}</svg>`);
    if (illustrations.size >= 8) illustrations.delete(illustrations.keys().next().value);
    illustrations.set(key, source);
    return source;
  }

  function homepageHtml() {
    const project = escapeHtml(state.project);
    const roles = palette().roles;
    const settings = state.buttonDesign || {};
    const buttonClass = DSStudio.samples.buttonClass;
    // Page action roles match the wizard variants; Outline remains a gallery example.
    const sectionActions = ([href, label], [secondaryHref, secondaryLabel], indent = '      ') => `${indent}<div class="button-row sample-section-actions">
${indent}  <a class="${buttonClass('primary')}" href="${escapeHtml(href)}">${escapeHtml(label)}</a>
${indent}  <a class="${buttonClass('secondary')}" href="${escapeHtml(secondaryHref)}">${escapeHtml(secondaryLabel)}</a>
${indent}</div>`;
    const variant = ['primary', 'secondary', 'accent', 'outline', 'text'].includes(settings.variant) ? settings.variant : 'primary';
    const interaction = settings.selectedState || 'default';
    const inactive = ['disabled', 'loading'].includes(interaction);
    const actionAttributes = `${inactive ? ' disabled' : ''}${interaction === 'loading' ? ' aria-busy="true"' : ''}${interaction === 'selected' ? ' aria-pressed="true"' : ''}`;
    const actionLabel = interaction === 'loading' ? 'Processing…' : interaction === 'selected' ? 'Email updates' : 'Continue';
    const actionHint = interaction === 'disabled' ? 'Unavailable in this state example. Explain any prerequisite beside a disabled action in your application.' :
      interaction === 'loading' ? 'Processing example: duplicate actions are blocked. Application code should announce completion.' :
        interaction === 'selected' ? 'Toggle examples, off and on: keep the label unchanged and update aria-pressed in application code.' :
          'State example only. Connect this button to an action in your application.';
    const actionExample = `<p class="small-text">Current action state: ${escapeHtml(interaction)}.</p><div class="button-row">${interaction === 'selected' ? `<button class="${buttonClass(variant)}" type="button" aria-pressed="false" aria-describedby="sample-action-help">Email updates</button>` : ''}<button class="${buttonClass(variant)} sample-selected-action" type="button" data-preview-state="${escapeHtml(interaction)}" aria-describedby="sample-action-help"${actionAttributes}>${actionLabel}</button></div><p id="sample-action-help" class="small-text">${actionHint}</p>`;
    const fieldAttributes = `${adv.state === 'disabled' ? ' disabled' : ''}${adv.state === 'readonly' ? ' readonly' : ''}${adv.state === 'invalid' ? ' aria-invalid="true"' : ''}`;
    const emailHelp = adv.state === 'invalid' ? 'Enter an email address in the format name@example.com.' :
      adv.state === 'success' ? 'Your email address looks good.' : 'Use a sample address while exploring this practice form.';
    const headerLinks = [['home', 'Home'], ['about', 'About'], ['design-process', 'Process'], ['services', 'Lessons'], ['resources', 'Resources'], ['contact', 'Contact']]
      .map(([id, label]) => `          <li><a href="#${id}">${label}</a></li>`).join('\n');
    return `<!doctype html>
<html lang="en" data-theme="${state.theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="Learn web design with ${project}: practical lessons in project planning, HTML, CSS Grid and Flexbox, typography, colour and accessible components.">
  <title>${project} — Web Design Field Guide</title>
${DSStudio.fonts.htmlLinks()}  <!-- Save the exported CSS alongside this file. -->
  <link rel="stylesheet" href="tokens.css">
</head>
<body class="sample-home">
  <a class="sample-skip" href="#main-content">Skip to main content</a>
  <header class="sample-header" id="top" tabindex="-1">
    <div class="container sample-header-inner">
      <a class="sample-brand" href="#home">
        <span class="sample-logo" aria-hidden="true">Logo</span>
        <span class="sample-brand-title">${project}</span>
      </a>
      <nav class="sample-desktop-navigation" aria-label="Main navigation">
        <ul class="sample-nav">
${headerLinks}
        </ul>
      </nav>
      <details class="sample-menu" id="sample-menu">
        <summary aria-controls="sample-mobile-navigation">
          <svg class="sample-menu-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false">
            <path class="sample-menu-bars" d="M4 6h16M4 12h16M4 18h16"/>
            <path class="sample-menu-close" d="m6 6 12 12M6 18 18 6"/>
          </svg>
          <span>Menu</span>
        </summary>
        <nav id="sample-mobile-navigation" class="sample-mobile-navigation" aria-label="Main navigation">
          <ul class="sample-nav">
${headerLinks}
          </ul>
        </nav>
      </details>
    </div>
  </header>
  <main id="main-content" class="container" tabindex="-1">
    <section id="home" class="sample-grid sample-hero" aria-labelledby="hero-title">
      <div>
        <p class="sample-eyebrow">${project} / Web Design Field Guide</p>
        <h1 id="hero-title" class="page-title">A better web starts with one good decision.</h1>
        <p class="sample-lead">Learn by making. Turn a simple page into a thoughtful design system with practical lessons in layout, type, colour and accessible interfaces.</p>
        <div class="button-row sample-section-actions">
          <a class="${buttonClass('primary')}" href="#services">Find your first lesson</a>
          <a class="${buttonClass('secondary')}" href="#grid-lab">Explore the live grid <span aria-hidden="true">↘</span></a>
        </div>
        <dl class="sample-stats">
          <div><dt>10 practical lessons</dt><dd>From brief to review</dd></div>
          <div><dt>1 living system</dt><dd>Small decisions, shared rules</dd></div>
        </dl>
      </div>
      <figure class="sample-hero-image">
        <img src="${illustration(roles)}" width="960" height="720" alt="A browser wireframe with a header, a two-column hero, lesson cards and palette-coloured layout blocks.">
        <figcaption>Sketch the page. Connect the decisions. Make it your own.</figcaption>
      </figure>
    </section>
    <section id="about" class="sample-section sample-grid sample-split" aria-labelledby="about-title">
      <figure class="sample-about-image">
        <img src="${illustration(roles, true)}" width="960" height="720" loading="lazy" alt="Twelve grid tracks supporting two equal panels and a row of three cards.">
        <figcaption>One grid can support many compositions.</figcaption>
      </figure>
      <div>
        <p class="sample-eyebrow">About this practice space</p>
        <h2 id="about-title" class="heading-1">Start with structure. Add intention.</h2>
        <p>You do not need a perfect mockup to begin. Start with meaningful content, give it a clear hierarchy, then create a few rules you can reuse.</p>
        <ol class="sample-method"><li><strong>Structure:</strong> use header, main, sections and footer to describe the page.</li><li><strong>Hierarchy:</strong> give headings, body copy and actions distinct jobs.</li><li><strong>Consistency:</strong> connect repeated choices with design tokens.</li></ol>
        <blockquote><p>One layout. A handful of tokens. A system you can explain.</p><cite>Your goal for this field guide</cite></blockquote>
${sectionActions(['#services', 'Browse the lessons'], ['#design-process', 'Plan before the palette'], '        ')}
      </div>
    </section>
    <section id="design-process" class="sample-section" aria-labelledby="process-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">Before the palette</p><h2 id="process-title" class="heading-1">Plan the experience. Then give it a visual language.</h2><p>Start with the audience and task, organize the content, sketch its hierarchy and follow a prototype path. These artifacts reflect the planning fields saved in your studio project. The field guide remains a teaching sample; adapt it to build your finished website.</p></div>
      ${DSStudio.process.stages.map(([id,title,heading],index)=>`<article id="${id}-lab" class="sample-process-stage" aria-labelledby="sample-${id}-title"><p class="sample-eyebrow">${String(index+1).padStart(2,'0')} / ${title}</p><h3 id="sample-${id}-title" class="heading-2">${heading}</h3>${DSStudio.process.artifactHtml(id,'sample-plan')}</article>`).join('\n      ')}
${sectionActions(['#colour-lab', 'Give colours a purpose'], ['#services', 'Choose your next lesson'])}
    </section>
    <section id="services" class="sample-section" aria-labelledby="services-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">Your learning path</p><h2 id="services-title" class="heading-1">Ten small lessons. A stronger foundation.</h2><p>Follow the sequence or choose the skill you want to practise next. Every lesson leads to an example on this page.</p></div>
      <div class="sample-grid card-grid">
        <article id="lesson-brief" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">01 / Brief</span><h3 class="heading-2">Name the problem.</h3><p>Record audience, task, scope, success and constraints.</p><ul><li>An observable audience task</li><li>A success signal to review</li></ul><a class="${buttonClass('text')}" href="#brief-lab">Write a project brief &rarr;</a></article>
        <article id="lesson-architecture" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">02 / Architecture</span><h3 class="heading-2">Make content findable.</h3><p>Group pages and labels around the main audience task.</p><ul><li>A content inventory</li><li>Parent and child relationships</li></ul><a class="${buttonClass('text')}" href="#ia-lab">Read the content map &rarr;</a></article>
        <article id="lesson-wireframe" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">03 / Wireframe</span><h3 class="heading-2">Sketch before styling.</h3><p>Plan hierarchy and responsive reading order with neutral blocks.</p><ul><li>Main and supporting content</li><li>Narrow and wide arrangements</li></ul><a class="${buttonClass('text')}" href="#wireframe-lab">Explore the wireframe &rarr;</a></article>
        <article id="lesson-prototype" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">04 / Prototype</span><h3 class="heading-2">Follow a task.</h3><p>Connect screens, observe hesitation and revise the plan.</p><ul><li>Discover, Choose and Review</li><li>Notes from a task walkthrough</li></ul><a class="${buttonClass('text')}" href="#prototype-lab">Try the prototype &rarr;</a></article>
        <article id="lesson-colour" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">05 / Colour</span><h3 class="heading-2">Give every colour a job.</h3><p>Use the brief to connect brand references to interface roles.</p><ul><li>Primary, Supporting and Accent</li><li>Text, surfaces and contrast</li></ul><a class="${buttonClass('text')}" href="#colour-lab">Read the palette &rarr;</a></article>
        <article id="lesson-typography" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">06 / Typography</span><h3 class="heading-2">Make the next line inviting.</h3><p>Build hierarchy with a small, repeatable type scale.</p><ul><li>Readable body text and leading</li><li>Headings that respond to width</li></ul><a class="${buttonClass('text')}" href="#type-lab">Practise typography &rarr;</a></article>
        <article id="lesson-structure" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">07 / Structure</span><h3 class="heading-2">Give content a home.</h3><p>Use semantic HTML to organize a page before styling it.</p><ul><li>One clear page heading</li><li>Useful landmarks and sections</li></ul><a class="${buttonClass('text')}" href="#about">Start with structure &rarr;</a></article>
        <article id="lesson-layout" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">08 / Layout</span><h3 class="heading-2">Choose a layout system.</h3><p>Use Grid for shared tracks and Flexbox for content along an axis.</p><ul><li>Grid: rows and columns</li><li>Flexbox: align, grow and wrap</li></ul><a class="${buttonClass('text')}" href="#grid-lab">Explore Grid and Flexbox &rarr;</a></article>
        <article id="lesson-components" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">09 / Components</span><h3 class="heading-2">Design beyond the default.</h3><p>Make actions, progress and feedback understandable.</p><ul><li>Hover, focus and pressed cues</li><li>Labels and meaningful feedback</li></ul><a class="${buttonClass('text')}" href="#components">Explore the interface lab &rarr;</a></article>
        <article id="lesson-review" class="card sample-lesson-card sample-flex-stack"><span class="sample-badge">10 / Review</span><h3 class="heading-2">Check what you made.</h3><p>Test with realistic content and keep the next change clear.</p><ul><li>Keyboard, contrast and small screens</li><li>Record remaining human checks</li></ul><a class="${buttonClass('text')}" href="#resources">Review the field notes &rarr;</a></article>
      </div>
${sectionActions(['#grid-lab', 'Start the layout exercise'], ['#resources', 'Browse the field notes'])}
    </section>
    <section id="grid-lab" class="sample-section" aria-labelledby="grid-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">The layout workshop</p><h2 id="grid-title" class="heading-1">Grid and Flexbox. One connected system.</h2><p>Start with normal document flow for headings and paragraphs. Add Grid when rows and columns need shared tracks; use Flexbox when content needs to align along a row or column. Resize this page to compare both systems.</p></div>
      <h3 id="grid-example" class="heading-2">1. Grid gives the page a structure.</h3>
      <div class="sample-grid sample-workshop-grid">
        <figure class="card sample-grid-figure">
          <div class="sample-grid-tracks" aria-hidden="true">${Array.from({ length: 12 }, () => '<span></span>').join('')}</div>
          <div class="sample-grid-demo">
            <div class="sample-demo-header"><strong>Header</strong><small>All 12 columns</small></div>
            <div class="sample-demo-main"><strong>Room for the main idea.</strong><p>The most important content gets the most space.</p><small>Desktop: 8 of 12 columns</small></div>
            <div class="sample-demo-aside"><strong>A useful aside.</strong><p>Keep related notes close.</p><small>Desktop: 4 of 12 columns</small></div>
            <div class="sample-demo-card"><strong>Learn</strong><small>Desktop: 4 columns</small></div>
            <div class="sample-demo-card"><strong>Build</strong><small>Desktop: 4 columns</small></div>
            <div class="sample-demo-card"><strong>Reflect</strong><small>Desktop: 4 columns</small></div>
            <div class="sample-demo-footer"><strong>Footer</strong><small>One complete row</small></div>
          </div>
          <figcaption>Wide screens: 12 equal tracks. Small screens: one readable column.</figcaption>
        </figure>
        <aside class="card sample-lab-notes" aria-labelledby="grid-notes-title">
          <span class="sample-badge">Try this</span><h3 id="grid-notes-title" class="heading-2">Give the layout some room.</h3><ol><li>Compare the page at phone and desktop widths.</li><li>Find the 8 / 4 split and the three equal cards.</li><li>Change the grid gap in the studio, then compare again.</li></ol>
          <details class="sample-code-solution"><summary>See the grid recipe</summary><pre><code>.sample-grid-demo {
  display: grid;
  grid-template-columns:
    repeat(12, minmax(0, 1fr));
  gap: var(--grid-gap);
}

/* Wide view: main / aside */
.sample-demo-main { grid-column: span 8; }
.sample-demo-aside { grid-column: span 4; }
.sample-demo-card { grid-column: span 4; }
.sample-demo-header, .sample-demo-footer {
  grid-column: 1 / -1;
}

@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .sample-grid-demo {
    grid-template-columns: minmax(0, 1fr);
  }
  .sample-demo-main, .sample-demo-aside,
  .sample-demo-card { grid-column: auto; }
}</code></pre></details>
        </aside>
      </div>
      <article id="flex-lab" class="sample-flex-lab" aria-labelledby="flex-title">
        <h3 id="flex-title" class="heading-2">2. Flexbox lets content find its fit.</h3>
        <p>Flexbox works along one main axis at a time. A row follows the inline direction; a column follows the block direction. With wrapping, each new line distributes its own space independently.</p>
        <div class="sample-grid sample-split">
          <div class="card">
            <h4 class="heading-2">A wrapping topic row</h4>
            <div class="sample-flex-row">
              <strong>Explore a topic</strong>
              <div class="sample-flex-tags" role="list" aria-label="Example topics">
                <span class="sample-badge" role="listitem">HTML</span><span class="sample-badge" role="listitem">CSS Grid</span><span class="sample-badge" role="listitem">Flexbox</span>
              </div>
            </div>
            <p class="small-text">The title and topics use space-between on the main axis and center on the cross axis. Gap keeps a minimum separation; flex-wrap moves items onto another line when space runs out.</p>
            <h4 class="heading-2">A flexible content row</h4>
            <div class="sample-flex-media">
              <span class="sample-flex-marker" aria-hidden="true">Aa</span>
              <div class="sample-flex-copy"><strong>Let the words take the space.</strong><p>The marker keeps its width. This text grows into available space, shrinks when needed and wraps below the marker when its basis no longer fits.</p></div>
            </div>
            <p class="small-text">flex: 1 1 12rem means grow: 1, shrink: 1, basis: 12rem. min-width: 0 allows the text item to shrink below its automatic minimum.</p>
          </div>
          <aside class="card" aria-labelledby="flex-notes-title">
            <span class="sample-badge">Try this</span><h4 id="flex-notes-title" class="heading-2">Follow the axes.</h4>
            <ol><li>Compare 390 px and 1280 px previews. Watch the topics wrap.</li><li>Change the grid gap: both Grid tracks and these Flexbox rows share that token.</li><li>Inspect the lesson cards: Grid places each card; a column flex container pushes its final link down with margin-top: auto.</li></ol>
            <p>Use justify-content along the main axis and align-items across it. Changing flex-direction changes which axis each property controls. Keep the HTML in a meaningful reading order when wrapping.</p>
            <details class="sample-code-solution"><summary>See the Flexbox recipes</summary><pre><code>${escapeHtml(flexRecipe)}</code></pre></details>
          </aside>
        </div>
      </article>
      <div class="sample-layout-comparison" aria-labelledby="layout-choice-title">
        <h3 id="layout-choice-title" class="heading-2">3. Combine the systems with purpose.</h3>
        <div id="layout-comparison" class="sample-table-wrap" role="region" aria-label="Layout system comparison" tabindex="0">
          <table><caption>Choose by the relationship your content needs</caption><thead><tr><th scope="col">System</th><th scope="col">Useful for</th><th scope="col">On this page</th></tr></thead><tbody>
            <tr><th scope="row">Normal flow</th><td>Content read in sequence</td><td>Headings and paragraphs</td></tr>
            <tr><th scope="row">CSS Grid</th><td>Shared row and column tracks</td><td>Page splits and lesson-card placement</td></tr>
            <tr><th scope="row">Flexbox</th><td>Alignment and sizing along an axis</td><td>Navigation, action pairs, topic rows and card interiors</td></tr>
          </tbody></table>
        </div>
        <p class="small-text">Grid can lay out a single row, and Flexbox can wrap into several rows. Choose based on whether items need shared tracks or independent space distribution. The lesson board nests Flexbox inside Grid.</p>
      </div>
${sectionActions(['#type-lab', 'Explore type and colour'], ['#resources', 'Check your layout'])}
    </section>
    <section id="type-lab" class="sample-section" aria-labelledby="type-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">The visual language workshop</p><h2 id="type-title" class="heading-1">Make the important thing easy to find.</h2><p>Use type to create hierarchy and colour to reinforce purpose. The examples below follow your current design decisions.</p></div>
      <div class="sample-grid sample-split">
        <article id="type-specimen" class="card sample-type-specimen"><p class="sample-eyebrow">An exercise in hierarchy</p><h3 class="heading-1">Space to think.<br>Room to create.</h3><p>Good typography guides a reader from the big idea to the useful details. Keep the message clear, the measure comfortable and the next action easy to find.</p><dl class="sample-type-settings"><div><dt>Body size</dt><dd>${state.base}px</dd></div><div><dt>Scale ratio</dt><dd>${state.ratio}</dd></div><div><dt>Body line-height</dt><dd>${state.leading}</dd></div></dl></article>
        <article id="colour-lab" class="card sample-colour-lab" aria-labelledby="colour-title"><span class="sample-badge">Colour with purpose</span><h3 id="colour-title" class="heading-2">A palette becomes a language.</h3><p>These are interface roles, not a list of interchangeable paint colours. Check each foreground against its actual background in both themes.</p><ul class="sample-token-palette"><li><span class="sample-palette-dot sample-palette-dot--primary" aria-hidden="true"></span><span><strong>Primary</strong><small>Main actions and links</small></span><code>${roles.primary}</code></li><li><span class="sample-palette-dot sample-palette-dot--secondary" aria-hidden="true"></span><span><strong>Supporting</strong><small>Supporting actions</small></span><code>${roles.secondary}</code></li><li><span class="sample-palette-dot sample-palette-dot--accent" aria-hidden="true"></span><span><strong>Accent</strong><small>Highlights and details</small></span><code>${roles.accent}</code></li></ul><p class="small-text">Add words, shape or an icon whenever colour communicates meaning.</p></article>
      </div>
${sectionActions(['#components', 'Explore component states'], ['#contact', 'Ask a design question'])}
    </section>
    <section id="resources" class="sample-section" aria-labelledby="resources-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">Keep these field notes close</p><h2 id="resources-title" class="heading-1">A little guidance for your next build.</h2><p>Start small, review the details and leave yourself a clear next step.</p></div>
      <div class="sample-grid sample-split">
        <div id="resource-library" class="sample-table-wrap" role="region" aria-label="Resource library" tabindex="0">
          <table><caption>Resources for your next website</caption><thead><tr><th scope="col">Resource</th><th scope="col">Format</th><th scope="col">Explore</th></tr></thead><tbody>
            <tr><th scope="row">Build your first page</th><td><span class="sample-badge">Guide</span></td><td><a href="#getting-started">Read the guide</a></td></tr>
            <tr><th scope="row">Review your design</th><td><span class="sample-badge">Checklist</span></td><td><a href="#working-together">See the checklist</a></td></tr>
            <tr><th scope="row">A question worth asking</th><td><span class="sample-badge">Practice</span></td><td><a href="#contact">Ask a question</a></td></tr>
          </tbody></table>
        </div>
        <div class="sample-faq">
          <details id="getting-started" open><summary>How do I use this field guide?</summary><p>Start with the brief, content map, wireframe and prototype before choosing a palette. Then choose a lesson, inspect the example and change one design decision in the studio. Compare the preview with the generated HTML and CSS. Write down what changed and why it helped.</p></details>
          <details id="working-together"><summary>What belongs in my review checklist?</summary><p>Check a narrow viewport, long headings, keyboard focus, form labels and text contrast in both themes. Test intermediate widths too. Record anything that still needs a human review before sharing your work.</p></details>
          <details id="learning-from-exports"><summary>Can I learn from the exported page?</summary><p>Yes. Save the HTML and its companion CSS together, open the page and trace a component class back to its design tokens. The planning artifacts, linked prototype, Grid, Flexbox and native menu work without a JavaScript framework.</p></details>
        </div>
      </div>
      <aside id="practice-tip" class="sample-notice" aria-label="Practice tip"><strong>Change one decision at a time.</strong> Compare before and after, test at another width, and write down the reason for your choice.</aside>
${sectionActions(['#contact', 'Bring a design question'], ['#components', 'Explore the interface lab'])}
    </section>
    <section id="contact" class="sample-section sample-grid sample-split" aria-labelledby="contact-title">
      <div><p class="sample-eyebrow">A space for your next question</p><h2 id="contact-title" class="heading-1">What would you like to figure out?</h2><p>A layout that will not quite fit? A type scale that feels too loud? Describe the decision you are practising, what you tried and what you noticed.</p><p class="small-text">Use this practice form to explore labels, validation and field states. It has no message-delivery backend.</p></div>
      <form class="card sample-form" action="#contact" method="get" aria-describedby="contact-note">
        <div><label for="contact-name">Your name</label><input class="input" id="contact-name" name="name" autocomplete="name" placeholder="Alex Morgan" required></div>
        <div><label for="contact-email">Email address</label><input class="input" type="email" id="contact-email" name="email" autocomplete="email" placeholder="alex@example.com" aria-describedby="contact-email-help"${fieldAttributes} required><small id="contact-email-help"${adv.state === 'invalid' ? ' class="sample-error"' : ''}>${emailHelp}</small></div>
        <div><label for="contact-service">What are you practising?</label><select class="input" id="contact-service" name="service"><option value="">Choose a topic</option><option>Project brief and architecture</option><option>Wireframing and prototyping</option><option>Semantic HTML</option><option>Responsive CSS Grid and Flexbox</option><option>Typography and colour</option><option>Accessible components</option></select></div>
        <fieldset><legend>How would you like to practise?</legend><label class="sample-choice"><input type="radio" name="start" value="conversation" checked> A quick question</label><label class="sample-choice"><input type="radio" name="start" value="workshop"> A guided exercise</label></fieldset>
        <div><label for="contact-message">What have you tried?</label><textarea class="input" id="contact-message" name="message" rows="4" placeholder="I am trying to… Here is what I noticed…"></textarea></div>
        <label class="sample-choice"><input type="checkbox" name="copy" value="yes"> Include a copy in this practice request.</label>
        <div class="button-row sample-section-actions">
          <button class="${buttonClass('primary')}" type="submit">Preview my question</button>
          <a class="${buttonClass('secondary')}" href="#services">Revisit the lessons</a>
        </div>
        <p id="contact-note" class="small-text">This is a sample form. No message is sent; submitting returns to this page.</p>
      </form>
    </section>
    <section id="components" class="sample-section" aria-labelledby="components-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">The interface lab</p><h2 id="components-title" class="heading-1">Small details. A more usable interface.</h2><p>Compare action priorities, look for non-colour state cues and explore native form controls. These examples follow the settings in your Button Design Wizard.</p></div>
      <div class="sample-grid card-grid">
        <article id="component-actions" class="card"><h3 class="heading-2">Actions that feel familiar</h3><div class="button-row">${['primary', 'secondary', 'accent', 'outline', 'text'].map(v => `<button class="${buttonClass(v)}" type="button">${v[0].toUpperCase() + v.slice(1)} action</button>`).join('')}</div>${actionExample}</article>
        <article id="component-feedback" class="card"><h3 class="heading-2">Helpful feedback</h3><p class="sample-feedback sample-feedback--success"><strong>Success.</strong> You’re ready for the next step.</p><p class="sample-feedback sample-feedback--warning"><strong>One more thing.</strong> Review your details before continuing.</p><p class="sample-feedback sample-feedback--danger"><strong>Something needs attention.</strong> Check the highlighted field.</p></article>
        <article id="component-progress" class="card"><h3 class="heading-2">Progress at a glance</h3><label for="sample-progress">Practice checklist — 3 of 4 complete</label><progress id="sample-progress" value="3" max="4">75%</progress><label for="sample-range">Your confidence with CSS Grid</label><input id="sample-range" type="range" min="1" max="5" value="3"><label for="sample-reference">Lesson reference</label><input class="input" id="sample-reference" value="LESSON-001" readonly><label for="sample-unavailable">Available after your review</label><input class="input" id="sample-unavailable" value="Not available yet" disabled></article>
      </div>
${sectionActions(['#contact', 'Ask a design question'], ['#grid-lab', 'Return to the grid'])}
    </section>
  </main>
  ${DSStudio.samples.footerHtml('advanced')}
</body>
</html>
`;
  }

  function homepageCss() {
    // Breakpoints follow the actual content width and the saved card controls.
    const threeCards = adv.columns * 3 + adv.gap * 2;
    const twoCards = adv.columns * 2 + adv.gap;
    return `/* SAMPLE HOME PAGE: 12-column layout; 8px rhythm with 4px fine spacing at defaults.
   The spacing-unit and component controls remain configurable. */
.sample-home { color-scheme: light; }
[data-theme="dark"].sample-home { color-scheme: dark; }
.sample-home *, .sample-home *::before, .sample-home *::after { box-sizing: border-box; }
.sample-home h1, .sample-home h2, .sample-home h3 { margin: 0 0 var(--space-4); font-weight: var(--heading-weight); text-wrap: balance; overflow-wrap: anywhere; }
.sample-home p { margin: 0 0 var(--space-6); }
.sample-home :where(a:not(.ds-button)) { color: var(--primary); text-underline-offset: .2em; overflow-wrap: anywhere; }
.sample-home img { display: block; width: 100%; height: auto; border-radius: var(--radius-base); }
.sample-home figure { margin: 0; min-width: 0; }
.sample-home figcaption { margin-top: var(--space-2); color: var(--text-muted); font-size: var(--text-small); }
.sample-home section[id] { scroll-margin-top: var(--space-8); }
.sample-header, .sample-footer { background: var(--surface); border-block: var(--border-width) solid var(--border); }
.sample-header-inner, .sample-footer-inner { display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: var(--space-4); padding-block: var(--space-4); }
.sample-header-inner { position: relative; }
.sample-home .sample-brand { display: inline-flex; gap: var(--space-2); align-items: center; color: var(--text); font-weight: var(--heading-weight); text-decoration: none; max-width: 100%; }
.sample-logo { display: grid; place-items: center; flex: none; width: var(--space-12); aspect-ratio: 1; border: var(--border-width) solid var(--primary); border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font-size: clamp(.75rem, 3vw, 1rem); line-height: 1; letter-spacing: 0; }
.sample-brand-title { min-width: 0; font-family: var(--font-heading); font-size: var(--text-h2); line-height: var(--heading-leading); letter-spacing: var(--heading-letter-spacing); overflow-wrap: anywhere; }
.sample-nav { display: flex; flex-wrap: wrap; gap: var(--space-2) var(--space-6); padding: 0; margin: 0; list-style: none; }
.sample-table-wrap a { text-decoration: none; text-underline-offset: .2em; text-decoration-thickness: .1em; }
.sample-table-wrap a:hover { text-decoration-line: underline; }
.sample-table-wrap a:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }
.sample-table-wrap a:active { text-decoration-line: underline; text-decoration-thickness: .2em; }
.sample-menu { display: none; }
.sample-menu summary { display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2); min-width: 48px; min-height: 48px; padding: var(--space-2); border: 0; border-radius: var(--radius-base); background: transparent; color: var(--text); font: inherit; font-weight: 700; cursor: pointer; list-style: none; }
.sample-menu summary::-webkit-details-marker { display: none; }
.sample-menu-icon { flex: none; color: var(--accent); }
.sample-menu-close, .sample-menu[open] .sample-menu-bars { display: none; }
.sample-menu[open] .sample-menu-close { display: inline; }
.sample-mobile-navigation { position: absolute; inset-inline: 0; top: 100%; z-index: 10; padding: var(--space-2); border: var(--border-width) solid var(--control-border); border-radius: var(--radius-base); background: var(--surface); box-shadow: var(--elevation); }
.sample-menu:not([open]) .sample-mobile-navigation { display: none; }
.sample-mobile-navigation .sample-nav { display: grid; gap: 0; }
.sample-mobile-navigation a { display: flex; align-items: center; min-height: 48px; padding: var(--space-2); border-radius: var(--radius-base); }
.sample-mobile-navigation a:hover { background: var(--surface-muted); }
.sample-skip { position: absolute; left: var(--space-4); top: -10rem; padding: var(--space-4); z-index: 1; background: var(--surface); }
.sample-skip:focus { top: var(--space-4); }
.sample-home main.container { container: sample-content / inline-size; }
.sample-home .sample-grid { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--grid-gap); }
.sample-grid > * { grid-column: span 6; min-width: 0; }
.sample-home .card-grid > .card { grid-column: span 4; }
.sample-hero { align-items: center; padding-block: var(--space-12); }
.sample-split { align-items: start; }
.sample-home .sample-eyebrow { font-size: var(--text-small); font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: var(--text-muted); }
.sample-lead { font-size: var(--text-h2); line-height: var(--body-leading); color: var(--text-muted); }
.sample-home .button-row { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-2); }
.sample-section > .sample-section-actions { margin-top: var(--space-6); }
.sample-home .ds-button { max-width: 100%; overflow-wrap: anywhere; }
.sample-home #sample-action-help { margin-top: var(--space-4); }
${['primary', 'secondary', 'accent', 'outline', 'text'].map(v => `.sample-selected-action.ds-button--${v}[data-preview-state="hover"] { background: var(--button-${v}-hover); color: var(--button-${v}-hover-text); }
.sample-selected-action.ds-button--${v}[data-preview-state="active"] { background: var(--button-${v}-active); color: var(--button-${v}-active-text); }`).join('\n')}
.sample-selected-action[data-preview-state="focus"] { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }
.sample-stats { display: flex; flex-wrap: wrap; gap: var(--space-6); margin: var(--space-8) 0 0; padding-top: var(--space-4); border-top: var(--border-width) solid var(--border); }
.sample-stats dt { font-weight: 700; }
.sample-stats dd { margin: var(--space-1) 0 0; font-size: var(--text-small); color: var(--text-muted); }
.sample-section { padding-block: var(--space-8); border-top: var(--border-width) solid var(--border); }
.sample-process-stage { padding-block: var(--space-8); border-top: var(--border-width) solid var(--border); }
.sample-process-stage > :last-child { margin-bottom: 0; }
.sample-section-heading { max-width: 44rem; margin-bottom: var(--space-8); }
.sample-section-heading > :last-child, .sample-home .card > :last-child, .sample-form > :last-child { margin-bottom: 0; }
.sample-home .card ul { padding-inline-start: var(--space-6); margin-block: var(--space-4); }
${flexRecipe}
.sample-flex-lab, .sample-layout-comparison { margin-top: var(--space-8); }
.sample-flex-row, .sample-flex-media { padding: var(--space-4); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); background: var(--surface-muted); }
.sample-flex-row > *, .sample-flex-tags > * { min-width: 0; overflow-wrap: anywhere; }
.sample-flex-marker { display: grid; place-items: center; min-height: var(--space-12); border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font-weight: 700; }
.sample-flex-copy { overflow-wrap: anywhere; }
.sample-flex-copy > :last-child { margin-bottom: 0; }
.sample-flex-lab h4 { margin-top: var(--space-4); }
.sample-layout-comparison + .sample-section-actions { margin-top: var(--space-6); }
.sample-method, .sample-lab-notes ol { padding-inline-start: var(--space-6); margin-block: var(--space-6); }
.sample-workshop-grid > .sample-grid-figure { grid-column: span 8; }
.sample-workshop-grid > .sample-lab-notes { grid-column: span 4; }
.sample-grid-tracks { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--space-1); margin-bottom: var(--space-4); }
.sample-grid-tracks span { min-width: 0; height: var(--space-4); border-radius: var(--radius-base); background: var(--primary); opacity: .25; }
.sample-grid-demo { display: grid; grid-template-columns: repeat(12, minmax(0, 1fr)); gap: var(--grid-gap); }
.sample-grid-demo > div { min-width: 0; padding: var(--space-4); border-radius: var(--radius-base); overflow-wrap: anywhere; }
.sample-grid-demo p { margin: var(--space-2) 0; }
.sample-grid-demo small { display: block; margin-top: var(--space-1); }
.sample-demo-header, .sample-demo-footer { grid-column: 1 / -1; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: var(--space-2); background: var(--primary); color: var(--on-primary); }
.sample-demo-main { grid-column: span 8; background: var(--surface-muted); }
.sample-demo-aside { grid-column: span 4; background: var(--accent); color: var(--on-accent); }
.sample-demo-card { grid-column: span 4; border: var(--border-width) solid var(--border); background: var(--surface); }
.sample-code-solution { padding-top: var(--space-4); border-top: var(--border-width) solid var(--border); }
.sample-code-solution summary { cursor: pointer; font-weight: 600; }
.sample-code-solution pre { max-width: 100%; margin: var(--space-4) 0 0; padding: var(--space-4); white-space: pre-wrap; overflow-wrap: anywhere; font-size: var(--text-small); border-radius: var(--radius-base); background: var(--surface-muted); }
.sample-type-settings { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: var(--space-4); margin: var(--space-6) 0 0; padding-top: var(--space-4); border-top: var(--border-width) solid var(--border); }
.sample-type-settings dt { font-size: var(--text-small); color: var(--text-muted); }
.sample-type-settings dd { margin: var(--space-2) 0 0; font-size: var(--text-h2); font-weight: var(--heading-weight); overflow-wrap: anywhere; }
.sample-home .card .sample-token-palette { display: grid; gap: var(--space-4); padding: 0; margin: var(--space-6) 0; list-style: none; }
.sample-token-palette li { display: grid; grid-template-columns: var(--space-8) minmax(0, 1fr) auto; align-items: center; gap: var(--space-2); min-width: 0; }
.sample-token-palette li + li { margin-top: 0; }
.sample-token-palette span, .sample-token-palette code { min-width: 0; overflow-wrap: anywhere; }
.sample-token-palette small { display: block; color: var(--text-muted); }
.sample-token-palette code { font-size: var(--text-small); }
.sample-palette-dot { width: var(--space-8); aspect-ratio: 1; border: var(--border-width) solid var(--border); border-radius: var(--radius-base); }
.sample-palette-dot--primary { background: var(--primary); }
.sample-palette-dot--secondary { background: var(--secondary); }
.sample-palette-dot--accent { background: var(--accent); }
.sample-home li + li { margin-top: var(--space-2); }
.sample-home .sample-nav li + li { margin-top: 0; }
.sample-badge { display: inline-block; padding: var(--space-1) var(--space-2); margin-bottom: var(--space-4); border-radius: var(--radius-base); background: var(--accent); color: var(--on-accent); font-size: var(--text-small); font-weight: 600; }
.sample-home blockquote { margin: var(--space-6) 0; padding: var(--space-4); border-inline-start: 4px solid var(--accent); background: var(--surface-muted); border-radius: 0 var(--radius-base) var(--radius-base) 0; }
.sample-home blockquote p { margin-bottom: var(--space-2); }
.sample-home cite { font-size: var(--text-small); color: var(--text-muted); }
.sample-table-wrap { overflow: auto; border: var(--border-width) solid var(--border); border-radius: var(--radius-base); }
.sample-home table { border-collapse: collapse; width: 100%; background: var(--surface); text-align: start; }
.sample-home caption { padding: var(--space-4); text-align: start; font-weight: 700; }
.sample-home th, .sample-home td { padding: var(--space-4); border-top: var(--border-width) solid var(--border); }
.sample-home thead { background: var(--surface-muted); }
.sample-home td .sample-badge { margin: 0; }
.sample-faq details { padding: var(--space-4); background: var(--surface); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); margin-bottom: var(--space-2); }
.sample-faq summary { cursor: pointer; font-weight: 700; }
.sample-faq details p { margin: var(--space-4) 0 0; }
.sample-notice { margin-top: var(--space-8); padding: var(--space-4); background: var(--surface-muted); border-inline-start: 4px solid var(--primary); border-radius: var(--radius-base); }
.sample-form { display: grid; gap: var(--space-4); }
.sample-home label, .sample-home legend { display: block; font-weight: 600; margin-bottom: var(--space-2); }
.sample-home .input + label { margin-top: var(--space-4); }
.sample-home .input { display: block; width: 100%; max-width: 100%; padding: var(--space-2) var(--space-4); border-radius: var(--radius-base); background: var(--surface); color: var(--text); font: inherit; }
.sample-home .input[readonly] { background: var(--surface-muted); }
.sample-home .input:disabled { opacity: .55; cursor: not-allowed; }
.sample-home small, .sample-home .small-text { font-size: var(--text-small); }
.sample-form small { display: block; margin-top: var(--space-1); color: var(--text-muted); }
.sample-form .sample-error { color: var(--danger); }
.sample-form fieldset { min-width: 0; margin: 0; padding: var(--space-4); border: var(--border-width) solid var(--control-border); border-radius: var(--radius-base); }
.sample-home .sample-choice { display: flex; align-items: baseline; gap: var(--space-2); font-weight: 400; }
.sample-home input[type="checkbox"], .sample-home input[type="radio"], .sample-home input[type="range"], .sample-home progress { accent-color: var(--primary); }
.sample-home progress, .sample-home input[type="range"] { display: block; width: 100%; margin: var(--space-2) 0 var(--space-6); }
.sample-feedback { padding: var(--space-4); border: var(--border-width) solid var(--border); border-inline-start-width: 4px; border-radius: var(--radius-base); background: var(--surface-muted); }
.sample-feedback--success { border-inline-start-color: var(--success); }
.sample-feedback--warning { border-inline-start-color: var(--warning); }
.sample-feedback--danger { border-inline-start-color: var(--danger); }
.sample-footer-inner { align-items: start; padding-block: var(--space-8); }
.sample-footer p { margin-top: var(--space-2); color: var(--text-muted); }
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .sample-section { padding-block: var(--space-12); }
}
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().wide)}) {
  .sample-home .container { padding-inline: var(--page-gutter-wide); }
  .sample-logo { width: var(--space-16); }
  .sample-hero { padding-block: var(--space-20); }
  .sample-section { padding-block: var(--space-16); }
}
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().wide)}) {
  .sample-home .sample-workshop-grid { grid-template-columns: minmax(0, 1fr); }
  .sample-workshop-grid > .sample-grid-figure, .sample-workshop-grid > .sample-lab-notes { grid-column: auto; }
}
/* Keep the card minimum/gap controls effective within the 12-column page. */
@container sample-content (width < ${threeCards}px) {
  .sample-home .card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .sample-home .card-grid > .card { grid-column: auto; }
}
@container sample-content (width < ${twoCards}px) {
  .sample-home .card-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .sample-home .sample-hero, .sample-home .sample-split { grid-template-columns: minmax(0, 1fr); }
  .sample-hero > *, .sample-split > * { grid-column: auto; }
  .sample-header-inner { align-items: center; flex-direction: row; flex-wrap: nowrap; }
  .sample-header .sample-brand { flex: 1; min-width: 0; }
  .sample-desktop-navigation { display: none; }
  .sample-menu { display: block; flex: none; }
  .sample-hero-image { max-width: 36rem; }
  .sample-about-image { max-width: 32rem; }
  .sample-grid-demo { grid-template-columns: minmax(0, 1fr); }
  .sample-demo-main, .sample-demo-aside, .sample-demo-card { grid-column: auto; }
  .sample-token-palette li { grid-template-columns: var(--space-8) minmax(0, 1fr); }
  .sample-token-palette code { grid-column: 2; }
}
`;
  }

  DSStudio.register({
    id: 'sample-homepage',
    title: 'Sample home page',
    init() {
      DSStudio.samples.illustration = illustration;
      const previousCss = cssExport;
      cssExport = () => previousCss() + '\n' + homepageCss() + DSStudio.samples.footerCss();
      htmlExport = homepageHtml;
      renderCode();
    }
  });
})();
