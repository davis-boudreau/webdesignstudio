'use strict';
/* A deliberately small teaching page. Advanced retains its existing generators;
   both modes share the project foundations, preview and paired file actions. */
(() => {
  function basicHtml() {
    const project = escapeHtml(state.project);
    const action = (href, label, variant = 'primary') => `<a class="button ${DSStudio.samples.buttonClass(variant)}" href="#${href}">${label}</a>`;
    const actions = (href, label, secondaryHref, secondaryLabel) => `<div class="section-actions">${action(href, label)}${action(secondaryHref, secondaryLabel, 'secondary')}</div>`;
    return `<!doctype html>
<html lang="en" data-theme="${state.theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${project}: a beginner-friendly website workshop with practical skills, a project toolkit and a sample sign-up form.">
  <title>${project} | Build your first website</title>
${DSStudio.fonts.htmlLinks()}  <link rel="stylesheet" href="tokens.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>

  <!-- A visible, wrapping navigation works at every width without JavaScript. -->
  <header class="site-header" id="top" tabindex="-1">
    <div class="container header-inner">
      <a class="brand" href="#top"><span class="logo" aria-hidden="true">Logo</span><span>${project}</span></a>
      <nav aria-label="Main navigation">
        <ul class="nav-list">
          <li><a href="#home">Home</a></li>
          <li><a href="#features">What you can learn</a></li>
          <li><a href="#lists">Project toolkit</a></li>
          <li><a href="#signup">Sign up</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main-content" tabindex="-1">
    <!-- One page heading introduces the main idea and next action. -->
    <section class="hero" id="home" aria-labelledby="hero-title">
      <div class="container hero-layout">
        <div>
          <p class="eyebrow">Your first website starts here.</p>
          <h1 id="hero-title">Turn your idea into a website.</h1>
          <p class="intro">Have an idea for a club, a portfolio or a small business? Work through the essentials and leave with a clear plan for your first page. No previous coding experience needed.</p>
          ${actions('signup', 'Plan my first website', 'features', 'Explore what you can learn')}
          <p class="hero-note">Start with one page. Build at your own pace. Keep a checklist for your next step.</p>
        </div>
        <figure class="hero-image">
          <img src="${DSStudio.samples.illustration(palette().roles)}" width="960" height="720" alt="A browser wireframe with a header, a two-column hero, lesson cards and palette-coloured layout blocks.">
          <figcaption><span class="hero-caption-number" aria-hidden="true">01 /</span> Your idea, with room to grow.</figcaption>
        </figure>
      </div>
    </section>

    <!-- An editorial introduction sits beside a numbered lesson sequence. -->
    <section class="section container" id="features" aria-labelledby="features-title">
      <div class="skills-layout">
        <div class="skills-intro">
          <p class="eyebrow">The essentials / 3 useful skills</p>
          <h2 id="features-title">From a blank page to a clear next step</h2>
          <p>Focus on three practical skills. Try each one on a real idea, then use the toolkit below to bring your page together.</p>
          ${actions('lists', 'Get the project toolkit', 'signup', 'Choose my next step')}
        </div>
        <div class="feature-grid">
          <article class="card" id="basic-structure"><p class="eyebrow"><span aria-hidden="true">01 / </span>Structure</p><h3>Give content meaning</h3><p>Decide who your page is for and what they need to do. Turn that goal into a useful heading and a short content checklist.</p><a href="#list-collection">Find your starting checklist &rarr;</a></article>
          <article class="card" id="basic-layout"><p class="eyebrow"><span aria-hidden="true">02 / </span>Layout</p><h3>Let the layout adapt</h3><p>Arrange your content so it stays easy to follow on a phone or a larger screen. Build one section at a time and check the reading order.</p><a href="#list-workflow">Follow the three-step workflow &rarr;</a></article>
          <article class="card" id="basic-usability"><p class="eyebrow"><span aria-hidden="true">03 / </span>Usability</p><h3>Make the basics easy</h3><p>Give links clear names, make text comfortable to read and test with a keyboard. Small checks make your page easier to use.</p><a href="#list-terms">Get comfortable with the terms &rarr;</a></article>
        </div>
      </div>
    </section>

    <!-- Lists communicate groups, sequences and term/description relationships. -->
    <section class="section toolkit" id="lists" aria-labelledby="lists-title">
      <div class="container">
      <div class="toolkit-heading"><p class="eyebrow">Keep this close</p>
      <h2 id="lists-title">A small toolkit. A manageable first project.</h2>
      <p>Keep these notes beside you as you work. You do not need a complete website today: choose one useful page, gather its content and test a first version.</p></div>
      <div class="list-grid">
        <article class="card" id="list-collection"><p class="eyebrow">Your starting checklist</p><h3>What to include</h3><ul><li>One audience and a clear page goal</li><li>A heading, helpful copy and a next action</li><li>Readable text, useful labels and visible focus</li></ul><p class="toolkit-note">Keep it small: one audience, one page, one useful next action.</p></article>
        <article class="card" id="list-workflow"><h3>A simple workflow</h3><ol><li>Write a short project brief.</li><li>Group the content in a sitemap.</li><li>Sketch, build and test the page.</li></ol></article>
        <article class="card" id="list-terms"><h3>Useful terms</h3><dl><dt>HTML</dt><dd>Describes the meaning and structure of content.</dd><dt>CSS</dt><dd>Controls presentation and responsive layout.</dd><dt>Sitemap</dt><dd>Shows how pages and content groups relate.</dd></dl></article>
      </div>
      ${actions('signup', 'Put my plan into practice', 'features', 'Revisit the three essentials')}
      </div>
    </section>

    <section class="section signup" id="signup" aria-labelledby="signup-title">
      <div class="container signup-layout">
        <div class="signup-intro"><p class="eyebrow">Take the next step</p><h2 id="signup-title">Give your first page a starting point.</h2><p>Ready to practise? Try the workshop sign-up below, then use the toolkit to outline a page for your own idea.</p><p>You will work towards a short brief, a content checklist and a first layout to test.</p><p id="basic-signup-note" role="status">Static demo: use sample details. No account is created. Submitting the exported page returns to this page.</p></div>
        <!-- A real sign-up service would supply the form action and processing. -->
        <form class="signup-form card" action="#signup" method="get" aria-describedby="basic-signup-note">
          <div><label for="signup-name">Name</label><input class="input" id="signup-name" name="name" autocomplete="name" required></div>
          <div><label for="signup-email">Email address</label><input class="input" id="signup-email" name="email" type="email" autocomplete="email" aria-describedby="signup-email-help" required><small id="signup-email-help">For example, alex@example.com. Use a sample address in this demo.</small></div>
          <label class="checkbox-label"><input type="checkbox" name="updates" value="yes" required> I would like to receive learning updates (demo).</label>
          <div class="section-actions">
            <button class="button ${DSStudio.samples.buttonClass()}" type="submit">Try the workshop sign-up</button>
            ${action('lists', 'Review the toolkit first', 'secondary')}
          </div>
        </form>
      </div>
    </section>
  </main>

  ${DSStudio.samples.footerHtml('basic')}
</body>
</html>
`;
  }

  function basicCss() {
    return DSStudio.samples.foundationCss() + `
/* BASIC WEBSITE: the same system tokens and components as Advanced.
   Normal flow, Flexbox navigation and responsive Grid keep the markup simple. */
* { box-sizing: border-box; }
h1, h2, h3 { font-weight: var(--heading-weight); line-height: var(--heading-leading); }
h1 { font-size: var(--text-display); max-width: 17ch; }
h2 { font-size: var(--text-h1); }
h3 { font-size: var(--text-h2); }
h1, h2, h3 { margin: 0 0 var(--space-4); overflow-wrap: anywhere; }
p { margin: 0 0 var(--space-6); }
a { color: var(--primary); text-underline-offset: .2em; }
a:hover { text-decoration: underline; }
section, #top, #main-content { scroll-margin-top: var(--space-4); }
.section { padding-block: var(--space-8); }
.container, .card, .brand { overflow-wrap: anywhere; }
.skip-link { position: absolute; top: -10rem; left: var(--space-4); padding: var(--space-4); background: var(--surface); z-index: 1; }
.skip-link:focus { top: var(--space-4); }

/* Flexbox lets navigation wrap while keeping the source order. */
.site-header { border-bottom: var(--border-width) solid var(--border); background: var(--surface); }
.header-inner { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: var(--space-4); padding-block: var(--space-4); }
.brand { display: flex; align-items: center; gap: var(--space-2); min-width: 0; max-width: 100%; font-weight: var(--heading-weight); text-decoration: none; }
.brand > span:last-child { min-width: 0; }
.logo { display: grid; place-items: center; flex: 0 0 var(--space-12); min-height: var(--space-12); border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font-size: var(--text-small); }
nav { min-width: 0; max-width: 100%; }
.nav-list { display: flex; flex-wrap: wrap; gap: var(--space-2) var(--space-4); margin: 0; padding: 0; list-style: none; }
.nav-list a { display: inline-flex; align-items: center; min-height: 44px; }
.hero { padding-block: var(--space-12); background: var(--surface-muted); }
.hero-layout { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--grid-gap); align-items: center; }
.hero-layout > * { min-width: 0; }
.hero-image { margin: 0; padding: var(--space-4); background: var(--surface); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); }
.hero-image figcaption { display: flex; align-items: center; gap: var(--space-4); padding: var(--space-4) var(--space-2) 0; font-size: var(--text-small); color: var(--text-muted); }
.hero-caption-number { color: var(--primary); font-weight: var(--heading-weight); }
.hero-image img { display: block; width: 100%; height: auto; border-radius: var(--radius-base); }
.eyebrow { font-size: var(--text-small); font-weight: var(--heading-weight); letter-spacing: .08em; text-transform: uppercase; }
.intro { font-size: var(--text-h2); }
.button { max-width: 100%; overflow-wrap: anywhere; }
.section-actions { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-4); margin-top: var(--space-6); }
.section-actions > * { min-width: 0; }
.hero-note { margin: var(--space-4) 0 0; font-size: var(--text-small); color: var(--text-muted); }

/* Distinct compositions share the saved grid gap and card alignment.
   The toolkit's two tracks also respect the saved minimum card width. */
.skills-layout { display: grid; grid-template-columns: minmax(0, 5fr) minmax(0, 7fr); gap: var(--grid-gap); align-items: start; }
.skills-layout > * { min-width: 0; }
.skills-intro { padding-block: var(--space-6); }
.feature-grid { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--grid-gap); align-items: var(--grid-align); }
.feature-grid .eyebrow::before { content: ""; display: inline-block; width: var(--space-2); height: var(--space-2); margin-inline-end: var(--space-2); border-radius: var(--radius-base); background: var(--primary); }
.feature-grid .eyebrow { color: var(--text-muted); margin-bottom: var(--space-2); }
.toolkit { background: var(--surface-muted); border-block: var(--border-width) solid var(--border); }
.toolkit-heading { max-width: var(--reading-measure); }
.list-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, max(var(--grid-card-min), calc((100% - var(--grid-gap)) / 2))), 1fr)); gap: var(--grid-gap); align-items: var(--grid-align); margin-top: var(--space-8); }
.list-grid > :first-child { grid-row: span 2; display: flex; flex-direction: column; }
.toolkit-note { border-top: var(--border-width) solid var(--border); padding-top: var(--space-6); margin-top: auto; color: var(--text-muted); }
.card { min-width: 0; }
.card > :last-child { margin-bottom: 0; }
.feature-grid article > a { display: inline-flex; align-items: center; min-height: 44px; }
.list-grid ul, .list-grid ol { margin: 0; padding-inline-start: var(--space-6); }
.list-grid li + li { margin-top: var(--space-2); }
.list-grid dl { margin: 0; }
.list-grid dt { font-weight: var(--heading-weight); }
.list-grid dd { margin: var(--space-1) 0 var(--space-4); }
.list-grid dd:last-child { margin-bottom: 0; }
.signup { background: var(--surface); }
.signup-layout { display: grid; grid-template-columns: minmax(0, 1fr); gap: var(--grid-gap); justify-items: center; }
.signup-intro { max-width: var(--reading-measure); text-align: center; }
.signup-intro > p { margin-inline: auto; }
.signup-form { width: 100%; max-width: var(--reading-measure); text-align: start; }
.signup-layout > * { min-width: 0; }
.signup-form { display: grid; gap: var(--space-4); }
label { display: block; margin-bottom: var(--space-2); font-weight: var(--heading-weight); }
input { max-width: 100%; font: inherit; }
.input { width: 100%; padding: var(--space-2) var(--space-4); border-radius: var(--radius-base); background: var(--surface); color: var(--text); }
small { display: block; margin-top: var(--space-1); font-size: var(--text-small); color: var(--text-muted); }
.checkbox-label { display: flex; align-items: flex-start; gap: var(--space-2); margin: 0; font-weight: 400; }
.checkbox-label input { flex: none; width: 1.25em; height: 1.25em; margin-top: .25em; accent-color: var(--primary); }
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .section { padding-block: var(--space-12); }
}
@media (min-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().wide)}) {
  .container { padding-inline: var(--page-gutter-wide); }
  .section { padding-block: var(--space-16); }
  .hero { padding-block: var(--space-20); }
}
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .header-inner { align-items: flex-start; flex-direction: column; }
  .hero-layout, .skills-layout { grid-template-columns: minmax(0, 1fr); }
  .skills-intro { padding-block: 0; }
}
` + DSStudio.samples.footerCss() + basicFooterCss();
  }

  function basicFooterCss() {
    return `/* BASIC FOOTER: identity, a short route map and a suggested next step. */
.site-footer { border-top: var(--space-1) solid var(--primary); }
.site-footer .footer-inner { grid-template-columns: minmax(0, 2fr) minmax(0, 1fr) minmax(0, 1fr); }
.site-footer .footer-brand { gap: var(--space-4); text-decoration: none; }
.site-footer .footer-links { display: grid; gap: 0; }
.site-footer .footer-next { border-inline-start: var(--border-width) solid var(--border); padding-inline-start: var(--space-6); }
.site-footer .footer-next p { margin-block: var(--space-2); }
.site-footer .footer-next a { display: inline-flex; align-items: center; min-height: 44px; font-weight: var(--heading-weight); }
.site-footer .sitemap { background: var(--surface-muted); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); padding: var(--space-2) var(--space-4); margin-bottom: var(--space-6); }
.site-footer .footer-sitemap-hint { display: inline; margin-inline-start: var(--space-2); }
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .site-footer .footer-inner { grid-template-columns: minmax(0, 1fr); }
  .site-footer .footer-links { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0 var(--space-4); }
  .site-footer .footer-next { border-inline-start: 0; border-top: var(--border-width) solid var(--border); padding-inline-start: 0; padding-top: var(--space-4); }
  .site-footer .footer-sitemap-hint { display: block; }
}
`;
  }

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
        document.getElementById('sampleModeHelp').textContent = basic ? 'Basic: illustrated hero, stacked skill lessons, asymmetric project toolkit, centred demo sign-up and a three-part footer with sitemap. Uses your shared typography, spacing, colours, components, buttons and responsive settings.' : 'Advanced: the full field guide, planning workshops and component/state gallery.';
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
