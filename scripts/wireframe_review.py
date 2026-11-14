"""Independent read-only wireframe mirror and fidelity browser checks.

Run: python scripts/wireframe_review.py. Uses its own isolated app/profile and
shared Chrome runner, without importing or replacing the integration harness.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Wireframe review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Wireframe review: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const input=(id,value,type='input')=>{
    const el=d.getElementById(id);w.DSStudio.paletteWorkspace?.revealControl(el);w.DSStudio.typographyWorkspace?.revealControl(el);
    el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
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
  test('Independent wireframe startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  app.style.width='1440px';reset();w.DSStudio.wireframeView.setFidelity('high');input('wf-width','live','change');await wait();
  // Read-only wireframes use the actual website HTML and responsive CSS.
  {
    const engine=w.DSStudio.wireframeEngine;
    const compareWireframePaint=(reference,mirror)=>{
      const nodes=doc=>[doc.body,...doc.body.querySelectorAll('*')].filter(el=>!el.matches('script,iframe,object,embed,base'));
      const original=nodes(reference),copied=nodes(mirror),properties=['backgroundColor','backgroundImage','color','borderTopColor','opacity'],differences=[];
      if(original.length!==copied.length)throw Error('Paint comparison element count differs: '+original.length+' / '+copied.length);
      original.forEach((el,index)=>{const other=copied[index],expected=reference.defaultView.getComputedStyle(el),actual=mirror.defaultView.getComputedStyle(other);for(const property of properties)if(expected[property]!==actual[property])differences.push({element:el.tagName+'.'+el.className,property,expected:expected[property],actual:actual[property]});});
      if(differences.length)throw Error(JSON.stringify(differences.slice(0,5)));return true;
    };

    for(const mode of ['basic','advanced']) {
      reset();await wait();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
      w.dssShowWizardStep(2,false);w.dssRevealSection('process-wireframe',false);await wait();w.DSStudio.wireframeView.refresh();await wait();
      const frame=d.getElementById('wf-page'),doc=frame.contentDocument;
      const source=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      test(mode+' wireframe retains actual website structure and wording',()=>doc.body.textContent===source.body.textContent && JSON.stringify([...doc.querySelectorAll('body [id]')].map(el=>el.id))===JSON.stringify([...source.querySelectorAll('body [id]')].map(el=>el.id)));
      test(mode+' wireframe exposes page, content-width, layout and child containers',()=>['region','content','layout','item'].every(kind=>doc.querySelector('[data-wf-container="'+kind+'"]')) && doc.querySelector(mode==='basic'?'.hero-layout[data-wf-layout="grid"]':'.sample-hero[data-wf-layout="grid"]') && d.querySelector('.wf-container-key').textContent.includes('Grid/Flex'));
      test(mode+' wireframe distinguishes container boundaries without adding layout borders',()=>['region','content','layout','item'].every(kind=>{const el=[...doc.querySelectorAll('[data-wf-container="'+kind+'"]')].find(node=>node.getBoundingClientRect().height>0);return el && frame.contentWindow.getComputedStyle(el).outlineStyle===({region:'solid',content:'dashed',layout:'dotted',item:'solid'})[kind];}));
      test(mode+' wireframe reveals nested list, disclosure and normal-flow groups',()=>doc.querySelector('main li[data-wf-container="item"]') && doc.querySelector('main details[data-wf-container="item"]') && [...doc.querySelectorAll('main div[data-wf-container="item"]')].some(el=>!el.dataset.wfLayout) && [...doc.querySelectorAll('[data-wf-container]')].every(el=>(el.getAttribute('title')||'').length>0));
      test(mode+' wireframe outlines text, inline links, controls and outer illustrations as page objects',()=>['h1','p','a','button','input','label','summary','td','th','svg'].every(selector=>[...doc.querySelectorAll(selector)].every(el=>el.hasAttribute('data-wf-container'))) && [...doc.querySelectorAll('svg *')].every(el=>!el.hasAttribute('data-wf-container')) && doc.querySelector('[aria-hidden="true"][data-wf-container="object"]'));
      const folded=[...doc.querySelectorAll('details:not([open])')].find(el=>el.getBoundingClientRect().height>0);if(folded){folded.open=true;await wait();const object=[...folded.querySelectorAll('[data-wf-container="object"]')].find(el=>el.getBoundingClientRect().height>0);test(mode+' newly disclosed content already has page-object boundaries',()=>object && frame.contentWindow.getComputedStyle(object).outlineStyle!=='none');folded.open=false;await wait();}

      test(mode+' wireframe identifies its selected sample without colour alone',()=>d.getElementById('wf-'+mode).getAttribute('aria-pressed')==='true' && w.getComputedStyle(d.getElementById('wf-'+mode),'::before').content.includes(String.fromCharCode(0x2713)));
      test(mode+' wireframe has no layout or content authoring controls',()=>!d.querySelector('#wf-scope,#wf-layout,#wf-content,#wf-emphasis,#plan-layout,#plan-wireframeNotes') && frame.sandbox.value==='allow-same-origin');
      test(mode+' wireframe makes website controls inert and removes executable or nested embeds',()=>[...doc.querySelectorAll('input,select,textarea,button')].every(el=>el.inert) && !doc.querySelector('script,iframe,object,embed,base,a[href]:not([href^="#"])'));
      const before=JSON.stringify(JSON.parse(evaluate('projectJson()')).designProcess);
      const reference=d.createElement('iframe');reference.style.cssText='height:768px;border:0';
      reference.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+w.DSStudio.fonts.previewCss()+'</style>');
      await new Promise(resolve=>{reference.onload=resolve;d.body.append(reference);});
      for(const width of [320,390,768,1280]) {
        input('wf-width',String(width),'change');reference.style.width=width+'px';await wait();
        test(mode+' wireframe matches live responsive geometry at '+width+'px',()=>{
          const rd=reference.contentDocument,differences=[];
          const ids=[...rd.querySelectorAll('body [id]')].filter(el=>el.getBoundingClientRect().height>0).map(el=>el.id);
          for(const id of ids){const a=rd.getElementById(id).getBoundingClientRect(),b=doc.getElementById(id).getBoundingClientRect();if(['x','y','width','height'].some(key=>Math.abs(a[key]-b[key])>1))differences.push({id,a:[a.x,a.y,a.width,a.height],b:[b.x,b.y,b.width,b.height]});}
          // Include un-ID'd wrappers and their children, not just semantic IDs.
          const original=[...rd.body.querySelectorAll('*')],mirrored=[...doc.body.querySelectorAll('*')];
          for(const el of doc.querySelectorAll('[data-wf-container]')){const source=original[mirrored.indexOf(el)],a=source.getBoundingClientRect(),b=el.getBoundingClientRect();if(['x','y','width','height'].some(key=>Math.abs(a[key]-b[key])>1))differences.push({container:el.className,kind:el.dataset.wfContainer});}
          if(differences.length)throw Error(JSON.stringify(differences.slice(0,4)));
          return frame.contentWindow.innerWidth===width;
        });
        test(mode+' default wireframe component backgrounds and text match website at '+width+'px',()=>compareWireframePaint(reference.contentDocument,doc));
        test(mode+' every rendered wireframe object has a visible boundary at '+width+'px',()=>{
          const missing=[];for(const el of doc.body.querySelectorAll('*')){
            if(el.matches('script,style,link,meta,title,base,template,source,track,br,wbr') || (el.namespaceURI==='http://www.w3.org/2000/svg' && (el.localName!=='svg' || el.parentElement?.closest('svg'))))continue;
            const style=frame.contentWindow.getComputedStyle(el);if(style.visibility==='hidden' || ![...el.getClientRects()].some(rect=>rect.width>0 && rect.height>0))continue;
            if(!el.dataset.wfContainer || style.outlineStyle==='none' || parseFloat(style.outlineWidth)<1)missing.push(el.tagName+'.'+el.className);
          }if(missing.length)throw Error(JSON.stringify(missing.slice(0,10)));return true;
        });
      }
      const focusLink=[...doc.querySelectorAll('a[href]:not(.ds-button)')].find(el=>el.getBoundingClientRect().height>0);
      if(focusLink){focusLink.focus();const focusStyle=frame.contentWindow.getComputedStyle(focusLink);test(mode+' page-object borders preserve the distinct keyboard focus ring',()=>focusLink.matches(':focus-visible') && focusStyle.outlineWidth==='3px' && focusStyle.outlineOffset==='3px');focusLink.blur();}
      reference.remove();
      test(mode+' viewing widths does not alter saved Architecture or planning data',()=>JSON.stringify(JSON.parse(evaluate('projectJson()')).designProcess)===before);
      const exported=engine.documentHtml(),parsed=new w.DOMParser().parseFromString(exported,'text/html');
      test(mode+' wireframe download contains original CSS plus outlines and inert controls',()=>parsed.getElementById('wf-source-styles').textContent.includes(evaluate('cssExport()')) && parsed.getElementById('wf-outline-styles') && parsed.querySelector('[data-wf-container="layout"]') && parsed.body.textContent===source.body.textContent && !parsed.querySelector('script,iframe') && [...parsed.querySelectorAll('input,select,textarea,button')].every(el=>el.inert));
      const files=[],original=w.download;w.download=(name,content,mime)=>files.push({name,content,mime});d.getElementById('wf-download').click();w.download=original;
      test(mode+' wireframe button downloads the read-only mirror',()=>files.length===1 && files[0].name==='wireframe.html' && files[0].content===exported);
      const legacy=JSON.parse(evaluate('projectJson()'));legacy.designProcess.wireframes[mode]={scope:'content-absent',content:'proposed',layout:'grid',blocks:[{id:'content-absent',layout:'split',emphasis:'primary'}]};w.importConfig(legacy);await wait();w.DSStudio.wireframeView.refresh();await wait();
      test(mode+' old authoring settings round-trip without changing the mirrored website',()=>engine.documentHtml()===exported && JSON.parse(evaluate('projectJson()')).designProcess.wireframes[mode].layout==='grid');
      const content=w.DSStudio.websiteContent,heading=w.DSStudio.contentArchitecture.nodes().find(node=>node.sourceKey==='id:hero-title');
      const fields=content.describe(heading.sourceKey,mode).fields;
      const edited=content.merge(mode,fields.map(field=>({...field,value:'Updated <safe> website heading'})));
      evaluate('state.designProcess.websiteContent['+JSON.stringify(mode)+']='+JSON.stringify(edited)+';apply()');await wait();
      test(mode+' saved Architecture website wording refreshes the active read-only view safely',()=>doc.getElementById('hero-title').textContent==='Updated <safe> website heading' && !doc.getElementById('hero-title').querySelector('safe') && engine.documentHtml().includes('Updated &lt;safe&gt; website heading'));
      const disclosure=doc.querySelector('details');if(disclosure){disclosure.open=true;evaluate('apply()');await wait();test(mode+' unchanged refresh retains native disclosure state',()=>disclosure.isConnected && disclosure.open);}
      const anchor=[...doc.querySelectorAll('a[href^="#"]')].find(el=>doc.getElementById(el.getAttribute('href').slice(1)));
      if(anchor){const outerHash=w.location.hash;anchor.click();await wait();test(mode+' wireframe local navigation stays within its iframe',()=>w.location.hash===outerHash && doc.getElementById(anchor.getAttribute('href').slice(1)).getBoundingClientRect().top<frame.contentWindow.innerHeight);}
      for(const width of ['mobile','tablet','desktop']){evaluate('updateResponsivePreview('+JSON.stringify(width)+')');input('wf-width','live','change');await wait();test(mode+' match live width follows '+width,()=>frame.contentWindow.innerWidth===({mobile:390,tablet:768,desktop:1280})[width]);}
      for(const width of [320,390,1440]){app.style.width=width+'px';await wait();test(mode+' wireframe controls fit '+width+'px studio',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#wireframe-workspace select,#wireframe-workspace button')].every(el=>{const r=el.getBoundingClientRect();return r.height>=44 && r.right<=w.innerWidth+1;}));}
      app.style.width='1440px';
    }
    // Region opacity, component surfaces and every button variant retain configured paint.
    for(const mode of ['basic','advanced']){
      reset();await wait();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
      evaluate('state.semanticOverrides={light:{background:"#E9DFCA","header-background":"#C8E2DB","main-background":"#D6DFEE","footer-background":"#C9BADB",surface:"#E8F1DE","surface-muted":"#D8EAD0"},dark:{background:"#192D39","header-background":"#283B26","main-background":"#252C4B","footer-background":"#362B40",surface:"#243A3B","surface-muted":"#304D49"}};state.backgroundOpacity={light:{body:60,header:70,main:80,footer:50},dark:{body:80,header:60,main:70,footer:40}};apply()');
      for(const [index,variant]of ['primary','secondary','accent','outline','text'].entries()){input('bdVariant',variant);input('bdDefaultBg',['#276B57','#74552E','#8B3261','#315B8D','#694181'][index]);input('bdText','#FFFFFF');}
      for(const theme of ['light','dark']){
        input('jTheme',theme);w.dssShowWizardStep(2,false);w.dssRevealSection('process-wireframe',false);await wait();w.DSStudio.wireframeView.refresh();await wait();
        const sourceDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');sourceDoc.querySelectorAll('script').forEach(el=>el.remove());sourceDoc.querySelector('link[href="tokens.css"]').remove();const styles=sourceDoc.createElement('style');styles.textContent=evaluate('cssExport()')+w.DSStudio.fonts.previewCss()+'*{animation:none!important;transition:none!important}';sourceDoc.head.append(styles);
        const reference=d.createElement('iframe');reference.style.cssText='height:768px;border:0';reference.srcdoc='<!doctype html>'+sourceDoc.documentElement.outerHTML;await new Promise(resolve=>{reference.onload=resolve;d.body.append(reference);});
        const frame=d.getElementById('wf-page');
        for(const width of [320,1280]){input('wf-width',String(width),'change');reference.style.width=width+'px';await wait();test(mode+' '+theme+' configured component and button backgrounds match website at '+width+'px',()=>compareWireframePaint(reference.contentDocument,frame.contentDocument));}
        test(mode+' '+theme+' read-only controls preserve original disabled appearance',()=>[...frame.contentDocument.querySelectorAll('input,select,textarea,button')].every((el,index)=>el.inert && el.disabled===sourceDoc.querySelectorAll('input,select,textarea,button')[index].disabled));
        const exported=d.createElement('iframe');exported.style.cssText='width:1280px;height:768px;border:0';exported.srcdoc=engine.documentHtml();await new Promise(resolve=>{exported.onload=resolve;d.body.append(exported);});
        test(mode+' '+theme+' wireframe download preserves configured backgrounds and button colours',()=>compareWireframePaint(reference.contentDocument,exported.contentDocument));exported.remove();reference.remove();
        const control=frame.contentDocument.querySelector('button:not([disabled]),input:not([disabled])');if(control){const prior=frame.contentDocument.activeElement;control.focus();test(mode+' '+theme+' inert website controls cannot receive user focus',()=>frame.contentDocument.activeElement===prior && frame.contentDocument.activeElement!==control);}
      }
    }
    reset();await wait();
  }
  // Fidelity is a transient tab choice over the same annotated website.
  {
    reset();w.dssShowWizardStep(2,false);w.dssRevealSection('process-wireframe',false);await wait();
    const ui=w.DSStudio.wireframeView,frame=d.getElementById('wf-page'),high=d.getElementById('wf-tab-high'),low=d.getElementById('wf-tab-low');
    test('Wireframe offers labelled Low Fidelity and High Fidelity tabs with the existing high view selected',()=>d.querySelector('[role="tablist"][aria-label="Wireframe fidelity"]') && high.getAttribute('aria-selected')==='true' && high.tabIndex===0 && low.tabIndex===-1 && d.getElementById('wf-fidelity-panel').getAttribute('aria-labelledby')===high.id && d.getElementById('wf-fidelity-panel').contains(frame));
    high.focus();high.dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}));await wait();
    test('Arrow keys activate and focus Low Fidelity without changing project data',()=>ui.fidelity==='low' && d.activeElement===low && low.getAttribute('aria-selected')==='true' && high.tabIndex===-1 && frame.title.includes('Low Fidelity'));
    low.dispatchEvent(new w.KeyboardEvent('keydown',{key:'End',bubbles:true}));await wait();test('End activates High Fidelity and updates the shared panel label',()=>ui.fidelity==='high' && d.activeElement===high && d.getElementById('wf-fidelity-panel').getAttribute('aria-labelledby')===high.id);
    high.dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));await wait();test('Home activates Low Fidelity',()=>ui.fidelity==='low' && d.activeElement===low);
    low.dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));await wait();test('ArrowRight returns to High Fidelity',()=>ui.fidelity==='high' && d.activeElement===high);
    const neutral=value=>{const channels=value.match(/[\d.]+/g);return !channels || channels.length<3 || channels[0]===channels[1] && channels[1]===channels[2];};
    for(const mode of ['basic','advanced']){
      d.getElementById(mode==='basic'?'wf-basic':'wf-advanced').click();await wait();
      for(const theme of ['light','dark']){
        input('jTheme',theme);await wait();ui.setFidelity('high');await wait();
        const doc=frame.contentDocument,source=doc.body.textContent,before=evaluate('projectJson()');
        const disclosure=[...doc.querySelectorAll('details')].find(el=>el.getBoundingClientRect().height>0);if(disclosure)disclosure.open=true;
        for(const width of [320,1280]){
          input('wf-width',String(width),'change');await wait();
          const highBoxes=[...doc.body.querySelectorAll('*')].map(el=>{const box=el.getBoundingClientRect();return [box.x,box.y,box.width,box.height];});
          low.click();await wait();
          test(mode+' '+theme+' Low Fidelity preserves every object and layout box at '+width+'px',()=>doc.body.textContent===source && [...doc.body.querySelectorAll('*')].every((el,index)=>{const box=el.getBoundingClientRect();return [box.x,box.y,box.width,box.height].every((value,key)=>Math.abs(value-highBoxes[index][key])<=1);}) && evaluate('projectJson()')===before);
          test(mode+' '+theme+' Low Fidelity leaves non-button objects unfilled and keeps grey buttons at '+width+'px',()=>doc.documentElement.dataset.wfFidelity==='low' && frame.contentWindow.getComputedStyle(doc.documentElement).colorScheme==='light' && [...doc.querySelectorAll('input')].every(el=>frame.contentWindow.getComputedStyle(el).accentColor==='rgb(102, 102, 102)') && frame.contentWindow.getComputedStyle(doc.body).backgroundColor==='rgb(255, 255, 255)' && [...doc.body.querySelectorAll('*')].every(el=>{const style=frame.contentWindow.getComputedStyle(el);return neutral(style.color) && style.backgroundImage==='none' && style.backgroundColor===(el.matches('button,.button,.ds-button,[role="button"]')?'rgb(102, 102, 102)':'rgba(0, 0, 0, 0)');}) && [...doc.querySelectorAll('button,.button,.ds-button,[role="button"]')].every(el=>frame.contentWindow.getComputedStyle(el).backgroundColor==='rgb(102, 102, 102)') && [...doc.querySelectorAll('svg,img')].every(el=>frame.contentWindow.getComputedStyle(el).filter==='grayscale(1)'));
          high.click();await wait();test(mode+' '+theme+' High Fidelity restores the configured website stylesheet at '+width+'px',()=>!doc.getElementById('wf-low-fidelity-styles') && doc.documentElement.dataset.wfFidelity==='high' && doc.getElementById('wf-source-styles').textContent.includes(evaluate('cssExport()')) && evaluate('projectJson()')===before);
        }
        test(mode+' '+theme+' tab changes preserve open disclosures',()=>!disclosure || [...doc.querySelectorAll('details')].find(el=>el.querySelector('summary')?.textContent===disclosure.querySelector('summary')?.textContent)?.open);
        const files=[],download=w.download;w.download=(name,content)=>files.push({name,content});low.click();await wait();d.getElementById('wf-download').click();high.click();await wait();d.getElementById('wf-download').click();w.download=download;
        test(mode+' '+theme+' download follows the selected fidelity tab',()=>files.length===2 && files[0].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'low'}) && files[1].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'high'}) && files[0].content.includes('wf-low-fidelity-styles') && !files[1].content.includes('wf-low-fidelity-styles'));
      }
    }
    const saved=evaluate('projectJson()');ui.setFidelity('unexpected');test('Unknown fidelity values fall back to High Fidelity without saving view preferences',()=>ui.fidelity==='high' && evaluate('projectJson()')===saved && !w.DSStudio.wireframeEngine.createDocument({fidelity:'unexpected'}).getElementById('wf-low-fidelity-styles'));
    for(const theme of ['light','dark'])for(const width of [320,390,1440]){app.style.width=width+'px';if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();await wait();for(const fidelity of ['low','high']){ui.setFidelity(fidelity);await wait();test(theme+' '+fidelity+' fidelity tabs and controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#wireframe-workspace button,#wireframe-workspace select')].every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.left>=0 && box.right<=w.innerWidth+1;}));}}
    app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();ui.setFidelity('high');reset();await wait();
  }
  // End fidelity tab checks.

  // View preferences belong to this workspace, while file/project replacement
  // must refresh the mirror from the complete latest model on lesson entry.
  for(const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();w.importConfig({sampleMode:mode});input('jProject',mode+' wireframe replacement fixture');
    d.getElementById('jSaveLocal').click();const id=d.getElementById('jProjects').value;
    w.dssShowWizardStep(2,false);w.DSStudio.wireframeView.setFidelity('high');await wait();
    const ui=w.DSStudio.wireframeView,frame=d.getElementById('wf-page'),originalDoc=frame.contentDocument;
    const original=evaluate('projectJson()'),library=w.localStorage.getItem('dss-v27-projects'),originalHeading=originalDoc.getElementById('hero-title').textContent;
    input('wf-width','390','change');d.getElementById('wf-tab-low').click();await wait();
    test(mode+' local viewport and fidelity preferences stay outside project JSON and autosave',()=>ui.fidelity==='low' && frame.contentWindow.innerWidth===390 && evaluate('projectJson()')===original && w.localStorage.getItem('dss-v27-projects')===library);
    const imported=JSON.parse(original),text='Imported <img src=x onerror="window.wireframeImportExecuted=true"> '+mode+' heading';
    const service=w.DSStudio.websiteContent,fields=service.describe('id:hero-title',mode).fields;
    imported.base=20;imported.project=mode+' imported wireframe';
    imported.designProcess.websiteContent[mode]=service.merge(mode,fields.map(field=>({...field,value:text})));
    w.dssShowWizardStep(0,false);await importFile(JSON.stringify(imported));
    w.dssShowWizardStep(2,false);await wait();
    test(mode+' inactive file replacement refreshes latest wording and typography on wireframe entry',()=>
      d.getElementById('wf-page')===frame && frame.contentDocument===originalDoc && originalDoc.getElementById('hero-title').textContent===text && !originalDoc.getElementById('hero-title').querySelector('img,script') && !w.wireframeImportExecuted && frame.contentWindow.getComputedStyle(originalDoc.body).fontSize==='20px' && ui.fidelity==='low' && originalDoc.documentElement.dataset.wfFidelity==='low' && frame.contentWindow.innerWidth===390 && w.localStorage.getItem('dss-v27-projects')===library);
    const importedJson=evaluate('projectJson()'),website=evaluate('[htmlExport(),cssExport()]');
    d.getElementById('wf-open-live').click();await wait();
    test(mode+' live comparison reveals the current website without replacing the wireframe or saved data',()=>
      d.activeElement===d.getElementById('previewShell') && previewDoc().getElementById('hero-title').textContent===text && frame.contentDocument===originalDoc && ui.fidelity==='low' && frame.contentWindow.innerWidth===390 && evaluate('projectJson()')===importedJson && w.localStorage.getItem('dss-v27-projects')===library);
    const files=[],oldDownload=w.download;
    try{w.download=(name,content,mime)=>files.push({name,content,mime});d.getElementById('wf-download').click();d.getElementById('wf-tab-high').click();await wait();d.getElementById('wf-download').click();}
    finally{w.download=oldDownload;}
    test(mode+' imported wireframe downloads use current data and selected fidelity without leaking into website exports',()=>{
      const docs=files.map(file=>new w.DOMParser().parseFromString(file.content,'text/html'));
      return files.length===2 && files.every(file=>file.name==='wireframe.html' && file.mime==='text/html') &&
        files[0].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'low'}) && files[1].content===w.DSStudio.wireframeEngine.documentHtml({fidelity:'high'}) &&
        docs.every(doc=>doc.getElementById('hero-title').textContent===text && !doc.querySelector('script,iframe,object,embed') && [...doc.querySelectorAll('input,select,textarea,button')].every(el=>el.inert)) &&
        docs[0].getElementById('wf-low-fidelity-styles') && !docs[1].getElementById('wf-low-fidelity-styles') &&
        evaluate('projectJson()')===importedJson && JSON.stringify(evaluate('[htmlExport(),cssExport()]'))===JSON.stringify(website) && w.localStorage.getItem('dss-v27-projects')===library;
    });
    d.getElementById('wf-tab-low').click();d.getElementById('jProjects').value=id;d.getElementById('jLoadLocal').click();await wait();
    test(mode+' local project load restores its website in the same frame while retaining local view preferences',()=>
      evaluate('projectJson()')===original && frame.contentDocument===originalDoc && originalDoc.getElementById('hero-title').textContent===originalHeading && ui.fidelity==='low' && originalDoc.documentElement.dataset.wfFidelity==='low' && frame.contentWindow.innerWidth===390 && w.localStorage.getItem('dss-v27-projects')===library);
  }
  test('No wireframe JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Wireframe harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
