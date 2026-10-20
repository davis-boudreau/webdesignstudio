'use strict';
/* The guided button review consumes the contrast inventory, including its
   surface contexts, opacity, indicator targets and inactive exemptions. */
DSStudio.register({
  id: 'button-contrast',
  title: 'Button contrast review',
  init({ studio }) {
    const get = id => document.getElementById(id);
    const variants = { primary: 'Primary', secondary: 'Secondary', accent: 'Accent', outline: 'Outline', text: 'Text' };
    const states = { default: 'Default', hover: 'Hover', focus: 'Focus-visible', active: 'Active / pressed', selected: 'Selected toggle', disabled: 'Disabled', loading: 'Loading' };
    const themes = { light: 'Light', dark: 'Dark' };
    const kinds = { text: 'Text', focus: 'Focus ring', selection: 'Selection ring', inner: 'Inner selection edge', boundary: 'Boundary' };
    const hints = {
      default: 'Default text and background also apply to focus, selection, disabled and loading states.',
      hover: 'Hover underlines the label and has its own text and background colours for this variant.',
      active: 'Active / pressed adds a momentary inset cue and has its own text and background colours for this variant.',
      focus: 'Text uses the default colours. The focus ring colour is shared by every variant.',
      selected: 'A checkmark and ring show toggle selection. Keep the label unchanged and update aria-pressed in application code. The ring shares the global focus colour.',
      disabled: 'Ratios include disabled opacity and are informational. Edit the underlying default colours to change them.',
      loading: 'A progress indicator and Processing label show loading at full opacity. Busy alone does not mean disabled; application code must manage repeated actions and status announcements.'
    };
    const cells = new Map(), summaries = new Map(), pairs = new Map();
    let rows = [];

    // Build once: refreshes preserve disclosure state, keyboard focus and dialog
    // return targets while updating the existing text nodes and attributes.
    for (const [variant, label] of Object.entries(variants)) {
      const details = document.createElement('details');
      details.className = 'bd-review-variant';
      details.dataset.variant = variant;
      details.innerHTML = `<summary>${label} <small></small></summary>
        <table class="bd-review-table"><caption>${label}: all states in both themes</caption>
        <thead><tr><th scope="col">State</th><th scope="col">Light</th><th scope="col">Dark</th></tr></thead><tbody></tbody></table>`;
      summaries.set(variant, details.querySelector('small'));
      for (const [stateName, stateLabel] of Object.entries(states)) {
        const row = document.createElement('tr');
        row.innerHTML = `<th scope="row"><button type="button" data-review-variant="${variant}" data-review-state="${stateName}" aria-controls="bdReviewSelection">${stateLabel}</button></th><td data-review-theme="light"></td><td data-review-theme="dark"></td>`;
        cells.set(`${variant}:${stateName}`, row);
        details.querySelector('tbody').append(row);
      }
      get('bdReviewVariants').append(details);
    }
    for (const [theme, label] of Object.entries(themes)) {
      const section = document.createElement('section');
      section.className = 'bd-review-theme';
      section.setAttribute('aria-label', `${label} theme contrast`);
      section.innerHTML = `<h5>${label} theme</h5>`;
      for (const [kind, label] of Object.entries(kinds)) {
        const card = document.createElement('div');
        card.className = 'bd-review-pair';
        card.dataset.kind = kind;
        card.hidden = true;
        card.innerHTML = `<strong>${label}</strong><p class="bd-review-ratio"></p><p class="help bd-review-context"></p><button type="button" class="ghost">Edit colours</button>`;
        pairs.set(`${theme}:${kind}`, card);
        section.append(card);
      }
      get('bdReviewPairs').append(section);
    }

    const required = list => list.filter(row => row.scope === 'required' && row.threshold !== null);
    const worst = list => list.reduce((lowest, row) => !lowest || row.ratio < lowest.ratio ? row : lowest, null);
    const result = list => !required(list).length ? 'exempt' : required(list).some(row => row.status === 'review') ? 'review' : 'pass';
    const label = status => ({ pass: 'Pass', review: 'Review', exempt: 'Exempt' })[status];
    const kindOf = row => row.group === 'Button Laboratory: text' ? 'text' :
      row.name.includes('focus ring') ? 'focus' : row.name.includes('(outer)') ? 'selection' :
      row.name.includes('(inner)') ? 'inner' : 'boundary';
    const announce = (node, text) => { if (node.textContent !== text) node.textContent = text; };

    function refresh() {
      rows = window.dssGetContrastChecks().filter(row => row.group.startsWith('Button Laboratory:'));
      const settings = state.buttonDesign;
      const groups = new Map();
      for (const row of rows) {
        const variant = row.targets.find(target => target.type === 'button').variant;
        const key = `${variant}:${row.state}:${row.theme}`;
        if (!groups.has(key)) groups.set(key, []);
        groups.get(key).push(row);
      }
      const totals = { review: 0, pass: 0, exempt: 0 };
      for (const variant of Object.keys(variants)) {
        let review = 0;
        for (const stateName of Object.keys(states)) {
          const row = cells.get(`${variant}:${stateName}`);
          const button = row.querySelector('button');
          const selected = variant === settings.variant && stateName === settings.selectedState;
          if (selected) button.setAttribute('aria-current', 'true');
          else button.removeAttribute('aria-current');
          row.classList.toggle('is-selected', selected);
          const descriptions = [];
          for (const [theme, themeLabel] of Object.entries(themes)) {
            const status = result(groups.get(`${variant}:${stateName}:${theme}`) || []);
            const cell = row.querySelector(`[data-review-theme="${theme}"]`);
            cell.dataset.result = status;
            cell.textContent = label(status);
            descriptions.push(`${themeLabel}: ${label(status)}`);
            totals[status]++;
            if (status === 'review') review++;
          }
          button.setAttribute('aria-label', `Review ${variants[variant]} ${states[stateName]}. ${descriptions.join('. ')}`);
        }
        summaries.get(variant).textContent = review ? `${review} to review` : 'Targets met';
      }
      announce(get('bdReviewSummary'), `${Object.values(totals).reduce((sum, count) => sum + count, 0)} variant/state/theme combinations: ${totals.review} to review, ${totals.pass} pass, ${totals.exempt} disabled exemptions. Conditional checks are shown separately.`);
      get('bdReviewTitle').textContent = `${variants[settings.variant]} · ${states[settings.selectedState]}`;
      get('bdReviewHint').textContent = hints[settings.selectedState];
      const descriptions = [];
      for (const [theme, themeLabel] of Object.entries(themes)) {
        const list = groups.get(`${settings.variant}:${settings.selectedState}:${theme}`) || [];
        descriptions.push(`${themeLabel}: ${label(result(list))}`);
        for (const [kind, kindLabel] of Object.entries(kinds)) {
          const card = pairs.get(`${theme}:${kind}`);
          const row = worst(list.filter(row => kindOf(row) === kind));
          card.hidden = !row;
          if (!row) continue;
          const assessment = row.status === 'conditional' ? `Conditional: ${row.ratio >= row.threshold ? 'target met' : 'judge context'}` : label(row.status);
          card.dataset.result = row.status;
          card.querySelector('.bd-review-ratio').textContent = `${row.ratio.toFixed(3)}:1 · ${assessment}${row.threshold === null ? ' (no target)' : ` · target ${row.threshold}:1`}`;
          card.querySelector('.bd-review-context').textContent = `Lowest ratio on ${row.location}.`;
          const button = card.querySelector('button');
          button.dataset.buttonRepair = row.id;
          button.textContent = kind === 'focus' || kind === 'selection' || kind === 'inner' ? 'Edit shared ring colour' : kind === 'boundary' ? 'Edit boundary colours' : 'Edit text / background';
          button.setAttribute('aria-label', `${button.textContent}: ${variants[settings.variant]}, ${states[settings.selectedState]}, ${themeLabel}, ${kindLabel}`);
        }
      }
      announce(get('bdContrast'), descriptions.join(' · '));
    }

    get('bdReviewVariants').addEventListener('click', event => {
      const button = event.target.closest('[data-review-variant]');
      if (button) window.dssSelectButtonState(button.dataset.reviewVariant, button.dataset.reviewState);
    });
    get('bdReviewPairs').addEventListener('click', event => {
      const button = event.target.closest('[data-button-repair]');
      if (button) window.dssOpenColourRepair(rows.find(row => row.id === button.dataset.buttonRepair));
    });
    studio.on('contrast:updated', refresh);
    refresh();
  }
});
