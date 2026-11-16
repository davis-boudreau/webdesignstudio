"""Shared property controls: draft boundaries, save/discard and focused preview."""
from browser_runner import run_review

HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Property actions review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
 const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code),get=id=>d.getElementById(id);
 const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
 const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}catch(error){results.push({name,pass:false,error:String(error.stack||error)});}document.title='Property review '+results.length;};
 const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
 const edit=(id,value,type='input')=>{const control=get(id);if(control.type==='checkbox')control.checked=value;else control.value=value;control.dispatchEvent(new w.Event(type,{bubbles:true}));};
 const actions=id=>d.querySelector('[data-property-actions="'+id+'"]');
 try{
 test('Shared property editors initialize without errors',()=>!!w.DSStudio.propertyEditors && !w.__reviewErrors.length);
 const cases=[['palette-roles','jPrimary','#246789','state.primary'],['palette-shades','jRamp','mix','state.method'],['palette-backgrounds','page-background-hex','#345678','state.semanticOverrides.light.background'],['palette-components','bdHover','#345678','state.buttonDesign.overrides.primary.hover'],['palette-review','palette-status-colour','#345678','state.semanticOverrides.light.success'],['brief','plan-goal','A new purpose','state.designProcess.goal'],['prototype','plan-prototypeTask','A new visitor task','state.designProcess.prototypeTask'],['destination-outline','plan-pages','Home > Child','state.designProcess.pages'],['typography','jBase','20','state.base'],['typography','jRatio','1.3','state.ratio'],['typography','jHeadingLeading','1.4','state.headingLeading'],['typography','clampFactor','.8','clampConfig.mobileFactor'],['button-workspace','bdRadius','18','state.buttonDesign.radius'],['spacing','jSpacing','7','state.spacing'],['responsive','responsive-gutter','30','state.responsiveDesign.gutter'],['accessibility','advReduce',true,'state.advanced.reduce']];
 for(const [scope,id,value,path]of cases){
  evaluate('resetStudio()');await wait();get('jSaveLocal').click();
  const before=evaluate('projectJson()'),css=evaluate('cssExport()'),html=evaluate('htmlExport()'),storage=w.localStorage.getItem('dss-v27-projects');
  edit(id,value);await wait();
  test(scope+' draft stays out of project, CSS, HTML and storage',()=>evaluate('projectJson()')===before && evaluate('cssExport()')===css && evaluate('htmlExport()')===html && w.localStorage.getItem('dss-v27-projects')===storage && !actions(scope).querySelector('button').disabled);
  actions(scope).querySelectorAll('button')[1].click();await wait();
  test(scope+' Discard restores only the properties',()=>evaluate('projectJson()')===before && actions(scope).querySelectorAll('button')[1].disabled);
  edit(id,value);actions(scope).querySelector('button').click();await wait();
  test(scope+' Save commits the intended value and autosaves',()=>(typeof evaluate(path)==='number'?evaluate(path)===Number(value):String(evaluate(path))===String(value)) && evaluate('projectJson()')!==before && w.localStorage.getItem('dss-v27-projects')!==storage);
 }

 evaluate('resetStudio()');await wait();
 edit('jPrimary','#234567');edit('jBase','20');
 const concurrent=evaluate('projectJson()');actions('typography').querySelector('button').click();await wait();
 test('Saving body type leaves an unrelated palette draft unsaved',()=>evaluate('state.base')===20 && evaluate('state.primary')==='#004780' && get('jPrimary').value==='#234567');
 actions('palette-roles').querySelectorAll('button')[1].click();await wait();
 test('Discarding a palette draft preserves the saved typography',()=>evaluate('state.base')===20 && evaluate('state.primary')==='#004780' && get('jPrimary').value==='#004780');
 edit('jPrimary','#234567');evaluate("state.primary='#abcdef';apply()");await wait();
 test('An external source change invalidates stale property drafts',()=>get('jPrimary').value==='#abcdef' && actions('palette-roles').querySelectorAll('button')[1].disabled);
 edit('jPrimary','#234567');evaluate('importConfig(JSON.parse(projectJson()))');await wait();
 test('Project replacement clears property drafts',()=>get('jPrimary').value==='#abcdef' && actions('palette-roles').querySelectorAll('button')[1].disabled);
 evaluate('resetStudio()');await wait();
 edit('page-background-hex','red;/*');actions('palette-backgrounds').querySelector('button').click();await wait();
 test('Invalid property values cannot reach model or exports',()=>!evaluate('state.semanticOverrides?.light?.background') && !evaluate('cssExport()').includes('red;/*') && get('page-background-hex').getAttribute('aria-invalid')==='true');
 actions('palette-backgrounds').querySelectorAll('button')[1].click();
 edit('fontSource','google','change');await wait();
 test('A staged font source enables controls without changing saved font links',()=>!get('fontGoogleOptions').hidden && evaluate('state.fontSettings.source')==='system' && !d.querySelector('link[data-dss-font]'));
 actions('typography').querySelectorAll('button')[1].click();await wait();
 test('Discard restores saved font-source controls',()=>get('fontGoogleOptions').hidden && get('fontSource').value==='system');

 edit('jPrimaryBrand','#FFFFFF','change');await wait();
 test('A proposed brand assignment remains selected while its anchor stays unsaved',()=>get('jPrimaryBrand').value==='#FFFFFF' && get('jPrimary').value==='#ffffff' && evaluate('state.primary')==='#004780');
 actions('palette-roles').querySelectorAll('button')[1].click();
 const legacy='Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact';
 w.importConfig({sampleMode:'basic',designProcess:{pages:legacy}});await wait();
 test('Legacy outlines display the resolved sample without rewriting stored data',()=>get('plan-pages').value===w.DSStudio.process.samplePages('basic') && evaluate('state.designProcess.pages')===legacy);
 const outlineBefore=evaluate('projectJson()');edit('plan-pages','Root > Branch > Detail > Too deep');actions('destination-outline').querySelector('button').click();await wait();
 test('Invalid outline drafts show validation and preserve the saved structure',()=>!get('plan-pages').checkValidity() && evaluate('projectJson()')===outlineBefore && get('plan-sample-status').textContent.includes('three information levels'));
 actions('destination-outline').querySelectorAll('button')[1].click();await wait();
 test('Discard clears outline validation and restores the resolved saved outline',()=>get('plan-pages').checkValidity() && get('plan-pages').value===w.DSStudio.process.samplePages('basic'));
 const semanticBefore=evaluate('projectJson()');edit('palette-semantic-hex','#345678');actions('palette-semantics').querySelector('button').click();await wait();
 test('Shared semantic Save retains the contrast-review boundary',()=>get('colourRepair').open && evaluate('projectJson()')===semanticBefore && get('repairHex').value==='#345678');
 get('repairCancel').click();await wait();
 test('Cancelling semantic review leaves the saved project unchanged',()=>evaluate('projectJson()')===semanticBefore && !get('colourRepair').open);
 actions('palette-semantics').querySelectorAll('button')[1].click();
 edit('jBase','19');
 for(const theme of ['light','dark'])for(const width of [320,390,1440]){
  app.style.width=width+'px';evaluate("state.theme='"+theme+"';apply()");await wait();
  for(const [id,stage,substage]of [['palette-roles',4,'roles'],['palette-shades',4,'shades'],['palette-backgrounds',4,'backgrounds'],['palette-components',4,'components'],['palette-review',4,'review'],['palette-semantics',4,'semantics'],['typography',5,'body'],['brief',0],['button-workspace',7],['spacing',8],['responsive',9],['accessibility',10],['content',1],['sitemap',1]]){
   w.dssShowWizardStep(stage,false);
   if(stage===4)w.DSStudio.paletteWorkspace.show(substage,false);
   if(stage===5)w.DSStudio.typographyWorkspace.show(substage,false);
   if(id==='sitemap'){get('sitemap-source').value='custom';get('sitemap-source').dispatchEvent(new w.Event('change',{bubbles:true}));}
   await wait();const bar=actions(id),button=bar.querySelector('[data-property-preview]'),before=evaluate('projectJson()'),storage=w.localStorage.getItem('dss-v27-projects'),doc=get('previewPage').contentDocument;
   button.click();await wait();
   test(theme+' '+width+'px '+id+' preview keeps source, focuses result and preserves project',()=>{const checks={source:get(w.DSStudio.stages[stage].lesson).open,result:get('studio-section-4').open,focus:d.activeElement===get('previewShell'),sections:d.querySelectorAll('#main > .studio-section[open]').length===2,project:evaluate('projectJson()')===before,storage:w.localStorage.getItem('dss-v27-projects')===storage,document:get('previewPage').contentDocument===doc,draft:get('jBase').value==='19',heading:get('studio-section-4').getBoundingClientRect().top>=d.querySelector('.topbar').getBoundingClientRect().bottom-1};if(!Object.values(checks).every(Boolean))throw Error(JSON.stringify({checks,top:get('studio-section-4').getBoundingClientRect().top,header:d.querySelector('.topbar').getBoundingClientRect().bottom}));return true;});
   w.dssShowWizardStep(stage,false);if(stage===4)w.DSStudio.paletteWorkspace.show(substage,false);if(stage===5)w.DSStudio.typographyWorkspace.show(substage,false);await wait();
   test(theme+' '+width+'px '+id+' shared actions fit the editor',()=>[...bar.querySelectorAll('button')].every(control=>{const box=control.getBoundingClientRect();return box.width>0 && box.height>=44 && box.left>=0 && box.right<=w.innerWidth+1;}));
  }
 }
 test('Shared property checks finish without JavaScript errors',()=>!w.__reviewErrors.length);
 }catch(error){results.push({name:'Property harness completed',pass:false,error:String(error.stack||error)});}
 finish();
};
</script>'''

if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
