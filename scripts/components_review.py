"""Independent components browser checks using the shared local Chrome runner.

Run: python scripts/components_review.py. Owns its app/profile and fixtures; does not
import or patch the integration harness. No runtime dependency is introduced.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Components review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Components: '+results.length+' checks; last: '+name;
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
    el.dispatchEvent(new w.Event(type,{bubbles:true}));w.DSStudio.propertyEditors?.saveFor(el);
  };
  try {
  test('Independent components startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(7,false);await wait();
  test('Default button focus contrasts with light and dark surfaces', () => evaluate("['#FFFFFF','#152236'].every(bg=>contrast(state.buttonDesign.focus,bg)>=3)"));
  test('New project defaults use 8px component dimensions and a 24px grid gutter', () => evaluate('adv.height===48 && adv.gap===24 && state.buttonDesign.padX===16 && state.buttonDesign.padY===8 && state.buttonDesign.minHeight===48'));
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(7,false);await wait();
  input('advState','loading','change');
  test('Loading demo exposes busy and disabled states', () => d.getElementById('advDemoButton').disabled && d.getElementById('advDemoButton').getAttribute('aria-busy')==='true');
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(7,false);await wait();
  const matrixStates=state=>[...d.querySelectorAll(`#bdMatrix [data-sim="${state}"]`)];
  for (const theme of ['light','dark']) {
    input('jTheme',theme); await wait();
    test(theme+' hover cues underline every button variant without changing geometry', () => matrixStates('hover').length===5 && matrixStates('hover').every((button,i)=>{
      const normal=matrixStates('default')[i];
      return w.getComputedStyle(button).textDecorationLine.includes('underline') && Math.abs(button.getBoundingClientRect().width-normal.getBoundingClientRect().width)<1 && Math.abs(button.getBoundingClientRect().height-normal.getBoundingClientRect().height)<1;
    }));
    test(theme+' pressed states add an inset cue to every variant', () => matrixStates('active').length===5 && matrixStates('active').every(button=>w.getComputedStyle(button).boxShadow.includes('inset')));
    test(theme+' selected states have a visible checkmark and an unchanged label', () => matrixStates('selected').length===5 && matrixStates('selected').every((button,i)=>{
      const icon=w.getComputedStyle(button,'::before');
      return button.getAttribute('aria-pressed')==='true' && icon.content==='""' && parseFloat(icon.borderBottomWidth)>0 && button.textContent===matrixStates('default')[i].textContent;
    }));
    test(theme+' focus simulations retain the full outline around every variant', () => matrixStates('focus').every(button=>parseFloat(w.getComputedStyle(button).outlineWidth)===3 && w.getComputedStyle(button).outlineStyle==='solid' && parseFloat(w.getComputedStyle(button).outlineOffset)===3));
    test(theme+' loading states retain readable opacity, visible progress and text', () => matrixStates('loading').length===5 && matrixStates('loading').every(button=>w.getComputedStyle(button).opacity==='1' && button.textContent==='Processing…' && w.getComputedStyle(button,'::after').content==='""' && parseFloat(w.getComputedStyle(button,'::after').width)>0));
    test(theme+' disabled states remain natively unavailable and separately explained', () => matrixStates('disabled').every(button=>button.disabled && w.getComputedStyle(button).cursor==='not-allowed'));
    for (const stateName of ['hover','active','focus','selected','loading','disabled']) {
      input('bdState',stateName); await wait();
      const action=previewDoc().querySelector('.sample-selected-action');
      const style=previewWindow().getComputedStyle(action);
      test(theme+' exported-page '+stateName+' state has its non-colour cue and semantics', () => {
        if (stateName==='hover') return style.textDecorationLine.includes('underline');
        if (stateName==='active') return style.boxShadow.includes('inset');
        if (stateName==='focus') return style.outlineStyle==='solid' && parseFloat(style.outlineOffset)===3;
        if (stateName==='selected') {
          const toggles=[...previewDoc().querySelectorAll('#components button[aria-pressed]')];
          return toggles.length===2 && toggles[0].textContent===toggles[1].textContent && toggles[0].getAttribute('aria-pressed')==='false' && action.getAttribute('aria-pressed')==='true' && previewWindow().getComputedStyle(action,'::before').content==='""' && previewWindow().getComputedStyle(toggles[0],'::before').visibility==='hidden' && Math.abs(toggles[0].getBoundingClientRect().width-action.getBoundingClientRect().width)<1;
        }
        if (stateName==='loading') return action.disabled && action.getAttribute('aria-busy')==='true' && action.textContent==='Processing…' && style.opacity==='1' && previewWindow().getComputedStyle(action,'::after').content==='""';
        return action.disabled && !!previewDoc().getElementById(action.getAttribute('aria-describedby'))?.textContent.includes('prerequisite');
      });
    }
  }
  input('advState','loading','change'); await wait();
  test('State Explorer loading uses the same progress cue and full-opacity text', () => d.getElementById('advDemoButton').textContent==='Processing…' && w.getComputedStyle(d.getElementById('advDemoButton')).opacity==='1' && w.getComputedStyle(d.getElementById('advDemoButton'),'::after').content==='""');
  input('bdState','loading');
  d.getElementById('advReduce').checked=true; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true}));w.DSStudio.propertyEditors?.saveFor(d.getElementById('advReduce')); await wait();
  test('Reduce demo animations stops progress in the laboratory and State Explorer', () => ['#bdSingle .bd-button','#advDemoButton'].every(selector=>w.getComputedStyle(d.querySelector(selector),'::after').animationName==='none'));
  test('Reduced demo motion also reaches the generated page and CSS export', () => previewWindow().getComputedStyle(previewDoc().querySelector('.sample-selected-action'),'::after').animationName==='none' && evaluate('cssExport()').includes('--button-progress-animation: none'));
  d.getElementById('advReduce').checked=false; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true}));w.DSStudio.propertyEditors?.saveFor(d.getElementById('advReduce')); await wait();
  test('Restoring demo animations preserves the platform reduced-motion preference', () => w.getComputedStyle(d.querySelector('#bdSingle .bd-button'),'::after').animationName===(w.matchMedia('(prefers-reduced-motion: reduce)').matches?'none':'dss-button-progress'));
  input('advState','selected','change'); await wait();
  test('State Explorer selection has a checkmark and nearby state guidance', () => w.getComputedStyle(d.getElementById('advDemoButton'),'::before').content==='""' && d.getElementById('advButtonHelp').textContent.includes('Keep the label'));
  input('bdState','default'); await wait();
  const focusSpecimen=d.querySelector('#bdSingle .bd-button'); w.dssRevealSection('bdSingle',false);focusSpecimen.focus();
  test('Actual keyboard-visible focus retains its outline independently of state simulations', () => !focusSpecimen.matches('[data-sim="focus"]') && focusSpecimen.matches(':focus-visible') && parseFloat(w.getComputedStyle(focusSpecimen).outlineWidth)===3);
  const statesDownload=[]; const priorStateDownload=w.download;
  w.download=(name,content)=>statesDownload.push({name,content}); d.getElementById('bdExport').click(); w.download=priorStateDownload;
  test('Standalone button CSS includes the shared state cues, forced-colour fallback and reduced motion', () => statesDownload[0].content.includes('text-decoration-line: underline') && statesDownload[0].content.includes('box-shadow: inset') && statesDownload[0].content.includes('[aria-pressed]::before') && statesDownload[0].content.includes('[aria-busy="true"]::after') && statesDownload[0].content.includes('prefers-reduced-motion: reduce') && statesDownload[0].content.includes('forced-colors: active'));
  const practicesProject=evaluate('projectJson()');
  input('bdFocus','#775599'); const customFocusProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+customFocusProject+')'); await wait();
  test('Imported custom focus colours remain editable under the new default practices', () => evaluate('state.buttonDesign.focus')==='#775599' && evaluate('cssExport()').includes('--button-focus: #775599'));
  evaluate('importConfig('+practicesProject+')'); reset(); await wait();
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(7,false);await wait();
  for (const stateName of ['default','hover','focus','active','selected','disabled','loading','invalid','success','readonly']) {
    input('advState',stateName,'change');
    test('State Explorer correctly exposes '+stateName+' semantics', () => {
      const button=d.getElementById('advDemoButton'), field=d.getElementById('advDemoInput');
      return button.disabled===['disabled','loading'].includes(stateName) &&
        button.getAttribute('aria-busy')===String(stateName==='loading') &&
        button.hasAttribute('aria-pressed')===(stateName==='selected') &&
        field.disabled===(stateName==='disabled') && field.readOnly===(stateName==='readonly') &&
        field.getAttribute('aria-invalid')===String(stateName==='invalid');
    });
  }
  reset();
  for (const [id,value,type] of [['advFocus',5],['advHeight',50],['advWeight',800,'change'],['advMeasure',75],['advBorder',6],['advShadow','strong','change'],['advOpacity',70],['advColumns',260],['advGap',20],['advAlign','end','change'],['advMotion',250],['bdVariant','outline'],['bdSize','lg'],['bdPaddingX',24],['bdPaddingY',18],['bdMinHeight',56],['bdRadius',20],['bdBorder',3],['bdWeight',700],['bdFocusWidth',4],['bdMotion',250],['bdSource','custom'],['bdCustom','#123456'],['bdHover','#234567'],['bdActive','#345678'],['bdText','#456789'],['bdHoverText','#ffffff'],['bdActiveText','#ffffff'],['bdDefaultBg','#eeeeee'],['bdBorderColor','#123456']]) input(id,value,type||'input');
  input('advAlign','start','change');
  const fullConfig=JSON.parse(evaluate('projectJson()'));
  reset(); evaluate('importConfig('+JSON.stringify(fullConfig)+')');
  test('Advanced and button editor settings survive a full project round trip', () => {
    const loaded=JSON.parse(evaluate('projectJson()'));
    return JSON.stringify(loaded.advanced)===JSON.stringify(fullConfig.advanced) && JSON.stringify(loaded.buttonDesign)===JSON.stringify(fullConfig.buttonDesign) && !/undefined|NaN|Infinity/.test(evaluate('cssExport()'));
  });
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(7,false);await wait();
  d.getElementById('dockTabCss').click();
  for (const theme of ['light','dark']) {
    input('dockTheme',theme,'change'); input('bdVariant','secondary'); input('bdSource','custom'); input('bdCustom','#b52266'); await wait();
    // Resolve live styles without transition timing affecting the sampled colour.
    const motion=previewDoc().createElement('style'); motion.textContent='.ds-button { transition: none !important; }'; previewDoc().head.append(motion);
    const secondaryActions=()=>[...previewDoc().querySelectorAll('.sample-section-actions > :last-child')];
    test(theme+' secondary custom base colour updates every page action pair', () => secondaryActions().length===9 && secondaryActions().every(action=>action.matches('a.ds-button--secondary') && previewWindow().getComputedStyle(action).backgroundColor==='rgb(181, 34, 102)'));
    test(theme+' secondary edits keep primary actions and the outline example independent', () => previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(0, 71, 128)' && !!previewDoc().querySelector('#components .ds-button--outline'));
    input('bdCustom','#196b63'); await wait();
    test(theme+' repeated custom colour edits reach the live page without a palette change', () => secondaryActions().every(action=>previewWindow().getComputedStyle(action).backgroundColor==='rgb(25, 107, 99)') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
    test(theme+' wizard and page show the same secondary default colour', () => w.getComputedStyle(d.querySelector('#bdSingle .bd-button')).backgroundColor===previewWindow().getComputedStyle(secondaryActions()[0]).backgroundColor);
  }
  const secondaryExport=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Secondary custom-colour exports use the matching variant for all section actions', () => [...secondaryExport.querySelectorAll('.sample-section-actions > :last-child')].every(action=>action.classList.contains('ds-button--secondary')) && evaluate('cssExport()').includes('--button-secondary-bg: #196b63'));
  reset(); await wait();
  d.querySelector('[data-journey-step="4"]').click(); await wait();

  // Buttons learning workspace: proposals stay local until the combined Save.
  reset();w.dssShowWizardStep(7,false);w.dssRevealSection('button-workspace-title',false);await wait();
  const get=id=>d.getElementById(id),edit=(id,value,type='input')=>{const el=get(id);if(el.type==='checkbox')el.checked=value;else el.value=value;el.dispatchEvent(new w.Event(type,{bubbles:true}));};
  const saveButtons=()=>d.querySelector('[data-property-actions="button-workspace"] button').click();
  const discardButtons=()=>d.querySelector('[data-property-actions="button-workspace"] button:nth-child(2)').click();
  const proposed=()=>w.DSStudio.propertyEditors.buttonSnapshot().state;
  test('Buttons has one visible shared action bar below both workspace columns',()=>get('button-workspace').contains(get('bdPaddingX'))&&get('button-workspace').contains(get('bdSource'))&&get('button-workspace').contains(get('bdState'))&&d.querySelector('[data-property-actions="buttons"]').hidden&&get('button-workspace-save-status').previousElementSibling.dataset.propertyActions==='button-workspace');
  test('Complete button matrix, stylesheet and saved audit start collapsed',()=>!get('bdMatrix').closest('details').open&&!get('bdCode').closest('details').open&&!get('bdReview').open);
  const savedBefore=evaluate('projectJson()'),cssBefore=evaluate('cssExport()');
  edit('bdPaddingX',30);edit('bdRadius',24);await wait();
  test('Button geometry drafts change specimens and CSS without saving project or export',()=>w.getComputedStyle(get('bdSingle').firstChild).paddingRight==='30px'&&w.getComputedStyle(get('bdSingle').firstChild).borderRadius==='24px'&&get('bdCode').textContent.includes('--button-pad-x: 30px')&&evaluate('projectJson()')===savedBefore&&evaluate('cssExport()')===cssBefore);
  test('Draft geometry also reaches the full matrix and both theme cards',()=>[...d.querySelectorAll('#bdMatrix .bd-button,#bdThemes .bd-button')].every(el=>w.getComputedStyle(el).borderRadius==='24px'));
  edit('bdDefaultBg','#ffffff');edit('bdText','#ffffff');await wait();
  test('Proposed contrast detects unreadable text without changing the saved audit',()=>get('button-learning-contrast').textContent.includes('required pairs need review')&&!evaluate('state.buttonDesign.overrides.primary?.bg'));
  edit('bdVariant','secondary');edit('bdDefaultBg','#123456');edit('bdFocus','#123456');edit('bdVariant','primary');await wait();
  test('Switching variants preserves every proposed colour and shared focus',()=>proposed().buttonDesign.overrides.primary.bg==='#ffffff'&&proposed().buttonDesign.overrides.secondary.bg==='#123456'&&get('bdDefaultBg').value==='#ffffff'&&get('bdFocus').value==='#123456'&&get('bdPaddingX').value==='30');
  edit('bdVariant','secondary');edit('bdFocus','#234567');edit('bdVariant','primary');await wait();
  test('The latest shared focus proposal wins across variant contexts',()=>proposed().buttonDesign.focus==='#234567'&&get('bdFocus').value==='#234567');
  w.DSStudio.propertyEditors.setTransparent(get('bdFocus'));edit('bdVariant','secondary');edit('bdFocus','#345678');await wait();
  test('A real shared focus colour clears a transparent proposal from another variant',()=>proposed().buttonDesign.focus==='#345678'&&!proposed().colourTransparency?.['button:focus']);
  edit('bdVariant','primary');discardButtons();await wait();
  test('Combined Discard restores geometry and every variant without saving colours',()=>!w.DSStudio.propertyEditors.hasButtonDrafts()&&proposed().buttonDesign.padX===16&&!proposed().buttonDesign.overrides.primary&&!proposed().buttonDesign.overrides.secondary&&get('bdFocus').value===evaluate('state.buttonDesign.focus').toLowerCase());
  edit('bdPaddingX',28);edit('bdDefaultBg','#123456');edit('bdVariant','secondary');edit('bdDefaultBg','#234567');
  edit('jPrimary','#345678');saveButtons();await wait();
  test('Combined Save commits geometry and colours for all edited variants',()=>evaluate('state.buttonDesign.padX')===28&&evaluate('state.buttonDesign.overrides.primary.bg')==='#123456'&&evaluate('state.buttonDesign.overrides.secondary.bg')==='#234567'&&!w.DSStudio.propertyEditors.hasButtonDrafts());
  test('Buttons Save preserves unrelated Palette drafts',()=>evaluate('state.primary')==='#004780'&&get('jPrimary').value==='#345678'&&w.DSStudio.propertyEditors.hasDrafts('palette-roles'));
  test('Saved button CSS reaches the website and JSON',()=>previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()')&&JSON.parse(evaluate('projectJson()')).buttonDesign.padX===28);
  d.querySelector('[data-property-actions="palette-roles"] button:nth-child(2)').click();
  edit('bdVariant','primary');edit('bdDefaultBg','#abcdef');edit('bdSource','custom');edit('bdCustom','#456789');
  get('palette-button-clear').click();await wait();
  test('Clearing variant overrides works on drafts and retains proposed source',()=>!proposed().buttonDesign.overrides.primary&&proposed().buttonDesign.sources.primary==='custom'&&proposed().buttonDesign.custom.primary==='#456789'&&evaluate('state.buttonDesign.overrides.primary.bg')==='#123456');
  edit('bdDefaultBg','#123456');await wait();
  test('Editing after clearing overrides retains the reset and the newly chosen paint',()=>proposed().buttonDesign.overrides.primary.bg==='#123456'&&!proposed().buttonDesign.overrides.primary.text);
  w.DSStudio.propertyEditors.setTransparent(get('bdDefaultBg'));await wait();
  test('None produces transparent proposed paint without committing',()=>w.getComputedStyle(get('bdSingle').firstChild).backgroundColor==='rgba(0, 0, 0, 0)'&&!evaluate('state.colourTransparency?.["button:primary:bg"]'));
  discardButtons();edit('bdMobileFull',true);edit('button-learning-viewport','narrow','change');await wait();
  test('Mobile width draft fills the narrow learning context and leaves saved width unchanged',()=>get('button-learning-context').classList.contains('button-learning-mobile-full')&&Math.abs(get('button-learning-context').firstChild.getBoundingClientRect().width-(get('button-learning-context').getBoundingClientRect().width-16))<2&&!evaluate('state.buttonDesign.mobileFull'));
  for(const st of ['hover','focus','active','selected','disabled','loading','default']){
    edit('bdState',st);await wait();
    test('Selected '+st+' state has a matching short CSS lesson',()=>get('button-learning-rule').textContent.includes(st==='default'?'--button-primary-bg':st==='hover'?':hover':st==='focus'?':focus-visible':st==='active'?':active':st==='selected'?'aria-pressed':st==='disabled'?':disabled':'aria-busy')&&!!get('button-learning-explanation').textContent);
  }
  const focused=get('bdSingle').firstChild;focused.focus();w.DSStudio.propertyEditors.refresh();await wait();
  test('Unchanged draft refresh preserves the real specimen and keyboard focus',()=>get('bdSingle').firstChild===focused&&d.activeElement===focused);
  edit('bdRadius',20);const beforePreview=proposed().buttonDesign.radius;
  d.querySelector('[data-property-actions="button-workspace"] [data-property-preview]').click();await wait();
  test('Responsive preview keeps Buttons open and preserves its unsaved proposals',()=>get('buttonDesignLab').open&&get('studio-section-4').open&&d.activeElement===get('previewShell')&&proposed().buttonDesign.radius===beforePreview&&evaluate('state.buttonDesign.radius')!==beforePreview);
  w.dssRevealSection('bdSource',false);await wait();
  test('Token and Palette routes reveal the single colour editor in Buttons',()=>get('buttonDesignLab').open&&get('button-group-colours').open&&get('palette-button-colours').closest('#button-workspace'));
  test('Learning preview shows all five labelled action variants',()=>[...get('button-learning-context').children].map(el=>el.textContent).join('|')==='Primary action|Secondary action|Accent action|Outline action|Text action');
  for(const variant of ['primary','secondary','accent','outline','text']){
    get('button-learning-context').querySelector('[data-button-variant='+variant+']').click();await wait();
    test('The contextual '+variant+' action selects its variant and preserves drafts',()=>evaluate('state.buttonDesign.variant')===variant&&d.activeElement===get('bdVariant')&&w.DSStudio.propertyEditors.hasButtonDrafts()&&get('button-learning-context').querySelector('[aria-current=true]').dataset.buttonVariant===variant);
  }
  get('bdMatrix').closest('details').open=true;d.querySelector('#bdMatrix [data-sim=hover]').click();await wait();
  test('The full matrix selects a state without saving pending properties',()=>get('bdState').value==='hover'&&d.activeElement===get('bdVariant')&&w.DSStudio.propertyEditors.hasButtonDrafts());
  for(const theme of ['light','dark'])for(const width of [320,390,1440]){
    app.style.width=width+'px';if(evaluate('state.theme')!==theme)input('dockTheme',theme,'change');w.dssRevealSection('button-workspace-title',false);get('button-group-colours').open=true;await wait();
    test(theme+' Buttons colour controls retain their dimensions at '+width+'px',()=>[...get('palette-button-colours').querySelectorAll('input,select,button')].filter(el=>el.getBoundingClientRect().height>0).every(el=>{const box=el.getBoundingClientRect();return box.height>=44&&box.right<=w.innerWidth+1;}));
    test(theme+' all learning variants wrap within '+width+'px',()=>get('button-learning-context').children.length===5&&[...get('button-learning-context').children].every(el=>{const box=el.getBoundingClientRect(),host=get('button-learning-context').getBoundingClientRect();return box.width>0&&box.left>=host.left&&box.right<=host.right+1;}));
    test(theme+' Buttons workspace fits '+width+'px',()=>d.documentElement.scrollWidth<=d.documentElement.clientWidth+1&&get('button-workspace').getBoundingClientRect().width>0&&get('button-workspace').scrollWidth<=get('button-workspace').clientWidth+1);
  }
  app.style.width='1440px';edit('bdRadius',22);evaluate('importConfig(JSON.parse(projectJson()))');await wait();
  test('Project replacement clears combined button drafts',()=>!w.DSStudio.propertyEditors.hasButtonDrafts()&&proposed().buttonDesign.radius===evaluate('state.buttonDesign.radius'));
  // The short CSS lesson follows every editable Buttons control group.
  reset();w.dssShowWizardStep(7,false);w.dssRevealSection('button-workspace-title',false);await wait();
  const lessonCases=[
    ['bdPaddingX',30,'Size and spacing','--button-pad-x: 30px','30px'],
    ['bdPaddingY',12,'Size and spacing','--button-pad-y: 12px','12px'],
    ['bdMinHeight',56,'Size and spacing','--button-min-height: 56px','56px'],
    ['bdSize','sm','Size and spacing','.ds-button--sm','0.8'],
    ['bdSize','lg','Size and spacing','.ds-button--lg','1.22'],
    ['bdSize','md','Size and spacing','--button-min-height: 56px','Medium'],
    ['bdRadius',20,'Shape and typography','--button-radius: 20px','20px'],
    ['bdBorder',3,'Shape and typography','--button-border-width: 3px','3px'],
    ['bdWeight',400,'Shape and typography','--button-font-weight: 400','400'],
    ['bdSource','secondary','Colours and tokens','--button-primary-source:','secondary'],
    ['bdSource','custom','Colours and tokens','--button-primary-source:','Custom'],
    ['bdCustom','#123456','Colours and tokens','--button-primary-source: #123456','Custom'],
    ['bdDefaultBg','#234567','Colours and tokens','--button-primary-bg: #234567','Primary'],
    ['bdText','#ffffff','Colours and tokens','--button-primary-text: #ffffff','Primary'],
    ['bdHover','#345678','Colours and tokens','--button-primary-hover: #345678','Primary'],
    ['bdHoverText','#eeeeee','Colours and tokens','--button-primary-hover-text: #eeeeee','Primary'],
    ['bdActive','#456789','Colours and tokens','--button-primary-active: #456789','Primary'],
    ['bdActiveText','#dddddd','Colours and tokens','--button-primary-active-text: #dddddd','Primary'],
    ['bdBorderColor','#56789a','Colours and tokens','--button-primary-border: #56789a','Primary'],
    ['bdFocus','#6789ab','Colours and tokens','--button-focus: #6789ab','Focus'],
    ['bdFocusWidth',5,'States and behaviour','--button-focus-width: 5px','5px'],
    ['bdMotion',250,'States and behaviour','--button-motion: 250ms','250ms'],
    ['bdMobileFull',true,'States and behaviour','.ds-button--mobile-full { width: 100%; }','on,'],
    ['bdMobileFull',false,'States and behaviour','Full-width mobile actions are off','off.']
  ];
  const originalLessonJson=evaluate('projectJson()'),originalLessonCss=evaluate('cssExport()');
  for(const [id,value,group,cssText,explanation]of lessonCases){
    edit(id,value,'change');await wait();
    test(id+' updates the appropriate CSS lesson and proposed values',()=>get('button-learning-topic').textContent===group&&get('button-learning-rule').textContent.toLowerCase().includes(cssText.toLowerCase())&&get('button-learning-explanation').textContent.includes(explanation)&&!get('button-learning-rule').textContent.includes('undefined'));
  }
  test('Exploring every CSS lesson keeps saved JSON and export CSS unchanged',()=>evaluate('projectJson()')===originalLessonJson&&evaluate('cssExport()')===originalLessonCss);
  w.DSStudio.propertyEditors.setTransparent(get('bdDefaultBg'));await wait();
  test('Transparent paint is explicit in the colour lesson',()=>get('button-learning-topic').textContent==='Colours and tokens'&&get('button-learning-rule').textContent.includes('--button-primary-bg: transparent;'));
  for(const st of ['hover','focus','active','selected','disabled','loading','default']){edit('bdState',st);await wait();test(st+' retains a matching state lesson and valid CSS blocks',()=>get('button-learning-topic').textContent==='States and behaviour'&&get('button-learning-explanation').textContent.startsWith(w.DSStudio.buttons.stateLabels[st]+'.')&&get('button-learning-rule').textContent.includes('@media (prefers-reduced-motion: reduce)')&&(get('button-learning-rule').textContent.match(/{/g)||[]).length===(get('button-learning-rule').textContent.match(/}/g)||[]).length);}
  w.dssRevealSection('bdWeight',false);get('bdWeight').focus();await wait();
  test('Focusing a control group reveals its lesson without changing a value',()=>get('button-learning-topic').textContent==='Shape and typography'&&get('button-learning-rule').textContent.includes('--button-font-weight: 400;')&&d.activeElement===get('bdWeight'));
  discardButtons();await wait();
  test('Discard refreshes CSS lessons to saved values',()=>get('bdCode').textContent===w.DSStudio.buttons.css()&&!w.DSStudio.propertyEditors.hasButtonDrafts()&&!get('button-learning-rule').textContent.includes('undefined'));
  edit('bdWeight',700,'change');saveButtons();await wait();
  test('Save keeps the short and complete font-weight rules consistent with exports',()=>get('button-learning-rule').textContent.includes('--button-font-weight: 700;')&&get('bdCode').textContent===w.DSStudio.buttons.css()&&evaluate('cssExport()').includes('--button-font-weight: 700;') );
  for(const theme of ['light','dark']){
    input('dockTheme',theme,'change');edit('bdDefaultBg','#345678','change');await wait();
    test(theme+' colour lesson uses the proposed theme scope and exported component token',()=>get('button-learning-topic').textContent==='Colours and tokens'&&get('button-learning-rule').textContent.startsWith(theme==='dark'?'[data-theme="dark"]':':root')&&get('button-learning-rule').textContent.includes('--button-primary-bg: #345678;')&&get('bdCode').textContent.includes('--button-primary-bg: #345678;'));
    w.DSStudio.propertyEditors.setTransparent(get('bdDefaultBg'));await wait();
    test(theme+' colour lesson keeps transparent token values explicit',()=>get('button-learning-rule').textContent.includes('--button-primary-bg: transparent;')&&!get('button-learning-rule').textContent.includes('undefined'));
  }
  discardButtons();
  // Per-variant elevation and the synchronized website theme selector.
  {
    reset();w.dssShowWizardStep(7,false);w.dssRevealSection('bdElevation',false);await wait();
    const bget=id=>d.getElementById(id),stage=(id,value)=>{const el=bget(id);el.value=value;el.dispatchEvent(new w.Event(id==='bdVariant'||id==='bdState'?'input':'change',{bubbles:true}));},cancel=()=>d.querySelector('[data-property-actions="button-workspace"] button:nth-child(2)').click(),commit=()=>d.querySelector('[data-property-actions="button-workspace"] button').click();
    const shadow=selector=>w.getComputedStyle(d.querySelector(selector)).boxShadow,snapshot=()=>w.DSStudio.propertyEditors.buttonSnapshot().state;
    test('Button elevation defaults to None in every variant',()=>bget('bdElevation').value==='none'&&[...d.querySelectorAll('#button-learning-context .bd-button')].every(el=>w.getComputedStyle(el).boxShadow==='none')&&!evaluate('cssExport()').includes('--button-primary-shadow:'));
    const cleanJson=evaluate('projectJson()'),cleanCss=evaluate('cssExport()'),page=previewDoc();
    stage('bdElevation','subtle');await wait();
    test('Primary elevation drafts update only the intended variant',()=>snapshot().buttonDesign.elevation.primary==='subtle'&&shadow('#button-learning-context [data-button-variant="primary"]').includes('4px')&&shadow('#button-learning-context [data-button-variant="secondary"]')==='none'&&shadow('#button-learning-context [data-button-variant="outline"]')==='none'&&shadow('#button-learning-context [data-button-variant="text"]')==='none');
    test('Elevation proposal updates CSS and explanation while saved output stays unchanged',()=>bget('button-learning-topic').textContent==='Shape and typography'&&bget('button-learning-rule').textContent.includes('--button-primary-shadow: 0 2px 4px #00000024;')&&bget('button-learning-explanation').textContent.includes('elevation: subtle')&&bget('bdCode').textContent.includes('--button-primary-shadow:')&&evaluate('projectJson()')===cleanJson&&evaluate('cssExport()')===cleanCss&&previewDoc()===page);
    const uiTheme=d.documentElement.dataset.theme,lightShadow=shadow('#bdSingle .bd-button');
    stage('button-website-theme','dark');await wait();
    test('Nearby website theme control synchronizes all website theme controls independently of Studio',()=>evaluate('state.theme')==='dark'&&bget('dockTheme').value==='dark'&&bget('palette-theme').value==='dark'&&bget('spacing-website-theme').value==='dark'&&d.documentElement.dataset.theme===uiTheme);
    test('Dark website preview keeps editing instructions readable on the Studio surface',()=>{const hint=bget('button-learning-instructions'),color=w.getComputedStyle(hint).color.match(/\d+/g).slice(0,3).map(Number),hex='#'+color.map(value=>value.toString(16).padStart(2,'0')).join(''),surface=w.getComputedStyle(d.documentElement).getPropertyValue('--studio-surface').trim();return !bget('button-learning-page').contains(hint)&&w.eval('contrast')(hex,surface)>=4.5;});
    test('Theme switching retains the elevation draft and its current lesson',()=>snapshot().buttonDesign.elevation.primary==='subtle'&&!evaluate('state.buttonDesign.elevation.primary')&&bget('button-learning-topic').textContent==='Shape and typography'&&bget('button-learning-rule').textContent.includes('--button-primary-shadow: 0 2px 4px #00000066;')&&shadow('#bdSingle .bd-button')!==lightShadow);
    stage('bdVariant','secondary');stage('bdElevation','medium');stage('bdVariant','primary');await wait();
    test('Variant browsing preserves independent elevation proposals',()=>bget('bdElevation').value==='subtle'&&snapshot().buttonDesign.elevation.secondary==='medium'&&shadow('#button-learning-context [data-button-variant="secondary"]').includes('10px'));
    cancel();await wait();
    test('Discard clears every proposed elevation and preserves website theme',()=>!w.DSStudio.propertyEditors.hasButtonDrafts()&&Object.keys(snapshot().buttonDesign.elevation).length===0&&evaluate('state.theme')==='dark'&&shadow('#bdSingle .bd-button')==='none');
    stage('bdElevation','medium');stage('bdVariant','secondary');stage('bdElevation','subtle');stage('bdVariant','primary');commit();await wait();
    test('Save commits all variant elevations to JSON and page CSS',()=>evaluate('state.buttonDesign.elevation.primary')==='medium'&&evaluate('state.buttonDesign.elevation.secondary')==='subtle'&&JSON.parse(evaluate('projectJson()')).buttonDesign.elevation.primary==='medium'&&previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
    const savedShadowProject=JSON.parse(evaluate('projectJson()'));w.importConfig(savedShadowProject);await wait();
    test('Elevation survives project round trip',()=>bget('bdElevation').value==='medium'&&evaluate('state.buttonDesign.elevation.secondary')==='subtle'&&shadow('#bdSingle .bd-button').includes('10px'));
    bget('jSaveLocal').click();await wait();stage('bdElevation','none');bget('jLoadLocal').click();await wait();
    test('Loading a saved project restores elevations and clears an unsaved shadow proposal',()=>bget('bdElevation').value==='medium'&&evaluate('state.buttonDesign.elevation.secondary')==='subtle'&&!w.DSStudio.propertyEditors.hasButtonDrafts());
    for(const theme of ['light','dark'])for(const stateName of ['default','hover','active','focus','selected','disabled','loading']){
      stage('button-website-theme',theme);stage('bdState',stateName);await wait();
      test(theme+' '+stateName+' keeps elevation and its applicable state cues',()=>{
        const el=d.querySelector('#bdSingle .bd-button'),style=w.getComputedStyle(el);return style.boxShadow.includes('10px')&&(stateName!=='active'||style.boxShadow.includes('inset'))&&(stateName!=='selected'||style.boxShadow.includes('2px'))&&(stateName!=='disabled'||el.disabled)&&(stateName!=='loading'||el.getAttribute('aria-busy')==='true');
      });
    }
    for(const mode of ['basic','advanced'])for(const theme of ['light','dark']){
      bget(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();stage('button-website-theme',theme);stage('bdState','default');await wait();
      const frame=d.createElement('iframe');frame.srcdoc='<!doctype html><html data-theme="'+theme+'"><head></head><body><button class="ds-button ds-button--primary" type="button" id="shadow-export">Primary action</button><button class="ds-button ds-button--text">Text action</button></body></html>';d.body.append(frame);await wait();const doc=frame.contentDocument,view=frame.contentWindow,css=d.createElement('style');css.textContent=evaluate('cssExport()');doc.head.append(doc.importNode(css,true));const el=doc.getElementById('shadow-export');
      test(mode+' '+theme+' standalone styles match saved elevation and keep Text flat',()=>view.getComputedStyle(el).boxShadow.includes('10px')&&view.getComputedStyle(doc.querySelector('.ds-button--text')).boxShadow==='none');
      el.dataset.previewState='active';test(mode+' '+theme+' exported pressed styling composes elevation',()=>view.getComputedStyle(el).boxShadow.includes('inset')&&view.getComputedStyle(el).boxShadow.includes('10px'));
      el.setAttribute('aria-pressed','true');test(mode+' '+theme+' combined pressed toggle retains all three shadow layers',()=>{const value=view.getComputedStyle(el).boxShadow;return value.includes('inset')&&value.includes('2px')&&value.includes('10px');});
      delete el.dataset.previewState;el.focus();test(mode+' '+theme+' native keyboard focus remains separate from elevation',()=>view.getComputedStyle(el).outlineStyle==='solid'&&view.getComputedStyle(el).outlineWidth==='3px');frame.remove();
    }
    stage('bdState','default');w.dssConfigureToken({name:'--button-secondary-shadow',scope:'Dark'});await wait();
    test('Shadow token source routes to the correct variant elevation control',()=>w.DSStudio.activeStage===7&&bget('bdVariant').value==='secondary'&&d.activeElement===bget('bdElevation'));
    stage('bdElevation','none');commit();stage('bdVariant','primary');stage('bdElevation','none');commit();await wait();
    test('Selecting None removes optional shadow CSS when all variants are flat',()=>!evaluate('cssExport()').includes('--button-primary-shadow:')&&Object.keys(evaluate('state.buttonDesign.elevation')).length===0&&shadow('#bdSingle .bd-button')==='none');
    for(const width of [320,390,1440]){app.style.width=width+'px';w.dssRevealSection('bdElevation',false);await wait();test('Website theme and elevation controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1&&[bget('bdElevation'),bget('button-website-theme')].every(el=>el.getBoundingClientRect().height>=44&&el.getBoundingClientRect().right<=w.innerWidth+1));}
    app.style.width='1440px';
    const validated=w.DSStudio.project.normalize({buttonDesign:{elevation:{primary:'medium',secondary:'subtle',accent:'none',outline:'0 0 url(javascript:alert(1))',text:{},unknown:'medium'}}}).state.buttonDesign.elevation;
    test('Elevation imports accept only known presets and variants',()=>JSON.stringify(validated)==='{"primary":"medium","secondary":"subtle"}'&&Object.keys(w.DSStudio.project.normalize({buttonDesign:{elevation:['medium']}}).state.buttonDesign.elevation).length===0);
    test('Legacy projects retain the flat elevation default',()=>Object.keys(w.DSStudio.project.normalize({buttonDesign:{weight:700}}).state.buttonDesign.elevation).length===0);
  }
  test('No components JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Components harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
