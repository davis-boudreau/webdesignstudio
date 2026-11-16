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
    function transparencyKey(path){
      if(path[0]==='semanticOverrides')return path[1]+':'+path[2];
      if(['primary','secondary','accent'].includes(path[0]))return 'anchor:'+path[0];
      if(path[0]==='advanced' && path[1]==='colors')return 'light:'+path[2];
      if(path[0]==='backgroundOpacity')return path[1]+':'+(path[2]==='body'?'background':path[2]+'-background');
      if(path[0]==='buttonDesign'){
        if(path[1]==='focus')return 'button:focus';
        if(path[1]==='sources'||path[1]==='custom')return 'button:'+path[2]+':source';
        if(path[1]==='overrides' && path[3])return 'button:'+path[2]+':'+path[3];
      }
      return null;
    }
    function transparentBinding(control){return bindings.get(control)||stateBinding(control);}
    function setTransparent(control,value=true){
      const binding=transparentBinding(control),key=binding && transparencyKey(binding.path());if(!key)return false;
      stage({entry:binding.entry,control,path:()=>['colourTransparency',key]},value?true:undefined);return true;
    }
    function stage(binding,value) {
      const entry=binding.entry,path=binding.path();if(!path)return;
      const current=read(documentValue(),path),items=records(entry),key=JSON.stringify(path);
      // A button property has one proposed value even when edited from another variant.
      if(path[0]==='buttonDesign' || path[0]==='colourTransparency' && path[1].startsWith('button:'))for(const pending of entry.drafts.values())if(pending!==items)pending.delete(key);
      const buttonOverride=path[0]==='buttonDesign'&&path[1]==='overrides';
      if(buttonOverride&&path.length===3)for(const pending of entry.drafts.values())for(const [id,item]of pending)if(item.path.length>3&&item.path.slice(0,3).every((part,index)=>part===path[index]))pending.delete(id);
      const parentReset=buttonOverride&&path.length===4&&[...entry.drafts.values()].some(pending=>pending.has(JSON.stringify(path.slice(0,3))));
      if(equal(current,value)&&!parentReset)items.delete(key);else items.set(key,{path,base:copy(items.get(key)?.base??current),value:copy(value),control:binding.control});
      const paintKey=transparencyKey(path);
      if(paintKey){const clearPath=['colourTransparency',paintKey],base=read(documentValue(),clearPath),clearKey=JSON.stringify(clearPath);if(paintKey.startsWith('button:'))for(const pending of entry.drafts.values())if(pending!==items)pending.delete(clearKey);if(base===undefined)items.delete(clearKey);else items.set(clearKey,{path:clearPath,base:copy(base),value:undefined,control:binding.control});}

      if(path[0]==='semanticOverrides') {
        const token=binding.control.selectedOptions?.[0]?.dataset.token,sourcePath=['semanticSources',path[1],path[2]];
        const source=token && validHex(value)?{token,hex:value.toUpperCase()}:undefined;
        const sourceKey=JSON.stringify(sourcePath),base=read(documentValue(),sourcePath);
        if(equal(base,source))items.delete(sourceKey);else items.set(sourceKey,{path:sourcePath,base:copy(base),value:source,control:binding.control});
      }
      if(path[0]==='buttonDesign' && path[1]==='sources' && binding.control.value==='default') {
        const clearPath=['buttonDesign','overrides',path[2]],base=read(documentValue(),clearPath);
        for(const [key,item]of items)if(item.path[0]==='buttonDesign' && item.path[1]==='overrides' && item.path[2]===path[2])items.delete(key);
        if(base!==undefined)items.set(JSON.stringify(clearPath),{path:clearPath,base:copy(base),value:undefined,control:binding.control});
        for(const key of new Set([...Object.keys(state.colourTransparency||{}),...Array.from(items.values()).filter(item=>item.path[0]==='colourTransparency').map(item=>item.path[1])]))if(key.startsWith('button:'+path[2]+':')){
          const paintPath=['colourTransparency',key],paintBase=read(documentValue(),paintPath),paintId=JSON.stringify(paintPath);
          if(paintBase===undefined)items.delete(paintId);else items.set(paintId,{path:paintPath,base:copy(paintBase),value:undefined,control:binding.control});
        }

      }
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
          if(value===undefined){
            if(item && path[0]==='semanticOverrides') {
              const candidate={...state,semanticOverrides:{...state.semanticOverrides,[path[1]]:{...state.semanticOverrides?.[path[1]],[path[2]]:undefined}}};
              binding.control.value=binding.control.tagName==='SELECT'?'default':window.palette(path[1],candidate).roles[path[2]];
            }
            continue;
          }
          if(binding.control.type==='checkbox')binding.control.checked=!!value;else binding.control.value=String(value);
          // Custom HEX values need the real Custom option, rather than an
          // unselected list that can visually fall back to the first None row.
          if(binding.control.tagName==='SELECT' && binding.control.selectedIndex<0 && /-brand$|^j(?:Primary|Secondary|Accent)Brand$|^brandAccent$/.test(binding.control.id))binding.control.value='';
          if(path[0]==='semanticOverrides' && binding.control.tagName==='SELECT') {
            const sourcePath=['semanticSources',path[1],path[2]],pending=items.get(JSON.stringify(sourcePath));
            const source=pending?pending.value:read(model,sourcePath);
            const option=source && [...binding.control.options].find(option=>option.dataset.token===source.token && option.value===String(value));
            if(option)option.selected=true;
          }
          const paintKey=transparencyKey(path),paintItem=paintKey && items.get(JSON.stringify(['colourTransparency',paintKey]));
          const transparent=paintItem?paintItem.value:state.colourTransparency?.[paintKey];
          binding.control.dataset.transparentColour=String(!!transparent);
          if(transparent && binding.control.tagName==='SELECT' && [...binding.control.options].some(option=>option.value==='none'))binding.control.value='none';
          if(binding.validate)binding.control.setCustomValidity(binding.validate(binding.control.value));
          if(binding.control.pattern)binding.control.setAttribute('aria-invalid',String(!binding.control.validity.valid));
          const output=get(binding.control.id+'Out')||get(binding.control.id+'-value');
          if(output && typeof value==='number')output.textContent=output.textContent.replace(/-?\d+(?:\.\d+)?/,String(binding.control.id==='clampFactor'?Math.round(value*100):binding.control.id==='advTracking'?value/100:value));
        }
        if(entry.status){entry.actions.save.disabled=!items.size;entry.actions.discard.disabled=!items.size;entry.status.textContent=entry.message||(entry.id==='palette-backgrounds'?(items.size?'Unsaved backgrounds. The learning preview shows proposed values; Save updates the website.':'Backgrounds saved. The learning preview matches the project.'):entry.id==='spacing'?(items.size?'Unsaved spacing and surfaces. The learning preview shows proposed values; Save updates the website.':'Spacing and surfaces saved. Learning preview matches the project.'):entry.id==='typography'?(items.size?'Unsaved typography. The sample and scale show proposed values; Save updates the full website.':'Typography saved. The learning previews match the project.'):(items.size?'Unsaved properties. Save to update the project; preview shows saved values.':'Properties saved. Preview shows the saved project.'));}
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
        const value=item?item.value:path[0]==='semanticOverrides'?semanticSource(path[2])?.hex||read(model,path):read(model,path);
        const paintKey=transparencyKey(path),paintItem=records(binding.entry).get(JSON.stringify(['colourTransparency',paintKey]));
        if(paintItem?paintItem.value:state.colourTransparency?.[paintKey]){control.value='none';continue;}
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
      event.stopImmediatePropagation();if(event.target.value==='none' && transparencyKey(binding.path())){setTransparent(event.target);return;}const value=binding.decode();if(value!==null)stage(binding,value);
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
      for(const id of [role,'j'+name,'j'+name+'Brand'])bind(anchors,id,[role],{decode:()=>get(id).value==='default'?DEFAULT[role]:validHex(get(id).value)?get(id).value.toLowerCase():null,display:()=>state[role].toUpperCase(),format:value=>value?.toUpperCase()});
      reset(anchors,'palette-reset-'+role,()=>[[[role],DEFAULT[role]]]);
    }
    bind(anchors,'brandAccent',['accent'],{events:['change'],decode:()=>get('brandAccent').value==='default'?DEFAULT.accent:validHex(get('brandAccent').value)?get('brandAccent').value.toLowerCase():null,display:()=>state.accent.toUpperCase()});
    const shades=palette('shades');for(const id of ['jRamp','method'])bind(shades,id,['method']);
    const backgrounds=palette('backgrounds',()=>state.theme);
    for(const region of ['body','header','main','footer']) {
      const prefix=(region==='body'?'page':region)+'-background',key=region==='body'?'background':region+'-background',path=()=>['semanticOverrides',state.theme,key];
      for(const suffix of ['hex','colour','brand'])bind(backgrounds,prefix+'-'+suffix,path,{decode:()=>suffix==='brand'&&get(prefix+'-brand').value==='default'?undefined:suffix==='brand'&&!get(prefix+'-brand').value?null:get(prefix+'-'+suffix).value.toUpperCase(),display:()=>suffix==='brand'&&!state.semanticOverrides?.[state.theme]?.[key]?'default':window.palette().roles[key]});
      bind(backgrounds,prefix+'-opacity',()=>['backgroundOpacity',state.theme,region],{display:()=>colourIsTransparent(key)?0:state.backgroundOpacity?.[state.theme]?.[region]??100});
      const changes=()=>[[path(),undefined],[['backgroundOpacity',state.theme,region],undefined]];
      reset(backgrounds,prefix+'-reset',changes);
      for(const side of ['top','right','bottom','left'])bind(backgrounds,region+'-padding-'+side,['regionPadding',region,side],{display:()=>state.regionPadding?.[region]?.[side]??0});
      reset(backgrounds,region+'-padding-reset',()=>['top','right','bottom','left'].map(side=>[['regionPadding',region,side],undefined]));
    }
    reset(backgrounds,'palette-background-clear',()=>{const region=get('palette-region-selection').value;return [[['semanticOverrides',state.theme,region==='body'?'background':region+'-background'],undefined],[['backgroundOpacity',state.theme,region],undefined]];});
    const components=palette('components',()=>get('bdVariant').value),review=palette('review',()=>state.theme+':'+get('palette-status-role').value);
    const feedbackShades=scope('palette-feedback-shades',get('status-palette-steps-controls'),()=>state.theme);
    const buttonColour={bdDefaultBg:'bg',bdText:'text',bdHover:'hover',bdHoverText:'hoverText',bdActive:'active',bdActiveText:'activeText',bdBorderColor:'border'};
    for(const [id,key]of Object.entries(buttonColour))bind(components,id,()=>['buttonDesign','overrides',get('bdVariant').value,key],{display:()=>{const property=key==='text'?'fg':key,variant=get('bdVariant').value,value=window.dssGetButtonContrastData().themes[state.theme][variant][property];if(validHex(value))return value;const retained=window.dssGetButtonContrastData(state.buttonDesign,{...state,colourTransparency:{}}).themes[state.theme][variant][property];return validHex(retained)?retained:get(id).value;}});
    bind(components,'bdFocus',['buttonDesign','focus']);bind(components,'bdSource',()=>['buttonDesign','sources',get('bdVariant').value],{decode:()=>get('bdSource').value==='default'?DSStudio.project.buttonDefaults().sources[get('bdVariant').value]:get('bdSource').value,draft:value=>{get('bdCustomWrap').hidden=value!=='custom';}});
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
    bind(buttons,'bdElevation',()=>['buttonDesign','elevation',get('bdVariant').value],{decode:()=>get('bdElevation').value==='none'?undefined:get('bdElevation').value,format:value=>value||'none'});
    for(const [id,key]of Object.entries({bdSize:'size',bdPaddingX:'padX',bdPaddingY:'padY',bdMinHeight:'minHeight',bdRadius:'radius',bdBorder:'border',bdWeight:'weight',bdFocusWidth:'focusWidth',bdMotion:'motion',bdMobileFull:'mobileFull'}))bind(buttons,id,['buttonDesign',key],{decode:()=>get(id).type==='checkbox'?get(id).checked:get(id).type==='range'||id==='bdWeight'?Number(get(id).value):get(id).value});
    const spacing=scope('spacing',document.querySelector('[data-journey-pane="8"]')),responsive=scope('responsive',document.querySelector('[data-journey-pane="9"]')),accessibility=scope('accessibility',document.querySelector('[data-journey-pane="10"]'));
    for(const [id,key]of [['jSpacing','spacing'],['jRadius','radius'],['spacing','spacing'],['radius','radius']])bind(spacing,id,[key]);
    for(const [id,key]of Object.entries(advMap))if(!bindings.has(get(id)) && id!=='advTracking')bind(['advColumns','advGap','advAlign'].includes(id)?responsive:['advReduce','advUnderline','advMotion','advFocus','advState','advHeight'].includes(id)?accessibility:spacing,id,['advanced',key],{decode:()=>get(id).type==='checkbox'?get(id).checked:numeric.has(key)?Number(get(id).value):get(id).value});
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
    // Buttons owns a combined view of geometry and Palette's variant-colour drafts.
    // Keep the original records so both entry points see the same edits.
    function buttonRecords() {
      return [buttons,components].flatMap(entry=>[...entry.drafts.values()].flatMap(items=>[...items.values()].filter(item=>item.path[0]==='buttonDesign' || item.path[0]==='colourTransparency' && item.path[1].startsWith('button:')).map(item=>({items,item}))));
    }
    function buttonSnapshot() {
      const candidate=copy(documentValue());for(const {item}of buttonRecords())write(candidate,item.path,item.value);
      return DSStudio.project.normalize(candidate);
    }
    function finishButtons(commit) {
      refresh();const pending=buttonRecords();if(!pending.length)return;
      if(commit){
        for(const {item}of pending)if(!item.control.reportValidity())return;
        const model=buttonSnapshot().state;
        for(const {item}of pending)write(state,item.path,read(model,item.path));
      }
      for(const {items,item}of pending)items.delete(JSON.stringify(item.path));
      if(commit){syncControls();syncAdvanced();DSStudio.emit('properties:committed');apply();window.dssAutosave?.();}
      refresh();
    }
    DSStudio.propertyEditors={refresh,draftSnapshot,buttonSnapshot,hasButtonDrafts:()=>buttonRecords().length>0,saveButtons:()=>finishButtons(true),discardButtons:()=>finishButtons(false),setTransparent,transparencyKeyFor(control){const binding=transparentBinding(control);return binding && transparencyKey(binding.path());},hasDrafts(id){const entry=scopes.get(id);return !!entry && records(entry).size>0;},saveFor(control){const binding=bindings.get(control)||stateBinding(control);if(binding)binding.entry.actions.save.click();},scopes};refresh();
  }
});
