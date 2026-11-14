"""Independent shared planning workflow and Brief editor checks.

Run: python scripts/planning_review.py. Uses its own isolated app/profile and
shared local Chrome runner; does not import the integration harness.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Planning review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Planning review: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const previewWindow=()=>d.getElementById('previewPage').contentWindow;
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
  const revealAll = () => {revealArchitecture();d.querySelectorAll('#main > .studio-section, .step-more').forEach(section => {section.hidden=false;section.open=true;});};
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
  test('Independent planning startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  reset();w.dssShowWizardStep(3,false);await wait();
  // Planning workshops are part of the Advanced sample; New now starts Basic.
  d.getElementById('dockModeAdvanced').click();await wait();
  input('jProject','Community learning hub'); d.getElementById('jSaveLocal').click();
  const planProjectId=d.getElementById('jProjects').value;
  for (const [key,value] of Object.entries({audience:'New community members',goal:'Find a workshop and prepare a question.',scope:'Workshop listings and resources',content:'Organiser supplies workshop copy and photographs.',delivery:'Release in two weeks; organiser approves and maintains content.',success:'Find the right workshop without help.',constraints:'Keyboard and phone access',pages:'Home\nWorkshops > Layout\nWorkshops > Colour\nResources\nContact',prototypeTask:'Find the layout workshop.',prototypeNotes:'The participant hesitated at the first label.'})) input('plan-'+key,value);
  await wait();
  const processData=evaluate('JSON.stringify(state.designProcess)');
  test('Planning fields autosave with the active local project', () => JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planProjectId].data.designProcess)===processData);
  test('Brief, architecture, wireframe and prototype artifacts use the edited plan', () => d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent==='New community members' && d.querySelector('#process-ia .process-map').textContent.includes('Workshops') && d.querySelectorAll('#process-ia .process-map > ul > li').length===4 && d.querySelectorAll('#process-ia .process-map ul ul > li').length===2 && d.querySelector('#process-wireframe #wf-page') && d.querySelector('#process-prototype').textContent.includes('Find the layout workshop.'));
  test('Planning edits reach the HTML inspector, JSON export and responsive sample', () => {
    d.getElementById('dockTabHtml').click();
    return d.getElementById('dockCss').textContent===evaluate('htmlExport()') && evaluate('htmlExport()').includes('New community members') && JSON.stringify(JSON.parse(evaluate('projectJson()')).designProcess)===processData && previewDoc().querySelector('#brief-lab').textContent.includes('New community members') && previewDoc().querySelector('#wireframe-lab .wireframe-source-note');
  });
  const planExport=evaluate('projectJson()');
  reset(); evaluate('importConfig('+planExport+')'); await wait();
  test('All planning fields round trip through JSON and synchronize the editors', () => evaluate('JSON.stringify(state.designProcess)')===processData && [...d.querySelectorAll('[data-process-field]')].every(control=>control.value===JSON.parse(processData)[control.dataset.processField]));
  d.getElementById('jNewLocal').click(); input('plan-goal','A separate project task.'); d.getElementById('jSaveLocal').click();
  input('jProjects',planProjectId,'change'); d.getElementById('jLoadLocal').click(); await wait();
  test('Local project switching restores planning without overwriting the previous project', () => evaluate('JSON.stringify(state.designProcess)')===processData && JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planProjectId].data.designProcess)===processData);
  await importFile(JSON.stringify({project:'Imported planning file',designProcess:JSON.parse(processData)}));
  test('Actual JSON file input restores planning fields and lessons', () => evaluate('state.project')==='Imported planning file' && !d.getElementById('loadFile').value && evaluate('JSON.stringify(state.designProcess)')===processData && d.getElementById('plan-goal').value==='Find a workshop and prepare a question.');
  evaluate('importConfig({primary:"#123456"})'); await wait();
  test('Legacy projects receive starter planning data while preserving their palette', () => evaluate('state.primary==="#123456" && JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  evaluate('importConfig({designProcess:{audience:42,pages:["Bad"],layout:"split;display:none",scope:"x".repeat(5000),goal:"",unknown:"ignored"}})'); await wait();
  test('Imported planning validates field types, lengths, arrangement and empty drafts', () => evaluate('state.designProcess.audience===DSStudio.process.defaults().audience && state.designProcess.pages===DSStudio.process.defaults().pages && state.designProcess.layout==="split" && state.designProcess.scope.length===1200 && state.designProcess.goal==="" && !("unknown" in state.designProcess)') && d.getElementById('plan-goal').value==='');
  test('Architecture parsing bounds entries, depth and labels', () => {
    const groups=w.DSStudio.process.hierarchy(Array.from({length:100},(_,i)=>'Group '+i+'x'.repeat(80)+' > Child > Ignored').join('\n'));
    return groups.length===64 && groups.every(([label,children])=>label.length===64 && children.length===1 && children[0]==='Child');
  });
  for (const value of [null,[],42,'invalid']) {
    evaluate('importConfig({designProcess:'+JSON.stringify(value)+'})');
    test('Malformed planning '+JSON.stringify(value)+' uses safe defaults', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  }
  const hostile='<img src=x onerror="window.planExecuted=true"><script>window.planExecuted=true<\/script>';
  input('plan-audience',hostile); input('plan-pages',hostile+' > Child'); input('plan-prototypeNotes',hostile); await wait();
  test('Planning text is escaped in studio lessons, exports and the live sample', () => {
    const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !d.querySelector('[data-process-artifact] img, [data-process-artifact] script') && !exported.querySelector('#design-process img, #design-process script') && !previewDoc().querySelector('#design-process img, #design-process script') && d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent===hostile && exported.querySelector('#brief-lab [data-brief-field="audience"] dd').textContent===hostile && !w.planExecuted;
  });
  reset(); await wait();
  test('Editing planning never mutates the starter defaults; reset restores every field', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults()) && JSON.stringify(DEFAULT.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  d.getElementById('process-prototype').open=true;
  d.querySelector('#process-prototype .step-more').open=true;
  w.dssRevealSection('process-prototype',false);
  const prototypeNode=d.getElementById('studio-plan-choose'); prototypeNode.querySelector('a').focus();
  input('jAccent','#00badc'); await wait();
  test('Unrelated palette edits preserve planning nodes and prototype focus', () => d.getElementById('studio-plan-choose')===prototypeNode && d.activeElement===prototypeNode.querySelector('a'));
  d.getElementById('process-prototype').open=true;
  d.querySelector('a[href="#studio-plan-choose"]').click(); await wait();
  test('Centre prototype links reach real screen anchors', () => w.location.hash==='#studio-plan-choose' && d.getElementById('process-prototype').open);
  d.querySelector('a[href="#studio-plan-discover"]').click(); await wait();
  test('Centre prototype supports returning to the first screen', () => w.location.hash==='#studio-plan-discover');
  for (const destination of ['choose','review','discover']) {
    const source=destination==='choose'?'discover':destination==='review'?'choose':'review';
    previewDoc().querySelector(`#sample-plan-${source} a[href="#sample-plan-${destination}"]`).click(); await wait();
    test('Live prototype navigates to '+destination+' inside the preview', () => previewDoc().getElementById('sample-plan-'+destination).getBoundingClientRect().top>=-1 && previewDoc().getElementById('sample-plan-'+destination).getBoundingClientRect().top<previewWindow().innerHeight && !w.__reviewErrors.length);
  }
  const processPage=d.createElement('iframe'); processPage.style.cssText='width:1440px;height:1200px;border:0';
  const loadProcessPage=async()=>{
    processPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{processPage.onload=resolve;if(!processPage.isConnected)d.body.append(processPage);});
  };
  for (const theme of ['light','dark']) {
    input('jTheme',theme); await loadProcessPage();
    for (const width of [320,390,768,1440]) {
      processPage.style.width=width+'px'; app.style.width=width+'px'; await wait();
      const pd=processPage.contentDocument, pw=processPage.contentWindow;
      test(theme+' planning artifacts and controls fit at '+width+'px', () => {
        revealAll();
        const wire=pd.querySelector('.wireframe-source-note');
        return pd.documentElement.scrollWidth<=width+1 && d.documentElement.scrollWidth<=width+1 && wire && wire.textContent.includes('read-only') && [...pd.querySelectorAll('#design-process .process-wireframe > div, #design-process .process-screens > li')].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && el.scrollWidth<=el.clientWidth+1;});
      });
    }
    processPage.style.width='320px'; app.style.width='320px'; await wait();
    for (const step of [0,1,2,3]) {
      d.querySelector(`[data-journey-step="${step}"]`).click(); await wait();
      test(theme+' planning wizard stage '+(step+1)+' fits a 320px studio', () => {
        const controls=[...d.querySelectorAll(`[data-journey-pane="${step}"] textarea, [data-journey-pane="${step}"] select`)];
        if (d.documentElement.scrollWidth<=320 && controls.every(el=>el.scrollWidth<=el.clientWidth+1)) return true;
        throw Error(JSON.stringify({page:d.documentElement.scrollWidth,viewport:w.innerWidth,controls:controls.map(el=>({id:el.id,width:el.clientWidth,scroll:el.scrollWidth}))}));
      });
    }
  }
  processPage.remove(); app.style.width='1440px'; reset(); await wait();
  reset();await wait();previewDoc().getElementById('sample-menu').open=false;
  test('Brief lesson teaches seven website-project prompts instead of displaying a prefilled project', () => d.querySelectorAll('#process-brief .process-brief-guide > li').length===7 && d.querySelector('#process-brief .process-brief-template').textContent.includes('[audience]') && !d.querySelector('#process-brief .process-brief-draft') && ['goal','audience','scope','content','constraints','delivery','success'].every(key=>d.getElementById('plan-'+key).value===''));
  test('Website brief covers scope, content ownership, requirements, delivery and a concrete example', () => {
    const lesson=d.querySelector('#process-brief'), guide=lesson.querySelector('.process-brief-guide').textContent;
    return ['Purpose:','Audience:','Pages and features:','Content:','Design and requirements:','Delivery:','Success:'].every(label=>guide.includes(label)) && ['out of scope','who will supply','deadline','budget','approves','maintains'].every(term=>guide.includes(term)) && lesson.querySelector('.process-brief-example').textContent.includes('online ordering is out of scope') && lesson.querySelector('.learning-reference a').href==='https://www.smashingmagazine.com/2018/02/comprehensive-website-planning-guide-part1/' && !lesson.querySelector('a[href*="gov.uk"]') && previewDoc().querySelector('#brief-lab .process-brief-example') && evaluate('htmlExport()').includes('Build [website] for [audience]');
  });
  test('Website brief example and wizard labels render cleanly with preserved saved fields', () => d.querySelector('#process-brief .process-brief-example h4').textContent==='Example: a small café website' && d.querySelector('#process-brief .process-brief-example').textContent.includes("today's opening hours") && d.querySelector('label[for="plan-goal"]').textContent==='1. Purpose' && d.querySelector('label[for="plan-constraints"]').textContent==='5. Design and requirements');
  test('Brief wizard has the seven approved lesson questions in the same order with matching labels and prompts', () => {
    const controls=[...d.querySelectorAll('#plan-brief-fields [data-process-field]')], lesson=[...d.querySelectorAll('#process-brief .process-brief-guide li')];
    return JSON.stringify(controls.map(el=>el.dataset.processField))===JSON.stringify(['goal','audience','scope','content','constraints','delivery','success']) && controls.every((el,i)=>d.querySelector('label[for="'+el.id+'"]').textContent===(i+1)+'. '+lesson[i].querySelector('strong').textContent.slice(0,-1) && lesson[i].textContent.trim().endsWith(d.getElementById(el.getAttribute('aria-describedby')).textContent));
  });
  previewDoc().getElementById('working-together').open=true;
  input('plan-audience','Draft audience'); await wait();
  test('Adding the first brief draft preserves the correct preview FAQ and menu state', () => previewDoc().getElementById('working-together').open && !previewDoc().getElementById('sample-menu').open && !previewDoc().querySelector('.process-brief-draft').open);
  reset(); await wait();
  evaluate('importConfig({designProcess:{audience:"Local readers",goal:"Find opening times",scope:"Home and contact",success:"Find an answer",constraints:"Small budget"}})'); await wait();
  test('Existing brief drafts remain available beside the training guide', () => d.querySelector('#process-brief .process-brief-guide') && d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent==='Local readers' && d.getElementById('plan-goal').value==='Find opening times');
  test('Legacy combined brief notes stay intact and new Content/Delivery fields start blank', () => d.getElementById('plan-scope').value==='Home and contact' && d.getElementById('plan-constraints').value==='Small budget' && d.getElementById('plan-content').value==='' && d.getElementById('plan-delivery').value==='');
  input('plan-content','Owner supplies text, logo and photos.'); input('plan-delivery','Two weeks; owner approves and maintains.'); await wait();
  const sevenFieldBrief=evaluate('projectJson()'); reset(); evaluate('importConfig('+sevenFieldBrief+')'); await wait();
  test('Seven-field brief round trips and updates the centre draft and exported website', () => d.getElementById('plan-content').value==='Owner supplies text, logo and photos.' && d.getElementById('plan-delivery').value==='Two weeks; owner approves and maintains.' && d.querySelector('#process-brief [data-brief-field="content"] dd').textContent==='Owner supplies text, logo and photos.' && d.querySelector('#process-brief [data-brief-field="delivery"] dd').textContent==='Two weeks; owner approves and maintains.' && evaluate('htmlExport()').includes('Owner supplies text, logo and photos.') && evaluate('htmlExport()').includes('Two weeks; owner approves and maintains.') && JSON.stringify([...d.querySelectorAll('#process-brief .process-brief dt')].map(el=>el.textContent))===JSON.stringify([...d.querySelectorAll('#process-brief .process-brief-guide strong')].map(el=>el.textContent.slice(0,-1))));
  evaluate('importConfig({designProcess:{content:"x".repeat(5000),delivery:42}})'); await wait();
  test('New brief fields validate imported types and lengths', () => d.getElementById('plan-content').value.length===1200 && d.getElementById('plan-delivery').value==='');
  input('plan-content','<img src=x onerror=alert(1)>'); input('plan-delivery','<script>alert(1)<\/script>'); await wait();
  test('Content and Delivery remain escaped text in centre and exported drafts', () => !d.querySelector('#process-brief .process-brief-draft img, #process-brief .process-brief-draft script') && d.querySelector('#process-brief [data-brief-field="content"] dd').textContent.includes('<img') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#brief-lab .process-brief-draft img, #brief-lab .process-brief-draft script'));
  reset(); await wait();
  test('Reset clears all seven brief editors and saved values', () => ['goal','audience','scope','content','constraints','delivery','success'].every(key=>d.getElementById('plan-'+key).value==='' && evaluate('state.designProcess.'+key)===''));
  // Brief editing stays in the centre; project identity belongs to the local library.
  {
    reset();w.dssShowWizardStep(0,false);await wait();const brief=d.getElementById('brief-editor'),name=d.getElementById('jProject'),goal=d.getElementById('plan-goal');
    test('Project name is beside My local projects rather than inside Brief controls',()=>name.closest('.local-projects') && !name.closest('[data-journey-pane]') && d.querySelectorAll('#jProject').length===1);
    test('The seven original Brief editors belong to the centre lesson',()=>brief.closest('.studio-section')?.id==='process-brief' && d.querySelectorAll('#brief-editor #plan-brief-fields [data-process-field]').length===7 && brief.contains(d.getElementById('jPreset')));
    for(const theme of ['light','dark'])for(const width of [320,390,1440]){app.style.width=width+'px';if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(0,false);await wait();test(theme+' Brief remains in the centre with usable editors at '+width+'px',()=>brief.closest('.studio-section')?.id==='process-brief' && !brief.hidden && d.getElementById('plan-goal')===goal && name.closest('.local-projects') && d.documentElement.scrollWidth<=w.innerWidth+1 && [...brief.querySelectorAll('textarea,select')].every(el=>{const b=el.getBoundingClientRect();return b.height>=44 && b.left>=0 && b.right<=w.innerWidth+1;}));}
    app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();w.dssShowWizardStep(7,false);await wait();name.focus();input('jProject','Brief centre verification');await wait();test('Project name remains editable from other steps without switching lessons',()=>w.DSStudio.activeStage===7 && d.activeElement===name && evaluate('state.project')==='Brief centre verification' && name.getBoundingClientRect().height>=44);
    w.dssShowWizardStep(0,false);input('plan-goal','Help visitors find the right lesson.');input('plan-audience','Students and tutors.');d.getElementById('jSaveLocal').click();const id=d.getElementById('jProjects').value;input('plan-goal','Help visitors choose a lesson and practise.');await wait();
    test('Centre Brief edits and the relocated name autosave through the existing local project',()=>{const item=JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id];return item.data.project==='Brief centre verification' && item.data.designProcess.goal==='Help visitors choose a lesson and practise.' && item.data.designProcess.audience==='Students and tutors.';});
    const snapshot=evaluate('projectJson()');d.getElementById('jNewLocal').click();d.getElementById('jProjects').value=id;d.getElementById('jLoadLocal').click();await wait();test('Loading a local project restores its name and centre Brief fields',()=>name.value==='Brief centre verification' && goal.value==='Help visitors choose a lesson and practise.' && d.getElementById('plan-audience').value==='Students and tutors.' && brief.closest('.studio-section')?.id==='process-brief');
    w.importConfig(JSON.parse(snapshot));await wait();test('Project JSON retains the same Brief data and original editor nodes',()=>evaluate('state.designProcess.goal')===goal.value && d.getElementById('jProject')===name && d.getElementById('plan-goal')===goal && brief.closest('.studio-section')?.id==='process-brief');
    const confirm=w.confirm;try{w.confirm=()=>true;d.getElementById('jProjects').value=id;d.getElementById('jDeleteLocal').click();}finally{w.confirm=confirm;}reset();await wait();
  }
  // End centre Brief checks.

  reset();w.dssShowWizardStep(0,false);await wait();
  const fieldKeys=['goal','audience','scope','content','constraints','delivery','success'];
  const fieldNodes=fieldKeys.map(key=>d.getElementById('plan-'+key));
  test('Seven distinct Brief examples remain placeholders rather than saved answers',()=>
    fieldNodes.every(el=>el.placeholder.length>30 && el.value==='') && new Set(fieldNodes.map(el=>el.placeholder)).size===7 && fieldKeys.every(key=>evaluate('state.designProcess.'+key)===''));
  for(const [index,key] of fieldKeys.entries()) {
    const value=key+' <img src=x onerror="window.planningFieldExecuted=true"> & "quoted" text';
    fieldNodes[index].focus();input('plan-'+key,value);await wait();
    test('Brief '+key+' editing preserves its node/focus and escapes live and exported drafts',()=>{
      const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      return d.getElementById('plan-'+key)===fieldNodes[index] && d.activeElement===fieldNodes[index] &&
        evaluate('state.designProcess.'+key)===value &&
        d.querySelector('#process-brief [data-brief-field="'+key+'"] dd').textContent===value &&
        previewDoc().querySelector('#brief-lab [data-brief-field="'+key+'"] dd').textContent===value &&
        exported.querySelector('#brief-lab [data-brief-field="'+key+'"] dd').textContent===value &&
        !d.querySelector('#process-brief .process-brief-draft img,#process-brief .process-brief-draft script') &&
        !exported.querySelector('#brief-lab .process-brief-draft img,#brief-lab .process-brief-draft script') && !w.planningFieldExecuted;
    });
  }
  for(const mode of ['basic','advanced']) {
    reset();w.importConfig({sampleMode:mode,designProcess:{goal:'Find the '+mode+' lesson.',audience:'Students and tutors',scope:'Lessons and component examples',content:'Tutor supplies the text.',constraints:'Keyboard and phone access',delivery:'Tutor approves the handover.',success:'Find a useful lesson without help.',prototypeTask:'Choose a lesson.',prototypeNotes:'The first label was clear.'}});await wait();
    input('jProject',mode+' planning fixture');d.getElementById('jSaveLocal').click();
    const id=d.getElementById('jProjects').value,json=evaluate('projectJson()'),plan=evaluate('JSON.stringify(state.designProcess)'),html=evaluate('htmlExport()');
    d.getElementById('jNewLocal').click();d.getElementById('jProjects').value=id;d.getElementById('jLoadLocal').click();await wait();
    test(mode+' local load restores every Brief field and prototype notes',()=>evaluate('JSON.stringify(state.designProcess)')===plan && evaluate('state.sampleMode')===mode && fieldKeys.every(key=>d.getElementById('plan-'+key).value===JSON.parse(plan)[key]) && d.getElementById('plan-prototypeNotes').value==='The first label was clear.' && evaluate('htmlExport()')===html);
    const files=[],oldDownload=w.download;
    try{w.download=(name,content,type)=>files.push({name,content,type});d.getElementById('jExportJson').click();}
    finally{w.download=oldDownload;}
    reset();await importFile(files[0].content);await wait();
    test(mode+' downloaded planning JSON restores the same model and sample',()=>files.length===1 && files[0].name==='design-system-studio.json' && files[0].type==='application/json' && files[0].content===json && evaluate('projectJson()')===json && evaluate('state.sampleMode')===mode && evaluate('JSON.stringify(state.designProcess)')===plan);
    test(mode+' keeps planning in Studio and renders only its intended website content',()=>{
      const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      return d.querySelector('#process-brief [data-brief-field="content"] dd').textContent==='Tutor supplies the text.' &&
        d.querySelector('#process-prototype').textContent.includes('The first label was clear.') &&
        (mode==='advanced'?previewDoc().querySelector('#brief-lab [data-brief-field="content"] dd').textContent==='Tutor supplies the text.' && exported.querySelector('#prototype-lab').textContent.includes('The first label was clear.'):!previewDoc().querySelector('#design-process') && !exported.querySelector('#design-process') && !evaluate('htmlExport()').includes('The first label was clear.'));
    });
  }
  test('No planning JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Planning harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
