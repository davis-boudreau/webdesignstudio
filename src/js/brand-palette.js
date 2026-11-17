'use strict';
/* Project brand references stay separate from the three main UI colour roles.
   Choosing a swatch copies its HEX; changing a reference is a separate decision. */
(() => {
  const roles = { primary: 'Primary UI colour', secondary: 'Supporting colour', accent: 'Accent colour' };
  const get = id => document.getElementById(id);
  const cards = new Map();
  let targetRole = 'primary';
  function defaults() {
    return ['primary', 'accent'].flatMap(group => EXAMPLE_PALETTE[group].map(([name, hex]) => ({
      id: group === 'primary' ? name === 'Deep blue' ? 'blue' : name.toLowerCase().replaceAll(' ', '-') : 'accent-' + name.toLowerCase().replaceAll(' ', '-'),
      name, hex, group
    })));
  }
  function normalize(raw) {
    if (!Array.isArray(raw)) return defaults();
    const seen = new Set(), result = [];
    for (const item of raw.slice(0, 24)) {
      if (!item || typeof item !== 'object' || typeof item.id !== 'string' || !/^[a-z][a-z0-9-]{0,39}$/.test(item.id) || seen.has(item.id) ||
        typeof item.hex !== 'string' || !/^#[0-9a-f]{6}$/i.test(item.hex)) continue;
      seen.add(item.id);
      result.push({ id: item.id, name: typeof item.name === 'string' && item.name.trim() ? item.name.trim().slice(0, 40) : item.id,
        hex: item.hex.toUpperCase(), group: item.group === 'primary' ? 'primary' : 'accent' });
    }
    return result.length ? result : defaults();
  }
  function render() {
    const container = get('brandSwatches');
    const items = normalize(state.brandPalette);
    get('brandApplyRole').value = targetRole;
    for (const [id, card] of cards) if (!items.some(item => item.id === id)) { card.remove(); cards.delete(id); }
    for (const [index, item] of items.entries()) {
      let card = cards.get(item.id);
      if (!card) {
        card = document.createElement('article'); card.className = 'brand-swatch'; card.dataset.brandSwatch = item.id;
        card.innerHTML = '<button type="button" class="brand-swatch-apply"><span class="brand-swatch-color" aria-hidden="true"></span><span class="brand-swatch-info"><strong></strong><code></code><span class="brand-swatch-action"></span></span><span class="brand-swatch-usage" data-brand-usage></span></button>';
        cards.set(item.id, card);
      }
      if (container.children[index] !== card) container.insertBefore(card, container.children[index] || null);
      const button = card.querySelector('button');
      button.dataset.brandRole = targetRole; button.dataset.brandHex = item.hex;
      button.setAttribute('aria-label', `Set ${roles[targetRole]} to ${item.name} (${item.hex})`);
      const usageId = `brandSwatchUsage-${item.id}`;
      card.querySelector('[data-brand-usage]').id = usageId;
      button.setAttribute('aria-describedby', usageId);
      card.querySelector('.brand-swatch-color').style.backgroundColor = item.hex;
      card.querySelector('strong').textContent = item.name;
      card.querySelector('code').textContent = item.hex;
      card.querySelector('.brand-swatch-action').textContent = `Set as ${roles[targetRole]}`;
      const assigned = Object.keys(roles).filter(role => state[role].toUpperCase() === item.hex);
      card.querySelector('[data-brand-usage]').textContent = assigned.length ? `Used for: ${assigned.map(role => roles[role]).join(', ')}` : 'Not assigned to the Main Palette';
      card.dataset.current = String(assigned.includes(targetRole));
    }
    for (const key of Object.keys(roles)) {
      const hex = state[key].toUpperCase(), item = items.find(item => item.hex === hex);
      get('brandCurrent' + key[0].toUpperCase() + key.slice(1)).textContent = `${item ? item.name : 'Custom colour'} · ${hex}`;
      get('brandRoleAssignments').querySelector(`[data-role-chip="${key}"]`).style.backgroundColor = hex;
    }
  }
  function assign(role, hex, feedbackId) {
    if (!Object.prototype.hasOwnProperty.call(roles, role) || !/^#[0-9a-f]{6}$/i.test(hex)) return;
    const input = get(role); input.value = hex; input.dispatchEvent(new Event('input', { bubbles: true }));
    const item = state.brandPalette.find(item => item.hex === hex.toUpperCase());
    get(feedbackId).textContent = `${roles[role]} set to ${item ? item.name : 'custom colour'} (${hex.toUpperCase()}) in properties. Save the assignment to update the project and preview; review contrast in both themes.`;
  }
  DSStudio.brandPalette = { defaults, normalize, render, css: items => normalize(items).map(item => `  --brand-${item.id}: ${item.hex};`).join('\n') };
  DSStudio.register({
    id: 'brand-palette', title: 'Brand and main palettes',
    init() {
      const editor = get('jBrandEditor'), rows = new Map(), drafts = new Map();
      let signature = '', stateIdentity, rowNumber = 0;
      function fields(row) {
        return Object.fromEntries(['name','id','hex'].map(key=>{const value=row.querySelector(`[data-brand-field="${key}"]`).value;return [key,key==='hex'?value.toUpperCase():value];}));
      }
      function restore(row, item) {
        for (const key of ['name','id','hex']) { const input=row.querySelector(`[data-brand-field="${key}"]`);input.value=item[key];input.setCustomValidity(''); }
        row.querySelector('code').textContent=`--brand-${item.id}: ${item.hex};`;
      }
      function draftStatus(row) {
        const dirty=drafts.has(row.dataset.brandId);
        row.querySelector('[data-brand-discard]').disabled=!dirty;
        row.querySelector('[data-brand-edit-status]').textContent=dirty?'Unsaved properties. Save this colour to update the project and preview.':'Properties saved. Preview shows the saved project.';
      }
      function sync() {
        const replaced = stateIdentity !== state; stateIdentity = state;
        if (replaced) drafts.clear();
        const items = state.brandPalette;
        const next = JSON.stringify(items);
        if (next !== signature || replaced) {
          signature = next;
          get('jBrandStatus').textContent = '';
          get('brandFeedback').textContent = 'Brand references updated. Choose a role, then click a swatch to apply its colour.';
          get('jBrandSwatches').replaceChildren(...items.map(item => {
            const li = document.createElement('li'), chip = document.createElement('span'), label = document.createElement('span');
            chip.className = 'brand-palette-chip'; chip.style.backgroundColor = item.hex; chip.setAttribute('aria-hidden', 'true');
            label.textContent = `${item.name} · --brand-${item.id} · ${item.hex}`;
            const token = document.createElement('code'); token.textContent = `--brand-${item.id}`;
            label.append(document.createElement('br'), token); li.append(chip, label); return li;
          }));
          for (const [id, row] of rows) if (!items.some(item => item.id === id)) { row.remove(); rows.delete(id); drafts.delete(id); }
          for (const [index, item] of items.entries()) {
            let row = rows.get(item.id);
            if (!row) {
              row = document.createElement('div'); row.className = 'brand-palette-row field'; row.dataset.brandId = item.id;
              const nameLabel = document.createElement('label'); nameLabel.textContent = 'Colour name';
              const name = document.createElement('input'); name.type = 'text'; name.maxLength = 40; name.dataset.brandField = 'name'; nameLabel.append(name);
              const tokenLabel = document.createElement('label'); tokenLabel.textContent = 'Token name suffix · --brand-';
              const token = document.createElement('input'); token.type = 'text'; token.maxLength = 40; token.pattern = '[a-z][a-z0-9-]{0,39}'; token.dataset.brandField = 'id'; tokenLabel.append(token);
              const colourLabel = document.createElement('label'); colourLabel.textContent = 'Colour';
              const colour = document.createElement('input'); colour.type = 'color'; colour.dataset.brandField = 'hex'; colourLabel.append(colour);
              const code = document.createElement('code');
              const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'ghost'; remove.dataset.removeBrand = item.id; remove.textContent = 'Remove colour';
              const shared=DSStudio.propertyActions.create({parent:row});shared.bar.classList.add('brand-palette-actions');
              const {save,discard,preview}=shared;save.dataset.brandSave='';discard.dataset.brandDiscard='';preview.dataset.brandPreview='';
              const status=document.createElement('p');status.className='help';status.id='brand-edit-status-'+(++rowNumber);status.dataset.brandEditStatus='';status.setAttribute('role','status');
              for(const input of [name,token,colour])input.setAttribute('aria-describedby',status.id);
              row.append(nameLabel, tokenLabel, colourLabel, code, shared.bar, status, remove); rows.set(item.id, row);
            }
            if (editor.children[index] !== row) editor.insertBefore(row, editor.children[index] || null);
            if(drafts.has(item.id) && drafts.get(item.id).base!==JSON.stringify(item))drafts.delete(item.id);
            if(!drafts.has(item.id))restore(row,item);
            draftStatus(row);
            row.querySelector('[data-brand-field="id"]').setAttribute('aria-label', `Token name suffix for ${item.name}`);
            row.querySelector('[data-brand-field="name"]').setAttribute('aria-label', `Name for brand colour ${index + 1}`);
            row.querySelector('[data-brand-field="hex"]').setAttribute('aria-label', `Colour for ${item.name}`);
            row.querySelector('[data-remove-brand]').disabled = items.length === 1;
            row.querySelector('[data-remove-brand]').dataset.removeBrand = item.id;
            row.querySelector('[data-remove-brand]').setAttribute('aria-label', `Remove ${item.name}`);
            row.querySelector('[data-brand-save]').setAttribute('aria-label',`Save ${item.name}`);
            row.querySelector('[data-brand-discard]').setAttribute('aria-label',`Discard edits for ${item.name}`);
          }
          for (const key of Object.keys(roles)) {
            get('j' + key[0].toUpperCase() + key.slice(1) + 'Brand').replaceChildren(new Option('Custom colour (use picker below)', ''), ...items.map(item => new Option(`${item.name} · --brand-${item.id} · ${item.hex}`, item.hex)));
          }
          get('brandAccent').replaceChildren(new Option('Custom accent colour', ''), ...items.filter(item => item.group === 'accent').map(item => new Option(`${item.name} · --brand-${item.id} · ${item.hex}`, item.hex)));
          get('jBrandAdd').disabled = items.length >= 24;
          get('jBrandCount').textContent = `${items.length} of 24 colours`;
        }
        for (const key of Object.keys(roles)) {
          const select = get('j' + key[0].toUpperCase() + key.slice(1) + 'Brand');
          select.value = items.some(item => item.hex === state[key].toUpperCase()) ? state[key].toUpperCase() : '';
        }
        get('brandAccent').value = items.some(item => item.group === 'accent' && item.hex === state.accent.toUpperCase()) ? state.accent.toUpperCase() : '';
        render();
      }
      function changed(message) {
        sync(); apply(); window.dssAutosave?.(); get('jBrandStatus').textContent = message;
      }
      for (const key of Object.keys(roles)) {
        get('j' + key[0].toUpperCase() + key.slice(1) + 'Brand').addEventListener('change', event => {
          if (!/^#[0-9a-f]{6}$/i.test(event.target.value)) { sync(); return; }
          assign(key, event.target.value, 'jBrandStatus');
        });
      }
      function edit(event) {
        const input = event.target.closest('[data-brand-field]'); if (!input) return;
        const row=input.closest('[data-brand-id]'),id=row.dataset.brandId,item=state.brandPalette.find(item=>item.id===id);
        if(!item)return;
        input.setCustomValidity('');
        if (input.dataset.brandField === 'id') {
          const value = input.value;
          if (!/^[a-z][a-z0-9-]{0,39}$/.test(value) || state.brandPalette.some(item=>item.id!==id && item.id===value)) {
            input.setCustomValidity('Use a unique suffix of 1–40 lowercase letters, digits or hyphens, starting with a letter.');
            if(event.type==='change')input.reportValidity();
          }
        }
        const next=fields(row),dirty=['name','id','hex'].some(key=>next[key]!==item[key]);
        if(dirty)drafts.set(id,{base:JSON.stringify(item)});else drafts.delete(id);
        row.querySelector('code').textContent=`--brand-${next.id}: ${next.hex.toUpperCase()};`;draftStatus(row);
      }
      editor.addEventListener('input', edit); editor.addEventListener('change', edit);
      editor.addEventListener('click', event => {
        const row=event.target.closest('[data-brand-id]');
        if(event.target.closest('[data-brand-preview]'))return;
        if(event.target.closest('[data-brand-discard]')){
          const item=state.brandPalette.find(item=>item.id===row.dataset.brandId);if(!item)return;
          drafts.delete(item.id);restore(row,item);draftStatus(row);row.querySelector('[data-brand-field="name"]').focus();return;
        }
        if(event.target.closest('[data-brand-save]')){
          const id=row.dataset.brandId,item=state.brandPalette.find(item=>item.id===id),next=fields(row);if(!item)return;
          if(!drafts.has(id))return;
          const token=row.querySelector('[data-brand-field="id"]');
          token.setCustomValidity(/^[a-z][a-z0-9-]{0,39}$/.test(next.id) && !state.brandPalette.some(other=>other.id!==id && other.id===next.id)?'':'Use a unique suffix of 1–40 lowercase letters, digits or hyphens, starting with a letter.');
          if(!token.reportValidity())return;
          if(!next.name.trim()){const name=row.querySelector('[data-brand-field="name"]');name.setCustomValidity('Enter a colour name.');name.reportValidity();return;}
          if(!/^#[0-9a-f]{6}$/i.test(next.hex))return;
          drafts.delete(id);
          if(next.id!==id){rows.delete(id);rows.set(next.id,row);row.dataset.brandId=next.id;}
          state.brandPalette=normalize(state.brandPalette.map(other=>other.id===id?{...other,...next}:other));
          restore(row,state.brandPalette.find(saved=>saved.id===next.id));draftStatus(row);
          changed('Brand colour saved. Existing UI anchors keep their copied colours.');return;
        }
        const button = event.target.closest('[data-remove-brand]'); if (!button || state.brandPalette.length <= 1) return;
        state.brandPalette = state.brandPalette.filter(item => item.id !== button.dataset.removeBrand);
        changed('Brand colour removed. Existing Main Palette choices keep their HEX values.'); get('jBrandAdd').focus();
      });
      get('jBrandAdd').addEventListener('click', () => {
        if (state.brandPalette.length >= 24) return;
        let index = 1; while (state.brandPalette.some(item => item.id === `colour-${index}`)) index++;
        const id = `colour-${index}`;
        state.brandPalette = [...state.brandPalette, { id, name: `Brand colour ${index}`, hex: '#004780', group: 'accent' }];
        changed('Brand colour added. Set its name and colour.'); rows.get(id).querySelector('input').focus();
      });
      get('brandApplyRole').addEventListener('change', event => {
        targetRole = Object.prototype.hasOwnProperty.call(roles, event.target.value) ? event.target.value : 'primary';
        render(); get('brandFeedback').textContent = `Click a swatch to set ${roles[targetRole]}.`;
      });
      get('brandSwatches').addEventListener('click', event => {
        const button = event.target.closest('button[data-brand-hex]');
        if (button) assign(targetRole, button.dataset.brandHex, 'brandFeedback');
      });
      get('brandEditPalette').addEventListener('click', () => {
        document.querySelector('[data-journey-step="4"]').click();
        editor.closest('details').open = true;
        const input = editor.querySelector('input'); input.focus(); input.scrollIntoView({ block: 'center', behavior: 'instant' });
      });
      document.addEventListener('dss:reset', () => {
        targetRole = 'primary'; get('brandFeedback').textContent = 'Choose a role, then click a swatch below.';
      });
      DSStudio.on('foundation:updated', sync);
      DSStudio.brandPalette.proposedItems=()=>normalize(state.brandPalette.map(item=>{
        const row=rows.get(item.id);if(!drafts.has(item.id)||!row)return item;
        const next=fields(row);
        return next.name.trim() && /^[a-z][a-z0-9-]{0,39}$/.test(next.id) && !state.brandPalette.some(other=>other.id!==item.id && other.id===next.id) && validHex(next.hex)?{...item,...next}:item;
      }));
      DSStudio.brandPalette.hasDrafts=()=>drafts.size>0;
      sync();
    }
  });
})();
