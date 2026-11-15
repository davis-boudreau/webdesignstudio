'use strict';
/* Explicit model paths keep drafts scoped. Browsing, comparisons and collection
   operations are not property edits. No project snapshots are restored by undo. */
DSStudio.register({
  id:'property-editors',title:'Shared property drafts and actions',
  init() {
    const get=id=>document.getElementById(id),scopes=new Map(),bindings=new Map();
    const copy=value=>value===undefined?undefined:JSON.parse(JSON.stringify(value));
    const equal=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
    const documentValue=()=>({...state,clampConfig});
    const read=(root,path)=>path.reduce((value,key)=>value?.[key],root);
    function write(root,path,value) {
      if(path.some(key=>['__proto__','prototype','constructor'].includes(key)))throw new TypeError('Invalid property path');
      for(const key of path.slice(0,-1))root=root[key]??={};
      if(value===undefined)delete root[path.at(-1)];else root[path.at(-1)]=copy(value);
    }
    let identity=state;
    function scope(id,parent,context=()=>'',previewOnly=false) {
      const entry={id,parent,context,drafts:new Map(),fields:[],message:''};
      scopes.set(id,entry);
      entry.actions=DSStudio.propertyActions.create({id,parent,previewOnly,save:()=>save(entry),discard:()=>discard(entry)});
      if(!previewOnly){entry.status=document.createElement('p');entry.status.className='help property-edit-status';entry.status.setAttribute('role','status');entry.status.id='property-status-'+id;parent.append(entry.status);}
      return entry;
    }
    function records(entry) {const key=entry.context();if(!entry.drafts.has(key))entry.drafts.set(key,new Map());return entry.drafts.get(key);}
    function bind(entry,id,path,{decode,display,events=['input','change'],draft,format,validate}={}) {
      const control=typeof id==='string'?get(id):id;if(!control)return;
      const binding={entry,control,path:typeof path==='function'?path:()=>path,decode:decode||(()=>control.type==='checkbox'?control.checked:control.type==='range'||control.type==='number'?Number(control.value):control.value),display,events,draft,format,validate};
      bindings.set(control,binding);entry.fields.push(binding);control.setAttribute('aria-describedby',((control.getAttribute('aria-describedby')||'')+' '+entry.status.id).trim());
    }
    function stage(binding,value) {
      const entry=binding.entry,path=binding.path();if(!path)return;
      const current=read(documentValue(),path),items=records(entry),key=JSON.stringify(path);
      if(equal(current,value))items.delete(key);else items.set(key,{path,base:copy(items.get(key)?.base??current),value:copy(value),control:binding.control});
      entry.message='';binding.draft?.(value);refresh();
    }
    function refresh() {
      if(identity!==state){identity=state;for(const entry of scopes.values()){entry.drafts.clear();entry.message='';}}
      const model=documentValue();
      for(const entry of scopes.values()) {
        for(const items of entry.drafts.values())for(const [key,item]of items)if(!equal(read(model,item.path),item.base)){items.delete(key);entry.message='Saved source changed; stale edits were cleared.';}
        const items=records(entry);
        for(const binding of entry.fields) {
          const path=binding.path();if(!path)continue;
          const item=items.get(JSON.stringify(path));let value=item?item.value:binding.display?binding.display():read(model,path);
          if(binding.format)value=binding.format(value);
          if(value===undefined)continue;
          if(binding.control.type==='checkbox')binding.control.checked=!!value;else binding.control.value=String(value);
          if(binding.validate)binding.control.setCustomValidity(binding.validate(binding.control.value));
          if(binding.control.pattern)binding.control.setAttribute('aria-invalid',String(!binding.control.validity.valid));
          const output=get(binding.control.id+'Out')||get(binding.control.id+'-value');
          if(output && typeof value==='number')output.textContent=output.textContent.replace(/-?\d+(?:\.\d+)?/,String(binding.control.id==='clampFactor'?Math.round(value*100):binding.control.id==='advTracking'?value/100:value));
        }
        if(entry.status){entry.actions.save.disabled=!items.size;entry.actions.discard.disabled=!items.size;entry.status.textContent=entry.message||(entry.id==='typography'?(items.size?'Unsaved typography. The sample and scale show proposed values; Save updates the full website.':'Typography saved. The learning previews match the project.'):(items.size?'Unsaved properties. Save to update the project; preview shows saved values.':'Properties saved. Preview shows the saved project.'));}
      }
      const google=get('fontSource').value==='google',family=get('type-font-role').value;
      get('fontSystemOptions').hidden=google||family!=='heading';get('fontGoogleOptions').hidden=!google;
      get('jFont').closest('.field').hidden=google||family!=='body';get('jFont').disabled=google;get('font').disabled=google;
      get('fontGoogleBody').closest('.field').hidden=family!=='body';get('fontGoogleHeading').closest('.field').hidden=family!=='heading';
      get('fontWeight400').closest('details').hidden=!google;
      get('bdCustomWrap').hidden=get('bdSource').value!=='custom';
      const outlineError=get('plan-pages').validationMessage;
      if(outlineError || get('plan-sample-status').textContent.includes('three information levels'))get('plan-sample-status').textContent=outlineError;
      const stateRows=new Map();
      for(const control of document.querySelectorAll('[data-state-colour]')) {
        const binding=stateBinding(control,stateRows);if(!binding)continue;
        const path=binding.path(),item=records(binding.entry).get(JSON.stringify(path));
        const value=item?item.value:read(model,path);
        control.value=value===undefined || (path[0]==='buttonDesign' && path[1]==='focus' && value?.toUpperCase()===DSStudio.project.buttonDefaults().focus)?'default':value;
      }
      DSStudio.emit('properties:refreshed');
    }
    function save(entry) {
      refresh();
      const items=records(entry);if(!items.size)return;
      for(const item of items.values())if(!item.control.reportValidity())return;
      const next=copy(documentValue());for(const item of items.values())write(next,item.path,item.value);
      const normalized=DSStudio.project.normalize(next),model={...normalized.state,clampConfig:normalized.clampConfig};
      // Commit only edited paths; concurrent decisions in other editors survive.
      for(const item of items.values())write(item.path[0]==='clampConfig'?{clampConfig}:state,item.path,read(model,item.path));
      if([...items.values()].some(item=>item.path[0]==='responsiveDesign'))state.responsiveDesign.wide=normalized.state.responsiveDesign.wide;
      items.clear();entry.message='Properties saved.';
      syncControls();syncAdvanced();DSStudio.emit('properties:committed');apply();window.dssAutosave?.();refresh();
    }
    function discard(entry) {records(entry).clear();entry.message='Unsaved properties discarded.';refresh();}
    function stateBinding(control,cache) {
      if(!control.matches('[data-state-colour]'))return null;
      const view=control.closest('.palette-token-lesson'),group=get(view.id+'-component').value;
      const key=state.theme+':'+group;let rows=cache?.get(key);
      if(!rows){rows=DSStudio.statePalettes.entries(state.theme,group);cache?.set(key,rows);}
      const row=rows.find(item=>item.key===control.dataset.stateColour);
      if(!row)return null;
      const entry=control.closest('[data-palette-stage="semantics"]')?feedbackShades:components;
      const path=row.semantic?['semanticOverrides',state.theme,row.semantic]:row.property==='focus'?['buttonDesign','focus']:['buttonDesign','overrides',row.variant,row.property];
      return {entry,control,path:()=>path,events:['change'],decode:()=>control.value==='default'?(row.property==='focus'?DSStudio.project.buttonDefaults().focus:undefined):control.value.toUpperCase()};
    }
    for(const type of ['input','change'])document.addEventListener(type,event=>{
      const binding=bindings.get(event.target)||stateBinding(event.target);if(!binding || !binding.events.includes(type))return;
      event.stopImmediatePropagation();const value=binding.decode();if(value!==null)stage(binding,value);
    },true);
    function reset(entry,id,changes) {
      const button=get(id);if(!button)return;
      bindings.set(button,{entry,path:()=>null,events:[]});
      button.addEventListener('click',event=>{event.preventDefault();event.stopImmediatePropagation();for(const [path,value]of changes())stage({entry,path:()=>path,control:button},value);},true);
    }
    const palette=(key,context)=>scope('palette-'+key,get('palette-properties-'+key),context);
    const anchors=palette('roles');
    for(const role of ['primary','secondary','accent']) {
      const name=role[0].toUpperCase()+role.slice(1);
      for(const id of [role,'j'+name,'j'+name+'Brand'])bind(anchors,id,[role],{decode:()=>validHex(get(id).value)?get(id).value.toLowerCase():null,display:()=>state[role].toUpperCase(),format:value=>value?.toUpperCase()});
      reset(anchors,'palette-reset-'+role,()=>[[[role],DEFAULT[role]]]);
    }
    const shades=palette('shades');for(const id of ['jRamp','method'])bind(shades,id,['method']);
    const backgrounds=palette('backgrounds',()=>state.theme+':'+get('palette-region-selection').value);
    for(const region of ['body','header','main','footer']) {
      const prefix=(region==='body'?'page':region)+'-background',key=region==='body'?'background':region+'-background',path=()=>['semanticOverrides',state.theme,key];
      for(const suffix of ['hex','colour','brand'])bind(backgrounds,prefix+'-'+suffix,path,{decode:()=>suffix==='brand'&&!get(prefix+'-brand').value?null:get(prefix+'-'+suffix).value.toUpperCase(),display:()=>window.palette().roles[key]});
      bind(backgrounds,prefix+'-opacity',()=>['backgroundOpacity',state.theme,region],{display:()=>state.backgroundOpacity?.[state.theme]?.[region]??100});
      const changes=()=>[[path(),undefined],[['backgroundOpacity',state.theme,region],undefined]];
      reset(backgrounds,prefix+'-reset',changes);
      for(const side of ['top','right','bottom','left'])bind(backgrounds,region+'-padding-'+side,['regionPadding',region,side],{display:()=>state.regionPadding?.[region]?.[side]??0});
      reset(backgrounds,region+'-padding-reset',()=>['top','right','bottom','left'].map(side=>[['regionPadding',region,side],undefined]));
    }
    reset(backgrounds,'palette-background-clear',()=>{const region=get('palette-region-selection').value;return [[['semanticOverrides',state.theme,region==='body'?'background':region+'-background'],undefined],[['backgroundOpacity',state.theme,region],undefined]];});
    const components=palette('components',()=>get('bdVariant').value),review=palette('review',()=>state.theme+':'+get('palette-status-role').value);
    const feedbackShades=scope('palette-feedback-shades',get('status-palette-steps-controls'),()=>state.theme);
    const buttonColour={bdDefaultBg:'bg',bdText:'text',bdHover:'hover',bdHoverText:'hoverText',bdActive:'active',bdActiveText:'activeText',bdBorderColor:'border'};
    for(const [id,key]of Object.entries(buttonColour))bind(components,id,()=>['buttonDesign','overrides',get('bdVariant').value,key],{display:()=>{const value=window.dssGetButtonContrastData().themes[state.theme][get('bdVariant').value][key==='text'?'fg':key];return validHex(value)?value:get(id).value;}});
    bind(components,'bdFocus',['buttonDesign','focus']);bind(components,'bdSource',()=>['buttonDesign','sources',get('bdVariant').value],{draft:value=>{get('bdCustomWrap').hidden=value!=='custom';}});
    bind(components,'bdCustom',()=>['buttonDesign','custom',get('bdVariant').value],{display:()=>state.buttonDesign.custom[get('bdVariant').value]||state.primary});
    reset(components,'palette-button-clear',()=>[[['buttonDesign','overrides',get('bdVariant').value],undefined]]);
    reset(components,'palette-button-focus-reset',()=>[[['buttonDesign','focus'],DSStudio.project.buttonDefaults().focus]]);
    bind(review,'palette-status-colour',()=>['semanticOverrides',state.theme,get('palette-status-role').value],{display:()=>window.palette().roles[get('palette-status-role').value]});
    reset(review,'palette-status-reset',()=>[[['semanticOverrides',state.theme,get('palette-status-role').value],undefined]]);
    const semantics=DSStudio.propertyActions.create({id:'palette-semantics',parent:get('palette-properties-semantics'),saveButton:get('jSemanticEdit'),discardButton:get('palette-semantic-discard')});
    semantics.save.setAttribute('aria-label','Save semantic colour: review contrast before applying');
    // Existing content and destination forms retain their feature-owned drafts.
    for(const [id,saveId,discardId]of [['content','ia-save','ia-discard'],['sitemap','sitemap-save','sitemap-discard']])DSStudio.propertyActions.create({id,parent:get(saveId).parentElement,saveButton:get(saveId),discardButton:get(discardId)});
    const brief=scope('brief',get('brief-editor')),prototype=scope('prototype',document.querySelector('[data-journey-pane="3"]')),outline=scope('destination-outline',get('plan-pages').parentElement);
    for(const control of document.querySelectorAll('[data-process-field]'))bind(control.dataset.processField==='pages'?outline:control.dataset.processField.startsWith('prototype')?prototype:brief,control,['designProcess',control.dataset.processField],{display:()=>DSStudio.process.currentPlan()[control.dataset.processField],validate:control.dataset.processField==='pages'?value=>value.split('\n').some(line=>line.split('>').length>3)?'Use at most three information levels: Parent > Child > Detail.':'':undefined});
    const typography=scope('typography',get('type-shared-actions'));
    const typeScopes=new Map(['fonts','body','hierarchy','responsive'].map(key=>[key,typography]));
    const typeFields={jFont:['fonts','font'],fontSource:['fonts','fontSettings','source'],fontSystemHeading:['fonts','fontSettings','systemHeading'],fontGoogleBody:['fonts','fontSettings','body'],fontGoogleHeading:['fonts','fontSettings','heading'],jBase:['body','base'],jLeading:['body','leading'],advMeasure:['body','advanced','measure'],jRatio:['hierarchy','ratio'],jHeadingLeading:['hierarchy','headingLeading'],jHeadingTracking:['hierarchy','headingTracking'],jBodyTracking:['body','bodyTracking'],advWeight:['hierarchy','advanced','weight'],clampMinWidth:['responsive','clampConfig','minWidth'],clampMaxWidth:['responsive','clampConfig','maxWidth'],clampFactor:['responsive','clampConfig','mobileFactor']};
    for(const [id,[key,...path]]of Object.entries(typeFields))bind(typeScopes.get(key),id,path,{decode:()=>get(id).type==='range'||id==='advWeight'?Number(get(id).value):get(id).value,draft:id==='fontSource'?value=>{get('fontSystemOptions').hidden=value!=='system';get('fontGoogleOptions').hidden=value!=='google';}:undefined});
    for(const [id,key,owner]of [['base','base','body'],['clampBase','base','body'],['leading','leading','body'],['font','font','fonts'],['ratio','ratio','hierarchy'],['clampRatio','ratio','hierarchy'],['headingTracking','headingTracking','hierarchy'],['bodyTracking','bodyTracking','body'],['typoHeadingTracking','headingTracking','hierarchy'],['typoBodyTracking','bodyTracking','body']])bind(typeScopes.get(owner),id,[key]);
    bind(typeScopes.get('hierarchy'),'advTracking',['headingTracking'],{decode:()=>Number(get('advTracking').value)/100,format:value=>value*100});
    for(const weight of [400,500,600,700,800,900])bind(typeScopes.get('fonts'),'fontWeight'+weight,['fontSettings','weights'],{decode:()=>[400,500,600,700,800,900].filter(value=>get('fontWeight'+value)?.checked),format:value=>value?.includes(weight)||[400,600,700,Number(adv.weight),Number(state.buttonDesign.weight)].includes(weight)});
    reset(typeScopes.get('responsive'),'clampReset',()=>Object.entries(CLAMP_DEFAULTS).map(([key,value])=>[['clampConfig',key],value]));
    for(const id of ['jScalePreset','clampScalePreset'])bind(typeScopes.get('hierarchy'),id,['ratio'],{decode:()=>TYPE_SCALES.find(([key])=>key===get(id).value)?.[2]??null,format:value=>TYPE_SCALES.find(([, ,ratio])=>Math.abs(ratio-value)<.00001)?.[0]||'custom'});
    const buttons=scope('buttons',document.querySelector('[data-journey-pane="7"]'));
    for(const [id,key]of Object.entries({bdSize:'size',bdPaddingX:'padX',bdPaddingY:'padY',bdMinHeight:'minHeight',bdRadius:'radius',bdBorder:'border',bdWeight:'weight',bdFocusWidth:'focusWidth',bdMotion:'motion',bdMobileFull:'mobileFull'}))bind(buttons,id,['buttonDesign',key],{decode:()=>get(id).type==='checkbox'?get(id).checked:get(id).type==='range'||id==='bdWeight'?Number(get(id).value):get(id).value});
    const spacing=scope('spacing',document.querySelector('[data-journey-pane="8"]')),responsive=scope('responsive',document.querySelector('[data-journey-pane="9"]')),accessibility=scope('accessibility',document.querySelector('[data-journey-pane="10"]'));
    for(const [id,key]of [['jSpacing','spacing'],['jRadius','radius'],['spacing','spacing'],['radius','radius']])bind(spacing,id,[key]);
    for(const [id,key]of Object.entries(advMap))if(!bindings.has(get(id)) && id!=='advTracking')bind(['advColumns','advGap','advAlign'].includes(id)?responsive:['advReduce','advUnderline','advMotion','advFocus','advState'].includes(id)?accessibility:spacing,id,['advanced',key],{decode:()=>get(id).type==='checkbox'?get(id).checked:numeric.has(key)?Number(get(id).value):get(id).value});
    for(const control of document.querySelectorAll('[data-responsive-field]'))bind(responsive,control,['responsiveDesign',control.dataset.responsiveField]);
    for(const id of ['process-wireframe','studio-section-6'])scope('preview-'+id,get(id).querySelector(':scope > .panel'),()=>'',true);
    DSStudio.propertyActions.create({id:'colour-lab',parent:get('oklchApply').parentElement,saveButton:get('oklchApply'),discard:()=>get('oklchRole').dispatchEvent(new Event('change',{bubbles:true}))});
    // Native browsing/toggles and feature refreshes may replace field values.
    document.addEventListener('change',()=>queueMicrotask(refresh));document.addEventListener('toggle',()=>queueMicrotask(refresh),true);
    DSStudio.views.subscribe({id:'property-drafts',phase:'lesson',events:['foundation:updated','output:updated','project:sync'],run:refresh});
    DSStudio.on('project:install',()=>{identity=null;refresh();});
    function draftSnapshot(id) {
      const entry=scopes.get(id),candidate=copy(documentValue());
      if(entry)for(const item of records(entry).values())write(candidate,item.path,item.value);
      return DSStudio.project.normalize(candidate);
    }
    DSStudio.propertyEditors={refresh,draftSnapshot,hasDrafts(id){const entry=scopes.get(id);return !!entry && records(entry).size>0;},saveFor(control){const binding=bindings.get(control)||stateBinding(control);if(binding)binding.entry.actions.save.click();},scopes};refresh();
  }
});
