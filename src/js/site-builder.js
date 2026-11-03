'use strict';
/* Edit the existing bounded plan and semantic roles; previews and exports keep
   using their shared generators. Imported labels are always rendered as text. */
DSStudio.register({
  id: 'site-builder', title: 'Sitemap editor and webpage background',
  init() {
    const get = id => document.getElementById(id);
    const root = get('sitemap-editor');
    root.className = 'sitemap-editor';
    root.innerHTML = `<label for="sitemap-items">Sitemap entries</label>
      <select id="sitemap-items" size="8" aria-describedby="sitemap-help"></select>
      <p class="help" id="sitemap-help">Select an entry to edit its label, parent or destination. Changes appear in the responsive preview, footer sitemap and live HTML inspector.</p>
      <div class="button-row"><button id="sitemap-new" type="button" class="ghost">New entry</button><button id="sitemap-up" type="button" class="ghost">Move up</button><button id="sitemap-down" type="button" class="ghost">Move down</button></div>
      <form id="sitemap-form">
        <label for="sitemap-label">Entry label</label><input id="sitemap-label" maxlength="64" required autocomplete="off">
        <label for="sitemap-parent">Parent section</label><select id="sitemap-parent"></select>
        <label for="sitemap-target">Link destination</label><select id="sitemap-target"></select>
        <p class="help">Choose an existing section, or keep a planned page without a link. Two levels are supported.</p>
        <div class="button-row"><button type="submit" class="ghost">Save entry</button><button id="sitemap-delete" type="button" class="ghost">Delete entry</button></div>
      </form>
      <label class="sitemap-planned-toggle"><input id="sitemap-planned" type="checkbox"> Show planned entries in the footer</label>
      <button id="sitemap-undo" type="button" class="ghost" disabled>Undo last sitemap change</button>
      <p id="sitemap-status" class="help" role="status"></p>`;
    let selected = null, previous = null, signature = '', undoMode = null, ownChange = false;
    const mode = () => state.sampleMode === 'basic' ? 'basic' : 'advanced';
    const plan = () => DSStudio.process.currentPlan();
    const groups = () => DSStudio.process.hierarchy(plan().pages);
    const decode = () => selected === null ? null : selected.split(':').map(Number);
    const entries = () => groups().flatMap(([label,children],p) => [[`${p}:-1`,label],...children.map((child,c)=>[`${p}:${c}`,`  — ${child}`])]);
    const options = (control, items) => control.replaceChildren(...items.map(([value,label])=>new Option(label,value)));
    function edit() {
      const map = groups(), choice = decode();
      const [p,c] = choice || [-1,-1], group = map[p];
      const label = group ? c<0 ? group[0] : group[1][c] : '';
      get('sitemap-label').value = label || '';
      options(get('sitemap-parent'), [['','Top level'],...map.flatMap(([name],i)=>i===p && c<0 ? [] : [[String(i),name]])]);
      get('sitemap-parent').value = group && c>=0 ? String(p) : '';
      options(get('sitemap-target'), [['planned','Planned page (no link)'],['auto','Match the label automatically'],...DSStudio.process.inventory(mode()).map(([name,id])=>[id,name])]);
      const links = plan().pageLinks[mode()];
      get('sitemap-target').value = Object.hasOwn(links,label) ? links[label] || 'planned' : label ? DSStudio.process.inventory(mode()).find(([name])=>name===label)?.[1] || 'auto' : 'planned';
      get('sitemap-delete').disabled = !group;
      get('sitemap-delete').textContent = group && c<0 && group[1].length ? `Delete group (${group[1].length+1} entries)` : 'Delete entry';
      const index = choice ? c<0 ? p : c : -1, count = choice ? c<0 ? map.length : group?.[1].length || 0 : 0;
      get('sitemap-up').disabled = index<=0;
      get('sitemap-down').disabled = index<0 || index>=count-1;
    }
    function sync() {
      const current = plan(), next = JSON.stringify([mode(),current.pages,current.pageLinks,current.showPlanned]);
      if (signature !== next) {
        if (!ownChange || undoMode !== mode()) { previous = null; get('sitemap-undo').disabled = true; }
        signature = next;
        const list = entries();
        if (!list.some(([key])=>key===selected)) selected = list[0]?.[0] ?? null;
        options(get('sitemap-items'), list);
        get('sitemap-items').value = selected ?? '';
        get('sitemap-planned').checked = current.showPlanned;
        edit();
      }
      const colour = palette().roles.background;
      get('page-background-colour').value = colour;
      if (document.activeElement !== get('page-background-hex')) get('page-background-hex').value = colour;
      get('page-background-theme').textContent = `${state.theme === 'dark' ? 'Dark' : 'Light'} theme · ${colour}`;
      get('page-background-reset').disabled = !state.semanticOverrides?.[state.theme]?.background;
    }
    function commit(map, links, message, showPlanned = true) {
      const pages = map.flatMap(([label,children])=>[label,...children.map(child=>`${label} > ${child}`)]).join('\n');
      if (map.reduce((n,[,children])=>n+1+children.length,0)>64 || pages.length>8400) {
        selected = null;
        get('sitemap-status').textContent = 'Keep the sitemap within 64 entries and 8,400 characters.'; return false;
      }
      previous = normalizePlan(); undoMode = mode();
      state.designProcess = DSStudio.process.normalize({...plan(),pages,pageLinks:{...plan().pageLinks,[mode()]:links},showPlanned});
      signature = ''; ownChange = true;
      try { apply(); } finally { ownChange = false; }
      get('sitemap-undo').disabled = false;
      get('sitemap-status').textContent = message;
      return true;
    }
    const normalizePlan = () => DSStudio.process.normalize(plan());
    get('sitemap-items').addEventListener('change', event=>{selected=event.target.value; edit();});
    get('sitemap-new').addEventListener('click',()=>{selected=null; get('sitemap-items').selectedIndex=-1; edit(); get('sitemap-label').focus();});
    get('sitemap-form').addEventListener('submit',event=>{
      event.preventDefault();
      const label = get('sitemap-label').value.trim(), map = groups(), choice = decode(), parent = get('sitemap-parent').value;
      const invalid = !label || /[>\r\n]/.test(label) || map.some(([name,children],p)=>name===label && !(choice?.[0]===p && choice[1]<0) || children.some((name,c)=>name===label && !(choice?.[0]===p && choice[1]===c)));
      if (invalid || label.length>64) { get('sitemap-status').textContent = 'Use a unique label of 1–64 characters without > or line breaks.'; return; }
      const [p,c] = choice || [-1,-1], old = choice ? c<0 ? map[p][0] : map[p][1][c] : null;
      if (choice && c<0 && map[p][1].length && parent!=='') { get('sitemap-status').textContent='Move this group’s children first; only two sitemap levels are supported.'; return; }
      const links = {...plan().pageLinks[mode()]}, target = get('sitemap-target').value;
      if (old) delete links[old];
      if (target!=='auto') links[label] = target==='planned' ? '' : target;
      // Remember the destination parent's identity before removing/reordering a group.
      const parentGroup = parent==='' ? null : map[Number(parent)];
      if (choice && c<0 && !parentGroup) { map[p][0]=label; selected=`${p}:-1`; }
      else if (choice && c>=0 && parentGroup===map[p]) { map[p][1][c]=label; }
      else {
        if (choice) { if(c<0) map.splice(p,1); else map[p][1].splice(c,1); }
        if (parentGroup) { parentGroup[1].push(label); selected=`${map.indexOf(parentGroup)}:${parentGroup[1].length-1}`; }
        else { map.push([label,[]]); selected=`${map.length-1}:-1`; }
      }
      if (commit(map,links,`Saved ${label}. Preview and HTML inspector updated.`)) get('sitemap-items').focus();
    });
    get('sitemap-delete').addEventListener('click',()=>{
      const choice=decode(); if(!choice)return;
      const [p,c]=choice,map=groups(),links={...plan().pageLinks[mode()]};
      const removed=c<0?[map[p][0],...map[p][1]]:[map[p][1][c]];
      removed.forEach(label=>delete links[label]);
      if(c<0)map.splice(p,1);else map[p][1].splice(c,1);
      selected=null; commit(map,links,`Deleted ${removed.length} ${removed.length===1?'entry':'entries'}. Undo is available.`); get('sitemap-items').focus();
    });
    for(const [id,delta] of [['sitemap-up',-1],['sitemap-down',1]])get(id).addEventListener('click',()=>{
      const choice=decode();if(!choice)return;
      const [p,c]=choice,map=groups(),list=c<0?map:map[p][1],index=c<0?p:c,next=index+delta;
      if(next<0||next>=list.length)return;
      [list[index],list[next]]=[list[next],list[index]];
      selected=c<0?`${next}:-1`:`${p}:${next}`;
      commit(map,{...plan().pageLinks[mode()]},'Sitemap order updated.',plan().showPlanned);
    });
    get('sitemap-planned').addEventListener('change',()=>commit(groups(),{...plan().pageLinks[mode()]},'Footer visibility updated.',get('sitemap-planned').checked));
    get('sitemap-undo').addEventListener('click',()=>{
      if(!previous)return;
      state.designProcess=previous;previous=null;signature='';apply();get('sitemap-undo').disabled=true;get('sitemap-status').textContent='Last sitemap change undone.';
    });
    function background(value) {
      if(!validHex(value))return;
      state.semanticOverrides={...state.semanticOverrides,[state.theme]:{...state.semanticOverrides?.[state.theme],background:value.toUpperCase()}};
      apply();
    }
    get('page-background-colour').addEventListener('input',event=>{get('page-background-hex').value=event.target.value.toUpperCase();background(event.target.value);});
    get('page-background-hex').addEventListener('input',event=>background(event.target.value));
    get('page-background-reset').addEventListener('click',()=>{if(state.semanticOverrides?.[state.theme])delete state.semanticOverrides[state.theme].background;apply();});
    for (const event of ['dss:reset','dss:imported']) document.addEventListener(event,()=>{previous=null;get('sitemap-undo').disabled=true;get('sitemap-status').textContent='';signature='';sync();});
    const previousRender=renderCode;
    renderCode=function(){previousRender();sync();};
    sync();
  }
});
