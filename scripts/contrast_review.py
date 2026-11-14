"""Independent contrast browser checks using the shared local Chrome runner.

Run: python scripts/contrast_review.py. Owns its app/profile and fixtures; does not
import or patch the integration harness. No runtime dependency is introduced.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Contrast review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Contrast: '+results.length+' checks; last: '+name;
  };
  const wait=(ms=100)=>new Promise(resolve=>setTimeout(resolve,ms));
  const reset=()=>{evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc=()=>d.getElementById('previewPage').contentDocument;
  const previewWindow=()=>d.getElementById('previewPage').contentWindow;
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
  try {
  test('Independent contrast startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(10,false);await wait();
  test('Known contrast ratios', () => evaluate("contrast('#000000','#FFFFFF')===21 && contrast('#FFFFFF','#FFFFFF')===1"));
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(10,false);await wait();
  const report = () => w.dssGetContrastChecks();
  test('Contrast report covers both themes without changing the active theme', () => {
    return new Set(report().map(row=>row.theme)).size===2 && d.documentElement.dataset.theme==='light' && evaluate('state.theme')==='light';
  });
  test('Every button variant and state is represented in both themes', () => {
    return ['light','dark'].every(theme=>['primary','secondary','accent','outline','text'].every(variant=>
      ['default','hover','focus','active','selected','disabled','loading'].every(state=>report().some(row=>
        row.group==='Button Laboratory: text' && row.theme===theme && row.name.toLowerCase()===variant && row.state===state))));
  });
  test('Reference swatches and every generated ramp step have candidate checks', () => {
    const rows=report().filter(row=>row.scope==='candidate');
    return rows.length===(11+44)*2*2 && rows.every(row=>row.status==='candidate');
  });
  test('Disabled controls are exempt and read-only text is tested', () => report().filter(row=>row.state==='disabled').every(row=>row.status==='exempt') &&
    report().some(row=>row.name==='State Explorer input text' && row.state==='readonly' && row.threshold===4.5));
  test('Loading exemption follows the actual disabled state', () => {
    const rows=report().filter(row=>row.state==='loading');
    return rows.filter(row=>row.group==='Button Laboratory: text').every(row=>row.threshold===4.5) &&
      rows.filter(row=>row.name==='State Explorer button text').every(row=>row.status==='exempt');
  });
  test('Focus indicators have a separate non-text target', () => report().some(row=>row.name==='Primary focus ring' && row.threshold===3 && row.state==='focus'));
  const oldForeground=report().find(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light').fg;
  input('bdVariant','primary'); input('bdHoverText','#123456'); await wait();
  test('Button override updates the contrast inventory', () => report().some(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light' && row.fg==='#123456' && row.fg!==oldForeground));
  input('bdDefaultBg','#ffffff'); input('bdText','#ffffff'); await wait();
  test('White text on white is flagged at exactly 1:1', () => report().some(row=>row.name==='Primary' && row.state==='default' && row.ratio===1 && row.status==='review'));
  input('bdDefaultBg','#ffffff'); input('bdText','#777777'); await wait();
  test('A ratio below 4.5 is not rounded into a text pass', () => report().some(row=>row.name==='Primary' && row.state==='default' && row.ratio>4.4 && row.ratio<4.5 && row.status==='review'));
  input('bdDefaultBg','#000000'); input('bdText','#ffffff'); await wait();
  test('Disabled opacity uses unrounded sRGB compositing', () => {
    const row=report().find(row=>row.name==='Primary' && row.theme==='light' && row.state==='disabled' && row.location==='surface');
    const expected=1.05/(Math.pow((.45+.055)/1.055,2.4)+.05);
    return Math.abs(row.ratio-expected)<1e-10 && row.status==='exempt';
  });
  const beforeOpacity=report().find(row=>row.name==='Preview card: --text' && row.theme==='light').ratio;
  input('advOpacity',20); await wait();
  test('Surface opacity updates the composited contrast', () => report().find(row=>row.name==='Preview card: --text' && row.theme==='light').ratio<beforeOpacity);
  input('advColor_danger','#abcdef'); await wait();
  test('Feedback changes update invalid-state checks', () => report().some(row=>row.name==='State Explorer input border' && row.theme==='light' && row.state==='invalid' && row.fg==='#ABCDEF'));
  input('contrastTheme','dark','change'); input('contrastResult','review','change');
  test('Contrast theme and result filters apply together', () => {
    const shown=[...d.querySelectorAll('#contrastChecks tbody tr')];
    return shown.length>0 && shown.every(row=>row.dataset.status==='review' && row.cells[0].textContent==='Dark');
  });
  input('contrastTheme','all','change'); input('contrastResult','all','change'); input('contrastSort','ratio','change');
  test('Ratios sort ascending within each result group', () => [...d.querySelectorAll('#contrastChecks tbody')].every(body=>{
    const values=[...body.rows].map(row=>parseFloat(row.cells[3].textContent));return values.every((value,i)=>!i||value>=values[i-1]);
  }));
  input('contrastSearch','Primary focus ring');
  test('Search narrows the displayed contrast pairs', () => {
    const shown=[...d.querySelectorAll('#contrastChecks tbody tr')];
    return shown.length>0 && shown.every(row=>row.cells[1].textContent.includes('Primary focus ring'));
  });
  const realDownload=w.download; let contrastCsv;
  w.download=(name,content)=>{contrastCsv={name,content};};
  d.getElementById('contrastDownload').click(); w.download=realDownload;
  test('Contrast CSV exports the currently filtered list', () => contrastCsv.name==='contrast-checks.csv' && contrastCsv.content.includes('Primary focus ring') && !contrastCsv.content.includes('Swatch candidates:'));
  input('contrastSearch',''); input('contrastSort','priority','change');
  test('Default sorting puts review rows before passes within groups', () => [...d.querySelectorAll('#contrastChecks tbody')].every(body=>{
    const ranks={review:0,conditional:1,pass:2,candidate:3,exempt:4};const values=[...body.rows].map(row=>ranks[row.dataset.status]);
    return values.every((value,i)=>!i||value>=values[i-1]);
  }));
  app.style.width='320px';
  d.querySelector('#contrastChecks .contrast-group summary').click(); await wait();
  test('Expanded contrast table scrolls within a 320px page', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  test('Contrast report ratios are finite and between 1 and 21', () => report().every(row=>Number.isFinite(row.ratio) && row.ratio>=1 && row.ratio<=21));
  reset(); await wait();
  test('Optional feedback text is a potential use, not a required failure', () => report().filter(row=>row.name.includes('message text')).every(row=>row.scope==='potential' && row.status==='candidate'));
  test('Button boundaries and extra inner ring checks are conditional', () => report().filter(row=>row.group==='Button Laboratory: indicators' && (row.name.includes('boundary') || row.name.includes('(inner)'))).every(row=>row.status==='conditional'));
  test('Actual input boundaries remain required checks', () => report().some(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light' && row.status==='review'));
  const openRepair = predicate => {
    const row=report().find(predicate);
    const action=[...d.querySelectorAll('[data-edit-contrast]')].find(el=>el.dataset.editContrast===row.id);
    action.closest('details').open=true; action.click(); return row;
  };
  d.getElementById('jSaveLocal').click();
  const beforeRepair=evaluate('projectJson()'), beforeRepairCss=evaluate('cssExport()'), beforeRepairStorage=w.localStorage.getItem('dss-v27-projects');
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light');
  test('Edit action opens the relevant control-border editor', () => d.getElementById('colourRepair').open && d.getElementById('repairTarget').selectedOptions[0].textContent.includes('--control-border'));
  test('Repair provides three tested colour suggestions', () => d.querySelectorAll('[data-suggest-colour]').length===3);
  d.querySelector('[data-suggest-colour]').click();
  test('Suggestion preview does not mutate state, CSS or saved projects', () => evaluate('projectJson()')===beforeRepair && evaluate('cssExport()')===beforeRepairCss && w.localStorage.getItem('dss-v27-projects')===beforeRepairStorage);
  test('Preview explains effects on related pairs', () => d.getElementById('repairPreview').textContent.includes('required problems introduced') && d.getElementById('repairPreview').textContent.includes('All worsened pairs'));
  input('repairHex','#oops');
  test('Invalid HEX disables Apply', () => d.getElementById('repairApply').disabled);
  d.getElementById('repairCancel').click(); await wait();
  test('Cancel leaves the project unchanged', () => !d.getElementById('colourRepair').open && evaluate('projectJson()')===beforeRepair);
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light');
  input('repairHex','#7B8A9B');
  test('Border preview predicts seven required pairs resolved', () => d.getElementById('repairPreview').textContent.includes('7 required problems resolved; 0 required problems introduced'));
  d.getElementById('repairApply').click(); await wait();
  test('Apply changes control borders without changing decorative borders', () => evaluate("palette('light').roles['control-border']==='#7B8A9B' && palette('light').roles.border==='#C5D0DD'"));
  test('Applied border is used by actual input styling', () => w.getComputedStyle(d.getElementById('demoEmail')).borderTopColor==='rgb(123, 138, 155)');
  test('Editing light theme leaves dark theme unchanged', () => evaluate("palette('dark').roles['control-border']==='#60748D'"));
  test('Applied semantic colour updates CSS and active local save', () => evaluate('cssExport()').includes('--control-border: #7B8A9B') && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.semanticOverrides?.light?.['control-border']==='#7B8A9B'));
  const repaired=evaluate('projectJson()');
  reset(); evaluate('importConfig('+repaired+')'); await wait();
  test('Semantic overrides survive JSON round trip', () => evaluate("palette('light').roles['control-border']==='#7B8A9B'"));
  input('semanticTheme','light','change'); input('semanticRole','control-border','change');
  d.getElementById('semanticReset').click(); await wait();
  test('Use generated colour restores the role fallback', () => evaluate("palette('light').roles['control-border']===palette('light').roles.border"));
  input('semanticRole','text','change'); d.getElementById('semanticEdit').click(); input('repairHex','#ffffff');
  test('Harmful preview exposes newly failing related pairs', () => /[1-9]\d* required problems introduced/.test(d.getElementById('repairPreview').textContent) && d.getElementById('repairPreview').querySelector('details').open);
  d.getElementById('repairCancel').click(); await wait();
  input('semanticRole','success','change'); d.getElementById('semanticEdit').click();
  input('repairHex','#137A39'); d.getElementById('repairApply').click(); await wait();
  test('Semantic editor synchronizes existing feedback controls', () => d.getElementById('advColor_success').value==='#137a39' && evaluate("palette('light').roles.success==='#137A39'"));
  input('advColor_success','#126b34'); await wait();
  test('Existing feedback control can replace an editor override', () => evaluate("palette('light').roles.success==='#126B34' && !state.semanticOverrides.light.success"));
  input('semanticTheme','dark','change'); input('semanticRole','text','change'); d.getElementById('semanticEdit').click();
  input('repairHex','#DDEEFF'); d.getElementById('repairApply').click(); await wait();
  test('Dark theme editing preserves light theme and current theme selection', () => evaluate("palette('dark').roles.text==='#DDEEFF' && palette('light').roles.text==='#14253A' && state.theme==='light'"));
  test('Dark override is exported in the dark block only', () => {
    const css=evaluate('cssExport()'), dark=css.indexOf('[data-theme="dark"]');
    return !css.slice(0,dark).includes('--text: #DDEEFF') && css.slice(dark).includes('--text: #DDEEFF');
  });
  openRepair(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light');
  input('repairHex','#123456'); d.getElementById('repairApply').click(); await wait();
  test('Button repair reaches the selected state in both themes', () => ['light','dark'].every(theme=>report().some(row=>row.name==='Primary' && row.state==='hover' && row.theme===theme && row.fg==='#123456')));
  openRepair(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light');
  input('repairHex','#ffffff'); input('jBase',18); await wait();
  d.getElementById('repairApply').click();
  test('Stale previews require a renewed review before Apply', () => d.getElementById('colourRepair').open && d.getElementById('repairNotice').textContent.includes('project changed') && evaluate('state.buttonDesign.overrides.primary.hoverText')==='#123456');
  d.getElementById('repairCancel').click(); await wait();
  app.style.width='320px';
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light'); await wait();
  test('Colour repair dialog fits a 320px viewport', () => d.getElementById('colourRepair').getBoundingClientRect().width<=w.innerWidth && d.getElementById('colourRepair').scrollWidth<=d.getElementById('colourRepair').clientWidth+1);
  d.getElementById('repairCancel').click(); await wait();
  evaluate('importConfig({semanticOverrides:{light:{text:"red;position:fixed",unknown:"#000000"},dark:{text:"#abcdef"}}})'); await wait();
  test('Semantic imports reject unknown roles and malformed colours', () => evaluate("!state.semanticOverrides.light.text && !state.semanticOverrides.light.unknown && palette('dark').roles.text==='#ABCDEF'"));
  reset(); await wait();
  test('Reset removes semantic overrides', () => evaluate("!state.semanticOverrides && palette('light').roles['control-border']===palette('light').roles.border"));
  d.querySelector('[data-journey-step="6"]').click(); await wait();
  w.dssRevealSection('jSemanticRole',false);
  test('Palette exposes every semantic role with a friendly label and token', () => {
    const roles=evaluate('SEMANTIC_COLOUR_KEYS');
    return d.getElementById('palette-stage-semantics').open && roles.length===d.getElementById('jSemanticRole').options.length && roles.every(key=>[...d.getElementById('jSemanticRole').options].some(option=>option.value===key && option.textContent.includes('--'+key)));
  });
  d.getElementById('jSaveLocal').click();
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('jSemanticRole','text','change'); await wait();
    const beforeGuided=evaluate('projectJson()');
    test(theme+' wizard shows the current semantic value, purpose and generated status', () => d.getElementById('jSemanticCurrent').textContent.includes(evaluate(`palette('${theme}').roles.text`)) && d.getElementById('jSemanticCurrent').textContent.startsWith(theme==='dark'?'Dark:':'Light:') && d.getElementById('jSemanticReset').disabled && d.getElementById('jSemanticHelp').textContent.includes('Default readable text'));
    d.getElementById('jSemanticEdit').focus(); d.getElementById('jSemanticEdit').click();
    input('repairHex',theme==='light'?'#14253A':'#DDEEFF');
    test(theme+' guided semantic edit previews without mutating the project', () => d.getElementById('colourRepair').open && d.getElementById('repairScope').textContent.includes('the '+theme+' theme only') && evaluate('projectJson()')===beforeGuided);
    d.getElementById('repairCancel').click(); await wait();
    test(theme+' cancelling guided semantic edits returns focus and preserves colours', () => evaluate('projectJson()')===beforeGuided && d.activeElement===d.getElementById('jSemanticEdit'));
    d.getElementById('jSemanticEdit').click(); input('repairHex',theme==='light'?'#14253A':'#DDEEFF');
    d.getElementById('repairApply').click(); await wait();
    const expected=theme==='light'?'#14253A':'#DDEEFF';
    test(theme+' guided override updates the preview, export and active local save', () => evaluate(`palette('${theme}').roles.text==='${expected}'`) && previewWindow().getComputedStyle(previewDoc().body).color===(theme==='light'?'rgb(20, 37, 58)':'rgb(221, 238, 255)') && evaluate('cssExport()').includes('--text: '+expected) && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data.semanticOverrides[theme].text===expected && d.getElementById('jSemanticCurrent').textContent.includes('custom override') && !d.getElementById('jSemanticReset').disabled);
    input('semanticTheme',theme,'change'); input('semanticRole','text','change');
    test(theme+' centre and guided editors show the same semantic override', () => d.getElementById('semanticCurrent').textContent.includes(expected));
  }
  const guidedJson=evaluate('projectJson()'); evaluate('importConfig('+guidedJson+')'); await wait();
  test('Guided semantic overrides survive project JSON import', () => evaluate("state.semanticOverrides.light.text==='#14253A' && state.semanticOverrides.dark.text==='#DDEEFF'") && d.getElementById('jSemanticCurrent').textContent.includes('#DDEEFF'));
  d.getElementById('jSemanticReset').click(); await wait();
  test('Guided reset restores just the selected theme and role', () => evaluate("!state.semanticOverrides.dark.text && state.semanticOverrides.light.text==='#14253A'") && d.getElementById('jSemanticReset').disabled && !d.getElementById('semanticCurrent').textContent.includes('custom override'));
  app.style.width='320px'; await wait();
  test('Guided semantic controls fit the narrow studio layout', () => {
    w.DSStudio.paletteWorkspace.revealControl(d.getElementById('jSemanticEdit'));const pane=d.getElementById('palette-stage-semantics');
    return pane.scrollWidth<=pane.clientWidth+1 && d.getElementById('jSemanticEdit').getBoundingClientRect().width>0 && d.documentElement.scrollWidth<=320;
  });
  app.style.width='1440px'; reset(); await wait();
  test('Project reset refreshes guided semantic values', () => d.getElementById('jSemanticCurrent').textContent.startsWith('Light:') && d.getElementById('jSemanticReset').disabled && !evaluate('state.semanticOverrides'));
  d.querySelector('[data-journey-step="7"]').click(); await wait();
  d.getElementById('bdReview').open=true;
  d.getElementById('jSaveLocal').click();
  const reviewButton = (variant, state) => d.querySelector(`[data-review-variant="${variant}"][data-review-state="${state}"]`);
  const reviewCell = (variant, state, theme) => reviewButton(variant,state).closest('tr').querySelector(`[data-review-theme="${theme}"]`);
  const reviewPair = (theme, kind) => d.querySelector(`#bdReviewPairs [aria-label="${theme} theme contrast"] [data-kind="${kind}"]`);
  const selectReview = (variant, state) => {
    const button=reviewButton(variant,state);
    button.closest('details').open=true; button.focus(); button.click();
  };
  test('Guided button review includes all 35 states and 70 theme results', () =>
    d.querySelectorAll('#bdReviewVariants details').length===5 &&
    d.querySelectorAll('#bdReviewVariants tbody tr').length===35 &&
    d.querySelectorAll('#bdReviewVariants td[data-result]').length===70 &&
    d.getElementById('bdReviewSummary').textContent.includes('10 disabled exemptions'));
  test('Every guided result agrees with the full contrast inventory', () => {
    return ['Primary','Secondary','Accent','Outline','Text'].every(variant=>
      ['default','hover','focus','active','selected','disabled','loading'].every(state=>
        ['light','dark'].every(theme=>{
          const rows=report().filter(row=>row.group.startsWith('Button Laboratory:') && row.name.split(' ')[0]===variant && row.state===state && row.theme===theme && row.scope==='required' && row.threshold!==null);
          const expected=state==='disabled'?'exempt':rows.some(row=>row.ratio<row.threshold)?'review':'pass';
          return reviewCell(variant.toLowerCase(),state,theme).dataset.result===expected;
        })));
  });
  const beforeReviewCss=evaluate('cssExport()');
  const beforeReviewColours=evaluate('JSON.stringify([state.buttonDesign.overrides,state.buttonDesign.custom,state.buttonDesign.sources])');
  selectReview('secondary','hover'); await wait();
  test('Selecting a reviewed state synchronizes the wizard and live specimen', () => d.getElementById('bdVariant').value==='secondary' && d.getElementById('bdState').value==='hover' && d.querySelector('#bdSingle .bd-button').textContent.includes('Secondary') && d.getElementById('bdReviewTitle').textContent.includes('Secondary'));
  test('Review navigation preserves colours and component CSS', () => evaluate('cssExport()')===beforeReviewCss && evaluate('JSON.stringify([state.buttonDesign.overrides,state.buttonDesign.custom,state.buttonDesign.sources])')===beforeReviewColours);
  test('Review selection has one accessible current-state marker', () => d.querySelectorAll('#bdReviewVariants [aria-current="true"]').length===1 && reviewButton('secondary','hover').getAttribute('aria-current')==='true' && reviewButton('secondary','hover').getAttribute('aria-controls')==='bdReviewSelection');
  const stableReviewButton=reviewButton('secondary','hover');
  const stableReviewDetails=stableReviewButton.closest('details');
  input('bdHover','#ffffff'); input('bdHoverText','#ffffff'); await wait();
  test('Poor state overrides flag both themes and show their exact text ratio', () => ['light','dark'].every(theme=>reviewCell('secondary','hover',theme).dataset.result==='review') && ['Light','Dark'].every(theme=>reviewPair(theme,'text').textContent.includes('1.000:1')));
  test('Live contrast refresh preserves review focus and disclosure state', () => reviewButton('secondary','hover')===stableReviewButton && d.activeElement===stableReviewButton && stableReviewDetails.open);
  const beforeWizardRepair=evaluate('projectJson()');
  const wizardRepairButton=reviewPair('Light','text').querySelector('button');
  wizardRepairButton.focus(); wizardRepairButton.click(); input('repairHex','#101820');
  test('Wizard colour repair previews effects across both themes without committing', () => d.getElementById('colourRepair').open && d.getElementById('repairTarget').selectedOptions[0].textContent.includes('Secondary: hoverText') && evaluate('projectJson()')===beforeWizardRepair);
  d.getElementById('repairCancel').click(); await wait();
  test('Cancel returns focus to the wizard edit action and keeps the failing colour', () => d.activeElement===wizardRepairButton && evaluate('projectJson()')===beforeWizardRepair && reviewCell('secondary','hover','light').dataset.result==='review');
  wizardRepairButton.click(); input('repairHex','#101820');
  const wizardRepairClosed=new Promise(resolve=>d.getElementById('colourRepair').addEventListener('close',resolve,{once:true}));
  d.getElementById('repairApply').click(); await Promise.race([wizardRepairClosed,wait(1000)]); await wait();
  test('Applying a reviewed text fix updates both theme results and returns focus', () => {
    const themes=['light','dark'].map(theme=>reviewCell('secondary','hover',theme).dataset.result), colour=evaluate('state.buttonDesign.overrides.secondary.hoverText');
    if(themes.every(result=>result==='pass') && colour==='#101820' && d.activeElement===wizardRepairButton) return true;
    throw Error(JSON.stringify({themes,colour,active:d.activeElement.outerHTML.slice(0,300),dialogOpen:d.getElementById('colourRepair').open}));
  });
  test('Wizard fixes reach the live CSS/HTML preview and project save', () => previewDoc().getElementById('dssPreviewStyles').textContent.includes('--button-secondary-hover-text: #101820') &&
    previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--secondary')).getPropertyValue('--button-secondary-hover-text').trim()==='#101820' &&
    Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.buttonDesign?.overrides.secondary?.hoverText==='#101820'));
  const wizardRepaired=evaluate('projectJson()'); reset(); evaluate('importConfig('+wizardRepaired+')'); await wait();
  test('Saved button fixes and selected review state survive JSON round trip', () => reviewButton('secondary','hover').getAttribute('aria-current')==='true' && ['light','dark'].every(theme=>reviewCell('secondary','hover',theme).dataset.result==='pass') && d.getElementById('bdHoverText').value==='#101820');
  input('bdDefaultBg','#777777'); input('bdText','#000000'); selectReview('secondary','loading'); await wait();
  test('Loading review retains full opacity and the default text contrast', () => reviewCell('secondary','default','light').dataset.result==='pass' && reviewCell('secondary','loading','light').dataset.result==='pass' && w.getComputedStyle(d.querySelector('#bdMatrix [data-sim="loading"]')).opacity==='1' && report().filter(row=>row.name==='Secondary' && row.state==='loading').every(row=>row.ratio===report().find(other=>other.name===row.name && other.theme===row.theme && other.location===row.location && other.state==='default').ratio));
  selectReview('secondary','disabled'); await wait();
  test('Disabled states show informational ratios and an exemption in both themes', () => ['light','dark'].every(theme=>reviewCell('secondary','disabled',theme).dataset.result==='exempt') && ['Light','Dark'].every(theme=>reviewPair(theme,'text').textContent.includes('Exempt (no target)')) && !d.getElementById('bdContrast').textContent.includes('Pass'));
  input('bdDefaultBg','#000000'); input('bdText','#ffffff'); input('bdFocus','#ffffff'); selectReview('secondary','focus'); await wait();
  test('Focus review catches a failing ring even when its text passes', () => reviewPair('Light','text').dataset.result==='pass' && reviewPair('Light','focus').dataset.result==='review' && reviewCell('secondary','focus','light').dataset.result==='review' && reviewCell('secondary','focus','dark').dataset.result==='pass');
  const ringEdit=reviewPair('Light','focus').querySelector('button'); ringEdit.focus(); ringEdit.click(); input('repairHex','#808080'); d.getElementById('repairApply').click(); await wait();
  test('Ring editing uses the shared focus setting across every variant and theme', () => report().filter(row=>row.group==='Button Laboratory: indicators' && row.name.includes('focus ring')).every(row=>row.fg==='#808080') && evaluate('state.buttonDesign.focus')==='#808080');
  selectReview('secondary','selected'); await wait();
  test('Selection reviews expose required outer and conditional inner indicators separately', () => !reviewPair('Light','selection').hidden && reviewPair('Light','inner').dataset.result==='conditional' && reviewPair('Light','inner').textContent.includes('Conditional'));
  selectReview('secondary','default'); await wait();
  test('Conditional button boundaries do not turn readable labels into required failures', () => reviewPair('Light','boundary').dataset.result==='conditional' && reviewCell('secondary','default','light').dataset.result==='pass');
  input('bdVariant','outline'); input('bdState','active'); await wait();
  test('Existing variant and state selectors update the contrast review selection', () => reviewButton('outline','active').getAttribute('aria-current')==='true' && d.getElementById('bdReviewTitle').textContent.includes('Outline'));
  const validReview=evaluate('projectJson()');
  evaluate('dssSelectButtonState("__proto__","default"); dssSelectButtonState("primary","bad-state")'); await wait();
  test('Review navigation rejects unknown variants and states', () => evaluate('projectJson()')===validReview);
  for (const theme of ['light','dark']) {
    input('jTheme',theme); app.style.width='320px';
    d.querySelectorAll('#bdReviewVariants details').forEach(el=>el.open=true); await wait();
    test('All guided button reviews fit the '+theme+' 320px layout', () => [...d.querySelectorAll('.bd-review-table,.bd-review-selection')].every(el=>el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1) &&
      [...d.querySelectorAll('#bdReviewVariants button')].every(el=>el.getBoundingClientRect().height>=40 && el.tabIndex===0));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset clears repaired button colours and refreshes the selected review', () => evaluate('!Object.keys(state.buttonDesign.overrides).length') && reviewButton('primary','default').getAttribute('aria-current')==='true');
  test('New default button colours meet required text and indicator targets in all states and themes', () => report().filter(row=>row.group.startsWith('Button Laboratory:') && row.scope==='required' && row.threshold!==null).every(row=>row.status==='pass'));

  // A native close event may arrive after the user has already reopened the dialog.
  app.style.width='1440px';reset();w.dssShowWizardStep(4,false);w.DSStudio.paletteWorkspace.show('semantics',false);await wait();
  input('jSemanticRole','text','change');d.getElementById('jSemanticEdit').focus();d.getElementById('jSemanticEdit').click();
  d.getElementById('repairCancel').click();
  input('jSemanticRole','control-border','change');d.getElementById('jSemanticEdit').focus();d.getElementById('jSemanticEdit').click();
  const repairDialog=d.getElementById('colourRepair'),beforeLateClose=evaluate('projectJson()'),beforeText=evaluate('palette().roles.text'),beforeErrors=w.__reviewErrors.length;
  repairDialog.dispatchEvent(new w.Event('close'));
  input('repairHex','#7B8A9B');
  test('Late close from a cancelled repair preserves the reopened editor and its draft',()=>repairDialog.open && d.activeElement===d.getElementById('repairHex') && d.getElementById('repairScope').textContent.includes('--control-border') && evaluate('projectJson()')===beforeLateClose && w.__reviewErrors.length===beforeErrors);
  d.getElementById('repairApply').click();await wait();
  test('Reopened repair applies only its current target after a delayed close event',()=>!repairDialog.open && evaluate('state.semanticOverrides?.light?.["control-border"]')==='#7B8A9B' && evaluate('palette().roles.text')===beforeText && d.activeElement===d.getElementById('jSemanticEdit'));
  if(repairDialog.open)repairDialog.close();await wait();
  const afterRepair=evaluate('projectJson()'),afterRepairErrors=w.__reviewErrors.length;
  d.getElementById('repairApply').click();await wait();
  test('Apply on a closed repair dialog cannot mutate the project or throw',()=>evaluate('projectJson()')===afterRepair && w.__reviewErrors.length===afterRepairErrors && !repairDialog.open);

  test('No contrast JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Contrast harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
