'use strict';
/* A compact beginner UI component showcase. Advanced retains its existing generators;
   both modes share the project foundations, preview and paired file actions. */
(() => {
  // Format generated teaching markup without parsing or executing its content.
  function readableHtml(html) {
    const preservedBlocks = [];
    html = html.replace(/<(pre|textarea)\b[^>]*>[\s\S]*?<\/\1>/g, block => {
      preservedBlocks.push(block);
      return `<!--PRESERVED-BLOCK:${preservedBlocks.length - 1}-->`;
    });
    let depth = 0;
    const voidTag = /^(?:area|base|br|col|embed|hr|img|input|link|meta|source|track|wbr)$/;
    return html.replace(/>\s*</g, '>\n<').split('\n').map(raw => {
      const line = raw.trim();
      if (!line) return '';
      const startsWithClose = /^<\//.test(line);
      const indent = Math.max(0, depth - (startsWithClose ? 1 : 0));
      for (const tag of line.matchAll(/<(\/?)([a-z][a-z0-9-]*)\b[^>]*>/gi)) {
        if (!voidTag.test(tag[2].toLowerCase()) && !tag[0].endsWith('/>')) depth += tag[1] ? -1 : 1;
      }
      return '  '.repeat(indent) + line;
    }).join('\n').replace(/<!--PRESERVED-BLOCK:(\d+)-->/g, (_, index) => preservedBlocks[Number(index)]);
  }

  function basicHtml() {
    const project = escapeHtml(state.project);
    const navigation = DSStudio.samples.basicNavigationHtml();
    const action = (href, label, variant = 'primary') => `<a class="button ${DSStudio.samples.buttonClass(variant)}" href="#${href}">${label}</a>`;
    const actions = (href, label, secondaryHref, secondaryLabel) => `<div class="section-actions">${action(href, label)}${action(secondaryHref, secondaryLabel, 'secondary')}</div>`;
    return readableHtml(`<!doctype html>
<html lang="en" data-theme="${state.theme}">
<!-- SECTION: basics | Document setup and a stylesheet shared by every section. -->
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${project}: essential HTML components, Flexbox rows and responsive Grid layouts.">
  <title>${project} | UI essentials</title>
${DSStudio.fonts.htmlLinks()}  <link rel="stylesheet" href="tokens.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>

  <!-- SECTION: header | Desktop links become a native hamburger menu on narrow screens. -->
  <header class="site-header" id="top" tabindex="-1">
    <div class="container header-inner">
      <a class="brand" href="#top"><span class="logo" aria-hidden="true">Logo</span><span>${project}</span></a>
      <nav class="desktop-navigation" aria-label="Main navigation">
        <ul class="nav-list">${navigation}</ul>
      </nav>
      <!-- Native details/summary provides keyboard and touch operation without scripts. -->
      <details class="basic-menu" id="basic-menu">
        <summary>
          <svg class="menu-icon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true" focusable="false">
            <path class="menu-bars" d="M4 6h16M4 12h16M4 18h16"/>
            <path class="menu-close" d="m6 6 12 12M6 18 18 6"/>
          </svg>
          <span>Menu</span>
        </summary>
        <nav class="mobile-navigation" aria-label="Mobile navigation">
          <ul class="nav-list">${navigation}</ul>
        </nav>
      </details>
    </div>
  </header>

  <main id="main-content" tabindex="-1">
    <!-- SECTION: hero | A two-column introduction with two clear calls to action. -->
    <section class="hero" id="home" aria-labelledby="hero-title">
      <div class="container hero-layout">
        <div>
          <p class="eyebrow">HTML &amp; CSS essentials</p>
          <h1 id="hero-title">Start with the essentials.</h1>
          <p class="intro">Explore the building blocks of a responsive page. Simple components, meaningful HTML and layouts that adapt.</p>
          ${actions('features', 'Explore components', 'lists', 'Compare layouts')}
          <p class="hero-note">Links take you somewhere. Buttons perform an action. Try both on this page.</p>
        </div>
        <figure class="hero-image">
          <img src="${DSStudio.samples.illustration(palette().roles)}" width="960" height="720" alt="A website concept with a clear header, welcoming introduction and neatly arranged content cards.">
          <figcaption>A clear page structure, from header to footer.</figcaption>
        </figure>
      </div>
    </section>

    <!-- SECTION: skills | Flexbox places the introduction beside three component cards. -->
    <section class="section container" id="features" aria-labelledby="features-title">
      <div class="skills-layout">
        <div class="skills-intro">
          <p class="eyebrow">Components / Flexbox</p>
          <h2 id="features-title">Everyday components. Simple structure.</h2>
          <p>This section combines a flexible introduction with a vertical card stack. Each article has a heading and a purpose.</p>
          ${actions('lists', 'Explore Grid layouts', 'signup', 'Try the form controls')}
        </div>
        <div class="skill-cards">
          <article class="card" id="basic-structure"><p class="eyebrow">Article / Content card</p><h3>A heading, text and a clear link.</h3><p>A card groups related content. Use article when the item makes sense on its own.</p><a href="#list-collection">Explore the list cards &rarr;</a></article>
          <article class="card" id="basic-layout"><p class="eyebrow">Flexbox / Profile row</p><h3>Fixed avatar. Flexible content.</h3><div class="component-demo media-object"><span class="avatar" aria-hidden="true">AB</span><div class="media-copy"><strong>Alex Brooks</strong><p>Course mentor</p><span class="badge">Available</span></div></div><p>This row works for profiles, comments and compact list items.</p><a href="#list-workflow">See an ordered sequence &rarr;</a></article>
          <article class="card" id="basic-usability"><p class="eyebrow">Details / FAQ disclosure</p><h3>A question with an expandable answer.</h3><details class="component-demo faq-demo" id="basic-faq"><summary>Does this disclosure need JavaScript?</summary><p>No. The browser handles opening, closing and keyboard interaction through details and summary.</p></details><a href="#list-terms">Review useful layout terms &rarr;</a></article>
        </div>
      </div>
    </section>

    <!-- SECTION: toolkit | CSS Grid groups list examples into equal-width cards. -->
    <section class="section toolkit" id="lists" aria-labelledby="lists-title">
      <div class="container">
        <div class="toolkit-heading"><p class="eyebrow">Layouts / CSS Grid</p><h2 id="lists-title">One grid. Different kinds of content.</h2><p>These equal-width cards add columns when space allows. Resize the page to see the grid adapt, keeping the content in reading order.</p></div>
        <div class="list-grid" id="cards-grid">
          <article class="card" id="list-collection"><h3>Unordered list</h3><p>Related items without a required sequence.</p><ul><li>A useful heading</li><li>Readable content</li><li>A clear next action</li></ul></article>
          <article class="card" id="list-workflow"><h3>Ordered list</h3><p>Steps where the sequence matters.</p><ol><li>Write the HTML.</li><li>Add the CSS.</li><li>Test the page.</li></ol></article>
          <article class="card" id="list-terms"><h3>Description list</h3><dl><dt>Flexbox</dt><dd>A row or column of flexible items.</dd><dt>Grid</dt><dd>A layout organised into rows and columns.</dd><dt>Responsive</dt><dd>Content that adapts to available space.</dd></dl></article>
        </div>
        <section class="layout-example" aria-labelledby="sidebar-example-title">
          <h3 id="sidebar-example-title">Main content with a related sidebar.</h3>
          <div class="content-sidebar">
            <article class="card" aria-labelledby="main-content-example-title"><h4 id="main-content-example-title">Main article</h4><p>An article holds a self-contained piece of content. This one gets the wider Grid column.</p><p>The related aside follows it in HTML and stacks underneath on narrow screens.</p></article>
            <aside class="card" aria-labelledby="related-links-title"><h4 id="related-links-title">Related information</h4><p>Use aside for supporting content, wherever CSS positions it.</p><ul><li><a href="#basic-layout">Profile row</a></li><li><a href="#contact-form">Form controls</a></li></ul></aside>
          </div>
        </section>
        ${actions('signup', 'Try the form', 'features', 'Revisit components')}
      </div>
    </section>

    <!-- SECTION: form | Labelled form controls, grouped choices and native validation. -->
    <section class="section signup" id="signup" aria-labelledby="signup-title">
      <div class="container signup-layout">
        <div class="signup-intro"><p class="eyebrow">Forms / Labels &amp; controls</p><h2 id="signup-title">Try a few common form controls.</h2><p>Labels identify each field. Required fields and email format are checked by the browser before submission.</p><p id="basic-signup-note" role="status">Demo form: use sample details. No messages are sent. Submitting the exported page returns here.</p></div>
        <!-- Static GET demonstration only; a working enquiry service needs a backend. -->
        <form class="signup-form card" id="contact-form" action="#signup" method="get" aria-describedby="basic-signup-note">
          <div><label for="signup-name">Name (required)</label><input class="input" id="signup-name" name="name" autocomplete="name" required></div>
          <div><label for="signup-email">Email address (required)</label><input class="input" id="signup-email" name="email" type="email" autocomplete="email" aria-describedby="signup-email-help" required><small id="signup-email-help">Use a sample address, such as alex@example.com.</small></div>
          <div><label for="signup-topic">Choose a topic</label><select class="input" id="signup-topic" name="topic"><option value="">Choose a topic</option><option value="html">Semantic HTML</option><option value="flexbox">Flexbox</option><option value="grid">CSS Grid</option></select></div>
          <div><label for="signup-question">Your question</label><textarea class="input" id="signup-question" name="question" rows="3"></textarea></div>
          <fieldset class="choice-group" id="form-options"><legend>Learning preference</legend><label class="choice-label"><input type="radio" name="learning" value="self-paced" checked> At my own pace</label><label class="choice-label"><input type="radio" name="learning" value="group"> With a group</label></fieldset>
          <label class="checkbox-label"><input type="checkbox" name="updates" value="yes" required> I understand this is a demo (required).</label>
          <div class="section-actions"><button class="button ${DSStudio.samples.buttonClass()}" type="submit">Submit demo form</button>${action('lists', 'Back to layouts', 'secondary')}</div>
        </form>
      </div>
    </section>
  </main>

  <!-- SECTION: footer | Horizontal main navigation and sitemap columns with stacked child links. -->
  ${DSStudio.samples.footerHtml('basic')}
</body>
</html>
`);
  }

  function readableCss(css) {
    return css.replace(/^([^\n{}]+) \{ ([^{}\n]*) \}$/gm, (_, selector, declarations) =>
      selector + ' {\n  ' + declarations.split(/;\s*/).filter(Boolean).join(';\n  ') + ';\n}');
  }

  function basicCss() {
    return DSStudio.samples.foundationCss() + readableCss(`
/* SECTION: basics */
/* BASIC WEBSITE: the same system tokens and components as Advanced.
   Normal flow, Flexbox navigation and responsive Grid keep the markup simple. */
* { box-sizing: border-box; }
h1, h2, h3 { margin: 0 0 var(--space-4); font-weight: var(--heading-weight); line-height: var(--heading-leading); overflow-wrap: anywhere; }
h1 { font-size: var(--text-display); max-width: 17ch; }
h2 { font-size: var(--text-h1); }
h3 { font-size: var(--text-h2); }
p { margin: 0 0 var(--space-6); }
a { color: var(--primary); text-underline-offset: .2em; }
a:hover { text-decoration: underline; }
section, #top, #main-content { scroll-margin-top: var(--space-4); }
.section { padding-block: var(--space-8); }
.container, .card, .brand { overflow-wrap: anywhere; }
.skip-link { position: absolute; top: -10rem; left: var(--space-4); padding: var(--space-4); background: var(--surface); z-index: 1; }
.skip-link:focus { top: var(--space-4); }

/* SECTION: shared */
/* Shared text and action styles apply to several sections. */

.eyebrow { font-size: var(--text-small); font-weight: var(--heading-weight); letter-spacing: .08em; text-transform: uppercase; }
.intro { font-size: var(--text-h2); }
.button { max-width: 100%; overflow-wrap: anywhere; }
.section-actions { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-4); margin-top: var(--space-6); }
/* Flexible children can shrink without pushing the page wider. */
.hero-layout > *, .skills-layout > *, .signup-layout > *, .section-actions > *, .card { min-width: 0; }
.card > :last-child { margin-bottom: 0; }
/* Give navigation and card links a comfortable target size. */
.nav-list a, .skill-cards article > a, .content-sidebar a { display: inline-flex; align-items: center; min-height: 44px; }

/* SECTION: header */
/* Flexbox aligns the brand and desktop navigation. Native details controls the mobile menu. */
.site-header { border-bottom: var(--border-width) solid var(--border); background: var(--surface); }
.header-inner { position: relative; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-4); padding-block: var(--space-4); }
.brand { display: flex; align-items: center; gap: var(--space-2); min-width: 0; max-width: 100%; font-weight: var(--heading-weight); text-decoration: none; }
.brand > span:last-child { min-width: 0; }
.logo { display: grid; place-items: center; flex: 0 0 var(--space-12); min-height: var(--space-12); border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font-size: var(--text-small); }
nav { min-width: 0; max-width: 100%; }
.nav-list { display: flex; flex-wrap: wrap; gap: var(--space-2) var(--space-4); margin: 0; padding: 0; list-style: none; }
.basic-menu { display: none; }
.basic-menu summary { display: inline-flex; align-items: center; justify-content: center; gap: var(--space-2); min-width: 48px; min-height: 48px; padding: var(--space-2); color: var(--text); font-weight: var(--heading-weight); cursor: pointer; list-style: none; }
.basic-menu summary::-webkit-details-marker { display: none; }
.menu-icon { flex: none; color: var(--accent); }
.menu-close, .basic-menu[open] .menu-bars { display: none; }
.basic-menu[open] .menu-close { display: inline; }
.mobile-navigation { position: absolute; inset-inline: 0; top: 100%; z-index: 2; padding: var(--space-2); border: var(--border-width) solid var(--control-border); border-radius: var(--radius-base); background: var(--surface); }
.basic-menu:not([open]) .mobile-navigation { display: none; }
.mobile-navigation .nav-list { flex-direction: column; gap: 0; }
.mobile-navigation a { display: flex; padding: var(--space-2); min-height: 48px; }
.mobile-navigation a:hover { background: var(--surface-muted); }

/* SECTION: hero */
.hero { padding-block: var(--space-12); background: var(--surface-muted); }
.hero-layout { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--grid-gap); align-items: center; }
.hero-image { margin: 0; padding: var(--space-4); background: var(--surface); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); }
.hero-image figcaption { padding: var(--space-4) var(--space-2) 0; font-size: var(--text-small); color: var(--text-muted); }
.hero-image img { display: block; width: 100%; height: auto; border-radius: var(--radius-base); }
.hero-note { margin: var(--space-4) 0 0; font-size: var(--text-small); color: var(--text-muted); }
/* SECTION: skills */
/* FLEXBOX SECTION: a flexible introduction beside a vertical stack.
   No Grid layout is used in this section. */
.skills-layout { display: flex; gap: var(--grid-gap); align-items: flex-start; }
.skills-intro { flex: 5; padding-block: var(--space-6); }
.skill-cards { display: flex; flex: 7; flex-direction: column; gap: var(--grid-gap); align-items: var(--grid-align); }
.skill-cards > .card { width: 100%; }
.skill-cards .eyebrow { color: var(--text-muted); margin-bottom: var(--space-2); }
/* Common UI components use normal flow and Flexbox in this section. */
.component-demo { margin-block: var(--space-4); padding: var(--space-4); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); background: var(--surface-muted); }
.component-demo p { margin: 0 0 var(--space-2); }
.media-object { display: flex; align-items: flex-start; gap: var(--space-4); }
.avatar { display: flex; align-items: center; justify-content: center; flex: 0 0 var(--space-12); height: var(--space-12); border-radius: 50%; background: var(--primary); color: var(--on-primary); font-weight: var(--heading-weight); }
.media-copy { flex: 1; min-width: 0; }
.media-copy p { margin: var(--space-2) 0; }
.badge { display: inline-flex; max-width: 100%; padding: var(--space-1) var(--space-2); border-radius: var(--radius-base); background: var(--secondary); color: var(--on-secondary); font-size: var(--text-small); }
.faq-demo summary { cursor: pointer; min-height: 44px; align-content: center; font-weight: var(--heading-weight); }
.faq-demo p { margin: var(--space-2) 0 0; }
/* SECTION: toolkit */
/* GRID SECTION: auto-fit adds equal-width columns when the saved minimum fits. */
.toolkit { background: var(--surface-muted); border-block: var(--border-width) solid var(--border); }
.toolkit-heading { max-width: var(--reading-measure); }
.list-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-card-min)), 1fr)); gap: var(--grid-gap); align-items: var(--grid-align); margin-top: var(--space-8); }
.list-grid ul, .list-grid ol { margin: 0; padding-inline-start: var(--space-6); }
.list-grid li + li { margin-top: var(--space-2); }
.list-grid dl { margin: 0; }
.list-grid dt { font-weight: var(--heading-weight); }
.list-grid dd { margin: var(--space-1) 0 var(--space-4); }
.list-grid dd:last-child { margin-bottom: 0; }
.layout-example { margin-top: var(--space-8); }
.content-sidebar { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: var(--grid-gap); margin-block: var(--space-6); align-items: start; }
.content-sidebar h4 { margin: 0 0 var(--space-2); font-family: var(--font-heading); font-size: var(--text-body); font-weight: var(--heading-weight); line-height: var(--heading-leading); }
.content-sidebar ul { margin: 0; padding-inline-start: var(--space-4); }
/* SECTION: form */
.signup { background: var(--surface); }
.signup-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--grid-gap); justify-items: center; }
.signup-intro, .signup-form { width: 100%; max-width: var(--reading-measure); }
.signup-intro { text-align: center; }
.signup-intro > p { margin-inline: auto; }
.signup-form { display: grid; gap: var(--space-4); text-align: start; }
label { display: block; margin-bottom: var(--space-2); font-weight: var(--heading-weight); }
input, select, textarea { max-width: 100%; font: inherit; }
textarea { resize: vertical; }
.input { width: 100%; padding: var(--space-2) var(--space-4); border-radius: var(--radius-base); background: var(--surface); color: var(--text); }
small { display: block; margin-top: var(--space-1); font-size: var(--text-small); color: var(--text-muted); }
.choice-group { min-width: 0; margin: 0; padding: var(--space-4); border: var(--border-width) solid var(--control-border); border-radius: var(--radius-base); }
.choice-group legend { padding-inline: var(--space-2); font-weight: var(--heading-weight); }
.choice-label, .checkbox-label { display: flex; gap: var(--space-2); margin: 0; font-weight: 400; }
.choice-label { align-items: center; min-height: 44px; }
.checkbox-label { align-items: flex-start; }
.choice-label input, .checkbox-label input { flex: none; accent-color: var(--primary); }
.checkbox-label input { width: 1.25em; height: 1.25em; margin-top: .25em; }
/* SECTION: responsive */
/* Wider viewports add space; the final query stacks Hero and Skills. */
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .section { padding-block: var(--space-12); }
}
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().wide)}) {
  .container { padding-inline: var(--page-gutter-wide); }
  .section { padding-block: var(--space-16); }
  .hero { padding-block: var(--space-20); }
}
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .header-inner { flex-wrap: nowrap; }
  .site-header .brand { flex: 1; }
  .desktop-navigation { display: none; }
  .basic-menu { display: block; flex: none; }
  .hero-layout, .content-sidebar { grid-template-columns: minmax(0, 1fr); }
  .skills-layout { flex-direction: column; }
  .skills-intro { padding-block: 0; }
  .skills-intro, .skill-cards { flex: auto; width: 100%; }
}
` + '\n/* SECTION: footer */\n' + DSStudio.samples.footerCss());
  }

  DSStudio.samples.basicExcerpt = (code, language, section) => {
    const sections = ['basics', 'header', 'hero', 'skills', 'toolkit', 'form', 'footer'];
    if (!sections.includes(section)) return code;
    if (language === 'html') {
      const marker = `<!-- SECTION: ${section} |`;
      const start = code.indexOf(marker);
      if (start < 0) return code;
      const end = code.indexOf('<!-- SECTION:', start + marker.length);
      // Exclude page wrappers belonging to the complete document.
      return code.slice(start, end < 0 ? code.length : end)
        .replace(/\s*<\/?(?:html|body|main)\b[^>]*>/g, '').trim();
    }
    const chunks = code.split(/(?=\/\* SECTION: [a-z]+ \*\/)/);
    const selected = chunks.filter(chunk => {
      const name = chunk.match(/^\/\* SECTION: ([a-z]+) \*\//)?.[1];
      return [section, 'shared', 'responsive'].includes(name);
    });
    const spacing = section === 'basics' ?
      '/* Reusable spacing values: change the studio spacing unit to update these. */\n:root {\n' +
      (code.match(/^\s*--space-(?:unit|\d+):[^;\n]+;/gm) || []).map(line => '  ' + line.trim()).join('\n') + '\n}\n\n' : '';
    return '/* Study excerpt: requires the complete tokens.css for foundations and components. */\n' + spacing + selected.join('\n');
  };

  DSStudio.register({
    id: 'basic-homepage',
    title: 'Basic and Advanced website samples',
    init() {
      const advancedHtml = htmlExport, advancedCss = cssExport;
      htmlExport = () => state.sampleMode === 'basic' ? basicHtml() : advancedHtml();
      cssExport = () => state.sampleMode === 'basic' ? basicCss() : advancedCss();
      const tabs = ['dockModeAdvanced', 'dockModeBasic'];
      function sync() {
        const basic = state.sampleMode === 'basic';
        tabs.forEach((id, index) => {
          const selected = basic === (index === 1), tab = document.getElementById(id);
          tab.setAttribute('aria-selected', String(selected)); tab.tabIndex = selected ? 0 : -1;
        });
        document.getElementById('dockSamplePanel').setAttribute('aria-labelledby', tabs[basic ? 1 : 0]);
        document.getElementById('sampleModeHelp').textContent = basic ? 'Basic: essential UI components in a compact page. Responsive header/hero, cards, profile row, FAQ, Grid/lists, article/aside, native form controls and grouped footer navigation. Uses your shared typography, spacing, colours, components, buttons and responsive settings.' : 'Advanced: the full field guide, planning workshops and component/state gallery.';
      }
      tabs.forEach((id, index) => {
        const tab = document.getElementById(id);
        tab.addEventListener('click', () => { state.sampleMode = index === 1 ? 'basic' : 'advanced'; apply(); });
        tab.addEventListener('keydown', event => {
          let next;
          if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') next = 1 - index;
          else if (event.key === 'Home') next = 0;
          else if (event.key === 'End') next = 1;
          else return;
          event.preventDefault(); document.getElementById(tabs[next]).click(); document.getElementById(tabs[next]).focus();
        });
      });
      const previousRender = renderCode;
      renderCode = function() { sync(); previousRender(); };
      renderCode();
    }
  });
})();
