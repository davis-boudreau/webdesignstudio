   /* Keep a second, always-readable CSS panel in sync with the existing V2 engine. */
(() => {
 const $ = id => document.getElementById(id);
 const live = $('dockCss');
 function refreshDock(){ if(typeof cssExport==='function') live.textContent=cssExport(); }
 // The existing studio calls renderCode() whenever any foundation value changes.
 const originalRenderCode=renderCode;
 renderCode=function(){ originalRenderCode(); refreshDock(); };
 $('dockCopy').addEventListener('click',async()=>{try{await navigator.clipboard.writeText(cssExport());$('dockCopy').textContent='Copied!';}catch{ $('dockCopy').textContent='Select code to copy'; }setTimeout(()=>$('dockCopy').textContent='Copy CSS',1800)});
 $('dockDownload').addEventListener('click',()=>download('tokens.css',cssExport(),'text/css'));
 /* FIX: $() is getElementById, so $('.studio-code-dock') returned null and the Collapse button crashed. */
 $('dockToggle').addEventListener('click',()=>{const collapsed=document.querySelector('.studio-code-dock').classList.toggle('is-collapsed');$('dockToggle').textContent=collapsed?'Expand code':'Collapse code';$('dockToggle').setAttribute('aria-expanded',String(!collapsed));});
 refreshDock();
})();
  
