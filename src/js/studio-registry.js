'use strict';
/* Extension point for Web Design System Studio.
Feature modules register themselves here instead of reaching into each other's globals.
Load this file before any module; see docs/ARCHITECTURE.md. */
(() => {
  const modules = new Map();
  const listeners = new Map();
  // Stable control indices keep existing routes compatible; positions set the
  // learner's sequence independently of those internal identifiers.
  const stageOrder = Object.freeze([0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 3]);

  const DSStudio = {
    version: '4.1.0',
    stageOrder,
    get orderedStages() { return stageOrder.map(index => this.stages[index]); },

    // One identity for builder controls, lessons and output connections. These
    // fixed IDs are UI metadata; imported projects cannot supply routes or code.
    stages: [
      ['brief', 'Brief', 'process-brief', 'Plan', '', 'Record the purpose and audience. Check that the brief describes one useful visitor task.'],
      ['architecture', 'Architecture', 'process-ia', 'Plan', '', 'Use the brief to organize the full information structure. Choose which entries appear in the sitemap, then test labels and compare the visitor sitemap with the preview footer.'],
      ['wireframe', 'Wireframe', 'process-wireframe', 'Plan', '', 'Choose a layout and compare the wireframe below. This plans hierarchy; it does not rebuild the sample page.'],
      ['prototype', 'Prototype', 'process-prototype', 'Review and deliver', '', 'Review the finished live prototype using your brief and task. Test both samples, themes and viewport sizes, record observations, then export the HTML and CSS.'],
      ['palette', 'Palette', 'brandPalette', 'Foundations', '--primary:', 'Name a brand token, assign a Main Palette role and compare its generated shade steps. Follow the light and dark semantic values into the page and CSS.'],
      ['typography', 'Typography', 'studio-section-2', 'Foundations', '--font-size-base:', 'Change the base text size. Compare headings and body text, then inspect the generated type scale.'],
      ['semantic', 'Semantic colours', 'studio-section-1', 'Foundations', '--surface:', 'Choose a purpose-based colour. Compare the affected text or surface in the current theme.'],
      ['buttons', 'Buttons', 'buttonDesignLab', 'Apply', '--button-primary-bg:', 'Change the primary button background. Compare the page action, check its text contrast and follow the token into CSS.'],
      ['spacing', 'Spacing and surfaces', 'studio-section-3', 'Apply', '--space-unit:', 'Change the spacing unit. Compare section padding and related spacing tokens, then explain why they change together.'],
      ['responsive', 'Responsive layout', 'responsiveDesign', 'Apply', '--grid-card-min:', 'Compare 390 px and Fluid. Change the narrow cutoff and find the rule that stacks the layout. Preview widths test rules; they do not save breakpoints.'],
      ['accessibility', 'Accessibility', 'studio-section-5', 'Review and deliver', '--focus-width:', 'Review the contrast results, then use Tab on real controls. Check visible focus and meaning without colour.'],
      ['deliver', 'Deliver', 'studio-section-6', 'Review and deliver', '', 'Download index.html and tokens.css together and reopen the page. Save project JSON separately so you can resume editing in the studio.']
    ].map(([id, label, lesson, phase, find, task], index) => Object.freeze({ id, label, lesson, phase, find, task, index, position: stageOrder.indexOf(index) })),

    /** Register a feature module: { id, title, init(ctx), exportCss?(), exportTokens?() } */
    register(mod) {
      if (!mod || typeof mod.id !== 'string' || typeof mod.init !== 'function') {
        throw new TypeError('DSStudio.register: module needs a string "id" and an "init" function');
      }
      if (modules.has(mod.id)) throw new Error(`DSStudio.register: duplicate module id "${mod.id}"`);
      modules.set(mod.id, mod);
      return mod;
    },

    get modules() {
      return [...modules.values()];
    },

    on(event, fn) {
      if (!listeners.has(event)) listeners.set(event, new Set());
      listeners.get(event).add(fn);
      return () => listeners.get(event).delete(fn);
    },

    emit(event, detail) {
      (listeners.get(event) || []).forEach(fn => {
        try {
          fn(detail);
        } catch (err) {
          console.error(`DSStudio listener for "${event}" failed`, err);
        }
      });
    },

    /** Collect CSS fragments contributed by registered modules (used by export). */
    collectCss() {
      return [...modules.values()]
        .map(m => (typeof m.exportCss === 'function' ? m.exportCss() : ''))
        .filter(Boolean)
        .join('\n\n');
    },

    start() {
      modules.forEach(mod => {
        try {
          mod.init({
            studio: DSStudio
          });
        } catch (err) {
          console.error(`DSStudio module "${mod.id}" failed to init`, err);
        }
      });
      DSStudio.emit('ready');
    }
  };

  window.DSStudio = DSStudio;
  document.addEventListener('DOMContentLoaded', () => DSStudio.start());
})();
