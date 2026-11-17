"use strict";
/* A detached, normalized background draft paints a small page; the website and
   exports continue using the saved project until the shared Save action. */
DSStudio.register({
  id:'background-workspace',title:'Semantic colour learning workspace',
  init(){
    const get=id=>document.getElementById(id),regions=['body','header','main','footer'];
    const stage=get('palette-stage-backgrounds'),columns=stage.querySelector('.palette-editor-columns'),controls=get('palette-browse-backgrounds'),preview=get('palette-properties-backgrounds'),lesson=get('webpage-background-lesson'),selector=get('palette-region-selection');
    const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el;};
    const title=region=>region[0].toUpperCase()+region.slice(1),keyFor=region=>region==='body'?'background':region+'-background';
    const editor=stage.querySelector('.page-background-editor');
    columns.classList.add('background-learning-layout');controls.classList.add('background-learning-controls');preview.classList.add('background-learning-preview');
    controls.querySelector('h4').textContent='Background controls';
    controls.querySelector('p').textContent='Choose a region and edit its paint. The small page shows proposed changes; Save applies them to the website. Colour and opacity belong to this theme; padding is shared.';
    const selectedHeading=node('h5',null);selectedHeading.id='background-controls-title';controls.append(selectedHeading,editor,get('palette-background-clear'));
    // The selector belongs above the selected editor, retaining its native label.
    const selectorField=selector.closest('.field');controls.insertBefore(selectorField,selectedHeading);
    const actionArea=node('div','background-learning-actions');actionArea.id='background-shared-actions';
    actionArea.append(preview.querySelector('[data-property-actions="palette-backgrounds"]'),get('property-status-palette-backgrounds'));columns.after(actionArea);
    const intro=editor.querySelector(':scope > p.help');if(intro)intro.hidden=true;
    lesson.querySelector('h4').hidden=true;
    lesson.querySelector(':scope > p').textContent='Body is the outer canvas. Header, Main and Footer sit inside it; cards keep their own Surface colour. Select a labelled region to edit it.';
    const diagnostics=node('details','background-saved-details'),diagnosticTitle=node('summary',null,'Saved project: CSS, contrast and padding');diagnostics.id='background-saved-details';diagnostics.append(diagnosticTitle);
    const oldModel=lesson.querySelector('.background-page-model');oldModel.setAttribute('aria-label','Saved background tokens and contrast values');diagnostics.append(oldModel);
    for(const paragraph of [...lesson.querySelectorAll(':scope > p')].slice(2))diagnostics.append(paragraph);
    diagnostics.insertBefore(get('background-lesson-theme'),oldModel);diagnostics.insertBefore(get('background-opacity-help'),oldModel);
    const editorTitle=editor.querySelector('h4');if(editorTitle)editorTitle.hidden=true;
    const status=node('p','help');status.id='background-preview-status';status.setAttribute('role','status');
    const canvas=node('div','background-learning-canvas');canvas.id='background-learning-canvas';canvas.setAttribute('role','group');canvas.setAttribute('aria-label','Page regions: select a label to edit its background');
    const paper=node('body','background-learning-paper');paper.dataset.backgroundRegion='body';canvas.append(paper);
    const parts=new Map(),picks=new Map();
    function regionPart(region,parent){
      const part=region==='body'?paper:node(region,'background-learning-region');if(region!=='body'){part.dataset.backgroundRegion=region;parent.append(part);}
      const pick=node('button','background-region-pick',title(region)+(region==='body'?' canvas':''));pick.type='button';pick.dataset.backgroundPick=region;pick.setAttribute('aria-label','Edit '+title(region)+' background');
      const field=get(region==='body'?'body-background-controls':region+'-background-hex').closest('fieldset');field.id ||= region+'-background-controls';if(region==='body')pick.setAttribute('aria-controls',field.id);else{part.id='learning-region-'+region;pick.setAttribute('aria-controls',part.id);}pick.setAttribute('aria-description','Select this page region and its properties in the Studio editor.');
      pick.addEventListener('click',()=>{selector.value=region;selector.dispatchEvent(new Event('change',{bubbles:true}));});if(region==='body')canvas.insertBefore(pick,paper);else part.append(pick);parts.set(region,part);picks.set(region,pick);return part;
    }
    regionPart('body',paper);
    const header=regionPart('header',paper),brand=node('strong','background-example-brand');brand.id='background-example-brand';header.append(brand,node('span','background-example-link','Home  |  About'));
    const main=regionPart('main',paper);main.append(node('strong','background-example-heading','A clear page heading'),node('p',null,'Useful content gives your visitor a next step.'),node('span','background-example-link','Explore the page'));
    header.classList.add('site-header','sample-header');
    const card=node('div','background-example-card card');card.append(node('strong',null,'Content card / Surface'));main.append(card);
    const footer=regionPart('footer',paper);footer.classList.add('website-footer');footer.append(node('span',null,'Contact information and useful links'));
    const caption=node('p','help');caption.id='background-preview-caption';canvas.setAttribute('aria-describedby',caption.id);
    const checks=node('p','help');checks.id='background-preview-contrast';
    const cssDetails=node('details','background-proposed-css'),cssTitle=node('summary',null,'Selected region CSS'),pre=node('pre'),code=node('code');code.id='background-preview-css';pre.append(code);const paintMath=node('p','help');cssDetails.append(cssTitle,pre,paintMath);
    lesson.append(status,canvas,caption,checks,cssDetails,diagnostics);
    const learning=DSStudio.learningPreviews.mount({id:'semantic-learning-frame',title:'Semantic colour learning preview',element:paper,parent:canvas,ready:render,layout:`
.background-learning-region { min-height: 3rem; }
.background-region-pick { display: block; font: 600 12px/1.4 system-ui,sans-serif; padding: 6px; min-height: 44px; border: 1px dashed var(--learning-ui-control-border); border-radius: 0; letter-spacing: normal; color: var(--learning-ui-text); background: var(--learning-ui-surface); }
.background-region-pick[aria-pressed="true"]::after { content: " ?"; }
.background-region-pick:focus-visible { outline: 2px solid var(--learning-ui-focus); outline-offset: 3px; }
.is-selected { outline: 2px solid var(--learning-ui-focus); outline-offset: -2px; }
.background-example-brand, .background-example-heading { display: block; }
.background-example-link { color: var(--primary); }
.semantic-page-specimens { display: grid; gap: var(--space-3); }
.semantic-page-specimens > p { background: var(--surface-muted); color: var(--text-muted); }
.semantic-field-sample { padding: var(--space-2); background: var(--surface); color: var(--text); border: var(--border-width) solid var(--control-border); outline: 2px solid var(--focus); }
.semantic-action-samples, .semantic-feedback-samples { display: flex; flex-wrap: wrap; gap: var(--space-2); }
.semantic-action-samples > span { padding: var(--space-2); }
[data-role=primary] { background: var(--primary); color: var(--on-primary); } [data-role=primary-hover] { background: var(--primary-hover); color: var(--on-primary); } [data-role=secondary] { background: var(--secondary); color: var(--on-secondary); } [data-role=accent] { background: var(--accent); color: var(--on-accent); }
[data-role=success] { color: var(--success); border: 1px solid var(--success); } [data-role=warning] { color: var(--warning); border: 1px solid var(--warning); } [data-role=danger] { color: var(--danger); border: 1px solid var(--danger); }
`});
    const descriptions={body:'Body padding creates a frame around Header, Main and Footer. Opaque regions can cover the Body colour when padding is zero. Main follows Body until given a separate colour.',header:'Header sits above the content. Its default background follows Surface.',main:'Main holds the page content and follows Body by default. A card uses its own Surface background.',footer:'Footer sits below the content. Its default background follows Surface.'};
    let signature='';
    function render(){
      if(get('semantic-website-theme'))get('semantic-website-theme').value=state.theme;
      if(!(DSStudio.semanticWorkspace?get('palette-stage-semantics').open:stage.open) || !get('brandPalette').open)return;
      const snapshot=DSStudio.propertyEditors.draftSnapshot('palette-backgrounds'),base=snapshot.state,foundation=DSStudio.paletteBrowser.proposedState(base),region=selector.value,{roles}=palette(foundation.theme,foundation),layers=backgroundLayers(foundation.theme,foundation,roles),dirty=DSStudio.propertyEditors.hasDrafts('palette-backgrounds');
      // Saved-control synchronizers can run for unrelated project edits too.
      // Keep these visible control readouts aligned with this scope's draft.
      for(const name of regions){
        const key=keyFor(name),prefix=name==='body'?'page-background':name+'-background',alpha=backgroundOpacity(name,foundation.theme,foundation),source=semanticSource(key,foundation.theme,foundation);
        const paint=colourIsTransparent(key,foundation.theme,foundation)?'None (transparent)':(source?source.token+' / ':'')+roles[key];
        const current=get(name==='body'?'page-background-theme':prefix+'-current'),message=(dirty?'Proposed ':'Saved ')+(foundation.theme==='dark'?'Dark':'Light')+' theme \u00b7 '+paint;
        if(current.textContent!==message)current.textContent=message;
        get(prefix+'-opacity').value=String(Math.round(alpha*100));get(prefix+'-opacity-value').textContent=Math.round(alpha*100)+'%';get(prefix+'-opacity').setAttribute('aria-valuetext',Math.round(alpha*100)+'% opaque');
        const insets=PADDING_SIDES.map(side=>regionPadding(name,side,foundation));
        get(name+'-padding-summary').textContent=title(name)+' padding \u00b7 '+insets.join(' / ')+' px';
        get(name+'-padding-reset').disabled=insets.every(value=>value===0);
        get(prefix+'-reset').disabled=get(prefix+'-hex').validity.valid && !foundation.semanticOverrides?.[foundation.theme]?.[key] && !foundation.colourTransparency?.[foundation.theme+':'+key] && alpha===1;
      }
      get('palette-background-clear').disabled=get((region==='body'?'page':region)+'-background-reset').disabled;
      learning.render({...snapshot,state:foundation});
      const next=JSON.stringify([foundation,get('jSemanticRole').value,get('palette-semantic-proposal-status').textContent,foundation.theme,foundation.project,roles,foundation.semanticSources,foundation.colourTransparency,foundation.backgroundOpacity,foundation.regionPadding,region,dirty]);if(next===signature)return;signature=next;
      selectedHeading.textContent=title(region)+' properties';
      status.textContent=(dirty?'Proposed':'Saved')+' '+(foundation.theme==='dark'?'Dark':'Light')+' backgrounds. '+(dirty?'Save updates the website; Discard restores saved values.':'The small page matches the saved project.');
      canvas.style.backgroundColor=rgbHex(layers.canvas);
      brand.textContent='Learning Studio';
      for(const name of regions){
        const part=parts.get(name),key=keyFor(name),alpha=backgroundOpacity(name,foundation.theme,foundation);
        part.classList.toggle('is-selected',name===region);picks.get(name).setAttribute('aria-pressed',String(name===region));
      }
      const visible=rgbHex(layers[region]),text=colourIsTransparent('text',foundation.theme,foundation)?1:contrast(roles.text,visible),link=colourIsTransparent('primary',foundation.theme,foundation)?1:contrast(roles.primary,visible),key=keyFor(region),alpha=backgroundOpacity(region,foundation.theme,foundation),source=semanticSource(key,foundation.theme,foundation);
      const paint=colourIsTransparent(key,foundation.theme,foundation)?'transparent':source?'var('+source.token+')':roles[key];
      caption.textContent=descriptions[region]+' Opacity changes only background paint. '+(region==='body'?'Header, Main and Footer padding changes inner spacing. Padding is shared across themes.':'Padding adds space inside this region and is shared across themes.');
      checks.textContent=title(region)+' text '+text.toFixed(2)+':1; links '+link.toFixed(2)+':1. '+(text>=4.5 && link>=4.5?'Both meet 4.5:1.':'Review contrast before saving.')+' Check cards and interactive states separately.';
      DSStudio.semanticWorkspace?.paint(foundation,roles);
      paintMath.textContent='Paint opacity: '+Math.round(alpha*100)+' / 100 = '+alpha+'. Padding values are shared between themes; colour and paint opacity belong to this theme.';
      code.textContent=`/* ${dirty?'Proposed':'Saved'} ${title(region)} */
--${key}: ${paint};
--${region}-background-opacity: ${alpha};`+'\n'+PADDING_SIDES.map(side=>`--${region}-padding-${side}: ${regionPadding(region,side,foundation)}px;`).join('\n');
    }
    stage.addEventListener('toggle',()=>{if(stage.open)render();});get('brandPalette').addEventListener('toggle',()=>{if(get('brandPalette').open)render();});
    selector.addEventListener('change',render);DSStudio.on('properties:refreshed',render);
    DSStudio.views.subscribe({id:'background-learning-preview',phase:'lesson',events:['output:updated','project:sync','stage:change'],run:render});
    const semanticStage=get('palette-stage-semantics'),semanticControls=get('palette-browse-semantics'),semanticPreview=get('palette-properties-semantics');
    const semanticColumns=semanticStage.querySelector('.palette-editor-columns');semanticColumns.classList.add('semantic-learning-layout');
    semanticControls.querySelector('h4').textContent='Semantic colour controls';
    const propertyTitle=get('palette-properties-title-semantics');propertyTitle.textContent='Semantic colour learning preview';
    // Keep the original editors and their contrast-review/save boundaries.
    const semanticSection=get('jSemanticTitle').closest('section');semanticControls.append(semanticSection);
    const semanticActions=semanticPreview.querySelector('[data-property-actions="palette-semantics"]');semanticControls.append(semanticActions);
    const semanticStatus=get('property-status-palette-semantics');if(semanticStatus)semanticControls.append(semanticStatus);
    const layoutDetails=node('details','semantic-region-settings'),layoutSummary=node('summary',null,'Page regions: colours, opacity and padding');layoutDetails.id='semantic-region-settings';
    layoutDetails.append(layoutSummary,controls,actionArea);semanticControls.append(layoutDetails);
    controls.querySelector('h4').hidden=true;
    controls.querySelector('p').textContent='These region controls keep their own proposals. Save here applies region colour, opacity and padding; the semantic colour Save above reviews the selected role. Padding is shared across website themes.';
    propertyTitle.after(lesson);semanticPreview.classList.add('background-learning-preview');
    // A hidden compatibility destination keeps existing token routes intact.
    stage.hidden=true;stage.open=false;
    lesson.querySelector(':scope > p').textContent='Select a role on the left, or a labelled page region. The sample previews the selected colour proposal with any region drafts. The website and exports use saved values. Role tiles below cover every semantic token.';
    const roleGrid=node('div','semantic-role-samples');roleGrid.id='semantic-role-samples';roleGrid.setAttribute('role','group');roleGrid.setAttribute('aria-label','All semantic colour roles');
    const roleSamples=new Map();
    for(const option of get('jSemanticRole').options){
      const pick=node('button','semantic-role-sample'),chip=node('span','semantic-sample-chip'),label=node('span',null,option.textContent.split(' (')[0]),token=node('code',null,'--'+option.value);pick.type='button';pick.dataset.semanticPick=option.value;chip.setAttribute('aria-hidden','true');pick.append(chip,label,token);roleGrid.append(pick);roleSamples.set(option.value,{pick,chip,token});
      pick.addEventListener('click',()=>{get('jSemanticRole').value=option.value;get('jSemanticRole').dispatchEvent(new Event('change',{bubbles:true}));});
    }
    const specimens=node('div','semantic-page-specimens');card.append(specimens);
    const muted=node('p',null,'Supporting text on a muted surface.'),inputSample=node('div','semantic-field-sample','Example input / focus'),actions=node('div','semantic-action-samples'),feedback=node('div','semantic-feedback-samples');specimens.append(muted,inputSample,actions,feedback);
    const actionSamples=['primary','primary-hover','secondary','accent'].map(key=>{const sample=node('span',null,key==='primary-hover'?'Primary hover':title(key));sample.dataset.role=key;actions.append(sample);return {key,sample};});
    const feedbackSamples=['success','warning','danger'].map(key=>{const sample=node('span',null,title(key)+' message');sample.dataset.role=key;feedback.append(sample);return {key,sample};});
    const selectedCss=node('details','background-proposed-css'),selectedSummary=node('summary',null,'Generated CSS and the calculation'),selectedPre=node('pre'),selectedCode=node('code');selectedCode.id='semantic-preview-css';selectedPre.append(selectedCode);selectedCss.append(selectedSummary,selectedPre);
    selectedCss.id='semantic-learning-css';selectedCss.classList.add('learning-css-quick');selectedCss.append(cssDetails);lesson.prepend(selectedCss);const themeField=node('div'),websiteTheme=DSStudio.learningPreviews.theme('semantic-website-theme',themeField);selectedCss.after(themeField);canvas.after(roleGrid);
    function selectRegionRole(){const key=keyFor(selector.value);get('jSemanticRole').value=key;get('jSemanticRole').dispatchEvent(new Event('change',{bubbles:true}));layoutDetails.open=true;}
    selector.addEventListener('change',selectRegionRole);
    get('jSemanticRole').addEventListener('change',()=>{const region=regions.find(name=>keyFor(name)===get('jSemanticRole').value);if(region){selector.value=region;DSStudio.paletteWorkspace.selectRegion();}render();});
    semanticStage.addEventListener('toggle',render);
    DSStudio.on('palette:proposal',render);
    DSStudio.semanticWorkspace={revealRegions(){layoutDetails.open=true;selectRegionRole();},paint(foundation,roles){
      const key=get('jSemanticRole').value,theme=foundation.theme,paint=role=>semanticPaint(role,theme,foundation,roles[role]);
      for(const selected of paper.querySelectorAll('[data-learning-selected]'))selected.removeAttribute('data-learning-selected');
      const region=regions.find(name=>keyFor(name)===key),action=actionSamples.find(item=>item.key===key || key==='on-'+item.key),message=feedbackSamples.find(item=>item.key===key);
      const selected=region?parts.get(region):action?.sample||message?.sample||(['control-border','focus'].includes(key)?inputSample:['text-muted','surface-muted'].includes(key)?muted:key==='button-focus'?actions:['surface','border'].includes(key)?card:main);
      selected.setAttribute('data-learning-selected','');
      for(const [role,{pick,chip,token}]of roleSamples){chip.style.backgroundColor=paint(role);pick.setAttribute('aria-pressed',String(role===key));token.textContent='--'+role+' / '+(colourIsTransparent(role,theme,foundation)?'transparent':semanticSource(role,theme,foundation)?.token||roles[role]);}
      const source=semanticSource(key,theme,foundation),value=colourIsTransparent(key,theme,foundation)?'transparent':source?'var('+source.token+')':roles[key];
      const property=key==='focus'?'outline-color':key.includes('border')?'border-color':key.startsWith('on-') || ['text','text-muted','success','warning','danger'].includes(key)?'color':'background-color';
      selectedCode.textContent='/* '+(theme==='dark'?'Dark':'Light')+' website theme; selected proposal */\n--'+key+': '+value+';\n\n.sample { '+property+': var(--'+key+'); }\n/* Save applies this role to the website and exports. */';
      status.textContent=(dirtyRegion()?'Proposed ':'Saved ')+(theme==='dark'?'Dark':'Light')+' regions. '+'Learning preview: '+(theme==='dark'?'Dark':'Light')+' website theme. '+get('palette-semantic-proposal-status').textContent+(dirtyRegion()?' Region proposals are also shown; use the region Save to apply them.':'');
    }};
    function dirtyRegion(){return DSStudio.propertyEditors.hasDrafts('palette-backgrounds');}
    DSStudio.backgroundWorkspace=Object.freeze({render});render();
  }
});
