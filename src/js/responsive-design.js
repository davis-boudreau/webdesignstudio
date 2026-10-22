'use strict';
/* Shared, bounded responsive decisions. Media queries need literal lengths;
   CSS custom properties describe the container measurements instead. */
(() => {
  const defaults = () => ({ stack: 768, wide: 1024, maxWidth: 1152, gutter: 16, wideGutter: 32 });
  function normalize(value) {
    const result = defaults();
    if (!value || typeof value !== 'object' || Array.isArray(value)) return result;
    for (const [key,min,max] of [['stack',480,960],['wide',800,1600],['maxWidth',960,1600],['gutter',8,48],['wideGutter',8,64]])
      if (typeof value[key] === 'number' && Number.isFinite(value[key])) result[key] = Math.round(Math.min(max, Math.max(min,value[key])));
    result.wide = Math.max(result.stack + 160, result.wide);
    return result;
  }
  const settings = () => normalize(state.responsiveDesign);
  const rem = px => Number((px / 16).toFixed(4)) + 'rem';
  function tokens() {
    const r = settings();
    return `  --page-max-width: ${rem(r.maxWidth)};\n  --page-gutter: ${rem(r.gutter)};\n  --page-gutter-wide: ${rem(r.wideGutter)};`;
  }
  DSStudio.responsive = { defaults, normalize, settings, rem, tokens };
  DSStudio.register({
    id: 'responsive-design',
    title: 'Content-led breakpoints and responsive layout',
    init() {
      const controls = [...document.querySelectorAll('[data-responsive-field]')];
      for (const control of controls) control.addEventListener('input', () => {
        state.responsiveDesign = normalize({ ...state.responsiveDesign, [control.dataset.responsiveField]: Number(control.value) });
        apply();
      });
      function viewport() {
        const view = document.getElementById('previewPage').contentWindow;
        const width = view?.innerWidth || 0;
        const r = settings();
        const narrow = view?.matchMedia(`(max-width: ${rem(r.stack)})`).matches;
        const wide = view?.matchMedia(`(min-width: ${rem(r.wide)})`).matches;
        document.getElementById('responsiveLessonViewport').textContent = width ? `Current preview: ${width}px. ${narrow ? 'Narrow: main sections stack.' : 'Main sections can sit side by side.'} ${wide ? 'Wide side gutters apply.' : 'Standard side gutters apply.'} Cards can wrap earlier when their container is too narrow.` : 'Open the responsive preview to compare widths.';
      }
      function sync() {
        const r = settings();
        for (const control of controls) {
          const key = control.dataset.responsiveField;
          control.value = r[key];
          document.getElementById(control.id+'Out').textContent = `${r[key]}px / ${rem(r[key])}`;
        }
        document.getElementById('responsiveRecipe').textContent = `/* Start with the smallest useful layout. */
.container {
  width: 100%;
  max-width: var(--page-max-width); /* ${rem(r.maxWidth)} */
  margin-inline: auto;
  padding-inline: var(--page-gutter); /* ${rem(r.gutter)} */
}
@media (min-width: ${rem(r.wide)}) {
  .container { padding-inline: var(--page-gutter-wide); }
}
/* At and below ${r.stack}px, main sections use one column.
   Basic also stacks its header; Advanced uses its native mobile menu. */
@media (max-width: ${rem(r.stack)}) { /* stacking rules */ }
/* Media queries use literal lengths: var() cannot set a breakpoint.
   rem values use the browser's initial font size (normally 16px).
   Grid card wrapping follows card minimum + gap, not these cutoffs. */`;
        viewport();
      }
      const previousRender = renderCode;
      renderCode = function() { sync(); previousRender(); };
      const observer = new ResizeObserver(viewport);
      observer.observe(document.getElementById('previewFrame'));
      document.getElementById('previewPage').addEventListener('load', viewport);
      renderCode();
    }
  });
})();
