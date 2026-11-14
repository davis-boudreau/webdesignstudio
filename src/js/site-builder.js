'use strict';
/* Edit the existing bounded plan; previews and exports keep
   using their shared generators. Imported labels are always rendered as text. */
DSStudio.register({
  id: 'site-builder', title: 'Information architecture and sitemap choices',
  init() {
    const get = id => document.getElementById(id);
    const root = get('sitemap-editor');
    root.className = 'sitemap-editor';
    root.innerHTML = `<select id="sitemap-items" hidden aria-label="Selected custom destination"></select>
      <p class="help" id="sitemap-help">Custom navigation uses your own labels and grouping instead of the page eyebrow hierarchy. This destination hierarchy also preserves previous outlines. Its compact editor supports three navigation levels; the content outline supports deeper containment.</p>
      <div class="sitemap-workspace"><section class="sitemap-browser" aria-label="Find custom destinations"><label for="sitemap-search">Find destination</label><input id="sitemap-search" type="search" placeholder="Search custom destinations"><div id="sitemap-choices" class="sitemap-choices" role="region" tabindex="0" aria-label="Sitemap inclusion choices"></div>
      <button id="sitemap-new" type="button" class="ghost">Add destination</button><details><summary>Organise destinations</summary><div class="button-row"><button id="sitemap-up" type="button" class="ghost">Move up</button><button id="sitemap-down" type="button" class="ghost">Move down</button><button id="sitemap-delete" type="button" class="ghost">Delete entry</button></div></details></section>
      <form id="sitemap-form" class="sitemap-properties" aria-labelledby="sitemap-selected-heading"><h4 id="sitemap-selected-heading">Selected destination properties</h4><strong id="sitemap-selected-name"></strong><p id="sitemap-selected-path" class="help"></p>
        <label class="sitemap-selected-inclusion"><input id="sitemap-included" type="checkbox"> Include in visitor sitemap</label><p id="sitemap-inclusion-help" class="help"></p>
        <label for="sitemap-label">Entry label</label><input id="sitemap-label" maxlength="64" required autocomplete="off">
        <label for="sitemap-parent">Parent section</label><select id="sitemap-parent"></select>
        <label for="sitemap-type">Information type</label><select id="sitemap-type"><option value="section">Page section</option><option value="page">Page</option><option value="group">Group (heading only)</option><option value="content">Content item</option></select>
        <label for="sitemap-target">Link destination</label><select id="sitemap-target"></select>
        <p class="help">Choose an existing section, or keep a planned page without a link. Groups are headings rather than links. Information types describe the plan; they do not create or remove website content.</p>
        <div class="button-row"><button id="sitemap-save" type="submit" class="ghost">Save destination</button><button id="sitemap-discard" type="button" class="ghost" disabled>Discard unsaved edits</button></div>
      </form></div>
      <label class="sitemap-planned-toggle"><input id="sitemap-planned" type="checkbox"> Also show selected planned entries without links</label>
      <button id="sitemap-undo" type="button" class="ghost" disabled>Undo last architecture or sitemap change</button>
      <p id="sitemap-status" class="help" role="status"></p>`;
    let selected=null,previous=null,signature='',undoMode=null,ownChange=false,dirty=false,seenMode='';
    const mode=()=>state.sampleMode==='basic'?'basic':'advanced';
    const plan=()=>DSStudio.process.currentPlan();
    const records=()=>DSStudio.process.entries(plan());
    const key=node=>node.position.length===1?`${node.position[0]}:-1`:node.position.join(':');
    const parentKey=node=>node.position.join(':');
    const samePath=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
    const within=(path,parent)=>path.length>=parent.length && parent.every((part,i)=>path[i]===part);
    const options=(control,items)=>control.replaceChildren(...items.map(([value,label])=>new Option(label,value)));
    const strip=({id,path,type,includeInSitemap})=>({id,path:[...path],type,includeInSitemap});
    const rows=new Map();
    const outline=DSStudio.sectionSitemap.createOutline(get('sitemap-choices'),get('sitemap-search'),id=>{if(!canLeave())return;selected=id;get('sitemap-items').value=key(records().find(node=>node.id===id));outline.updateSelection(id);edit();get('sitemap-label').focus();});
    function canLeave() {
      if(!dirty)return true;
      get('sitemap-status').textContent='Save or discard your unsaved destination edits before changing the selection or sitemap.';get('sitemap-save').focus();return false;
    }
    DSStudio.sitemapEditor={canLeave};
    function syncChoices(nodes) {
      const box=get('sitemap-choices'),keep=new Set(),effective=new Map();
      nodes.forEach((node,index)=>{
        const inherited=!node.parentId || effective.get(node.parentId);
        effective.set(node.id,inherited && node.includeInSitemap);
        const rowKey=mode()+':'+node.id;keep.add(rowKey);
        let row=rows.get(rowKey);
        if(!row){
          const label=document.createElement('label'),input=document.createElement('input'),text=document.createElement('span');
          input.type='checkbox';input.dataset.iaId=node.id;label.append(input,text);row={label,input,text};rows.set(rowKey,row);
        }
        row.input.checked=node.includeInSitemap;row.input.disabled=!inherited;
        row.input.setAttribute('aria-label','Include '+node.label+' in sitemap'+(!inherited?', ancestor excluded':''));
        row.label.classList.toggle('is-child',node.depth===2);
        row.label.classList.toggle('is-grandchild',node.depth===3);
        const description=node.label+(!inherited?' (ancestor excluded)':'');
        if(row.text.textContent!==description)row.text.textContent=description;
      });
      for(const [rowKey,row] of rows)if(!keep.has(rowKey)){row.label.remove();rows.delete(rowKey);}
      outline.sync(nodes,id=>rows.get(mode()+':'+id),selected);
    }
    function edit() {
      const nodes=records(),node=nodes.find(node=>node.id===selected);
      dirty=false;get('sitemap-discard').disabled=true;
      get('sitemap-selected-name').textContent=node?.label||'New destination';get('sitemap-selected-path').textContent=node?node.path.join(' / '):'Choose a name and containing destination, then save.';
      const inclusion=rows.get(mode()+':'+selected)?.input;
      get('sitemap-included').checked=!!inclusion?.checked;get('sitemap-included').disabled=!node || !!inclusion?.disabled;
      get('sitemap-inclusion-help').textContent=!node?'Save this destination before configuring inclusion.':inclusion?.disabled?'A containing destination is excluded. Include its parent first.':'Inclusion changes navigation only; website content is retained.';
      outline.updateSelection(selected);
      const descendants=node?nodes.filter(item=>within(item.path,node.path)):[];
      const height=node?Math.max(...descendants.map(item=>item.depth-node.depth+1)):1;
      get('sitemap-label').value=node?.label || '';
      get('sitemap-type').value=node?.type || 'page';
      const parents=nodes.filter(item=>item.depth<3 && item.depth+height<=3 && (!node || !within(item.path,node.path)));
      options(get('sitemap-parent'),[['','Top level'],...parents.map(item=>[parentKey(item),item.path.join(' / ')])]);
      const parent=nodes.find(item=>item.id===node?.parentId);
      get('sitemap-parent').value=parent?parentKey(parent):'';
      options(get('sitemap-target'),[['planned','Planned page (no link)'],['auto','Match the label automatically'],...DSStudio.process.inventory(mode()).map(([name,id])=>[id,name])]);
      const links=plan().pageLinks[mode()],label=node?.label;
      get('sitemap-target').value=Object.hasOwn(links,label)?links[label] || 'planned':label?DSStudio.process.inventory(mode()).find(([name])=>name===label)?.[1] || 'auto':'planned';
      get('sitemap-target').disabled=get('sitemap-type').value==='group';
      get('sitemap-delete').disabled=!node;
      get('sitemap-delete').textContent=descendants.length>1?`Delete group (${descendants.length} entries)`:'Delete entry';
      const siblings=nodes.filter(item=>item.parentId===node?.parentId),index=siblings.findIndex(item=>item.id===selected);
      get('sitemap-up').disabled=!node || index<=0;
      get('sitemap-down').disabled=!node || index<0 || index>=siblings.length-1;
    }
    function sync() {
      const current=plan(),next=JSON.stringify([mode(),current.pages,current.pageLinks,current.iaEntries,current.showPlanned,current.sitemapSource,current.sitemapExcluded]);
      if(signature===next)return;
      if(!ownChange || undoMode!==mode()){previous=null;get('sitemap-undo').disabled=true;}
      signature=next;
      const nodes=records();
      if(seenMode!==mode()){outline.reset();seenMode=mode();}
      if(!nodes.some(node=>node.id===selected))selected=nodes[0]?.id ?? null;
      options(get('sitemap-items'),nodes.map(node=>[key(node),'\u00a0\u00a0'.repeat(node.depth-1)+(node.depth>1?'— ':'')+node.label]));
      get('sitemap-items').value=nodes.find(node=>node.id===selected)?key(nodes.find(node=>node.id===selected)):'';
      get('sitemap-planned').checked=current.showPlanned;
      syncChoices(nodes);edit();
    }
    function commit(nodes,links,message,{showPlanned=plan().showPlanned,oldPath=null,newPath=null}={}) {
      const current=plan(),sameStructure=samePath(nodes.map(node=>node.path),records().map(node=>node.path));
      const pages=sameStructure?current.pages:nodes.map(node=>node.path.join(' > ')).join('\n');
      if((!sameStructure && nodes.length>64) || pages.length>8400){get('sitemap-status').textContent='Keep the information architecture within 64 entries and 8,400 characters.';return false;}
      if(nodes.some(node=>node.path.length>3)){get('sitemap-status').textContent='Use at most three information levels.';return false;}
      const data={basic:current.iaEntries.basic.map(strip),advanced:current.iaEntries.advanced.map(strip)};
      const used=new Set([...data[mode()].map(node=>node.id),...nodes.map(node=>node.id).filter(Boolean)]);let nextId=1;
      for(const node of nodes)if(!node.id){while(used.has('ia-'+nextId))nextId++;node.id='ia-'+nextId++;used.add(node.id);}
      data[mode()]=nodes.map(strip);
      if(oldPath)for(const sample of ['basic','advanced'])if(sample!==mode())data[sample]=data[sample].flatMap(node=>!within(node.path,oldPath)?[node]:newPath?[{...node,path:[...newPath,...node.path.slice(oldPath.length)]}]:[]);
      previous=DSStudio.process.normalize(current);undoMode=mode();
      dirty=false;state.designProcess=DSStudio.process.normalize({...current,pages,pageLinks:{...current.pageLinks,[mode()]:links},iaEntries:data,showPlanned,sitemapSource:{...current.sitemapSource,[mode()]:'custom'}});
      signature='';ownChange=true;try{apply();}finally{ownChange=false;}
      get('sitemap-undo').disabled=false;get('sitemap-status').textContent=message;return true;
    }
    get('sitemap-items').addEventListener('change',event=>{if(!canLeave()){event.target.value=records().find(node=>node.id===selected)?key(records().find(node=>node.id===selected)):'';return;}selected=records().find(node=>key(node)===event.target.value)?.id ?? null;edit();});
    for(const type of ['input','change'])get('sitemap-form').addEventListener(type,event=>{if(event.target.id==='sitemap-included')return;dirty=true;get('sitemap-discard').disabled=false;get('sitemap-status').textContent='Unsaved destination edits. Save or discard before choosing another destination.';});
    get('sitemap-discard').addEventListener('click',()=>{edit();get('sitemap-status').textContent='Unsaved destination edits discarded.';get('sitemap-save').focus();});
    for(const id of ['sitemap-new','sitemap-up','sitemap-down','sitemap-delete','sitemap-undo','sitemap-planned'])get(id).addEventListener('click',event=>{if(!canLeave()){event.preventDefault();event.stopImmediatePropagation();}},true);
    get('sitemap-type').addEventListener('change',()=>{get('sitemap-target').disabled=get('sitemap-type').value==='group';});
    get('sitemap-parent').addEventListener('change',()=>{if(selected===null){const parent=records().find(node=>parentKey(node)===get('sitemap-parent').value);get('sitemap-type').value=parent?.depth===2?'content':'page';}});
    get('sitemap-choices').addEventListener('change',event=>{
      const input=event.target.closest('input[data-ia-id]');if(!input || input.disabled)return;
      const nodes=records(),node=nodes.find(node=>node.id===input.dataset.iaId);if(!node)return;
      if(!canLeave()){input.checked=node.includeInSitemap;return;}
      node.includeInSitemap=input.checked;
      commit(nodes,{...plan().pageLinks[mode()]},'Sitemap inclusion updated. Information architecture and website content are retained.');
    });
    get('sitemap-included').setAttribute('aria-describedby','sitemap-inclusion-help');
    get('sitemap-included').addEventListener('change',()=>{const input=rows.get(mode()+':'+selected)?.input;if(!input || input.disabled)return;if(!canLeave()){get('sitemap-included').checked=input.checked;return;}input.checked=get('sitemap-included').checked;input.dispatchEvent(new Event('change',{bubbles:true}));});
    get('sitemap-new').addEventListener('click',()=>{selected=null;get('sitemap-items').selectedIndex=-1;edit();get('sitemap-label').focus();});
    get('sitemap-form').addEventListener('submit',event=>{
      event.preventDefault();
      const label=get('sitemap-label').value.trim(),nodes=records(),node=nodes.find(node=>node.id===selected),parentValue=get('sitemap-parent').value;
      if(!label || label.length>64 || /[>\r\n]/.test(label) || nodes.some(item=>item.id!==selected && item.label===label)){get('sitemap-status').textContent='Use a unique label of 1–64 characters without > or line breaks.';return;}
      const parent=parentValue===''?null:nodes.find(item=>parentKey(item)===parentValue);
      const branch=node?nodes.filter(item=>within(item.path,node.path)):[];
      const height=node?Math.max(...branch.map(item=>item.depth-node.depth+1)):1;
      if((parentValue!=='' && !parent) || (parent && (parent.depth+height>3 || (node && within(parent.path,node.path))))){get('sitemap-status').textContent='Choose a parent outside this branch; at most three information levels are supported.';return;}
      const oldPath=node?[...node.path]:null,newPath=[...(parent?.path || []),label],type=get('sitemap-type').value;
      const links={...plan().pageLinks[mode()]},target=get('sitemap-target').value;
      if(node)delete links[node.label];
      if(target!=='auto')links[label]=target==='planned'?'':target;
      const sameParent=node && samePath(node.path.slice(0,-1),parent?.path || []);
      let next;
      if(sameParent){next=nodes.map(item=>within(item.path,oldPath)?{...item,path:[...newPath,...item.path.slice(oldPath.length)],...(item.id===node.id?{type}: {})}:item);}
      else{
        next=nodes.filter(item=>!node || !within(item.path,oldPath));
        const moved=node?branch.map(item=>({...item,path:[...newPath,...item.path.slice(oldPath.length)],...(item.id===node.id?{type}: {})})):[{id:null,path:newPath,type,includeInSitemap:type!=='content'}];
        const last=parent?next.findLastIndex(item=>within(item.path,parent.path)):next.length-1;
        next.splice(last+1,0,...moved);
        if(!node)selected=null;
      }
      if(commit(next,links,`Saved ${label}. Information architecture and sitemap updated.`,{oldPath,newPath})){
        selected=records().find(item=>samePath(item.path,newPath))?.id ?? null;edit();get('sitemap-items').value=key(records().find(item=>item.id===selected));outline.focus(selected);
      }
    });
    get('sitemap-delete').addEventListener('click',()=>{
      const nodes=records(),node=nodes.find(node=>node.id===selected);if(!node)return;
      const removed=nodes.filter(item=>within(item.path,node.path)),links={...plan().pageLinks[mode()]};
      removed.forEach(item=>delete links[item.label]);
      if(commit(nodes.filter(item=>!within(item.path,node.path)),links,`Deleted ${removed.length} ${removed.length===1?'entry':'entries'}. Undo is available.`,{oldPath:node.path})){outline.focus(selected);}
    });
    for(const [id,delta] of [['sitemap-up',-1],['sitemap-down',1]])get(id).addEventListener('click',()=>{
      const nodes=records(),node=nodes.find(node=>node.id===selected);if(!node)return;
      const siblings=nodes.filter(item=>item.parentId===node.parentId),index=siblings.findIndex(item=>item.id===selected),other=siblings[index+delta];if(!other)return;
      const moved=nodes.filter(item=>within(item.path,node.path)),rest=nodes.filter(item=>!within(item.path,node.path));
      const insert=delta<0?rest.findIndex(item=>item.id===other.id):rest.findLastIndex(item=>within(item.path,other.path))+1;
      rest.splice(insert,0,...moved);commit(rest,{...plan().pageLinks[mode()]},'Sitemap order updated.');
    });
    get('sitemap-planned').addEventListener('change',()=>commit(records(),{...plan().pageLinks[mode()]},'Footer visibility updated.',{showPlanned:get('sitemap-planned').checked}));
    get('sitemap-undo').addEventListener('click',()=>{if(!previous)return;state.designProcess=previous;previous=null;signature='';apply();get('sitemap-undo').disabled=true;get('sitemap-status').textContent='Last architecture or sitemap change undone.';});
    for(const event of ['dss:reset','dss:imported'])document.addEventListener(event,()=>{previous=null;dirty=false;outline.reset();get('sitemap-undo').disabled=true;get('sitemap-status').textContent='';signature='';sync();});
    DSStudio.on('output:updated',sync);sync();
  }
});
