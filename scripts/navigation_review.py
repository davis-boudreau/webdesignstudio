"""Independent navigation, focus and workspace layout browser checks.

Run: python scripts/navigation_review.py. Uses the shared local Chrome runner
with its own app/profile; no integration harness or user storage is imported.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Navigation review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Navigation review: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const input=(id,value,type='input')=>{
    const el=d.getElementById(id);w.DSStudio.typographyWorkspace?.revealControl(el);
    el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const previewWindow=()=>d.getElementById('previewPage').contentWindow;
  try {
  test('Independent navigation startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  test('Fresh startup opens the Brief centre accordion that matches the active builder step',()=>w.DSStudio.activeStage===0 && d.querySelector('[data-journey-step="0"]').getAttribute('aria-current')==='step' && d.getElementById('process-brief').open && !d.getElementById('process-brief').hidden && !d.getElementById('process-ia').open);
  const stepDisclosure=d.querySelector('.journey-step-list');
  test('Choose a step starts expanded with all twelve steps available',()=>stepDisclosure.open && stepDisclosure.querySelectorAll('[data-journey-step]').length===12);
  w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);evaluate('apply()');
  test('Step navigation and rendering keep the step chooser expanded',()=>stepDisclosure.open && w.DSStudio.activeStage===0);
  stepDisclosure.open=false;w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);evaluate('apply()');
  test('A user-collapsed step chooser stays collapsed across navigation and rendering',()=>!stepDisclosure.open);
  stepDisclosure.open=true;w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);
  test('A reopened step chooser stays expanded across navigation',()=>stepDisclosure.open);
  test('Startup keeps the preview and active Brief expanded with inspector hidden', () => d.querySelector('#main > :first-child').id==='studio-section-4' && [...d.querySelectorAll('#main > .studio-section')].every(section=>!section.hidden && section.open===(section.id==='studio-section-4' || section.id==='process-brief')) && !d.querySelector('.studio-code-dock').open && !d.getElementById('studioInspector').open);
  test('Hidden inspector leaves one quarter for the desktop builder and the rest for the preview', () => Math.abs(d.querySelector('.sidebar').getBoundingClientRect().width-(d.querySelector('.layout').clientWidth-16)/4)<1 && d.getElementById('dockCss').getBoundingClientRect().height===0);
  test('Inspector has a native details/summary disclosure arrow in both states',()=>d.getElementById('studioInspector').tagName==='DETAILS' && d.getElementById('inspectorToggle').tagName==='SUMMARY' && d.getElementById('inspectorToggle').textContent==='Live CSS/HTML Inspector' && w.getComputedStyle(d.getElementById('inspectorToggle')).display==='list-item' && d.getElementById('inspectorToggle').tabIndex===0 && d.getElementById('inspectorToggle').getBoundingClientRect().height>=44);
  test('Competing beginner and centre navigation is removed', () => !d.getElementById('workspaceNav') && !d.getElementById('beginnerStart') && !d.getElementById('beginnerPath') && !d.querySelector('.studio-section-nav') && !d.querySelector('[data-configure-step]'));
  test('Preview initially fills the centre pane in Fluid mode', () => d.getElementById('previewFrame').dataset.width==='fluid' && d.querySelector('button[data-width="fluid"]').getAttribute('aria-pressed')==='true');
  test('Twelve wizard steps connect project planning to fifteen centre lessons and the preview', () => d.querySelectorAll('[data-journey-step]').length===12 && d.querySelectorAll('[data-journey-pane]').length===12 && d.querySelectorAll('#main > .studio-section > .panel .studio-lesson').length===15 && d.getElementById('jProgress').textContent.includes('of 12'));
  // Reload fixtures start from their own real document, independently of
  // appearance tests. Reloading intentionally starts with unsaved defaults.
  const fresh=d.createElement('iframe');fresh.src='/index.html';
  await new Promise(resolve=>{fresh.onload=resolve;d.body.append(fresh);});
  try {
  // Reload real documents, preserving each section fragment and reopening a
  // manually collapsed active lesson. Phase indices differ from display order.
  fresh.style.cssText='position:fixed;inset:0;width:100%;height:100%;border:0;z-index:10000';
  for(const stage of w.DSStudio.orderedStages) {
    const fw=fresh.contentWindow,fd=fresh.contentDocument;
    fw.dssShowWizardStep(stage.index,false);
    fw.history.replaceState(null,'','#'+stage.lesson);
    fd.getElementById(stage.lesson).open=false;
    const priorDoc=fd,priorProject=fw.eval('projectJson()');
    await new Promise(resolve=>{fresh.onload=resolve;fw.location.reload();});await wait();
    const reloaded=fresh.contentWindow,doc=fresh.contentDocument;
    test('Reload opens Step '+(stage.position+1)+' '+stage.label+' and matches the active builder',()=>doc!==priorDoc && reloaded.DSStudio.activeStage===stage.index && doc.querySelector('[data-journey-step="'+stage.index+'"]').getAttribute('aria-current')==='step' && doc.getElementById(stage.lesson).open && !doc.getElementById(stage.lesson).hidden && !doc.querySelector('[data-journey-pane="'+stage.index+'"]').hidden && [...doc.querySelectorAll('#main > .studio-section')].filter(section=>section.id!=='studio-section-4').every(section=>section.open===(section.id===stage.lesson)) && reloaded.eval('projectJson()')===priorProject && !reloaded.__reviewErrors.length);
  }
  } finally {fresh.remove();}
  reset();await wait();
  d.getElementById('studio-section-4').open=false;
  d.querySelector('[data-journey-step="5"]').click(); input('jBase',18); await wait();
  const closedPreviewDoc=previewDoc();
  test('Wizard edits update the generated CSS while the responsive section is collapsed', () => !d.getElementById('studio-section-4').open && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('--font-size-base: 18px;'));
  evaluate("dssRevealSection('previewPage',false)"); await wait();
  test('Reopening the collapsed preview keeps the document and current settings', () => d.getElementById('studio-section-4').open && previewDoc()===closedPreviewDoc && parseFloat(previewWindow().getComputedStyle(previewDoc().body).fontSize)===18 && Math.abs(previewWindow().innerWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<2);
  d.getElementById('studio-section-4').open=false;
  reset(); d.querySelector('[data-journey-step="0"]').click(); await wait();
  test('Editing and reopening the preview leaves Colour systems collapsed', () => !d.getElementById('studio-section-1').open && !d.getElementById('studio-section-4').open);
  app.style.width='1440px';reset();await wait();
  d.querySelector('[data-journey-step="3"]').click();
  test('Wizard ends at Prototype without implying completed checks', () => !d.querySelector('[data-journey-pane="3"]').hidden && d.getElementById('jNext').hidden && d.getElementById('jProgress').textContent.includes('Step 12 of 12') && !d.querySelector('.journey-steps .is-complete'));
  d.getElementById('jBack').click();
  test('Back from Prototype reaches Deliver',()=>!d.querySelector('[data-journey-pane="11"]').hidden && !d.getElementById('jNext').hidden);
  d.getElementById('jBack').click();
  test('Back navigation reaches accessibility and restores Next', () => !d.querySelector('[data-journey-pane="10"]').hidden && !d.getElementById('jNext').hidden);
  test('Content and typography planning lead into Wireframe and Palette, with Prototype final', () => {
    const labels=[...d.querySelectorAll('[data-journey-step]')].map(button=>button.textContent);
    const destinations=w.DSStudio.orderedStages.slice(0,5).map(stage=>'#'+stage.lesson);
    return ['Brief','Architecture','Typography','Wireframe','Palette'].every((label,index)=>labels[index].includes(label))
      && labels.at(-1)==='12 · Prototype' && w.DSStudio.orderedStages.filter(stage=>stage.phase==='Plan').length===4
      && JSON.stringify(destinations)===JSON.stringify(['#process-brief','#process-ia','#studio-section-2','#process-wireframe','#brandPalette']);
  });
  for (const [index,id] of ['brief','ia','wireframe','prototype'].entries()) {
    d.querySelector(`[data-journey-step="${index}"]`).click();
    const before=evaluate('projectJson()');
    await wait();
    test(id+' wizard shortcut opens its centre lesson without changing project data', () => d.getElementById('process-'+id).open && evaluate('projectJson()')===before);
    d.querySelector(`[data-journey-step="${index}"]`).click();
    test(id+' lesson returns to the correct wizard stage and focuses its heading', () => !d.querySelector(`[data-journey-pane="${index}"]`).hidden && d.activeElement===d.querySelector(`#process-${id} > summary h2`));
  }
  app.style.width='1440px';reset();await wait();
  d.getElementById('studio-section-4').open=true;
  w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
  const teachingProject=evaluate('projectJson()');
  d.querySelector('[data-journey-step="8"]').click();
  test('One selection connects spacing controls and lesson without changing the project', () => !d.querySelector('[data-journey-pane="8"]').hidden && !d.getElementById('studio-section-3').hidden && d.getElementById('studio-section-3').open && evaluate('projectJson()')===teachingProject && d.activeElement===d.querySelector('#studio-section-3 > summary h2'));
  d.documentElement.style.scrollBehavior='auto';
  d.documentElement.style.overflowAnchor='none';
  for (const width of [320,390,768,1280,1440,2560]) {
    app.style.width=width+'px'; await wait();
    d.querySelector('[data-journey-step="6"]').click(); await wait();
    const section=d.getElementById('studio-section-1');
    w.dispatchEvent(new w.Event('resize'));
    section.scrollIntoView({block:'start',behavior:'instant'}); await wait();
    test('Active lesson fits beneath the sticky header at '+width+'px', () => {
      const header=d.querySelector('.topbar').getBoundingClientRect(), summary=section.querySelector('summary').getBoundingClientRect();
      return summary.top>=header.bottom+7 && summary.bottom<=w.innerHeight && d.documentElement.scrollWidth<=w.innerWidth+1;
    });
    test('Inspector stays right on desktop and follows the centre on smaller screens at '+width+'px', () => {
      const code=d.querySelector('.studio-code-dock').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect();
      return (width>1280?code.left>=centre.right:code.top>=centre.bottom) && d.querySelector('#main > :first-child').id==='studio-section-4';
    });
  }
  d.documentElement.style.removeProperty('scroll-behavior');
  d.documentElement.style.removeProperty('overflow-anchor');
  // Regression coverage for the shared journey and confirmed action/scope defects.
  app.style.width='1440px';reset();await wait();
  const wizardProject=evaluate('projectJson()');
  const wizardPreviewDocument=previewDoc();
  for (const stage of w.DSStudio.stages) {
    d.querySelector(`[data-journey-step="${stage.index}"]`).click();
    test('Shared stage '+stage.id+' selects one lesson, controls and focused heading',()=>{
      const active=d.getElementById(stage.lesson);
      return !d.querySelector(`[data-journey-pane="${stage.index}"]`).hidden && !active.hidden && active.open && d.querySelector('#main > :first-child').id==='studio-section-4' && d.activeElement===active.querySelector(':scope > summary h2') && [...d.querySelectorAll('#main > .studio-section')].filter(section=>section.open).length===(d.getElementById('studio-section-4').open?2:1) && evaluate('projectJson()')===wizardProject;
    });
    if(stage.index<4) {
      d.querySelector('#'+stage.lesson+' [data-inspect="json"]').click();
      test(stage.id+' inspects actual planning data in the single inspector',()=>d.getElementById('dockTabJson').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('projectJson()'));
    } else {
      d.querySelector('#'+stage.lesson+' [data-inspect="css"]').click();
      test(stage.id+' inspects complete CSS and a real declaration',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && (!stage.find || evaluate('cssExport()').includes(stage.find)));
    }
  }
  await wait();
  test('Stage navigation preserves the live preview browsing context',()=>previewDoc()===wizardPreviewDocument && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  d.getElementById('jBack').click();
  test('Previous changes lesson and controls together',()=>evaluate('DSStudio.activeStage')===10 && !d.getElementById('studio-section-5').hidden);
  d.getElementById('jNext').click();
  test('Next changes lesson and controls together',()=>evaluate('DSStudio.activeStage')===11 && !d.getElementById('studio-section-6').hidden);
  for (const width of [320,390,1440]) {
    app.style.width=width+'px';await wait();
    d.querySelector('[data-journey-step="7"]').click();
    const controls=d.querySelector('[data-journey-pane="7"]');
    test('Actual controls join the lesson on narrow screens at '+width+'px',()=>width<=900?controls.closest('.studio-section')?.id==='buttonDesignLab' && controls.previousElementSibling.classList.contains('studio-lesson'):controls.closest('.studio-journey')!==null);
    const row=w.dssReadTokens().find(token=>token.name==='--space-unit');
    w.dssConfigureToken(row);
    test('Token source route selects its lesson and exact control at '+width+'px',()=>evaluate('DSStudio.activeStage')===8 && !d.getElementById('studio-section-3').hidden && d.activeElement===d.getElementById('jSpacing'));
  }
  app.style.width='1440px';await wait();
  w.dssRevealSection('studio-section-8',false);
  d.querySelector('#studio-section-8 > .panel > button').click();
  test('Reference return restores the current step without changing settings',()=>!d.getElementById('studio-section-8').open && !d.getElementById('studio-section-3').hidden && evaluate('projectJson()')===wizardProject);
  app.style.width='1440px';reset();await wait();
  d.getElementById('studio-section-4').open=true;
  // Collapsing code releases the complete column and safely restores focus.
  d.getElementById('dockModeBasic').click();input('dockSection','footer','change');
  d.querySelector('button[data-width="fluid"]').click();
  w.DSStudio.inspector.show({language:'html',section:'footer'});await wait();
  const collapseProject=evaluate('projectJson()'),collapseDocument=previewDoc();
  for (const width of [320,901,1280,1440,2560]) {
    app.style.width=width+'px';await wait();
    const expandedWidth=d.getElementById('previewFrame').getBoundingClientRect().width;
    d.getElementById('dockCss').focus();d.getElementById('dockToggle').click();await wait();
    test('Collapse releases inspector space and restores opener focus at '+width+'px',()=>{
      const layout=d.querySelector('.layout'),left=d.querySelector('.sidebar').getBoundingClientRect().width;
      const openerBounds=d.getElementById('inspectorToggle').getBoundingClientRect();
      if(openerBounds.top<d.querySelector('.topbar').getBoundingClientRect().bottom || openerBounds.bottom>w.innerHeight) throw Error(JSON.stringify({width,top:openerBounds.top,bottom:openerBounds.bottom,header:d.querySelector('.topbar').getBoundingClientRect().bottom,scroll:w.scrollY,active:d.activeElement.id}));
      return !d.getElementById('studioInspector').open && d.getElementById('inspectorToggle').getBoundingClientRect().width>0 && d.getElementById('dockCss').getBoundingClientRect().height===0 && d.activeElement===d.getElementById('inspectorToggle') && (width<=900 || Math.abs(left-(layout.clientWidth-16)/4)<1) && (width<=1280 || d.getElementById('previewFrame').getBoundingClientRect().width>expandedWidth) && d.documentElement.scrollWidth<=w.innerWidth+1;
    });
    d.getElementById('inspectorToggle').click();await wait();
    test('Native disclosure restores language, excerpt and live document at '+width+'px',()=>d.getElementById('studioInspector').open && d.getElementById('studioInspector').open && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='footer' && d.activeElement===d.getElementById('inspectorToggle') && previewDoc()===collapseDocument && evaluate('projectJson()')===collapseProject && d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  d.getElementById('dockToggle').click();
  test('Pane Collapse returns to its compact bar and releases the inspector column',()=>!d.getElementById('studioInspector').open && d.querySelector('.layout').classList.contains('is-inspector-collapsed'));
  d.querySelector('[data-journey-step="7"]').click();d.querySelector('#buttonDesignLab [data-inspect="css"]').click();
  test('Contextual Inspect CSS reopens the hidden column and selects its promised output',()=>d.getElementById('studioInspector').open && !d.querySelector('.layout').classList.contains('is-inspector-collapsed') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc()===collapseDocument);
  test('Inspector visibility is absent from project JSON',()=>!Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/inspector|collapsed/i.test(key)));
  // Studio section returns never navigate or regenerate the sample website.
  reset();app.style.width='1440px';await wait();
  input('jProject','Navigation return fixture');d.getElementById('jSaveLocal').click();
  const returnProjectId=d.getElementById('jProjects').value;
  if(!JSON.parse(w.localStorage.getItem('dss-v27-projects')||'{}')[returnProjectId])throw Error('Return-link fixture did not create a saved project');
  test('Every studio panel, wizard pane and inspector ends with one native return link',()=>[...d.querySelectorAll('.studio-section > .panel, [data-journey-pane], #studioInspector')].every(container=>{
    const rows=container.querySelectorAll(':scope > .studio-home-return'),link=rows[0]?.querySelector('a');
    return rows.length===1 && container.lastElementChild===rows[0] && link?.getAttribute('href')==='#studio-home' && link.tabIndex===0 && link.textContent.startsWith('Back to top') && link.querySelector('span').getAttribute('aria-hidden')==='true';
  }));
  for(const theme of ['light','dark']) for(const width of [320,901,1440]) {
    input('jTheme',theme);app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    const controls=d.querySelector('[data-journey-pane="4"]'),panel=d.querySelector('#brandPalette > .panel');
    test(theme+' section return links align right and fit '+width+'px',()=>[controls,panel].every(container=>{
      const row=container.querySelector(':scope > .studio-home-return'),link=row.querySelector('a'),box=link.getBoundingClientRect(),rowBox=row.getBoundingClientRect();
      return box.width>=44 && box.height>=44 && box.width<=container.clientWidth+1 && Math.abs(box.right-(rowBox.right-parseFloat(w.getComputedStyle(row).paddingRight)))<1;
    }) && d.documentElement.scrollWidth<=w.innerWidth+1);
    const beforeHome=evaluate('projectJson()'),beforeStage=w.DSStudio.activeStage,beforeDocument=previewDoc(),beforeLibrary=w.localStorage.getItem('dss-v27-projects');
    const openState=[...d.querySelectorAll('#main > .studio-section')].map(el=>el.open).join(',');
    const link=panel.querySelector(':scope > .studio-home-return a');link.scrollIntoView({block:'center',behavior:'instant'});link.focus();link.click();await wait();
    test(theme+' return reaches the studio top with visible focus at '+width+'px',()=>w.scrollY<=1 && d.activeElement===d.getElementById('studio-home') && w.getComputedStyle(d.getElementById('studio-home')).outlineStyle==='solid' && d.getElementById('studio-home').getBoundingClientRect().top>=-1);
    test(theme+' return preserves the current stage, project, library and preview at '+width+'px',()=>evaluate('projectJson()')===beforeHome && w.DSStudio.activeStage===beforeStage && previewDoc()===beforeDocument && w.localStorage.getItem('dss-v27-projects')===beforeLibrary && [...d.querySelectorAll('#main > .studio-section')].map(el=>el.open).join(',')===openState);
  }
  app.style.width='1440px';w.dssShowWizardStep(8);await wait();
  const nativeReturn=d.querySelector('#studio-section-3 > .panel > .studio-home-return a');
  nativeReturn.scrollIntoView({block:'center',behavior:'instant'});nativeReturn.focus();d.documentElement.style.scrollBehavior='smooth';
  nativeReturn.dispatchEvent(new w.MouseEvent('click',{bubbles:true,cancelable:true,button:0,detail:0}));await wait();
  test('Keyboard-style link activation returns immediately despite smooth page scrolling',()=>w.scrollY<=1 && d.activeElement===d.getElementById('studio-home'));
  d.documentElement.style.removeProperty('scroll-behavior');
  for(const stage of w.DSStudio.orderedStages) {
    w.dssShowWizardStep(stage.index,false);await wait();
    test(stage.label+' retains one return link after stage routing',()=>d.querySelectorAll('#'+stage.lesson+' > .panel > .studio-home-return').length===1 && d.querySelectorAll('[data-journey-pane="'+stage.index+'"] > .studio-home-return').length===1);
  }
  w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
  const homeCode=d.getElementById('dockCss').textContent,homeMode=evaluate('state.sampleMode');
  d.querySelector('#studioInspector > .studio-home-return a').click();await wait();
  test('Inspector return retains its visibility, selected language and exact output',()=>d.getElementById('studioInspector').open && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===homeCode && evaluate('state.sampleMode')===homeMode && d.activeElement===d.getElementById('studio-home'));
  for(const mode of ['basic','advanced']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    test(mode+' preview and exported files contain no studio return controls',()=>!previewDoc().querySelector('.studio-home-return,.studio-home-link,#studio-home') && !evaluate('htmlExport()').includes('studio-home') && !evaluate('cssExport()').includes('studio-home'));
  }
  // End studio section return checks.


  // Exercise both directions across the exact control-placement breakpoint.
  app.style.width='1440px';reset();await wait();w.dssShowWizardStep(7,false);await wait();
  const originalPane=d.querySelector('[data-journey-pane="7"]'),originalRadius=d.getElementById('bdRadius');
  const routeJson=evaluate('projectJson()'),routeCss=evaluate('cssExport()'),routeHtml=evaluate('htmlExport()'),routePreview=previewDoc();
  for(const width of [1440,900,901,320,901,1440]) {
    app.style.width=width+'px';await wait();w.dssShowWizardStep(7,false);await wait();
    test('Breakpoint transition '+width+'px preserves original editor nodes, model and preview',()=>{
      const inline=originalPane.closest('.studio-section')?.id==='buttonDesignLab';
      return d.querySelector('[data-journey-pane="7"]')===originalPane && d.getElementById('bdRadius')===originalRadius &&
        d.querySelectorAll('#bdRadius').length===1 && (width<=900?inline:originalPane.closest('.studio-journey')!==null) &&
        evaluate('projectJson()')===routeJson && evaluate('cssExport()')===routeCss && evaluate('htmlExport()')===routeHtml && previewDoc()===routePreview;
    });
  }
  input('bdRadius',18);await wait();
  test('Editor listeners survive repeated moves between sidebar and lesson',()=>d.getElementById('bdRadius')===originalRadius && evaluate('state.buttonDesign.radius')===18 && evaluate('cssExport()')!==routeCss);
  const disclosure=d.getElementById('buttonDesignLab'),summary=disclosure.querySelector(':scope > summary');
  const disclosureJson=evaluate('projectJson()');summary.click();await wait();
  test('Native lesson collapse preserves the selected step and project',()=>!disclosure.open && w.DSStudio.activeStage===7 && evaluate('projectJson()')===disclosureJson);
  summary.click();await wait();
  test('Native lesson reopening preserves its original controls and project',()=>disclosure.open && disclosure.contains(originalPane)===false && d.getElementById('bdRadius')===originalRadius && evaluate('projectJson()')===disclosureJson);
  const hashJson=evaluate('projectJson()'),hashCss=evaluate('cssExport()');
  for(const stage of w.DSStudio.orderedStages) {
    w.location.hash='#'+stage.lesson;await wait();
    test('Live fragment selects '+stage.label+' without changing the design',()=>w.DSStudio.activeStage===stage.index && d.getElementById(stage.lesson).open && !d.querySelector('[data-journey-pane="'+stage.index+'"]').hidden && evaluate('projectJson()')===hashJson && evaluate('cssExport()')===hashCss && previewDoc()===routePreview);
  }
  const lastStage=w.DSStudio.activeStage;
  for(const fragment of ['#missing-navigation-target','#%E0%A4%A']) {
    w.location.hash=fragment;await wait();
    test('Unknown or malformed fragment '+fragment+' preserves the active workspace',()=>w.DSStudio.activeStage===lastStage && d.getElementById(w.DSStudio.stages[lastStage].lesson).open && evaluate('projectJson()')===hashJson && previewDoc()===routePreview && !w.__reviewErrors.length);
  }
  test('No navigation JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Navigation harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
