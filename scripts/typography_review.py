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
  const input=(id,value,type='input')=>{const el=d.getElementById(id);w.DSStudio.paletteWorkspace?.revealControl(el);w.DSStudio.typographyWorkspace?.revealControl(el);el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));};
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
  d.getElementById('clampReset').click(); await wait();
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
  test('A shared heading/body family produces one family request per document', () => fontRequests.length===2 && fontRequests.every(href=>new URL(href).searchParams.getAll('family').length===1));
  input('fontGoogleHeading','literata','change'); await wait(250);
  test('Google heading/body selections update specimens, components and the preview', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Literata') && w.getComputedStyle(d.querySelector('#mobileType [data-font-role="body"]')).fontFamily.includes('Inter') && w.getComputedStyle(d.querySelector('.bd-button')).fontFamily.includes('Inter') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter'));
  const fontExport=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('HTML exports include deduplicated preconnects, crossorigin and the CSS2 font request', () => fontExport.querySelectorAll('link[rel="preconnect"]').length===2 && fontExport.querySelector('link[href="https://fonts.gstatic.com"]').hasAttribute('crossorigin') && fontExport.querySelector('link[href^="https://fonts.googleapis.com/css2?"]').getAttribute('href')===evaluate('DSStudio.fonts.url()') && evaluate('htmlExport()').includes('&amp;display=swap'));
  test('Font requests include selected families, page weights and italic body copy', () => {
    const request=new URL(evaluate('DSStudio.fonts.url()'));
    return request.searchParams.get('display')==='swap' && request.searchParams.getAll('family').join('|').includes('Inter:ital,wght@0,400;0,600;0,700;1,400') && request.searchParams.getAll('family').join('|').includes('Literata:wght@400;600;700');
  });
  d.getElementById('fontWeight500').click(); input('advWeight',800,'change'); input('bdWeight',700); await wait(250);
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
  input('fontSource','system','change'); await wait();
  test('Switching to system fonts removes all managed font connections and restores body controls', () => !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && !d.getElementById('font').disabled && !d.getElementById('jFont').disabled && !evaluate('htmlExport()').includes('fonts.googleapis.com'));
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
  // Typography fixtures start in desktop/light Studio, independent of Brief.
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();await wait();
  // Guided Typography reuses the shared model and actual website wording.
  {
    reset();w.dssShowWizardStep(5,false);await wait();const ui=w.DSStudio.typographyWorkspace,keys=['content','fonts','body','hierarchy','rhythm','responsive','context','review'],sample=()=>d.getElementById('type-specimen-text');
    test('Typography sidebar is a short process guide without saved-setting controls',()=>!d.querySelector('[data-journey-pane="5"] input,[data-journey-pane="5"] select') && d.querySelectorAll('[data-type-go]').length===8);
    test('Eight typography stages use Architecture-style browse and properties columns',()=>d.querySelectorAll('[data-type-stage]').length===8 && keys.every(key=>d.querySelector('#type-stage-'+key+' .type-browser') && d.querySelector('#type-stage-'+key+' .type-properties')) && d.querySelectorAll('.type-specimen').length===1);
    const original=evaluate('projectJson()');
    for(const key of keys){ui.show(key,false);await wait();test('Typography '+key+' shows its shared specimen above selected properties in one explained stage',()=>d.querySelectorAll('[data-type-stage][open]').length===1 && d.getElementById('type-stage-'+key).open && keys.filter(other=>other!==key).every(other=>d.getElementById('type-properties-'+other).getBoundingClientRect().height===0) && d.getElementById('type-properties-'+key).firstElementChild===d.querySelector('.type-specimen') && d.querySelector('.type-specimen').nextElementSibling===d.getElementById('type-properties-title-'+key) && d.querySelector('#type-browse-'+key+' .type-observe').textContent.length>20 && d.querySelector('[data-type-go="'+key+'"]').getAttribute('aria-current')==='step' && evaluate('projectJson()')===original);}
    ui.show('content',false);input('type-content-choice','headline','change');await wait();const site=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    test('Typography browses actual Architecture website wording rather than generic specimens',()=>sample().textContent===site.getElementById('hero-title').textContent && d.getElementById('type-content-text').value===sample().textContent && d.getElementById('type-content-text').readOnly && d.getElementById('type-content-tag').value==='h1' && parseFloat(sample().style.fontSize)===evaluate('fluidTypePx(4,Number(document.getElementById("clampViewport").value))'));
    ui.show('fonts',false);input('jFont',"Georgia, 'Times New Roman', serif");input('type-font-role','heading','change');input('fontSystemHeading','verdana','change');await wait();
    test('Selected font role exposes only its original editable family fields',()=>d.getElementById('jFont').closest('.field').hidden && !d.getElementById('fontSystemOptions').hidden && d.getElementById('type-properties-fonts').contains(d.getElementById('fontSystemHeading')) && evaluate('state.font').includes('Georgia') && evaluate('state.fontSettings.systemHeading')==='verdana');
    d.getElementById('type-reset-fonts').click();await wait();test('Resetting the heading family preserves the chosen body font',()=>evaluate('state.fontSettings.systemHeading')==='same' && evaluate('state.font').includes('Georgia'));
    input('jBase',20);input('jLeading',1.8);input('advMeasure',55);input('jPrimary','#246ABC');input('jHeadingTracking',.03);ui.show('body',false);d.getElementById('type-reset-body').click();await wait();
    test('Body readability reset preserves fonts, palette and heading rhythm',()=>evaluate('state.base===DEFAULT.base && state.leading===DEFAULT.leading && adv.measure===ADV_DEFAULT.measure') && evaluate('state.font').includes('Georgia') && evaluate('state.primary').toUpperCase()==='#246ABC' && evaluate('state.headingTracking')===.03);
    input('jBase',18);input('jScalePreset','major-third','change');input('clampRole','4','change');await wait();
    test('Hierarchy uses one editable scale and generated read-only sizes',()=>evaluate('state.ratio')===1.25 && d.getElementById('type-role-size').readOnly && d.getElementById('type-role-size').value===evaluate('fluidTypePx(4,Number(document.getElementById("clampViewport").value))')+'px' && d.getElementById('type-properties-hierarchy').contains(d.getElementById('jRatio')) && d.getElementById('type-browse-hierarchy').contains(d.getElementById('clampRole')) && d.getElementById('clampRole').getBoundingClientRect().height>=44);
    d.getElementById('type-reset-hierarchy').click();await wait();test('Scale reset preserves body size and the font family',()=>evaluate('state.ratio===DEFAULT.ratio && state.base===18') && evaluate('state.font').includes('Georgia'));
    input('jBodyTracking',.025);await wait();test('Body rhythm owns one em editor while heading settings stay hidden',()=>!d.getElementById('jBodyTracking').closest('.field').hidden && d.getElementById('jHeadingTracking').closest('.field').hidden && d.getElementById('type-rhythm-role').value==='body');d.getElementById('type-reset-rhythm').click();await wait();test('Body rhythm reset preserves heading tracking',()=>evaluate('state.bodyTracking===DEFAULT.bodyTracking && state.headingTracking===.03'));
    input('clampFactor',.7);input('clampViewport',390);await wait();test('Responsive stage keeps the original calculator and the shared specimen synchronized',()=>d.getElementById('type-stage-responsive').open && d.getElementById('clampComputed').textContent===sample().style.fontSize && d.getElementById('clampCss').textContent.includes('clamp(') && d.getElementById('type-properties-responsive').contains(d.getElementById('clampGraph')) && d.getElementById('type-browse-responsive').contains(d.getElementById('clampRole')) && ![...d.getElementById('clampGraph').parentElement.childNodes].some(node=>node.nodeType===w.Node.TEXT_NODE && node.textContent.trim()==='null'));
    d.getElementById('clampReset').click();await wait();test('Responsive reset preserves the selected type scale and rhythm',()=>evaluate('clampConfig.minWidth===CLAMP_DEFAULTS.minWidth && clampConfig.mobileFactor===CLAMP_DEFAULTS.mobileFactor && state.base===18 && state.headingTracking===.03'));
    ui.show('context',false);input('type-context-choice','button','change');await wait();
    test('Component context uses real action text and resolved live typography',()=>sample().textContent===previewDoc().querySelector('.ds-button').textContent.trim() && d.getElementById('type-context-family').value===previewWindow().getComputedStyle(previewDoc().querySelector('.ds-button')).fontFamily && d.getElementById('type-context-family').readOnly);
    ui.show('review',false);const beforeComparison=evaluate('projectJson()'),beforeSize=parseFloat(sample().style.fontSize);input('type-preview-enlarge','2','change');d.getElementById('type-preview-spacing').checked=true;d.getElementById('type-preview-spacing').dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
    test('Specimen enlargement and user-spacing overrides are comparison-only',()=>Math.abs(parseFloat(sample().style.fontSize)-beforeSize*2)<.1 && sample().style.letterSpacing==='0.12em' && sample().style.wordSpacing==='0.16em' && evaluate('projectJson()')===beforeComparison && d.querySelector('.type-specimen-scroll').tabIndex===0);
    const saved=JSON.parse(evaluate('projectJson()'));w.importConfig(saved);await wait();test('Import restores saved typography and clears specimen-only comparisons',()=>evaluate('state.base')===18 && evaluate('state.font').includes('Georgia') && d.getElementById('type-preview-enlarge').value==='1' && !d.getElementById('type-preview-spacing').checked && d.getElementById('type-stage-content').open);
    const beforeAlias=evaluate('projectJson()');input('clampBase',19);await wait();test('Hidden legacy aliases keep their existing model bindings and reveal the canonical editor',()=>evaluate('state.base')===19 && d.getElementById('jBase').value==='19' && d.getElementById('type-stage-body').open && d.getElementById('type-legacy-controls').contains(d.getElementById('clampBase')));
    w.dssConfigureToken({name:'--heading-letter-spacing',scope:'Light / base'});await wait();test('Configure links reach the owning Typography stage and visible original field',()=>w.DSStudio.activeStage===5 && d.getElementById('type-stage-rhythm').open && d.activeElement===d.getElementById('jHeadingTracking') && !d.getElementById('jHeadingTracking').closest('.field').hidden);
    const content=w.DSStudio.websiteContent,heading=w.DSStudio.contentArchitecture.nodes().find(node=>node.sourceKey==='id:hero-title'),mode=evaluate('state.sampleMode');const fields=content.describe(heading.sourceKey,mode).fields,next=content.merge(mode,fields.map(field=>({...field,value:'A safe <img src=x onerror=alert(1)> title'})));
    evaluate('state.designProcess.websiteContent['+JSON.stringify(mode)+']='+JSON.stringify(next)+';apply()');ui.show('content',false);input('type-content-choice','headline','change');await wait();test('Website text edits update Typography specimens as safe text',()=>sample().textContent==='A safe <img src=x onerror=alert(1)> title' && !sample().querySelector('img,script') && d.getElementById('type-content-text').value===sample().textContent);
    w.dssShowWizardStep(3,false);await wait();const opener=d.querySelector('#process-prototype > summary');opener.focus();const previewBefore=previewDoc();evaluate('state.base=20;apply()');await wait();test('Background typography changes preserve another lesson, preview document and focus',()=>w.DSStudio.activeStage===3 && d.activeElement===opener && previewDoc()===previewBefore && !d.getElementById('studio-section-2').open);
    w.dssShowWizardStep(5,false);await wait();
    for(const theme of ['light','dark'])for(const width of [320,390,1440]){app.style.width=width+'px';if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();await wait();for(const key of keys){ui.show(key,false);await wait();test(theme+' '+key+' Typography browse/properties fit '+width+'px',()=>{const grid=d.querySelector('#type-stage-'+key+' .type-editor-columns'),left=grid.children[0].getBoundingClientRect(),right=grid.children[1].getBoundingClientRect();if(d.documentElement.scrollWidth>w.innerWidth+1)throw Error('Page width '+d.documentElement.scrollWidth+' exceeds '+w.innerWidth);if(!(grid.clientWidth>720?Math.abs(left.top-right.top)<=1:right.top>=left.bottom-1))throw Error('Columns do not align: '+JSON.stringify({width:grid.clientWidth,left:left.toJSON(),right:right.toJSON()}));return [...grid.querySelectorAll('button,select,textarea,input')].filter(el=>el.getBoundingClientRect().height>0).every(el=>{const box=el.getBoundingClientRect();if(!(box.left>=0 && box.right<=w.innerWidth+1 && (el.type==='checkbox' || box.height>=44)))throw Error('Control '+el.id+' '+JSON.stringify(box.toJSON())+' in '+w.innerWidth);return true;});});}}
    for(const width of [320,1440]){app.style.width=width+'px';await wait();w.dispatchEvent(new w.Event('resize'));d.querySelector('[data-type-go="fonts"]').click();await wait();test(width+'px Typography stage navigation leaves its focused heading below the sticky header',()=>{const title=d.querySelector('#type-stage-fonts > summary'),header=d.querySelector('.topbar');return d.activeElement===title && title.getBoundingClientRect().top>=header.getBoundingClientRect().bottom-1;});}
    app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();await wait();
  }
  // End guided Typography checks.
  // Native Typography headers must retain a visible destination after sibling collapse.
  {
    reset();w.dssShowWizardStep(5,false);await wait();const ui=w.DSStudio.typographyWorkspace,keys=['content','fonts','body','hierarchy','rhythm','responsive','context','review'];
    for(const width of [320,1440]){app.style.width=width+'px';await wait();w.dispatchEvent(new w.Event('resize'));ui.show('content');await wait();const before=evaluate('projectJson()');
      for(const key of keys.slice(1)){const summary=d.querySelector('#type-stage-'+key+' > summary');summary.scrollIntoView({block:'center',behavior:'instant'});summary.focus({preventScroll:true});summary.click();await wait();test(width+'px opening Typography '+key+' directly keeps its heading visible',()=>{const box=summary.getBoundingClientRect(),header=d.querySelector('.topbar').getBoundingClientRect();return d.activeElement===summary && d.getElementById('type-stage-'+key).open && d.querySelectorAll('[data-type-stage][open]').length===1 && box.top>=header.bottom-1 && box.bottom<=w.innerHeight && evaluate('projectJson()')===before;});}
      const summary=d.querySelector('#type-stage-review > summary');summary.click();await wait();test(width+'px clicking an open Typography heading still collapses it',()=>!d.getElementById('type-stage-review').open);
    }
    app.style.width='1440px';reset();await wait();
  }
  // End native Typography header checks.

  // Typography is established from content before inspecting wireframe sizes.
  {
    reset();await wait();const ordered=[0,1,5,2,4,6,7,8,9,10,11,3];
    test('Course follows Brief, Architecture, Typography, Wireframe and Palette with stable route indices',()=>JSON.stringify(w.DSStudio.stageOrder)===JSON.stringify(ordered) && w.DSStudio.stages[5].id==='typography' && w.DSStudio.stages[2].id==='wireframe' && w.DSStudio.stages[4].id==='palette' && [5,2,4].every((index,position)=>w.DSStudio.stages[index].position===position+2));
    test('Planning phase is contiguous and contains the working typography baseline',()=>w.DSStudio.orderedStages.slice(0,4).every(stage=>stage.phase==='Plan') && [...d.querySelectorAll('.journey-phase')].map(el=>el.textContent).join('|')==='Plan|Foundations|Apply|Review and deliver');
    const original=evaluate('projectJson()');w.dssShowWizardStep(1,false);d.getElementById('jNext').click();await wait();
    test('Architecture Next opens Typography as Step 3',()=>w.DSStudio.activeStage===5 && d.getElementById('jProgress').textContent.includes('Step 3 of 12') && d.getElementById('studio-section-2').open && !d.querySelector('[data-journey-pane="5"]').hidden && d.getElementById('jNext').textContent==='Next: Wireframe' && evaluate('projectJson()')===original);
    d.getElementById('jBack').click();await wait();test('Typography Previous returns to Architecture',()=>w.DSStudio.activeStage===1 && d.getElementById('jNext').textContent==='Next: Typography' && evaluate('projectJson()')===original);
    d.getElementById('jNext').click();await wait();
    input('jFont',"Georgia, 'Times New Roman', serif",'input');input('jBase',18);input('jLeading',1.6);d.getElementById('advMeasure').closest('details').open=true;input('advMeasure',58);await wait();
    const edited=evaluate('projectJson()'),fontControl=d.getElementById('jFont');
    d.getElementById('jNext').click();await wait();
    test('Typography Next opens Wireframe as Step 4 without changing typography',()=>w.DSStudio.activeStage===2 && d.getElementById('jProgress').textContent.includes('Step 4 of 12') && d.getElementById('process-wireframe').open && d.getElementById('jNext').textContent==='Next: Palette' && evaluate('projectJson()')===edited);
    d.getElementById('jNext').click();await wait();test('Wireframe Next opens Palette as Step 5',()=>w.DSStudio.activeStage===4 && d.getElementById('jProgress').textContent.includes('Step 5 of 12') && d.getElementById('brandPalette').querySelector(':scope > summary h2').textContent==='Step 5 of 12: Palette' && evaluate('projectJson()')===edited);
    d.getElementById('jBack').click();await wait();test('Palette Previous returns to Wireframe',()=>w.DSStudio.activeStage===2 && evaluate('projectJson()')===edited);
    for(const mode of ['basic','advanced']){
      d.getElementById(mode==='basic'?'wf-basic':'wf-advanced').click();await wait();
      for(const theme of ['light','dark']){input('jTheme',theme);await wait();for(const fidelity of ['low','high']){
        w.DSStudio.wireframeView.setFidelity(fidelity);await wait();const doc=d.getElementById('wf-page').contentDocument,style=doc.defaultView.getComputedStyle(doc.body);
        test(mode+' '+theme+' '+fidelity+' wireframe uses the early typography baseline',()=>style.fontFamily.includes('Georgia') && style.fontSize==='18px' && Math.abs(parseFloat(style.lineHeight)-28.8)<.1 && doc.getElementById('wf-source-styles').textContent.includes('--reading-measure: 58ch') && evaluate('state.font').includes('Georgia') && evaluate('state.base')===18);
      }}
    }
    const saved=JSON.parse(evaluate('projectJson()'));w.importConfig(saved);await wait();w.dssShowWizardStep(5,false);await wait();
    test('Project round trip retains typography values and original control identity at the new visible step',()=>d.getElementById('jFont')===fontControl && fontControl.value.includes('Georgia') && d.getElementById('jBase').value==='18' && d.getElementById('jLeading').value==='1.6' && d.getElementById('advMeasure').value==='58' && d.getElementById('jProgress').textContent.includes('Step 3 of 12'));
    input('tokenSearch','--font-size-base');await wait();test('Typography token source metadata uses visible Step 3',()=>[...d.querySelectorAll('#tokenTableBody tr')].find(row=>row.querySelector('td:nth-child(2) code')?.textContent==='--font-size-base').textContent.includes('wizard step 3'));
    w.dssConfigureToken({name:'--font-size-base',scope:'Light / base'});await wait();test('Existing typography Configure route reaches its original control',()=>w.DSStudio.activeStage===5 && d.activeElement===d.getElementById('jBase'));
    for(const width of [320,1440]){
      app.style.width=width+'px';await wait();w.dssShowWizardStep(0,false);await wait();const before=evaluate('projectJson()');
      for(const [position,index]of ordered.entries()){if(position)d.getElementById('jNext').click();await wait();test(width+'px Next follows reordered '+(position+1)+' '+w.DSStudio.stages[index].label,()=>w.DSStudio.activeStage===index && d.getElementById('jProgress').textContent.startsWith('Step '+(position+1)+' of 12') && evaluate('projectJson()')===before);}
    }
    app.style.width='1440px';w.DSStudio.wireframeView.setFidelity('high');reset();await wait();
  }
  // End early typography checks.
  test('No typography JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Focused harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
