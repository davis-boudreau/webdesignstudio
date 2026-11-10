'use strict';
/* Teach real exported classes without turning Studio controls into specimens. */
DSStudio.register({
  id: 'utility-lesson', title: 'Trace HTML classes into CSS and design tokens',
  init() {
    const get = id => document.getElementById(id);
    const section = get('studio-section-3');
    const lesson = section.querySelector('.studio-lesson');
    const content = document.createElement('section');
    content.id = 'utilityLesson'; content.className = 'utility-lesson';
    content.setAttribute('aria-labelledby', 'utilityTitle');
    // Static authored content only; all project/output values use textContent.
    content.innerHTML = `<h4 id="utilityTitle">Read a class, follow its CSS</h4>
      <p><strong>Start with local CSS.</strong> Keep meaning in HTML and put reusable styling in one linked stylesheet. A class such as <code>card</code> groups the rules for a repeated component. Reuse it instead of copying those declarations onto every article. Use shared tokens for values you want to change together.</p>
      <p>This minimal example uses the base <code>card</code> rule from your current exported stylesheet. Sample cards reuse component classes. The live inspector, preview and website downloads all use the same local CSS and HTML. The complete page also has layout, typography and component rules.</p>
      <pre id="localCardHtml" tabindex="0" aria-label="Minimal HTML example using the local stylesheet"></pre>
      <pre id="localCardCss" tabindex="0" aria-label="Base card rule from the current CSS export"></pre>
      <div class="button-row"><button id="localInspectCss" type="button">Inspect card CSS</button></div>
      <p><strong>The learning transition: one spacing decision, three ways to apply it.</strong> The examples below focus on padding; a complete card has other rules too.</p>
      <ol id="cssLearningTransition" aria-label="Learning transition from local component CSS to Tailwind">
        <li><strong>Local component:</strong> <code>.card { padding: var(--space-6); }</code> keeps padding with the card's other reusable styles.</li>
        <li><strong>Local utility:</strong> <code>.p-6 { padding: var(--space-6); }</code> gives one class one job. You write this optional rule in a practice stylesheet.</li>
        <li><strong>Tailwind:</strong> generates <code>p-6</code> using the mapped spacing theme in the separate Tailwind exercise.</li>
      </ol>
      <p>A token stores the decision; a class applies it to an HTML element. Here, <code>--space-6</code> means six spacing units. The supplied Tailwind theme maps <code>--spacing</code> to <code>--space-unit</code>, so its <code>p-6</code> also uses six units. A matching class name needs the corresponding CSS; Tailwind needs setup and compilation. The live inspector and website exports stay with local component CSS, which is a complete way to finish your site.</p>
      <p><strong>Try first:</strong> save the HTML and CSS exports together, then open the HTML in a browser. Find <code>.card</code> in <code>tokens.css</code> and follow its spacing token. A shared component rule is a useful starting point when several cards should change together. Keep this approach for as long as it makes your page easy to understand.</p>
      <details id="utilityPractice"><summary>Next: try one local utility class</summary>
      <p><code>&lt;article&gt;</code> identifies self-contained content. A utility is an ordinary CSS class with one job, such as padding. Add one when you need to vary that property without changing every card. A framework is optional.</p>
      <p class="step-task"><strong>Try it in a practice copy:</strong> choose a class below. Copy its rule to the end of your copied <code>tokens.css</code> and add that class to this article in the copied HTML, as shown. Compare <code>p-6</code> with <code>p-4</code>, using one at a time, then reload your copy. The Studio preview and inspector keep the component version.</p>
      <p id="utilityContext" class="help"></p>
      <pre id="utilityHtml" tabindex="0" aria-label="Actual article opening tag from the HTML export"></pre>
      <div class="field"><label for="utilityClass">Class to trace</label><select id="utilityClass"></select></div>
      <pre id="utilityPracticeHtml" tabindex="0" aria-label="Practice article opening tag with one optional utility"></pre>
      <pre id="utilityRule" tabindex="0" aria-label="Optional utility rule to add to your practice stylesheet"></pre>
      <p id="utilityToken"></p><p id="utilityMeasured" class="help"></p>
      <div class="button-row"><button id="utilityPreview" type="button">Show component in preview</button><button id="utilityInspectHtml" type="button">Inspect component HTML</button><button id="utilityInspectCss" type="button">Inspect component CSS</button><button id="utilityConfigure" type="button">Configure source token</button></div>
      <p class="help">These optional rules are lesson examples, separate from the website files. Use one padding utility at a time: putting <code>p-4</code> after <code>p-6</code> in HTML does not make it win. Stylesheet order and selector specificity determine the result. Grid gap has its own setting; <code>gap-4</code> uses the spacing unit.</p>
      <details id="utilityVocabularyDetails"><summary>Explore the plain CSS utility vocabulary</summary><p>These ordinary CSS examples prepare you for later framework study. Add only a rule you need to your practice copy; the website export keeps its reusable component rules. No Tailwind installation or build is needed for this exercise. Colours and spacing follow your project, so always review contrast after changes.</p>
        <div class="utility-table-scroll" tabindex="0" role="region" aria-label="Available utility classes"><table><caption>One class, one CSS declaration</caption><thead><tr><th scope="col">Class</th><th scope="col">Declaration</th></tr></thead><tbody id="utilityVocabulary"></tbody></table></div>
      </details>
      <p><strong>Reflect:</strong> would you change the shared card rule or add a padding utility to just one article? Explain which cards should change and why.</p>
      </details>
      <p><strong>Optional next step:</strong> once you can explain the local rule, <a id="utilityToTailwind" href="#tailwindBridge">compare it with Tailwind in Deliver</a>. You can finish and export this website using local CSS.</p>`;
    lesson.append(content);
    get('localCardHtml').textContent = '<link rel="stylesheet" href="tokens.css">\n<article class="card">\n  <h3>A useful heading</h3>\n  <p>Your content.</p>\n</article>';
    const classes = ['p-6', 'p-4', 'bg-surface', 'text-content', 'rounded-card'];
    get('utilityClass').replaceChildren(...classes.map(name => new Option(name, name)));
    for (const item of DSStudio.utilities.definitions) {
      const row = document.createElement('tr'), name = document.createElement('th'), declaration = document.createElement('td');
      name.scope = 'row';
      for (const [cell, text] of [[name, item.name], [declaration, `${item.property}: ${item.value};`]]) {
        const code = document.createElement('code'); code.textContent = text; cell.append(code);
      }
      row.append(name, declaration); get('utilityVocabulary').append(row);
    }
    const example = () => state.sampleMode === 'basic' ? { id: 'basic-structure', label: 'Basic' } : { id: 'lesson-brief', label: 'Advanced' };
    const selected = () => DSStudio.utilities.definitions.find(item => item.name === get('utilityClass').value) || DSStudio.utilities.definitions.find(item => item.name === classes[0]);
    const setText = (id, text) => { if (get(id).textContent !== text) get(id).textContent = text; };
    let lastCss = '', tokens = [];
    function sync(force = false) {
      if (!force && !section.open) return;
      const css = cssExport(), html = htmlExport(), current = example(), item = selected();
      if (css !== lastCss) { tokens = window.dssReadTokens(css); lastCss = css; }
      const baseCard = css.match(/(?:^|\n)(\.card \{[^}]*\})/);
      const readableCard = baseCard?.[1].replace('{ ', '{\n  ').replace(/; /g, ';\n  ').replace('\n  }', '\n}');
      setText('localCardCss', readableCard || 'Inspect the complete CSS to find the card rule.');
      // IDs and selector names are authored above, never supplied by imported data.
      const opening = html.match(new RegExp('<article\\b[^>]*\\bid="' + current.id + '"[^>]*>'))?.[0];
      const rule = DSStudio.utilities.rule(item.name);
      setText('utilityHtml', opening || 'Inspect the complete HTML to find the article.');
      const practiceOpening = opening?.replace(/\bclass="([^"]*)"/, (_, names) => `class="${names} ${item.name}"`);
      setText('utilityPracticeHtml', practiceOpening || 'Add the selected class to your practice article.');
      setText('utilityRule', rule);
      const candidates = tokens.filter(row => row.name === item.token);
      const token = (state.theme === 'dark' ? candidates.findLast(row => row.scope === 'Dark') : null) || candidates.findLast(row => row.scope !== 'Dark');
      let explanation = `${item.token}: ${token?.value || 'See complete CSS'}.`;
      if (item.token?.startsWith('--space-')) {
        const unit = tokens.find(row => row.name === '--space-unit' && row.scope !== 'Dark');
        explanation += ` Its source is --space-unit: ${unit?.value || 'See complete CSS'}.`;
      }
      setText('utilityToken', explanation);
      setText('utilityContext', `${current.label} article · ${state.theme === 'dark' ? 'Dark' : 'Light'} page theme. First is the actual exported article; next is a practice version with one optional utility and its rule.`);
      const frame = get('previewPage'), article = frame.contentDocument?.getElementById(current.id);
      const measured = article && frame.contentWindow.getComputedStyle(article).getPropertyValue(item.property);
      setText('utilityMeasured', measured ? `Before the exercise, the component preview measures ${item.property}: ${measured}. The optional utility has not been applied to this preview.` : 'Open the page preview to measure this component.');
    }
    get('utilityClass').addEventListener('change', () => sync(true));
    get('utilityInspectHtml').addEventListener('click', () => DSStudio.inspector.show({ language: 'html', section: 'all', find: `id="${example().id}"` }));
    const inspectCard = () => DSStudio.inspector.show({ language: 'css', section: 'all', find: '.card {' });
    get('localInspectCss').addEventListener('click', inspectCard);
    get('utilityInspectCss').addEventListener('click', inspectCard);
    get('utilityConfigure').addEventListener('click', () => window.dssConfigureToken({ name: selected().token, scope: state.theme === 'dark' ? 'Dark' : 'Light / base' }));
    get('utilityPreview').addEventListener('click', () => {
      window.dssRevealSection('previewShell', false);
      const shell = get('previewShell');
      shell.scrollIntoView({ block: 'start', behavior: 'instant' });
      shell.focus({ preventScroll: true });
      const frame = get('previewPage'), article = frame.contentDocument?.getElementById(example().id);
      if (article) {
        frame.contentWindow.scrollTo({ top: frame.contentWindow.scrollY + article.getBoundingClientRect().top - 24, behavior: 'instant' });
        article.tabIndex = -1; article.focus({ preventScroll: true });
      }
    });
    let queued = false;
    const schedule = () => {
      if (queued) return;
      queued = true;
      queueMicrotask(() => { queued = false; sync(); });
    };
    // Existing preview events run after imports, font changes and rendering settle.
    DSStudio.on('preview:change', schedule);
    DSStudio.on('stage:change', schedule);
    section.addEventListener('toggle', () => { if (section.open) sync(true); });
    get('utilityPractice').addEventListener('toggle', () => { if (get('utilityPractice').open) sync(true); });
    sync(true);
  }
});
