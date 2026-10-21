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
        <a class="button" href="#features">Explore the essentials</a>
      </div>
    </section>

    <!-- Grid creates columns when space allows and fewer columns when needed. -->
    <section class="section container" id="features" aria-labelledby="features-title">
      <h2 id="features-title">Three essentials for your next website</h2>
      <p>Begin with these foundations, then practise by making one small change at a time.</p>
      <div class="feature-grid">
        <article class="card"><p class="eyebrow">01 / Structure</p><h3>Give content meaning</h3><p>Use headings, sections and navigation to help people understand the page and find their next step.</p></article>
        <article class="card"><p class="eyebrow">02 / Layout</p><h3>Let the layout adapt</h3><p>CSS Grid gives these cards a shared structure. Resize the page to see columns respond to the available space.</p></article>
        <article class="card"><p class="eyebrow">03 / Usability</p><h3>Make the basics easy</h3><p>Write useful labels, keep text readable and provide visible keyboard focus. Review your page at narrow and wide widths.</p></article>
      </div>
    </section>

    <section class="section signup" id="signup" aria-labelledby="signup-title">
      <div class="container signup-layout">
        <div><p class="eyebrow">Keep learning</p><h2 id="signup-title">Make room for your next idea.</h2><p>Practise a short sign-up form with clear labels and native browser validation.</p><p id="basic-signup-note">Static demo: use sample details. No account is created. Submitting the exported page returns to this page.</p></div>
        <!-- A real sign-up service would supply the form action and processing. -->
        <form class="signup-form" action="#signup" method="get" aria-describedby="basic-signup-note">
          <div><label for="signup-name">Name</label><input id="signup-name" name="name" autocomplete="name" required></div>
          <div><label for="signup-email">Email address</label><input id="signup-email" name="email" type="email" autocomplete="email" aria-describedby="signup-email-help" required><small id="signup-email-help">For example, alex@example.com. Use a sample address in this demo.</small></div>
          <label class="checkbox-label"><input type="checkbox" name="updates" value="yes" required> I would like to receive learning updates (demo).</label>
          <button class="button" type="submit">Try signing up</button>
        </form>
      </div>
    </section>
  </main>

  <footer class="site-footer">
    <div class="container footer-inner">
      <p><strong>${project}</strong><br>A small website with a clear purpose.</p>
      <nav aria-label="Footer navigation"><ul class="nav-list"><li><a href="#home">Home</a></li><li><a href="#features">What you can learn</a></li><li><a href="#signup">Sign up</a></li></ul></nav>
      <a class="back-to-top" href="#top">Back to top &uarr;</a>
    </div>
  </footer>
</body>
</html>
`;
  }

  function basicCss() {
    const fonts = DSStudio.fonts.resolve();
    const roleNames = ['background','surface','surface-muted','text','text-muted','border','control-border','primary','primary-hover','on-primary','focus'];
    const roles = theme => {
      const values = palette(theme).roles;
      return roleNames.map(name => `  --${name}: ${values[name]};`).join('\n');
    };
    return `/* BASIC WEBSITE: save as tokens.css beside index.html.
   1. Shared design values. 2. Page foundations. 3. Layout and components.
   The optional Google font links live in the HTML. No JavaScript is required. */
:root {
  --font-body: ${fonts.body};
  --font-heading: ${fonts.heading};
  --text-body: ${state.base}px;
  --text-h1: ${fluidTypeCss(4)};
  --text-h2: ${fluidTypeCss(3)};
  --body-leading: ${state.leading};
  --heading-leading: ${state.headingLeading};
  --heading-weight: ${adv.weight};
  --heading-letter-spacing: ${state.headingTracking}em;
  --body-letter-spacing: ${state.bodyTracking}em;
  --radius-base: ${state.radius}px;
  --grid-gap: ${adv.gap}px;
  --grid-card-min: ${adv.columns}px;
  --focus-width: ${adv.focus}px;
${roles('light')}
}
[data-theme="dark"] {
  color-scheme: dark;
${roles('dark')}
}

/* Page foundations: include padding in widths and let long text wrap. */
* { box-sizing: border-box; }
body { margin: 0; font: var(--text-body)/var(--body-leading) var(--font-body); letter-spacing: var(--body-letter-spacing); color: var(--text); background: var(--background); }
h1, h2, h3 { font-family: var(--font-heading); font-weight: var(--heading-weight); line-height: var(--heading-leading); letter-spacing: var(--heading-letter-spacing); }
h1 { font-size: var(--text-h1); max-width: 17ch; }
h2 { font-size: var(--text-h2); }
h3 { font-size: 1.25rem; }
h1, h2, h3, p { margin-top: 0; }
p { max-width: 65ch; }
a { color: var(--primary); text-underline-offset: .2em; }
a:hover { text-decoration-thickness: .15em; }
:focus-visible { outline: var(--focus-width) solid var(--focus); outline-offset: 4px; }
section, #top, #main-content { scroll-margin-top: 1rem; }
.container { width: min(100%, 72rem); margin-inline: auto; padding-inline: 1rem; }
.section { padding-block: clamp(2.5rem, 6vw, 5rem); }
.container, .card, .brand { overflow-wrap: anywhere; }
.skip-link { position: absolute; top: -10rem; left: 1rem; padding: 1rem; background: var(--surface); z-index: 1; }
.skip-link:focus { top: 1rem; }

/* Flexbox aligns the logo and navigation; links wrap instead of overflowing. */
.site-header { border-bottom: 1px solid var(--border); background: var(--surface); }
.header-inner, .footer-inner { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 1.5rem; padding-block: 1.5rem; }
.brand { display: flex; align-items: center; gap: .75rem; min-width: 0; max-width: 100%; font-weight: 700; text-decoration: none; }
.brand > span:last-child { min-width: 0; }
.logo { display: grid; place-items: center; flex: 0 0 3rem; min-height: 3rem; border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font-size: .75rem; }
nav { min-width: 0; max-width: 100%; }
.nav-list { display: flex; flex-wrap: wrap; gap: .5rem 1rem; margin: 0; padding: 0; list-style: none; }
.nav-list a, .back-to-top { display: inline-flex; align-items: center; min-height: 44px; }
.hero { padding-block: clamp(3rem, 8vw, 7rem); background: var(--surface-muted); }
.eyebrow { font-size: .8rem; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.intro { max-width: 50ch; font-size: 1.2rem; }
.button { display: inline-flex; align-items: center; justify-content: center; min-height: 48px; max-width: 100%; padding: .75rem 1.25rem; border: 1px solid transparent; border-radius: var(--radius-base); background: var(--primary); color: var(--on-primary); font: inherit; font-weight: 700; text-decoration: none; text-align: center; cursor: pointer; overflow-wrap: anywhere; }
.button:hover { background: var(--primary-hover); }

/* Grid fits as many cards as possible, even when only one column will fit. */
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-card-min)), 1fr)); gap: var(--grid-gap); margin-top: 2rem; }
.card { min-width: 0; padding: 1.5rem; border: 1px solid var(--border); border-radius: var(--radius-base); background: var(--surface); }
.card > :last-child { margin-bottom: 0; }
.signup { background: var(--surface-muted); }
.signup-layout { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 2rem; align-items: start; }
.signup-layout > * { min-width: 0; }
.signup-form { display: grid; gap: 1.25rem; padding: 1.5rem; border: 1px solid var(--border); border-radius: var(--radius-base); background: var(--surface); }
label { display: block; margin-bottom: .5rem; font-weight: 700; }
input { max-width: 100%; font: inherit; }
input:not([type="checkbox"]) { width: 100%; min-height: 48px; padding: .75rem; border: 1px solid var(--control-border); border-radius: var(--radius-base); background: var(--surface); color: var(--text); }
small { display: block; margin-top: .5rem; color: var(--text-muted); }
.checkbox-label { display: flex; align-items: flex-start; gap: .75rem; margin: 0; font-weight: 400; }
.checkbox-label input { flex: none; width: 1.25rem; height: 1.25rem; margin-top: .25rem; }
.site-footer { border-top: 1px solid var(--border); background: var(--surface); }
.site-footer p { margin-bottom: 0; }

/* A narrow viewport keeps the source reading order and a single form column. */
@media (max-width: 48rem) {
  .header-inner { align-items: flex-start; flex-direction: column; }
  .signup-layout { grid-template-columns: minmax(0, 1fr); }
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
        document.getElementById('sampleModeHelp').textContent = basic ? 'Basic: header, hero, Grid cards, static sign-up and footer. Uses foundation colours, fonts and layout settings.' : 'Advanced: the full field guide, planning workshops and component/state gallery.';
        document.getElementById('websiteSampleDescription').textContent = basic ? 'Basic static homepage: logo and navigation, hero, responsive Grid cards, static sign-up form and footer with Back to top.' : 'Advanced static homepage: header and mobile menu, hero, images, cards, Grid/Flexbox layouts, forms, table, FAQs, component states and footer.';
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
