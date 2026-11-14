"""Independent local-project and JSON persistence checks.

Run: python scripts/project_library_review.py. Uses only a temporary Chrome
profile and the shared local runner; no integration-harness import or user data.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Project library review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload = async () => {
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Project library: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const input=(id,value,type='input')=>{
    const el=d.getElementById(id);
    w.DSStudio.typographyWorkspace?.revealControl(el);
    el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const stored=()=>JSON.parse(w.localStorage.getItem('dss-v27-projects')||'{}');
  const differences=(actual,expected,path='')=>{
    if(JSON.stringify(actual)===JSON.stringify(expected))return [];
    if(actual && expected && typeof actual==='object' && typeof expected==='object')
      return [...new Set([...Object.keys(actual),...Object.keys(expected)])].flatMap(key=>differences(actual[key],expected[key],path+'.'+key)).slice(0,12);
    return [{path,actual,expected}];
  };
  const saved=()=>stored()[d.getElementById('jProjects').value].data;
  const importFile=async text=>{
    const transfer=new w.DataTransfer();transfer.items.add(new w.File([text],'project.json',{type:'application/json'}));
    const picker=d.getElementById('loadFile');picker.files=transfer.files;
    picker.dispatchEvent(new w.Event('change',{bubbles:true}));
    for(let attempt=0;picker.value && attempt<100;attempt++)await fetch('/__review_tick__?attempt='+attempt,{cache:'no-store'});
    if(picker.value)throw Error('File input handler did not finish');
  };
  try {
  test('Independent startup has an empty library and no JavaScript errors',()=>!w.__reviewErrors.length && Object.keys(stored()).length===0);
  reset();
  input('clampMinWidth',480); input('clampMaxWidth',1440); input('clampFactor',.7);
  const fluidCss=evaluate('fluidTypeCss(5)');
  const project=evaluate('projectJson()');
  test('Project JSON preserves responsive typography settings', () => {
    input('clampFactor',1); input('clampMinWidth',375); input('clampMaxWidth',1280);
    evaluate('importConfig('+project+')'); return evaluate('fluidTypeCss(5)')===fluidCss;
  });
  input('clampFactor',.7);
  reset();
  test('Reset restores responsive typography defaults', () => evaluate('JSON.stringify(clampConfig)===JSON.stringify(CLAMP_DEFAULTS)'));
  test('Import clamps numeric values and rejects executable font text', () => {
    evaluate('importConfig({base:1e10,ratio:-5,font:"Arial; color:red",project:"<img src=x onerror=alert(1)>"})');
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return evaluate('state.base===22 && state.ratio===1.05 && state.font===DEFAULT.font') && !page.querySelector('img[onerror]') && page.querySelector('.sample-brand').textContent.includes('<img src=x onerror=alert(1)>');
  });
  test('Malformed button variant safely falls back', () => {
    evaluate('importConfig({buttonDesign:{variant:"__proto__"}})');
    return evaluate('state.buttonDesign.variant')==='primary';
  });
  test('Imported clamp settings are finite and bounded', () => {
    evaluate('importConfig({clampConfig:{minWidth:-1,maxWidth:1e10,mobileFactor:2}})');
    return evaluate('clampConfig.minWidth===320 && clampConfig.maxWidth===1600 && clampConfig.mobileFactor===1');
  });
  reset();
  w.localStorage.clear(); d.getElementById('jSaveLocal').click();
  input('advWeight',600,'change');
  test('Advanced select changes autosave after state updates', () => saved().advanced.weight===600);
  d.getElementById('advUnderline').checked=false;
  d.getElementById('advUnderline').dispatchEvent(new w.Event('change',{bubbles:true}));
  test('Advanced checkbox changes autosave', () => saved().advanced.underline===false);
  input('clampBase',20);
  test('Clamp foundation changes autosave', () => saved().base===20);
  input('clampFactor',.7);
  test('Clamp settings autosave', () => saved().clampConfig?.mobileFactor===.7);
  const beforeImport=JSON.stringify(saved());
  test('Import does not overwrite the active saved project', () => {
    evaluate('importConfig({project:"Imported",base:18,advanced:{weight:800}})');
    return JSON.stringify(saved())===beforeImport;
  });
  test('Reset does not overwrite the active saved project', () => {
    reset(); return JSON.stringify(saved())===beforeImport;
  });
  input('bdRadius',18);
  test('Button settings round trip through JSON', () => {
    const json=evaluate('projectJson()'); reset(); evaluate('importConfig('+json+')');
    return evaluate('state.buttonDesign.radius')===18;
  });
  test('Heading weight round trips as a finite number', () => {
    input('advWeight',800,'change');
    const json=evaluate('projectJson()'); reset(); evaluate('importConfig('+json+')');
    return evaluate('adv.weight')===800;
  });
  reset();
  d.getElementById('jNewLocal').click(); input('jProject','Audit project A'); input('jBase',18); d.getElementById('jSaveLocal').click();
  const projectA=d.getElementById('jProjects').value;
  d.getElementById('jNewLocal').click(); input('jProject','Audit project B'); input('jBase',20); d.getElementById('jSaveLocal').click();
  const projectB=d.getElementById('jProjects').value;
  d.getElementById('jProjects').value=projectA; d.getElementById('jLoadLocal').click();
  test('Saved projects load their own settings', () => evaluate('state.base===18 && state.project==="Audit project A"'));
  input('jBase',19);
  test('Switching saved projects routes autosave to the loaded project', () => {
    const stored=JSON.parse(w.localStorage.getItem('dss-v27-projects'));
    return stored[projectA].data.base===19 && stored[projectB].data.base===20;
  });
  const originalConfirm=w.confirm;
  w.confirm=()=>false; d.getElementById('jDeleteLocal').click();
  test('Cancelling deletion preserves the saved project', () => !!JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectA]);
  w.confirm=()=>true; d.getElementById('jDeleteLocal').click();
  test('Confirmed deletion removes only the selected project', () => {
    const stored=JSON.parse(w.localStorage.getItem('dss-v27-projects')); return !stored[projectA] && !!stored[projectB];
  });
  w.confirm=originalConfirm;
  const priorStorage=w.localStorage.getItem('dss-v27-projects');
  w.localStorage.setItem('dss-v27-projects',JSON.stringify({bad:null,missing:{},array:{name:'Bad',updated:'invalid',data:[]},valid:{name:'Valid',updated:'2026-10-19T12:00:00Z',data:{project:'Recovered',base:18}}}));
  const recovery=d.createElement('iframe'); recovery.src='/index.html';
  await new Promise(resolve=>{recovery.onload=resolve;d.body.append(recovery);});
  test('Malformed saved entries do not prevent startup or valid project recovery', () => {
    const rd=recovery.contentDocument, rw=recovery.contentWindow;
    if (rw.__reviewErrors.length || rd.getElementById('jProjects').options.length!==1 || rd.getElementById('jProjects').value!=='valid') return false;
    rd.getElementById('jLoadLocal').click();
    return rw.eval('state.project==="Recovered" && state.base===18') && typeof rw.dssGetContrastChecks==='function';
  });
  recovery.remove(); w.localStorage.setItem('dss-v27-projects',priorStorage);
  reset();
  const originalAlert=w.alert, alerts=[]; w.alert=message=>alerts.push(message);
  await importFile(JSON.stringify({project:'File import',base:21,buttonDesign:{radius:17}}));
  test('JSON file picker imports all modules and clears the file selection', () => evaluate('state.project==="File import" && state.base===21 && state.buttonDesign.radius===17') && !d.getElementById('loadFile').value);
  const beforeBadFile=evaluate('projectJson()');
  await importFile('{broken json');
  test('Invalid JSON reports an error without changing the project', () => alerts.length===1 && evaluate('projectJson()')===beforeBadFile);
  await importFile(' '.repeat(6000001));
  test('Oversized JSON files are rejected without changing the project', () => alerts.at(-1).includes('too large') && evaluate('projectJson()')===beforeBadFile);
  w.alert=originalAlert;

  // These fixtures start through New, rather than inheriting another feature's
  // state. Golden exports come from user edits before save/load/file replacement.
  for(const mode of ['basic','advanced']) {
    const libraryBeforeNew=w.localStorage.getItem('dss-v27-projects');
    d.getElementById('jNewLocal').click();await wait();
    test(mode+' New restores complete defaults and preserves the library',()=>
      evaluate('state.sampleMode==="basic" && state.base===16 && state.advanced.measure===65 && state.buttonDesign.radius===8 && JSON.stringify(clampConfig)===JSON.stringify(CLAMP_DEFAULTS)') &&
      w.localStorage.getItem('dss-v27-projects')===libraryBeforeNew);
    // Seed the codec's normalized optional maps before byte-for-byte round trips.
    // New intentionally omits these maps; import supplies empty override maps.
    w.importConfig({sampleMode:mode});
    input('jProject',mode+' persistence fixture');input('jBase',18);input('jTheme','dark');
    input('advWeight',800,'change');input('bdRadius',18);input('clampFactor',.8);
    input('plan-goal','Find the '+mode+' lesson.');input('plan-content','Tutor supplies lesson text.');
    input('plan-delivery','Tutor reviews the handover.');await wait();
    test(mode+' unsaved editor changes leave saved projects untouched',()=>w.localStorage.getItem('dss-v27-projects')===libraryBeforeNew);
    d.getElementById('jSaveLocal').click();const id=d.getElementById('jProjects').value;
    const json=evaluate('projectJson()'),css=evaluate('cssExport()'),html=evaluate('htmlExport()');
    test(mode+' Save creates a complete detached snapshot',()=>{
      const data=stored()[id].data;
      const pass=data.sampleMode===mode && data.theme==='dark' && data.base===18 &&
        data.advanced.weight===800 && data.buttonDesign.radius===18 && data.clampConfig.mobileFactor===.8 &&
        data.designProcess.content==='Tutor supplies lesson text.' && data.designProcess.delivery==='Tutor reviews the handover.';
      if(!pass)throw Error(JSON.stringify({mode:data.sampleMode,theme:data.theme,base:data.base,weight:data.advanced.weight,radius:data.buttonDesign.radius,clamp:data.clampConfig,content:data.designProcess.content,delivery:data.designProcess.delivery}));
      return true;
    });
    const fresh=d.createElement('iframe');fresh.src='/index.html';
    try {
      await new Promise(resolve=>{fresh.onload=resolve;d.body.append(fresh);});
      const fd=fresh.contentDocument,fw=fresh.contentWindow;
      fd.getElementById('jProjects').value=id;fd.getElementById('jLoadLocal').click();await wait();
      test(mode+' a fresh document loads the saved model and identical exports',()=>{
        const checks={errors:fw.__reviewErrors,json:differences(JSON.parse(fw.eval('projectJson()')),JSON.parse(json)),css:fw.eval('cssExport()')===css,html:fw.eval('htmlExport()')===html,name:fd.getElementById('jProject').value,goal:fd.getElementById('plan-goal').value};
        if(checks.errors.length || checks.json.length || !checks.css || !checks.html || checks.name!==mode+' persistence fixture' || checks.goal!=='Find the '+mode+' lesson.')throw Error(JSON.stringify(checks));
        return true;
      });
    } finally {fresh.remove();}
    const files=[],previousDownload=w.download;
    try{w.download=(name,content,type)=>files.push({name,content,type});d.getElementById('jExportJson').click();}
    finally{w.download=previousDownload;}
    test(mode+' JSON download contains the exact serialized model',()=>files.length===1 && files[0].name==='design-system-studio.json' && files[0].type==='application/json' && files[0].content===json);
    const beforeRejectedFile=w.localStorage.getItem('dss-v27-projects'),fileAlerts=[],previousAlert=w.alert;
    try {
      w.alert=message=>fileAlerts.push(String(message));
      await importFile('{invalid');
      test(mode+' invalid file preserves the complete model and saved snapshots',()=>fileAlerts.length===1 && evaluate('projectJson()')===json && w.localStorage.getItem('dss-v27-projects')===beforeRejectedFile);
      input('jBase',20);
      test(mode+' invalid file retains the active autosave destination',()=>stored()[id].data.base===20);
    } finally {w.alert=previousAlert;}
    const beforeImportedFile=w.localStorage.getItem('dss-v27-projects');
    await importFile(files[0].content);await wait();
    test(mode+' downloaded JSON restores the complete model, exports and preview',()=>{
      const checks={json:differences(JSON.parse(evaluate('projectJson()')),JSON.parse(json)),css:evaluate('cssExport()')===css,html:evaluate('htmlExport()')===html,preview:d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent===css,content:d.getElementById('plan-content').value};
      if(checks.json.length || !checks.css || !checks.html || !checks.preview || checks.content!=='Tutor supplies lesson text.')throw Error(JSON.stringify(checks));
      return true;
    });
    input('jBase',21);input('bdRadius',19);await wait();
    test(mode+' successful file import detaches autosave from every saved project',()=>w.localStorage.getItem('dss-v27-projects')===beforeImportedFile);
    d.getElementById('jProjects').value=id;d.getElementById('jLoadLocal').click();
    const oldConfirm=w.confirm,preReset=evaluate('projectJson()');
    try {
      w.confirm=()=>false;d.getElementById('resetBtn').click();
      test(mode+' cancelling Reset preserves the loaded model',()=>evaluate('projectJson()')===preReset);
      input('jBase',19);
      test(mode+' cancelling Reset preserves the active autosave destination',()=>stored()[id].data.base===19);
      const preConfirmedReset=w.localStorage.getItem('dss-v27-projects');
      w.confirm=()=>true;d.getElementById('resetBtn').click();input('jBase',21);
      test(mode+' confirmed Reset detaches autosave and preserves saved snapshots',()=>evaluate('state.sampleMode')==='basic' && w.localStorage.getItem('dss-v27-projects')===preConfirmedReset);
    } finally {w.confirm=oldConfirm;}
  }
  d.getElementById('jNewLocal').click();await wait();
  const newJson=JSON.parse(evaluate('projectJson()')),newCss=evaluate('cssExport()'),newHtml=evaluate('htmlExport()');
  await importFile(JSON.stringify(newJson));await wait();
  test('A New-project file adds only normalized empty override maps and preserves generated output',()=>{
    const expected={...newJson,semanticOverrides:{light:{},dark:{}},regionPadding:{},backgroundOpacity:{light:{},dark:{}}};
    const changed=differences(JSON.parse(evaluate('projectJson()')),expected);
    if(changed.length)throw Error(JSON.stringify(changed));
    return evaluate('cssExport()')===newCss && evaluate('htmlExport()')===newHtml;
  });
  await importFile(JSON.stringify({schemaVersion:'2.5',project:'Legacy file',base:18,advanced:{tracking:3,measure:71},buttonDesign:{radius:13}}));
  test('Legacy JSON file migrates tracking and sample mode while supplying missing defaults',()=>
    evaluate('state.project==="Legacy file" && state.base===18 && state.sampleMode==="advanced" && state.headingTracking===.03 && state.advanced.measure===71 && state.buttonDesign.radius===13 && JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  test('No project library JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Project library harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
