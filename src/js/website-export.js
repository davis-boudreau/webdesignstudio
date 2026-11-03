'use strict';
/* Explicit standalone file actions share the preview's existing generators. */
DSStudio.register({
  id: 'website-export',
  title: 'Responsive static website downloads',
  init() {
    const exports = {
      html: { name: 'index.html', type: 'text/html', content: () => htmlExport() },
      css: { name: 'tokens.css', type: 'text/css', content: () => cssExport() }
    };
    for (const button of document.querySelectorAll('[data-website-download]')) {
      button.addEventListener('click', () => {
        const file = exports[button.dataset.websiteDownload];
        if (!file) return;
        download(file.name, file.content(), file.type);
        const message = `${file.name} download requested. Save index.html and tokens.css in the same folder, then open index.html.`;
        announce(message);
      });
    }
  }
});
