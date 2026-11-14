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
    el.dispatchEvent(new w.Event(type,{bubbles:true}));
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
  d.getElementById('advReduce').checked=true; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true})); await wait();
  test('Reduce demo animations stops progress in the laboratory and State Explorer', () => ['#bdSingle .bd-button','#advDemoButton'].every(selector=>w.getComputedStyle(d.querySelector(selector),'::after').animationName==='none'));
  test('Reduced demo motion also reaches the generated page and CSS export', () => previewWindow().getComputedStyle(previewDoc().querySelector('.sample-selected-action'),'::after').animationName==='none' && evaluate('cssExport()').includes('--button-progress-animation: none'));
  d.getElementById('advReduce').checked=false; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true})); await wait();
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

  test('No components JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Components harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
