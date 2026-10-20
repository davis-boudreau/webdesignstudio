'use strict';
/* A static, self-contained HTML specimen using the same exports as the studio.
   Embedded SVG images follow the selected theme and palette without network calls. */
(() => {
  // A bounded cache avoids repeatedly encoding unchanged SVGs during live edits.
  const illustrations = new Map();
  function illustration(r, detail = false) {
    const key = JSON.stringify([detail, r.primary, r.secondary, r.accent, r.surface, r['surface-muted'], r.text]);
    if (illustrations.has(key)) return illustrations.get(key);
    const scene = detail ? `
  <rect x="140" y="150" width="480" height="350" rx="28" fill="${r.primary}"/>
  <circle cx="620" cy="260" r="150" fill="${r.accent}"/>
  <path d="M140 500L380 240L620 500Z" fill="${r.secondary}"/>
  <rect x="230" y="530" width="570" height="24" rx="12" fill="${r.text}" opacity=".15"/>` : `
  <circle cx="720" cy="190" r="115" fill="${r.accent}"/>
  <path d="M0 480Q210 310 490 455T960 400V720H0Z" fill="${r.secondary}"/>
  <path d="M250 550V270A170 170 0 0 1 590 270V550Z" fill="${r.surface}"/>
  <path d="M310 550V290A110 110 0 0 1 530 290V550Z" fill="${r.primary}"/>
  <path d="M0 610Q300 475 570 570T960 520V720H0Z" fill="${r.primary}"/>
  <path d="M365 720Q590 590 420 455" fill="none" stroke="${r.accent}" stroke-width="65"/>
  <path d="M790 510V345M790 400L745 365M790 440L840 395" fill="none" stroke="${r.text}" stroke-width="13" stroke-linecap="round"/>`;
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
    const size = ['sm', 'lg'].includes(settings.size) ? ` ds-button--${settings.size}` : '';
    const full = settings.mobileFull ? ' ds-button--mobile-full' : '';
    const buttonClass = variant => `ds-button ds-button--${variant}${size}${full}`;
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
      adv.state === 'success' ? 'Your email address looks good.' : 'We will only use your email to reply to your enquiry.';
    const headerLinks = [['home', 'Home'], ['about', 'About'], ['services', 'Services'], ['resources', 'Resources'], ['contact', 'Contact']]
      .map(([id, label]) => `          <li><a href="#${id}">${label}</a></li>`).join('\n');
    return `<!doctype html>
<html lang="en" data-theme="${state.theme}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="A welcoming home page for ${project}.">
  <title>${project} — Home</title>
${DSStudio.fonts.htmlLinks()}  <!-- Save the exported CSS alongside this file. -->
  <link rel="stylesheet" href="tokens.css">
</head>
<body class="sample-home">
  <a class="sample-skip" href="#main-content">Skip to main content</a>
  <header class="sample-header">
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
        <p class="sample-eyebrow">Welcome to ${project}</p>
        <h1 id="hero-title" class="page-title">Make room for your next big idea.</h1>
        <p class="sample-lead">Thoughtful services, useful resources and a team that cares. Let’s turn what comes next into something worth sharing.</p>
        <div class="button-row sample-section-actions">
          <a class="${buttonClass('primary')}" href="#services">Explore our services</a>
          <a class="${buttonClass('secondary')}" href="#contact">Let’s talk <span aria-hidden="true">↗</span></a>
        </div>
        <dl class="sample-stats">
          <div><dt>People first</dt><dd>Every step of the way</dd></div>
          <div><dt>Built together</dt><dd>From idea to impact</dd></div>
        </dl>
      </div>
      <figure class="sample-hero-image">
        <img src="${illustration(roles)}" width="960" height="720" alt="An open archway and a winding path through a colourful landscape.">
        <figcaption>A new perspective starts with an open door.</figcaption>
      </figure>
    </section>
    <section id="about" class="sample-section sample-grid sample-split" aria-labelledby="about-title">
      <figure class="sample-about-image">
        <img src="${illustration(roles, true)}" width="960" height="720" loading="lazy" alt="A circle, triangle and rectangle arranged as a balanced composition.">
        <figcaption>Different strengths. One shared direction.</figcaption>
      </figure>
      <div>
        <p class="sample-eyebrow">A little about us</p>
        <h2 id="about-title" class="heading-1">Good work begins with good connections.</h2>
        <p>We bring curiosity, care and clear thinking to every project. Your goals shape the journey; our experience helps you find a way forward.</p>
        <blockquote><p>“The best results happen when everyone has a place at the table.”</p><cite>The ${project} team</cite></blockquote>
${sectionActions(['#services', 'Explore our services'], ['#contact', 'Start a conversation'], '        ')}
      </div>
    </section>
    <section id="services" class="sample-section" aria-labelledby="services-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">What we do</p><h2 id="services-title" class="heading-1">Support for every next step.</h2><p>Start with a question. Leave with a clear direction.</p></div>
      <div class="sample-grid card-grid">
        <article class="card"><span class="sample-badge">Discover</span><h3 class="heading-2">Strategy &amp; direction</h3><p>Find the opportunity, focus your priorities and build a plan that fits.</p><ul><li>Research and discovery</li><li>Practical roadmaps</li><li>Collaborative workshops</li></ul><a class="${buttonClass('text')}" href="#contact">Plan your next step →</a></article>
        <article class="card"><span class="sample-badge">Create</span><h3 class="heading-2">Design &amp; experience</h3><p>Make every interaction feel clear, welcoming and easy to use.</p><ul><li>Visual identity</li><li>Accessible experiences</li><li>Content that connects</li></ul><a class="${buttonClass('text')}" href="#contact">Bring an idea to life →</a></article>
        <article class="card"><span class="sample-badge">Grow</span><h3 class="heading-2">Build &amp; improve</h3><p>Put your ideas into practice, learn from the results and keep moving.</p><ul><li>Thoughtful delivery</li><li>Team enablement</li><li>Continuous improvement</li></ul><a class="${buttonClass('text')}" href="#contact">Build something lasting →</a></article>
      </div>
${sectionActions(['#contact', 'Discuss your project'], ['#resources', 'Browse resources'])}
    </section>
    <section id="resources" class="sample-section" aria-labelledby="resources-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">Useful by design</p><h2 id="resources-title" class="heading-1">A head start on what’s next.</h2></div>
      <div class="sample-grid sample-split">
        <div class="sample-table-wrap" role="region" aria-label="Resource library" tabindex="0">
          <table><caption>Resources for your next project</caption><thead><tr><th scope="col">Resource</th><th scope="col">Format</th><th scope="col">Explore</th></tr></thead><tbody>
            <tr><th scope="row">Getting started</th><td><span class="sample-badge">Guide</span></td><td><a href="#getting-started">Read the guide</a></td></tr>
            <tr><th scope="row">Working together</th><td><span class="sample-badge">Checklist</span></td><td><a href="#working-together">See the checklist</a></td></tr>
            <tr><th scope="row">Your next conversation</th><td><span class="sample-badge">Support</span></td><td><a href="#contact">Ask a question</a></td></tr>
          </tbody></table>
        </div>
        <div class="sample-faq">
          <details id="getting-started" open><summary>Where should I start?</summary><p>Tell us what you want to achieve. We’ll help you explore your options and choose a useful first step.</p></details>
          <details id="working-together"><summary>How do we work together?</summary><p>We agree on your goals, keep communication open and review progress together. You’ll know what’s happening and what comes next.</p></details>
          <details><summary>Can we start small?</summary><p>Absolutely. A focused first project is a good way to learn, build confidence and decide where to go next.</p></details>
        </div>
      </div>
      <aside class="sample-notice" aria-label="Getting started tip"><strong>A useful first step.</strong> Bring your questions, a rough idea or a challenge you haven’t quite put into words. We’ll start there.</aside>
${sectionActions(['#contact', 'Ask a question'], ['#components', 'Explore components'])}
    </section>
    <section id="contact" class="sample-section sample-grid sample-split" aria-labelledby="contact-title">
      <div><p class="sample-eyebrow">Let’s make a start</p><h2 id="contact-title" class="heading-1">What are you thinking about?</h2><p>A fresh idea, a better experience or a problem worth solving. We’d love to hear about it.</p></div>
      <form class="card sample-form" action="#contact" method="get" aria-describedby="contact-note">
        <div><label for="contact-name">Your name</label><input class="input" id="contact-name" name="name" autocomplete="name" placeholder="Alex Morgan" required></div>
        <div><label for="contact-email">Email address</label><input class="input" type="email" id="contact-email" name="email" autocomplete="email" placeholder="alex@example.com" aria-describedby="contact-email-help"${fieldAttributes} required><small id="contact-email-help"${adv.state === 'invalid' ? ' class="sample-error"' : ''}>${emailHelp}</small></div>
        <div><label for="contact-service">What can we help with?</label><select class="input" id="contact-service" name="service"><option value="">Choose a service</option><option>Strategy &amp; direction</option><option>Design &amp; experience</option><option>Build &amp; improve</option></select></div>
        <fieldset><legend>How would you like to start?</legend><label class="sample-choice"><input type="radio" name="start" value="conversation" checked> A conversation</label><label class="sample-choice"><input type="radio" name="start" value="workshop"> A workshop</label></fieldset>
        <div><label for="contact-message">A little about your idea</label><textarea class="input" id="contact-message" name="message" rows="4" placeholder="Here’s what we have in mind…"></textarea></div>
        <label class="sample-choice"><input type="checkbox" name="copy" value="yes"> I’d like a copy of my enquiry.</label>
        <div class="button-row sample-section-actions">
          <button class="${buttonClass('primary')}" type="submit">Preview enquiry</button>
          <a class="${buttonClass('secondary')}" href="#services">Review our services</a>
        </div>
        <p id="contact-note" class="small-text">This is a sample form. No message is sent; submitting returns to this page.</p>
      </form>
    </section>
    <section id="components" class="sample-section" aria-labelledby="components-title">
      <div class="sample-section-heading"><p class="sample-eyebrow">The little details</p><h2 id="components-title" class="heading-1">A consistent experience, everywhere.</h2><p>Clear actions, helpful feedback and familiar controls.</p></div>
      <div class="sample-grid card-grid">
        <article class="card"><h3 class="heading-2">Actions that feel familiar</h3><div class="button-row">${['primary', 'secondary', 'accent', 'outline', 'text'].map(v => `<button class="${buttonClass(v)}" type="button">${v[0].toUpperCase() + v.slice(1)} action</button>`).join('')}</div>${actionExample}</article>
        <article class="card"><h3 class="heading-2">Helpful feedback</h3><p class="sample-feedback sample-feedback--success"><strong>Success.</strong> You’re ready for the next step.</p><p class="sample-feedback sample-feedback--warning"><strong>One more thing.</strong> Review your details before continuing.</p><p class="sample-feedback sample-feedback--danger"><strong>Something needs attention.</strong> Check the highlighted field.</p></article>
        <article class="card"><h3 class="heading-2">Progress at a glance</h3><label for="sample-progress">Project checklist — 3 of 4 complete</label><progress id="sample-progress" value="3" max="4">75%</progress><label for="sample-range">How much support do you need?</label><input id="sample-range" type="range" min="1" max="5" value="3"><label for="sample-reference">Your reference</label><input class="input" id="sample-reference" value="PROJECT-001" readonly><label for="sample-unavailable">Available after your first visit</label><input class="input" id="sample-unavailable" value="Not available yet" disabled></article>
      </div>
${sectionActions(['#contact', 'Start a conversation'], ['#home', 'Back to top'])}
    </section>
  </main>
  <footer class="sample-footer">
    <div class="container sample-footer-inner"><div><a class="sample-brand" href="#home">${project}</a><p class="small-text">Good people. Thoughtful work. A shared way forward.</p><small>© ${project}. All rights reserved.</small></div><nav aria-label="Footer navigation"><ul class="sample-nav"><li><a href="#home">Home</a></li><li><a href="#about">About</a></li><li><a href="#resources">Resources</a></li><li><a href="#contact">Contact</a></li></ul></nav></div>
  </footer>
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
.sample-nav a { font-weight: 600; }
.sample-header .sample-nav a { text-decoration: none; text-underline-offset: .2em; text-decoration-thickness: .1em; }
.sample-header .sample-nav a:hover { text-decoration-line: underline; }
.sample-header .sample-nav a:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }
.sample-header .sample-nav a:active { text-decoration-line: underline; text-decoration-thickness: .2em; }
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
.sample-section-heading { max-width: 44rem; margin-bottom: var(--space-8); }
.sample-section-heading > :last-child, .sample-home .card > :last-child, .sample-form > :last-child { margin-bottom: 0; }
.sample-home .card ul { padding-inline-start: var(--space-6); margin-block: var(--space-4); }
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
@media (min-width: 48rem) {
  .sample-section { padding-block: var(--space-12); }
}
@media (min-width: 64rem) {
  .sample-home .container { padding-inline: var(--space-8); }
  .sample-logo { width: var(--space-16); }
  .sample-hero { padding-block: var(--space-20); }
  .sample-section { padding-block: var(--space-16); }
}
/* Keep the card minimum/gap controls effective within the 12-column page. */
@container sample-content (width < ${threeCards}px) {
  .sample-home .card-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .sample-home .card-grid > .card { grid-column: auto; }
}
@container sample-content (width < ${twoCards}px) {
  .sample-home .card-grid { grid-template-columns: minmax(0, 1fr); }
}
@media (max-width: 48rem) {
  .sample-home .sample-hero, .sample-home .sample-split { grid-template-columns: minmax(0, 1fr); }
  .sample-hero > *, .sample-split > * { grid-column: auto; }
  .sample-header-inner { align-items: center; flex-direction: row; flex-wrap: nowrap; }
  .sample-header .sample-brand { flex: 1; min-width: 0; }
  .sample-desktop-navigation { display: none; }
  .sample-menu { display: block; flex: none; }
  .sample-hero-image { max-width: 36rem; }
  .sample-about-image { max-width: 32rem; }
}
`;
  }

  DSStudio.register({
    id: 'sample-homepage',
    title: 'Sample home page',
    init() {
      const previousCss = cssExport;
      cssExport = () => previousCss() + '\n' + homepageCss();
      htmlExport = homepageHtml;
      renderCode();
    }
  });
})();
