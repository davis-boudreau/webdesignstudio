'use strict';
/* V2.7: guided builder and browser-local project library.
localStorage stores JSON only. Never execute imported project content.
Browser storage may be unavailable in private or restricted contexts. */
(() => {
  const el = id => document.getElementById(id);
  const STORE = 'dss-v27-projects';
  let step = 0,
    activeId = null,
    projects = {};
  const bindings = {
    jProject: 'project',
    jPrimary: 'primary',
    jSecondary: 'secondary',
    jAccent: 'accent',
    jRamp: 'method',
    jFont: 'font',
    jBase: 'base',
    jRatio: 'ratio',
    jLeading: 'leading',
    jSpacing: 'spacing',
    jRadius: 'radius',
    jTheme: 'theme'
  };
  const numbers = new Set(['base', 'ratio', 'leading', 'spacing', 'radius']);

  function notify(message) {
    el('jSaveStatus').textContent = message;
  }

  function showStep(n) {
    step = Math.max(0, Math.min(5, n));
    document.querySelectorAll('[data-journey-pane]').forEach(p => p.hidden = Number(p.dataset.journeyPane) !== step);
    document.querySelectorAll('[data-journey-step]').forEach(b => {
      const i = Number(b.dataset.journeyStep);
      if (i === step) b.setAttribute('aria-current', 'step');
      else b.removeAttribute('aria-current');
      b.classList.toggle('is-complete', i < step)
    });
    el('jBack').disabled = step === 0;
    el('jNext').hidden = step === 5;
    el('jProgress').textContent = `Step ${step+1} of 6 · ${['Start','Palette','Typography','Components','Buttons','Deliver'][step]}`;
  }

  function syncJourney() {
    for (const [id, key] of Object.entries(bindings)) {
      const e = el(id);
      e.value = state[key];
      if (e.type === 'color') el(id + 'Out').textContent = String(state[key]).toUpperCase();
      if (['jBase', 'jRatio', 'jLeading', 'jSpacing', 'jRadius'].includes(id)) el(id + 'Out').textContent = state[key] + (['jBase', 'jSpacing', 'jRadius'].includes(id) ? 'px' : '');
    }
  }

  function serialize() {
    return {
      schemaVersion: 2.9,
      preset: 'custom',
      ...state,
      advanced: JSON.parse(JSON.stringify(adv))
    };
  }

  function persist() {
    try {
      localStorage.setItem(STORE, JSON.stringify(projects));
      return true;
    } catch (err) {
      notify('Browser storage unavailable or full. Download JSON instead.');
      return false;
    }
  }
  /* FIX: one autosave routine, also used by the theme toggle and the Button wizard (exposed below),
  so every kind of change is written to the active local project. */
  function autosave() {
    if (activeId && projects[activeId]) {
      projects[activeId].data = serialize();
      projects[activeId].updated = new Date().toISOString();
      if (persist()) notify('Changes saved locally to ' + projects[activeId].name + '.');
    }
  }
  window.dssAutosave = autosave;
  /* FIX: the theme select has no matching legacy control (there is no #theme element),
  so el('theme') was null and changing "Preview theme" crashed. Theme is now set directly. */
  function updateKey(key, value) {
    if (key === 'theme') {
      state.theme = value;
      apply();
    } else {
      const source = el(key);
      source.value = value;
      source.dispatchEvent(new Event('input', {
        bubbles: true
      }));
    }
    syncJourney();
    autosave();
  }
  for (const [id, key] of Object.entries(bindings)) el(id).addEventListener('input', e => updateKey(key, numbers.has(key) ? Number(e.target.value) : e.target.value));
  /* FIX: keep the guided fields in sync with every change (brand swatch buttons, theme toggle, JSON import, reset). */
  const prevApply = apply;
  apply = function() {
    prevApply();
    syncJourney();
  };
  el('jPreset').addEventListener('change', e => {
    if (e.target.value === 'example') {
      resetStudio('Example project restored.');
      notify('Example project restored. Save a project copy to keep your changes.');
    } else {
      activeId = null;
      notify('Custom project: change the parameters, then select Save project.');
    }
  });

  function refreshList() {
    const select = el('jProjects');
    select.replaceChildren();
    const entries = Object.entries(projects).sort((a, b) => String(b[1].updated).localeCompare(String(a[1].updated)));
    if (!entries.length) {
      select.add(new Option('No saved projects yet', ''));
      return;
    }
    for (const [id, p] of entries) select.add(new Option(p.name + ' · ' + new Date(p.updated).toLocaleDateString(), id));
    if (activeId && projects[activeId]) select.value = activeId;
  }

  function loadProject(id) {
    const p = projects[id];
    if (!p) return notify('Choose a saved project first.');
    try {
      importConfig(p.data);
      activeId = id;
      el('jPreset').value = 'custom';
      syncJourney();
      refreshList();
      notify('Loaded ' + p.name + ' from this browser.');
    } catch (err) {
      notify('Could not load project: ' + err.message);
    }
  }

  function saveProject() {
    const name = String(state.project || 'Untitled design system').trim().slice(0, 90) || 'Untitled design system';
    if (!activeId) {
      activeId = 'p-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 8);
    }
    projects[activeId] = {
      name,
      updated: new Date().toISOString(),
      data: serialize()
    };
    if (persist()) {
      refreshList();
      el('jPreset').value = 'custom';
      notify('Saved ' + name + ' in this browser. Export JSON for backup.');
    }
  }
  el('jSaveLocal').addEventListener('click', saveProject);
  el('jLoadLocal').addEventListener('click', () => loadProject(el('jProjects').value));
  el('jNewLocal').addEventListener('click', () => {
    resetStudio('New project started.');
    el('jPreset').value = 'custom';
    showStep(0);
    notify('New unsaved project. Choose settings, then Save project.');
  });
  el('jDeleteLocal').addEventListener('click', () => {
    const id = el('jProjects').value;
    if (!id || !projects[id]) return;
    if (!confirm('Delete this saved local project?')) return;
    delete projects[id];
    if (activeId === id) activeId = null;
    persist();
    refreshList();
    notify('Local project deleted.');
  });
  document.querySelectorAll('.readiness-item').forEach(box => box.addEventListener('change', () => {
    const count = document.querySelectorAll('.readiness-item:checked').length;
    el('readinessStatus').textContent = `${count} of 6 checks completed. These are self-reported, not automated accessibility tests.`;
  }));
  el('jBack').addEventListener('click', () => showStep(step - 1));
  el('jNext').addEventListener('click', () => showStep(step + 1));
  document.querySelectorAll('[data-journey-step]').forEach(b => b.addEventListener('click', () => showStep(Number(b.dataset.journeyStep))));
  el('jExportCss').addEventListener('click', () => download('design-system-tokens.css', cssExport(), 'text/css'));
  el('jExportJson').addEventListener('click', () => download('design-system-project.json', JSON.stringify(serialize(), null, 2), 'application/json'));
  el('jViewCss').addEventListener('click', () => {
    document.getElementById('studio-section-6')?.scrollIntoView({
      behavior: 'smooth',
      block: 'start'
    });
  });
  try {
    const saved = JSON.parse(localStorage.getItem(STORE) || '{}');
    if (saved && typeof saved === 'object' && !Array.isArray(saved)) projects = saved;
  } catch (err) {
    notify('Local storage unavailable. JSON export still works.');
  }
  /* Refresh journey fields when an advanced control changes state. */
  document.querySelectorAll('.studio-legacy input,.studio-legacy select').forEach(control => control.addEventListener('input', () => {
    syncJourney();
    autosave();
  }));
  el('themeToggle').addEventListener('click', autosave);
  /* FIX: only react to resets that actually happened (the old listener ran even when Reset was cancelled). */
  document.addEventListener('dss:reset', () => {
    activeId = null;
    el('jPreset').value = 'example';
  });
  /* FIX: replaces the old setTimeout(150) guess; fired after a JSON file has finished loading. */
  document.addEventListener('dss:imported', () => {
    activeId = null;
    el('jPreset').value = 'custom';
    syncJourney();
  });
  refreshList();
  syncJourney();
  showStep(0);
})();
