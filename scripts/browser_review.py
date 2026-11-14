"""Dependency-free Chrome smoke tests. Run: python scripts/browser_review.py.

Uses a temporary browser profile and a local-only server; saved user projects
and the user's normal browser session are never opened.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Browser review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload = async () => {
  const w = app.contentWindow, d = w.document, results = [];
  window.addEventListener('unhandledrejection', event => {
    results.push({name:'Browser harness completed without an unhandled exception',pass:false,error:String(event.reason?.stack || event.reason)});
    document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  });
  const evaluate = code => w.eval(code);
  const test = (name, fn) => {
    try { if (!fn()) throw Error('Assertion failed'); results.push({name, pass:true}); }
    catch (e) { results.push({name, pass:false, error:String(e)}); }
    document.title='Browser review: '+results.length+' checks; last: '+name;
  };
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
  // Most historical feature fixtures exercise the complete Advanced sample.
  // Default/reset behavior is checked separately through resetStudio directly.
  const reset = () => {evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc = () => d.getElementById('previewPage').contentDocument;
  const previewWindow = () => d.getElementById('previewPage').contentWindow;
  const saved = () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data;
  const wait = (ms=100) => new Promise(resolve => setTimeout(resolve,ms));
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
  test('No startup JavaScript errors', () => !w.__reviewErrors.length);
  test('New projects start with Basic on the left and Advanced on the right',()=>evaluate('state.sampleMode')==='basic' && [...d.querySelectorAll('[aria-label="Website sample complexity"] [role="tab"]')].map(el=>el.id).join(',')==='dockModeBasic,dockModeAdvanced' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && d.getElementById('dockModeBasic').tabIndex===0 && d.getElementById('dockModeAdvanced').tabIndex===-1 && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')==='dockModeBasic');
  d.getElementById('dockModeAdvanced').click();await wait();
  // Studio appearance is a browser preference; project theme and samples are independent.
  const appearanceToggle=d.getElementById('themeToggle');
  const styleSnapshot=element=>{
    const cs=w.getComputedStyle(element);
    return ['color','backgroundColor','fontFamily','fontSize','lineHeight','letterSpacing','borderRadius','borderColor'].map(key=>cs[key]).join('|');
  };
  const chromeSnapshot=()=>[d.body,d.querySelector('.topbar'),d.querySelector('.sidebar .panel'),d.getElementById('journeyTitle'),d.getElementById('inspectorToggle'),d.getElementById('previewTheme')].map(styleSnapshot).join('~');
  test('Studio starts light with a labelled appearance toggle',()=>d.documentElement.dataset.theme==='light' && appearanceToggle.textContent==='Studio: Light' && appearanceToggle.getAttribute('aria-pressed')==='false' && appearanceToggle.getAttribute('aria-label').includes('Studio appearance'));
  for(const studio of ['light','dark']) {
    if(d.documentElement.dataset.theme!==studio)appearanceToggle.click();
    const fixedChrome=chromeSnapshot();
    for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
      d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();
      input('previewTheme',theme,'change');await wait();
      test(studio+' Studio supports '+theme+' '+mode+' page independently',()=>d.documentElement.dataset.theme===studio && previewDoc().documentElement.dataset.theme===theme && d.getElementById('jTheme').value===theme && d.getElementById('dockTheme').value===theme && chromeSnapshot()===fixedChrome);
      test(studio+' Studio keeps '+theme+' '+mode+' design examples in project colours',()=>{
        const sample=w.getComputedStyle(d.getElementById('bdSingle'));
        return sample.getPropertyValue('--text').trim()===evaluate('palette().roles.text') && sample.backgroundColor===evaluate("'rgb('+hexRgb(palette().roles['surface-muted']).join(', ')+')'");
      });
    }
    input('jBase',22);input('jRadius',28);input('jSpacing',8);input('jPrimary','#883366');input('jLeading',1.9);
    input('advColor_success','#661144');d.getElementById('advUnderline').checked=false;d.getElementById('advUnderline').dispatchEvent(new w.Event('change',{bubbles:true}));
    test(studio+' Studio type, controls and surfaces survive project foundation edits',()=>chromeSnapshot()===fixedChrome && w.getComputedStyle(d.body).fontSize==='16px' && w.getComputedStyle(d.getElementById('mobileType').querySelector('.sample')).fontSize!=='16px');
    reset();await wait();
  }
  // Verify preference persistence in a fresh document, never the user's profile.
  const beforeAppearance=evaluate('[projectJson(),htmlExport(),cssExport()]');
  const appearanceDocument=previewDoc(),appearanceCssNode=d.getElementById('dockCss').firstChild;
  appearanceToggle.focus();appearanceToggle.click();await wait(); // Dark -> Light.
  test('Studio changes preserve project, exports, inspector text, focus and preview document',()=>JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'))===JSON.stringify(beforeAppearance) && previewDoc()===appearanceDocument && d.getElementById('dockCss').firstChild===appearanceCssNode && d.activeElement===appearanceToggle);
  appearanceToggle.click();
  const nativePreferenceWrite=w.Storage.prototype.setItem;
  w.Storage.prototype.setItem=function(){throw new w.DOMException('Storage blocked','SecurityError');};
  appearanceToggle.click();
  test('Studio appearance works when preference storage is blocked',()=>d.documentElement.dataset.theme==='light' && !w.__reviewErrors.length);
  appearanceToggle.click();w.Storage.prototype.setItem=nativePreferenceWrite;
  const fresh=d.createElement('iframe');fresh.style.display='none';
  const loadFresh=()=>new Promise(resolve=>{fresh.onload=resolve;fresh.src='/index.html?appearance-review='+Math.random();if(!fresh.isConnected)d.body.append(fresh);});
  await loadFresh();
  test('A fresh document restores dark Studio appearance while its new project stays light',()=>fresh.contentDocument.documentElement.dataset.theme==='dark' && fresh.contentWindow.eval('state.theme')==='light' && fresh.contentDocument.getElementById('themeToggle').getAttribute('aria-pressed')==='true');
  w.localStorage.setItem('dss-studio-appearance','<img src=x onerror=alert(1)>');await loadFresh();
  test('Invalid stored Studio appearance falls back to light without inserting content',()=>fresh.contentDocument.documentElement.dataset.theme==='light' && fresh.contentDocument.getElementById('themeToggle').textContent==='Studio: Light' && !fresh.contentDocument.querySelector('img[onerror]'));
  fresh.remove();
  if(d.documentElement.dataset.theme!=='light')appearanceToggle.click();
  for(const width of [320,390,1440])for(const studio of ['light','dark']) {
    app.style.width=width+'px';if(d.documentElement.dataset.theme!==studio)appearanceToggle.click();await wait();
    test(studio+' Studio appearance controls fit '+width+'px with visible focus',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && appearanceToggle.getBoundingClientRect().height>=44 && appearanceToggle.getBoundingClientRect().right<=w.innerWidth+1 && w.getComputedStyle(appearanceToggle).outlineStyle!=='none');
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')appearanceToggle.click();reset();await wait();

  test('Every exported token has a source in its wizard step or centre Palette workspace', () => w.dssReadTokens().length>150 && w.dssReadTokens().every(row=>{
    const source=w.dssTokenSource(row), control=source && d.getElementById(source.control);
    return control && (control.closest('[data-journey-pane]')?.dataset.journeyPane===String(source.step) || (source.step===4 && d.getElementById('palette-workspace').contains(control)) || (source.step===5 && d.getElementById('typography-workspace').contains(control)));
  }));
  test('Derived token families identify their foundation instead of arbitrary overrides', () => ['--space-6','--primary-700','--text-step-4','--text-h1','--font-ui','--heading-tracking','--button-progress-animation'].every(name=>/Derived|Alias/.test(w.dssTokenSource({name}).mode)));
  test('Font, responsive, layout and interaction settings live in their owning workspaces', () => [['fontSource',5],['clampMinWidth',5],['advWeight',5],['advColumns',9],['advBorder',8],['jSpacing',8],['advState',10],['advReduce',10]].every(([id,step])=>d.getElementById(id).closest('[data-journey-pane]')?.dataset.journeyPane===String(step) || (step===5 && d.getElementById('typography-workspace').contains(d.getElementById(id)))));
  reset(); d.querySelector('[data-journey-step="0"]').click(); await wait();
  revealAll(); await wait();
  test('Neutral CSS, JSON, and HTML exports', () => !/nscc/i.test(evaluate('cssExport()+projectJson()+htmlExport()')));
  test('Live inspector matches CSS export', () => d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  test('Every label points to a control', () => [...d.querySelectorAll('label[for]')].every(el=>d.getElementById(el.htmlFor)));
  test('Internal anchors resolve', () => [...d.querySelectorAll('a[href^="#"]')].every(el=>d.getElementById(el.hash.slice(1))));
  test('HTML IDs are unique', () => {
    const ids=[...d.querySelectorAll('[id]')].map(el=>el.id); return ids.length===new Set(ids).size;
  });
  input('jTheme','dark');
  test('Page theme and guided controls synchronize independently of Studio appearance', () => d.documentElement.dataset.projectTheme==='dark' && d.documentElement.dataset.theme==='light' && d.getElementById('jTheme').value==='dark');
  test('Dark theme exports both theme blocks', () => evaluate('cssExport().includes(\'[data-theme="dark"]\') && cssExport().includes("--background: #F3F6FA")'));
  // Detailed import validation, autosave and round trips: project_library_review.py.
  reset();
  test('CSS generation reads both themes without writing project state', () => evaluate(`(() => {
    const theme=Object.getOwnPropertyDescriptor(state,'theme');
    Object.defineProperty(state,'theme',{configurable:true,get:()=>theme.value,set:()=>{throw Error('Export changed theme');}});
    try { return cssExport().includes('[data-theme="dark"]'); }
    finally { Object.defineProperty(state,'theme',theme); }
  })()`));
  test('Unchanged exports preserve selectable code text in both inspectors', () => {
    const centre=d.getElementById('codeView').firstChild, dock=d.getElementById('dockCss').firstChild;
    evaluate('renderCode()');
    return d.getElementById('codeView').firstChild===centre && d.getElementById('dockCss').firstChild===dock;
  });
  input('bdSize','lg');
  test('Exported HTML preserves selected button size', () => evaluate('htmlExport().includes("ds-button--lg")'));
  input('jTheme','dark');
  test('Exported HTML preserves selected theme', () => evaluate('htmlExport().includes(\'data-theme="dark"\')'));
  const darkCss=evaluate('cssExport()');
  input('jTheme','light');
  test('Button CSS theme definitions are independent of active theme', () => evaluate('cssExport()')===darkCss);
  input('advAlign','center','change'); input('advOpacity',60);
  const exported=d.createElement('iframe');
  exported.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
  await new Promise(resolve=>{exported.onload=resolve;d.body.append(exported);});
  test('Exported card opacity matches controls', () => Number(exported.contentWindow.getComputedStyle(exported.contentDocument.querySelector('.card')).opacity)===.6);
  test('Exported grid alignment matches controls', () => exported.contentWindow.getComputedStyle(exported.contentDocument.querySelector('.card-grid')).alignItems==='center');
  test('Exported CSS contains no undefined or nonfinite values', () => !/undefined|NaN|Infinity/.test(evaluate('cssExport()')));
  exported.remove();
  w.DSStudio.inspector.show({language:'css',section:'all'});
  d.getElementById('dockTabCss').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
  test('Inspector tabs support arrow-key selection and focus', () => d.activeElement.id==='dockTabHtml' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockTabCss').tabIndex===-1);
  test('Inspector code panel is labelled by active tab', () => d.getElementById('dockCss').getAttribute('aria-labelledby')==='dockTabHtml');
  d.getElementById('dockTabCss').click();
  reset();
  // One Palette/contrast/component path stays in integration. Detailed source,
  // repair/review and state matrices have independent focused suites.
  {
    app.style.width='1440px';reset();w.importConfig({sampleMode:'advanced'});w.dssShowWizardStep(4,false);w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
    d.getElementById('jSaveLocal').click();const id=d.getElementById('jProjects').value;
    input('jPrimary','#235678');await wait();
    test('Colour journey anchor edits reach JSON, local save, preview and inspector',()=>evaluate('state.primary').toUpperCase()==='#235678' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id].data.primary.toUpperCase()==='#235678' && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('--primary-500: #235678') && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
    input('jSemanticRole','control-border','change');d.getElementById('jSemanticEdit').click();
    const before=evaluate('projectJson()'),beforeLibrary=w.localStorage.getItem('dss-v27-projects');input('repairHex','#7B8A9B');
    const previewOnly=evaluate('projectJson()')===before && w.localStorage.getItem('dss-v27-projects')===beforeLibrary;
    d.getElementById('repairCancel').click();await wait();
    const cancelled=evaluate('projectJson()')===before;d.getElementById('jSemanticEdit').click();input('repairHex','#7B8A9B');d.getElementById('repairApply').click();await wait();
    test('Colour journey previews and cancels before committing a reviewed semantic fix',()=>previewOnly && cancelled && evaluate('palette("light").roles["control-border"]')==='#7B8A9B' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id].data.semanticOverrides.light['control-border']==='#7B8A9B' && w.dssGetContrastChecks().some(row=>row.name==='State Explorer input border' && row.theme==='light' && row.state==='default' && row.fg==='#7B8A9B'));
    w.dssShowWizardStep(7,false);input('bdVariant','secondary');input('bdSource','custom');input('bdCustom','#345678');input('bdHover','#234567');input('bdHoverText','#FFFFFF');input('bdState','hover');await wait();
    const motion=previewDoc().createElement('style');motion.textContent='.ds-button{transition:none!important}';previewDoc().head.append(motion);await wait();
    const buttonFiles=[],oldDownload=w.download;
    try{w.download=(name,content,type)=>buttonFiles.push({name,content,type});d.getElementById('bdExport').click();}finally{w.download=oldDownload;}
    test('Colour journey component overrides reach live states, CSS download and saved settings',()=>previewWindow().getComputedStyle(previewDoc().querySelector('.sample-selected-action')).backgroundColor==='rgb(35, 69, 103)' && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-selected-action')).textDecorationLine.includes('underline') && buttonFiles[0].name==='design-system-buttons.css' && buttonFiles[0].content.includes('#234567') && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id].data.buttonDesign.overrides.secondary.hoverText.toUpperCase()==='#FFFFFF');
    const json=evaluate('projectJson()'),css=evaluate('cssExport()'),html=evaluate('htmlExport()'),library=w.localStorage.getItem('dss-v27-projects');
    const files=[],previousDownload=w.download;
    try{w.download=(name,content,type)=>files.push({name,content,type});d.getElementById('jExportJson').click();}finally{w.download=previousDownload;}
    await importFile(files[0].content);await wait();
    test('Colour journey JSON download restores combined palette, repair and component data without overwriting local saves',()=>files[0].content===json && files[0].name==='design-system-studio.json' && evaluate('projectJson()')===json && evaluate('cssExport()')===css && evaluate('htmlExport()')===html && previewDoc().getElementById('dssPreviewStyles').textContent===css && w.localStorage.getItem('dss-v27-projects')===library);
    reset();app.style.width='1440px';w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
  }
  app.style.width='1440px';reset();w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
  // One typography/spacing journey keeps source, persistence, preview and files connected.
  {
    reset();w.importConfig({sampleMode:'advanced'});w.dssShowWizardStep(5,false);await wait();
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value,liveDocument=previewDoc();
    input('jFont',"Georgia, 'Times New Roman', serif");input('fontSystemHeading','verdana','change');
    input('jBase',18);input('jScalePreset','major-third','change');input('jLeading',1.7);input('jHeadingLeading',1.35);input('jHeadingTracking',.02);
    w.dssShowWizardStep(8,false);input('jSpacing',6);input('main-padding-left',17);await wait();
    const snapshot=evaluate('projectJson()'),css=evaluate('cssExport()'),html=evaluate('htmlExport()');
    const storedMatches=()=>JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectId].data)===JSON.stringify({preset:'custom',...JSON.parse(snapshot)});
    const matchesType=()=>{const body=previewWindow().getComputedStyle(previewDoc().body),heading=previewWindow().getComputedStyle(previewDoc().querySelector('h1'));return body.fontFamily.includes('Georgia') && body.fontSize==='18px' && Math.abs(parseFloat(body.lineHeight)-30.6)<.1 && heading.fontFamily.includes('Verdana') && Math.abs(parseFloat(heading.letterSpacing)-parseFloat(heading.fontSize)*.02)<.01;};
    test('Typography and spacing journey autosaves shared edits and updates the original preview',()=>previewDoc()===liveDocument && matchesType() && storedMatches() && css.includes('--space-unit: 6px;') && css.includes('--main-padding-left: 17px;') && d.getElementById('dockCss').textContent===css);
    input('spacingReflection','Integration comparison only');const beforeComparison=evaluate('projectJson()');d.getElementById('spacingCompare').click();d.getElementById('spacingInspectTokens').click();await wait();
    test('Spacing comparison and inspection keep typography and saved website settings intact',()=>evaluate('projectJson()')===beforeComparison && d.getElementById('spacingBeforeUnit').textContent==='6 px' && !evaluate('projectJson()+htmlExport()+cssExport()').includes('Integration comparison only') && d.getElementById('dockCss').textContent===css && matchesType());
    const files={},priorDownload=w.download;
    try{w.download=(name,content)=>{files[name]=content;};for(const id of ['jExportJson','jExportHtml','jExportCss'])d.getElementById(id).click();}finally{w.download=priorDownload;}
    reset();await importFile(files['design-system-studio.json']);await wait();
    test('Typography and spacing website downloads and JSON file restore agree with the saved model',()=>files['tokens.css']===css && files['index.html']===html && evaluate('projectJson()')===snapshot && evaluate('cssExport()')===css && evaluate('htmlExport()')===html && storedMatches() && matchesType() && !d.getElementById('spacingReflection').value);
    d.getElementById('dockModeBasic').click();await wait();
    const basicMatches=matchesType() && evaluate('state.spacing===6 && state.regionPadding.main.left===17') && previewDoc().getElementById('lists') && !previewDoc().getElementById('design-process');
    d.getElementById('dockModeAdvanced').click();await wait();
    test('Typography and spacing survive Basic and Advanced switching with the matching website and inspector',()=>basicMatches && matchesType() && evaluate('projectJson()')===snapshot && evaluate('htmlExport()')===html && d.getElementById('dockCss').textContent===css);
    reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(5,false);await wait();
  }
  // Combined responsive source -> live page -> separate downloads -> file restore.
  for(const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();w.importConfig({sampleMode:mode});
    if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();
    w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(9,false);await wait();
    input('jProject','Responsive <safe> journey');d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    const liveDocument=previewDoc(),fieldId=mode==='basic'?'signup-name':'contact-name';
    previewDoc().getElementById(fieldId).value='Robin fixture';previewDoc().getElementById('footer-sitemap').open=true;
    for(const [key,value] of Object.entries({stack:640,wide:1152,maxWidth:1280,gutter:20,wideGutter:40}))input('responsive-'+key,value);
    input('jRadius',24);input('previewTheme','dark','change');d.querySelector('[data-width="mobile"]').click();await wait();
    const json=evaluate('projectJson()'),html=evaluate('htmlExport()'),css=evaluate('cssExport()'),library=w.localStorage.getItem('dss-v27-projects');
    test(mode+' responsive journey joins editable cutoffs, autosave and the retained mobile preview',()=>previewDoc()===liveDocument && previewWindow().innerWidth===390 && previewDoc().documentElement.scrollWidth<=391 && previewDoc().getElementById(fieldId).value==='Robin fixture' && previewDoc().getElementById('footer-sitemap').open && previewDoc().documentElement.dataset.theme==='dark' && previewDoc().getElementById('dssPreviewStyles').textContent===css && d.getElementById('dockCss').textContent===css && JSON.stringify(JSON.parse(library)[projectId].data)===JSON.stringify({preset:'custom',...JSON.parse(json)}));
    const files={},priorDownload=w.download;
    try{w.download=(name,content,type)=>{files[name]={content,type};};for(const id of ['jExportHtml','jExportCss','jExportJson'])d.getElementById(id).click();}finally{w.download=priorDownload;}
    const page=d.createElement('iframe');page.style.cssText='width:639px;height:1000px;border:0';
    const cssUrl=w.URL.createObjectURL(new w.Blob([files['tokens.css'].content],{type:'text/css'}));
    const exported=new w.DOMParser().parseFromString(files['index.html'].content,'text/html');
    let layoutsMatch=true;
    try {
      page.srcdoc=files['index.html'].content.replace('href="tokens.css"','href="'+cssUrl+'"');
      await new Promise(resolve=>{page.onload=resolve;d.body.append(page);});
      for(const width of [639,641,1152]) {
        page.style.width=width+'px';await wait();const pd=page.contentDocument,pw=page.contentWindow;
        const layout=pw.getComputedStyle(pd.querySelector(mode==='basic'?'.skills-layout':'.sample-hero'));
        const columns=mode==='basic'?(layout.flexDirection==='column'?1:2):layout.gridTemplateColumns.split(' ').length;
        layoutsMatch=layoutsMatch && pd.querySelector('link[rel="stylesheet"]').sheet && !pd.querySelector('style,script') && pd.documentElement.dataset.theme==='dark' && pd.documentElement.scrollWidth<=width+1 && pw.getComputedStyle(pd.querySelector('.container')).paddingLeft===(width>=1152?'40px':'20px') && columns===(width<=640?1:mode==='basic'?2:12);
      }
      test(mode+' responsive journey downloads a working separate HTML/CSS pair with the configured layout',()=>files['index.html'].type==='text/html' && files['tokens.css'].type==='text/css' && files['index.html'].content===html && files['tokens.css'].content===css && exported.querySelector('link[href="tokens.css"]') && !exported.querySelector('style,script,safe') && exported.title.includes('Responsive <safe> journey') && layoutsMatch && evaluate('projectJson()')===json);
    } finally {page.remove();w.URL.revokeObjectURL(cssUrl);}
    reset();await importFile(files['design-system-studio.json'].content);await wait();
    test(mode+' responsive journey restores downloaded JSON without overwriting saved projects or retaining form entries',()=>{
      const checks={mime:files['design-system-studio.json'].type==='application/json',json:evaluate('projectJson()')===json,html:evaluate('htmlExport()')===html,css:evaluate('cssExport()')===css,stack:d.getElementById('responsive-stack').value==='640',gutter:d.getElementById('responsive-wideGutter').value==='40',inspector:d.getElementById('dockCss').textContent===css,previewCss:previewDoc().getElementById('dssPreviewStyles').textContent===css,form:previewDoc().getElementById(fieldId).value==='',library:w.localStorage.getItem('dss-v27-projects')===library};
      if(!Object.values(checks).every(Boolean))throw Error(JSON.stringify(checks));return true;
    });
  }
  app.style.width='1440px';reset();d.querySelector('[data-width="desktop"]').click();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(5,false);await wait();
  const sections=[...d.querySelectorAll('#main > .studio-section')];
  test('Every centre-pane section has a native heading accordion', () => sections.length===16 && sections.every(el=>el.tagName==='DETAILS' && el.querySelector(':scope > summary > h2')));
  const beforeCollapse=evaluate('projectJson()');
  d.getElementById('studio-section-4').open=false;
  d.querySelector('[data-journey-step="5"]').click(); await wait();
  test('Selecting a step opens its lesson without changing design data', () => d.getElementById('studio-section-2').open && !d.getElementById('studio-section-2').hidden && evaluate('projectJson()')===beforeCollapse);
  d.getElementById('dockTabHtml').click();d.getElementById('jViewCss').click(); await wait();
  test('Deliver Inspect CSS selects CSS even after HTML was selected', () => d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.activeElement===d.getElementById('dockCss'));
  d.getElementById('buttonDesignLab').open=false; d.getElementById('bdJump').click(); await wait();
  test('Button laboratory shortcut activates its matching step and opens the detail', () => d.getElementById('buttonDesignLab').open && !d.getElementById('buttonDesignLab').hidden && evaluate('DSStudio.activeStage')===7);
  d.getElementById('studio-section-4').open=false; evaluate("dssRevealSection('previewFrame',false)"); await wait();
  test('Reopening the responsive preview restores its exact width', () => d.getElementById('studio-section-4').open && Math.abs(d.getElementById('previewFrame').getBoundingClientRect().width-1280)<1);
  d.querySelector('[data-journey-step="5"]').click();
  d.querySelector('#studio-section-2 > summary').click();
  test('Individual lesson headings toggle their disclosure', () => !d.getElementById('studio-section-2').open);
  d.querySelector('#studio-section-2 > summary').click(); await wait();
  app.style.width='320px';await wait();
  test('Active lesson headings and typography controls fit a 320px page', () => w.innerWidth===320 && d.documentElement.scrollWidth<=321);
  app.style.width='1440px';await wait();
  revealAll();
  reset();await wait();d.getElementById('dockTabCss').click();
  const downloadCalls=[];
  const originalDownload=w.download;
  w.download=(name,content,type)=>downloadCalls.push({name,content,type});
  for (const [id,name] of [['saveBtn','design-system-studio.json'],['cssBtn','tokens.css'],['dockDownload','tokens.css'],['jExportHtml','index.html'],['jExportCss','tokens.css'],['jExportJson','design-system-studio.json'],['bdExport','design-system-buttons.css']]) {
    d.getElementById(id).click();
    test(id+' produces the expected download', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content.length>0);
  }
  for (const [tab,name] of [['viewCss','tokens.css'],['viewJson','design-system-studio.json'],['viewHtml','index.html']]) {
    d.getElementById(tab).click(); d.getElementById('downloadCode').click();
    test(tab+' downloads exactly the displayed code', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content===d.getElementById('codeView').textContent);
  }
  test('Responsive preview omits the introductory lesson and duplicate export card', () => !d.querySelector('#studio-section-4 .studio-lesson, #studio-section-4 .website-export, #studio-section-4 [data-website-download], #studio-section-4 [data-website-code]') && d.getElementById('previewPage'));
  const beforeWebsiteDownloads=evaluate('projectJson()');
  for (const [index,button] of [...d.querySelectorAll('[data-website-download]')].entries()) {
    button.click();
    test('Standalone website action '+(index+1)+' downloads the matching live file with its MIME type', () => {
      const html=button.dataset.websiteDownload==='html', file=downloadCalls.at(-1);
      return file.name===(html?'index.html':'tokens.css') && file.type===(html?'text/html':'text/css') && file.content===evaluate(html?'htmlExport()':'cssExport()');
    });
  }
  test('Deliver downloads preserve saved settings', () => evaluate('projectJson()')===beforeWebsiteDownloads);
  input('tokenSearch','--button-primary-hover'); await wait();
  d.getElementById('tokenDownload').click();
  test('Token search and CSV agree on the filtered tokens', () => [...d.querySelectorAll('#tokenTableBody tr')].every(row=>row.textContent.includes('--button-primary-hover')) && downloadCalls.at(-1).name==='design-system-tokens.csv' && !downloadCalls.at(-1).content.includes('--brand-white'));
  w.download=originalDownload;
  // Keep one cross-feature persistence path here; detailed library contracts
  // live in project_library_review.py with a fresh, independent app.
  d.getElementById('jNewLocal').click();
  // Import-normalized starter keeps optional map shape stable across backups.
  w.importConfig({sampleMode:'advanced'});
  input('jProject','Integration save and restore');input('jBase',18);
  input('plan-goal','Find a lesson and practise.');input('bdRadius',18);
  d.getElementById('jSaveLocal').click();const integrationId=d.getElementById('jProjects').value;
  input('jBase',19);await wait();
  const integrationJson=evaluate('projectJson()'),integrationCss=evaluate('cssExport()'),integrationHtml=evaluate('htmlExport()');
  test('End-to-end editor changes autosave a complete local project',()=>{
    const data=JSON.parse(w.localStorage.getItem('dss-v27-projects'))[integrationId].data;
    return data.base===19 && data.buttonDesign.radius===18 && data.designProcess.goal==='Find a lesson and practise.';
  });
  d.getElementById('jNewLocal').click();
  test('End-to-end New starts Basic without overwriting the saved design',()=>evaluate('state.sampleMode')==='basic' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[integrationId].data.base===19);
  d.getElementById('jProjects').value=integrationId;d.getElementById('jLoadLocal').click();await wait();
  test('End-to-end local load restores editors, exports and live preview',()=>evaluate('projectJson()')===integrationJson && d.getElementById('jBase').value==='19' && evaluate('htmlExport()')===integrationHtml && d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent===integrationCss);
  const integrationDownloads=[],priorIntegrationDownload=w.download;
  try{w.download=(name,content,type)=>integrationDownloads.push({name,content,type});d.getElementById('jExportJson').click();}
  finally{w.download=priorIntegrationDownload;}
  reset();await importFile(integrationDownloads[0].content);await wait();
  test('End-to-end downloaded JSON reimports through the file picker with matching preview and exports',()=>integrationDownloads[0].name==='design-system-studio.json' && integrationDownloads[0].type==='application/json' && evaluate('projectJson()')===integrationJson && evaluate('cssExport()')===integrationCss && evaluate('htmlExport()')===integrationHtml && d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent===integrationCss);
  const originalClipboard=w.navigator.clipboard;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(Error('Denied for audit'))}});
  d.getElementById('copyCode').click(); await wait();
  test('Clipboard rejection gives a manual-copy fallback', () => d.getElementById('liveStatus').textContent.includes('Clipboard unavailable'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard});
  reset();
  input('brandApplyRole','accent','change');
  const referenceAction=d.querySelector('[data-brand-role="accent"][data-brand-hex="#00BADC"]'); referenceAction.click();
  test('Reference swatch selection synchronizes palette and guided controls', () => d.getElementById('accent').value===d.getElementById('jAccent').value && evaluate('state.accent')===referenceAction.dataset.brandHex.toLowerCase());
  d.querySelector('[data-journey-step="0"]').click(); d.getElementById('jNext').click();
  test('Guided navigation advances and returns to the first step', () => {
    if (!d.getElementById('jProgress').textContent.startsWith('Step 2')) return false;
    d.getElementById('jBack').click(); return d.getElementById('jBack').disabled && d.getElementById('jProgress').textContent.startsWith('Step 1');
  });
  d.getElementById('dockToggle').click();
  test('CSS dock collapse and expand update accessible state', () => {
    if (d.getElementById('dockToggle').getAttribute('aria-expanded')!=='false') return false;
    d.getElementById('dockToggle').click(); return d.getElementById('dockToggle').getAttribute('aria-expanded')==='true' && !d.querySelector('.studio-code-dock').classList.contains('is-collapsed');
  });
  const storageSet=w.Storage.prototype.setItem;
  w.Storage.prototype.setItem=()=>{throw Error('Storage quota exceeded for audit');};
  d.getElementById('jSaveLocal').click();
  test('Unavailable storage offers JSON backup without crashing', () => d.getElementById('jSaveStatus').textContent.includes('Download JSON instead'));
  w.Storage.prototype.setItem=storageSet;
  reset(); await wait();
  const beforeInspector=evaluate('projectJson()');
  d.getElementById('dockTabCss').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
  test('Inspector keyboard tabs select HTML and label the code panel', () => d.activeElement.id==='dockTabHtml' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockTabCss').tabIndex===-1 && d.getElementById('dockCss').getAttribute('aria-labelledby')==='dockTabHtml' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  test('Switching inspector languages leaves project data unchanged', () => evaluate('projectJson()')===beforeInspector);
  input('jProject','Cedar Studio'); input('jTheme','dark'); input('bdSize','lg');
  d.getElementById('bdMobileFull').checked=true; d.getElementById('bdMobileFull').dispatchEvent(new w.Event('input',{bubbles:true}));
  test('HTML inspector follows project, theme and button selections live', () => d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('dockCss').textContent.includes('Cedar Studio') && d.getElementById('dockCss').textContent.includes('data-theme="dark"') && d.getElementById('dockCss').textContent.includes('ds-button--lg ds-button--mobile-full'));
  const inspectorDownloads=[]; w.download=(name,content,type)=>inspectorDownloads.push({name,content,type});
  d.getElementById('dockDownload').click();
  test('HTML inspector downloads the exact visible home page', () => inspectorDownloads.at(-1).name==='index.html' && inspectorDownloads.at(-1).type==='text/html' && inspectorDownloads.at(-1).content===d.getElementById('dockCss').textContent && d.getElementById('dockCopy').textContent==='Copy HTML');
  let copiedInspector='';
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{copiedInspector=text;}}});
  d.getElementById('dockCopy').click(); await wait();
  test('Inspector copies the selected HTML', () => copiedInspector===evaluate('htmlExport()'));
  d.getElementById('dockTabHtml').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));
  d.getElementById('dockDownload').click();
  test('Inspector returns to live CSS with CSS download and copy labels', () => d.activeElement.id==='dockTabCss' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && inspectorDownloads.at(-1).name==='tokens.css' && inspectorDownloads.at(-1).content===evaluate('cssExport()') && d.getElementById('dockCopy').textContent==='Copy CSS');
  d.getElementById('dockCopy').click(); await wait();
  test('Inspector copies the selected CSS', () => copiedInspector===evaluate('cssExport()'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard}); w.download=originalDownload;
  test('Generated reference tokens use the universal brand prefix', () => evaluate('cssExport()').includes('--brand-white: #FFFFFF') && !evaluate('cssExport()').includes('--example-'));
  input('tokenSearch','--brand-'); await wait();
  test('Token catalogue classifies renamed brand references', () => d.querySelectorAll('#tokenTableBody tr').length===11 && [...d.querySelectorAll('#tokenTableBody tr')].every(row=>row.textContent.includes('Brand palette')));
  reset(); await wait(); input('tokenSearch','');
  for (const [name,scope,control,step] of [['--space-6','Light / base','jSpacing',8],['--grid-gap','Light / base','advGap',9],['--text-h1','Light / base','clampFactor',5],['--text','Dark','jSemanticRole',4],['--button-secondary-hover-text','Dark','bdHoverText',4],['--brand-blue','Light / base',null,4]]) {
    d.getElementById('studio-section-8').open=true;
    const button=d.querySelector(`[data-token-name="${name}"][data-token-scope="${scope}"]`);
    button.click(); await wait();
    test(name+' catalogue action reveals and focuses its wizard source', () => {
      const focused=d.activeElement;
      return !d.querySelector(`[data-journey-pane="${step}"]`).hidden && (control?focused===d.getElementById(control):focused.matches('[data-brand-id="blue"] [data-brand-field="hex"]')) && focused.getBoundingClientRect().width>0 && (scope!=='Dark' || evaluate('state.theme')==='dark');
    });
  }
  test('Button token routing selects the matching variant', () => evaluate('state.buttonDesign.variant')==='secondary');
  test('Semantic catalogue routing retains the intended theme role', () => d.getElementById('jSemanticRole').value==='text');
  test('Constant-sized body text and the base scale step route to the base-size control', () => ['--text-step-2','--text-body','--text-small'].every(name=>w.dssTokenSource({name}).control==='jBase'));
  for (const theme of ['light','dark']) {
    input('jTheme',theme); app.style.width='320px';
    for (const step of [5,8,9,10,11]) {
      d.querySelector(`[data-journey-step="${step}"]`).click();
      d.querySelectorAll(`[data-journey-pane="${step}"] details:not([hidden])`).forEach(details=>details.open=true);
      await wait();
      test(theme+' expanded wizard step '+(step+1)+' fits 320px', () => d.documentElement.scrollWidth<=320 && d.querySelector(`[data-journey-pane="${step}"]`).scrollWidth<=d.querySelector(`[data-journey-pane="${step}"]`).clientWidth+1);
    }
  }
  app.style.width='1440px'; reset(); await wait();
  test('Delivery reviews include planning and report their actual checklist count', () => {
    const boxes=[...d.querySelectorAll('.readiness-item')];
    boxes[0].checked=true; boxes[0].dispatchEvent(new w.Event('change'));
    const passes=boxes.length===8 && boxes[0].parentElement.textContent.includes('brief') && boxes[1].parentElement.textContent.includes('prototype') && d.getElementById('readinessStatus').textContent.startsWith('1 of 8');
    boxes[0].checked=false; boxes[0].dispatchEvent(new w.Event('change')); return passes;
  });
  w.dssShowWizardStep(3,false);
  // One shared-planning path remains in integration; detailed workflow and
  // Brief fixtures live in planning_review.py.
  reset();w.importConfig({sampleMode:'advanced'});w.dssShowWizardStep(0,false);await wait();
  input('jProject','Integration planning fixture');input('plan-goal','Find a practical lesson.');
  input('plan-audience','Learners reviewing the field guide.');input('plan-content','Tutor supplies the examples.');
  input('plan-delivery','Tutor reviews the exported website.');input('plan-prototypeTask','Choose a lesson without help.');
  d.getElementById('jSaveLocal').click();const planningJourneyId=d.getElementById('jProjects').value;
  input('plan-prototypeNotes','The learner found the right example.');await wait();
  const planningJourneyData=evaluate('JSON.stringify(state.designProcess)'),planningJourneyHtml=evaluate('htmlExport()');
  test('Planning journey connects edited Brief and prototype notes to local save and Advanced preview',()=>JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planningJourneyId].data.designProcess)===planningJourneyData && d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent==='Learners reviewing the field guide.' && previewDoc().querySelector('#brief-lab [data-brief-field="content"] dd').textContent==='Tutor supplies the examples.' && previewDoc().querySelector('#prototype-lab').textContent.includes('The learner found the right example.'));
  const planningJourneyFiles=[],priorPlanningDownload=w.download;
  try{w.download=(name,content,type)=>planningJourneyFiles.push({name,content,type});d.getElementById('jExportJson').click();}
  finally{w.download=priorPlanningDownload;}
  reset();await importFile(planningJourneyFiles[0].content);await wait();
  test('Planning journey JSON download reimports through the file picker with matching editors and website',()=>planningJourneyFiles[0].name==='design-system-studio.json' && JSON.stringify(JSON.parse(planningJourneyFiles[0].content).designProcess)===planningJourneyData && evaluate('JSON.stringify(state.designProcess)')===planningJourneyData && d.getElementById('plan-delivery').value==='Tutor reviews the exported website.' && evaluate('htmlExport()')===planningJourneyHtml);
  d.getElementById('dockModeBasic').click();await wait();
  const planningJourneyBasic=evaluate('JSON.stringify(state.designProcess)')===planningJourneyData && !previewDoc().querySelector('#design-process');
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Planning journey survives Basic and Advanced switching with the correct sample boundary',()=>planningJourneyBasic && evaluate('JSON.stringify(state.designProcess)')===planningJourneyData && evaluate('htmlExport()')===planningJourneyHtml && previewDoc().querySelector('#brief-lab [data-brief-field="audience"] dd').textContent==='Learners reviewing the field guide.');
  app.style.width='1440px';reset();await wait();
  // One custom-sitemap journey stays in integration; sitemap_review.py owns
  // CRUD, inclusion/source/compatibility and responsive editor matrices.
  {
    app.style.width='1440px';reset();w.importConfig({sampleMode:'basic',designProcess:{pages:w.DSStudio.process.samplePages('basic'),sitemapSource:{basic:'custom',advanced:'sections'}}});w.dssShowWizardStep(1,false);revealDestinationPlan();w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
    const entry=w.DSStudio.process.entries().find(node=>node.label==='Content card');
    const choose=()=>{const button=[...d.querySelectorAll('#sitemap-choices button')].find(el=>el.dataset.sitemapNodeId===entry.id);for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    choose();d.getElementById('jSaveLocal').click();const id=d.getElementById('jProjects').value;
    const before=evaluate('projectJson()'),library=w.localStorage.getItem('dss-v27-projects'),body=previewDoc().querySelector('main').innerHTML,css=evaluate('cssExport()');
    input('sitemap-label','Integration lesson link');input('sitemap-target','basic-structure','change');
    test('Sitemap journey keeps unsaved destination edits outside the model and local save',()=>evaluate('projectJson()')===before && w.localStorage.getItem('dss-v27-projects')===library && !d.getElementById('sitemap-discard').disabled);
    d.getElementById('sitemap-save').click();await wait();const saved=evaluate('projectJson()');
    test('Sitemap journey saves a stable destination in storage, preview, inspector and exported HTML',()=>{
      const node=w.DSStudio.process.entries().find(row=>row.id===entry.id),exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      return node.label==='Integration lesson link' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id].data.designProcess.pageLinks.basic[node.label]==='basic-structure' && previewDoc().querySelector('#sitemap a[href="#basic-structure"]').textContent===node.label && exported.querySelector('#sitemap a[href="#basic-structure"]').textContent===node.label && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && previewDoc().querySelector('main').innerHTML===body && evaluate('cssExport()')===css;
    });
    const files=[],oldDownload=w.download;
    try{w.download=(name,content,type)=>files.push({name,content,type});d.getElementById('jExportJson').click();}
    finally{w.download=oldDownload;}
    input('sitemap-label','Discard this label');d.getElementById('sitemap-discard').click();
    const discarded=evaluate('projectJson()')===saved && d.getElementById('sitemap-label').value==='Integration lesson link';
    d.getElementById('sitemap-undo').click();await wait();
    test('Sitemap journey Discard and Undo restore the prior destination without changing website content',()=>discarded && evaluate('projectJson()')===before && w.DSStudio.process.entries().find(row=>row.id===entry.id).label==='Content card' && previewDoc().querySelector('main').innerHTML===body);
    const libraryBeforeFile=w.localStorage.getItem('dss-v27-projects');await importFile(files[0].content);await wait();choose();
    test('Sitemap journey downloaded JSON restores the edited destination without overwriting the local library',()=>files[0].name==='design-system-studio.json' && files[0].type==='application/json' && files[0].content===saved && evaluate('projectJson()')===saved && d.getElementById('sitemap-label').value==='Integration lesson link' && previewDoc().querySelector('#sitemap a[href="#basic-structure"]').textContent==='Integration lesson link' && w.localStorage.getItem('dss-v27-projects')===libraryBeforeFile && previewDoc().querySelector('main').innerHTML===body);
  }
  input('jProject','My learning project'); input('jBase',18);
  const beforeLearning=JSON.parse(evaluate('projectJson()'));
  const settleLearningColours=()=>{const style=previewDoc().createElement('style');style.textContent='.ds-button { transition: none !important; }';previewDoc().head.append(style);};
  d.getElementById('dockModeBasic').click();
  d.querySelector('[data-journey-step="7"]').click();
  w.DSStudio.inspector.show({section:'all',language:'css'}); await wait();
  const startedLearning=JSON.parse(evaluate('projectJson()'));
  delete beforeLearning.sampleMode; delete startedLearning.sampleMode;
  test('Unified Buttons step retains design values while showing its task and example',()=>Object.keys(beforeLearning).every(key=>JSON.stringify(beforeLearning[key])===JSON.stringify(startedLearning[key])) && d.getElementById('studyExample').value==='action' && d.querySelector('#buttonDesignLab .step-task').textContent.includes('primary button'));
  test('Teaching state stays outside generated files and project data',()=>!evaluate('htmlExport()').includes('step-task') && !evaluate('cssExport()').includes('journey-phase') && !evaluate('projectJson()').includes('activeStage'));
  d.getElementById('exampleConnections').open=true;
  test('Primary action exposes its exact exported rule and live token values',()=>evaluate('cssExport()').includes(d.getElementById('studyRule').textContent) && d.getElementById('studyRule').textContent.startsWith('.ds-button--primary {') && d.getElementById('studyTokens').textContent.includes('--button-primary-bg:'));
  input('bdDefaultBg','#602d54'); await wait(); settleLearningColours();
  test('A beginner colour change updates the example, connected token and inspector together',()=>previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(96, 45, 84)' && d.getElementById('studyTokens').textContent.toLowerCase().includes('#602d54') && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  d.querySelector('[data-journey-step="8"]').click();
  await wait();
  test('Spacing exercise opens the existing source control',()=>{const control=d.getElementById('jSpacing'),box=control.getBoundingClientRect();return !d.querySelector('[data-journey-pane="8"]').hidden && box.width>0 && box.height>0 && !control.disabled;});
  const beforeLearningPadding=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('#lists')).paddingTop);
  input('jSpacing',6); await wait();
  test('Spacing connection shows derived values from the current generator',()=>d.getElementById('studyTokens').textContent.includes('--space-unit: 6px') && d.getElementById('studyTokens').textContent.includes('--space-8: calc(var(--space-unit) * 8)') && Math.abs(parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('#lists')).paddingTop)-beforeLearningPadding*1.5)<.1 && d.getElementById('studyRule').textContent.includes('var(--space-8)') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('studyExample','header','change'); await wait();
    const primary=w.dssReadTokens().filter(row=>row.name==='--primary').find(row=>theme==='dark'?row.scope==='Dark':row.scope!=='Dark');
    test(theme+' connected token reads the correct exported theme scope',()=>d.getElementById('studyTokens').textContent.includes('--primary: '+primary.value));
  }
  for (const option of [...d.getElementById('studyExample').options]) {
    input('studyExample',option.value,'change');
    test('Example '+option.value+' maps to a real generated CSS rule',()=>evaluate('cssExport()').includes(d.getElementById('studyRule').textContent) && !d.getElementById('studyRule').textContent.includes('Inspect its section') && (option.value!=='faq' || d.getElementById('studyTokens').textContent.includes('--heading-weight')) && (option.value!=='footer' || d.getElementById('studyTokens').textContent.includes('--space-8')));
  }
  input('studyExample','profile','change'); d.getElementById('studyPreview').click(); await wait();
  test('Show example focuses its actual preview element',()=>previewDoc().activeElement===previewDoc().getElementById('basic-layout'));
  const beforePicking=evaluate('projectJson()'), pickingDoc=previewDoc();
  d.getElementById('studyPick').click();
  previewDoc().querySelector('#basic-layout a').click(); await wait();
  test('Opt-in selection connects the clicked example without following its link or changing project data',()=>previewDoc()===pickingDoc && d.getElementById('studyExample').value==='profile' && !w.DSStudio.learning.picking && d.activeElement===d.getElementById('studyExample') && evaluate('projectJson()')===beforePicking);
  previewDoc().querySelector('#basic-layout a').click(); await wait();
  test('Normal preview navigation resumes after selecting an example',()=>previewDoc().activeElement===previewDoc().getElementById('list-workflow'));
  d.getElementById('studyPick').click(); previewDoc().dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  test('Escape inside the preview cancels example selection',()=>!w.DSStudio.learning.picking && d.getElementById('studyPick').getAttribute('aria-pressed')==='false');
  d.getElementById('studyPick').click(); previewDoc().querySelector('#home h1').click(); await wait();
  test('Selecting a hero heading connects its layout rather than an unrelated action',()=>d.getElementById('studyExample').value==='hero');
  d.getElementById('studyPick').click(); previewDoc().querySelector('#home .ds-button--primary').click(); await wait();
  test('Selecting a primary action connects its component rule',()=>d.getElementById('studyExample').value==='action' && !w.DSStudio.learning.picking);
  input('dockSection','footer','change');
  test('Existing study-section selection also updates example connections',()=>d.getElementById('studyExample').value==='footer' && d.getElementById('studyRule').textContent.includes('.website-footer .footer-inner'));
  d.getElementById('dockTabHtml').click(); d.getElementById('dockToggle').click();
  w.DSStudio.inspector.show();
  test('Code shortcut retains the selected language and excerpt and expands the inspector',()=>d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='footer' && !d.querySelector('.studio-code-dock').classList.contains('is-collapsed') && d.activeElement===d.getElementById('dockCss') && d.getElementById('dockCss').textContent===w.DSStudio.samples.basicExcerpt(evaluate('htmlExport()'),'html','footer'));
  d.getElementById('studyCode').click();
  test('Find rule selects complete CSS so shared dependencies remain visible',()=>d.getElementById('dockSection').value==='all' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').scrollTop>0 && d.activeElement===d.getElementById('dockCss'));
  d.querySelector('[data-journey-step="9"]').click(); const beforeLearningResponsive=evaluate('JSON.stringify(state.responsiveDesign)');
  d.querySelector('button[data-width="mobile"]').click();d.getElementById('studyPreview').click(); await wait();
  test('Responsive task tests 390px without changing saved breakpoints',()=>Math.abs(previewWindow().innerWidth-390)<1 && evaluate('JSON.stringify(state.responsiveDesign)')===beforeLearningResponsive && previewDoc().activeElement===previewDoc().getElementById('home'));
  const learningFiles=[], beforeLearningDownload=w.download;w.download=(name,content,type)=>learningFiles.push({name,content,type});
  d.querySelector('[data-journey-step="11"]').click();
  test('Export exercise focuses Deliver without downloading automatically',()=>!d.querySelector('[data-journey-pane="11"]').hidden && learningFiles.length===0);
  d.getElementById('jExportHtml').click();d.getElementById('jExportCss').click();
  test('Beginner project exports the complete matching HTML and CSS',()=>learningFiles[0].name==='index.html' && learningFiles[0].content===evaluate('htmlExport()') && learningFiles[1].name==='tokens.css' && learningFiles[1].content===evaluate('cssExport()'));
  w.download=beforeLearningDownload;
  const learningExport=evaluate('projectJson()'); reset();evaluate('importConfig('+learningExport+')'); await wait(); settleLearningColours();
  test('Beginner design survives a project JSON round trip independently of session progress',()=>Object.keys(JSON.parse(learningExport)).every(key=>JSON.stringify(JSON.parse(learningExport)[key])===JSON.stringify(JSON.parse(evaluate('projectJson()'))[key])) && previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(96, 45, 84)');
  for (const width of [320,390,1280,1440]) {
    app.style.width=width+'px'; await wait();
    w.DSStudio.inspector.show();
    test('Workspace shortcuts and focused code remain usable at '+width+'px',()=>d.documentElement.scrollWidth<=width+1 && [...d.querySelectorAll('.step-output button')].filter(button=>button.getBoundingClientRect().width>0).every(button=>button.getBoundingClientRect().height>=44) && d.activeElement===d.getElementById('dockCss') && d.getElementById('dockCss').getBoundingClientRect().bottom>0 && d.getElementById('dockCss').getBoundingClientRect().top<app.contentWindow.innerHeight);
  }
  app.style.width='1440px';d.querySelector('button[data-width="fluid"]').click();d.getElementById('exampleConnections').open=false;reset();await wait();
  // One learner journey remains here; navigation_review.py owns the route,
  // breakpoint, disclosure, focus and fragment-reload matrices.
  app.style.width='1440px';reset();await wait();
  const journeyPreview=previewDoc();
  d.querySelector('[data-journey-step="0"]').click();input('plan-goal','Choose a lesson and practise.');
  test('Learner journey starts with Brief controls and the matching lesson',()=>w.DSStudio.activeStage===0 && d.getElementById('process-brief').open && d.getElementById('plan-goal').value==='Choose a lesson and practise.');
  d.querySelector('[data-journey-step="5"]').click();input('jBase',18);d.getElementById('jBase').focus();await wait();
  test('Learner journey connects Typography editing to the current preview and CSS',()=>w.DSStudio.activeStage===5 && d.getElementById('studio-section-2').open && d.activeElement===d.getElementById('jBase') && previewDoc()===journeyPreview && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('--font-size-base: 18px;'));
  d.querySelector('[data-journey-step="11"]').click();
  d.querySelector('#studio-section-6 [data-inspect="css"]').click();await wait();
  test('Learner journey reaches Deliver and inspects the edited CSS',()=>w.DSStudio.activeStage===11 && d.getElementById('studio-section-6').open && d.getElementById('studioInspector').open && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && evaluate('state.designProcess.goal')==='Choose a lesson and practise.');
  const journeyFiles=[],oldJourneyDownload=w.download;
  try{w.download=(name,content,type)=>journeyFiles.push({name,content,type});d.querySelectorAll('[data-website-download]').forEach(button=>button.click());}
  finally{w.download=oldJourneyDownload;}
  test('Learner journey hands over the current website without replacing the preview document',()=>journeyFiles.some(file=>file.name==='index.html' && file.content===evaluate('htmlExport()')) && journeyFiles.some(file=>file.name==='tokens.css' && file.content===evaluate('cssExport()')) && previewDoc()===journeyPreview);
  // The following readiness fixtures explicitly start from their Spacing stage.
  reset();w.dssShowWizardStep(8,false);await wait();
  const reviewBox=d.querySelector('.readiness-item');
  const acknowledge=()=>{reviewBox.checked=true;reviewBox.dispatchEvent(new w.Event('change',{bubbles:true}));};
  acknowledge();input('jSpacing',5);
  test('Editing the design invalidates readiness acknowledgements',()=>!reviewBox.checked && !d.getElementById('readinessStatus').textContent.startsWith('1 of'));
  acknowledge();reset();
  test('Reset clears readiness even if the same values are restored',()=>!reviewBox.checked);
  acknowledge();evaluate('importConfig(JSON.parse(projectJson()))');d.dispatchEvent(new w.Event('dss:imported'));
  test('Loading a project clears readiness acknowledgements',()=>!reviewBox.checked);
  const beforeClampClipboard=w.navigator.clipboard;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('Clipboard denied'))}});
  d.getElementById('clampCopy').click();await wait();
  test('Rejected clamp clipboard access offers a manual copy fallback',()=>d.getElementById('clampCopyStatus').textContent.includes('copy it manually'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:beforeClampClipboard});
  const unifiedDownloads=[],beforeUnifiedDownload=w.download;
  w.download=(name,content,type)=>unifiedDownloads.push({name,content,type});
  d.getElementById('saveBtn').click();d.getElementById('jExportJson').click();
  test('Project JSON entry points export identical filenames and data',()=>unifiedDownloads.length===2 && unifiedDownloads[0].name===unifiedDownloads[1].name && unifiedDownloads[0].content===unifiedDownloads[1].content);
  w.download=beforeUnifiedDownload;
  // Tailwind is an optional source mapping; the website generators remain authoritative.
  reset();await wait();w.dssShowWizardStep(11);await wait();
  const bridgeSource=()=>w.DSStudio.tailwind.source();
  const bridgeSnapshot=()=>JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'));
  const bridgeCell=source=>d.querySelector('#tailwindMappingRows tr[data-source="'+source+'"] td code');
  test('Deliver presents the Tailwind explanation inside its existing centre lesson',()=>d.getElementById('tailwindBridge').closest('.studio-section').id==='studio-section-6' && d.getElementById('tailwindBridge').closest('.studio-lesson') && w.DSStudio.activeStage===11);
  test('Tailwind example teaches the same four properties without executing its markup',()=>d.getElementById('tailwindCssExample').textContent.includes('padding: var(--space-6)') && ['p-6','bg-surface','text-content','rounded-card'].every(value=>d.getElementById('tailwindHtmlExample').textContent.includes(value)) && !d.getElementById('tailwindHtmlExample').querySelector('article'));
  const bridgeInitial=bridgeSource();
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('previewTheme',theme,'change');await wait();
    test(mode+' '+theme+' mapping follows exported semantic roles independently of Studio appearance',()=>bridgeCell('--surface').textContent===evaluate('palette().roles.surface') && bridgeCell('--text').textContent===evaluate('palette().roles.text') && d.getElementById('tailwindContext').textContent.includes(theme==='dark'?'Dark':'Light'));
    test(mode+' '+theme+' selection leaves the two-theme Tailwind source unchanged',()=>bridgeSource()===bridgeInitial);
  }
  test('Tailwind source maps colour/font/type/radius/spacing without self-references or component CSS',()=>bridgeSource().includes('--color-content: var(--text);') && bridgeSource().includes('--font-display: var(--font-heading);') && bridgeSource().includes('--spacing: var(--space-unit);') && bridgeSource().includes('@theme inline') && !/--([\w-]+): var\(--\1\);/.test(bridgeSource()) && !bridgeSource().includes('.ds-button {') && !bridgeSource().includes('@import'));
  const bridgeRows=[...d.querySelectorAll('#tailwindMappingRows tr')];
  input('jSpacing',8);input('jRadius',26);input('bdRadius',18);input('jBase',20);await wait();
  test('Spacing and independent card/button corners trace current project values',()=>bridgeCell('--space-unit').textContent==='8px' && d.getElementById('tailwindSpacingExample').textContent.includes('48px') && bridgeCell('--radius-base').textContent==='26px' && bridgeCell('--button-radius').textContent==='18px');
  test('Tailwind type mapping reads the exact fluid export declaration',()=>bridgeCell('--text-body').textContent===w.dssReadTokens().find(row=>row.name==='--text-body').value && bridgeSource().includes('--text-body: '+bridgeCell('--text-body').textContent+';'));
  const bridgeFont=d.getElementById('jFont').options[1].value;input('jFont',bridgeFont);await wait();
  test('Font mapping reads the project font stack instead of the Studio font',()=>bridgeCell('--font-body').textContent===w.dssReadTokens().find(row=>row.name==='--font-body').value && bridgeSource().includes('--font-body: '+bridgeCell('--font-body').textContent+';'));
  evaluate("state.semanticOverrides={light:{surface:'#F0E0D0',text:'#332211'},dark:{surface:'#112233',text:'#DDEEFF'}};apply()");await wait();
  input('previewTheme','light','change');await wait();
  test('Light mapping reflects overrides and source preserves both theme values',()=>bridgeCell('--surface').textContent==='#F0E0D0' && bridgeSource().includes('--surface: #F0E0D0;') && bridgeSource().includes('--surface: #112233;') && bridgeSource().includes('@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *))'));
  input('previewTheme','dark','change');await wait();
  test('Dark mapping reflects its own overrides without replacing the light definitions',()=>bridgeCell('--text').textContent==='#DDEEFF' && bridgeSource().includes('--text: #332211;'));
  evaluate('state.responsiveDesign={stack:640,wide:1120,maxWidth:1152,gutter:16,wideGutter:32};apply()');await wait();
  test('Tailwind breakpoints use saved literal lengths outside the inline alias block',()=>bridgeSource().includes('@theme {\n  --breakpoint-page-stack: 40rem;\n  --breakpoint-page-wide: 70rem;') && !bridgeSource().includes('--breakpoint-page-stack: var(') && bridgeCell('Saved stacking cutoff').textContent==='40rem');
  evaluate('renderCode()');await wait();
  test('Mapping rows and unchanged source text survive refreshes',()=>bridgeRows.every((row,index)=>row===d.querySelectorAll('#tailwindMappingRows tr')[index]));
  const bridgeText=d.getElementById('tailwindSource').firstChild;evaluate('renderCode()');await wait();
  test('Unchanged Tailwind source retains its selectable text node',()=>d.getElementById('tailwindSource').firstChild===bridgeText);
  const bridgeBeforeActions=bridgeSnapshot(),bridgePreview=previewDoc();
  const bridgeDownloads=[],bridgeDownload=w.download,bridgeClipboard=w.navigator.clipboard;
  w.download=(name,text,type)=>bridgeDownloads.push({name,text,type});
  let bridgeCopied='';Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{bridgeCopied=text;}}});
  d.getElementById('tailwindMappings').open=true;d.getElementById('tailwindSourceDetails').open=true;
  d.getElementById('tailwindCopy').click();await wait();d.getElementById('tailwindDownload').click();
  test('Tailwind copy and download use current source with a distinct filename and MIME type',()=>bridgeCopied===bridgeSource() && bridgeDownloads.length===1 && bridgeDownloads[0].name==='tailwind-theme.css' && bridgeDownloads[0].type==='text/css' && bridgeDownloads[0].text===bridgeSource() && d.getElementById('tailwindStatus').textContent.includes('download requested'));
  test('Bridge interactions preserve exact project JSON, website HTML/CSS and preview document',()=>bridgeSnapshot()===bridgeBeforeActions && previewDoc()===bridgePreview && !evaluate('cssExport()').includes('@theme') && !evaluate('htmlExport()').includes('tailwindBridge'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('Clipboard denied'))}});
  d.getElementById('tailwindSourceDetails').open=false;d.getElementById('tailwindCopy').click();await wait();
  test('Denied Tailwind clipboard access opens source and explains manual copying',()=>d.getElementById('tailwindSourceDetails').open && d.getElementById('tailwindStatus').textContent.includes('copy it manually'));
  let bridgeFinishCopy;Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>new Promise(resolve=>{bridgeFinishCopy=resolve;})}});
  d.getElementById('tailwindCopy').click();input('jSpacing',3);await wait();bridgeFinishCopy();await wait();
  test('Delayed Tailwind clipboard feedback identifies an older settings snapshot',()=>d.getElementById('tailwindStatus').textContent.includes('earlier theme source'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:bridgeClipboard});w.download=bridgeDownload;
  d.getElementById('tailwindInspect').click();await wait();
  test('Mapping inspection opens the complete existing website CSS',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  evaluate('importConfig({project:"<img src=x onerror=alert(1)>",spacing:1e10,radius:-100,font:"Arial; color:red",responsiveDesign:{stack:-1,wide:1e10},semanticOverrides:{light:{surface:"red; color:green"}}})');await wait();
  test('Hostile imports cannot inject mapping markup or executable theme declarations',()=>!d.getElementById('tailwindBridge').querySelector('img,script,style') && !bridgeSource().includes('onerror') && !bridgeSource().includes('color:green') && !bridgeSource().includes('Arial;') && bridgeCell('--space-unit').textContent==='8px' && bridgeSource().includes('--breakpoint-page-stack: 30rem;'));
  reset();await wait();
  test('Project reset refreshes mapping defaults without adding persistence fields',()=>bridgeCell('--space-unit').textContent==='4px' && !Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/tailwind/i.test(key)));
  for(const width of [320,390,1440])for(const studio of ['light','dark']) {
    app.style.width=width+'px';if(d.documentElement.dataset.theme!==studio)d.getElementById('themeToggle').click();
    w.dssShowWizardStep(11);d.getElementById('tailwindMappings').open=true;d.getElementById('tailwindSourceDetails').open=true;await wait();
    test(studio+' Tailwind lesson stays readable and scrolls its table locally at '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['tailwindCopy','tailwindDownload','tailwindInspect'].every(id=>{const r=d.getElementById(id).getBoundingClientRect();return r.height>=44 && r.left>=0 && r.right<=w.innerWidth+1;}) && (width>390 || d.querySelector('.tailwind-table-scroll').scrollWidth>d.querySelector('.tailwind-table-scroll').clientWidth));
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();reset();await wait();
  // Compare against an otherwise identical document without this optional module.
  const bridgeBaselineHtml=(await (await w.fetch('/index.html')).text()).replace(/<script[^>]+src="src\/js\/tailwind-bridge\.js[^>]*><\/script>/g,'').replace(/<link[^>]+href="src\/css\/tailwind-bridge\.css[^>]*>/g,'');
  const bridgeBaseline=d.createElement('iframe');bridgeBaseline.hidden=true;
  await new Promise(resolve=>{bridgeBaseline.onload=resolve;bridgeBaseline.srcdoc=bridgeBaselineHtml;d.body.append(bridgeBaseline);});
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    const config=JSON.parse(evaluate('projectJson()'));config.sampleMode=mode;config.theme=theme;config.spacing=7;config.radius=20;
    w.importConfig(config);bridgeBaseline.contentWindow.importConfig(config);await wait();
    test(mode+' '+theme+' website exports are byte-identical with and without the Tailwind bridge',()=>!bridgeBaseline.contentWindow.DSStudio.tailwind && evaluate('cssExport()')===bridgeBaseline.contentWindow.cssExport() && evaluate('htmlExport()')===bridgeBaseline.contentWindow.htmlExport() && evaluate('projectJson()')===bridgeBaseline.contentWindow.projectJson());
  }
  bridgeBaseline.remove();reset();await wait();

  // Authored website editing establishes its own model below.
  app.style.width='1440px';reset();await wait();
  // Authored website text is distinct from the content-planning proposal.
  {
    const service=w.DSStudio.websiteContent,rows=()=>w.DSStudio.contentArchitecture.nodes();
    const choose=node=>{const button=d.querySelector('[data-content-id="'+node.id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    const save=async()=>{d.getElementById('ia-form').requestSubmit();await wait();};
    const fields=()=>[...d.querySelectorAll('[data-website-field]')];
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1,false);await wait();
      const heading=rows().find(node=>node.sourceKey==='id:hero-title'),original=heading.value,css=evaluate('cssExport()');
      choose(heading);
      test(mode+' authored heading offers a labelled website editor separate from the proposal',()=>fields().length===1 && fields()[0].value===original && d.getElementById('ia-website-reason').textContent==='' && d.getElementById('ia-restore-item').hidden && d.querySelector('label[for="'+fields()[0].id+'"]') && d.getElementById('ia-draft').value===original && !d.getElementById('ia-has-draft').checked);
      input(fields()[0].id,'Unsaved website text');choose(rows().find(node=>node.label==='Footer'));
      test(mode+' website text stays unsaved and selecting another item is guarded',()=>previewDoc().getElementById('hero-title').textContent===original && fields()[0].value==='Unsaved website text' && d.getElementById('ia-selected-name').textContent===heading.label);
      d.getElementById('ia-discard').click();
      test(mode+' discard returns to saved website text without adding an override',()=>fields()[0].value===original && evaluate('state.designProcess.websiteContent.'+mode+'.length')===0);
      const beforeOversize=evaluate('projectJson()');input(fields()[0].id,'x'.repeat(2401));await save();
      test(mode+' over-limit website text is rejected without partially saving the plan',()=>evaluate('projectJson()')===beforeOversize && d.getElementById('ia-status-message').textContent.includes('limits') && fields()[0].value.length===2401);d.getElementById('ia-discard').click();
      const wording='Learners <img src=x onerror="alert(1)"> & their next step';
      input(fields()[0].id,wording);input('ia-draft','A separate planning proposal');await save();
      test(mode+' saved website text reaches preview and inventory as inert text',()=>previewDoc().getElementById('hero-title').textContent===wording && !previewDoc().getElementById('hero-title').querySelector('img') && rows().find(node=>node.id===heading.id).value===wording && rows().find(node=>node.id===heading.id).draft==='A separate planning proposal');
      w.DSStudio.inspector.show({language:'html',section:'all'});await wait();
      const output=evaluate('htmlExport()'),parsed=new w.DOMParser().parseFromString(output,'text/html');
      test(mode+' inspector and standalone HTML share edited content while CSS remains unchanged',()=>d.getElementById('dockCss').textContent===output && parsed.getElementById('hero-title').textContent===wording && parsed.getElementById('hero-title').id==='hero-title' && evaluate('cssExport()')===css);
      const oldDownload=evaluate('download'),downloads=[];w.__contentDownloads=downloads;evaluate('download=(name,content,type)=>window.__contentDownloads.push({name,content,type})');d.querySelector('[data-website-download="html"]').click();w.__restoreContentDownload=oldDownload;evaluate('download=window.__restoreContentDownload');
      test(mode+' actual HTML download uses the edited shared output',()=>downloads.length===1 && downloads[0].name==='index.html' && downloads[0].content===output);
      const project=JSON.parse(evaluate('projectJson()'));w.importConfig(project);await wait();
      test(mode+' project JSON round trip retains website overrides and separate proposals',()=>previewDoc().getElementById('hero-title').textContent===wording && rows().find(node=>node.id===heading.id).draft==='A separate planning proposal' && evaluate('state.designProcess.websiteContent.'+mode+'.length')===1);
      const fileTransfer=new w.DataTransfer();fileTransfer.items.add(new w.File([JSON.stringify(project)],'website-text.json',{type:'application/json'}));d.getElementById('loadFile').files=fileTransfer.files;
      await loadSelectedProjectFile();await wait();
      test(mode+' website text round trips through the real Load JSON file control',()=>previewDoc().getElementById('hero-title').textContent===wording && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode][0].value===wording);
      d.getElementById('jSaveLocal').click();const savedId=d.getElementById('jProjects').value;
      test(mode+' local project save includes validated website edits',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[savedId].data.designProcess.websiteContent[mode][0].value===wording);
      choose(rows().find(node=>node.id===heading.id));input(fields()[0].id,'');await save();
      test(mode+' intentionally blank website text survives a render and JSON normalization',()=>previewDoc().getElementById('hero-title').textContent==='' && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode][0].value==='');
      d.getElementById('ia-undo').click();await wait();
      test(mode+' Undo restores the previous website text and content plan together',()=>previewDoc().getElementById('hero-title').textContent===wording);
      d.getElementById('ia-restore-item').click();
      test(mode+' item restoration is pending until saved',()=>fields()[0].value===original && previewDoc().getElementById('hero-title').textContent===wording && !d.getElementById('ia-discard').disabled);
      await save();
      test(mode+' saving item restoration removes its override while keeping its proposal',()=>previewDoc().getElementById('hero-title').textContent===original && evaluate('state.designProcess.websiteContent.'+mode+'.length')===0 && rows().find(node=>node.id===heading.id).draft==='A separate planning proposal');
      const eyebrow=rows().find(node=>node.label==='Eyebrow' && w.DSStudio.contentArchitecture.path(rows(),node).includes('Home'));choose(eyebrow);
      input(fields()[0].id,mode==='advanced'?' / Learn by making':'Learn by making');await save();
      const mapLabel=mode==='advanced'?evaluate('state.project')+' / Learn by making':'Learn by making';
      test(mode+' edited page eyebrows update visitor sitemap labels with stable anchors',()=>w.DSStudio.sectionSitemap.nodes().find(node=>node.id==='home').label===mapLabel && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.hash==='#home' && a.textContent===mapLabel));
      const alt=rows().find(node=>node.label==='Alternative text');choose(alt);input(fields()[0].id,'');await save();
      test(mode+' an empty image alternative is deliberate and does not change its source',()=>previewDoc().querySelector('#home img').getAttribute('alt')==='' && previewDoc().querySelector('#home img').getAttribute('src').startsWith('data:image/svg+xml'));
      const fieldId=mode==='basic'?'signup-name':'contact-name';choose(rows().find(node=>node.sourceKey==='id:'+fieldId));
      let labelIndex=service.describe('id:'+fieldId,mode).fields.findIndex(field=>field.label==='Field label'),placeholderIndex=service.describe('id:'+fieldId,mode).fields.findIndex(field=>field.field==='placeholder');
      input(fields()[labelIndex].id,'Your preferred name');input(fields()[placeholderIndex].id,'Example <name>');await save();
      test(mode+' form label and placeholder edits preserve control identity and behavior',()=>previewDoc().querySelector('label[for="'+fieldId+'"]').textContent==='Your preferred name' && previewDoc().getElementById(fieldId).placeholder==='Example <name>' && previewDoc().getElementById(fieldId).required && previewDoc().getElementById(fieldId).name==='name');
      const textareaId=mode==='basic'?'signup-question':'contact-message';choose(rows().find(node=>node.sourceKey==='id:'+textareaId));
      const initialIndex=service.describe('id:'+textareaId,mode).fields.findIndex(field=>field.label==='Initial text');input(fields()[initialIndex].id,'My next design question');await save();
      test(mode+' initially empty textarea content can be authored without changing its form binding',()=>previewDoc().getElementById(textareaId).defaultValue==='My next design question' && previewDoc().getElementById(textareaId).name===(mode==='basic'?'question':'message'));
      const selectId=mode==='basic'?'signup-topic':'contact-service',optionNode=rows().find(node=>node.sourceKey==='id:'+selectId+'/option:1'),optionValue=previewDoc().getElementById(selectId).options[1].value;
      choose(optionNode);input(fields()[0].id,'An accessible learning path');await save();
      test(mode+' option wording changes without changing its submitted value',()=>previewDoc().getElementById(selectId).options[1].textContent==='An accessible learning path' && previewDoc().getElementById(selectId).options[1].value===optionValue);
      const listLink=rows().find(node=>node.type==='link' && !node.sourceKey.startsWith('id:top') && node.reference.startsWith('#') && node.label!=='Wordmark');choose(listLink);input(fields()[0].id,'Explore the learning path');await save();
      test(mode+' link wording edits retain the authored destination',()=>new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('a[href="'+listLink.reference+'"]').getAttribute('href')===listLink.reference && rows().find(node=>node.id===listLink.id).value==='Explore the learning path');
      const supporting=rows().find(node=>node.label==='Supporting text' && node.value.startsWith('\u00a9'));choose(supporting);const suffix=fields().length-1;input(fields()[suffix].id,'. Learning together.');await save();
      input('jProject','Studio learners');await wait();
      test(mode+' mixed inline text keeps project-owned identity and its markup connected to Brief',()=>previewDoc().querySelector('.footer-bottom small [data-website-setting="project"]').textContent==='Studio learners' && previewDoc().querySelector('.footer-bottom small').textContent.endsWith('. Learning together.') && previewDoc().querySelector('.footer-brand').textContent==='Studio learners');
      choose(rows().find(node=>node.label==='Wordmark'));
      test(mode+' setting-owned identity explains its existing editor',()=>!fields().length && d.getElementById('ia-website-reason').textContent.includes('Brief'));
      choose(rows().find(node=>node.label==='Footer'));
      test(mode+' containers expose structural guidance rather than flattening their children',()=>!fields().length && d.getElementById('ia-website-reason').textContent.includes('Expand'));
      if(mode==='advanced'){choose(rows().find(node=>node.sourceKey==='id:ia-lab'));test('Generated planning artifacts explain their source instead of accepting text overrides',()=>!fields().length && d.getElementById('ia-website-reason').textContent.includes('Generated'));}
      const beforeSwitch=JSON.parse(evaluate('projectJson()'));d.getElementById(mode==='basic'?'dockModeAdvanced':'dockModeBasic').click();await wait();
      test(mode+' website text overrides are isolated from the other sample',()=>previewDoc().getElementById('hero-title').textContent!=='Explore the learning path' && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode].length===beforeSwitch.designProcess.websiteContent[mode].length && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode==='basic'?'advanced':'basic'].length===0);
      d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
      const missingProject=JSON.parse(evaluate('projectJson()')),otherMode=mode==='basic'?'advanced':'basic',otherField=service.describe('id:hero-title',otherMode).fields[0];missingProject.designProcess.websiteContent[otherMode]=[{...otherField,value:'Other sample saved heading'}];missingProject.designProcess.websiteContent[mode].push({sourceKey:'id:no-longer-authored',field:'text:0',fingerprint:'abc123',value:'Do not put this on another node'},{sourceKey:'id:hero-title',field:'text:0',fingerprint:'changed',value:'Do not overwrite changed source text'});w.importConfig(missingProject);await wait();
      test(mode+' missing source bindings are reported, retained and never assigned elsewhere',()=>d.getElementById('ia-website-missing').textContent.includes('2 saved website text') && !previewDoc().body.textContent.includes('Do not put this on another node') && !previewDoc().body.textContent.includes('Do not overwrite changed source text') && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode].some(row=>row.sourceKey==='id:no-longer-authored'));
      d.getElementById('ia-restore').click();await wait();
      test(mode+' sample restoration clears its website text and content plan while retaining sitemap choices',()=>JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode].length===0 && JSON.parse(evaluate('projectJson()')).designProcess.contentPlan[mode]===null && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[otherMode][0].value==='Other sample saved heading' && previewDoc().querySelector('#home img').alt!=='' && JSON.stringify(JSON.parse(evaluate('projectJson()')).designProcess.sitemapExcluded)===JSON.stringify(missingProject.designProcess.sitemapExcluded));
      d.getElementById('ia-undo').click();await wait();
      test(mode+' Undo sample restoration recovers website text and unmatched records',()=>previewDoc().querySelector('#home img').alt==='' && JSON.parse(evaluate('projectJson()')).designProcess.websiteContent[mode].some(row=>row.sourceKey==='id:no-longer-authored'));
    }
    test('Website import normalization rejects arbitrary attributes, invalid identities and duplicate records',()=>{const valid={sourceKey:'id:hero-title',field:'text:0',fingerprint:'abc123',value:'Safe text'},result=service.normalize([valid,valid,{...valid,field:'onclick'},{...valid,field:'href'},{...valid,fingerprint:''},{...valid,sourceKey:''},{...valid,value:{html:'no'}}]);return result.length===1 && result[0].value==='Safe text';});
    test('Website import normalization bounds text, fields and serialized storage',()=>{const normalized=service.normalize(Array.from({length:2500},(_,i)=>({sourceKey:'id:entry-'+i,field:'text:0',fingerprint:'abc123',value:'x'.repeat(3000)})));return normalized.every(row=>row.value.length===2400) && normalized.length<2000 && JSON.stringify(normalized).length<=service.MAX_TOTAL;});
    test('Website editing produces no captured JavaScript errors',()=>!w.__reviewErrors.length);
    reset();await wait();
  }
  // One Architecture-to-wireframe path stays in integration. The full mirror,
  // geometry/paint/fidelity matrices live in wireframe_review.py.
  {
    app.style.width='1440px';reset();w.importConfig({sampleMode:'basic',base:18});w.dssShowWizardStep(1,false);await wait();
    const heading=w.DSStudio.contentArchitecture.nodes().find(node=>node.sourceKey==='id:hero-title');
    const choice=d.querySelector('[data-content-id="'+heading.id+'"]');for(let parent=choice.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;choice.click();
    input('ia-website-field-0','Wireframe journey <safe> heading');d.getElementById('ia-save').click();await wait();d.getElementById('jSaveLocal').click();
    const project=evaluate('projectJson()'),library=w.localStorage.getItem('dss-v27-projects'),exports=evaluate('[htmlExport(),cssExport()]');
    w.dssShowWizardStep(2,false);w.DSStudio.wireframeView.setFidelity('high');await wait();
    const frame=d.getElementById('wf-page'),doc=frame.contentDocument;
    test('Wireframe journey mirrors saved Architecture wording and current typography',()=>doc.getElementById('hero-title').textContent==='Wireframe journey <safe> heading' && !doc.getElementById('hero-title').querySelector('safe') && frame.contentWindow.getComputedStyle(doc.body).fontSize==='18px' && doc.getElementById('wf-source-styles').textContent.includes(evaluate('cssExport()')) && previewDoc().getElementById('hero-title').textContent===doc.getElementById('hero-title').textContent);
    input('wf-width','390','change');d.getElementById('wf-tab-low').click();await wait();
    test('Wireframe journey viewport and Low Fidelity change only the local view',()=>frame.contentWindow.innerWidth===390 && doc.documentElement.dataset.wfFidelity==='low' && doc.getElementById('wf-low-fidelity-styles') && evaluate('projectJson()')===project && w.localStorage.getItem('dss-v27-projects')===library && JSON.stringify(evaluate('[htmlExport(),cssExport()]'))===JSON.stringify(exports));
    const files=[],oldDownload=w.download;
    try{w.download=(name,content,mime)=>files.push({name,content,mime});d.getElementById('wf-download').click();d.getElementById('wf-tab-high').click();await wait();d.getElementById('wf-download').click();}
    finally{w.download=oldDownload;}
    test('Wireframe journey downloads the selected fidelities without changing website exports',()=>files.length===2 && files.every(file=>file.name==='wireframe.html' && file.mime==='text/html') && files[0].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'low'}) && files[1].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'high'}) && JSON.stringify(evaluate('[htmlExport(),cssExport()]'))===JSON.stringify(exports) && evaluate('projectJson()')===project && w.localStorage.getItem('dss-v27-projects')===library);
    d.getElementById('wf-open-live').click();await wait();
    test('Wireframe journey compares with the real website while retaining the read-only mirror',()=>d.activeElement===d.getElementById('previewShell') && d.getElementById('studio-section-4').open && d.getElementById('wf-page')===frame && frame.contentDocument===doc && frame.sandbox.value==='allow-same-origin' && [...doc.querySelectorAll('input,select,textarea,button')].every(el=>el.inert) && previewDoc().getElementById('hero-title').textContent==='Wireframe journey <safe> heading' && evaluate('projectJson()')===project);
    w.DSStudio.wireframeView.setFidelity('high');app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();await wait();
  }


  // Keep one content-planning journey here; content_tree_review.py owns the
  // complete inventory, branch operations, validation and dirty-form matrices.
  {
    app.style.width='1440px';reset();w.importConfig({sampleMode:'basic'});w.dssShowWizardStep(1,false);await wait();
    const contentModel=w.DSStudio.contentArchitecture;
    const heading=contentModel.nodes().find(node=>node.sourceKey==='id:hero-title');
    const choose=()=>{const button=d.querySelector('[data-content-id="'+heading.id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    choose();input('jProject','Content-tree integration fixture');d.getElementById('jSaveLocal').click();
    const id=d.getElementById('jProjects').value,before=evaluate('projectJson()'),beforeStorage=w.localStorage.getItem('dss-v27-projects'),website=evaluate('htmlExport()');
    input('ia-draft','A clearer introduction for learners.');input('ia-notes','Owner: course tutor. Next action: review.');input('ia-status','needs-content','change');
    test('Content-tree journey keeps unsaved proposals outside the model and local save',()=>evaluate('projectJson()')===before && w.localStorage.getItem('dss-v27-projects')===beforeStorage && !d.getElementById('ia-discard').disabled && previewDoc().getElementById('hero-title').textContent===heading.value);
    d.getElementById('ia-save').click();await wait();
    const saved=evaluate('projectJson()');
    test('Content-tree journey saves proposal data locally without rewriting the actual website',()=>{
      const node=contentModel.nodes().find(row=>row.id===heading.id),stored=JSON.parse(w.localStorage.getItem('dss-v27-projects'))[id].data.designProcess.contentPlan.basic.find(row=>row.id===heading.id);
      return node.draft==='A clearer introduction for learners.' && node.status==='needs-content' && stored.draft===node.draft && stored.notes===node.notes && previewDoc().getElementById('hero-title').textContent===heading.value && evaluate('htmlExport()')===website;
    });
    const files=[],oldDownload=w.download;
    try{w.download=(name,content,type)=>files.push({name,content,type});d.getElementById('jExportJson').click();}
    finally{w.download=oldDownload;}
    input('ia-draft','Discard this temporary wording');d.getElementById('ia-discard').click();
    const discarded=evaluate('projectJson()')===saved && d.getElementById('ia-draft').value==='A clearer introduction for learners.';
    d.getElementById('ia-undo').click();await wait();
    test('Content-tree journey Discard and Undo restore the correct saved state',()=>discarded && evaluate('projectJson()')===before && contentModel.nodes().find(row=>row.id===heading.id).draft===null && evaluate('htmlExport()')===website);
    const libraryBeforeFile=w.localStorage.getItem('dss-v27-projects');
    await importFile(files[0].content);await wait();choose();
    test('Content-tree journey downloaded JSON restores the proposal and editor without overwriting saved projects',()=>files[0].name==='design-system-studio.json' && files[0].type==='application/json' && files[0].content===saved && evaluate('projectJson()')===saved && contentModel.nodes().find(row=>row.id===heading.id).draft==='A clearer introduction for learners.' && d.getElementById('ia-draft').value==='A clearer introduction for learners.' && w.localStorage.getItem('dss-v27-projects')===libraryBeforeFile && previewDoc().getElementById('hero-title').textContent===heading.value);
    app.style.width='1440px';reset();await wait();
  }

  reset();await wait();
  test('No interaction JavaScript errors', () => !w.__reviewErrors.length);
  document.getElementById('results').textContent=JSON.stringify({results, errors:w.__reviewErrors});
};
</script>'''


def main():
    return run_review(HARNESS)


if __name__ == '__main__':
    raise SystemExit(main())
