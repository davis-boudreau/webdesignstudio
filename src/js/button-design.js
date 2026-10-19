'use strict';
/* V4.1 Button Design: shared project settings, preview and exported component CSS.
State simulations are labelled; browser-native focus/disabled remain testable. */
(() => {
  const $ = id => document.getElementById(id);
  const defaults = {
    variant: 'primary',
    size: 'md',
    selectedState: 'default',
    padX: 18,
    padY: 12,
    minHeight: 44,
    radius: 8,
    border: 1,
    weight: 600,
    focus: '#B45309',
    focusWidth: 3,
    motion: 150,
    mobileFull: false,
    overrides: {},
    sources: {
      primary: 'primary',
      secondary: 'secondary',
      accent: 'accent',
      outline: 'primary',
      text: 'primary'
    },
    custom: {}
  };
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

  function sourceLabel(v) {
    const source = b.sources[v] || defaults.sources[v];
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

  function clampNumber(v, min, max, fallback) {
    v = Number(v);
    return Number.isFinite(v) ? Math.max(min, Math.min(max, v)) : fallback;
  }

  function validColor(c) {
    return typeof c === 'string' && /^#[0-9a-f]{6}$/i.test(c);
  }

  function sanitize(raw) {
    let b = {
      ...defaults,
      overrides: {},
      sources: {
        ...defaults.sources
      },
      custom: {}
    };
    if (!raw || typeof raw !== 'object') return b;
    for (const [k, lo, hi] of [
        ['padX', 8, 36],
        ['padY', 6, 22],
        ['minHeight', 36, 64],
        ['radius', 0, 28],
        ['border', 1, 4],
        ['focusWidth', 2, 5],
        ['motion', 0, 350]
      ]) b[k] = clampNumber(raw[k], lo, hi, defaults[k]);
    b.weight = [400, 500, 600, 700].includes(Number(raw.weight)) ? Number(raw.weight) : 600;
    b.variant = Object.prototype.hasOwnProperty.call(names, raw.variant) ? raw.variant : 'primary';
    b.size = ['sm', 'md', 'lg'].includes(raw.size) ? raw.size : 'md';
    b.selectedState = states.includes(raw.selectedState) ? raw.selectedState : 'default';
    b.focus = validColor(raw.focus) ? raw.focus : defaults.focus;
    b.mobileFull = raw.mobileFull === true;
    for (const k of Object.keys(names)) {
      const source = raw.sources?.[k];
      if (['primary', 'secondary', 'accent', 'custom'].includes(source) || validColor(source)) b.sources[k] = source;
      if (validColor(raw.custom?.[k])) b.custom[k] = raw.custom[k];
      const item = raw.overrides?.[k];
      if (item && typeof item === 'object') {
        b.overrides[k] = {};
        for (const prop of ['hover', 'active', 'text', 'hoverText', 'activeText', 'bg', 'border'])
          if (validColor(item[prop])) b.overrides[k][prop] = item[prop];
      }
    }
    return b;
  }
  let b = sanitize(state.buttonDesign);

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
    return {
      bg,
      fg,
      border: o.border || (v === 'outline' ? base : 'transparent'),
      hover,
      active,
      hoverText: o.hoverText || readable(hover),
      activeText: o.activeText || readable(active)
    };
  }

  function props(v, size = b.size, mode = state.theme) {
    const c = colors(v, mode),
      scale = size === 'sm' ? .8 : size === 'lg' ? 1.22 : 1;
    return {
      c,
      style: `--bd-focus:${b.focus};--bd-focus-width:${b.focusWidth}px;--bd-motion:${b.motion}ms;background:${c.bg};color:${c.fg};border:${b.border}px solid ${c.border};border-radius:${b.radius}px;min-height:${Math.round(b.minHeight*scale)}px;padding:${Math.round(b.padY*scale)}px ${Math.round(b.padX*scale)}px;font-weight:${b.weight};font-size:${size==='sm'?'0.875rem':size==='lg'?'1.125rem':'1rem'}`
    };
  }

  function esc(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  }

  function btn(v, st = 'default', size = b.size, mode = state.theme, real = false) {
    const p = props(v, size, mode);
    let c = p.c;
    let style = p.style;
    if (st === 'hover') style += `;background:${c.hover};color:${c.hoverText}`;
    if (st === 'active') style += `;background:${c.active};color:${c.activeText}`;
    const disabled = st === 'disabled' ? ' disabled' : '';
    const pressed = st === 'selected' ? ' aria-pressed="true"' : '';
    const busy = st === 'loading' ? ' aria-busy="true"' : '';
    const sim = real ? '' : ` data-sim="${st}"`;
    const label = st === 'loading' ? 'Processing…' : st === 'selected' ? 'Toggle setting' : `${names[v]} action`;
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
      })) $(id).value = val.toLowerCase();
    for (const id of ['bdHover', 'bdActive', 'bdFocus', 'bdText', 'bdHoverText', 'bdActiveText', 'bdDefaultBg', 'bdBorderColor']) $(id + 'Out').textContent = $(id).value.toUpperCase();
  }

  function render() {
    const cc = colors(b.variant);
    const bg = b.selectedState === 'hover' ? cc.hover : b.selectedState === 'active' ? cc.active : cc.bg === 'transparent' ? (state.theme === 'dark' ? '#142434' : '#FFFFFF') : cc.bg;
    const fg = b.selectedState === 'hover' ? cc.hoverText : b.selectedState === 'active' ? cc.activeText : cc.fg;
    const r = ratio(fg, bg);
    $('bdContrast').textContent = `${r.toFixed(2)}:1 — ${r>=4.5?'PASS AA text':'REVIEW: below 4.5:1'}`;
    state.buttonDesign = JSON.parse(JSON.stringify(b));
    $('bdContext').textContent = `${names[b.variant]} · ${b.size.toUpperCase()} · ${b.selectedState}`;
    $('bdDescription').textContent = explain[b.selectedState];
    $('bdSingle').innerHTML = btn(b.variant, b.selectedState, b.size, state.theme, true);
    $('bdThemes').innerHTML = ['light', 'dark'].map(m => `<div class="bd-theme-card" data-mode="${m}"><strong>${m==='light'?'Light':'Dark'} preview</strong>${btn(b.variant,b.selectedState,b.size,m)}</div>`).join('');
    $('bdMatrix').innerHTML = stateGroups.map(group => `<section class="bd-state-group" aria-label="${group.title}"><div class="bd-state-group-heading"><h4>${group.title}</h4><p class="help">${group.description}</p></div>${group.items.map(st=>`<section class="bd-state-section" aria-label="${stateLabels[st]}"><div class="bd-state-section-head"><h5>${stateLabels[st]}</h5><p class="help">${esc(explain[st])}</p></div>${colorGroups.map(type=>`<div class="bd-color-group"><h6>${type.title}</h6><div class="bd-state-grid">${type.variants.map(v=>`<div class="bd-cell"><strong>${names[v]}</strong><span class="bd-source-label">${esc(sourceLabel(v))}</span>${btn(v,st,'md',state.theme)}</div>`).join('')}</div></div>`).join('')}</section>`).join('')}</section>`).join('');
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

  function buttonCSS() {
    const variants = mode => Object.keys(names).map(v => {
      const c = colors(v, mode);
      return `  /* ${names[v]} variant colours */\n  --button-${v}-source: ${baseFor(v)};\n  --button-${v}-bg: ${c.bg};\n  --button-${v}-text: ${c.fg};\n  --button-${v}-border: ${c.border};\n  --button-${v}-hover: ${c.hover};\n  --button-${v}-active: ${c.active};\n  --button-${v}-hover-text: ${c.hoverText};\n  --button-${v}-active-text: ${c.activeText};`;
    }).join('\n');
    return `/* Design System Studio V4.1 · Button component CSS\n   FOUNDATION → COMPONENT TOKENS → STATES.\n   Verify text contrast in each theme and state. */\n:root {\n  --button-pad-x: ${b.padX}px;\n  --button-pad-y: ${b.padY}px;\n  --button-min-height: ${b.minHeight}px;\n  --button-radius: ${b.radius}px;\n  --button-border-width: ${b.border}px;\n  --button-font-weight: ${b.weight};\n  --button-focus: ${b.focus};\n  --button-focus-width: ${b.focusWidth}px;\n  --button-motion: ${b.motion}ms;\n${variants('light')}\n}\n[data-theme="dark"] {\n${variants('dark')}\n}\n/* Base component: reusable for all variants. */\n.ds-button {\n  display: inline-flex; align-items: center; justify-content: center;\n  gap: .5em; min-height: var(--button-min-height);\n  padding: var(--button-pad-y) var(--button-pad-x);\n  border: var(--button-border-width) solid transparent;\n  border-radius: var(--button-radius);\n  font: inherit; font-weight: var(--button-font-weight);\n  cursor: pointer; text-align: center;\n  transition: background-color var(--button-motion), border-color var(--button-motion);\n}\n/* Size variants scale the same foundation dimensions. */\n.ds-button--sm { min-height: calc(var(--button-min-height) * .8); padding: calc(var(--button-pad-y) * .8) calc(var(--button-pad-x) * .8); font-size: .875rem; }\n.ds-button--lg { min-height: calc(var(--button-min-height) * 1.22); padding: calc(var(--button-pad-y) * 1.22) calc(var(--button-pad-x) * 1.22); font-size: 1.125rem; }\n${Object.keys(names).map(v=>`/* ${names[v]} variant and its interactive states. */\n.ds-button--${v} { background: var(--button-${v}-bg); color: var(--button-${v}-text); border-color: var(--button-${v}-border); }\n.ds-button--${v}:hover:not(:disabled) { background: var(--button-${v}-hover); color: var(--button-${v}-hover-text); }\n.ds-button--${v}:active:not(:disabled) { background: var(--button-${v}-active); color: var(--button-${v}-active-text); }`).join('\n')}\n/* Real keyboard focus, not just the preview simulation. */\n.ds-button:focus-visible { outline: var(--button-focus-width) solid var(--button-focus); outline-offset: 3px; }\n/* Native disabled attribute prevents activation. */\n.ds-button:disabled { opacity: .55; cursor: not-allowed; }\n/* aria-pressed is only for persistent toggle buttons. */\n.ds-button[aria-pressed="true"] { box-shadow: 0 0 0 2px var(--button-focus); }\n/* aria-busy requires JavaScript behaviour and status announcements. */\n.ds-button[aria-busy="true"] { cursor: progress; }\n${b.mobileFull?'/* Optional mobile full-width action. */\n@media (max-width: 40rem) { .ds-button--mobile-full { width: 100%; } }\n':''}/* Honour user reduced-motion preferences. */\n@media (prefers-reduced-motion: reduce) { .ds-button { transition: none; } }\n`;
  }
  // Keep existing JSON/project save mechanisms by storing settings inside the shared state.
  const oldImport = importConfig;
  importConfig = function(data) {
    oldImport(data);
    b = sanitize(data?.buttonDesign);
    controls();
    render();
  };
  const oldCss = cssExport;
  cssExport = function() {
    return oldCss() + '\n' + buttonCSS();
  };
  /* FIX: when "Full-width on narrow screens" is on, the example HTML now actually uses the class the CSS defines. */
  const oldHtml = htmlExport;
  htmlExport = function() {
    let html = oldHtml();
    const sizeClass = b.size === 'md' ? '' : ` ds-button--${b.size}`;
    const extra = b.mobileFull ? ' ds-button--mobile-full' : '';
    return html.replace('<\/main>', `<section class="card"><h2>Button system</h2><div class="button-row">${Object.keys(names).map(v=>`<button class="ds-button ds-button--${v}${sizeClass}${extra}" type="button">${names[v]} action</button>`).join('')}<\/div><\/section>\n<\/main>`);
  };
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
    b = sanitize(b);
    controls();
    render();
    window.dssAutosave?.();
    window.dssUpdateTokenCatalogue?.();
  });
  $('bdJump').addEventListener('click', () => $('buttonDesignLab').scrollIntoView({
    behavior: 'smooth',
    block: 'start'
  }));
  $('bdCopy').addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(buttonCSS());
      $('bdCopy').textContent = 'Copied';
    } catch (e) {
      $('bdCopy').textContent = 'Select CSS above to copy';
    }
    setTimeout(() => $('bdCopy').textContent = 'Copy button CSS', 1800);
  });
  $('bdExport').addEventListener('click', () => download('design-system-buttons.css', buttonCSS(), 'text/css'));
  // Update the preview when the global theme or foundation colours change.
  const oldApply = apply;
  apply = function() {
    oldApply();
    render();
  };
  /* FIX: Reset / Restore Example / New project now also reset the button design. */
  document.addEventListener('dss:reset', () => {
    b = sanitize(null);
    controls();
  });
  // Read the same resolved colours as the previews and CSS export.
  window.dssGetButtonContrastData = (settings = b, foundation = state) => ({
    settings: JSON.parse(JSON.stringify(settings)),
    themes: Object.fromEntries(['light', 'dark'].map(theme => [theme,
      Object.fromEntries(Object.keys(names).map(variant => [variant, colors(variant, theme, settings, foundation)]))
    ]))
  });
  window.dssSetButtonContrastColour = (variant, property, value) => {
    if (!validColor(value) || !Object.prototype.hasOwnProperty.call(names, variant)) return;
    if (property === 'focus') b.focus = value;
    else if (['text', 'bg', 'hover', 'active', 'hoverText', 'activeText', 'border'].includes(property)) {
      b.overrides[variant] = { ...b.overrides[variant], [property]: value };
    } else return;
    controls();
    render();
    window.dssAutosave?.();
  };
  controls();
  render();
})();
