'use strict';
/* One normalized draft, existing component CSS and a script-free local sample. */
DSStudio.register({
  id:'spacing-workspace',title:'Spacing and surfaces learning workspace',
  init(){
    const get=id=>document.getElementById(id),section=get('studio-section-3'),panel=section.querySelector(':scope > .panel'),pane=document.querySelector('[data-journey-pane="8"]'),editors=DSStudio.propertyEditors;
    const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el;};
    const action=(text,handler)=>{const el=node('button','ghost',text);el.type='button';el.addEventListener('click',handler);return el;};
    const details=(text,body,open=false)=>{const el=node('details','spacing-workspace-details');el.append(node('summary',null,text),body);el.open=open;return el;};
    const workspace=node('section','spacing-workspace');workspace.id='spacing-workspace';
    const title=node('h3',null,'Spacing and surfaces learning workspace');title.id='spacing-workspace-title';title.tabIndex=-1;workspace.setAttribute('aria-labelledby',title.id);
    workspace.append(title,node('p','help','Explore spacing and surfaces on a small page. Proposed edits update this learning preview; Save applies them to the website and exports.'));
    const layout=node('div','spacing-workspace-layout'),controls=node('div','spacing-workspace-controls'),previews=node('div','spacing-workspace-previews');layout.append(controls,previews);workspace.append(layout);panel.append(workspace);
    const groups=new Map();
    for(const [key,label,help]of [
      ['scale','Spacing system','The base unit generates related spacing tokens. Changing it updates every rule using those tokens.'],
      ['relationships','Inside and outside spacing','Inspect padding inside a card, paragraph margins and grid gap between cards. Values follow the existing website rules.'],
      ['shape','Shape and borders','Base radius shapes cards and inputs. Border width is shared by cards and form fields. Buttons keep their own geometry.'],
      ['surfaces','Surfaces and elevation','Surface colours follow Palette. Elevation adds a shadow; Component opacity fades the whole card, including text and controls.']
    ]){const body=node('div');body.append(node('p','help',help));const group=details(label,body,['scale','shape'].includes(key));group.id='spacing-group-'+key;groups.set(key,body);controls.append(group);}
    for(const [id,key]of [['jSpacing','scale'],['jRadius','shape'],['advBorder','shape'],['advShadow','surfaces'],['advOpacity','surfaces']])groups.get(key).append(get(id).closest('.field'));
    const opacityLabel=document.querySelector('label[for="advOpacity"]');for(const child of opacityLabel.childNodes)if(child.nodeType===Node.TEXT_NODE&&child.textContent.trim())child.textContent='Component opacity (%) ';
    const measured=node('p','help');measured.id='spacing-selected-properties';groups.get('relationships').append(measured);
    const links=node('div','spacing-workspace-links');
    for(const [label,id]of [['Edit grid gap in Responsive layout','advGap'],['Edit page-region padding in Palette','body-padding-top'],['Edit surface colours in Palette','jSemanticRole'],['Edit control height in Accessibility','advHeight'],['Edit button geometry in Buttons','bdRadius']])links.append(action(label,()=>{if(id==='jSemanticRole'){get(id).value='surface';get(id).dispatchEvent(new Event('change',{bubbles:true}));}go(id);}));
    groups.get('relationships').append(links);
    const surfaceTokens=node('p','help');surfaceTokens.id='spacing-surface-tokens';groups.get('surfaces').append(surfaceTokens);
    function select(id,label,options,parent){const field=node('div','field'),caption=node('label',null,label),control=node('select');caption.htmlFor=id;control.id=id;for(const [value,text]of options)control.add(new Option(text,value));field.append(caption,control);parent.append(field);return control;}
    previews.append(node('h4',null,'Spacing and surfaces learning preview'));
    const tools=node('div','spacing-learning-tools');previews.append(tools);
    const theme=select('spacing-website-theme','Website theme',[['light','Light'],['dark','Dark']],tools),width=select('spacing-learning-width','Learning page width',[['fluid','Available width'],['320','Narrow (320px maximum)']],tools);
    const chosen=select('spacing-learning-element','Element to inspect',[['section','Page section'],['card','First card'],['card-secondary','Second card'],['nested','Nested surface'],['input','Form field']],groups.get('relationships'));chosen.value='card';
    const overlayLabel=node('label','checkrow'),overlay=node('input');overlay.type='checkbox';overlay.id='spacing-learning-overlays';overlayLabel.append(overlay,document.createTextNode('Show padding, margin and gap guides'));tools.append(overlayLabel);
    const meta=node('p','help');meta.id='spacing-learning-status';meta.setAttribute('role','status');previews.append(meta);
    const scroller=node('div','spacing-learning-scroller'),frame=node('iframe');frame.id='spacing-learning-frame';frame.title='Spacing and surfaces offline learning page';frame.setAttribute('sandbox','allow-same-origin');scroller.append(frame);previews.append(scroller);
    previews.append(node('p','help','Click a card, nested surface or field to inspect it. Spacing and shape are shared across themes. Opacity fades content too; review it against the chosen background. Guides and element selection affect only this learning sample.'));
    const scale=node('section'),scaleTitle=node('h4',null,'Complete spacing ladder'),ladder=node('div','spacing-learning-ladder');ladder.id='spacing-learning-ladder';scale.append(scaleTitle,node('p','help','Labels show current pixel sizes. Bars compare the token multiples; select a token to follow its calculation.'),ladder);previews.append(scale);
    const barRows=new Map();for(const n of SPACING_STEPS){const row=action('',()=>{selectedToken=n;topic='scale';sync();});row.dataset.spacingToken=String(n);const label=node('span'),bar=node('i');bar.setAttribute('aria-hidden','true');bar.style.width=n/Math.max(...SPACING_STEPS)*100+'%';row.append(label,bar);ladder.append(row);barRows.set(n,{row,label});}
    const cssPanel=node('details','spacing-learning-css');cssPanel.id='spacing-learning-css';cssPanel.append(node('summary',null,'Generated CSS and the calculation'));const cssTitle=node('h5'),code=node('pre','code'),explanation=node('p','help');cssTitle.id='spacing-learning-topic';code.id='spacing-learning-code';explanation.id='spacing-learning-explanation';cssPanel.append(cssTitle,code,explanation);previews.prepend(cssPanel);
    // Keep the existing saved-output exercises intact as optional reference tools.
    const saved=node('div'),savedSummary=details('Compare saved values and inspect the website',saved);savedSummary.id='spacing-saved-reference';
    const lesson=panel.querySelector(':scope > .studio-lesson'),utility=get('utilityLesson');saved.append(lesson);
    const practice=details('Further learning: local utilities and Tailwind',utility);practice.id='spacing-further-learning';
    const diagnostics=node('div'),diagnosticDetails=details('Saved component examples',diagnostics);diagnosticDetails.id='spacing-saved-diagnostics';
    for(const child of [...panel.children])if(child!==workspace)diagnostics.append(child);
    workspace.append(savedSummary,practice,diagnosticDetails);
    const entry=editors.scopes.get('spacing');layout.after(entry.actions.bar,entry.status);
    const old=node('div');old.hidden=true;for(const child of [...pane.children])old.append(child);pane.append(node('h3',null,'Spacing and surfaces'),node('p','help','Explore spacing tokens, card shapes and surface layers in one workspace.'),action('Open Spacing and surfaces workspace',()=>go(title.id)),old);
    panel.append(workspace);
    let selectedToken=6,topic='scale',previous=null,identity=state,signature='',rendering=false;
    const scaffold=`
html { overflow-wrap: anywhere; } * { box-sizing: border-box; }
.spacing-sample-main { padding-inline: var(--space-4); }
.spacing-sample-main h3 { font-size: 1.125rem; line-height: 1.3; margin: 0 0 var(--space-4); }
.spacing-sample-main p { margin: 0 0 var(--space-6); }
.spacing-sample-main .card { min-width: 0; }
.spacing-sample-main .nested-surface { padding: var(--space-4); background: var(--surface-muted); border: var(--border-width) solid var(--border); border-radius: var(--radius-base); }
.spacing-sample-main .input { display: block; width: 100%; padding: var(--space-2); border-radius: var(--radius-base); background: var(--surface); color: var(--text); font: inherit; }
.spacing-sample-main label { display: block; margin-bottom: var(--space-2); }
[data-space-selected] { outline: 2px solid var(--learning-ui-focus); outline-offset: 3px; }
html[data-guides] .card { background-image: linear-gradient(var(--surface),var(--surface)); background-origin: content-box; background-repeat: no-repeat; background-color: var(--surface-muted); }
html[data-guides] .card-grid { outline: 2px dashed var(--control-border); background: var(--surface-muted); }
html[data-guides] .card p { outline: 1px dashed var(--control-border); box-shadow: 0 var(--space-6) 0 var(--surface-muted); }
`;
    // No project strings are parsed as HTML. All generated CSS is assigned as text.
    frame.srcdoc='<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><style id="spacing-draft-style"></style><style id="spacing-layout-style"></style></head><body><main class="spacing-sample-main"><section id="spacing-sample-section" data-space-part="section"><h3>Make room for learning</h3><div class="card-grid"><article class="card" data-space-part="card"><h3>A clear starting point</h3><p>Related spacing helps the content feel connected.</p><div class="nested-surface" data-space-part="nested"><label for="spacing-sample-input">Example field</label><input class="input" id="spacing-sample-input" data-space-part="input" value="Your next lesson"></div></article><article class="card" data-space-part="card-secondary"><h3>Keep the rhythm</h3><p>Card padding uses six spacing units. Grid gap has its own Responsive setting.</p><button type="button" class="ds-button ds-button--primary">Explore a lesson</button></article></div></section></main></body></html>';
    function go(id){window.dssRevealSection(id,false);get(id)?.focus();get(id)?.scrollIntoView({block:'center',behavior:'instant'});}
    function revealControl(control){if(!workspace.contains(control))return;for(let el=control;el&&el!==workspace;el=el.parentElement)if(el.tagName==='DETAILS')el.open=true;}
    function rules(css,selector){const found=[...css.matchAll(new RegExp('(?:^|\\n)('+selector.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+' \\{[^}]*\\})','g'))].map(match=>match[1]);return [...new Set(found)].map(rule=>rule.replace('{ ','{\n  ').replace(/; /g,';\n  ').replace('\n  }','\n}')).join('\n');}
    function renderLesson(snapshot,css,doc){
      const s=snapshot.state,a=s.advanced,tokens=window.dssReadTokens(css),names=topic==='scale'?['--space-unit','--space-'+selectedToken]:topic==='shape'?['--radius-base','--border-width']:topic==='surfaces'?['--surface-opacity','--elevation']:['--space-6','--space-4','--grid-gap','--control-height'];
      const declarations=names.map(name=>{const row=tokens.findLast(row=>row.name===name&&row.scope!=='Dark');return '  '+name+': '+(row?.value||'/* Inspect full CSS */')+';';}).join('\n');
      cssTitle.textContent={scale:'Spacing system',relationships:'Inside and outside spacing',shape:'Shape and borders',surfaces:'Surfaces and elevation'}[topic];
      code.textContent=':root {\n'+declarations+'\n}\n'+(topic==='scale'?rules(css,'.card'):topic==='shape'?rules(css,'.card')+'\n'+rules(css,'.input'):topic==='surfaces'?rules(css,'.card'):rules(css,'.card')+'\n'+rules(css,'.card-grid'));
      // The displayed declarations and rendered page use the same draft stylesheet.
      explanation.textContent=topic==='scale'?s.spacing+'px per unit x '+selectedToken+' = '+s.spacing*selectedToken+'px for --space-'+selectedToken+'. Cards use --space-6 ('+s.spacing*6+'px). Grid gap stays '+a.gap+'px unless changed in Responsive layout.':topic==='shape'?'Base radius '+s.radius+'px; border width '+a.border+'px. Cards and fields use these shared values. Buttons have independent radius and border settings in Buttons.':topic==='surfaces'?'Component opacity '+a.opacity+'% affects the whole card, including its text, nested field and action. Elevation is '+a.shadow+'. Surface colours resolve through --surface and --surface-muted in the '+s.theme+' website theme. Change background paint opacity separately in Palette.':'Card padding follows --space-6; nested padding uses --space-4 in this learning sample. Paragraph bottom margin uses --space-6. Grid gap '+a.gap+'px and field minimum height '+a.height+'px are saved settings owned by Responsive layout and Accessibility.';
      const target=doc.querySelector('[data-space-part="'+chosen.value+'"]'),style=target&&frame.contentWindow.getComputedStyle(target),paragraph=doc.querySelector('.card p');
      measured.textContent=style?'Inspecting '+chosen.selectedOptions[0].textContent+': padding '+style.padding+'; border '+style.borderTopWidth+'; radius '+style.borderTopLeftRadius+'. Card paragraph bottom margin '+frame.contentWindow.getComputedStyle(paragraph).marginBottom+'. Grid gap '+a.gap+'px is independent of the base unit.':'The preview is loading.';
      for(const el of doc.querySelectorAll('[data-space-selected]'))el.removeAttribute('data-space-selected');if(target)target.setAttribute('data-space-selected','');
    }
    function sync(){
      if(rendering)return;rendering=true;
      try{
        if(identity!==state){identity=state;selectedToken=6;topic='scale';previous=null;signature='';chosen.value='card';overlay.checked=false;width.value='fluid';}
        theme.value=state.theme;if(!section.open&&DSStudio.activeStage!==8)return;
        const snapshot=editors.draftSnapshot('spacing'),s=snapshot.state,a=s.advanced,dirty=editors.hasDrafts('spacing'),doc=frame.contentDocument;
        if(!doc?.getElementById('spacing-draft-style'))return;
        const values={scale:s.spacing,shape:JSON.stringify([s.radius,a.border]),surfaces:JSON.stringify([a.shadow,a.opacity])};
        if(previous)for(const key of ['scale','shape','surfaces'])if(values[key]!==previous[key])topic=key;previous=values;
        const css=DSStudio.exports.css(s.sampleMode,snapshot),key=JSON.stringify([css,s.spacing,s.radius,s.theme,width.value,s.buttonDesign.size,DSStudio.fonts.showFallback]);
        if(signature!==key){signature=key;doc.getElementById('spacing-draft-style').textContent=css;doc.getElementById('spacing-layout-style').textContent=scaffold+DSStudio.fonts.previewCss();doc.documentElement.dataset.theme=s.theme;doc.querySelector('.ds-button').className=DSStudio.samples.buttonClass('primary');doc.body.className=s.sampleMode==='basic'?'spacing-sample-page':'sample-home spacing-sample-page';doc.getElementById('spacing-sample-section').className=s.sampleMode==='basic'?'section':'sample-section';frame.style.width=width.value==='320'?'320px':'100%';}
        DSStudio.fonts.syncLearning(doc,s,()=>{},DSStudio.fonts.showFallback,true);
        DSStudio.learningPreviews.guideColours(doc);
        doc.documentElement.toggleAttribute('data-guides',overlay.checked);theme.value=s.theme;
        const message=(dirty?'Proposed':'Saved')+' spacing and surfaces / '+(s.theme==='dark'?'Dark':'Light')+' website theme. Save applies edits to the full website.';if(meta.textContent!==message)meta.textContent=message;
        for(const [n,{row,label}]of barRows){label.textContent='--space-'+n+' / '+n*s.spacing+'px';row.setAttribute('aria-pressed',String(n===selectedToken));}
        const roles=palette(s.theme,s).roles;surfaceTokens.textContent='--surface: '+roles.surface+'; --surface-muted: '+roles['surface-muted']+'; --border: '+roles.border+'. Colours are shared with Palette; Component opacity is '+a.opacity+'%.';
        renderLesson(snapshot,css,doc);
      }finally{rendering=false;}
    }
    frame.addEventListener('load',()=>{frame.contentDocument.addEventListener('click',event=>{const part=event.target.closest('[data-space-part]');if(part){chosen.value=part.dataset.spacePart;topic='relationships';sync();}});sync();});
    const appearanceObserver=new MutationObserver(()=>DSStudio.learningPreviews.guideColours(frame.contentDocument));appearanceObserver.observe(document.documentElement,{attributes:true,attributeFilter:['data-theme']});
    DSStudio.learningPreviews.bindTheme(theme);
    width.addEventListener('change',()=>{signature='';sync();});chosen.addEventListener('change',()=>{topic='relationships';sync();});overlay.addEventListener('change',sync);
    controls.addEventListener('focusin',event=>{const key=event.target.closest('[id^="spacing-group-"]')?.id.slice('spacing-group-'.length);if(key){topic=key;sync();}});
    DSStudio.on('project:install',()=>{if(frame.contentDocument)DSStudio.fonts.clearLearning(frame.contentDocument);});get('fontRetry').addEventListener('click',()=>{if(frame.contentDocument)DSStudio.fonts.clearLearning(frame.contentDocument);sync();});
    const beforeReveal=window.dssRevealSection;window.dssRevealSection=function(id,scroll=true){revealControl(get(id));return beforeReveal(id,scroll);};
    DSStudio.on('properties:refreshed',sync);DSStudio.views.subscribe({id:'spacing-learning-preview',phase:'lesson',events:['foundation:updated','output:updated','project:sync','stage:change'],run:sync});
    section.addEventListener('toggle',()=>{if(section.open)sync();});window.addEventListener('resize',sync);
    DSStudio.spacingWorkspace={sync,revealControl};sync();DSStudio.emit('lesson:content');
  }
});
