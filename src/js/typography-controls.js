'use strict';
/* Named modular scales are separate from responsive heading shrinkage.
   State stores letter spacing in em; old advanced JSON uses hundredths. */
(() => {
  const get = id => document.getElementById(id);
  const selects = ['jScalePreset', 'clampScalePreset'];
  for (const id of selects) {
    get(id).replaceChildren(...TYPE_SCALES.map(([key, label, ratio]) => new Option(`${label} · ${ratio}`, key)), new Option('Custom ratio', 'custom'));
    get(id).addEventListener('change', event => {
      const preset = TYPE_SCALES.find(([key]) => key === event.target.value);
      if (!preset) return;
      state.ratio = preset[2];
      get('ratio').value = state.ratio;
      apply();
    });
  }
  function sync() {
    const preset = TYPE_SCALES.find(([, , ratio]) => Math.abs(ratio - state.ratio) < .00001);
    for (const id of selects) get(id).value = preset ? preset[0] : 'custom';
    for (const id of ['ratio', 'jRatio', 'clampRatio']) get(id).value = state.ratio;
    for (const id of ['ratioOut', 'jRatioOut', 'clampRatioOut']) get(id).textContent = round(state.ratio, 4);
    for (const [id, key] of [['headingTracking', 'headingTracking'], ['bodyTracking', 'bodyTracking'], ['jHeadingTracking', 'headingTracking'], ['jBodyTracking', 'bodyTracking'], ['typoHeadingTracking', 'headingTracking'], ['typoBodyTracking', 'bodyTracking']]) {
      get(id).value = state[key];
      get(id + 'Out').textContent = `${round(state[key],3)}em`;
    }
    get('advTracking').value = state.headingTracking * 100;
    get('advTrackingOut').textContent = `${round(state.headingTracking,3)}em`;
  }
  for (const [id, key] of [['typoHeadingTracking', 'headingTracking'], ['typoBodyTracking', 'bodyTracking']])
    get(id).addEventListener('input', event => {
      get(key).value = event.target.value;
      get(key).dispatchEvent(new Event('input', { bubbles: true }));
    });
  const originalApply = apply;
  apply = function() {
    adv.tracking = state.headingTracking * 100;
    originalApply();
    sync();
  };
  sync();
})();
