'use strict';
/* V4.1 Button Design: shared project settings, preview and exported component CSS.
State simulations are labelled; browser-native focus/disabled remain testable. */
(() => {
  const $ = id => document.getElementById(id);
  const defaults = DSStudio.project.buttonDefaults();
  const names = {
    primary: 'Primary',
    secondary: 'Secondary',
    accent: 'Accent',
    outline: 'Outline',
    text: 'Text'
  };
  const states = ['default', 'hover', 'focus', 'active', 'selected', 'disabled', 'loading'];
  const stateGroups = [{
    title: 'Standard interaction',
    description: 'The normal pointer and keyboard interaction sequence.',
    items: ['default', 'hover', 'focus', 'active']
  }, {
    title: 'Toggle selection',
    description: 'Persistent selected state for toggle buttons only.',
    items: ['selected']
  }, {
    title: 'Availability and progress',
    description: 'Unavailable or processing actions.',
    items: ['disabled', 'loading']
  }];
  const stateLabels = {
    default: 'Default',
    hover: 'Hover',
    focus: 'Focus-visible',
    active: 'Active / pressed',
    selected: 'Selected toggle',
    disabled: 'Disabled',
    loading: 'Loading'
  };
  const colorGroups = [{
    title: 'Filled colours',
    variants: ['primary', 'secondary', 'accent']
  }, {
    title: 'Minimal colours',
    variants: ['outline', 'text']
  }];

  function sourceLabel(v, settings = b, foundation = state) {
    if(foundation.colourTransparency?.['button:'+v+':source'])return 'None (transparent paint)';
    const source = settings.sources[v] || defaults.sources[v];
    if (source === 'custom') return 'Custom colour';
    if (source.startsWith('#')) return `Example swatch ${source.toUpperCase()}`;
    return `Theme ${source}`;
  }
  const explain = {
    default: 'Normal action, ready to activate.',
    hover: 'Pointer hover uses a variant-specific background.',
    focus: 'Keyboard focus must remain visible; use Tab to test actual focus.',
    active: 'The pressed state is momentary, not a persistent selection.',
    disabled: 'Unavailable action: use the native disabled attribute.',
    loading: 'Pending action: requires JavaScript to block duplicate submissions and announce status.',
    selected: 'Persistent pressed state applies only to toggle buttons with aria-pressed.'
  };

  const sanitize = DSStudio.project.normalizeButtons;
  const validColor = validHex;
  let b = state.buttonDesign;

  function hexDark(hex, factor) {
    let n = parseInt(hex.slice(1), 16);
    const a = [n >> 16 & 255, n >> 8 & 255, n & 255].map(x => Math.round(x * factor).toString(16).padStart(2, '0'));
    return '#' + a.join('');
  }

  function luminance(hex) {
    let c = hex.slice(1).match(/../g).map(v => parseInt(v, 16) / 255).map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
    return .2126 * c[0] + .7152 * c[1] + .0722 * c[2];
  }

  function readable(bg) {
    return (1.05 / (luminance(bg) + .05)) >= ((luminance(bg) + .05) / .05) ? '#FFFFFF' : '#101820';
  }

  function baseFor(v, settings = b, foundation = state) {
    const source = settings.sources[v] || defaults.sources[v];
    return source === 'custom' ? (settings.custom[v] || foundation.primary) : (['primary', 'secondary', 'accent'].includes(source) ? foundation[source] : source);
  }

  function bases() {
    return Object.fromEntries(Object.keys(names).map(v => [v, baseFor(v)]));
  }

  function ratio(fg, bg) {
    const a = luminance(fg),
      z = luminance(bg);
    return (Math.max(a, z) + .05) / (Math.min(a, z) + .05);
  }

  function readableAgainst(base, bg) {
    return ratio(base, bg) >= 4.5 ? base : (readable(bg) === '#FFFFFF' ? '#FFFFFF' : '#101820');
  }

  function colors(v, mode = state.theme, settings = b, foundation = state) {
    const base = baseFor(v, settings, foundation),
      isClear = v === 'outline' || v === 'text',
      o = settings.overrides[v] || {};
    const surface = mode === 'dark' ? '#142434' : '#FFFFFF';
    const bg = o.bg || (isClear ? 'transparent' : base);
    const fg = o.text || (isClear ? readableAgainst(base, surface) : readable(base));
    const hover = o.hover || hexDark(base, .83),
      active = o.active || hexDark(base, .69);
    const clear=foundation.colourTransparency||{},prefix='button:'+v+':';
    const sourceClear=clear[prefix+'source'] || clear['anchor:'+settings.sources[v]];
    const paint=(key,value)=>clear[prefix+key] || sourceClear && ['bg','hover','active','border'].includes(key)?'transparent':value;
    return {
      bg:paint('bg',bg),
      fg:paint('text',fg),
      border:paint('border',o.border || (v === 'outline' ? base : 'transparent')),
      hover:paint('hover',hover),
      active:paint('active',active),
      hoverText:paint('hoverText',o.hoverText || readable(hover)),
      activeText:paint('activeText',o.activeText || readable(active))
    };
  }

  function elevation(v,mode=state.theme,settings=b){
    const preset=settings.elevation?.[v];
    if(preset==='subtle')return mode==='dark'?'0 2px 4px #00000066':'0 2px 4px #00000024';
    if(preset==='medium')return mode==='dark'?'0 4px 10px #00000099':'0 4px 10px #00000038';
    return 'none';
  }
  function elevationCSS(settings){
    const variants=Object.keys(names).filter(v=>elevation(v,'light',settings)!=='none');
    if(!variants.length)return '';
    const tokens=mode=>Object.keys(names).map(v=>'  --button-'+v+'-shadow: '+elevation(v,mode,settings)+';').join('\n');
    return '\n/* Optional per-variant elevation; None keeps other variants flat. */\n:root {\n'+tokens('light')+'\n}\n[data-theme="dark"] {\n'+tokens('dark')+'\n}\n'+variants.map(v=>'.ds-button--'+v+' { --button-elevation-shadow: var(--button-'+v+'-shadow); }').join('\n')+'\n'+DSStudio.buttonStates.elevationCss('.ds-button','data-preview-state','--button-elevation-shadow','--button-focus');
  }

  function props(v, size = b.size, mode = state.theme, settings = b, foundation = state) {
    const c = colors(v, mode, settings, foundation),
      scale = size === 'sm' ? .8 : size === 'lg' ? 1.22 : 1;
    return {
      c,
      style: `${elevation(v,mode,settings)==='none'?'':'--bd-elevation-shadow:'+elevation(v,mode,settings)+';'}--bd-focus:${foundation.colourTransparency?.['button:focus']?'transparent':settings.focus};--bd-focus-width:${settings.focusWidth}px;--bd-motion:${settings.motion}ms;background:${c.bg};color:${c.fg};border:${settings.border}px solid ${c.border};border-radius:${settings.radius}px;min-height:${Math.round(settings.minHeight*scale)}px;padding:${Math.round(settings.padY*scale)}px ${Math.round(settings.padX*scale)}px;font-weight:${settings.weight};font-size:${size==='sm'?'0.875rem':size==='lg'?'1.125rem':'1rem'}`
    };
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function btn(v, st = 'default', size = b.size, mode = state.theme, real = false, settings = b, foundation = state) {
    const p = props(v, size, mode, settings, foundation);
    let c = p.c;
    let style = p.style;
    if (st === 'hover') style += `;background:${c.hover};color:${c.hoverText}`;
    if (st === 'active') style += `;background:${c.active};color:${c.activeText}`;
    const disabled = st === 'disabled' ? ' disabled' : '';
    const pressed = st === 'selected' ? ' aria-pressed="true"' : '';
    const busy = st === 'loading' ? ' aria-busy="true"' : '';
    const sim = real && st === 'focus' ? '' : ` data-sim="${st}"`;
    const label = st === 'loading' ? 'Processing…' : `${names[v]} action`;
    return `<button type="button" class="bd-button" style="${esc(style)}"${sim}${disabled}${pressed}${busy}>${esc(label)}</button>`;
  }

  function controls() {
    const map = {
      bdVariant: b.variant,
      bdSize: b.size,
      bdState: b.selectedState,
      bdPaddingX: b.padX,
      bdPaddingY: b.padY,
      bdMinHeight: b.minHeight,
      bdRadius: b.radius,
      bdBorder: b.border,
      bdWeight: b.weight,
      bdFocus: b.focus.toLowerCase(),
      bdFocusWidth: b.focusWidth,
      bdMotion: b.motion
    };
    for (const [id, val] of Object.entries(map)) $(id).value = val;
    $('bdMobileFull').checked = b.mobileFull;
    $('bdElevation').value=b.elevation?.[b.variant]||'none';
    const v = b.variant,
      base = bases()[v];
    $('bdSource').value = b.sources[v] || defaults.sources[v];
    $('bdCustomWrap').hidden = $('bdSource').value !== 'custom';
    $('bdCustom').value = (b.custom[v] || base).toLowerCase();
    $('bdCustomOut').textContent = $('bdCustom').value.toUpperCase();
    $('bdHover').value = (b.overrides[v]?.hover || hexDark(base, .83)).toLowerCase();
    $('bdActive').value = (b.overrides[v]?.active || hexDark(base, .69)).toLowerCase();
    for (const id of ['bdPaddingX', 'bdPaddingY', 'bdMinHeight', 'bdRadius', 'bdBorder', 'bdFocusWidth', 'bdMotion']) $(id + 'Out').textContent = $(id).value + (id === 'bdMotion' ? 'ms' : 'px');
    const col = colors(v);
    for (const [id, val] of Object.entries({
        bdText: col.fg,
        bdHoverText: col.hoverText,
        bdActiveText: col.activeText,
        bdDefaultBg: col.bg === 'transparent' ? base : col.bg,
        bdBorderColor: col.border === 'transparent' ? base : col.border
      })) $(id).value = validColor(val)?val.toLowerCase():base.toLowerCase();
    for (const id of ['bdHover', 'bdActive', 'bdFocus', 'bdText', 'bdHoverText', 'bdActiveText', 'bdDefaultBg', 'bdBorderColor']) $(id + 'Out').textContent = $(id).value.toUpperCase();
  }

  function matrix(settings = b, foundation = state) {
    return stateGroups.map(group => `<section class="bd-state-group" aria-label="${group.title}"><div class="bd-state-group-heading"><h4>${group.title}</h4><p class="help">${group.description}</p></div>${group.items.map(st=>`<section class="bd-state-section" aria-label="${stateLabels[st]}"><div class="bd-state-section-head"><h5>${stateLabels[st]}</h5><p class="help">${esc(explain[st])}</p></div>${colorGroups.map(type=>`<div class="bd-color-group"><h6>${type.title}</h6><div class="bd-state-grid">${type.variants.map(v=>`<div class="bd-cell"><strong>${names[v]}</strong><span class="bd-source-label">${esc(sourceLabel(v, settings, foundation))}</span>${btn(v,st,'md',foundation.theme,false,settings,foundation)}</div>`).join('')}</div></div>`).join('')}</section>`).join('')}</section>`).join('');
  }

  function render() {
    $('bdContext').textContent = `${names[b.variant]} · ${b.size.toUpperCase()} · ${b.selectedState}`;
    $('bdDescription').textContent = explain[b.selectedState] + (b.selectedState === 'disabled' ? ' This state example is unavailable; explain the prerequisite beside disabled actions in your application.' : '');
    $('bdSingle').innerHTML = btn(b.variant, b.selectedState, b.size, state.theme, true);
    $('bdThemes').innerHTML = ['light', 'dark'].map(m => `<div class="bd-theme-card" data-mode="${m}"><strong>${m==='light'?'Light':'Dark'} preview</strong>${btn(b.variant,b.selectedState,b.size,m)}</div>`).join('');
    $('bdMatrix').innerHTML = matrix(b, state);
    syncLegacyButtons();
    window.dssUpdateContrastChecks?.();
    $('bdCode').textContent = buttonCSS();
    if (typeof renderCode === 'function') renderCode();
  }

  function syncLegacyButtons() {
    // The general Components demonstration shares the Button Laboratory's outline tokens.
    // Both default and hover colours now follow the outline variant, including its selected Example accent source.
    const c = colors('outline');
    const root = document.documentElement;
    root.style.setProperty('--demo-outline-bg', c.bg);
    root.style.setProperty('--demo-outline-text', c.fg);
    root.style.setProperty('--demo-outline-border', c.border);
    root.style.setProperty('--demo-outline-hover-bg', c.hover);
    root.style.setProperty('--demo-outline-hover-text', c.hoverText);
    root.style.setProperty('--demo-outline-active-bg', c.active);
    root.style.setProperty('--demo-outline-active-text', c.activeText);
    // Keep the Accent demo identical to the Accent laboratory variant.
    const accent = colors('accent');
    root.style.setProperty('--demo-accent-bg', accent.bg);
    root.style.setProperty('--demo-accent-text', accent.fg);
    root.style.setProperty('--demo-accent-border', accent.border);
    root.style.setProperty('--demo-accent-hover-bg', accent.hover);
    root.style.setProperty('--demo-accent-hover-text', accent.hoverText);
    root.style.setProperty('--demo-accent-active-bg', accent.active);
    root.style.setProperty('--demo-accent-active-text', accent.activeText);
  }

  function buttonColourCSS(settings = b, foundation = state) {
    const variants = mode => Object.keys(names).map(v => {
      const c = colors(v, mode, settings, foundation);
      return `  /* ${names[v]} variant colours */\n  --button-${v}-source: ${baseFor(v, settings, foundation)};\n  --button-${v}-bg: ${c.bg};\n  --button-${v}-text: ${c.fg};\n  --button-${v}-border: ${c.border};\n  --button-${v}-hover: ${c.hover};\n  --button-${v}-active: ${c.active};\n  --button-${v}-hover-text: ${c.hoverText};\n  --button-${v}-active-text: ${c.activeText};`;
    }).join('\n');
    return `/* Web Design System Studio V4.1 · Button component CSS\n   FOUNDATION → COMPONENT TOKENS → STATES.\n   Verify text contrast in each theme and state. */\n:root {\n  --button-pad-x: ${settings.padX}px;\n  --button-pad-y: ${settings.padY}px;\n  --button-min-height: ${settings.minHeight}px;\n  --button-radius: ${settings.radius}px;\n  --button-border-width: ${settings.border}px;\n  --button-font-weight: ${settings.weight};\n  --button-focus: ${foundation.colourTransparency?.['button:focus']?'transparent':settings.focus};\n  --button-focus-width: ${settings.focusWidth}px;\n  --button-motion: ${settings.motion}ms;\n${variants('light')}\n}\n[data-theme="dark"] {\n${variants('dark')}\n}\n/* Base component: reusable for all variants. */\n.ds-button {\n  display: inline-flex; align-items: center; justify-content: center;\n  gap: .5em; min-height: var(--button-min-height);\n  padding: var(--button-pad-y) var(--button-pad-x);\n  border: var(--button-border-width) solid transparent;\n  border-radius: var(--button-radius);\n  font: inherit; font-weight: var(--button-font-weight);\n  cursor: pointer; text-align: center;\n  transition: background-color var(--button-motion), border-color var(--button-motion);\n}\n/* Size variants scale the same foundation dimensions. */\n.ds-button--sm { min-height: calc(var(--button-min-height) * .8); padding: calc(var(--button-pad-y) * .8) calc(var(--button-pad-x) * .8); font-size: .875rem; }\n.ds-button--lg { min-height: calc(var(--button-min-height) * 1.22); padding: calc(var(--button-pad-y) * 1.22) calc(var(--button-pad-x) * 1.22); font-size: 1.125rem; }\n${Object.keys(names).map(v=>`/* ${names[v]} variant and its interactive states. */\n.ds-button--${v} { background: var(--button-${v}-bg); color: var(--button-${v}-text); border-color: var(--button-${v}-border); }\n.ds-button--${v}:hover:not(:disabled) { background: var(--button-${v}-hover); color: var(--button-${v}-hover-text); }\n.ds-button--${v}:active:not(:disabled) { background: var(--button-${v}-active); color: var(--button-${v}-active-text); }`).join('\n')}\n/* Real keyboard focus, not just the preview simulation. */\n.ds-button:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }\n/* Native disabled attribute prevents activation. */\n.ds-button:disabled { opacity: .55; cursor: not-allowed; }\n/* aria-pressed is only for persistent toggle buttons. */\n.ds-button[aria-pressed="true"] { box-shadow: 0 0 0 2px var(--button-focus); }\n/* aria-busy requires JavaScript behaviour and status announcements. */\n.ds-button[aria-busy="true"] { cursor: progress; }\n${settings.mobileFull?'/* Optional mobile full-width action. */\n@media (max-width: 40rem) { .ds-button--mobile-full { width: 100%; } }\n':''}/* Honour user reduced-motion preferences. */\n@media (prefers-reduced-motion: reduce) { .ds-button { transition: none; } }\n`;
  }
  function buttonCSS(settings = b, foundation = state) {
    return buttonColourCSS(settings, foundation) + `\n:root { --button-progress-animation: ${foundation.advanced.reduce ? 'none' : 'dss-button-progress'}; }\n` + DSStudio.buttonStates.css('.ds-button, .button', 'data-preview-state') + elevationCSS(settings);
  }
  DSStudio.on('project:install', () => { b = state.buttonDesign; });
  DSStudio.on('project:sync', controls);
  DSStudio.on('properties:committed', () => { controls(); render(); });
  DSStudio.exports.registerCss({id:'buttons',stage:'components',order:20,generate:snapshot=> '\n' + buttonCSS(snapshot?.state?.buttonDesign || b, snapshot?.state || state)});
  // sample-homepage.js reads shared button settings for generated HTML.
  for (const id of ['bdVariant', 'bdSize', 'bdState', 'bdPaddingX', 'bdPaddingY', 'bdMinHeight', 'bdRadius', 'bdBorder', 'bdWeight', 'bdFocus', 'bdFocusWidth', 'bdMotion', 'bdMobileFull', 'bdHover', 'bdActive', 'bdText', 'bdHoverText', 'bdActiveText', 'bdDefaultBg', 'bdBorderColor', 'bdSource', 'bdCustom']) $(id).addEventListener('input', e => {
    const key = {
      bdVariant: 'variant',
      bdSize: 'size',
      bdState: 'selectedState',
      bdPaddingX: 'padX',
      bdPaddingY: 'padY',
      bdMinHeight: 'minHeight',
      bdRadius: 'radius',
      bdBorder: 'border',
      bdWeight: 'weight',
      bdFocus: 'focus',
      bdFocusWidth: 'focusWidth',
      bdMotion: 'motion',
      bdMobileFull: 'mobileFull'
    } [id];
    if (id === 'bdSource') {
      b.sources[b.variant] = e.target.value;
      if (e.target.value === 'custom' && !b.custom[b.variant]) b.custom[b.variant] = state.primary;
    } else if (id === 'bdCustom') {
      b.custom[b.variant] = e.target.value;
    } else if (['bdHover', 'bdActive', 'bdText', 'bdHoverText', 'bdActiveText', 'bdDefaultBg', 'bdBorderColor'].includes(id)) {
      const c = colors(b.variant);
      const current = b.overrides[b.variant] || {};
      const prop = {
        bdHover: 'hover',
        bdActive: 'active',
        bdText: 'text',
        bdHoverText: 'hoverText',
        bdActiveText: 'activeText',
        bdDefaultBg: 'bg',
        bdBorderColor: 'border'
      } [id];
      current[prop] = e.target.value;
      b.overrides[b.variant] = current;
    } else if (key) b[key] = e.target.type === 'checkbox' ? e.target.checked : e.target.type === 'range' || id === 'bdWeight' ? Number(e.target.value) : e.target.value;
    state.buttonDesign = b = sanitize(b);
    controls();
    render();
    window.dssAutosave?.();
    window.dssUpdateTokenCatalogue?.();
  });
  $('bdJump').addEventListener('click', () => window.dssRevealSection('buttonDesignLab'));
  $('bdCopy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText($('bdCode').textContent);
      $('bdCopy').textContent = 'Copied';
    } catch (e) {
      $('bdCopy').textContent = 'Select CSS above to copy';
    }
    setTimeout(() => $('bdCopy').textContent = 'Copy button CSS', 1800);
  });
  $('bdExport').addEventListener('click', () => download('design-system-buttons.css', buttonCSS(), 'text/css'));
  // Update the preview when the global theme or foundation colours change.
  DSStudio.on('foundation:updated', render);
  // Read the same resolved colours as the previews and CSS export.
  window.dssGetButtonContrastData = (settings = b, foundation = state) => ({
    settings: JSON.parse(JSON.stringify(settings)),
    themes: Object.fromEntries(['light', 'dark'].map(theme => [theme,
      Object.fromEntries(Object.keys(names).map(variant => [variant, colors(variant, theme, settings, foundation)]))
    ]))
  });
  window.dssSelectButtonState = (variant, selectedState) => {
    if (!Object.prototype.hasOwnProperty.call(names, variant) || !states.includes(selectedState)) return;
    b.variant = variant;
    b.selectedState = selectedState;
    controls();
    render();
    window.dssAutosave?.();
  };
  window.dssSetButtonContrastColour = (variant, property, value) => {
    if ((value !== null && !validColor(value)) || !Object.prototype.hasOwnProperty.call(names, variant)) return;
    if (property === 'focus') b.focus = value === null ? defaults.focus : value;
    else if (['text', 'bg', 'hover', 'active', 'hoverText', 'activeText', 'border'].includes(property)) {
      b.overrides[variant] = { ...b.overrides[variant] };
      if (value === null) delete b.overrides[variant][property];
      else b.overrides[variant][property] = value;
    } else return;
    controls();
    render();
    window.dssAutosave?.();
  };
  window.dssResetButtonColourOverrides = variant => {
    if (!Object.prototype.hasOwnProperty.call(names, variant)) return;
    delete b.overrides[variant];
    controls(); render(); window.dssAutosave?.();
  };
  window.dssGetButtonDefaultContrastColour = (variant, property, theme = state.theme) => {
    if (!Object.prototype.hasOwnProperty.call(names, variant)) return null;
    if (property === 'focus') return defaults.focus;
    if (!['text', 'bg', 'hover', 'active'].includes(property)) return null;
    const settings = JSON.parse(JSON.stringify(b));
    if (settings.overrides[variant]) delete settings.overrides[variant][property];
    return colors(variant, theme, settings,{...state,colourTransparency:{}})[property === 'text' ? 'fg' : property];
  };
  DSStudio.buttons = { specimen: btn, css: buttonCSS, matrix, elevation, sourceLabel, names, states, stateLabels };
  controls();
  render();
})();
