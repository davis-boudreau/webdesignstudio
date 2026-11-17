"""Independent teaching content, shared website CSS and local learning controls."""
from browser_runner import run_review

HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Learning previews review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe><pre id="results">RUNNING</pre><script>
app.onload=async()=>{
 const w=app.contentWindow,d=w.document,results=[],get=id=>d.getElementById(id),evaluate=code=>w.eval(code);
 const wait=()=>new Promise(r=>setTimeout(r,100));
 const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}catch(e){results.push({name,pass:false,error:String(e.stack||e)});}document.title='Learning previews: '+results.length+' checks';};
 const edit=(id,value)=>{get(id).value=value;get(id).dispatchEvent(new w.Event('input',{bubbles:true}));};
 const configurations=[
  {stage:5,frame:'type-learning-frame',theme:'type-website-theme',quick:'type-generated-css',scope:'typography'},
  {stage:7,frame:'button-learning-frame',theme:'button-website-theme',quick:'button-learning-css',scope:'buttons'},
  {stage:8,frame:'spacing-learning-frame',theme:'spacing-website-theme',quick:'spacing-learning-css',scope:'spacing'},
  {stage:4,frame:'semantic-learning-frame',theme:'semantic-website-theme',quick:'semantic-learning-css',scope:'semantic'}
 ];
 const snapshot=c=>c.scope==='buttons'?w.DSStudio.propertyEditors.buttonSnapshot():c.scope==='semantic'?(()=>{const value=w.DSStudio.propertyEditors.draftSnapshot('palette-backgrounds');return {...value,state:w.DSStudio.paletteBrowser.proposedState(value.state)};})():w.DSStudio.propertyEditors.draftSnapshot(c.scope);
 try{
  await wait();test('Learning previews start without captured errors',()=>!w.__reviewErrors.length);
  test('Typography role control names the ladder and isolated preview frame',()=>get('clampRole').getAttribute('aria-controls').split(/\s+/).every(id=>!!d.getElementById(id)));
  for(const c of configurations){
   w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);w.DSStudio.views.flush();await wait();
   test(c.frame+' has a closed CSS quick view above its sample',()=>get(c.quick).tagName==='DETAILS'&&!get(c.quick).open&&get(c.quick).querySelector('summary').textContent==='Generated CSS and the calculation'&&!!(get(c.quick).compareDocumentPosition(get(c.frame))&w.Node.DOCUMENT_POSITION_FOLLOWING));
   test(c.frame+' uses the exact shared website CSS',()=>get(c.frame).contentDocument.getElementById(c.scope==='spacing'?'spacing-draft-style':'learning-website-css').textContent===w.DSStudio.exports.css(evaluate('state.sampleMode'),snapshot(c)));
   test(c.frame+' local ARIA control references resolve in their own document',()=>[...get(c.frame).contentDocument.querySelectorAll('[aria-controls]')].every(el=>el.getAttribute('aria-controls').split(/\s+/).every(id=>!!el.ownerDocument.getElementById(id))));
  }
  const before=evaluate('projectJson()'),beforeCss=evaluate('cssExport()');
  for(const c of configurations){
   w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();
   get(c.quick).open=true;await wait();test(c.quick+' opening is view-only',()=>evaluate('projectJson()')===before&&evaluate('cssExport()')===beforeCss);get(c.quick).open=false;
  }
  const studio=d.documentElement.dataset.theme,studioFont=w.getComputedStyle(d.body).fontSize;
  for(const mode of ['basic','advanced']){
   w.importConfig({sampleMode:mode});get('jSaveLocal').click();await wait();
   const clean=w.DSStudio.project.normalize(JSON.parse(evaluate('projectJson()')));
   test(mode+' normalized clean snapshot preserves the complete saved stylesheet',()=>w.DSStudio.exports.css(mode,clean)===evaluate('cssExport()'));
   for(const theme of ['light','dark'])for(const width of [320,1440]){
    app.style.width=width+'px';await wait();
    for(const c of configurations){
     w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();
     get(c.theme).value=theme;get(c.theme).dispatchEvent(new w.Event('change',{bubbles:true}));w.DSStudio.views.flush();await wait();
     const frame=get(c.frame),doc=frame.contentDocument,model=snapshot(c),saved=evaluate('projectJson()'),css=evaluate('cssExport()'),storage=w.localStorage.getItem('dss-v27-projects');
     test(mode+' '+theme+' '+width+'px '+c.frame+' consumes exact website CSS and theme',()=>doc.getElementById(c.scope==='spacing'?'spacing-draft-style':'learning-website-css').textContent===w.DSStudio.exports.css(mode,model)&&doc.documentElement.dataset.theme===theme&&get(c.theme).value===theme&&evaluate('state.theme')===theme&&doc.defaultView.getComputedStyle(doc.body).color==='rgb('+[1,3,5].map(i=>parseInt(w.palette(theme,model.state).roles.text.slice(i,i+2),16)).join(', ')+')');
     test(mode+' '+theme+' '+width+'px '+c.frame+' leaves Studio styling and saved state intact',()=>d.documentElement.dataset.theme===studio&&w.getComputedStyle(d.body).fontSize===studioFont&&evaluate('projectJson()')===saved&&evaluate('cssExport()')===css&&w.localStorage.getItem('dss-v27-projects')===storage&&d.documentElement.scrollWidth<=w.innerWidth+1&&frame.getAttribute('sandbox')==='allow-same-origin');
    }
   }
  }
  app.style.width='1440px';w.importConfig({sampleMode:'basic'});get('jSaveLocal').click();await wait();
  const saved=evaluate('projectJson()'),savedCss=evaluate('cssExport()'),savedHtml=evaluate('htmlExport()'),savedStorage=w.localStorage.getItem('dss-v27-projects');
  edit('jBase','20');edit('jSpacing','7');edit('bdRadius','18');get('jSemanticRole').value='surface';get('jSemanticRole').dispatchEvent(new w.Event('change',{bubbles:true}));edit('palette-semantic-hex','#123456');await wait();
  for(const c of configurations){
   w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);w.DSStudio.views.flush();await wait();
   const doc=get(c.frame).contentDocument;
   test(c.frame+' renders its own proposal through the website CSS generator',()=>doc.getElementById(c.scope==='spacing'?'spacing-draft-style':'learning-website-css').textContent===w.DSStudio.exports.css('basic',snapshot(c)));
   test(c.frame+' proposal stays out of saved project, CSS, HTML and storage',()=>evaluate('projectJson()')===saved&&evaluate('cssExport()')===savedCss&&evaluate('htmlExport()')===savedHtml&&w.localStorage.getItem('dss-v27-projects')===savedStorage);
  }
  w.dssShowWizardStep(5,false);get('type-website-theme').value='dark';get('type-website-theme').dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Typography Light/Dark preserves all independent drafts and Studio appearance',()=>get('jBase').value==='20'&&get('jSpacing').value==='7'&&get('bdRadius').value==='18'&&w.DSStudio.propertyEditors.hasDrafts('typography')&&w.DSStudio.propertyEditors.hasDrafts('spacing')&&w.DSStudio.propertyEditors.hasButtonDrafts()&&d.documentElement.dataset.theme===studio);
  for(const theme of ['light','dark']){
   const selector=get('type-website-theme');selector.value=theme;selector.dispatchEvent(new w.Event('input',{bubbles:true}));selector.dispatchEvent(new w.Event('change',{bubbles:true}));w.DSStudio.views.flush();await wait();
   test('Typography native input then change updates the '+theme+' specimen',()=>{const doc=get('type-learning-frame').contentDocument,model=snapshot(configurations[0]);return selector.value===theme&&evaluate('state.theme')===theme&&doc.documentElement.dataset.theme===theme&&doc.defaultView.getComputedStyle(doc.body).color==='rgb('+[1,3,5].map(i=>parseInt(w.palette(theme,model.state).roles.text.slice(i,i+2),16)).join(', ')+')'&&get('jBase').value==='20'&&w.DSStudio.propertyEditors.hasDrafts('typography')&&d.documentElement.dataset.theme===studio;});
  }
  const texts=new Map();for(const c of configurations){w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();texts.set(c.frame,get(c.frame).contentDocument.body.textContent);}
  edit('jProject','</style><img src=x onerror=alert(1)> */');await wait();
  for(const c of configurations){w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();const doc=get(c.frame).contentDocument;test(c.frame+' content stays independent and project strings cannot inject markup',()=>doc.body.textContent===texts.get(c.frame)&&!doc.querySelector('img,script'));}
  const model=evaluate('projectJson()'),exported=evaluate('cssExport()'),row=JSON.stringify(w.DSStudio.statePalettes.sourceFor('--state-default','light'));
  const candidate=w.DSStudio.project.normalize({...JSON.parse(model),primary:'#246789'}),candidateCss=w.DSStudio.exports.css('basic',candidate);
  test('Detached CSS generation uses candidate tokens without changing saved exports or state',()=>candidateCss.includes('--primary-500: #246789;')&&evaluate('projectJson()')===model&&evaluate('cssExport()')===exported);
  test('Detached state palettes do not replace saved UI source metadata',()=>!!row&&JSON.stringify(w.DSStudio.statePalettes.sourceFor('--state-default','light'))===row);
  const restores=[];
  for(const doc of [d,get('previewPage').contentDocument,...configurations.map(c=>get(c.frame).contentDocument)]){
   const head=doc.head,append=head.append;head.append=function(...nodes){for(const node of nodes)if(node.tagName==='LINK'&&node.href?.startsWith('https://fonts.'))node.href=node.rel==='stylesheet'?'/__font_fixture__'+new URL(node.href).search:w.location.origin;return append.apply(this,nodes);};restores.push(()=>head.append=append);
  }
  w.importConfig({sampleMode:'basic',fontSettings:{source:'google',body:'literata',heading:'inter'}});await wait();
  for(const c of configurations){w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();const doc=get(c.frame).contentDocument;await doc.fonts.load('400 16px "Literata"');test(c.frame+' loads the selected website font into its own document',()=>!!doc.querySelector('link[data-dss-learning-font][rel=stylesheet]')&&[...doc.fonts].some(face=>face.family.includes('Literata')&&face.status==='loaded'));}
  const fontProject=evaluate('projectJson()'),fontCss=evaluate('cssExport()');get('fontFallback').click();await wait();
  for(const c of configurations){w.dssShowWizardStep(c.stage,false);if(c.stage===4)w.DSStudio.paletteWorkspace.show('semantics',false);await wait();const doc=get(c.frame).contentDocument;test(c.frame+' supports the optional system-fallback comparison',()=>{const value={family:doc.defaultView.getComputedStyle(doc.body).fontFamily,links:doc.querySelectorAll('link[data-dss-learning-font]').length,fallback:w.DSStudio.fonts.showFallback,checked:get('fontFallback').checked,disabled:get('fontFallback').disabled};if(value.family!==w.DSStudio.fonts.resolve(true,snapshot(c).state).body.replaceAll("'",'"')||value.links)throw Error(JSON.stringify(value));return true;});}
  test('Font comparison preserves selected font exports and the saved project',()=>evaluate('projectJson()')===fontProject&&evaluate('cssExport()')===fontCss&&fontCss.includes('--font-body: "Literata"'));
  restores.forEach(restore=>restore());
  w.importConfig({sampleMode:'basic',colourTransparency:{'light:text':true,'light:focus':true}});w.dssShowWizardStep(5,false);await wait();
  for(const appearance of ['light','dark']){if(d.documentElement.dataset.theme!==appearance)get('themeToggle').click();await wait();const doc=get('type-learning-frame').contentDocument,label=doc.querySelector('.type-sample-role'),style=doc.defaultView.getComputedStyle(label);test(appearance+' Studio keeps Typography role labels readable when project text is transparent',()=>style.color===w.getComputedStyle(d.body).color&&!style.backgroundColor.endsWith(', 0)')&&doc.defaultView.getComputedStyle(doc.body).color.endsWith(', 0)')&&doc.documentElement.dataset.theme==='light');}
  w.dssShowWizardStep(4,false);w.DSStudio.paletteWorkspace.show('semantics',false);await wait();
  const semantic=get('semantic-learning-frame').contentDocument;
  test('Semantic region editing controls retain Studio colours with transparent project text',()=>[...semantic.querySelectorAll('[data-background-pick]')].every(el=>semantic.defaultView.getComputedStyle(el).color===w.getComputedStyle(d.body).color&&!semantic.defaultView.getComputedStyle(el).backgroundColor.endsWith(', 0)')));
  test('Learning preview checks finish without captured errors',()=>!w.__reviewErrors.length);
 }catch(e){results.push({name:'Learning preview harness completes',pass:false,error:String(e.stack||e)});}
 document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};</script>'''

if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
