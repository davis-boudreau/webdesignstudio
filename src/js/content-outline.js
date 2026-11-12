'use strict';
DSStudio.register({
  id:'content-outline',title:'Website content structure',
  init() {
    const model=DSStudio.contentArchitecture,get=id=>document.getElementById(id),sample=()=>state.sampleMode==='basic'?'basic':'advanced';
    const legacy=get('sitemap-editor'),destination=document.createElement('details');
    destination.id='sitemap-destination-editor';
    const summary=document.createElement('summary');summary.textContent='Custom destinations';destination.append(summary);legacy.before(destination);destination.append(legacy);
    const raw=get('plan-pages').closest('details');
    raw.id='sitemap-outline-editor';raw.querySelector(':scope > summary').textContent='Sitemap text outline';
    const root=document.createElement('section');root.id='ia-content-editor';root.className='ia-content-editor';destination.before(root);
    const typeNames=model.typeNames;
    const typeHelp={region:'A shared area, such as Header or Footer, holds content used across the website.',page:'A page brings together information for a visitor task.',section:'A section groups related information around one topic.',group:'A content group holds smaller items, such as an image and its caption.',text:'A text item contains words, such as a heading, paragraph or image description.',image:'An image item represents a visual asset. Plan what it should show and the text alternative it needs.',link:'A link helps a visitor reach a destination. Plan clear link wording and where it should lead.',field:'A field or control lets someone enter information or take an action. Plan its label and instructions.'};
    root.innerHTML=`<h3>Content structure</h3><p class="help">Choose an item to edit its website text, organise its place or develop its content plan.</p>
      <details class="ia-learning-guide"><summary>How to develop a content plan</summary><ol><li><strong>Choose an item.</strong> Expand a branch and select a heading, image, link or container.</li><li><strong>Understand it.</strong> Read its properties and current content. Decide what the audience needs from it.</li><li><strong>Edit and save.</strong> Change Website content to update the page. Use the content plan for proposals, ownership and next actions. Save before choosing another item.</li></ol><p class="help">Try Home ? Hero ? Heading. Edit Website content to write a clearer heading for your intended audience, then explain why it helps in your planning notes. Review the saved result in the website preview.</p></details>
      <label for="ia-search">Find content</label><input id="ia-search" type="search" placeholder="Search names, content and notes">
      <div class="button-row"><button id="ia-expand" type="button" class="ghost">Expand all</button><button id="ia-collapse" type="button" class="ghost">Collapse all</button></div>
      <p id="ia-count" class="help" role="status"></p><div id="ia-outline" class="ia-outline" role="region" tabindex="0" aria-label="Expandable website content outline"></div>
      <div class="ia-add-controls"><label for="ia-add-placement">Place new item</label><select id="ia-add-placement"><option value="inside">Inside selected item</option><option value="beside">Beside selected item</option><option value="top">At top level</option></select><button id="ia-add" type="button" class="ghost">Add item</button></div>
      <p class="help">Inside adds a child in the hierarchy. Beside adds an item at the same level. Top level starts a new branch.</p>
      <form id="ia-form" aria-labelledby="ia-editor-heading">
        <header class="ia-selection-heading"><strong id="ia-selected-name"></strong><p id="ia-current-path" class="help"></p><p id="ia-origin" class="ia-origin"></p></header>
        <section id="ia-properties" aria-labelledby="ia-editor-heading"><h4 id="ia-editor-heading">Selected content properties</h4>
        <div class="ia-field ia-readiness"><label for="ia-status">Content readiness</label><select id="ia-status" aria-describedby="ia-status-help"><option value="present">Available in the sample</option><option value="planned">Still to create</option><option value="needs-content">Needs content or revision</option></select><p id="ia-status-help" class="help">Status for this item. Update it as its content is created, revised or reviewed.</p></div>
        <fieldset class="ia-property-group" id="ia-website-content"><legend>Website content</legend>
          <p class="help" id="ia-website-help">These words appear on the website when you save. Separate fields preserve inline formatting and links. Planning proposals remain separate.</p>
          <div id="ia-website-fields"></div><p id="ia-website-reason" class="help"></p>
          <button id="ia-restore-item" type="button" class="ghost">Use original text for this item</button>
          <p id="ia-website-missing" class="help" role="status"></p>
        </fieldset>
        <fieldset class="ia-property-group"><legend>Understand this item</legend>
          <p class="help">Properties describe this item and its place in your outline.</p>
          <div class="ia-current-content"><label id="ia-actual-label" for="ia-actual">In the sample (read only)</label><textarea id="ia-actual" rows="3" readonly aria-describedby="ia-actual-help"></textarea><p id="ia-actual-help" class="help"></p></div>
          <div class="ia-field"><label for="ia-label">Name in the outline</label><input id="ia-label" maxlength="120" required aria-describedby="ia-label-help"><p id="ia-label-help" class="help">Names this item, such as Hero heading. Edit its website words above or use Develop the content plan above.</p></div>
          <div class="ia-field"><label for="ia-type">Kind of content</label><select id="ia-type" aria-describedby="ia-type-help">${model.types.map(type=>`<option value="${type}">${typeNames[type]}</option>`).join('')}</select><p id="ia-type-help" class="help"></p></div>
          <div class="ia-field"><label for="ia-parent">Lives inside</label><select id="ia-parent" aria-describedby="ia-parent-help"></select><p id="ia-parent-help" class="help">Choose its containing item, or Top level for a new branch.</p></div>
          <div class="ia-field"><label for="ia-target">Related website section (optional)</label><select id="ia-target" aria-describedby="ia-reference-help"></select><p id="ia-reference-help" class="help"></p></div>

        </fieldset>
        </section>
        <details id="ia-content-plan" class="ia-editor-disclosure ia-content-planning"><summary><h4 id="ia-plan-heading">Develop the content plan</h4></summary>
        <fieldset class="ia-property-group ia-plan-group" aria-labelledby="ia-plan-heading">
          <p id="ia-plan-selection" class="help"></p>
          <p id="ia-plan-boundary" class="help">Your proposal is saved with this project. It does not replace the sample website's text, images or links.</p>
          <div class="ia-field"><label id="ia-draft-label" for="ia-draft">Proposed content</label><p id="ia-draft-help" class="help"></p><textarea id="ia-draft" rows="4" maxlength="2400" aria-describedby="ia-draft-help ia-plan-boundary"></textarea></div>
          <label class="ia-checkbox"><input id="ia-has-draft" type="checkbox" aria-describedby="ia-proposal-state"> Include this proposal in the saved plan</label><p id="ia-proposal-state" class="help"></p>
          <div class="ia-field"><label for="ia-notes">Purpose, owner and next action</label><textarea id="ia-notes" rows="4" maxlength="1200" placeholder="Purpose: What should this help visitors do?&#10;Owner: Who will supply or review it?&#10;Next action: What needs to happen?" aria-describedby="ia-notes-help"></textarea><p id="ia-notes-help" class="help">Explain the decision so someone else can continue the work. Note missing information or a review date when useful.</p></div>
        </fieldset>
        </details>
        <section class="ia-save-area" aria-labelledby="ia-save-heading"><h4 id="ia-save-heading">Save and review</h4><p id="ia-edit-state" class="help" role="status"></p><div class="button-row"><button id="ia-save" type="submit" form="ia-form" class="ghost">Save content plan</button><button id="ia-discard" type="button" class="ghost" disabled>Discard unsaved edits</button></div><p class="help">Saving applies Website content to the page and keeps proposals separately in the plan. Review the website preview and saved plan. Save before selecting another item. Save a project JSON backup when you are ready to continue elsewhere.</p></section>
      </form>
      <p id="ia-status-message" class="help" role="status"></p>
      <div class="ia-branch-tools"><h4>Organize this branch</h4><p class="help">Move an item among others at the same level, or remove it and its children from the plan. The sample website stays available.</p><div class="button-row"><button id="ia-up" type="button" class="ghost">Move up</button><button id="ia-down" type="button" class="ghost">Move down</button><button id="ia-delete" type="button" class="ghost">Delete branch</button><button id="ia-undo" type="button" class="ghost" disabled>Undo content change</button></div></div>
      <p id="ia-sitemap-summary" class="help"></p><button id="ia-manage-sitemap" type="button" class="ghost">Edit this sitemap destination</button>
      <details><summary>Restore sample content inventory</summary><p class="help">Restore this sample's original website text and content inventory, replacing its website text edits and content plan. Other samples and sitemap choices are kept. Undo is available.</p><button id="ia-restore" type="button" class="ghost">Restore current sample content</button></details>`;
    // Keep the existing controls and listeners in one responsive editing surface.
    const browser=document.createElement('section');browser.className='ia-browser';browser.setAttribute('aria-label','Find and select website content');
    const grid=document.createElement('div');grid.className='ia-workspace-grid';
    const search=get('ia-search'),form=get('ia-form');
    const treeUtilities=get('ia-expand').parentElement;
    browser.append(search.previousElementSibling,search,get('ia-count'),get('ia-outline'));
    const introduction=document.createElement('header');introduction.className='ia-browser-heading';
    introduction.append(root.querySelector(':scope > h3'),root.querySelector(':scope > p'));browser.prepend(introduction);
    const add=document.createElement('details');add.className='ia-add-menu';
    const addSummary=document.createElement('summary');addSummary.textContent='Add item';add.append(addSummary);
    const addRow=get('ia-add').parentElement,addHelp=addRow.nextElementSibling;add.append(addRow,addHelp);browser.append(add);
    grid.append(browser,form);root.querySelector('.ia-learning-guide').after(grid);
    const branch=root.querySelector('.ia-branch-tools'),branchMenu=document.createElement('details'),branchSummary=document.createElement('summary');
    branchSummary.textContent='Organise content';branchMenu.append(branchSummary);
    branch.querySelector('h4').remove();while(branch.firstChild)branchMenu.append(branch.firstChild);branch.append(branchMenu);
    branchMenu.append(treeUtilities);
    // Undo stays visible even when branch actions are closed.
    const branchSelection=document.createElement('p');branchSelection.id='ia-branch-selection';branchSelection.className='help';branchMenu.querySelector('summary').after(branchSelection);
    branch.append(get('ia-undo'));browser.append(branch);
    const save=root.querySelector('.ia-save-area');save.append(get('ia-status-message'));browser.append(save);
    const restore=get('ia-restore'),restoreDisclosure=restore.closest('details'),restoreHelp=restoreDisclosure.querySelector('p');
    restoreHelp.id='ia-restore-help';restore.setAttribute('aria-describedby',restoreHelp.id);
    get('ia-save').parentElement.append(restore);save.append(restoreHelp);restoreDisclosure.remove();
    const related=document.createElement('details');related.id='ia-related-section';related.className='ia-editor-disclosure';
    const relatedSummary=document.createElement('summary');relatedSummary.textContent='Related website section';related.append(relatedSummary,get('ia-target').closest('.ia-field'),get('ia-sitemap-summary'),get('ia-manage-sitemap'));get('ia-properties').append(related);
    const syncSitemap=DSStudio.sectionSitemap.initControls(destination,raw);
    let selected=null,newParent=null,creating=false,previous=null,signature='',contentSignature='',modeSeen=sample(),expanded=new Set(),ownChange=false,dirty=false,websiteFields=[];
    const list=()=>model.nodes();
    const tell=message=>{get('ia-status-message').textContent=message;if(message){const review=get('architecture-saved-review');if(review)review.open=true;}};
    function focusSave() {
      const review=get('architecture-saved-review');if(review)review.open=true;
      get('ia-save').focus();
    }
    function canLeaveItem(message='Save or discard your unsaved edits before choosing another item or changing the branch.') {
      if(!dirty)return true;
      tell(message);
      focusSave();return false;
    }
    for(const id of ['ia-delete','ia-up','ia-down','ia-undo','ia-restore'])get(id).addEventListener('click',event=>{
      if(!canLeaveItem()){event.preventDefault();event.stopImmediatePropagation();}
    },true);
    function proposalState() {
      get('ia-proposal-state').textContent=!get('ia-has-draft').checked?'No proposed replacement. Properties, readiness and notes can still be saved.':get('ia-draft').value.trim()?'This proposal will be saved separately from the current sample content.':'An intentionally blank proposal will be saved. This does not delete the sample content.';
    }
    function planningGuidance() {
      const kind=get('ia-type').value;
      const guidance=({
        image:['Image brief','Revise the selected image description and alternative text.'],
        link:['Proposed link wording','Revise this link wording. Its current destination is shown in the item properties.'],
        field:['Proposed label or instructions','Revise this control\'s label or instructions using its current website content.'],
        text:['Proposed wording','Start with this item\'s current website wording and revise it for your site.']
      })[kind]||['What this area needs','Describe what this website area should contain and how its content should be grouped.'];
      get('ia-type-help').textContent=typeHelp[kind];get('ia-draft-label').textContent=guidance[0];get('ia-draft-help').textContent=guidance[1];get('ia-draft').placeholder=guidance[0];
    }
    function editState(changed=false) {
      dirty=changed;get('ia-discard').disabled=!dirty;
      if(dirty){const review=get('architecture-saved-review');if(review)review.open=true;}
      get('ia-edit-state').textContent=dirty?'Unsaved edits ? choose Save content plan before selecting another item.':creating?'New item ? give it a name, develop its plan, then save.':'Viewing the saved plan. Edit any field to develop this item.';
    }
    function targets() {get('ia-target').replaceChildren(new Option('No related section',''),...DSStudio.process.inventory(sample()).map(([label,id])=>new Option(label,id)));}
    function edit() {
      const rows=list(),node=creating?null:rows.find(node=>node.id===selected),branch=node?model.descendants(rows,node.id):new Set();
      get('ia-label').value=node?.label||'';get('ia-type').value=node?.type||'text';
      const height=node?Math.max(...rows.filter(item=>branch.has(item.id)).map(item=>model.path(rows,item).length-model.path(rows,node).length+1)):1;
      const parents=rows.filter(item=>!branch.has(item.id) && model.path(rows,item).length+height<=model.MAX_DEPTH);
      get('ia-parent').replaceChildren(new Option('Top level',''),...parents.map(item=>new Option(model.path(rows,item).join(' / ')+((item.draft??item.value)?' — '+(item.draft??item.value).slice(0,70):''),item.id)));
      get('ia-parent').value=creating?newParent||'':node?.parentId||'';
      get('ia-selected-name').textContent=node?.label||'New planning item';
      get('ia-branch-selection').textContent=node?'Selected: '+node.label:'Save the new item before moving or removing it.';
      get('ia-current-path').textContent=node?'Location: '+model.path(rows,node).join(' / '):'Choose where this new item belongs in the outline.';
      get('ia-plan-selection').textContent=node?'Planning for: '+model.path(rows,node).join(' / '):'Planning for: a new content item. Name it in Content structure below.';
      get('ia-origin').textContent=node?.sourceMissing?'Sample source is no longer available':node?.sourceKey?'From the sample website':'Planning item ? not added to the sample website';
      const children=rows.filter(item=>item.parentId===node?.id).length;
      get('ia-actual-help').textContent=children?`This item contains ${children} ${children===1?'item':'items'}. Expand its branch to inspect them. This is a summary of the saved website content.`:'This is the saved website text. Edit Website content above to change the page, or develop a separate proposal above.';
      get('ia-actual-label').textContent=node?.sourceMissing?'Sample content unavailable':node?.sourceKey?'Saved website content (read only)':'Recorded content (read only)';
      get('ia-actual').value=node?.sourceMissing?'This source item is not present in the current sample.':node?(node.value||'No text content for this container.')+(node.reference?'\nReference: '+node.reference:''):'No current sample content. Describe what is needed below.';
      const website=DSStudio.websiteContent.describe(node?.sourceKey||'',sample());websiteFields=website.fields;
      const controls=document.createDocumentFragment();
      websiteFields.forEach((field,index)=>{
        const group=document.createElement('div'),label=document.createElement('label'),input=document.createElement('textarea');group.className='ia-field';
        input.id='ia-website-field-'+index;input.rows=field.field.startsWith('text:')?3:2;input.maxLength=DSStudio.websiteContent.MAX_CHARS;input.value=field.value;input.dataset.websiteField=String(index);input.setAttribute('aria-describedby','ia-website-help');
        label.htmlFor=input.id;label.textContent=field.label+(websiteFields.filter(other=>other.label===field.label).length>1?' ('+(index+1)+')':'');group.append(label,input);controls.append(group);
      });
      get('ia-website-fields').replaceChildren(controls);get('ia-website-reason').textContent=website.reason;get('ia-website-reason').hidden=!website.reason;
      get('ia-restore-item').hidden=!websiteFields.some(field=>field.value!==field.original);get('ia-website-help').hidden=!websiteFields.length;
      get('ia-website-missing').textContent=website.missing?`${website.missing} saved website text edits have unavailable or changed source bindings. They are retained in your project but are not applied. Restore the sample to remove them.`:'';
      get('ia-website-missing').hidden=!website.missing;
      const currentWording=websiteFields.map(field=>field.value).filter(Boolean).join('\n')||(!node?.sourceMissing && ['text','link','field'].includes(node?.type)?node.value:'');
      get('ia-draft').value=node?.draft??currentWording.slice(0,2400);get('ia-has-draft').checked=node?.draft!==null && !!node;
      planningGuidance();proposalState();editState();
      get('ia-notes').value=node?.notes||'';get('ia-status').value=node?.status||'planned';targets();get('ia-target').value=node?.target||'';
      get('ia-notes').placeholder=node?model.planningNotes(rows,node,sample()):'Purpose: Describe this new item\'s role in '+state.project+'.\nOwner: Unassigned.\nNext action: Add its content and review it in the prototype.';
      get('ia-reference-help').textContent=node?.type==='link'?'Choose the section this link should reach. This planning choice does not change the sample link.':'Optional connection to an existing section. Sitemap inclusion is configured below.';
      get('ia-delete').disabled=!node;get('ia-delete').textContent=node?`Delete branch (${branch.size} ${branch.size===1?'entry':'entries'})`:'Delete branch';
      const siblings=rows.filter(item=>item.parentId===node?.parentId),index=siblings.findIndex(item=>item.id===selected);
      get('ia-up').disabled=!node || index<=0;get('ia-down').disabled=!node || index<0 || index>=siblings.length-1;
      get('ia-add-placement').options[0].disabled=!node || model.path(rows,node).length>=model.MAX_DEPTH;get('ia-add-placement').options[1].disabled=!node;
      if(get('ia-add-placement').selectedOptions[0]?.disabled)get('ia-add-placement').value='top';
      get('ia-related-section').open=node?.type==='link';
      const destinationNode=node && node.type!=='link' && node.target?DSStudio.process.entries().find(entry=>DSStudio.process.destinationId(entry.label)===node.target):null;
      const section=DSStudio.sectionSitemap.source()==='sections' && node?.type!=='link'?DSStudio.sectionSitemap.nodes().find(item=>item.id===node?.target):null;
      get('ia-manage-sitemap').disabled=DSStudio.sectionSitemap.source()==='sections'?!section:!destinationNode;
      get('ia-manage-sitemap').dataset.sectionId=section?.id||'';
      get('ia-manage-sitemap').textContent=section?'Configure this sitemap section':'Edit this sitemap destination';
      get('ia-manage-sitemap').dataset.entryId=destinationNode?.id||'';
      get('ia-sitemap-summary').textContent=section?`Sitemap label: ${section.label}. Configure inclusion below; the label follows the visible page content.`:DSStudio.sectionSitemap.source()==='sections'?(node?.type==='link'?'Navigation references do not have separate sitemap membership. Select the referenced section to configure inclusion.':'The Sitemap links to labelled page sections. This content is reached through its containing section.'):destinationNode?`Sitemap destination: ${destinationNode.label}. ${destinationNode.includeInSitemap?'Selected; parent destination choices also apply.':'Excluded from the visitor sitemap.'}`:node?.type==='link'?'Navigation references do not have separate sitemap membership. Select the referenced section to manage its destination.':'Content entries do not automatically become sitemap destinations. Use Manage sitemap destinations to plan a new destination.';
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
          const kind=document.createElement('small');kind.className='ia-kind';kind.textContent=typeNames[node.type]+(node.type==='link' && node.target?' → '+(DSStudio.process.inventory(sample()).find(([,id])=>id===node.target)?.[0]||node.target):'')+(node.status!=='present'?' · '+model.statusNames[node.status]:'');button.append(kind);
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
      const rows=list(),next=JSON.stringify([sample(),rows,state.designProcess.websiteContent,DSStudio.process.currentPlan().iaEntries,DSStudio.process.currentPlan().pages,DSStudio.process.currentPlan().pageLinks,DSStudio.process.currentPlan().sitemapSource,DSStudio.process.currentPlan().sitemapExcluded]);
      if(signature===next && !force)return;
      if(modeSeen!==sample()){selected=null;creating=false;previous=null;expanded=new Set();get('ia-search').value='';modeSeen=sample();}
      if(!ownChange && signature && signature!==next){previous=null;get('ia-undo').disabled=true;}
      signature=next;
      const nextContent=JSON.stringify([sample(),rows,state.designProcess.websiteContent]),keepEdits=dirty && contentSignature===nextContent;
      contentSignature=nextContent;
      if(!creating && !rows.some(node=>node.id===selected))selected=rows[0]?.id||null;
      renderOutline();if(!keepEdits)edit();get('ia-undo').disabled=!previous;
    }
    function commit(rows,message,websiteEdits=null) {
      const normalized=model.normalizeNodes(rows,sample());
      if(rows.length>model.MAX_NODES || normalized.length!==rows.length){tell(`Keep a valid outline within ${model.MAX_NODES} entries and ${model.MAX_DEPTH} nesting levels. For a large plan, shorten drafts or notes. Cycles and duplicate identities are not allowed.`);return false;}
      previous=DSStudio.process.normalize(state.designProcess);
      state.designProcess=DSStudio.process.normalize({...state.designProcess,contentPlan:{...state.designProcess.contentPlan,[sample()]:normalized},websiteContent:{...state.designProcess.websiteContent,[sample()]:websiteEdits??state.designProcess.websiteContent[sample()]}});
      ownChange=true;try{apply();}finally{ownChange=false;}
      get('ia-undo').disabled=false;tell(message);return true;
    }
    get('ia-outline').addEventListener('click',event=>{
      const button=event.target.closest('button[data-content-id]');if(!button)return;event.preventDefault();if(!canLeaveItem())return;selected=button.dataset.contentId;creating=false;renderOutline();edit();get('ia-label').focus();
    });
    get('ia-outline').addEventListener('toggle',event=>{const id=event.target.dataset.contentBranch;if(id && !get('ia-search').value.trim()){if(event.target.open)expanded.add(id);else expanded.delete(id);}},true);
    get('ia-search').addEventListener('input',renderOutline);
    get('ia-expand').addEventListener('click',()=>{expanded=new Set(list().map(node=>node.id));renderOutline();});
    get('ia-collapse').addEventListener('click',()=>{expanded.clear();get('ia-search').value='';renderOutline();});
    const begin=parentId=>{if(!canLeaveItem())return;creating=true;newParent=parentId;edit();get('ia-label').focus();};
    get('ia-add').addEventListener('click',()=>{const placement=get('ia-add-placement');if(placement.selectedOptions[0]?.disabled)return;begin(placement.value==='inside'?selected:placement.value==='beside'?list().find(node=>node.id===selected)?.parentId||null:null);});
    get('ia-draft').addEventListener('input',()=>{get('ia-has-draft').checked=true;proposalState();});
    get('ia-has-draft').addEventListener('change',proposalState);
    for(const editor of [get('ia-form'),get('ia-content-plan')]) {
      for(const type of ['input','change'])editor.addEventListener(type,()=>{if(!dirty){editState(true);tell('');}});
      editor.addEventListener('invalid',event=>{const disclosure=event.target.closest('.ia-editor-disclosure');if(disclosure)disclosure.open=true;},true);
    }
    get('ia-discard').addEventListener('click',()=>{edit();tell('Unsaved edits discarded. Your saved website text and plan are retained.');focusSave();});
    get('ia-restore-item').addEventListener('click',()=>{websiteFields.forEach((field,index)=>{get('ia-website-field-'+index).value=field.original;});editState(true);tell('Original website text selected. Save to apply it, or discard to keep your saved text.');});
    get('ia-type').addEventListener('change',()=>{planningGuidance();if(get('ia-type').value==='link')get('ia-related-section').open=true;get('ia-reference-help').textContent=get('ia-type').value==='link'?'This link references a destination; it does not duplicate that destination.':'Plan content containment here. Manage navigation destinations separately.';});
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
      const websiteEdits=DSStudio.websiteContent.merge(sample(),websiteFields.map((field,index)=>({...field,value:get('ia-website-field-'+index).value})));
      if(!websiteEdits){tell('Website text exceeds the project limits. Shorten your edits before saving.');return;}
      selected=saved.id;creating=false;if(parentId)expanded.add(parentId);
      if(commit(next,`Saved ${label}. Website text and content plan updated. Sitemap choices retained.`,websiteEdits)){sync(true);focusSave();}
    });
    get('ia-delete').addEventListener('click',()=>{const rows=list(),branch=model.descendants(rows,selected),node=rows.find(item=>item.id===selected);if(!node)return;selected=node.parentId;creating=false;commit(rows.filter(item=>!branch.has(item.id)),`Deleted ${branch.size} content planning entries. Undo is available. Sitemap destinations and sample content are retained.`);});
    for(const [id,delta]of [['ia-up',-1],['ia-down',1]])get(id).addEventListener('click',()=>{const rows=list(),node=rows.find(item=>item.id===selected);if(!node)return;const siblings=rows.filter(item=>item.parentId===node.parentId),other=siblings[siblings.indexOf(node)+delta];if(!other)return;const branch=model.descendants(rows,node.id),otherBranch=model.descendants(rows,other.id),moved=rows.filter(item=>branch.has(item.id)),rest=rows.filter(item=>!branch.has(item.id));const index=delta<0?rest.findIndex(item=>item.id===other.id):rest.findLastIndex(item=>otherBranch.has(item.id))+1;rest.splice(index,0,...moved);commit(rest,'Content order updated.');});
    get('ia-undo').addEventListener('click',()=>{if(!previous)return;state.designProcess=previous;previous=null;ownChange=true;try{apply();}finally{ownChange=false;}get('ia-undo').disabled=true;tell('Last content change undone.');});
    get('ia-restore').addEventListener('click',()=>{previous=DSStudio.process.normalize(state.designProcess);state.designProcess=DSStudio.process.normalize({...state.designProcess,contentPlan:{...state.designProcess.contentPlan,[sample()]:null},websiteContent:{...state.designProcess.websiteContent,[sample()]:[]}});selected=null;creating=false;ownChange=true;try{apply();}finally{ownChange=false;}get('ia-undo').disabled=false;tell('Current sample website text and content inventory restored. Sitemap choices retained. Undo is available.');});
    get('ia-manage-sitemap').addEventListener('click',()=>{const view=get('architecture-sitemap');if(view)view.open=true;const sectionId=get('ia-manage-sitemap').dataset.sectionId;if(sectionId){const controls=[...document.querySelectorAll('#section-sitemap-choices input')],sections=DSStudio.sectionSitemap.nodes();let id=sectionId,checkbox=controls.find(input=>input.dataset.sectionId===id);while(checkbox?.disabled){id=sections.find(item=>item.id===id)?.parentId;checkbox=controls.find(input=>input.dataset.sectionId===id);}if(checkbox)for(let parent=checkbox.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;checkbox?.scrollIntoView({block:'nearest'});checkbox?.focus();return;}const node=DSStudio.process.entries().find(node=>node.id===get('ia-manage-sitemap').dataset.entryId);if(!node)return;const advanced=get('architecture-sitemap-advanced');if(advanced)advanced.open=true;destination.open=true;get('sitemap-items').value=node.position.length===1?`${node.position[0]}:-1`:node.position.join(':');get('sitemap-items').dispatchEvent(new Event('change',{bubbles:true}));get('sitemap-label').focus();});
    for(const event of ['dss:reset','dss:imported'])document.addEventListener(event,()=>{selected=null;creating=false;previous=null;signature='';dirty=false;expanded.clear();get('ia-search').value='';get('ia-content-plan').open=false;tell('');sync(true);});
    // Rebuild only when actual content/planning changes. Theme and token edits
    // cannot execute imported content or overwrite a form while it is being typed.
    const before=renderCode;renderCode=function(){model.prepare();before();syncSitemap();sync();};
    DSStudio.on('stage:change',({stage})=>{if(stage.index===1)sync(true);});
    DSStudio.contentEditor={canLeave:canLeaveItem,isDirty:()=>dirty,select(id){
      if(!canLeaveItem())return false;
      const rows=list(),node=rows.find(item=>item.id===id);if(!node)return false;
      selected=id;creating=false;get('ia-search').value='';
      let parent=node.parentId;while(parent){expanded.add(parent);parent=rows.find(item=>item.id===parent)?.parentId;}
      renderOutline();edit();get('ia-label').focus();return true;
    }};
    syncSitemap();sync(true);renderCode();
  }
});
