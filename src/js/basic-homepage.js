'use strict';
/* A deliberately small teaching page. Advanced retains its existing generators;
   both modes share the project foundations, preview and paired file actions. */
(() => {
  function basicHtml() {
    const project = escapeHtml(state.project);
    return `<!doctype html>
<html lang="en" data-theme="${state.theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="${project}: a simple responsive website demonstrating semantic HTML, CSS Grid and a static sign-up form.">
  <title>${project} | A simple place to begin</title>
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
          <li><a href="#lists">Lists</a></li>
          <li><a href="#signup">Sign up</a></li>
        </ul>
      </nav>
    </div>
  </header>

  <main id="main-content" tabindex="-1">
    <!-- One page heading introduces the main idea and next action. -->
    <section class="hero" id="home" aria-labelledby="hero-title">
      <div class="container">
        <p class="eyebrow">Small steps. Useful skills.</p>
        <h1 id="hero-title">Start small. Build something useful.</h1>
        <p class="intro">Learn how clear content, thoughtful layout and a few shared styles can turn a simple page into a welcoming website.</p>
        <a class="button ${DSStudio.samples.buttonClass()}" href="#features">Explore the essentials</a>
      </div>
    </section>

    <!-- Grid creates columns when space allows and fewer columns when needed. -->
    <section class="section container" id="features" aria-labelledby="features-title">
      <h2 id="features-title">Three essentials for your next website</h2>
      <p>Begin with these foundations, then practise by making one small change at a time.</p>
      <div class="feature-grid">
        <article class="card" id="basic-structure"><p class="eyebrow">01 / Structure</p><h3>Give content meaning</h3><p>Use headings, sections and navigation to help people understand the page and find their next step.</p></article>
        <article class="card" id="basic-layout"><p class="eyebrow">02 / Layout</p><h3>Let the layout adapt</h3><p>CSS Grid gives these cards a shared structure. Resize the page to see columns respond to the available space.</p></article>
        <article class="card" id="basic-usability"><p class="eyebrow">03 / Usability</p><h3>Make the basics easy</h3><p>Write useful labels, keep text readable and provide visible keyboard focus. Review your page at narrow and wide widths.</p></article>
      </div>
    </section>

    <!-- Lists communicate groups, sequences and term/description relationships. -->
    <section class="section container" id="lists" aria-labelledby="lists-title">
      <h2 id="lists-title">Choose the right list for the content</h2>
      <p>Use an unordered list for a collection, an ordered list for a sequence, and a description list for terms and explanations.</p>
      <div class="list-grid">
        <article class="card" id="list-collection"><h3>What to include</h3><ul><li>A clear page heading</li><li>Useful navigation labels</li><li>Readable text and visible focus</li></ul></article>
        <article class="card" id="list-workflow"><h3>A simple workflow</h3><ol><li>Write a short project brief.</li><li>Group the content in a sitemap.</li><li>Sketch, build and test the page.</li></ol></article>
        <article class="card" id="list-terms"><h3>Useful terms</h3><dl><dt>HTML</dt><dd>Describes the meaning and structure of content.</dd><dt>CSS</dt><dd>Controls presentation and responsive layout.</dd><dt>Sitemap</dt><dd>Shows how pages and content groups relate.</dd></dl></article>
      </div>
    </section>

    <section class="section signup" id="signup" aria-labelledby="signup-title">
      <div class="container signup-layout">
        <div><p class="eyebrow">Keep learning</p><h2 id="signup-title">Make room for your next idea.</h2><p>Practise a short sign-up form with clear labels and native browser validation.</p><p id="basic-signup-note">Static demo: use sample details. No account is created. Submitting the exported page returns to this page.</p></div>
        <!-- A real sign-up service would supply the form action and processing. -->
        <form class="signup-form card" action="#signup" method="get" aria-describedby="basic-signup-note">
          <div><label for="signup-name">Name</label><input class="input" id="signup-name" name="name" autocomplete="name" required></div>
          <div><label for="signup-email">Email address</label><input class="input" id="signup-email" name="email" type="email" autocomplete="email" aria-describedby="signup-email-help" required><small id="signup-email-help">For example, alex@example.com. Use a sample address in this demo.</small></div>
          <label class="checkbox-label"><input type="checkbox" name="updates" value="yes" required> I would like to receive learning updates (demo).</label>
          <button class="button ${DSStudio.samples.buttonClass()}" type="submit">Try signing up</button>
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
.eyebrow { font-size: var(--text-small); font-weight: var(--heading-weight); letter-spacing: .08em; text-transform: uppercase; }
.intro { font-size: var(--text-h2); }
.button { max-width: 100%; overflow-wrap: anywhere; }

/* Grid uses the saved minimum card width, gap and alignment. */
.feature-grid, .list-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-card-min)), 1fr)); gap: var(--grid-gap); align-items: var(--grid-align); margin-top: var(--space-8); }
.card { min-width: 0; }
.card > :last-child { margin-bottom: 0; }
.list-grid ul, .list-grid ol { margin: 0; padding-inline-start: var(--space-6); }
.list-grid li + li { margin-top: var(--space-2); }
.list-grid dl { margin: 0; }
.list-grid dt { font-weight: var(--heading-weight); }
.list-grid dd { margin: var(--space-1) 0 var(--space-4); }
.list-grid dd:last-child { margin-bottom: 0; }
.signup { background: var(--surface-muted); }
.signup-layout { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: var(--grid-gap); align-items: start; }
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
  .signup-layout { grid-template-columns: minmax(0, 1fr); }
}
` + DSStudio.samples.footerCss();
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
        document.getElementById('sampleModeHelp').textContent = basic ? 'Basic: header, hero, Grid cards, three list types, static sign-up and footer sitemap. Uses your shared typography, spacing, colours, components, buttons and responsive settings.' : 'Advanced: the full field guide, planning workshops and component/state gallery.';
        document.getElementById('websiteSampleDescription').textContent = basic ? 'Basic static homepage: logo and navigation, hero, responsive Grid cards, three list examples, static sign-up form and footer sitemap with Back to top.' : 'Advanced static homepage: header and mobile menu, hero, images, cards, Grid/Flexbox layouts, forms, table, FAQs, component states and footer.';
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
