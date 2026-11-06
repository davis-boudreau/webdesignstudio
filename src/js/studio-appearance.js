'use strict';
/* Browser preference only: never part of a project or generated website. */
(() => {
  const key = 'dss-studio-appearance';
  const valid = value => value === 'light' || value === 'dark';
  let mode = 'light';
  try {
    const stored = localStorage.getItem(key);
    if (valid(stored)) mode = stored;
  } catch { /* The Studio still works when browser storage is unavailable. */ }
  function render() {
    document.documentElement.dataset.theme = mode;
    document.documentElement.style.colorScheme = mode;
    const toggle = document.getElementById('themeToggle');
    toggle.textContent = `Studio: ${mode === 'dark' ? 'Dark' : 'Light'}`;
    toggle.setAttribute('aria-label', `Studio appearance: ${mode}. Switch to ${mode === 'dark' ? 'light' : 'dark'}.`);
    toggle.setAttribute('aria-pressed', String(mode === 'dark'));
  }
  render();
  DSStudio.register({
    id: 'studio-appearance', title: 'Independent Studio appearance',
    init() {
      document.getElementById('themeToggle').addEventListener('click', () => {
        mode = mode === 'dark' ? 'light' : 'dark';
        render();
        try { localStorage.setItem(key, mode); } catch { /* Session-only preference. */ }
      });
      window.addEventListener('storage', event => {
        if (event.storageArea !== localStorage || (event.key !== key && event.key !== null)) return;
        mode = valid(event.newValue) ? event.newValue : 'light';
        render();
      });
    }
  });
})();
