"""Accordion opening, visual-step lessons and theme/save consistency."""
from browser_runner import run_review

HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Interaction consistency review</title>
<iframe id="app" style="width:1440px;height:1100px" src="/index.html"></iframe><pre id="results">RUNNING</pre><script>
app.onload=async()=>{
 const w=app.contentWindow,d=w.document,results=[],get=id=>d.getElementById(id),evaluate=code=>w.eval(code),wait=(ms=120)=>new Promise(r=>setTimeout(r,ms));
 const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}catch(e){results.push({name,pass:false,error:String(e.stack||e)});}document.title='Interaction consistency: '+results.length+' checks';};
 const edit=(id,value,type='input')=>{get(id).value=value;get(id).dispatchEvent(new w.Event(type,{bubbles:true}));};
 const choose=(id,value)=>{get(id).value=value;for(const type of ['input','change'])get(id).dispatchEvent(new w.Event(type,{bubbles:true}));w.DSStudio.views.flush();};
 const selectedTheme=()=>evaluate('state.theme');
 try{
  await wait();test('New visual learning modules start without errors',()=>!!w.DSStudio.stepLearning&&w.DSStudio.stepLearning.views.length===8&&!w.__reviewErrors.length);
  for(const mode of ['basic','advanced']){
   w.importConfig({sampleMode:mode});await wait();
   for(const view of w.DSStudio.stepLearning.views){
    w.dssShowWizardStep(view.stage,false);if(view.stage===4)w.DSStudio.paletteWorkspace.show(view.id.slice('palette-'.length),false);await wait();
    test(mode+' '+view.id+' CSS quick view precedes the specimen and starts closed',()=>!get(view.id+'-learning-css').open&&get(view.id+'-learning-css').querySelector('summary').textContent==='Generated CSS and the calculation'&&!!(get(view.id+'-learning-css').compareDocumentPosition(view.preview.frame)&w.Node.DOCUMENT_POSITION_FOLLOWING));
    for(const theme of ['dark','light']){
     choose(view.id+'-website-theme',theme);await wait();const doc=view.preview.document;
     test(mode+' '+view.id+' native theme choice changes actual specimen colours and JSON',()=>doc.documentElement.dataset.theme===theme&&view.theme.value===theme&&selectedTheme()===theme&&JSON.parse(evaluate('projectJson()')).theme===theme&&doc.defaultView.getComputedStyle(doc.body).color==='rgb('+[1,3,5].map(i=>parseInt(w.palette(theme).roles.text.slice(i,i+2),16)).join(', ')+')');
     test(mode+' '+view.id+' specimen and quick view use the same full CSS',()=>get(view.id+'-learning-code').textContent===doc.getElementById('learning-website-css').textContent&&get(view.id+'-learning-calculation').textContent.length>90&&!!doc.querySelector('[data-learning-selected]'));
     if(view.stepTheme){choose(view.stepTheme.id,theme==='dark'?'light':'dark');await wait();test(mode+' '+view.id+' sidebar theme also changes its learning specimen',()=>view.theme.value===view.stepTheme.value&&doc.documentElement.dataset.theme===view.stepTheme.value);choose(view.id+'-website-theme',theme);await wait();}
    }
   }
   for(const [stage,id,frame]of [[5,'type-website-theme','type-learning-frame'],[7,'button-website-theme','button-learning-frame'],[8,'spacing-website-theme','spacing-learning-frame'],[4,'semantic-website-theme','semantic-learning-frame'],[4,'palette-theme','semantic-learning-frame']]){
    w.dssShowWizardStep(stage,false);if(stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();
    for(const theme of ['dark','light']){choose(id,theme);await wait();test(mode+' '+id+' native selection updates the learning page',()=>get(frame).contentDocument.documentElement.dataset.theme===theme&&get(id).value===theme&&selectedTheme()===theme);}
   }
  }
  w.importConfig({sampleMode:'basic'});w.dssShowWizardStep(9,false);await wait();
  const saved=evaluate('projectJson()');edit('advGap','27');await wait();
  let view=w.DSStudio.stepLearning.views.find(item=>item.id==='responsive');
  test('Responsive proposal uses the real grid CSS and highlights the grid',()=>view.preview.document.defaultView.getComputedStyle(view.preview.document.querySelector('.card-grid')).gap==='27px'&&view.preview.document.querySelector('.card-grid').hasAttribute('data-learning-selected')&&evaluate('projectJson()')===saved);
  choose('responsive-step-theme','dark');await wait();
  test('Theme changes keep responsive proposals separate from saved properties',()=>get('advGap').value==='27'&&w.DSStudio.propertyEditors.hasDrafts('responsive')&&evaluate('state.advanced.gap')!==27&&view.preview.document.documentElement.dataset.theme==='dark');
  d.querySelector('[data-responsive-field="gutter"]').focus({preventScroll:true});get('responsive-step-theme').focus({preventScroll:true});choose('responsive-step-theme','light');await wait();test('Theme control focus preserves the selected layout component',()=>view.preview.document.querySelector('[data-learning-part="layout"]').hasAttribute('data-learning-selected'));
  w.DSStudio.propertyEditors.saveFor(get('advGap'));await wait();
  w.dssShowWizardStep(10,false);edit('advHeight','60');edit('advFocus','5');edit('advState','invalid');await wait();view=w.DSStudio.stepLearning.views.find(item=>item.id==='accessibility');
  test('Accessibility proposal includes native inputs, buttons, links and validation',()=>view.preview.document.defaultView.getComputedStyle(view.preview.document.querySelector('.input')).minHeight==='60px'&&view.preview.document.querySelector('.input').getAttribute('aria-invalid')==='true'&&view.preview.document.querySelector('[data-learning-part="links"]')&&view.preview.document.querySelector('[data-learning-selected]'));
  w.DSStudio.propertyEditors.saveFor(get('advHeight'));await wait();
  const perTheme={light:'#123456',dark:'#FEDCBA'};
  for(const theme of ['light','dark']){
   w.dssShowWizardStep(4,false);w.DSStudio.paletteWorkspace.show('semantics',false);choose('semantic-website-theme',theme);edit('jSemanticRole','text','change');edit('palette-semantic-hex',perTheme[theme]);
   // The semantic role editor owns its explicit Apply action.
   get('jSemanticEdit').click();await wait();get('repairApply').click();await wait();
  }
  test('Both theme overrides coexist in the generated CSS',()=>evaluate('state.semanticOverrides.light.text')===perTheme.light&&evaluate('state.semanticOverrides.dark.text')===perTheme.dark&&evaluate('cssExport()').includes(perTheme.light)&&evaluate('cssExport()').includes(perTheme.dark));
  get('jSaveLocal').click();const active=get('jProjects').value,stored=JSON.parse(w.localStorage.getItem('dss-v27-projects'))[active].data;
  const files=[],previousDownload=w.download;try{w.download=(name,content,type)=>files.push({name,content,type});get('jExportJson').click();}finally{w.download=previousDownload;}
  const exported=JSON.parse(files[0].content);
  test('Local project and downloaded JSON retain selected theme and both colour configurations',()=>stored.theme==='dark'&&exported.theme==='dark'&&exported.semanticOverrides.light.text===perTheme.light&&exported.semanticOverrides.dark.text===perTheme.dark&&exported.advanced.gap===27&&exported.advanced.height===60);
  w.importConfig(exported);w.dssShowWizardStep(10,false);await wait();
  test('JSON reimport restores theme controls, component configuration and learning preview',()=>get('accessibility-step-theme').value==='dark'&&get('accessibility-learning-frame').contentDocument.documentElement.dataset.theme==='dark'&&get('advHeight').value==='60'&&get('advGap').value==='27');
  w.dssShowWizardStep(4,false);w.DSStudio.paletteWorkspace.show('components',false);await wait();
  for(const family of ['cards','inputs','links','buttons']){edit('palette-component-family',family,'change');await wait();const doc=get('palette-components-learning-frame').contentDocument;test('Palette '+family+' selection highlights matching components in its specimen',()=>[...doc.querySelectorAll('[data-learning-part="'+family+'"]')].every(el=>el.hasAttribute('data-learning-selected')));}
  w.DSStudio.paletteWorkspace.show('brand',false);await wait();const brandJson=evaluate('projectJson()'),brandRow=get('jBrandEditor').querySelector('[data-brand-id]:not([hidden])'),brandInput=brandRow.querySelector('[data-brand-field="hex"]');brandInput.value='#345678';brandInput.dispatchEvent(new w.Event('input',{bubbles:true}));await wait();
  test('Brand proposal paints its selected swatch without changing saved JSON',()=>get('palette-brand-learning-frame').contentDocument.getElementById('learning-website-css').textContent.includes('--brand-'+brandRow.dataset.brandId+': #345678')&&get('palette-brand-learning-status').textContent.startsWith('Proposed')&&evaluate('projectJson()')===brandJson);
  brandRow.querySelector('[data-brand-discard]').click();await wait();test('Discard restores the brand learning sample and saved model',()=>!get('palette-brand-learning-code').textContent.includes('--brand-'+brandRow.dataset.brandId+': #345678')&&evaluate('projectJson()')===brandJson);
  w.DSStudio.paletteWorkspace.show('shades',false);get('palette-stage-shades').querySelector('[data-palette-family="secondary"]').click();await wait();
  test('Selected shade family displays its actual generated token swatches',()=>get('palette-shades-learning-frame').contentDocument.querySelector('.step-learning-swatches').textContent.includes('--secondary-500')&&!get('palette-shades-learning-frame').contentDocument.querySelector('.step-learning-swatches').textContent.includes('--primary-500'));
  w.DSStudio.paletteWorkspace.show('semantics',false);edit('jSemanticRole','focus','change');await wait();
  test('Semantic selection highlights the matching focused field inside its preview',()=>get('semantic-learning-frame').contentDocument.querySelector('.semantic-field-sample').hasAttribute('data-learning-selected'));
  // Exercise actual native summary activation, nested scroll containers and late
  // layout changes in both Studio appearances and narrow/wide layouts.
  for(const width of [1440,320])for(const appearance of ['light','dark']){
   app.style.width=width+'px';if(d.documentElement.dataset.theme!==appearance)get('themeToggle').click();w.dssShowWizardStep(9,false);await wait();
   const panel=get('responsiveDesign').querySelector(':scope > .panel'),fixture=d.createElement('section');fixture.innerHTML='<div style="height:500px"></div><details><summary>Open a learning area</summary><div style="height:1100px">Long learning content</div></details><div style="height:1100px"></div>';panel.append(fixture);
   const details=fixture.querySelector('details'),summary=details.querySelector('summary'),json=evaluate('projectJson()');summary.focus({preventScroll:true});w.setTimeout(()=>fixture.firstElementChild.style.height='640px',60);summary.click();await wait(300);
   test(width+' '+appearance+' opening an accordion aligns its summary below the header',()=>details.open&&Math.abs(summary.getBoundingClientRect().top-d.querySelector('.topbar').getBoundingClientRect().bottom-8)<3&&d.activeElement===summary&&evaluate('projectJson()')===json);
   details.open=false;await wait();const before=w.scrollY;details.open=true;await wait();
   test(width+' '+appearance+' programmatic opening preserves scroll and project',()=>Math.abs(w.scrollY-before)<3&&evaluate('projectJson()')===json);
   details.open=false;await wait();summary.click();get('responsive-step-theme').focus({preventScroll:true});w.scrollTo({top:0,behavior:'instant'});await wait();
   test(width+' '+appearance+' later focus cancels delayed accordion alignment',()=>w.scrollY<3&&d.activeElement===get('responsive-step-theme'));
   details.open=false;await wait();summary.focus({preventScroll:true});summary.click();summary.dispatchEvent(new w.WheelEvent('wheel',{bubbles:true}));w.scrollTo({top:0,behavior:'instant'});await wait(300);test(width+' '+appearance+' manual scrolling cancels settling alignment without changing focus',()=>w.scrollY<3&&d.activeElement===summary);
   fixture.remove();
   const scroller=d.createElement('div');scroller.style.cssText='height:160px;overflow-y:auto;';scroller.innerHTML='<div style="height:400px"></div><details><summary>Nested scrolling lesson</summary><div style="height:600px"></div></details><div style="height:600px"></div>';panel.append(scroller);const nested=scroller.querySelector('summary');nested.focus({preventScroll:true});nested.click();await wait();
   test(width+' '+appearance+' accordion in a scrolling panel reveals the opened area',()=>Math.abs(nested.getBoundingClientRect().top-scroller.getBoundingClientRect().top-8)<3&&scroller.scrollTop>0);scroller.remove();
  }
  test('Consistency checks finish without runtime errors',()=>!w.__reviewErrors.length);
 }catch(e){results.push({name:'Consistency harness completes',pass:false,error:String(e.stack||e)});}
 document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};</script>'''

if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
