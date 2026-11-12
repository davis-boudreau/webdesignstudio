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
  function collect(html,mode,documentSource=null) {
    const doc=documentSource||new DOMParser().parseFromString(html,'text/html');
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
    const {contentPlan,wireframes,...planning}=state.designProcess||{};
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
  // Shared native outline for page-derived and custom destinations. Reconcile
  // existing rows so inclusion changes preserve focus and expanded branches.
  function createOutline(box,search,onSelect) {
    const list=document.createElement('ul'),status=document.createElement('p'),entries=new Map();status.className='help';status.setAttribute('role','status');box.classList.add('sitemap-outline');box.append(list,status);
    let current=[],selection=null,searching=false,expandedBeforeSearch=new Set();
    function filter() {
      const query=search.value.trim().toLowerCase();
      if(query && !searching)expandedBeforeSearch=new Set([...entries].filter(([,row])=>row.details.open).map(([id])=>id));
      const byId=new Map(current.map(node=>[node.id,node])),visible=new Set();
      for(const node of current)if(!query || node.label.toLowerCase().includes(query)) {
        let item=node;while(item && !visible.has(item.id)){visible.add(item.id);item=byId.get(item.parentId);}
      }
      for(const [id,row]of entries){row.li.hidden=!visible.has(id);if(query)row.details.open=visible.has(id);else if(searching)row.details.open=expandedBeforeSearch.has(id);}
      searching=!!query;
      status.textContent=query?`${current.filter(node=>node.label.toLowerCase().includes(query)).length} matching destinations; containing branches shown.`:`${current.length} destinations. Expand branches to see their children.`;
      box.setAttribute('aria-label',query?`Sitemap outline: ${current.filter(node=>node.label.toLowerCase().includes(query)).length} matches, with containing destinations`:'Expandable sitemap destinations');
    }
    function updateSelection(id) {selection=id;for(const [key,row]of entries)row.button.setAttribute('aria-pressed',String(key===id));}
    function sync(nodes,rowFor,id) {
      current=nodes;const keep=new Set(nodes.map(node=>node.id)),parents=new Set(nodes.map(node=>node.parentId));
      for(const [key,row]of entries)if(!keep.has(key)){row.li.remove();entries.delete(key);}
      for(const node of nodes) {
        let row=entries.get(node.id);
        if(!row){
          const li=document.createElement('li'),details=document.createElement('details'),summary=document.createElement('summary'),leaf=document.createElement('div'),children=document.createElement('ul'),button=document.createElement('button');
          button.type='button';button.className='sitemap-select';button.dataset.sitemapNodeId=node.id;
          button.addEventListener('click',event=>{event.preventDefault();onSelect(node.id);});
          details.append(summary,children);leaf.className='sitemap-outline-row';row={li,details,summary,leaf,children,button};entries.set(node.id,row);
        }
        row.button.textContent=node.label;const line=parents.has(node.id)?row.summary:row.leaf;
        if(row.li.firstChild!==(parents.has(node.id)?row.details:row.leaf))row.li.replaceChildren(parents.has(node.id)?row.details:row.leaf);
        if(row.button.parentElement!==line)line.prepend(row.button);
        const inclusion=rowFor(node.id);inclusion.text.textContent='Include';
        if(inclusion.label.parentElement!==line)line.append(inclusion.label);
      }
      const positions=new Map();
      for(const node of nodes){const parent=entries.get(node.parentId)?.children||list,index=positions.get(parent)||0;const li=entries.get(node.id).li;if(parent.children[index]!==li)parent.insertBefore(li,parent.children[index]||null);positions.set(parent,index+1);}
      updateSelection(id);filter();
    }
    function focus(id=selection) {
      const row=entries.get(id);if(!row){box.focus();return;}
      for(let parent=row.button.parentElement;parent && parent!==box;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;
      row.button.focus();row.button.scrollIntoView({block:'nearest'});
    }
    search.addEventListener('input',filter);
    return {sync,updateSelection,focus,reset(){search.value='';searching=false;for(const row of entries.values())row.details.open=false;filter();}};
  }
  function initControls(destination,raw) {
    const root=document.createElement('section');root.id='section-sitemap-editor';root.className='sitemap-editor';
    root.innerHTML=`<div id="sitemap-source-field" class="field"><label for="sitemap-source">Sitemap labels and hierarchy</label><select id="sitemap-source"><option value="sections">Page eyebrows and headings</option><option value="custom">Custom destination plan</option></select></div><p class="help">Choose which destinations visitors can reach from the sitemap. Excluding a destination leaves its website content intact.</p><p id="sitemap-source-summary" class="help"></p>
      <div id="section-sitemap-settings" class="sitemap-workspace"><section class="sitemap-browser" aria-label="Find sitemap destinations"><label for="section-sitemap-search">Find destination</label><input id="section-sitemap-search" type="search" placeholder="Search page labels"><p class="help">Expand a branch or select a destination. Include controls update the visitor map immediately.</p><div id="section-sitemap-choices" class="sitemap-choices" role="region" tabindex="0" aria-label="Page section sitemap choices"></div><button id="section-sitemap-restore" type="button" class="ghost">Include all sections</button></section>
      <section class="sitemap-properties" aria-labelledby="section-sitemap-heading"><h4 id="section-sitemap-heading" tabindex="-1">Selected destination</h4><strong id="section-sitemap-name"></strong><p id="section-sitemap-path" class="help"></p><label class="sitemap-selected-inclusion"><input id="section-sitemap-included" type="checkbox"> Include in visitor sitemap</label><p id="section-sitemap-inclusion-help" class="help"></p><p class="help">Labels and nesting follow the page. Choose Custom destination plan above to edit your own labels and hierarchy.</p><a id="section-sitemap-preview-link" href="#previewShell">Preview this destination</a></section></div>
      <button id="section-sitemap-undo" type="button" class="ghost" disabled>Undo sitemap configuration</button><p id="section-sitemap-status" class="help" role="status"></p><div id="architecture-sitemap-preview"></div>
      <details id="architecture-sitemap-advanced" class="architecture-options"><summary>Advanced sitemap options</summary></details>`;
    destination.before(root);
    const get=id=>root.querySelector('#'+id),rows=new Map();let previous=null,last='',visibleSource='',ownChange=false,selected=null,seenMode='';
    const preview=get('architecture-sitemap-preview');
    const outline=createOutline(get('section-sitemap-choices'),get('section-sitemap-search'),id=>{selected=id;outline.updateSelection(id);selection();get('section-sitemap-heading').focus();});
    function selection() {
      const records=nodes(),node=records.find(node=>node.id===selected),row=rows.get(selected),path=[];let item=node;const byId=new Map(records.map(item=>[item.id,item]));
      while(item){path.unshift(item.label);item=byId.get(item.parentId);}
      get('section-sitemap-name').textContent=node?.label||'No destinations';get('section-sitemap-path').textContent=path.join(' / ');
      get('section-sitemap-included').checked=!!row?.input.checked;get('section-sitemap-included').disabled=!row || row.input.disabled;
      get('section-sitemap-inclusion-help').textContent=!node?'No labelled destinations are available.':row.input.disabled?'A containing destination is excluded. Include its parent before changing this choice.':row.input.checked?'Included in the visitor sitemap.':'Excluded from navigation. Its website content is retained.';
      const link=get('section-sitemap-preview-link');link.hidden=!node;if(node)link.dataset.sitemapTarget=node.id;else delete link.dataset.sitemapTarget;
    }
    function sync() {
      const plan=DSStudio.process.currentPlan(),mode=sample(),current=source(plan),next=JSON.stringify([mode,plan.sitemapSource,plan.sitemapExcluded]);
      const workspace=current==='sections'?get('section-sitemap-settings'):destination.querySelector('.sitemap-workspace');
      if(preview.parentElement!==workspace)workspace.append(preview);
      if(mode!==seenMode){selected=null;outline.reset();seenMode=mode;}
      if(last!==next && !ownChange){previous=null;get('section-sitemap-undo').disabled=true;}last=next;
      get('sitemap-source').value=current;destination.hidden=current!=='custom';raw.hidden=current!=='custom';get('section-sitemap-settings').hidden=current!=='sections';
      get('sitemap-source-summary').textContent=current==='custom'?'Using your saved custom destination plan.':'Labels follow the page eyebrows and headings.';
      get('architecture-sitemap-advanced').hidden=current!=='custom';
      if(current!==visibleSource && current==='custom')destination.open=true;visibleSource=current;
      const excluded=new Set(plan.sitemapExcluded[mode]),effective=new Map(),keep=new Set(),box=get('section-sitemap-choices');
      nodes().forEach((node,index)=>{
        keep.add(node.id);let row=rows.get(node.id);
        if(!row){const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');input.type='checkbox';input.dataset.sectionId=node.id;label.append(input,text);row={label,input,text};rows.set(node.id,row);}
        const inherited=!node.parentId || effective.get(node.parentId);effective.set(node.id,inherited && !excluded.has(node.id));
        row.input.checked=!excluded.has(node.id);row.input.disabled=!inherited;
        row.input.setAttribute('aria-label','Include '+node.label+' in sitemap'+(!inherited?', ancestor excluded':''));
        row.label.classList.toggle('is-child',node.depth===2);row.label.classList.toggle('is-grandchild',node.depth>2);
        row.text.textContent=node.label+(!inherited?' (ancestor excluded)':'');
      });
      for(const [id,row]of rows)if(!keep.has(id)){row.label.remove();rows.delete(id);}
      const records=nodes();if(!records.some(node=>node.id===selected))selected=records[0]?.id||null;
      outline.sync(records,id=>rows.get(id),selected);selection();
    }
    function commit(change,message) {
      const plan=DSStudio.process.normalize(state.designProcess);previous={sitemapSource:plan.sitemapSource,sitemapExcluded:plan.sitemapExcluded};state.designProcess=DSStudio.process.normalize({...plan,...change});
      ownChange=true;try{apply();}finally{ownChange=false;}
      get('section-sitemap-undo').disabled=false;get('section-sitemap-status').textContent=message;
    }
    get('sitemap-source').addEventListener('change',()=>{if(!DSStudio.sitemapEditor.canLeave()){get('sitemap-source').value=source();return;}commit({sitemapSource:{...DSStudio.process.currentPlan().sitemapSource,[sample()]:get('sitemap-source').value}},'Sitemap source updated. Your content and saved custom plan are retained.');});
    get('section-sitemap-choices').addEventListener('change',event=>{
      const input=event.target.closest('input[data-section-id]');if(!input || !nodes().some(node=>node.id===input.dataset.sectionId))return;
      const plan=DSStudio.process.currentPlan(),excluded=new Set(plan.sitemapExcluded[sample()]);
      if(input.checked)excluded.delete(input.dataset.sectionId);else excluded.add(input.dataset.sectionId);
      commit({sitemapExcluded:{...plan.sitemapExcluded,[sample()]:[...excluded]}},'Sitemap sections updated. Website content is retained.');
    });
    get('section-sitemap-included').setAttribute('aria-describedby','section-sitemap-inclusion-help');
    get('section-sitemap-included').addEventListener('change',()=>{const input=rows.get(selected)?.input;if(!input || input.disabled)return;input.checked=get('section-sitemap-included').checked;input.dispatchEvent(new Event('change',{bubbles:true}));});
    get('section-sitemap-restore').addEventListener('click',()=>commit({sitemapExcluded:{...DSStudio.process.currentPlan().sitemapExcluded,[sample()]:[]}},'All labelled sections included in this sample. Undo is available.'));
    get('section-sitemap-undo').addEventListener('click',()=>{if(!previous)return;state.designProcess=DSStudio.process.normalize({...state.designProcess,...previous});previous=null;ownChange=true;try{apply();}finally{ownChange=false;}get('section-sitemap-undo').disabled=true;get('section-sitemap-status').textContent='Last sitemap configuration undone.';});
    for(const name of ['dss:reset','dss:imported'])document.addEventListener(name,()=>{previous=null;last='';selected=null;outline.reset();get('section-sitemap-undo').disabled=true;get('section-sitemap-status').textContent='';sync();});
    return sync;
  }
  DSStudio.sectionSitemap={source,collect,nodes,markup,initControls,createOutline,isCollecting:()=>collecting};
})();
