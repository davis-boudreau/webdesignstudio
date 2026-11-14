'use strict';
/* Project codec: defaults, legacy field migration, validation and JSON snapshots.
   These functions never read controls, mutate the active project or render views.
   Feature normalizers below are also data-only services. */
(() => {
  const clamp = (value, min, max) => Math.min(max, Math.max(min, value));
  const validHex = value => typeof value === 'string' && /^#[0-9a-f]{6}$/i.test(value);
  const SEMANTIC_COLOUR_KEYS = ['background', 'header-background', 'main-background', 'footer-background', 'surface', 'surface-muted', 'text', 'text-muted', 'border', 'control-border', 'primary', 'on-primary', 'primary-hover', 'secondary', 'on-secondary', 'accent', 'on-accent', 'success', 'warning', 'danger', 'focus'];
  const BACKGROUND_REGIONS = ['body', 'header', 'main', 'footer'];
  const PADDING_REGIONS = ['header', 'main', 'footer'];
  const PADDING_SIDES = ['top', 'right', 'bottom', 'left'];
  const BUTTON_VARIANTS = ['primary', 'secondary', 'accent', 'outline', 'text'];
  const BUTTON_STATES = ['default', 'hover', 'focus', 'active', 'selected', 'disabled', 'loading'];
  const advancedFields = {
    state: { values: ['default', 'hover', 'focus', 'active', 'disabled', 'selected', 'invalid', 'success', 'readonly', 'loading'] },
    focus: { min: 2, max: 6 }, height: { min: 34, max: 64 },
    weight: { values: [600, 700, 800] }, measure: { min: 40, max: 85 },
    tracking: { min: -5, max: 10 }, border: { min: 1, max: 4 },
    shadow: { values: ['none', 'subtle', 'medium', 'strong'] },
    opacity: { min: 20, max: 100 }, columns: { min: 150, max: 320 },
    gap: { min: 4, max: 32 }, align: { values: ['start', 'center', 'stretch'] },
    reduce: { boolean: true }, underline: { boolean: true }, motion: { min: 0, max: 500 }
  };

  function foundationDefaults() {
    return {
      project: 'My Project',
      theme: 'light',
      sampleMode: 'basic',
      method: 'oklch',
      primary: '#004780',
      secondary: '#495965',
      accent: '#cbdb2a',
      brandPalette: DSStudio.brandPalette.defaults(),
      designProcess: DSStudio.process.defaults(),
      responsiveDesign: DSStudio.responsive.defaults(),
      font: 'Arial, Helvetica, sans-serif',
      fontSettings: DSStudio.fonts.defaults(),
      base: 16,
      ratio: 1.2,
      leading: 1.55,
      headingLeading: 1.18,
      headingTracking: -.02,
      bodyTracking: 0,
      spacing: 4,
      radius: 12
    };
  }

  function advancedDefaults() {
    return {
      state: 'default',
      focus: 3,
      height: 48,
      weight: 700,
      measure: 65,
      tracking: -2,
      border: 1,
      shadow: 'none',
      opacity: 100,
      columns: 210,
      gap: 24,
      align: 'stretch',
      reduce: false,
      underline: true,
      motion: 150,
      colors: {
        success: '#15803D',
        warning: '#A85C00',
        danger: '#B91C1C',
        focus: '#9D5700'
      }
    };
  }

  function buttonDefaults() {
    return {
      variant: 'primary',
      size: 'md',
      selectedState: 'default',
      padX: 16,
      padY: 8,
      minHeight: 48,
      radius: 8,
      border: 1,
      weight: 600,
      focus: '#B86C20',
      focusWidth: 3,
      motion: 150,
      mobileFull: false,
      overrides: {},
      sources: {
        primary: 'primary',
        secondary: 'secondary',
        accent: 'accent',
        outline: 'primary',
        text: 'primary'
      },
      custom: {}
    };
  }

  function clampDefaults() {
    return {
      minWidth: 375,
      maxWidth: 1280,
      mobileFactor: .82
    };
  }

  function normalizeAdvanced(value, headingTracking) {
    const next = advancedDefaults();
    const raw = value && typeof value === 'object' && !Array.isArray(value) ? value : {};
    for (const [key, rule] of Object.entries(advancedFields)) {
      const v = raw[key];
      if (rule.values) {
        if (rule.values.includes(v)) next[key] = v;
      } else if (rule.boolean) {
        if (typeof v === 'boolean') next[key] = v;
      } else if (typeof v === 'number' && Number.isFinite(v)) {
        next[key] = clamp(v, rule.min, rule.max);
      }
    }
    for (const key of Object.keys(next.colors))
      if (validHex(raw.colors?.[key])) next.colors[key] = raw.colors[key].toUpperCase();
    next.tracking = headingTracking * 100;
    return next;
  }

  function clampNumber(v, min, max, fallback) {
    v = Number(v);
    return Number.isFinite(v) ? Math.max(min, Math.min(max, v)) : fallback;
  }

  function normalizeButtons(raw) {
    const defaults = buttonDefaults();
    const b = buttonDefaults();
    if (!raw || typeof raw !== 'object') return b;
    for (const [k, lo, hi] of [
        ['padX', 8, 36],
        ['padY', 6, 22],
        ['minHeight', 36, 64],
        ['radius', 0, 28],
        ['border', 1, 4],
        ['focusWidth', 2, 5],
        ['motion', 0, 350]
      ]) b[k] = clampNumber(raw[k], lo, hi, defaults[k]);
    b.weight = [400, 500, 600, 700].includes(Number(raw.weight)) ? Number(raw.weight) : 600;
    b.variant = BUTTON_VARIANTS.includes(raw.variant) ? raw.variant : 'primary';
    b.size = ['sm', 'md', 'lg'].includes(raw.size) ? raw.size : 'md';
    b.selectedState = BUTTON_STATES.includes(raw.selectedState) ? raw.selectedState : 'default';
    b.focus = validHex(raw.focus) ? raw.focus : defaults.focus;
    b.mobileFull = raw.mobileFull === true;
    for (const k of BUTTON_VARIANTS) {
      const source = raw.sources?.[k];
      if (['primary', 'secondary', 'accent', 'custom'].includes(source) || validHex(source)) b.sources[k] = source;
      if (validHex(raw.custom?.[k])) b.custom[k] = raw.custom[k];
      const item = raw.overrides?.[k];
      if (item && typeof item === 'object') {
        b.overrides[k] = {};
        for (const prop of ['hover', 'active', 'text', 'hoverText', 'activeText', 'bg', 'border'])
          if (validHex(item[prop])) b.overrides[k][prop] = item[prop];
      }
    }
    return b;
  }

  function normalize(obj) {
    if (!obj || typeof obj !== 'object' || Array.isArray(obj)) throw Error('Not a valid project configuration');
    const n = foundationDefaults();
    for (const k of ['primary', 'secondary', 'accent'])
      if (validHex(obj[k])) n[k] = obj[k].toLowerCase();
    if (['light', 'dark'].includes(obj.theme)) n.theme = obj.theme;
    if (['basic', 'advanced'].includes(obj.sampleMode)) n.sampleMode = obj.sampleMode;
    // Projects predating sample selection used the Advanced page.
    if (!Object.hasOwn(obj, 'sampleMode')) n.sampleMode = 'advanced';
    if (['mix', 'oklch'].includes(obj.method)) n.method = obj.method;
    if (['Arial, Helvetica, sans-serif', "Georgia, 'Times New Roman', serif", 'Verdana, Geneva, sans-serif', 'system-ui, sans-serif'].includes(obj.font)) n.font = obj.font;
    n.fontSettings = DSStudio.fonts.normalize(obj.fontSettings);
    n.brandPalette = DSStudio.brandPalette.normalize(obj.brandPalette);
    n.designProcess = DSStudio.process.normalize(obj.designProcess);
    n.responsiveDesign = DSStudio.responsive.normalize(obj.responsiveDesign);
    for (const [k, min, max] of [
        ['base', 14, 22],
        ['ratio', 1.05, 1.5],
        ['leading', 1.3, 1.9],
        ['headingLeading', 1, 1.6],
        ['headingTracking', -.05, .1],
        ['bodyTracking', -.02, .12],
        ['spacing', 3, 8],
        ['radius', 0, 28]
      ])
      if (typeof obj[k] === 'number' && Number.isFinite(obj[k])) n[k] = clamp(obj[k], min, max);
    if (typeof obj.project === 'string') n.project = obj.project.slice(0, 90);
    // Older projects stored heading tracking in hundredths of an em.
    if (typeof obj.headingTracking !== 'number' && typeof obj.advanced?.tracking === 'number' && Number.isFinite(obj.advanced.tracking))
      n.headingTracking = clamp(obj.advanced.tracking / 100, -.05, .1);
    const clampConfig = clampDefaults();
    for (const [key, min, max] of [
        ['minWidth', 320, 600],
        ['maxWidth', 900, 1600],
        ['mobileFactor', .7, 1]
      ]) {
      const value = obj.clampConfig?.[key];
      if (typeof value === 'number' && Number.isFinite(value)) clampConfig[key] = clamp(value, min, max);
    }
    n.semanticOverrides = { light: {}, dark: {} };
    n.regionPadding = {};
    for (const region of PADDING_REGIONS) {
      const sides = {};
      for (const side of PADDING_SIDES) {
        const value = obj.regionPadding?.[region]?.[side];
        if (typeof value === 'number' && Number.isFinite(value)) sides[side] = Math.round(clamp(value, 0, 64));
      }
      if (Object.keys(sides).length) n.regionPadding[region] = sides;
    }
    n.backgroundOpacity = { light: {}, dark: {} };
    for (const theme of ['light', 'dark']) for (const region of BACKGROUND_REGIONS) {
      const value = obj.backgroundOpacity?.[theme]?.[region];
      if (typeof value === 'number' && Number.isFinite(value)) n.backgroundOpacity[theme][region] = Math.round(clamp(value, 0, 100));
    }
    for (const theme of ['light', 'dark'])
      for (const key of SEMANTIC_COLOUR_KEYS)
        if (validHex(obj.semanticOverrides?.[theme]?.[key])) n.semanticOverrides[theme][key] = obj.semanticOverrides[theme][key].toUpperCase();
    n.advanced = normalizeAdvanced(obj.advanced, n.headingTracking);
    n.buttonDesign = normalizeButtons(obj.buttonDesign);
    return { state: n, clampConfig };
  }

  function defaults() {
    // New/reset projects omit optional override maps, as historical resets did.
    // Imports still normalize those maps independently of the default factory.
    return {
      state: { ...foundationDefaults(), advanced: advancedDefaults(), buttonDesign: buttonDefaults() },
      clampConfig: clampDefaults()
    };
  }

  function configuration(foundation, clampConfig) {
    const { advanced, ...values } = foundation;
    return {
      schemaVersion: 2.9,
      brandReference: 'Project Brand Palette',
      clampConfig: { ...clampConfig },
      ...values,
      advanced
    };
  }

  function snapshot(foundation, clampConfig) {
    // A detached snapshot is safe for browser-local persistence and callers.
    return JSON.parse(JSON.stringify(configuration(foundation, clampConfig)));
  }

  function serialize(foundation, clampConfig) {
    return JSON.stringify(configuration(foundation, clampConfig), null, 2);
  }

  DSStudio.project = { defaults, normalize, snapshot, serialize,
    advancedDefaults, advancedFields, buttonDefaults, normalizeButtons, clampDefaults,
    semanticColourKeys: SEMANTIC_COLOUR_KEYS, backgroundRegions: BACKGROUND_REGIONS,
    paddingRegions: PADDING_REGIONS, paddingSides: PADDING_SIDES };
})();
