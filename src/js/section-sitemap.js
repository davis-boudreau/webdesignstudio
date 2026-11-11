'use strict';
/* Derive navigation from authored sample labels, never imported HTML or URLs. */
(() => {
  let collecting=false;
  const cache=new Map();
  const sample=()=>state.sampleMode==='basic'?'basic':'advanced';
  function source(plan=DSStudio.process.currentPlan()) {
    const mode=sample(),choice=plan.sitemapSource[mode];
    if(choice!=='auto')return choice;
    // Existing custom outlines keep their behavior until the user switches source.
    return plan.pages!==DSStudio.process.samplePages(mode) || plan.iaEntries[mode].length || Object.keys(plan.pageLinks[mode]).length?'custom':'sections';
  }
  function collect(html,mode) {
    const doc=new DOMParser().parseFromString(html,'text/html');
    const candidates=new Map();
    for(const [,id] of DSStudio.process.inventory(mode)) {
      const element=doc.getElementById(id);
      if(element?.closest('main'))candidates.set(element,id);
    }
    const result=[],byElement=new Map();
    const compact=element=>element?.textContent.replace(/\s+/g,' ').trim()||'';
    for(const element of doc.querySelectorAll('main [id]')) {
      const id=candidates.get(element);if(!id)continue;
      // A container cannot borrow an eyebrow/heading from a nested destination.
      const owns=label=>{
        for(let parent=label.parentElement;parent && parent!==element;parent=parent.parentElement)
          if(candidates.has(parent) || parent.matches('section,article,aside,form,fieldset'))return false;
        return true;
      };
      const eyebrow=[...element.querySelectorAll('.eyebrow,.sample-eyebrow')].find(owns);
      const heading=element.matches('h1,h2,h3,h4,h5,h6')?element:[...element.querySelectorAll('h1,h2,h3,h4,h5,h6,legend')].find(owns);
      const label=compact(eyebrow||heading);if(!label)continue;
      let ancestor=element.parentElement;
      while(ancestor && !byElement.has(ancestor))ancestor=ancestor.parentElement;
      const parent=byElement.get(ancestor),node={id,label,parentId:parent?.id||null,depth:(parent?.depth||0)+1,labelSource:eyebrow?'eyebrow':'heading'};
      result.push(node);byElement.set(element,node);
    }
    return result;
  }
  function nodes() {
    if(collecting)return [];
    const mode=sample(),factory=DSStudio.samples?.[mode+'Html'];if(!factory)return [];
    const {contentPlan,...planning}=state.designProcess||{};
    const signature=JSON.stringify({...state,designProcess:planning,advanced:typeof adv==='object'?adv:null});
    if(cache.get(mode)?.signature===signature)return cache.get(mode).nodes;
    collecting=true;
    try {
      const rows=collect(factory(),mode);cache.set(mode,{signature,nodes:rows});return rows;
    } finally {collecting=false;}
  }
  function markup({previewLinks=false,topLevelLinksOnly=false}={}) {
    const rows=nodes(),excluded=new Set(DSStudio.process.currentPlan().sitemapExcluded[sample()]);
    const branch=(parentId=null)=>rows.filter(node=>node.parentId===parentId && !excluded.has(node.id)).map(node=>{
      const children=topLevelLinksOnly?'':branch(node.id);
      return `<li><a href="#${previewLinks?'previewShell':node.id}"${previewLinks?` data-sitemap-target="${node.id}"`:''}>${escapeHtml(node.label)}</a>${children?`<ul>${children}</ul>`:''}</li>`;
    }).join('');
    const html=branch();return html?`<ul class="sitemap-list sitemap-list--sections">${html}</ul>`:'<p>No sections selected. Choose sections in Sitemap configuration.</p>';
  }
  function initControls(destination,raw) {
    const root=document.createElement('section');root.id='section-sitemap-editor';root.className='sitemap-editor';
    root.innerHTML=`<h3>Sitemap configuration</h3><p class="help">Link directly to sections using their visible eyebrow text, or their existing heading when no eyebrow is present. Nested entries follow the page containers. The Website content structure above stays complete.</p>
      <label for="sitemap-source">Sitemap labels and hierarchy</label><select id="sitemap-source"><option value="sections">Page eyebrows and headings</option><option value="custom">Custom destination plan</option></select>
      <div id="section-sitemap-settings"><p class="help">Choose sections to include. Excluding a parent hides its branch; child choices are retained. Sections without their own label are reached through their containing section.</p><div id="section-sitemap-choices" class="sitemap-choices" role="region" tabindex="0" aria-label="Page section sitemap choices"></div><button id="section-sitemap-restore" type="button" class="ghost">Include all sections</button></div>
      <button id="section-sitemap-undo" type="button" class="ghost" disabled>Undo sitemap configuration</button><p id="section-sitemap-status" class="help" role="status"></p>`;
    destination.before(root);
    const get=id=>root.querySelector('#'+id),rows=new Map();let previous=null,last='',ownChange=false;
    function sync() {
      const plan=DSStudio.process.currentPlan(),mode=sample(),current=source(plan),next=JSON.stringify([mode,plan.sitemapSource,plan.sitemapExcluded]);
      if(last!==next && !ownChange){previous=null;get('section-sitemap-undo').disabled=true;}last=next;
      get('sitemap-source').value=current;destination.hidden=current!=='custom';raw.hidden=current!=='custom';get('section-sitemap-settings').hidden=current!=='sections';
      const excluded=new Set(plan.sitemapExcluded[mode]),effective=new Map(),keep=new Set(),box=get('section-sitemap-choices');
      nodes().forEach((node,index)=>{
        keep.add(node.id);let row=rows.get(node.id);
        if(!row){const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');input.type='checkbox';input.dataset.sectionId=node.id;label.append(input,text);row={label,input,text};rows.set(node.id,row);}
        const inherited=!node.parentId || effective.get(node.parentId);effective.set(node.id,inherited && !excluded.has(node.id));
        row.input.checked=!excluded.has(node.id);row.input.disabled=!inherited;
        row.input.setAttribute('aria-label','Include '+node.label+' in sitemap'+(!inherited?', ancestor excluded':''));
        row.label.classList.toggle('is-child',node.depth===2);row.label.classList.toggle('is-grandchild',node.depth>2);
        row.text.textContent=node.label+(!inherited?' (ancestor excluded)':'');
        if(box.children[index]!==row.label)box.insertBefore(row.label,box.children[index]||null);
      });
      for(const [id,row]of rows)if(!keep.has(id)){row.label.remove();rows.delete(id);}
    }
    function commit(change,message) {
      const plan=DSStudio.process.normalize(state.designProcess);previous={sitemapSource:plan.sitemapSource,sitemapExcluded:plan.sitemapExcluded};state.designProcess=DSStudio.process.normalize({...plan,...change});
      ownChange=true;try{apply();}finally{ownChange=false;}
      get('section-sitemap-undo').disabled=false;get('section-sitemap-status').textContent=message;
    }
    get('sitemap-source').addEventListener('change',()=>commit({sitemapSource:{...DSStudio.process.currentPlan().sitemapSource,[sample()]:get('sitemap-source').value}},'Sitemap source updated. Your content and saved custom plan are retained.'));
    get('section-sitemap-choices').addEventListener('change',event=>{
      const input=event.target.closest('input[data-section-id]');if(!input || !nodes().some(node=>node.id===input.dataset.sectionId))return;
      const plan=DSStudio.process.currentPlan(),excluded=new Set(plan.sitemapExcluded[sample()]);
      if(input.checked)excluded.delete(input.dataset.sectionId);else excluded.add(input.dataset.sectionId);
      commit({sitemapExcluded:{...plan.sitemapExcluded,[sample()]:[...excluded]}},'Sitemap sections updated. Website content is retained.');
    });
    get('section-sitemap-restore').addEventListener('click',()=>commit({sitemapExcluded:{...DSStudio.process.currentPlan().sitemapExcluded,[sample()]:[]}},'All labelled sections included in this sample. Undo is available.'));
    get('section-sitemap-undo').addEventListener('click',()=>{if(!previous)return;state.designProcess=DSStudio.process.normalize({...state.designProcess,...previous});previous=null;ownChange=true;try{apply();}finally{ownChange=false;}get('section-sitemap-undo').disabled=true;get('section-sitemap-status').textContent='Last sitemap configuration undone.';});
    for(const name of ['dss:reset','dss:imported'])document.addEventListener(name,()=>{previous=null;last='';get('section-sitemap-undo').disabled=true;get('section-sitemap-status').textContent='';sync();});
    return sync;
  }
  DSStudio.sectionSitemap={source,collect,nodes,markup,initControls};
})();
