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
    if (name.startsWith('--brand-')) return source(4, 'jBrandEditor', 'Brand reference', { brand: name.slice(8) });
    if (/^--(header|main|footer)-padding-(top|right|bottom|left)$/.test(name)) return source(4,name.slice(2),'Region padding shared across themes');
    const backgroundPaint=name.match(/^--(body|header|main|footer)-background-(opacity|rgb|paint)$/);
    if(backgroundPaint) return source(4,(backgroundPaint[1]==='body'?'page':backgroundPaint[1])+'-background-'+(backgroundPaint[2]==='rgb'?'colour':'opacity'),backgroundPaint[2]==='opacity'?'Background opacity / theme setting':'Derived background paint from colour and opacity',{background:true});
    if (name === '--background') return source(4, 'page-background-colour', 'Body background / optional theme override', { background: true });
    if (/^--(header|main|footer)-background$/.test(name)) return source(4, name.slice(2) + '-colour', 'Theme background / optional override', { background: true });
    if (/^--neutral-\d+$/.test(name)) return source(4, 'jPrimary', 'Derived from Primary UI hue with reduced chroma and the ramp method');
    const ramp = name.match(/^--(primary|secondary|accent)-\d+$/);
    if (ramp) return source(4, 'j'+ramp[1][0].toUpperCase()+ramp[1].slice(1), 'Derived from the Main Palette anchor and ramp method');
    const statusRamp = name.match(/^--(success|warning|danger)-\d+$/);
    if (statusRamp) return source(4, 'jSemanticRole', 'Derived from the theme status colour and ramp method', { semantic: statusRamp[1] });
    const interactionRamp=name.match(/^(--(?:button-(primary|secondary|accent|outline|text)-)?state-(default|hover|focus|active|selected|disabled|loading|invalid|success|readonly))-\d+$/);
    if(interactionRamp) {
      const entry=DSStudio.statePalettes.sourceFor(interactionRamp[1],row.scope==='Dark'?'dark':'light');
      if(entry)return source(4,entry.control,'Derived from the resolved state colour and ramp method',{...(entry.variant?{variant:entry.variant}:{semantic:entry.semantic})});
    }
    if (SEMANTIC_COLOUR_KEYS.includes(name.slice(2))) return source(4, 'jSemanticRole', 'Theme role / optional override', { semantic: name.slice(2) });
    const button = name.match(/^--button-(primary|secondary|accent|outline|text)-(source|bg|text|border|hover|active|hover-text|active-text)$/);
    if (button) return source(4, { source:'bdSource', bg:'bdDefaultBg', text:'bdText', border:'bdBorderColor', hover:'bdHover', active:'bdActive', 'hover-text':'bdHoverText', 'active-text':'bdActiveText' }[button[2]], 'Button variant setting / optional override', { variant: button[1] });
    const settings = {
      '--page-max-width':[9,'responsive-maxWidth'], '--page-gutter':[9,'responsive-gutter'], '--page-gutter-wide':[9,'responsive-wideGutter'],
      '--font-body':[5,'fontSource'], '--font-heading':[5,'fontSource'], '--font-ui':[5,'fontSource','Alias of the body font'],
      '--font-size-base':[5,'jBase'], '--type-ratio':[5,'jRatio'], '--body-leading':[5,'jLeading'], '--heading-leading':[5,'jHeadingLeading'],
      '--heading-letter-spacing':[5,'jHeadingTracking'], '--body-letter-spacing':[5,'jBodyTracking'], '--heading-tracking':[5,'jHeadingTracking','Alias of heading letter spacing'],
      '--space-unit':[8,'jSpacing'], '--radius-base':[8,'jRadius'], '--focus-width':[10,'advFocus'], '--control-height':[10,'advHeight'],
      '--border-width':[8,'advBorder'], '--heading-weight':[5,'advWeight'], '--reading-measure':[5,'advMeasure'],
      '--grid-card-min':[9,'advColumns'], '--grid-gap':[9,'advGap'], '--grid-align':[9,'advAlign'],
      '--surface-opacity':[8,'advOpacity'], '--elevation':[8,'advShadow'], '--motion-duration':[10,'advMotion'],
      '--button-pad-x':[7,'bdPaddingX'], '--button-pad-y':[7,'bdPaddingY'], '--button-min-height':[7,'bdMinHeight'],
      '--button-radius':[7,'bdRadius'], '--button-border-width':[7,'bdBorder'], '--button-font-weight':[7,'bdWeight'],
      '--button-focus':[4,'bdFocus'], '--button-focus-width':[7,'bdFocusWidth'], '--button-motion':[7,'bdMotion'],
      '--button-progress-animation':[10,'advReduce','Derived from reduced-motion configuration']
    };
    if (settings[name]) return source(...settings[name]);
    if (/^--space-\d+$/.test(name)) return source(8,'jSpacing','Derived multiple of the spacing unit');
    if (/^--text-step-\d+$/.test(name)) return source(5,'jBase','Derived from base size and type ratio');
    if (/^--text-(body|small)$/.test(name)) return source(5,'jBase','Derived from base size and type ratio');
    if (/^--text-(display|h1|h2)$/.test(name)) return source(5,'clampFactor','Derived from base size, ratio and responsive limits');
    return null;
  };
  window.dssTokenSource = sourceFor;

  const describe = (name, type) => {
    if (/^--(header|main|footer)-padding-(top|right|bottom|left)$/.test(name)) return 'Additional padding inside the website region; existing content gutters and section spacing still apply. Shared by light and dark themes.';
    if (/^--(body|header|main|footer)-background-(opacity|rgb|paint)$/.test(name)) return 'Background paint and alpha; text and controls remain independently opaque. Transparent regions blend over their parent background.';
    if (name.startsWith('--page-')) return 'Responsive page maximum width or side gutter; configure in the Responsive phase.';
    if (name.includes('letter-spacing') || name.includes('heading-tracking')) return 'Extra character spacing in em, relative to the element font size.';
    if (name.startsWith('--brand-')) return 'Project Brand Palette reference; choose separately for a Main Palette UI role.';
    if (/^--(?:button-(?:primary|secondary|accent|outline|text)-)?state-/.test(name)) return 'Generated state shade; 500 preserves the resolved source colour. Transparent backgrounds use the foreground anchor. Native behaviour, opacity and non-colour cues still apply.';
    if (/^--neutral-\d+$/.test(name)) return 'Neutral shade derived from the Primary UI hue with a restrained tint; 500 is its generated midpoint.';
    if (/^--(success|warning|danger)-\d+$/.test(name)) return 'Generated status shade for this theme; 500 preserves its resolved semantic colour. Check contrast and use text or icons alongside colour.';
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
    if (/^--(header|main|footer)-padding-(top|right|bottom|left)$/.test(name)) return 'Layout';
    if (/^--(body|header|main|footer)-background-(opacity|rgb|paint)$/.test(name)) return 'Surface & controls';
    if (name.includes('letter-spacing') || name.includes('heading-tracking')) return 'Typography';
    if (name.startsWith('--brand-')) return 'Brand palette';
    if (/^--(?:button-(?:primary|secondary|accent|outline|text)-)?state-/.test(name)) return 'Colour ramp';
    if (/^--(primary|secondary|accent|neutral|success|warning|danger)-\d+$/.test(name)) return 'Colour ramp';
    if (name.startsWith('--button-')) return 'Button component';
    if (/^--(font|text-|type-ratio|body-leading|heading-leading|heading-weight|reading-measure)/.test(name)) return 'Typography';
    if (/^--(space|radius)/.test(name)) return 'Spacing & shape';
    if (name.startsWith('--grid-') || name.startsWith('--page-')) return 'Layout';
    if (/^--(elevation|surface-opacity|border-width|control-height)/.test(name)) return 'Surface & controls';
    if (name === '--motion-duration') return 'Motion';
    return SEMANTIC_COLOUR_KEYS.includes(name.slice(2)) ? 'Semantic colours' : 'Interaction';
  };

  const readTokens = (css = cssExport()) => {
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

  const filtered = (css = cssExport()) => {
    const q = search.value.trim().toLowerCase();
    return readTokens(css).filter(row => [row.type, row.name, row.value, row.description, row.scope]
      .some(value => value.toLowerCase().includes(q)));
  };

  let renderedSignature='',renderedRows=new Map();
  const update = () => {
    const css=cssExport(),signature=css+'\u0000'+search.value;
    if(signature===renderedSignature)return;
    const rows = filtered(css);
    count.textContent = `${rows.length} tokens shown${search.value ? ' (filtered)' : ''}.`;
    const nextRows=new Map();
    const nodes=rows.map((row,index) => {
      const source=sourceFor(row);
      const colour = /^#[0-9a-f]{6}$/i.test(row.value) ?
        `<span class="token-dot" style="background:${row.value}" aria-hidden="true"></span>` : '';
      const html=`<tr><td>${escapeHtml(row.type)}</td><td><code>${escapeHtml(row.name)}</code></td>` +
        `<td><div class="token-value">${colour}<code>${escapeHtml(row.value)}</code></div></td>` +
        `<td>${escapeHtml(row.description)} <small class="muted">(${escapeHtml(row.scope)})</small>` +
        (source ? `<p class="help">${escapeHtml(source.mode)} · wizard step ${DSStudio.stages[source.step].position + 1}</p><button type="button" class="ghost" data-token-name="${escapeHtml(row.name)}" data-token-scope="${escapeHtml(row.scope)}" aria-label="Configure source for ${escapeHtml(row.name)} (${escapeHtml(row.scope)})">Configure source</button>` : '<p>Configuration source unavailable.</p>') + '</td></tr>';
      const key=index+'\u0000'+row.scope+'\u0000'+row.name;
      let entry=renderedRows.get(key);
      if(!entry || entry.html!==html) {
        const template=document.createElement('template');template.innerHTML=html;
        entry={html,node:template.content.firstElementChild};
      }
      nextRows.set(key,entry);return entry.node;
    });
    if(!nodes.length) {
      const row=document.createElement('tr'),cell=document.createElement('td');cell.colSpan=4;cell.textContent='No matching tokens.';row.append(cell);nodes.push(row);
    }
    if(table.children.length===nodes.length)nodes.forEach((node,index)=>{if(table.children[index]!==node)table.children[index].replaceWith(node);});
    else table.replaceChildren(...nodes);
    renderedRows=nextRows;
    renderedSignature=signature;
  };

  window.dssUpdateTokenCatalogue = update;
  table.addEventListener('click', event => {
    const button = event.target.closest('[data-token-name]');
    if (button) window.dssConfigureToken?.({ name: button.dataset.tokenName, scope: button.dataset.tokenScope });
  });
  DSStudio.on('output:updated', update);
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
