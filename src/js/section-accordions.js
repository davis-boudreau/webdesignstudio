'use strict';
/* Native disclosures keep section navigation useful when panels are closed. */
(() => {
  const sections = [...document.querySelectorAll('#main > .studio-section')];
  const header = document.querySelector('.topbar');
  function syncScrollOffset() {
    const headerHeight = Math.ceil(header.getBoundingClientRect().height);
    document.documentElement.style.setProperty('--studio-header-height', `${headerHeight}px`);
    document.documentElement.style.setProperty('--studio-section-scroll-offset', `${headerHeight + 8}px`);
  }
  const offsetObserver = new ResizeObserver(syncScrollOffset);
  offsetObserver.observe(header);
  window.addEventListener('resize', syncScrollOffset);
  syncScrollOffset();
  function reveal(id, scroll = true) {
    const target = document.getElementById(id);
    if (!target) return;
    DSStudio.activateLesson?.(id);
    for (let parent = target; parent; parent = parent.parentElement)
      if (parent.tagName === 'DETAILS') parent.open = true;
    if (scroll) target.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start' });
  }
  window.dssRevealSection = reveal;
  for (const section of sections) section.addEventListener('toggle', () => {
    if (section.open && section.id === 'studio-section-4') updateResponsivePreview(document.getElementById('previewFrame').dataset.width);
  });
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
  // A frame can paint before deferred modules initialize. Restore the fragment
  // after lesson routing is ready so startup cannot collapse its destination.
  DSStudio.on('ready', () => { if (location.hash) revealHash(); });
})();
