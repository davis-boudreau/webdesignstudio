'use strict';
/* Session-only learning/navigation state. Project values remain in the shared
   system; study rules and token values are read from the current CSS export. */
DSStudio.register({
  id: 'learning-path', title: 'Beginner path and example connections',
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
    const tasks = [
      { label: '1. Change an action colour', example: 'action', token: '--button-primary-bg', instruction: 'Change the primary button background in Buttons. See the action update in Basic, find --button-primary-bg in CSS, and review the text contrast before keeping the colour.' },
      { label: '2. Change reusable spacing', example: 'spacing', token: '--space-unit', instruction: 'Change the base spacing unit in Layout. Compare section padding before and after, then follow --space-unit into --space-8. Explain why several spaces change together.' },
      { label: '3. Test a narrow layout', example: 'hero', step: 9, control: 'responsive-stack', instruction: 'Compare the 390 px and Fluid preview widths. Find the rule that stacks the hero, then compare the saved narrow cutoff with the preview width. Presets test widths; they do not change your breakpoints.' },
      { label: '4. Export and reopen', example: 'hero', step: 11, control: 'jExportHtml', instruction: 'In Deliver, download index.html and tokens.css into the same folder. Open index.html in a browser. Export project JSON too, then explain the difference between editable website files and your restorable studio project.' }
    ];
    let selected = 'action', taskIndex = 0, picking = false, previousMode = state.sampleMode;
    const tried = new Set();
    let studySignature = '', focusVersion = 0;
    const focus = element => {
      if (!element) return;
      if (!element.hasAttribute('tabindex') && !element.matches('button, input, select, textarea')) element.tabIndex = -1;
      element.scrollIntoView({ block: 'center', behavior: 'instant' });
      element.focus({ preventScroll: true });
    };
    function basic() {
      if (state.sampleMode !== 'basic') get('dockModeBasic').click();
    }
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
    function setTask(index) {
      taskIndex = Math.max(0, Math.min(tasks.length - 1, index));
      const task = tasks[taskIndex];
      get('beginnerTask').value = String(taskIndex);
      get('beginnerInstruction').textContent = task.instruction;
      get('beginnerProgress').textContent = `${tried.size} of ${tasks.length} exercises tried. This is your own progress, not a test result.`;
      get('beginnerDone').textContent = taskIndex === tasks.length - 1 ? 'I tried this exercise' : 'I tried this - next exercise';
      select(task.example);
    }
    function openControl() {
      focusVersion++;
      basic();
      const task = tasks[taskIndex];
      if (task.token) configure(task.token);
      else { window.dssShowWizardStep(task.step); focus(get(task.control)); }
    }
    function navigate(place) {
      focusVersion++;
      if (place === 'build') focus(document.querySelector('[data-journey-pane]:not([hidden]) .journey-stage-title'));
      if (place === 'preview') showPreview();
      if (place === 'code') DSStudio.inspector.show();
      if (place === 'learn') { get('beginnerPath').hidden = false; get('beginnerPath').open = true; focus(get('beginnerTask')); }
      get('workspaceStatus').textContent = { build: 'Build: current wizard step', preview: 'Preview: generated website', code: 'Code: current inspector view', learn: 'Beginner exercises' }[place];
    }
    get('studyExample').replaceChildren(...Object.entries(examples).map(([key, example]) => new Option(example.label, key)));
    get('beginnerTask').replaceChildren(...tasks.map((task, index) => new Option(task.label, String(index))));
    get('beginnerReference').append(document.querySelector('.dock-start'));
    get('beginnerStart').addEventListener('click', () => {
      basic(); get('beginnerPath').hidden = false; get('beginnerPath').open = true; setTask(0); DSStudio.inspector.show({ section: 'all', language: 'css' }); openControl();
    });
    get('beginnerTask').addEventListener('change', event => { basic(); setTask(Number(event.target.value)); });
    get('beginnerBuild').addEventListener('click', openControl);
    get('beginnerPreview').addEventListener('click', () => {
      basic(); select(tasks[taskIndex].example);
      if (taskIndex === 2) document.querySelector('button[data-width="mobile"]').click();
      showPreview();
    });
    get('beginnerCode').addEventListener('click', () => {
      focusVersion++;
      basic(); select(tasks[taskIndex].example);
      if (taskIndex === 3) DSStudio.inspector.show({ section: 'all', language: 'html' }); else showCode();
    });
    get('beginnerDone').addEventListener('click', () => { tried.add(taskIndex); setTask(Math.min(taskIndex + 1, tasks.length - 1)); });
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
    for (const button of document.querySelectorAll('[data-workspace]')) button.addEventListener('click', () => navigate(button.dataset.workspace));
    const nav = get('workspaceNav');
    new ResizeObserver(() => {
      const root = document.documentElement, height = `${Math.ceil(nav.getBoundingClientRect().height)}px`;
      if (root.style.getPropertyValue('--workspace-nav-height') !== height) {
        root.style.setProperty('--workspace-nav-height', height);
        window.dispatchEvent(new Event('resize'));
      }
    }).observe(nav);
    DSStudio.learning = { get picking() { return picking; } };
    setTask(0);
  }
});
