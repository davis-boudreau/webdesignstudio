'use strict';
/* Original controls and shared draft records, with detached teaching specimens. */
DSStudio.register({
  id:'button-workspace',title:'Buttons learning workspace',
  init(){
    const get=id=>document.getElementById(id),section=get('buttonDesignLab'),panel=section.querySelector(':scope > .panel'),pane=document.querySelector('[data-journey-pane="7"]'),api=DSStudio.buttons,editors=DSStudio.propertyEditors;
    const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el;};
    const action=(text,handler)=>{const el=node('button','ghost',text);el.type='button';el.addEventListener('click',handler);return el;};
    const disclosure=(title,content,open=false)=>{const el=node('details','button-learning-details');el.append(node('summary',null,title),content);el.open=open;return el;};
    const workspace=node('section','button-workspace');workspace.id='button-workspace';
    const title=node('h3',null,'Buttons learning workspace');title.id='button-workspace-title';title.tabIndex=-1;
    workspace.setAttribute('aria-labelledby',title.id);
    const header=node('header');header.append(title,node('p','help','Explore the controls, compare proposed buttons and follow their CSS. Save applies all button edits across variants; Discard restores saved values.'));
    const layout=node('div','button-workspace-layout'),controls=node('div','button-workspace-controls'),previews=node('div','button-workspace-previews');layout.append(controls,previews);workspace.append(header,layout);
    const groups=new Map();
    for(const [key,label,help]of [
      ['purpose','Purpose and variant','Choose the action priority. Browsing variants and states preserves proposed edits.'],
      ['size','Size and spacing','Padding and minimum height affect all variants. Small and Large scale the shared dimensions.'],
      ['shape','Shape and typography','Radius, border width and font weight are shared across all variants.'],
      ['colours','Colours and tokens','Sources and colour overrides belong to the selected variant and affect both themes. Focus colour is shared. None makes the selected paint transparent.'],
      ['states','States and behaviour','Focus width, transition timing and mobile width affect the whole system. Simulations demonstrate appearance; test real interaction separately.']
    ]){const body=node('div');body.append(node('p','help',help));const details=disclosure(label,body,['purpose','size'].includes(key));details.id='button-group-'+key;controls.append(details);groups.set(key,body);}
    const move=(id,key)=>{const el=get(id);groups.get(key).append(el.closest('.field')||el.closest('label')||el);};
    move('bdVariant','purpose');move('bdSize','size');move('bdState','states');
    for(const id of ['bdPaddingX','bdPaddingY','bdMinHeight'])move(id,'size');
    for(const id of ['bdRadius','bdBorder','bdWeight','bdElevation'])move(id,'shape');
    for(const id of ['bdFocusWidth','bdMotion','bdMobileFull'])move(id,'states');
    const colours=get('palette-button-colours');groups.get('colours').append(colours);colours.hidden=false;
    const paletteEntry=node('p','help','Button colours share the Buttons draft and action bar.');
    paletteEntry.append(action('Edit colours in Buttons',()=>go('bdSource')));get('palette-properties-components').append(paletteEntry);
    // The old wizard becomes a short entry point; its original controls live here.
    const launch=action('Open Buttons workspace',()=>go(title.id));launch.id='open-button-workspace';
    const notes=node('div');for(const el of [...pane.querySelectorAll(':scope > details.build-guide')])notes.append(el);
    const review=get('bdReview'),selectedReview=get('bdReviewSelection');selectedReview.prepend(node('p','help','Saved-project contrast details. The learning summary above evaluates proposed edits.'));
    const oldActions=editors.scopes.get('buttons');oldActions.actions.bar.hidden=true;oldActions.status.hidden=true;
    const legacy=node('div');legacy.hidden=true;for(const child of [...pane.children])if(child!==oldActions.actions.bar && child!==oldActions.status)legacy.append(child);
    pane.append(node('h3',null,'Buttons'),node('p','help','Design action priority, spacing, colours and states in one learning workspace.'),launch,legacy);
    const meta=node('p','help');meta.id='button-learning-status';meta.setAttribute('role','status');previews.append(node('h4',null,'Button learning preview'),meta);
    const websiteThemeField=node('div','field'),websiteThemeLabel=node('label',null,'Website theme'),websiteTheme=node('select');websiteTheme.id='button-website-theme';websiteThemeLabel.htmlFor=websiteTheme.id;websiteTheme.add(new Option('Light','light'));websiteTheme.add(new Option('Dark','dark'));const websiteThemeHelp=node('p','help','Changes the shared website theme. Unsaved button edits stay in place.');websiteThemeHelp.id='button-website-theme-help';websiteTheme.setAttribute('aria-describedby',websiteThemeHelp.id);websiteThemeField.append(websiteThemeLabel,websiteTheme,websiteThemeHelp);previews.append(websiteThemeField);
    const viewportField=node('div','field'),viewportLabel=node('label',null,'Learning page width'),viewport=node('select');viewport.id='button-learning-viewport';viewportLabel.htmlFor=viewport.id;viewport.add(new Option('Wide context','wide'));viewport.add(new Option('Narrow context (390px maximum)','narrow'));viewportField.append(viewportLabel,viewport);previews.append(viewportField);
    const sample=node('section','button-learning-page');sample.id='button-learning-page';sample.append(node('p','mini','COURSE PLANNER'),node('h4',null,'Keep your next lesson ready'),node('p',null,'Save a lesson to return to it later, or explore the course before deciding.'));
    const context=node('div','button-learning-row');context.id='button-learning-context';context.setAttribute('role','group');context.setAttribute('aria-label','Button variants');sample.append(context);const sampleHost=node('div','button-learning-host');sampleHost.style.overflow='auto';previews.append(sampleHost);const learning=DSStudio.learningPreviews.mount({id:'button-learning-frame',title:'Button learning preview',element:sample,parent:sampleHost,ready:sync,layout:'.button-learning-page { padding: var(--space-4); overflow-wrap: anywhere; } .button-learning-row { display: flex; flex-wrap: wrap; gap: var(--space-3); align-items: center; padding: var(--space-2); }'});
    const previewHint=node('p','help','Compare all five action variants. Select one to edit its properties. This is a local teaching sample.');previewHint.id='button-learning-instructions';previews.append(previewHint);
    const selected=node('section','button-learning-selected');selected.append(node('h4',null,'Selected button and state'),get('bdSingle'),get('bdDescription'),node('p','help','State examples hold an appearance still. Use Tab on the Default specimen to test genuine keyboard focus.'));
    previews.append(selected);
    const sizes=node('div','button-learning-row');sizes.id='button-learning-sizes';previews.append(disclosure('Small, Medium and Large',sizes,true));
    const states=node('div','button-learning-states');states.id='button-learning-states';previews.append(disclosure('Compare states for this variant',states,true));
    const themes=get('bdThemes');previews.append(disclosure('Compare Light and Dark',themes));
    const properties=node('p','help');properties.id='button-learning-properties';previews.append(disclosure('Selected properties and token source',properties));
    const contrast=node('div');contrast.id='button-learning-contrast';previews.append(disclosure('Proposed contrast in both themes',contrast,true));
    const css=node('details','button-learning-css');css.id='button-learning-css';css.append(node('summary',null,'Generated CSS and the calculation'));
    const topic=node('h5');topic.id='button-learning-topic';css.append(topic);const snippet=node('pre','code');snippet.id='button-learning-rule';const lesson=node('p','help');lesson.id='button-learning-explanation';css.append(snippet,lesson);
    const full=node('div');full.append(get('bdCode'),get('bdCopy'),get('bdExport'),node('p','help','Copy uses the proposed stylesheet shown here. Download button CSS exports the saved project; Save first to include proposed changes.'));css.append(disclosure('Complete button stylesheet',full));previews.prepend(css);
    const all=node('div');all.append(get('bdMatrix'),review,selectedReview);workspace.append(disclosure('Complete variant and state reference',all));
    workspace.append(disclosure('Learn about button behaviour',notes));
    const actions=DSStudio.propertyActions.create({id:'button-workspace',parent:workspace,save:()=>editors.saveButtons(),discard:()=>editors.discardButtons()});
    const status=node('p','help');status.id='button-workspace-save-status';status.setAttribute('role','status');workspace.append(status);
    layout.after(actions.bar,status);
    for(const control of controls.querySelectorAll('input,select')){const descriptions=(control.getAttribute('aria-describedby')||'').split(/\s+/).filter(id=>id&&!['property-status-buttons','property-status-palette-components'].includes(id));control.setAttribute('aria-describedby',[...descriptions,status.id].join(' '));}
    // Remove superseded laboratory wrappers, retaining the original lesson and reference.
    const lessonHeader=panel.querySelector(':scope > .studio-lesson');if(lessonHeader)notes.prepend(lessonHeader);
    const old=node('div');old.hidden=true;for(const child of [...panel.children])old.append(child);panel.append(workspace,old);
    let signature='',contrastSignature='',matrixSignature='',matrixFirst=null,syncing=false;
    const painted=new WeakMap();
    let lessonGroup='size',previousLessons=null,lessonIdentity=state;
    function go(id){window.dssRevealSection(id,false);get(id)?.focus();get(id)?.scrollIntoView({block:'center',behavior:'instant'});}
    function revealControl(control){if(!workspace.contains(control))return;for(let el=control;el&&el!==workspace;el=el.parentElement)if(el.tagName==='DETAILS')el.open=true;}
    function paint(container,html){const previous=painted.get(container);if(previous?.html!==html||previous.first!==container.firstChild){container.innerHTML=html;painted.set(container,{html,first:container.firstChild});}}
    function renderLesson(b,foundation,stylesheet){
      const blocks=[...stylesheet.matchAll(/:root \{([^}]+)\}/g)].map(match=>match[1]).join('\n');
      const parse=text=>new Map([...text.matchAll(/(--[\w-]+)\s*:\s*([^;]+);/g)].map(match=>[match[1],match[2].trim()]));
      const root=parse(blocks),dark=parse([...stylesheet.matchAll(/\[data-theme="dark"\] \{([^}]+)\}/g)].map(match=>match[1]).join('\n'));
      const tokens=(names,themed=false)=>{const values=themed&&foundation.theme==='dark'?new Map([...root,...dark]):root;return (themed&&foundation.theme==='dark'?'[data-theme="dark"]':':root')+' {\n'+names.map(name=>'  '+name+': '+values.get(name)+';').join('\n')+'\n}';};
      const rule=selector=>{const start=stylesheet.indexOf(selector+' {');return start<0?'':stylesheet.slice(start,stylesheet.indexOf('}',start)+1);};
      const variant=b.variant,st=b.selectedState,prefix='--button-'+variant+'-',name=api.names[variant];
      topic.textContent={size:'Size and spacing',shape:'Shape and typography',colours:'Colours and tokens',states:'States and behaviour'}[lessonGroup];
      if(lessonGroup==='size'){
        snippet.textContent=tokens(['--button-pad-x','--button-pad-y','--button-min-height'])+'\n.ds-button {\n  padding: var(--button-pad-y) var(--button-pad-x);\n  min-height: var(--button-min-height);\n}'+(b.size==='md'?'':'\n'+rule('.ds-button--'+b.size));
        lesson.textContent='Shared padding: '+b.padY+'px vertically and '+b.padX+'px horizontally. Medium minimum height: '+b.minHeight+'px; content can make it taller. '+({sm:'Small scales padding and minimum height by 0.8 and uses 0.875rem text.',md:'Medium uses the shared dimensions and inherits its text size.',lg:'Large scales padding and minimum height by 1.22 and uses 1.125rem text.'})[b.size]+' These settings affect all variants.';
      }else if(lessonGroup==='shape'){
        snippet.textContent=tokens(['--button-radius','--button-border-width','--button-font-weight'])+'\n.ds-button {\n  border: var(--button-border-width) solid transparent;\n  border-radius: var(--button-radius);\n  font: inherit;\n  font-weight: var(--button-font-weight);\n}';
        const shadow=api.elevation(variant,foundation.theme,b);snippet.textContent+='\n'+(shadow==='none'?'/* '+name+' elevation: None. No shadow rule is exported for this variant. */':tokens([prefix+'shadow'],true)+'\n.ds-button--'+variant+' { --button-elevation-shadow: var('+prefix+'shadow); }\n:is(.ds-button) { box-shadow: var(--button-elevation-shadow, none); }');
        lesson.textContent='All variants use a '+b.radius+'px radius, '+b.border+'px border and font weight '+b.weight+'. '+name+' elevation: '+(b.elevation?.[variant]||'none')+' ('+foundation.theme+' theme: '+api.elevation(variant,foundation.theme,b)+'). Elevation is optional and belongs only to this variant. Each variant supplies its own border colour; transparent paint can hide a border. Font family and inherited text size come from the surrounding typography. Some fonts render nearby weights similarly.';
      }else if(lessonGroup==='colours'){
        snippet.textContent=tokens(['source','bg','text','border','hover','hover-text','active','active-text'].map(key=>prefix+key),true)+'\n'+tokens(['--button-focus'])+'\n'+rule('.ds-button--'+variant)+'\n'+rule('.ds-button--'+variant+':hover:not(:disabled)')+'\n'+rule('.ds-button--'+variant+':active:not(:disabled)');
        lesson.textContent=name+' source: '+api.sourceLabel(variant,b,foundation)+'. The '+foundation.theme+' values above come from the proposed stylesheet. Component rules consume var() references; source tokens can contain resolved colours rather than aliases. Explicit state overrides remain fixed when the source changes. None means transparent paint. Focus colour is shared across variants.';
      }else{
        const selector={default:'.ds-button--'+variant,hover:'.ds-button--'+variant+':hover:not(:disabled)',active:'.ds-button--'+variant+':active:not(:disabled)',focus:'.ds-button:focus-visible',selected:'.ds-button[aria-pressed="true"]',disabled:'.ds-button:disabled',loading:'.ds-button[aria-busy="true"]'}[st];
        const paints=st==='hover'?['hover','hover-text']:st==='active'?['active','active-text']:['bg','text'];
        snippet.textContent=tokens(['--button-focus','--button-focus-width','--button-motion'])+'\n'+tokens(paints.map(key=>prefix+key),true)+'\n.ds-button {\n  transition: background-color var(--button-motion), border-color var(--button-motion);\n}\n'+rule('.ds-button:focus-visible')+'\n'+(st==='focus'?'':rule(selector))+'\n'+(b.mobileFull?'@media (max-width: 40rem) { .ds-button--mobile-full { width: 100%; } }':'/* Full-width mobile actions are off. */')+'\n'+(stylesheet.match(/@media \(prefers-reduced-motion: reduce\) \{ \.ds-button \{ transition: none; \} \}/)?.[0]||'');
        if(api.elevation(variant,foundation.theme,b)!=='none')snippet.textContent+='\n'+DSStudio.buttonStates.elevationCss('.ds-button','data-preview-state','--button-elevation-shadow','--button-focus');
        lesson.textContent=api.stateLabels[st]+'. Shared focus width: '+b.focusWidth+'px; colour transition: '+b.motion+'ms. Full-width mobile actions: '+(b.mobileFull?'on, for elements with .ds-button--mobile-full at 40rem or narrower.':'off.')+' '+({default:'Default is the ready appearance.',hover:'Hover also underlines the label without changing its dimensions.',active:'Pressed also adds a momentary inset cue.',focus:'Use Tab to test the real shared focus outline.',selected:'Toggle selection also uses a checkmark; application logic must update aria-pressed.',disabled:'Use native disabled to prevent activation.',loading:'The shared stylesheet adds the progress indicator; application logic must announce status and prevent duplicate actions.'})[st]+' Optional elevation is layered with pressed and selected cues; the focus outline remains separate. Reduced-motion preferences disable transitions. These are excerpts; the complete stylesheet includes the shared state cues.';
      }
    }
    function sync(){
      if(syncing)return;syncing=true;
      try{
        const dirty=editors.hasButtonDrafts();actions.save.disabled=actions.discard.disabled=!dirty;websiteTheme.value=state.theme;
        if(!section.open && DSStudio.activeStage!==7)return;
        const snapshot=editors.buttonSnapshot(),foundation=snapshot.state,b=foundation.buttonDesign,variant=b.variant,st=b.selectedState,name=api.names[variant];
        colours.hidden=false;websiteTheme.value=foundation.theme;get('bdElevation').value=b.elevation?.[variant]||'none';
        const message=dirty?'Proposed buttons. Save updates the website, wireframes and exports.':'Saved buttons. Learning previews match the project.';
        if(meta.textContent!==message)meta.textContent=message;if(status.textContent!==message)status.textContent=message;
        if(lessonIdentity!==state){lessonIdentity=state;previousLessons=null;lessonGroup='size';}
        const lessonValues={size:JSON.stringify([b.size,b.padX,b.padY,b.minHeight]),shape:JSON.stringify([b.radius,b.border,b.weight,b.elevation]),colours:JSON.stringify([variant,b.sources[variant],b.custom[variant],b.overrides[variant],b.focus,foundation.colourTransparency,foundation.theme,foundation.primary,foundation.secondary,foundation.accent]),states:JSON.stringify([st,b.focusWidth,b.motion,b.mobileFull])};
        if(previousLessons)for(const group of ['size','shape','colours','states'])if(previousLessons[group]!==lessonValues[group])lessonGroup=group;
        previousLessons=lessonValues;
        learning.render(snapshot);
        const key=JSON.stringify([b,foundation.theme,foundation.colourTransparency,foundation.primary,foundation.secondary,foundation.accent,foundation.advanced.reduce,viewport.value,lessonGroup]);
        // Restore shared draft values after the legacy renderer synchronizes its saved controls.
        const resolved=window.dssGetButtonContrastData(b,foundation).themes[foundation.theme][variant];
        for(const [id,key]of Object.entries({bdDefaultBg:'bg',bdText:'fg',bdHover:'hover',bdHoverText:'hoverText',bdActive:'active',bdActiveText:'activeText',bdBorderColor:'border'})){const value=resolved[key];if(validHex(value)){get(id).value=value;get(id+'Out').textContent=value.toUpperCase();}}
        get('bdFocus').value=b.focus;get('bdFocusOut').textContent=b.focus.toUpperCase();
        for(const id of ['bdDefaultBg','bdText','bdHover','bdHoverText','bdActive','bdActiveText','bdBorderColor','bdFocus','bdSource','bdCustom']){const control=get(id),paintKey=editors.transparencyKeyFor(control);control.dataset.transparentColour=String(!!foundation.colourTransparency?.[paintKey]);}
        get('bdSource').value=foundation.colourTransparency?.['button:'+variant+':source']?'none':b.sources[variant];get('bdCustomWrap').hidden=get('bdSource').value!=='custom';
        if(signature!==key){
          signature=key;
          paint(get('bdSingle'),api.specimen(variant,st,b.size,foundation.theme,true,b,foundation));
          const variants=Object.keys(api.names);paint(context,variants.map(key=>api.specimen(key,'default',b.size,foundation.theme,true,b,foundation)).join(''));
          [...context.children].forEach((el,index)=>{el.dataset.buttonVariant=variants[index];el.toggleAttribute('data-learning-selected',variants[index]===variant);if(variants[index]===variant)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');});
          learning.frame.style.maxWidth=viewport.value==='narrow'?'390px':'none';sample.style.maxWidth='none';context.classList.toggle('button-learning-mobile-full',b.mobileFull&&viewport.value==='narrow');
          paint(sizes,['sm','md','lg'].map(size=>'<div><small>'+({sm:'Small',md:'Medium',lg:'Large'})[size]+'</small>'+api.specimen(variant,'default',size,foundation.theme,false,b,foundation)+'</div>').join(''));
          paint(states,api.states.map(stateName=>'<div><small>'+api.stateLabels[stateName]+'</small>'+api.specimen(variant,stateName,b.size,foundation.theme,false,b,foundation)+'</div>').join(''));
          paint(themes,['light','dark'].map(theme=>'<div class="bd-theme-card" data-mode="'+theme+'"><strong>'+theme+'</strong>'+api.specimen(variant,st,b.size,theme,false,b,foundation)+'</div>').join(''));
          for(const el of context.querySelectorAll('.bd-button')){el.removeAttribute('style');el.classList.add('ds-button','ds-button--'+el.dataset.buttonVariant);if(b.size!=='md')el.classList.add('ds-button--'+b.size);if(b.mobileFull)el.classList.add('ds-button--mobile-full');}learning.size();
          properties.textContent=name+' / '+b.size.toUpperCase()+'. '+api.sourceLabel(variant,b,foundation)+'. Padding '+b.padY+'px '+b.padX+'px; medium minimum height '+b.minHeight+'px; radius '+b.radius+'px; border '+b.border+'px; weight '+b.weight+'. Elevation '+(b.elevation?.[variant]||'none')+'. Colour token: --button-'+variant+'-bg. '+(b.overrides[variant]?'This variant has explicit colour overrides.':'Generated state colours follow its source.');
          get('bdCode').textContent=api.css(b,foundation);
          renderLesson(b,foundation,api.css(b,foundation));
        }
        if(matrixSignature!==key||matrixFirst!==get('bdMatrix').firstChild){paint(get('bdMatrix'),api.matrix(b,foundation));matrixSignature=key;matrixFirst=get('bdMatrix').firstChild;}
        // The saved renderer can run independently after a theme/output change.
        paint(get('bdSingle'),api.specimen(variant,st,b.size,foundation.theme,true,b,foundation));
        paint(themes,['light','dark'].map(theme=>'<div class="bd-theme-card" data-mode="'+theme+'"><strong>'+theme+'</strong>'+api.specimen(variant,st,b.size,theme,false,b,foundation)+'</div>').join(''));
        if(get('bdCode').textContent!==api.css(b,foundation))get('bdCode').textContent=api.css(b,foundation);
        const contrastKey=JSON.stringify([b,foundation.theme,foundation.semanticOverrides,foundation.semanticSources,foundation.backgroundOpacity,foundation.colourTransparency,foundation.primary,foundation.secondary,foundation.accent]);
        if(contrastSignature!==contrastKey){contrastSignature=contrastKey;contrast.replaceChildren();const rows=window.dssContrastTools.collect({foundation,buttonSettings:b});
          for(const theme of ['light','dark']){const relevant=rows.filter(row=>row.theme===theme&&row.state===st&&row.group.startsWith('Button Laboratory:')&&(row.name===name||row.name.startsWith(name+' '))),required=relevant.filter(row=>row.scope==='required'&&row.threshold!==null),lowest=required.reduce((a,row)=>!a||row.ratio<a.ratio?row:a,null),failures=required.filter(row=>row.status==='review');
            const line=node('p','help',theme+': '+(!required.length?'Inactive state: contrast exemption.':failures.length?failures.length+' required pairs need review.':'Required pairs meet their targets.')+(lowest?' Lowest required ratio '+lowest.ratio.toFixed(2)+':1 ('+lowest.name+' on '+lowest.location+').':''));contrast.append(line);
          }contrast.append(node('p','help','Checks cover the audited host surfaces. Conditional boundaries are separate; keyboard focus, meaning, geometry and real behaviour still need review.'));
        }
      }finally{syncing=false;}
    }
    controls.addEventListener('focusin',event=>{const group=event.target.closest('[id^="button-group-"]')?.id.slice('button-group-'.length);if(group&&group!=='purpose'){lessonGroup=group;sync();}});
    DSStudio.learningPreviews.bindTheme(websiteTheme,()=>{previousLessons=null;signature='';sync();});
    workspace.addEventListener('input',sync);workspace.addEventListener('change',sync);
    const previousReveal=window.dssRevealSection;window.dssRevealSection=function(id,scroll=true){revealControl(get(id));return previousReveal(id,scroll);};
    // Matrix clicks browse the selected state without committing properties.
    get('bdMatrix').addEventListener('click',event=>{const button=event.target.closest('.bd-button');if(!button)return;const cell=button.closest('.bd-cell'),variant=Object.keys(api.names).find(key=>api.names[key]===cell?.querySelector('strong')?.textContent);if(variant){window.dssSelectButtonState(variant,button.dataset.sim||'default');editors.refresh();go('bdVariant');}});
    context.addEventListener('click',event=>{const button=event.target.closest('[data-button-variant]');if(!button||!Object.hasOwn(api.names,button.dataset.buttonVariant))return;window.dssSelectButtonState(button.dataset.buttonVariant,'default');editors.refresh();go('bdVariant');});
    DSStudio.on('properties:refreshed',sync);DSStudio.on('contrast:updated',sync);
    DSStudio.views.subscribe({id:'button-learning-preview',phase:'lesson',events:['foundation:updated','output:updated','project:sync'],run:()=>{signature='';sync();}});
    section.addEventListener('toggle',()=>{if(section.open)sync();});
    DSStudio.buttonWorkspace={sync,revealControl};sync();DSStudio.emit('lesson:content');
  }
});
