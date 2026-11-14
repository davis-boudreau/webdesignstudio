"""Independent palette browser checks using the shared local Chrome runner.

Run: python scripts/palette_review.py. Owns its app/profile and fixtures; does not
import or patch the integration harness. No runtime dependency is introduced.
"""
from browser_runner import run_review


HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Palette review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload=async()=>{
  const w=app.contentWindow,d=w.document,results=[],evaluate=code=>w.eval(code);
  const finish=()=>document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  const test=(name,fn)=>{
    try{if(!fn())throw Error('Assertion failed');results.push({name,pass:true});}
    catch(error){results.push({name,pass:false,error:String(error.stack||error)});}
    document.title='Palette: '+results.length+' checks; last: '+name;
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
  test('Independent palette startup has no JavaScript errors',()=>!w.__reviewErrors.length);
  const report=()=>w.dssGetContrastChecks();
  test('Startup defaults to OKLCH across state, both method controls and lesson output',()=>evaluate('state.method')==='oklch' && d.getElementById('jRamp').value==='oklch' && d.getElementById('method').value==='oklch' && d.getElementById('rampMethodLabel').textContent==='OKLCH' && d.getElementById('palette-method-status').textContent.includes('OKLCH'));
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(4,false);await wait();
  for (const method of ['mix','oklch']) {
    input('method',method);
    test(method+' ramps preserve anchors and emit valid colours', () => evaluate(`
      ['primary','secondary','accent'].every(k=>{
        const ramp=makeRamp(state[k],state.method);
        return ramp[500]===state[k].toUpperCase() && Object.values(ramp).every(validHex);
      })`));
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(4,false);await wait();
  w.dssRevealSection('oklchRole',false);await wait();
  for (const hex of ['#FF0000','#00FF00','#0000FF','#FFFFFF','#000000','#004780']) {
    test('OKLCH round trip preserves '+hex, () => evaluate(`oklchHex(...rgbToOklch('${hex}'))` )===hex);
  }
  input('oklchRole','accent','change');
  input('oklchLight',65); input('oklchChroma',.12); input('oklchHue',150);
  const chosenHex=d.getElementById('oklchHex').textContent;
  test('OKLCH exploration leaves palette unchanged before Apply', () => evaluate('state.accent')==='#cbdb2a');
  d.getElementById('oklchApply').click();
  test('OKLCH Apply updates foundation, guided editor, export and saved project', () => {
    d.getElementById('jSaveLocal').click();
    return evaluate('state.accent').toUpperCase()===chosenHex && d.getElementById('jAccent').value.toUpperCase()===chosenHex && evaluate('cssExport()').includes('--accent-500: '+chosenHex) && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.accent.toUpperCase()===chosenHex);
  });
  input('oklchLight',90); d.getElementById('oklchReset').click();
  test('OKLCH Load discards exploration and reloads the current palette anchor', () => d.getElementById('oklchHex').textContent===chosenHex);
  input('oklchLight',60); input('oklchChroma',.4);
  test('OKLCH warns when chroma exceeds sRGB gamut', () => d.getElementById('oklchGamut').textContent.startsWith('Outside sRGB') && /^#[0-9A-F]{6}$/.test(d.getElementById('oklchHex').textContent));
  for (const role of ['primary','secondary','accent']) {
    input('oklchRole',role,'change'); input('oklchLight',65); input('oklchChroma',.12); input('oklchHue',150);
    d.getElementById('oklchApply').click();
    const otherRoles=evaluate(`JSON.stringify(Object.fromEntries(['primary','secondary','accent'].filter(key=>key!=='${role}').map(key=>[key,state[key]])))`);
    const references=evaluate('JSON.stringify(state.brandPalette)');
    d.getElementById('oklchDefault').click(); await wait();
    test('OKLCH default reset restores only '+role+' and synchronizes controls, preview, export and saved data', () => {
      const expected=evaluate(`DEFAULT.${role}`).toUpperCase();
      d.getElementById('jSaveLocal').click();
      return evaluate(`state.${role}.toUpperCase()===DEFAULT.${role}.toUpperCase()`)
        && d.getElementById('oklchHex').textContent===expected
        && d.getElementById('j'+role[0].toUpperCase()+role.slice(1)).value.toUpperCase()===expected
        && evaluate('cssExport()').includes('--'+role+'-500: '+expected)
        && d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent.includes('--'+role+'-500: '+expected)
        && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data[role].toUpperCase()===expected)
        && evaluate(`JSON.stringify(Object.fromEntries(['primary','secondary','accent'].filter(key=>key!=='${role}').map(key=>[key,state[key]])))`)===otherRoles
        && evaluate('JSON.stringify(state.brandPalette)')===references;
    });
    d.getElementById('oklchDefault').click();
    test('Repeated '+role+' default reset keeps the wheel selection stable', () => d.getElementById('oklchHex').textContent===evaluate(`DEFAULT.${role}.toUpperCase()`) && d.getElementById('oklchRole').value===role);
  }
  reset(); await wait();
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(4,false);await wait();
  // Palette uses Architecture-style browsing and selected form properties.
  {
    reset();w.dssShowWizardStep(4,false);await wait();const ui=w.DSStudio.paletteWorkspace;
    test('All Palette stages separate browsing from selected properties',()=>d.querySelectorAll('.palette-editor-columns').length===7 && [...d.querySelectorAll('.palette-editor-columns')].every(el=>el.children[0].classList.contains('palette-browser') && el.children[1].classList.contains('palette-properties')));
    const before=evaluate('projectJson()');d.querySelector('[data-palette-colour="blue"]').click();await wait();
    test('Selecting a brand shows its existing editable properties with focus',()=>d.getElementById('palette-brand-selection').value==='blue' && d.querySelector('[data-palette-colour="blue"]').getAttribute('aria-pressed')==='true' && d.activeElement===d.querySelector('[data-brand-id="blue"] [data-brand-field="name"]') && evaluate('projectJson()')===before);
    input('palette-brand-query','not-present-anywhere');await wait();test('Brand search explains an empty result while keeping the selected properties',()=>d.getElementById('palette-brand-results').textContent.includes('No matching') && ![...d.querySelectorAll('#palette-brand-list button')].some(el=>!el.hidden) && d.getElementById('palette-brand-selection').value==='blue' && !d.querySelector('[data-brand-id="blue"]').hidden);input('palette-brand-query','');
    d.getElementById('jBrandAdd').click();await wait();const newId=d.getElementById('palette-brand-selection').value;
    test('Brand Add belongs to the browser and focuses the new right-hand properties',()=>d.getElementById('palette-browse-brand').contains(d.getElementById('jBrandAdd')) && d.getElementById('palette-properties-brand').contains(d.activeElement) && d.querySelector('[data-palette-colour="'+newId+'"]').getAttribute('aria-pressed')==='true');
    d.getElementById('palette-brand-remove').click();await wait();test('Browser removal delegates to the existing guarded brand CRUD',()=>!evaluate('state.brandPalette').some(row=>row.id===newId) && d.activeElement===d.getElementById('jBrandAdd'));
    ui.show('roles',false);input('palette-anchor-selection','secondary','change');await wait();test('Anchor browsing exposes just the selected form and its reset action',()=>!d.getElementById('jSecondary').closest('.field').hidden && d.getElementById('jPrimary').closest('.field').hidden && !d.getElementById('palette-reset-secondary').hidden && d.getElementById('palette-properties-roles').contains(d.getElementById('jSecondary')));
    ui.show('shades',false);d.querySelector('[data-palette-family="neutral"]').click();await wait();test('Shade browsing shows one family as read-only form fields',()=>d.querySelectorAll('#main-palette-steps > [data-palette-role]:not([hidden])').length===1 && d.querySelector('#main-palette-steps [data-palette-role="neutral"] .palette-value-field').readOnly && d.querySelector('#main-palette-steps [data-palette-role="neutral"] .palette-value-label').textContent==='--neutral-50' && !d.getElementById('neutralPaletteAnchor').closest('section').hidden);
    ui.show('semantics',false);input('jSemanticRole','text','change');const original=evaluate('palette().roles.text'),proposal=original.toUpperCase()==='#246A68'?'#345678':'#246A68';input('palette-semantic-hex',proposal);await wait();
    test('Semantic properties stage an editable proposal without changing the website',()=>d.getElementById('palette-browse-semantics').contains(d.getElementById('jSemanticRole')) && d.getElementById('palette-properties-semantics').contains(d.getElementById('palette-semantic-hex')) && d.getElementById('palette-semantic-token').readOnly && evaluate('palette().roles.text')===original && d.getElementById('palette-semantic-proposal-status').textContent.includes('not applied'));
    d.getElementById('jSemanticEdit').focus();d.getElementById('jSemanticEdit').click();await wait();test('Semantic Preview uses the proposed property value in the existing contrast dialog',()=>d.getElementById('colourRepair').open && d.getElementById('repairHex').value.toUpperCase()===proposal && evaluate('palette().roles.text')===original);d.getElementById('repairCancel').click();await wait();test('Cancelling preview returns to right-hand properties and keeps saved colours',()=>d.activeElement===d.getElementById('jSemanticEdit') && evaluate('palette().roles.text')===original);
    d.getElementById('palette-semantic-discard').click();await wait();test('Discard restores the current value and clears proposal validity',()=>d.getElementById('palette-semantic-hex').value.toUpperCase()===original.toUpperCase() && d.getElementById('palette-semantic-hex').validity.valid && d.getElementById('palette-semantic-discard').disabled);
    input('palette-semantic-hex',proposal);d.getElementById('jSemanticEdit').click();await wait();d.getElementById('repairApply').click();await wait();test('Applying the semantic proposal updates existing project and property fields',()=>evaluate('palette().roles.text').toUpperCase()===proposal && d.getElementById('palette-semantic-hex').value.toUpperCase()===proposal && d.getElementById('palette-semantic-discard').disabled);
    input('palette-semantic-hex','bad');d.getElementById('jSemanticEdit').click();await wait();test('Invalid property proposals remain in the inspector without opening a dialog',()=>!d.getElementById('colourRepair').open && !d.getElementById('palette-semantic-hex').validity.valid);d.getElementById('palette-semantic-discard').click();
    w.dssConfigureToken({name:'--primary-500',scope:'Light / base'});await wait();test('Source routing selects and reveals the correct anchor properties',()=>!d.getElementById('jPrimary').closest('.field').hidden && d.getElementById('palette-anchor-selection').value==='primary' && d.activeElement===d.getElementById('jPrimary'));
    ui.show('components',false);input('palette-component-family','cards','change');ui.show('roles',false);evaluate('state.semanticOverrides={...state.semanticOverrides,light:{...state.semanticOverrides?.light,surface:"#EEECDD"}};apply()');await wait();d.querySelector('#palette-stage-components > summary').click();await wait();
    test('Native stage opening refreshes generated property fields after hidden changes',()=>{const code=d.querySelector('[data-component-token="--surface"]');return code.hidden && code.nextElementSibling.readOnly && code.nextElementSibling.value==='#EEECDD';});
    d.getElementById('brandPalette').open=false;evaluate('state.semanticOverrides.light.surface="#CCDDEE";apply()');d.getElementById('brandPalette').open=true;await wait();test('Manual Palette reopening refreshes read-only properties after hidden changes',()=>d.querySelector('[data-component-token="--surface"]').nextElementSibling.value==='#CCDDEE');
    for(const theme of ['light','dark'])for(const width of [320,390,1440]){app.style.width=width+'px';if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(4,false);await wait();for(const stage of ['brand','roles','shades','semantics','backgrounds','components','review']){ui.show(stage,false);await wait();test(theme+' '+stage+' Palette browser/properties fit '+width+'px',()=>{const grid=d.querySelector('#palette-stage-'+stage+' .palette-editor-columns'),left=grid.children[0].getBoundingClientRect(),right=grid.children[1].getBoundingClientRect();return d.documentElement.scrollWidth<=w.innerWidth+1 && (grid.clientWidth>720?Math.abs(left.top-right.top)<=1:right.top>=left.bottom-1) && [...grid.querySelectorAll('input,select,button')].filter(el=>el.getBoundingClientRect().height>0).every(el=>el.getBoundingClientRect().right<=w.innerWidth+1);});}}
    app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();await wait();
  }
  // End Palette browser checks.
  // Every UI anchor is discoverable and edits its own source colour.
  {
    reset();w.dssShowWizardStep(4,false);await wait();const ui=w.DSStudio.paletteWorkspace,selector=d.getElementById('palette-anchor-selection'),keys=['primary','secondary','accent'];
    ui.show('roles',false);await wait();
    test('UI anchor list visibly offers Primary, Secondary and Accent',()=>selector.size===3 && [...selector.options].map(option=>option.textContent).join(',')==='Primary,Secondary,Accent' && d.getElementById('palette-browse-roles').contains(selector));
    for(const theme of ['light','dark']){
      input('palette-theme',theme,'change');
      for(const [index,key]of keys.entries()){
        const title=key[0].toUpperCase()+key.slice(1),brandId='j'+title+'Brand',pickerId='j'+title;
        selector.focus();input('palette-anchor-selection',key,'change');await wait();
        test(theme+' '+key+' selection exposes its own editable properties and retains selector focus',()=>selector.value===key && d.activeElement===selector && keys.every(other=>d.getElementById('j'+other[0].toUpperCase()+other.slice(1)).closest('.field').hidden===(other!==key)) && !d.getElementById(pickerId).disabled && !d.getElementById(brandId).disabled && d.getElementById('palette-properties-title-roles').textContent===title+' anchor properties');
        const before=JSON.parse(evaluate('projectJson()')),hex=evaluate('state.brandPalette['+(index+3)+'].hex');input(brandId,hex,'change');await wait();
        test(theme+' '+key+' brand assignment updates only that anchor',()=>evaluate('state.'+key).toUpperCase()===hex.toUpperCase() && keys.every(other=>other===key || evaluate('state.'+other)===before[other]) && selector.value===key);
        const custom=['#235678','#765432','#9a286b'][index];input(pickerId,custom);await wait();
        test(theme+' '+key+' custom colour reaches project JSON and generated ramp',()=>JSON.parse(evaluate('projectJson()'))[key].toUpperCase()===custom.toUpperCase() && evaluate('cssExport()').toUpperCase().includes('--'+key.toUpperCase()+'-500: '+custom.toUpperCase()) && d.getElementById(brandId).value==='' && selector.value===key);
      }
    }
    const snapshot=JSON.parse(evaluate('projectJson()'));w.importConfig(snapshot);await wait();ui.show('roles',false);await wait();
    test('All three custom anchors survive project JSON loading',()=>keys.every(key=>evaluate('state.'+key)===snapshot[key]) && selector.value==='primary');
    input('palette-anchor-selection','accent','change');d.getElementById('palette-reset-accent').click();await wait();
    test('Selected Accent reset preserves Primary and Secondary',()=>evaluate('state.accent===DEFAULT.accent') && evaluate('state.primary')===snapshot.primary && evaluate('state.secondary')===snapshot.secondary && selector.value==='accent');
    reset();w.dssShowWizardStep(4,false);await wait();
  }

  // Guided Palette: a compact wizard and editable centre process.
  {
    const ui=w.DSStudio.paletteWorkspace;
    reset();w.dssShowWizardStep(4,false);await wait();
    test('Palette wizard is a short guide and all colour editors live in the centre',()=>!d.querySelector('[data-journey-pane="4"] input,[data-journey-pane="4"] select') && d.querySelectorAll('#palette-workspace [data-palette-stage]').length===7 && d.getElementById('palette-workspace').contains(d.getElementById('jPrimary')) && d.getElementById('palette-workspace').contains(d.getElementById('jBrandEditor')));
    test('Brand creation and count are visible collection actions without placeholder text',()=>d.getElementById('jBrandAdd').parentElement===d.getElementById('palette-browse-brand') && d.getElementById('jBrandCount').parentElement===d.getElementById('jBrandAdd').parentElement && !d.getElementById('palette-stage-brand').textContent.includes('nullnull'));
    const snapshot=evaluate('projectJson()');
    for(const key of ['brand','roles','shades','semantics','backgrounds','components','review']){ui.show(key);await wait();test('Palette '+key+' stage is explained, visible and selected without editing data',()=>d.querySelectorAll('#palette-workspace > details.palette-stage[open]').length===1 && d.getElementById('palette-stage-'+key).open && d.querySelector('[data-palette-go="'+key+'"]').getAttribute('aria-current')==='step' && d.activeElement===d.querySelector('#palette-stage-'+key+' > summary') && d.querySelector('#palette-stage-'+key+' .palette-browser > p').textContent.length>80 && evaluate('projectJson()')===snapshot);}
    ui.show('brand',false);d.getElementById('jBrandEditor').closest('details').open=true;
    d.getElementById('jBrandAdd').click();await wait();
    const added=evaluate('state.brandPalette.at(-1).id'),selectedRow=()=>d.querySelector('#jBrandEditor [data-brand-id]:not([hidden])');
    test('Adding a brand colour selects its single visible editable row',()=>d.getElementById('palette-brand-selection').value===added && d.querySelectorAll('#jBrandEditor [data-brand-id]:not([hidden])').length===1 && selectedRow().contains(d.activeElement));
    const name=selectedRow().querySelector('[data-brand-field="name"]');name.value='Harbour <safe> teal';name.dispatchEvent(new w.Event('change',{bubbles:true}));
    const colour=selectedRow().querySelector('[data-brand-field="hex"]');colour.value='#246a68';colour.dispatchEvent(new w.Event('input',{bubbles:true}));await wait();
    test('Selected brand edits update names and tokens safely without duplicating controls',()=>d.getElementById('palette-brand-selection').selectedOptions[0].textContent.includes('Harbour <safe> teal') && !d.querySelector('#palette-workspace safe') && evaluate('cssExport()').includes('--brand-'+added+': #246A68') && d.querySelectorAll('#jBrandEditor').length===1);
    input('jPrimaryBrand','#246A68','change');const secondary=evaluate('state.secondary');
    ui.show('brand',false);ui.selectBrand(added);selectedRow().querySelector('[data-remove-brand]').click();await wait();
    test('Removing a selected reference preserves its copied UI colour and selects an available row',()=>evaluate('state.primary')==='#246a68' && !evaluate('state.brandPalette').some(row=>row.id===added) && selectedRow() && d.activeElement===d.getElementById('jBrandAdd'));
    ui.show('roles',false);d.getElementById('palette-reset-primary').click();await wait();
    test('Reset UI assignment changes only that required role',()=>evaluate('state.primary===DEFAULT.primary') && evaluate('state.secondary')===secondary);
    input('palette-theme','light','change');ui.show('review',false);input('palette-status-role','warning','change');input('palette-status-colour','#654321');await wait();
    input('palette-theme','dark','change');input('palette-status-colour','#aabbcc');await wait();
    test('Feedback colour creates independent overrides in both themes',()=>evaluate('state.semanticOverrides.light.warning')==='#654321' && evaluate('state.semanticOverrides.dark.warning').toUpperCase()==='#AABBCC' && d.getElementById('palette-status-source').textContent.includes('custom override'));
    d.getElementById('palette-status-reset').click();await wait();
    test('Clearing feedback colour removes only the current theme override',()=>!evaluate('state.semanticOverrides.dark.warning') && evaluate('state.semanticOverrides.light.warning')==='#654321');
    for(const region of ['body','header','main','footer']){ui.show('backgrounds',false);input('palette-region-selection',region,'change');test('Background '+region+' exposes just the selected region',()=>[...d.querySelectorAll('.page-background-editor fieldset')].filter(el=>!el.hidden).length===1 && !d.getElementById(region==='body'?'body-background-controls':region+'-background-hex').closest('fieldset').hidden);}
    w.dssConfigureToken({name:'--header-background',scope:'Dark'});await wait();
    test('Configure background selects the correct stage, region and theme before focus',()=>d.getElementById('palette-stage-backgrounds').open && d.getElementById('palette-region-selection').value==='header' && evaluate('state.theme')==='dark' && d.activeElement===d.getElementById('header-background-colour'));
    const preserved=JSON.parse(evaluate('projectJson()'));w.importConfig(preserved);await wait();
    test('Import retains palette data and starts at brand references without modifying settings',()=>d.getElementById('palette-stage-brand').open && evaluate('state.semanticOverrides.light.warning')==='#654321' && !evaluate('state.semanticOverrides.dark.warning'));
    ui.show('review',false);[...d.querySelectorAll('#palette-stage-review button')].find(button=>button.textContent==='Review live website').click();await wait();
    test('Palette review opens the live website and leaves focus at the result',()=>d.getElementById('studio-section-4').open && d.activeElement===d.getElementById('previewShell'));
    [...d.querySelectorAll('#palette-stage-review button')].find(button=>button.textContent==='Check contrast and accessibility').click();await wait();
    test('Palette accessibility review reaches its destination with visible native focus',()=>w.DSStudio.activeStage===10 && d.activeElement===d.querySelector('#studio-section-5 > summary'));
    for(const theme of ['light','dark'])for(const width of [320,390,1440]){
      app.style.width=width+'px';if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(4,false);await wait();
      for(const key of ['brand','roles','shades','semantics','backgrounds','components','review']){ui.show(key,false);await wait();test(theme+' Palette '+key+' controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#palette-stage-'+key+' input,#palette-stage-'+key+' select,#palette-stage-'+key+' button')].filter(el=>el.getBoundingClientRect().height>0).every(el=>{const box=el.getBoundingClientRect();return box.right<=w.innerWidth+1 && box.left>=0 && (el.type==='range'||box.height>=44);}));}
    }
    app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.dssShowWizardStep(4,false);await wait();
  }
  // Complete colour-token flow: semantic sources and component outputs.
  {
    reset();w.dssShowWizardStep(4,false);await wait();const ui=w.DSStudio.paletteWorkspace;
    test('Semantic and component colours follow shade generation in Palette',()=>[...d.querySelectorAll('#palette-workspace > [data-palette-stage]')].map(el=>el.dataset.paletteStage).join(',')==='brand,roles,shades,semantics,backgrounds,components,review' && d.querySelector('[data-journey-step="6"]').textContent.includes('Colour lab'));
    input('tokenSearch','--surface');await wait();
    test('Semantic token catalogue identifies the visible Palette step rather than its internal index',()=>[...d.querySelectorAll('#tokenTableBody tr')].find(row=>row.querySelector('td:nth-child(2) code')?.textContent==='--surface').textContent.includes('wizard step 5'));
    input('tokenSearch','');
    for(const theme of ['light','dark']){
      input('palette-theme',theme,'change');ui.show('components',false);
      for(const family of ['cards','inputs','links','buttons']){input('palette-component-family',family,'change');await wait();test(theme+' '+family+' component colours read the actual exported token values',()=>[...d.querySelectorAll('[data-component-token]')].length>=2 && [...d.querySelectorAll('[data-component-token]')].every(el=>el.textContent===((theme==='dark'?w.dssReadTokens().find(row=>row.name===el.dataset.componentToken && row.scope==='Dark'):null)||w.dssReadTokens().find(row=>row.name===el.dataset.componentToken && row.scope!=='Dark')).value));}
    }
    input('palette-button-variant','secondary','change');input('bdSource','primary');input('bdText','#102030');await wait();
    test('Palette button source and overrides update the existing button settings',()=>evaluate('state.buttonDesign.variant')==='secondary' && evaluate('state.buttonDesign.sources.secondary')==='primary' && evaluate('state.buttonDesign.overrides.secondary.text').toUpperCase()==='#102030' && ['light','dark'].every(theme=>w.dssGetButtonContrastData().themes[theme].secondary.fg.toUpperCase()==='#102030'));
    input('palette-button-variant','primary','change');input('bdText','#aabbcc');input('bdFocus','#445566');input('palette-button-variant','secondary','change');await wait();
    d.getElementById('palette-button-clear').click();await wait();
    test('Clearing component overrides preserves its source, other variants and shared focus',()=>!evaluate('state.buttonDesign.overrides.secondary') && evaluate('state.buttonDesign.sources.secondary')==='primary' && evaluate('state.buttonDesign.overrides.primary.text').toUpperCase()==='#AABBCC' && evaluate('state.buttonDesign.focus').toUpperCase()==='#445566');
    d.getElementById('palette-button-focus-reset').click();await wait();
    test('Shared button focus resets separately from variant overrides',()=>evaluate('state.buttonDesign.focus').toUpperCase()===w.dssGetButtonDefaultContrastColour('secondary','focus').toUpperCase() && evaluate('state.buttonDesign.overrides.primary.text').toUpperCase()==='#AABBCC');
    input('palette-component-family','cards','change');d.querySelector('#palette-component-values button').click();await wait();
    test('Component semantic source opens Palette role editing with focus',()=>w.DSStudio.activeStage===4 && d.getElementById('palette-stage-semantics').open && d.getElementById('jSemanticRole').value==='surface' && d.activeElement===d.getElementById('jSemanticRole'));
    w.dssConfigureToken({name:'--button-outline-hover',scope:'Dark'});await wait();
    test('Button token source opens the component family and correct variant before focus',()=>w.DSStudio.activeStage===4 && d.getElementById('palette-stage-components').open && d.getElementById('palette-component-family').value==='buttons' && d.getElementById('palette-button-variant').value==='outline' && d.activeElement===d.getElementById('bdHover'));
    const savedColours=JSON.parse(evaluate('projectJson()'));w.importConfig(savedColours);await wait();
    test('Colour-flow editing round trips through the existing project schema',()=>evaluate('state.buttonDesign.sources.secondary')==='primary' && evaluate('state.buttonDesign.overrides.primary.text').toUpperCase()==='#AABBCC' && !Object.hasOwn(JSON.parse(evaluate('projectJson()')),'paletteWorkspace'));
    for(const width of [320,390,1440]){app.style.width=width+'px';await wait();for(const variant of ['primary','secondary','accent','outline','text']){w.dssConfigureToken({name:'--button-'+variant+'-bg',scope:'Light / base'});await wait();test(variant+' expanded component colour controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#palette-button-colours input,#palette-button-colours select,#palette-button-colours button')].filter(el=>el.getBoundingClientRect().height>0).every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.right<=w.innerWidth+1;}));}}
    app.style.width='1440px';reset();await wait();
  }
  // Palette visibility helpers must preserve unrelated lessons and focus.
  {
    reset();w.dssShowWizardStep(3,false);await wait();const prototype=d.getElementById('studio-plan-choose'),link=prototype.querySelector('a');for(let node=link.parentElement;node;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;link.focus();input('jPrimary','#225577');await wait();
    test('Background palette updates preserve the prototype lesson, nodes and focus',()=>w.DSStudio.activeStage===3 && d.getElementById('studio-plan-choose')===prototype && d.activeElement===link);
    w.dssShowWizardStep(7,false);d.getElementById('bdReview').open=true;const review=d.querySelector('[data-review-variant="secondary"][data-review-state="hover"]');review.closest('details').open=true;review.focus();review.click();await wait();input('bdHover','#ffffff');input('bdHoverText','#ffffff');await wait();
    test('Background button-colour updates keep the existing contrast review focused',()=>w.DSStudio.activeStage===7 && d.activeElement===review && review.closest('details').open);
    const edit=d.querySelector('#bdReviewPairs [aria-label="Light theme contrast"] [data-kind="text"] button');edit.focus();edit.click();input('repairHex','#101820');d.getElementById('repairCancel').click();await wait();
    test('Contrast dialog cancel still returns to its visible review action',()=>d.activeElement===edit && !d.getElementById('colourRepair').open);
    w.dssConfigureToken({name:'--text',scope:'Dark'});await wait();test('Explicit semantic source navigation still activates Palette',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('jSemanticRole'));
    w.dssConfigureToken({name:'--button-secondary-hover-text',scope:'Dark'});await wait();test('Explicit component source navigation still reveals and focuses its colour field',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('bdHoverText') && !d.getElementById('palette-button-colours').hidden);
    w.dssShowWizardStep(7,false);d.getElementById('brandPalette').open=true;w.DSStudio.paletteWorkspace.show('components',false);input('palette-component-family','buttons','change');await wait();test('Manually expanded Palette refreshes component values without forcing the builder step',()=>w.DSStudio.activeStage===7 && d.querySelectorAll('[data-component-token]').length===8 && !d.getElementById('palette-component-values').textContent.includes('Not available'));
    d.getElementById('dockModeBasic').click();input('bdVariant','primary');input('bdDefaultBg','#602d54');await wait();test('Unrelated button-colour changes retain the connected action example',()=>w.DSStudio.activeStage===7 && d.getElementById('studyExample').value==='action' && d.getElementById('studyTokens').textContent.toLowerCase().includes('#602d54'));
    reset();await wait();
  }
  // End Palette visibility preservation checks.
  // End complete colour-token flow checks.
  // End guided Palette checks.
  // Start this fixture in its own visible lesson rather than inheriting the
  // previous background-update tests' manually expanded Palette disclosure.
  w.dssRevealSection('jBrandEditor',false); await wait();
  const brandSelect=role=>d.getElementById('j'+role[0].toUpperCase()+role.slice(1)+'Brand');
  const brandField=(id,field)=>d.querySelector(`[data-brand-id="${id}"] [data-brand-field="${field}"]`);
  const editBrand=(id,field,value)=>{const el=brandField(id,field);w.DSStudio.paletteWorkspace?.revealControl(el);el.value=value;el.dispatchEvent(new w.Event(field==='name'?'change':'input',{bubbles:true}));};
  test('Guided Brand Palette lists all starter colours and all three role dropdowns', () => d.querySelectorAll('#jBrandSwatches li').length===11 && ['primary','secondary','accent'].every(role=>brandSelect(role).options.length===12 && [...brandSelect(role).options].slice(1).every(option=>/^#[0-9A-F]{6}$/.test(option.value) && option.textContent.includes(option.value))));
  for (const [role,hex] of [['primary','#00BADC'],['secondary','#F37327'],['accent','#004780']]) {
    input(brandSelect(role).id,hex,'change'); await wait();
    test('Brand selection updates '+role+' across main and guided controls and live CSS', () => evaluate(`state.${role}`)===hex.toLowerCase() && d.getElementById(role).value===hex.toLowerCase() && d.getElementById('j'+role[0].toUpperCase()+role.slice(1)).value===hex.toLowerCase() && previewDoc().getElementById('dssPreviewStyles').textContent.includes('--'+role+'-500: '+hex));
  }
  input('jSecondary','#123456'); await wait();
  test('Manual role colours remain available and show Custom in the brand dropdown', () => brandSelect('secondary').value==='' && evaluate('state.secondary')==='#123456');
  input('primary','#F37327'); await wait();
  test('Advanced role edits synchronize the matching guided brand choice', () => brandSelect('primary').value==='#F37327');
  d.getElementById('jBrandEditor').closest('details').open=true;
  d.getElementById('jBrandAdd').click(); await wait();
  test('Adding a named brand colour offers an editable focused row', () => {
    const field=brandField('colour-1','name');
    if(evaluate('state.brandPalette.length')!==12 || d.activeElement!==field){
      const disclosures=[];for(let node=field;node;node=node.parentElement)if(node.tagName==='DETAILS')disclosures.push({id:node.id,open:node.open});
      throw Error(JSON.stringify({count:evaluate('state.brandPalette.length'),stage:w.DSStudio.activeStage,active:d.activeElement?.id||d.activeElement?.outerHTML.slice(0,160),disclosures}));
    }
    return true;
  });
  editBrand('colour-1','name','Harbour teal');
  const mainBeforeBrandEdit=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
  const stableBrandPicker=brandField('colour-1','hex'); stableBrandPicker.focus();
  editBrand('colour-1','hex','#246a68'); await wait();
  test('Editing a brand reference preserves Main Palette choices and editor focus', () => evaluate('JSON.stringify([state.primary,state.secondary,state.accent])')===mainBeforeBrandEdit && brandField('colour-1','hex')===stableBrandPicker && d.activeElement===stableBrandPicker);
  test('Custom brand colours reach dropdowns, reference swatches, export and contrast candidates', () => ['primary','secondary','accent'].every(role=>[...brandSelect(role).options].some(option=>option.value==='#246A68' && option.textContent.includes('Harbour teal'))) && d.getElementById('brandSwatches').textContent.includes('Harbour teal') && evaluate('cssExport()').includes('--brand-colour-1: #246A68') && report().some(row=>row.name==='Brand: Harbour teal (--brand-colour-1) / white text' && row.bg==='#246A68'));
  input('jAccentBrand','#246A68','change'); d.getElementById('jSaveLocal').click();
  const brandProjectId=d.getElementById('jProjects').value;
  editBrand('blue','hex','#224488'); await wait();
  test('Brand palette edits autosave without overwriting independent role choices', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[brandProjectId].data.brandPalette.find(item=>item.id==='blue').hex==='#224488' && evaluate('state.accent')==='#246a68');
  const brandedProject=evaluate('projectJson()');
  reset(); evaluate('importConfig('+brandedProject+')'); await wait();
  test('Brand palette names, token IDs, colours and role selections survive JSON round trip', () => evaluate('state.brandPalette.length')===12 && brandField('colour-1','name').value==='Harbour teal' && brandSelect('accent').value==='#246A68' && evaluate('cssExport()').includes('--brand-blue: #224488'));
  d.querySelector('[data-remove-brand="colour-1"]').click(); await wait();
  test('Removing a selected brand reference keeps its UI colour and removes obsolete exports', () => evaluate('state.accent')==='#246a68' && brandSelect('accent').value==='' && !evaluate('cssExport()').includes('--brand-colour-1:') && !report().some(row=>row.name.includes('--brand-colour-1')) && d.activeElement.id==='jBrandAdd');
  evaluate('importConfig({primary:"#123456",secondary:"#456789",accent:"#987654"})'); await wait();
  test('Older projects receive starter brand references while retaining custom Main Palette colours', () => evaluate('state.brandPalette.length===11 && state.primary==="#123456" && state.secondary==="#456789" && state.accent==="#987654"') && ['primary','secondary','accent'].every(role=>brandSelect(role).value===''));
  evaluate('importConfig({brandPalette:[{id:"safe",name:"<img src=x onerror=alert(1)>",hex:"#abcdef"},{id:"bad;css",name:"Bad",hex:"#ffffff"},{id:"badhex",name:"Bad",hex:"red;position:fixed"},{id:"safe",name:"Duplicate",hex:"#000000"}]})'); await wait();
  test('Imported brand palettes reject duplicate IDs, CSS injection and invalid colours', () => evaluate('state.brandPalette.length===1 && state.brandPalette[0].id==="safe" && state.brandPalette[0].hex==="#ABCDEF"') && evaluate('cssExport()').includes('--brand-safe: #ABCDEF') && !evaluate('cssExport()').includes('--brand-bad'));
  test('Imported brand names are rendered as text in every palette surface', () => d.getElementById('jBrandSwatches').textContent.includes('<img') && !d.querySelector('#jBrandSwatches img, #brandSwatches img') && [...brandSelect('primary').options].some(option=>option.textContent.includes('<img')));
  test('The final remaining brand colour cannot be removed', () => d.querySelector('[data-remove-brand="safe"]').disabled);
  evaluate('importConfig({brandPalette:[{id:"one",name:"primary-500",hex:"#123456"},{id:"two",name:"primary-500",hex:"#654321"}]})'); await wait();
  test('Duplicate brand names retain unique contrast identities and cannot impersonate ramp anchors', () => {
    const rows=report().filter(row=>row.name.startsWith('Brand: primary-500'));
    return rows.length===8 && new Set(rows.map(row=>row.id)).size===8 && rows.every(row=>row.targets.every(target=>target.type!=='anchor'));
  });
  evaluate('importConfig({brandPalette:Array.from({length:30},(_,i)=>({id:"test-"+i,name:"A".repeat(90),hex:"#123456"}))})'); await wait();
  test('Imported palettes enforce 24 colours and bounded names', () => evaluate('state.brandPalette.length===24 && state.brandPalette.every(item=>item.name.length===40)') && d.getElementById('jBrandAdd').disabled);
  for (const theme of ['light','dark']) {
    app.style.width='320px'; input('jTheme',theme); d.querySelector('[data-journey-step="4"]').click();
    d.getElementById('jBrandEditor').closest('details').open=true; await wait();
    test('Brand editing and role dropdowns fit '+theme+' 320px layouts', () => [d.getElementById('jBrandEditor'),d.getElementById('jBrandSwatches'),...['primary','secondary','accent'].map(brandSelect)].every(el=>el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset restores starter Brand Palette and Main Palette choices', () => evaluate('state.brandPalette.length===11') && brandSelect('primary').value==='#004780' && brandSelect('secondary').value==='#495965' && brandSelect('accent').value==='#CBDB2A');
  d.getElementById('brandPalette').open=true;w.DSStudio.paletteWorkspace.revealControl(d.getElementById('brandApplyRole'));
  const swatch=id=>d.querySelector(`[data-brand-swatch="${id}"]`);
  test('Brand Colour Palette names its purpose and replaces the whole-project reset with editing', () => d.querySelector('#brandPalette > summary h2').textContent==='Step 5 of 12: Palette' && !d.getElementById('restoreDefaults') && d.getElementById('brandEditPalette').textContent==='Edit Brand Palette');
  test('Every brand swatch has one complete clickable card with an explicit role action', () => d.querySelectorAll('#brandSwatches .brand-swatch').length===11 && [...d.querySelectorAll('#brandSwatches .brand-swatch')].every(card=>card.querySelectorAll('button').length===1 && !!card.querySelector('button .brand-swatch-color') && card.querySelector('button').getAttribute('aria-label').startsWith('Set Primary UI colour to') && d.getElementById(card.querySelector('button').getAttribute('aria-describedby'))===card.querySelector('[data-brand-usage]')));
  const beforeRoleChoice=evaluate('projectJson()'); input('brandApplyRole','secondary','change'); await wait();
  test('Choosing a target role prepares every card without changing project colours', () => evaluate('projectJson()')===beforeRoleChoice && [...d.querySelectorAll('#brandSwatches button')].every(button=>button.dataset.brandRole==='secondary' && button.textContent.includes('Set as Supporting colour')));
  d.getElementById('jSaveLocal').click(); const swatchProjectId=d.getElementById('jProjects').value;
  const roleLabels={primary:'Primary UI colour',secondary:'Supporting colour',accent:'Accent colour'};
  for (const [role,id,hex] of [['primary','accent-orange','#F37327'],['secondary','white','#FFFFFF'],['accent','blue','#004780']]) {
    input('brandApplyRole',role,'change');
    const priorRoles=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
    const beforeSwatchPalette=evaluate('JSON.stringify(state.brandPalette)');
    const action=swatch(id).querySelector('button'); action.focus();
    // Click the colour block itself, rather than only the text label.
    swatch(id).querySelector('.brand-swatch-color').click(); await wait();
    test('Any swatch can set '+role+' and visibly confirm its assignment', () => evaluate(`state.${role}`)===hex.toLowerCase() && swatch(id).querySelector('[data-brand-usage]').textContent.includes(roleLabels[role]) && swatch(id).dataset.current==='true' && d.getElementById('brandFeedback').textContent.includes(roleLabels[role]+' set to') && d.getElementById('brandFeedback').textContent.includes(hex));
    test(role+' swatch updates preserve other roles, brand references and keyboard focus', () => {
      const prior=JSON.parse(priorRoles),after=JSON.parse(evaluate('JSON.stringify([state.primary,state.secondary,state.accent])'));
      return ['primary','secondary','accent'].every((key,i)=>key===role || prior[i]===after[i]) && evaluate('JSON.stringify(state.brandPalette)')===beforeSwatchPalette && swatch(id).querySelector('button')===action && d.activeElement===action;
    });
    test(role+' swatch stays synchronized with summary, guided controls, preview and local save', () => d.getElementById('brandCurrent'+role[0].toUpperCase()+role.slice(1)).textContent.includes(hex) && brandSelect(role).value===hex && previewWindow().getComputedStyle(previewDoc().documentElement).getPropertyValue('--button-'+role+'-bg').trim().toUpperCase()===hex && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[swatchProjectId].data[role]===hex.toLowerCase());
  }
  input('brandApplyRole','secondary','change'); d.getElementById('brandFeedback').textContent=''; swatch('blue').querySelector('[data-brand-usage]').click(); await wait();
  test('Clicking the usage footer applies the swatch just like its colour and label', () => evaluate('state.secondary')==='#004780' && d.getElementById('brandFeedback').textContent.includes('Supporting colour set to Deep blue'));
  const beforeEditShortcut=evaluate('projectJson()'); d.getElementById('brandEditPalette').click(); await wait();
  test('Edit Brand Palette opens the guided editor, focuses its name control and preserves the project', () => !d.querySelector('[data-journey-pane="4"]').hidden && d.getElementById('jBrandEditor').closest('details').open && d.activeElement===d.getElementById('jBrandEditor').querySelector('input') && evaluate('projectJson()')===beforeEditShortcut);
  const existingBlueCard=swatch('blue'); editBrand('blue','name','Harbour blue'); await wait();
  test('Renaming a brand reference updates cards and current assignments without recreating controls', () => swatch('blue')===existingBlueCard && swatch('blue').querySelector('strong').textContent==='Harbour blue' && d.getElementById('brandCurrentAccent').textContent.includes('Harbour blue'));
  input('brandApplyRole','primary','change'); input('jPrimary','#13579b'); await wait();
  test('Custom role edits clear current-card styling and update the visible summary', () => d.getElementById('brandCurrentPrimary').textContent==='Custom colour · #13579B' && !d.querySelector('#brandSwatches [data-current="true"]'));
  input('jPrimary','#004780'); await wait();
  test('Guided dropdowns and swatch cards reflect the same current colour', () => swatch('blue').dataset.current==='true' && swatch('blue').querySelector('[data-brand-usage]').textContent.includes('Primary UI colour') && swatch('blue').querySelector('[data-brand-usage]').textContent.includes('Accent colour'));
  for (const theme of ['light','dark']) {
    app.style.width='320px'; input('jTheme',theme); await wait();
    test('Swatch actions and current role summaries fit '+theme+' 320px layouts', () => [d.getElementById('palette-anchor-selection'),d.getElementById('brandApplyRole'),...d.querySelectorAll('#brandSwatches .brand-swatch')].every(el=>el.getBoundingClientRect().width>0 && el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset restores the swatch target and current-role feedback', () => d.getElementById('brandApplyRole').value==='primary' && d.getElementById('brandCurrentPrimary').textContent.includes('#004780') && swatch('blue').dataset.current==='true');
  // Inline state colours edit/reset existing sources, with mirrored defaults.
  reset();app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  const stateColour=(view,key)=>d.querySelector('#interaction-palette-'+view+' [data-state-colour="'+key+'"]');
  input('interaction-palette-controls-component','general','change');
  d.getElementById('jSaveLocal').click();const inlineSavedId=d.getElementById('jProjects').value;
  const hoverColour=stateColour('lesson','hover'),hoverCard=hoverColour.closest('details');w.DSStudio.paletteWorkspace.revealControl(hoverColour);hoverCard.open=true;hoverColour.focus();
  const originalDarkHover=evaluate('palette("dark").roles["primary-hover"]');
  hoverColour.value='#00BADC';hoverColour.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Inline semantic state colour keeps focus/disclosure, mirrors controls, autosaves and edits only its theme',()=>d.activeElement===hoverColour && hoverCard.open && stateColour('controls','hover').value==='#00BADC' && evaluate('state.semanticOverrides.light["primary-hover"]')==='#00BADC' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[inlineSavedId].data.semanticOverrides.light['primary-hover']==='#00BADC' && evaluate('palette("dark").roles["primary-hover"]')===originalDarkHover && d.querySelector('#interaction-palette-lesson [data-interaction-state="hover"] [data-shade="500"]').textContent.includes('#00BADC'));
  input(hoverColour.id,'default','change');await wait();
  test('Inline Default removes a semantic override and restores its generated source colour',()=>!evaluate('state.semanticOverrides.light["primary-hover"]') && stateColour('lesson','hover').value==='default' && stateColour('lesson','hover').options[0].textContent.includes(evaluate('palette().roles["primary-hover"]').toUpperCase()));
  input(stateColour('lesson','invalid').id,'#00BADC','change');input(stateColour('controls','readonly').id,'#CBDB2A','change');await wait();
  test('Invalid and read-only dropdowns update their actual feedback/surface sources',()=>evaluate('state.semanticOverrides.light.danger')==='#00BADC' && evaluate('state.semanticOverrides.light["surface-muted"]')==='#CBDB2A' && d.querySelector('#status-palette-ramp-lessons [data-palette-role="danger"] [data-shade="500"]').textContent.includes('#00BADC'));
  const inlineProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(inlineProject)+')');await wait();
  test('Inline state colour choices survive JSON round-trip using existing saved fields',()=>stateColour('lesson','invalid').value==='#00BADC' && stateColour('controls','readonly').value==='#CBDB2A' && !Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/statePalette/i.test(key)));
  input('interaction-palette-controls-component','primary','change');
  input(stateColour('lesson','hover').id,'#00BADC','change');input(stateColour('controls','active').id,'#CBDB2A','change');await wait();
  test('Button hover and pressed dropdowns update separate real component properties in both themes',()=>['light','dark'].every(theme=>{const data=w.dssGetButtonContrastData().themes[theme].primary;return data.hover==='#00BADC' && data.active==='#CBDB2A';}) && stateColour('controls','hover').value==='#00BADC' && stateColour('lesson','active').value==='#CBDB2A');
  input(stateColour('lesson','hover').id,'default','change');await wait();
  test('Default removes only the selected button property override',()=>!evaluate('state.buttonDesign.overrides.primary.hover') && evaluate('state.buttonDesign.overrides.primary.active')==='#CBDB2A' && stateColour('controls','hover').value==='default');
  input(stateColour('lesson','default').id,'#00BADC','change');await wait();
  test('Shared button base dropdowns synchronize default, disabled and loading and explain the scope',()=>['default','disabled','loading'].every(key=>stateColour('lesson',key).value==='#00BADC') && d.getElementById(stateColour('lesson','default').getAttribute('aria-describedby')).textContent.includes('Disabled, Loading'));
  input(stateColour('controls','focus').id,'#00BADC','change');await wait();
  test('Focus dropdown updates the shared focus/selected source across variants',()=>w.DSStudio.statePalettes.variants.every(variant=>w.DSStudio.statePalettes.entries('light',variant).filter(entry=>['focus','selected'].includes(entry.key)).every(entry=>entry.anchor==='#00BADC')) && stateColour('lesson','selected').value==='#00BADC');
  input(stateColour('lesson','selected').id,'default','change');await wait();
  test('Focus Default restores the button default without changing other properties',()=>evaluate('state.buttonDesign.focus')==='#B86C20' && evaluate('state.buttonDesign.overrides.primary.active')==='#CBDB2A' && stateColour('controls','focus').value==='default');
  input('interaction-palette-lesson-component','outline','change');input(stateColour('lesson','default').id,'#00BADC','change');await wait();
  test('Transparent state dropdown edits its foreground while retaining a transparent background',()=>w.dssGetButtonContrastData().themes.light.outline.bg==='transparent' && w.dssGetButtonContrastData().themes.light.outline.fg==='#00BADC' && stateColour('controls','disabled').value==='#00BADC');
  input(stateColour('controls','default').id,'default','change');await wait();
  test('Transparent state Default removes the foreground override',()=>!evaluate('state.buttonDesign.overrides.outline.text') && stateColour('lesson','default').value==='default');
  const beforeInvalidStateChoice=evaluate('projectJson()');input(stateColour('lesson','hover').id,'not-a-colour','change');await wait();
  test('Inline state dropdown rejects unsupported values without changing project data',()=>evaluate('projectJson()')===beforeInvalidStateChoice);
  // Every general/button interaction state exposes shades from its resolved source.
  reset();w.dssShowWizardStep(4);await wait();
  const interactionGroups=['general','primary','secondary','accent','outline','text'];
  const interactionStates=['default','hover','focus','active','selected','disabled','loading','invalid','success','readonly'];
  for(const method of ['mix','oklch']) for(const theme of ['light','dark']) {
    input('jRamp',method);input('jTheme',theme);await wait();
    const allStateTokens=w.dssReadTokens();
    for(const group of interactionGroups) {
      const beforeStatePaletteView=evaluate('projectJson()');
      input('interaction-palette-controls-component',group,'change');await wait();
      const entries=w.DSStudio.statePalettes.entries(theme,group);
      test(method+' '+theme+' '+group+' has every state, eleven exported shades and a configuration source',()=>entries.length===(group==='general'?10:7) && entries.every(entry=>{
        const expected=evaluate('makeRamp('+JSON.stringify(entry.anchor)+',state.method)');
        return Array.from({length:11},(_,i)=>[50,100,200,300,400,500,600,700,800,900,950][i]).every(step=>{
          const token=allStateTokens.find(token=>token.name===entry.prefix+'-'+step && (token.scope==='Dark')===(theme==='dark'));
          return token && token.value===expected[step] && w.dssTokenSource(token)?.control===entry.control;
        });
      }));
      test(method+' '+theme+' '+group+' mirrored state lessons show actual CSS and preserve project data',()=>['interaction-palette-controls','interaction-palette-lesson'].every(id=>d.getElementById(id+'-component').value===group && [...d.querySelectorAll('#'+id+' [data-interaction-state]')].length===entries.length && entries.every(entry=>{
        const card=d.querySelector('#'+id+' [data-interaction-state="'+entry.key+'"]');
        return card.querySelectorAll('[data-shade]').length===11 && card.querySelector('[data-shade="500"]').textContent.includes(entry.prefix+'-500: '+entry.anchor+';');
      })) && evaluate('projectJson()')===beforeStatePaletteView);
      test(method+' '+theme+' '+group+' gives every state a labelled Default and brand colour dropdown',()=>['controls','lesson'].every(view=>entries.every(entry=>{const select=stateColour(view,entry.key);return select && d.querySelector('label[for="'+select.id+'"]') && d.getElementById(select.getAttribute('aria-describedby')) && select.options[0].value==='default' && [...select.options].some(option=>option.value==='#00BADC');})));
    }
  }
  input('interaction-palette-controls-component','outline','change');await wait();
  test('Transparent variant state ramps explicitly use the foreground source',()=>['default','disabled','loading'].every(key=>{
    const entry=w.DSStudio.statePalettes.entries('dark','outline').find(entry=>entry.key===key);
    return entry.source==='--button-outline-text' && entry.control==='bdText' && entry.cue.includes('transparent') && d.querySelector('#interaction-palette-lesson [data-interaction-state="'+key+'"]').textContent.includes('transparent');
  }));
  evaluate('dssSetButtonContrastColour("outline","bg","#3a5b7c")');await wait();
  test('Button overrides regenerate state ramps and update transparent-source routing without stale views',()=>{
    const entry=w.DSStudio.statePalettes.entries('dark','outline').find(entry=>entry.key==='default');
    return entry.anchor==='#3A5B7C' && entry.source==='--button-outline-bg' && entry.control==='bdDefaultBg' && d.querySelector('#interaction-palette-lesson [data-interaction-state="default"] [data-shade="500"]').textContent.includes('#3A5B7C') && w.dssTokenSource({name:entry.prefix+'-500',scope:'Dark'}).control==='bdDefaultBg';
  });
  d.querySelector('#interaction-palette-lesson [data-interaction-state="default"] button').click();await wait();
  test('Interaction shade inspector contains the complete current stylesheet and preview uses it',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  d.querySelector('#interaction-palette-lesson [data-interaction-state="hover"] button:last-child').click();await wait();
  test('Button state shade configure reaches the correct variant and property',()=>w.DSStudio.activeStage===4 && d.getElementById('bdVariant').value==='outline' && d.activeElement===d.getElementById('bdHover'));
  w.dssShowWizardStep(4);input('interaction-palette-controls-component','general','change');await wait();
  const generalDisclosure=d.querySelector('#interaction-palette-controls [data-interaction-state="readonly"]');generalDisclosure.open=true;
  input('jTheme','light');await wait();
  test('General state theme changes preserve disclosure nodes and include all State Explorer states',()=>generalDisclosure===d.querySelector('#interaction-palette-controls [data-interaction-state="readonly"]') && generalDisclosure.open && [...d.getElementById('advState').options].every(option=>interactionStates.includes(option.value)));
  d.querySelector('#interaction-palette-lesson [data-interaction-state="invalid"] button:last-child').click();await wait();
  test('Invalid state shade configure reaches the current theme Danger semantic colour',()=>w.DSStudio.activeStage===4 && d.getElementById('jSemanticRole').value==='danger' && evaluate('state.theme')==='light');
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    d.querySelectorAll('#interaction-palette-controls details, #interaction-palette-lesson details').forEach(el=>el.open=true);
    test('All expanded interaction state ramps fit '+width+'px with usable component and colour selectors',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['interaction-palette-controls','interaction-palette-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1 && d.getElementById(id+'-component').getBoundingClientRect().height>=44 && [...el.querySelectorAll('[data-state-colour]')].every(select=>select.getBoundingClientRect().height>=44);}));
  }
  const stableCatalogueRow=d.querySelector('#tokenTableBody tr');w.dssUpdateTokenCatalogue();
  test('Unchanged state exports retain catalogue rows instead of rebuilding the large table',()=>d.querySelector('#tokenTableBody tr')===stableCatalogueRow);
  input('tokenSearch','');const stableBrandCatalogueRow=d.querySelector('#tokenTableBody tr');input('jBase',19);await wait();
  test('Editing one foundation token refreshes its catalogue value while reusing unaffected rows',()=>d.querySelector('#tokenTableBody tr')===stableBrandCatalogueRow && d.querySelector('[data-token-name="--font-size-base"]').closest('tr').textContent.includes('19px'));
  // Status ramps reuse resolved theme colours and the exported shade generator.
  reset();w.dssShowWizardStep(4);await wait();
  for(const method of ['mix','oklch']) for(const theme of ['light','dark']) {
    input('jRamp',method);input('jTheme',theme);await wait();
    test(method+' '+theme+' status ramps preserve semantic anchors and match preview/export',()=>evaluate(`
      STATUS_PALETTE_ROLES.every(role=>{
        const anchor=palette('${theme}').roles[role],ramp=makeRamp(anchor,state.method);
        return steps.every(step=>cssExport().includes('--'+role+'-'+step+': '+ramp[step]+';')) && ramp[500]===anchor;
      })`) && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
    test(method+' '+theme+' status teaching reads all eleven theme-specific exported steps',()=>['status-palette-steps','status-palette-ramp-lessons'].every(id=>['success','warning','danger'].every(role=>{
      const rows=[...d.querySelectorAll('#'+id+' [data-palette-role="'+role+'"] [data-shade]')];
      const tokens=w.dssReadTokens().filter(row=>(row.scope==='Dark')===(theme==='dark'));
      return rows.length===11 && rows.every(row=>row.textContent.includes('--'+role+'-'+row.dataset.shade+': '+tokens.find(token=>token.name==='--'+role+'-'+row.dataset.shade).value+';'));
    })) && d.getElementById('status-palette-theme').textContent.includes(theme==='dark'?'Dark':'Light'));
  }
  evaluate('state.semanticOverrides={light:{success:"#246840",warning:"#784500",danger:"#903344"},dark:{success:"#88DDAA",warning:"#EECC77",danger:"#EE8899"}};apply();renderCode()');await wait();
  test('Status overrides regenerate each theme independently and catalogue routes to the semantic source',()=>['light','dark'].every(theme=>['success','warning','danger'].every(role=>{
    const token=w.dssReadTokens().find(row=>row.name==='--'+role+'-500' && (row.scope==='Dark')===(theme==='dark'));
    const source=w.dssTokenSource(token);
    return token.value===evaluate('state.semanticOverrides.'+theme+'.'+role) && token.type==='Colour ramp' && source.step===4 && source.semantic===role && source.control==='jSemanticRole';
  })));
  d.querySelector('#status-palette-steps [data-palette-role="danger"] button').click();await wait();
  test('Status shade inspection opens complete synchronized CSS',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true');
  const statusBeforeConfigure=evaluate('projectJson()');
  d.querySelector('#status-palette-steps [data-palette-role="warning"] .button-row button:last-child').click();await wait();
  test('Status configuration reaches the correct theme role without changing project data',()=>w.DSStudio.activeStage===4 && d.getElementById('jSemanticRole').value==='warning' && evaluate('state.theme')==='dark' && evaluate('projectJson()')===statusBeforeConfigure);
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    d.querySelectorAll('#status-palette-steps details, #status-palette-ramp-lessons details').forEach(el=>el.open=true);
    test('Expanded status steps fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['status-palette-steps-controls','status-palette-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  // Palette process: explicit token names, exported ramps and final Prototype.
  reset();app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  d.getElementById('jBrandEditor').closest('details').open=true;
  const tokenField=()=>d.querySelector('[data-brand-id="blue"] [data-brand-field="id"]');
  const beforeTokenRoles=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
  const displayName=d.querySelector('[data-brand-id="blue"] [data-brand-field="name"]');
  displayName.value='Ocean blue';displayName.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Colour display names remain independent of brand token names',()=>tokenField().value==='blue' && evaluate('cssExport()').includes('--brand-blue: #004780'));
  const stableTokenInput=tokenField();w.DSStudio.paletteWorkspace.revealControl(stableTokenInput);stableTokenInput.focus();stableTokenInput.value='ocean-blue';stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Token rename updates exports, teaching surfaces and catalogue while retaining focus and copied roles',()=>d.activeElement===stableTokenInput && d.querySelector('[data-brand-id="ocean-blue"] [data-brand-field="id"]')===stableTokenInput && evaluate('cssExport()').includes('--brand-ocean-blue: #004780') && !evaluate('cssExport()').includes('--brand-blue:') && d.getElementById('palette-brand-token-list').textContent.includes('--brand-ocean-blue: #004780;') && w.dssReadTokens().some(row=>row.name==='--brand-ocean-blue') && evaluate('JSON.stringify([state.primary,state.secondary,state.accent])')===beforeTokenRoles);
  for(const invalid of ['white','Bad name','x;--evil','']) {
    stableTokenInput.value=invalid;stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
    test('Token suffix rejects '+JSON.stringify(invalid)+' without changing saved data',()=>!stableTokenInput.validity.valid && evaluate('state.brandPalette.some(item=>item.id==="ocean-blue")') && evaluate('cssExport()').includes('--brand-ocean-blue: #004780'));
  }
  stableTokenInput.value='ocean-blue';stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));
  d.getElementById('jSaveLocal').click();const tokenProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(tokenProject)+')');await wait();
  test('Token suffix survives project JSON import and local storage',()=>d.querySelector('[data-brand-id="ocean-blue"] [data-brand-field="id"]').value==='ocean-blue' && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>project.data.brandPalette.some(item=>item.id==='ocean-blue')));
  test('Palette sequence puts Main Palette generation before backgrounds, then interaction state steps in both panes',()=>{
    const pairs=[[d.getElementById('jRamp'),d.getElementById('palette-steps-controls')],[d.getElementById('palette-steps-controls'),d.querySelector('.page-background-editor')],[d.getElementById('palette-token-lesson'),d.getElementById('webpage-background-lesson')],[d.querySelector('.page-background-editor'),d.getElementById('interaction-palette-controls')],[d.getElementById('webpage-background-lesson'),d.getElementById('interaction-palette-lesson')]];
    return pairs.every(([before,after])=>Boolean(before.compareDocumentPosition(after)&w.Node.DOCUMENT_POSITION_FOLLOWING));
  });
  for(const method of ['mix','oklch']) for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) {
    for(const [role,hex] of (method==='mix'?[['primary','#004780'],['secondary','#495965'],['accent','#CBDB2A']]:[['primary','#00BADC'],['secondary','#F37327'],['accent','#EF426F']])) input('j'+role[0].toUpperCase()+role.slice(1)+'Brand',hex,'change');
    input('jRamp',method);d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);await wait();
    test(method+' '+mode+' '+theme+' all Main Palette shade steps match exported tokens',()=>evaluate('state.method')===method && ['primary','secondary','accent'].every(role=>{
      const rows=[...d.querySelectorAll('#palette-ramp-lessons [data-palette-role="'+role+'"] [data-shade]')];
      const tokens=w.dssReadTokens();return rows.length===11 && rows.every(row=>row.textContent.includes('--'+role+'-'+row.dataset.shade+': '+tokens.find(token=>token.name==='--'+role+'-'+row.dataset.shade).value+';')) && rows.find(row=>row.dataset.shade==='500').textContent.includes(evaluate('state.'+role).toUpperCase()) && rows.find(row=>row.dataset.shade==='500').dataset.anchor==='true';
    }));
    test(method+' '+mode+' '+theme+' semantic explanation follows both exported themes',()=>['primary','secondary','accent'].every(role=>{
      const text=d.querySelector('#palette-ramp-lessons [data-palette-role="'+role+'"] .palette-token-chain').textContent;
      const tokens=w.dssReadTokens().filter(token=>token.name==='--'+role);return tokens.every(token=>text.includes('--'+role+': '+token.value+';')) && text.includes('generated from --'+role+'-'+(role==='secondary'?700:500)) && text.includes('generated from --'+role+'-300');
    }));
  }
  input('jPrimaryBrand','#004780','change');evaluate('state.semanticOverrides={light:{primary:"#123456"},dark:{}};apply()');await wait();
  test('Palette lesson distinguishes semantic overrides from generated shade values',()=>d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] .palette-token-chain').textContent.includes('--primary: #123456; (custom semantic override)') && d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] [data-shade="500"]').textContent.includes('#004780'));
  d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] button').click();await wait();
  test('Palette shade inspection shows complete current CSS',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true');
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();d.getElementById('jBrandEditor').closest('details').open=true;d.querySelectorAll('#main-palette-steps details').forEach(el=>el.open=true);
    test('Palette token teaching and expanded ramps fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['palette-steps-controls','palette-token-lesson','jBrandEditor'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();w.dssShowWizardStep(4);await wait();
  const resetTokenInput=d.querySelector('[data-brand-id="blue"] [data-brand-field="id"]');w.DSStudio.paletteWorkspace.revealControl(resetTokenInput);resetTokenInput.focus();resetTokenInput.value='white';resetTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));reset();await wait();
  test('Reset restores token suffix values and clears stale validation while retaining editor focus',()=>resetTokenInput.value==='blue' && resetTokenInput.validity.valid && d.activeElement===resetTokenInput);
  w.dssShowWizardStep(0,false);await wait();
  const beforeOrderedWalk=evaluate('projectJson()');
  test('Centre lessons follow wizard order immediately after the unchanged preview',()=>[...d.querySelectorAll('#main > .studio-section')].slice(1,13).every((section,position)=>section.id===w.DSStudio.orderedStages[position].lesson));
  for(const [position,index] of w.DSStudio.stageOrder.entries()) {
    if(position)d.getElementById('jNext').click();await wait();
    test('Next follows stage '+(position+1)+' '+w.DSStudio.stages[index].label,()=>w.DSStudio.activeStage===index && d.getElementById('jProgress').textContent.startsWith('Step '+(position+1)+' of 12') && d.querySelector('[data-journey-step="'+index+'"]').getAttribute('aria-current')==='step' && evaluate('projectJson()')===beforeOrderedWalk);
  }
  const finalPrototypeDocument=previewDoc();d.getElementById('reviewFinalPrototype').click();await wait();
  test('Final Prototype reviews the existing live page with native preview focus',()=>d.getElementById('studio-section-4').open && d.activeElement===d.querySelector('#studio-section-4 > summary') && previewDoc()===finalPrototypeDocument && d.getElementById('jNext').hidden);
  d.getElementById('reviewPrototypeExport').click();await wait();
  test('Prototype export route opens existing Deliver without replacing project or preview',()=>w.DSStudio.activeStage===11 && !d.querySelector('[data-journey-pane="11"]').hidden && previewDoc()===finalPrototypeDocument && evaluate('projectJson()')===beforeOrderedWalk);
  // End palette process checks.
  // Neutral palette follows Primary UI without a second editable anchor.
  reset();w.dssShowWizardStep(4);await wait();
  const neutralRows=()=>w.dssReadTokens().filter(row=>/^--neutral-\d+$/.test(row.name));
  for(const method of ['mix','oklch']) for(const primary of ['#004780','#F37327','#008050','#000000','#FFFFFF','#808080']) {
    input('jRamp',method);input('jPrimary',primary);await wait();
    const colours=neutralRows().map(row=>row.value);
    test(method+' '+primary+' produces eleven valid neutral steps ordered light to dark',()=>colours.length===11 && new Set(colours).size===11 && colours.every((hex,i)=>/^#[0-9A-F]{6}$/.test(hex) && (i===0 || evaluate('lum('+JSON.stringify(colours[i-1])+')')>evaluate('lum('+JSON.stringify(hex)+')'))));
    test(method+' '+primary+' neutral midpoint retains hue at low chroma or remains grey',()=>{
      const source=evaluate('rgbToOklch(state.primary)'),mid=evaluate('rgbToOklch(palette().n[500])');
      const delta=Math.abs(Math.atan2(Math.sin(source[2]-mid[2]),Math.cos(source[2]-mid[2])));
      const rgb=evaluate('hexRgb(palette().n[500])');
      return mid[1]<=Math.min(source[1]*.12,.025)+.003 && (source[1]<.005?Math.max(...rgb)-Math.min(...rgb)<=1:delta<.2) && Math.abs(mid[0]-.6)<.005;
    });
    test(method+' '+primary+' neutral lesson reads real tokens and distinguishes its midpoint',()=>['main-palette-steps','palette-ramp-lessons'].every(id=>{
      const rows=[...d.querySelectorAll('#'+id+' [data-palette-role="neutral"] [data-shade]')];
      return rows.length===11 && rows.every(row=>row.textContent.includes('--neutral-'+row.dataset.shade+': '+neutralRows().find(token=>token.name==='--neutral-'+row.dataset.shade).value+';')) && rows.find(row=>row.dataset.shade==='500').textContent.includes('derived midpoint');
    }));
  }
  input('jPrimary','#004780');await wait();const blueNeutrals=JSON.stringify(neutralRows());
  input('jSecondary','#F37327');input('jAccent','#EF426F');await wait();
  test('Supporting and Accent changes do not alter Neutral',()=>JSON.stringify(neutralRows())===blueNeutrals);
  input('jPrimary','#F37327');await wait();
  test('Changing Primary UI hue updates Neutral and all background option groups',()=>JSON.stringify(neutralRows())!==blueNeutrals && ['page','header','main','footer'].every(region=>{
    const options=[...d.getElementById(region+'-background-brand').querySelectorAll('optgroup option')];return options.length===11 && options.every((option,i)=>option.value===neutralRows()[i].value && option.textContent.includes(neutralRows()[i].name));
  }));
  const selectedNeutral=neutralRows().find(row=>row.name==='--neutral-100').value;
  for(const region of ['page','header','main','footer']) input(region+'-background-brand',selectedNeutral,'change');
  await wait();
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const region of ['page','header','main','footer'])input(region+'-background-brand',selectedNeutral,'change');await wait();
    const checkNeutral=(pd,pw)=>['body','header','main','footer'].every(region=>pw.getComputedStyle(pd.querySelector(region==='body'?'body':'body > '+region)).backgroundColor==='rgb('+evaluate('hexRgb('+JSON.stringify(selectedNeutral)+')').join(', ')+')');
    test(mode+' '+theme+' applies a neutral step in all four live backgrounds',()=>checkNeutral(previewDoc(),previewWindow()) && neutralRows().length===11);
    const page=d.createElement('iframe');page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(page);await wait();
    test(mode+' '+theme+' standalone export includes and applies Neutral',()=>checkNeutral(page.contentDocument,page.contentWindow) && page.contentDocument.querySelector('style').textContent.includes('--neutral-100: '+selectedNeutral));page.remove();
  }
  const assignedNeutrals=evaluate('JSON.stringify(state.semanticOverrides)');input('jPrimary','#008050');await wait();
  test('New neutral generation preserves previously copied background choices',()=>evaluate('JSON.stringify(state.semanticOverrides)')===assignedNeutrals && evaluate('palette().roles.background')===selectedNeutral);
  const neutralProject=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();reset();evaluate('importConfig('+JSON.stringify(neutralProject)+')');await wait();
  test('Neutral regenerates from saved Primary and method without storing another anchor',()=>evaluate('state.primary')==='#008050' && neutralRows().length===11 && !Object.hasOwn(JSON.parse(evaluate('projectJson()')),'neutral') && evaluate('JSON.stringify(state.semanticOverrides)')===assignedNeutrals);
  test('Neutral catalogue tokens are classified and configured from Primary UI',()=>neutralRows().every(row=>row.type==='Colour ramp' && w.dssTokenSource(row).control==='jPrimary' && w.dssTokenSource(row).step===4));
  w.dssConfigureToken(neutralRows()[0]);await wait();
  test('Configure Neutral focuses Primary rather than creating an independent colour',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('jPrimary'));
  const neutralCandidates=w.dssGetContrastChecks().filter(row=>/^neutral-\d+ /.test(row.name));
  test('Every neutral step has contrast candidates with valid Primary source targets',()=>neutralCandidates.length===44 && neutralCandidates.every(row=>row.scope==='candidate' && row.targets.some(target=>target.type==='anchor' && target.key==='primary')));
  d.querySelector('#palette-ramp-lessons [data-palette-role="neutral"] button').click();await wait();
  test('Neutral Inspect CSS uses the current complete stylesheet',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--neutral-500:'));
  const neutralBackgroundInspect=d.querySelectorAll('#palette-ramp-lessons [data-palette-role="neutral"] button')[1];neutralBackgroundInspect.click();await wait();
  test('Neutral background inspection targets an existing semantic declaration',()=>neutralBackgroundInspect.textContent==='Inspect background CSS' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--background:') && d.getElementById('dockCss').scrollTop>0);
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);d.querySelector('#main-palette-steps [data-palette-role="neutral"]').open=true;await wait();
    test('Neutral palette fits '+width+'px with expanded steps',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['main-palette-steps','palette-ramp-lessons'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();await wait();
  test('Reset restores the Primary-derived neutral default',()=>JSON.stringify(evaluate('palette().n'))===JSON.stringify(evaluate('makeNeutralRamp(DEFAULT.primary,DEFAULT.method)')));
  input('jRamp','mix');evaluate('resetStudio()');await wait();
  test('Reset restores OKLCH and its neutral output after RGB mix',()=>evaluate('state.method')==='oklch' && d.getElementById('jRamp').value==='oklch' && JSON.stringify(evaluate('palette().n'))===JSON.stringify(evaluate('makeNeutralRamp(state.primary,"oklch")')));
  input('jRamp','mix');d.getElementById('jNewLocal').click();await wait();
  test('New projects restore OKLCH after choosing RGB mix',()=>evaluate('state.method')==='oklch' && d.getElementById('method').value==='oklch');
  for(const method of ['mix','oklch']) {
    evaluate('importConfig({method:'+JSON.stringify(method)+'})');await wait();
    test('Import preserves explicit '+method+' ramp choice',()=>evaluate('state.method')===method && d.getElementById('jRamp').value===method && d.getElementById('method').value===method);
  }
  evaluate('importConfig({method:"invalid"})');await wait();
  test('Invalid imported methods fall back to OKLCH',()=>evaluate('state.method')==='oklch');
  evaluate('importConfig({})');await wait();
  test('Projects without a method inherit OKLCH',()=>evaluate('state.method')==='oklch');
  // End neutral palette checks.
  // Background transparency paints alpha without fading region contents.
  reset();w.dssShowWizardStep(4);await wait();
  const opacityRegions=['body','header','main','footer'];
  const opacityId=region=>(region==='body'?'page':region)+'-background';
  test('Background opacity defaults to fully opaque for existing projects',()=>opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1 && d.getElementById(opacityId(region)+'-opacity').value==='100'));
  const opacityColours={body:'#004780',header:'#F37327',main:'#5FC5BF',footer:'#EF426F'};
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) for(const percent of [0,35,100]) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const region of opacityRegions){input(opacityId(region)+'-hex',opacityColours[region]);input(opacityId(region)+'-opacity',percent);}
    await wait();
    const checkOpacity=(pd,pw)=>opacityRegions.every(region=>{
      const el=pd.querySelector(region==='body'?'body':'body > '+region),style=pw.getComputedStyle(el),rgb=evaluate('hexRgb('+JSON.stringify(opacityColours[region])+')');
      return style.opacity==='1' && style.backgroundColor===(percent===100?'rgb('+rgb.join(', ')+')':'rgba('+rgb.join(', ')+', '+percent/100+')');
    });
    test(mode+' '+theme+' '+percent+'% background paint preserves full content opacity',()=>checkOpacity(previewDoc(),previewWindow()) && previewWindow().getComputedStyle(previewDoc().querySelector('header a')).opacity==='1' && opacityRegions.every(region=>d.getElementById(opacityId(region)+'-opacity-value').textContent===percent+'%' && d.getElementById(region+'-background-opacity-code').textContent==='--'+region+'-background-opacity: '+percent/100+';'));
    const standalone=d.createElement('iframe');standalone.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(standalone);await wait();
    test(mode+' '+theme+' '+percent+'% standalone transparency matches live output',()=>checkOpacity(standalone.contentDocument,standalone.contentWindow) && standalone.contentWindow.getComputedStyle(standalone.contentDocument.documentElement).backgroundColor===evaluate("'rgb('+hexRgb(palette().roles.surface).join(', ')+')'"));standalone.remove();
  }
  input('jTheme','light');input('jSemanticRole','surface','change');evaluate('state.semanticOverrides.light.surface="#FFFFFF";state.semanticOverrides.light.text="#000000";apply()');
  input('page-background-opacity',50);input('header-background-opacity',50);await wait();
  test('Translucent Header contrast uses the actual Body-over-canvas blend',()=>{
    const row=w.dssGetContrastChecks().find(row=>row.theme==='light'&&row.group==='Text and semantic roles'&&row.name==='--text'&&row.location==='--header-background');
    return row.bg==='#B98B73' && d.getElementById('header-background-composite').textContent.includes('#B98B73') && d.getElementById('body-background-composite').textContent.includes('#80A3C0');
  });
  const savedOpacity=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();await wait();
  test('Opacity values autosave with the existing project state',()=>Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>project.data.backgroundOpacity?.light?.header===50));
  reset();evaluate('importConfig('+JSON.stringify(savedOpacity)+')');await wait();
  test('JSON round trip restores both themes and all opacity sliders',()=>evaluate('state.backgroundOpacity.light.header')===50 && evaluate('state.backgroundOpacity.dark.header')===100 && d.getElementById('header-background-opacity').value==='50');
  const previousOpacity=evaluate('state.backgroundOpacity.light.header');input('header-background-brand',evaluate('palette().n[100]'),'change');await wait();
  test('Brand or Neutral background selection preserves its opacity choice',()=>evaluate('state.backgroundOpacity.light.header')===previousOpacity);
  input('jTheme','dark');input('header-background-opacity',25);input('main-background-opacity',35);d.getElementById('header-background-reset').click();await wait();
  test('Background reset clears current-region colour and alpha only',()=>!evaluate('state.backgroundOpacity.dark.header') && !evaluate('state.semanticOverrides.dark["header-background"]') && evaluate('backgroundOpacity("header")')===1 && evaluate('state.backgroundOpacity.dark.main')===35 && evaluate('state.backgroundOpacity.light.header')===50);
  const alphaToken=w.dssReadTokens().find(row=>row.name==='--header-background-opacity'&&row.scope==='Light / base');w.dssConfigureToken(alphaToken);await wait();
  test('Opacity catalogue source selects its theme and focuses its range',()=>evaluate('state.theme')==='light' && w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('header-background-opacity'));
  d.getElementById('header-background-opacity').focus();input('header-background-opacity',64);await wait();
  test('Opacity edits preserve focus and update complete inspector CSS',()=>d.activeElement===d.getElementById('header-background-opacity') && (w.DSStudio.inspector.show({language:'css',section:'all',find:'--header-background-opacity:'}),d.getElementById('dockCss').textContent===evaluate('cssExport()')) && d.getElementById('dockCss').textContent.includes('--header-background-opacity: 0.64;'));
  evaluate('importConfig({backgroundOpacity:{light:{body:-20,header:240,main:33.6,footer:"20",unknown:0},dark:{body:null,header:{bad:1},main:50,footer:0}}})');await wait();
  test('Opacity imports clamp finite numbers, round percentages and reject non-numeric data',()=>evaluate('state.backgroundOpacity.light.body===0 && state.backgroundOpacity.light.header===100 && state.backgroundOpacity.light.main===34 && !("footer" in state.backgroundOpacity.light) && !("unknown" in state.backgroundOpacity.light) && !("body" in state.backgroundOpacity.dark) && !("header" in state.backgroundOpacity.dark) && state.backgroundOpacity.dark.main===50 && state.backgroundOpacity.dark.footer===0'));
  evaluate('importConfig({backgroundOpacity:{light:{body:NaN,header:Infinity,main:-Infinity}}})');await wait();
  test('Non-finite opacity imports remain fully opaque',()=>opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    test('Opacity controls and centre model fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && opacityRegions.every(region=>{const el=d.getElementById(opacityId(region)+'-opacity');w.DSStudio.paletteWorkspace.revealControl(el);return el.getBoundingClientRect().height>=44 && el.getBoundingClientRect().width>0 && el.getAttribute('aria-describedby')==='background-opacity-help';}) && d.getElementById('webpage-background-lesson').scrollWidth<=d.getElementById('webpage-background-lesson').clientWidth+1);
  }
  app.style.width='1440px';input('page-background-opacity',0);evaluate('resetStudio()');await wait();
  test('Reset removes custom opacity data and restores opaque defaults',()=>!evaluate('state.backgroundOpacity') && opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1 && d.getElementById(opacityId(region)+'-opacity').value==='100'));
  // End background transparency checks.
  app.style.width='1440px';if(d.documentElement.dataset.theme==='dark')d.getElementById('themeToggle').click();reset();w.DSStudio.inspector.show({language:'css',section:'all'});w.dssShowWizardStep(4,false);await wait();
  // Background fixtures start with a complete Basic custom outline.
  app.style.width='1440px';reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1,false);input('plan-pages',w.DSStudio.process.samplePages('basic'));await wait();
  w.dssShowWizardStep(4);
  const defaultCanvas=evaluate('palette().roles.background');
  input('page-background-hex','#E1E9F0');await wait();
  test('Page background control updates tokens, inspector and Basic preview',()=>evaluate('palette().roles.background')==='#E1E9F0' && previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(225, 233, 240)' && evaluate('cssExport()').includes('--background: #E1E9F0') && d.getElementById('page-background-colour').value==='#e1e9f0');
  for (const [theme,colour,rgb] of [['light','#E1E9F0','rgb(225, 233, 240)'],['dark','#172635','rgb(23, 38, 53)']]) {
    evaluate(`state.theme='${theme}';apply()`);input('page-background-hex',colour);await wait();
    const checkCanvas=(pd,pw)=>pw.getComputedStyle(pd.body).backgroundColor===rgb && [...pd.querySelectorAll('main > section')].length===4 && [...pd.querySelectorAll('main > section')].every(section=>pw.getComputedStyle(section).backgroundColor==='rgba(0, 0, 0, 0)');
    test(theme+' Basic selected background is visible behind every main section',()=>checkCanvas(previewDoc(),previewWindow()));
    const canvasPage=d.createElement('iframe');
    canvasPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    d.body.append(canvasPage);await wait();
    test(theme+' Basic exported background is visible behind every main section',()=>checkCanvas(canvasPage.contentDocument,canvasPage.contentWindow));
    canvasPage.remove();
  }
  evaluate("state.theme='light';apply()");await wait();
  input('page-background-hex','bad');await wait();
  test('Page background rejects invalid input without changing state',()=>evaluate('palette().roles.background')==='#E1E9F0');
  const backgroundProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(backgroundProject)+')');await wait();
  test('Page background survives project round trip',()=>evaluate('palette().roles.background')==='#E1E9F0');
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Page background applies to Advanced as well as Basic',()=>previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(225, 233, 240)');
  evaluate("state.theme='dark';apply()");await wait();
  input('page-background-colour','#172635');await wait();
  test('Page background is independently editable per theme',()=>evaluate('state.semanticOverrides.dark.background')==='#172635' && evaluate('state.semanticOverrides.light.background')==='#E1E9F0' && previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(23, 38, 53)');
  d.getElementById('page-background-reset').click();await wait();
  test('Page background reset restores only the current theme',()=>!evaluate('state.semanticOverrides.dark.background') && evaluate('state.semanticOverrides.light.background')==='#E1E9F0');
  evaluate("state.theme='light';apply()");d.getElementById('page-background-reset').click();await wait();
  test('Page background reset restores the default canvas',()=>evaluate('palette().roles.background')===defaultCanvas);
  reset();await wait();
  w.dssShowWizardStep(4);
  const regions=['header','main','footer'];w.DSStudio.paletteWorkspace.revealControl(d.getElementById('page-background-colour'));
  test('Background controls follow Brand and Main Palettes, in page order',()=>{
    const pane=d.querySelector('[data-journey-pane="4"]'),editor=d.querySelector('.page-background-editor');
    return Boolean(d.getElementById('jRamp').compareDocumentPosition(editor)&w.Node.DOCUMENT_POSITION_FOLLOWING) &&
      [...editor.querySelectorAll('legend')].map(el=>el.textContent).join('|')==='Body background|Header background|Main background|Footer background' &&
      d.getElementById('palette-stage-backgrounds').contains(editor) && !pane.contains(editor) && d.querySelector('#palette-workspace #webpage-background-lesson');
  });
  test('Body is a visible first-class control and contains the centre page regions',()=>d.getElementById('body-background-controls').closest('[data-palette-stage]').dataset.paletteStage==='backgrounds' && d.getElementById('page-background-colour').getBoundingClientRect().height>=44 && ['header','main','footer'].every(region=>d.getElementById('body-background-value').closest('section').querySelector('.background-contained-regions').contains(d.getElementById(region+'-background-value'))));
  test('Every background selector offers the complete Brand Palette in its saved order',()=>regions.concat('page').every(region=>{
    const values=[...d.getElementById(region+'-background-brand').children].filter(el=>el.tagName==='OPTION').slice(1);
    return values.length===evaluate('state.brandPalette.length') && values.every((option,i)=>option.value===evaluate('state.brandPalette')[i].hex && option.textContent.includes(evaluate('state.brandPalette')[i].name));
  }));
  const regionColours={light:['#004780','#5FC5BF','#F37327'],dark:['#EF426F','#495965','#57B7E7']};
  const bodyColours={light:'#00BADC',dark:'#2B71B9'};
  for (const theme of ['light','dark']) {
    input('jTheme',theme);await wait();
    input('page-background-brand',bodyColours[theme],'change');await wait();
    test(theme+' Body brand choice updates the existing background role and centre model',()=>evaluate('palette().roles.background')===bodyColours[theme] && d.getElementById('body-background-value').textContent==='--background: '+bodyColours[theme]+';' && d.getElementById('body-background-contrast').textContent.includes('Text '));
    for (const [index,region] of regions.entries()) {
      input(region+'-background-brand',regionColours[theme][index],'change');await wait();
      test(theme+' '+region+' background selects a brand value independently',()=>evaluate('palette().roles')[region+'-background']===regionColours[theme][index] && d.getElementById(region+'-background-hex').value===regionColours[theme][index] && d.getElementById(region+'-background-value').textContent.includes(regionColours[theme][index]));
    }
    for (const mode of ['basic','advanced']) {
      d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
      const checkRegions=(pd,pw)=>pw.getComputedStyle(pd.body).backgroundColor==='rgb('+evaluate('hexRgb('+JSON.stringify(bodyColours[theme])+')').join(', ')+')' && regions.every((region,i)=>{
        const rgb=evaluate('hexRgb('+JSON.stringify(regionColours[theme][i])+')');
        return pw.getComputedStyle(pd.querySelector('body > '+region)).backgroundColor==='rgb('+rgb.join(', ')+')';
      });
      test(theme+' '+mode+' preview paints Body and all three regions and preserves card surfaces',()=>checkRegions(previewDoc(),previewWindow()) && previewWindow().getComputedStyle(previewDoc().querySelector('.card')).backgroundColor!==previewWindow().getComputedStyle(previewDoc().querySelector('main')).backgroundColor);
      const exportPage=d.createElement('iframe');exportPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(exportPage);await wait();
      test(theme+' '+mode+' standalone HTML and CSS paint the same backgrounds',()=>checkRegions(exportPage.contentDocument,exportPage.contentWindow));exportPage.remove();
      for (const region of ['body',...regions]) for (const language of ['css','html']) {
        const row=d.getElementById(region+'-background-value').closest('section');row.querySelector('[data-background-inspect="'+language+'"]').click();await wait();
        test(theme+' '+mode+' '+region+' Inspect '+language+' shows the complete current output',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate(language==='css'?'cssExport()':'htmlExport()') && d.getElementById(language==='css'?'dockTabCss':'dockTabHtml').getAttribute('aria-selected')==='true');
      }
    }
  }
  const regionProject=JSON.parse(evaluate('projectJson()'));input('jProject','Region background test');d.getElementById('jSaveLocal').click();await wait();
  input('header-background-colour','#123456');await wait();
  test('A custom region picker updates the current inspector output',()=>evaluate("palette().roles['header-background']")==='#123456' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  d.getElementById('jLoadLocal').click();await wait();
  test('Saved projects restore autosaved per-theme region and Body backgrounds',()=>evaluate('state.semanticOverrides.dark["header-background"]')==='#123456' && evaluate('state.semanticOverrides.light["header-background"]')===regionColours.light[0] && evaluate('state.semanticOverrides.dark.background')===bodyColours.dark && evaluate('state.semanticOverrides.light.background')===bodyColours.light);
  reset();evaluate('importConfig('+JSON.stringify(regionProject)+')');await wait();
  test('Region and Body backgrounds survive project JSON round trip',()=>regions.every((region,i)=>evaluate('state.semanticOverrides.dark')[region+'-background']===regionColours.dark[i] && evaluate('state.semanticOverrides.light')[region+'-background']===regionColours.light[i]) && evaluate('state.semanticOverrides.dark.background')===bodyColours.dark && evaluate('state.semanticOverrides.light.background')===bodyColours.light);
  w.dssConfigureToken({name:'--background',scope:'Light'});await wait();
  test('Body token source routes to the correct theme and visible Body control',()=>evaluate('state.theme')==='light' && w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('page-background-colour'));
  input('jTheme','dark');await wait();
  input('main-background-hex','#123ABC');await wait();
  input('main-background-hex','red;/*');await wait();
  test('Invalid region hex cannot change state or generated output',()=>evaluate('state.semanticOverrides.dark["main-background"]')==='#123ABC' && !evaluate('cssExport()').includes('red;/*') && d.getElementById('main-background-hex').getAttribute('aria-invalid')==='true');
  for (const region of regions) {d.getElementById(region+'-background-reset').click();await wait();}
  test('Region reset restores current-theme defaults and retains other-theme choices',()=>regions.every((region,i)=>!evaluate('state.semanticOverrides.dark')[region+'-background'] && evaluate('state.semanticOverrides.light')[region+'-background']===regionColours.light[i]) && evaluate("palette().roles['main-background']===palette().roles.background && palette().roles['header-background']===palette().roles.surface && palette().roles['footer-background']===palette().roles.surface"));
  input('page-background-hex','#234567');await wait();
  test('Default Main background follows subsequent canvas changes',()=>evaluate("palette().roles['main-background']==='#234567'"));
  d.getElementById('page-background-reset').click();await wait();
  test('Body reset restores only its theme and updates default Main',()=>!evaluate('state.semanticOverrides.dark.background') && evaluate('state.semanticOverrides.light.background')===bodyColours.light && evaluate('palette().roles.background===palette().roles["main-background"]'));
  input('header-background-brand','#FFFFFF','change');await wait();
  evaluate("state.brandPalette=state.brandPalette.map(item=>item.hex==='#FFFFFF'?{...item,name:'<img onerror=alert(1)>',hex:'#EEEEEE'}:item);apply()");await wait();
  test('Brand edits refresh all choices safely while existing assignments retain copied hex',()=>evaluate("palette().roles['header-background']")==='#FFFFFF' && regions.every(region=>[...d.getElementById(region+'-background-brand').options].some(option=>option.value==='#EEEEEE'&&option.textContent.includes('<img onerror=alert(1)>'))) && !d.querySelector('#webpage-region-controls img'));
  evaluate('importConfig({semanticOverrides:{light:{"header-background":"url(javascript:alert(1))","main-background":{},"footer-background":"#abc"},dark:{"header-background":"#abcdef"}}})');await wait();
  test('Imported region overrides validate hex types and lengths',()=>evaluate("!state.semanticOverrides.light['header-background'] && !state.semanticOverrides.light['main-background'] && !state.semanticOverrides.light['footer-background'] && state.semanticOverrides.dark['header-background']==='#ABCDEF'"));
  for (const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    test('Background controls and centre lesson fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['body-background-controls','webpage-region-controls','webpage-background-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}) && ['page',...regions].every(region=>['brand','colour','hex'].every(kind=>{const el=d.getElementById(region+'-background-'+kind);w.DSStudio.paletteWorkspace.revealControl(el);el.focus();return d.activeElement===el && el.getBoundingClientRect().height>=44;})));
  }
  app.style.width='1440px';reset();await wait();
  test('Reset clears all region overrides and restores selectors',()=>!evaluate('state.semanticOverrides') && regions.every(region=>d.getElementById(region+'-background-reset').disabled));

  test('No palette JavaScript errors',()=>!w.__reviewErrors.length);
  }catch(error){results.push({name:'Palette harness completed',pass:false,error:String(error.stack||error)});}
  finish();
};
</script>'''


if __name__ == '__main__':
    raise SystemExit(run_review(HARNESS))
