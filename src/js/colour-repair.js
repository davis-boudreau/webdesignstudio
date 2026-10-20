'use strict';
/* Preview edits against a copied project. Only Apply writes to the studio. */
(() => {
  const get = id => document.getElementById(id);
  const dialog = get('colourRepair');
  const tools = window.dssContrastTools;
  if (!dialog || !tools) return;
  const esc = value => escapeHtml(String(value));
  const copy = value => JSON.parse(JSON.stringify(value));
  let session = null;

  function semanticTarget(theme, key) {
    return { type: 'semantic', theme, key, value: palette(theme).roles[key], label: `${theme === 'light' ? 'Light' : 'Dark'}: --${key}` };
  }

  function proposal(target, colour) {
    const foundation = copy(state);
    const settings = window.dssGetButtonContrastData().settings;
    if (target.type === 'semantic') {
      foundation.semanticOverrides = foundation.semanticOverrides || {};
      foundation.semanticOverrides[target.theme] = { ...foundation.semanticOverrides[target.theme], [target.key]: colour };
    } else if (target.type === 'anchor') foundation[target.key] = colour;
    else if (target.property === 'focus') settings.focus = colour;
    else settings.overrides[target.variant] = { ...settings.overrides[target.variant], [target.property]: colour };
    return tools.collect({ foundation, buttonSettings: settings });
  }

  function effects(before, after) {
    const prior = new Map(before.map(row => [row.id, row]));
    const changed = after.flatMap(row => {
      const old = prior.get(row.id);
      if (old && Math.abs(row.ratio - old.ratio) < 1e-8) return [];
      return [{ before: old, after: row }];
    });
    return {
      changed,
      improved: changed.filter(item => item.before && item.after.ratio > item.before.ratio),
      worsened: changed.filter(item => item.before && item.after.ratio < item.before.ratio),
      resolved: changed.filter(item => item.before?.status === 'review' && item.after.status === 'pass'),
      introduced: changed.filter(item => item.after.status === 'review' && item.before?.status !== 'review')
    };
  }

  function target() { return session.targets[Number(get('repairTarget').value)]; }

  function listChanges(items) {
    return items.length ? `<ul>${items.map(item => `<li>${esc(item.after.theme)} · ${esc(item.after.name)} · ${esc(item.after.state)} · ${esc(item.after.location)}: ${item.before ? item.before.ratio.toFixed(3) : 'new'} → ${item.after.ratio.toFixed(3)}:1 <small>(${item.after.threshold === null ? 'inactive exemption' : item.after.scope === 'required' ? 'required pair' : item.after.scope === 'conditional' ? 'conditional check' : 'potential use'})</small></li>`).join('')}</ul>` : '<p>None.</p>';
  }

  function preview() {
    const colour = get('repairHex').value.trim();
    if (!validHex(colour)) {
      get('repairApply').disabled = true;
      get('repairPreview').textContent = 'Enter a six-digit HEX colour, such as #137A39.';
      return;
    }
    get('repairPicker').value = colour.toLowerCase();
    get('repairApply').disabled = false;
    const before = tools.collect();
    const after = proposal(target(), colour);
    const change = effects(before, after);
    const oldPair = session.row && before.find(row => row.id === session.row.id);
    const newPair = session.row && after.find(row => row.id === session.row.id);
    const sample = newPair || after.find(row => row.targets.some(item => item.type === target().type && item.key === target().key && item.theme === target().theme));
    get('repairEffectStatus').textContent = `${change.resolved.length} required problems resolved; ${change.introduced.length} introduced. ${change.improved.length} ratios improve; ${change.worsened.length} worsen.`;
    get('repairPreview').innerHTML = `
      ${sample ? `<p><span class="contrast-example" style="color:${sample.fg};background:${sample.bg}">Sample Aa</span> ${esc(sample.theme)} · ${esc(sample.name)} · ${esc(sample.location)}</p>` : ''}
      ${oldPair && newPair ? `<p><strong>Selected pair: ${oldPair.ratio.toFixed(3)} → ${newPair.ratio.toFixed(3)}:1</strong> · target ${newPair.threshold ?? 'exempt'}${newPair.threshold ? ':1' : ''}. ${newPair.threshold && newPair.ratio >= newPair.threshold ? 'Pair target met.' : 'Review the pair and its category.'}</p>` : ''}
      <p>${change.improved.length} ratios improve; ${change.worsened.length} ratios worsen. <strong>${change.resolved.length} required problems resolved; ${change.introduced.length} required problems introduced.</strong> Both themes are included.</p>
      <details${change.introduced.length ? ' open' : ''}><summary>New required problems (${change.introduced.length})</summary>${listChanges(change.introduced)}</details>
      <details><summary>All improved pairs (${change.improved.length})</summary>${listChanges(change.improved)}</details>
      <details><summary>All worsened pairs (${change.worsened.length})</summary>${listChanges(change.worsened)}</details>
      <p class="help">A higher ratio is not automatically a better design. Conditional checks and potential uses remain separate from required problems. Only this model's named contexts are evaluated.</p>`;
  }

  function suggestions() {
    const selected = target();
    const original = selected.value;
    const [L, C, H] = rgbToOklch(original);
    const candidates = new Set(['#000000', '#FFFFFF']);
    for (const amount of [-.4, -.25, -.15, -.08, -.04, .04, .08, .15, .25, .4])
      candidates.add(oklchHex(clamp(L + amount, 0, 1), C, H));
    const before = tools.collect();
    const ranked = [...candidates].filter(colour => colour.toUpperCase() !== original.toUpperCase()).map(colour => {
      const after = proposal(selected, colour);
      const change = effects(before, after);
      const pair = session.row && after.find(row => row.id === session.row.id);
      return { colour, ...change, meets: pair?.threshold ? pair.ratio >= pair.threshold : true,
        distance: Math.abs(rgbToOklch(colour)[0] - L) };
    }).sort((a, b) => a.introduced.length - b.introduced.length || Number(b.meets) - Number(a.meets) || b.resolved.length - a.resolved.length || a.distance - b.distance);
    get('repairSuggestions').innerHTML = ranked.slice(0, 3).map(item => `<button type="button" class="repair-suggestion" data-suggest-colour="${item.colour}">
      <span class="repair-chip" style="background:${item.colour}" aria-hidden="true"></span><strong>Preview ${item.colour}</strong>
      <small>${item.resolved.length} required problems resolved; ${item.introduced.length} introduced${session.row?.threshold ? `; selected pair ${item.meets ? 'meets target' : 'below target'}` : ''}</small></button>`).join('');
  }

  function selectTarget() {
    const selected = target();
    get('repairHex').value = selected.value.toUpperCase();
    get('repairPicker').value = selected.value.toLowerCase();
    get('repairScope').textContent = selected.type === 'semantic' ?
      `Changes --${selected.key} in the ${selected.theme} theme only. This override stays fixed after palette-anchor edits; “Use generated colour” removes it.` :
      selected.type === 'anchor' ? 'Changes this palette anchor and its generated ramps in both themes. Fixed semantic and button overrides keep their own colours.' :
        'Changes this button setting across both themes. Colour overrides belong to the named variant; the focus colour is shared by all variants.';
    get('repairNotice').textContent = 'Preview only. Apply commits the change; Cancel keeps the current project.';
    preview();
    suggestions();
  }

  function open(targets, row = null) {
    if (!targets.length) return;
    session = { targets: copy(targets), row, revision: projectJson(), opener: document.activeElement };
    get('repairTitle').textContent = row ? `Edit colour: ${row.name}` : 'Edit semantic colour';
    get('repairTarget').replaceChildren(...targets.map((item, index) => new Option(item.label, index)));
    selectTarget();
    dialog.showModal();
    get('repairHex').focus();
  }

  window.dssOpenColourRepair = row => { if (row) open(row.targets, row); };
  get('repairTarget').addEventListener('change', selectTarget);
  get('repairPicker').addEventListener('input', () => { get('repairHex').value = get('repairPicker').value.toUpperCase(); preview(); });
  get('repairHex').addEventListener('input', preview);
  get('repairSuggestions').addEventListener('click', event => {
    const button = event.target.closest('[data-suggest-colour]');
    if (button) { get('repairHex').value = button.dataset.suggestColour; preview(); }
  });
  get('repairCancel').addEventListener('click', () => dialog.close());
  dialog.addEventListener('close', () => {
    const opener = session?.opener;
    session = null;
    if (opener?.isConnected && opener.getClientRects().length) opener.focus();
    else get('contrastSummary').focus();
  });
  get('repairApply').addEventListener('click', () => {
    const colour = get('repairHex').value.trim().toUpperCase();
    if (!validHex(colour)) return;
    if (projectJson() !== session.revision) {
      session.revision = projectJson();
      preview(); suggestions();
      get('repairNotice').textContent = 'The project changed while this preview was open. The effects have been recalculated; review them before applying again.';
      return;
    }
    const selected = target();
    if (selected.type === 'semantic') {
      state.semanticOverrides = { ...state.semanticOverrides, [selected.theme]: { ...state.semanticOverrides?.[selected.theme], [selected.key]: colour } };
      apply(); syncAdvanced();
    } else if (selected.type === 'anchor') {
      state[selected.key] = colour;
      syncControls(); apply();
    } else window.dssSetButtonContrastColour(selected.variant, selected.property, colour);
    dialog.close();
    syncEditor();
    announce(`Applied ${colour} to ${selected.label}.`);
  });

  function syncEditor() {
    const theme = get('semanticTheme').value, key = get('semanticRole').value;
    get('semanticCurrent').textContent = `${palette(theme).roles[key]} · ${state.semanticOverrides?.[theme]?.[key] ? 'custom override' : 'generated / base value'}`;
    get('semanticReset').disabled = !state.semanticOverrides?.[theme]?.[key];
    const guidedKey = get('jSemanticRole').value;
    const colour = palette(state.theme).roles[guidedKey];
    get('jSemanticCurrent').textContent = `${state.theme === 'dark' ? 'Dark' : 'Light'}: ${colour} · ${state.semanticOverrides?.[state.theme]?.[guidedKey] ? 'custom override' : 'generated / base value'}`;
    get('jSemanticSwatch').style.backgroundColor = colour;
    get('jSemanticHelp').textContent = roleDescriptions[guidedKey][1];
    get('jSemanticReset').disabled = !state.semanticOverrides?.[state.theme]?.[guidedKey];
  }
  const roleDescriptions = {
    background: ['Page background', 'The canvas behind the page content.'],
    surface: ['Surface', 'Cards, header, footer and form surfaces.'],
    'surface-muted': ['Muted surface', 'Subtle grouped content and read-only fields.'],
    text: ['Body text', 'Default readable text on page and surface colours.'],
    'text-muted': ['Muted text', 'Secondary descriptions and supporting copy.'],
    border: ['Decorative border', 'Separators and card edges; form controls use a separate border.'],
    'control-border': ['Control border', 'Visible input and select boundaries.'],
    primary: ['Primary action', 'The main action and ordinary link colour. Button wizard settings can override component colours.'],
    'on-primary': ['Text on primary', 'Text placed on the primary action background.'],
    'primary-hover': ['Primary hover', 'The semantic primary action hover background.'],
    secondary: ['Supporting action', 'The supporting action background.'],
    'on-secondary': ['Text on supporting', 'Text placed on the supporting action background.'],
    accent: ['Accent', 'Highlights and the sample mobile menu icon.'],
    'on-accent': ['Text on accent', 'Text placed on the accent background.'],
    success: ['Success', 'Positive feedback; accompany meaning with words or an icon.'],
    warning: ['Warning', 'Caution feedback; accompany meaning with words or an icon.'],
    danger: ['Error / danger', 'Error feedback and invalid controls; explain the problem in text.'],
    focus: ['Keyboard focus', 'The semantic keyboard outline. Buttons and header navigation use the Button Design Wizard focus setting.']
  };
  get('jSemanticRole').replaceChildren(...SEMANTIC_COLOUR_KEYS.map(key => new Option(`${roleDescriptions[key][0]} (--${key})`, key)));
  get('jSemanticRole').value = 'text';
  get('jSemanticRole').addEventListener('change', syncEditor);
  get('jSemanticEdit').addEventListener('click', () => open([semanticTarget(state.theme, get('jSemanticRole').value)]));
  function resetRole(theme, key) {
    if (state.semanticOverrides?.[theme]) delete state.semanticOverrides[theme][key];
    apply(); syncAdvanced(); syncEditor();
    announce(`Restored the generated ${theme} --${key} colour.`);
  }
  get('jSemanticReset').addEventListener('click', () => resetRole(state.theme, get('jSemanticRole').value));
  get('semanticRole').replaceChildren(...SEMANTIC_COLOUR_KEYS.map(key => new Option(`--${key}`, key)));
  get('semanticRole').value = 'control-border';
  for (const id of ['semanticTheme', 'semanticRole']) get(id).addEventListener('change', syncEditor);
  get('semanticEdit').addEventListener('click', () => open([semanticTarget(get('semanticTheme').value, get('semanticRole').value)]));
  get('semanticReset').addEventListener('click', () => {
    const theme = get('semanticTheme').value, key = get('semanticRole').value;
    resetRole(theme, key);
  });
  get('semanticEditor').addEventListener('toggle', syncEditor);
  window.dssSyncSemanticEditor = syncEditor;
  document.addEventListener('dss:reset', syncEditor);
  document.addEventListener('dss:imported', syncEditor);
  syncEditor();
})();
