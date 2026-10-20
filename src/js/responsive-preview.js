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
      let queued = false, renderedDocument = null, previousHtml = '', previousCss = '';

      function wire(doc) {
        if (wired.has(doc)) return;
        wired.add(doc);
        // Fragment URLs in srcdoc otherwise resolve against the studio's URL.
        doc.addEventListener('click', event => {
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
          const note = doc.getElementById('contact-note');
          if (note) note.textContent = 'This is a sample form. No enquiry has been sent.';
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
          details: [...doc.querySelectorAll('details')].map(detail => detail.open)
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
        doc.querySelectorAll('details').forEach((detail, index) => {
          if (index < saved.details.length) detail.open = saved.details[index];
        });
        const active = doc.getElementById(saved.activeId) || controls[saved.activeControl];
        active?.focus({ preventScroll: true });
        doc.defaultView.scrollTo(saved.x, saved.y);
      }

      function render() {
        queued = false;
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
          const saved = capture(doc);
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
          restore(doc, saved);
        } else if (css !== previousCss) {
          doc.getElementById('dssPreviewStyles').textContent = css;
        }
        previousHtml = html;
        previousCss = css;
        DSStudio.fonts.syncPreview(doc);
        syncResponsivePreview();
      }

      function schedule() {
        if (queued) return;
        queued = true;
        queueMicrotask(render);
      }
      const originalRenderCode = renderCode;
      renderCode = function() {
        originalRenderCode();
        schedule();
      };
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
