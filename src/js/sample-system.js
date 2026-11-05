'use strict';
/* Both teaching pages use the same saved foundations and component rules. */
(() => {
  function basicNavigationHtml() {
    return [['home', 'Home'], ['features', 'Components'], ['lists', 'Layouts'], ['signup', 'Forms']]
      .map(([id, label]) => `<li><a href="#${id}">${escapeHtml(label)}</a></li>`).join('');
  }
  function buttonClass(variant = 'primary') {
    const settings = state.buttonDesign || {};
    const size = ['sm', 'lg'].includes(settings.size) ? ` ds-button--${settings.size}` : '';
    return `ds-button ds-button--${variant}${size}${settings.mobileFull ? ' ds-button--mobile-full' : ''}`;
  }
  function navigationCss() {
    return `/* Header navigation shares the Advanced text and interaction treatment. */
:is(.site-header .nav-list, .sample-header .sample-nav) a { font-weight: 600; text-decoration: none; text-underline-offset: .2em; text-decoration-thickness: .1em; }
:is(.site-header .nav-list, .sample-header .sample-nav) a:hover { text-decoration-line: underline; }
:is(.site-header .nav-list, .sample-header .sample-nav) a:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }
:is(.site-header .nav-list, .sample-header .sample-nav) a:active { text-decoration-line: underline; text-decoration-thickness: .2em; }
`;
  }
  function footerHtml(mode) {
    const project = escapeHtml(state.project);
    const basic = mode === 'basic';
    const navigation = basic ? basicNavigationHtml() : [['Home','home'],['About','about'],['Resources','resources'],['Contact','contact']]
      .map(([label, id]) => `<li><a href="#${id}">${label}</a></li>`).join('');
    const sitemap = basic ? DSStudio.process.sitemapHtml({ linksOnly: true, parentIds: ['features', 'lists', 'signup'] }) : DSStudio.process.sitemapHtml();
    return `<footer class="website-footer ${basic ? 'site-footer' : 'sample-footer'}" id="footer">
    <div class="container">
      <div class="footer-inner">
        <div class="footer-identity">
          <a class="footer-brand" href="#home">${project}</a>
          <p>${basic ? 'Small examples. Solid foundations.' : 'A place to learn, practise and build something useful.'}</p>
        </div>
        <nav aria-label="Footer navigation">
          <ul class="footer-links">${navigation}</ul>
        </nav>
      </div>
      <details class="footer-sitemap" id="footer-sitemap">
        <summary id="sitemap-toggle"><h2 id="sitemap-title">Sitemap</h2></summary>
        <nav class="sitemap" id="sitemap" aria-labelledby="sitemap-title" tabindex="-1">
          ${sitemap}
        </nav>
      </details>
      <div class="footer-bottom">
        <small>&copy; ${project}. ${basic ? 'HTML &amp; CSS essentials.' : 'A website practice space.'}</small>
        <a class="back-to-top" href="#top">Back to top <span aria-hidden="true">&uarr;</span></a>
      </div>
    </div>
  </footer>`;
  }
  function footerCss() {
    return `/* Shared classic footer: main navigation, native sitemap disclosure and return link. */
.website-footer { border-top: var(--border-width) solid var(--border); background: var(--footer-background-paint); }
.website-footer .footer-inner { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: start; gap: var(--space-8); padding-block: var(--space-8); }
.website-footer .footer-inner > * { min-width: 0; }
.website-footer .footer-brand { display: inline-flex; align-items: center; min-height: 44px; max-width: 100%; color: var(--text); font-family: var(--font-heading); font-weight: var(--heading-weight); overflow-wrap: anywhere; text-decoration: none; }
.website-footer .footer-identity p { margin: var(--space-2) 0 0; color: var(--text-muted); }
.website-footer .footer-links { display: flex; flex-wrap: wrap; gap: var(--space-1) var(--space-6); list-style: none; margin: 0; padding: 0; }
.website-footer .footer-links li { margin: 0; }
.website-footer .footer-links a { font-weight: var(--heading-weight); }
.website-footer a { overflow-wrap: anywhere; text-underline-offset: .2em; }
.website-footer a:hover { text-decoration: underline; }
.website-footer .footer-links a, .website-footer .back-to-top { display: inline-flex; align-items: center; gap: var(--space-2); min-height: 44px; }
.website-footer .footer-sitemap { margin: 0; padding: 0; border: 0; border-top: var(--border-width) solid var(--border); border-radius: 0; }
.website-footer .footer-sitemap > summary { display: list-item; min-height: 44px; padding-block: var(--space-6) var(--space-4); box-sizing: border-box; color: var(--text); text-align: left; cursor: pointer; }
.website-footer .footer-sitemap > summary:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }
.website-footer .sitemap { padding-block: 0 var(--space-6); }
.website-footer .footer-sitemap:not([open]) > .sitemap { display: none; }
.website-footer .sitemap-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); gap: var(--space-6); list-style: none; padding: 0; max-width: 48rem; margin: 0 auto; justify-items: center; }
.website-footer .sitemap-list > li { min-width: 0; max-width: 100%; margin: 0; overflow-wrap: anywhere; text-align: center; }
.website-footer .sitemap-list > li > a, .website-footer .sitemap-list > li > span { font-weight: var(--heading-weight); }
.website-footer .sitemap-list ul { display: flex; flex-direction: column; align-items: center; margin: var(--space-2) 0 0; padding: 0; list-style: none; }
.website-footer .sitemap-list ul a { font-size: var(--text-small); }
.website-footer .sitemap-list li li { margin: 0; }
.website-footer .sitemap-list a { max-width: 100%; display: inline-flex; align-items: center; min-height: 44px; }
.website-footer .sitemap-planned { display: block; font-size: var(--text-small); font-weight: 400; color: var(--text-muted); }
.website-footer .footer-bottom { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-4); padding-block: var(--space-4); border-top: var(--border-width) solid var(--border); }
.website-footer .footer-bottom small { margin: 0; font-size: var(--text-small); color: var(--text-muted); overflow-wrap: anywhere; }
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .website-footer .footer-inner { grid-template-columns: minmax(0, 1fr); gap: var(--space-6); }
}
.website-footer .footer-inner > nav { justify-self: end; }
.website-footer #sitemap-title { display: inline; font: inherit; font-weight: var(--heading-weight); margin: 0; text-align: left; }
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .website-footer .footer-inner > nav { justify-self: start; }
  .website-footer .footer-bottom { flex-direction: column; align-items: flex-start; }
}

`;
  }
  DSStudio.samples = { buttonClass, footerHtml, footerCss, basicNavigationHtml };
  DSStudio.register({
    id: 'sample-system', title: 'Shared website design system',
    init() {
      const sharedCss = cssExport;
      DSStudio.samples.foundationCss = () => sharedCss() + '\nbody > main { background: var(--main-background-paint); }\n' + PADDING_REGIONS.map(region=>`body > ${region} { padding: ${PADDING_SIDES.map(side=>`var(--${region}-padding-${side})`).join(' ')}; }`).join('\n') + '\n:focus-visible { outline: var(--focus-width) solid var(--focus); outline-offset: 3px; }\n' + navigationCss();
      cssExport = DSStudio.samples.foundationCss;
    }
  });
})();
