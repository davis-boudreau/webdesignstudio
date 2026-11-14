'use strict';
/* Render the same HTML/CSS as the inspector inside a real, isolated viewport. */
(() => {
  DSStudio.register({
    id: 'responsive-preview',
    title: 'Responsive sample preview',
    init() {
      const frame = document.getElementById('previewPage');
      const theme = document.getElementById('previewTheme');
      const wired = new WeakSet();
      let renderedDocument = null, previousHtml = '', previousCss = '', previousMode = '';

      // Imported/loaded/reset projects own a fresh browsing session, even when
      // their output is identical or intermediate sample changes are coalesced.
      DSStudio.on('project:install', () => {
        previousHtml = previousCss = previousMode = '';
      });

      function wire(doc) {
        if (wired.has(doc)) return;
        wired.add(doc);
        doc.addEventListener('keydown', event => {
          if (event.key === 'Escape' && DSStudio.learning?.picking) DSStudio.emit('preview:cancel');
        });
        // Fragment URLs in srcdoc otherwise resolve against the studio's URL.
        doc.addEventListener('click', event => {
          if (state.sampleMode === 'basic' && DSStudio.learning?.picking) {
            const action = event.target.closest('.ds-button--primary');
            const example = action || event.target.closest('#basic-layout, #basic-usability, #cards-grid, #contact-form, #home, #features, #lists, #signup, #top, #footer');
            if (example) {
              event.preventDefault();
              DSStudio.emit('preview:example', { id: example.id, example: action ? 'action' : null });
              return;
            }
          }
          const anchor = event.target.closest('a[href]');
          const href = anchor?.getAttribute('href');
          if (!href?.startsWith('#')) return;
          event.preventDefault();
          let target;
          try { target = doc.getElementById(decodeURIComponent(href.slice(1))); } catch { return; }
          if (!target) return;
          for (let ancestor = target; ancestor; ancestor = ancestor.parentElement)
            if (ancestor.tagName === 'DETAILS') ancestor.open = true;
          const view = doc.defaultView;
          view.scrollTo({ top: view.scrollY + target.getBoundingClientRect().top - 24, behavior: 'instant' });
          target.tabIndex = -1;
          target.focus({ preventScroll: true });
        });
        doc.addEventListener('submit', event => {
          event.preventDefault();
          const note = doc.getElementById('contact-note') || doc.getElementById('basic-signup-note');
          if (note) note.textContent = state.sampleMode === 'basic' ? 'Validation passed. No message has been sent.' : 'This is a sample form. No enquiry has been sent.';
        });
      }

      function detailsByKey(doc) {
        const counts = new Map();
        return [...doc.querySelectorAll('details')].map(detail => {
          const label = detail.id ? 'id:'+detail.id : 'summary:'+detail.querySelector('summary')?.textContent;
          const occurrence = counts.get(label) || 0;
          counts.set(label, occurrence+1);
          return [label+':'+occurrence, detail];
        });
      }
      function capture(doc) {
        const controls = [...doc.querySelectorAll('input, select, textarea')];
        return {
          x: doc.defaultView.scrollX, y: doc.defaultView.scrollY,
          activeId: doc.activeElement?.id,
          activeControl: controls.indexOf(doc.activeElement),
          controls: controls.map(control => ({ id: control.id, name: control.name,
            type: control.type, value: control.value, checked: control.checked })),
          details: detailsByKey(doc).map(([key,detail]) => [key,detail.open])
        };
      }

      function restore(doc, saved) {
        const controls = [...doc.querySelectorAll('input, select, textarea')];
        controls.forEach((control, index) => {
          const old = saved.controls[index];
          if (!old || old.id !== control.id || old.name !== control.name || old.type !== control.type || control.type === 'file') return;
          control.value = old.value;
          if (['checkbox', 'radio'].includes(control.type)) control.checked = old.checked;
        });
        const disclosures = new Map(saved.details);
        for (const [key,detail] of detailsByKey(doc))
          if (disclosures.has(key)) detail.open = disclosures.get(key);
        const active = doc.getElementById(saved.activeId) || controls[saved.activeControl];
        active?.focus({ preventScroll: true });
        doc.defaultView.scrollTo(saved.x, saved.y);
      }

      function render() {
        theme.value = state.theme;
        frame.title = `Live generated home page — ${state.theme} theme`;
        const doc = frame.contentDocument;
        if (!doc?.head || !doc.body) return;
        wire(doc);
        if (doc !== renderedDocument) {
          renderedDocument = doc;
          previousHtml = previousCss = '';
        }
        const html = htmlExport(), css = cssExport() + DSStudio.fonts.previewCss();
        if (html !== previousHtml) {
          const saved = previousMode === state.sampleMode ? capture(doc) : null;
          const parsed = new DOMParser().parseFromString(html, 'text/html');
          parsed.querySelector('link[rel="stylesheet"][href="tokens.css"]')?.remove();
          // Font requests are managed independently so fallback comparison stays preview-only.
          parsed.querySelectorAll('link[href^="https://fonts.googleapis.com"], link[href^="https://fonts.gstatic.com"]').forEach(link => link.remove());
          const fontLinks = [...doc.head.querySelectorAll('link[data-dss-font]')];
          const style = parsed.createElement('style');
          style.id = 'dssPreviewStyles';
          // Insert CSS as a text node, without reparsing it as HTML.
          style.textContent = css;
          parsed.head.append(style);
          for (const element of ['documentElement', 'body']) {
            for (const attr of [...doc[element].attributes]) doc[element].removeAttribute(attr.name);
            for (const attr of parsed[element].attributes) doc[element].setAttribute(attr.name, attr.value);
          }
          doc.head.replaceChildren(...[...parsed.head.childNodes].map(node => doc.importNode(node, true)), ...fontLinks);
          doc.body.replaceChildren(...[...parsed.body.childNodes].map(node => doc.importNode(node, true)));
          if (saved) restore(doc, saved);
          else doc.defaultView.scrollTo(0, 0);
        } else if (css !== previousCss) {
          doc.getElementById('dssPreviewStyles').textContent = css;
        }
        previousHtml = html;
        previousCss = css;
        previousMode = state.sampleMode;
        DSStudio.fonts.syncPreview(doc);
        syncResponsivePreview();
      }

      const { schedule } = DSStudio.views.subscribe({
        id: 'responsive-preview', phase: 'preview', events: ['output:updated'], run: render
      });
      theme.addEventListener('change', event => {
        state.theme = event.target.value;
        apply();
      });
      frame.addEventListener('load', schedule);
      const observer = new ResizeObserver(syncResponsivePreview);
      observer.observe(document.getElementById('previewFrame'));
      schedule();
    }
  });
})();
