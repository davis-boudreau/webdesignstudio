"""Dependency-free Chrome smoke tests. Run: python scripts/browser_review.py.

Uses a temporary browser profile and a local-only server; saved user projects
and the user's normal browser session are never opened.
"""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from html import unescape
from pathlib import Path
import json
import os
import re
import shutil
import subprocess
import tempfile
import threading

ROOT = Path(__file__).resolve().parent.parent
HARNESS = r'''<!doctype html><meta charset="utf-8"><title>Browser review</title>
<iframe id="app" style="width:1440px;height:1000px" src="/index.html"></iframe>
<pre id="results">RUNNING</pre><script>
app.onload = async () => {
  const w = app.contentWindow, d = w.document, results = [];
  const evaluate = code => w.eval(code);
  const test = (name, fn) => {
    try { if (!fn()) throw Error('Assertion failed'); results.push({name, pass:true}); }
    catch (e) { results.push({name, pass:false, error:String(e)}); }
  };
  const input = (id, value, type='input') => {
    const el=d.getElementById(id); el.value=value;
    el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  const reset = () => evaluate('resetStudio()');
  const saved = () => Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects')))[0].data;
  const wait = () => new Promise(resolve => setTimeout(resolve,100));
  test('No startup JavaScript errors', () => !w.__reviewErrors.length);
  test('Centre sections start collapsed', () => [...d.querySelectorAll('#main > .studio-section')].every(el=>!el.open));
  d.getElementById('expandSections').click(); await wait();
  test('Neutral CSS, JSON, and HTML exports', () => !/nscc/i.test(evaluate('cssExport()+projectJson()+htmlExport()')));
  test('Live inspector matches CSS export', () => d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  test('Every label points to a control', () => [...d.querySelectorAll('label[for]')].every(el=>d.getElementById(el.htmlFor)));
  test('Internal anchors resolve', () => [...d.querySelectorAll('a[href^="#"]')].every(el=>d.getElementById(el.hash.slice(1))));
  test('HTML IDs are unique', () => {
    const ids=[...d.querySelectorAll('[id]')].map(el=>el.id); return ids.length===new Set(ids).size;
  });
  for (const method of ['mix','oklch']) {
    input('method',method);
    test(method+' ramps preserve anchors and emit valid colours', () => evaluate(`
      ['primary','secondary','accent'].every(k=>{
        const ramp=makeRamp(state[k],state.method);
        return ramp[500]===state[k].toUpperCase() && Object.values(ramp).every(validHex);
      })`));
  }
  test('Known contrast ratios', () => evaluate("contrast('#000000','#FFFFFF')===21 && contrast('#FFFFFF','#FFFFFF')===1"));
  input('jTheme','dark');
  test('Dark theme and guided controls synchronize', () => d.documentElement.dataset.theme==='dark' && d.getElementById('jTheme').value==='dark');
  test('Dark theme exports both theme blocks', () => evaluate('cssExport().includes(\'[data-theme="dark"]\') && cssExport().includes("--background: #F3F6FA")'));
  reset();
  input('clampMinWidth',480); input('clampMaxWidth',1440); input('clampFactor',.7);
  const fluidCss=evaluate('fluidTypeCss(5)');
  const project=evaluate('projectJson()');
  test('Project JSON preserves responsive typography settings', () => {
    input('clampFactor',1); input('clampMinWidth',375); input('clampMaxWidth',1280);
    evaluate('importConfig('+project+')'); return evaluate('fluidTypeCss(5)')===fluidCss;
  });
  input('clampFactor',.7);
  reset();
  test('Reset restores responsive typography defaults', () => evaluate('JSON.stringify(clampConfig)===JSON.stringify(CLAMP_DEFAULTS)'));
  test('Import clamps numeric values and rejects executable font text', () => {
    evaluate('importConfig({base:1e10,ratio:-5,font:"Arial; color:red",project:"<img src=x onerror=alert(1)>"})');
    return evaluate('state.base===22 && state.ratio===1.05 && state.font===DEFAULT.font && !htmlExport().includes("<img")');
  });
  test('Malformed button variant safely falls back', () => {
    evaluate('importConfig({buttonDesign:{variant:"__proto__"}})');
    return evaluate('state.buttonDesign.variant')==='primary';
  });
  test('Imported clamp settings are finite and bounded', () => {
    evaluate('importConfig({clampConfig:{minWidth:-1,maxWidth:1e10,mobileFactor:2}})');
    return evaluate('clampConfig.minWidth===320 && clampConfig.maxWidth===1600 && clampConfig.mobileFactor===1');
  });
  reset();
  w.localStorage.clear(); d.getElementById('jSaveLocal').click();
  input('advWeight',600,'change');
  test('Advanced select changes autosave after state updates', () => saved().advanced.weight===600);
  d.getElementById('advUnderline').checked=false;
  d.getElementById('advUnderline').dispatchEvent(new w.Event('change',{bubbles:true}));
  test('Advanced checkbox changes autosave', () => saved().advanced.underline===false);
  input('clampBase',20);
  test('Clamp foundation changes autosave', () => saved().base===20);
  input('clampFactor',.7);
  test('Clamp settings autosave', () => saved().clampConfig?.mobileFactor===.7);
  const beforeImport=JSON.stringify(saved());
  test('Import does not overwrite the active saved project', () => {
    evaluate('importConfig({project:"Imported",base:18,advanced:{weight:800}})');
    return JSON.stringify(saved())===beforeImport;
  });
  test('Reset does not overwrite the active saved project', () => {
    reset(); return JSON.stringify(saved())===beforeImport;
  });
  input('bdRadius',18);
  test('Button settings round trip through JSON', () => {
    const json=evaluate('projectJson()'); reset(); evaluate('importConfig('+json+')');
    return evaluate('state.buttonDesign.radius')===18;
  });
  test('Heading weight round trips as a finite number', () => {
    input('advWeight',800,'change');
    const json=evaluate('projectJson()'); reset(); evaluate('importConfig('+json+')');
    return evaluate('adv.weight')===800;
  });
  reset();
  test('Default button focus contrasts with light and dark surfaces', () => evaluate("['#FFFFFF','#152236'].every(bg=>contrast(state.buttonDesign.focus,bg)>=3)"));
  input('bdSize','lg');
  test('Exported HTML preserves selected button size', () => evaluate('htmlExport().includes("ds-button--lg")'));
  input('jTheme','dark');
  test('Exported HTML preserves selected theme', () => evaluate('htmlExport().includes(\'data-theme="dark"\')'));
  const darkCss=evaluate('cssExport()');
  input('jTheme','light');
  test('Button CSS theme definitions are independent of active theme', () => evaluate('cssExport()')===darkCss);
  input('advAlign','center','change'); input('advOpacity',60);
  const exported=d.createElement('iframe');
  exported.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
  await new Promise(resolve=>{exported.onload=resolve;d.body.append(exported);});
  test('Exported card opacity matches controls', () => Number(exported.contentWindow.getComputedStyle(exported.contentDocument.querySelector('.card')).opacity)===.6);
  test('Exported grid alignment matches controls', () => exported.contentWindow.getComputedStyle(exported.contentDocument.querySelector('.card-grid')).alignItems==='center');
  test('Exported CSS contains no undefined or nonfinite values', () => !/undefined|NaN|Infinity/.test(evaluate('cssExport()')));
  exported.remove();
  d.getElementById('viewCss').click();
  d.getElementById('viewCss').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
  test('Code tabs support arrow-key selection and focus', () => d.activeElement.id==='viewJson' && d.getElementById('viewJson').getAttribute('aria-selected')==='true' && d.getElementById('viewCss').tabIndex===-1);
  test('Code tab panel is labelled by active tab', () => d.getElementById('codeView').getAttribute('aria-labelledby')==='viewJson');
  input('advState','loading','change');
  test('Loading demo exposes busy and disabled states', () => d.getElementById('advDemoButton').disabled && d.getElementById('advDemoButton').getAttribute('aria-busy')==='true');
  reset();
  input('jFont','Georgia, \'Times New Roman\', serif');
  test('Typography specimens use selected font', () => w.getComputedStyle(d.querySelector('#mobileType .sample')).fontFamily.includes('Georgia'));
  reset();
  for (const width of [320,390,768,1440]) {
    app.style.width=width+'px'; await wait();
    test('Page fits '+width+'px viewport', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  for (const [mode,width] of [['mobile',375],['tablet',768],['desktop',1280]]) {
    d.querySelector('button[data-width="'+mode+'"]').click(); await wait();
    test('Preview has exact '+mode+' width', () => Math.abs(d.getElementById('previewFrame').getBoundingClientRect().width-width)<1);
  }
  reset(); await wait();
  const report = () => w.dssGetContrastChecks();
  test('Contrast report covers both themes without changing the active theme', () => {
    return new Set(report().map(row=>row.theme)).size===2 && d.documentElement.dataset.theme==='light' && evaluate('state.theme')==='light';
  });
  test('Every button variant and state is represented in both themes', () => {
    return ['light','dark'].every(theme=>['primary','secondary','accent','outline','text'].every(variant=>
      ['default','hover','focus','active','selected','disabled','loading'].every(state=>report().some(row=>
        row.group==='Button Laboratory: text' && row.theme===theme && row.name.toLowerCase()===variant && row.state===state))));
  });
  test('Reference swatches and every generated ramp step have candidate checks', () => {
    const rows=report().filter(row=>row.scope==='candidate');
    return rows.length===(11+33)*2*2 && rows.every(row=>row.status==='candidate');
  });
  test('Disabled controls are exempt and read-only text is tested', () => report().filter(row=>row.state==='disabled').every(row=>row.status==='exempt') &&
    report().some(row=>row.name==='State Explorer input text' && row.state==='readonly' && row.threshold===4.5));
  test('Loading exemption follows the actual disabled state', () => {
    const rows=report().filter(row=>row.state==='loading');
    return rows.filter(row=>row.group==='Button Laboratory: text').every(row=>row.threshold===4.5) &&
      rows.filter(row=>row.name==='State Explorer button text').every(row=>row.status==='exempt');
  });
  test('Focus indicators have a separate non-text target', () => report().some(row=>row.name==='Primary focus ring' && row.threshold===3 && row.state==='focus'));
  const oldForeground=report().find(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light').fg;
  input('bdVariant','primary'); input('bdHoverText','#123456'); await wait();
  test('Button override updates the contrast inventory', () => report().some(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light' && row.fg==='#123456' && row.fg!==oldForeground));
  input('bdDefaultBg','#ffffff'); input('bdText','#ffffff'); await wait();
  test('White text on white is flagged at exactly 1:1', () => report().some(row=>row.name==='Primary' && row.state==='default' && row.ratio===1 && row.status==='review'));
  input('bdDefaultBg','#ffffff'); input('bdText','#777777'); await wait();
  test('A ratio below 4.5 is not rounded into a text pass', () => report().some(row=>row.name==='Primary' && row.state==='default' && row.ratio>4.4 && row.ratio<4.5 && row.status==='review'));
  input('bdDefaultBg','#000000'); input('bdText','#ffffff'); await wait();
  test('Disabled opacity uses unrounded sRGB compositing', () => {
    const row=report().find(row=>row.name==='Primary' && row.theme==='light' && row.state==='disabled' && row.location==='surface');
    const expected=1.05/(Math.pow((.45+.055)/1.055,2.4)+.05);
    return Math.abs(row.ratio-expected)<1e-10 && row.status==='exempt';
  });
  const beforeOpacity=report().find(row=>row.name==='Preview card: --text' && row.theme==='light').ratio;
  input('advOpacity',20); await wait();
  test('Surface opacity updates the composited contrast', () => report().find(row=>row.name==='Preview card: --text' && row.theme==='light').ratio<beforeOpacity);
  input('advColor_danger','#abcdef'); await wait();
  test('Feedback changes update invalid-state checks', () => report().some(row=>row.name==='State Explorer input border' && row.theme==='light' && row.state==='invalid' && row.fg==='#ABCDEF'));
  input('contrastTheme','dark','change'); input('contrastResult','review','change');
  test('Contrast theme and result filters apply together', () => {
    const shown=[...d.querySelectorAll('#contrastChecks tbody tr')];
    return shown.length>0 && shown.every(row=>row.dataset.status==='review' && row.cells[0].textContent==='Dark');
  });
  input('contrastTheme','all','change'); input('contrastResult','all','change'); input('contrastSort','ratio','change');
  test('Ratios sort ascending within each result group', () => [...d.querySelectorAll('#contrastChecks tbody')].every(body=>{
    const values=[...body.rows].map(row=>parseFloat(row.cells[3].textContent));return values.every((value,i)=>!i||value>=values[i-1]);
  }));
  input('contrastSearch','Primary focus ring');
  test('Search narrows the displayed contrast pairs', () => {
    const shown=[...d.querySelectorAll('#contrastChecks tbody tr')];
    return shown.length>0 && shown.every(row=>row.cells[1].textContent.includes('Primary focus ring'));
  });
  const realDownload=w.download; let contrastCsv;
  w.download=(name,content)=>{contrastCsv={name,content};};
  d.getElementById('contrastDownload').click(); w.download=realDownload;
  test('Contrast CSV exports the currently filtered list', () => contrastCsv.name==='contrast-checks.csv' && contrastCsv.content.includes('Primary focus ring') && !contrastCsv.content.includes('Swatch candidates:'));
  input('contrastSearch',''); input('contrastSort','priority','change');
  test('Default sorting puts review rows before passes within groups', () => [...d.querySelectorAll('#contrastChecks tbody')].every(body=>{
    const ranks={review:0,conditional:1,pass:2,candidate:3,exempt:4};const values=[...body.rows].map(row=>ranks[row.dataset.status]);
    return values.every((value,i)=>!i||value>=values[i-1]);
  }));
  app.style.width='320px';
  d.querySelector('#contrastChecks .contrast-group summary').click(); await wait();
  test('Expanded contrast table scrolls within a 320px page', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  test('Contrast report ratios are finite and between 1 and 21', () => report().every(row=>Number.isFinite(row.ratio) && row.ratio>=1 && row.ratio<=21));
  reset(); await wait();
  test('Optional feedback text is a potential use, not a required failure', () => report().filter(row=>row.name.includes('message text')).every(row=>row.scope==='potential' && row.status==='candidate'));
  test('Button boundaries and extra inner ring checks are conditional', () => report().filter(row=>row.group==='Button Laboratory: indicators' && (row.name.includes('boundary') || row.name.includes('(inner)'))).every(row=>row.status==='conditional'));
  test('Actual input boundaries remain required checks', () => report().some(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light' && row.status==='review'));
  const openRepair = predicate => {
    const row=report().find(predicate);
    const action=[...d.querySelectorAll('[data-edit-contrast]')].find(el=>el.dataset.editContrast===row.id);
    action.closest('details').open=true; action.click(); return row;
  };
  d.getElementById('jSaveLocal').click();
  const beforeRepair=evaluate('projectJson()'), beforeRepairCss=evaluate('cssExport()'), beforeRepairStorage=w.localStorage.getItem('dss-v27-projects');
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light');
  test('Edit action opens the relevant control-border editor', () => d.getElementById('colourRepair').open && d.getElementById('repairTarget').selectedOptions[0].textContent.includes('--control-border'));
  test('Repair provides three tested colour suggestions', () => d.querySelectorAll('[data-suggest-colour]').length===3);
  d.querySelector('[data-suggest-colour]').click();
  test('Suggestion preview does not mutate state, CSS or saved projects', () => evaluate('projectJson()')===beforeRepair && evaluate('cssExport()')===beforeRepairCss && w.localStorage.getItem('dss-v27-projects')===beforeRepairStorage);
  test('Preview explains effects on related pairs', () => d.getElementById('repairPreview').textContent.includes('required problems introduced') && d.getElementById('repairPreview').textContent.includes('All worsened pairs'));
  input('repairHex','#oops');
  test('Invalid HEX disables Apply', () => d.getElementById('repairApply').disabled);
  d.getElementById('repairCancel').click(); await wait();
  test('Cancel leaves the project unchanged', () => !d.getElementById('colourRepair').open && evaluate('projectJson()')===beforeRepair);
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light');
  input('repairHex','#7B8A9B');
  test('Border preview predicts seven required pairs resolved', () => d.getElementById('repairPreview').textContent.includes('7 required problems resolved; 0 required problems introduced'));
  d.getElementById('repairApply').click(); await wait();
  test('Apply changes control borders without changing decorative borders', () => evaluate("palette('light').roles['control-border']==='#7B8A9B' && palette('light').roles.border==='#C5D0DD'"));
  test('Applied border is used by actual input styling', () => w.getComputedStyle(d.getElementById('demoEmail')).borderTopColor==='rgb(123, 138, 155)');
  test('Editing light theme leaves dark theme unchanged', () => evaluate("palette('dark').roles['control-border']==='#60748D'"));
  test('Applied semantic colour updates CSS and active local save', () => evaluate('cssExport()').includes('--control-border: #7B8A9B') && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.semanticOverrides?.light?.['control-border']==='#7B8A9B'));
  const repaired=evaluate('projectJson()');
  reset(); evaluate('importConfig('+repaired+')'); await wait();
  test('Semantic overrides survive JSON round trip', () => evaluate("palette('light').roles['control-border']==='#7B8A9B'"));
  input('semanticTheme','light','change'); input('semanticRole','control-border','change');
  d.getElementById('semanticReset').click(); await wait();
  test('Use generated colour restores the role fallback', () => evaluate("palette('light').roles['control-border']===palette('light').roles.border"));
  input('semanticRole','text','change'); d.getElementById('semanticEdit').click(); input('repairHex','#ffffff');
  test('Harmful preview exposes newly failing related pairs', () => /[1-9]\d* required problems introduced/.test(d.getElementById('repairPreview').textContent) && d.getElementById('repairPreview').querySelector('details').open);
  d.getElementById('repairCancel').click(); await wait();
  input('semanticRole','success','change'); d.getElementById('semanticEdit').click();
  input('repairHex','#137A39'); d.getElementById('repairApply').click(); await wait();
  test('Semantic editor synchronizes existing feedback controls', () => d.getElementById('advColor_success').value==='#137a39' && evaluate("palette('light').roles.success==='#137A39'"));
  input('advColor_success','#126b34'); await wait();
  test('Existing feedback control can replace an editor override', () => evaluate("palette('light').roles.success==='#126B34' && !state.semanticOverrides.light.success"));
  input('semanticTheme','dark','change'); input('semanticRole','text','change'); d.getElementById('semanticEdit').click();
  input('repairHex','#DDEEFF'); d.getElementById('repairApply').click(); await wait();
  test('Dark theme editing preserves light theme and current theme selection', () => evaluate("palette('dark').roles.text==='#DDEEFF' && palette('light').roles.text==='#14253A' && state.theme==='light'"));
  test('Dark override is exported in the dark block only', () => {
    const css=evaluate('cssExport()'), dark=css.indexOf('[data-theme="dark"]');
    return !css.slice(0,dark).includes('--text: #DDEEFF') && css.slice(dark).includes('--text: #DDEEFF');
  });
  openRepair(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light');
  input('repairHex','#123456'); d.getElementById('repairApply').click(); await wait();
  test('Button repair reaches the selected state in both themes', () => ['light','dark'].every(theme=>report().some(row=>row.name==='Primary' && row.state==='hover' && row.theme===theme && row.fg==='#123456')));
  openRepair(row=>row.name==='Primary' && row.state==='hover' && row.theme==='light');
  input('repairHex','#ffffff'); input('jBase',18); await wait();
  d.getElementById('repairApply').click();
  test('Stale previews require a renewed review before Apply', () => d.getElementById('colourRepair').open && d.getElementById('repairNotice').textContent.includes('project changed') && evaluate('state.buttonDesign.overrides.primary.hoverText')==='#123456');
  d.getElementById('repairCancel').click(); await wait();
  app.style.width='320px';
  openRepair(row=>row.name==='State Explorer input border' && row.state==='default' && row.theme==='light'); await wait();
  test('Colour repair dialog fits a 320px viewport', () => d.getElementById('colourRepair').getBoundingClientRect().width<=w.innerWidth && d.getElementById('colourRepair').scrollWidth<=d.getElementById('colourRepair').clientWidth+1);
  d.getElementById('repairCancel').click(); await wait();
  evaluate('importConfig({semanticOverrides:{light:{text:"red;position:fixed",unknown:"#000000"},dark:{text:"#abcdef"}}})'); await wait();
  test('Semantic imports reject unknown roles and malformed colours', () => evaluate("!state.semanticOverrides.light.text && !state.semanticOverrides.light.unknown && palette('dark').roles.text==='#ABCDEF'"));
  reset(); await wait();
  test('Reset removes semantic overrides', () => evaluate("!state.semanticOverrides && palette('light').roles['control-border']===palette('light').roles.border"));
  input('jScalePreset','minor-second','change'); await wait();
  test('Minor Second preset updates the scale without changing mobile percentage', () => evaluate('state.ratio===1.067 && clampConfig.mobileFactor===.82') && d.getElementById('clampScalePreset').value==='minor-second');
  input('clampScalePreset','perfect-fourth','change'); await wait();
  test('Calculator scale preset synchronizes the guided builder', () => evaluate('state.ratio===1.333') && d.getElementById('jScalePreset').value==='perfect-fourth');
  input('clampFactor',.75); await wait();
  test('Mobile heading percentage does not change the scale interval', () => evaluate('state.ratio===1.333 && clampConfig.mobileFactor===.75'));
  input('ratio',1.29); await wait();
  test('Manual ratio selects Custom in both preset controls', () => d.getElementById('jScalePreset').value==='custom' && d.getElementById('clampScalePreset').value==='custom');
  reset(); await wait();
  test('Typography ladder displays matching PX and REM values', () => {
    const base=d.querySelectorAll('#typeLadder .type-row small')[2].textContent;
    const step=d.querySelectorAll('#typeLadder .type-row small')[3].textContent;
    return base.includes('16px') && base.includes('1rem') && step.includes('20px') && step.includes('1.25rem');
  });
  test('Mobile and desktop specimens also include REM values', () => d.querySelector('#mobileType small').textContent.includes('rem') && d.querySelector('#desktopType small').textContent.includes('rem'));
  input('typoHeadingTracking',.03); input('typoBodyTracking',.02); await wait();
  test('Direct em controls synchronize all typography editors', () => evaluate('state.headingTracking===.03 && state.bodyTracking===.02 && adv.tracking===3') && d.getElementById('jHeadingTracking').value==='0.03' && d.getElementById('advTrackingOut').textContent==='0.03em');
  test('Specimen letter spacing scales with the local font size', () => {
    const heading=w.getComputedStyle(d.querySelector('#desktopType .sample'));
    const body=w.getComputedStyle(d.querySelectorAll('#desktopType .sample')[3]);
    return Math.abs(parseFloat(heading.letterSpacing)-parseFloat(heading.fontSize)*.03)<.001 && Math.abs(parseFloat(body.letterSpacing)-.32)<.001;
  });
  test('Responsive preview uses heading and body em spacing', () => {
    const heading=w.getComputedStyle(d.querySelector('#previewFrame > h3'));
    const body=w.getComputedStyle(d.querySelector('#previewFrame > p'));
    return Math.abs(parseFloat(heading.letterSpacing)-parseFloat(heading.fontSize)*.03)<.001 && Math.abs(parseFloat(body.letterSpacing)-parseFloat(body.fontSize)*.02)<.001;
  });
  test('CSS export contains heading and body letter-spacing tokens', () => evaluate('cssExport()').includes('--heading-letter-spacing: 0.03em') && evaluate('cssExport()').includes('--body-letter-spacing: 0.02em'));
  const typographyProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+typographyProject+')'); await wait();
  test('Letter-spacing settings round trip through JSON', () => evaluate('state.headingTracking===.03 && state.bodyTracking===.02 && adv.tracking===3'));
  evaluate('importConfig({advanced:{tracking:-3}})'); await wait();
  test('Older heading-tracking projects migrate from hundredths to em', () => evaluate('state.headingTracking===-.03 && state.bodyTracking===0'));
  input('advTracking',2.5); await wait();
  test('Existing advanced tracking control updates the shared em setting', () => evaluate('state.headingTracking===.025') && d.getElementById('typoHeadingTrackingOut').textContent==='0.025em');
  d.getElementById('clampReset').click(); await wait();
  test('Reset responsive limits preserves letter spacing', () => evaluate('clampConfig.mobileFactor===.82 && state.headingTracking===.025'));
  const sections=[...d.querySelectorAll('#main > .studio-section')];
  test('Every centre-pane section has a native heading accordion', () => sections.length===11 && sections.every(el=>el.tagName==='DETAILS' && el.querySelector(':scope > summary > h2')));
  const beforeCollapse=evaluate('projectJson()');
  d.getElementById('collapseSections').click(); await wait();
  test('Collapse all closes only the centre sections without changing the design', () => sections.every(el=>!el.open) && evaluate('projectJson()')===beforeCollapse);
  d.querySelector('.studio-section-nav a[href="#studio-section-2"]').click(); await wait();
  test('Section navigation opens a collapsed destination', () => d.getElementById('studio-section-2').open);
  d.getElementById('studio-section-6').open=false; d.getElementById('jViewCss').click(); await wait();
  test('Builder Show CSS opens the export accordion', () => d.getElementById('studio-section-6').open);
  d.getElementById('buttonDesignLab').open=false; d.getElementById('bdJump').click(); await wait();
  test('Button laboratory shortcut opens its accordion', () => d.getElementById('buttonDesignLab').open);
  d.getElementById('studio-section-4').open=false; evaluate("dssRevealSection('previewFrame',false)"); await wait();
  test('Reopening the responsive preview restores its exact width', () => d.getElementById('studio-section-4').open && Math.abs(d.getElementById('previewFrame').getBoundingClientRect().width-1280)<1);
  d.getElementById('expandSections').click(); await wait();
  test('Expand all restores all centre sections', () => sections.every(el=>el.open));
  d.querySelector('#studio-section-2 > summary').click();
  test('Individual section headings toggle their disclosure', () => !d.getElementById('studio-section-2').open);
  d.querySelector('#studio-section-2 > summary').click(); await wait();
  test('Accordion headings and typography controls fit a 320px page', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  test('No interaction JavaScript errors', () => !w.__reviewErrors.length);
  document.getElementById('results').textContent=JSON.stringify({results, errors:w.__reviewErrors});
};
</script>'''


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/__review__':
            body = HARNESS
        elif path == '/index.html':
            body = (ROOT / 'index.html').read_text(encoding='utf-8')
            body = body.replace('<head>', '''<head><script>
window.__reviewErrors=[];
addEventListener('error',e=>window.__reviewErrors.push(e.message));
addEventListener('unhandledrejection',e=>window.__reviewErrors.push(String(e.reason)));
</script>''', 1)
        else:
            return super().do_GET()
        data = body.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def main():
    browser = os.environ.get('CHROME_BIN') or shutil.which('google-chrome') or shutil.which('chromium')
    if not browser:
        for location in ['C:/Program Files/Google/Chrome/Application/chrome.exe',
                         'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe']:
            if Path(location).is_file():
                browser = location
                break
    if not browser:
        raise SystemExit('Chrome/Chromium not found. Set CHROME_BIN to its executable.')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory(prefix='studio-review-') as profile:
            run = subprocess.run([browser, '--headless', '--disable-gpu', '--no-first-run',
                                  '--no-default-browser-check', '--disable-background-networking',
                                  '--user-data-dir=' + profile, '--virtual-time-budget=15000',
                                  '--dump-dom', f'http://127.0.0.1:{server.server_port}/__review__'],
                                 capture_output=True, encoding='utf-8', errors='replace', timeout=60)
            match = re.search(r'<pre id="results">(.*?)</pre>', run.stdout, re.S)
            if not match or match[1] == 'RUNNING':
                raise SystemExit('Browser review did not complete.\n' + run.stderr[-2000:])
            report = json.loads(unescape(match[1]))
            for item in report['results']:
                print(('PASS' if item['pass'] else 'FAIL') + ': ' + item['name'])
            print(f"{sum(item['pass'] for item in report['results'])}/{len(report['results'])} browser checks passed")
            print(json.dumps(report['errors']))
            return int(any(not item['pass'] for item in report['results']))
    finally:
        server.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
