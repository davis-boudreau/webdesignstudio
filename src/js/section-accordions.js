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
  // Only a deliberate summary activation moves the view. Programmatic opens
  // during routing, imports and preview refreshes must not steal focus or scroll.
  let activation=0;
  document.addEventListener('click', event => {
    const summary=event.target.closest('summary'),details=summary?.parentElement;
    if(!details || details.tagName!=='DETAILS' || details.open || event.button!==0 || event.ctrlKey || event.metaKey || event.altKey || event.shiftKey)return;
    const revision=++activation;
    queueMicrotask(()=>{
      if(event.defaultPrevented || !details.open)return;
      const focused=document.activeElement;
      if(focused!==document.body && focused!==summary && !summary.contains(focused))return;
      function align(){
        if(revision!==activation || !details.open || !summary.isConnected || document.activeElement!==focused)return;
        for(let parent=details.parentElement;parent && parent!==document.body;parent=parent.parentElement){
          if(!/(auto|scroll)/.test(getComputedStyle(parent).overflowY) || parent.scrollHeight<=parent.clientHeight)continue;
          parent.scrollTop+=summary.getBoundingClientRect().top-parent.getBoundingClientRect().top-8;
        }
        const top=header.getBoundingClientRect().bottom+8;
        window.scrollBy({top:summary.getBoundingClientRect().top-top,behavior:'instant'});
      }
      align();requestAnimationFrame(()=>requestAnimationFrame(align));
    });
  },true);
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
