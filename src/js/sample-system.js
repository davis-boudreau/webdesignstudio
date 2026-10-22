'use strict';
/* Both teaching pages use the same saved foundations and component rules. */
(() => {
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
    const basic = mode === 'basic', project = escapeHtml(state.project);
    const links = basic ? [['Home','home'],['What you can learn','features'],['Lists','lists'],['Sign up','signup']] : [['Home','home'],['About','about'],['Resources','resources'],['Contact','contact']];
    return `<footer class="website-footer ${basic ? 'site-footer' : 'sample-footer'}" id="footer">
    <div class="container">
      <div class="footer-inner sample-footer-inner">
        <div class="footer-identity"><a class="footer-brand" href="#home">${project}</a><p>A place to learn, practise and build something useful.</p></div>
        <nav aria-label="Footer navigation"><h2 class="footer-heading">Explore</h2><ul class="footer-links ${basic ? 'nav-list' : 'sample-nav'}">${links.map(([label,id])=>`<li><a href="#${id}">${label}</a></li>`).join('')}<li><a href="#sitemap">Sitemap</a></li></ul></nav>
      </div>
      <details class="sitemap" id="sitemap">
        <summary id="sitemap-title"><span>Sitemap</span><span class="footer-sitemap-hint">All sections and topics</span></summary>
        <nav aria-labelledby="sitemap-title">${DSStudio.process.sitemapHtml()}</nav>
      </details>
      <div class="footer-bottom"><small>&copy; ${project}. A website practice space.</small><a class="back-to-top" href="#top">Back to top <span aria-hidden="true">&uarr;</span></a></div>
    </div>
  </footer>`;
  }
  function footerCss() {
    return `/* Shared footer: identity, key destinations, optional full map and return link. */
.website-footer { border-top: var(--border-width) solid var(--border); background: var(--surface); }
.website-footer .footer-inner { display: grid; grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); align-items: start; gap: var(--space-8); padding-block: var(--space-8); }
.website-footer .footer-inner > * { min-width: 0; }
.website-footer .footer-brand { display: inline-flex; align-items: center; min-height: 44px; max-width: 100%; color: var(--text); font-family: var(--font-heading); font-weight: var(--heading-weight); overflow-wrap: anywhere; }
.website-footer .footer-identity p { margin: var(--space-2) 0 0; color: var(--text-muted); }
.website-footer .footer-heading { margin: 0 0 var(--space-2); font: inherit; font-weight: var(--heading-weight); }
.website-footer .footer-links { display: flex; flex-wrap: wrap; gap: var(--space-1) var(--space-6); list-style: none; margin: 0; padding: 0; }
.website-footer .footer-links li { margin: 0; }
.website-footer .footer-links a { font-weight: var(--heading-weight); }
.website-footer a { overflow-wrap: anywhere; text-underline-offset: .2em; }
.website-footer a:hover { text-decoration: underline; }
.website-footer .footer-links a, .website-footer .back-to-top { display: inline-flex; align-items: center; gap: var(--space-2); min-height: 44px; }
.website-footer .sitemap { border-top: var(--border-width) solid var(--border); padding-block: var(--space-4); }
.website-footer .sitemap summary { padding-block: var(--space-2); min-height: 44px; cursor: pointer; font-weight: var(--heading-weight); overflow-wrap: anywhere; }
.website-footer .footer-sitemap-hint { display: block; margin-inline-start: var(--space-4); font-size: var(--text-small); font-weight: 400; color: var(--text-muted); }
.website-footer .sitemap-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 12rem), 1fr)); gap: var(--space-6); list-style: none; padding: 0; margin-block: var(--space-4); }
.website-footer .sitemap-list > li { min-width: 0; margin: 0; overflow-wrap: anywhere; }
.website-footer .sitemap-list > li > a, .website-footer .sitemap-list > li > span { font-weight: var(--heading-weight); }
.website-footer .sitemap-list ul { padding-inline-start: var(--space-4); }
.website-footer .sitemap-list li li { margin: 0; }
.website-footer .sitemap-list a { display: inline-flex; align-items: center; min-height: 44px; }
.website-footer .sitemap-planned { display: block; font-size: var(--text-small); font-weight: 400; color: var(--text-muted); }
.website-footer .footer-bottom { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: center; gap: var(--space-4); padding-block: var(--space-4); border-top: var(--border-width) solid var(--border); }
.website-footer .footer-bottom small { margin: 0; font-size: var(--text-small); color: var(--text-muted); overflow-wrap: anywhere; }
@media (max-width: ${DSStudio.responsive.rem(DSStudio.responsive.settings().stack)}) {
  .website-footer .footer-inner { grid-template-columns: minmax(0, 1fr); gap: var(--space-6); }
}
`;
  }
  DSStudio.samples = { buttonClass, footerHtml, footerCss };
  DSStudio.register({
    id: 'sample-system', title: 'Shared website design system',
    init() {
      const sharedCss = cssExport;
      DSStudio.samples.foundationCss = () => sharedCss() + '\n:focus-visible { outline: var(--focus-width) solid var(--focus); outline-offset: 3px; }\n' + navigationCss();
      cssExport = DSStudio.samples.foundationCss;
    }
  });
})();
