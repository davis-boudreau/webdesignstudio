"use strict";
/* Reuse the existing palette controls and generators in a guided centre workspace. */
DSStudio.register({
  id:'palette-workspace',title:'Guided Palette workspace',
  init() {
    const get=id=>document.getElementById(id),pane=document.querySelector('[data-journey-pane="4"]'),panel=get('brandPalette').querySelector(':scope > .panel');
    const old=[...panel.children],workspace=document.createElement('section');workspace.id='palette-workspace';workspace.className='palette-workspace';workspace.setAttribute('aria-labelledby','palette-workspace-title');
    workspace.innerHTML='<header><h3 id="palette-workspace-title" tabindex="-1">Palette workspace</h3><p>Give each colour a purpose, then check it in the website. Work through the colour-token process or reopen a stage to revise a decision. Changes update your project, live preview and exported CSS immediately.</p><label for="palette-theme">Website theme to edit and review</label><select id="palette-theme"><option value="light">Light</option><option value="dark">Dark</option></select><p class="help">Brand colours and UI anchors are shared. Background and semantic overrides apply to the selected theme.</p></header><p id="palette-workspace-status" class="help" role="status"></p>';
    workspace.querySelector('header').setAttribute('data-stage-controls','');
    panel.prepend(workspace);
    const definitions=[
      ['brand','Brand colours','Record the colours that identify your site. Add a colour, choose it from the list, then change its name, token suffix or value. Remove references you do not need; keep at least one, with a limit of 24. Editing a reference keeps the UI roles that already copied its colour.'],
      ['roles','Choose UI anchors','Primary, Supporting and Accent are source colour families shared by both website themes. They generate the shade ramps used by semantic roles. Choose a brand reference or a custom anchor. Reset restores the starter assignment. These three required anchors cannot be deleted.'],
      ['shades','Generate and understand shades','RGB mix blends toward white or black; OKLCH adjusts perceptual lightness and chroma. Choose a method and inspect the eleven steps for each family. Step 500 preserves the UI anchor. Neutral derives from Primary. These are generated outputs: change their source instead of adding or deleting individual steps. Shade numbers do not guarantee contrast.'],
      ['semantics','Assign semantic colours','Turn shades into purpose-based roles: text, surfaces, borders, actions, focus and feedback. Review each role in the selected website theme. Preview contrast effects before applying a custom override; Use generated removes it and reconnects the role to the palette.'],
      ['backgrounds','Apply page backgrounds','Choose a region, then create or edit its background override for this theme. Use default removes that override and restores inheritance. Opacity affects the background paint, not the text. Check the actual foreground/background pair.'],
      ['components','Colour the key components','Cards, inputs and links consume shared semantic roles. Buttons add variant-specific colour sources and state overrides. Inspect the actual exported values, edit a semantic source, or customize a button. Button sources and overrides affect both website themes; semantic overrides affect only the selected theme.'],
      ['review','States and review','Review both website themes and actual component states. Revisit semantic roles or component colours when a pair needs adjustment. Tokens alone do not show keyboard behavior, opacity or loading feedback. Include words or icons and check contrast before exporting.']
    ],stages=new Map();
    for(const [index,[key,title,help]]of definitions.entries()) {
      const details=document.createElement('details');details.id='palette-stage-'+key;details.className='palette-stage';details.dataset.paletteStage=key;
      const summary=document.createElement('summary');summary.textContent=(index+1)+'. '+title;
      const body=document.createElement('div');body.className='palette-stage-body';const intro=document.createElement('p');intro.textContent=help;body.append(intro);details.append(summary,body);workspace.append(details);stages.set(key,{details,body,summary});
      details.addEventListener('toggle',()=>{if(details.open)show(key,false);});
    }
    function reference(title,...nodes){const details=document.createElement('details'),summary=document.createElement('summary');details.className='palette-reference';summary.textContent=title;details.append(summary,...nodes);return details;}
    function append(key,...nodes){stages.get(key).body.append(...nodes);}
    function show(key,focus=true){const item=stages.get(key);if(!item)return;item.details.open=true;for(const [other,stage]of stages)if(other!==key)stage.details.open=false;updateProgress(key);if(key==='components')syncComponents();if(focus){item.summary.focus();item.summary.scrollIntoView({block:'start',behavior:'instant'});}}
    const heading=pane.querySelector('h3'),help=pane.querySelector(':scope > p.help');heading.textContent=(DSStudio.stages[4].position+1)+'. Build your palette';help.textContent='Use the centre workspace to create your brand references, assign colour jobs and review the website in both themes.';
    const open=document.createElement('button');open.id='open-palette-workspace';open.type='button';open.className='ghost';open.textContent='Open Palette workspace';open.addEventListener('click',()=>{window.dssRevealSection('brandPalette',false);get('palette-workspace-title').focus();get('palette-workspace-title').scrollIntoView({block:'start',behavior:'instant'});});
    const progress=document.createElement('p');progress.id='palette-progress';progress.className='help';const nav=document.createElement('ol');nav.className='palette-stage-nav';nav.setAttribute('aria-label','Palette process');
    for(const [key,title]of definitions){const li=document.createElement('li'),button=document.createElement('button');button.type='button';button.className='ghost';button.dataset.paletteGo=key;button.textContent=title;button.addEventListener('click',()=>{window.dssRevealSection('brandPalette',false);show(key);});li.append(button);nav.append(li);}
    const note=document.createElement('p');note.className='help';note.textContent='Changes apply immediately. Save JSON or save your local project to keep a portable copy.';
    // Move every existing editor before clearing the compact wizard pane.
    const editor=get('jBrandEditor'),oldEditor=editor.closest('details'),editDetails=document.createElement('section');editDetails.id='palette-brand-properties';editDetails.setAttribute('aria-labelledby','palette-brand-properties-title');
    const propertiesTitle=document.createElement('h4');propertiesTitle.id='palette-brand-properties-title';propertiesTitle.textContent='Selected colour properties';editDetails.append(propertiesTitle,...[...oldEditor.children].filter(node=>node.tagName!=='SUMMARY'));oldEditor.remove();
    editDetails.querySelector('p.help').textContent='Choose a unique token suffix using lowercase letters, digits and hyphens, starting with a letter. Changing the display name keeps the token ID.';
    const selector=document.createElement('div');selector.className='field';selector.innerHTML='<label for="palette-brand-selection">Choose a brand colour to edit</label><select id="palette-brand-selection"></select>';
    append('brand',selector,editDetails.querySelector('#jBrandAdd'),editDetails.querySelector('#jBrandCount'),editDetails,get('jBrandStatus'),reference('All brand references',get('jBrandSwatches')));
    const roleFields=document.createElement('div');roleFields.className='palette-role-editors';
    append('roles',get('brandRoleAssignments'),roleFields);
    for(const role of ['primary','secondary','accent']){
      const title=role[0].toUpperCase()+role.slice(1),field=get('j'+title).closest('.field'),reset=document.createElement('button');reset.type='button';reset.className='ghost';reset.id='palette-reset-'+role;reset.textContent='Reset '+(role==='secondary'?'Supporting':title)+' assignment';reset.addEventListener('click',()=>{get('j'+title).value=DEFAULT[role];get('j'+title).dispatchEvent(new Event('input',{bubbles:true}));get('palette-workspace-status').textContent=title+' assignment reset. Other palette choices are retained.';});field.append(reset);roleFields.append(field);
    }
    append('roles',reference('Apply a brand swatch to a role',get('brandApplyRole').closest('.field'),get('brandApplyHelp'),get('brandFeedback'),get('brandSwatches'),get('brandEditPalette')));
    const tokenLesson=get('palette-token-lesson'),statusLesson=get('status-palette-lesson');statusLesson.remove();
    append('shades',get('jRamp').closest('.field'),get('neutralPaletteAnchor').closest('section'),get('palette-steps-controls'),reference('Read the token declarations and colour model',tokenLesson));
    append('semantics',get('jSemanticTitle').closest('section'));
    const semanticPane=document.querySelector('[data-journey-pane="6"]'),semanticLink=document.createElement('button');semanticLink.type='button';semanticLink.className='ghost';semanticLink.textContent='Edit semantic colours in Palette';semanticLink.addEventListener('click',()=>{window.dssRevealSection('jSemanticRole',false);get('jSemanticRole').focus();get('jSemanticRole').scrollIntoView({block:'center',behavior:'instant'});});semanticPane.append(semanticLink);
    const labHelp=document.createElement('p');labHelp.className='help';labHelp.textContent='Explore RGB, HSL and OKLCH here. Build and edit purpose-based semantic colours in the Palette workspace.';semanticPane.querySelector('h3').after(labHelp);
    semanticPane.querySelector('h3').textContent=(DSStudio.stages[6].position+1)+'. Explore colour models';
    const backgrounds=document.querySelector('.page-background-editor'),regionSelector=document.createElement('div');regionSelector.className='field';regionSelector.innerHTML='<label for="palette-region-selection">Page region to edit</label><select id="palette-region-selection"><option value="body">Body</option><option value="header">Header</option><option value="main">Main</option><option value="footer">Footer</option></select>';backgrounds.querySelector('fieldset').before(regionSelector);
    append('backgrounds',backgrounds,reference('Compare region colours, contrast and padding',get('webpage-background-lesson')));
    const componentPicker=document.createElement('div');componentPicker.className='field';componentPicker.innerHTML='<label for="palette-component-family">Component family</label><select id="palette-component-family"><option value="cards">Cards</option><option value="inputs">Inputs and feedback</option><option value="links">Links</option><option value="buttons">Buttons</option></select>';
    const componentContext=document.createElement('p');componentContext.id='palette-component-context';componentContext.className='help';
    const componentValues=document.createElement('dl');componentValues.id='palette-component-values';componentValues.className='palette-component-values';
    const buttonColours=document.createElement('section');buttonColours.id='palette-button-colours';buttonColours.hidden=true;
    const variantPicker=document.createElement('div');variantPicker.className='field';variantPicker.innerHTML='<label for="palette-button-variant">Button variant to colour</label><select id="palette-button-variant"></select>';variantPicker.querySelector('select').replaceChildren(...[...get('bdVariant').options].map(option=>new Option(option.textContent,option.value)));
    buttonColours.append(get('bdSource').closest('.field'),get('bdCustomWrap'));
    const overrides=reference('Override button colours and shared focus');overrides.classList.add('palette-component-overrides');
    const colourFields=document.createElement('div');colourFields.className='palette-component-fields';for(const id of ['bdDefaultBg','bdText','bdHover','bdHoverText','bdActive','bdActiveText','bdBorderColor','bdFocus'])colourFields.append(get(id).closest('.field'));overrides.append(colourFields);
    const clearButton=document.createElement('button');clearButton.id='palette-button-clear';clearButton.type='button';clearButton.className='ghost';clearButton.textContent="Clear this variant's colour overrides";clearButton.addEventListener('click',()=>window.dssResetButtonColourOverrides(get('bdVariant').value));
    const focusReset=document.createElement('button');focusReset.id='palette-button-focus-reset';focusReset.type='button';focusReset.className='ghost';focusReset.textContent='Use default shared button focus colour';focusReset.addEventListener('click',()=>window.dssSetButtonContrastColour(get('bdVariant').value,'focus',null));
    const scopeNote=document.createElement('p');scopeNote.className='help';scopeNote.textContent='Clearing overrides keeps the selected source, custom source colour and other variants. Focus colour is shared across all button variants and resets separately.';
    buttonColours.append(overrides,clearButton,focusReset,scopeNote);
    append('components',componentPicker,variantPicker,componentContext,componentValues,buttonColours,reference('General controls and button-state colour ramps',get('interaction-palette-controls')));
    const behaviour=get('bdFocusWidth').closest('details');behaviour.querySelector('summary').textContent='Advanced button behaviour';for(const hint of behaviour.querySelectorAll('.control-hint'))hint.remove();const behaviourHelp=document.createElement('p');behaviourHelp.className='help';behaviourHelp.textContent='Edit colour sources and overrides in Palette. These controls adjust focus width, timing and mobile behavior.';behaviour.querySelector('.group-body').prepend(behaviourHelp);
    const buttonLink=document.createElement('button');buttonLink.type='button';buttonLink.className='ghost';buttonLink.textContent='Edit button colours in Palette';buttonLink.addEventListener('click',()=>{window.dssRevealSection('bdSource',false);get('bdSource').focus();get('bdSource').scrollIntoView({block:'center',behavior:'instant'});});document.querySelector('[data-journey-pane="7"]').prepend(buttonLink);
    const statusEditor=document.createElement('div');statusEditor.className='field';statusEditor.innerHTML='<label for="palette-status-role">Feedback role</label><select id="palette-status-role"><option value="success">Success</option><option value="warning">Warning</option><option value="danger">Danger</option></select><label for="palette-status-colour">Feedback colour for this theme</label><input id="palette-status-colour" type="color"><button type="button" class="ghost" id="palette-status-reset">Use generated feedback colour</button><p id="palette-status-source" class="help"></p>';
    append('semantics',reference('Generated feedback shade families',get('status-palette-steps-controls')));
    const reviewGuide=document.createElement('ul');for(const text of ['Check text, surfaces, borders and focus in both website themes.','Compare default, hover, pressed, selected, disabled and validation states in real components.','Use text or icons as well as colour; inspect contrast before exporting.']){const item=document.createElement('li');item.textContent=text;reviewGuide.append(item);}
    append('review',reviewGuide,reference('Quick feedback adjustments',statusEditor),reference('Feedback token reference',statusLesson,get('interaction-palette-lesson')));
    const actions=document.createElement('div');actions.className='button-row';
    for(const [title,target]of [['Review live website','previewShell'],['Check contrast and accessibility','studio-section-5']]){const button=document.createElement('button');button.type='button';button.className='ghost';button.textContent=title;button.addEventListener('click',()=>{window.dssRevealSection(target,false);const element=get(target);element.scrollIntoView({block:'start',behavior:'instant'});if(target==='previewShell')element.focus();else element.querySelector(':scope > summary')?.focus();});actions.append(button);}append('review',actions);
    for(const [index,[key]]of definitions.entries()){
      const buttons=document.createElement('div');buttons.className='button-row palette-stage-actions';
      for(const offset of [-1,1]){const next=definitions[index+offset];if(!next)continue;const button=document.createElement('button');button.type='button';button.className='ghost';button.textContent=(offset<0?'Previous: ':'Next: ')+next[1];button.addEventListener('click',()=>show(next[0]));buttons.append(button);}append(key,buttons);
    }
    const leftovers=old.filter(node=>node.parentElement===panel);if(leftovers.length)workspace.append(reference('More about palette decisions',...leftovers));
    const navigation=document.createElement('details'),navigationSummary=document.createElement('summary');navigation.className='palette-navigation';navigationSummary.textContent='Choose a Palette stage';navigation.append(navigationSummary,nav);const narrow=matchMedia('(max-width: 900px)');navigation.open=!narrow.matches;narrow.addEventListener('change',()=>{navigation.open=!narrow.matches;});help.classList.add('palette-guide-intro');note.classList.add('palette-storage-note');
    pane.replaceChildren(heading,help,open,progress,navigation,note);
    function updateProgress(key){const index=definitions.findIndex(([id])=>id===key);progress.textContent='Palette stage '+(index+1)+' of '+definitions.length+': '+definitions[index][1];for(const button of nav.querySelectorAll('button')){if(button.dataset.paletteGo===key)button.setAttribute('aria-current','step');else button.removeAttribute('aria-current');}}
    let componentSignature='';
    const componentRoles={cards:['surface','surface-muted','text','text-muted','border'],inputs:['surface','surface-muted','text','text-muted','control-border','primary','focus','danger','success'],links:['primary','text','surface-muted','focus','button-focus']};
    const componentNotes={cards:'Cards and nested panels use Surface or Muted surface, readable Text, supporting Muted text and Border roles. These shared roles also affect other components.',inputs:'Inputs use Surface, Text and Control border. Muted roles support placeholders and read-only fields; Primary accents choices, Focus marks keyboard focus, and Danger/Success identify validation.',links:'Ordinary links use Primary; navigation labels use Text and navigation hover uses Muted surface. Focus applies to ordinary links; Button focus also covers linked actions and resource-table links.',buttons:'Resolved values are shown for this website theme. Sources and overrides apply to both themes; button focus is shared. Disabled opacity and non-colour state cues still affect the actual component.'};
    function syncComponents(){
      if(!get('brandPalette').open || !stages.get('components').details.open)return;
      const family=get('palette-component-family').value,variant=get('bdVariant').value;buttonColours.hidden=family!=='buttons';variantPicker.hidden=family!=='buttons';get('palette-button-variant').value=variant;componentContext.textContent=componentNotes[family]||'';
      const names=family==='buttons'?['bg','text','border','hover','hover-text','active','active-text'].map(key=>'--button-'+variant+'-'+key).concat('--button-focus'):(componentRoles[family]||[]).map(key=>'--'+key);
      const tokens=window.dssReadTokens(),rows=names.map(name=>({name,value:(state.theme==='dark'?tokens.find(row=>row.name===name && row.scope==='Dark'):null)?.value||tokens.find(row=>row.name===name && row.scope!=='Dark')?.value||'Not available'}));
      const signature=JSON.stringify([family,variant,state.theme,rows]);if(signature===componentSignature)return;componentSignature=signature;
      componentValues.replaceChildren(...rows.map(({name,value})=>{const group=document.createElement('div'),term=document.createElement('dt'),description=document.createElement('dd'),chip=document.createElement('span'),code=document.createElement('code'),edit=document.createElement('button');term.textContent=name;code.textContent=value;code.dataset.componentToken=name;chip.className='brand-palette-chip';chip.setAttribute('aria-hidden','true');if(validHex(value))chip.style.backgroundColor=value;else chip.hidden=true;edit.type='button';edit.className='ghost';edit.textContent='Edit source';edit.setAttribute('aria-label','Edit source of '+name);edit.addEventListener('click',()=>window.dssConfigureToken({name,scope:state.theme==='dark'?'Dark':'Light / base'}));description.append(chip,code,edit);group.append(term,description);return group;}));
    }
    get('palette-component-family').addEventListener('change',syncComponents);
    get('palette-button-variant').addEventListener('change',event=>{get('bdVariant').value=event.target.value;get('bdVariant').dispatchEvent(new Event('input',{bubbles:true}));});
    let selected='',brandSignature='',stateIdentity;
    function selectBrand(id){selected=id;get('palette-brand-selection').value=id;for(const row of editor.querySelectorAll('[data-brand-id]'))row.hidden=row.dataset.brandId!==id;}
    function selectRegion(){const region=get('palette-region-selection').value;for(const name of ['body','header','main','footer'])get(name==='body'?'body-background-controls':name+'-background-hex').closest('fieldset').hidden=name!==region;}
    function sync(){
      if(stateIdentity!==state){stateIdentity=state;selected='';brandSignature='';show('brand',false);}
      const brands=state.brandPalette,next=JSON.stringify(brands.map(({id,name})=>[id,name]));
      if(next!==brandSignature){brandSignature=next;get('palette-brand-selection').replaceChildren(...brands.map(item=>new Option(item.name+' (--brand-'+item.id+')',item.id)));}
      const active=document.activeElement?.closest('[data-brand-id]')?.dataset.brandId;
      selectBrand(brands.some(item=>item.id===(active||selected))?(active||selected):brands[0].id);
      get('palette-theme').value=state.theme;
      const role=get('palette-status-role').value,hex=palette().roles[role];get('palette-status-colour').value=hex;get('palette-status-reset').disabled=!validHex(state.semanticOverrides?.[state.theme]?.[role]);
      get('palette-status-source').textContent=(state.theme==='dark'?'Dark':'Light')+' theme: '+role+' '+hex.toUpperCase()+' ('+(validHex(state.semanticOverrides?.[state.theme]?.[role])?'custom override; Use generated removes it':'generated from the UI palette')+').';
      selectRegion();syncComponents();
    }
    get('palette-brand-selection').addEventListener('change',event=>selectBrand(event.target.value));get('palette-region-selection').addEventListener('change',selectRegion);
    get('palette-theme').addEventListener('change',event=>{get('jTheme').value=event.target.value;get('jTheme').dispatchEvent(new Event('input',{bubbles:true}));});
    get('palette-status-role').addEventListener('change',sync);
    get('palette-status-colour').addEventListener('input',event=>{if(!validHex(event.target.value))return;const role=get('palette-status-role').value;state.semanticOverrides={...state.semanticOverrides,[state.theme]:{...state.semanticOverrides?.[state.theme],[role]:event.target.value}};apply();window.dssAutosave?.();});
    get('palette-status-reset').addEventListener('click',()=>{delete state.semanticOverrides?.[state.theme]?.[get('palette-status-role').value];apply();window.dssAutosave?.();});
    // Source routing and add/rename focus must expose the selected row before focus.
    editor.addEventListener('focusin',event=>{const row=event.target.closest('[data-brand-id]');if(row)selectBrand(row.dataset.brandId);});
    get('jBrandAdd').addEventListener('click',()=>{show('brand',false);selectBrand(state.brandPalette.at(-1).id);editor.querySelector('[data-brand-id]:not([hidden]) input')?.focus();});
    get('brandEditPalette').addEventListener('click',()=>{show('brand',false);selectBrand(state.brandPalette[0].id);editor.querySelector('[data-brand-id]:not([hidden]) input')?.focus();});
    const configure=window.dssConfigureToken;window.dssConfigureToken=function(row){const source=window.dssTokenSource(row);if(source?.brand){show('brand',false);selectBrand(source.brand);}return configure(row);};
    function revealControl(control){
      const stage=control?.closest('[data-palette-stage]');if(!stage)return;
      if(control.closest('#palette-button-colours')){get('palette-component-family').value='buttons';syncComponents();}
      show(stage.dataset.paletteStage,false);
      const row=control.closest('[data-brand-id]');if(row)selectBrand(row.dataset.brandId);
      const field=control.closest('fieldset');
      if(stage.dataset.paletteStage==='backgrounds' && field){const match=['body','header','main','footer'].find(name=>field.contains(get(name==='body'?'page-background-colour':name+'-background-colour')));if(match){get('palette-region-selection').value=match;selectRegion();}}
      for(let node=control.parentElement;node && node!==workspace;node=node.parentElement)if(node.tagName==='DETAILS')node.open=true;
    }
    const previousReveal=window.dssRevealSection;window.dssRevealSection=function(id,scroll=true){revealControl(get(id));return previousReveal(id,scroll);};
    get('brandPalette').addEventListener('toggle',()=>{if(get('brandPalette').open)syncComponents();});
    DSStudio.on('stage:change',({stage})=>{if(stage.index===4)syncComponents();});
    const previous=apply;apply=function(){previous();sync();};
    const beforeRender=renderCode;renderCode=function(){beforeRender();syncComponents();};
    for(const event of ['dss:reset','dss:imported'])document.addEventListener(event,()=>{selected='';brandSignature='';show('brand',false);sync();get('palette-workspace-status').textContent='';});
    DSStudio.paletteWorkspace={show,selectBrand,selectRegion,revealControl};show('brand',false);sync();DSStudio.emit('lesson:content');
  }
});
