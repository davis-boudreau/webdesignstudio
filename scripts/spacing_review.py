"""Independent spacing checks using the local Chrome runner.

Run: python scripts/spacing_review.py. Owns its app, profile and fixtures.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Spacing review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  window.addEventListener('unhandledrejection',event=>{results.push({name:'Harness completed without an unhandled exception',pass:false,error:String(event.reason?.stack||event.reason)});finish();});
  const test=(name,fn)=>{try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}catch(error){results.push({name,pass:false,error:String(error.stack||error)});}document.title='Focused review: '+results.length+' checks; last: '+name;};
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const previewWindow=()=>d.getElementById('previewPage').contentWindow;
  const input=(id,value,type='input')=>{const el=d.getElementById(id);w.DSStudio.paletteWorkspace?.revealControl(el);w.DSStudio.typographyWorkspace?.revealControl(el);el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));};
  const prepare=async step=>{
    app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();
    reset();w.DSStudio.inspector.show({language:'css',section:'all'});d.querySelector('[data-width="fluid"]').click();w.dssShowWizardStep(step,false);await wait();
  };
  try {
  test('Independent spacing startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  await prepare(8);
  // Padding fixtures own their model and Palette workspace setup.
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();await wait();
  // Region padding extends the existing layout without replacing content gutters.
  reset();w.dssShowWizardStep(4);await wait();
  const paddingRegions=['header','main','footer'],paddingSides=['top','right','bottom','left'];
  const paddingValues=()=>Object.fromEntries(paddingRegions.map(region=>[region,paddingSides.map(side=>evaluate('regionPadding('+JSON.stringify(region)+','+JSON.stringify(side)+')'))]));
  test('Region padding starts at zero and is available only for Header, Main and Footer',()=>paddingRegions.every(region=>d.getElementById(region+'-padding-controls') && paddingValues()[region].every(value=>value===0)) && !d.getElementById('body-padding-controls'));
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) for(const width of [320,1440]) for(const value of [0,64]) {
    app.style.width=width+'px';d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);w.dssShowWizardStep(4);
    for(const region of paddingRegions)for(const side of paddingSides)input(region+'-padding-'+side,value);await wait();
    const checkPadding=(pd,pw)=>paddingRegions.every(region=>{
      const style=pw.getComputedStyle(pd.querySelector('body > '+region));
      const gutter=mode==='advanced'&&region==='main'?parseFloat(pw.getComputedStyle(pd.querySelector('header > .container')).paddingLeft):0;
      return paddingSides.every(side=>Math.abs(parseFloat(style.getPropertyValue('padding-'+side))-value-(['left','right'].includes(side)?gutter:0))<.1);
    });
    test(mode+' '+theme+' '+width+'px region padding '+value+'px matches live output',()=>checkPadding(previewDoc(),previewWindow()) && paddingRegions.every(region=>d.getElementById(region+'-padding-code').textContent.includes('--'+region+'-padding-left: '+value+'px;')));
    const page=d.createElement('iframe');page.style.cssText='width:'+width+'px;height:800px;border:0';page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(page);await wait();
    test(mode+' '+theme+' '+width+'px region padding '+value+'px exports without overflow',()=>checkPadding(page.contentDocument,page.contentWindow) && page.contentDocument.documentElement.scrollWidth<=width+1);page.remove();
  }
  app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  for(const [index,region] of paddingRegions.entries())for(const [sideIndex,side] of paddingSides.entries())input(region+'-padding-'+side,8+index*16+sideIndex*4);await wait();
  test('All four padding sides are independently saved and shown in the centre',()=>paddingRegions.every((region,index)=>paddingSides.every((side,sideIndex)=>evaluate('regionPadding('+JSON.stringify(region)+','+JSON.stringify(side)+')')===8+index*16+sideIndex*4 && d.getElementById(region+'-padding-'+side+'-value').textContent===(8+index*16+sideIndex*4)+' px')));
  const sharedPadding=evaluate('JSON.stringify(state.regionPadding)');input('jTheme','light');await wait();
  test('Region padding is shared across themes',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding && d.getElementById('header-padding-left').value==='20');
  input('header-background-hex','#123456');input('header-background-opacity',40);d.getElementById('header-background-reset').click();await wait();
  test('Resetting a background preserves its separate padding',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding);
  const paddingProject=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();await wait();
  test('Region padding autosaves in existing local projects',()=>Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>JSON.stringify(project.data.regionPadding)===sharedPadding));
  reset();evaluate('importConfig('+JSON.stringify(paddingProject)+')');await wait();
  test('Region padding round trips through project JSON',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding && d.getElementById('footer-padding-left').value==='52');
  const nonHeaderPadding=evaluate('JSON.stringify([state.regionPadding.main,state.regionPadding.footer,state.semanticOverrides,state.backgroundOpacity])');d.getElementById('header-padding-reset').click();await wait();
  test('Padding reset restores one region without changing colours, alpha or other regions',()=>paddingValues().header.every(value=>value===0) && evaluate('JSON.stringify([state.regionPadding.main,state.regionPadding.footer,state.semanticOverrides,state.backgroundOpacity])')===nonHeaderPadding);
  const paddingToken=w.dssReadTokens().find(row=>row.name==='--main-padding-left');w.dssConfigureToken(paddingToken);await wait();
  test('Padding catalogue source reveals and focuses the actual slider',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('main-padding-left') && d.getElementById('main-padding-controls').open);
  input('main-padding-left',17);await wait();
  test('Padding edits preserve focus and update the centre inset',()=>d.activeElement===d.getElementById('main-padding-left') && d.getElementById('main-padding-demo').style.paddingLeft==='17px');
  d.querySelector('#main-padding-demo').parentElement.querySelector('button').click();await wait();
  test('Inspect padding opens complete live CSS at the real padding tokens',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--main-padding-left: 17px;') && d.getElementById('dockCss').scrollTop>0);
  evaluate('importConfig({regionPadding:{header:{top:-10,right:500,bottom:13.6,left:"20",unknown:10},main:{top:NaN,right:Infinity,bottom:null,left:32},footer:"bad",body:{top:20}}})');await wait();
  test('Padding imports accept only bounded finite numbers and known regions/sides',()=>evaluate('state.regionPadding.header.top===0 && state.regionPadding.header.right===64 && state.regionPadding.header.bottom===14 && !("left" in state.regionPadding.header) && !("unknown" in state.regionPadding.header) && state.regionPadding.main.left===32 && !("top" in state.regionPadding.main) && !("right" in state.regionPadding.main) && !("bottom" in state.regionPadding.main) && !("body" in state.regionPadding) && !("footer" in state.regionPadding)'));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    paddingRegions.forEach(region=>d.getElementById(region+'-padding-controls').open=true);await wait();
    test('Expanded padding controls and demos fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && paddingRegions.every(region=>{
      const details=d.getElementById(region+'-padding-controls'),demo=d.getElementById(region+'-padding-demo');
      w.DSStudio.paletteWorkspace.revealControl(d.getElementById(region+'-padding-top'));w.DSStudio.paletteWorkspace.revealControl(demo);
      return details.scrollWidth<=details.clientWidth+1 && demo.scrollWidth<=demo.clientWidth+1 && paddingSides.every(side=>d.getElementById(region+'-padding-'+side).getBoundingClientRect().height>=44);
    }));
  }
  app.style.width='1440px';evaluate('resetStudio()');await wait();
  test('Reset clears custom region padding and restores existing spacing defaults',()=>!evaluate('state.regionPadding') && paddingRegions.every(region=>paddingValues()[region].every(value=>value===0) && d.getElementById(region+'-padding-reset').disabled));
  // End region padding checks.
  await prepare(8);
  test('Spacing chart lists exactly the numbered spacing tokens in the CSS export', () => {
    const shown=[...d.querySelectorAll('#spacingBars .space-row span')].map(span=>'--'+span.firstChild.textContent);
    const exported=w.dssReadTokens().filter(row=>/^--space-\d+$/.test(row.name)).map(row=>row.name);
    return JSON.stringify(shown)===JSON.stringify(exported) && !shown.includes('--space-3');
  });
  input('jSpacing',8); await wait();
  test('Spacing chart labels update from the same source as exported tokens', () => [...d.querySelectorAll('#spacingBars .space-row span')].every(span=>parseInt(span.lastChild.textContent)===Number(span.firstChild.textContent.split('-')[1])*8) && evaluate('cssExport()').includes('--space-unit: 8px;'));
  input('jSpacing',4);
  await prepare(8);
  // A lesson uses the learner's own settings, real output and session comparison.
  for (const mode of ['basic','advanced']) for (const theme of ['light','dark']) {
    app.style.width='1440px';reset();await wait();
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    const beforeSpacingLesson=evaluate('projectJson()');
    d.querySelector('[data-journey-step="8"]').click();await wait();
    const spacingNode=d.querySelector('#studio-section-3 > .panel > .spacing-lesson');
    const exampleId=mode==='basic'?'lists':'services',exampleSelector=mode==='basic'?'.section':'.sample-section';
    test(mode+' '+theme+' spacing lesson connects five teaching parts without replacing the design',()=>spacingNode && [...spacingNode.querySelectorAll(':scope > section:not(#utilityLesson) > h4')].map(heading=>heading.textContent).join('|')==='Understand|Try|Observe|Inspect|Reflect' && evaluate('projectJson()')===beforeSpacingLesson && d.getElementById('spacingPrompt').textContent.includes('4 px to 6 px'));
    test(mode+' '+theme+' lesson starts its comparison from current exported spacing',()=>d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingBefore4').textContent==='16 px' && d.getElementById('spacingBefore8').textContent==='32 px' && d.getElementById('spacingCss').textContent.includes('--space-4: calc(var(--space-unit) * 4);'));
    d.getElementById('spacingEdit').click();
    test(mode+' '+theme+' lesson routes to the actual spacing control',()=>d.activeElement===d.getElementById('jSpacing') && evaluate('DSStudio.activeStage')===8);
    const spacingDocument=previewDoc();
    const beforeLessonPadding=parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart);
    input('jSpacing',6);await wait();
    test(mode+' '+theme+' spacing edit updates explanation, tokens and page without stealing control focus',()=>d.activeElement===d.getElementById('jSpacing') && previewDoc()===spacingDocument && d.getElementById('spacingNowUnit').textContent==='6 px' && d.getElementById('spacingNow4').textContent==='24 px' && d.getElementById('spacingNow8').textContent==='48 px' && d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingObservation').textContent.includes('4 px to 6 px') && parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart)===beforeLessonPadding*1.5);
    test(mode+' '+theme+' lesson shows the current sample HTML and consuming CSS rule',()=>evaluate('htmlExport()').includes(d.getElementById('spacingHtml').textContent) && d.getElementById('spacingHtml').textContent.includes('id="'+exampleId+'"') && d.getElementById('spacingHtml').children.length===0 && d.getElementById('spacingCss').textContent.includes(exampleSelector+' {') && d.getElementById('spacingConnection').textContent.includes('page currently measures '+parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart)+' px'));
    input('spacingReflection','My explanation <scr'+'ipt>window.lessonInjected=true</scr'+'ipt>');input('jAccent','#246a68');await wait();
    test(mode+' '+theme+' unrelated colour edits retain comparison, reflection and lesson nodes',()=>d.querySelector('.spacing-lesson')===spacingNode && d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingReflection').value.includes('My explanation') && !w.lessonInjected);
    input('advGap',32);await wait();
    test(mode+' '+theme+' grid gap is explained as a separate live decision',()=>d.getElementById('spacingGapNote').textContent.includes('32px') && d.getElementById('spacingGapNote').textContent.includes('comparison: 24px') && d.getElementById('spacingNow8').textContent==='48 px');
    const beforeCompare=evaluate('projectJson()');d.getElementById('spacingCompare').click();
    test(mode+' '+theme+' new comparison changes only session teaching state',()=>d.getElementById('spacingBeforeUnit').textContent==='6 px' && d.getElementById('spacingBefore8').textContent==='48 px' && evaluate('projectJson()')===beforeCompare);
    d.getElementById('spacingInspectTokens').click();
    test(mode+' '+theme+' Inspect spacing tokens opens complete current CSS',()=>d.getElementById('studioInspector').open && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='all' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingInspectRule').click();
    test(mode+' '+theme+' Inspect section CSS finds a real generated rule',()=>d.getElementById('dockCss').textContent.includes(exampleSelector+' {') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingInspectHtml').click();
    test(mode+' '+theme+' Inspect section HTML selects complete HTML',()=>d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingExample').click();await wait();
    test(mode+' '+theme+' preview observation opens the real section without changing project values',()=>previewDoc().activeElement===previewDoc().getElementById(exampleId) && d.getElementById('studio-section-4').open && evaluate('projectJson()')===beforeCompare);
    d.getElementById('spacingExample').click();d.getElementById('spacingInspectTokens').click();await wait();
    test(mode+' '+theme+' queued example focus cannot steal a subsequent code selection',()=>d.activeElement===d.getElementById('dockCss'));
    test(mode+' '+theme+' comparison, reflection and tutorial controls stay out of saved/exported data',()=>!evaluate('projectJson()+htmlExport()+cssExport()').includes('My explanation') && !evaluate('projectJson()+htmlExport()+cssExport()').includes('spacingReflection'));
    d.querySelector('[data-journey-step="9"]').click();d.querySelector('[data-journey-step="8"]').click();
    test(mode+' '+theme+' revisiting the lesson retains the session comparison',()=>d.getElementById('spacingBeforeUnit').textContent==='6 px' && d.getElementById('spacingReflection').value.includes('My explanation'));
  }
  d.getElementById('dockModeBasic').click();await wait();
  for (const [preset,token,multiplier] of [['mobile','--space-8',8],['tablet','--space-12',12],['desktop','--space-16',16]]) {
    d.querySelector('button[data-width="'+preset+'"]').click();d.getElementById('previewPage').getBoundingClientRect();await wait();
    test('Basic lesson follows actual responsive section padding at '+preset+' width',()=>{
      const connection=d.getElementById('spacingConnection').textContent,padding=parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById('lists')).paddingBlockStart);
      if(connection.includes('padding-block uses '+token) && connection.includes((6*multiplier)+' px') && padding===6*multiplier && d.getElementById('spacingCss').textContent.includes('var('+token+')')) return true;
      throw Error(JSON.stringify({preset,width:previewWindow().innerWidth,padding,connection,css:d.getElementById('spacingCss').textContent}));
    });
  }
  d.querySelector('button[data-width="fluid"]').click();await wait();
  const beforeLessonResize=evaluate('projectJson()');
  d.getElementById('dockToggle').click();await wait();
  test('Fluid lesson reacts to released inspector width without changing the comparison',()=>{
    const connection=d.getElementById('spacingConnection').textContent;
    if(connection.includes('padding-block uses --space-12') && d.getElementById('spacingBeforeUnit').textContent==='6 px' && evaluate('projectJson()')===beforeLessonResize) return true;
    throw Error(JSON.stringify({width:previewWindow().innerWidth,connection,before:d.getElementById('spacingBeforeUnit').textContent,inspector:d.getElementById('studioInspector').open}));
  });
  d.getElementById('inspectorToggle').click();await wait();
  test('Fluid lesson follows the narrower rule when inspector opens again',()=>d.getElementById('spacingConnection').textContent.includes('padding-block uses --space-8') && evaluate('projectJson()')===beforeLessonResize);
  evaluate('importConfig({spacing:7.25})');await wait();
  test('Imported spacing drives lesson arithmetic from settled generated declarations',()=>d.getElementById('spacingNowUnit').textContent==='7.25 px' && d.getElementById('spacingNow4').textContent==='29 px' && d.getElementById('spacingNow8').textContent==='58 px' && d.getElementById('spacingBeforeUnit').textContent==='7.25 px' && !d.getElementById('spacingReflection').value && d.getElementById('spacingGapNote').textContent.startsWith('Grid gap is 24px.'));
  input('jSpacing',8);d.getElementById('spacingCompare').click();
  test('Spacing experiment stays within the real control limits at the upper bound',()=>d.getElementById('spacingPrompt').textContent.includes('8 px to 6 px'));
  input('spacingReflection','Clear after project reset');reset();await wait();
  test('Reset starts a fresh comparison and clears optional reflection',()=>d.getElementById('spacingBeforeUnit').textContent==='4 px' && !d.getElementById('spacingReflection').value);
  input('jProject','Spacing lesson test');d.getElementById('jSaveLocal').click();input('spacingReflection','Clear after local load');d.getElementById('jLoadLocal').click();await wait();
  test('Loading even identical saved project values starts a fresh tutorial session comparison',()=>!d.getElementById('spacingReflection').value && d.getElementById('spacingBeforeUnit').textContent==='4 px');
  const spacingPracticeWasOpen=d.getElementById('utilityPractice').open;
  for (const theme of ['light','dark']) for (const width of [320,901,1440]) {
    app.style.width=width+'px';input('jTheme',theme);await wait();d.querySelector('[data-journey-step="8"]').click();
    // Measure displayed controls, not cached geometry inside a closed disclosure.
    d.getElementById('utilityPractice').open=true;await wait();
    test(theme+' spacing tutorial stays within its lesson at '+width+'px',()=>{
      const lesson=d.querySelector('.spacing-lesson'),box=lesson.getBoundingClientRect();
      const source=d.getElementById('jSpacing'),inline=source.closest('.spacing-lesson > section');
      const buttons=[...lesson.querySelectorAll('.button-row > button')].map(button=>{const b=button.getBoundingClientRect();return {id:button.id,height:b.height,left:b.left,right:b.right,closedPractice:button.closest('#utilityPractice')?.open===false};});
      const fits=d.documentElement.scrollWidth<=w.innerWidth+1 && lesson.scrollWidth<=lesson.clientWidth+1 && (width>900?source.closest('.studio-journey')!==null:inline?.querySelector('h4').textContent==='Try') && buttons.every(b=>b.height>=44 && b.left>=box.left-1 && b.right<=box.right+1);
      if(!fits)throw Error(JSON.stringify({documentWidth:d.documentElement.scrollWidth,viewport:w.innerWidth,lessonWidth:lesson.clientWidth,lessonScroll:lesson.scrollWidth,left:box.left,right:box.right,inline:inline?.querySelector('h4').textContent,desktop:!!source.closest('.studio-journey'),buttons}));
      return true;
    });
  }
  d.getElementById('utilityPractice').open=spacingPracticeWasOpen;
  app.style.width='1440px';reset();await wait();
  await prepare(8);
  // Working plain-CSS utilities retain semantic HTML and component defaults.
  reset();await wait();
  w.dssShowWizardStep(8);await wait();
  test('Local CSS starts with a linked stylesheet and utility practice stays optional',()=>d.getElementById('localCardHtml').textContent.includes('<link rel="stylesheet" href="tokens.css">') && d.getElementById('localCardHtml').textContent.includes('<article class="card">') && !d.getElementById('localCardHtml').querySelector('article,link') && !d.getElementById('utilityPractice').open && !d.getElementById('utilityVocabularyDetails').open && d.getElementById('localCardCss').getBoundingClientRect().height>0);
  test('Optional utility examples are bounded native CSS and excluded from website CSS',()=>w.DSStudio.utilities.definitions.length===20 && new Set(w.DSStudio.utilities.definitions.map(item=>item.name)).size===20 && w.DSStudio.utilities.definitions.every(item=>w.CSS.supports(item.property,item.value) && w.DSStudio.utilities.css().includes(w.DSStudio.utilities.rule(item.name)) && !evaluate('cssExport()').includes(w.DSStudio.utilities.rule(item.name))) && w.DSStudio.utilities.rule('__proto__')==='');
  const utilityParityFrame=d.createElement('iframe');utilityParityFrame.style.cssText='border:0;position:absolute;left:-10000px';d.body.append(utilityParityFrame);
  const utilityNames=new Set(w.DSStudio.utilities.definitions.map(item=>item.name));
  const utilityStyleKeys=['display','flexDirection','flexWrap','alignItems','justifyContent','gap','padding','backgroundColor','color','borderRadius','border','boxShadow','opacity','fontFamily','fontSize','lineHeight','width','height'];
  const utilitySignature=(el,view)=>{const cs=view.getComputedStyle(el);return utilityStyleKeys.map(key=>cs[key]).join('|');};
  const utilityTargets='.card,.media-object,.hero-layout,.skills-layout,.list-grid,.sample-flex-row,.sample-flex-media,.sample-flex-stack';
  async function loadUtilityPractice() {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    parsed.getElementById(evaluate('state.sampleMode')==='basic'?'basic-structure':'lesson-brief').classList.add('p-6','bg-surface','text-content','rounded-card');
    const utilityBlob=w.URL.createObjectURL(new w.Blob([evaluate('cssExport()')+w.DSStudio.utilities.css()],{type:'text/css'}));
    parsed.querySelector('link[href="tokens.css"]').href=utilityBlob;
    utilityParityFrame.style.width=previewWindow().innerWidth+'px';utilityParityFrame.style.height=previewWindow().innerHeight+'px';
    await new Promise(resolve=>{utilityParityFrame.onload=resolve;utilityParityFrame.srcdoc='<!doctype html>'+parsed.documentElement.outerHTML;});
    w.URL.revokeObjectURL(utilityBlob);
  }
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const custom of [false,true]) {
      if(custom){input('jSpacing',8);input('jRadius',26);input('advGap',32);input('advOpacity',75);input('advShadow','medium','change');}
      for(const width of [320,1440]) {
        app.style.width=width+'px';d.querySelector('[data-width="fluid"]').click();await wait();
        await loadUtilityPractice();
        const actual=[...previewDoc().querySelectorAll(utilityTargets)],native=[...utilityParityFrame.contentDocument.querySelectorAll(utilityTargets)];
        test(mode+' '+theme+' '+(custom?'custom':'default')+' separate utility practice matches component appearance at '+width+'px',()=>actual.length>0 && actual.length===native.length && actual.every((el,index)=>utilitySignature(el,previewWindow())===utilitySignature(native[index],utilityParityFrame.contentWindow)));
        const article=previewDoc().getElementById(mode==='basic'?'basic-structure':'lesson-brief');
        test(mode+' '+theme+' '+(custom?'custom':'default')+' website HTML keeps component classes without exercise utilities at '+width+'px',()=>![...previewDoc().querySelectorAll('[class]')].some(el=>[...el.classList].some(name=>utilityNames.has(name))) && !evaluate('cssExport()').includes('OPTIONAL PRACTICE'));
        test(mode+' '+theme+' '+(custom?'custom':'default')+' semantic article uses its shared local card rule at '+width+'px',()=>article.tagName==='ARTICLE' && article.classList.contains('card') && Math.abs(parseFloat(previewWindow().getComputedStyle(article).paddingTop)-evaluate('state.spacing')*6)<.01 && !previewDoc().querySelector('script'));
      }
    }
  }
  app.style.width='1440px';reset();await wait();
  const beforeUtilityExercise=evaluate('htmlExport()+cssExport()+projectJson()'),beforeExerciseDoc=previewDoc();
  await loadUtilityPractice();
  const exerciseWindow=utilityParityFrame.contentWindow;
  const utilityArticle=utilityParityFrame.contentDocument.getElementById('lesson-brief'),utilityOriginalClass=utilityArticle.className;
  utilityArticle.classList.replace('p-6','p-4');
  test('Practice-only p-4 changes padding and retains article meaning and component border',()=>exerciseWindow.getComputedStyle(utilityArticle).paddingTop==='16px' && utilityArticle.tagName==='ARTICLE' && utilityArticle.classList.contains('card') && parseFloat(exerciseWindow.getComputedStyle(utilityArticle).borderTopWidth)>0);
  utilityArticle.className='p-6 p-4 card bg-surface text-content rounded-card';const utilityFirstOrder=exerciseWindow.getComputedStyle(utilityArticle).paddingTop;
  utilityArticle.className='p-4 p-6 card bg-surface text-content rounded-card';
  test('Conflicting practice utilities follow stylesheet order rather than HTML class order',()=>utilityFirstOrder==='24px' && exerciseWindow.getComputedStyle(utilityArticle).paddingTop===utilityFirstOrder);
  utilityArticle.className=utilityOriginalClass;utilityArticle.classList.replace('bg-surface','bg-primary');utilityArticle.classList.replace('text-content','text-on-primary');
  test('Practice colour utilities consume active project theme roles',()=>exerciseWindow.getComputedStyle(utilityArticle).backgroundColor===evaluate("'rgb('+hexRgb(palette().roles.primary).join(', ')+')'") && exerciseWindow.getComputedStyle(utilityArticle).color===evaluate("'rgb('+hexRgb(palette().roles['on-primary']).join(', ')+')'"));
  test('Utility practice leaves website preview and all exports unchanged',()=>previewDoc()===beforeExerciseDoc && evaluate('htmlExport()+cssExport()+projectJson()')===beforeUtilityExercise && previewWindow().getComputedStyle(previewDoc().getElementById('lesson-brief')).paddingTop==='24px');
  utilityParityFrame.remove();
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);w.dssShowWizardStep(8);await wait();
    const id=mode==='basic'?'basic-structure':'lesson-brief';
    test(mode+' '+theme+' local CSS example reads the exported component rule',()=>evaluate('cssExport()').replace(/\s+/g,'').includes(d.getElementById('localCardCss').textContent.replace(/\s+/g,'')) && d.getElementById('localCardCss').textContent.startsWith('.card {\n  ') && d.getElementById('localCardCss').textContent.includes('padding: var(--space-6)'));
    d.getElementById('utilityPractice').open=true;await wait();
    test(mode+' '+theme+' lesson follows spacing reflection and reads the real article tag',()=>d.getElementById('utilityLesson').closest('.studio-lesson').classList.contains('spacing-lesson') && d.getElementById('utilityLesson').previousElementSibling.querySelector('h4').textContent==='Reflect' && d.getElementById('utilityHtml').textContent.includes('id="'+id+'"') && evaluate('htmlExport()').includes(d.getElementById('utilityHtml').textContent));
    for(const name of ['p-6','p-4','bg-surface','text-content','rounded-card']) {
      input('utilityClass',name,'change');await wait();const definition=w.DSStudio.utilities.definitions.find(item=>item.name===name);
      test(mode+' '+theme+' lesson separates practice '+name+' from actual component output',()=>d.getElementById('utilityRule').textContent===w.DSStudio.utilities.rule(name) && !evaluate('cssExport()').includes(d.getElementById('utilityRule').textContent) && d.getElementById('utilityPracticeHtml').textContent.includes(' '+name+'"') && !evaluate('htmlExport()').includes(d.getElementById('utilityPracticeHtml').textContent) && !d.getElementById('utilityPracticeHtml').children.length && d.getElementById('utilityToken').textContent.includes(definition.token+':') && d.getElementById('utilityMeasured').textContent.includes('component preview measures '+definition.property+': '+previewWindow().getComputedStyle(previewDoc().getElementById(id)).getPropertyValue(definition.property)));
    }
  }
  input('utilityClass','p-6','change');input('jSpacing',7);await wait();
  test('Source edits refresh lesson and page padding',()=>d.getElementById('utilityToken').textContent.includes('--space-unit: 7px') && d.getElementById('utilityMeasured').textContent.includes('42px'));
  d.getElementById('utilityConfigure').click();
  test('Utility configuration focuses the existing spacing control',()=>d.activeElement===d.getElementById('jSpacing') && w.DSStudio.activeStage===8);
  d.getElementById('utilityInspectCss').click();await wait();
  test('Component CSS inspection keeps the complete local stylesheet',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockNote').textContent.includes('No framework needed') && !d.getElementById('dockCss').textContent.includes('.p-6 {'));
  d.getElementById('dockTabHtml').click();d.getElementById('localInspectCss').click();await wait();
  test('Local-first action opens component CSS from the HTML inspector',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.activeElement===d.getElementById('dockCss'));
  d.getElementById('utilityInspectHtml').click();await wait();
  test('Utility HTML inspection keeps the complete semantic page',()=>d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  const utilityProject=evaluate('projectJson()'),utilityDocument=previewDoc();d.getElementById('utilityPreview').click();await wait();
  test('Showing the utility article retains project and preview document',()=>previewDoc()===utilityDocument && previewDoc().activeElement===previewDoc().getElementById('lesson-brief') && evaluate('projectJson()')===utilityProject);
  test('Showing the utility article brings the preview into view',()=>d.getElementById('previewShell').getBoundingClientRect().top>=0 && d.getElementById('previewShell').getBoundingClientRect().top<w.innerHeight);
  for(const width of [320,390,1440])for(const theme of ['light','dark']) {
    app.style.width=width+'px';input('jTheme',theme);w.dssShowWizardStep(8);d.querySelectorAll('#utilityLesson details').forEach(details=>details.open=true);await wait();
    test(theme+' utility lesson fits '+width+'px with usable controls',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['localInspectCss','utilityClass','utilityPreview','utilityInspectHtml','utilityInspectCss','utilityConfigure'].every(id=>{const r=d.getElementById(id).getBoundingClientRect();return r.height>=44 && r.left>=0 && r.right<=w.innerWidth+1;}) && (width>390 || d.querySelector('.utility-table-scroll').scrollWidth>d.querySelector('.utility-table-scroll').clientWidth));
  }
  app.style.width='1440px';reset();await wait();
  w.dssShowWizardStep(8);await wait();
  const beforeLearningPath=evaluate('projectJson()'),learningPathDoc=previewDoc();
  d.getElementById('utilityToTailwind').click();await wait();
  test('Optional next step reaches Tailwind without changing the local website',()=>w.DSStudio.activeStage===11 && !d.getElementById('studio-section-6').hidden && evaluate('projectJson()')===beforeLearningPath && previewDoc()===learningPathDoc && d.getElementById('tailwindBridge').textContent.includes('separate Tailwind v4 practice project'));
  d.querySelector('#tailwindBridge a[href="#utilityLesson"]').click();await wait();
  test('Tailwind exercise links back to the local CSS lesson',()=>w.DSStudio.activeStage===8 && !d.getElementById('studio-section-3').hidden && evaluate('projectJson()')===beforeLearningPath && previewDoc()===learningPathDoc);

  test('No spacing JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Focused harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
