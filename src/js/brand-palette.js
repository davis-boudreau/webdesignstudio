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
    get(feedbackId).textContent = `${roles[role]} set to ${item ? item.name : 'custom colour'} (${hex.toUpperCase()}). Preview and generated CSS updated. Review contrast in both themes.`;
  }
  DSStudio.brandPalette = { defaults, normalize, render, css: items => normalize(items).map(item => `  --brand-${item.id}: ${item.hex};`).join('\n') };
  DSStudio.register({
    id: 'brand-palette', title: 'Brand and main palettes',
    init() {
      const editor = get('jBrandEditor'), rows = new Map();
      let signature = '';
      function sync() {
        const items = state.brandPalette;
        const next = JSON.stringify(items);
        if (next !== signature) {
          signature = next;
          get('jBrandStatus').textContent = '';
          get('brandFeedback').textContent = 'Brand references updated. Choose a role, then click a swatch to apply its colour.';
          get('jBrandSwatches').replaceChildren(...items.map(item => {
            const li = document.createElement('li'), chip = document.createElement('span'), label = document.createElement('span');
            chip.className = 'brand-palette-chip'; chip.style.backgroundColor = item.hex; chip.setAttribute('aria-hidden', 'true');
            label.textContent = `${item.name} · ${item.hex}`; li.append(chip, label); return li;
          }));
          for (const [id, row] of rows) if (!items.some(item => item.id === id)) { row.remove(); rows.delete(id); }
          for (const [index, item] of items.entries()) {
            let row = rows.get(item.id);
            if (!row) {
              row = document.createElement('div'); row.className = 'brand-palette-row field'; row.dataset.brandId = item.id;
              const nameLabel = document.createElement('label'); nameLabel.textContent = 'Colour name';
              const name = document.createElement('input'); name.type = 'text'; name.maxLength = 40; name.dataset.brandField = 'name'; nameLabel.append(name);
              const colourLabel = document.createElement('label'); colourLabel.textContent = 'Colour';
              const colour = document.createElement('input'); colour.type = 'color'; colour.dataset.brandField = 'hex'; colourLabel.append(colour);
              const code = document.createElement('code');
              const remove = document.createElement('button'); remove.type = 'button'; remove.className = 'ghost'; remove.dataset.removeBrand = item.id; remove.textContent = 'Remove colour';
              row.append(nameLabel, colourLabel, code, remove); rows.set(item.id, row);
            }
            if (editor.children[index] !== row) editor.insertBefore(row, editor.children[index] || null);
            for (const field of ['name', 'hex']) {
              const input = row.querySelector(`[data-brand-field="${field}"]`);
              if (document.activeElement !== input) input.value = item[field];
            }
            row.querySelector('code').textContent = item.hex;
            row.querySelector('[data-brand-field="name"]').setAttribute('aria-label', `Name for brand colour ${index + 1}`);
            row.querySelector('[data-brand-field="hex"]').setAttribute('aria-label', `Colour for ${item.name}`);
            row.querySelector('button').disabled = items.length === 1;
            row.querySelector('button').setAttribute('aria-label', `Remove ${item.name}`);
          }
          for (const key of Object.keys(roles)) {
            get('j' + key[0].toUpperCase() + key.slice(1) + 'Brand').replaceChildren(new Option('Custom colour (use picker below)', ''), ...items.map(item => new Option(`${item.name} · ${item.hex}`, item.hex)));
          }
          get('brandAccent').replaceChildren(new Option('Custom accent colour', ''), ...items.filter(item => item.group === 'accent').map(item => new Option(`${item.name} · ${item.hex}`, item.hex)));
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
        if (input.dataset.brandField === 'name' && event.type !== 'change') return;
        const id = input.closest('[data-brand-id]').dataset.brandId;
        const next = normalize(state.brandPalette.map(item => item.id === id ? { ...item, [input.dataset.brandField]: input.value } : item));
        if (JSON.stringify(next) === JSON.stringify(state.brandPalette)) return;
        state.brandPalette = next;
        input.value = state.brandPalette.find(item => item.id === id)[input.dataset.brandField];
        changed('Brand Palette updated. Choose a swatch again to apply its new colour to the Main Palette.');
      }
      editor.addEventListener('input', edit); editor.addEventListener('change', edit);
      editor.addEventListener('click', event => {
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
        document.querySelector('[data-journey-step="1"]').click();
        editor.closest('details').open = true;
        const input = editor.querySelector('input'); input.focus(); input.scrollIntoView({ block: 'center', behavior: 'instant' });
      });
      document.addEventListener('dss:reset', () => {
        targetRole = 'primary'; get('brandFeedback').textContent = 'Choose a role, then click a swatch below.';
      });
      const priorApply = apply;
      apply = function() { priorApply(); sync(); };
      sync();
    }
  });
})();
