"""Independent content-tree editor, proposal and import browser checks.

Run: python scripts/content_tree_review.py. Uses its own isolated app/profile
and shared Chrome runner; never imports or patches the integration harness.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Content tree review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Content tree review: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const revealArchitecture=()=>d.querySelectorAll('#architecture-sitemap,#architecture-saved-review,#architecture-sitemap-advanced,#architecture-advanced,#sitemap-choices details,#section-sitemap-choices details,#sitemap-editor details').forEach(el=>el.open=true);
  const addContent=placement=>{d.getElementById('ia-add-placement').value=placement;d.getElementById('ia-add').click();};
  // Destination-editor fixtures explicitly reveal its secondary controls.
  const revealDestinationPlan=()=>{revealArchitecture();const source=d.getElementById('sitemap-source');if(source && source.value!=='custom'){source.value='custom';source.dispatchEvent(new w.Event('change',{bubbles:true}));}d.querySelectorAll('#sitemap-destination-editor, #sitemap-outline-editor, #process-ia .ia-destination-map, #sitemap-choices details, #sitemap-editor details').forEach(el=>el.open=true);};
  const input = (id, value, type='input') => {
    if(id.startsWith('sitemap-') || id==='plan-pages')revealDestinationPlan();
    const el=d.getElementById(id);
    w.DSStudio.paletteWorkspace?.revealControl(el);
    w.DSStudio.typographyWorkspace?.revealControl(el);
    if(id.startsWith('ia-')){const disclosure=el.closest('.ia-editor-disclosure');if(disclosure)disclosure.open=true;}
    el.value=value;
    el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  // Blob/File reads use real I/O. A pending local request prevents Chrome's
  // virtual clock from expiring an artificial timer before that I/O completes.
  const loadSelectedProjectFile = async () => {
    let imported=false;const alerts=[],oldAlert=w.alert,done=()=>{imported=true;};
    d.addEventListener('dss:imported',done,{once:true});w.alert=message=>alerts.push(String(message));
    try {
      d.getElementById('loadFile').dispatchEvent(new w.Event('change',{bubbles:true}));
      for(let attempt=0;!imported && !alerts.length && attempt<100;attempt++)await fetch('/__review_tick__?attempt='+attempt,{cache:'no-store'});
      if(!imported)throw new Error('Project file import did not complete: '+alerts.join('; '));
      return true;
    } finally {d.removeEventListener('dss:imported',done);w.alert=oldAlert;}
  };
  const importFile=async text=>{
    const transfer=new w.DataTransfer();transfer.items.add(new w.File([text],'project.json',{type:'application/json'}));
    d.getElementById('loadFile').files=transfer.files;
    await loadSelectedProjectFile();
  };
  try {
  test('Independent content-tree startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  test('Architecture starts with one primary editor and optional navigation, saved review and advanced tools closed',()=>d.querySelector('#ia-content-editor .ia-browser-heading > h3').textContent==='Content structure' && ['architecture-sitemap','architecture-saved-review','architecture-advanced','architecture-sitemap-advanced'].every(id=>!d.getElementById(id).open) && d.getElementById('architecture-saved-review').contains(d.querySelector('#process-ia .ia-content-map')) && d.querySelectorAll('#process-ia .process-sitemap-preview').length===1 && d.getElementById('architecture-sitemap').contains(d.querySelector('#process-ia .process-sitemap-preview')));
  reset();await wait();
  // Complete content inventory, independent destination references and deep editing.
  {
  await w.DSStudio.ready;
  d.getElementById('sitemap-destination-editor').open=false;
  const model=w.DSStudio.contentArchitecture;
  const contentNodes=()=>model.nodes();
  const contentNode=(label,value)=>contentNodes().find(node=>node.type!=='link' && node.label===label && (value===undefined || node.value===value))||contentNodes().find(node=>node.label===label && (value===undefined || node.value===value));
  const selectContent=id=>{const button=d.querySelector('[data-content-id="'+id+'"]');let ancestor=button.parentElement;while(ancestor){if(ancestor.tagName==='DETAILS')ancestor.open=true;ancestor=ancestor.parentElement;}button.click();};
  const saveContent=async()=>{d.getElementById('ia-form').requestSubmit();await wait();};
  test('Content outline starts without runtime errors and keeps Restore with Save without the footer inspection shortcut',()=>!w.__reviewErrors.length && d.getElementById('ia-content-editor') && !d.getElementById('sitemap-destination-editor').open && d.getElementById('ia-restore').closest('.ia-save-area') && d.getElementById('ia-restore').parentElement===d.getElementById('ia-save').parentElement && !d.querySelector('#architecture-advanced #ia-restore, #process-ia [data-inspect="html"]') && d.getElementById('ia-restore').getAttribute('aria-describedby')==='ia-restore-help');
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
    const nodes=contentNodes(),header=contentNode('Header'),home=contentNode('Home'),hero=nodes.find(node=>node.parentId===home.id && node.label==='Hero');
    test(mode+' inventories actual shared header, hero, footer and deep content',()=>nodes.length>100 && nodes.length<=1000 && header.type==='region' && contentNode('Footer').type==='region' && hero && nodes.some(node=>model.path(nodes,node).length>3));
    test(mode+' inventory contains actual heading, logo, wordmark, image alternative text and CTA wording',()=>contentNode('Wordmark').value===evaluate('state.project') && contentNode('Logo') && nodes.some(node=>node.label==='Heading' && node.value===(mode==='basic'?'Start with the essentials.':'A better web starts with one good decision.')) && contentNode('Alternative text') && nodes.some(node=>node.label==='Primary CTA' && node.value===(mode==='basic'?'Explore components':'Find your first lesson')));
    if(mode==='advanced')test('Numeric progress controls are captured as safe text values',()=>nodes.some(node=>node.type==='field' && node.value==='3' && node.label.includes('Practice checklist')));
    const nav=nodes.find(node=>node.label==='Main navigation' && node.parentId===header.id);
    const homeRef=nodes.find(node=>node.parentId===nav.id && node.label==='Home');
    test(mode+' navigation references canonical destinations without duplicating their content',()=>homeRef.type==='link' && homeRef.target==='home' && homeRef.reference==='#home' && nodes.filter(node=>node.target==='home' && node.type!=='link').length===1 && !nodes.some(node=>node.parentId===homeRef.id));
    test(mode+' every authored sitemap destination has exactly one canonical content entry',()=>w.DSStudio.process.inventory(mode).every(([,id])=>nodes.filter(node=>node.target===id && node.type!=='link').length===1));
    test(mode+' native outline starts collapsed and center/export content roles remain safe text',()=>[...d.querySelectorAll('#ia-outline details')].every(el=>!el.open) && d.querySelectorAll('#process-ia .ia-content-map details').length>10 && !d.querySelector('#process-ia .ia-content-map img, #process-ia .ia-content-map script'));
    input('ia-search','alternative text');await wait();
    test(mode+' search reveals matching deep content and ancestor context',()=>d.getElementById('ia-count').textContent.includes('matching') && [...d.querySelectorAll('#ia-outline details')].some(el=>el.open) && d.getElementById('ia-outline').textContent.includes('Alternative text'));
    input('ia-search','');d.getElementById('ia-collapse').click();
    const heading=nodes.find(node=>node.type==='text' && node.label==='Heading' && model.path(nodes,node).includes('Hero'));
    const beforeBody=previewDoc().getElementById('hero-title').textContent,beforeFooter=previewDoc().querySelector('#sitemap').innerHTML;
    selectContent(heading.id);input('ia-draft','A proposed new heading');input('ia-notes','Confirm with the project owner');input('ia-status','planned','change');await saveContent();
    test(mode+' planned content saves alongside current source content without rewriting the sample',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && contentNodes().find(node=>node.id===heading.id).value===beforeBody && previewDoc().getElementById('hero-title').textContent===beforeBody && previewDoc().querySelector('#sitemap').innerHTML===beforeFooter && d.getElementById('ia-actual').value===beforeBody);
    input('ia-draft','');await saveContent();
    test(mode+' an explicitly empty draft is retained',()=>contentNodes().find(node=>node.id===heading.id).draft==='');
    d.getElementById('ia-undo').click();await wait();
    test(mode+' undo restores planned wording',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading');
    const project=JSON.parse(evaluate('projectJson()'));w.importConfig(project);await wait();
    test(mode+' JSON round trip retains content identities, notes and draft separately from actual content',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && contentNodes().find(node=>node.id===heading.id).notes==='Confirm with the project owner' && contentNodes().find(node=>node.id===heading.id).value===beforeBody);
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    test(mode+' local save contains full content planning data',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectId].data.designProcess.contentPlan[mode].some(node=>node.id===heading.id && node.draft==='A proposed new heading'));
    const fileJson=evaluate('projectJson()'),fileTransfer=new w.DataTransfer(),fileAlerts=[],previousAlert=w.alert;
    w.alert=message=>fileAlerts.push(message);fileTransfer.items.add(new w.File([fileJson],'content-plan.json',{type:'application/json'}));d.getElementById('loadFile').files=fileTransfer.files;
    // The file contains the current plan: equality alone cannot prove the file read
    // finished. Await import completion before deleting any planning branches.
    const fileImportCompleted=await loadSelectedProjectFile();await wait();w.alert=previousAlert;
    test(mode+' actual exported JSON file reimports through Load JSON with the complete content plan',()=>fileImportCompleted && !fileAlerts.length && contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && evaluate('projectJson()')===fileJson);
    selectContent(header.id);d.getElementById('ia-delete').click();await wait();
    test(mode+' removing the header planning branch does not remove Home from sitemap or page',()=>!contentNode('Header') && previewDoc().querySelector('#sitemap').innerHTML===beforeFooter && previewDoc().getElementById('home'));
    d.getElementById('ia-undo').click();await wait();
    test(mode+' branch deletion undo restores all descendant identities',()=>contentNode('Header').id===header.id && contentNodes().some(node=>node.id===homeRef.id));
    selectContent(homeRef.id);
    test(mode+' navigation references do not offer separate sitemap membership',()=>d.getElementById('ia-manage-sitemap').disabled && d.getElementById('ia-sitemap-summary').textContent.includes('do not have separate sitemap membership'));
    selectContent(home.id);d.getElementById('ia-manage-sitemap').click();await wait();
    test(mode+' canonical section reaches its matching eyebrow sitemap inclusion control',()=>d.activeElement.dataset.sectionId==='home' && d.getElementById('sitemap-destination-editor').hidden);
    selectContent(hero.id);addContent('inside');input('ia-label','New content group');input('ia-type','group','change');await saveContent();
    const newGroup=contentNode('New content group');
    test(mode+' add child retains the selected container relationship',()=>newGroup.parentId===hero.id && newGroup.status==='planned');
    addContent('inside');input('ia-label','New text');input('ia-draft','Actual planned copy');await saveContent();const child=contentNode('New text');
    selectContent(newGroup.id);input('ia-label','Renamed content group');input('ia-parent',header.id,'change');await saveContent();
    test(mode+' rename and reparent preserve descendant identities and planned copy',()=>contentNode('Renamed content group').id===newGroup.id && contentNode('Renamed content group').parentId===header.id && contentNode('New text').id===child.id && contentNode('New text').parentId===newGroup.id && contentNode('New text').draft==='Actual planned copy');
    const unchanged=evaluate('projectJson()'),forged=new w.Option('Cycle',child.id);d.getElementById('ia-parent').add(forged);input('ia-parent',child.id,'change');await saveContent();
    test(mode+' forged cyclic reparent does not mutate saved content',()=>evaluate('projectJson()')===unchanged && d.getElementById('ia-status-message').textContent.includes('outside this branch'));
    d.getElementById('ia-discard').click();selectContent(child.id);addContent('beside');input('ia-label','Second text');await saveContent();
    const siblingsBefore=contentNodes().filter(node=>node.parentId===newGroup.id).map(node=>node.id).join(',');d.getElementById('ia-up').click();await wait();
    test(mode+' sibling reorder preserves the whole branch and changes order',()=>contentNodes().filter(node=>node.parentId===newGroup.id).map(node=>node.id).join(',')!==siblingsBefore && contentNode('New text').id===child.id);
    const footerBeforeRestore=previewDoc().querySelector('#sitemap').innerHTML;d.getElementById('ia-restore').click();await wait();
    test(mode+' restoring sample inventory clears only that sample content edits and retains sitemap',()=>!contentNode('Renamed content group') && previewDoc().querySelector('#sitemap').innerHTML===footerBeforeRestore && evaluate('state.designProcess.contentPlan.'+mode)===null);
    d.getElementById('ia-undo').click();await wait();
    test(mode+' restore can be undone',()=>contentNode('Renamed content group').id===newGroup.id);
    const paragraphs=contentNodes().filter(node=>node.label==='Paragraph');
    selectContent(paragraphs[0].id);input('ia-notes','Repeated role labels use separate identities');await saveContent();
    test(mode+' repeated paragraph role labels remain independently editable',()=>contentNodes().find(node=>node.id===paragraphs[0].id).notes==='Repeated role labels use separate identities' && contentNodes().find(node=>node.id===paragraphs[1].id).notes!== 'Repeated role labels use separate identities');
  }
  reset();d.getElementById('dockModeBasic').click();await wait();
  selectContent(contentNode('Wordmark').id);input('ia-notes','Basic only');await saveContent();d.getElementById('dockModeAdvanced').click();await wait();
  test('Sample switches retain independent content plans',()=>contentNode('Wordmark').notes!=='Basic only' && contentNode('Wordmark').notes.includes('Advanced Web Design Field Guide'));d.getElementById('dockModeBasic').click();await wait();
  test('Switching back restores the saved content plan',()=>contentNode('Wordmark').notes==='Basic only');
  input('jProject','Renamed live project');await wait();
  test('Current content refreshes from authored source while preserving planned notes and IDs',()=>contentNode('Wordmark').value==='Renamed live project' && contentNode('Wordmark').notes==='Basic only');
  reset();await wait();const invalidContentConfig=JSON.parse(evaluate('projectJson()'));invalidContentConfig.advanced.state='invalid';w.importConfig(invalidContentConfig);await wait();
  test('Advanced-only state changes refresh actual source feedback rather than reusing stale cached text',()=>contentNodes().some(node=>node.value==='Enter an email address in the format name@example.com.'));
  w.importConfig({sampleMode:'basic',designProcess:{pages:'Home\nHome > Future content\nFuture destination',iaEntries:{basic:[{id:'ia-77',path:['Home'],type:'section',includeInSitemap:false}]}}});await wait();
  test('Previous custom plans migrate into the content structure without losing destination choices',()=>contentNode('Future content') && contentNode('Future destination') && contentNode('Home').id==='content-legacy-ia-77' && contentNodes().filter(node=>node.target==='home' && node.type!=='link').length===1 && !w.DSStudio.process.entries().find(node=>node.label==='Home').includeInSitemap);
  const deep=Array.from({length:12},(_,i)=>({id:'content-depth-'+i,parentId:i?'content-depth-'+(i-1):null,label:'Level '+(i+1),type:i===11?'text':'group',draft:i===11?'Twelve levels of useful content':null,status:'planned'}));
  w.importConfig({sampleMode:'basic',designProcess:{contentPlan:{basic:deep}}});w.dssShowWizardStep(1);await wait();
  test('Content structures support twelve levels independently from the destination outline',()=>contentNodes().length===12 && model.path(contentNodes(),contentNode('Level 12')).length===12 && d.querySelectorAll('#ia-outline details').length===11);
  selectContent(contentNode('Level 12').id);test('Depth limit disables adding a child at the boundary',()=>d.getElementById('ia-add-placement').options[0].disabled);
  const unsafe=[{id:'content-safe',parentId:null,label:'<img src=x onerror=alert(1)>',type:'text',draft:'<script>alert(1)<\/script>',notes:'<svg onload=alert(1)>',status:'planned',target:'javascript:alert(1)'},{id:'content-cycle-a',parentId:'content-cycle-b',label:'Cycle A'},{id:'content-cycle-b',parentId:'content-cycle-a',label:'Cycle B'},{id:'content-safe',label:'Duplicate'}];
  const sanitized=model.normalizeNodes(unsafe,'basic');
  test('Content imports validate identities, targets and cycles',()=>sanitized.length===1 && !sanitized[0].target && sanitized[0].label.includes('<img'));
  w.importConfig({sampleMode:'advanced',designProcess:{contentPlan:{advanced:unsafe}}});await wait();
  test('Hostile content labels, drafts and notes stay inert in controls and exported artifacts',()=>!d.querySelector('#ia-content-editor img, #ia-content-editor script, #process-ia .ia-content-map img, #process-ia .ia-content-map svg') && d.getElementById('ia-outline').textContent.includes('<script>') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#ia-lab .ia-content-map img, #ia-lab .ia-content-map script'));
  const oversized=Array.from({length:1010},(_,i)=>({id:'content-bound-'+i,label:'Node '+i,parentId:null,type:'text'}));test('Content imports bound inventory size',()=>model.normalizeNodes(oversized,'basic').length===1000);
  const textHeavy=model.normalizeNodes(Array.from({length:1000},(_,i)=>({id:'content-heavy-'+i,label:'Large '+i,value:'x'.repeat(2400),draft:'y'.repeat(2400),notes:'z'.repeat(1200)})),'basic');
  test('Content imports bound aggregate plan data as well as individual values',()=>textHeavy.length>0 && textHeavy.length<1000 && JSON.stringify(textHeavy).length<=model.MAX_PLAN_CHARS);
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(1);await wait();d.getElementById('ia-expand').click();const heading=model.nodes().find(node=>node.sourceKey==='id:hero-title');selectContent(heading.id);d.querySelectorAll('.ia-editor-disclosure, .ia-add-menu, .ia-branch-tools > details').forEach(el=>el.open=true);
    for(const width of [320,390,1440]) {app.style.width=width+'px';await wait();
      test(mode+' '+theme+' deep outline and content controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && d.getElementById('ia-outline').scrollWidth<=d.getElementById('ia-outline').clientWidth+1 && [...d.querySelectorAll('#ia-content-editor input:not([type=checkbox]), #ia-content-editor select, #ia-content-editor textarea, #ia-content-editor button')].filter(el=>!el.hidden).every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.right<=d.getElementById('ia-content-editor').getBoundingClientRect().right+1;}) && !w.__reviewErrors.length);
    }
  }
  app.style.width='1440px';reset();await wait();
  }

  app.style.width='1440px';reset();await wait();
  // Student content planning: understand the item, propose content, save and review.
  {
    const model=w.DSStudio.contentArchitecture,rows=()=>model.nodes();
    const select=id=>{const button=d.querySelector('[data-content-id="'+id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const heading=rows().find(node=>node.label==='Heading'),home=rows().find(node=>node.label==='Home' && node.type!=='link');select(heading.id);
      test(mode+' selected content identifies the item and teaches its properties',()=>d.getElementById('ia-selected-name').textContent===heading.label && d.getElementById('ia-current-path').textContent.startsWith('Location: ') && d.getElementById('ia-origin').textContent==='From the sample website' && d.getElementById('ia-actual-label').textContent==='Saved website content (read only)' && d.getElementById('ia-type-help').textContent.includes('words') && d.getElementById('ia-actual').readOnly && d.getElementById('ia-actual').value===heading.value);
      test(mode+' content planning uses descriptive unnumbered headings and an explicit sample boundary',()=>[...d.querySelectorAll('#ia-properties > fieldset > legend')].map(el=>el.textContent).join('|')==='Website content|Understand this item' && d.getElementById('ia-plan-heading').textContent==='Develop the content plan' && d.getElementById('ia-save-heading').textContent==='Save and review' && d.getElementById('ia-plan-boundary').textContent.includes('does not replace') && d.getElementById('ia-draft-label').textContent==='Proposed wording');
      const before=evaluate('projectJson()');input('ia-draft','A clear introduction for our learners');input('ia-notes','Purpose: introduce the course. Owner: course tutor. Next action: review with a beginner.');input('ia-status','needs-content','change');
      test(mode+' content edits stay in the form until saved and are clearly marked',()=>evaluate('projectJson()')===before && d.getElementById('ia-has-draft').checked && d.getElementById('ia-edit-state').textContent.includes('Unsaved edits') && !d.getElementById('ia-discard').disabled);
      d.getElementById('architecture-saved-review').open=false;d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' save retains the proposed wording, readiness and next action separately from the sample',()=>{const node=rows().find(node=>node.id===heading.id);return node.draft==='A clear introduction for our learners' && node.notes.includes('Owner: course tutor') && node.status==='needs-content' && node.value===heading.value && d.getElementById('ia-actual').value===heading.value && d.getElementById('ia-edit-state').textContent.includes('saved plan') && d.getElementById('ia-discard').disabled && d.getElementById('architecture-saved-review').open && d.activeElement===d.getElementById('ia-save') && d.getElementById('ia-outline').textContent.includes(node.draft) && d.getElementById('ia-outline').textContent.includes('Needs content or revision') && d.querySelector('#process-ia .ia-content-map').textContent.includes('Needs content or revision');});
      const savedPlan=evaluate('projectJson()');input('ia-label','Unsaved name');input('ia-type','image','change');input('ia-draft','Unsaved image brief');
      test(mode+' changing content kind explains the matching planning task',()=>d.getElementById('ia-draft-label').textContent==='Image brief' && !d.getElementById('ia-example') && d.getElementById('ia-draft-help').textContent.includes('alternative text') && d.getElementById('ia-type-help').textContent.includes('visual asset'));
      d.getElementById('ia-discard').click();
      test(mode+' discarding form edits restores saved properties and proposal without changing the project',()=>evaluate('projectJson()')===savedPlan && d.getElementById('ia-label').value===heading.label && d.getElementById('ia-type').value===heading.type && d.getElementById('ia-draft').value==='A clear introduction for our learners' && d.getElementById('ia-draft-label').textContent==='Proposed wording' && d.getElementById('ia-discard').disabled && d.getElementById('architecture-saved-review').open && d.activeElement===d.getElementById('ia-save'));
      input('ia-draft','');d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' deliberately blank proposals are explained and saved distinctly',()=>rows().find(node=>node.id===heading.id).draft==='' && d.getElementById('ia-proposal-state').textContent.includes('intentionally blank'));
      d.getElementById('ia-has-draft').click();d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' no proposal retains notes and uses the original sample as the starting point',()=>rows().find(node=>node.id===heading.id).draft===null && rows().find(node=>node.id===heading.id).notes.includes('Owner: course tutor') && d.getElementById('ia-proposal-state').textContent.includes('No proposed replacement'));
      for(const [kind,label]of [['image','Image brief'],['link','Proposed link wording'],['field','Proposed label or instructions'],['group','What this area needs']]) {
        const node=rows().find(node=>node.type===kind);select(node.id);
        test(mode+' '+kind+' items show a relevant planning prompt without an example panel',()=>d.getElementById('ia-draft-label').textContent===label && !d.getElementById('ia-example') && d.getElementById('ia-draft-help').textContent.length>30 && d.getElementById('ia-type-help').textContent.length>40);
      }
      select(home.id);addContent('inside');
      test(mode+' adding inside explains a new planning item and retains the chosen parent',()=>d.getElementById('ia-selected-name').textContent==='New planning item' && d.getElementById('ia-origin').textContent.includes('not added to the sample') && d.getElementById('ia-parent').value===home.id && d.getElementById('ia-edit-state').textContent.includes('New item'));
      input('ia-label','Audience introduction');input('ia-draft','Explain who this course is for.');d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' a new item saves within its chosen container and stays explicitly planned',()=>rows().some(node=>node.label==='Audience introduction' && node.parentId===home.id && node.status==='planned' && node.draft==='Explain who this course is for.') && d.getElementById('ia-origin').textContent.includes('not added to the sample') && d.getElementById('ia-actual-label').textContent==='Recorded content (read only)');
    }
    w.importConfig({sampleMode:'basic',designProcess:{contentPlan:{basic:[{id:'content-unsafe-name',label:'<img src=x onerror=alert(1)>',type:'text',draft:'<svg onload=alert(1)>',notes:'<script>unsafe<\/script>'}]}}});w.dssShowWizardStep(1);await wait();
    test('Student item summaries render imported names and proposals as inert text',()=>d.getElementById('ia-selected-name').textContent.includes('<img') && d.getElementById('ia-draft').value.includes('<svg') && !d.querySelector('#ia-form img, #ia-form svg, #ia-form script'));
    app.style.width='1440px';reset();await wait();
  }

  // Architecture uses the current site as its working content, with visible status.
  {
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1,false);await wait();
      const model=w.DSStudio.contentArchitecture,rows=()=>model.nodes(),heading=rows().find(node=>node.sourceKey==='id:hero-title');
      const choose=node=>{const button=d.querySelector('[data-content-id="'+node.id+'"]');for(let p=button.parentElement;p;p=p.parentElement)if(p.tagName==='DETAILS')p.open=true;button.click();};
      const before=evaluate('projectJson()'),html=evaluate('htmlExport()');choose(heading);
      test(mode+' proposed wording starts from actual site content without creating a saved proposal',()=>d.getElementById('ia-draft').value===previewDoc().getElementById('hero-title').textContent && !d.getElementById('ia-has-draft').checked && rows().find(node=>node.id===heading.id).draft===null && evaluate('projectJson()')===before && evaluate('htmlExport()')===html);
      test(mode+' fresh notes relate to this site and selected item without inventing an owner',()=>d.getElementById('ia-notes').value.includes(evaluate('state.project')) && d.getElementById('ia-notes').value.includes('Home / Hero / Heading') && d.getElementById('ia-notes').value.includes('Owner: Unassigned.') && d.getElementById('ia-notes').value.includes(mode==='basic'?'Basic HTML and CSS':'Advanced Web Design Field Guide'));
      test(mode+' planning has no example panel and review is named for its current role',()=>!d.getElementById('ia-example') && !d.querySelector('.ia-plan-example') && d.querySelector('#architecture-saved-review > summary').textContent==='Review the Content Plan');
      for(const kind of model.types){input('ia-type',kind,'change');test(mode+' '+kind+' keeps readiness visible as an item property',()=>d.getElementById('ia-status').closest('#ia-properties') && !d.getElementById('ia-content-plan').contains(d.getElementById('ia-status')) && d.getElementById('ia-status').form===d.getElementById('ia-form') && d.getElementById('ia-status').getBoundingClientRect().height>=44 && d.getElementById('ia-status').value==='present');}
      d.getElementById('ia-discard').click();input('ia-status','needs-content','change');input('ia-notes','Purpose: our site introduction. Owner: site team. Next action: review.');d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' readiness and site notes save while seeded wording remains an uncommitted proposal',()=>rows().find(node=>node.id===heading.id).status==='needs-content' && rows().find(node=>node.id===heading.id).draft===null && d.getElementById('ia-draft').value===heading.value);
      const project=JSON.parse(evaluate('projectJson()'));project.designProcess.contentPlan[mode].find(node=>node.id===heading.id).notes='';project.designProcess.contentPlan[mode].find(node=>node.id===heading.id).draft='';w.importConfig(project);await wait();choose(rows().find(node=>node.id===heading.id));
      test(mode+' explicit empty saved notes and wording survive imports instead of being replaced by defaults',()=>d.getElementById('ia-notes').value==='' && d.getElementById('ia-draft').value==='' && d.getElementById('ia-has-draft').checked && d.getElementById('ia-status').value==='needs-content' && d.getElementById('ia-notes').placeholder.includes(evaluate('state.project')));
      for(const width of [320,390,1440]){app.style.width=width+'px';await wait();const browser=d.querySelector('.ia-browser'),form=d.getElementById('ia-form'),intro=browser.querySelector(':scope > .ia-browser-heading'),b=browser.getBoundingClientRect(),f=form.getBoundingClientRect(),status=d.getElementById('ia-status').getBoundingClientRect();test(mode+' browser owns its introduction and properties start at the column top at '+width+'px',()=>intro===browser.firstElementChild && intro.querySelector('h3').textContent==='Content structure' && intro.querySelector('p').textContent.includes('Choose an item') && (d.getElementById('architecture-workspace').clientWidth<736?f.top>=b.bottom-1:Math.abs(f.top-b.top)<=1) && status.top<d.getElementById('ia-website-content').getBoundingClientRect().top && d.documentElement.scrollWidth<=w.innerWidth+1);}
      app.style.width='1440px';reset();await wait();
    }
  }
  // Properties stay visible; tree actions and the external Save control share the selection.
  {
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const properties=d.getElementById('ia-properties'),plan=d.getElementById('ia-content-plan'),planSummary=plan.querySelector('summary'),form=d.getElementById('ia-form'),save=d.querySelector('.ia-save-area'),browser=d.querySelector('.ia-browser');
      test(mode+' selected content properties are visible without a disclosure or local step number',()=>properties.tagName==='SECTION' && !properties.querySelector(':scope > summary') && d.getElementById('ia-editor-heading').textContent==='Selected content properties' && d.getElementById('ia-label').getBoundingClientRect().height>=44 && !plan.open && planSummary.textContent==='Develop the content plan');
      test(mode+' planning leads the workspace and its external fields belong to the selected content form',()=>plan.parentElement===d.getElementById('architecture-workspace') && plan.previousElementSibling.tagName==='HEADER' && plan.nextElementSibling===d.getElementById('ia-content-editor') && !form.contains(plan) && [...plan.querySelectorAll('input,textarea,select,button')].every(control=>control.form===form) && d.getElementById('ia-plan-selection').textContent.includes(d.getElementById('ia-selected-name').textContent));
      const before=evaluate('projectJson()');
      d.querySelector('[data-content-id]').click();
      test(mode+' selecting content focuses the visible name field and identifies the branch action target',()=>d.activeElement===d.getElementById('ia-label') && d.getElementById('ia-branch-selection').textContent==='Selected: '+d.getElementById('ia-selected-name').textContent && browser.contains(d.querySelector('.ia-branch-tools')));
      planSummary.click();
      test(mode+' expanding content planning keeps properties visible and does not change project data',()=>plan.open && d.getElementById('ia-label').getBoundingClientRect().height>=44 && evaluate('projectJson()')===before);
      input('ia-draft','A proposal retained while collapsed');planSummary.click();
      test(mode+' collapsing planning retains unsaved values with external Save and Discard available',()=>!plan.open && d.getElementById('ia-draft').value==='A proposal retained while collapsed' && !d.getElementById('ia-discard').disabled && !form.contains(save) && d.getElementById('ia-save').form===form && evaluate('projectJson()')===before);
      d.getElementById('ia-save').click();await wait();
      test(mode+' external Save submits the selected form and retains the saved proposal',()=>!plan.open && w.DSStudio.contentArchitecture.nodes().some(node=>node.draft==='A proposal retained while collapsed') && d.getElementById('ia-discard').disabled && d.getElementById('architecture-saved-review').open && d.activeElement===d.getElementById('ia-save'));
      d.getElementById('architecture-saved-review').open=false;d.getElementById('ia-undo').click();await wait();
      test(mode+' content Undo reveals feedback in the collapsed Review the Content Plan section',()=>d.getElementById('architecture-saved-review').open && d.getElementById('ia-status-message').textContent.includes('undone'));
      addContent('top');
      test(mode+' adding an item focuses its always-visible required name',()=>!plan.open && d.activeElement===d.getElementById('ia-label'));
      d.getElementById('ia-save').click();
      test(mode+' external Save validates and focuses an empty required name',()=>d.activeElement===d.getElementById('ia-label') && !d.getElementById('ia-label').validity.valid);
      d.dispatchEvent(new w.Event('dss:imported'));await wait();
      test(mode+' importing retains visible properties and resets only the planning disclosure',()=>!plan.open && properties.tagName==='SECTION' && d.getElementById('ia-label').getBoundingClientRect().height>=44);
      for(const width of [320,390,1440]) {
        app.style.width=width+'px';await wait();
        const review=d.getElementById('architecture-saved-review');review.open=true;plan.open=true;const s=save.getBoundingClientRect(),b=browser.getBoundingClientRect(),branch=browser.querySelector('.ia-branch-tools').getBoundingClientRect();
        test(mode+' Save and review sits below the left content browser at '+width+'px',()=>review.querySelector(':scope > summary').textContent==='Review the Content Plan' && !review.contains(save) && browser.lastElementChild===save && review.lastElementChild.matches('[data-process-artifact="ia"]') && review.lastElementChild.previousElementSibling===d.getElementById('architecture-review-guidance') && d.querySelectorAll('#process-ia .process-ia-guidance').length===1 && d.getElementById('architecture-review-guidance').querySelector('h4').textContent==='Information architecture and sitemap: different jobs' && d.getElementById('ia-content-editor').contains(save) && s.top>=branch.bottom-1 && s.left>=b.left && s.right<=b.right+1 && d.documentElement.scrollWidth<=w.innerWidth+1 && [...save.querySelectorAll('button')].every(el=>el.getBoundingClientRect().height>=44) && plan.getBoundingClientRect().top<d.getElementById('ia-content-editor').getBoundingClientRect().top && [...plan.querySelectorAll('textarea,select,input:not([type=checkbox])')].every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.left>=0 && box.right<=w.innerWidth+1;}));
      }
    }
    app.style.width='1440px';reset();await wait();
  }

  // Architecture uses one centre editor, with draft protection across navigation.
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
    const workspace=d.getElementById('architecture-workspace'),form=d.getElementById('ia-form'),outline=d.getElementById('ia-outline');
    test(mode+' Architecture has one centre editor and a concise wizard step',()=>workspace.closest('#process-ia') && workspace.contains(form) && workspace.contains(outline) && workspace.contains(d.getElementById('section-sitemap-editor')) && !d.querySelector('[data-journey-pane="1"] input, [data-journey-pane="1"] select, [data-journey-pane="1"] textarea') && d.querySelectorAll('#ia-form').length===1);
    d.getElementById('open-architecture-workspace').click();
    test(mode+' workspace shortcut opens its lesson and focuses the workspace heading',()=>d.getElementById('process-ia').open && d.activeElement.id==='architecture-workspace-title');
    const selected=d.getElementById('ia-selected-name').textContent,before=evaluate('projectJson()');
    input('ia-notes','Keep this unsaved planning note');d.getElementById('architecture-saved-review').open=false;
    const other=[...d.querySelectorAll('[data-content-id]')].find(el=>el.getAttribute('aria-pressed')==='false');other.click();
    test(mode+' selecting another item preserves unsaved content and saved project data',()=>d.getElementById('ia-selected-name').textContent===selected && d.getElementById('ia-notes').value==='Keep this unsaved planning note' && d.activeElement.id==='ia-save' && d.getElementById('architecture-saved-review').open && evaluate('projectJson()')===before && d.getElementById('ia-status-message').textContent.includes('Save or discard'));
    for(const id of ['ia-add','ia-delete','ia-up','ia-undo','ia-restore'])d.getElementById(id).click();
    test(mode+' branch actions and creation cannot replace an unsaved form',()=>d.getElementById('ia-selected-name').textContent===selected && d.getElementById('ia-notes').value==='Keep this unsaved planning note' && evaluate('projectJson()')===before);
    d.querySelector('#section-sitemap-choices input:not(:disabled)').click();await wait();
    test(mode+' sitemap changes preserve unsaved content form values',()=>d.getElementById('ia-notes').value==='Keep this unsaved planning note' && !d.getElementById('ia-discard').disabled);
    w.dssShowWizardStep(2);w.dssShowWizardStep(1);evaluate('apply()');
    test(mode+' returning to Architecture preserves unsaved edits',()=>d.getElementById('ia-notes').value==='Keep this unsaved planning note' && !d.getElementById('ia-discard').disabled);
    d.getElementById('ia-discard').click();d.querySelector('[data-content-id="'+other.dataset.contentId+'"]').click();
    test(mode+' discarding allows selection to continue',()=>d.getElementById('ia-selected-name').textContent!==selected && d.getElementById('ia-notes').value!=='Keep this unsaved planning note');
    for(const width of [320,390,1440]) {
      app.style.width=width+'px';await wait();
      const browser=d.querySelector('.ia-browser').getBoundingClientRect(),editor=form.getBoundingClientRect();
      test(mode+' Architecture workspace stacks or splits to fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && (workspace.clientWidth<736?editor.top>=browser.bottom-1:editor.left>=browser.right-1) && workspace.contains(form) && d.querySelectorAll('#ia-form').length===1);
    }
    app.style.width='1440px';
  }
  reset();await wait();
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
    const before=evaluate('projectJson()'),exported=evaluate('htmlExport()'),sitemap=d.getElementById('architecture-sitemap'),review=d.getElementById('architecture-saved-review');
    sitemap.open=false;review.open=false;
    test(mode+' tree creation has one Add action with three placement choices',()=>d.querySelectorAll('.ia-add-controls button').length===1 && [...d.getElementById('ia-add-placement').options].map(option=>option.value).join(',')==='inside,beside,top' && d.querySelector('.ia-branch-tools').contains(d.getElementById('ia-expand')) && d.querySelector('.ia-branch-tools').contains(d.getElementById('ia-collapse')));
    test(mode+' optional section reference keeps the essential properties visible',()=>!d.getElementById('ia-related-section').open && ['ia-actual','ia-label','ia-type','ia-parent'].every(id=>d.getElementById(id).getBoundingClientRect().height>=44));
    input('ia-notes','Unsaved note while reviewing navigation');
    d.getElementById('architecture-view-sitemap').click();
    test(mode+' visitor sitemap shortcut opens the sole live map without discarding content edits',()=>sitemap.open && d.activeElement===sitemap.querySelector(':scope > summary') && d.getElementById('ia-notes').value==='Unsaved note while reviewing navigation' && evaluate('projectJson()')===before && evaluate('htmlExport()')===exported && d.querySelectorAll('#process-ia .process-sitemap-preview').length===1);
    review.open=true;evaluate('apply()');
    test(mode+' saved review remains optional and stable across unrelated rendering',()=>review.open && review.contains(d.querySelector('#process-ia .ia-content-map')) && d.getElementById('ia-notes').value==='Unsaved note while reviewing navigation' && evaluate('projectJson()')===before);
    d.getElementById('ia-discard').click();
    const link=w.DSStudio.contentArchitecture.nodes().find(node=>node.type==='link');
    const button=d.querySelector('[data-content-id="'+link.id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();
    test(mode+' selecting a link reveals its destination reference',()=>d.getElementById('ia-related-section').open && d.getElementById('ia-type').value==='link');
  }
  reset();await wait();

  // Replacement boundaries must clear private dirty/Undo state even when the
  // incoming file contains the same saved model as the current project.
  for(const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();w.importConfig({sampleMode:mode});w.dssShowWizardStep(1,false);await wait();
    input('jProject',mode+' content-tree fixture');d.getElementById('jSaveLocal').click();
    const model=w.DSStudio.contentArchitecture,heading=model.nodes().find(node=>node.sourceKey==='id:hero-title');
    const choose=()=>{const button=d.querySelector('[data-content-id="'+heading.id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    choose();input('ia-draft','Saved '+mode+' proposal');input('ia-notes','Owner: tutor. Next action: review.');
    d.getElementById('ia-save').click();await wait();
    const saved=evaluate('projectJson()'),library=w.localStorage.getItem('dss-v27-projects'),draftEditor=d.getElementById('ia-draft');
    input('ia-draft','Unsaved wording that must not survive import');
    await importFile(saved);await wait();
    test(mode+' identical JSON file import clears dirty state and incompatible Undo history',()=>
      !w.DSStudio.contentEditor.isDirty() && d.getElementById('ia-undo').disabled && evaluate('projectJson()')===saved && w.localStorage.getItem('dss-v27-projects')===library);
    choose();
    test(mode+' file import restores the proposal in the original editor and retains actual website text',()=>
      d.getElementById('ia-draft')===draftEditor && draftEditor.value==='Saved '+mode+' proposal' && d.getElementById('ia-discard').disabled && d.getElementById('ia-actual').value===heading.value && previewDoc().getElementById('hero-title').textContent===heading.value);
    input('ia-notes','Changed after file import');d.getElementById('ia-save').click();await wait();
    test(mode+' saving imported content changes the current model without autosaving into the old local project',()=>
      model.nodes().find(node=>node.id===heading.id).notes==='Changed after file import' && !d.getElementById('ia-undo').disabled && w.localStorage.getItem('dss-v27-projects')===library);
    d.getElementById('ia-undo').click();await wait();
    test(mode+' Undo after an imported edit returns to the imported snapshot',()=>evaluate('projectJson()')===saved && d.getElementById('ia-undo').disabled && w.localStorage.getItem('dss-v27-projects')===library);
    choose();input('ia-draft','Unsaved proposal before New');d.getElementById('jNewLocal').click();await wait();
    test(mode+' New clears unsaved content and history while preserving the saved library',()=>
      !w.DSStudio.contentEditor.isDirty() && d.getElementById('ia-undo').disabled && d.getElementById('ia-discard').disabled &&
      evaluate('state.sampleMode==="basic" && state.designProcess.contentPlan.basic===null && state.designProcess.contentPlan.advanced===null') && w.localStorage.getItem('dss-v27-projects')===library);
  }
  test('No content-tree JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Content-tree harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
