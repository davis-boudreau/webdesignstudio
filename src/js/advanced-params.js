'use strict';
/* V2.6 Advanced parameters: these values are separate from the immutable example palette reference. */
/* FIX: defaults now match the light-theme palette. The old focus default (#00BADC teal) is only ~2.2:1
against white, which fails the 3:1 non-text contrast minimum for focus indicators. */
const ADV_DEFAULT = {
  state: 'default',
  focus: 3,
  height: 42,
  weight: 700,
  measure: 65,
  tracking: -2,
  border: 1,
  shadow: 'none',
  opacity: 100,
  columns: 210,
  gap: 12,
  align: 'stretch',
  reduce: false,
  underline: true,
  motion: 150,
  colors: {
    success: '#15803D',
    warning: '#A85C00',
    danger: '#B91C1C',
    focus: '#9D5700'
  }
};
let adv = JSON.parse(JSON.stringify(ADV_DEFAULT));
const advColorNames = {
  success: 'Success',
  warning: 'Warning',
  danger: 'Error / danger',
  focus: 'Focus indicator'
};
const advColors = document.getElementById('advColors');
advColors.innerHTML = Object.entries(advColorNames).map(([key, label]) => `<div class="field"><label for="advColor_${key}">${label}</label><div class="palette-line"><input type="color" id="advColor_${key}" value="${adv.colors[key].toLowerCase()}"><output id="advColor_${key}Out">${adv.colors[key]}</output></div></div>`).join('');
const advMap = {
  advState: 'state',
  advFocus: 'focus',
  advHeight: 'height',
  advWeight: 'weight',
  advMeasure: 'measure',
  advTracking: 'tracking',
  advBorder: 'border',
  advShadow: 'shadow',
  advOpacity: 'opacity',
  advColumns: 'columns',
  advGap: 'gap',
  advAlign: 'align',
  advReduce: 'reduce',
  advUnderline: 'underline',
  advMotion: 'motion'
};
const numeric = new Set(['focus', 'height', 'weight', 'measure', 'tracking', 'border', 'opacity', 'columns', 'gap', 'motion']);
/* FIX: feedback colours are now part of the light-theme semantic roles.
Previously they were written into a second :root block that also overrode the dark theme,
and apply() silently replaced them in the live preview. */
const basePalette = palette;
palette = function() {
  const result = basePalette();
  if (state.theme === 'light') Object.assign(result.roles, adv.colors);
  return result;
};

function syncAdvanced() {
  for (const [id, key] of Object.entries(advMap)) {
    const el = document.getElementById(id);
    if (el.type === 'checkbox') el.checked = adv[key];
    else el.value = adv[key];
  }
  for (const key of Object.keys(adv.colors)) document.getElementById('advColor_' + key).value = adv.colors[key].toLowerCase();
  applyAdvanced();
}

function applyAdvanced() {
  const root = document.documentElement;
  const vars = {
    '--focus-width-demo': adv.focus + 'px',
    '--control-height': adv.height + 'px',
    '--border-width-demo': adv.border + 'px',
    '--shadow-demo': ({
      none: 'none',
      subtle: '0 2px 8px #00000018',
      medium: '0 6px 20px #00000028',
      strong: '0 12px 32px #00000040'
    })[adv.shadow],
    '--demo-measure': adv.measure + 'ch',
    '--demo-tracking': adv.tracking / 100 + 'em',
    '--demo-heading-weight': adv.weight,
    '--demo-grid-min': adv.columns + 'px',
    '--demo-grid-gap': adv.gap + 'px',
    '--demo-align': adv.align,
    '--demo-motion': (adv.reduce ? 0 : adv.motion) + 'ms'
  };
  for (const [k, v] of Object.entries(vars)) root.style.setProperty(k, v);
  const roles = palette().roles;
  for (const key of Object.keys(adv.colors)) root.style.setProperty('--' + key, roles[key]);
  document.querySelectorAll('.preview-grid').forEach(el => {
    el.style.gridTemplateColumns = `repeat(auto-fit,minmax(min(100%,${adv.columns}px),1fr))`;
    el.style.gap = adv.gap + 'px';
    el.style.alignItems = adv.align;
  });
  document.querySelectorAll('.preview-frame p').forEach(el => el.style.maxWidth = adv.measure + 'ch');
  document.querySelectorAll('.preview-frame h3').forEach(el => {
    el.style.fontWeight = adv.weight;
    el.style.letterSpacing = adv.tracking / 100 + 'em';
  });
  document.querySelectorAll('.preview-card,.component.muted-surface').forEach(el => el.style.opacity = adv.opacity / 100);
  document.querySelectorAll('a').forEach(el => {
    if (!el.closest('.studio-section-nav')) el.style.textDecoration = adv.underline ? 'underline' : 'none';
  });
  document.querySelectorAll('.demo-btn').forEach(el => el.style.transitionDuration = (adv.reduce ? 0 : adv.motion) + 'ms');
  const btn = document.getElementById('advDemoButton'),
    inp = document.getElementById('advDemoInput');
  for (const id of ['stateButtonTile', 'stateInputTile']) document.getElementById(id).dataset.state = adv.state;
  btn.disabled = ['disabled', 'loading'].includes(adv.state);
  inp.disabled = adv.state === 'disabled';
  inp.readOnly = adv.state === 'readonly';
  inp.setAttribute('aria-invalid', String(adv.state === 'invalid'));
  /* FIX: aria-pressed="false" turns an ordinary button into a toggle for screen readers; only add it when selected. */
  if (adv.state === 'selected') btn.setAttribute('aria-pressed', 'true');
  else btn.removeAttribute('aria-pressed');
  document.getElementById('advStateLabel').textContent = adv.state.charAt(0).toUpperCase() + adv.state.slice(1);
  document.getElementById('advInputHelp').textContent = adv.state === 'invalid' ? 'Error: please enter a valid email address' : adv.state === 'success' ? 'Success: input looks valid' : 'Surface + border + feedback states';
  for (const [id, key] of Object.entries(advMap)) {
    const out = document.getElementById(id + 'Out');
    if (out) out.textContent = String(adv[key]) + (key === 'measure' ? 'ch' : key === 'motion' ? 'ms' : key === 'tracking' ? ' / 100em' : ['focus', 'height', 'border', 'columns', 'gap'].includes(key) ? 'px' : key === 'opacity' ? '%' : '');
  }
  for (const key of Object.keys(adv.colors)) document.getElementById('advColor_' + key + 'Out').textContent = adv.colors[key].toUpperCase();
  if (typeof renderCode === 'function') renderCode();
}
for (const [id, key] of Object.entries(advMap)) {
  const el = document.getElementById(id);
  el.addEventListener(el.type === 'checkbox' || el.tagName === 'SELECT' ? 'change' : 'input', () => {
    adv[key] = el.type === 'checkbox' ? el.checked : numeric.has(key) ? Number(el.value) : el.value;
    applyAdvanced();
  });
}
for (const key of Object.keys(adv.colors)) document.getElementById('advColor_' + key).addEventListener('input', e => {
  adv.colors[key] = e.target.value.toUpperCase();
  apply();
  applyAdvanced();
});
document.getElementById('resetAdvanced').addEventListener('click', () => {
  adv = JSON.parse(JSON.stringify(ADV_DEFAULT));
  apply();
  syncAdvanced();
});
/* Wrap existing exports without changing V2.5 foundation/semantic logic. */
const oldCssExport = cssExport;
cssExport = function() {
  return oldCssExport() + `\n/* V2.6: ADVANCED COMPONENT TOKENS. Feedback colours live in the theme blocks above. */\n:root {\n  --focus-width: ${adv.focus}px;\n  --control-height: ${adv.height}px;\n  --border-width: ${adv.border}px;\n  --heading-weight: ${adv.weight};\n  --reading-measure: ${adv.measure}ch;\n  --heading-tracking: ${adv.tracking/100}em;\n  --grid-card-min: ${adv.columns}px;\n  --grid-gap: ${adv.gap}px;\n  --surface-opacity: ${adv.opacity/100};\n  --elevation: ${({none:'none',subtle:'0 2px 8px #00000018',medium:'0 6px 20px #00000028',strong:'0 12px 32px #00000040'})[adv.shadow]};\n  --motion-duration: ${adv.reduce?0:adv.motion}ms;\n}\n/* Interactive states: visible focus is essential for keyboard navigation. */\n.button { min-height: var(--control-height); border-width: var(--border-width); transition: background var(--motion-duration), transform var(--motion-duration); }\n.button:hover:not(:disabled) { background: var(--primary-hover); }\n.button:active:not(:disabled) { transform: translateY(2px); }\n.button:focus-visible, .input:focus-visible { outline: var(--focus-width) solid var(--focus); outline-offset: 3px; }\n.button:disabled { opacity: .55; cursor: not-allowed; }\n.button[aria-pressed="true"] { box-shadow: 0 0 0 2px var(--primary); }\n.input { min-height: var(--control-height); border: var(--border-width) solid var(--border); }\n.input[aria-invalid="true"] { border-color: var(--danger); }\n.input:read-only { background: var(--surface-muted); }\n.card { box-shadow: var(--elevation); border-width: var(--border-width); }\n.card-grid { gap: var(--grid-gap); grid-template-columns: repeat(auto-fit, minmax(min(100%, var(--grid-card-min)), 1fr)); }\n.page-title { font-weight: var(--heading-weight); letter-spacing: var(--heading-tracking); }\np { max-width: var(--reading-measure); }\na { text-decoration: ${adv.underline?'underline':'none'}; }\n@media (prefers-reduced-motion: reduce) { .button { transition: none; } }\n`
};
projectJson = function() {
  return JSON.stringify({
    schemaVersion: 2.9,
    brandReference: 'Studio example palette',
    ...state,
    advanced: adv
  }, null, 2);
};
const oldImportConfig = importConfig;
importConfig = function(obj) {
  oldImportConfig(obj);
  if (obj.advanced && typeof obj.advanced === 'object') {
    const next = JSON.parse(JSON.stringify(ADV_DEFAULT));
    for (const [id, key] of Object.entries(advMap)) {
      const v = obj.advanced[key];
      if (typeof next[key] === 'boolean' && typeof v === 'boolean') next[key] = v;
      else if (typeof next[key] === 'number' && typeof v === 'number' && Number.isFinite(v)) {
        const el = document.getElementById(id);
        const min = el.min === '' ? -999 : Number(el.min),
          max = el.max === '' ? 999 : Number(el.max);
        next[key] = Math.max(min, Math.min(max, v));
      } else if (typeof next[key] === 'string' && typeof v === 'string' && Array.from(document.getElementById(id).options || []).some(o => o.value === v)) next[key] = v;
    }
    for (const k of Object.keys(next.colors))
      if (validHex(obj.advanced.colors?.[k])) next.colors[k] = obj.advanced.colors[k].toUpperCase();
    adv = next;
  } else adv = JSON.parse(JSON.stringify(ADV_DEFAULT));
  apply();
  syncAdvanced();
};
document.addEventListener('dss:reset', () => {
  adv = JSON.parse(JSON.stringify(ADV_DEFAULT));
  syncAdvanced();
});
syncAdvanced();
