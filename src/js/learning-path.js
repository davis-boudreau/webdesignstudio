'use strict';
/* Session-only learning/navigation state. Project values remain in the shared
   system; study rules and token values are read from the current CSS export. */
DSStudio.register({
  id: 'learning-path', title: 'Contextual example connections',
  init() {
    const get = id => document.getElementById(id);
    const examples = {
      action: { label: 'Primary action', id: 'home', section: 'hero', selector: '.ds-button--primary', tokens: ['--button-primary-bg', '--button-primary-text', '--button-radius'], explanation: 'The primary action uses component tokens. Its colours can override the main palette; use a token control below to follow the actual setting.' },
      spacing: { label: 'Section spacing', id: 'lists', section: 'basics', selector: '.section', tokens: ['--space-unit', '--space-8', '--space-16'], explanation: 'Section padding uses multiples of the spacing unit. Wider viewport rules can select a different multiple.' },
      header: { label: 'Header and logo', id: 'top', section: 'header', selector: '.logo', tokens: ['--primary', '--on-primary', '--radius-base'], explanation: 'The logo consumes semantic colours and the shared radius. Brand swatches copy values into roles; equal colours are not necessarily live aliases.' },
      hero: { label: 'Hero layout', id: 'home', section: 'hero', selector: '.hero-layout', tokens: ['--grid-gap', '--text-display', '--page-gutter'], explanation: 'Grid creates two columns. The exported responsive rule stacks them at the saved narrow cutoff; text stays before the image.' },
      skills: { label: 'Flexbox components', id: 'features', section: 'skills', selector: '.skills-layout', tokens: ['--grid-gap', '--radius-base'], explanation: 'Flexbox places the introduction beside the components. It changes direction at the saved narrow cutoff.' },
      profile: { label: 'Profile row', id: 'basic-layout', section: 'skills', selector: '.media-object', tokens: ['--space-4', '--radius-base'], explanation: 'A fixed avatar and flexible text form a compact Flexbox row. The component sits inside a shared card.' },
      faq: { label: 'Native FAQ', id: 'basic-usability', section: 'skills', selector: '.faq-demo summary', tokens: ['--heading-weight', '--space-2', '--focus-width'], explanation: 'Details and summary provide native disclosure behaviour. The summary keeps a 44px minimum target; heading weight, answer spacing and shared focus styling supply its appearance.' },
      grid: { label: 'Responsive card Grid', id: 'cards-grid', section: 'toolkit', selector: '.list-grid', tokens: ['--grid-card-min', '--grid-gap', '--grid-align'], explanation: 'Auto-fit adds columns when the saved minimum card width and gap fit. Reading order follows the HTML.' },
      form: { label: 'Form controls', id: 'contact-form', section: 'form', selector: '.signup-form', tokens: ['--reading-measure', '--space-4', '--control-height'], explanation: 'Grid spaces the form fields; the reading measure limits its width. Labels and native validation remain in HTML.' },
      footer: { label: 'Footer navigation', id: 'footer', section: 'footer', selector: '.website-footer .footer-inner', tokens: ['--space-8', '--border-width'], explanation: 'The footer combines identity and navigation. Its sitemap follows Architecture; planned entries do not create body sections.' }
    };
    let selected = 'action', picking = false, previousMode = state.sampleMode;
    let studySignature = '', focusVersion = 0;
    const focus = element => {
      if (!element) return;
      if (!element.hasAttribute('tabindex') && !element.matches('button, input, select, textarea')) element.tabIndex = -1;
      element.scrollIntoView({ block: 'center', behavior: 'instant' });
      element.focus({ preventScroll: true });
    };
    function tokenRow(name) {
      const rows = window.dssReadTokens().filter(row => row.name === name);
      return (state.theme === 'dark' ? rows.find(row => row.scope === 'Dark') : null) || rows.find(row => row.scope !== 'Dark');
    }
    function configure(name) {
      const row = tokenRow(name);
      if (row) window.dssConfigureToken(row);
    }
    function studyRule(css) {
      const example = examples[selected];
      const start = css.indexOf(example.selector + ' {');
      if (start < 0) return 'This example also uses shared rules. Inspect its section and complete CSS for the full implementation.';
      return css.slice(start, css.indexOf('}', start) + 1);
    }
    function sync(cssHint) {
      const isBasic = state.sampleMode === 'basic';
      if (previousMode !== state.sampleMode) {
        picking = false;
        get('studyStatus').textContent = '';
        previousMode = state.sampleMode;
      }
      get('exampleConnections').hidden = !isBasic;
      if (!isBasic) picking = false;
      get('studyPick').setAttribute('aria-pressed', String(picking));
      get('studyPick').textContent = picking ? 'Stop selecting examples' : 'Select in preview';
      if (!isBasic) { studySignature = ''; return; }
      const css = typeof cssHint === 'string' ? cssHint : cssExport();
      const signature = state.theme + selected + css;
      if (studySignature === signature) return;
      studySignature = signature;
      const example = examples[selected];
      get('studyExample').value = selected;
      get('studyExplanation').textContent = example.explanation + (['hero', 'skills'].includes(selected) ? ` Current narrow cutoff: ${DSStudio.responsive.settings().stack}px.` : '');
      const rule = studyRule(css);
      if (get('studyRule').textContent !== rule) get('studyRule').textContent = rule;
      const rows = window.dssReadTokens(css);
      get('studyTokens').replaceChildren(...example.tokens.map(name => {
        const candidates = rows.filter(row => row.name === name);
        const row = (state.theme === 'dark' ? candidates.find(item => item.scope === 'Dark') : null) || candidates.find(item => item.scope !== 'Dark');
        const item = document.createElement('div'), value = document.createElement('code'), button = document.createElement('button');
        item.className = 'study-token';
        value.textContent = `${name}: ${row?.value || 'See shared CSS'}`;
        button.type = 'button'; button.textContent = 'Configure';
        button.setAttribute('aria-label', `Configure ${name}`);
        button.disabled = !row || !window.dssTokenSource(row);
        button.addEventListener('click', () => configure(name));
        item.append(value, button); return item;
      }));
    }
    function select(key) {
      if (!Object.hasOwn(examples, key)) return;
      selected = key;
      get('studyStatus').textContent = '';
      sync();
    }
    function showPreview() {
      window.dssRevealSection('studio-section-4', false);
      focus(get('previewShell'));
      const version = ++focusVersion, targetId = examples[selected].id;
      queueMicrotask(() => {
        if (version !== focusVersion) return;
        const doc = get('previewPage').contentDocument, example = doc?.getElementById(targetId);
        if (example) {
          for (let parent = example; parent; parent = parent.parentElement) if (parent.tagName === 'DETAILS') parent.open = true;
          doc.defaultView.scrollTo({ top: doc.defaultView.scrollY + example.getBoundingClientRect().top - 24, behavior: 'instant' });
          example.tabIndex = -1;
          example.focus({ preventScroll: true });
        }
      });
    }
    function showCode() {
      focusVersion++;
      DSStudio.inspector.show({ section: 'all', language: 'css', find: examples[selected].selector + ' {' });
      get('studyStatus').textContent = `Complete CSS: ${examples[selected].selector}. Shared rules and responsive overrides also apply.`;
    }
    get('studyExample').replaceChildren(...Object.entries(examples).map(([key, example]) => new Option(example.label, key)));
    get('studyExample').addEventListener('change', event => select(event.target.value));
    get('studyPreview').addEventListener('click', showPreview);
    get('studyCode').addEventListener('click', showCode);
    get('studyPick').addEventListener('click', () => {
      picking = !picking; sync();
      get('studyStatus').textContent = picking ? 'Select an example in the preview. Selection mode pauses its normal click action. Stop selecting to use links and controls normally.' : 'Normal preview interactions restored.';
      if (picking) focus(get('previewShell'));
    });
    document.addEventListener('keydown', event => { if (event.key === 'Escape' && picking) { picking = false; sync(); get('studyStatus').textContent = 'Normal preview interactions restored.'; } });
    DSStudio.on('preview:example', ({ id, example }) => {
      const byId = { home: 'hero', top: 'header', features: 'skills', lists: 'grid', signup: 'form', 'basic-layout': 'profile', 'basic-usability': 'faq', 'cards-grid': 'grid', 'contact-form': 'form', footer: 'footer' };
      const key = Object.hasOwn(examples, example) ? example : byId[id];
      picking = false; select(key || 'hero');
      get('exampleConnections').open = true;
      focus(get('studyExample'));
      get('studyStatus').textContent = 'Example selected. Normal preview interactions restored. Find its CSS or configure a token below.';
    });
    DSStudio.on('preview:cancel', () => { picking = false; sync(); get('studyStatus').textContent = 'Normal preview interactions restored.'; });
    DSStudio.on('inspector:change', ({ section, completeCss }) => {
      const bySection = { basics: 'spacing', header: 'header', hero: 'hero', skills: 'skills', toolkit: 'grid', form: 'form', footer: 'footer' };
      if (bySection[section] && examples[selected].section !== section) selected = bySection[section];
      sync(completeCss);
    });
    DSStudio.on('stage:change', ({ stage }) => {
      focusVersion++;
      picking = false;
      const key = { architecture: 'footer', palette: 'header', typography: 'hero', semantic: 'header', buttons: 'action', spacing: 'spacing', responsive: 'hero', accessibility: 'form', deliver: 'hero' }[stage.id];
      if (key) select(key); else sync();
      // Entering a step frames its representative result without taking focus.
      // Ordinary design edits do not run this path or disturb preview scrolling.
      if (key && stage.index < 11) {
        const doc = get('previewPage').contentDocument;
        const target = stage.id === 'buttons' ? doc?.querySelector('#home .ds-button--primary') : doc?.getElementById(examples[key].id);
        if (target) doc.defaultView.scrollTo({ top: doc.defaultView.scrollY + target.getBoundingClientRect().top - 24, behavior: 'instant' });
      }
    });
    DSStudio.learning = { get picking() { return picking; } };
    sync();
  }
});
