'use strict';
/* Native disclosures keep section navigation useful when panels are closed. */
(() => {
  const sections = [...document.querySelectorAll('#main > .studio-section')];
  function reveal(id, scroll = true) {
    const target = document.getElementById(id);
    if (!target) return;
    for (let parent = target; parent; parent = parent.parentElement)
      if (parent.tagName === 'DETAILS') parent.open = true;
    if (scroll) target.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
  }
  window.dssRevealSection = reveal;
  for (const section of sections) section.addEventListener('toggle', () => {
    if (section.open && section.id === 'studio-section-4') updateResponsivePreview(document.getElementById('previewFrame').dataset.width);
  });
  document.getElementById('expandSections').addEventListener('click', () => sections.forEach(section => section.open = true));
  document.getElementById('collapseSections').addEventListener('click', () => sections.forEach(section => section.open = false));
  document.addEventListener('click', event => {
    const anchor = event.target.closest('a[href]');
    if (!anchor || !anchor.hash || anchor.origin !== location.origin || anchor.pathname !== location.pathname) return;
    try { reveal(decodeURIComponent(anchor.hash.slice(1)), false); } catch { /* Ignore malformed fragments. */ }
  });
  function revealHash() {
    if (location.hash) {
      try { reveal(decodeURIComponent(location.hash.slice(1))); } catch { /* Ignore malformed fragments. */ }
    }
  }
  window.addEventListener('hashchange', revealHash);
  if (location.hash) requestAnimationFrame(revealHash);
})();
