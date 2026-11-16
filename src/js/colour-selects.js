'use strict';
/* Shared visual palette choices over the original labelled select controls.
   IDs, values, focus, form ownership and native input/change contracts survive. */
DSStudio.register({
  id:'colour-selects',title:'Inline colour previews in palette selectors',
  init(){
    const get=id=>document.getElementById(id),entries=new Map();
    const menu=document.createElement('div');menu.id='colour-select-options';menu.className='colour-select-menu';menu.setAttribute('role','listbox');menu.hidden=true;document.body.append(menu);
    const sourceIds=new Set(['bdSource','oklchRole','brandApplyRole','palette-anchor-selection']);
    const roleIds=new Set(['jSemanticRole','palette-status-role']);
    let active=null,activeIndex=-1,rows=[],queued=false,typeText='',typeTimer,roleColours;
    const hex=value=>validHex(value)?value.toUpperCase():null;
    const node=(tag,cls,text)=>{const el=document.createElement(tag);if(cls)el.className=cls;if(text)el.textContent=text;return el;};
    function colour(select,option){
      if(!option)return null;
      if(option.value==='none')return null;
      if(option.value==='default'){
        const match=/^(page|header|main|footer)-background-brand$/.exec(select.id),key=match?(match[1]==='page'?'background':match[1]+'-background'):select.id==='palette-semantic-colour'?get('jSemanticRole').value:null;
        if(key)return hex(palette(state.theme,{...state,semanticOverrides:{...state.semanticOverrides,[state.theme]:{...state.semanticOverrides?.[state.theme],[key]:undefined}}}).roles[key]);
        const anchor=/^j(Primary|Secondary|Accent)Brand$/.exec(select.id);if(anchor)return hex(DEFAULT[anchor[1].toLowerCase()]);
        if(select.id==='brandAccent')return hex(DEFAULT.accent);
        if(select.id==='bdSource'){const source=DSStudio.project.buttonDefaults().sources[get('bdVariant').value];return hex(state[source])||hex(source);}
      }

      if(select.id==='palette-brand-selection')return hex(state.brandPalette.find(item=>item.id===option.value)?.hex);
      if(roleIds.has(select.id))return colourIsTransparent(option.value)?null:hex(roleColours?.[option.value]);
      if(sourceIds.has(select.id) && ['primary','secondary','accent'].includes(option.value))return state.colourTransparency?.['anchor:'+option.value]?null:hex(state[option.value]);
      if(!option.value||option.value==='custom')return customColour(select);
      return hex(option.dataset.hex)||hex(option.value)||hex(option.textContent.match(/#[0-9a-f]{6}\b/i)?.[0]);
    }
    function customColour(select){
      const prefix=select.id.replace(/-brand$/,'');
      const linked=select.id==='bdSource'?'bdCustom':select.id==='palette-semantic-colour'?'palette-semantic-hex':/^j(Primary|Secondary|Accent)Brand$/.test(select.id)?select.id.replace(/Brand$/,''):select.id==='brandAccent'?'accent':prefix+'-hex';
      return hex(get(linked)?.value);
    }
    function choices(select){
      return [...select.options].map((option,index)=>({option,index,hex:colour(select,option),group:option.parentElement.tagName==='OPTGROUP'?option.parentElement.label:'',disabled:option.disabled||!!option.closest('optgroup[disabled]'),hidden:option.hidden||!!option.closest('optgroup[hidden]')})).filter(row=>!row.hidden);
    }
    function label(row){const text=row.option.textContent,token=row.option.dataset.token||(['primary','secondary','accent'].includes(row.option.value)&&sourceIds.has(row.option.closest('select').id)?'--'+row.option.value+'-500':'');return text+(token&&!text.includes(token)?' / '+token:'')+(row.hex && !text.toUpperCase().includes(row.hex)?' / '+row.hex:'');}
    function chip(value){const el=node('span','colour-select-swatch');el.setAttribute('aria-hidden','true');if(value)el.style.backgroundColor=value;else el.classList.add('is-custom');return el;}
    function renderInline(entry,options){
      const scroll=entry.view.scrollTop,fragment=document.createDocumentFragment();let group=null;
      for(const row of options){
        if(row.group&&row.group!==group)fragment.append(node('div','colour-select-group',row.group));group=row.group;
        const item=node('div','colour-select-inline-row');item.dataset.inlineColourOption=String(row.index);item.classList.toggle('is-selected',row.index===entry.select.selectedIndex);item.classList.toggle('is-disabled',row.disabled);
        item.append(chip(row.hex),node('span','colour-select-option-label',label(row)));fragment.append(item);
      }
      entry.view.replaceChildren(fragment);entry.view.style.maxHeight=(Math.min(8,Math.max(1,entry.select.size))*44+8)+'px';entry.view.scrollTop=scroll;
      if(document.activeElement===entry.select)entry.view.querySelector('.is-selected')?.scrollIntoView({block:'nearest'});
    }
    function close(){
      if(active){active.select.setAttribute('aria-expanded','false');active.select.removeAttribute('aria-activedescendant');}
      active=null;activeIndex=-1;menu.hidden=true;typeText='';clearTimeout(typeTimer);
    }
    function position(){
      if(!active)return;
      const box=active.wrapper.getBoundingClientRect(),width=Math.min(Math.max(box.width,240),window.innerWidth-16),below=window.innerHeight-box.bottom-8,above=box.top-8;
      menu.style.width=width+'px';menu.style.left=Math.max(8,Math.min(box.left,window.innerWidth-width-8))+'px';
      const useBelow=below>=Math.min(240,above),height=Math.max(44,Math.min(360,useBelow?below:above));
      menu.style.maxHeight=height+'px';
      const top=useBelow?box.bottom+4:box.top-4-Math.min(menu.scrollHeight,height);
      menu.style.top=Math.max(8,Math.min(top,window.innerHeight-Math.min(menu.scrollHeight,height)-8))+'px';
    }
    function highlight(index){
      if(!active)return;
      const row=rows.find(item=>item.index===index&&!item.disabled);if(!row)return;
      activeIndex=index;
      for(const item of rows)item.element.classList.toggle('is-active',item.index===index);
      active.select.setAttribute('aria-activedescendant',row.element.id);row.element.scrollIntoView({block:'nearest'});
    }
    function renderMenu(){
      if(!active)return;
      const select=active.select,fragment=document.createDocumentFragment();let lastGroup=null;
      rows=choices(select);
      for(const row of rows){
        if(row.group && row.group!==lastGroup)fragment.append(node('div','colour-select-group',row.group));lastGroup=row.group;
        const el=node('div','colour-select-option');el.id='colour-select-option-'+row.index;el.setAttribute('role','option');el.setAttribute('aria-selected',String(row.index===select.selectedIndex));el.setAttribute('aria-disabled',String(row.disabled));el.dataset.colourOption=String(row.index);
        el.append(chip(row.hex),node('span','colour-select-option-label',label(row)));row.element=el;fragment.append(el);
      }
      menu.replaceChildren(fragment);
      const selected=rows.find(row=>row.index===activeIndex&&!row.disabled)||rows.find(row=>row.index===select.selectedIndex&&!row.disabled)||rows.find(row=>!row.disabled);
      position();if(selected)highlight(selected.index);
    }
    function open(entry){
      if(entry.select.disabled || !entry.select.getBoundingClientRect().width)return;
      close();active=entry;activeIndex=entry.select.selectedIndex;
      const host=entry.select.closest('dialog')||document.body;if(menu.parentElement!==host)host.append(menu);
      menu.setAttribute('aria-label',entry.select.getAttribute('aria-label')||[...entry.select.labels].map(label=>label.textContent.trim()).join(' ')||'Palette colours');
      entry.select.setAttribute('aria-expanded','true');menu.hidden=false;renderMenu();
    }
    function choose(index){
      const entry=active,row=rows.find(item=>item.index===index&&!item.disabled);if(!entry||!row)return;
      close();entry.select.selectedIndex=index;
      entry.select.dispatchEvent(new Event('input',{bubbles:true}));entry.select.dispatchEvent(new Event('change',{bubbles:true}));refresh();entry.select.focus({preventScroll:true});
    }
    function keys(event,entry){
      if(entry.select.disabled)return;
      const key=event.key;
      if(key==='Tab'){close();return;}
      if(key==='Escape'){if(active===entry){event.preventDefault();close();}return;}
      if(['Enter',' ','F4'].includes(key)){
        event.preventDefault();if(active===entry){if(key==='F4')close();else choose(activeIndex);}else open(entry);return;
      }
      if(['ArrowDown','ArrowUp','Home','End','PageDown','PageUp'].includes(key)){
        event.preventDefault();if(active!==entry)open(entry);
        const enabled=rows.filter(row=>!row.disabled);if(!enabled.length)return;
        let index=enabled.findIndex(row=>row.index===activeIndex);
        index=key==='Home'?0:key==='End'?enabled.length-1:Math.max(0,Math.min(enabled.length-1,index+(key==='ArrowUp'?-1:key==='PageUp'?-10:key==='PageDown'?10:1)));
        highlight(enabled[index].index);return;
      }
      if(key.length===1 && !event.ctrlKey && !event.metaKey && !event.altKey){
        event.preventDefault();if(active!==entry)open(entry);
        typeText+=key.toLowerCase();clearTimeout(typeTimer);typeTimer=setTimeout(()=>{typeText='';},700);
        const found=rows.find(row=>!row.disabled&&label(row).toLowerCase().startsWith(typeText))||rows.find(row=>!row.disabled&&label(row).toLowerCase().includes(typeText));if(found)highlight(found.index);
      }
    }
    function enhance(select){
      const wrapper=node('div','colour-select'),view=node('div','colour-select-value'),swatch=chip(null),text=node('span','colour-select-label'),arrow=node('span','colour-select-arrow');view.setAttribute('aria-hidden','true');view.append(swatch,text,arrow);
      select.before(wrapper);wrapper.append(view,select);select.dataset.colourSelect='';
      const inline=Number(select.getAttribute('size')||1)>1;
      if(inline){wrapper.classList.add('is-inline');view.classList.add('colour-select-inline');}else{select.setAttribute('aria-haspopup','listbox');select.setAttribute('aria-controls',menu.id);select.setAttribute('aria-expanded','false');}
      const entry={select,wrapper,view,swatch,text,inline,signature:''};entries.set(select,entry);
      function chooseInline(index){const option=select.options[index];if(select.disabled||!option||option.disabled||option.closest('optgroup[disabled]'))return;select.focus({preventScroll:true});select.selectedIndex=index;select.dispatchEvent(new Event('input',{bubbles:true}));select.dispatchEvent(new Event('change',{bubbles:true}));refresh();}
      select.addEventListener('pointerdown',event=>{
        if(event.button!==0||select.disabled)return;event.preventDefault();select.focus({preventScroll:true});
        if(inline){const item=[...view.querySelectorAll('[data-inline-colour-option]')].find(item=>{const box=item.getBoundingClientRect();return event.clientY>=box.top&&event.clientY<=box.bottom;});if(item)chooseInline(Number(item.dataset.inlineColourOption));return;}
        if(active===entry)close();else open(entry);
      });
      select.addEventListener('mousedown',event=>event.preventDefault());
      select.addEventListener('click',event=>{event.preventDefault();if(!inline&&event.detail===0){if(active===entry)close();else open(entry);}});
      select.addEventListener('keydown',event=>{if(!inline)keys(event,entry);});select.addEventListener('blur',()=>{if(active===entry)close();});
      // The visible list keeps native mouse/touch scrolling. The original select
      // retains its keyboard, accessibility, focus and input/change contracts.
      if(inline)view.addEventListener('click',event=>{const item=event.target.closest('[data-inline-colour-option]');if(item)chooseInline(Number(item.dataset.inlineColourOption));});
      return entry;
    }
    function refresh(){
      roleColours=palette().roles;
      for(const input of document.querySelectorAll('input[type="color"]')){
        if(input.dataset.noneControl || !DSStudio.propertyEditors.transparencyKeyFor(input))continue;
        const button=node('button','ghost colour-none-control','None');button.type='button';button.setAttribute('aria-label','Make '+([...input.labels].map(label=>label.textContent.trim()).join(' ')||'colour')+' transparent');
        button.addEventListener('click',()=>DSStudio.propertyEditors.setTransparent(input,input.dataset.transparentColour!=='true'));button.dataset.transparentFor=input.id;input.after(button);input.dataset.noneControl='true';
      }

      for(const button of document.querySelectorAll('[data-transparent-for]'))button.setAttribute('aria-pressed',String(get(button.dataset.transparentFor)?.dataset.transparentColour==='true'));
      for(const [select]of entries)if(!select.isConnected){if(active?.select===select)close();entries.delete(select);}
      for(const select of document.querySelectorAll('select:not([multiple])')){
        if((/^j(Primary|Secondary|Accent)Brand$/.test(select.id)||select.id==='brandAccent'||select.id==='bdSource') && ![...select.options].some(option=>option.value==='none')){
          const index=select.selectedIndex,value=select.value;select.prepend(new Option('None (transparent)','none'),new Option('Use default colour','default'));if(index<0)select.selectedIndex=-1;else select.value=value;
        }
        const options=choices(select),eligible=sourceIds.has(select.id)||roleIds.has(select.id)||select.id==='palette-brand-selection'||[...select.options].some(option=>hex(option.value)||hex(option.dataset.hex));
        if(!entries.has(select)&&!eligible)continue;
        const entry=entries.get(select)||enhance(select),selected=options.find(row=>row.index===select.selectedIndex),value=selected?.option.value==='none'?null:selected?.hex||customColour(select);
        const nativeHidden=select.hidden||select.style.display==='none';if(nativeHidden!==entry.nativeHidden){entry.wrapper.hidden=nativeHidden;entry.nativeHidden=nativeHidden;}
        const text=selected?label(selected):(select.options[0]?.textContent||'Custom colour');if(entry.text.textContent!==text)entry.text.textContent=text;
        entry.swatch.classList.toggle('is-custom',!value);entry.swatch.style.backgroundColor=value||'';entry.wrapper.classList.toggle('is-disabled',select.disabled);
        const signature=JSON.stringify(options.map(row=>[row.option.value,row.option.textContent,row.hex,row.group,row.disabled]));
        if(entry.inline && (signature!==entry.signature||select.selectedIndex!==entry.selectedIndex))renderInline(entry,options);
        if(active===entry){if(!select.getBoundingClientRect().width||select.disabled)close();else if(signature!==entry.signature||select.selectedIndex!==entry.selectedIndex)renderMenu();}
        entry.signature=signature;entry.selectedIndex=select.selectedIndex;
      }
    }
    // Feature toggle handlers may queue their own control synchronization.
    // Paint after those callbacks as well as the synchronous property refresh.
    function schedule(){if(queued)return;queued=true;setTimeout(()=>{queued=false;refresh();},0);}
    menu.addEventListener('pointerdown',event=>event.preventDefault());
    menu.addEventListener('click',event=>{const row=event.target.closest('[data-colour-option]');if(row)choose(Number(row.dataset.colourOption));});
    document.addEventListener('pointerdown',event=>{if(active&&!active.wrapper.contains(event.target)&&!menu.contains(event.target))close();},true);
    document.addEventListener('input',schedule,true);document.addEventListener('change',schedule,true);document.addEventListener('toggle',schedule,true);
    function reposition(){if(!active)return;const box=active.wrapper.getBoundingClientRect();if(!box.width||box.bottom<0||box.top>window.innerHeight)close();else position();}
    window.addEventListener('resize',reposition);window.addEventListener('scroll',event=>{if(active&&!menu.contains(event.target))reposition();},true);
    new MutationObserver(records=>{if(records.some(record=>record.target.closest?.('select')||[...record.addedNodes,...record.removedNodes].some(node=>node.nodeType===1&&(node.matches('select')||node.querySelector('select')))||(record.type==='attributes'&&record.target.querySelector?.('select'))))schedule();}).observe(document.body,{childList:true,subtree:true,attributes:true,attributeFilter:['disabled','hidden','selected','label','value','data-hex']});
    DSStudio.on('properties:refreshed',()=>{refresh();schedule();});DSStudio.views.subscribe({id:'colour-select-previews',phase:'lesson',events:['output:updated','project:sync','stage:change'],run:()=>{refresh();schedule();}});
    DSStudio.colourSelects={refresh,close};refresh();
  }
});
