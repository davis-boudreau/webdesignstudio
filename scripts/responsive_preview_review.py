"""Independent responsive preview checks using the local Chrome runner.

Run: python scripts/responsive_preview_review.py. Owns its app, profile and fixtures.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Responsive Preview review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
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
  const prepare=async()=>{
    app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();
    reset();w.DSStudio.inspector.show({language:'css',section:'all'});d.querySelector('[data-width="desktop"]').click();w.dssShowWizardStep(0,false);await wait();
  };
  try {
  test('Independent responsive preview startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  await prepare();
  for (const width of [320,390,768,1440]) {
    app.style.width=width+'px'; await wait();
    test('Page fits '+width+'px viewport', () => {
      if (d.documentElement.scrollWidth<=w.innerWidth+1) return true;
      throw Error(JSON.stringify({viewport:w.innerWidth,page:d.documentElement.scrollWidth,overflow:[...d.querySelectorAll('body *')].filter(el=>el.getBoundingClientRect().right>w.innerWidth+1 && el.getBoundingClientRect().width>0 && !el.closest('table,pre,.preview-shell,.studio-code-dock,.studio-section-nav')).slice(0,12).map(el=>({id:el.id,tag:el.tagName,cls:el.className,width:el.getBoundingClientRect().width,right:el.getBoundingClientRect().right}))}));
    });
  }
  const desktopPanes=[];
  for (const width of [1281,1440,1920,2560,3440]) {
    app.style.width=width+'px'; await wait();
    const left=d.querySelector('.sidebar').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect(), right=d.querySelector('.studio-code-dock').getBoundingClientRect();
    const shell=d.querySelector('body > .shell').getBoundingClientRect();
    desktopPanes.push({width, left:left.width, centre:centre.width, right:right.width, shell:shell.width});
    test('Three desktop columns keep the builder at 25% and cap the inspector at 25% at '+width+'px', () => Math.abs(left.width-(d.querySelector('.layout').clientWidth-16)/4)<1 && Math.abs(centre.left-left.right-16)<1 && Math.abs(right.left-centre.right-16)<1 && Math.abs(centre.width-right.width*2)<1 && right.width<=(d.querySelector('.layout').clientWidth-16)/4+1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  test('All three columns grow across large and ultrawide screens', () => {
    const first=desktopPanes.find(pane=>pane.width===1440), last=desktopPanes.at(-1);
    return last.left>first.left && last.centre>first.centre && last.right>first.right;
  });
  app.style.width='1280px'; await wait();
  test('Inspector stacks after the centre when three columns would be cramped', () => {
    const left=d.querySelector('.sidebar').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect(), right=d.querySelector('.studio-code-dock').getBoundingClientRect();
    return Math.abs(left.width-(d.querySelector('.layout').clientWidth-16)/4)<1 && Math.abs(centre.left-right.left)<1 && right.top>=centre.bottom && d.documentElement.scrollWidth<=w.innerWidth+1;
  });
  app.style.width='900px'; await wait();
  test('Side panes stack at tablet widths without horizontal page overflow', () => w.getComputedStyle(d.querySelector('.sidebar')).position==='static' && Math.abs(d.querySelector('.sidebar').getBoundingClientRect().left-d.getElementById('main').getBoundingClientRect().left)<1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  app.style.width='1440px'; await wait();
  for (const [mode,width] of [['mobile',390],['tablet',768],['desktop',1280]]) {
    d.querySelector('button[data-width="'+mode+'"]').click(); await wait();
    test('Preview has exact '+mode+' width', () => {
      const frame=d.getElementById('previewFrame'), actual=frame.getBoundingClientRect().width;
      if (Math.abs(actual-width)>=1) throw Error(`Expected ${width}px; got ${actual}px; mode=${frame.dataset.width}; transition=${w.getComputedStyle(frame).transition}`);
      return true;
    });
    test('Preview typography matches the '+mode+' viewport readout', () => {
      const actual=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontSize);
      const expected=evaluate(`fluidTypePx(5,${width})`);
      if (Math.abs(actual-expected)>.11) throw Error(`Expected ${expected}px; got ${actual}px`);
      return true;
    });
    test('Generated document has an exact '+mode+' viewport', () => previewWindow().innerWidth===width);
    test('Generated sample reflows inside the '+mode+' viewport', () => previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1);
  }
  reset(); await wait();
  await prepare();
  d.getElementById('dockTabHtml').click();await wait();
  const actionDocument=previewDoc(), actionProject=evaluate('projectJson()');
  for (const link of [...previewDoc().querySelectorAll('.sample-lesson-card a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Field-guide lesson link to '+link.getAttribute('href')+' browses its live example', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2 && evaluate('projectJson()')===actionProject);
  }
  for (const link of [...previewDoc().querySelectorAll('.sample-section-actions a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Preview '+link.closest('section').id+' action to '+link.getAttribute('href')+' browses its destination', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2 && evaluate('projectJson()')===actionProject);
  }
  test('Live preview uses the generated HTML and CSS without a second stylesheet request', () => {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return previewDoc().querySelector('h1').outerHTML===parsed.querySelector('h1').outerHTML && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && !previewDoc().querySelector('link[rel="stylesheet"]');
  });
  test('Export and live preview use Home, About, Resources and Contact footer shortcuts in order', () => {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return [parsed,previewDoc()].every(doc=>JSON.stringify([...doc.querySelectorAll('footer nav[aria-label="Footer navigation"] a')].map(link=>[link.textContent,link.getAttribute('href')]))===JSON.stringify([['Home','#home'],['About','#about'],['Resources','#resources'],['Contact','#contact']]));
  });
  for (const link of [...previewDoc().querySelectorAll('footer nav[aria-label="Footer navigation"] a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Preview footer '+link.textContent+' link browses its section', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2);
  }
  test('Live preview sandbox supports form validation while blocking scripts and top navigation', () => {
    const sandbox=d.getElementById('previewPage').sandbox;
    return sandbox.contains('allow-same-origin') && sandbox.contains('allow-forms') && !sandbox.contains('allow-scripts') && !sandbox.contains('allow-top-navigation');
  });
  d.getElementById('dockTabHtml').click();
  d.getElementById('jSaveLocal').click();
  const themedProject=d.getElementById('jProjects').value;
  const bothThemeCss=evaluate('cssExport()');
  input('dockTheme','dark','change'); await wait();
  test('Inspector theme selection synchronizes project editors, preview and exported HTML', () => evaluate('state.theme')==='dark' && d.documentElement.dataset.projectTheme==='dark' && d.documentElement.dataset.theme==='light' && d.getElementById('jTheme').value==='dark' && d.getElementById('previewTheme').value==='dark' && previewDoc().documentElement.dataset.theme==='dark' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('previewPage').title.includes('dark'));
  test('Inspector theme is saved to the active project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='dark');
  test('Theme selection retains a CSS export containing both theme definitions', () => evaluate('cssExport()')===bothThemeCss && evaluate('cssExport()').includes('[data-theme="dark"]'));
  input('previewTheme','light','change'); await wait();
  test('Preview theme control synchronizes the inspector and saved project', () => d.getElementById('dockTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='light');
  const savedBeforeStudioToggle=JSON.stringify(saved()), filesBeforeStudioToggle=evaluate('[projectJson(),htmlExport(),cssExport()]');
  d.getElementById('themeToggle').click(); await wait();
  test('Studio appearance leaves the active saved project and exported files unchanged',()=>JSON.stringify(saved())===savedBeforeStudioToggle && JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'))===JSON.stringify(filesBeforeStudioToggle));
  test('Studio appearance toggle leaves page theme controls and preview unchanged', () => d.documentElement.dataset.theme==='dark' && d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light');
  evaluate('importConfig({project:"Imported theme",theme:"light",studioAppearance:"light"})'); await wait();
  test('Imported theme reaches both selectors and the generated preview', () => d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && previewDoc().title.includes('Imported theme'));
  test('Imported project cannot override the local Studio preference',()=>d.documentElement.dataset.theme==='dark' && w.localStorage.getItem('dss-studio-appearance')==='dark');
  d.getElementById('jProjects').value=themedProject;d.getElementById('jLoadLocal').click();await wait();
  test('Loading a saved project preserves Studio appearance and restores its page theme',()=>d.documentElement.dataset.theme==='dark' && evaluate('state.theme')==='light' && d.getElementById('previewTheme').value==='light');
  reset();await wait();
  test('Project reset preserves Studio appearance',()=>d.documentElement.dataset.theme==='dark' && evaluate('state.theme')==='light');
  d.getElementById('themeToggle').click();
  input('jProject','Live preview'); input('jPrimary','#294f77'); input('bdSize','lg'); await wait();
  test('Preview imagery and component classes follow live project changes', () => previewDoc().querySelector('.sample-brand').textContent.includes('Live preview') && decodeURIComponent(previewDoc().querySelector('img').src).includes(evaluate('palette().roles.primary')) && !!previewDoc().querySelector('.ds-button--lg') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  test('Tutorial palette readouts and swatches follow live semantic roles', () => {
    const expected=evaluate('[palette().roles.primary,palette().roles.secondary,palette().roles.accent]');
    return [...previewDoc().querySelectorAll('.sample-token-palette li')].every((item,i)=>item.querySelector('code').textContent===expected[i] && previewWindow().getComputedStyle(item.querySelector('.sample-palette-dot')).backgroundColor===evaluate(`'rgb('+hexRgb('${expected[i]}').join(', ')+')'`));
  });
  test('Tutorial typography readouts follow live wizard settings', () => JSON.stringify([...previewDoc().querySelectorAll('.sample-type-settings dd')].map(item=>item.textContent))===JSON.stringify(evaluate('[state.base+"px",String(state.ratio),String(state.leading)]')));
  const browsingDoc=previewDoc(), studioHash=w.location.hash;
  previewDoc().querySelector('header a[href="#resources"]').click(); await wait();
  test('Sample navigation scrolls within the generated page without opening the studio inside it', () => previewDoc()===browsingDoc && previewWindow().scrollY>0 && Math.abs(previewDoc().getElementById('resources').getBoundingClientRect().top-24)<2 && previewWindow().location.href.startsWith('about:srcdoc') && w.location.hash===studioHash);
  previewDoc().querySelector('a[href="#working-together"]').click(); await wait();
  test('Sample resource links reveal their FAQ destination inside the preview', () => previewDoc().getElementById('working-together').open && previewDoc()===browsingDoc);
  previewDoc().getElementById('contact-name').value='Taylor';
  previewDoc().getElementById('contact-email').value='taylor@example.com';
  previewDoc().querySelector('input[name="copy"]').checked=true;
  previewDoc().querySelector('input[value="workshop"]').checked=true;
  previewWindow().scrollTo(0,500); await wait();
  const originalNameControl=previewDoc().getElementById('contact-name'), browsePosition=previewWindow().scrollY;
  input('jRadius',20); await wait();
  test('CSS-only edits preserve browsing position, controls and entered values', () => previewDoc().getElementById('contact-name')===originalNameControl && originalNameControl.value==='Taylor' && Math.abs(previewWindow().scrollY-browsePosition)<2 && previewWindow().getComputedStyle(previewDoc().querySelector('img')).borderRadius==='20px');
  input('dockTheme','dark','change'); await wait();
  test('HTML and theme refreshes preserve entered fields, choices, FAQs and scroll', () => previewDoc()===browsingDoc && previewDoc().getElementById('contact-name')!==originalNameControl && previewDoc().getElementById('contact-name').value==='Taylor' && previewDoc().querySelector('input[name="copy"]').checked && previewDoc().querySelector('input[value="workshop"]').checked && previewDoc().getElementById('working-together').open && Math.abs(previewWindow().scrollY-browsePosition)<2);
  const previewAddress=previewWindow().location.href;
  previewDoc().querySelector('form').requestSubmit(); await wait();
  test('Sample form submission remains in the preview without sending an enquiry', () => previewWindow().location.href===previewAddress && previewDoc().getElementById('contact-note').textContent.includes('No enquiry has been sent'));
  d.querySelector('button[data-width="fluid"]').click(); app.style.width='390px'; await wait();
  const firstFluidWidth=previewWindow().innerWidth;
  test('Fluid preview uses its actual available viewport at mobile width', () => Math.abs(firstFluidWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<1 && previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  app.style.width='768px'; await wait();
  test('Fluid preview follows pane resizing and retains entered form values', () => previewWindow().innerWidth>firstFluidWidth && Math.abs(previewWindow().innerWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<1 && previewDoc().getElementById('contact-name').value==='Taylor');
  input('jProject','Safe </style><script>parent.__previewInjection=1</scr'+'ipt>'); await wait();
  test('Preview inserts generated CSS as text and keeps project markup escaped', () => !w.__previewInjection && !previewDoc().querySelector('script') && previewDoc().querySelector('.sample-brand').textContent.includes('</style><script>') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && previewDoc().styleSheets[0].cssRules.length>0);
  reset(); await wait();
  d.querySelector('button[data-width="mobile"]').click(); await wait();
  previewDoc().getElementById('sample-menu').querySelector('summary').click();
  input('jAccent','#D97706'); await wait();
  test('Open preview hamburger follows live accent edits and retains its open state', () => previewDoc().getElementById('sample-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-menu-icon')).stroke==='rgb(217, 119, 6)' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  input('dockTheme','dark','change'); await wait();
  test('Preview hamburger follows the dark theme accent', () => previewDoc().getElementById('sample-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-menu-icon')).stroke===evaluate("'rgb('+hexRgb(palette('dark').roles.accent).join(', ')+')'"));
  const beforeMenuNavigation=evaluate('projectJson()');
  previewDoc().getElementById('sample-mobile-navigation').querySelector('a[href="#services"]').click(); await wait();
  test('Opened mobile menu links browse the generated page without changing its project settings', () => Math.abs(previewDoc().getElementById('services').getBoundingClientRect().top-24)<2 && previewWindow().location.href.startsWith('about:srcdoc') && evaluate('projectJson()')===beforeMenuNavigation);
  const menuProject=evaluate('projectJson()');
  previewDoc().getElementById('sample-menu').querySelector('summary').click();
  test('Closing the mobile menu changes only the preview disclosure', () => !previewDoc().getElementById('sample-menu').open && evaluate('projectJson()')===menuProject);
  input('jProject','A long project name that should wrap beside the mobile menu without hiding the navigation'); await wait();
  test('Mobile header accommodates long project names without overflowing', () => previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1 && previewDoc().getElementById('sample-menu').querySelector('summary').getBoundingClientRect().width>=44);
  reset(); await wait();
  const previousHeaderSize=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontSize);
  input('jProject','Harbour House'); input('jRatio',1.4); await wait();
  test('Live header title follows the project name and heading typography', () => previewDoc().querySelector('header .sample-brand-title').textContent==='Harbour House' && previewDoc().querySelector('header .sample-logo').textContent==='Logo' && parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontSize)>previousHeaderSize && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  reset(); await wait();
  test('Reset restores the light theme across the inspector and preview', () => d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light');
  await prepare();
  // Detailed Brief contracts now run in planning_review.py.
  reset();await wait();
  d.querySelector('[data-journey-step="9"]').click();
  test('Responsive is a distinct phase between Layout and Accessibility with grid controls and a centre lesson', () => !d.querySelector('[data-journey-pane="9"]').hidden && d.getElementById('advColumns').closest('[data-journey-pane]').dataset.journeyPane==='9' && !d.getElementById('responsiveDesign').hidden && d.getElementById('responsiveDesign').open);
  test('Responsive page tokens are classified as Layout and route to the correct wizard controls', () => w.dssReadTokens().filter(row=>row.name.startsWith('--page-')).every(row=>row.type==='Layout') && [['--page-max-width','responsive-maxWidth'],['--page-gutter','responsive-gutter'],['--page-gutter-wide','responsive-wideGutter']].every(([name,id])=>w.dssTokenSource({name}).step===9 && w.dssTokenSource({name}).control===id));
  evaluate('importConfig({responsiveDesign:{stack:960,wide:1,maxWidth:1e9,gutter:-20,wideGutter:"evil"}})');
  test('Responsive imports bound lengths and keep ordered breakpoints', () => evaluate('state.responsiveDesign.stack===960 && state.responsiveDesign.wide===1120 && state.responsiveDesign.maxWidth===1600 && state.responsiveDesign.gutter===8 && state.responsiveDesign.wideGutter===32'));
  evaluate('importConfig({responsiveDesign:{stack:NaN,wide:Infinity,maxWidth:null,gutter:"48",wideGutter:NaN}})');
  test('Nonfinite or nonnumeric responsive imports use safe defaults', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  for (const value of [null,[],42,'bad']) {
    evaluate('importConfig({responsiveDesign:'+JSON.stringify(value)+'})');
    test('Malformed responsive data '+JSON.stringify(value)+' uses defaults', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  }
  evaluate('importConfig({responsiveDesign:{stack:701,wide:1001,maxWidth:1237,gutter:19,wideGutter:37}})'); await wait();
  test('Valid responsive lengths retain exact imported values in sliders and exports', () => ['stack','wide','maxWidth','gutter','wideGutter'].every(key=>Number(d.getElementById('responsive-'+key).value)===evaluate('state.responsiveDesign.'+key)) && evaluate('state.responsiveDesign.stack===701 && state.responsiveDesign.maxWidth===1237'));
  reset(); d.getElementById('jSaveLocal').click(); const responsiveProjectId=d.getElementById('jProjects').value;
  for (const [key,value] of Object.entries({stack:640,wide:1152,maxWidth:1280,gutter:20,wideGutter:40})) input('responsive-'+key,value);
  await wait();
  const responsiveData=evaluate('JSON.stringify(state.responsiveDesign)'), responsiveJson=evaluate('projectJson()');
  test('Responsive lesson reports the actual preview media-query state', () => {
    const narrow=previewWindow().matchMedia('(max-width: 40rem)').matches;
    return d.getElementById('responsiveLessonViewport').textContent.includes(narrow?'Narrow: main sections stack.':'Main sections can sit side by side.');
  });

  test('Responsive controls update outputs, source recipes, preview and active local save', () => d.getElementById('responsive-stackOut').textContent.includes('40rem') && d.getElementById('responsiveRecipe').textContent.includes('@media (max-width: 40rem)') && d.getElementById('responsiveLessonViewport').textContent.includes('Current preview:') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[responsiveProjectId].data.responsiveDesign)===responsiveData);
  reset(); evaluate('importConfig('+responsiveJson+')'); await wait();
  test('Responsive settings round trip through project JSON and synchronize sliders', () => evaluate('JSON.stringify(state.responsiveDesign)')===responsiveData && d.getElementById('responsive-wide').value==='1152');
  const responsivePage=d.createElement('iframe'); responsivePage.style.cssText='width:1440px;height:1000px;border:0';
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();
    for (const theme of ['light','dark']) {
      input('jTheme',theme); await wait();
      const css=evaluate('cssExport()');
      test(mode+' '+theme+' exports literal breakpoints and shared container values', () => css.includes('@media (max-width: 40rem)') && css.includes('@media (min-width: 72rem)') && css.includes('--page-max-width: 80rem;') && css.includes('--page-gutter: 1.25rem;') && !/@media[^\{]*var\(/.test(css));
      responsivePage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+css+'</style>');
      await new Promise(resolve=>{responsivePage.onload=resolve;if(!responsivePage.isConnected)d.body.append(responsivePage);});
      const pd=responsivePage.contentDocument,pw=responsivePage.contentWindow;
      for (const width of [639,640,641,1151,1152,1153,1440]) {
        responsivePage.style.width=width+'px'; await wait();
        test(mode+' '+theme+' obeys configured cutoffs and gutters at '+width+'px', () => {
          const container=pw.getComputedStyle(pd.querySelector('.container'));
          const composition=pw.getComputedStyle(pd.querySelector(mode==='basic'?'.skills-layout':'.sample-hero'));
          const columns=mode==='basic'?(composition.flexDirection==='column'?1:2):composition.gridTemplateColumns.split(' ').length;
          return pd.documentElement.scrollWidth<=width+1 && container.maxWidth==='1280px' && container.paddingLeft===(width>=1152?'40px':'20px') && columns===(width<=640?1:mode==='basic'?2:12);
        });
      }
      if (mode==='advanced') test('Advanced grid recipe reflects the edited breakpoint', () => pd.querySelector('.sample-code-solution code').textContent.includes('@media (max-width: 40rem)'));
    }
  }
  responsivePage.remove();
  test('Changing sample modes preserves shared responsive decisions', () => evaluate('JSON.stringify(state.responsiveDesign)')===responsiveData);
  reset(); await wait();
  test('Reset restores responsive defaults without mutating the starter object', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults()) && JSON.stringify(DEFAULT.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  d.getElementById('dockModeBasic').click(); await wait();
  test('Basic lists lesson contains unordered, ordered and description lists with titles', () => previewDoc().querySelectorAll('#lists .list-grid > article').length===3 && ['ul','ol','dl'].every(selector=>previewDoc().querySelector('#lists .list-grid '+selector)) && [...previewDoc().querySelectorAll('#lists .list-grid > article')].every(card=>card.querySelector('h3')));
  // Project replacement starts a new browsing session even when output is identical.
  for(const mode of ['basic','advanced']) {
    await prepare();w.importConfig({sampleMode:mode});await wait();
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    const fieldId=mode==='basic'?'signup-name':'contact-name',doc=previewDoc();
    const seed=()=>{previewDoc().getElementById(fieldId).value='Replacement visitor';previewDoc().getElementById('footer-sitemap').open=true;previewWindow().scrollTo(0,240);};
    const fresh=()=>previewDoc()===doc && previewDoc().getElementById(fieldId).value==='' && !previewDoc().getElementById('footer-sitemap').open && Math.abs(previewWindow().scrollY)<1;
    seed();input('jRadius',22);await wait();
    const snapshot=evaluate('projectJson()'),html=evaluate('htmlExport()'),css=evaluate('cssExport()'),library=w.localStorage.getItem('dss-v27-projects');
    test(mode+' ordinary live edits retain entered form values and open native disclosures',()=>previewDoc()===doc && previewDoc().getElementById(fieldId).value==='Replacement visitor' && previewDoc().getElementById('footer-sitemap').open && Math.abs(previewWindow().scrollY-240)<2);
    w.importConfig(JSON.parse(snapshot));await wait();
    test(mode+' identical project import clears browsing state in the original preview document',()=>fresh() && evaluate('projectJson()')===snapshot && evaluate('htmlExport()')===html && evaluate('cssExport()')===css && w.localStorage.getItem('dss-v27-projects')===library);
    seed();d.getElementById('jProjects').value=projectId;d.getElementById('jLoadLocal').click();await wait();
    test(mode+' loading identical saved values clears browsing without altering the saved project',()=>fresh() && evaluate('projectJson()')===snapshot && w.localStorage.getItem('dss-v27-projects')===library);
    seed();await importFile(snapshot);await wait();
    test(mode+' identical JSON file replacement clears browsing and protects the local library',()=>fresh() && evaluate('projectJson()')===snapshot && previewDoc().getElementById('dssPreviewStyles').textContent===css && w.localStorage.getItem('dss-v27-projects')===library);
    seed();if(mode==='advanced')reset();else evaluate('resetStudio()');await wait();
    test(mode+' project reset clears browsing even when Basic and Advanced changes are coalesced',()=>fresh() && evaluate('state.radius')===12 && w.localStorage.getItem('dss-v27-projects')===library);
    seed();d.getElementById('jNewLocal').click();if(mode==='advanced')d.getElementById('dockModeAdvanced').click();await wait();
    test(mode+' New starts a fresh browsing session while retaining saved projects',()=>fresh() && evaluate('state.sampleMode')===mode && w.localStorage.getItem('dss-v27-projects')===library);
  }
  test('No responsive preview JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Focused harness completed',pass:false,error:String(error.stack||error)});}
  document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
