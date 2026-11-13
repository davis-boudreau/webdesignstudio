'use strict';
/* One typography model, original controls, and safe specimens from website content. */
DSStudio.register({
  id:'typography-workspace',title:'Guided typography workspace',
  init(){
    const get=id=>document.getElementById(id),section=get('studio-section-2'),panel=section.querySelector(':scope > .panel'),pane=document.querySelector('[data-journey-pane="5"]');
    const lesson=panel.querySelector('.studio-lesson'),oldMore=panel.querySelector(':scope > .step-more');
    const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el;};
    const button=(text,action)=>{const el=node('button','ghost',text);el.type='button';el.addEventListener('click',action);return el;};
    const reference=(title,...children)=>{const el=node('details','type-reference'),summary=node('summary',null,title);el.append(summary,...children.filter(Boolean));return el;};
    const workspace=node('section','typography-workspace');workspace.id='typography-workspace';workspace.setAttribute('aria-labelledby','typography-workspace-title');
    const header=node('header');header.setAttribute('data-stage-controls','');lesson.querySelector('h3').textContent='Typography workspace';lesson.querySelector('h3').id='typography-workspace-title';lesson.querySelector('h3').tabIndex=-1;
    lesson.querySelector('p').textContent='Use the content from Architecture to choose type, observe its effect and refine your decisions. Select a learning stage, browse an item on the left and edit its properties on the right. Website settings update immediately; specimen-only comparisons are labelled.';
    lesson.querySelector('.step-task')?.remove();const inspectActions=lesson.querySelector('.step-output');if(inspectActions)inspectActions.remove();header.append(lesson);workspace.append(header);panel.prepend(workspace);
    const definitions=[
      ['content','Start with content','Choose an actual website heading, paragraph or label. Identify its purpose and audience before choosing its appearance. Wording is edited in Architecture.','Explain which text should be noticed first and which should support it.'],
      ['fonts','Choose font families','Choose body and heading families. Compare character shapes, tone, long words and fallback behavior. System fonts work offline; Google Fonts is an optional online source.','Compare the same words in two families and describe the changes in width and character shapes.'],
      ['body','Establish readable body text','Set body size, line height and reading measure using a real paragraph. Reading measure limits the line length in font-dependent ch units.','Change one value and explain how wrapping and paragraph height respond.'],
      ['hierarchy','Build visual hierarchy','Choose a named scale or a custom ratio. Generated visual roles share the body-size baseline; their sizes are calculated, not independently saved overrides. A visual role does not change the HTML heading level.','Compare two roles and explain their emphasis using size and context.'],
      ['rhythm','Refine emphasis and rhythm','Choose body or headings, then refine the settings owned by that family. Tracking uses em. Small changes can affect wrapping, especially in connected scripts.','Compare spacing near zero with your proposed value using actual words.'],
      ['responsive','Make typography responsive','Explore a visual role across viewport widths. Display, H1 and H2 use fluid limits; body and small text retain their base sizes in this system. The mobile percentage is separate from the scale ratio.','Move the specimen viewport and explain where the selected size stops growing.'],
      ['context','Test type in components','Inspect actual website text in cards, navigation, buttons, forms and tables. These examples use the current live website styles; component-owned overrides are inspected here and edited in their owning workspace.','Compare a long label with paragraph text and explain the different constraints.'],
      ['review','Review and continue','Compare the specimen at narrow and wide widths, with fallback fonts, enlargement and user-spacing overrides. These comparisons do not certify accessibility. Use the full website for browser zoom, reflow and keyboard review.','Explain your body, heading and responsive choices, then inspect their effect in Wireframe.']
    ],stages=new Map();let active='content',family='body',rhythm='heading',identity,syncing=false,sourceHtml='',sourceDoc;
    for(const [index,[key,title,help,prompt]]of definitions.entries()){
      const details=node('details','type-stage'),summary=node('summary',null,(index+1)+'. '+title),grid=node('div','type-editor-columns'),browse=node('section','type-browser'),props=node('section','type-properties');
      details.id='type-stage-'+key;details.dataset.typeStage=key;browse.id='type-browse-'+key;props.id='type-properties-'+key;
      const bt=node('h4',null,'Browse and explore'),pt=node('h4',null,'Selected properties');bt.id='type-browse-title-'+key;pt.id='type-properties-title-'+key;browse.setAttribute('aria-labelledby',bt.id);props.setAttribute('aria-labelledby',pt.id);
      browse.append(bt,node('p',null,help),node('p','type-observe',prompt));props.append(pt);grid.append(browse,props);details.append(summary,grid);
      const actions=node('div','type-stage-actions');if(index)actions.append(button('Previous: '+definitions[index-1][1],()=>show(definitions[index-1][0])));if(index<definitions.length-1)actions.append(button('Next: '+definitions[index+1][1],()=>show(definitions[index+1][0])));details.append(actions);workspace.append(details);
      stages.set(key,{details,summary,browse,props,title:pt});details.addEventListener('toggle',()=>{if(details.open && active!==key)show(key,false);});
      summary.addEventListener('click',event=>{event.preventDefault();if(details.open)details.open=false;else show(key);});
    }
    const append=(key,...children)=>stages.get(key).props.append(...children.filter(Boolean));
    function field(id,label,input){const wrap=node('div','field'),caption=node('label',null,label);input.id=id;caption.htmlFor=id;wrap.append(caption,input);return wrap;}
    function select(id,label,options,parent){const el=node('select');for(const [value,text]of options)el.add(new Option(text,value));parent.append(field(id,label,el));return el;}
    function value(id,label,parent){const input=node('input');input.type='text';input.readOnly=true;parent.append(field(id,label,input));return input;}
    const controlStages=new Map();
    function moveField(id,key){const el=get(id);append(key,el.closest('.field'));controlStages.set(id,key);return el;}
    function moveLine(id,key,parent=stages.get(key).props){const el=get(id),label=document.querySelector('label[for="'+id+'"]'),wrap=node('div','field');wrap.append(label,el);parent.append(wrap);controlStages.set(id,key);return el;}
    function dispatch(id,next,event='input'){const el=get(id);el.value=next;el.dispatchEvent(new Event(event,{bubbles:true}));}
    function go(id){window.dssRevealSection(id,false);const el=get(id);el.focus();el.scrollIntoView({block:'center',behavior:'instant'});}
    const choices=[['headline','Hero heading','#hero-title'],['heading','Section heading','main h2'],['paragraph','Body paragraph','.sample-lead,.hero-lead,main p'],['card','Card paragraph','.card p,.sample-card p,main article p'],['navigation','Navigation label','body > header nav a'],['button','Action label','.ds-button'],['form','Form label','form label'],['table','Table cell','td'],['caption','Image caption','figcaption'],['emphasis','Emphasis or citation','cite,em'],['list','List item','main li']];
    const contentSelect=select('type-content-choice','Website text to explore',choices.map(([key,label])=>[key,label]),stages.get('content').browse);contentSelect.value='paragraph';
    const contentTag=value('type-content-tag','Source HTML element',stages.get('content').props),contentText=node('textarea');contentText.readOnly=true;contentText.rows=4;stages.get('content').props.append(field('type-content-text','Current website wording',contentText));
    stages.get('content').browse.append(button('Edit wording in Architecture',()=>go('process-ia')));
    const fontRole=select('type-font-role','Font family to edit',[['body','Body'],['heading','Headings']],stages.get('fonts').browse);fontRole.size=2;
    stages.get('fonts').browse.append(get('fontSource').closest('.field'));controlStages.set('fontSource','fonts');
    moveField('jFont','fonts');append('fonts',get('fontSystemOptions'),get('fontGoogleOptions'));
    for(const id of ['fontSystemHeading','fontGoogleBody','fontGoogleHeading'])controlStages.set(id,'fonts');
    const fontWeights=reference('Font files and requested weights',document.querySelector('.font-weights'),get('fontWeightsHelp'));append('fonts',fontWeights);
    const fallback=get('fontFallback').closest('label'),fallbackHelp=fallback.nextElementSibling;append('fonts',fallback,fallbackHelp,get('fontLoadStatus'),get('fontRetry'));controlStages.set('fontFallback','fonts');controlStages.set('fontRetry','fonts');
    const fontReference=get('fontHtmlCode').closest('details');if(fontReference)append('fonts',fontReference);
    stages.get('fonts').browse.append(button('Reset selected family',()=>{const defaults=DSStudio.fonts.defaults();if(state.fontSettings?.source==='google')dispatch(family==='body'?'fontGoogleBody':'fontGoogleHeading',family==='body'?defaults.body:defaults.heading,'change');else dispatch(family==='body'?'jFont':'fontSystemHeading',family==='body'?DEFAULT.font:defaults.systemHeading,family==='body'?'input':'change');}));
    append('fonts',reference('Font anatomy, pairing and coverage',node('p',null,'Compare x-height, character width, serifs and stroke contrast using the same words. Check punctuation, numbers and the scripts your audience uses. A fallback may change line breaks. Requested font files and the weight actually used by a role are separate choices.')));
    for(const id of ['jBase','jLeading','advMeasure'])moveField(id,'body');
    stages.get('body').browse.append(button('Reset body readability',()=>{dispatch('jBase',DEFAULT.base);dispatch('jLeading',DEFAULT.leading);dispatch('advMeasure',ADV_DEFAULT.measure);}));
    for(const id of ['jScalePreset','jRatio'])moveField(id,'hierarchy');
    const roleField=node('div','field');roleField.append(document.querySelector('label[for="clampRole"]'),get('clampRole'));stages.get('hierarchy').browse.append(roleField);controlStages.set('clampRole','hierarchy');
    const roleSize=value('type-role-size','Generated size at the specimen viewport',stages.get('hierarchy').props),roleRem=value('type-role-rem','REM at a nominal 16px root',stages.get('hierarchy').props);
    stages.get('hierarchy').browse.append(button('Edit body-size baseline',()=>{show('body');get('jBase').focus();}),button('Reset scale ratio',()=>dispatch('jRatio',DEFAULT.ratio)));
    const ladder=reference('Complete generated size ladder',get('typeLadder'));append('hierarchy',ladder,reference('Visual roles and HTML headings',node('p',null,'Display and heading sizes are visual roles. Choose semantic heading levels from the content structure in Architecture. Generated sizes follow the base and ratio; changing the ratio affects several roles together. PX describes CSS pixels, REM follows root font size, and em spacing follows the element font size.')));
    const rhythmRole=select('type-rhythm-role','Text family to refine',[['heading','Headings'],['body','Body']],stages.get('rhythm').browse);rhythmRole.size=2;
    for(const id of ['jHeadingLeading','advWeight','jHeadingTracking','jBodyTracking'])moveField(id,'rhythm');
    stages.get('rhythm').browse.append(button('Reset selected rhythm settings',()=>{if(rhythm==='body')dispatch('jBodyTracking',DEFAULT.bodyTracking);else{dispatch('jHeadingLeading',DEFAULT.headingLeading);dispatch('jHeadingTracking',DEFAULT.headingTracking);dispatch('advWeight',ADV_DEFAULT.weight,'change');}}));
    append('rhythm',reference('Emphasis, language and spacing',node('p',null,'Use weight and italic emphasis with meaning; the component-context browser includes existing citations and emphasis. Body leading belongs to Body readability. Paragraph and word spacing can be explored with the specimen-only override in Review. Connected scripts may need different spacing behavior; inspect actual audience content.')));
    for(const id of ['clampMinWidth','clampMaxWidth','clampFactor'])moveLine(id,'responsive');append('responsive',get('clampReset'));controlStages.set('clampReset','responsive');
    const graph=get('clampGraph').closest('.clamp-result');
    // The legacy lesson prepended a missing field, leaving a literal null text node.
    for(const child of [...graph.childNodes])if(child.nodeType===Node.TEXT_NODE && child.textContent.trim()==='null')child.remove();
    graph.querySelector('h4').textContent='Observe fluid size';append('responsive',graph);
    const calculation=get('clampCss').closest('.component');calculation.querySelector('h4').textContent='Generated CSS and calculation';append('responsive',reference('Inspect the generated rule',calculation));controlStages.set('clampCopy','responsive');
    const contextSelect=select('type-context-choice','Component text to inspect',choices.map(([key,label])=>[key,label]),stages.get('context').browse);contextSelect.value='button';
    const contextFamily=value('type-context-family','Resolved font family',stages.get('context').props),contextSize=value('type-context-size','Resolved font size / line height / weight',stages.get('context').props);
    stages.get('context').browse.append(button('Edit button typography in Buttons',()=>go('bdWeight')),button('Edit component spacing',()=>go('jSpacing')),button('Edit website wording',()=>go('process-ia')));
    append('context',node('p','help','Component samples use resolved styles from the current live preview. The specimen width controls wrapping here; use Wireframe to inspect the full responsive composition.'));
    const review=stages.get('review');const checklist=node('ul');for(const text of ['Read the actual content at narrow and wide widths.','Check fallback fonts, long labels, punctuation and emphasis.','Use browser zoom and user text settings on the full website.','Look for clipping, overlap and lost controls; explain your chosen hierarchy.'])checklist.append(node('li',null,text));review.browse.append(checklist);
    review.browse.append(button('Continue to Wireframe',()=>go('process-wireframe')),button('Review the live website',()=>go('previewShell')),button('Open Accessibility review',()=>go('studio-section-5')));
    if(inspectActions)append('review',inspectActions);
    const oldSpecimens=get('mobileType').closest('.grid2');append('review',reference('Compare mobile and desktop specimens',oldSpecimens));
    // A single specimen follows the active stage. No imported text is inserted as HTML.
    const preview=node('section','type-specimen');preview.setAttribute('aria-labelledby','type-specimen-title');const previewTitle=node('h4',null,'Observe the website text');previewTitle.id='type-specimen-title';
    const previewTools=node('div','type-preview-tools');preview.append(previewTitle,previewTools);moveLine('clampViewport','responsive',previewTools);
    const enlargement=select('type-preview-enlarge','Specimen text enlargement',[['1','100%'],['2','200%']],previewTools);
    const spacing=node('input');spacing.type='checkbox';const spacingLabel=node('label','type-spacing-label','Preview user-spacing overrides ');spacing.id='type-preview-spacing';spacingLabel.prepend(spacing);previewTools.append(spacingLabel);
    const comparisonNote=node('p','help','Viewport, enlargement and spacing overrides affect this specimen only. They are not saved website settings or a full-page accessibility test.');preview.append(comparisonNote);
    const previewMeta=node('p','help');previewMeta.id='type-specimen-meta';const scroller=node('div','type-specimen-scroll'),paper=node('div','type-specimen-paper'),sample=node('div','type-specimen-text');scroller.tabIndex=0;scroller.setAttribute('role','region');scroller.setAttribute('aria-label','Scrollable website text specimen');scroller.setAttribute('aria-describedby',previewMeta.id);sample.id='type-specimen-text';paper.append(sample);scroller.append(paper);preview.append(previewMeta,scroller);
    // Original aliases remain bound for old projects/tests, but are not duplicate editors.
    const legacy=node('div');legacy.id='type-legacy-controls';legacy.hidden=true;workspace.append(legacy);
    if(oldMore){legacy.append(oldMore);oldMore.hidden=true;}
    for(const child of [...pane.children])if(child.tagName!=='H3')legacy.append(child);
    const nav=node('ol','type-stage-nav');nav.setAttribute('aria-label','Typography learning stages');const progress=node('p','help');progress.id='type-stage-progress';
    pane.querySelector('h3').textContent='Develop your typography';pane.append(node('p','help','Choose a learning stage. Browse and edit in the centre workspace; observe the effect with real website wording.'),button('Open Typography workspace',()=>go('typography-workspace-title')),progress);
    const picker=reference('Typography stages',nav);pane.append(picker);
    for(const [key,title]of definitions){const li=node('li'),action=button(title,()=>{window.dssRevealSection('studio-section-2',false);show(key);});action.dataset.typeGo=key;li.append(action);nav.append(li);}
    for(const key of ['fonts','body','hierarchy','rhythm']){const reset=[...stages.get(key).browse.querySelectorAll('button')].find(el=>el.textContent.startsWith('Reset'));if(reset)reset.id='type-reset-'+key;}
    const aliases=new Map([['clampBase','jBase'],['clampRatio','jRatio'],['clampScalePreset','jScalePreset'],['typoHeadingTracking','jHeadingTracking'],['typoBodyTracking','jBodyTracking'],['advTracking','jHeadingTracking'],['fontControls','fontSource'],['clampLabTitle','clampMinWidth'],['clamp-lab','clampMinWidth']]);
    function canonical(control){return aliases.has(control?.id)?get(aliases.get(control.id)):control;}
    function show(key,focus=true){if(!stages.has(key))return;active=key;for(const [name,entry]of stages)entry.details.open=name===key;
      if(key==='hierarchy' || key==='responsive'){stages.get(key).browse.append(roleField);controlStages.set('clampRole',key);}
      stages.get(key).props.prepend(preview);for(const action of nav.querySelectorAll('button')){if(action.dataset.typeGo===key)action.setAttribute('aria-current','step');else action.removeAttribute('aria-current');}
      progress.textContent='Typography stage '+(definitions.findIndex(row=>row[0]===key)+1)+' of '+definitions.length+' - '+definitions.find(row=>row[0]===key)[1]+'. This marks your position, not completion.';
      sync();if(focus){stages.get(key).summary.focus({preventScroll:true});stages.get(key).summary.scrollIntoView({block:'start',behavior:'instant'});}
    }
    function readSite(){const html=htmlExport();if(html!==sourceHtml){sourceHtml=html;sourceDoc=new DOMParser().parseFromString(html,'text/html');}return sourceDoc;}
    function chosen(doc,key){const row=choices.find(row=>row[0]===key)||choices[2];return doc.querySelector(row[2]);}
    function sync(){
      if(syncing)return;syncing=true;try{
        if(identity!==state){identity=state;family='body';rhythm='heading';fontRole.value=family;rhythmRole.value=rhythm;contentSelect.value='paragraph';enlargement.value='1';spacing.checked=false;show('content',false);}
        const google=state.fontSettings?.source==='google';
        get('jFont').closest('.field').hidden=google || family!=='body';get('fontSystemOptions').hidden=google || family!=='heading';
        get('fontGoogleBody').closest('.field').hidden=family!=='body';get('fontGoogleHeading').closest('.field').hidden=family!=='heading';fontWeights.hidden=!google;fallback.hidden=!google;if(fallbackHelp)fallbackHelp.hidden=!google;
        stages.get('fonts').title.textContent=(family==='body'?'Body':'Heading')+' font properties';
        for(const id of ['jHeadingLeading','advWeight','jHeadingTracking'])get(id).closest('.field').hidden=rhythm!=='heading';get('jBodyTracking').closest('.field').hidden=rhythm!=='body';stages.get('rhythm').title.textContent=(rhythm==='body'?'Body':'Heading')+' rhythm properties';
        if(!section.open || !stages.get(active).details.open)return;
        const site=readSite();for(const select of [contentSelect,contextSelect]){for(const option of select.options)option.disabled=!chosen(site,option.value);if(select.selectedOptions[0]?.disabled)select.value=[...select.options].find(option=>!option.disabled)?.value||'paragraph';}
        const key=active==='context'?contextSelect.value:contentSelect.value,source=chosen(site,key),fallbackSource=chosen(site,'paragraph');
        const text=(source?.textContent||fallbackSource?.textContent||'').trim();contentText.value=(chosen(site,contentSelect.value)?.textContent||'').trim();contentTag.value=chosen(site,contentSelect.value)?.tagName.toLowerCase()||'No matching entry in this sample';
        let step=Number(get('clampRole').value),heading=step>0;
        if(active==='body'){step=0;heading=false;}if(active==='fonts' || active==='rhythm'){heading=(active==='fonts'?family:rhythm)==='heading';step=heading?4:0;}
        if(active==='content'){heading=!!source?.matches('h1,h2,h3,h4,h5,h6');step=source?.matches('h1')?4:heading?3:0;}
        const width=Number(get('clampViewport').value),fonts=DSStudio.fonts.resolve(DSStudio.fonts.showFallback),base=fluidTypePx(step,width),enlarged=Number(enlargement.value);
        sample.removeAttribute('style');sample.textContent=active==='body'?(fallbackSource?.textContent||text).trim():active==='fonts'||active==='rhythm'||active==='hierarchy'||active==='responsive'?(chosen(site,heading?'headline':'paragraph')?.textContent||text).trim():text;
        Object.assign(sample.style,{fontFamily:heading?fonts.heading:fonts.body,fontSize:base*enlarged+'px',fontWeight:heading?String(adv.weight):'400',lineHeight:String(heading?state.headingLeading:state.leading),letterSpacing:(heading?state.headingTracking:state.bodyTracking)+'em',maxWidth:heading?'none':adv.measure+'ch',overflowWrap:'anywhere'});
        let resolved;
        if(active==='context'){
          const live=get('previewPage').contentDocument,entry=choices.find(row=>row[0]===contextSelect.value),actual=live?.querySelector(entry[2]);
          if(actual){resolved=live.defaultView.getComputedStyle(actual);for(const property of ['fontFamily','fontSize','fontWeight','fontStyle','lineHeight','letterSpacing','textTransform','textDecoration','color','backgroundColor','border','borderRadius','padding'])sample.style[property]=resolved[property];sample.style.fontSize=parseFloat(resolved.fontSize)*enlarged+'px';}
        }
        if(spacing.checked){sample.style.lineHeight='1.5';sample.style.letterSpacing='.12em';sample.style.wordSpacing='.16em';sample.style.marginBottom='2em';}
        paper.style.width=width+'px';paper.style.backgroundColor=palette().roles.surface;paper.style.color=palette().roles.text;previewMeta.textContent=(state.sampleMode==='basic'?'Basic':'Advanced')+' website - '+(active==='context'?choices.find(row=>row[0]===contextSelect.value)[1]:heading?'Heading specimen':'Body specimen')+' - '+sample.style.fontSize+' at '+width+'px.';
        roleSize.value=fluidTypePx(Number(get('clampRole').value),width)+'px';roleRem.value=round(fluidTypePx(Number(get('clampRole').value),width)/16,4)+'rem';
        contextFamily.value=resolved?.fontFamily||fonts.body;contextSize.value=resolved?resolved.fontSize+' / '+resolved.lineHeight+' / '+resolved.fontWeight:'Choose a component in the context stage';
        for(const el of workspace.querySelectorAll('#mobileType .sample,#desktopType .sample,#typeLadder .sample'))el.textContent=(chosen(site,el.dataset.fontRole==='heading'?'headline':'paragraph')?.textContent||text).trim();
      }finally{syncing=false;}
    }
    function revealControl(control){control=canonical(control);if(!control)return;let key=controlStages.get(control.id)||control.closest('[data-type-stage]')?.dataset.typeStage;if(!key)return;
      if(['jFont','fontGoogleBody'].includes(control.id)){family='body';fontRole.value=family;}if(['fontSystemHeading','fontGoogleHeading'].includes(control.id)){family='heading';fontRole.value=family;}
      if(control.id==='jBodyTracking'){rhythm='body';rhythmRole.value=rhythm;}else if(['jHeadingLeading','advWeight','jHeadingTracking'].includes(control.id)){rhythm='heading';rhythmRole.value=rhythm;}
      show(key,false);for(let parent=control.parentElement;parent && parent!==workspace;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;
    }
    fontRole.addEventListener('change',()=>{family=fontRole.value;sync();});rhythmRole.addEventListener('change',()=>{rhythm=rhythmRole.value;sync();});
    workspace.addEventListener('input',sync);workspace.addEventListener('change',sync);
    const beforeReveal=window.dssRevealSection;window.dssRevealSection=function(id,scroll=true){const control=canonical(get(id));revealControl(control);return beforeReveal(control?.id||id,scroll);};
    function revealAlias(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{return;}if(aliases.has(id))go(aliases.get(id));}
    window.addEventListener('hashchange',revealAlias);DSStudio.on('ready',revealAlias);
    const beforeApply=apply;apply=function(){beforeApply();sync();};const beforeType=renderType;renderType=function(){beforeType();sync();};const beforeCode=renderCode;renderCode=function(){beforeCode();sync();};
    section.addEventListener('toggle',()=>{if(section.open)sync();});DSStudio.on('stage:change',({stage})=>{if(stage.index===5)sync();});
    DSStudio.typographyWorkspace={show,revealControl,sync};show('content',false);DSStudio.emit('lesson:content');
  }
});
