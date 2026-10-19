'use strict';
/* STATE: all user-editable foundation values live in one plain object.
JSON import validates fields; exporting never executes imported code. */
/* BRAND SOURCE OF TRUTH: illustrative colours for the example preset.
The palette is immutable in this example preset. You can experiment
with editable interface colours without changing the reference swatch list. */
const EXAMPLE_PALETTE = {
  primary: [
    ['White', '#FFFFFF'],
    ['Deep blue', '#004780'],
    ['Dark grey', '#495965']
  ],
  accent: [
    ['Teal', '#00BADC'],
    ['Turquoise', '#5FC5BF'],
    ['Orange', '#F37327'],
    ['Blue', '#2B71B9'],
    ['Green', '#CBDB2A'],
    ['Fuchsia', '#EF426F'],
    ['Light blue', '#57B7E7'],
    ['Yellow', '#FFEF00']
  ]
};

function renderBrand() {
  const make = (items, role) => items.map(([name, hex]) => `<div class="brand-swatch"><div class="brand-swatch-color" style="background:${hex}"></div><div class="brand-swatch-info"><strong>${name}</strong><code>${hex}</code><button type="button" data-brand-role="${role}" data-brand-hex="${hex}" aria-label="Use ${name} as ${role} colour">Use as ${role==='accent'?'accent':'UI primary'}</button></div></div>`).join('');
  $('brandPrimary').innerHTML = make(EXAMPLE_PALETTE.primary, 'primary');
  $('brandAccents').innerHTML = make(EXAMPLE_PALETTE.accent, 'accent');
  document.querySelectorAll('[data-brand-role]').forEach(btn => btn.addEventListener('click', () => {
    const role = btn.dataset.brandRole;
    state[role] = btn.dataset.brandHex.toLowerCase();
    $(role).value = state[role];
    apply();
    announce('Selected example palette swatch as an editable UI role.');
  }));
}
const DEFAULT = {
  project: 'My Project',
  theme: 'light',
  method: 'mix',
  primary: '#004780',
  secondary: '#495965',
  accent: '#cbdb2a',
  font: 'Arial, Helvetica, sans-serif',
  base: 16,
  ratio: 1.25,
  leading: 1.55,
  spacing: 4,
  radius: 12
};
let state = {
    ...DEFAULT
  },
  codeTab = 'css';
const $ = id => document.getElementById(id);
const steps = [50, 100, 200, 300, 400, 500, 600, 700, 800, 900, 950],
  mixes = [.95, .85, .7, .5, .25, 0, -.1, -.25, -.4, -.65, -.85];
const clamp = (x, min, max) => Math.min(max, Math.max(min, x));
const round = (n, p = 2) => Number(n.toFixed(p));

function hexRgb(hex) {
  const s = hex.replace('#', '');
  return [0, 2, 4].map(i => parseInt(s.slice(i, i + 2), 16));
}

function rgbHex(rgb) {
  return '#' + rgb.map(x => clamp(Math.round(x), 0, 255).toString(16).padStart(2, '0')).join('').toUpperCase();
}

function rgbMix(hex, m) {
  return rgbHex(hexRgb(hex).map(c => m >= 0 ? c + (255 - c) * m : c * (1 + m)));
}
/* OKLCH: sRGB <-> linear RGB <-> Oklab <-> OKLCH.
Convert to linear light before matrix operations. Reduce chroma
iteratively when a colour falls outside the sRGB display gamut. */
const srgbToLinear = c => {
  c /= 255;
  return c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4
};
const linearToSrgb = c => c <= .0031308 ? 12.92 * c : 1.055 * Math.max(0, c) ** (1 / 2.4) - .055;

function rgbToOklch(hex) {
  const [r, g, b] = hexRgb(hex).map(srgbToLinear);
  const l = Math.cbrt(.4122214708 * r + .5363325363 * g + .0514459929 * b),
    m = Math.cbrt(.2119034982 * r + .6806995451 * g + .1073969566 * b),
    s = Math.cbrt(.0883024619 * r + .2817188376 * g + .6299787005 * b);
  const L = .2104542553 * l + .793617785 * m - .0040720468 * s,
    a = 1.9779984951 * l - 2.428592205 * m + .4505937099 * s,
    b2 = .0259040371 * l + .7827717662 * m - .808675766 * s;
  return [L, Math.hypot(a, b2), Math.atan2(b2, a)];
}

function oklchRgb(L, C, h) {
  const a = C * Math.cos(h),
    b = C * Math.sin(h);
  const l = (L + .3963377774 * a + .2158037573 * b) ** 3,
    m = (L - .1055613458 * a - .0638541728 * b) ** 3,
    s = (L - .0894841775 * a - 1.291485548 * b) ** 3;
  return [(4.0767416621 * l - 3.3077115913 * m + .2309699292 * s), (-1.2684380046 * l + 2.6097574011 * m - .3413193965 * s), (-.0041960863 * l - .7034186147 * m + 1.707614701 * s)].map(linearToSrgb);
}

function oklchHex(L, C, h) {
  let vals = oklchRgb(L, C, h);
  for (let i = 0; i < 32 && vals.some(v => v < 0 || v > 1 || !Number.isFinite(v)); i++) {
    C *= .88;
    vals = oklchRgb(L, C, h);
  }
  return rgbHex(vals.map(v => clamp(v, 0, 1) * 255));
}

function makeRamp(hex, method) {
  if (method === 'mix') return Object.fromEntries(steps.map((s, i) => [s, s === 500 ? hex.toUpperCase() : rgbMix(hex, mixes[i])]));
  const [L, C, h] = rgbToOklch(hex);
  return Object.fromEntries(steps.map((s, i) => {
    if (s === 500) return [s, hex.toUpperCase()];
    const t = i / 10;
    const targetL = t < .5 ? (.98 + (L - .98) * t / .5) : (L + (.18 - L) * (t - .5) / .5);
    const targetC = C * (.2 + .8 * (1 - Math.abs(t - .5) * 2) ** .6);
    return [s, oklchHex(targetL, targetC, h)];
  }));
}

function lum(hex) {
  const v = hexRgb(hex).map(srgbToLinear);
  return .2126 * v[0] + .7152 * v[1] + .0722 * v[2];
}

function contrast(a, b) {
  const [x, y] = [lum(a), lum(b)].sort((a, b) => b - a);
  return (x + .05) / (y + .05);
}

function onColor(hex) {
  return contrast(hex, '#FFFFFF') >= contrast(hex, '#14253A') ? '#FFFFFF' : '#14253A';
}

function palette() {
  const p = makeRamp(state.primary, state.method),
    s = makeRamp(state.secondary, state.method),
    a = makeRamp(state.accent, state.method);
  const dark = state.theme === 'dark';
  const roles = dark ? {
    background: '#0B1422',
    surface: '#152236',
    'surface-muted': '#20324B',
    text: '#EEF4FC',
    'text-muted': '#B8C8DB',
    border: '#60748D',
    primary: p[300],
    'on-primary': onColor(p[300]),
    'primary-hover': p[200],
    secondary: s[300],
    'on-secondary': onColor(s[300]),
    accent: a[300],
    'on-accent': onColor(a[300]),
    success: '#4ADE80',
    warning: '#FBBF24',
    danger: '#FCA5A5',
    focus: '#FBBF24'
  } : {
    background: '#F3F6FA',
    surface: '#FFFFFF',
    'surface-muted': '#EDF2F7',
    text: '#14253A',
    'text-muted': '#53657A',
    border: '#C5D0DD',
    primary: p[500],
    'on-primary': onColor(p[500]),
    'primary-hover': p[700],
    secondary: s[700],
    'on-secondary': onColor(s[700]),
    accent: a[500],
    'on-accent': onColor(a[500]),
    success: '#15803D',
    warning: '#A85C00',
    danger: '#B91C1C',
    focus: '#9D5700'
  };
  return {
    p,
    s,
    a,
    roles
  };
}

function apply() {
  const {
    p,
    s,
    a,
    roles
  } = palette(), root = document.documentElement;
  root.dataset.theme = state.theme;
  root.style.colorScheme = state.theme;
  for (const [k, v] of Object.entries(roles)) root.style.setProperty('--' + k, v);
  root.style.setProperty('--font-ui', state.font);
  root.style.setProperty('--base-size', state.base + 'px');
  root.style.setProperty('--body-leading', state.leading);
  root.style.setProperty('--space-unit', state.spacing + 'px');
  root.style.setProperty('--radius-base', state.radius + 'px');
  root.style.setProperty('--card-radius', state.radius + 'px');
  root.style.setProperty('--button-radius', Math.round(state.radius * .7) + 'px');
  root.style.setProperty('--primary-hover', roles['primary-hover']);
  $('themeToggle').textContent = state.theme === 'light' ? 'Switch to dark' : 'Switch to light';
  $('rampMethodLabel').textContent = state.method === 'mix' ? 'RGB mix' : 'OKLCH';
  ['primary', 'secondary', 'accent'].forEach(k => $(k + 'Out').textContent = state[k].toUpperCase());
  ['base', 'ratio', 'leading', 'spacing', 'radius'].forEach(k => $(k + 'Out').textContent = state[k] + (k === 'base' || k === 'spacing' || k === 'radius' ? 'px' : ''));
  $('brandAccent').value = EXAMPLE_PALETTE.accent.some(([, hex]) => hex.toLowerCase() === state.accent.toLowerCase()) ? state.accent.toUpperCase() : '';
  renderRamps({
    primary: p,
    secondary: s,
    accent: a
  });
  renderRoles(roles);
  renderType();
  renderSpacing();
  renderContrast(roles);
  renderInspector(roles);
  renderCode();
}

function renderRamps(all) {
  $('ramps').innerHTML = Object.entries(all).map(([name, r]) => `<div class="ramp-group"><strong>${name[0].toUpperCase()+name.slice(1)} ramp</strong><div class="ramp">${steps.map(s=>`<div class="ramp-cell" title="${name}-${s}: ${r[s]}" style="background:${r[s]}"></div>`).join('')}</div><div class="ramp-labels">${steps.map(s=>`<span>${s}</span>`).join('')}</div><p class="help">Anchor 500: <code>${r[500]}</code> · Lightest 50: <code>${r[50]}</code> · Darkest 950: <code>${r[950]}</code></p></div>`).join('');
}

function renderRoles(roles) {
  $('semanticSwatches').innerHTML = Object.entries(roles).map(([k, v]) => `<div class="swatch"><div class="paint" style="background:${v}"></div><div class="swatch-text"><strong>--${k}</strong><code>${v}</code></div></div>`).join('');
}

function sizes() {
  return [-2, -1, 0, 1, 2, 3, 4, 5].map(n => ({
    name: n < 0 ? 'xs' + Math.abs(n) : n === 0 ? 'base' : 'step ' + n,
    size: round(state.base * state.ratio ** n, 1)
  }));
}
const CLAMP_DEFAULTS = {
  minWidth: 375,
  maxWidth: 1280,
  mobileFactor: .82
};
let clampConfig = {
  ...CLAMP_DEFAULTS
};

function fluidTypeBounds(step) {
  const full = state.base * Math.pow(state.ratio, step);
  return {
    full,
    min: full * (step >= 3 ? clampConfig.mobileFactor : 1)
  };
}

function fluidTypePx(step, viewport) {
  const {
    full,
    min
  } = fluidTypeBounds(step), {
    minWidth,
    maxWidth
  } = clampConfig;
  return round(Math.max(min, Math.min(full, min + (full - min) * (viewport - minWidth) / (maxWidth - minWidth))), 1);
}

function fluidTypeCss(step, unit = 'vw') {
  const {
    full,
    min
  } = fluidTypeBounds(step), {
    minWidth,
    maxWidth
  } = clampConfig;
  const slope = (full - min) / (maxWidth - minWidth) * 100;
  const offset = min - slope * minWidth / 100;
  // rem offsets scale with user root font preferences; 16px is the nominal root.
  return `clamp(${round(min/16,5)}rem, calc(${round(offset/16,5)}rem + ${round(slope,5)}${unit}), ${round(full/16,5)}rem)`;
}

function syncFluidTypography() {
  const frame = $('previewFrame');
  if (!frame) return;
  for (const [key, step] of [
      ['display', 5],
      ['h1', 4],
      ['h2', 3],
      ['body', 0],
      ['small', -1]
    ]) {
    frame.style.setProperty('--preview-type-' + key, fluidTypeCss(step, 'cqi'));
  }
  frame.style.setProperty('--preview-leading', state.leading);
  frame.style.setProperty('--preview-font', state.font);
  const width = frame.dataset.width === 'fluid' ? Math.round(frame.getBoundingClientRect().width) : ({
    mobile: 375,
    tablet: 768,
    desktop: 1280
  })[frame.dataset.width] || 1280;
  const readout = $('responsiveTypeReadout');
  if (readout) readout.textContent = `At ${width}px: Display ${fluidTypePx(5,width)}px · H1 ${fluidTypePx(4,width)}px · H2 ${fluidTypePx(3,width)}px · Body ${fluidTypePx(0,width)}px · Small ${fluidTypePx(-1,width)}px`;
}

function renderType() {
  const sz = sizes(),
    spec = (id, viewport) => {
      $(id).innerHTML = [{
        role: 'Display',
        n: 5
      }, {
        role: 'H1',
        n: 4
      }, {
        role: 'H2',
        n: 3
      }, {
        role: 'Body',
        n: 0
      }, {
        role: 'Small',
        n: -1
      }].map(o => {
        const px = fluidTypePx(o.n, viewport);
        return `<div class="type-row"><small>${o.role}<br>${px}px</small><div class="sample" style="font-size:${px}px;line-height:${o.n>0?1.18:state.leading};font-weight:${o.n>0?700:400}">${o.role==='Body'?'Build a clear and readable interface.':o.role==='Small'?'Labels and supporting details':'Design for people'}</div></div>`;
      }).join('');
    };
  spec('mobileType', 375);
  spec('desktopType', 1280);
  $('typeLadder').innerHTML = sz.map(o => `<div class="type-row"><small>${o.name}<br>${o.size}px</small><div class="sample" style="font-size:${o.size}px;line-height:1.2">Aa Bb Cc — Typography</div></div>`).join('');
  syncFluidTypography();
}

function renderSpacing() {
  $('spacingBars').innerHTML = [1, 2, 3, 4, 6, 8, 12].map(n => `<div class="space-row"><span>space-${n}<br>${n*state.spacing}px</span><i style="width:${n*state.spacing*2}px"></i></div>`).join('');
}

function renderContrast(roles) {
  const pairs = [
    ['Body text', 'text', 'surface', 4.5],
    ['Muted text', 'text-muted', 'surface', 4.5],
    ['Primary button', 'on-primary', 'primary', 4.5],
    ['Secondary button', 'on-secondary', 'secondary', 4.5],
    ['Accent button', 'on-accent', 'accent', 4.5]
  ];
  $('contrastChecks').innerHTML = pairs.map(([name, fg, bg, threshold]) => {
    const r = contrast(roles[fg], roles[bg]);
    return `<div class="contrast"><span><strong>${name}</strong><br><small>${fg} on ${bg}</small></span><span style="background:${roles[bg]};color:${roles[fg]};padding:8px 12px;border-radius:6px">Sample Aa</span><strong>${round(r)}:1 · ${r>=threshold?'PASS':'REVIEW'}</strong></div>`;
  }).join('');
}

function renderInspector(roles) {
  const names = ['primary', 'on-primary', 'text', 'text-muted', 'background', 'surface', 'surface-muted', 'border'];
  $('tokenInspector').innerHTML = names.map(k => `<div class="token-item"><strong>--${k}</strong><code>${roles[k]}</code><span class="help">${k==='primary'?'Foundation ramp → semantic primary → button':k==='surface'?'Semantic surface → card background':k==='text'?'Semantic text → body and headings':'Semantic role → multiple components'}</span></div>`).join('');
}

function cssExport() {
  const {
    p,
    s,
    a,
    roles
  } = palette();
  const other = state.theme === 'light' ? 'dark' : 'light';
  const saved = state.theme;
  state.theme = other;
  const opposite = palette().roles;
  state.theme = saved;
  const foundation = Object.entries({
    primary: p,
    secondary: s,
    accent: a
  }).flatMap(([name, r]) => steps.map(s => `  --${name}-${s}: ${r[s]};`)).join('\n');
  const semantic = r => Object.entries(r).map(([k, v]) => `  --${k}: ${v};`).join('\n');
  const sz = sizes();
  return `/* Design System Studio V4.1 — ${state.project.replace(/\*\//g,'')}\n   Studio-generated starting point. Review contrast and project requirements.\n   Foundation → Semantic → Components. */\n:root {\n  /* EXAMPLE PALETTE: fixed reference colours. */\n  --example-white: #FFFFFF;\n  --example-blue: #004780;\n  --example-dark-grey: #495965;\n  --example-accent-teal: #00BADC;\n  --example-accent-turquoise: #5FC5BF;\n  --example-accent-orange: #F37327;\n  --example-accent-blue: #2B71B9;\n  --example-accent-green: #CBDB2A;\n  --example-accent-fuchsia: #EF426F;\n  --example-accent-light-blue: #57B7E7;\n  --example-accent-yellow: #FFEF00;\n\n  /* FOUNDATION: generated ramps extend the reference palette. Step 500 is your chosen HEX. */\n${foundation}\n\n  /* FOUNDATION: typography. Arial is the default system font. */\n  --font-ui: ${state.font};\n  --font-size-base: ${state.base}px;\n  --type-ratio: ${state.ratio};\n${sz.map((o,i)=>`  --text-step-${i}: ${o.size}px;`).join('\n')}\n  --text-display: ${fluidTypeCss(5)};
--text-h1: ${fluidTypeCss(4)};
--text-h2: ${fluidTypeCss(3)};
--text-body: ${fluidTypeCss(0)};
--text-small: ${fluidTypeCss(-1)};\n  --body-leading: ${state.leading};\n  --heading-leading: 1.18;\n\n  /* FOUNDATION: spacing and corners */\n  --space-unit: ${state.spacing}px;\n  --space-2: calc(var(--space-unit) * 2);\n  --space-4: calc(var(--space-unit) * 4);\n  --radius-base: ${state.radius}px;\n\n  /* SEMANTIC: light theme roles */\n${semantic(saved==='light'?roles:opposite)}\n}\n/* SEMANTIC: dark theme swaps roles, not component rules. */\n[data-theme="dark"] {\n  color-scheme: dark;\n${semantic(saved==='dark'?roles:opposite)}\n}\n/* COMPONENT: responsive, reusable and accessible starting points. */\nbody { margin: 0; font: var(--text-body)/var(--body-leading) var(--font-ui); background: var(--background); color: var(--text); }\n.container { width: min(100% - 2rem, 72rem); margin-inline: auto; }\n.page-title { font-size: var(--text-display); line-height: var(--heading-leading); }
.heading-1 { font-size: var(--text-h1); line-height: var(--heading-leading); }
.heading-2 { font-size: var(--text-h2); line-height: var(--heading-leading); }
.small-text { font-size: var(--text-small); }\n.card-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 15rem), 1fr)); gap: var(--space-4); }\n.card { padding: var(--space-4); border: 1px solid var(--border); border-radius: var(--radius-base); background: var(--surface); }\n.button { padding: var(--space-2) var(--space-4); border: 0; border-radius: calc(var(--radius-base) * .7); background: var(--primary); color: var(--on-primary); }\n.button:hover { background: var(--primary-hover); }\n:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }\n@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; animation-duration: .01ms !important; } }\n`;
}

function htmlExport() {
  return `<!doctype html>\n<html lang="en" data-theme="${state.theme}">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>${escapeHtml(state.project)}<\/title>\n  <!-- Save the exported CSS alongside this file. -->\n  <link rel="stylesheet" href="tokens.css">\n<\/head>\n<body>\n  <main class="container">\n    <h1 class="page-title">${escapeHtml(state.project)}</h1>\n    <p>A responsive example using semantic design tokens.</p>\n    <div class="card-grid">\n      <article class="card"><h2>Colour</h2><p>Primary, surface, and text roles.</p><button class="button">Explore</button></article>\n      <article class="card"><h2>Typography</h2><p>Responsive type and readable leading.</p></article>\n      <article class="card"><h2>Layout</h2><p>CSS Grid automatically adapts to space.</p></article>\n    </div>\n  <\/main>\n<\/body>\n<\/html>\n`;
}

function escapeHtml(s) {
  return s.replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;').replaceAll('"', '&quot;');
}
/* FIX: one function produces the project JSON, so Save JSON, the JSON tab and
"Download visible code" always agree. Later scripts extend it instead of
hijacking button clicks. */
function projectJson() {
  return JSON.stringify({
    schemaVersion: 2,
    brandReference: "Studio example palette",
    clampConfig: { ...clampConfig },
    ...state
  }, null, 2);
}

function codeContent() {
  return codeTab === 'css' ? cssExport() : codeTab === 'json' ? projectJson() : htmlExport();
}

function renderCode() {
  $('codeView').textContent = codeContent();
  [
    ['viewCss', 'css'],
    ['viewJson', 'json'],
    ['viewHtml', 'html']
  ].forEach(([id, t]) => {
    $(id).setAttribute('aria-selected', String(codeTab === t));
    $(id).tabIndex = codeTab === t ? 0 : -1;
    if (codeTab === t) $('codeView').setAttribute('aria-labelledby', id);
  });
}

function download(name, content, type) {
  const blob = new Blob([content], {
      type
    }),
    url = URL.createObjectURL(blob),
    a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}
/* FIX: renamed from status() — a global function called "status" collides with the built-in window.status property. */
function announce(msg) {
  $('liveStatus').textContent = msg;
}

function syncControls() {
  Object.keys(DEFAULT).filter(k => $(k)).forEach(k => $(k).value = state[k]);
}
/* FIX: a single reset path. Other modules listen for "dss:reset" so they only reset
when a reset actually happens (previously they reset even when the confirm box was cancelled). */
function resetStudio(msg) {
  clampConfig = { ...CLAMP_DEFAULTS };
  state = {
    ...DEFAULT
  };
  syncControls();
  document.dispatchEvent(new Event('dss:reset'));
  apply();
  if (msg) announce(msg);
}
const validHex = s => typeof s === 'string' && /^#[0-9a-f]{6}$/i.test(s);

function importConfig(obj) {
  if (!obj || typeof obj !== 'object' || Array.isArray(obj)) throw Error('Not a valid project configuration');
  const n = {
    ...DEFAULT
  };
  for (const k of ['primary', 'secondary', 'accent'])
    if (validHex(obj[k])) n[k] = obj[k].toLowerCase();
  if (['light', 'dark'].includes(obj.theme)) n.theme = obj.theme;
  if (['mix', 'oklch'].includes(obj.method)) n.method = obj.method;
  if (['Arial, Helvetica, sans-serif', "Georgia, 'Times New Roman', serif", 'Verdana, Geneva, sans-serif', 'system-ui, sans-serif'].includes(obj.font)) n.font = obj.font;
  for (const [k, min, max] of [
      ['base', 14, 22],
      ['ratio', 1.125, 1.5],
      ['leading', 1.3, 1.9],
      ['spacing', 3, 8],
      ['radius', 0, 28]
    ])
    if (typeof obj[k] === 'number' && Number.isFinite(obj[k])) n[k] = clamp(obj[k], min, max);
  if (typeof obj.project === 'string') n.project = obj.project.slice(0, 90);
  clampConfig = { ...CLAMP_DEFAULTS };
  for (const [key, min, max] of [
      ['minWidth', 320, 600],
      ['maxWidth', 900, 1600],
      ['mobileFactor', .7, 1]
    ]) {
    const value = obj.clampConfig?.[key];
    if (typeof value === 'number' && Number.isFinite(value)) clampConfig[key] = clamp(value, min, max);
  }
  state = n;
  syncControls();
  apply();
}
['project', 'method', 'primary', 'secondary', 'accent', 'font', 'base', 'ratio', 'leading', 'spacing', 'radius'].forEach(k => $(k).addEventListener('input', e => {
  state[k] = ['base', 'ratio', 'leading', 'spacing', 'radius'].includes(k) ? Number(e.target.value) : e.target.value;
  apply();
}));
$('brandAccent').addEventListener('change', e => {
  if (e.target.value) {
    state.accent = e.target.value.toLowerCase();
    $('accent').value = state.accent;
    apply();
  }
});
$('restoreDefaults').addEventListener('click', () => resetStudio('Example defaults restored.'));
$('themeToggle').addEventListener('click', () => {
  state.theme = state.theme === 'light' ? 'dark' : 'light';
  apply();
});
$('resetBtn').addEventListener('click', () => {
  if (confirm('Reset all studio settings to the example defaults?')) resetStudio('Settings reset.');
});
$('saveBtn').addEventListener('click', () => {
  download('design-system-studio.json', projectJson(), 'application/json');
  announce('Project JSON downloaded.');
});
$('loadBtn').addEventListener('click', () => $('loadFile').click());
$('loadFile').addEventListener('change', async e => {
  const file = e.target.files?.[0];
  if (!file) return;
  try {
    if (file.size > 100000) throw Error('JSON file is too large');
    importConfig(JSON.parse(await file.text()));
    document.dispatchEvent(new Event('dss:imported'));
    announce('Project configuration loaded.');
  } catch (err) {
    alert('Could not load configuration: ' + err.message);
  }
  e.target.value = '';
});
$('cssBtn').addEventListener('click', () => {
  download('tokens.css', cssExport(), 'text/css');
  announce('Commented CSS downloaded.');
});
$('copyCode').addEventListener('click', async () => {
  try {
    await navigator.clipboard.writeText(codeContent());
    announce('Code copied.');
  } catch {
    announce('Clipboard unavailable; select code and copy manually.');
  }
});
$('downloadCode').addEventListener('click', () => download(codeTab === 'css' ? 'tokens.css' : codeTab === 'json' ? 'design-system-studio.json' : 'example.html', codeContent(), codeTab === 'css' ? 'text/css' : codeTab === 'json' ? 'application/json' : 'text/html'));
[
  ['viewCss', 'css'],
  ['viewJson', 'json'],
  ['viewHtml', 'html']
].forEach(([id, t]) => $(id).addEventListener('click', () => {
  codeTab = t;
  renderCode();
}));
const codeTabs = ['viewCss', 'viewJson', 'viewHtml'];
codeTabs.forEach((id, index) => $(id).addEventListener('keydown', event => {
  let next;
  if (event.key === 'ArrowRight') next = (index + 1) % codeTabs.length;
  else if (event.key === 'ArrowLeft') next = (index + codeTabs.length - 1) % codeTabs.length;
  else if (event.key === 'Home') next = 0;
  else if (event.key === 'End') next = codeTabs.length - 1;
  else return;
  event.preventDefault();
  $(codeTabs[next]).click();
  $(codeTabs[next]).focus();
}));
/* FIX: only the width tab buttons. The old selector "[data-width]" also matched the preview frame itself,
so clicking anywhere inside the preview un-pressed every width tab. */
function updateResponsivePreview(w) {
  const frame = $('previewFrame'),
    shell = $('previewShell'),
    status = $('previewWidthStatus');
  frame.dataset.width = w;
  document.querySelectorAll('.tabs [data-width]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.width === w)));
  // On narrower screens, keep the real preview width and allow horizontal scrolling.
  const sync = () => {
    const overflows = frame.getBoundingClientRect().width > shell.clientWidth - 24;
    shell.dataset.previewOverflow = String(overflows);
    status.textContent = w === 'fluid' ? 'Fluid preview: fills the available preview area.' :
      `${({mobile:375,tablet:768,desktop:1280})[w]} px viewport` + (overflows ? ' — scroll horizontally to inspect the full-width page.' : ' — fully visible.');
  };
  requestAnimationFrame(() => {
    sync();
    syncFluidTypography();
  });
  shell.scrollLeft = 0;
}
document.querySelectorAll('.tabs [data-width]').forEach(btn => btn.addEventListener('click', () => updateResponsivePreview(btn.dataset.width)));
updateResponsivePreview($('previewFrame').dataset.width);
window.addEventListener('resize', () => syncFluidTypography());
renderBrand();
syncControls();
apply();
