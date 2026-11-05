'use strict';
/* Studio navigation only: preserve the current project, stage and preview. */
DSStudio.register({
  id:'section-navigation', title:'Return to the studio top from each section',
  init() {
    const home=document.getElementById('studio-home');
    const containers=document.querySelectorAll('.studio-section > .panel, [data-journey-pane], #studioInspector');
    for(const container of containers) {
      if(container.querySelector(':scope > .studio-home-return'))continue;
      const row=document.createElement('div');row.className='studio-home-return';
      const link=document.createElement('a');link.className='studio-home-link';link.href='#studio-home';
      link.append(document.createTextNode('Back to top '));
      const arrow=document.createElement('span');arrow.textContent='↑';arrow.setAttribute('aria-hidden','true');link.append(arrow);
      row.append(link);container.append(row);
    }
    document.addEventListener('click',event=>{
      const link=event.target.closest('a.studio-home-link');
      if(!link || event.defaultPrevented || event.button!==0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)return;
      // A sticky header is already in view at any scroll depth. Explicitly
      // return to the document start, then give keyboard users a visible target.
      event.preventDefault();
      window.scrollTo({top:0,left:0,behavior:'instant'});
      home.focus({preventScroll:true});
    });
  }
});
