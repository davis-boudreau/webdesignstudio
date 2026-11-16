"""Independent typography checks using the local Chrome runner.

Run: python scripts/typography_review.py. Owns its app, profile and fixtures.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Typography review</title>
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
  const input=(id,value,type='input')=>{const el=d.getElementById(id);w.DSStudio.paletteWorkspace?.revealControl(el);w.DSStudio.typographyWorkspace?.revealControl(el);el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));w.DSStudio.propertyEditors?.saveFor(el);};
  const prepare=async step=>{
    app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();
    reset();w.DSStudio.inspector.show({language:'css',section:'all'});d.querySelector('[data-width="fluid"]').click();w.dssShowWizardStep(step,false);await wait();
  };
  try {
  test('Independent typography startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  await prepare(5);
  test('Startup selects Minor Third 1.2 throughout the typography controls and export', () => evaluate('state.ratio===1.2 && cssExport().includes("--type-ratio: 1.2;")') && ['jScalePreset','clampScalePreset'].every(id=>d.getElementById(id).value==='minor-third') && ['ratio','jRatio','clampRatio'].every(id=>d.getElementById(id).value==='1.2'));
  await prepare(5);
  input('jFont','Georgia, \'Times New Roman\', serif');
  test('Typography specimens use selected font', () => w.getComputedStyle(d.querySelector('#mobileType .sample')).fontFamily.includes('Georgia'));
  reset();
  await prepare(5);
  input('jScalePreset','minor-second','change'); await wait();
  test('Minor Second preset updates the scale without changing mobile percentage', () => evaluate('state.ratio===1.067 && clampConfig.mobileFactor===.82') && d.getElementById('clampScalePreset').value==='minor-second');
  input('clampScalePreset','perfect-fourth','change'); await wait();
  test('Calculator scale preset synchronizes the guided builder', () => evaluate('state.ratio===1.333') && d.getElementById('jScalePreset').value==='perfect-fourth');
  input('clampFactor',.75); await wait();
  test('Mobile heading percentage does not change the scale interval', () => evaluate('state.ratio===1.333 && clampConfig.mobileFactor===.75'));
  input('ratio',1.29); await wait();
  test('Manual ratio selects Custom in both preset controls', () => d.getElementById('jScalePreset').value==='custom' && d.getElementById('clampScalePreset').value==='custom');
  reset(); await wait();
  test('Reset restores Minor Third without changing responsive heading limits', () => evaluate('state.ratio===1.2 && clampConfig.mobileFactor===.82') && d.getElementById('jScalePreset').value==='minor-third' && d.getElementById('clampScalePreset').value==='minor-third');
  test('Typography ladder displays matching PX and REM values', () => {
    const base=d.querySelectorAll('#typeLadder .type-row small')[2].textContent;
    const step=d.querySelectorAll('#typeLadder .type-row small')[3].textContent;
    return base.includes('16px') && base.includes('1rem') && step.includes('19.2px') && step.includes('1.2rem');
  });
  test('Mobile and desktop specimens also include REM values', () => d.querySelector('#mobileType small').textContent.includes('rem') && d.querySelector('#desktopType small').textContent.includes('rem'));
  input('typoHeadingTracking',.03); input('typoBodyTracking',.02); await wait();
  test('Direct em controls synchronize all typography editors', () => evaluate('state.headingTracking===.03 && state.bodyTracking===.02 && adv.tracking===3') && d.getElementById('jHeadingTracking').value==='0.03' && d.getElementById('advTrackingOut').textContent==='0.03em');
  test('Specimen letter spacing scales with the local font size', () => {
    const heading=w.getComputedStyle(d.querySelector('#desktopType .sample'));
    const body=w.getComputedStyle(d.querySelectorAll('#desktopType .sample')[3]);
    return Math.abs(parseFloat(heading.letterSpacing)-parseFloat(heading.fontSize)*.03)<.001 && Math.abs(parseFloat(body.letterSpacing)-.32)<.001;
  });
  test('Responsive preview uses heading and body em spacing', () => {
    const heading=previewWindow().getComputedStyle(previewDoc().querySelector('h1'));
    const body=previewWindow().getComputedStyle(previewDoc().body);
    return Math.abs(parseFloat(heading.letterSpacing)-parseFloat(heading.fontSize)*.03)<.001 && Math.abs(parseFloat(body.letterSpacing)-parseFloat(body.fontSize)*.02)<.001;
  });
  test('CSS export contains heading and body letter-spacing tokens', () => evaluate('cssExport()').includes('--heading-letter-spacing: 0.03em') && evaluate('cssExport()').includes('--body-letter-spacing: 0.02em'));
  const typographyProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+typographyProject+')'); await wait();
  test('Letter-spacing settings round trip through JSON', () => evaluate('state.headingTracking===.03 && state.bodyTracking===.02 && adv.tracking===3'));
  evaluate('importConfig({advanced:{tracking:-3}})'); await wait();
  test('Older heading-tracking projects migrate from hundredths to em', () => evaluate('state.headingTracking===-.03 && state.bodyTracking===0'));
  input('advTracking',2.5); await wait();
  test('Existing advanced tracking control updates the shared em setting', () => evaluate('state.headingTracking===.025') && d.getElementById('typoHeadingTrackingOut').textContent==='0.025em');
  d.getElementById('clampReset').click();w.DSStudio.propertyEditors.saveFor(d.getElementById('clampReset')); await wait();
  test('Reset responsive limits preserves letter spacing', () => evaluate('clampConfig.mobileFactor===.82 && state.headingTracking===.025'));
  await prepare(5);
  test('System fonts remain the offline default in the studio, preview and HTML export', () => evaluate('state.fontSettings.source')==='system' && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && !evaluate('htmlExport()').includes('fonts.googleapis.com') && d.getElementById('fontFallback').disabled);
  input('fontSystemHeading','georgia','change'); await wait();
  test('Separate system heading and body fonts reach specimens and the generated page', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Georgia') && w.getComputedStyle(d.querySelector('#mobileType [data-font-role="body"]')).fontFamily.includes('Arial') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Georgia') && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Arial'));
  evaluate(`importConfig({font:"Georgia, 'Times New Roman', serif"})`); await wait();
  test('Legacy font projects import without opting in to network fonts', () => evaluate('state.fontSettings.source==="system" && state.fontSettings.systemHeading==="same"') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Georgia') && !d.querySelector('link[data-dss-font]'));
  evaluate('importConfig({fontSettings:{source:"https://evil.invalid",body:"Inter; color:red",heading:"__proto__",systemHeading:"bad",weights:["400",-1,400,500,10000]}})');
  test('Font imports reject arbitrary sources, family CSS and invalid weights', () => evaluate('state.fontSettings.source==="system" && state.fontSettings.body==="inter" && state.fontSettings.heading==="same" && state.fontSettings.systemHeading==="same" && JSON.stringify(state.fontSettings.weights)==="[400,500]"') && !evaluate('cssExport()+htmlExport()').includes('evil.invalid'));
  reset(); await wait();
  // Serve deterministic local font-face fixtures; the separate live-CDN smoke check
  // verifies real downloads without making this regression suite depend on Google.
  let fontFixtureMode='ok';
  const fontRequests=[], fontRestores=[];
  for (const doc of [d, previewDoc()]) {
    const head=doc.head, originalAppend=head.append;
    head.append=function(...nodes) {
      for (const node of nodes) if (node.tagName==='LINK' && node.href?.startsWith('https://fonts.')) {
        const originalUrl=new URL(node.href);
        if (node.rel==='stylesheet') {
          fontRequests.push(node.href);
          node.href='/__font_fixture__'+originalUrl.search+'&mode='+fontFixtureMode;
        } else node.href=w.location.origin;
      }
      return originalAppend.apply(this,nodes);
    };
    fontRestores.push(()=>{head.append=originalAppend;});
  }
  d.getElementById('jSaveLocal').click();
  const fontProjectId=d.getElementById('jProjects').value;
  input('fontSource','google','change');
  test('Google font selection reports loading and enables the CDN controls', () => d.getElementById('fontLoadStatus').dataset.state==='loading' && !d.getElementById('fontGoogleOptions').hidden && d.getElementById('font').disabled && d.getElementById('jFont').disabled);
  await wait(250);
  test('Font stylesheets and font faces load successfully through the browser', () => d.getElementById('fontLoadStatus').dataset.state==='loaded' && [...d.fonts].some(face=>face.family.includes('Inter') && face.status==='loaded') && [...previewDoc().fonts].some(face=>face.family.includes('Inter') && face.status==='loaded'));
  test('Each saved or learning stylesheet deduplicates shared heading/body families', () => fontRequests.length>=2 && fontRequests.every(href=>new URL(href).searchParams.getAll('family').length===1));
  input('fontGoogleHeading','literata','change'); await wait(250);
  test('Google heading/body selections update specimens, components and the preview', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Literata') && w.getComputedStyle(d.querySelector('#mobileType [data-font-role="body"]')).fontFamily.includes('Inter') && w.getComputedStyle(d.querySelector('.bd-button')).fontFamily.includes('Inter') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter'));
  const fontExport=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('HTML exports include deduplicated preconnects, crossorigin and the CSS2 font request', () => fontExport.querySelectorAll('link[rel="preconnect"]').length===2 && fontExport.querySelector('link[href="https://fonts.gstatic.com"]').hasAttribute('crossorigin') && fontExport.querySelector('link[href^="https://fonts.googleapis.com/css2?"]').getAttribute('href')===evaluate('DSStudio.fonts.url()') && evaluate('htmlExport()').includes('&amp;display=swap'));
  test('Font requests include selected families, page weights and italic body copy', () => {
    const request=new URL(evaluate('DSStudio.fonts.url()'));
    return request.searchParams.get('display')==='swap' && request.searchParams.getAll('family').join('|').includes('Inter:ital,wght@0,400;0,600;0,700;1,400') && request.searchParams.getAll('family').join('|').includes('Literata:wght@400;600;700');
  });
  d.getElementById('fontWeight500').click();w.DSStudio.propertyEditors.saveFor(d.getElementById('fontWeight500')); input('advWeight',800,'change'); input('bdWeight',700); await wait(250);
  test('Optional and currently used weights stay represented in generated requests', () => evaluate('DSStudio.fonts.url()').includes('0,500') && evaluate('DSStudio.fonts.url()').includes('0,800') && d.getElementById('fontWeight800').checked && d.getElementById('fontWeight800').disabled && d.getElementById('fontWeight400').disabled);
  evaluate('importConfig({...JSON.parse(projectJson()),buttonDesign:{...state.buttonDesign,weight:650}})'); await wait(250);
  test('Font requests use the validated button weight after import', () => evaluate('state.buttonDesign.weight===600 && !DSStudio.fonts.url().includes("0,650")') && evaluate('cssExport()').includes('--button-font-weight: 600'));
  input('bdWeight',700); await wait(250);
  test('Font settings autosave with the active local project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[fontProjectId].data.fontSettings.heading==='literata' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[fontProjectId].data.fontSettings.weights.includes(500));
  test('Learning examples match the actual HTML links and font tokens', () => d.getElementById('fontHtmlCode').textContent===evaluate('DSStudio.fonts.htmlLinks()') && d.getElementById('fontCssCode').textContent.includes('--font-heading: "Literata"') && evaluate('cssExport()').includes('--font-body: "Inter"') && evaluate('cssExport()').includes('--font-ui: var(--font-body)'));
  const fontCssBefore=evaluate('cssExport()'), fontHtmlBefore=evaluate('htmlExport()'), fontJsonBefore=evaluate('projectJson()');
  const mainFontLink=d.querySelector('link[data-dss-font][rel="stylesheet"]'), previewFontLink=previewDoc().querySelector('link[data-dss-font][rel="stylesheet"]');
  input('jRadius',20); await wait();
  test('Unrelated live edits preserve existing font stylesheet nodes', () => d.querySelector('link[data-dss-font][rel="stylesheet"]')===mainFontLink && previewDoc().querySelector('link[data-dss-font][rel="stylesheet"]')===previewFontLink);
  input('jRadius',12); await wait();
  const beforeFallbackRequests=fontRequests.length;
  d.getElementById('fontFallback').click(); await wait();
  test('Fallback comparison updates samples and preview without altering saved settings or exports', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Georgia') && !previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter') && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && d.getElementById('fontLoadStatus').dataset.state==='fallback' && evaluate('cssExport()')===fontCssBefore && evaluate('htmlExport()')===fontHtmlBefore && evaluate('projectJson()')===fontJsonBefore && fontRequests.length===beforeFallbackRequests);
  d.getElementById('fontFallback').click(); await wait(250);
  test('Turning comparison off restores selected fonts in the same preview document', () => previewDoc().documentElement.dataset.theme==='light' && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Literata') && d.getElementById('fontLoadStatus').dataset.state==='loaded');
  const fontRoundTrip=evaluate('projectJson()');
  reset(); evaluate('importConfig('+fontRoundTrip+')'); await wait(250);
  test('Font selections and weights survive JSON import and reset clears comparison', () => evaluate('state.fontSettings.heading==="literata" && state.fontSettings.body==="inter" && state.fontSettings.weights.includes(500)') && d.getElementById('fontSource').value==='google' && !d.getElementById('fontFallback').checked && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter'));
  fontFixtureMode='error'; input('fontGoogleBody','source-sans-3','change'); await wait(250);
  test('A failed font stylesheet offers readable fallbacks and a retry action', () => d.getElementById('fontLoadStatus').dataset.state==='error' && !d.getElementById('fontRetry').hidden && previewDoc().querySelector('h1').getBoundingClientRect().height>0);
  fontFixtureMode='ok'; d.getElementById('fontRetry').click(); await wait(250);
  // Offscreen iframe text may defer font use until painted; explicitly request
  // the face to verify that retry made it available to the preview document.
  await previewDoc().fonts.load('400 16px "Source Sans 3"');
  test('Retry recovers both selected font families without resetting the project', () => {
    const report={status:d.getElementById('fontLoadStatus').dataset.state,body:evaluate('state.fontSettings.body'),faces:[...previewDoc().fonts].map(face=>({family:face.family,status:face.status})),links:[...previewDoc().querySelectorAll('link[data-dss-font]')].map(link=>link.href)};
    if (report.status!=='loaded' || report.body!=='source-sans-3' || !report.faces.some(face=>face.family.includes('Source Sans 3') && face.status==='loaded')) throw Error(JSON.stringify(report));
    return true;
  });
  d.getElementById('fontFallback').click();await wait();
  input('fontSource','system','change'); await wait();
  test('Switching to system fonts removes all managed font connections and restores body controls', () => !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && !d.getElementById('font').disabled && !d.getElementById('jFont').disabled && !evaluate('htmlExport()').includes('fonts.googleapis.com'));
  test('Saving a different font source clears the previous fallback comparison',()=>!w.DSStudio.fonts.showFallback && !d.getElementById('fontFallback').checked);
  fontFixtureMode='error'; input('fontSource','google','change'); input('fontSource','system','change'); await wait(250);
  test('Stale font callbacks cannot replace the status after switching back to system fonts', () => d.getElementById('fontLoadStatus').dataset.state==='system' && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]'));
  for (const restore of fontRestores) restore();
  reset(); await wait();
  await prepare(5);
  d.querySelector('[data-journey-step="5"]').click(); d.getElementById('jSaveLocal').click();
  input('jHeadingLeading',1.4); await wait();
  test('Wizard heading line-height updates exported CSS and rendered page', () => evaluate('state.headingLeading===1.4 && cssExport().includes("--heading-leading: 1.4;")') && Math.abs(parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).lineHeight)/parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontSize)-1.4)<.01);
  test('Heading line-height autosaves to the active local project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data.headingLeading===1.4);
  input('jLeading',1.7); input('advWeight',800,'change'); await wait();
  test('Typography ladder follows heading and body line-height settings', () => [...d.querySelectorAll('#typeLadder .sample')].every(sample=>{
    const style=w.getComputedStyle(sample), expected=sample.dataset.fontRole==='heading'?1.4:1.7;
    return Math.abs(parseFloat(style.lineHeight)/parseFloat(style.fontSize)-expected)<.01;
  }));
  test('Heading specimens and ladder follow the selected heading weight', () => [...d.querySelectorAll('#mobileType [data-font-role="heading"],#desktopType [data-font-role="heading"],#typeLadder [data-font-role="heading"]')].every(sample=>w.getComputedStyle(sample).fontWeight==='800') && [...d.querySelectorAll('#typeLadder [data-font-role="body"]')].every(sample=>w.getComputedStyle(sample).fontWeight==='400'));
  const headingProject=evaluate('projectJson()'); evaluate('importConfig('+headingProject+')'); await wait();
  test('Heading line-height survives JSON imports and synchronizes the wizard', () => evaluate('state.headingLeading')===1.4 && d.getElementById('jHeadingLeading').value==='1.4');
  evaluate('importConfig({headingLeading:99})'); await wait();
  test('Imported heading line-height is bounded and old projects keep the default', () => {
    const bounded=evaluate('state.headingLeading')===1.6;
    evaluate('importConfig({})'); return bounded && evaluate('state.headingLeading')===1.18;
  });
  await prepare(5);
  evaluate('importConfig({ratio:1.25})'); await wait();
  test('Previously saved Major Third projects retain their explicit scale', () => evaluate('state.ratio===1.25') && d.getElementById('jScalePreset').value==='major-third');
  evaluate('importConfig({})'); await wait();
  test('Projects without a ratio inherit the Minor Third default', () => evaluate('state.ratio===1.2') && d.getElementById('clampScalePreset').value==='minor-third');
  input('jRatio',1.4); d.getElementById('jNewLocal').click(); await wait();
  test('New project starts with Minor Third after a custom scale', () => evaluate('state.ratio===1.2') && d.getElementById('jScalePreset').value==='minor-third');
  await prepare(5);
  const get=id=>d.getElementById(id),ui=w.DSStudio.typographyWorkspace;
  const bar=()=>d.querySelector('[data-property-actions="typography"]'),save=()=>bar().querySelector('button').click(),discard=()=>bar().querySelectorAll('button')[1].click();
  const draft=(id,value,event='input')=>{ui.revealControl(get(id));get(id).value=value;get(id).dispatchEvent(new w.Event(event,{bubbles:true}));};
  const visible=id=>get(id).getBoundingClientRect().width>0;
  const rows=()=>[...get('typeLadder').children];
  test('Unified workspace has five independent control groups and one shared action bar',()=>get('type-control-pane').querySelectorAll('[data-type-stage]').length===5 && get('typography-workspace').querySelectorAll('[data-property-actions]').length===1 && !!bar());
  test('Review group and redundant component selector are removed from settings and topic navigation',()=>!get('type-stage-review') && !get('type-context-choice') && !d.querySelector('[data-type-go="review"]') && [...d.querySelectorAll('[data-type-go]')].map(el=>el.dataset.typeGo).join(',')==='content,fonts,body,hierarchy,responsive');
  test('Selected font details live with the sample and comparisons stay above it',()=>get('type-learning-preview').contains(get('type-context-family')) && get('type-learning-preview').contains(get('type-context-size')) && visible('type-selected-text-details') && get('type-learning-preview').contains(get('type-preview-enlarge')) && get('type-learning-preview').contains(get('type-preview-spacing')));
  test('Generated CSS is global to Typography immediately below the Learning preview',()=>{const panel=get('type-generated-css'),preview=get('type-learning-preview');return preview.nextElementSibling===panel && panel.parentElement===preview.parentElement && !panel.closest('[data-type-stage]') && panel.contains(get('clampCss')) && panel.contains(get('clampMath')) && !panel.contains(get('clampGraph'));});
  const calculationLesson=get('clamp-calculation-lesson'),lessonSummary=calculationLesson.querySelector('summary');
  test('Clamp calculation is an initially closed, labelled native disclosure beside the generated CSS',()=>calculationLesson.tagName==='DETAILS' && !calculationLesson.open && lessonSummary.textContent==='Learn the clamp calculation' && get('type-generated-css').contains(calculationLesson) && get('clampCss').parentElement.nextElementSibling===calculationLesson);
  const beforeLesson=evaluate('projectJson()'),beforeLessonCss=evaluate('cssExport()');lessonSummary.focus();lessonSummary.click();await wait();
  test('Opening the four-step lesson preserves saved output and property drafts',()=>calculationLesson.open && get('clampCalculationSteps').children.length===4 && evaluate('projectJson()')===beforeLesson && evaluate('cssExport()')===beforeLessonCss && !w.DSStudio.propertyEditors.hasDrafts('typography'));
  test('Viewport slider and graph belong to the Responsive typography exploration disclosure',()=>{const exploration=get('clampGraph').closest('.type-reference');return get('type-stage-responsive').contains(exploration) && exploration.contains(get('clampViewport')) && !get('type-learning-preview').contains(get('clampViewport')) && exploration.querySelector('summary').textContent==='Explore the viewport';});
  test('Viewport exploration and generated CSS headings have no step numbers',()=>[...get('typography-workspace').querySelectorAll('h4,summary')].some(el=>el.textContent==='Explore the viewport') && ![...get('typography-workspace').querySelectorAll('h4,summary')].some(el=>/^[34]\s/.test(el.textContent)));
  test('Realistic sample and all eight scale rows are visible together',()=>visible('type-realistic-sample') && visible('typeLadder') && rows().length===8);
  const previewDisclosure=get('type-learning-preview'),previewSummary=get('type-specimen-title'),beforeCollapse=evaluate('projectJson()'),beforeCollapseCss=evaluate('cssExport()');
  test('Learning preview uses an initially open native disclosure',()=>previewDisclosure.tagName==='DETAILS' && previewDisclosure.open && previewSummary.tagName==='SUMMARY' && previewSummary.parentElement===previewDisclosure);
  previewSummary.focus();previewSummary.click();await wait();
  test('Collapsing Learning preview keeps global CSS and the full ladder visible without changing project',()=>!previewDisclosure.open && !visible('type-realistic-sample') && visible('type-generated-css') && visible('typeLadder') && d.activeElement===previewSummary && evaluate('projectJson()')===beforeCollapse);
  draft('jBase',20);await wait();
  test('Global CSS follows drafts while Learning preview stays collapsed',()=>!previewDisclosure.open && get('clampCss').textContent.includes('20px') && get('type-css-state').textContent.startsWith('Proposed CSS') && evaluate('projectJson()')===beforeCollapse && evaluate('cssExport()')===beforeCollapseCss);
  discard();previewSummary.click();await wait();
  test('Reopening Learning preview restores its saved sample and leaves exports unchanged',()=>previewDisclosure.open && visible('type-realistic-sample') && w.getComputedStyle(d.querySelector('.type-sample-paragraph')).fontSize==='16px' && evaluate('cssExport()')===beforeCollapseCss);
  previewSummary.click();await wait();ui.show('context',false);await wait();
  test('Legacy inline-properties route opens the collapsed Learning preview',()=>previewDisclosure.open && visible('type-selected-text-details'));
  ui.show('fonts',false);ui.show('body',false);ui.show('hierarchy',false);
  test('Opening topics preserves other open control groups and both previews',()=>['fonts','body','hierarchy'].every(key=>get('type-stage-'+key).open) && visible('type-realistic-sample') && visible('typeLadder'));
  get('jSaveLocal').click();
  const baseline=evaluate('projectJson()'),css=evaluate('cssExport()'),html=evaluate('htmlExport()'),storage=w.localStorage.getItem('dss-v27-projects'),savedDoc=previewDoc(),savedHeading=previewWindow().getComputedStyle(savedDoc.querySelector('h1')).fontSize;
  draft('jBase',20);draft('jRatio',1.3);draft('jLeading',1.8);draft('jHeadingLeading',1.4);draft('advWeight',800,'change');draft('jHeadingTracking',.03);draft('jBodyTracking',.02);draft('advMeasure',55);draft('clampFactor',.75);await wait();
  test('Shared CSS and calculation follow unsaved base, ratio and fluid limits',()=>get('clampCss').textContent.includes('--text-h1:') && get('clampCss').textContent.includes('20px') && get('clampCss').textContent.includes('1.3^4') && get('clampMinFont').textContent==='42.84px' && get('clampMaxFont').textContent==='57.12px' && get('clampComputed').textContent===get('type-role-size').value && get('type-css-state').textContent.startsWith('Proposed CSS'));
  draft('clampMinWidth',400);draft('clampMaxWidth',1200);draft('clampViewport',600);await wait();
  test('Changing the preview viewport preserves proposed responsive controls and updates shared calculations',()=>get('clampMinWidth').value==='400' && get('clampMaxWidth').value==='1200' && get('clampFactor').value==='0.75' && get('clampMath').textContent.includes('1200') && get('clampExplanation').textContent.includes('At 600px') && get('clampComputed').textContent===get('type-role-size').value);
  test('Open lesson follows proposed values through limits, slope, offset and rem conversion',()=>calculationLesson.open && get('clampCalculationLimits').textContent.includes('1.3^4 = 57.122px') && get('clampCalculationSlope').textContent.includes('1.78506vw') && get('clampCalculationPreferred').textContent.includes('calc(2.23133rem + 1.78506vw)') && get('clampCalculationRem').textContent.includes('/ 16 =') && evaluate('projectJson()')===baseline);

  draft('clampMinWidth',375);draft('clampMaxWidth',1280);draft('clampViewport',768);await wait();
  const beforeCopyProject=evaluate('projectJson()'),copyWrites=[],originalClipboard=w.navigator.clipboard;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async value=>copyWrites.push(value)}});
  get('clampCopy').click();await wait();
  test('Common Copy CSS copies the current proposed rule without committing it',()=>copyWrites[0]===get('clampCss').textContent && get('clampCopyStatus').textContent==='CSS copied.' && evaluate('projectJson()')===beforeCopyProject);
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard});
  test('Combined Typography draft leaves project, exports and storage unchanged',()=>evaluate('projectJson()')===baseline && evaluate('cssExport()')===css && evaluate('htmlExport()')===html && w.localStorage.getItem('dss-v27-projects')===storage);
  test('Full website document and typography retain saved values during a draft',()=>previewDoc()===savedDoc && previewWindow().getComputedStyle(savedDoc.querySelector('h1')).fontSize===savedHeading);
  test('Draft body size, leading, tracking and measure reach the realistic sample immediately',()=>{const p=d.querySelector('.type-sample-paragraph'),s=w.getComputedStyle(p);return s.fontSize==='20px' && s.lineHeight==='36px' && s.letterSpacing==='0.4px' && p.style.maxWidth==='55ch';});
  test('Draft heading weight, rhythm and fluid scale reach sample and ladder immediately',()=>{const s=w.getComputedStyle(d.querySelector('.type-sample-heading')),ladder=rows().find(row=>row.dataset.typeLevel==='4').querySelector('.sample');return s.fontWeight==='800' && s.fontSize===w.getComputedStyle(ladder).fontSize && Math.abs(parseFloat(s.lineHeight)/parseFloat(s.fontSize)-1.4)<.01 && parseFloat(s.fontSize)>40;});
  test('Draft size ladder shows each computed PX and REM value',()=>rows().every(row=>{const n=Number(row.dataset.typeLevel),px=evaluate('fluidTypePx('+n+','+get('clampViewport').value+',DSStudio.propertyEditors.draftSnapshot("typography").state,DSStudio.propertyEditors.draftSnapshot("typography").clampConfig)');return row.querySelector('small').textContent.includes(px+'px') && Math.abs(parseFloat(w.getComputedStyle(row.querySelector('.sample')).fontSize)-px)<.01;}));
  test('Realistic sample contains every labelled typography level at its actual proposed size',()=>{
    const levels=[...get('type-realistic-sample').querySelectorAll('[data-sample-level]')];
    return levels.length===8 && new Set(levels.map(el=>el.dataset.sampleLevel)).size===8 && levels.every(el=>{const level=Number(el.dataset.sampleLevel),expected=evaluate('fluidTypePx('+level+','+get('clampViewport').value+',DSStudio.propertyEditors.draftSnapshot("typography").state,DSStudio.propertyEditors.draftSnapshot("typography").clampConfig)');return Math.abs(parseFloat(w.getComputedStyle(el).fontSize)-expected)<.01 && !!el.parentElement.querySelector('.type-sample-role') && el.getBoundingClientRect().height>0;});
  });
  for(const measure of [40,85]){
    draft('advMeasure',measure);await wait();
    test('Sample header fills the paper width at '+measure+'ch reading measure',()=>{const paper=get('type-realistic-sample'),nav=paper.querySelector('.type-sample-nav'),style=w.getComputedStyle(paper),expected=paper.clientWidth-parseFloat(style.paddingLeft)-parseFloat(style.paddingRight);return Math.abs(nav.getBoundingClientRect().width-expected)<1 && w.getComputedStyle(nav).maxWidth==='none';});
  }
  draft('advMeasure',55);
  test('Learning preview clearly identifies its proposed versus saved boundary',()=>get('type-specimen-meta').textContent.includes('Proposed typography') && get('type-specimen-meta').textContent.includes('saved values'));
  for(const group of d.querySelectorAll('[data-type-stage]'))group.open=false;await wait();
  test('Collapsing every control group retains both previews and all proposed values',()=>visible('type-realistic-sample') && visible('typeLadder') && visible('type-generated-css') && get('jBase').value==='20' && !bar().querySelector('button').disabled);
  discard();await wait();
  test('One Discard restores every Typography group and learning preview',()=>evaluate('projectJson()')===baseline && get('jBase').value==='16' && get('jRatio').value==='1.2' && get('advWeight').value==='700' && get('clampFactor').value==='0.82' && w.getComputedStyle(d.querySelector('.type-sample-paragraph')).fontSize==='16px' && bar().querySelector('button').disabled);
  test('Discard restores the common saved CSS and calculation alongside the preview',()=>get('type-css-state').textContent.startsWith('Saved CSS') && evaluate('cssExport()').includes(get('clampCss').textContent.split('\n').at(-1)) && get('clampComputed').textContent===get('type-role-size').value);
  draft('jBase',20);draft('jRatio',1.3);draft('jHeadingLeading',1.4);draft('advWeight',800,'change');draft('clampFactor',.75);save();await wait();
  test('One Save commits values across all Typography groups',()=>evaluate('state.base===20 && state.ratio===1.3 && state.headingLeading===1.4 && adv.weight===800 && clampConfig.mobileFactor===.75') && bar().querySelector('button').disabled);
  test('Unified Save updates actual website, exports and active local project',()=>evaluate('cssExport()')!==css && previewWindow().getComputedStyle(previewDoc().body).fontSize==='20px' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[get('jProjects').value].data.base===20 && get('type-specimen-meta').textContent.startsWith('Saved typography'));
  draft('jBase',21);input('jPrimary','#246789');discard();await wait();
  test('Typography Discard preserves a concurrent saved Palette change',()=>evaluate('state.base===20 && state.primary==="#246789"') && get('jBase').value==='20');
  draft('jBase',21);evaluate('state.base=18;apply()');await wait();
  test('Conflicting source changes invalidate obsolete Typography draft fields',()=>get('jBase').value==='18' && bar().querySelector('button').disabled);
  draft('jBase',21);evaluate('importConfig(JSON.parse(projectJson()))');await wait();
  test('Project replacement clears Typography drafts and comparisons',()=>get('jBase').value==='18' && bar().querySelector('button').disabled && get('type-preview-enlarge').value==='1');
  for(const [level,label]of [[5,'Display'],[4,'H1'],[3,'H2'],[2,'H3'],[1,'H4'],[0,'Body'],[-1,'Small'],[-2,'Extra small']]){
    get('clampRole').value=String(level);get('clampRole').focus();get('clampRole').dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
    test(label+' selection highlights exactly one ladder row and matching sample',()=>get('typeLadder').querySelectorAll('[aria-current="true"]').length===1 && rows().find(row=>row.dataset.typeLevel===String(level)).getAttribute('aria-current')==='true' && get('type-selected-level').textContent.includes(label) && d.activeElement===get('clampRole') && d.querySelectorAll('#type-realistic-sample [aria-current="true"]').length===1);
    test(label+' selection keeps all eight sample levels visible and highlights its exact example',()=>{
      const levels=[...get('type-realistic-sample').querySelectorAll('[data-sample-level]')],selected=get('type-realistic-sample').querySelector('[aria-current="true"]');
      return levels.length===8 && levels.every(el=>el.getBoundingClientRect().height>0) && selected.closest('[data-sample-level]')?.dataset.sampleLevel===String(level);
    });
    test(label+' common CSS uses the current exported size token',()=>evaluate('cssExport()').includes(get('clampCss').textContent.split('\n').at(-1)) && get('type-css-state').textContent.includes('for '+label+'.'));
    test(label+' lesson describes the actual fixed, constant or fluid exported rule',()=>{const fixed=[2,1,-2].includes(level),note=get('clampCalculationCase').textContent;return get('clampCalculationSteps').hidden===fixed && (fixed?note.includes('exports a fixed size:') && !get('clampCss').textContent.includes('clamp('):[0,-1].includes(level)?note.includes('Both limits are equal') && get('clampCalculationSlope').textContent.includes('0 px/px'):note.includes('Follow '+label));});

  }
  rows().find(row=>row.dataset.typeLevel==='4').click();draft('clampFactor',1);await wait();
  test('Equal heading limits explain how to enable fluid growth',()=>get('clampCalculationCase').textContent.includes('Lower Mobile heading size') && get('clampCalculationPreferred').textContent.includes('0vw'));
  discard();await wait();
  get('type-stage-hierarchy').open=false;rows().find(row=>row.dataset.typeLevel==='2').click();await wait();
  test('Picking a ladder row reveals its owning group without hiding either preview',()=>get('clampRole').value==='2' && get('type-stage-hierarchy').open && visible('type-realistic-sample') && visible('typeLadder'));
  rows().find(row=>row.dataset.typeLevel==='-1').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Enter',bubbles:true}));await wait();
  test('Ladder selection supports keyboard activation',()=>get('clampRole').value==='-1' && get('type-stage-body').open);
  d.querySelector('.type-sample-heading button').click();await wait();
  test('Picking realistic heading connects it to hierarchy settings',()=>get('type-stage-hierarchy').open && get('clampRole').value==='4');
  for(const level of [5,4,3,2,1,0,-1,-2]){
    const control=get('type-realistic-sample').querySelector('[data-sample-level="'+level+'"] button');control.click();await wait();
    test('Picking sample level '+level+' selects its matching hierarchy role',()=>get('clampRole').value===String(level) && control.getAttribute('aria-current')==='true');
    test('Inline computed details follow selected sample level '+level,()=>{const style=w.getComputedStyle(get('type-specimen-text'));return get('type-context-family').value===style.fontFamily && get('type-context-size').value===style.fontSize+' / '+style.lineHeight+' / '+style.fontWeight;});
  }
  const beforeButtonShortcut=evaluate('projectJson()');get('type-edit-button').click();await wait();
  test('Inline button shortcut opens the original Button typography control without changing project',()=>{const checks={adjacent:get('type-edit-button').parentElement.contains(d.querySelector('.type-sample-cta')),section:get('buttonDesignLab').open,focus:d.activeElement===get('bdWeight'),project:evaluate('projectJson()')===beforeButtonShortcut};if(!Object.values(checks).every(Boolean))throw Error(JSON.stringify({...checks,active:d.activeElement?.id,stage:w.DSStudio.activeStage}));return true;});
  w.dssShowWizardStep(5,false);await wait();
  for(const [fragment,target]of [['type-stage-review','type-selected-text-details'],['type-stage-context','type-selected-text-details'],['type-context-choice','type-content-choice']]){
    w.location.hash=fragment;await wait();
    test('Legacy '+fragment+' fragment reveals its inline replacement',()=>get('studio-section-2').open && visible(target) && d.activeElement===get(target));
  }
  w.location.hash='';await wait();
  const comparisonProject=evaluate('projectJson()'),comparisonCss=evaluate('cssExport()'),baseSize=parseFloat(w.getComputedStyle(d.querySelector('.type-sample-heading')).fontSize);
  get('type-preview-enlarge').value='2';get('type-preview-enlarge').dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('200 percent enlargement affects realistic sample and ladder without saving it',()=>Math.abs(parseFloat(w.getComputedStyle(d.querySelector('.type-sample-heading')).fontSize)-baseSize*2)<.01 && evaluate('projectJson()')===comparisonProject && evaluate('cssExport()')===comparisonCss);
  get('type-preview-spacing').click();await wait();
  test('User spacing comparison affects both learning previews without changing saved data',()=>{const sample=w.getComputedStyle(d.querySelector('.type-sample-paragraph')),ladder=w.getComputedStyle(rows()[0].querySelector('.sample'));return Math.abs(parseFloat(sample.letterSpacing)/parseFloat(sample.fontSize)-.12)<.001 && Math.abs(parseFloat(ladder.wordSpacing)/parseFloat(ladder.fontSize)-.16)<.001 && evaluate('projectJson()')===comparisonProject;});
  get('type-preview-enlarge').value='1';get('type-preview-enlarge').dispatchEvent(new w.Event('change',{bubbles:true}));get('type-preview-spacing').click();
  for(const id of ['jBase','jRatio','jHeadingTracking','clampMinWidth','fontGoogleHeading']){
    w.dssRevealSection(id,false);await wait();test('Configure route reveals original '+id+' control',()=>get(id).closest('[data-type-stage]').open && get('typography-workspace').contains(get(id)));
  }
  ui.show('rhythm',false);ui.show('context',false);await wait();
  test('Legacy topic aliases reveal hierarchy and inline text properties',()=>get('type-stage-hierarchy').open && visible('type-selected-text-details') && !get('type-stage-review'));
  reset();w.dssShowWizardStep(5,false);await wait();
  for(const wording of ['Learners <img src=x onerror="alert(1)"> & next steps','']){
    const fields=w.DSStudio.websiteContent.describe('id:hero-title','advanced').fields;
    const changes=fields.map(field=>({...field,value:wording}));
    w.__typeWording=w.DSStudio.websiteContent.merge('advanced',changes);
    evaluate('state.designProcess.websiteContent.advanced=window.__typeWording;apply()');await wait();
    test('Realistic sample and ladder preserve inert Architecture wording '+(wording?'with markup':'when blank'),()=>d.querySelector('.type-sample-heading').textContent===wording && !d.querySelector('.type-sample-heading img') && rows().filter(row=>Number(row.dataset.typeLevel)>0).every(row=>row.querySelector('.sample').textContent===wording));
  }
  reset();w.dssShowWizardStep(5,false);await wait();
  for(const mode of ['basic','advanced']){
    get(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    const source=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    test(mode+' realistic sample uses the real introduction rather than an earlier eyebrow label',()=>d.querySelector('.type-sample-paragraph').textContent===source.querySelector(mode==='basic'?'.hero .intro':'.sample-lead').textContent);
    test(mode+' sample card uses body copy rather than a category label',()=>d.querySelector('.type-sample-copy').textContent===source.querySelector('.card > p:not(.eyebrow):not(.sample-eyebrow)').textContent);
  }
  const resetBaseline=evaluate('projectJson()');
  draft('jBase',20);draft('jRatio',1.3);draft('jHeadingTracking',.03);draft('jBodyTracking',.02);draft('advWeight',800,'change');
  test('Named scale remains Custom for a proposed ratio across group navigation',()=>get('jScalePreset').value==='custom' && (ui.show('review',false),get('jRatio').value==='1.3'));
  get('type-reset-body').click();await wait();
  test('Body reset stages owned defaults and preserves heading proposals',()=>get('jBase').value==='16' && get('jBodyTracking').value==='0' && get('jHeadingTracking').value==='0.03' && get('advWeight').value==='800' && evaluate('projectJson()')===resetBaseline);
  get('type-reset-heading').click();await wait();
  test('Heading reset preserves the proposed ratio and project boundary',()=>get('jRatio').value==='1.3' && get('jHeadingTracking').value===String(evaluate('DEFAULT.headingTracking')) && get('advWeight').value===String(evaluate('ADV_DEFAULT.weight')) && evaluate('projectJson()')===resetBaseline);
  get('type-reset-hierarchy').click();await wait();
  test('Scale reset restores the named preset without saving',()=>get('jRatio').value==='1.2' && get('jScalePreset').value==='minor-third' && evaluate('projectJson()')===resetBaseline);
  discard();await wait();
  test('Default sample stays compact with H3 and H4 sharing one row',()=>{const paper=get('type-realistic-sample'),items=[...paper.querySelector('.type-sample-supporting').children];return paper.getBoundingClientRect().height<850 && Math.abs(items[0].getBoundingClientRect().top-items[1].getBoundingClientRect().top)<1;});
  let draftFontMode='ok';const head=d.head,append=head.append;
  head.append=function(...nodes){for(const link of nodes)if(link.tagName==='LINK' && link.href?.startsWith('https://fonts.')){link.href=link.rel==='stylesheet'?'/__font_fixture__'+new URL(link.href).search+'&mode='+draftFontMode:w.location.origin;}return append.apply(this,nodes);};
  const beforeFonts=evaluate('projectJson()'),beforeFontCss=evaluate('cssExport()');
  draft('fontSource','google','change');draft('fontGoogleBody','literata','change');await wait(400);
  test('Proposed curated font loads into a separate learning-preview stylesheet',()=>!!d.querySelector('[data-dss-learning-font][rel="stylesheet"]') && get('type-learning-font-status').textContent.includes('loaded') && w.getComputedStyle(d.querySelector('.type-sample-paragraph')).fontFamily.includes('Literata'));
  test('Draft font loading preserves saved links, website, storage model and exports',()=>!d.querySelector('[data-dss-font]') && !previewDoc().querySelector('[data-dss-font]') && evaluate('projectJson()')===beforeFonts && evaluate('cssExport()')===beforeFontCss && !previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Literata'));
  get('type-reset-fonts').click();await wait(250);
  test('Selected family reset uses the proposed Google source without committing',()=>get('fontSource').value==='google' && get('fontGoogleBody').value==='inter' && evaluate('projectJson()')===beforeFonts);
  const stale=d.querySelector('[data-dss-learning-font][rel="stylesheet"]').onload;discard();await wait();await stale();await wait();
  test('Discard removes proposed font connections and ignores late completion',()=>!d.querySelector('[data-dss-learning-font]') && get('fontSource').value==='system' && get('type-learning-font-status').textContent.includes('System fonts') && evaluate('projectJson()')===beforeFonts);
  draftFontMode='error';draft('fontSource','google','change');await wait(400);
  test('Failed proposed font loads show readable fallback and retry without a model write',()=>get('type-learning-font-status').textContent.includes('could not load') && w.getComputedStyle(d.querySelector('.type-sample-paragraph')).fontFamily.includes('Arial') && evaluate('projectJson()')===beforeFonts);
  discard();head.append=append;await wait();
  for(const theme of ['light','dark'])for(const width of [320,390,768,1440]){
    app.style.width=width+'px';evaluate("state.theme='"+theme+"';apply()");w.dssShowWizardStep(5,false);for(const group of d.querySelectorAll('[data-type-stage]'))group.open=true;await wait(200);
    test(theme+' '+width+'px unified sample and scale fit without page overflow',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && visible('type-realistic-sample') && visible('typeLadder'));
    test(theme+' '+width+'px unified controls and shared actions retain accessible target sizes',()=>[...get('typography-workspace').querySelectorAll('select,input:not([type=checkbox]),textarea,button')].filter(el=>el.getBoundingClientRect().width>0).every(el=>{const box=el.getBoundingClientRect();return box.height>=43.9 && box.left>=0 && (el.closest('.type-specimen-scroll') || box.right<=w.innerWidth+1); }));
  }
  draft('jBase',19);const beforePreview=evaluate('projectJson()'),previewCss=evaluate('cssExport()'),docBefore=previewDoc();bar().querySelector('[data-property-preview]').click();await wait();
  test('Shared saved-page preview retains Typography source, draft and keyboard focus',()=>get('studio-section-2').open && get('studio-section-4').open && d.activeElement===get('previewShell') && get('jBase').value==='19' && evaluate('projectJson()')===beforePreview && evaluate('cssExport()')===previewCss && previewDoc()===docBefore);
  test('No Typography JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Focused harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>
'''

if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
