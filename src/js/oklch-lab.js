'use strict';
/* OKLCH laboratory: a standalone, dependency-free interactive visualization.
   Hue is angular, chroma is radial, and lightness is an independent axis. */
(() => {
  const get = id => document.getElementById(id);
  const canvas = get('oklchWheel');
  if (!canvas || typeof rgbToOklch !== 'function') return;
  const ctx = canvas.getContext('2d');
  const N = canvas.width, center = N / 2, radius = center - 9;
  let L = .55, C = .1, H = 230;
  const maxC = .4;
  const wheelCache = new Map();
  function inGamut(l,c,h) {
    return oklchRgb(l,c,h).every(v => Number.isFinite(v) && v >= 0 && v <= 1);
  }
  function renderWheel() {
    const key = L.toFixed(2);
    if (wheelCache.has(key)) {
      ctx.putImageData(wheelCache.get(key), 0, 0);
    } else {
      const pixels = ctx.createImageData(N, N);
      for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) {
        const dx = x + .5 - center, dy = y + .5 - center;
        const r = Math.hypot(dx, dy) / radius;
        const i = (y * N + x) * 4;
        if (r > 1) continue;
        const hue = (Math.atan2(dy, dx) + Math.PI * 2) % (Math.PI * 2);
        const chroma = r * maxC;
        const rgb = oklchRgb(L, chroma, hue);
        const safe = inGamut(L, chroma, hue) ? rgb : hexRgb(oklchHex(L, chroma, hue)).map(v => v / 255);
        for (let k = 0; k < 3; k++) pixels.data[i + k] = Math.round(Math.max(0, Math.min(1, safe[k])) * 255);
        pixels.data[i + 3] = 255;
      }
      ctx.putImageData(pixels, 0, 0);
      if (wheelCache.size > 7) wheelCache.clear();
      wheelCache.set(key, pixels);
    }
    const x = center + Math.min(C / maxC, 1) * radius * Math.cos(H * Math.PI / 180);
    const y = center + Math.min(C / maxC, 1) * radius * Math.sin(H * Math.PI / 180);
    get('oklchWheelCross').style.left = (x / N * 100) + '%';
    get('oklchWheelCross').style.top = (y / N * 100) + '%';
  }
  function update() {
    get('oklchLight').value = Math.round(L * 100);
    get('oklchChroma').value = C.toFixed(3);
    get('oklchHue').value = Math.round(H) % 360;
    get('oklchLightOut').textContent = Math.round(L * 100) + '%';
    get('oklchChromaOut').textContent = C.toFixed(3);
    get('oklchHueOut').textContent = Math.round(H) + '°';
    const hex = oklchHex(L, C, H * Math.PI / 180);
    get('oklchHex').textContent = hex;
    get('oklchCoords').textContent = `oklch(${(L * 100).toFixed(1)}% ${C.toFixed(3)} ${Math.round(H)})`;
    get('oklchGamut').textContent = inGamut(L,C,H*Math.PI/180) ? 'Within sRGB gamut' : 'Outside sRGB gamut · chroma reduced for HEX preview';
    get('oklchSwatch').style.background = hex;
    renderWheel();
  }
  function loadRole() {
    const role = get('oklchRole').value;
    [L,C,H] = rgbToOklch(state[role]);
    H = (H * 180 / Math.PI + 360) % 360;
    update();
  }
  get('oklchRole').addEventListener('change', loadRole);
  get('oklchLight').addEventListener('input', e => { L = +e.target.value / 100; update(); });
  get('oklchChroma').addEventListener('input', e => { C = +e.target.value; update(); });
  get('oklchHue').addEventListener('input', e => { H = +e.target.value; update(); });
  let dragging = false;
  function point(e) {
    const r = canvas.getBoundingClientRect();
    const dx = (e.clientX - r.left) / r.width * N - center;
    const dy = (e.clientY - r.top) / r.height * N - center;
    H = (Math.atan2(dy,dx) * 180 / Math.PI + 360) % 360;
    C = Math.min(1, Math.hypot(dx,dy) / radius) * maxC;
    update();
  }
  canvas.addEventListener('pointerdown', e => { dragging = true; canvas.setPointerCapture(e.pointerId); point(e); });
  canvas.addEventListener('pointermove', e => { if (dragging) point(e); });
  canvas.addEventListener('pointerup', () => { dragging = false; });
  canvas.addEventListener('pointercancel', () => { dragging = false; });
  get('oklchReset').addEventListener('click', loadRole);
  get('oklchApply').addEventListener('click', () => {
    const role = get('oklchRole').value;
    state[role] = oklchHex(L,C,H*Math.PI/180).toLowerCase();
    syncControls();
    apply();
    // The guided wizard maintains its own controls; synchronize them too.
    const guided = get('j' + role[0].toUpperCase() + role.slice(1));
    if (guided) { guided.value = state[role]; const out = get(guided.id + 'Out'); if (out) out.textContent = state[role].toUpperCase(); }
    const status = get('liveStatus');
    if (status) status.textContent = `Updated ${role} to ${state[role].toUpperCase()}`;
  });
  loadRole();
})();
