'use strict';
/* Extension point for Design System Studio.
   Feature modules register themselves here instead of reaching into each other's globals.
   Load this file before any module; see docs/ARCHITECTURE.md. */
(() => {
  const modules = new Map();
  const listeners = new Map();

  const DSStudio = {
    version: '4.1.0',

    /** Register a feature module: { id, title, init(ctx), exportCss?(), exportTokens?() } */
    register(mod) {
      if (!mod || typeof mod.id !== 'string' || typeof mod.init !== 'function') {
        throw new TypeError('DSStudio.register: module needs a string "id" and an "init" function');
      }
      if (modules.has(mod.id)) throw new Error(`DSStudio.register: duplicate module id "${mod.id}"`);
      modules.set(mod.id, mod);
      return mod;
    },

    get modules() { return [...modules.values()]; },

    on(event, fn) {
      if (!listeners.has(event)) listeners.set(event, new Set());
      listeners.get(event).add(fn);
      return () => listeners.get(event).delete(fn);
    },

    emit(event, detail) {
      (listeners.get(event) || []).forEach(fn => {
        try { fn(detail); } catch (err) { console.error(`DSStudio listener for "${event}" failed`, err); }
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
        try { mod.init({ studio: DSStudio }); }
        catch (err) { console.error(`DSStudio module "${mod.id}" failed to init`, err); }
      });
      DSStudio.emit('ready');
    }
  };

  window.DSStudio = DSStudio;
  document.addEventListener('DOMContentLoaded', () => DSStudio.start());
})();
