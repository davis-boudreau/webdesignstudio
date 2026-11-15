/* V4.1 interactive clamp explorer: one source of truth for all responsive typography. */
(() => {
  const el = id => document.getElementById(id);
  if (!el('clampRole')) return;
  const controls = ['clampBase', 'clampRatio', 'clampMinWidth', 'clampMaxWidth', 'clampFactor', 'clampViewport'];
  const labels = {
    5: 'Display',
    4: 'H1',
    2: 'H3',
    1: 'H4',
    '-2': 'Extra small',
    3: 'H2',
    0: 'Body',
    '-1': 'Small'
  };

  function update() {
    const draft=DSStudio.propertyEditors?.draftSnapshot('typography'),foundation=draft?.state||state,config=draft?.clampConfig||clampConfig;
    el('clampBase').value = foundation.base;
    el('clampRatio').value = foundation.ratio;
    el('clampMinWidth').value = config.minWidth;
    el('clampMaxWidth').value = config.maxWidth;
    el('clampFactor').value = config.mobileFactor;
    render(foundation,config);
  }
  function render(foundation=state,config=clampConfig) {
    const step=Number(el('clampRole').value),v=Number(el('clampViewport').value);
    for (const [id, val] of Object.entries({
        clampBaseOut: foundation.base + 'px',
        clampRatioOut: round(foundation.ratio, 4),
        clampMinWidthOut: config.minWidth + 'px',
        clampMaxWidthOut: config.maxWidth + 'px',
        clampFactorOut: Math.round(config.mobileFactor * 100) + '%',
        clampViewportOut: v + 'px'
      })) el(id).textContent = val;
    const {
      full,
      min
    } = fluidTypeBounds(step,foundation,config), actual = fluidTypePx(step,v,foundation,config), slope = (full - min) / (config.maxWidth - config.minWidth), offset = min - slope * config.minWidth;
    el('clampMinFont').textContent = round(min, 2) + 'px';
    el('clampComputed').textContent = round(actual, 2) + 'px';
    el('clampMaxFont').textContent = round(full, 2) + 'px';
    const token=({5:'--text-display',4:'--text-h1',3:'--text-h2',2:'--text-step-4',1:'--text-step-3',0:'--text-body','-1':'--text-small','-2':'--text-step-0'})[step];
    const rule=[2,1,-2].includes(step)?round(full,4)+'px':fluidTypeCss(step,'vw',0,foundation,config);
    // Use the exported token names; H3/H4/extra-small are fixed modular steps.
    const css = `/* ${labels[step]}: ${foundation.base}px × ${foundation.ratio}^${step} */\n${token}: ${rule};`;
    el('clampCss').textContent = css;
    el('clampMath').textContent = `Maximum = ${foundation.base} × ${foundation.ratio}^${step} = ${round(full,3)}px. Minimum = ${round(min,3)}px. Slope = (${round(full,3)} − ${round(min,3)}) / (${config.maxWidth} − ${config.minWidth}) = ${round(slope,6)} px/px. Preferred = ${round(slope*100,4)}vw + ${round(offset,3)}px (expressed with rem offset in CSS).`;
    el('clampExplanation').textContent = `At ${v}px, the browser clamps the fluid ${labels[step]} value to ${round(actual,2)}px, between ${round(min,2)}px and ${round(full,2)}px.`;
    const x = w => 48 + (w - 320) / 1280 * 572;
    const span = Math.max(full - min, 1);
    const y = px => 142 - (px - min) / span * 102;
    el('clampCurve').setAttribute('d', `M ${x(320)} ${y(fluidTypePx(step,320,foundation,config))} L ${x(config.minWidth)} ${y(min)} L ${x(config.maxWidth)} ${y(full)} L ${x(1600)} ${y(fluidTypePx(step,1600,foundation,config))}`);
    el('clampDot').setAttribute('cx', x(v));
    el('clampDot').setAttribute('cy', y(actual));
  }
  DSStudio.clampExplorer=Object.freeze({render});
  el('clampBase').addEventListener('input', e => {
    state.base = Number(e.target.value);
    if (el('base')) el('base').value = state.base;
    apply();
    update();
  });
  el('clampRatio').addEventListener('input', e => {
    state.ratio = Number(e.target.value);
    if (el('ratio')) el('ratio').value = state.ratio;
    apply();
    update();
  });
  el('clampMinWidth').addEventListener('input', e => {
    clampConfig.minWidth = Math.min(Number(e.target.value), clampConfig.maxWidth - 100);
    apply();
    update();
  });
  el('clampMaxWidth').addEventListener('input', e => {
    clampConfig.maxWidth = Math.max(Number(e.target.value), clampConfig.minWidth + 100);
    apply();
    update();
  });
  el('clampFactor').addEventListener('input', e => {
    clampConfig.mobileFactor = Number(e.target.value);
    apply();
    update();
  });
  el('clampViewport').addEventListener('input', update);
  el('clampRole').addEventListener('change', update);
  el('clampReset').addEventListener('click', () => {
    clampConfig = {
      ...CLAMP_DEFAULTS
    };
    apply();
    update();
  });
  const copyStatus = document.createElement('p');
  copyStatus.className = 'help'; copyStatus.id = 'clampCopyStatus'; copyStatus.setAttribute('role', 'status');
  el('clampCopy').after(copyStatus);
  el('clampCopy').addEventListener('click', async () => {
    const value = el('clampCss').textContent;
    try {
      await navigator.clipboard.writeText(value);
      copyStatus.textContent = 'CSS copied.';
    } catch {
      copyStatus.textContent = 'Clipboard unavailable. Select the CSS above and copy it manually.';
    }
  });
  DSStudio.on('type:updated', update);
  update();
})();
