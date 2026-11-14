'use strict';
/* The inspector and downloads share the studio's live export generators. */
(() => {
  const $ = id => document.getElementById(id);
  const live = $('dockCss');
  const tabs = ['dockTabCss', 'dockTabHtml', 'dockTabJson'];
  const languages = ['css', 'html', 'json'];
  let language = 'css', copyTimer;
  const dock = document.querySelector('.studio-code-dock');
  const layout = document.querySelector('.layout');
  function setCollapsed(collapsed) {
    const restoreFocus = collapsed && dock.contains(document.activeElement);
    layout.classList.toggle('is-inspector-collapsed', collapsed);
    dock.classList.toggle('is-collapsed', collapsed);
    dock.open = !collapsed;
    $('dockToggle').textContent = collapsed ? 'Expand code' : 'Collapse code';
    $('dockToggle').setAttribute('aria-expanded', String(!collapsed));
    if (restoreFocus) {
      const opener = $('inspectorToggle');
      opener.focus({ preventScroll: true });
      const bounds = opener.getBoundingClientRect();
      if (bounds.top < document.querySelector('.topbar').getBoundingClientRect().bottom || bounds.bottom > innerHeight)
        dock.scrollIntoView({ block: 'center', behavior: 'instant' });
    }
    syncResponsivePreview();
  }
  const content = () => language === 'css' ? cssExport() : language === 'json' ? projectJson() : htmlExport();
  const section = () => language !== 'json' && state.sampleMode === 'basic' ? $('dockSection').value : 'all';
  const visibleContent = () => section() === 'all' ? content() : DSStudio.samples.basicExcerpt(content(), language, section());
  const copyLabel = () => 'Copy ' + language.toUpperCase() + (section() === 'all' ? '' : ' excerpt');

  function refreshDock() {
    $('dockTheme').value = state.theme;
    $('dockLearning').hidden = state.sampleMode !== 'basic' || language === 'json';
    const code = visibleContent();
    if (live.textContent !== code) live.textContent = code;
    live.setAttribute('aria-label', `Generated ${language.toUpperCase()} code`);
    live.setAttribute('aria-labelledby', tabs[languages.indexOf(language)]);
    $('dockDownload').textContent = 'Download ' + (language === 'css' ? 'tokens.css' : language === 'json' ? 'design-system-studio.json' : 'index.html');
    $('dockCopy').textContent = copyLabel();
    $('dockNote').textContent = language === 'json' ? 'Project JSON preserves editable settings and planning data. Load it into the studio to resume your work.' : state.sampleMode === 'basic' ?
      `Basic ${language.toUpperCase()}: ${section() === 'all' ? 'complete file' : 'study excerpt; shared foundations remain in the complete CSS'}. Local HTML and reusable component CSS; no framework needed. Download saves the complete file. Save index.html beside tokens.css.` : language === 'css' ?
      'Local CSS: shared tokens → reusable component rules for light and dark themes. No framework needed. Save tokens.css beside index.html.' :
      `Local HTML for the ${state.theme} home page, also shown in the responsive preview. Save index.html beside tokens.css; images are embedded.`;
    DSStudio.emit('inspector:change', { language, section: section(), completeCss: language === 'css' && section() === 'all' ? code : null });
    tabs.forEach((id, index) => {
      const selected = language === languages[index];
      $(id).setAttribute('aria-selected', String(selected));
      $(id).tabIndex = selected ? 0 : -1;
    });
  }
  // Explicit inspector actions and compatibility readouts remain synchronous.
  DSStudio.on('output:updated', refreshDock);
  DSStudio.inspector = {
    show({ section: requestedSection = section(), language: requestedLanguage = language, find = '' } = {}) {
      language = languages.includes(requestedLanguage) ? requestedLanguage : 'css';
      const available = [...$('dockSection').options].some(option => option.value === requestedSection);
      $('dockSection').value = available ? requestedSection : 'all';
      clearTimeout(copyTimer);
      refreshDock();
      setCollapsed(false);
      const index = find ? live.textContent.indexOf(find) : -1;
      const line = index < 0 ? 0 : live.textContent.slice(0, index).split('\n').length - 1;
      live.scrollTop = line * parseFloat(getComputedStyle(live).lineHeight);
      live.focus({ preventScroll: true });
      live.scrollIntoView({ block: 'center', behavior: 'instant' });
    }
  };
  $('dockTheme').addEventListener('change', event => {
    state.theme = event.target.value;
    apply();
  });
  $('dockSection').addEventListener('change', () => {
    clearTimeout(copyTimer);
    refreshDock();
    live.scrollTop = 0;
    live.scrollLeft = 0;
  });
  tabs.forEach((id, index) => {
    $(id).addEventListener('click', () => {
      language = languages[index];
      clearTimeout(copyTimer);
      refreshDock();
      live.scrollTop = 0;
      live.scrollLeft = 0;
    });
    $(id).addEventListener('keydown', event => {
      let next;
      if (event.key === 'ArrowRight') next = (index + 1) % tabs.length;
      else if (event.key === 'ArrowLeft') next = (index + tabs.length - 1) % tabs.length;
      else if (event.key === 'Home') next = 0;
      else if (event.key === 'End') next = tabs.length - 1;
      else return;
      event.preventDefault();
      $(tabs[next]).click();
      $(tabs[next]).focus();
    });
  });
  $('dockCopy').addEventListener('click', async () => {
    const selectedLanguage = language, selectedMode = state.sampleMode, selectedSection = section();
    const stillSelected = () => language === selectedLanguage && state.sampleMode === selectedMode && section() === selectedSection;
    try {
      await navigator.clipboard.writeText(visibleContent());
      if (stillSelected()) $('dockCopy').textContent = 'Copied!';
    } catch {
      if (stillSelected()) $('dockCopy').textContent = 'Select code to copy';
    }
    clearTimeout(copyTimer);
    copyTimer = setTimeout(() => $('dockCopy').textContent = copyLabel(), 1800);
  });
  $('dockDownload').addEventListener('click', () => download(
    language === 'css' ? 'tokens.css' : language === 'json' ? 'design-system-studio.json' : 'index.html', content(),
    language === 'css' ? 'text/css' : language === 'json' ? 'application/json' : 'text/html'));
  /* FIX: $() is getElementById, so $('.studio-code-dock') returned null and the Collapse button crashed. */
  $('dockToggle').addEventListener('click', () => {
    setCollapsed(dock.open);
  });
  dock.addEventListener('toggle', () => setCollapsed(!dock.open));
  setCollapsed(dock.classList.contains('is-collapsed'));
  refreshDock();
})();
