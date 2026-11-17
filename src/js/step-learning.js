'use strict';
/* Visual design steps use the website generator with their own normalized draft.
   Planning artifacts and delivery tools retain their existing purpose. */
DSStudio.register({
  id:'step-learning',title:'Consistent CSS lessons and selected component previews',
  init(){
    const get=id=>document.getElementById(id),api=DSStudio.learningPreviews,views=[];
    const node=(tag,text)=>{const el=document.createElement(tag);if(text)el.textContent=text;return el;};
    const definitions=[
      ['palette-brand',4,'palette-stage-brand','palette-brand'],
      ['palette-roles',4,'palette-stage-roles','palette-roles'],
      ['palette-shades',4,'palette-stage-shades','palette-shades'],
      ['palette-components',4,'palette-stage-components','palette-components'],
      ['palette-review',4,'palette-stage-review','palette-review'],
      ['colour',6,'studio-section-1',null],
      ['responsive',9,'responsiveDesign','responsive'],
      ['accessibility',10,'studio-section-5','accessibility']
    ];
    function create([id,stage,ownerId,scope]){
      const owner=get(ownerId),parent=owner.querySelector(':scope > .palette-stage-body, :scope > .panel');
      const host=node('section');host.id=id+'-learning';host.className='step-learning';host.setAttribute('aria-label',DSStudio.stages[stage].label+' learning workspace');
      const quick=node('details');quick.id=id+'-learning-css';quick.className='learning-css-quick';quick.append(node('summary','Generated CSS and the calculation'));
      const calculation=node('p');calculation.id=id+'-learning-calculation';calculation.className='help';const pre=node('pre'),code=node('code');code.id=id+'-learning-code';pre.append(code);quick.append(calculation,pre);host.append(quick,node('h4','Learning preview'));
      const tools=node('div');tools.className='step-learning-tools';host.append(tools);const theme=api.theme(id+'-website-theme',tools);
      const widthField=node('div'),label=node('label','Learning viewport'),width=node('select');width.id=id+'-learning-width';label.htmlFor=width.id;
      for(const [value,text]of [['fluid','Available width'],['320','320px'],['768','768px'],['1280','1280px']])width.add(new Option(text,value));widthField.className='field';widthField.append(label,width);tools.append(widthField);
      const status=node('p');status.id=id+'-learning-status';status.className='help';status.setAttribute('role','status');host.append(status);
      const scroll=node('div');scroll.className='step-learning-scroller';host.append(scroll);parent.prepend(host);
      const paper=node('body');paper.innerHTML='<header class="site-header sample-header" data-learning-part="navigation"><div class="container header-inner"><strong>Learning Studio</strong><nav aria-label="Learning navigation"><a href="#learning-content">Lessons</a> <a href="#learning-footer">Contact</a></nav></div></header><main id="learning-content"><section class="section sample-section container" data-learning-part="layout"><h1 class="page-title">Make room for learning</h1><p>Explore the same components in both website themes. The outlined component follows your selection.</p><div class="card-grid" data-learning-part="grid"><article class="card" data-learning-part="cards"><h2 class="heading-2">A clear next step</h2><p>Readable text, surfaces and borders help this content belong together.</p><a href="#learning-field" data-learning-part="links">Explore a lesson</a><div data-learning-part="buttons" class="step-learning-actions"></div></article><article class="card" data-learning-part="cards"><h2 class="heading-2">Try a useful control</h2><label for="learning-field">Your next lesson</label><input class="input" id="learning-field" data-learning-part="inputs" value="Design foundations"><p role="status" data-learning-part="feedback">A useful status message accompanies colour.</p><button class="button" type="button" data-learning-part="control">Try this action</button></article></div></section></main><footer class="website-footer" id="learning-footer" data-learning-part="footer"><div class="container">Independent teaching content. Website CSS and saved themes are shared.</div></footer>';
      const buttons=paper.querySelector('.step-learning-actions');for(const variant of ['primary','secondary','accent','outline','text']){const button=node('button',variant[0].toUpperCase()+variant.slice(1)+' action');button.type='button';button.dataset.learningVariant=variant;buttons.append(button);}
      const swatches=node('div');swatches.className='step-learning-swatches';paper.querySelector('main > section').prepend(swatches);
      const preview=api.mount({id:id+'-learning-frame',title:DSStudio.stages[stage].label+' learning preview',element:paper,parent:scroll,ready:sync,layout:'.step-learning-actions { display:flex; flex-wrap:wrap; gap:var(--space-2); margin-block:var(--space-3); } [data-learning-selected] { outline:3px solid var(--learning-ui-focus); outline-offset:-3px; } [data-simulated-state="focus"] :is(.button,.input) { outline:var(--focus-width) solid var(--focus); outline-offset:3px; } [data-simulated-state="hover"] .button { background:var(--primary-hover); } [data-simulated-state="active"] .button { transform:translateY(2px); }'});
      let selected=stage===9?'grid':stage===10?'inputs':'cards';
      const view={id,stage,owner,host,scope,theme,width,status,code,calculation,preview,paper,get selected(){return selected;}};views.push(view);
      function choose(part){selected=part;sync();}
      width.addEventListener('change',sync);
      const pane=document.querySelector('[data-journey-pane="'+stage+'"]');
      if(stage!==4){const field=node('div');field.className='step-theme-field';pane.querySelector('h3').after(field);view.stepTheme=api.theme(id+'-step-theme',field);}
      for(const container of [owner,pane])container.addEventListener('focusin',event=>{
        if(host.contains(event.target))return;const control=event.target.id;
        if(stage===9)choose(/gutter|maxWidth|wide|stack/i.test(control)?'layout':'grid');
        if(stage===10)choose(/Underline/.test(control)?'links':/Motion|Reduce/.test(control)?'control':'inputs');
      });
      owner.addEventListener('toggle',sync);return view;
    }
    function candidate(view){
      let snapshot=DSStudio.propertyEditors.draftSnapshot(view.scope);
      if(view.id==='palette-brand')snapshot.state.brandPalette=DSStudio.brandPalette.proposedItems();
      if(view.id==='palette-components')snapshot=DSStudio.propertyEditors.buttonSnapshot();
      if(view.id==='colour'){
        const hex=get('oklchHex').textContent.trim(),role=get('oklchRole').value;
        if(validHex(hex)&&['primary','secondary','accent'].includes(role))snapshot.state[role]=hex;
      }
      return snapshot;
    }
    function sync(){
      for(const view of views){
        view.theme.value=state.theme;if(view.stepTheme)view.stepTheme.value=state.theme;if(DSStudio.activeStage!==view.stage || !view.owner.open)continue;
        const snapshot=candidate(view),s=snapshot.state,a=s.advanced,r=s.responsiveDesign;
        const family=view.id==='palette-components'?get('palette-component-family').value:view.selected;
        for(const part of view.paper.querySelectorAll('[data-learning-part]'))part.toggleAttribute('data-learning-selected',part.dataset.learningPart===family);
        const role=view.id==='colour'?get('oklchRole').value:view.id==='palette-roles'?get('palette-anchor-selection').value:null;
        for(const button of view.paper.querySelectorAll('[data-learning-variant]')){button.className='ds-button ds-button--'+button.dataset.learningVariant+(s.buttonDesign.size==='md'?'':' ds-button--'+s.buttonDesign.size);button.toggleAttribute('data-learning-selected',button.dataset.learningVariant===role);}
        const swatches=view.paper.querySelector('.step-learning-swatches');swatches.hidden=!['palette-brand','palette-shades'].includes(view.id);
        if(!swatches.hidden){
          const selection=get('palette-brand-selection').value,family=get('palette-stage-shades').querySelector('[data-palette-family][aria-pressed="true"]')?.dataset.paletteFamily||'primary';
          const ramp=family==='neutral'?makeNeutralRamp(s.primary,s.method):makeRamp(s[family],s.method);
          const items=view.id==='palette-brand'?s.brandPalette.map(brand=>({name:brand.name,token:'--brand-'+brand.id,hex:brand.hex,selected:brand.id===selection})):Object.entries(ramp).map(([step,hex])=>({name:family+' '+step,token:'--'+family+'-'+step,hex,selected:step==='500'}));
          swatches.replaceChildren(...items.map(item=>{const swatch=node('p',item.name+' / '+item.token+' / '+item.hex);swatch.style.borderLeft='2rem solid var('+item.token+')';swatch.style.padding='8px';swatch.toggleAttribute('data-learning-selected',item.selected);return swatch;}));
        }
        const input=view.paper.querySelector('.input'),control=view.paper.querySelector('.button'),feedback=view.paper.querySelector('[data-learning-part="feedback"]');
        view.paper.dataset.simulatedState=view.stage===10?a.state:'default';
        input.disabled=view.stage===10&&a.state==='disabled';input.readOnly=view.stage===10&&a.state==='readonly';input.setAttribute('aria-invalid',String(view.stage===10&&a.state==='invalid'));
        control.disabled=view.stage===10&&['disabled','loading'].includes(a.state);control.setAttribute('aria-busy',String(view.stage===10&&a.state==='loading'));control.setAttribute('aria-pressed',String(view.stage===10&&a.state==='selected'));control.textContent=view.stage===10&&a.state==='loading'?'Processing…':'Try this action';
        feedback.style.color='var(--'+(a.state==='invalid'?'danger':a.state==='success'?'success':'text-muted')+')';feedback.textContent=a.state==='invalid'?'Choose a valid lesson.':a.state==='success'?'Lesson selected.':'A useful status message accompanies colour.';
        view.preview.frame.style.width=view.width.value==='fluid'?'100%':view.width.value+'px';view.preview.render(snapshot);
        const css=DSStudio.exports.css(s.sampleMode,snapshot);if(view.code.textContent!==css)view.code.textContent=css;
        const theme=s.theme==='dark'?'Dark':'Light',draft=DSStudio.propertyEditors.hasDrafts(view.scope)||view.id==='palette-components'&&DSStudio.propertyEditors.hasButtonDrafts()||view.id==='palette-brand'&&DSStudio.brandPalette.hasDrafts();
        view.status.textContent=(draft?'Proposed':'Saved')+' settings / '+theme+' website theme. Outlined: '+family+'. Theme selection is saved in project JSON; proposed property edits use their Save action.';
        const math=view.stage===9?'Breakpoints: '+r.stack+'px ÷ 16 = '+r.stack/16+'rem; wide '+r.wide+'px ÷ 16 = '+r.wide/16+'rem. Card minimum '+a.columns+'px + gap '+a.gap+'px controls wrapping. Gutters '+r.gutter+'px / '+r.wideGutter+'px.':view.stage===10?'Focus width '+a.focus+'px; field/action minimum height '+a.height+'px; motion '+(a.reduce?0:a.motion)+'ms. Link underline '+(a.underline?'enabled':'disabled')+'. State: '+a.state+'. Use Tab on the real controls to review focus.':view.id==='colour'?'OKLCH proposal '+get('oklchCoords').textContent+' → '+get('oklchHex').textContent+'. Apply saves the selected anchor; the full CSS below shows this proposal.':'Anchor → generated shade → semantic role → component. '+theme+' semantic values are in '+(s.theme==='dark'?'[data-theme="dark"]':':root')+'. Brand and button settings are shared; semantic colour overrides belong to the selected theme.';
        view.calculation.textContent=math+' Complete generated '+s.sampleMode+' CSS follows. Shared rules apply in both themes; the dark block replaces the theme tokens.';
      }
    }
    definitions.forEach(create);
    // Palette browsing changes the chosen component without changing project data.
    for(const type of ['input','change','click'])document.addEventListener(type,()=>queueMicrotask(sync));
    document.addEventListener('toggle',sync,true);
    DSStudio.on('properties:refreshed',sync);DSStudio.on('stage:change',sync);DSStudio.on('palette:proposal',sync);
    DSStudio.views.subscribe({id:'step-learning-previews',phase:'lesson',events:['foundation:updated','output:updated','project:sync'],run:sync});
    DSStudio.stepLearning={sync,views};sync();
  }
});
