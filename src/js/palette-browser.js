"use strict";
/* Architecture-style selection and properties, sharing the existing Palette model. */
DSStudio.register({
  id:'palette-browser',title:'Palette lists and selected properties',
  init() {
    const get=id=>document.getElementById(id),ui=DSStudio.paletteWorkspace,root=get('palette-workspace');
    root.querySelector(':scope > header > p').textContent='Choose an item on the left and edit its properties on the right. Use Save to apply property changes or Discard to restore saved values. Semantic Save opens contrast review before Apply. Responsive page preview shows saved values and preserves drafts.';
    const layouts=new Map(),brandButtons=new Map(),readouts=new WeakMap();let anchor='primary',shade='primary',readoutId=0,identity,draftKey='',draftBase='',draft='';
    function element(tag,cls,text){const node=document.createElement(tag);if(cls)node.className=cls;if(text)node.textContent=text;return node;}
    function button(text,action){const node=element('button','ghost',text);node.type='button';node.addEventListener('click',action);return node;}
    function append(target,...nodes){target.append(...nodes.filter(Boolean));}
    for(const stage of root.querySelectorAll(':scope > [data-palette-stage]')){
      const body=stage.querySelector('.palette-stage-body'),intro=body.querySelector(':scope > p'),actions=body.querySelector(':scope > .palette-stage-actions');
      const grid=element('div','palette-editor-columns'),browse=element('section','palette-browser'),props=element('section','palette-properties');
      const key=stage.dataset.paletteStage;browse.id='palette-browse-'+key;props.id='palette-properties-'+key;
      browse.setAttribute('aria-labelledby','palette-browse-title-'+key);props.setAttribute('aria-labelledby','palette-properties-title-'+key);
      const browseTitle=element('h4',null,'Browse and manage'),propsTitle=element('h4',null,'Selected properties');browseTitle.id='palette-browse-title-'+key;propsTitle.id='palette-properties-title-'+key;
      append(browse,browseTitle,intro);props.append(propsTitle);
      for(const child of [...body.children])if(child!==actions)props.append(child);
      grid.append(browse,props);body.prepend(grid);if(actions)body.append(actions);layouts.set(key,{browse,props,title:propsTitle});
    }
    const brand=layouts.get('brand'),brandNative=get('palette-brand-selection');brandNative.closest('.field').hidden=true;brand.browse.append(brandNative.closest('.field'));
    const searchField=element('div','field'),searchLabel=element('label',null,'Find a brand colour'),search=element('input');search.id='palette-brand-query';search.type='search';searchLabel.htmlFor=search.id;searchField.append(searchLabel,search);
    const brandList=element('div','palette-item-list');brandList.id='palette-brand-list';brandList.setAttribute('role','group');brandList.setAttribute('aria-label','Brand colours');
    const results=element('p','help');results.id='palette-brand-results';results.setAttribute('role','status');
    const remove=button('Remove selected colour',()=>get('jBrandEditor').querySelector('[data-brand-id]:not([hidden]) [data-remove-brand]')?.click());remove.id='palette-brand-remove';
    append(brand.browse,searchField,get('jBrandCount'),get('jBrandAdd'),remove,results,brandList,get('jBrandStatus'));
    get('palette-brand-properties-title').hidden=true;brand.title.textContent='Selected colour properties';const allBrands=get('jBrandSwatches').closest('details');if(allBrands)brand.browse.append(allBrands);
    // Shared UI anchors are fixed roles; only their assignments can be reset.
    const roles=layouts.get('roles'),anchorField=element('div','field'),anchorLabel=element('label',null,'UI anchor to edit'),anchorSelect=element('select');
    anchorSelect.id='palette-anchor-selection';anchorSelect.size=3;anchorLabel.htmlFor=anchorSelect.id;
    for(const key of ['primary','secondary','accent']){anchorSelect.add(new Option(key[0].toUpperCase()+key.slice(1),key));roles.browse.append(get('palette-reset-'+key));}
    anchorField.append(anchorLabel,anchorSelect);roles.browse.insertBefore(anchorField,get('palette-reset-primary'));get('brandRoleAssignments').hidden=true;
    anchorSelect.addEventListener('change',()=>{anchor=anchorSelect.value;sync();});
    const anchorHelp=element('p','help');anchorHelp.id='palette-anchor-help';roles.title.after(anchorHelp);
    anchorSelect.setAttribute('aria-describedby',anchorHelp.id);
    const shades=layouts.get('shades'),shadeList=element('div','palette-item-list'),shadeButtons=new Map();shades.browse.append(shadeList);
    for(const [key,label]of [['primary','Primary'],['secondary','Supporting'],['accent','Accent'],['neutral','Neutral']]){const item=button(label+' family',()=>{shade=key;sync();get('jRamp').focus();});item.dataset.paletteFamily=key;shadeList.append(item);shadeButtons.set(key,item);}
    shades.title.textContent='Selected family properties';
    const semantics=layouts.get('semantics'),semanticSelect=get('jSemanticRole');semanticSelect.size=8;append(semantics.browse,semanticSelect.closest('.field'),get('jSemanticReset'));
    semantics.title.textContent='Selected semantic role properties';get('jSemanticTitle').hidden=true;
    const semanticSection=get('jSemanticTitle').closest('section'),form=element('div','palette-semantic-fields');
    function field(id,label,type='text',readonly=false){const wrap=element('div','field'),caption=element('label',null,label),input=element('input');caption.htmlFor=id;input.id=id;input.type=type;input.readOnly=readonly;wrap.append(caption,input);form.append(wrap);return input;}
    const semanticName=field('palette-semantic-name','Role name','text',true),semanticToken=field('palette-semantic-token','CSS token','text',true),semanticHex=field('palette-semantic-hex','Proposed HEX colour'),semanticPicker=field('palette-semantic-picker','Colour picker','color');
    const choiceField=element('div','field'),choiceLabel=element('label',null,'Proposed colour'),colourChoice=element('select'),choiceHelp=element('p','help');
    colourChoice.id='palette-semantic-colour';choiceLabel.htmlFor=colourChoice.id;
    choiceHelp.id='palette-semantic-colour-help';choiceHelp.textContent='Choose a brand colour or generated shade for the current theme, or enter a custom colour below. Preview before applying; applied custom colours stay fixed when the palette changes.';
    colourChoice.setAttribute('aria-describedby',choiceHelp.id);choiceField.append(choiceLabel,colourChoice,choiceHelp);semanticHex.closest('.field').before(choiceField);
    let choiceSignature='',preferredChoice=null;
    function syncColourChoices(){
      const signature=JSON.stringify([state.brandPalette,state.primary,state.secondary,state.accent,state.method,state.theme,state.semanticOverrides,state.buttonDesign,state.advanced?.colors]);
      if(signature!==choiceSignature){
        choiceSignature=signature;
        const colours=new Map(),groups=new Map(),brandNames=new Map(state.brandPalette.map(item=>['--brand-'+item.id,item.name]));
        for(const row of window.dssReadTokens()){
          if(!validHex(row.value) || !(row.name.startsWith('--brand-') || /-(50|100|200|300|400|500|600|700|800|900|950)$/.test(row.name)))continue;
          if(row.scope==='Dark'){if(state.theme==='dark')colours.set(row.name,row);}
          else if(!colours.has(row.name))colours.set(row.name,row);
        }
        for(const row of colours.values()){
          const brand=row.name.startsWith('--brand-'),family=row.name.slice(2).replace(/-\d+$/,'');
          const label=brand?'Brand colours':family.split('-').map(word=>word[0].toUpperCase()+word.slice(1)).join(' ')+' shades';
          if(!groups.has(label)){const group=element('optgroup');group.label=label;groups.set(label,group);}
          const option=new Option((brand?brandNames.get(row.name)+' · ':'')+row.name+' · '+row.value.toUpperCase(),row.name);
          option.dataset.hex=row.value.toUpperCase();groups.get(label).append(option);
        }
        colourChoice.replaceChildren(new Option('Custom colour','custom'),...groups.values());
      }
      const options=[...colourChoice.options],hex=draft.toUpperCase(),selected=options.find(option=>option.value===preferredChoice);
      if(preferredChoice!=='custom' && (!selected || selected.dataset.hex!==hex))preferredChoice=null;
      colourChoice.value=preferredChoice||options.find(option=>option.dataset.hex===hex)?.value||'custom';
    }
    semanticHex.maxLength=7;semanticHex.pattern='#[0-9A-Fa-f]{6}';semanticHex.placeholder='#14253A';
    const proposalStatus=element('p','help');proposalStatus.id='palette-semantic-proposal-status';semanticHex.setAttribute('aria-describedby',proposalStatus.id);
    const discard=button('Discard proposed colour',()=>{draft=draftBase;preferredChoice=null;semanticHex.setCustomValidity('');syncSemantic();});discard.id='palette-semantic-discard';form.append(proposalStatus,discard);semanticSection.insertBefore(form,get('jSemanticHelp'));
    function syncSemantic(){
      const key=state.theme+':'+semanticSelect.value,value=palette().roles[semanticSelect.value];
      if(key!==draftKey)preferredChoice=null;
      if(key!==draftKey || value!==draftBase){draftKey=key;draftBase=value;draft=value;semanticHex.setCustomValidity('');}
      semanticName.value=(semanticSelect.selectedOptions[0]?.textContent||'').replace(/\s*\(--[^)]+\)$/,'');semanticToken.value='--'+semanticSelect.value;
      if(document.activeElement!==semanticHex)semanticHex.value=draft;if(validHex(draft))semanticPicker.value=draft;
      syncColourChoices();
      const changed=draft.toUpperCase()!==draftBase.toUpperCase();discard.disabled=!changed;
      proposalStatus.textContent=changed?'Proposed change is not applied. Preview its contrast effects, then Apply or cancel.':'Current website value. Edit a proposal, then preview before applying.';
    }
    colourChoice.addEventListener('change',()=>{
      if(colourChoice.value==='custom'){preferredChoice='custom';syncSemantic();return;}
      const option=colourChoice.selectedOptions[0];if(!validHex(option?.dataset.hex))return;
      preferredChoice=option.value;draft=option.dataset.hex;semanticHex.value=draft;semanticHex.setCustomValidity('');syncSemantic();
    });
    semanticHex.addEventListener('input',()=>{draft=semanticHex.value;preferredChoice=null;semanticHex.setCustomValidity('');syncSemantic();});
    semanticPicker.addEventListener('input',()=>{draft=semanticPicker.value;preferredChoice=null;semanticHex.value=draft;semanticHex.setCustomValidity('');syncSemantic();});
    semanticHex.addEventListener('keydown',event=>{if(event.key==='Enter'){event.preventDefault();get('jSemanticEdit').click();}});
    get('jSemanticEdit').addEventListener('click',event=>{syncSemantic();if(!validHex(draft)){semanticHex.setCustomValidity('Enter a six-digit HEX colour, such as #14253A.');semanticHex.reportValidity();event.preventDefault();event.stopImmediatePropagation();}},true);
    get('jSemanticEdit').addEventListener('click',()=>{if(get('colourRepair').open && validHex(draft) && draft.toUpperCase()!==draftBase.toUpperCase()){get('repairHex').value=draft;get('repairHex').dispatchEvent(new Event('input',{bubbles:true}));}});
    const backgrounds=layouts.get('backgrounds'),regionSelect=get('palette-region-selection');regionSelect.size=4;backgrounds.browse.append(regionSelect.closest('.field'));
    const clearBackground=button('Use default for selected region',()=>get((regionSelect.value==='body'?'page':regionSelect.value)+'-background-reset').click());clearBackground.id='palette-background-clear';backgrounds.browse.append(clearBackground);
    const components=layouts.get('components'),familySelect=get('palette-component-family'),variantSelect=get('palette-button-variant');familySelect.size=4;variantSelect.size=5;
    append(components.browse,familySelect.closest('.field'),variantSelect.closest('.field'),get('palette-component-context'),get('palette-button-clear'),get('palette-button-focus-reset'));
    const review=layouts.get('review');review.title.textContent='Feedback and review properties';
    const guide=review.props.querySelector(':scope > ul');if(guide)review.browse.append(guide);
    const feedback=get('palette-status-role'),feedbackProperties=feedback.closest('.field'),feedbackReference=feedbackProperties.closest('details'),feedbackPicker=element('div','field');feedback.size=3;append(feedbackPicker,feedbackProperties.querySelector('label[for="palette-status-role"]'),feedback);review.browse.append(feedbackPicker,get('palette-status-reset'));review.props.insertBefore(feedbackProperties,review.props.children[1]||null);if(feedbackReference?.children.length===1)feedbackReference.remove();
    for(const actions of review.props.querySelectorAll(':scope > .button-row'))review.browse.append(actions);
    // Generated declarations remain inspectable/copyable as real read-only fields.
    function readout(code){
      let entry=readouts.get(code);if(!entry){const input=element('input','palette-value-field');input.type='text';input.readOnly=true;input.id='palette-value-'+(++readoutId);code.hidden=true;code.after(input);entry={input};readouts.set(code,entry);}
      const name=code.dataset.componentToken||code.textContent.split(':')[0];
      if(!code.dataset.componentToken){if(!entry.label){entry.label=element('label','palette-value-label');entry.label.htmlFor=entry.input.id;entry.input.before(entry.label);}entry.label.textContent=name;}
      entry.input.setAttribute('aria-label',name+' generated value');entry.input.value=code.dataset.componentToken?code.textContent:(code.textContent.match(/#[0-9a-f]{6}/i)?.[0]||code.textContent);
    }
    function syncBrand(){
      const items=state.brandPalette,current=brandNative.value,query=search.value.trim().toLowerCase();
      for(const [id,item]of brandButtons)if(!items.some(colour=>colour.id===id)){item.remove();brandButtons.delete(id);}
      for(const [index,colour]of items.entries()){
        let item=brandButtons.get(colour.id);if(!item){item=button('',()=>{ui.selectBrand(colour.id);sync();get('jBrandEditor').querySelector('[data-brand-id]:not([hidden]) [data-brand-field="name"]')?.focus();});const chip=element('span','brand-palette-chip'),text=element('span'),name=element('strong'),token=element('code');chip.setAttribute('aria-hidden','true');text.append(name,token);item.append(chip,text);item.dataset.paletteColour=colour.id;brandButtons.set(colour.id,item);}
        if(brandList.children[index]!==item)brandList.insertBefore(item,brandList.children[index]||null);
        item.querySelector('strong').textContent=colour.name;item.querySelector('code').textContent='--brand-'+colour.id+' '+colour.hex;item.querySelector('.brand-palette-chip').style.backgroundColor=colour.hex;item.setAttribute('aria-pressed',String(colour.id===current));item.hidden=!((colour.name+' '+colour.id+' '+colour.hex).toLowerCase().includes(query));
      }
      remove.disabled=items.length<=1;results.hidden=!query;if(query){const count=[...brandButtons.values()].filter(item=>!item.hidden).length;results.textContent=count?count+' matching colour'+(count===1?'':'s')+'.':'No matching colours. Change or clear the search.';}
    }
    function sync(){
      if(identity!==state){identity=state;anchor='primary';shade='primary';draftKey='';search.value='';}
      syncBrand();
      anchorSelect.value=anchor;
      for(const key of ['primary','secondary','accent']){const title=key[0].toUpperCase()+key.slice(1);get('j'+title).closest('.field').hidden=key!==anchor;get('palette-reset-'+key).hidden=key!==anchor;}
      roles.title.textContent=anchor[0].toUpperCase()+anchor.slice(1)+' anchor properties';
      anchorHelp.textContent={primary:'Primary supplies the main action and link colour family.',secondary:'Secondary supplies the supporting action colour family.',accent:'Accent supplies contrasting highlights and the accent action colour family.'}[anchor]+' Choose a brand colour or set a custom colour below. This anchor is shared by both website themes; fixed semantic or component overrides keep their own values.';
      for(const [key,item]of shadeButtons){const details=get('main-palette-steps').querySelector('[data-palette-role="'+key+'"]');details.hidden=key!==shade;if(key===shade)details.open=true;item.setAttribute('aria-pressed',String(key===shade));}
      get('neutralPaletteAnchor').closest('section').hidden=shade!=='neutral';
      syncSemantic();
      const region=regionSelect.value,reset=get((region==='body'?'page':region)+'-background-reset');clearBackground.disabled=reset.disabled;backgrounds.title.textContent=region[0].toUpperCase()+region.slice(1)+' background properties';
      const isButton=familySelect.value==='buttons';get('palette-component-values').hidden=isButton;get('palette-button-clear').hidden=!isButton;get('palette-button-focus-reset').hidden=!isButton;
      if(isButton)root.querySelector('.palette-component-overrides').open=true;
      components.title.textContent=isButton?(variantSelect.selectedOptions[0]?.textContent||'Button')+' colour properties':(familySelect.selectedOptions[0]?.textContent||'Component')+' properties';
      for(const code of root.querySelectorAll('#main-palette-steps [data-shade] code,[data-component-token]'))readout(code);
    }
    function prepare(control){const match=control?.id.match(/^j(Primary|Secondary|Accent)(Brand)?$/);if(match)anchor=match[1].toLowerCase();const family=control?.closest('#main-palette-steps [data-palette-role]')?.dataset.paletteRole;if(family)shade=family;}
    search.addEventListener('input',syncBrand);
    for(const id of ['palette-brand-selection','jSemanticRole','palette-region-selection','palette-component-family','palette-button-variant','palette-status-role'])get(id).addEventListener('change',sync);
    get('jBrandEditor').addEventListener('focusin',sync);get('jBrandAdd').addEventListener('click',sync);
    const beforeReveal=window.dssRevealSection;window.dssRevealSection=function(id,scroll=true){prepare(get(id));const result=beforeReveal(id,scroll);sync();return result;};
    const beforeControl=ui.revealControl;ui.revealControl=function(control){prepare(control);beforeControl(control);sync();};
    const beforeShow=ui.show;ui.show=function(key,focus=true){beforeShow(key,focus);sync();};
    const beforeBrand=ui.selectBrand;ui.selectBrand=function(id){beforeBrand(id);sync();};
    DSStudio.on('foundation:updated',sync);
    DSStudio.on('output:updated',sync);
    root.addEventListener('toggle',()=>queueMicrotask(sync),true);
    get('brandPalette').addEventListener('toggle',()=>{if(get('brandPalette').open)sync();});
    DSStudio.on('stage:change',({stage})=>{if(stage.index===4)sync();});
    DSStudio.paletteBrowser={sync};sync();DSStudio.emit('lesson:content');
  }
});
