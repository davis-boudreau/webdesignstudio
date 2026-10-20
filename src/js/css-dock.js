'use strict';
/* The inspector and downloads share the studio's live export generators. */
(() => {
  const $ = id => document.getElementById(id);
  const live = $('dockCss');
  const tabs = ['dockTabCss', 'dockTabHtml'];
  let language = 'css', copyTimer;
  const content = () => language === 'css' ? cssExport() : htmlExport();

  function refreshDock() {
    $('dockTheme').value = state.theme;
    const code = content();
    if (live.textContent !== code) live.textContent = code;
    live.setAttribute('aria-label', `Generated ${language.toUpperCase()} code`);
    live.setAttribute('aria-labelledby', language === 'css' ? tabs[0] : tabs[1]);
    $('dockDownload').textContent = 'Download ' + (language === 'css' ? 'tokens.css' : 'index.html');
    $('dockCopy').textContent = 'Copy ' + language.toUpperCase();
    $('dockNote').textContent = language === 'css' ?
      'Brand → semantic → component rules for light and dark themes. Save tokens.css beside index.html.' :
      `The ${state.theme} home page, also shown in the responsive preview. Save index.html beside tokens.css; images are embedded.`;
    tabs.forEach((id, index) => {
      const selected = language === (index === 0 ? 'css' : 'html');
      $(id).setAttribute('aria-selected', String(selected));
      $(id).tabIndex = selected ? 0 : -1;
    });
  }
  // The existing studio calls renderCode() whenever any foundation value changes.
  const originalRenderCode = renderCode;
  renderCode = function() {
    originalRenderCode();
    refreshDock();
  };
  $('dockTheme').addEventListener('change', event => {
    state.theme = event.target.value;
    apply();
  });
  tabs.forEach((id, index) => {
    $(id).addEventListener('click', () => {
      language = index === 0 ? 'css' : 'html';
      clearTimeout(copyTimer);
      refreshDock();
      live.scrollTop = 0;
      live.scrollLeft = 0;
    });
    $(id).addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') next = (index + 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      $(tabs[next]).click();
      $(tabs[next]).focus();
    });
  });
  $('dockCopy').addEventListener('click', async () => {
    const selectedLanguage = language;
    try {
      await navigator.clipboard.writeText(content());
      if (language === selectedLanguage) $('dockCopy').textContent = 'Copied!';
    } catch {
      if (language === selectedLanguage) $('dockCopy').textContent = 'Select code to copy';
    }
    clearTimeout(copyTimer);
    copyTimer = setTimeout(() => $('dockCopy').textContent = 'Copy ' + language.toUpperCase(), 1800);
  });
  $('dockDownload').addEventListener('click', () => download(
    language === 'css' ? 'tokens.css' : 'index.html', content(),
    language === 'css' ? 'text/css' : 'text/html'));
  /* FIX: $() is getElementById, so $('.studio-code-dock') returned null and the Collapse button crashed. */
  $('dockToggle').addEventListener('click', () => {
    const collapsed = document.querySelector('.studio-code-dock').classList.toggle('is-collapsed');
    $('dockToggle').textContent = collapsed ? 'Expand code' : 'Collapse code';
    $('dockToggle').setAttribute('aria-expanded', String(!collapsed));
  });
  refreshDock();
})();
