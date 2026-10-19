/* V4.1: token catalogue reads the same CSS generator used by Export CSS.
No separate hardcoded values: the table stays synchronized with the export. */
(() => {
  'use strict';
  const table = document.getElementById('tokenTableBody');
  const search = document.getElementById('tokenSearch');
  const count = document.getElementById('tokenCount');
  if (!table || !search || !count) return;

  const describe = (name, type) => {
    if (name.startsWith('--nscc-')) return 'Fixed official NSCC brand reference; not an editable semantic role.';
    if (/^--(primary|secondary|accent)-\d+$/.test(name))
      return 'Generated colour ramp step; 500 preserves the selected anchor colour.';
    if (name.includes('hover-text')) return 'Foreground colour for the button hover state.';
    if (name.includes('active-text')) return 'Foreground colour for the button pressed state.';
    if (name.includes('hover')) return 'Colour applied during pointer hover.';
    if (name.includes('active')) return 'Colour applied while a button is pressed.';
    if (name.includes('focus')) return 'Visible keyboard-focus indicator setting.';
    if (name.includes('border')) return 'Border colour or thickness used by components.';
    if (name.includes('radius')) return 'Corner rounding applied to surfaces or controls.';
    if (name.includes('space') || name.includes('pad-')) return 'Spacing measurement used to maintain consistent layout.';
    if (name.includes('font') || name.includes('text-step') || name.includes('leading') || name.includes('type-ratio'))
      return 'Typography foundation value for readable, consistent text.';
    if (name.includes('motion')) return 'Animation or transition duration; respect reduced-motion preferences.';
    if (name.startsWith('--button-')) return 'Button component token shared by the preview and exported stylesheet.';
    if (type === 'Semantic colours') return 'Contextual interface colour role; may change between light and dark themes.';
    return 'Reusable design-system foundation value.';
  };

  const classify = name => {
    if (name.startsWith('--nscc-')) return 'Official brand';
    if (/^--(primary|secondary|accent)-\d+$/.test(name)) return 'Colour ramp';
    if (name.startsWith('--button-')) return 'Button component';
    if (/^--(font|text-step|text-display|type-ratio|body-leading|heading-leading)/.test(name)) return 'Typography';
    if (/^--(space|radius)/.test(name)) return 'Spacing & shape';
    return 'Semantic colours';
  };

  const readTokens = () => {
    const css = cssExport();
    const tokens = [];
    let scope = 'Light / base';
    for (const line of css.split('\n')) {
      if (/^\[data-theme="dark"\]\s*\{/.test(line.trim())) scope = 'Dark';
      else if (/^:root\s*\{/.test(line.trim())) scope = 'Light / base';
      const match = line.match(/^\s*(--[\w-]+)\s*:\s*(.+?)\s*;\s*$/);
      if (!match) continue;
      const [, name, value] = match;
      const type = classify(name);
      tokens.push({
        type,
        name,
        value,
        description: describe(name, type),
        scope
      });
    }
    return tokens;
  };

  const escapeHtml = value => String(value).replace(/[&<>"']/g, char =>
    ({
      '&': '&amp;',
      '<': '&lt;',
      '>': '&gt;',
      '"': '&quot;',
      "'": '&#39;'
    } [char]));

  const filtered = () => {
    const q = search.value.trim().toLowerCase();
    return readTokens().filter(row => [row.type, row.name, row.value, row.description, row.scope]
      .some(value => value.toLowerCase().includes(q)));
  };

  const update = () => {
    const rows = filtered();
    count.textContent = `${rows.length} tokens shown${search.value ? ' (filtered)' : ''}.`;
    table.innerHTML = rows.map(row => {
      const colour = /^#[0-9a-f]{6}$/i.test(row.value) ?
        `<span class="token-dot" style="background:${row.value}" aria-hidden="true"></span>` : '';
      return `<tr><td>${escapeHtml(row.type)}</td><td><code>${escapeHtml(row.name)}</code></td>` +
        `<td><div class="token-value">${colour}<code>${escapeHtml(row.value)}</code></div></td>` +
        `<td>${escapeHtml(row.description)} <small class="muted">(${escapeHtml(row.scope)})</small></td></tr>`;
    }).join('') || '<tr><td colspan="4">No matching tokens.</td></tr>';
  };

  window.dssUpdateTokenCatalogue = update;
  const originalRenderCode = renderCode;
  renderCode = function() {
    originalRenderCode();
    update();
  };
  search.addEventListener('input', update);
  document.getElementById('tokenDownload').addEventListener('click', () => {
    const csv = [
        ['Token type', 'Token name', 'Value', 'Description', 'Scope'],
        ...filtered().map(row => [row.type, row.name, row.value, row.description, row.scope])
      ]
      .map(row => row.map(cell => `"${String(cell).replace(/"/g,'""')}"`).join(','))
      .join('\r\n');
    download('design-system-tokens.csv', '\ufeff' + csv, 'text/csv;charset=utf-8');
  });
  update();
})();
