'use strict';
/* Contrast inventory for the studio's defined colours and state samples.
   Ratios use unrounded values for decisions. Geometry, behaviour and meaning
   still require human review; this is not a page-wide conformance scanner. */
(() => {
  const get = id => document.getElementById(id);
  const container = get('contrastChecks');
  if (!container) return;
  const textStates = ['default', 'hover', 'focus', 'active', 'selected', 'disabled', 'loading'];
  const explorerStates = [...textStates, 'invalid', 'success', 'readonly'];
  const statusOrder = { review: 0, conditional: 1, pass: 2, candidate: 3, exempt: 4 };
  const stateOrder = Object.fromEntries(['default', 'hover', 'focus', 'active', 'selected', 'disabled', 'loading', 'invalid', 'success', 'warning', 'danger', 'readonly', 'candidate'].map((name, index) => [name, index]));
  const esc = value => escapeHtml(String(value));
  const rgb = colour => Array.isArray(colour) ? colour : hexRgb(colour);
  const blend = (fg, bg, opacity = 1) => rgb(fg).map((v, i) => v * opacity + rgb(bg)[i] * (1 - opacity));
  const brighten = (colour, factor) => rgb(colour).map(v => v * factor);
  const luminance = colour => rgb(colour).map(srgbToLinear).reduce((sum, channel, i) => sum + channel * [.2126, .7152, .0722][i], 0);
  const title = value => value.charAt(0).toUpperCase() + value.slice(1);
  let rows = [], queued = false;
  const openGroups = new Set();

  function targetsFor(row, button, foundation, palettes) {
    const r = palettes[row.theme].roles;
    const semantic = key => SEMANTIC_COLOUR_KEYS.includes(key) ? {
      type: 'semantic', theme: row.theme, key, value: r[key],
      label: `${title(row.theme)}: --${key}`
    } : null;
    const anchor = key => ({ type: 'anchor', key, value: foundation[key], label: `${title(key)} palette anchor (both themes)` });
    const variant = row.name.split(' ')[0].toLowerCase();
    const c = button.themes[row.theme][variant];
    const buttonTarget = property => ({
      type: 'button', variant, property,
      value: property === 'focus' ? button.settings.focus :
        ({ text: c.fg, bg: c.bg, hoverText: c.hoverText, activeText: c.activeText, hover: c.hover, active: c.active, border: c.border })[property] === 'transparent' ?
          (r[row.location] || r.surface) : ({ text: c.fg, bg: c.bg, hoverText: c.hoverText, activeText: c.activeText, hover: c.hover, active: c.active, border: c.border })[property],
      label: `${property === 'focus' ? 'All buttons' : title(variant)}: ${property} (both themes)`
    });
    let targets = [];
    if (row.group.startsWith('Button Laboratory:')) {
      if (row.name.includes('ring')) targets = [buttonTarget('focus')];
      else if (row.name.includes('boundary')) targets = [buttonTarget('border'), buttonTarget(row.state === 'hover' ? 'hover' : row.state === 'active' ? 'active' : 'bg')];
      else targets = [buttonTarget(row.state === 'hover' ? 'hoverText' : row.state === 'active' ? 'activeText' : 'text'),
        buttonTarget(row.state === 'hover' ? 'hover' : row.state === 'active' ? 'active' : 'bg')];
      targets.push(semantic(row.location));
    } else if (row.group === 'Swatch candidates: reference and ramps') {
      const match = row.name.match(/^(primary|secondary|accent)-\d+ /);
      if (match) targets.push(anchor(match[1]));
      if (row.name.endsWith('/ semantic text')) targets.push(semantic('text'));
    } else if (row.group === 'Text and semantic roles') {
      const match = row.name.match(/^--([\w-]+)/);
      targets = [semantic(match ? match[1] : 'primary'), semantic(row.location.replace(/^--/, ''))];
    } else if (row.group === 'Boundaries and indicators') {
      const match = row.name.match(/^--(\w+)/);
      targets = [semantic(match ? match[1] : row.name.includes('focus') ? 'focus' : 'control-border'), semantic(row.location.replace(/^--/, ''))];
    } else if (row.group === 'Surfaces and opacity') {
      targets = [semantic(row.name.endsWith('--text-muted') ? 'text-muted' : 'text'), semantic(row.name.startsWith('Nested') ? 'surface-muted' : 'surface')];
    } else {
      if (row.name.includes('input text')) targets = [semantic('text'), semantic(row.state === 'readonly' ? 'surface-muted' : 'surface')];
      else if (row.name.includes('input border') || row.name === 'Input feedback outline')
        targets = [semantic(row.state === 'invalid' ? 'danger' : row.state === 'success' ? 'success' : 'control-border'), semantic(row.state === 'readonly' ? 'surface-muted' : 'surface')];
      else if (row.name.includes('focus')) targets = [semantic('focus'), semantic('surface')];
      else if (row.name.includes('selected tile')) targets = [semantic('primary'), semantic('surface')];
      else if (row.name.startsWith('General ')) targets = [semantic(row.name.includes('secondary') ? 'on-secondary' : 'on-primary'), semantic('primary-hover')];
      else targets = [semantic('on-primary'), semantic(row.state === 'hover' ? 'primary-hover' : 'primary')];
    }
    return targets.filter(Boolean).filter((target, index, all) => all.findIndex(other => JSON.stringify(other) === JSON.stringify(target)) === index);
  }

  function collect(configuration = {}) {
    const result = [];
    const foundation = configuration.foundation || state;
    const button = window.dssGetButtonContrastData(configuration.buttonSettings, foundation);
    const palettes = Object.fromEntries(['light', 'dark'].map(theme => [theme, palette(theme, foundation)]));
    const add = (theme, group, name, stateName, location, fg, bg, threshold = 4.5, note = '', scope = 'required') => {
      const [light, dark] = [luminance(fg), luminance(bg)].sort((a, b) => b - a);
      const ratio = (light + .05) / (dark + .05);
      result.push({ theme, group, name, state: stateName, location, fg: rgbHex(rgb(fg)), bg: rgbHex(rgb(bg)), threshold, ratio, note, scope,
        status: threshold === null ? 'exempt' : ['candidate', 'potential'].includes(scope) ? 'candidate' : scope === 'conditional' ? 'conditional' : ratio >= threshold ? 'pass' : 'review' });
    };
    for (const theme of ['light', 'dark']) {
      const { roles: r, p, s, a } = palettes[theme];
      const surfaces = ['background', 'surface', 'surface-muted'];
      for (const bg of surfaces) {
        for (const fg of ['text', 'text-muted'])
          add(theme, 'Text and semantic roles', `--${fg}`, 'default', `--${bg}`, r[fg], r[bg]);
        add(theme, 'Text and semantic roles', 'Link text (--primary)', 'default', `--${bg}`, r.primary, r[bg], 4.5, 'Check a non-colour cue such as an underline separately; custom visited or hover styles need their own review.');
        for (const fg of ['success', 'warning', 'danger']) {
          add(theme, 'Text and semantic roles', `--${fg} message text`, fg === 'danger' ? 'invalid' : fg, `--${bg}`, r[fg], r[bg], 4.5, 'Potential use as text; the sample alerts use ordinary body text. This is not a current text failure.', 'potential');
          add(theme, 'Boundaries and indicators', `--${fg} status indicator`, fg === 'danger' ? 'invalid' : fg, `--${bg}`, r[fg], r[bg], 3, 'Only required when this colour is necessary to identify status; also provide words or an icon.', 'conditional');
        }
        add(theme, 'Boundaries and indicators', 'Semantic focus ring', 'focus', `--${bg}`, r.focus, r[bg], 3, 'Colour check only; verify visibility, area, placement and that focus is not obscured.');
        add(theme, 'Boundaries and indicators', 'Control border', 'default', `--${bg}`, r['control-border'], r[bg], 3, 'Potential host context: necessary input boundaries need contrast; decorative borders have their own --border role.', 'conditional');
      }
      for (const variant of ['primary', 'secondary', 'accent'])
        add(theme, 'Text and semantic roles', `--on-${variant}`, 'default', `--${variant}`, r['on-' + variant], r[variant]);

      // Both the state matrix and selected sample use theme surfaces; the
      // side-by-side theme cards have one additional, fixed dark background.
      const hosts = surfaces.map(key => [key, r[key]]);
      const comparison = theme === 'dark' ? '#142434' : '#FFFFFF';
      if (!hosts.some(([, hex]) => hex.toUpperCase() === comparison)) hosts.push(['theme comparison card', comparison]);
      for (const [variant, c] of Object.entries(button.themes[theme])) {
        for (const [host, surround] of hosts) {
          const base = c.bg === 'transparent' ? surround : c.bg;
          for (const st of textStates) {
            const bg = st === 'hover' ? c.hover : st === 'active' ? c.active : base;
            const fg = st === 'hover' ? c.hoverText : st === 'active' ? c.activeText : c.fg;
            const alpha = st === 'disabled' ? .55 : st === 'loading' ? .8 : 1;
            const disabled = st === 'disabled';
            add(theme, 'Button Laboratory: text', title(variant), st, host,
              blend(fg, surround, alpha), blend(bg, surround, alpha), disabled ? null : 4.5,
              disabled ? 'Native disabled control: contrast exemption; ratio shown for information.' :
                st === 'loading' ? 'Matrix simulation uses 0.8 opacity. A busy button is not automatically disabled.' :
                st === 'focus' ? 'Text stays the default colour; focus ring checked separately.' :
                st === 'selected' ? 'Toggle text stays the default colour; selection ring checked separately.' : 'Resolved button colours on the named surrounding surface.');
            if (st === 'loading')
              add(theme, 'Button Laboratory: text', `${title(variant)} live/export loading`, st, host, fg, bg, 4.5,
                'The live/export busy button keeps full opacity; application logic determines whether it is disabled.');
            // Border/fill is conditional: a text label can identify an action
            // without a high-contrast enclosing rectangle.
            if (!disabled && variant !== 'text') {
              const edge = c.border === 'transparent' ? bg : c.border;
              add(theme, 'Button Laboratory: indicators', `${title(variant)} boundary`, st, host,
                blend(edge, surround, alpha), surround, 3,
                'Only necessary when the border or fill identifies the control; a readable action label can identify a button.', 'conditional');
            }
          }
          add(theme, 'Button Laboratory: indicators', `${title(variant)} focus ring`, 'focus', host, button.settings.focus, surround, 3,
            'Offset focus ring against its surrounding surface, including when hover/active is also present. Check geometry separately.');
          add(theme, 'Button Laboratory: indicators', `${title(variant)} selection ring (outer)`, 'selected', host, button.settings.focus, surround, 3,
            'Persistent toggle indicator against the outside surface; also expose aria-pressed.');
          add(theme, 'Button Laboratory: indicators', `${title(variant)} selection ring (inner)`, 'selected', host,
            button.settings.focus, c.border === 'transparent' ? base : c.border, 3,
            'Extra inner-edge check, not an independent failure when the outside ring already identifies selection.', 'conditional');
        }
      }

      // These formulas follow the state explorer CSS: active filters the
      // whole button; disabled/loading opacity blends it onto the tile.
      for (const st of explorerStates) {
        const faded = st === 'disabled' || st === 'loading';
        const bg = st === 'hover' ? r['primary-hover'] : st === 'active' ? brighten(r.primary, .86) : r.primary;
        const fg = st === 'active' ? brighten(r['on-primary'], .86) : r['on-primary'];
        add(theme, 'General components and form states', 'State Explorer button text', st, 'surface',
          blend(fg, r.surface, faded ? .55 : 1), blend(bg, r.surface, faded ? .55 : 1), faded ? null : 4.5,
          faded ? 'Explorer disables its loading/disabled button; inactive-control exemption applies.' : 'Includes active brightness filtering; states without their own text style retain default colours.');
        const inputBg = st === 'readonly' ? r['surface-muted'] : r.surface;
        // button:disabled has opacity; the explorer input does not.
        add(theme, 'General components and form states', 'State Explorer input text', st, 'input background', r.text, inputBg, st === 'disabled' ? null : 4.5,
          st === 'readonly' ? 'Read-only remains readable and is not exempt.' : 'States without an input text override retain the default text colour.');
        const border = st === 'invalid' ? r.danger : st === 'success' ? r.success : r['control-border'];
        add(theme, 'General components and form states', 'State Explorer input border', st, 'input background', border, inputBg, st === 'disabled' ? null : 3,
          'Input boundary check. Invalid/success border and outline must also remain visible against the outside surface.');
        if (st === 'invalid' || st === 'success')
          add(theme, 'General components and form states', 'Input feedback outline', st, 'surface', border, r.surface, 3, 'Feedback indicator against the surrounding tile.');
      }
      for (const variant of ['primary', 'secondary']) {
        add(theme, 'General components and form states', `General ${variant} button text`, 'hover', 'primary-hover', r['on-' + variant], r['primary-hover'], 4.5,
          'General demo hover uses --primary-hover; Laboratory variants have their own hover tokens.');
      }
      add(theme, 'General components and form states', 'Input and button focus outline', 'focus', 'surface', r.focus, r.surface, 3, 'Colour check for the State Explorer focus outlines.');
      add(theme, 'General components and form states', 'Explorer selected tile indicator', 'selected', 'surface', r.primary, r.surface, 3, 'Selected tile border/ring uses --primary. Meaning must not rely only on colour.');

      for (const [label, bg] of [['Preview card', r.surface], ['Nested muted surface', r['surface-muted']]])
        for (const text of ['text', 'text-muted'])
          add(theme, 'Surfaces and opacity', `${label}: --${text}`, 'default', 'surface',
            blend(r[text], r.surface, (configuration.opacity ?? adv.opacity) / 100), blend(bg, r.surface, (configuration.opacity ?? adv.opacity) / 100), 4.5,
            `Whole-component opacity ${configuration.opacity ?? adv.opacity}%, composited onto an opaque --surface. Other backgrounds require a separate check.`);

      const swatches = [...EXAMPLE_PALETTE.primary, ...EXAMPLE_PALETTE.accent,
        ...Object.entries({ primary: p, secondary: s, accent: a }).flatMap(([name, ramp]) =>
          steps.map(step => [`${name}-${step}`, ramp[step]]))];
      for (const [name, hex] of swatches)
        for (const [label, fg] of [['white text', '#FFFFFF'], ['semantic text', r.text]])
          add(theme, 'Swatch candidates: reference and ramps', `${name} / ${label}`, 'candidate', 'swatch as background', fg, hex, 4.5,
            'Exploration only: an unused swatch has no contrast requirement. Decide its actual foreground, role and state before use.', 'candidate');
    }
    return result.map(row => ({ ...row, id: [row.theme, row.threshold === null ? 'Exempt' : row.scope === 'conditional' ? 'Conditional' : ['candidate', 'potential'].includes(row.scope) ? 'Potential use' : 'Required', row.group, row.name, row.state, row.location].join('|'), targets: targetsFor(row, button, foundation, palettes) }));
  }

  function sortRows(list) {
    const mode = get('contrastSort').value;
    const name = row => `${row.name} ${row.state} ${row.location} ${row.theme}`;
    return [...list].sort((a, b) => {
      const groupOrder = a.group.localeCompare(b.group);
      if (groupOrder) return groupOrder;
      if (mode === 'name') return name(a).localeCompare(name(b));
      if (mode === 'state') return (stateOrder[a.state] ?? 99) - (stateOrder[b.state] ?? 99) || name(a).localeCompare(name(b));
      if (mode === 'ratio') return a.ratio - b.ratio || name(a).localeCompare(name(b));
      return statusOrder[a.status] - statusOrder[b.status] || a.ratio - b.ratio || name(a).localeCompare(name(b));
    });
  }

  function filtered() {
    const theme = get('contrastTheme').value, status = get('contrastResult').value;
    const search = get('contrastSearch').value.trim().toLowerCase();
    return sortRows(rows.filter(row => (theme === 'all' || row.theme === theme) &&
      (status === 'all' || row.status === status) &&
      (!search || `${row.group} ${row.name} ${row.state} ${row.location} ${row.note}`.toLowerCase().includes(search))));
  }

  function assessment(row) {
    if (row.status === 'exempt') return 'Exempt: inactive';
    if (row.status === 'conditional') return row.ratio >= row.threshold ? 'Conditional: target met' : 'Conditional: judge context';
    if (row.scope === 'potential') return row.ratio >= row.threshold ? 'Potential use: target met' : 'Potential use: below target';
    if (row.status === 'candidate') return row.ratio >= 4.5 ? 'Candidate: normal text' : row.ratio >= 3 ? 'Candidate: large text only' : 'Candidate: low contrast';
    if (row.status === 'pass') return 'Required pair: target met';
    return row.threshold === 4.5 && row.ratio >= 3 ? 'Required: large text only' : 'Required: below target';
  }

  function render() {
    const list = filtered();
    const counts = Object.fromEntries(Object.keys(statusOrder).map(key => [key, rows.filter(row => row.status === key).length]));
    get('contrastSummary').textContent = `${rows.length} pairs across both themes: ${counts.review} required pairs below target, ${counts.conditional} conditional checks, ${counts.pass} required pairs pass, ${counts.candidate} potential uses, ${counts.exempt} inactive exemptions. Showing ${list.length}.`;
    const groups = [...new Set(list.map(row => row.group))].sort((a, b) => a.localeCompare(b));
    container.innerHTML = groups.map(group => {
      const items = list.filter(row => row.group === group);
      const reviews = items.filter(row => row.status === 'review').length;
      return `<details class="contrast-group" data-group="${esc(group)}"${openGroups.has(group) ? ' open' : ''}>
        <summary>${esc(group)} <span class="help">${items.length} pairs${reviews ? ` · ${reviews} to review` : ''}</span></summary>
        <div class="contrast-table-wrap" tabindex="0" role="region" aria-label="${esc(group)} contrast results">
        <table class="contrast-table"><caption>${esc(group)} — sorted ${esc(get('contrastSort').selectedOptions[0].textContent.toLowerCase())}</caption>
        <thead><tr><th scope="col">Theme</th><th scope="col">Pair / state / context</th><th scope="col">Foreground / background</th><th scope="col">Ratio / target</th><th scope="col">Result</th></tr></thead>
        <tbody>${items.map(row => `<tr data-status="${row.status}"><td>${title(row.theme)}</td>
          <td><strong>${esc(row.name)}</strong><br>${esc(row.state)} · ${esc(row.location)}<small>${esc(row.note)}</small></td>
          <td><span class="contrast-example" style="color:${row.fg};background:${row.bg}">${row.threshold === 3 ? '●' : 'Aa'}</span><code>${row.fg}<br>${row.bg}</code></td>
          <td>${row.ratio.toFixed(3)}:1<br><small>${row.threshold === null ? 'No target' : `≥ ${row.threshold}:1 ${row.threshold === 3 ? 'non-text' : 'normal text'}`}</small></td>
          <td><strong class="contrast-result">${assessment(row)}</strong><br>${row.targets.length ? `<button type="button" class="contrast-edit" data-edit-contrast="${esc(row.id)}" aria-label="Edit colour for ${esc(row.name)} ${esc(row.state)} ${row.theme}">Edit this colour</button>` : '<small>Fixed reference colours</small>'}</td></tr>`).join('')}</tbody></table></div></details>`;
    }).join('') || '<p>No pairs match these filters.</p>';
    container.querySelectorAll('details').forEach(details => details.addEventListener('toggle', () => {
      if (!details.isConnected) return;
      if (details.open) openGroups.add(details.dataset.group);
      else openGroups.delete(details.dataset.group);
    }));
  }

  function refresh() { rows = collect(); render(); window.dssSyncSemanticEditor?.(); }
  function schedule() {
    if (queued) return;
    queued = true;
    queueMicrotask(() => { queued = false; refresh(); });
  }
  renderContrast = schedule;
  window.dssUpdateContrastChecks = schedule;
  window.dssGetContrastChecks = () => rows.map(row => ({ ...row }));
  for (const id of ['contrastTheme', 'contrastResult', 'contrastSort']) get(id).addEventListener('change', render);
  get('contrastSearch').addEventListener('input', render);
  get('contrastDownload').addEventListener('click', () => {
    const heading = ['Theme', 'Category', 'Group', 'Pair', 'State', 'Context', 'Foreground', 'Background', 'Ratio', 'Target', 'Result', 'Notes'];
    const data = filtered().map(row => [row.theme, row.threshold === null ? 'Exempt' : row.scope === 'conditional' ? 'Conditional' : ['candidate', 'potential'].includes(row.scope) ? 'Potential use' : 'Required', row.group, row.name, row.state, row.location, row.fg, row.bg, row.ratio, row.threshold ?? '', assessment(row), row.note]);
    const csv = [heading, ...data].map(row => row.map(value => `"${String(value).replace(/"/g, '""')}"`).join(',')).join('\r\n');
    download('contrast-checks.csv', '\ufeff' + csv, 'text/csv;charset=utf-8');
  });
  window.dssContrastTools = { collect, refresh: schedule };
  container.addEventListener('click', event => {
    const action = event.target.closest('[data-edit-contrast]');
    if (action) window.dssOpenColourRepair?.(rows.find(row => row.id === action.dataset.editContrast));
  });
  refresh();
})();
