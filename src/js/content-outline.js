'use strict';
DSStudio.register({
  id:'content-outline',title:'Website content structure',
  init() {
    const model=DSStudio.contentArchitecture,get=id=>document.getElementById(id),sample=()=>state.sampleMode==='basic'?'basic':'advanced';
    const legacy=get('sitemap-editor'),destination=document.createElement('details');
    destination.id='sitemap-destination-editor';
    const summary=document.createElement('summary');summary.textContent='Manage sitemap destinations';destination.append(summary);legacy.before(destination);destination.append(legacy);
    const raw=get('plan-pages').closest('details');
    raw.id='sitemap-outline-editor';raw.querySelector(':scope > summary').textContent='Sitemap text outline';
    const root=document.createElement('section');root.id='ia-content-editor';root.className='ia-content-editor';destination.before(root);
    root.innerHTML=`<h3>Website content structure</h3><p class="help">Inspect meaningful containers and actual content. Navigation links reference destinations elsewhere. Planned wording and notes are saved with this project; they do not rewrite the sample website.</p>
      <label for="ia-search">Find content</label><input id="ia-search" type="search" placeholder="Search labels, text and notes">
      <div class="button-row"><button id="ia-expand" type="button" class="ghost">Expand all</button><button id="ia-collapse" type="button" class="ghost">Collapse all</button></div>
      <p id="ia-count" class="help" role="status"></p><div id="ia-outline" class="ia-outline" role="region" tabindex="0" aria-label="Expandable website content outline"></div>
      <div class="button-row"><button id="ia-add-child" type="button" class="ghost">Add child</button><button id="ia-add-sibling" type="button" class="ghost">Add sibling</button><button id="ia-add-root" type="button" class="ghost">Add top-level entry</button></div>
      <form id="ia-form"><h4 id="ia-editor-heading">Selected content</h4><p id="ia-current-path" class="help"></p>
        <label for="ia-label">Role or planning label</label><input id="ia-label" maxlength="120" required>
        <label for="ia-type">Content type</label><select id="ia-type">${model.types.map(type=>`<option value="${type}">${({region:'Shared region',page:'Page',section:'Section',group:'Content group',text:'Text',image:'Image',link:'Navigation link / CTA',field:'Form field / control'})[type]}</option>`).join('')}</select>
        <label for="ia-parent">Contained in</label><select id="ia-parent"></select>
        <label for="ia-actual">Current sample content</label><textarea id="ia-actual" rows="4" readonly></textarea>
        <label for="ia-draft">Planned content</label><textarea id="ia-draft" rows="4" maxlength="2400" placeholder="Write proposed wording or describe the asset needed"></textarea>
        <label class="ia-checkbox"><input id="ia-has-draft" type="checkbox"> Use this planned content (including deliberately empty content)</label>
        <label for="ia-status">Planning status</label><select id="ia-status"><option value="present">Present in sample</option><option value="planned">Planned</option><option value="needs-content">Needs content</option></select>
        <label for="ia-target">Destination or reference</label><select id="ia-target"></select><p id="ia-reference-help" class="help"></p>
        <label for="ia-notes">Planning notes</label><textarea id="ia-notes" rows="3" maxlength="1200"></textarea>
        <div class="button-row"><button type="submit" class="ghost">Save content plan</button><button id="ia-delete" type="button" class="ghost">Delete branch</button></div>
      </form>
      <div class="button-row"><button id="ia-up" type="button" class="ghost">Move up</button><button id="ia-down" type="button" class="ghost">Move down</button><button id="ia-undo" type="button" class="ghost" disabled>Undo content change</button></div>
      <p id="ia-sitemap-summary" class="help"></p><button id="ia-manage-sitemap" type="button" class="ghost">Edit this sitemap destination</button>
      <details><summary>Restore sample content inventory</summary><p class="help">Replace this sample's content planning edits with its current website inventory. Other samples and sitemap choices are kept. Undo is available.</p><button id="ia-restore" type="button" class="ghost">Restore current sample content</button></details>
      <p id="ia-status-message" class="help" role="status"></p>`;
    let selected=null,newParent=null,creating=false,previous=null,signature='',modeSeen=sample(),expanded=new Set(),ownChange=false;
    const list=()=>model.nodes();
    const tell=message=>get('ia-status-message').textContent=message;
    function targets() {get('ia-target').replaceChildren(new Option('No destination',''),...DSStudio.process.inventory(sample()).map(([label,id])=>new Option(label,id)));}
    function edit() {
      const rows=list(),node=creating?null:rows.find(node=>node.id===selected),branch=node?model.descendants(rows,node.id):new Set();
      get('ia-label').value=node?.label||'';get('ia-type').value=node?.type||'text';
      const height=node?Math.max(...rows.filter(item=>branch.has(item.id)).map(item=>model.path(rows,item).length-model.path(rows,node).length+1)):1;
      const parents=rows.filter(item=>!branch.has(item.id) && model.path(rows,item).length+height<=model.MAX_DEPTH);
      get('ia-parent').replaceChildren(new Option('Top level',''),...parents.map(item=>new Option(model.path(rows,item).join(' / ')+((item.draft??item.value)?' — '+(item.draft??item.value).slice(0,70):''),item.id)));
      get('ia-parent').value=creating?newParent||'':node?.parentId||'';
      get('ia-current-path').textContent=node?model.path(rows,node).join(' / '):'New planning entry';
      get('ia-actual').value=node?.sourceMissing?'This source item is not present in the current sample.':node?(node.value||'No text content for this container.')+(node.reference?'\nReference: '+node.reference:''):'No current sample content. Describe what is needed below.';
      get('ia-draft').value=node?.draft??'';get('ia-has-draft').checked=node?.draft!==null && !!node;
      get('ia-notes').value=node?.notes||'';get('ia-status').value=node?.status||'planned';targets();get('ia-target').value=node?.target||'';
      get('ia-reference-help').textContent=node?.type==='link'?'This link references an existing destination. Its place in this content outline does not create a page or sitemap entry.':'A section can reference its matching destination. Sitemap labels, grouping and membership are managed separately below.';
      get('ia-delete').disabled=!node;get('ia-delete').textContent=node?`Delete branch (${branch.size} ${branch.size===1?'entry':'entries'})`:'Delete branch';
      const siblings=rows.filter(item=>item.parentId===node?.parentId),index=siblings.findIndex(item=>item.id===selected);
      get('ia-up').disabled=!node || index<=0;get('ia-down').disabled=!node || index<0 || index>=siblings.length-1;
      get('ia-add-child').disabled=!node || model.path(rows,node).length>=model.MAX_DEPTH;get('ia-add-sibling').disabled=!node;
      const destinationNode=node && node.type!=='link' && node.target?DSStudio.process.entries().find(entry=>DSStudio.process.destinationId(entry.label)===node.target):null;
      get('ia-manage-sitemap').disabled=!destinationNode;
      get('ia-manage-sitemap').dataset.entryId=destinationNode?.id||'';
      get('ia-sitemap-summary').textContent=destinationNode?`Sitemap destination: ${destinationNode.label}. ${destinationNode.includeInSitemap?'Selected; parent destination choices also apply.':'Excluded from the visitor sitemap.'}`:node?.type==='link'?'Navigation references do not have separate sitemap membership. Select the referenced section to manage its destination.':'Content entries do not automatically become sitemap destinations. Use Manage sitemap destinations to plan a new destination.';
    }
    function renderOutline() {
      const rows=list(),query=get('ia-search').value.trim().toLowerCase(),matches=new Set(rows.filter(node=>[node.label,node.value,node.draft,node.notes,node.target,node.reference].join(' ').toLowerCase().includes(query)).map(node=>node.id));
      const visible=new Set(matches);
      for(const id of matches){let node=rows.find(node=>node.id===id);while(node?.parentId){visible.add(node.parentId);node=rows.find(item=>item.id===node.parentId);}}
      const fragment=document.createDocumentFragment();
      function append(parentId,container) {
        const ul=document.createElement('ul');
        for(const node of rows.filter(node=>node.parentId===parentId && (!query || visible.has(node.id)))) {
          const li=document.createElement('li'),children=rows.some(child=>child.parentId===node.id),button=document.createElement('button');button.type='button';button.dataset.contentId=node.id;button.className='ia-select';button.setAttribute('aria-pressed',String(node.id===selected && !creating));
          const label=document.createElement('span');label.textContent=node.label;button.append(label);
          const value=node.draft??node.value;if(value){const preview=document.createElement('small');preview.textContent=value.length>110?value.slice(0,110)+'…':value;button.append(preview);}
          const kind=document.createElement('small');kind.className='ia-kind';kind.textContent=node.type+(node.type==='link' && node.target?' → '+(DSStudio.process.inventory(sample()).find(([,id])=>id===node.target)?.[0]||node.target):'')+(node.status!=='present'?' · '+node.status:'');button.append(kind);
          if(children){const details=document.createElement('details'),summary=document.createElement('summary');details.dataset.contentBranch=node.id;details.open=!!query || expanded.has(node.id);summary.append(button);details.append(summary);append(node.id,details);li.append(details);}else li.append(button);
          ul.append(li);
        }
        container.append(ul);
      }
      append(null,fragment);get('ia-outline').replaceChildren(fragment);
      get('ia-count').textContent=query?`${matches.size} matching entries; ancestors shown for context.`:`${rows.length} content entries. Expand only the branches you need.`;
    }
    function sync(force=false) {
      if(!force && DSStudio.activeStage!==1)return;
      const rows=list(),next=JSON.stringify([sample(),rows,DSStudio.process.currentPlan().iaEntries,DSStudio.process.currentPlan().pages,DSStudio.process.currentPlan().pageLinks]);
      if(signature===next && !force)return;
      if(modeSeen!==sample()){selected=null;creating=false;previous=null;expanded=new Set();get('ia-search').value='';modeSeen=sample();}
      if(!ownChange && signature && signature!==next){previous=null;get('ia-undo').disabled=true;}
      signature=next;
      if(!creating && !rows.some(node=>node.id===selected))selected=rows[0]?.id||null;
      renderOutline();edit();get('ia-undo').disabled=!previous;
    }
    function commit(rows,message) {
      const normalized=model.normalizeNodes(rows,sample());
      if(rows.length>model.MAX_NODES || normalized.length!==rows.length){tell(`Keep a valid outline within ${model.MAX_NODES} entries and ${model.MAX_DEPTH} nesting levels. For a large plan, shorten drafts or notes. Cycles and duplicate identities are not allowed.`);return false;}
      previous=DSStudio.process.normalize(state.designProcess);
      state.designProcess=DSStudio.process.normalize({...state.designProcess,contentPlan:{...state.designProcess.contentPlan,[sample()]:normalized}});
      ownChange=true;try{apply();}finally{ownChange=false;}
      get('ia-undo').disabled=false;tell(message);return true;
    }
    get('ia-outline').addEventListener('click',event=>{
      const button=event.target.closest('button[data-content-id]');if(!button)return;event.preventDefault();selected=button.dataset.contentId;creating=false;renderOutline();edit();get('ia-label').focus();
    });
    get('ia-outline').addEventListener('toggle',event=>{const id=event.target.dataset.contentBranch;if(id && !get('ia-search').value.trim()){if(event.target.open)expanded.add(id);else expanded.delete(id);}},true);
    get('ia-search').addEventListener('input',renderOutline);
    get('ia-expand').addEventListener('click',()=>{expanded=new Set(list().map(node=>node.id));renderOutline();});
    get('ia-collapse').addEventListener('click',()=>{expanded.clear();get('ia-search').value='';renderOutline();});
    const begin=parentId=>{creating=true;newParent=parentId;edit();get('ia-label').focus();};
    get('ia-add-child').addEventListener('click',()=>begin(selected));get('ia-add-sibling').addEventListener('click',()=>begin(list().find(node=>node.id===selected)?.parentId||null));get('ia-add-root').addEventListener('click',()=>begin(null));
    get('ia-draft').addEventListener('input',()=>{get('ia-has-draft').checked=true;});
    get('ia-type').addEventListener('change',()=>{get('ia-reference-help').textContent=get('ia-type').value==='link'?'This link references a destination; it does not duplicate that destination.':'Plan content containment here. Manage navigation destinations separately.';});
    get('ia-form').addEventListener('submit',event=>{
      event.preventDefault();const rows=list(),node=creating?null:rows.find(node=>node.id===selected),label=get('ia-label').value.trim(),parentId=get('ia-parent').value||null;
      const descendants=node?model.descendants(rows,node.id):new Set();
      if(!label || label.length>120 || (parentId && (!rows.some(item=>item.id===parentId) || descendants.has(parentId)))){tell('Choose a label and a parent outside this branch.');return;}
      let nextId=1;while(rows.some(item=>item.id==='content-user-'+nextId))nextId++;
      const saved={...(node||{id:'content-user-'+nextId,sourceKey:'',value:''}),parentId,label,type:get('ia-type').value,draft:get('ia-has-draft').checked?get('ia-draft').value:null,notes:get('ia-notes').value,status:get('ia-status').value,target:get('ia-target').value};
      let next=rows.map(item=>item.id===node?.id?saved:item);
      if(!node)next.push(saved);
      else if(node.parentId!==parentId){const moved=new Set(descendants);const branch=next.filter(item=>moved.has(item.id));next=next.filter(item=>!moved.has(item.id));next.push(...branch);}
      // Display order is sibling order in the array; descendants retain IDs and data.
      const height=node?Math.max(...rows.filter(item=>descendants.has(item.id)).map(item=>model.path(rows,item).length-model.path(rows,node).length+1)):1;
      const parent=rows.find(item=>item.id===parentId);
      if((parent?model.path(rows,parent).length:0)+height>model.MAX_DEPTH){tell(`This move would exceed ${model.MAX_DEPTH} nesting levels.`);return;}
      selected=saved.id;creating=false;if(parentId)expanded.add(parentId);
      if(commit(next,`Saved ${label}. Sample content and sitemap choices are retained.`)){sync(true);get('ia-label').focus();}
    });
    get('ia-delete').addEventListener('click',()=>{const rows=list(),branch=model.descendants(rows,selected),node=rows.find(item=>item.id===selected);if(!node)return;selected=node.parentId;creating=false;commit(rows.filter(item=>!branch.has(item.id)),`Deleted ${branch.size} content planning entries. Undo is available. Sitemap destinations and sample content are retained.`);});
    for(const [id,delta]of [['ia-up',-1],['ia-down',1]])get(id).addEventListener('click',()=>{const rows=list(),node=rows.find(item=>item.id===selected);if(!node)return;const siblings=rows.filter(item=>item.parentId===node.parentId),other=siblings[siblings.indexOf(node)+delta];if(!other)return;const branch=model.descendants(rows,node.id),otherBranch=model.descendants(rows,other.id),moved=rows.filter(item=>branch.has(item.id)),rest=rows.filter(item=>!branch.has(item.id));const index=delta<0?rest.findIndex(item=>item.id===other.id):rest.findLastIndex(item=>otherBranch.has(item.id))+1;rest.splice(index,0,...moved);commit(rest,'Content order updated.');});
    get('ia-undo').addEventListener('click',()=>{if(!previous)return;state.designProcess=previous;previous=null;ownChange=true;try{apply();}finally{ownChange=false;}get('ia-undo').disabled=true;tell('Last content planning change undone.');});
    get('ia-restore').addEventListener('click',()=>{previous=DSStudio.process.normalize(state.designProcess);state.designProcess=DSStudio.process.normalize({...state.designProcess,contentPlan:{...state.designProcess.contentPlan,[sample()]:null}});selected=null;creating=false;ownChange=true;try{apply();}finally{ownChange=false;}get('ia-undo').disabled=false;tell('Current sample content restored. Sitemap choices retained. Undo is available.');});
    get('ia-manage-sitemap').addEventListener('click',()=>{const node=DSStudio.process.entries().find(node=>node.id===get('ia-manage-sitemap').dataset.entryId);if(!node)return;destination.open=true;get('sitemap-items').value=node.position.length===1?`${node.position[0]}:-1`:node.position.join(':');get('sitemap-items').dispatchEvent(new Event('change',{bubbles:true}));get('sitemap-label').focus();});
    for(const event of ['dss:reset','dss:imported'])document.addEventListener(event,()=>{selected=null;creating=false;previous=null;signature='';expanded.clear();get('ia-search').value='';tell('');sync(true);});
    // Rebuild only when actual content/planning changes. Theme and token edits
    // cannot execute imported content or overwrite a form while it is being typed.
    const before=renderCode;renderCode=function(){model.prepare();before();sync();};
    DSStudio.on('stage:change',({stage})=>{if(stage.index===1)sync(true);});
    sync(true);renderCode();
  }
});
