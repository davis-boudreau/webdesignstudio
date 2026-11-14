"""Independent sitemap editor, source selection and compatibility checks.

Run: python scripts/sitemap_review.py. Uses its own isolated app/profile and
shared Chrome runner; no integration-harness imports or global replacements.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Sitemap review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Sitemap review: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const revealArchitecture=()=>d.querySelectorAll('#architecture-sitemap,#architecture-saved-review,#architecture-sitemap-advanced,#architecture-advanced,#sitemap-choices details,#section-sitemap-choices details,#sitemap-editor details').forEach(el=>el.open=true);
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
  test('Independent sitemap startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
    test(mode+' sitemap renders its intended depth and preserves the complete Architecture plan', () => {
      const page=previewDoc(), links=[...page.querySelectorAll('#sitemap a')], ids=new Set(links.map(a=>a.hash.slice(1)));
      const expected=w.DSStudio.process.samplePages(mode);
      const fullCount=expected.split('\n').length, topCount=w.DSStudio.process.hierarchy(expected).length;
      return d.getElementById('plan-pages').value===expected && links.length===w.DSStudio.sectionSitemap.nodes().length && !page.querySelector('#sitemap .sitemap-planned') && links.every(a=>page.querySelectorAll('[id="'+a.hash.slice(1)+'"]').length===1) && [...page.querySelectorAll('main > section')].every(el=>el.id && ids.has(el.id)) && d.querySelectorAll('#process-ia .process-map li').length===fullCount && (mode!=='basic'||page.querySelectorAll('#sitemap ul ul a').length===8) && evaluate('htmlExport()').includes('id="sitemap"');
    });
  }
  d.getElementById('process-ia').open=true;
  const planBeforeBasicView=evaluate('state.designProcess.pages');
  for(const theme of ['light','dark']) {
    input('jTheme',theme);
    for(const width of [320,768,1440]) {
      app.style.width=width+'px'; await wait();
      test(theme+' Basic plan aligns parent groups and related children at '+width+'px', () => {
        const map=d.querySelector('#process-ia .process-map--basic'), list=map.querySelector(':scope > ul'), groups=[...list.children];
        const gap=parseFloat(w.getComputedStyle(list).columnGap), bounds=list.getBoundingClientRect(), boxes=groups.map(group=>group.getBoundingClientRect());
        const inline=list.clientWidth>=groups.length*144+(groups.length-1)*gap;
        return groups.map(group=>group.querySelector('strong').textContent).join(',')==='Home,Components,Layouts,Forms,Footer' && w.getComputedStyle(list).display==='flex' && boxes.every(box=>box.left>=bounds.left-1 && box.right<=bounds.right+1) && (!inline||boxes.every(box=>Math.abs(box.top-boxes[0].top)<1)) && groups.every(group=>{
          const children=group.querySelector('ul'), title=group.querySelector('strong').getBoundingClientRect();
          return !children||(children.getBoundingClientRect().top>=title.bottom && Math.abs(children.getBoundingClientRect().left-title.left)<1);
        }) && map.querySelectorAll('ul ul > li').length===w.DSStudio.process.entries().filter(node=>node.depth>1).length && d.documentElement.scrollWidth<=width+1 && evaluate('state.designProcess.pages')===planBeforeBasicView && d.getElementById('plan-pages').value.includes('Forms') && d.getElementById('plan-pages').value.includes('Footer') && previewDoc().querySelector('#signup') && previewDoc().querySelector('footer');
      });
    }
  }
  app.style.width='1440px'; input('jTheme','light');
  input('plan-pages','Home\nSIGN-UP\n footer \nFlexbox > Forms'); await wait();
  test('Basic IA shows Forms/Footer aliases as part of its full model', () => [...d.querySelectorAll('#process-ia .process-map > ul > li > strong')].map(el=>el.textContent).join(',')==='Home,SIGN-UP,footer,Flexbox' && d.querySelector('#process-ia .process-map ul ul li').textContent==='Forms' && evaluate('state.designProcess.pages')==='Home\nSIGN-UP\n footer \nFlexbox > Forms');
  input('plan-pages','Forms\nFooter'); await wait();
  test('Basic IA retains Forms and Footer even when not sitemap destinations', () => d.querySelectorAll('#process-ia .process-map > ul > li').length===2 && d.querySelector('#process-ia .process-map').textContent.includes('sitemap destination outline') && evaluate('state.designProcess.pages')==='Forms\nFooter');
  input('plan-pages',w.DSStudio.process.samplePages('basic')); await wait();
  test('Basic footer contains only Components, Layouts and Forms while the complete plan is preserved', () => {
    const full=new w.DOMParser().parseFromString(evaluate('DSStudio.process.sitemapHtml()'),'text/html');
    return previewDoc().querySelectorAll('#sitemap a').length===14 && full.querySelectorAll('a').length===14 && full.querySelector('ul ul') && [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li > a')].map(a=>a.textContent).join(',')==='Components,Layouts,Forms' && previewDoc().querySelectorAll('#sitemap ul ul a').length===11 && [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].every((group,i)=>Boolean(group.querySelector('ul')));
  });
  input('plan-pages','Home > Forms\nFuture > Flexbox\nGrid & lists'); await wait();
  test('Basic expanded sitemap keeps known children under their parent and never promotes orphan children', () => [...previewDoc().querySelectorAll('#sitemap a')].map(a=>a.hash).join(',')==='#lists' && !previewDoc().querySelector('#sitemap ul ul') && evaluate('state.designProcess.pages')==='Home > Forms\nFuture > Flexbox\nGrid & lists' && d.querySelectorAll('#process-ia .process-map li').length===5);
  input('plan-pages','Flexbox > Semantic HTML\nFlexbox > Unbuilt topic\nGrid & lists > Ordered lists'); await wait();
  test('Basic expanded sitemap includes linked children and safely omits unlinked child labels', () => previewDoc().querySelectorAll('#sitemap a').length===4 && previewDoc().querySelectorAll('#sitemap ul ul a').length===2 && !previewDoc().querySelector('#sitemap .sitemap-planned') && !previewDoc().querySelector('#sitemap').textContent.includes('Unbuilt topic') && evaluate('state.designProcess.pages').includes('Unbuilt topic'));
  input('plan-pages','Home > Enquiry form\nFooter > Common questions\nServices > Website design'); await wait();
  test('Home and Footer groups and their children are omitted from custom footer navigation', () => [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].every(group=>group.querySelector('a').hash==='#features' && group.querySelector('ul')) && previewDoc().querySelectorAll('#sitemap a').length===2 && evaluate('state.designProcess.pages').includes('Footer > Common questions'));
  const previousMockPlan="Home\nServices\nServices > Website design\nServices > Content planning\nServices > Responsive websites\nResources\nResources > Project checklist\nResources > How we work\nResources > Useful terms\nContact\nContact > Enquiry form\nContact > Common questions\nFooter";
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousMockPlan}})+')'); await wait();
  test('Previous mock-site inventory resolves to the component scope without mutating saved data', () => evaluate('state.designProcess.pages')===previousMockPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===12 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  const previousTutorialPlan='Hero\nFlexbox\nFlexbox > Semantic HTML\nFlexbox > Flexbox layout\nFlexbox > Responsive navigation\nGrid & lists\nGrid & lists > Unordered lists\nGrid & lists > Ordered lists\nGrid & lists > Description lists\nForms\nFooter';
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousTutorialPlan}})+')'); await wait();
  test('The previous complete tutorial plan resolves to the mock inventory without overwriting saved data', () => evaluate('state.designProcess.pages')===previousTutorialPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===12 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  const previousBasicPlan='Home\nWhat you can learn\nWhat you can learn > Give content meaning\nWhat you can learn > Let the layout adapt\nWhat you can learn > Make the basics easy\nLists\nLists > What to include\nLists > A simple workflow\nLists > Useful terms\nSign up\nFooter';
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousBasicPlan}})+')'); await wait();
  test('Old complete Basic inventories resolve to tutorial labels without changing stored planning data', () => evaluate('state.designProcess.pages')===previousBasicPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && !previewDoc().querySelector('#sitemap .sitemap-planned') && previewDoc().querySelector('#sitemap a[href="#features"]').textContent==='Components / Flexbox');
  input('plan-pages','Home\nWhat you can learn > Give content meaning\nLists > What to include\nSign up'); await wait();
  test('Custom legacy Basic parent and child labels retain real destinations', () => previewDoc().querySelectorAll('#sitemap a').length===5 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  input('plan-pages','Home\nFeatures\nLists\nSign up\nFuture > Account'); await wait();
  test('Basic footer sitemap filters Architecture to linked parent and child entries', () => {
    const map=previewDoc().querySelector('#sitemap .sitemap-list');
    return map.children.length===3 && map.querySelectorAll('a').length===3 && !map.querySelector('ul, span, .sitemap-planned') && d.querySelector('#process-ia .process-map').textContent.includes('Account') && [...map.querySelectorAll('a')].every(a=>previewDoc().getElementById(a.hash.slice(1))) && previewDoc().querySelector('footer #sitemap');
  });
  input('plan-pages','Home\nLearn > Articles\nSign up'); await wait();
  test('Architecture edits update the centre map, Basic footer and downloadable HTML together', () => d.querySelector('#process-ia .process-map').textContent.includes('Learn') && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && !previewDoc().querySelector('#sitemap a[href="#features"]') && !evaluate('htmlExport()').includes('Articles') && evaluate('projectJson()').includes('Articles'));
  const customSitemap=d.getElementById('plan-pages').value, customSitemapExport=evaluate('projectJson()');
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Custom IA survives mode changes while unlinked sitemap entries remain hidden', () => d.getElementById('plan-pages').value===customSitemap && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && d.querySelector('#process-ia .process-map').textContent.includes('Articles'));
  evaluate('importConfig('+customSitemapExport+')'); await wait();
  test('Custom sitemap survives JSON round trip while Basic omits unlinked entries', () => d.getElementById('plan-pages').value===customSitemap && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && previewDoc().querySelectorAll('#sitemap a').length===1);
  input('plan-pages','<img src=x onerror=alert(1)> > <script>bad<\/script>'); await wait();
  test('Sitemap labels cannot inject HTML or arbitrary destinations', () => {
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !page.querySelector('#sitemap img, #sitemap script, #sitemap a') && !page.querySelector('#sitemap').textContent.includes('onerror=alert(1)') && page.querySelector('#sitemap').textContent.includes('No sitemap destinations selected') && d.getElementById('plan-pages').validationMessage.includes('three information levels') && !d.querySelector('#process-ia .process-map img, #process-ia .process-map script');
  });
  input('plan-pages',''); await wait();
  test('Empty Architecture has an honest empty sitemap and keeps real footer navigation', () => previewDoc().querySelector('#sitemap').textContent.includes('No sitemap destinations selected') && previewDoc().querySelector('footer .footer-brand[href="#home"]'));
  d.getElementById('plan-use-sample').click(); await wait();
  test('Use complete sitemap restores the full Basic mock-site plan and expanded footer links', () => d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===14 && d.querySelectorAll('#process-ia .process-map li').length===w.DSStudio.process.samplePages('basic').split('\n').length);
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
    input('plan-pages','Home\nCustom > Future page'); await wait();
    d.getElementById('process-ia').open=false;
    d.getElementById('plan-use-sample').click(); await wait();
    test(mode+' sitemap button restores stored/editor/centre/preview/inspector content and gives visible feedback', () => {
      const expected=w.DSStudio.process.samplePages(mode), parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      return evaluate('state.designProcess.pages')===expected && d.getElementById('plan-pages').value===expected && d.getElementById('process-ia').open && !d.querySelector('#process-ia .process-map').textContent.includes('Future page') && !previewDoc().querySelector('#sitemap .sitemap-planned') && previewDoc().querySelector('#sitemap').innerHTML===parsed.querySelector('#sitemap').innerHTML && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()') && d.getElementById('plan-sample-status').textContent.includes('destination outline applied:');
    });
    const restored=evaluate('projectJson()');
    d.getElementById('plan-use-sample').click(); await wait();
    test(mode+' repeated sitemap clicks confirm an already complete map without changing data', () => evaluate('projectJson()')===restored && d.getElementById('plan-sample-status').textContent.includes('already complete'));
    input('plan-pages','Home\nMy next page'); await wait();
    test(mode+' editing a restored sitemap clears outdated confirmation', () => d.getElementById('plan-sample-status').textContent==='');
    d.getElementById('plan-use-sample').click(); await wait();
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  d.getElementById('dockModeBasic').click(); await wait();
  w.dssShowWizardStep(1);
  const saveSitemap = async (label,parent='',target='planned') => {
    d.getElementById('sitemap-new').click();
    d.getElementById('sitemap-label').value=label;
    d.getElementById('sitemap-parent').value=parent;
    d.getElementById('sitemap-target').value=target;
    d.getElementById('sitemap-form').requestSubmit(); await wait();
  };
  // Ordinary edits must retain visibility in project data, UI and generated output.
  for (const mode of ['basic','advanced']) for (const visible of [false,true]) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    const destination=w.DSStudio.process.inventory(mode).find(([,id])=>!['home','footer','top'].includes(id))[1];
    evaluate('state.designProcess=DSStudio.process.normalize('+JSON.stringify({
      pages:'Overview\nOverview > Linked entry\nOverview > Second entry\nFuture page',
      pageLinks:{[mode]:{'Overview':destination,'Linked entry':destination,'Second entry':destination,'Future page':''}},
      showPlanned:visible
    })+');apply()');await wait();
    w.dssShowWizardStep(1);
    const initial=evaluate('JSON.stringify(state.designProcess)');
    const visibilityMatches=()=>evaluate('state.designProcess.showPlanned')===visible &&
      d.getElementById('sitemap-planned').checked===visible &&
      JSON.parse(evaluate('projectJson()')).designProcess.showPlanned===visible &&
      Boolean(previewDoc().querySelector('#sitemap .sitemap-planned'))===visible &&
      Boolean(new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap .sitemap-planned'))===visible;
    const undoSitemap=async action=>{
      d.getElementById('sitemap-undo').click();await wait();
      test(mode+' '+visible+' Undo restores '+action+' and visibility',()=>evaluate('JSON.stringify(state.designProcess)')===initial && visibilityMatches() && d.getElementById('sitemap-undo').disabled);
    };
    input('sitemap-items','0:0','change');
    d.getElementById('sitemap-label').value='Renamed entry';d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' '+visible+' rename preserves visibility and destination',()=>visibilityMatches() && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Renamed entry' && a.hash==='#'+destination));
    await undoSitemap('rename');
    await saveSitemap('New planned page');
    test(mode+' '+visible+' creation preserves visibility',()=>visibilityMatches() && evaluate('state.designProcess.pages').includes('New planned page') && previewDoc().querySelector('#sitemap').textContent.includes('New planned page')===visible);
    await undoSitemap('creation');
    input('sitemap-items','0:0','change');d.getElementById('sitemap-delete').click();await wait();
    test(mode+' '+visible+' deletion preserves visibility',()=>visibilityMatches() && !evaluate('state.designProcess.pages').includes('Linked entry') && !previewDoc().querySelector('#sitemap').textContent.includes('Linked entry'));
    await undoSitemap('deletion');
    input('sitemap-items','0:0','change');d.getElementById('sitemap-down').click();await wait();
    test(mode+' '+visible+' reorder preserves visibility and changes order',()=>visibilityMatches() && w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[0][1][1]==='Linked entry');
    await undoSitemap('reorder');
    d.getElementById('sitemap-planned').click();await wait();
    test(mode+' '+visible+' checkbox explicitly changes visibility',()=>evaluate('state.designProcess.showPlanned')===!visible && d.getElementById('sitemap-planned').checked===!visible);
    await undoSitemap('visibility toggle');
  }
  reset();d.getElementById('dockModeBasic').click();await wait();w.dssShowWizardStep(1);
  d.getElementById('sitemap-planned').click();await wait();
  await saveSitemap('Our team');
  test('Sitemap CRUD creates a planned group visible in Basic preview and export',()=>previewDoc().querySelector('#sitemap').textContent.includes('Our team') && previewDoc().querySelector('#sitemap .sitemap-planned') && evaluate('htmlExport()').includes('Our team') && d.querySelector('#process-ia').textContent.includes('Our team'));
  const teamIndex=w.DSStudio.process.hierarchy(evaluate('DSStudio.process.currentPlan().pages')).findIndex(([name])=>name==='Our team');
  await saveSitemap('Meet the mentor',String(teamIndex),'basic-layout');
  test('Sitemap CRUD creates a relationship with a safe existing destination',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(group=>group.textContent.includes('Our team') && group.querySelector('ul a[href="#basic-layout"]')?.textContent==='Meet the mentor'));
  d.getElementById('sitemap-label').value='Meet Alex';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Sitemap CRUD renames labels while preserving destinations and inspector output',()=>previewDoc().querySelector('#sitemap a[href="#basic-layout"]').textContent!=='Meet the mentor' && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Meet Alex'&&a.hash==='#basic-layout') && !evaluate('htmlExport()').includes('Meet the mentor') && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()'));
  d.getElementById('sitemap-parent').value='1';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Sitemap CRUD reparents a child under Components',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(group=>group.querySelector(':scope > a')?.textContent==='Components' && [...group.querySelectorAll('ul a')].some(a=>a.textContent==='Meet Alex')));
  d.getElementById('sitemap-up').click();await wait();
  test('Sitemap CRUD reorders children in the rendered footer',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[1][1].at(-2)==='Meet Alex');
  const beforeDelete=evaluate('JSON.stringify(state.designProcess)');
  d.getElementById('sitemap-delete').click();await wait();
  test('Sitemap CRUD deletes an entry',()=>!evaluate('htmlExport()').includes('Meet Alex'));
  d.getElementById('sitemap-undo').click();await wait();
  test('Sitemap CRUD undo restores relationships and destination mapping',()=>evaluate('JSON.stringify(state.designProcess)')===beforeDelete && evaluate('htmlExport()').includes('Meet Alex'));
  const customBuilder=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(customBuilder)+')');await wait();
  test('Sitemap relationships and destination mapping survive JSON round trip',()=>evaluate('htmlExport()').includes('Meet Alex') && previewDoc().querySelector('#sitemap .sitemap-planned') && d.getElementById('sitemap-undo').disabled);
  await saveSitemap('<img src=x onerror=alert(1)>');
  test('Sitemap CRUD rejects relationship delimiters without injecting markup',()=>!previewDoc().querySelector('#sitemap img') && d.getElementById('sitemap-status').textContent.includes('unique label'));
  const maliciousLinks={pageLinks:{basic:{Bad:'javascript:alert(1)',Safe:'basic-layout',Planned:''},advanced:{Bad:'basic-layout'}},showPlanned:true};
  test('Imported sitemap targets accept only fixed IDs for the corresponding mode',()=>{
    const normalized=w.DSStudio.process.normalize(maliciousLinks);return !Object.hasOwn(normalized.pageLinks.basic,'Bad') && normalized.pageLinks.basic.Safe==='basic-layout' && normalized.pageLinks.basic.Planned==='' && !Object.hasOwn(normalized.pageLinks.advanced,'Bad');
  });
  d.getElementById('plan-use-sample').click();await wait();
  test('Complete sitemap restores default labels, link mappings and visibility',()=>!evaluate('state.designProcess.showPlanned') && Object.keys(evaluate('state.designProcess.pageLinks.basic')).length===0 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  input('sitemap-items','1:1','change');
  d.getElementById('sitemap-label').value='Mentor profile';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Renaming a child retains its sibling order and existing destination',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[1][1][1]==='Mentor profile' && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Mentor profile'&&a.hash==='#basic-layout'));
  input('plan-pages','Home\nComponents');await wait();
  test('External text edits invalidate sitemap undo instead of restoring stale data',()=>d.getElementById('sitemap-undo').disabled);
  input('plan-pages',Array.from({length:64},(_,i)=>'Planned '+i).join('\n'));await wait();
  await saveSitemap('Too many');await saveSitemap('Still too many');
  test('Sitemap CRUD enforces entry limits and remains usable after repeated rejections',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages')).length===64 && d.getElementById('sitemap-status').textContent.includes('64 entries'));
  d.getElementById('plan-use-sample').click();await wait();
  d.getElementById('sitemap-planned').click();await wait();
  await saveSitemap('Research <notes');
  test('Sitemap labels render as escaped text without creating page sections',()=>previewDoc().querySelector('#sitemap').textContent.includes('Research <notes') && !previewDoc().querySelector('#sitemap notes') && previewDoc().querySelectorAll('main > section').length===4);
  for (const width of [320,1440]) {
    app.style.width=width+'px';await wait();
    test('Custom Sitemap outline and properties fit at '+width+'px',()=>[...d.querySelectorAll('#sitemap-editor select:not([hidden]), #sitemap-editor input:not([type="checkbox"]), #sitemap-editor button')].every(el=>{const box=el.getBoundingClientRect(),parent=d.getElementById('sitemap-editor').getBoundingClientRect();return box.width>0 && box.left>=parent.left-1 && box.right<=parent.right+1;}));
  }
  d.getElementById('plan-use-sample').click();await wait();
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  evaluate("state.designProcess.pageLinks.advanced={'Advanced custom':'about'};state.designProcess.pageLinks.basic={'Basic custom':'features'};apply()");
  d.getElementById('dockModeBasic').click();d.getElementById('plan-use-sample').click();
  test('Restoring Basic sitemap preserves Advanced link mappings',()=>evaluate("state.designProcess.pageLinks.advanced['Advanced custom']") ==='about' && evaluate('Object.keys(state.designProcess.pageLinks.basic).length')===0);
  evaluate("state.designProcess.pageLinks.basic={'Basic custom':'features'};apply()");
  d.getElementById('dockModeAdvanced').click();d.getElementById('plan-use-sample').click();
  test('Restoring Advanced sitemap preserves Basic link mappings',()=>evaluate("state.designProcess.pageLinks.basic['Basic custom']") ==='features' && evaluate('Object.keys(state.designProcess.pageLinks.advanced).length')===0);
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  // Full information architecture and independently selected visitor sitemap.
  const iaNodes=()=>{revealDestinationPlan();return w.DSStudio.process.entries();};
  const iaNode=label=>iaNodes().find(node=>node.label===label);
  const iaChoice=label=>[...d.querySelectorAll('#sitemap-choices input')].find(input=>input.dataset.iaId===iaNode(label)?.id);
  const iaSelect=label=>{const option=[...d.getElementById('sitemap-items').options].find(option=>option.textContent.replace(/^\s*—\s*/,'').trim()===label);input('sitemap-items',option.value,'change');};
  const iaFooterHas=label=>[...previewDoc().querySelectorAll('#sitemap a, #sitemap span')].some(el=>el.firstChild?.textContent===label);
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    const parent=mode==='basic'?'Components':'Lessons',child=mode==='basic'?'Content card':'Brief lesson';
    const target=mode==='basic'?'basic-structure':'lesson-brief';
    test(mode+' IA shows every parent and child including sitemap exclusions',()=>d.querySelectorAll('#process-ia .process-map li').length===iaNodes().length && d.querySelector('#process-ia .process-map').textContent.includes('Footer') && d.querySelector('#process-ia .process-map').textContent.includes('Home') && d.querySelectorAll('#sitemap-choices input').length===iaNodes().length);
    test(mode+' lesson distinguishes IA from the visitor sitemap and cites NN/g',()=>d.querySelector('#process-ia .process-ia-guidance a').href==='https://www.nngroup.com/articles/information-architecture-sitemaps/' && d.querySelector('#process-ia .process-ia-guidance').textContent.includes('not remove those hours') && JSON.stringify([...d.querySelectorAll('#process-ia .process-sitemap-preview a')].map(a=>[a.textContent,a.dataset.sitemapTarget]))===JSON.stringify([...previewDoc().querySelectorAll('#sitemap a')].map(a=>[a.textContent,a.hash.slice(1)])));
    const previewLink=d.querySelector('#process-ia .process-sitemap-preview a'),linkedId=previewLink.dataset.sitemapTarget,linkedDoc=previewDoc(),beforePreviewLink=evaluate('projectJson()');
    previewLink.click();await wait();
    test(mode+' visitor sitemap preview links focus the real iframe destination safely',()=>previewLink.hash==='#previewShell' && previewDoc()===linkedDoc && previewDoc().activeElement.id===linkedId && w.DSStudio.activeStage===1 && evaluate('projectJson()')===beforePreviewLink);
    const beforePages=evaluate('DSStudio.process.currentPlan().pages'),beforeCss=evaluate('cssExport()'),beforeBodySections=previewDoc().querySelectorAll('main > section').length;
    const original=iaNode(child),control=iaChoice(child);control.focus();control.click();await wait();
    test(mode+' child exclusion changes only sitemap navigation and retains checkbox focus',()=>!iaFooterHas(child) && iaNode(child).id===original.id && !iaNode(child).includeInSitemap && evaluate('DSStudio.process.currentPlan().pages')===beforePages && evaluate('cssExport()')===beforeCss && previewDoc().getElementById(target) && previewDoc().querySelectorAll('main > section').length===beforeBodySections && d.querySelector('#process-ia .process-map').textContent.includes(child) && d.activeElement===control);
    iaChoice(parent).click();await wait();
    test(mode+' excluded parent suppresses its branch without losing child choices',()=>!iaFooterHas(parent) && iaChoice(child).disabled && !iaChoice(child).checked && iaNodes().filter(node=>node.parentId===iaNode(parent).id).some(node=>node.includeInSitemap));
    iaChoice(parent).click();await wait();
    test(mode+' restoring parent respects individual child exclusions',()=>iaFooterHas(parent) && !iaChoice(child).disabled && !iaFooterHas(child) && !iaChoice(child).checked);
    iaSelect(child);input('sitemap-label','Renamed information');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' renaming excluded information preserves identity and inclusion',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap && !iaFooterHas('Renamed information') && d.querySelector('#process-ia .process-map').textContent.includes('Renamed information'));
    const destinationParent=mode==='basic'?'Layouts':'Layout workshop';
    input('sitemap-parent',String(w.DSStudio.process.hierarchy(w.DSStudio.process.currentPlan().pages).findIndex(([label])=>label===destinationParent)),'change');
    input('sitemap-type','content','change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' reparenting keeps stable identity, type and sitemap choice',()=>iaNode('Renamed information').id===original.id && iaNode('Renamed information').path[0]===destinationParent && iaNode('Renamed information').type==='content' && !iaNode('Renamed information').includeInSitemap);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores the previous relationship and its inclusion',()=>iaNode('Renamed information').id===original.id && iaNode('Renamed information').path[0]===parent && !iaNode('Renamed information').includeInSitemap);
    iaSelect('Renamed information');d.getElementById('sitemap-delete').click();await wait();d.getElementById('sitemap-undo').click();await wait();
    test(mode+' delete and undo restore identity and exclusion',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap);
    const savedIa=evaluate('projectJson()');w.importConfig(JSON.parse(savedIa));await wait();
    test(mode+' IA identities and inclusion survive project JSON round trip',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap && !iaFooterHas('Renamed information'));
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    iaChoice(parent).click();await wait();
    test(mode+' sitemap inclusion autosaves with the active project',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectId].data.designProcess.iaEntries[mode].some(node=>node.id===iaNode(parent).id && node.includeInSitemap===false));
    const exportDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    test(mode+' standalone HTML and inspector use the same selected sitemap',()=>exportDoc.querySelector('#sitemap').innerHTML===previewDoc().querySelector('#sitemap').innerHTML && ![...exportDoc.querySelectorAll('#sitemap a, #sitemap span')].some(el=>el.firstChild?.textContent===parent));
  }
  reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  iaChoice('Home').click();await wait();
  test('Explicit Home inclusion overrides the former Basic fixed omission',()=>iaFooterHas('Home') && iaNode('Home').includeInSitemap);
  iaChoice('Content card').click();await wait();d.getElementById('dockModeAdvanced').click();await wait();iaChoice('Brief lesson').click();await wait();d.getElementById('dockModeBasic').click();await wait();
  test('Sample switches preserve each sample inclusion choices',()=>!iaChoice('Content card').checked && w.DSStudio.process.currentPlan().iaEntries.advanced.some(node=>node.includeInSitemap===false));
  iaSelect('Components');input('sitemap-label','Teaching group');input('sitemap-type','group','change');d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Group type is a nonlinked heading with selected child destinations',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(li=>li.querySelector(':scope > span')?.textContent==='Teaching group' && li.querySelector('ul a')) && iaNode('Teaching group').type==='group');
  const groupId=iaNode('Teaching group').id;iaChoice('Teaching group').click();await wait();iaSelect('Teaching group');input('sitemap-label','Renamed group');d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Parent rename preserves its own identity and descendant exclusions',()=>iaNode('Renamed group').id===groupId && !iaNode('Renamed group').includeInSitemap && !iaNode('Content card').includeInSitemap && iaNode('Content card').path[0]==='Renamed group' && !iaFooterHas('Profile row'));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    test('IA inclusion controls and both lesson views fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#sitemap-editor select:not([hidden]), #sitemap-editor input:not([type=checkbox]), #process-ia .process-sitemap-preview a')].every(el=>el.getBoundingClientRect().height>=44) && d.getElementById('sitemap-choices').scrollWidth<=d.getElementById('sitemap-choices').clientWidth+1 && [...d.querySelectorAll('#sitemap-choices label')].every(row=>row.getBoundingClientRect().height>=44) && ['.process-map','.process-sitemap-preview'].every(selector=>{const el=d.querySelector('#process-ia '+selector);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();d.getElementById('dockModeBasic').click();
  const bulkIa=Array.from({length:64},(_,i)=>'Group '+i+' > Item '+i).join('\n');
  input('plan-pages',bulkIa);await wait();iaChoice('Item 63').click();await wait();
  test('Inclusion works for bounded legacy outlines without rewriting or truncating their lines',()=>evaluate('state.designProcess.pages')===bulkIa && iaNodes().length===128 && !iaNode('Item 63').includeInSitemap && iaNode('Item 63').path[0]==='Group 63');
  app.style.width='1440px';reset();await wait();
  const invalidIa=w.DSStudio.process.normalize({iaEntries:{basic:[{id:'ia-1',path:['Safe'],type:'<script>',includeInSitemap:false},{id:'ia-1',path:['Duplicate']},{id:'<img>',path:['Bad']},{id:'ia-2',path:['Too','Many','Nested','Levels']},{id:'ia-3',path:[null]}]}});
  test('Imported IA metadata validates identities, paths, types and duplicate IDs',()=>invalidIa.iaEntries.basic.length===1 && invalidIa.iaEntries.basic[0].type==='section' && invalidIa.iaEntries.basic[0].includeInSitemap===false);
  w.importConfig({sampleMode:'basic',designProcess:{pages:'Research <img src=x onerror=alert(1)',showPlanned:true,iaEntries:{basic:[{id:'ia-1',path:['Research <img src=x onerror=alert(1)'],type:'page',includeInSitemap:true}]}}});w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  test('Imported IA labels remain safe text in controls, full IA and sitemap',()=>!d.querySelector('#sitemap-choices img, #process-ia img, #process-ia script') && !previewDoc().querySelector('#sitemap img, #sitemap script') && d.getElementById('sitemap-choices').textContent.includes('<img') && previewDoc().querySelector('#sitemap').textContent.includes('<img'));
  evaluate('resetStudio()');await wait();
  test('Reset clears saved IA metadata and restores default sample inclusion',()=>!evaluate('state.designProcess.iaEntries.basic.length') && !evaluate('state.designProcess.iaEntries.advanced.length') && iaNodes().every(node=>node.includeInSitemap===(node.depth<3 && node.label!=='Home' && node.label!=='Footer')));

  // Three information levels retain a separate visitor sitemap in both samples.
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    const parent=mode==='basic'?'Components':'Design process',branch=mode==='basic'?'Profile row':'Project brief';
    const detail=mode==='basic'?'Availability status':'Purpose and audience';
    const sibling=mode==='basic'?'Name and role':'Scope and delivery';
    const target=mode==='basic'?'basic-layout':'brief-lab';
    const original=iaNodes().filter(node=>node.path.includes(branch)).map(node=>({id:node.id,label:node.label,include:node.includeInSitemap}));
    const sectionCount=previewDoc().querySelectorAll('main > section').length;
    test(mode+' sample includes excluded third-level content planning without invented links',()=>iaNode(detail).depth===3 && iaNode(detail).type==='content' && !iaNode(detail).includeInSitemap && !iaFooterHas(detail) && !d.querySelector('#process-ia .process-map a') && d.querySelector('#process-ia .process-map ul ul ul').textContent.length>0 && d.querySelector('#process-ia a[href="https://www.nngroup.com/articles/flat-vs-deep-hierarchy/"]'));
    iaChoice(detail).click();await wait();
    test(mode+' selected unlinked detail stays out of the visitor sitemap by default',()=>iaNode(detail).includeInSitemap && !iaFooterHas(detail));
    d.getElementById('sitemap-planned').click();await wait();
    test(mode+' planned detail appears at the correct third sitemap level as text',()=>[...previewDoc().querySelectorAll('#sitemap ul ul ul > li > span')].some(el=>el.firstChild.textContent===detail+' ') && ![...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent===detail));
    iaSelect(detail);input('sitemap-target',target,'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    const detailId=iaNode(detail).id;
    test(mode+' third-level destination uses an existing safe anchor in preview and export',()=>[...previewDoc().querySelectorAll('#sitemap ul ul ul a')].some(a=>a.textContent===detail && a.hash==='#'+target) && new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap ul ul ul a[href="#'+target+'"]') && previewDoc().querySelectorAll('main > section').length===sectionCount);
    iaChoice(parent).click();await wait();
    test(mode+' excluded ancestor suppresses third-level links while retaining choices',()=>iaChoice(detail).disabled && iaChoice(detail).checked && !iaFooterHas(detail));
    iaChoice(parent).click();await wait();iaChoice(branch).click();await wait();
    test(mode+' excluded immediate parent also suppresses the third level',()=>iaChoice(detail).disabled && iaChoice(detail).checked && !iaFooterHas(detail));
    iaChoice(branch).click();await wait();
    iaSelect(branch);
    test(mode+' branch parent options exclude descendants and fourth-level moves',()=>[...d.getElementById('sitemap-parent').options].every(option=>!option.textContent.includes(branch) && option.value.split(':').length<2));
    input('sitemap-label','Renamed branch');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' branch rename preserves every descendant identity and inclusion',()=>original.every(old=>iaNode(old.label===branch?'Renamed branch':old.label)?.id===old.id) && iaNode(detail).path[1]==='Renamed branch' && iaNode(detail).includeInSitemap && !iaNode(sibling).includeInSitemap && iaFooterHas(detail));
    const destination=mode==='basic'?'Layouts':'Lessons',dest=iaNode(destination);
    input('sitemap-parent',dest.position.join(':'),'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' moving a two-level branch retains third-level relationships and identities',()=>iaNode(detail).id===detailId && iaNode(detail).path.join(' / ')===destination+' / Renamed branch / '+detail && iaFooterHas(detail));
    iaSelect(detail);input('sitemap-label','Renamed detail');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' detail rename preserves its ID and explicit link mapping',()=>iaNode('Renamed detail').id===detailId && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Renamed detail' && a.hash==='#'+target));
    iaSelect('Renamed detail');const orderBefore=iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',');
    d.getElementById(mode==='basic'?'sitemap-up':'sitemap-down').click();await wait();
    test(mode+' detail siblings reorder without losing their identities',()=>iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',')!==orderBefore && iaNode('Renamed detail').id===detailId);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores third-level sibling order',()=>iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',')===orderBefore);
    iaSelect('Renamed branch');const beforeDelete=evaluate('projectJson()');d.getElementById('sitemap-delete').click();await wait();
    test(mode+' deleting a branch removes all descendants from the plan',()=>!iaNode('Renamed branch') && !iaNode('Renamed detail') && !iaNode(sibling));
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores the complete three-level branch and metadata',()=>evaluate('projectJson()')===beforeDelete && iaNode('Renamed detail').id===detailId);
    const roundTrip=JSON.parse(evaluate('projectJson()'));w.importConfig(roundTrip);await wait();
    test(mode+' third-level identities and choices survive JSON import',()=>iaNode('Renamed detail').id===detailId && iaNode('Renamed detail').includeInSitemap && !iaNode(sibling).includeInSitemap && iaFooterHas('Renamed detail'));
    d.getElementById('jSaveLocal').click();const savedId=d.getElementById('jProjects').value;
    test(mode+' third-level paths and IDs persist in local project storage',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[savedId].data.designProcess.iaEntries[mode].some(node=>node.id===detailId && node.path.length===3));
    iaSelect('Renamed branch');const unchanged=evaluate('projectJson()');
    const forged=new w.Option('Invalid descendant',iaNode('Renamed detail').position.join(':'));d.getElementById('sitemap-parent').add(forged);input('sitemap-parent',forged.value,'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' forged cycle or fourth-level parent is rejected without changing saved data',()=>evaluate('projectJson()')===unchanged && d.getElementById('sitemap-status').textContent.includes('at most three'));
    d.getElementById('sitemap-discard').click();d.getElementById('sitemap-new').click();input('sitemap-label','New planning detail');const newParent=iaNode(mode==='basic'?'Content card':'Information architecture');input('sitemap-parent',newParent.position.join(':'),'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' adding a third-level item defaults to content excluded from the sitemap',()=>iaNode('New planning detail').depth===3 && iaNode('New planning detail').type==='content' && !iaNode('New planning detail').includeInSitemap);
  }
  reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  const oldTwoLevel=w.DSStudio.process.samplePages('basic').split('\n').filter(line=>line.split('>').length<=2).join('\n');
  w.importConfig({sampleMode:'basic',designProcess:{pages:oldTwoLevel,iaEntries:{basic:[{id:'ia-88',path:['Components','Profile row'],type:'section',includeInSitemap:false}]}}});await wait();
  test('Previous complete two-level samples gain planning details without losing saved IDs or exclusions',()=>iaNode('Profile row').id==='ia-88' && !iaNode('Profile row').includeInSitemap && iaNode('Availability status').depth===3 && iaChoice('Availability status').disabled && evaluate('state.designProcess.pages')===oldTwoLevel);
  const customThree='Services\nServices > Consultation\nServices > Consultation > Duration\nServices > Consultation > Price\nAbout';input('plan-pages',customThree);await wait();
  test('Raw third-level outlines share a single parent tree and remain custom across modes',()=>iaNodes().length===5 && w.DSStudio.process.tree(customThree)[0].children[0].children.length===2 && w.DSStudio.process.hierarchy(customThree)[0][1].length===1);
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Sample switches preserve a custom three-level outline',()=>evaluate('DSStudio.process.currentPlan().pages')===customThree && iaNode('Duration').depth===3);
  input('plan-pages','Root > Branch > Detail > Too deep');await wait();
  test('Raw fourth-level lines are visibly flagged and excluded from rendered IA',()=>!d.getElementById('plan-pages').checkValidity() && d.getElementById('plan-sample-status').textContent.includes('three information levels') && iaNodes().length===0);
  const bulkThree=Array.from({length:64},(_,i)=>'Group '+i+' > Item '+i+' > Detail '+i).join('\n');input('plan-pages',bulkThree);await wait();iaChoice('Detail 63').click();await wait();
  test('Three-level legacy line limits retain all 192 derived entries and choices',()=>iaNodes().length===192 && evaluate('state.designProcess.pages')===bulkThree && iaNode('Detail 63').includeInSitemap && evaluate('state.designProcess.iaEntries.advanced.length')===192 && d.getElementById('plan-pages').checkValidity());
  input('plan-pages','Root > Branch > <img src=x onerror=alert(1)');await wait();
  test('Valid third-level hostile labels remain escaped text in the IA and editor',()=>iaNodes().length===3 && !d.querySelector('#process-ia img, #process-ia script, #sitemap-choices img') && d.querySelector('#process-ia .process-map').textContent.includes('<img src=x onerror=alert(1)') && d.getElementById('sitemap-choices').textContent.includes('<img') && !d.getElementById('plan-pages').validationMessage);
  const bounded=w.DSStudio.process.normalize({iaEntries:{basic:Array.from({length:200},(_,i)=>({id:'ia-'+(i+1),path:['Root '+i,'Branch','Detail'],type:'content',includeInSitemap:false}))}});
  test('Imported third-level metadata retains valid depth and a bounded 192-entry maximum',()=>bounded.iaEntries.basic.length===192 && bounded.iaEntries.basic.every(node=>node.path.length===3 && !node.includeInSitemap));
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    for(const width of [320,390,1440]) {
      app.style.width=width+'px';await wait();
      test(mode+' '+theme+' third-level IA fits '+width+'px with usable controls',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && d.getElementById('sitemap-choices').scrollWidth<=d.getElementById('sitemap-choices').clientWidth+1 && d.getElementById('sitemap-choices').querySelector('ul').scrollWidth<=d.getElementById('sitemap-choices').clientWidth+1 && [...d.querySelectorAll('#sitemap-choices .is-grandchild')].every(el=>el.getBoundingClientRect().height>=44) && ['.process-map','.process-sitemap-preview'].every(selector=>{const el=d.querySelector('#process-ia '+selector);return el.scrollWidth<=el.clientWidth+1;}));
    }
  }
  app.style.width='1440px';reset();await wait();

  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  // Eyebrow sitemap: shared visible labels, real destinations and saved configuration.
  {
    const sectionModel=w.DSStudio.sectionSitemap;
    const changeSource=value=>{revealArchitecture();const control=d.getElementById('sitemap-source');control.value=value;control.dispatchEvent(new w.Event('change',{bubbles:true}));};
    const chooseSection=(id,checked)=>{const control=[...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===id);control.checked=checked;control.dispatchEvent(new w.Event('change',{bubbles:true}));};
    const mapLinks=()=>[...previewDoc().querySelectorAll('#sitemap a')];
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const rows=sectionModel.nodes(),body=previewDoc(),beforeContent=JSON.stringify(w.DSStudio.contentArchitecture.nodes());
      test(mode+' defaults to page labels with source selection first and advanced text tools hidden',()=>d.getElementById('section-sitemap-editor').firstElementChild.id==='sitemap-source-field' && d.getElementById('sitemap-source-field').contains(d.getElementById('sitemap-source')) && d.getElementById('architecture-sitemap-advanced').hidden && sectionModel.source()==='sections' && d.getElementById('sitemap-source').value==='sections' && d.getElementById('sitemap-destination-editor').hidden && d.getElementById('sitemap-outline-editor').hidden && w.DSStudio.contentArchitecture.nodes().length>100);
      test(mode+' every sitemap label and destination matches a visible eyebrow or heading',()=>rows.length>10 && rows.every(node=>{const target=body.getElementById(node.id);return target && [...target.querySelectorAll('.eyebrow,.sample-eyebrow,h1,h2,h3,h4,h5,h6,legend'),target].some(el=>el.textContent.replace(/\s+/g,' ').trim()===node.label);}) && mapLinks().map(a=>a.hash.slice(1)).join(',')===rows.map(node=>node.id).join(',') && mapLinks().every((a,i)=>a.textContent===rows[i].label));
      test(mode+' sitemap follows container ancestry and keeps slash labels whole',()=>rows.some(node=>node.id==='home' && !node.parentId) && rows.every(node=>!node.parentId || body.getElementById(node.parentId).contains(body.getElementById(node.id))) && !rows.some(node=>node.id==='footer'));
      test(mode+' preview proxies and exported fragment links share the same labels',()=>{const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html'),proxies=[...d.querySelectorAll('.process-sitemap-preview a[data-sitemap-target]')];return proxies.length===rows.length && proxies.every((a,i)=>a.hash==='#previewShell' && a.dataset.sitemapTarget===rows[i].id && a.textContent===rows[i].label) && [...exported.querySelectorAll('#sitemap a')].every((a,i)=>a.hash==='#'+rows[i].id && a.textContent===rows[i].label && exported.querySelectorAll('[id="'+rows[i].id+'"]').length===1);});
      if(mode==='basic') {
        test('Basic sitemap root labels match the four section eyebrows',()=>rows.filter(node=>!node.parentId).map(node=>node.label).join('|')==='HTML & CSS essentials|Components / Flexbox|Layouts / CSS Grid|Forms / Labels & controls');
        test('Basic component eyebrows and list heading fallbacks remain correctly nested',()=>rows.find(node=>node.id==='basic-structure').label==='Article / Content card' && rows.find(node=>node.id==='basic-structure').parentId==='features' && rows.find(node=>node.id==='list-collection').label==='Unordered list' && rows.find(node=>node.id==='list-collection').parentId==='lists');
      }
      const parent=mode==='basic'?'features':'components',child=mode==='basic'?'basic-structure':'component-actions';
      chooseSection(child,false);chooseSection(parent,false);await wait();
      test(mode+' excluding a parent suppresses its branch without changing content',()=>!mapLinks().some(a=>a.hash==='#'+parent || a.hash==='#'+child) && [...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===child).disabled && JSON.stringify(w.DSStudio.contentArchitecture.nodes())===beforeContent);
      const canonical=w.DSStudio.contentArchitecture.nodes().find(node=>node.target===child && node.type!=='link'),select=d.querySelector('[data-content-id="'+canonical.id+'"]');
      for(let ancestor=select.parentElement;ancestor;ancestor=ancestor.parentElement)if(ancestor.tagName==='DETAILS')ancestor.open=true;
      select.click();d.getElementById('ia-manage-sitemap').click();
      test(mode+' configuring an excluded child focuses the parent that must be enabled first',()=>d.activeElement.dataset.sectionId===parent);
      chooseSection(parent,true);await wait();
      test(mode+' re-including a parent retains independent child exclusions',()=>mapLinks().some(a=>a.hash==='#'+parent) && !mapLinks().some(a=>a.hash==='#'+child));
      d.getElementById('jSaveLocal').click();const sectionProjectId=d.getElementById('jProjects').value;
      chooseSection('home',false);await wait();
      test(mode+' section inclusion autosaves to the active project',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[sectionProjectId].data.designProcess.sitemapExcluded[mode].includes('home'));
      chooseSection('home',true);await wait();
      const config=evaluate('projectJson()');evaluate('importConfig('+config+')');await wait();
      test(mode+' section choices round trip through project JSON',()=>evaluate('state.designProcess.sitemapExcluded.'+mode).join(',')===child && !mapLinks().some(a=>a.hash==='#'+child));
      d.getElementById('section-sitemap-restore').click();await wait();
      test(mode+' Include all sections restores the current sample',()=>mapLinks().length===rows.length);
      evaluate('state.designProcess.goal="Keep this unrelated brief edit";apply()');
      d.getElementById('section-sitemap-undo').click();await wait();
      test(mode+' sitemap undo retains later brief changes',()=>evaluate('state.designProcess.goal')==='Keep this unrelated brief edit');
      test(mode+' section configuration undo restores exclusions',()=>!mapLinks().some(a=>a.hash==='#'+child));
      changeSource('custom');await wait();
      test(mode+' custom source reveals compatible destination controls',()=>!d.getElementById('sitemap-destination-editor').hidden && !d.getElementById('sitemap-outline-editor').hidden && d.getElementById('section-sitemap-settings').hidden);
      changeSource('sections');d.getElementById('section-sitemap-restore').click();await wait();
      const proxy=d.querySelector('.process-sitemap-preview [data-sitemap-target="'+parent+'"]');proxy.click();await wait();
      test(mode+' eyebrow sitemap preview link focuses the actual page section',()=>previewDoc().activeElement.id===parent);
      for(const theme of ['light','dark']) {
        if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();
        for(const width of [320,390,1440]) {
          app.style.width=width+'px';w.dssShowWizardStep(1);await wait();
          revealArchitecture();test(mode+' '+theme+' eyebrow sitemap controls fit '+width+'px',()=>{const editor=d.getElementById('section-sitemap-editor'),box=editor.getBoundingClientRect();return d.documentElement.scrollWidth<=w.innerWidth+1 && [...editor.querySelectorAll('select,button,#section-sitemap-choices label')].filter(el=>el.getBoundingClientRect().width>0).every(el=>{const b=el.getBoundingClientRect();return b.height>=44 && b.right<=box.right+1;});});
        }
      }
    }
    app.style.width='1440px';reset();await wait();
    w.importConfig({sampleMode:'basic',designProcess:{sitemapSource:{basic:'sections',advanced:'sections'},sitemapExcluded:{basic:['home','features','lists','signup'],advanced:['about']}}});await wait();
    test('An empty section sitemap explains its selection state and retains website content',()=>!mapLinks().length && previewDoc().querySelector('#sitemap').textContent.includes('No sections selected') && previewDoc().querySelectorAll('main > section').length===4);
    d.getElementById('section-sitemap-restore').click();await wait();
    test('Restoring Basic section choices retains Advanced choices',()=>evaluate('state.designProcess.sitemapExcluded.basic').length===0 && evaluate('state.designProcess.sitemapExcluded.advanced').join(',')==='about');
    d.getElementById('dockModeAdvanced').click();await wait();
    test('Mode switches apply the matching saved section choices',()=>!mapLinks().some(a=>a.hash==='#about') && mapLinks().some(a=>a.hash==='#home'));
    d.getElementById('dockModeBasic').click();await wait();
    test('Returning to Basic restores its complete section sitemap',()=>mapLinks().length===12);
    const fixture='<main><section id="features"><p class="eyebrow">Components / Flexbox</p><article id="basic-structure"><p class="eyebrow">Repeated &amp; safe</p></article><article id="basic-layout"><h3>Repeated &amp; safe</h3></article></section><section id="lists"><article id="list-collection"><p class="eyebrow">Child only</p></article></section></main>';
    const collected=sectionModel.collect(fixture,'basic');
    test('Section collector preserves duplicate label identities and does not borrow child eyebrows',()=>collected.length===4 && collected[1].label===collected[2].label && collected[1].id!==collected[2].id && !collected.some(node=>node.id==='lists') && collected.find(node=>node.id==='list-collection').parentId===null);
    w.importConfig({sampleMode:'basic',designProcess:{sitemapSource:{basic:'malicious'},sitemapExcluded:{basic:['features','features','javascript:alert(1)','missing']}}});await wait();
    test('Imported sitemap source and exclusions use bounded fixed values',()=>evaluate('state.designProcess.sitemapSource.basic')==='auto' && evaluate('state.designProcess.sitemapExcluded.basic').join(',')==='features');
    w.importConfig({sampleMode:'basic',designProcess:{pages:'Home\nCustom > Content card',pageLinks:{basic:{Custom:'features'}}}});await wait();
    test('Older custom outlines retain their navigation until switched explicitly',()=>sectionModel.source()==='custom' && mapLinks().some(a=>a.textContent==='Custom'));
    const customBefore=evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.contentPlan])');changeSource('sections');await wait();
    test('Switching an old plan to page labels preserves its saved plan and content',()=>mapLinks().some(a=>a.textContent==='Components / Flexbox') && evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.contentPlan])')===customBefore);
    evaluate('state.project="<img src=x onerror=alert(1)> & Safe";state.sampleMode="advanced";state.designProcess.sitemapSource.advanced="sections";apply()');await wait();
    test('Dynamic eyebrow text stays escaped in sitemap controls, preview and exports',()=>mapLinks().some(a=>a.textContent.includes('<img')) && !previewDoc().querySelector('#sitemap img') && !d.querySelector('#section-sitemap-choices img') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap img'));
    reset();await wait();
  }

  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(1,false);revealArchitecture();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
  // The following sitemap fixtures establish their own clean desktop model.
  app.style.width='1440px';reset();await wait();
  // Sitemap uses the same native outline / selected-properties pattern in both sources.
  for(const mode of ['basic','advanced']) {
    if(d.getElementById('studioInspector').open)d.getElementById('inspectorToggle').click();
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();d.getElementById('architecture-sitemap').open=true;
    const sectionNodes=w.DSStudio.sectionSitemap.nodes(),child=sectionNodes.find(node=>node.parentId),automatic=d.getElementById('section-sitemap-settings'),before=evaluate('projectJson()');
    test(mode+' page sitemap provides a searchable native outline and selected destination properties',()=>automatic.querySelector('.sitemap-browser input[type="search"]') && automatic.querySelector('.sitemap-properties') && automatic.querySelectorAll('button[data-sitemap-node-id]').length===sectionNodes.length && automatic.querySelectorAll('.sitemap-outline details').length>0);
    const choose=id=>{const button=[...d.querySelectorAll('#section-sitemap-choices button')].find(el=>el.dataset.sitemapNodeId===id);for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    input('section-sitemap-search',child.label);
    test(mode+' sitemap search reveals matching descendants and their containing branches without editing data',()=>[...d.querySelectorAll('#section-sitemap-choices button')].find(el=>el.dataset.sitemapNodeId===child.id).closest('li').hidden===false && d.querySelector('#section-sitemap-choices details').open && evaluate('projectJson()')===before);
    choose(child.id);
    test(mode+' page destination selection exposes its label, location and native inclusion choice',()=>d.getElementById('section-sitemap-name').textContent===child.label && d.getElementById('section-sitemap-path').textContent.includes(' / ') && d.activeElement.id==='section-sitemap-heading' && d.getElementById('section-sitemap-preview-link').dataset.sitemapTarget===child.id);
    d.getElementById('section-sitemap-included').click();await wait();
    test(mode+' selected inclusion changes the same saved sitemap as outline checkboxes',()=>!d.getElementById('section-sitemap-included').checked && ![...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===child.id).checked && !previewDoc().querySelector('#sitemap a[href="#'+child.id+'"]'));
    d.getElementById('section-sitemap-undo').click();await wait();input('section-sitemap-search','');
    const focusedCheckbox=[...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===child.id);for(let parent=focusedCheckbox.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;focusedCheckbox.focus();focusedCheckbox.click();await wait();
    test(mode+' outline inclusion retains native checkbox focus through reconciliation',()=>d.activeElement===focusedCheckbox);
    d.getElementById('section-sitemap-undo').click();await wait();
    for(const source of ['sections','custom']) {
      const control=d.getElementById('sitemap-source');control.value=source;control.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
      if(source==='custom')d.getElementById('architecture-sitemap-advanced').open=false;
      const editor=source==='sections'?automatic:d.getElementById('sitemap-editor');
      test(mode+' '+source+' sitemap editing is available outside Advanced sitemap options',()=>!d.getElementById('architecture-sitemap-advanced').contains(editor) && (editor.matches('.sitemap-workspace') || editor.querySelector('.sitemap-workspace')) && editor.querySelector('.sitemap-properties'));
      for(const width of [320,390,1440]) {
        app.style.width=width+'px';await wait();editor.querySelectorAll('details').forEach(el=>el.open=true);
        const grid=editor.matches('.sitemap-workspace')?editor:editor.querySelector('.sitemap-workspace'),preview=d.getElementById('architecture-sitemap-preview'),b=grid.querySelector('.sitemap-browser').getBoundingClientRect(),p=grid.querySelector('.sitemap-properties').getBoundingClientRect(),m=preview.getBoundingClientRect(),available=d.getElementById('architecture-workspace').clientWidth;
        test(mode+' '+source+' Find, Selected and Preview use the available columns at '+width+'px',()=>preview.parentElement===grid && preview.querySelector('.process-sitemap-preview').tabIndex===0 && (available>=928?Math.abs(b.top-p.top)<1 && Math.abs(p.top-m.top)<1 && b.right<=p.left+1 && p.right<=m.left+1:available>=736?b.right<=p.left+1 && m.top>=Math.max(b.bottom,p.bottom)-1:p.top>=b.bottom-1 && m.top>=p.bottom-1));
        test(mode+' '+source+' outline and properties fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...editor.querySelectorAll('.sitemap-workspace input:not([type="checkbox"]),.sitemap-workspace select:not([hidden]),.sitemap-workspace button')].filter(el=>el.getBoundingClientRect().width>0).every(el=>{const r=el.getBoundingClientRect();return r.height>=44 && r.left>=0 && r.right<=w.innerWidth+1;}));
        test(mode+' '+source+' destination labels retain readable width without horizontal outline scrolling at '+width+'px',()=>editor.querySelector('.sitemap-outline').scrollWidth<=editor.querySelector('.sitemap-outline').clientWidth+1 && [...editor.querySelectorAll('.sitemap-select')].filter(el=>el.getBoundingClientRect().width>0).every(el=>el.getBoundingClientRect().width>=Math.min(80,el.closest('li').getBoundingClientRect().width-20)));
      }
      app.style.width='1440px';await wait();
    }
    const savedCustom=evaluate('projectJson()'),original=d.getElementById('sitemap-label').value;
    input('sitemap-label','Unsaved navigation label');
    const other=[...d.querySelectorAll('#sitemap-choices button')].find(el=>el.getAttribute('aria-pressed')==='false');other.click();
    test(mode+' custom outline selection protects unsaved properties',()=>d.getElementById('sitemap-label').value==='Unsaved navigation label' && evaluate('projectJson()')===savedCustom && d.activeElement.id==='sitemap-save');
    const control=d.getElementById('sitemap-source');control.value='sections';control.dispatchEvent(new w.Event('change',{bubbles:true}));
    test(mode+' switching sitemap source cannot discard unsaved custom properties',()=>control.value==='custom' && w.DSStudio.sectionSitemap.source()==='custom' && evaluate('projectJson()')===savedCustom);
    d.getElementById('sitemap-discard').click();
    test(mode+' custom Discard restores the saved label and releases the selection guard',()=>d.getElementById('sitemap-label').value===original && d.getElementById('sitemap-discard').disabled);
    input('sitemap-label','Navigation label '+mode);d.getElementById('sitemap-save').click();await wait();
    test(mode+' selected properties save through the original custom destination model',()=>w.DSStudio.process.entries().some(node=>node.label==='Navigation label '+mode) && d.getElementById('sitemap-discard').disabled);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' custom destination Undo retains the existing model and source',()=>!w.DSStudio.process.entries().some(node=>node.label==='Navigation label '+mode) && w.DSStudio.sectionSitemap.source()==='custom');
  }
  reset();await wait();

  // File replacement must clear private custom-editor state, while source Undo
  // changes only sitemap configuration and preserves later Brief edits.
  for(const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();
    const destination=mode==='basic'?'features':'about';
    w.importConfig({sampleMode:mode,designProcess:{pages:'Resources\nResources > Saved link\nFuture page',pageLinks:{[mode]:{Resources:destination,'Saved link':destination,'Future page':''}},sitemapSource:{basic:mode==='basic'?'custom':'sections',advanced:mode==='advanced'?'custom':'sections'},showPlanned:true}});
    w.dssShowWizardStep(1,false);revealDestinationPlan();await wait();
    input('jProject',mode+' sitemap replacement fixture');d.getElementById('jSaveLocal').click();
    const entry=w.DSStudio.process.entries().find(node=>node.label==='Saved link');
    const choose=()=>{const button=[...d.querySelectorAll('#sitemap-choices button')].find(el=>el.dataset.sitemapNodeId===entry.id);for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    choose();input('sitemap-label','Saved link updated');d.getElementById('sitemap-save').click();await wait();
    const saved=evaluate('projectJson()'),library=w.localStorage.getItem('dss-v27-projects'),labelEditor=d.getElementById('sitemap-label');
    input('sitemap-label','Unsaved label before import');await importFile(saved);await wait();choose();
    test(mode+' identical JSON file import replaces dirty destination edits and clears stale Undo',()=>
      evaluate('projectJson()')===saved && d.getElementById('sitemap-undo').disabled && d.getElementById('sitemap-discard').disabled && d.getElementById('sitemap-label')===labelEditor && labelEditor.value==='Saved link updated' && w.localStorage.getItem('dss-v27-projects')===library);
    const customData=evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.iaEntries,state.designProcess.contentPlan])');
    const sections=[...previewDoc().querySelectorAll('main > section')].map(el=>el.id).join(','),hero=previewDoc().getElementById('hero-title').textContent;
    const source=d.getElementById('sitemap-source');source.value='sections';source.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
    const keptWebsite=sections===[...previewDoc().querySelectorAll('main > section')].map(el=>el.id).join(',') && previewDoc().getElementById('hero-title').textContent===hero;
    input('plan-goal','Brief edit after source switch');d.getElementById('section-sitemap-undo').click();await wait();
    test(mode+' source Undo after import retains custom data and later Brief edits without touching old saves',()=>
      keptWebsite && w.DSStudio.sectionSitemap.source()==='custom' && evaluate('state.designProcess.goal')==='Brief edit after source switch' && evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.iaEntries,state.designProcess.contentPlan])')===customData && w.localStorage.getItem('dss-v27-projects')===library);
    choose();const importedBase=evaluate('projectJson()');
    input('sitemap-label','Changed after file');d.getElementById('sitemap-save').click();await wait();
    test(mode+' saving an imported destination preserves its identity and avoids the old autosave target',()=>
      w.DSStudio.process.entries().find(node=>node.id===entry.id).label==='Changed after file' && w.DSStudio.process.destinationId('Changed after file')===destination && !d.getElementById('sitemap-undo').disabled && w.localStorage.getItem('dss-v27-projects')===library);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' custom Undo returns to the imported model with later Brief edits intact',()=>evaluate('projectJson()')===importedBase && d.getElementById('sitemap-undo').disabled && w.localStorage.getItem('dss-v27-projects')===library);
    choose();input('sitemap-label','Unsaved destination before New');d.getElementById('jNewLocal').click();await wait();
    test(mode+' New clears dirty custom fields and both Undo histories without changing saved projects',()=>
      d.getElementById('sitemap-discard').disabled && d.getElementById('sitemap-undo').disabled && d.getElementById('section-sitemap-undo').disabled && w.DSStudio.sectionSitemap.source()==='sections' && evaluate('state.sampleMode==="basic" && !state.designProcess.iaEntries.basic.length && !state.designProcess.iaEntries.advanced.length') && w.localStorage.getItem('dss-v27-projects')===library);
  }
  test('No sitemap JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Sitemap harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
