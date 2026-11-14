'use strict';
/* Ordered, authored export contributors. Imported projects supply data only.
   Raw fragments retain their own separators so assembly preserves the cascade
   and the exact existing CSS/HTML, including Basic's page formatting. */
(() => {
  const stages = Object.freeze(['foundation', 'components', 'states', 'planning', 'layout']);

  function create() {
    const fragments = new Map(), samples = new Map(), rendering = new Set();
    const ordered = () => [...fragments.values()].sort((a, b) =>
      stages.indexOf(a.stage) - stages.indexOf(b.stage) || a.order - b.order ||
      (a.id < b.id ? -1 : a.id > b.id ? 1 : 0));

    function guard(name, generate) {
      if (rendering.has(name)) throw new Error(`Recursive export generation: ${name}`);
      rendering.add(name);
      try { return generate(); }
      finally { rendering.delete(name); }
    }

    function text(generate, name) {
      const value = generate();
      if (typeof value !== 'string') throw new TypeError(`Export contributor "${name}" must return a string`);
      return value;
    }

    function registerCss({ id, stage, order = 0, generate }) {
      if (typeof id !== 'string' || !id || fragments.has(id) || !stages.includes(stage) ||
          !Number.isFinite(order) || typeof generate !== 'function') {
        throw new TypeError('registerCss requires a unique id, known stage, finite order and generator');
      }
      const entry = Object.freeze({ id, stage, order, generate });
      fragments.set(id, entry);
      return () => { if (fragments.get(id) === entry) fragments.delete(id); };
    }

    function registerSample(id, { css, html }) {
      if (!['fallback', 'basic', 'advanced'].includes(id) || samples.has(id) ||
          typeof css !== 'function' || typeof html !== 'function') {
        throw new TypeError('registerSample requires a unique known sample and CSS/HTML generators');
      }
      const entry = Object.freeze({ css, html });
      samples.set(id, entry);
      return () => { if (samples.get(id) === entry) samples.delete(id); };
    }

    function sample(mode) {
      if (!['basic', 'advanced'].includes(mode)) throw new TypeError('Unknown export sample');
      // Before initialization completes, retain the original startup fallback.
      return samples.get(mode) || samples.get('advanced') || samples.get('fallback');
    }

    function sharedCss() {
      return guard('shared-css', () => ordered().map(entry => text(entry.generate, entry.id)).join(''));
    }

    function css(mode) {
      const selected = sample(mode);
      return guard('css', () => sharedCss() + (selected ? text(selected.css, mode + ' CSS') : ''));
    }

    function html(mode) {
      const selected = sample(mode);
      if (!selected) throw new Error('No HTML export generator registered');
      return guard('html', () => text(selected.html, mode + ' HTML'));
    }

    return Object.freeze({ registerCss, registerSample, sharedCss, css, html, stages,
      describe: () => ({ css: ordered().map(({ id, stage, order }) => ({ id, stage, order })),
        samples: [...samples.keys()].sort() }) });
  }

  DSStudio.exports = Object.freeze({ ...create(), create });
})();
