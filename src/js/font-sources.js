'use strict';
/* Curated font sources: imported projects select IDs, never arbitrary URLs/CSS.
   Loaded before core-state so validation and exports share the same catalogue. */
(() => {
  const sans = 'Arial, Helvetica, sans-serif';
  const serif = "Georgia, 'Times New Roman', serif";
  const systems = [['arial', 'Arial', sans], ['georgia', 'Georgia', serif],
    ['verdana', 'Verdana', 'Verdana, Geneva, sans-serif'], ['system', 'System UI', 'system-ui, sans-serif']];
  const catalogue = [
    { id: 'inter', family: 'Inter', fallback: sans, category: 'sans-serif' },
    { id: 'source-sans-3', family: 'Source Sans 3', fallback: sans, category: 'sans-serif' },
    { id: 'literata', family: 'Literata', fallback: serif, category: 'serif' }
  ];
  const weights = [400, 500, 600, 700, 800, 900];
  const defaults = () => ({ source: 'system', body: 'inter', heading: 'same', systemHeading: 'same', weights: [400, 600, 700] });
  const validId = id => catalogue.some(font => font.id === id);
  function normalize(value) {
    const next = defaults();
    if (!value || typeof value !== 'object' || Array.isArray(value)) return next;
    if (value.source === 'google') next.source = 'google';
    if (validId(value.body)) next.body = value.body;
    if (value.heading === 'same' || validId(value.heading)) next.heading = value.heading;
    if (value.systemHeading === 'same' || systems.some(([id]) => id === value.systemHeading)) next.systemHeading = value.systemHeading;
    if (Array.isArray(value.weights)) next.weights = weights.filter(weight => value.weights.includes(weight));
    return next;
  }
  const settings = () => normalize(state.fontSettings);
  const bodyFont = config => catalogue.find(font => font.id === config.body);
  const headingFont = config => config.heading === 'same' ? bodyFont(config) : catalogue.find(font => font.id === config.heading);
  let fallback = false;
  function resolve(useFallback = false) {
    const config = settings();
    if (config.source === 'system') return {
      body: state.font,
      heading: config.systemHeading === 'same' ? state.font : systems.find(([id]) => id === config.systemHeading)[2]
    };
    const stack = font => useFallback ? font.fallback : `"${font.family}", ${font.fallback}`;
    return { body: stack(bodyFont(config)), heading: stack(headingFont(config)) };
  }
  const requiredWeights = () => [...new Set([400, 600, 700, Number(adv.weight), Number(state.buttonDesign?.weight || 600)])]
    .filter(weight => weights.includes(weight)).sort((a, b) => a - b);
  const selectedWeights = () => [...new Set([...settings().weights, ...requiredWeights()])].sort((a, b) => a - b);
  function families() {
    const config = settings();
    const entries = new Map();
    for (const font of [bodyFont(config), headingFont(config)]) entries.set(font.family, font);
    return [...entries.values()];
  }
  function url() {
    const config = settings();
    if (config.source !== 'google') return '';
    const normal = selectedWeights();
    const queries = families().map(font => {
      // Body copy includes the italic cite in the sample; heading-only families need normal styles.
      const styles = font.id === config.body ? `ital,wght@${normal.map(weight => `0,${weight}`).join(';')};1,400` : `wght@${normal.join(';')}`;
      return `family=${font.family.replaceAll(' ', '+')}:${styles}`;
    });
    return 'https://fonts.googleapis.com/css2?' + queries.join('&') + '&display=swap';
  }
  function htmlLinks() {
    const href = url();
    return href ? `  <!-- Google Fonts: requested weights, italic body copy and swap loading. -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="${href.replaceAll('&', '&amp;')}">
` : '';
  }
  function previewCss() {
    if (!fallback || settings().source !== 'google') return '';
    const fonts = resolve(true);
    return `\n/* Preview-only fallback comparison; exports keep the selected fonts. */\n:root { --font-body: ${fonts.body}; --font-heading: ${fonts.heading}; }\n`;
  }

  const documents = new WeakMap();
  function clearLinks(doc) {
    const previous = documents.get(doc);
    if (!previous) return;
    clearTimeout(previous.timer);
    for (const link of previous.links) { link.onload = link.onerror = null; link.remove(); }
    documents.delete(doc);
  }
  function status(kind, message) {
    const node = document.getElementById('fontLoadStatus');
    node.dataset.state = kind;
    if (node.textContent !== message) node.textContent = message;
    document.getElementById('fontRetry').hidden = kind !== 'error';
  }
  function syncLinks(doc, href, report = false) {
    const previous = documents.get(doc);
    if (previous?.url === href && (!href || previous.sheet.isConnected)) return;
    clearLinks(doc);
    if (!href) return;
    const record = { url: href, links: [] };
    documents.set(doc, record);
    const current = () => documents.get(doc) === record;
    const fail = () => {
      if (!current()) return;
      clearTimeout(record.timer);
      if (report) status('error', 'Google Fonts could not load. The page can use its system fallback fonts. Retry when connected.');
    };
    for (const host of ['https://fonts.googleapis.com', 'https://fonts.gstatic.com']) {
      const link = doc.createElement('link'); link.rel = 'preconnect'; link.href = host;
      if (host.includes('gstatic')) link.crossOrigin = 'anonymous';
      link.dataset.dssFont = ''; record.links.push(link); doc.head.append(link);
    }
    const link = doc.createElement('link'); link.rel = 'stylesheet'; link.href = href; link.dataset.dssFont = '';
    record.sheet = link; record.links.push(link);
    if (report) {
      status('loading', 'Loading selected Google Fonts; fallback text stays visible.');
      const selected = families();
      link.onload = async () => {
        try {
          const loaded = await Promise.all(selected.map(font => doc.fonts.load(`400 16px "${font.family}"`)));
          if (!current()) return;
          if (!loaded.every(faces => faces.length > 0 && faces.every(face => face.status === 'loaded'))) { fail(); return; }
          clearTimeout(record.timer);
          status('loaded', 'Google Fonts loaded: ' + selected.map(font => font.family).join(' + ') + '.');
        } catch { fail(); }
      };
      link.onerror = fail;
      record.timer = setTimeout(fail, 12000);
    }
    doc.head.append(link);
  }
  function syncPreview(doc) {
    syncLinks(doc, fallback ? '' : url());
  }
  DSStudio.fonts = { defaults, normalize, resolve, url, htmlLinks, previewCss, syncPreview,
    get showFallback() { return fallback; } };

  DSStudio.register({
    id: 'font-sources', title: 'Font sources and CDN learning',
    init() {
      const get = id => document.getElementById(id);
      for (const id of ['fontGoogleBody', 'fontGoogleHeading']) {
        const options = catalogue.map(font => new Option(`${font.family} (${font.category})`, font.id));
        if (id === 'fontGoogleHeading') options.unshift(new Option('Same as body', 'same'));
        get(id).replaceChildren(...options);
      }
      get('fontSystemHeading').replaceChildren(new Option('Same as body', 'same'), ...systems.map(([id, label]) => new Option(label, id)));
      function sync() {
        const config = settings(), google = config.source === 'google', fonts = resolve(fallback);
        document.documentElement.style.setProperty('--font-body', fonts.body);
        document.documentElement.style.setProperty('--font-heading', fonts.heading);
        get('fontSource').value = config.source;
        get('fontGoogleBody').value = config.body; get('fontGoogleHeading').value = config.heading;
        get('fontSystemHeading').value = config.systemHeading;
        get('fontGoogleOptions').hidden = !google; get('fontSystemOptions').hidden = google;
        for (const id of ['font', 'jFont']) get(id).disabled = google;
        get('fontFallback').disabled = !google; get('fontFallback').checked = fallback && google;
        const used = requiredWeights(), selected = selectedWeights();
        for (const weight of weights) {
          const checkbox = get('fontWeight' + weight);
          checkbox.checked = selected.includes(weight); checkbox.disabled = used.includes(weight);
        }
        get('fontWeightsHelp').textContent = `Page weights ${used.join(', ')} stay included. Add other weights for comparison. Italic 400 is included for the body cite.`;
        const html = htmlLinks() || '<!-- System fonts need no CDN stylesheet. -->';
        const css = `:root {\n  --font-body: ${resolve().body};\n  --font-heading: ${resolve().heading};\n  --font-ui: var(--font-body);\n}\nbody { font-family: var(--font-body); }\nh1, h2, h3 { font-family: var(--font-heading); }`;
        if (get('fontHtmlCode').textContent !== html) get('fontHtmlCode').textContent = html;
        if (get('fontCssCode').textContent !== css) get('fontCssCode').textContent = css;
        syncLinks(document, google && !fallback ? url() : '', true);
        if (!google) status('system', 'Using system fonts. No external font requests.');
        else if (fallback) status('fallback', 'Showing system fallbacks in previews. Saved choices and exports still use your Google Fonts.');
      }
      for (const [id, key] of [['fontSource', 'source'], ['fontGoogleBody', 'body'], ['fontGoogleHeading', 'heading'], ['fontSystemHeading', 'systemHeading']]) {
        get(id).addEventListener('change', event => {
          state.fontSettings = normalize({ ...settings(), [key]: event.target.value });
          if (key === 'source') fallback = false;
          apply();
        });
      }
      for (const weight of weights) get('fontWeight' + weight).addEventListener('change', () => {
        state.fontSettings = normalize({ ...settings(), weights: weights.filter(value => get('fontWeight' + value).checked) });
        apply();
      });
      get('fontFallback').addEventListener('change', event => { fallback = event.target.checked; renderCode(); });
      get('fontRetry').addEventListener('click', () => {
        clearLinks(document);
        const preview = get('previewPage').contentDocument;
        if (preview) clearLinks(preview);
        renderCode();
      });
      const previousImport = importConfig;
      importConfig = function(data) { fallback = false; return previousImport(data); };
      document.addEventListener('dss:reset', () => { fallback = false; });
      const previousRender = renderCode;
      renderCode = function() { sync(); previousRender(); };
      sync();
    }
  });
})();
