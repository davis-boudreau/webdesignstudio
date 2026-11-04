'use strict';
/* Authored teaching content plus current generated output. Comparison and notes
   are session UI state; they never change project values or exported files. */
DSStudio.register({
  id: 'spacing-lesson', title: 'Learn spacing through your current design',
  init() {
    const get = id => document.getElementById(id);
    const stage = DSStudio.stages.find(item => item.id === 'spacing');
    const section = get(stage.lesson), lesson = section.querySelector(':scope > .panel > .studio-lesson');
    const examples = {
      basic: { label: 'Basic', id: 'lists', selector: '.section' },
      advanced: { label: 'Advanced', id: 'services', selector: '.sample-section' }
    };
    lesson.classList.add('spacing-lesson');
    // Fixed authored markup only. All live values/output enter through textContent.
    lesson.innerHTML = `<h3>One spacing decision, related spaces</h3>
      <section><h4>Understand</h4><p>A spacing unit is a reusable foundation. A rule can use a multiple of that unit for padding, margins or gaps. Changing the unit updates every place that uses those related tokens. Responsive rules can choose different multiples at different widths.</p></section>
      <section><h4>Try</h4><p id="spacingPrompt" class="step-task"></p><div class="button-row"><button id="spacingEdit" type="button">Change the spacing unit</button></div><span data-stage-controls hidden></span></section>
      <section><h4>Observe</h4><p id="spacingContext" class="help"></p>
        <div class="spacing-table-scroll" tabindex="0" aria-label="Spacing token comparison">
          <table><caption>Compare your spacing values</caption><thead><tr><th scope="col">Token</th><th scope="col">Before</th><th scope="col">Now</th></tr></thead>
          <tbody><tr><th scope="row"><code>--space-unit</code></th><td id="spacingBeforeUnit"></td><td id="spacingNowUnit"></td></tr>
          <tr><th scope="row"><code>--space-4</code></th><td id="spacingBefore4"></td><td id="spacingNow4"></td></tr>
          <tr><th scope="row"><code>--space-8</code></th><td id="spacingBefore8"></td><td id="spacingNow8"></td></tr></tbody></table>
        </div>
        <p id="spacingObservation" role="status" aria-live="polite" aria-atomic="true"></p><p id="spacingGapNote" class="help"></p>
        <div class="button-row"><button id="spacingExample" type="button">Show section in preview</button><button id="spacingCompare" type="button">Compare from current values</button></div>
        <p class="help">The comparison starts when you open this lesson. It stays for this session; loading or resetting a project clears it. Changing colours, themes or samples does not restart it.</p>
      </section>
      <section><h4>Inspect</h4><p id="spacingConnection"></p>
        <pre id="spacingHtml" tabindex="0" aria-label="Section opening tag from the current HTML export"></pre>
        <pre id="spacingCss" tabindex="0" aria-label="Spacing declarations and section rule from the current CSS export"></pre>
        <div class="button-row step-output"><button id="spacingInspectTokens" type="button" data-inspect="css">Inspect spacing tokens</button><button id="spacingInspectRule" type="button">Inspect section CSS</button><button id="spacingInspectHtml" type="button" data-inspect="html">Inspect section HTML</button></div>
        <p class="help">These are excerpts. The inspector opens complete files, including shared rules and responsive overrides. Opening it can narrow a Fluid preview and change which responsive rule applies. Other properties, such as grid gap, have their own controls.</p>
      </section>
      <section><h4>Reflect</h4><p>Which spaces changed together, and why? Did the new spacing make the content easier to scan? Explain why you would keep or revise this choice.</p>
        <details><summary>Write a reflection (optional)</summary><div class="field"><label for="spacingReflection">Your explanation</label><textarea id="spacingReflection" rows="3" maxlength="600" aria-describedby="spacingReflectionHelp"></textarea><p id="spacingReflectionHelp" class="help">Notes stay in this tab only. They are not saved in project JSON or website files. Trying the task does not prove understanding.</p></div></details>
      </section>`;

    let project = state, baseline = null, lastSignature = '', focusVersion = 0;
    const setText = (id, text) => { if (get(id).textContent !== text) get(id).textContent = text; };
    const format = value => Number.isFinite(value) ? `${Number(value.toFixed(2))} px` : 'See CSS';
    function readScale(css) {
      const rows = window.dssReadTokens(css).filter(row => row.scope === 'Light / base');
      const values = Object.fromEntries(rows.map(row => [row.name, row.value]));
      const number = value => /^\d+(?:\.\d+)?px$/.test(value || '') ? parseFloat(value) : NaN;
      const unit = number(values['--space-unit']);
      const multiple = n => {
        const raw = values[`--space-${n}`];
        // Recognize only the generator's known arithmetic, never evaluate CSS.
        return raw === `calc(var(--space-unit) * ${n})` ? unit * n : number(raw);
      };
      return { unit, four: multiple(4), eight: multiple(8), gap: values['--grid-gap'] || 'See complete CSS', values, multiple };
    }
    function rule(css, selector) {
      const start = css.indexOf(selector + ' {');
      const end = start < 0 ? -1 : css.indexOf('}', start);
      return end < 0 ? '' : css.slice(start, end + 1);
    }
    function sectionRules(css, example, view) {
      const base = rule(css, example.selector);
      const rules = [base];
      let active = { token: '--space-8', multiplier: 8, responsive: false };
      // Follow the fixed sample's authored padding rules in source order, using
      // their actual exported media queries rather than a second breakpoint map.
      const responsiveStart = css.indexOf('/* SECTION: responsive */');
      if (example === examples.basic && responsiveStart >= 0) {
        let pos = css.indexOf(example.selector + ' {', responsiveStart);
        while (pos >= 0) {
          const block = rule(css.slice(pos), example.selector);
          const token = block.match(/padding-block:\s*var\((--space-(\d+))\)/);
          const media = css.lastIndexOf('@media', pos);
          if (token && media >= responsiveStart) {
            const header = css.slice(media, css.indexOf('{', media)).trim();
            rules.push(`${header} {\n  ${block}\n}`);
            if (view?.matchMedia(header.slice(6).trim()).matches)
              active = { token: token[1], multiplier: Number(token[2]), responsive: true };
          }
          pos = css.indexOf(example.selector + ' {', pos + example.selector.length + 2);
        }
      }
      return { base, excerpt: rules.join('\n\n'), active };
    }
    function sync() {
      if (project !== state) {
        project = state; baseline = null; lastSignature = ''; focusVersion++;
        get('spacingReflection').value = '';
      }
      const css = cssExport();
      const current = readScale(css);
      if (!baseline && (section.open || DSStudio.activeStage === stage.index)) baseline = current;
      const example = examples[state.sampleMode === 'basic' ? 'basic' : 'advanced'];
      const doc = get('previewPage').contentDocument, view = doc?.defaultView;
      const selectedSection = doc?.getElementById(example.id);
      const livePadding = selectedSection ? parseFloat(view.getComputedStyle(selectedSection).paddingBlockStart) : NaN;
      const connections = sectionRules(css, example, view);
      const { token, multiplier, responsive } = connections.active;
      const signature = `${state.sampleMode}|${state.theme}|${baseline?.unit}|${baseline?.gap}|${view?.innerWidth}|${livePadding}|${token}|${css}`;
      if (signature === lastSignature) return;
      lastSignature = signature;
      const start = baseline || current;
      const min = Number(get('jSpacing').min), max = Number(get('jSpacing').max);
      const target = Math.min(max, Math.max(min, Math.round(start.unit) + (start.unit <= max - 2 ? 2 : -2)));
      setText('spacingPrompt', `Try changing the base spacing unit from ${format(start.unit)} to ${format(target)}. Predict what will happen to section padding before you move the control.`);
      for (const [suffix, key] of [['Unit','unit'], ['4','four'], ['8','eight']]) {
        setText('spacingBefore' + suffix, baseline ? format(start[key]) : '—');
        setText('spacingNow' + suffix, format(current[key]));
      }
      setText('spacingContext', `${example.label} sample · ${state.theme === 'dark' ? 'Dark' : 'Light'} theme · ${view?.innerWidth || 'Unknown'} px preview. Spacing tokens are shared by both themes. “Before” is a session comparison, not a saved project version.`);
      let observation = 'Open this lesson to start comparing values.';
      if (baseline) observation = start.unit === current.unit ?
        `Your unit is ${format(current.unit)}. Four units make ${format(current.four)}; eight units make ${format(current.eight)}. Change the unit to compare the result.` :
        `Your unit changed from ${format(start.unit)} to ${format(current.unit)}. Four-unit spacing changed from ${format(start.four)} to ${format(current.four)}, and eight-unit spacing from ${format(start.eight)} to ${format(current.eight)}. Both follow the same foundation.`;
      setText('spacingObservation', observation);
      setText('spacingGapNote', !baseline || start.gap === current.gap ?
        `Grid gap is ${current.gap}. It has its own Responsive layout control; changing the spacing unit alone does not change it.` :
        `Grid gap is now ${current.gap} (comparison: ${start.gap}). This is a separate decision in Responsive layout, rather than a multiple of the spacing unit.`);
      const usesSpacing = connections.base.includes('padding-block: var(--space-8)');
      setText('spacingConnection', usesSpacing ?
        `${example.selector} matches the selected section in your ${example.label} page. ${responsive ? 'A responsive rule overrides its base --space-8 padding.' : 'Its base padding rule applies.'} At this preview width, padding-block uses ${token} (${format(current.multiple(multiplier))}) at the start and end. ${Number.isFinite(livePadding) ? `The page currently measures ${format(livePadding)} per edge.` : 'Show the section in the preview to measure it.'} The class connects the HTML element to its CSS rule.` :
        'Inspect the current section rule and complete stylesheet to follow its spacing dependencies.');
      const html = htmlExport();
      const openingTag = html.match(new RegExp(`<section\\b[^>]*\\bid="${example.id}"[^>]*>`));
      setText('spacingHtml', openingTag ? openingTag[0] : 'Inspect the complete HTML for this section.');
      const declarations = ['--space-unit','--space-4','--space-8', ...(example === examples.basic ? ['--space-12','--space-16'] : [])].map(name => `  ${name}: ${current.values[name] || '/* See complete CSS */'};`).join('\n');
      setText('spacingCss', `/* Relevant declarations and section rules from the current export. */\n:root {\n${declarations}\n}\n\n${connections.excerpt || '/* Inspect the complete CSS for this section. */'}`);
    }
    get('spacingEdit').addEventListener('click', () => {
      focusVersion++;
      const row = window.dssReadTokens().find(item => item.name === '--space-unit');
      if (row) window.dssConfigureToken(row);
    });
    get('spacingCompare').addEventListener('click', () => {
      baseline = readScale(cssExport()); lastSignature = ''; sync();
    });
    get('spacingExample').addEventListener('click', () => {
      const mode = state.sampleMode, example = examples[mode === 'basic' ? 'basic' : 'advanced'];
      window.dssRevealSection('previewShell', false);
      const shell = get('previewShell');
      shell.scrollIntoView({ block: 'start', behavior: 'instant' }); shell.focus({ preventScroll: true });
      const version = ++focusVersion;
      queueMicrotask(() => {
        if (version !== focusVersion || mode !== state.sampleMode || document.activeElement !== shell) return;
        const doc = get('previewPage').contentDocument, target = doc?.getElementById(example.id);
        if (!target) return;
        target.tabIndex = -1;
        doc.defaultView.scrollTo({ top: doc.defaultView.scrollY + target.getBoundingClientRect().top - 24, behavior: 'instant' });
        target.focus({ preventScroll: true });
      });
    });
    for (const [id, language, find] of [
      ['spacingInspectTokens','css', () => '--space-unit:'],
      ['spacingInspectRule','css', () => examples[state.sampleMode === 'basic' ? 'basic' : 'advanced'].selector + ' {'],
      ['spacingInspectHtml','html', () => `id="${examples[state.sampleMode === 'basic' ? 'basic' : 'advanced'].id}"`]
    ]) get(id).addEventListener('click', () => {
      focusVersion++;
      DSStudio.inspector.show({ language, section: 'all', find: find() });
    });
    DSStudio.on('stage:change', () => { focusVersion++; sync(); });
    // Imports can refresh several legacy generators in one call. Read after the
    // stack settles so a fresh comparison never captures intermediate settings.
    let queued = false;
    const schedule = () => {
      if (queued) return;
      queued = true;
      // Preview rendering is queued by another listener in the same turn.
      queueMicrotask(() => queueMicrotask(() => { queued = false; sync(); }));
    };
    DSStudio.on('inspector:change', schedule);
    DSStudio.on('preview:change', schedule);
    get('previewPage').addEventListener('load', schedule);
    section.addEventListener('toggle', () => { if (section.open) sync(); });
    // Also clear comparison when a reset/import reloads identical project values.
    for (const event of ['dss:reset','dss:imported']) document.addEventListener(event, () => {
      baseline = null; lastSignature = ''; get('spacingReflection').value = ''; sync();
    });
    DSStudio.emit('lesson:content', { id: stage.id });
    sync();
  }
});
