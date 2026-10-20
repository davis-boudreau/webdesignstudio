/* V4.1: token catalogue reads the same CSS generator used by Export CSS.
No separate hardcoded values: the table stays synchronized with the export. */
(() => {
  'use strict';
  const table = document.getElementById('tokenTableBody');
  const search = document.getElementById('tokenSearch');
  const count = document.getElementById('tokenCount');
  if (!table || !search || !count) return;

  // Every exported declaration has a configuration source. Derived scales and
  // aliases deliberately edit their source instead of breaking the relationship.
  const sourceFor = row => {
    const name = row.name;
    const source = (step, control, mode = 'Direct setting', extra = {}) => ({ step, control, mode, ...extra });
    if (name.startsWith('--brand-')) return source(1, 'jBrandEditor', 'Brand reference', { brand: name.slice(8) });
    const ramp = name.match(/^--(primary|secondary|accent)-\d+$/);
    if (ramp) return source(1, 'j'+ramp[1][0].toUpperCase()+ramp[1].slice(1), 'Derived from the Main Palette anchor and ramp method');
    if (SEMANTIC_COLOUR_KEYS.includes(name.slice(2))) return source(3, 'jSemanticRole', 'Theme role / optional override', { semantic: name.slice(2) });
    const button = name.match(/^--button-(primary|secondary|accent|outline|text)-(source|bg|text|border|hover|active|hover-text|active-text)$/);
    if (button) return source(4, { source:'bdSource', bg:'bdDefaultBg', text:'bdText', border:'bdBorderColor', hover:'bdHover', active:'bdActive', 'hover-text':'bdHoverText', 'active-text':'bdActiveText' }[button[2]], 'Button variant setting / optional override', { variant: button[1] });
    const settings = {
      '--font-body':[2,'fontSource'], '--font-heading':[2,'fontSource'], '--font-ui':[2,'fontSource','Alias of the body font'],
      '--font-size-base':[2,'jBase'], '--type-ratio':[2,'jRatio'], '--body-leading':[2,'jLeading'], '--heading-leading':[2,'jHeadingLeading'],
      '--heading-letter-spacing':[2,'jHeadingTracking'], '--body-letter-spacing':[2,'jBodyTracking'], '--heading-tracking':[2,'jHeadingTracking','Alias of heading letter spacing'],
      '--space-unit':[5,'jSpacing'], '--radius-base':[5,'jRadius'], '--focus-width':[6,'advFocus'], '--control-height':[6,'advHeight'],
      '--border-width':[5,'advBorder'], '--heading-weight':[2,'advWeight'], '--reading-measure':[2,'advMeasure'],
      '--grid-card-min':[5,'advColumns'], '--grid-gap':[5,'advGap'], '--grid-align':[5,'advAlign'],
      '--surface-opacity':[5,'advOpacity'], '--elevation':[5,'advShadow'], '--motion-duration':[6,'advMotion'],
      '--button-pad-x':[4,'bdPaddingX'], '--button-pad-y':[4,'bdPaddingY'], '--button-min-height':[4,'bdMinHeight'],
      '--button-radius':[4,'bdRadius'], '--button-border-width':[4,'bdBorder'], '--button-font-weight':[4,'bdWeight'],
      '--button-focus':[4,'bdFocus'], '--button-focus-width':[4,'bdFocusWidth'], '--button-motion':[4,'bdMotion'],
      '--button-progress-animation':[6,'advReduce','Derived from reduced-motion configuration']
    };
    if (settings[name]) return source(...settings[name]);
    if (/^--space-\d+$/.test(name)) return source(5,'jSpacing','Derived multiple of the spacing unit');
    if (/^--text-step-\d+$/.test(name)) return source(2,'jBase','Derived from base size and type ratio');
    if (/^--text-(body|small)$/.test(name)) return source(2,'jBase','Derived from base size and type ratio');
    if (/^--text-(display|h1|h2)$/.test(name)) return source(2,'clampFactor','Derived from base size, ratio and responsive limits');
    return null;
  };
  window.dssTokenSource = sourceFor;

  const describe = (name, type) => {
    if (name.includes('letter-spacing') || name.includes('heading-tracking')) return 'Extra character spacing in em, relative to the element font size.';
    if (name.startsWith('--brand-')) return 'Project Brand Palette reference; choose separately for a Main Palette UI role.';
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
    if (name.includes('letter-spacing') || name.includes('heading-tracking')) return 'Typography';
    if (name.startsWith('--brand-')) return 'Brand palette';
    if (/^--(primary|secondary|accent)-\d+$/.test(name)) return 'Colour ramp';
    if (name.startsWith('--button-')) return 'Button component';
    if (/^--(font|text-|type-ratio|body-leading|heading-leading|heading-weight|reading-measure)/.test(name)) return 'Typography';
    if (/^--(space|radius)/.test(name)) return 'Spacing & shape';
    if (name.startsWith('--grid-')) return 'Layout';
    if (/^--(elevation|surface-opacity|border-width|control-height)/.test(name)) return 'Surface & controls';
    if (name === '--motion-duration') return 'Motion';
    return SEMANTIC_COLOUR_KEYS.includes(name.slice(2)) ? 'Semantic colours' : 'Interaction';
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

  window.dssReadTokens = readTokens;
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
        `<td>${escapeHtml(row.description)} <small class="muted">(${escapeHtml(row.scope)})</small>` +
        (sourceFor(row) ? `<p class="help">${escapeHtml(sourceFor(row).mode)} · wizard step ${sourceFor(row).step + 1}</p><button type="button" class="ghost" data-token-name="${escapeHtml(row.name)}" data-token-scope="${escapeHtml(row.scope)}" aria-label="Configure source for ${escapeHtml(row.name)} (${escapeHtml(row.scope)})">Configure source</button>` : '<p>Configuration source unavailable.</p>') + '</td></tr>';
    }).join('') || '<tr><td colspan="4">No matching tokens.</td></tr>';
  };

  window.dssUpdateTokenCatalogue = update;
  table.addEventListener('click', event => {
    const button = event.target.closest('[data-token-name]');
    if (button) window.dssConfigureToken?.({ name: button.dataset.tokenName, scope: button.dataset.tokenScope });
  });
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
