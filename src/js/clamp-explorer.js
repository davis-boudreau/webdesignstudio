/* V4.1 interactive clamp explorer: one source of truth for all responsive typography. */
(() => {
  const el = id => document.getElementById(id);
  if (!el('clampRole')) return;
  const controls = ['clampBase', 'clampRatio', 'clampMinWidth', 'clampMaxWidth', 'clampFactor', 'clampViewport'];
  const labels = {
    5: 'Display',
    4: 'H1',
    3: 'H2',
    0: 'Body',
    '-1': 'Small'
  };

  function update() {
    const step = Number(el('clampRole').value),
      v = Number(el('clampViewport').value);
    el('clampBase').value = state.base;
    el('clampRatio').value = state.ratio;
    el('clampMinWidth').value = clampConfig.minWidth;
    el('clampMaxWidth').value = clampConfig.maxWidth;
    el('clampFactor').value = clampConfig.mobileFactor;
    for (const [id, val] of Object.entries({
        clampBaseOut: state.base + 'px',
        clampRatioOut: round(state.ratio, 4),
        clampMinWidthOut: clampConfig.minWidth + 'px',
        clampMaxWidthOut: clampConfig.maxWidth + 'px',
        clampFactorOut: Math.round(clampConfig.mobileFactor * 100) + '%',
        clampViewportOut: v + 'px'
      })) el(id).textContent = val;
    const {
      full,
      min
    } = fluidTypeBounds(step), actual = fluidTypePx(step, v), slope = (full - min) / (clampConfig.maxWidth - clampConfig.minWidth), offset = min - slope * clampConfig.minWidth;
    el('clampMinFont').textContent = round(min, 2) + 'px';
    el('clampComputed').textContent = round(actual, 2) + 'px';
    el('clampMaxFont').textContent = round(full, 2) + 'px';
    const css = `/* ${labels[step]}: ${state.base}px × ${state.ratio}^${step} */\n--text-${labels[step].toLowerCase()}: ${fluidTypeCss(step)};`;
    el('clampCss').textContent = css;
    el('clampMath').textContent = `Maximum = ${state.base} × ${state.ratio}^${step} = ${round(full,3)}px. Minimum = ${round(min,3)}px. Slope = (${round(full,3)} − ${round(min,3)}) / (${clampConfig.maxWidth} − ${clampConfig.minWidth}) = ${round(slope,6)} px/px. Preferred = ${round(slope*100,4)}vw + ${round(offset,3)}px (expressed with rem offset in CSS).`;
    el('clampExplanation').textContent = `At ${v}px, the browser clamps the fluid ${labels[step]} value to ${round(actual,2)}px, between ${round(min,2)}px and ${round(full,2)}px.`;
    const x = w => 48 + (w - 320) / 1280 * 572;
    const span = Math.max(full - min, 1);
    const y = px => 142 - (px - min) / span * 102;
    el('clampCurve').setAttribute('d', `M ${x(320)} ${y(fluidTypePx(step,320))} L ${x(clampConfig.minWidth)} ${y(min)} L ${x(clampConfig.maxWidth)} ${y(full)} L ${x(1600)} ${y(fluidTypePx(step,1600))}`);
    el('clampDot').setAttribute('cx', x(v));
    el('clampDot').setAttribute('cy', y(actual));
  }
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
  el('clampCopy').addEventListener('click', () => {
    const value = el('clampCss').textContent;
    if (navigator.clipboard?.writeText) navigator.clipboard.writeText(value).catch(() => {});
    else {
      const ta = document.createElement('textarea');
      ta.value = value;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand('copy');
      ta.remove();
    }
  });
  const original = renderType;
  renderType = function() {
    original();
    update();
  };
  update();
})();
