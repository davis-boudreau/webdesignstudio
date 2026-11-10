'use strict';
/* Optional teaching/export target. Never contributes to website CSS or project JSON. */
DSStudio.register({
  id: 'tailwind-bridge', title: 'Trace project tokens into Tailwind v4',
  init() {
    const get = id => document.getElementById(id);
    const deliver = get('studio-section-6');
    const lesson = deliver.querySelector('.studio-lesson');
    const bridge = document.createElement('section');
    bridge.id = 'tailwindBridge';
    bridge.className = 'tailwind-bridge';
    bridge.setAttribute('aria-labelledby', 'tailwindTitle');
    // Authored markup only. Project values below enter through textContent.
    bridge.innerHTML = `<h4 id="tailwindTitle">From CSS tokens to Tailwind utilities</h4>
      <p><strong>Optional next step.</strong> Your local CSS is a complete way to build this website. Start here when you can explain the component rule and the small utility in <a href="#utilityLesson">Spacing's local CSS lesson</a>.</p>
      <p>A design token records a decision. Your page uses it in component CSS; a Tailwind utility can use the same decision through a theme alias.</p>
      <p><strong>The learning transition:</strong> local component <code>.card { padding: var(--space-6); }</code> → local utility <code>.p-6 { padding: var(--space-6); }</code> → Tailwind-generated <code>p-6</code>. The first groups card styles; the second is one rule you author; the third is generated in your Tailwind practice project. The spacing decision stays shared.</p>
      <p>In the optional local utility exercise, you write the <code>p-6</code> rule in a practice copy. In a Tailwind project, Tailwind generates that utility from its configured spacing theme. The familiar class name connects the two exercises; it needs the corresponding CSS in each project. Project names such as <code>bg-surface</code> and <code>rounded-card</code> need the theme mapping below. The live website inspector keeps the local component CSS.</p>
      <p><strong>Transition exercise:</strong> keep your local website as a reference. In a separate Tailwind v4 practice project, import the theme source below, use the four classes shown here on one article, then compile. Inspect its generated CSS and compare the four computed properties with the local example before moving on to responsive styles or interaction states. Choose the approach that keeps your project understandable and manageable.</p>
      <p><strong>Try it:</strong> change Spacing or a Semantic colour, then return here. Follow the updated value from the project token to its Tailwind name.</p>
      <p class="help" id="tailwindContext"></p>
      <div class="tailwind-example-pair">
        <section aria-labelledby="tailwindCssTitle"><h5 id="tailwindCssTitle">Component CSS</h5><pre><code id="tailwindCssExample">.mapped-example {
  padding: var(--space-6);
  background-color: var(--surface);
  color: var(--text);
  border-radius: var(--radius-base);
}</code></pre></section>
        <section aria-labelledby="tailwindHtmlTitle"><h5 id="tailwindHtmlTitle">Tailwind HTML</h5><pre><code id="tailwindHtmlExample"></code></pre></section>
      </div>
      <p id="tailwindSpacingExample"></p>
      <p class="help">These examples express the same four properties. A complete card still needs its other component rules; this does not convert the page's HTML or reproduce every component state.</p>
      <details id="tailwindMappings"><summary>Explore the live token mappings</summary>
        <div class="tailwind-table-scroll" role="region" aria-label="Project to Tailwind token mappings" tabindex="0"><table>
          <caption>Project token → Tailwind theme name → example utility</caption>
          <thead><tr><th scope="col">Project source</th><th scope="col">Current value</th><th scope="col">Tailwind theme name</th><th scope="col">Example utility</th></tr></thead>
          <tbody id="tailwindMappingRows"></tbody>
        </table></div>
      </details>
      <div class="button-row">
        <button type="button" id="tailwindInspect">Inspect website CSS</button>
        <button type="button" id="tailwindCopy">Copy Tailwind theme source</button>
        <button type="button" id="tailwindDownload">Download Tailwind theme source</button>
      </div>
      <p class="help" role="status" id="tailwindStatus"></p>
      <details id="tailwindSourceDetails"><summary>Read the Tailwind v4 theme source and setup</summary>
        <p>The source includes a snapshot of the mapped project tokens for both themes. Import it after Tailwind in an existing Tailwind v4 project and compile with that project's build tools. Download it again after changing your design.</p>
        <pre><code>@import "tailwindcss";
@import "./tailwind-theme.css";</code></pre>
        <p class="help">The theme source maps foundations, not the whole website. Fonts need their matching installed family or font files. Tailwind's reset and utilities affect the consuming project; review its forms, headings and lists. Your Studio preview continues to use the existing website CSS.</p>
        <pre><code id="tailwindSource"></code></pre>
        <p class="help">Semantic colour utilities follow <code>data-theme="dark"</code>. The custom dark variant also enables explicit <code>dark:</code> utilities. Breakpoint values are emitted as literal lengths; CSS variables cannot supply media-query conditions. Their utilities apply at and above each cutoff.</p>
        <p class="learning-reference">Official guidance: <a href="https://tailwindcss.com/docs/theme">Tailwind theme variables</a>, <a href="https://tailwindcss.com/docs/dark-mode">dark mode</a> and <a href="https://tailwindcss.com/docs/installation/tailwind-cli">local compilation</a>.</p>
      </details>`;
    lesson.append(bridge);
    get('tailwindHtmlExample').textContent = '<article class="p-6 bg-surface text-content rounded-card">\n  Your content\n</article>';

    const mappings = [
      ['--primary', '--color-primary', 'bg-primary'],
      ['--on-primary', '--color-on-primary', 'text-on-primary'],
      ['--primary-hover', '--color-primary-hover', 'hover:bg-primary-hover'],
      ['--secondary', '--color-secondary', 'bg-secondary'],
      ['--on-secondary', '--color-on-secondary', 'text-on-secondary'],
      ['--accent', '--color-accent', 'bg-accent'],
      ['--on-accent', '--color-on-accent', 'text-on-accent'],
      ['--surface', '--color-surface', 'bg-surface'],
      ['--surface-muted', '--color-surface-muted', 'bg-surface-muted'],
      ['--text', '--color-content', 'text-content'],
      ['--text-muted', '--color-content-muted', 'text-content-muted'],
      ['--border', '--color-divider', 'border-divider'],
      ['--control-border', '--color-control-border', 'border-control-border'],
      ['--focus', '--color-focus', 'outline-focus'],
      ['--success', '--color-success', 'text-success'],
      ['--warning', '--color-warning', 'text-warning'],
      ['--danger', '--color-danger', 'text-danger'],
      ['--space-unit', '--spacing', 'p-6 / gap-6'],
      ['--radius-base', '--radius-card', 'rounded-card'],
      ['--button-radius', '--radius-button', 'rounded-button'],
      ['--font-body', '--font-sans', 'font-sans'],
      ['--font-heading', '--font-display', 'font-display'],
      ['--text-body', '--text-page-body', 'text-page-body'],
      ['--text-display', '--text-page-display', 'text-page-display']
    ];
    const breakpointRows = [
      ['Saved stacking cutoff', '--breakpoint-page-stack', 'page-stack:grid-cols-2'],
      ['Saved wide cutoff', '--breakpoint-page-wide', 'page-wide:px-8']
    ];
    const cells = [...mappings, ...breakpointRows].map(([source, target, utility]) => {
      const row = document.createElement('tr');
      row.dataset.source = source;
      const values = [source, '', target, utility].map((text, index) => {
        const cell = document.createElement(index === 0 ? 'th' : 'td');
        if (index === 0) cell.scope = 'row';
        const code = document.createElement('code'); code.textContent = text;
        cell.append(code); row.append(cell); return code;
      });
      get('tailwindMappingRows').append(row);
      return values[1];
    });

    let previousCss = '', cached;
    function snapshot() {
      const css = cssExport();
      // Read the actual export rather than recreate font, palette or type logic.
      if (!cached || css !== previousCss) {
        const rows = window.dssReadTokens(css);
        const base = new Map(), dark = new Map();
        for (const row of rows) (row.scope === 'Dark' ? dark : base).set(row.name, row.value);
        const sources = [...new Set(mappings.map(row => row[0]))];
        if (sources.some(name => !base.has(name))) throw new Error('A mapped project token is missing from the CSS export.');
        const declarations = map => sources.filter(name => map.has(name)).map(name => `    ${name}: ${map.get(name)};`).join('\n');
        cached = { base, dark, declarations: declarations(base), darkDeclarations: declarations(dark) };
        previousCss = css;
      }
      const responsive = DSStudio.responsive.settings();
      const breakpoints = [responsive.stack, responsive.wide].map(DSStudio.responsive.rem);
      const source = `/* Tailwind v4 theme source: mapped project tokens, light and dark.
   Import after Tailwind and compile in your consuming project.
   This snapshot contains no website component rules or HTML conversion.
   Font families need their installed fonts or separately loaded font files. */
@layer theme {
  :root {
${cached.declarations}
  }
  [data-theme="dark"] {
${cached.darkDeclarations}
  }
}
@theme inline {
${mappings.map(([from, to]) => `  ${to}: var(${from});`).join('\n')}
}
@theme {
  --breakpoint-page-stack: ${breakpoints[0]};
  --breakpoint-page-wide: ${breakpoints[1]};
}
@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *));
`;
      const active = new Map(cached.base);
      if (state.theme === 'dark') for (const [name, value] of cached.dark) active.set(name, value);
      return { source, active, breakpoints };
    }
    DSStudio.tailwind = Object.freeze({ source: () => snapshot().source });
    const setText = (node, text) => { if (node.textContent !== text) node.textContent = text; };
    let renderedSource = '';
    function sync(force = false) {
      if (!force && !deliver.open) return;
      const view = snapshot();
      mappings.forEach(([from], index) => setText(cells[index], view.active.get(from)));
      view.breakpoints.forEach((value, index) => setText(cells[mappings.length + index], value));
      setText(get('tailwindContext'), `${state.theme === 'dark' ? 'Dark' : 'Light'} page theme. Basic and Advanced share these foundations; Studio appearance is independent.`);
      const unit = view.active.get('--space-unit');
      // Bounded pixel source emitted by the existing generator, never CSS evaluation.
      const pixels = /^\d+(?:\.\d+)?px$/.test(unit) ? Number.parseFloat(unit) * 6 : null;
      setText(get('tailwindSpacingExample'), `Current spacing: --space-unit is ${unit}. The supplied theme maps --spacing to --space-unit. The component's --space-6, the local p-6 exercise and Tailwind p-6 with that mapping all use six units${pixels === null ? '.' : `, giving ${round(pixels, 2)}px of padding.`}`);
      if (view.source !== renderedSource) {
        setText(get('tailwindSource'), view.source);
        get('tailwindStatus').textContent = '';
        renderedSource = view.source;
      }
    }
    get('tailwindInspect').addEventListener('click', () => DSStudio.inspector.show({ language: 'css', section: 'all', find: '--space-unit:' }));
    get('tailwindDownload').addEventListener('click', () => {
      sync(true);
      download('tailwind-theme.css', snapshot().source, 'text/css');
      get('tailwindStatus').textContent = 'tailwind-theme.css download requested. Import and compile it in your Tailwind v4 project.';
    });
    get('tailwindCopy').addEventListener('click', async () => {
      sync(true);
      const source = snapshot().source;
      try {
        await navigator.clipboard.writeText(source);
        get('tailwindStatus').textContent = snapshot().source === source ? 'Tailwind theme source copied.' : 'Copied the earlier theme source. Copy again for the latest settings.';
      } catch {
        get('tailwindSourceDetails').open = true;
        get('tailwindStatus').textContent = 'Clipboard unavailable. Select the theme source below and copy it manually.';
      }
    });
    let queued = false;
    const schedule = () => {
      if (queued) return;
      queued = true;
      queueMicrotask(() => { queued = false; sync(); });
    };
    const previousRender = renderCode;
    renderCode = function() { previousRender(); schedule(); };
    deliver.addEventListener('toggle', () => { if (deliver.open) sync(true); });
    DSStudio.on('stage:change', schedule);
    sync(true);
  }
});
