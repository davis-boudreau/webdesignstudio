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
from urllib.parse import parse_qs, urlsplit

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
  const previewDoc = () => d.getElementById('previewPage').contentDocument;
  const previewWindow = () => d.getElementById('previewPage').contentWindow;
  const saved = () => Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects')))[0].data;
  const wait = (ms=100) => new Promise(resolve => setTimeout(resolve,ms));
  test('No startup JavaScript errors', () => !w.__reviewErrors.length);
  test('Startup selects Minor Third 1.2 throughout the typography controls and export', () => evaluate('state.ratio===1.2 && cssExport().includes("--type-ratio: 1.2;")') && ['jScalePreset','clampScalePreset'].every(id=>d.getElementById(id).value==='minor-third') && ['ratio','jRatio','clampRatio'].every(id=>d.getElementById(id).value==='1.2'));
  test('Section menu precedes the preview, the only expanded centre section at startup', () => d.querySelector('#main > :first-child').classList.contains('studio-section-nav') && d.querySelector('#main > .studio-section').id==='studio-section-4' && [...d.querySelectorAll('#main > .studio-section')].every(el=>el.open===(el.id==='studio-section-4')));
  test('Only Responsive page preview starts expanded throughout the studio', () => [...d.querySelectorAll('details')].every(el=>el.open===(el.id==='studio-section-4')));
  test('Preview initially fills the centre pane in Fluid mode', () => d.getElementById('previewFrame').dataset.width==='fluid' && d.querySelector('button[data-width="fluid"]').getAttribute('aria-pressed')==='true');
  test('Eleven wizard steps connect project planning to fifteen centre lessons', () => d.querySelectorAll('[data-journey-step]').length===11 && d.querySelectorAll('[data-journey-pane]').length===11 && d.querySelectorAll('#main > .studio-section > .panel > .studio-lesson').length===15 && d.getElementById('jProgress').textContent.includes('of 11'));
  test('Every exported token has a configuration source inside the wizard', () => w.dssReadTokens().length>150 && w.dssReadTokens().every(row=>{
    const source=w.dssTokenSource(row), control=source && d.getElementById(source.control);
    return control && control.closest('[data-journey-pane]')?.dataset.journeyPane===String(source.step);
  }));
  test('Derived token families identify their foundation instead of arbitrary overrides', () => ['--space-6','--primary-700','--text-step-4','--text-h1','--font-ui','--heading-tracking','--button-progress-animation'].every(name=>/Derived|Alias/.test(w.dssTokenSource({name}).mode)));
  test('Font, responsive, layout and interaction settings now live in their wizard steps', () => [['fontSource',5],['clampMinWidth',5],['advWeight',5],['advColumns',8],['advBorder',8],['jSpacing',8],['advState',9],['advReduce',9]].every(([id,step])=>d.getElementById(id).closest('[data-journey-pane]').dataset.journeyPane===String(step)));
  d.getElementById('studio-section-4').open=false;
  d.querySelector('[data-journey-step="5"]').click(); input('jBase',18); await wait();
  const closedPreviewDoc=previewDoc();
  test('Wizard edits update the generated CSS while the responsive section is collapsed', () => !d.getElementById('studio-section-4').open && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('--font-size-base: 18px;'));
  evaluate("dssRevealSection('previewPage',false)"); await wait();
  test('Reopening the collapsed preview keeps the document and current settings', () => d.getElementById('studio-section-4').open && previewDoc()===closedPreviewDoc && parseFloat(previewWindow().getComputedStyle(previewDoc().body).fontSize)===18 && Math.abs(previewWindow().innerWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<2);
  d.getElementById('studio-section-4').open=false;
  reset(); d.querySelector('[data-journey-step="0"]').click(); await wait();
  test('Editing and reopening the preview leaves Colour systems collapsed', () => !d.getElementById('studio-section-1').open && !d.getElementById('studio-section-4').open);
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
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return evaluate('state.base===22 && state.ratio===1.05 && state.font===DEFAULT.font') && !page.querySelector('img[onerror]') && page.querySelector('.sample-brand').textContent.includes('<img src=x onerror=alert(1)>');
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
  test('New project defaults use 8px component dimensions and a 24px grid gutter', () => evaluate('adv.height===48 && adv.gap===24 && state.buttonDesign.padX===16 && state.buttonDesign.padY===8 && state.buttonDesign.minHeight===48'));
  test('CSS generation reads both themes without writing project state', () => evaluate(`(() => {
    const theme=Object.getOwnPropertyDescriptor(state,'theme');
    Object.defineProperty(state,'theme',{configurable:true,get:()=>theme.value,set:()=>{throw Error('Export changed theme');}});
    try { return cssExport().includes('[data-theme="dark"]'); }
    finally { Object.defineProperty(state,'theme',theme); }
  })()`));
  test('Unchanged exports preserve selectable code text in both inspectors', () => {
    const centre=d.getElementById('codeView').firstChild, dock=d.getElementById('dockCss').firstChild;
    evaluate('renderCode()');
    return d.getElementById('codeView').firstChild===centre && d.getElementById('dockCss').firstChild===dock;
  });
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
    test('Page fits '+width+'px viewport', () => {
      if (d.documentElement.scrollWidth<=w.innerWidth+1) return true;
      throw Error(JSON.stringify({viewport:w.innerWidth,page:d.documentElement.scrollWidth,overflow:[...d.querySelectorAll('body *')].filter(el=>el.getBoundingClientRect().right>w.innerWidth+1 && el.getBoundingClientRect().width>0 && !el.closest('table,pre,.preview-shell,.studio-code-dock,.studio-section-nav')).slice(0,12).map(el=>({id:el.id,tag:el.tagName,cls:el.className,width:el.getBoundingClientRect().width,right:el.getBoundingClientRect().right}))}));
    });
  }
  const desktopPanes=[];
  for (const width of [1281,1440,1920,2560,3440]) {
    app.style.width=width+'px'; await wait();
    const left=d.querySelector('.sidebar').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect(), right=d.querySelector('.studio-code-dock').getBoundingClientRect();
    const shell=d.querySelector('body > .shell').getBoundingClientRect();
    desktopPanes.push({width, left:left.width, centre:centre.width, right:right.width, shell:shell.width});
    test('Desktop side panes stay fixed while the centre fills '+width+'px', () => Math.abs(left.width-310)<1 && Math.abs(right.width-380)<1 && Math.abs(centre.left-left.right-16)<1 && Math.abs(right.left-centre.right-14)<1 && Math.abs(shell.width-d.documentElement.clientWidth)<1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  test('Only the centre pane grows across large and ultrawide screens', () => {
    const first=desktopPanes.find(pane=>pane.width===1440), last=desktopPanes.at(-1);
    return Math.abs(first.left-last.left)<1 && Math.abs(first.right-last.right)<1 && Math.abs((last.centre-first.centre)-(last.shell-first.shell))<1 && last.centre>first.centre;
  });
  app.style.width='1280px'; await wait();
  test('Inspector stacks above the centre before desktop columns become cramped', () => {
    const left=d.querySelector('.sidebar').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect(), right=d.querySelector('.studio-code-dock').getBoundingClientRect();
    return Math.abs(left.width-310)<1 && Math.abs(centre.left-right.left)<1 && right.bottom<=centre.top && d.documentElement.scrollWidth<=w.innerWidth+1;
  });
  app.style.width='900px'; await wait();
  test('Side panes stack at tablet widths without horizontal page overflow', () => w.getComputedStyle(d.querySelector('.sidebar')).position==='static' && Math.abs(d.querySelector('.sidebar').getBoundingClientRect().left-d.getElementById('main').getBoundingClientRect().left)<1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  app.style.width='1440px'; await wait();
  for (const [mode,width] of [['mobile',390],['tablet',768],['desktop',1280]]) {
    d.querySelector('button[data-width="'+mode+'"]').click(); await wait();
    test('Preview has exact '+mode+' width', () => {
      const frame=d.getElementById('previewFrame'), actual=frame.getBoundingClientRect().width;
      if (Math.abs(actual-width)>=1) throw Error(`Expected ${width}px; got ${actual}px; mode=${frame.dataset.width}; transition=${w.getComputedStyle(frame).transition}`);
      return true;
    });
    test('Preview typography matches the '+mode+' viewport readout', () => {
      const actual=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontSize);
      const expected=evaluate(`fluidTypePx(5,${width})`);
      if (Math.abs(actual-expected)>.11) throw Error(`Expected ${expected}px; got ${actual}px`);
      return true;
    });
    test('Generated document has an exact '+mode+' viewport', () => previewWindow().innerWidth===width);
    test('Generated sample reflows inside the '+mode+' viewport', () => previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1);
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
  d.querySelector('[data-journey-step="6"]').click(); await wait();
  test('Components wizard exposes every semantic role with a friendly label and token', () => {
    const roles=evaluate('SEMANTIC_COLOUR_KEYS');
    return !d.querySelector('[data-journey-pane="6"]').hidden && roles.length===d.getElementById('jSemanticRole').options.length && roles.every(key=>[...d.getElementById('jSemanticRole').options].some(option=>option.value===key && option.textContent.includes('--'+key)));
  });
  d.getElementById('jSaveLocal').click();
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('jSemanticRole','text','change'); await wait();
    const beforeGuided=evaluate('projectJson()');
    test(theme+' wizard shows the current semantic value, purpose and generated status', () => d.getElementById('jSemanticCurrent').textContent.includes(evaluate(`palette('${theme}').roles.text`)) && d.getElementById('jSemanticCurrent').textContent.startsWith(theme==='dark'?'Dark:':'Light:') && d.getElementById('jSemanticReset').disabled && d.getElementById('jSemanticHelp').textContent.includes('Default readable text'));
    d.getElementById('jSemanticEdit').focus(); d.getElementById('jSemanticEdit').click();
    input('repairHex',theme==='light'?'#14253A':'#DDEEFF');
    test(theme+' guided semantic edit previews without mutating the project', () => d.getElementById('colourRepair').open && d.getElementById('repairScope').textContent.includes('the '+theme+' theme only') && evaluate('projectJson()')===beforeGuided);
    d.getElementById('repairCancel').click(); await wait();
    test(theme+' cancelling guided semantic edits returns focus and preserves colours', () => evaluate('projectJson()')===beforeGuided && d.activeElement===d.getElementById('jSemanticEdit'));
    d.getElementById('jSemanticEdit').click(); input('repairHex',theme==='light'?'#14253A':'#DDEEFF');
    d.getElementById('repairApply').click(); await wait();
    const expected=theme==='light'?'#14253A':'#DDEEFF';
    test(theme+' guided override updates the preview, export and active local save', () => evaluate(`palette('${theme}').roles.text==='${expected}'`) && previewWindow().getComputedStyle(previewDoc().body).color===(theme==='light'?'rgb(20, 37, 58)':'rgb(221, 238, 255)') && evaluate('cssExport()').includes('--text: '+expected) && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data.semanticOverrides[theme].text===expected && d.getElementById('jSemanticCurrent').textContent.includes('custom override') && !d.getElementById('jSemanticReset').disabled);
    input('semanticTheme',theme,'change'); input('semanticRole','text','change');
    test(theme+' centre and guided editors show the same semantic override', () => d.getElementById('semanticCurrent').textContent.includes(expected));
  }
  const guidedJson=evaluate('projectJson()'); evaluate('importConfig('+guidedJson+')'); await wait();
  test('Guided semantic overrides survive project JSON import', () => evaluate("state.semanticOverrides.light.text==='#14253A' && state.semanticOverrides.dark.text==='#DDEEFF'") && d.getElementById('jSemanticCurrent').textContent.includes('#DDEEFF'));
  d.getElementById('jSemanticReset').click(); await wait();
  test('Guided reset restores just the selected theme and role', () => evaluate("!state.semanticOverrides.dark.text && state.semanticOverrides.light.text==='#14253A'") && d.getElementById('jSemanticReset').disabled && !d.getElementById('semanticCurrent').textContent.includes('custom override'));
  app.style.width='320px'; await wait();
  test('Guided semantic controls fit the narrow studio layout', () => {
    const pane=d.querySelector('[data-journey-pane="6"]');
    return pane.scrollWidth<=pane.clientWidth+1 && d.getElementById('jSemanticEdit').getBoundingClientRect().width>0 && d.documentElement.scrollWidth<=320;
  });
  app.style.width='1440px'; reset(); await wait();
  test('Project reset refreshes guided semantic values', () => d.getElementById('jSemanticCurrent').textContent.startsWith('Light:') && d.getElementById('jSemanticReset').disabled && !evaluate('state.semanticOverrides'));
  d.querySelector('[data-journey-step="7"]').click(); await wait();
  d.getElementById('bdReview').open=true;
  d.getElementById('jSaveLocal').click();
  const reviewButton = (variant, state) => d.querySelector(`[data-review-variant="${variant}"][data-review-state="${state}"]`);
  const reviewCell = (variant, state, theme) => reviewButton(variant,state).closest('tr').querySelector(`[data-review-theme="${theme}"]`);
  const reviewPair = (theme, kind) => d.querySelector(`#bdReviewPairs [aria-label="${theme} theme contrast"] [data-kind="${kind}"]`);
  const selectReview = (variant, state) => {
    const button=reviewButton(variant,state);
    button.closest('details').open=true; button.focus(); button.click();
  };
  test('Guided button review includes all 35 states and 70 theme results', () =>
    d.querySelectorAll('#bdReviewVariants details').length===5 &&
    d.querySelectorAll('#bdReviewVariants tbody tr').length===35 &&
    d.querySelectorAll('#bdReviewVariants td[data-result]').length===70 &&
    d.getElementById('bdReviewSummary').textContent.includes('10 disabled exemptions'));
  test('Every guided result agrees with the full contrast inventory', () => {
    return ['Primary','Secondary','Accent','Outline','Text'].every(variant=>
      ['default','hover','focus','active','selected','disabled','loading'].every(state=>
        ['light','dark'].every(theme=>{
          const rows=report().filter(row=>row.group.startsWith('Button Laboratory:') && row.name.split(' ')[0]===variant && row.state===state && row.theme===theme && row.scope==='required' && row.threshold!==null);
          const expected=state==='disabled'?'exempt':rows.some(row=>row.ratio<row.threshold)?'review':'pass';
          return reviewCell(variant.toLowerCase(),state,theme).dataset.result===expected;
        })));
  });
  const beforeReviewCss=evaluate('cssExport()');
  const beforeReviewColours=evaluate('JSON.stringify([state.buttonDesign.overrides,state.buttonDesign.custom,state.buttonDesign.sources])');
  selectReview('secondary','hover'); await wait();
  test('Selecting a reviewed state synchronizes the wizard and live specimen', () => d.getElementById('bdVariant').value==='secondary' && d.getElementById('bdState').value==='hover' && d.querySelector('#bdSingle .bd-button').textContent.includes('Secondary') && d.getElementById('bdReviewTitle').textContent.includes('Secondary'));
  test('Review navigation preserves colours and component CSS', () => evaluate('cssExport()')===beforeReviewCss && evaluate('JSON.stringify([state.buttonDesign.overrides,state.buttonDesign.custom,state.buttonDesign.sources])')===beforeReviewColours);
  test('Review selection has one accessible current-state marker', () => d.querySelectorAll('#bdReviewVariants [aria-current="true"]').length===1 && reviewButton('secondary','hover').getAttribute('aria-current')==='true' && reviewButton('secondary','hover').getAttribute('aria-controls')==='bdReviewSelection');
  const stableReviewButton=reviewButton('secondary','hover');
  const stableReviewDetails=stableReviewButton.closest('details');
  input('bdHover','#ffffff'); input('bdHoverText','#ffffff'); await wait();
  test('Poor state overrides flag both themes and show their exact text ratio', () => ['light','dark'].every(theme=>reviewCell('secondary','hover',theme).dataset.result==='review') && ['Light','Dark'].every(theme=>reviewPair(theme,'text').textContent.includes('1.000:1')));
  test('Live contrast refresh preserves review focus and disclosure state', () => reviewButton('secondary','hover')===stableReviewButton && d.activeElement===stableReviewButton && stableReviewDetails.open);
  const beforeWizardRepair=evaluate('projectJson()');
  const wizardRepairButton=reviewPair('Light','text').querySelector('button');
  wizardRepairButton.focus(); wizardRepairButton.click(); input('repairHex','#101820');
  test('Wizard colour repair previews effects across both themes without committing', () => d.getElementById('colourRepair').open && d.getElementById('repairTarget').selectedOptions[0].textContent.includes('Secondary: hoverText') && evaluate('projectJson()')===beforeWizardRepair);
  d.getElementById('repairCancel').click(); await wait();
  test('Cancel returns focus to the wizard edit action and keeps the failing colour', () => d.activeElement===wizardRepairButton && evaluate('projectJson()')===beforeWizardRepair && reviewCell('secondary','hover','light').dataset.result==='review');
  wizardRepairButton.click(); input('repairHex','#101820'); d.getElementById('repairApply').click(); await wait();
  test('Applying a reviewed text fix updates both theme results and returns focus', () => ['light','dark'].every(theme=>reviewCell('secondary','hover',theme).dataset.result==='pass') && evaluate('state.buttonDesign.overrides.secondary.hoverText')==='#101820' && d.activeElement===wizardRepairButton);
  test('Wizard fixes reach the live CSS/HTML preview and project save', () => previewDoc().getElementById('dssPreviewStyles').textContent.includes('--button-secondary-hover-text: #101820') &&
    previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--secondary')).getPropertyValue('--button-secondary-hover-text').trim()==='#101820' &&
    Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.buttonDesign?.overrides.secondary?.hoverText==='#101820'));
  const wizardRepaired=evaluate('projectJson()'); reset(); evaluate('importConfig('+wizardRepaired+')'); await wait();
  test('Saved button fixes and selected review state survive JSON round trip', () => reviewButton('secondary','hover').getAttribute('aria-current')==='true' && ['light','dark'].every(theme=>reviewCell('secondary','hover',theme).dataset.result==='pass') && d.getElementById('bdHoverText').value==='#101820');
  input('bdDefaultBg','#777777'); input('bdText','#000000'); selectReview('secondary','loading'); await wait();
  test('Loading review retains full opacity and the default text contrast', () => reviewCell('secondary','default','light').dataset.result==='pass' && reviewCell('secondary','loading','light').dataset.result==='pass' && w.getComputedStyle(d.querySelector('#bdMatrix [data-sim="loading"]')).opacity==='1' && report().filter(row=>row.name==='Secondary' && row.state==='loading').every(row=>row.ratio===report().find(other=>other.name===row.name && other.theme===row.theme && other.location===row.location && other.state==='default').ratio));
  selectReview('secondary','disabled'); await wait();
  test('Disabled states show informational ratios and an exemption in both themes', () => ['light','dark'].every(theme=>reviewCell('secondary','disabled',theme).dataset.result==='exempt') && ['Light','Dark'].every(theme=>reviewPair(theme,'text').textContent.includes('Exempt (no target)')) && !d.getElementById('bdContrast').textContent.includes('Pass'));
  input('bdDefaultBg','#000000'); input('bdText','#ffffff'); input('bdFocus','#ffffff'); selectReview('secondary','focus'); await wait();
  test('Focus review catches a failing ring even when its text passes', () => reviewPair('Light','text').dataset.result==='pass' && reviewPair('Light','focus').dataset.result==='review' && reviewCell('secondary','focus','light').dataset.result==='review' && reviewCell('secondary','focus','dark').dataset.result==='pass');
  const ringEdit=reviewPair('Light','focus').querySelector('button'); ringEdit.focus(); ringEdit.click(); input('repairHex','#808080'); d.getElementById('repairApply').click(); await wait();
  test('Ring editing uses the shared focus setting across every variant and theme', () => report().filter(row=>row.group==='Button Laboratory: indicators' && row.name.includes('focus ring')).every(row=>row.fg==='#808080') && evaluate('state.buttonDesign.focus')==='#808080');
  selectReview('secondary','selected'); await wait();
  test('Selection reviews expose required outer and conditional inner indicators separately', () => !reviewPair('Light','selection').hidden && reviewPair('Light','inner').dataset.result==='conditional' && reviewPair('Light','inner').textContent.includes('Conditional'));
  selectReview('secondary','default'); await wait();
  test('Conditional button boundaries do not turn readable labels into required failures', () => reviewPair('Light','boundary').dataset.result==='conditional' && reviewCell('secondary','default','light').dataset.result==='pass');
  input('bdVariant','outline'); input('bdState','active'); await wait();
  test('Existing variant and state selectors update the contrast review selection', () => reviewButton('outline','active').getAttribute('aria-current')==='true' && d.getElementById('bdReviewTitle').textContent.includes('Outline'));
  const validReview=evaluate('projectJson()');
  evaluate('dssSelectButtonState("__proto__","default"); dssSelectButtonState("primary","bad-state")'); await wait();
  test('Review navigation rejects unknown variants and states', () => evaluate('projectJson()')===validReview);
  for (const theme of ['light','dark']) {
    input('jTheme',theme); app.style.width='320px';
    d.querySelectorAll('#bdReviewVariants details').forEach(el=>el.open=true); await wait();
    test('All guided button reviews fit the '+theme+' 320px layout', () => [...d.querySelectorAll('.bd-review-table,.bd-review-selection')].every(el=>el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1) &&
      [...d.querySelectorAll('#bdReviewVariants button')].every(el=>el.getBoundingClientRect().height>=40 && el.tabIndex===0));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset clears repaired button colours and refreshes the selected review', () => evaluate('!Object.keys(state.buttonDesign.overrides).length') && reviewButton('primary','default').getAttribute('aria-current')==='true');
  test('New default button colours meet required text and indicator targets in all states and themes', () => report().filter(row=>row.group.startsWith('Button Laboratory:') && row.scope==='required' && row.threshold!==null).every(row=>row.status==='pass'));
  const matrixStates=state=>[...d.querySelectorAll(`#bdMatrix [data-sim="${state}"]`)];
  for (const theme of ['light','dark']) {
    input('jTheme',theme); await wait();
    test(theme+' hover cues underline every button variant without changing geometry', () => matrixStates('hover').length===5 && matrixStates('hover').every((button,i)=>{
      const normal=matrixStates('default')[i];
      return w.getComputedStyle(button).textDecorationLine.includes('underline') && Math.abs(button.getBoundingClientRect().width-normal.getBoundingClientRect().width)<1 && Math.abs(button.getBoundingClientRect().height-normal.getBoundingClientRect().height)<1;
    }));
    test(theme+' pressed states add an inset cue to every variant', () => matrixStates('active').length===5 && matrixStates('active').every(button=>w.getComputedStyle(button).boxShadow.includes('inset')));
    test(theme+' selected states have a visible checkmark and an unchanged label', () => matrixStates('selected').length===5 && matrixStates('selected').every((button,i)=>{
      const icon=w.getComputedStyle(button,'::before');
      return button.getAttribute('aria-pressed')==='true' && icon.content==='""' && parseFloat(icon.borderBottomWidth)>0 && button.textContent===matrixStates('default')[i].textContent;
    }));
    test(theme+' focus simulations retain the full outline around every variant', () => matrixStates('focus').every(button=>parseFloat(w.getComputedStyle(button).outlineWidth)===3 && w.getComputedStyle(button).outlineStyle==='solid' && parseFloat(w.getComputedStyle(button).outlineOffset)===3));
    test(theme+' loading states retain readable opacity, visible progress and text', () => matrixStates('loading').length===5 && matrixStates('loading').every(button=>w.getComputedStyle(button).opacity==='1' && button.textContent==='Processing…' && w.getComputedStyle(button,'::after').content==='""' && parseFloat(w.getComputedStyle(button,'::after').width)>0));
    test(theme+' disabled states remain natively unavailable and separately explained', () => matrixStates('disabled').every(button=>button.disabled && w.getComputedStyle(button).cursor==='not-allowed'));
    for (const stateName of ['hover','active','focus','selected','loading','disabled']) {
      input('bdState',stateName); await wait();
      const action=previewDoc().querySelector('.sample-selected-action');
      const style=previewWindow().getComputedStyle(action);
      test(theme+' exported-page '+stateName+' state has its non-colour cue and semantics', () => {
        if (stateName==='hover') return style.textDecorationLine.includes('underline');
        if (stateName==='active') return style.boxShadow.includes('inset');
        if (stateName==='focus') return style.outlineStyle==='solid' && parseFloat(style.outlineOffset)===3;
        if (stateName==='selected') {
          const toggles=[...previewDoc().querySelectorAll('#components button[aria-pressed]')];
          return toggles.length===2 && toggles[0].textContent===toggles[1].textContent && toggles[0].getAttribute('aria-pressed')==='false' && action.getAttribute('aria-pressed')==='true' && previewWindow().getComputedStyle(action,'::before').content==='""' && previewWindow().getComputedStyle(toggles[0],'::before').visibility==='hidden' && Math.abs(toggles[0].getBoundingClientRect().width-action.getBoundingClientRect().width)<1;
        }
        if (stateName==='loading') return action.disabled && action.getAttribute('aria-busy')==='true' && action.textContent==='Processing…' && style.opacity==='1' && previewWindow().getComputedStyle(action,'::after').content==='""';
        return action.disabled && !!previewDoc().getElementById(action.getAttribute('aria-describedby'))?.textContent.includes('prerequisite');
      });
    }
  }
  input('advState','loading','change'); await wait();
  test('State Explorer loading uses the same progress cue and full-opacity text', () => d.getElementById('advDemoButton').textContent==='Processing…' && w.getComputedStyle(d.getElementById('advDemoButton')).opacity==='1' && w.getComputedStyle(d.getElementById('advDemoButton'),'::after').content==='""');
  input('bdState','loading');
  d.getElementById('advReduce').checked=true; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true})); await wait();
  test('Reduce demo animations stops progress in the laboratory and State Explorer', () => ['#bdSingle .bd-button','#advDemoButton'].every(selector=>w.getComputedStyle(d.querySelector(selector),'::after').animationName==='none'));
  test('Reduced demo motion also reaches the generated page and CSS export', () => previewWindow().getComputedStyle(previewDoc().querySelector('.sample-selected-action'),'::after').animationName==='none' && evaluate('cssExport()').includes('--button-progress-animation: none'));
  d.getElementById('advReduce').checked=false; d.getElementById('advReduce').dispatchEvent(new w.Event('change',{bubbles:true})); await wait();
  test('Restoring demo animations preserves the platform reduced-motion preference', () => w.getComputedStyle(d.querySelector('#bdSingle .bd-button'),'::after').animationName===(w.matchMedia('(prefers-reduced-motion: reduce)').matches?'none':'dss-button-progress'));
  input('advState','selected','change'); await wait();
  test('State Explorer selection has a checkmark and nearby state guidance', () => w.getComputedStyle(d.getElementById('advDemoButton'),'::before').content==='""' && d.getElementById('advButtonHelp').textContent.includes('Keep the label'));
  input('bdState','default'); await wait();
  const focusSpecimen=d.querySelector('#bdSingle .bd-button'); focusSpecimen.focus();
  test('Actual keyboard-visible focus retains its outline independently of state simulations', () => !focusSpecimen.matches('[data-sim="focus"]') && focusSpecimen.matches(':focus-visible') && parseFloat(w.getComputedStyle(focusSpecimen).outlineWidth)===3);
  const statesDownload=[]; const priorStateDownload=w.download;
  w.download=(name,content)=>statesDownload.push({name,content}); d.getElementById('bdExport').click(); w.download=priorStateDownload;
  test('Standalone button CSS includes the shared state cues, forced-colour fallback and reduced motion', () => statesDownload[0].content.includes('text-decoration-line: underline') && statesDownload[0].content.includes('box-shadow: inset') && statesDownload[0].content.includes('[aria-pressed]::before') && statesDownload[0].content.includes('[aria-busy="true"]::after') && statesDownload[0].content.includes('prefers-reduced-motion: reduce') && statesDownload[0].content.includes('forced-colors: active'));
  const practicesProject=evaluate('projectJson()');
  input('bdFocus','#775599'); const customFocusProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+customFocusProject+')'); await wait();
  test('Imported custom focus colours remain editable under the new default practices', () => evaluate('state.buttonDesign.focus')==='#775599' && evaluate('cssExport()').includes('--button-focus: #775599'));
  evaluate('importConfig('+practicesProject+')'); reset(); await wait();
  input('jScalePreset','minor-second','change'); await wait();
  test('Minor Second preset updates the scale without changing mobile percentage', () => evaluate('state.ratio===1.067 && clampConfig.mobileFactor===.82') && d.getElementById('clampScalePreset').value==='minor-second');
  input('clampScalePreset','perfect-fourth','change'); await wait();
  test('Calculator scale preset synchronizes the guided builder', () => evaluate('state.ratio===1.333') && d.getElementById('jScalePreset').value==='perfect-fourth');
  input('clampFactor',.75); await wait();
  test('Mobile heading percentage does not change the scale interval', () => evaluate('state.ratio===1.333 && clampConfig.mobileFactor===.75'));
  input('ratio',1.29); await wait();
  test('Manual ratio selects Custom in both preset controls', () => d.getElementById('jScalePreset').value==='custom' && d.getElementById('clampScalePreset').value==='custom');
  reset(); await wait();
  test('Reset restores Minor Third without changing responsive heading limits', () => evaluate('state.ratio===1.2 && clampConfig.mobileFactor===.82') && d.getElementById('jScalePreset').value==='minor-third' && d.getElementById('clampScalePreset').value==='minor-third');
  test('Typography ladder displays matching PX and REM values', () => {
    const base=d.querySelectorAll('#typeLadder .type-row small')[2].textContent;
    const step=d.querySelectorAll('#typeLadder .type-row small')[3].textContent;
    return base.includes('16px') && base.includes('1rem') && step.includes('19.2px') && step.includes('1.2rem');
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
    const heading=previewWindow().getComputedStyle(previewDoc().querySelector('h1'));
    const body=previewWindow().getComputedStyle(previewDoc().body);
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
  test('Every centre-pane section has a native heading accordion', () => sections.length===15 && sections.every(el=>el.tagName==='DETAILS' && el.querySelector(':scope > summary > h2')));
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
  reset(); await wait();
  for (const hex of ['#FF0000','#00FF00','#0000FF','#FFFFFF','#000000','#004780']) {
    test('OKLCH round trip preserves '+hex, () => evaluate(`oklchHex(...rgbToOklch('${hex}'))` )===hex);
  }
  input('oklchRole','accent','change');
  input('oklchLight',65); input('oklchChroma',.12); input('oklchHue',150);
  const chosenHex=d.getElementById('oklchHex').textContent;
  test('OKLCH exploration leaves palette unchanged before Apply', () => evaluate('state.accent')==='#cbdb2a');
  d.getElementById('oklchApply').click();
  test('OKLCH Apply updates foundation, guided editor, export and saved project', () => {
    d.getElementById('jSaveLocal').click();
    return evaluate('state.accent').toUpperCase()===chosenHex && d.getElementById('jAccent').value.toUpperCase()===chosenHex && evaluate('cssExport()').includes('--accent-500: '+chosenHex) && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data.accent.toUpperCase()===chosenHex);
  });
  input('oklchLight',90); d.getElementById('oklchReset').click();
  test('OKLCH Load discards exploration and reloads the current palette anchor', () => d.getElementById('oklchHex').textContent===chosenHex);
  input('oklchLight',60); input('oklchChroma',.4);
  test('OKLCH warns when chroma exceeds sRGB gamut', () => d.getElementById('oklchGamut').textContent.startsWith('Outside sRGB') && /^#[0-9A-F]{6}$/.test(d.getElementById('oklchHex').textContent));
  for (const role of ['primary','secondary','accent']) {
    input('oklchRole',role,'change'); input('oklchLight',65); input('oklchChroma',.12); input('oklchHue',150);
    d.getElementById('oklchApply').click();
    const otherRoles=evaluate(`JSON.stringify(Object.fromEntries(['primary','secondary','accent'].filter(key=>key!=='${role}').map(key=>[key,state[key]])))`);
    const references=evaluate('JSON.stringify(state.brandPalette)');
    d.getElementById('oklchDefault').click(); await wait();
    test('OKLCH default reset restores only '+role+' and synchronizes controls, preview, export and saved data', () => {
      const expected=evaluate(`DEFAULT.${role}`).toUpperCase();
      d.getElementById('jSaveLocal').click();
      return evaluate(`state.${role}.toUpperCase()===DEFAULT.${role}.toUpperCase()`)
        && d.getElementById('oklchHex').textContent===expected
        && d.getElementById('j'+role[0].toUpperCase()+role.slice(1)).value.toUpperCase()===expected
        && evaluate('cssExport()').includes('--'+role+'-500: '+expected)
        && d.getElementById('previewPage').contentDocument.getElementById('dssPreviewStyles').textContent.includes('--'+role+'-500: '+expected)
        && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(p=>p.data[role].toUpperCase()===expected)
        && evaluate(`JSON.stringify(Object.fromEntries(['primary','secondary','accent'].filter(key=>key!=='${role}').map(key=>[key,state[key]])))`)===otherRoles
        && evaluate('JSON.stringify(state.brandPalette)')===references;
    });
    d.getElementById('oklchDefault').click();
    test('Repeated '+role+' default reset keeps the wheel selection stable', () => d.getElementById('oklchHex').textContent===evaluate(`DEFAULT.${role}.toUpperCase()`) && d.getElementById('oklchRole').value===role);
  }
  reset(); await wait();
  const downloadCalls=[];
  const originalDownload=w.download;
  w.download=(name,content,type)=>downloadCalls.push({name,content,type});
  for (const [id,name] of [['saveBtn','design-system-studio.json'],['cssBtn','tokens.css'],['dockDownload','tokens.css'],['jExportHtml','index.html'],['jExportCss','tokens.css'],['jExportJson','design-system-project.json'],['bdExport','design-system-buttons.css']]) {
    d.getElementById(id).click();
    test(id+' produces the expected download', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content.length>0);
  }
  for (const [tab,name] of [['viewCss','tokens.css'],['viewJson','design-system-studio.json'],['viewHtml','index.html']]) {
    d.getElementById(tab).click(); d.getElementById('downloadCode').click();
    test(tab+' downloads exactly the displayed code', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content===d.getElementById('codeView').textContent);
  }
  const beforeWebsiteDownloads=evaluate('projectJson()');
  for (const [index,button] of [...d.querySelectorAll('[data-website-download]')].entries()) {
    button.click();
    test('Standalone website action '+(index+1)+' downloads the matching live file with its MIME type', () => {
      const html=button.dataset.websiteDownload==='html', file=downloadCalls.at(-1);
      return file.name===(html?'index.html':'tokens.css') && file.type===(html?'text/html':'text/css') && file.content===evaluate(html?'htmlExport()':'cssExport()');
    });
  }
  test('Standalone download guidance names the matching files without changing saved settings', () => evaluate('projectJson()')===beforeWebsiteDownloads && d.querySelector('[data-website-status]').textContent.includes('Save index.html and tokens.css in the same folder'));
  for (const language of ['html','css']) {
    d.getElementById('studio-section-6').open=false;
    d.querySelector(`[data-website-code="${language}"]`).click();
    test('Website '+language+' shortcut opens and focuses its matching live code', () => d.getElementById('studio-section-6').open && d.getElementById(language==='html'?'viewHtml':'viewCss').getAttribute('aria-selected')==='true' && d.getElementById('codeView').textContent===evaluate(language==='html'?'htmlExport()':'cssExport()') && d.activeElement===d.getElementById('codeView'));
  }
  input('tokenSearch','--button-primary-hover'); await wait();
  d.getElementById('tokenDownload').click();
  test('Token search and CSV agree on the filtered tokens', () => [...d.querySelectorAll('#tokenTableBody tr')].every(row=>row.textContent.includes('--button-primary-hover')) && downloadCalls.at(-1).name==='design-system-tokens.csv' && !downloadCalls.at(-1).content.includes('--brand-white'));
  w.download=originalDownload;
  d.getElementById('jNewLocal').click(); input('jProject','Audit project A'); input('jBase',18); d.getElementById('jSaveLocal').click();
  const projectA=d.getElementById('jProjects').value;
  d.getElementById('jNewLocal').click(); input('jProject','Audit project B'); input('jBase',20); d.getElementById('jSaveLocal').click();
  const projectB=d.getElementById('jProjects').value;
  d.getElementById('jProjects').value=projectA; d.getElementById('jLoadLocal').click();
  test('Saved projects load their own settings', () => evaluate('state.base===18 && state.project==="Audit project A"'));
  input('jBase',19);
  test('Switching saved projects routes autosave to the loaded project', () => {
    const stored=JSON.parse(w.localStorage.getItem('dss-v27-projects'));
    return stored[projectA].data.base===19 && stored[projectB].data.base===20;
  });
  const originalConfirm=w.confirm;
  w.confirm=()=>false; d.getElementById('jDeleteLocal').click();
  test('Cancelling deletion preserves the saved project', () => !!JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectA]);
  w.confirm=()=>true; d.getElementById('jDeleteLocal').click();
  test('Confirmed deletion removes only the selected project', () => {
    const stored=JSON.parse(w.localStorage.getItem('dss-v27-projects')); return !stored[projectA] && !!stored[projectB];
  });
  w.confirm=originalConfirm;
  const priorStorage=w.localStorage.getItem('dss-v27-projects');
  w.localStorage.setItem('dss-v27-projects',JSON.stringify({bad:null,missing:{},array:{name:'Bad',updated:'invalid',data:[]},valid:{name:'Valid',updated:'2026-10-19T12:00:00Z',data:{project:'Recovered',base:18}}}));
  const recovery=d.createElement('iframe'); recovery.src='/index.html';
  await new Promise(resolve=>{recovery.onload=resolve;d.body.append(recovery);});
  test('Malformed saved entries do not prevent startup or valid project recovery', () => {
    const rd=recovery.contentDocument, rw=recovery.contentWindow;
    if (rw.__reviewErrors.length || rd.getElementById('jProjects').options.length!==1 || rd.getElementById('jProjects').value!=='valid') return false;
    rd.getElementById('jLoadLocal').click();
    return rw.eval('state.project==="Recovered" && state.base===18') && typeof rw.dssGetContrastChecks==='function';
  });
  recovery.remove(); w.localStorage.setItem('dss-v27-projects',priorStorage);
  reset();
  const originalAlert=w.alert, alerts=[]; w.alert=message=>alerts.push(message);
  const importFile=async text=>{
    const transfer=new w.DataTransfer(); transfer.items.add(new w.File([text],'project.json',{type:'application/json'}));
    d.getElementById('loadFile').files=transfer.files;
    d.getElementById('loadFile').dispatchEvent(new w.Event('change',{bubbles:true})); await wait();
    // File.text() resolves on the browser's I/O clock, independently of virtual
    // timers. Wait for the handler to clear the input before the next import.
    for (let attempt=0;attempt<40 && d.getElementById('loadFile').value;attempt++) await wait(50);
  };
  await importFile(JSON.stringify({project:'File import',base:21,buttonDesign:{radius:17}}));
  test('JSON file picker imports all modules and clears the file selection', () => evaluate('state.project==="File import" && state.base===21 && state.buttonDesign.radius===17') && !d.getElementById('loadFile').value);
  const beforeBadFile=evaluate('projectJson()');
  await importFile('{broken json');
  test('Invalid JSON reports an error without changing the project', () => alerts.length===1 && evaluate('projectJson()')===beforeBadFile);
  await importFile(' '.repeat(100001));
  test('Oversized JSON files are rejected without changing the project', () => alerts.at(-1).includes('too large') && evaluate('projectJson()')===beforeBadFile);
  w.alert=originalAlert;
  const originalClipboard=w.navigator.clipboard;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(Error('Denied for audit'))}});
  d.getElementById('copyCode').click(); await wait();
  test('Clipboard rejection gives a manual-copy fallback', () => d.getElementById('liveStatus').textContent.includes('Clipboard unavailable'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard});
  reset();
  for (const stateName of ['default','hover','focus','active','selected','disabled','loading','invalid','success','readonly']) {
    input('advState',stateName,'change');
    test('State Explorer correctly exposes '+stateName+' semantics', () => {
      const button=d.getElementById('advDemoButton'), field=d.getElementById('advDemoInput');
      return button.disabled===['disabled','loading'].includes(stateName) &&
        button.getAttribute('aria-busy')===String(stateName==='loading') &&
        button.hasAttribute('aria-pressed')===(stateName==='selected') &&
        field.disabled===(stateName==='disabled') && field.readOnly===(stateName==='readonly') &&
        field.getAttribute('aria-invalid')===String(stateName==='invalid');
    });
  }
  reset();
  for (const [id,value,type] of [['advFocus',5],['advHeight',50],['advWeight',800,'change'],['advMeasure',75],['advBorder',6],['advShadow','strong','change'],['advOpacity',70],['advColumns',260],['advGap',20],['advAlign','end','change'],['advMotion',250],['bdVariant','outline'],['bdSize','lg'],['bdPaddingX',24],['bdPaddingY',18],['bdMinHeight',56],['bdRadius',20],['bdBorder',3],['bdWeight',700],['bdFocusWidth',4],['bdMotion',250],['bdSource','custom'],['bdCustom','#123456'],['bdHover','#234567'],['bdActive','#345678'],['bdText','#456789'],['bdHoverText','#ffffff'],['bdActiveText','#ffffff'],['bdDefaultBg','#eeeeee'],['bdBorderColor','#123456']]) input(id,value,type||'input');
  input('advAlign','start','change');
  const fullConfig=JSON.parse(evaluate('projectJson()'));
  reset(); evaluate('importConfig('+JSON.stringify(fullConfig)+')');
  test('Advanced and button editor settings survive a full project round trip', () => {
    const loaded=JSON.parse(evaluate('projectJson()'));
    return JSON.stringify(loaded.advanced)===JSON.stringify(fullConfig.advanced) && JSON.stringify(loaded.buttonDesign)===JSON.stringify(fullConfig.buttonDesign) && !/undefined|NaN|Infinity/.test(evaluate('cssExport()'));
  });
  input('brandApplyRole','accent','change');
  const referenceAction=d.querySelector('[data-brand-role="accent"][data-brand-hex="#00BADC"]'); referenceAction.click();
  test('Reference swatch selection synchronizes palette and guided controls', () => d.getElementById('accent').value===d.getElementById('jAccent').value && evaluate('state.accent')===referenceAction.dataset.brandHex.toLowerCase());
  d.querySelector('[data-journey-step="0"]').click(); d.getElementById('jNext').click();
  test('Guided navigation advances and returns to the first step', () => {
    if (!d.getElementById('jProgress').textContent.startsWith('Step 2')) return false;
    d.getElementById('jBack').click(); return d.getElementById('jBack').disabled && d.getElementById('jProgress').textContent.startsWith('Step 1');
  });
  d.getElementById('dockToggle').click();
  test('CSS dock collapse and expand update accessible state', () => {
    if (d.getElementById('dockToggle').getAttribute('aria-expanded')!=='false') return false;
    d.getElementById('dockToggle').click(); return d.getElementById('dockToggle').getAttribute('aria-expanded')==='true' && !d.querySelector('.studio-code-dock').classList.contains('is-collapsed');
  });
  const storageSet=w.Storage.prototype.setItem;
  w.Storage.prototype.setItem=()=>{throw Error('Storage quota exceeded for audit');};
  d.getElementById('jSaveLocal').click();
  test('Unavailable storage offers JSON backup without crashing', () => d.getElementById('jSaveStatus').textContent.includes('Download JSON instead'));
  w.Storage.prototype.setItem=storageSet;
  reset(); await wait();
  const beforeInspector=evaluate('projectJson()');
  d.getElementById('dockTabCss').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
  test('Inspector keyboard tabs select HTML and label the code panel', () => d.activeElement.id==='dockTabHtml' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockTabCss').tabIndex===-1 && d.getElementById('dockCss').getAttribute('aria-labelledby')==='dockTabHtml' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  test('Switching inspector languages leaves project data unchanged', () => evaluate('projectJson()')===beforeInspector);
  input('jProject','Cedar Studio'); input('jTheme','dark'); input('bdSize','lg');
  d.getElementById('bdMobileFull').checked=true; d.getElementById('bdMobileFull').dispatchEvent(new w.Event('input',{bubbles:true}));
  test('HTML inspector follows project, theme and button selections live', () => d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('dockCss').textContent.includes('Cedar Studio') && d.getElementById('dockCss').textContent.includes('data-theme="dark"') && d.getElementById('dockCss').textContent.includes('ds-button--lg ds-button--mobile-full'));
  const inspectorDownloads=[]; w.download=(name,content,type)=>inspectorDownloads.push({name,content,type});
  d.getElementById('dockDownload').click();
  test('HTML inspector downloads the exact visible home page', () => inspectorDownloads.at(-1).name==='index.html' && inspectorDownloads.at(-1).type==='text/html' && inspectorDownloads.at(-1).content===d.getElementById('dockCss').textContent && d.getElementById('dockCopy').textContent==='Copy HTML');
  let copiedInspector='';
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{copiedInspector=text;}}});
  d.getElementById('dockCopy').click(); await wait();
  test('Inspector copies the selected HTML', () => copiedInspector===evaluate('htmlExport()'));
  d.getElementById('dockTabHtml').dispatchEvent(new w.KeyboardEvent('keydown',{key:'Home',bubbles:true}));
  d.getElementById('dockDownload').click();
  test('Inspector returns to live CSS with CSS download and copy labels', () => d.activeElement.id==='dockTabCss' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && inspectorDownloads.at(-1).name==='tokens.css' && inspectorDownloads.at(-1).content===evaluate('cssExport()') && d.getElementById('dockCopy').textContent==='Copy CSS');
  d.getElementById('dockCopy').click(); await wait();
  test('Inspector copies the selected CSS', () => copiedInspector===evaluate('cssExport()'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard}); w.download=originalDownload;
  test('Generated reference tokens use the universal brand prefix', () => evaluate('cssExport()').includes('--brand-white: #FFFFFF') && !evaluate('cssExport()').includes('--example-'));
  input('tokenSearch','--brand-'); await wait();
  test('Token catalogue classifies renamed brand references', () => d.querySelectorAll('#tokenTableBody tr').length===11 && [...d.querySelectorAll('#tokenTableBody tr')].every(row=>row.textContent.includes('Brand palette')));
  const sampleDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Sample home page has header, main, footer, hero and a single headline', () => !!sampleDoc.querySelector('body > header nav') && !!sampleDoc.querySelector('body > main') && !!sampleDoc.querySelector('body > footer nav') && !!sampleDoc.querySelector('#home .sample-lead') && sampleDoc.querySelectorAll('h1').length===1);
  test('Every sample navigation and action anchor reaches an existing section', () => [...sampleDoc.querySelectorAll('a[href^="#"]')].every(link=>sampleDoc.getElementById(link.hash.slice(1))));
  test('Every main section offers primary and secondary actions matching the wizard variants', () => [...sampleDoc.querySelectorAll('main > section')].length===9 && [...sampleDoc.querySelectorAll('main > section')].every(section=>{
    const rows=section.querySelectorAll('.sample-section-actions');
    return rows.length===1 && rows[0].children.length===2 && rows[0].firstElementChild.matches('.ds-button--primary') && rows[0].lastElementChild.matches('a.ds-button--secondary[href]') && (section.id==='contact'?rows[0].firstElementChild.matches('form button[type="submit"]'):rows[0].firstElementChild.matches('a[href]'));
  }));
  test('Section actions follow selected button size and mobile full-width settings', () => [...sampleDoc.querySelectorAll('.sample-section-actions .ds-button')].every(action=>action.classList.contains('ds-button--lg') && action.classList.contains('ds-button--mobile-full')));
  test('Header navigation and section actions make every main section reachable', () => {
    const targets=new Set([...sampleDoc.querySelectorAll('header nav a, .sample-section-actions a')].map(link=>link.getAttribute('href').slice(1)));
    return [...sampleDoc.querySelectorAll('main > section')].every(section=>targets.has(section.id));
  });
  test('Sample images are embedded, labelled and follow the selected palette', () => {
    const images=[...sampleDoc.querySelectorAll('img')];
    return images.length>=2 && images.every(img=>img.alt && img.getAttribute('width') && img.src.startsWith('data:image/svg+xml')) && decodeURIComponent(images[0].src).includes(evaluate('palette().roles.primary')) && !sampleDoc.querySelector('script');
  });
  test('Sample home page showcases actions, cards, forms, table, FAQ and progress', () => ['.card','.ds-button--primary','.ds-button--secondary','.ds-button--accent','.ds-button--outline','.ds-button--text','form input[type="email"]','select','textarea','input[type="radio"]','input[type="checkbox"]','input[type="range"]','input[readonly]','input[disabled]','table caption','details summary','progress','blockquote'].every(selector=>sampleDoc.querySelector(selector)));
  test('Field guide offers ten lesson cards with real practice destinations', () => {
    const cards=[...sampleDoc.querySelectorAll('#services .sample-lesson-card')];
    return sampleDoc.title.includes('Web Design Field Guide') && cards.length===10 && cards.every(card=>sampleDoc.getElementById(card.querySelector('a').hash.slice(1))) && sampleDoc.querySelector('header a[href="#services"]').textContent==='Lessons';
  });
  test('Grid workshop includes twelve tracks, seven layout regions and an inspectable CSS recipe', () => sampleDoc.querySelectorAll('.sample-grid-tracks > span').length===12 && sampleDoc.querySelectorAll('.sample-grid-demo > div').length===7 && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('repeat(12, minmax(0, 1fr))') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('grid-column: 1 / -1;') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('.sample-demo-card { grid-column: span 4; }') && sampleDoc.querySelector('.sample-code-solution code').textContent.includes('@media (max-width: 48rem)'));
  test('Type and colour examples describe the actual selected design settings', () => {
    const values=[...sampleDoc.querySelectorAll('.sample-type-settings dd')].map(item=>item.textContent);
    const colours=[...sampleDoc.querySelectorAll('.sample-token-palette code')].map(item=>item.textContent);
    return JSON.stringify(values)===JSON.stringify(evaluate('[state.base+"px",String(state.ratio),String(state.leading)]')) && JSON.stringify(colours)===JSON.stringify(evaluate('[palette().roles.primary,palette().roles.secondary,palette().roles.accent]'));
  });
  test('Flexbox workshop exports working examples, a shared CSS recipe and a layout comparison', () => {
    const recipe=sampleDoc.querySelector('#flex-lab code').textContent;
    return sampleDoc.querySelectorAll('.sample-flex-tags [role="listitem"]').length===3
      && sampleDoc.querySelectorAll('.sample-layout-comparison tbody tr').length===3
      && sampleDoc.querySelectorAll('.sample-lesson-card.sample-flex-stack').length===10
      && recipe.includes('flex: 1 1 12rem') && recipe.includes('margin-top: auto') && evaluate('cssExport()').includes(recipe);
  });
  test('Sample IDs and labelled controls are valid', () => {
    const ids=[...sampleDoc.querySelectorAll('[id]')].map(el=>el.id);
    return ids.length===new Set(ids).size && [...sampleDoc.querySelectorAll('label[for]')].every(label=>sampleDoc.getElementById(label.htmlFor));
  });
  input('bdState','loading'); input('advState','invalid','change');
  const selectedDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Sample markup reflects selected loading and invalid field states', () => !!selectedDoc.querySelector('.sample-selected-action[disabled][aria-busy="true"]') && selectedDoc.getElementById('contact-email').getAttribute('aria-invalid')==='true');
  test('Loading demonstrations leave section navigation and the contact action usable', () => [...selectedDoc.querySelectorAll('.sample-section-actions a')].every(link=>link.getAttribute('href')?.startsWith('#') && !link.hasAttribute('aria-disabled') && !link.hasAttribute('disabled')) && !selectedDoc.querySelector('.sample-form button[type="submit"]').disabled);
  reset(); input('jProject','Cedar Studio'); input('jRadius',24); input('advHeight',52); input('advWeight',800,'change');
  for (const theme of ['light','dark']) {
    input('jTheme',theme);
    const page=d.createElement('iframe'); page.style.cssText='width:1440px;height:1400px;border:0';
    page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{page.onload=resolve;d.body.append(page);});
    const pd=page.contentDocument, pw=page.contentWindow;
    test('Rendered '+theme+' sample applies theme, typography, radius and control height', () => {
      const heading=pw.getComputedStyle(pd.querySelector('h1')), image=pw.getComputedStyle(pd.querySelector('img')), field=pw.getComputedStyle(pd.querySelector('.input'));
      const body=pw.getComputedStyle(pd.body), expected=evaluate(`palette('${theme}').roles.background`);
      return heading.fontWeight==='800' && image.borderRadius==='24px' && parseFloat(field.minHeight)===52 && body.backgroundColor===evaluate(`'rgb('+hexRgb('${expected}').join(', ')+')'`);
    });
    test('Rendered '+theme+' hero image loads without external assets', () => pd.querySelector('#home img').complete && pd.querySelector('#home img').naturalWidth===960);
    test('Rendered '+theme+' button foreground uses the selected component token', () => pw.getComputedStyle(pd.querySelector('.ds-button--primary')).color===evaluate("'rgb('+hexRgb(dssGetButtonContrastData().themes['"+theme+"'].primary.fg).join(', ')+')'"));
    for (const width of [320,768,1440]) {
      page.style.width=width+'px'; await wait();
      test('Rendered '+theme+' home page fits '+width+'px', () => pd.documentElement.scrollWidth<=pw.innerWidth+1);
      test(theme+' section action pairs fit and keep their spacing at '+width+'px', () => [...pd.querySelectorAll('.sample-section-actions')].every(row=>{
        const bounds=row.getBoundingClientRect(), buttons=[...row.children].map(button=>button.getBoundingClientRect());
        const [first,second]=buttons;
        return buttons.every(box=>box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44) && (Math.abs(second.top-first.top)<1?second.left-first.right>=7.5:second.top-first.bottom>=7.5);
      }));
      test(theme+' header logo and project title scale at '+width+'px', () => {
        const logo=pd.querySelector('header .sample-logo'), title=pd.querySelector('header .sample-brand-title');
        const box=logo.getBoundingClientRect(), expected=evaluate(`fluidTypePx(3,${width})`);
        return logo.textContent==='Logo' && logo.getAttribute('aria-hidden')==='true' && box.width>=44 && Math.abs(box.width-box.height)<1 && logo.scrollWidth<=logo.clientWidth+1 && title.textContent==='Cedar Studio' && Math.abs(parseFloat(pw.getComputedStyle(title).fontSize)-expected)<.11;
      });
      const menu=pd.getElementById('sample-menu'), toggle=menu.querySelector('summary');
      const desktop=pd.querySelector('.sample-desktop-navigation'), mobile=pd.getElementById('sample-mobile-navigation');
      if (width<=768) {
        test(theme+' header uses a closed hamburger at '+width+'px', () => pw.getComputedStyle(desktop).display==='none' && toggle.getBoundingClientRect().width>=44 && toggle.getBoundingClientRect().height>=44 && !menu.open && mobile.getClientRects().length===0 && toggle.getAttribute('aria-controls')===mobile.id);
        toggle.focus(); toggle.click();
        test(theme+' hamburger opens and closes the navigation at '+width+'px', () => {
          const opened=menu.open && mobile.getBoundingClientRect().height>0 && mobile.querySelectorAll('a').length===6 && pw.getComputedStyle(toggle.querySelector('.sample-menu-bars')).display==='none' && pd.activeElement===toggle;
          toggle.click();
          return opened && !menu.open && mobile.getClientRects().length===0;
        });
        test(theme+' menu is borderless with default text and an accent-only icon', () => {
          const accent=evaluate(`palette('${theme}').roles.accent`), text=evaluate(`palette('${theme}').roles.text`);
          const colour=hex=>evaluate(`'rgb('+hexRgb('${hex}').join(', ')+')'`);
          const style=pw.getComputedStyle(toggle);
          return pw.getComputedStyle(toggle.querySelector('svg')).stroke===colour(accent) && style.color===colour(text) && style.backgroundColor==='rgba(0, 0, 0, 0)' && parseFloat(style.borderTopWidth)===0 && toggle.querySelector('span').textContent==='Menu';
        });
      } else {
        test(theme+' desktop navigation stays visible with its mobile menu closed', () => !menu.open && pw.getComputedStyle(menu).display==='none' && desktop.getBoundingClientRect().height>0 && desktop.querySelectorAll('a').length===6);
      }
    }
    page.remove();
  }
  reset(); await wait();
  const gridPage=d.createElement('iframe'); gridPage.style.cssText='width:1440px;height:1000px;border:0';
  const loadGridPage = async () => {
    gridPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{gridPage.onload=resolve;if(!gridPage.isConnected)d.body.append(gridPage);});
  };
  await loadGridPage();
  const gridDoc=()=>gridPage.contentDocument, gridWindow=()=>gridPage.contentWindow;
  const gridStyle=selector=>gridWindow().getComputedStyle(gridDoc().querySelector(selector));
  for (const underline of [true,false]) {
    evaluate(`adv.underline=${underline}; applyAdvanced(); renderCode();`);
    await loadGridPage(); await wait();
    test('Header navigation overrides the general underline setting '+underline+' in export and preview', () => [gridDoc(),previewDoc()].every(doc=>{
      const win=doc.defaultView;
      return [...doc.querySelectorAll('.sample-header .sample-nav a')].every(link=>win.getComputedStyle(link).textDecorationLine==='none') && win.getComputedStyle(doc.querySelector('.sample-footer .sample-nav a')).textDecorationLine===(underline?'underline':'none');
    }));
    test('All resource table links start plain with general underlines '+underline+' in export and preview', () => [gridDoc(),previewDoc()].every(doc=>{
      const links=[...doc.querySelectorAll('.sample-table-wrap a')];
      return links.length===3 && links.every(link=>doc.defaultView.getComputedStyle(link).textDecorationLine==='none');
    }));
  }
  reset(); await wait(); await loadGridPage();
  for (const theme of ['light','dark']) {
    gridDoc().documentElement.dataset.theme=theme;
    for (const width of [320,1440]) {
      gridPage.style.width=width+'px'; await wait();
      gridDoc().getElementById('sample-menu').open=width<=768;
      const link=gridDoc().querySelector(width<=768?'.sample-mobile-navigation a':'.sample-desktop-navigation a');
      const style=gridDoc().querySelector('style'), original=style.textContent;
      // Equal-specificity class substitutions exercise the exported pointer-state cascade.
      style.textContent=original.replaceAll(':hover','.review-hover').replaceAll(':active','.review-active');
      try {
        test(theme+' header navigation underlines on hover without resizing at '+width+'px', () => {
          const before=link.getBoundingClientRect(); link.classList.add('review-hover');
          const hovered=gridWindow().getComputedStyle(link), after=link.getBoundingClientRect();
          const passes=hovered.textDecorationLine==='underline' && Math.abs(before.width-after.width)<1 && Math.abs(before.height-after.height)<1;
          link.classList.remove('review-hover'); return passes;
        });
        test(theme+' header navigation adds a non-colour pressed cue at '+width+'px', () => {
          const normal=parseFloat(gridWindow().getComputedStyle(link).textDecorationThickness);
          link.classList.add('review-active'); const pressed=gridWindow().getComputedStyle(link);
          const passes=pressed.textDecorationLine==='underline' && parseFloat(pressed.textDecorationThickness)>normal;
          link.classList.remove('review-active'); return passes;
        });
        test(theme+' header navigation uses the button keyboard focus ring at '+width+'px', () => {
          link.focus(); const focus=gridWindow().getComputedStyle(link), root=gridWindow().getComputedStyle(gridDoc().documentElement);
          const expected=evaluate(`'rgb('+hexRgb('${root.getPropertyValue('--button-focus').trim()}').join(', ')+')'`);
          const passes=gridDoc().activeElement===link && link.matches(':focus-visible') && focus.outlineStyle==='solid' && focus.outlineWidth===root.getPropertyValue('--button-focus-width').trim() && focus.outlineColor===expected && focus.outlineOffset==='3px';
          link.blur(); return passes;
        });
        const resources=[...gridDoc().querySelectorAll('.sample-table-wrap a')];
        test(theme+' resource links underline on hover without resizing at '+width+'px', () => resources.every(resource=>{
          const before=resource.getBoundingClientRect(); resource.classList.add('review-hover');
          const computed=gridWindow().getComputedStyle(resource), after=resource.getBoundingClientRect();
          const passes=computed.textDecorationLine==='underline' && Math.abs(before.width-after.width)<1 && Math.abs(before.height-after.height)<1;
          resource.classList.remove('review-hover'); return passes;
        }));
        test(theme+' resource links have a stronger pressed underline at '+width+'px', () => resources.every(resource=>{
          const normal=parseFloat(gridWindow().getComputedStyle(resource).textDecorationThickness);
          resource.classList.add('review-active'); const computed=gridWindow().getComputedStyle(resource);
          const passes=computed.textDecorationLine==='underline' && parseFloat(computed.textDecorationThickness)>normal;
          resource.classList.remove('review-active'); return passes;
        }));
        test(theme+' resource links retain the shared keyboard focus ring at '+width+'px', () => resources.every(resource=>{
          resource.focus(); const computed=gridWindow().getComputedStyle(resource), root=gridWindow().getComputedStyle(gridDoc().documentElement);
          const expected=evaluate(`'rgb('+hexRgb('${root.getPropertyValue('--button-focus').trim()}').join(', ')+')'`);
          const passes=gridDoc().activeElement===resource && resource.matches(':focus-visible') && computed.outlineStyle==='solid' && computed.outlineWidth===root.getPropertyValue('--button-focus-width').trim() && computed.outlineColor===expected && computed.outlineOffset==='3px';
          resource.blur(); return passes;
        }));
      } finally { style.textContent=original; }
    }
  }
  gridPage.style.width='1440px'; await loadGridPage();
  test('Wide page uses twelve tracks with six-column halves and four-column cards', () => {
    const width=selector=>gridDoc().querySelector(selector).getBoundingClientRect().width;
    return ['.sample-hero','.sample-split','.card-grid'].every(selector=>gridStyle(selector).gridTemplateColumns.split(' ').length===12) && Math.abs(width('.sample-hero > div')*2+24-width('.sample-hero'))<1 && Math.abs(width('.card-grid > .card')*3+48-width('.card-grid'))<1;
  });
  test('Default layout padding, margins and gutters follow the 8px spacing scale', () => {
    const checks=[['main','paddingLeft',32],['.sample-hero','paddingTop',80],['.sample-section','paddingTop',64],['.card','paddingTop',24],['.sample-home h1','marginBottom',16],['.sample-lead','marginBottom',24],['.card-grid','columnGap',24],['.sample-home .input','paddingLeft',16],['.sample-home .input','paddingTop',8],['.sample-footer-inner','paddingTop',32]];
    return checks.every(([selector,prop,size])=>parseFloat(gridStyle(selector)[prop])===size);
  });
  test('Footer spacing is applied once and ordinary selects retain the surface colour', () => gridStyle('.sample-footer').paddingTop==='0px' && gridStyle('.sample-footer').marginTop==='0px' && gridStyle('select.input').backgroundColor===gridStyle('.card').backgroundColor && gridStyle('input[readonly]').backgroundColor!==gridStyle('select.input').backgroundColor);
  test('Link and button state colours survive the simplified cascade in both themes', () => {
    // Substitute classes of equal specificity to resolve pointer-state CSS in headless Chrome.
    const style=gridDoc().querySelector('style'), original=style.textContent;
    style.textContent=original.replaceAll(':hover','.review-hover').replaceAll(':active','.review-active')+'\n.ds-button { transition: none !important; }';
    try {
      return ['light','dark'].every(theme=>{
        gridDoc().documentElement.dataset.theme=theme;
        return ['primary','secondary','accent','outline','text'].every(variant=>['hover','active'].every(stateName=>[...gridDoc().querySelectorAll('.ds-button--'+variant)].every(button=>{
        button.classList.add('review-'+stateName);
        const computed=gridWindow().getComputedStyle(button), root=gridWindow().getComputedStyle(gridDoc().documentElement);
        const rgb=value=>evaluate(`'rgb('+hexRgb('${value.trim()}').join(', ')+')'`);
        const matches=computed.color===rgb(root.getPropertyValue('--button-'+variant+'-'+stateName+'-text')) && computed.backgroundColor===rgb(root.getPropertyValue('--button-'+variant+'-'+stateName));
        button.classList.remove('review-'+stateName);
        return matches;
        })));
      });
    } finally { style.textContent=original; gridDoc().documentElement.dataset.theme='light'; }
  });
  for (const width of [320,390,600,768,900,1024,1280,1440]) {
    gridPage.style.width=width+'px'; await wait();
    test('Grid and spacing fit the generated page at '+width+'px', () => {
      const doc=gridDoc(), cards=[...doc.querySelectorAll('#services .card')], row=doc.querySelector('#services .card-grid').getBoundingClientRect();
      const expected=width<476?1:width<710?2:3;
      const firstRow=cards.filter(card=>Math.abs(card.getBoundingClientRect().top-cards[0].getBoundingClientRect().top)<1);
      return doc.documentElement.scrollWidth<=width+1 && firstRow.length===expected && cards.every(card=>card.getBoundingClientRect().left>=row.left-1 && card.getBoundingClientRect().right<=row.right+1) && (width>768 || gridStyle('.sample-hero').gridTemplateColumns.split(' ').length===1);
    });
    test('Tutorial grid adapts spans and keeps every region in bounds at '+width+'px', () => {
      const doc=gridDoc(), demo=doc.querySelector('.sample-grid-demo'), bounds=demo.getBoundingClientRect(), figure=doc.querySelector('.sample-grid-figure').getBoundingClientRect(), notes=doc.querySelector('.sample-lab-notes').getBoundingClientRect();
      const columns=gridStyle('.sample-grid-demo').gridTemplateColumns.split(' ').length;
      const gap=parseFloat(gridStyle('.sample-grid-demo').columnGap), main=doc.querySelector('.sample-demo-main').getBoundingClientRect(), aside=doc.querySelector('.sample-demo-aside').getBoundingClientRect(), cards=[...doc.querySelectorAll('.sample-demo-card')];
      const spans=width<=768?[...demo.children].every(region=>Math.abs(region.getBoundingClientRect().width-bounds.width)<1):Math.abs(main.width-aside.width*2-gap)<1 && Math.abs(cards.reduce((total,card)=>total+card.getBoundingClientRect().width,0)+gap*2-bounds.width)<1;
      return columns===(width<=768?1:12) && spans && (width<=1024?notes.top>figure.bottom:notes.left>figure.right) && [...demo.children].every(region=>{const box=region.getBoundingClientRect();return box.left>=bounds.left-1 && box.right<=bounds.right+1 && region.scrollWidth<=region.clientWidth+1;});
    });
  }
  gridPage.style.width='768px'; input('advColumns',320); input('advGap',32); await loadGridPage();
  test('Card minimum width and gutter controls still change responsive column counts', () => gridStyle('.card-grid').gridTemplateColumns.split(' ').length===2 && gridStyle('.card-grid').columnGap==='32px');
  test('Tutorial grid uses the configured grid gap', () => gridStyle('.sample-grid-demo').gap==='32px');
  test('Flexbox rows share the configured grid gap', () => gridStyle('.sample-flex-row').gap==='32px' && gridStyle('.sample-flex-media').gap==='32px');
  for (const theme of ['light','dark']) {
    evaluate(`state.theme='${theme}'; apply();`); await loadGridPage();
    for (const width of [320,390,768,1280,1440]) {
      gridPage.style.width=width+'px'; await wait();
      test(theme+' Flexbox examples align, wrap and fit at '+width+'px', () => {
        const doc=gridDoc(), row=doc.querySelector('.sample-flex-row'), tags=doc.querySelector('.sample-flex-tags'), media=doc.querySelector('.sample-flex-media');
        const marker=doc.querySelector('.sample-flex-marker').getBoundingClientRect(), copy=doc.querySelector('.sample-flex-copy').getBoundingClientRect();
        const rowStyle=gridStyle('.sample-flex-row');
        return rowStyle.display==='flex' && rowStyle.flexWrap==='wrap' && rowStyle.alignItems==='center' && rowStyle.justifyContent==='space-between'
          && gridStyle('.sample-flex-copy').flexGrow==='1' && gridStyle('.sample-flex-copy').flexShrink==='1'
          && gridStyle('.sample-flex-stack').flexDirection==='column'
          && (width>390 || (tags.getBoundingClientRect().top>row.firstElementChild.getBoundingClientRect().bottom && copy.top>=marker.bottom))
          && [row,tags,media,...row.children,...media.children].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && el.scrollWidth<=el.clientWidth+1;})
          && doc.documentElement.scrollWidth<=width+1;
      });
    }
  }
  gridPage.style.width='320px'; await wait();
  test('Large custom gutters and card minimums collapse without mobile overflow', () => gridStyle('.card-grid').gridTemplateColumns.split(' ').length===1 && gridDoc().documentElement.scrollWidth<=320);
  evaluate('importConfig({spacing:3,advanced:{gap:12,height:42},buttonDesign:{padX:18,padY:12,minHeight:44}})');
  await loadGridPage();
  test('Imported spacing and component dimensions are preserved without snapping', () => evaluate('state.spacing===3 && adv.gap===12 && adv.height===42 && state.buttonDesign.padX===18 && state.buttonDesign.padY===12 && state.buttonDesign.minHeight===44') && gridStyle('.card').paddingTop==='18px' && gridStyle('.ds-button').paddingLeft==='18px' && gridStyle('.input').minHeight==='42px');
  gridPage.remove();
  reset(); await wait();
  const actionDocument=previewDoc(), actionProject=evaluate('projectJson()');
  for (const link of [...previewDoc().querySelectorAll('.sample-lesson-card a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Field-guide lesson link to '+link.getAttribute('href')+' browses its live example', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2 && evaluate('projectJson()')===actionProject);
  }
  for (const link of [...previewDoc().querySelectorAll('.sample-section-actions a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Preview '+link.closest('section').id+' action to '+link.getAttribute('href')+' browses its destination', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2 && evaluate('projectJson()')===actionProject);
  }
  test('Live preview uses the generated HTML and CSS without a second stylesheet request', () => {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return previewDoc().querySelector('h1').outerHTML===parsed.querySelector('h1').outerHTML && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && !previewDoc().querySelector('link[rel="stylesheet"]');
  });
  test('Export and live preview use Home, About, Resources and Contact footer links in order', () => {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return [parsed,previewDoc()].every(doc=>JSON.stringify([...doc.querySelectorAll('footer nav a')].map(link=>[link.textContent,link.getAttribute('href')]))===JSON.stringify([['Home','#home'],['About','#about'],['Resources','#resources'],['Contact','#contact']]));
  });
  for (const link of [...previewDoc().querySelectorAll('footer nav a')]) {
    const target=previewDoc().getElementById(link.getAttribute('href').slice(1));
    link.click(); await wait(20);
    test('Preview footer '+link.textContent+' link browses its section', () => previewDoc()===actionDocument && previewDoc().activeElement===target && Math.abs(target.getBoundingClientRect().top-24)<2);
  }
  test('Live preview sandbox supports form validation while blocking scripts and top navigation', () => {
    const sandbox=d.getElementById('previewPage').sandbox;
    return sandbox.contains('allow-same-origin') && sandbox.contains('allow-forms') && !sandbox.contains('allow-scripts') && !sandbox.contains('allow-top-navigation');
  });
  d.getElementById('dockTabHtml').click();
  d.getElementById('jSaveLocal').click();
  const themedProject=d.getElementById('jProjects').value;
  const bothThemeCss=evaluate('cssExport()');
  input('dockTheme','dark','change'); await wait();
  test('Inspector theme selection synchronizes the studio, preview and exported HTML', () => evaluate('state.theme')==='dark' && d.documentElement.dataset.theme==='dark' && d.getElementById('jTheme').value==='dark' && d.getElementById('previewTheme').value==='dark' && previewDoc().documentElement.dataset.theme==='dark' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('previewPage').title.includes('dark'));
  test('Inspector theme is saved to the active project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='dark');
  test('Theme selection retains a CSS export containing both theme definitions', () => evaluate('cssExport()')===bothThemeCss && evaluate('cssExport()').includes('[data-theme="dark"]'));
  input('previewTheme','light','change'); await wait();
  test('Preview theme control synchronizes the inspector and saved project', () => d.getElementById('dockTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='light');
  d.getElementById('themeToggle').click(); await wait();
  test('Global theme toggle keeps both new theme controls synchronized', () => d.getElementById('dockTheme').value==='dark' && d.getElementById('previewTheme').value==='dark' && previewDoc().documentElement.dataset.theme==='dark');
  evaluate('importConfig({project:"Imported theme",theme:"light"})'); await wait();
  test('Imported theme reaches both selectors and the generated preview', () => d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && previewDoc().title.includes('Imported theme'));
  input('jProject','Live preview'); input('jPrimary','#294f77'); input('bdSize','lg'); await wait();
  test('Preview imagery and component classes follow live project changes', () => previewDoc().querySelector('.sample-brand').textContent.includes('Live preview') && decodeURIComponent(previewDoc().querySelector('img').src).includes(evaluate('palette().roles.primary')) && !!previewDoc().querySelector('.ds-button--lg') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  test('Tutorial palette readouts and swatches follow live semantic roles', () => {
    const expected=evaluate('[palette().roles.primary,palette().roles.secondary,palette().roles.accent]');
    return [...previewDoc().querySelectorAll('.sample-token-palette li')].every((item,i)=>item.querySelector('code').textContent===expected[i] && previewWindow().getComputedStyle(item.querySelector('.sample-palette-dot')).backgroundColor===evaluate(`'rgb('+hexRgb('${expected[i]}').join(', ')+')'`));
  });
  test('Tutorial typography readouts follow live wizard settings', () => JSON.stringify([...previewDoc().querySelectorAll('.sample-type-settings dd')].map(item=>item.textContent))===JSON.stringify(evaluate('[state.base+"px",String(state.ratio),String(state.leading)]')));
  const browsingDoc=previewDoc(), studioHash=w.location.hash;
  previewDoc().querySelector('header a[href="#resources"]').click(); await wait();
  test('Sample navigation scrolls within the generated page without opening the studio inside it', () => previewDoc()===browsingDoc && previewWindow().scrollY>0 && Math.abs(previewDoc().getElementById('resources').getBoundingClientRect().top-24)<2 && previewWindow().location.href.startsWith('about:srcdoc') && w.location.hash===studioHash);
  previewDoc().querySelector('a[href="#working-together"]').click(); await wait();
  test('Sample resource links reveal their FAQ destination inside the preview', () => previewDoc().getElementById('working-together').open && previewDoc()===browsingDoc);
  previewDoc().getElementById('contact-name').value='Taylor';
  previewDoc().getElementById('contact-email').value='taylor@example.com';
  previewDoc().querySelector('input[name="copy"]').checked=true;
  previewDoc().querySelector('input[value="workshop"]').checked=true;
  previewWindow().scrollTo(0,500); await wait();
  const originalNameControl=previewDoc().getElementById('contact-name'), browsePosition=previewWindow().scrollY;
  input('jRadius',20); await wait();
  test('CSS-only edits preserve browsing position, controls and entered values', () => previewDoc().getElementById('contact-name')===originalNameControl && originalNameControl.value==='Taylor' && Math.abs(previewWindow().scrollY-browsePosition)<2 && previewWindow().getComputedStyle(previewDoc().querySelector('img')).borderRadius==='20px');
  input('dockTheme','dark','change'); await wait();
  test('HTML and theme refreshes preserve entered fields, choices, FAQs and scroll', () => previewDoc()===browsingDoc && previewDoc().getElementById('contact-name')!==originalNameControl && previewDoc().getElementById('contact-name').value==='Taylor' && previewDoc().querySelector('input[name="copy"]').checked && previewDoc().querySelector('input[value="workshop"]').checked && previewDoc().getElementById('working-together').open && Math.abs(previewWindow().scrollY-browsePosition)<2);
  const previewAddress=previewWindow().location.href;
  previewDoc().querySelector('form').requestSubmit(); await wait();
  test('Sample form submission remains in the preview without sending an enquiry', () => previewWindow().location.href===previewAddress && previewDoc().getElementById('contact-note').textContent.includes('No enquiry has been sent'));
  d.querySelector('button[data-width="fluid"]').click(); app.style.width='390px'; await wait();
  const firstFluidWidth=previewWindow().innerWidth;
  test('Fluid preview uses its actual available viewport at mobile width', () => Math.abs(firstFluidWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<1 && previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  app.style.width='768px'; await wait();
  test('Fluid preview follows pane resizing and retains entered form values', () => previewWindow().innerWidth>firstFluidWidth && Math.abs(previewWindow().innerWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<1 && previewDoc().getElementById('contact-name').value==='Taylor');
  input('jProject','Safe </style><script>parent.__previewInjection=1</scr'+'ipt>'); await wait();
  test('Preview inserts generated CSS as text and keeps project markup escaped', () => !w.__previewInjection && !previewDoc().querySelector('script') && previewDoc().querySelector('.sample-brand').textContent.includes('</style><script>') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && previewDoc().styleSheets[0].cssRules.length>0);
  reset(); await wait();
  d.querySelector('button[data-width="mobile"]').click(); await wait();
  previewDoc().getElementById('sample-menu').querySelector('summary').click();
  input('jAccent','#D97706'); await wait();
  test('Open preview hamburger follows live accent edits and retains its open state', () => previewDoc().getElementById('sample-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-menu-icon')).stroke==='rgb(217, 119, 6)' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  input('dockTheme','dark','change'); await wait();
  test('Preview hamburger follows the dark theme accent', () => previewDoc().getElementById('sample-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-menu-icon')).stroke===evaluate("'rgb('+hexRgb(palette('dark').roles.accent).join(', ')+')'"));
  const beforeMenuNavigation=evaluate('projectJson()');
  previewDoc().getElementById('sample-mobile-navigation').querySelector('a[href="#services"]').click(); await wait();
  test('Opened mobile menu links browse the generated page without changing its project settings', () => Math.abs(previewDoc().getElementById('services').getBoundingClientRect().top-24)<2 && previewWindow().location.href.startsWith('about:srcdoc') && evaluate('projectJson()')===beforeMenuNavigation);
  const menuProject=evaluate('projectJson()');
  previewDoc().getElementById('sample-menu').querySelector('summary').click();
  test('Closing the mobile menu changes only the preview disclosure', () => !previewDoc().getElementById('sample-menu').open && evaluate('projectJson()')===menuProject);
  input('jProject','A long project name that should wrap beside the mobile menu without hiding the navigation'); await wait();
  test('Mobile header accommodates long project names without overflowing', () => previewDoc().documentElement.scrollWidth<=previewDoc().documentElement.clientWidth+1 && previewDoc().getElementById('sample-menu').querySelector('summary').getBoundingClientRect().width>=44);
  reset(); await wait();
  const previousHeaderSize=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontSize);
  input('jProject','Harbour House'); input('jRatio',1.4); await wait();
  test('Live header title follows the project name and heading typography', () => previewDoc().querySelector('header .sample-brand-title').textContent==='Harbour House' && previewDoc().querySelector('header .sample-logo').textContent==='Logo' && parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontSize)>previousHeaderSize && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  reset(); await wait();
  test('Reset restores the light theme across the inspector and preview', () => d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light');
  test('System fonts remain the offline default in the studio, preview and HTML export', () => evaluate('state.fontSettings.source')==='system' && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && !evaluate('htmlExport()').includes('fonts.googleapis.com') && d.getElementById('fontFallback').disabled);
  input('fontSystemHeading','georgia','change'); await wait();
  test('Separate system heading and body fonts reach specimens and the generated page', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Georgia') && w.getComputedStyle(d.querySelector('#mobileType [data-font-role="body"]')).fontFamily.includes('Arial') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Georgia') && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Arial'));
  evaluate(`importConfig({font:"Georgia, 'Times New Roman', serif"})`); await wait();
  test('Legacy font projects import without opting in to network fonts', () => evaluate('state.fontSettings.source==="system" && state.fontSettings.systemHeading==="same"') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Georgia') && !d.querySelector('link[data-dss-font]'));
  evaluate('importConfig({fontSettings:{source:"https://evil.invalid",body:"Inter; color:red",heading:"__proto__",systemHeading:"bad",weights:["400",-1,400,500,10000]}})');
  test('Font imports reject arbitrary sources, family CSS and invalid weights', () => evaluate('state.fontSettings.source==="system" && state.fontSettings.body==="inter" && state.fontSettings.heading==="same" && state.fontSettings.systemHeading==="same" && JSON.stringify(state.fontSettings.weights)==="[400,500]"') && !evaluate('cssExport()+htmlExport()').includes('evil.invalid'));
  reset(); await wait();
  // Serve deterministic local font-face fixtures; the separate live-CDN smoke check
  // verifies real downloads without making this regression suite depend on Google.
  let fontFixtureMode='ok';
  const fontRequests=[], fontRestores=[];
  for (const doc of [d, previewDoc()]) {
    const head=doc.head, originalAppend=head.append;
    head.append=function(...nodes) {
      for (const node of nodes) if (node.tagName==='LINK' && node.href?.startsWith('https://fonts.')) {
        const originalUrl=new URL(node.href);
        if (node.rel==='stylesheet') {
          fontRequests.push(node.href);
          node.href='/__font_fixture__'+originalUrl.search+'&mode='+fontFixtureMode;
        } else node.href=w.location.origin;
      }
      return originalAppend.apply(this,nodes);
    };
    fontRestores.push(()=>{head.append=originalAppend;});
  }
  d.getElementById('jSaveLocal').click();
  const fontProjectId=d.getElementById('jProjects').value;
  input('fontSource','google','change');
  test('Google font selection reports loading and enables the CDN controls', () => d.getElementById('fontLoadStatus').dataset.state==='loading' && !d.getElementById('fontGoogleOptions').hidden && d.getElementById('font').disabled && d.getElementById('jFont').disabled);
  await wait(250);
  test('Font stylesheets and font faces load successfully through the browser', () => d.getElementById('fontLoadStatus').dataset.state==='loaded' && [...d.fonts].some(face=>face.family.includes('Inter') && face.status==='loaded') && [...previewDoc().fonts].some(face=>face.family.includes('Inter') && face.status==='loaded'));
  test('A shared heading/body family produces one family request per document', () => fontRequests.length===2 && fontRequests.every(href=>new URL(href).searchParams.getAll('family').length===1));
  input('fontGoogleHeading','literata','change'); await wait(250);
  test('Google heading/body selections update specimens, components and the preview', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Literata') && w.getComputedStyle(d.querySelector('#mobileType [data-font-role="body"]')).fontFamily.includes('Inter') && w.getComputedStyle(d.querySelector('.bd-button')).fontFamily.includes('Inter') && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().querySelector('.sample-brand-title')).fontFamily.includes('Literata') && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter'));
  const fontExport=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('HTML exports include deduplicated preconnects, crossorigin and the CSS2 font request', () => fontExport.querySelectorAll('link[rel="preconnect"]').length===2 && fontExport.querySelector('link[href="https://fonts.gstatic.com"]').hasAttribute('crossorigin') && fontExport.querySelector('link[href^="https://fonts.googleapis.com/css2?"]').getAttribute('href')===evaluate('DSStudio.fonts.url()') && evaluate('htmlExport()').includes('&amp;display=swap'));
  test('Font requests include selected families, page weights and italic body copy', () => {
    const request=new URL(evaluate('DSStudio.fonts.url()'));
    return request.searchParams.get('display')==='swap' && request.searchParams.getAll('family').join('|').includes('Inter:ital,wght@0,400;0,600;0,700;1,400') && request.searchParams.getAll('family').join('|').includes('Literata:wght@400;600;700');
  });
  d.getElementById('fontWeight500').click(); input('advWeight',800,'change'); input('bdWeight',700); await wait(250);
  test('Optional and currently used weights stay represented in generated requests', () => evaluate('DSStudio.fonts.url()').includes('0,500') && evaluate('DSStudio.fonts.url()').includes('0,800') && d.getElementById('fontWeight800').checked && d.getElementById('fontWeight800').disabled && d.getElementById('fontWeight400').disabled);
  evaluate('importConfig({...JSON.parse(projectJson()),buttonDesign:{...state.buttonDesign,weight:650}})'); await wait(250);
  test('Font requests use the validated button weight after import', () => evaluate('state.buttonDesign.weight===600 && !DSStudio.fonts.url().includes("0,650")') && evaluate('cssExport()').includes('--button-font-weight: 600'));
  input('bdWeight',700); await wait(250);
  test('Font settings autosave with the active local project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[fontProjectId].data.fontSettings.heading==='literata' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[fontProjectId].data.fontSettings.weights.includes(500));
  test('Learning examples match the actual HTML links and font tokens', () => d.getElementById('fontHtmlCode').textContent===evaluate('DSStudio.fonts.htmlLinks()') && d.getElementById('fontCssCode').textContent.includes('--font-heading: "Literata"') && evaluate('cssExport()').includes('--font-body: "Inter"') && evaluate('cssExport()').includes('--font-ui: var(--font-body)'));
  const fontCssBefore=evaluate('cssExport()'), fontHtmlBefore=evaluate('htmlExport()'), fontJsonBefore=evaluate('projectJson()');
  const mainFontLink=d.querySelector('link[data-dss-font][rel="stylesheet"]'), previewFontLink=previewDoc().querySelector('link[data-dss-font][rel="stylesheet"]');
  input('jRadius',20); await wait();
  test('Unrelated live edits preserve existing font stylesheet nodes', () => d.querySelector('link[data-dss-font][rel="stylesheet"]')===mainFontLink && previewDoc().querySelector('link[data-dss-font][rel="stylesheet"]')===previewFontLink);
  input('jRadius',12); await wait();
  const beforeFallbackRequests=fontRequests.length;
  d.getElementById('fontFallback').click(); await wait();
  test('Fallback comparison updates samples and preview without altering saved settings or exports', () => w.getComputedStyle(d.querySelector('#mobileType [data-font-role="heading"]')).fontFamily.includes('Georgia') && !previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter') && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && d.getElementById('fontLoadStatus').dataset.state==='fallback' && evaluate('cssExport()')===fontCssBefore && evaluate('htmlExport()')===fontHtmlBefore && evaluate('projectJson()')===fontJsonBefore && fontRequests.length===beforeFallbackRequests);
  d.getElementById('fontFallback').click(); await wait(250);
  test('Turning comparison off restores selected fonts in the same preview document', () => previewDoc().documentElement.dataset.theme==='light' && previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontFamily.includes('Literata') && d.getElementById('fontLoadStatus').dataset.state==='loaded');
  const fontRoundTrip=evaluate('projectJson()');
  reset(); evaluate('importConfig('+fontRoundTrip+')'); await wait(250);
  test('Font selections and weights survive JSON import and reset clears comparison', () => evaluate('state.fontSettings.heading==="literata" && state.fontSettings.body==="inter" && state.fontSettings.weights.includes(500)') && d.getElementById('fontSource').value==='google' && !d.getElementById('fontFallback').checked && previewWindow().getComputedStyle(previewDoc().body).fontFamily.includes('Inter'));
  fontFixtureMode='error'; input('fontGoogleBody','source-sans-3','change'); await wait(250);
  test('A failed font stylesheet offers readable fallbacks and a retry action', () => d.getElementById('fontLoadStatus').dataset.state==='error' && !d.getElementById('fontRetry').hidden && previewDoc().querySelector('h1').getBoundingClientRect().height>0);
  fontFixtureMode='ok'; d.getElementById('fontRetry').click(); await wait(250);
  // Offscreen iframe text may defer font use until painted; explicitly request
  // the face to verify that retry made it available to the preview document.
  await previewDoc().fonts.load('400 16px "Source Sans 3"');
  test('Retry recovers both selected font families without resetting the project', () => {
    const report={status:d.getElementById('fontLoadStatus').dataset.state,body:evaluate('state.fontSettings.body'),faces:[...previewDoc().fonts].map(face=>({family:face.family,status:face.status})),links:[...previewDoc().querySelectorAll('link[data-dss-font]')].map(link=>link.href)};
    if (report.status!=='loaded' || report.body!=='source-sans-3' || !report.faces.some(face=>face.family.includes('Source Sans 3') && face.status==='loaded')) throw Error(JSON.stringify(report));
    return true;
  });
  input('fontSource','system','change'); await wait();
  test('Switching to system fonts removes all managed font connections and restores body controls', () => !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]') && !d.getElementById('font').disabled && !d.getElementById('jFont').disabled && !evaluate('htmlExport()').includes('fonts.googleapis.com'));
  fontFixtureMode='error'; input('fontSource','google','change'); input('fontSource','system','change'); await wait(250);
  test('Stale font callbacks cannot replace the status after switching back to system fonts', () => d.getElementById('fontLoadStatus').dataset.state==='system' && !d.querySelector('link[data-dss-font]') && !previewDoc().querySelector('link[data-dss-font]'));
  for (const restore of fontRestores) restore();
  reset(); await wait();
  d.getElementById('dockTabCss').click();
  for (const theme of ['light','dark']) {
    input('dockTheme',theme,'change'); input('bdVariant','secondary'); input('bdSource','custom'); input('bdCustom','#b52266'); await wait();
    // Resolve live styles without transition timing affecting the sampled colour.
    const motion=previewDoc().createElement('style'); motion.textContent='.ds-button { transition: none !important; }'; previewDoc().head.append(motion);
    const secondaryActions=()=>[...previewDoc().querySelectorAll('.sample-section-actions > :last-child')];
    test(theme+' secondary custom base colour updates every page action pair', () => secondaryActions().length===9 && secondaryActions().every(action=>action.matches('a.ds-button--secondary') && previewWindow().getComputedStyle(action).backgroundColor==='rgb(181, 34, 102)'));
    test(theme+' secondary edits keep primary actions and the outline example independent', () => previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(0, 71, 128)' && !!previewDoc().querySelector('#components .ds-button--outline'));
    input('bdCustom','#196b63'); await wait();
    test(theme+' repeated custom colour edits reach the live page without a palette change', () => secondaryActions().every(action=>previewWindow().getComputedStyle(action).backgroundColor==='rgb(25, 107, 99)') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
    test(theme+' wizard and page show the same secondary default colour', () => w.getComputedStyle(d.querySelector('#bdSingle .bd-button')).backgroundColor===previewWindow().getComputedStyle(secondaryActions()[0]).backgroundColor);
  }
  const secondaryExport=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Secondary custom-colour exports use the matching variant for all section actions', () => [...secondaryExport.querySelectorAll('.sample-section-actions > :last-child')].every(action=>action.classList.contains('ds-button--secondary')) && evaluate('cssExport()').includes('--button-secondary-bg: #196b63'));
  reset(); await wait();
  d.querySelector('[data-journey-step="4"]').click(); await wait();
  const brandSelect=role=>d.getElementById('j'+role[0].toUpperCase()+role.slice(1)+'Brand');
  const brandField=(id,field)=>d.querySelector(`[data-brand-id="${id}"] [data-brand-field="${field}"]`);
  const editBrand=(id,field,value)=>{const el=brandField(id,field);el.value=value;el.dispatchEvent(new w.Event(field==='name'?'change':'input',{bubbles:true}));};
  test('Guided Brand Palette lists all starter colours and all three role dropdowns', () => d.querySelectorAll('#jBrandSwatches li').length===11 && ['primary','secondary','accent'].every(role=>brandSelect(role).options.length===12 && [...brandSelect(role).options].slice(1).every(option=>/^#[0-9A-F]{6}$/.test(option.value) && option.textContent.includes(option.value))));
  for (const [role,hex] of [['primary','#00BADC'],['secondary','#F37327'],['accent','#004780']]) {
    input(brandSelect(role).id,hex,'change'); await wait();
    test('Brand selection updates '+role+' across main and guided controls and live CSS', () => evaluate(`state.${role}`)===hex.toLowerCase() && d.getElementById(role).value===hex.toLowerCase() && d.getElementById('j'+role[0].toUpperCase()+role.slice(1)).value===hex.toLowerCase() && previewDoc().getElementById('dssPreviewStyles').textContent.includes('--'+role+'-500: '+hex));
  }
  input('jSecondary','#123456'); await wait();
  test('Manual role colours remain available and show Custom in the brand dropdown', () => brandSelect('secondary').value==='' && evaluate('state.secondary')==='#123456');
  input('primary','#F37327'); await wait();
  test('Advanced role edits synchronize the matching guided brand choice', () => brandSelect('primary').value==='#F37327');
  d.getElementById('jBrandEditor').closest('details').open=true;
  d.getElementById('jBrandAdd').click(); await wait();
  test('Adding a named brand colour offers an editable focused row', () => evaluate('state.brandPalette.length')===12 && d.activeElement===brandField('colour-1','name'));
  editBrand('colour-1','name','Harbour teal');
  const mainBeforeBrandEdit=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
  const stableBrandPicker=brandField('colour-1','hex'); stableBrandPicker.focus();
  editBrand('colour-1','hex','#246a68'); await wait();
  test('Editing a brand reference preserves Main Palette choices and editor focus', () => evaluate('JSON.stringify([state.primary,state.secondary,state.accent])')===mainBeforeBrandEdit && brandField('colour-1','hex')===stableBrandPicker && d.activeElement===stableBrandPicker);
  test('Custom brand colours reach dropdowns, reference swatches, export and contrast candidates', () => ['primary','secondary','accent'].every(role=>[...brandSelect(role).options].some(option=>option.value==='#246A68' && option.textContent.includes('Harbour teal'))) && d.getElementById('brandSwatches').textContent.includes('Harbour teal') && evaluate('cssExport()').includes('--brand-colour-1: #246A68') && report().some(row=>row.name==='Brand: Harbour teal (--brand-colour-1) / white text' && row.bg==='#246A68'));
  input('jAccentBrand','#246A68','change'); d.getElementById('jSaveLocal').click();
  const brandProjectId=d.getElementById('jProjects').value;
  editBrand('blue','hex','#224488'); await wait();
  test('Brand palette edits autosave without overwriting independent role choices', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[brandProjectId].data.brandPalette.find(item=>item.id==='blue').hex==='#224488' && evaluate('state.accent')==='#246a68');
  const brandedProject=evaluate('projectJson()');
  reset(); evaluate('importConfig('+brandedProject+')'); await wait();
  test('Brand palette names, token IDs, colours and role selections survive JSON round trip', () => evaluate('state.brandPalette.length')===12 && brandField('colour-1','name').value==='Harbour teal' && brandSelect('accent').value==='#246A68' && evaluate('cssExport()').includes('--brand-blue: #224488'));
  d.querySelector('[data-remove-brand="colour-1"]').click(); await wait();
  test('Removing a selected brand reference keeps its UI colour and removes obsolete exports', () => evaluate('state.accent')==='#246a68' && brandSelect('accent').value==='' && !evaluate('cssExport()').includes('--brand-colour-1:') && !report().some(row=>row.name.includes('--brand-colour-1')) && d.activeElement.id==='jBrandAdd');
  evaluate('importConfig({primary:"#123456",secondary:"#456789",accent:"#987654"})'); await wait();
  test('Older projects receive starter brand references while retaining custom Main Palette colours', () => evaluate('state.brandPalette.length===11 && state.primary==="#123456" && state.secondary==="#456789" && state.accent==="#987654"') && ['primary','secondary','accent'].every(role=>brandSelect(role).value===''));
  evaluate('importConfig({brandPalette:[{id:"safe",name:"<img src=x onerror=alert(1)>",hex:"#abcdef"},{id:"bad;css",name:"Bad",hex:"#ffffff"},{id:"badhex",name:"Bad",hex:"red;position:fixed"},{id:"safe",name:"Duplicate",hex:"#000000"}]})'); await wait();
  test('Imported brand palettes reject duplicate IDs, CSS injection and invalid colours', () => evaluate('state.brandPalette.length===1 && state.brandPalette[0].id==="safe" && state.brandPalette[0].hex==="#ABCDEF"') && evaluate('cssExport()').includes('--brand-safe: #ABCDEF') && !evaluate('cssExport()').includes('--brand-bad'));
  test('Imported brand names are rendered as text in every palette surface', () => d.getElementById('jBrandSwatches').textContent.includes('<img') && !d.querySelector('#jBrandSwatches img, #brandSwatches img') && [...brandSelect('primary').options].some(option=>option.textContent.includes('<img')));
  test('The final remaining brand colour cannot be removed', () => d.querySelector('[data-remove-brand="safe"]').disabled);
  evaluate('importConfig({brandPalette:[{id:"one",name:"primary-500",hex:"#123456"},{id:"two",name:"primary-500",hex:"#654321"}]})'); await wait();
  test('Duplicate brand names retain unique contrast identities and cannot impersonate ramp anchors', () => {
    const rows=report().filter(row=>row.name.startsWith('Brand: primary-500'));
    return rows.length===8 && new Set(rows.map(row=>row.id)).size===8 && rows.every(row=>row.targets.every(target=>target.type!=='anchor'));
  });
  evaluate('importConfig({brandPalette:Array.from({length:30},(_,i)=>({id:"test-"+i,name:"A".repeat(90),hex:"#123456"}))})'); await wait();
  test('Imported palettes enforce 24 colours and bounded names', () => evaluate('state.brandPalette.length===24 && state.brandPalette.every(item=>item.name.length===40)') && d.getElementById('jBrandAdd').disabled);
  for (const theme of ['light','dark']) {
    app.style.width='320px'; input('jTheme',theme); d.querySelector('[data-journey-step="4"]').click();
    d.getElementById('jBrandEditor').closest('details').open=true; await wait();
    test('Brand editing and role dropdowns fit '+theme+' 320px layouts', () => [d.getElementById('jBrandEditor'),d.getElementById('jBrandSwatches'),...['primary','secondary','accent'].map(brandSelect)].every(el=>el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset restores starter Brand Palette and Main Palette choices', () => evaluate('state.brandPalette.length===11') && brandSelect('primary').value==='#004780' && brandSelect('secondary').value==='#495965' && brandSelect('accent').value==='#CBDB2A');
  d.getElementById('brandPalette').open=true;
  const swatch=id=>d.querySelector(`[data-brand-swatch="${id}"]`);
  test('Brand Colour Palette names its purpose and replaces the whole-project reset with editing', () => d.querySelector('#brandPalette > summary h2').textContent==='6. Brand Colour Palette' && !d.getElementById('restoreDefaults') && d.getElementById('brandEditPalette').textContent==='Edit Brand Palette');
  test('Every brand swatch has one complete clickable card with an explicit role action', () => d.querySelectorAll('#brandSwatches .brand-swatch').length===11 && [...d.querySelectorAll('#brandSwatches .brand-swatch')].every(card=>card.querySelectorAll('button').length===1 && !!card.querySelector('button .brand-swatch-color') && card.querySelector('button').getAttribute('aria-label').startsWith('Set Primary UI colour to') && d.getElementById(card.querySelector('button').getAttribute('aria-describedby'))===card.querySelector('[data-brand-usage]')));
  const beforeRoleChoice=evaluate('projectJson()'); input('brandApplyRole','secondary','change'); await wait();
  test('Choosing a target role prepares every card without changing project colours', () => evaluate('projectJson()')===beforeRoleChoice && [...d.querySelectorAll('#brandSwatches button')].every(button=>button.dataset.brandRole==='secondary' && button.textContent.includes('Set as Supporting colour')));
  d.getElementById('jSaveLocal').click(); const swatchProjectId=d.getElementById('jProjects').value;
  const roleLabels={primary:'Primary UI colour',secondary:'Supporting colour',accent:'Accent colour'};
  for (const [role,id,hex] of [['primary','accent-orange','#F37327'],['secondary','white','#FFFFFF'],['accent','blue','#004780']]) {
    input('brandApplyRole',role,'change');
    const priorRoles=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
    const beforeSwatchPalette=evaluate('JSON.stringify(state.brandPalette)');
    const action=swatch(id).querySelector('button'); action.focus();
    // Click the colour block itself, rather than only the text label.
    swatch(id).querySelector('.brand-swatch-color').click(); await wait();
    test('Any swatch can set '+role+' and visibly confirm its assignment', () => evaluate(`state.${role}`)===hex.toLowerCase() && swatch(id).querySelector('[data-brand-usage]').textContent.includes(roleLabels[role]) && swatch(id).dataset.current==='true' && d.getElementById('brandFeedback').textContent.includes(roleLabels[role]+' set to') && d.getElementById('brandFeedback').textContent.includes(hex));
    test(role+' swatch updates preserve other roles, brand references and keyboard focus', () => {
      const prior=JSON.parse(priorRoles),after=JSON.parse(evaluate('JSON.stringify([state.primary,state.secondary,state.accent])'));
      return ['primary','secondary','accent'].every((key,i)=>key===role || prior[i]===after[i]) && evaluate('JSON.stringify(state.brandPalette)')===beforeSwatchPalette && swatch(id).querySelector('button')===action && d.activeElement===action;
    });
    test(role+' swatch stays synchronized with summary, guided controls, preview and local save', () => d.getElementById('brandCurrent'+role[0].toUpperCase()+role.slice(1)).textContent.includes(hex) && brandSelect(role).value===hex && previewWindow().getComputedStyle(previewDoc().documentElement).getPropertyValue('--button-'+role+'-bg').trim().toUpperCase()===hex && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[swatchProjectId].data[role]===hex.toLowerCase());
  }
  input('brandApplyRole','secondary','change'); d.getElementById('brandFeedback').textContent=''; swatch('blue').querySelector('[data-brand-usage]').click(); await wait();
  test('Clicking the usage footer applies the swatch just like its colour and label', () => evaluate('state.secondary')==='#004780' && d.getElementById('brandFeedback').textContent.includes('Supporting colour set to Deep blue'));
  const beforeEditShortcut=evaluate('projectJson()'); d.getElementById('brandEditPalette').click(); await wait();
  test('Edit Brand Palette opens the guided editor, focuses its name control and preserves the project', () => !d.querySelector('[data-journey-pane="4"]').hidden && d.getElementById('jBrandEditor').closest('details').open && d.activeElement===d.getElementById('jBrandEditor').querySelector('input') && evaluate('projectJson()')===beforeEditShortcut);
  const existingBlueCard=swatch('blue'); editBrand('blue','name','Harbour blue'); await wait();
  test('Renaming a brand reference updates cards and current assignments without recreating controls', () => swatch('blue')===existingBlueCard && swatch('blue').querySelector('strong').textContent==='Harbour blue' && d.getElementById('brandCurrentAccent').textContent.includes('Harbour blue'));
  input('brandApplyRole','primary','change'); input('jPrimary','#13579b'); await wait();
  test('Custom role edits clear current-card styling and update the visible summary', () => d.getElementById('brandCurrentPrimary').textContent==='Custom colour · #13579B' && !d.querySelector('#brandSwatches [data-current="true"]'));
  input('jPrimary','#004780'); await wait();
  test('Guided dropdowns and swatch cards reflect the same current colour', () => swatch('blue').dataset.current==='true' && swatch('blue').querySelector('[data-brand-usage]').textContent.includes('Primary UI colour') && swatch('blue').querySelector('[data-brand-usage]').textContent.includes('Accent colour'));
  for (const theme of ['light','dark']) {
    app.style.width='320px'; input('jTheme',theme); await wait();
    test('Swatch actions and current role summaries fit '+theme+' 320px layouts', () => [d.getElementById('brandRoleAssignments'),d.getElementById('brandApplyRole'),...d.querySelectorAll('#brandSwatches .brand-swatch')].every(el=>el.getBoundingClientRect().width>0 && el.getBoundingClientRect().width<=w.innerWidth && el.scrollWidth<=el.clientWidth+1));
  }
  reset(); app.style.width='1440px'; await wait();
  test('Reset restores the swatch target and current-role feedback', () => d.getElementById('brandApplyRole').value==='primary' && d.getElementById('brandCurrentPrimary').textContent.includes('#004780') && swatch('blue').dataset.current==='true');
  reset(); await wait(); input('tokenSearch','');
  d.querySelector('[data-journey-step="10"]').click();
  test('Wizard reaches its eleventh step and returns without implying completed checks', () => !d.querySelector('[data-journey-pane="10"]').hidden && d.getElementById('jNext').hidden && d.getElementById('jProgress').textContent.includes('Step 11 of 11') && !d.querySelector('.journey-steps .is-complete'));
  d.getElementById('jBack').click();
  test('Back navigation reaches accessibility and restores Next', () => !d.querySelector('[data-journey-pane="9"]').hidden && !d.getElementById('jNext').hidden);
  for (const [name,scope,control,step] of [['--space-6','Light / base','jSpacing',8],['--grid-gap','Light / base','advGap',8],['--text-h1','Light / base','clampFactor',5],['--text','Dark','jSemanticRole',6],['--button-secondary-hover-text','Dark','bdHoverText',7],['--brand-blue','Light / base',null,4]]) {
    d.getElementById('studio-section-8').open=true;
    const button=d.querySelector(`[data-token-name="${name}"][data-token-scope="${scope}"]`);
    button.click(); await wait();
    test(name+' catalogue action reveals and focuses its wizard source', () => {
      const focused=d.activeElement;
      return !d.querySelector(`[data-journey-pane="${step}"]`).hidden && (control?focused===d.getElementById(control):focused.matches('[data-brand-id="blue"] [data-brand-field="hex"]')) && focused.getBoundingClientRect().width>0 && (scope!=='Dark' || evaluate('state.theme')==='dark');
    });
  }
  test('Button token routing selects the matching variant', () => evaluate('state.buttonDesign.variant')==='secondary');
  test('Semantic catalogue routing retains the intended theme role', () => d.getElementById('jSemanticRole').value==='text');
  test('Constant-sized body text and the base scale step route to the base-size control', () => ['--text-step-2','--text-body','--text-small'].every(name=>w.dssTokenSource({name}).control==='jBase'));
  d.querySelector('[data-journey-step="5"]').click(); d.getElementById('jSaveLocal').click();
  input('jHeadingLeading',1.4); await wait();
  test('Wizard heading line-height updates exported CSS and rendered page', () => evaluate('state.headingLeading===1.4 && cssExport().includes("--heading-leading: 1.4;")') && Math.abs(parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).lineHeight)/parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('h1')).fontSize)-1.4)<.01);
  test('Heading line-height autosaves to the active local project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[d.getElementById('jProjects').value].data.headingLeading===1.4);
  input('jLeading',1.7); input('advWeight',800,'change'); await wait();
  test('Typography ladder follows heading and body line-height settings', () => [...d.querySelectorAll('#typeLadder .sample')].every(sample=>{
    const style=w.getComputedStyle(sample), expected=sample.dataset.fontRole==='heading'?1.4:1.7;
    return Math.abs(parseFloat(style.lineHeight)/parseFloat(style.fontSize)-expected)<.01;
  }));
  test('Heading specimens and ladder follow the selected heading weight', () => [...d.querySelectorAll('#mobileType [data-font-role="heading"],#desktopType [data-font-role="heading"],#typeLadder [data-font-role="heading"]')].every(sample=>w.getComputedStyle(sample).fontWeight==='800') && [...d.querySelectorAll('#typeLadder [data-font-role="body"]')].every(sample=>w.getComputedStyle(sample).fontWeight==='400'));
  test('Spacing chart lists exactly the numbered spacing tokens in the CSS export', () => {
    const shown=[...d.querySelectorAll('#spacingBars .space-row span')].map(span=>'--'+span.firstChild.textContent);
    const exported=w.dssReadTokens().filter(row=>/^--space-\d+$/.test(row.name)).map(row=>row.name);
    return JSON.stringify(shown)===JSON.stringify(exported) && !shown.includes('--space-3');
  });
  input('jSpacing',8); await wait();
  test('Spacing chart labels update from the same source as exported tokens', () => [...d.querySelectorAll('#spacingBars .space-row span')].every(span=>parseInt(span.lastChild.textContent)===Number(span.firstChild.textContent.split('-')[1])*8) && evaluate('cssExport()').includes('--space-unit: 8px;'));
  input('jSpacing',4);
  const headingProject=evaluate('projectJson()'); evaluate('importConfig('+headingProject+')'); await wait();
  test('Heading line-height survives JSON imports and synchronizes the wizard', () => evaluate('state.headingLeading')===1.4 && d.getElementById('jHeadingLeading').value==='1.4');
  evaluate('importConfig({headingLeading:99})'); await wait();
  test('Imported heading line-height is bounded and old projects keep the default', () => {
    const bounded=evaluate('state.headingLeading')===1.6;
    evaluate('importConfig({})'); return bounded && evaluate('state.headingLeading')===1.18;
  });
  for (const theme of ['light','dark']) {
    input('jTheme',theme); app.style.width='320px';
    for (const step of [5,8,9,10]) {
      d.querySelector(`[data-journey-step="${step}"]`).click();
      d.querySelectorAll(`[data-journey-pane="${step}"] details:not([hidden])`).forEach(details=>details.open=true);
      await wait();
      test(theme+' expanded wizard step '+(step+1)+' fits 320px', () => d.documentElement.scrollWidth<=320 && d.querySelector(`[data-journey-pane="${step}"]`).scrollWidth<=d.querySelector(`[data-journey-pane="${step}"]`).clientWidth+1);
    }
  }
  app.style.width='1440px'; reset(); await wait();
  const teachingProject=evaluate('projectJson()');
  d.querySelector('#studio-section-3 [data-configure-step]').click();
  test('Lesson configuration shortcuts open the wizard without changing the design', () => !d.querySelector('[data-journey-pane="8"]').hidden && evaluate('projectJson()')===teachingProject && d.activeElement===d.querySelector('[data-journey-pane="8"] h3'));
  d.querySelector('[data-journey-pane="8"] > button:last-child').click(); await wait();
  test('Wizard exploration opens the related centre lesson', () => d.getElementById('studio-section-3').open && evaluate('projectJson()')===teachingProject);
  // Measure settled geometry independently of the preceding smooth lesson jump
  // and browser scroll anchoring while the iframe changes viewport widths.
  d.documentElement.style.scrollBehavior='auto';
  d.documentElement.style.overflowAnchor='none';
  w.scrollTo({top:w.scrollY,behavior:'instant'});
  for (const width of [320,390,768,1280,1440,2560]) {
    app.style.width=width+'px'; await wait();
    const section=d.getElementById('studio-section-1'); section.open=true;
    await wait();
    section.scrollIntoView({block:'start',behavior:'instant'}); await wait();
    test('Section menu stays visible beneath the sticky header at '+width+'px', () => {
      const nav=d.querySelector('.studio-section-nav'), box=nav.getBoundingClientRect(), header=d.querySelector('.topbar').getBoundingClientRect();
      return w.getComputedStyle(nav).position==='sticky' && box.top>=header.bottom-1 && box.top<=header.bottom+2 && box.bottom<w.innerHeight && nav.querySelectorAll('a').length===15 && [...nav.querySelectorAll('a')].every(link=>link.getBoundingClientRect().height>=44) && d.documentElement.scrollWidth<=w.innerWidth+1;
    });
    test('Section navigation keeps headings below the sticky header at '+width+'px', () => {
      const header=d.querySelector('.topbar').getBoundingClientRect();
      const nav=d.querySelector('.studio-section-nav'), sticky=w.getComputedStyle(nav).position==='sticky';
      const bottom=Math.max(header.bottom,sticky?nav.getBoundingClientRect().bottom:0);
      const top=section.querySelector('summary').getBoundingClientRect().top;
      if (top>=bottom+7 && section.querySelector('summary').getBoundingClientRect().bottom<=w.innerHeight) return true;
      throw Error(JSON.stringify({width,top,bottom,header:header.bottom,nav:nav.getBoundingClientRect().bottom,offset:w.getComputedStyle(d.documentElement).getPropertyValue('--studio-section-scroll-offset')}));
    });
    test('Keyboard focus can reveal the last section-menu link at '+width+'px', () => {
      const nav=d.querySelector('.studio-section-nav'), last=nav.querySelector('a:last-child');
      last.focus(); const box=last.getBoundingClientRect(), bounds=nav.getBoundingClientRect();
      const passes=d.activeElement===last && box.left>=bounds.left && box.right<=bounds.right && d.documentElement.scrollWidth<=w.innerWidth+1;
      last.blur(); nav.scrollLeft=0; return passes;
    });
  }
  d.documentElement.style.removeProperty('scroll-behavior');
  d.documentElement.style.removeProperty('overflow-anchor');
  evaluate('importConfig({ratio:1.25})'); await wait();
  test('Previously saved Major Third projects retain their explicit scale', () => evaluate('state.ratio===1.25') && d.getElementById('jScalePreset').value==='major-third');
  evaluate('importConfig({})'); await wait();
  test('Projects without a ratio inherit the Minor Third default', () => evaluate('state.ratio===1.2') && d.getElementById('clampScalePreset').value==='minor-third');
  input('jRatio',1.4); d.getElementById('jNewLocal').click(); await wait();
  test('New project starts with Minor Third after a custom scale', () => evaluate('state.ratio===1.2') && d.getElementById('jScalePreset').value==='minor-third');
  test('Delivery reviews include planning and report their actual checklist count', () => {
    const boxes=[...d.querySelectorAll('.readiness-item')];
    boxes[0].checked=true; boxes[0].dispatchEvent(new w.Event('change'));
    const passes=boxes.length===8 && boxes[0].parentElement.textContent.includes('brief') && boxes[1].parentElement.textContent.includes('prototype') && d.getElementById('readinessStatus').textContent.startsWith('1 of 8');
    boxes[0].checked=false; boxes[0].dispatchEvent(new w.Event('change')); return passes;
  });
  test('Planning stages precede palette in both wizard and centre navigation', () => {
    const labels=[...d.querySelectorAll('[data-journey-step]')].slice(0,5).map(button=>button.textContent);
    const destinations=[...d.querySelectorAll('.studio-section-nav a')].slice(1,6).map(link=>link.hash);
    return ['Brief','Architecture','Wireframe','Prototype','Palette'].every((label,index)=>labels[index].includes(label))
      && JSON.stringify(destinations)===JSON.stringify(['#process-brief','#process-ia','#process-wireframe','#process-prototype','#brandPalette']);
  });
  for (const [index,id] of ['brief','ia','wireframe','prototype'].entries()) {
    d.querySelector(`[data-journey-step="${index}"]`).click();
    const before=evaluate('projectJson()');
    d.querySelector(`[data-journey-pane="${index}"] > button:last-child`).click(); await wait();
    test(id+' wizard shortcut opens its centre lesson without changing project data', () => d.getElementById('process-'+id).open && evaluate('projectJson()')===before);
    d.querySelector(`#process-${id} [data-configure-step]`).click();
    test(id+' lesson returns to the correct wizard stage and focuses its heading', () => !d.querySelector(`[data-journey-pane="${index}"]`).hidden && d.activeElement===d.querySelector(`[data-journey-pane="${index}"] h3`));
  }
  input('jProject','Community learning hub'); d.getElementById('jSaveLocal').click();
  const planProjectId=d.getElementById('jProjects').value;
  for (const [key,value] of Object.entries({audience:'New community members',goal:'Find a workshop and prepare a question.',scope:'Workshop listings and resources',success:'Find the right workshop without help.',constraints:'Keyboard and phone access',pages:'Home\nWorkshops > Layout\nWorkshops > Colour\nResources\nContact',layout:'stack',wireframeNotes:'Put workshop choices before supporting resources.',prototypeTask:'Find the layout workshop.',prototypeNotes:'The participant hesitated at the first label.'})) input('plan-'+key,value);
  await wait();
  const processData=evaluate('JSON.stringify(state.designProcess)');
  test('Planning fields autosave with the active local project', () => JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planProjectId].data.designProcess)===processData);
  test('Brief, architecture, wireframe and prototype artifacts use the edited plan', () => d.querySelector('#process-brief dd').textContent==='New community members' && d.querySelector('#process-ia .process-map').textContent.includes('Workshops') && d.querySelectorAll('#process-ia .process-map > ul > li').length===4 && d.querySelectorAll('#process-ia .process-map ul ul > li').length===2 && d.querySelector('#process-wireframe .process-wireframe--stack') && d.querySelector('#process-prototype').textContent.includes('Find the layout workshop.'));
  test('Planning edits reach the HTML inspector, JSON export and responsive sample', () => {
    d.getElementById('dockTabHtml').click();
    return d.getElementById('dockCss').textContent===evaluate('htmlExport()') && evaluate('htmlExport()').includes('New community members') && JSON.stringify(JSON.parse(evaluate('projectJson()')).designProcess)===processData && previewDoc().querySelector('#brief-lab').textContent.includes('New community members') && previewDoc().querySelector('#wireframe-lab .process-wireframe--stack');
  });
  const planExport=evaluate('projectJson()');
  reset(); evaluate('importConfig('+planExport+')'); await wait();
  test('All planning fields round trip through JSON and synchronize the editors', () => evaluate('JSON.stringify(state.designProcess)')===processData && [...d.querySelectorAll('[data-process-field]')].every(control=>control.value===JSON.parse(processData)[control.dataset.processField]));
  d.getElementById('jNewLocal').click(); input('plan-goal','A separate project task.'); d.getElementById('jSaveLocal').click();
  input('jProjects',planProjectId,'change'); d.getElementById('jLoadLocal').click(); await wait();
  test('Local project switching restores planning without overwriting the previous project', () => evaluate('JSON.stringify(state.designProcess)')===processData && JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planProjectId].data.designProcess)===processData);
  await importFile(JSON.stringify({project:'Imported planning file',designProcess:JSON.parse(processData)}));
  test('Actual JSON file input restores planning fields and lessons', () => evaluate('state.project')==='Imported planning file' && !d.getElementById('loadFile').value && evaluate('JSON.stringify(state.designProcess)')===processData && d.getElementById('plan-goal').value==='Find a workshop and prepare a question.');
  evaluate('importConfig({primary:"#123456"})'); await wait();
  test('Legacy projects receive starter planning data while preserving their palette', () => evaluate('state.primary==="#123456" && JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  evaluate('importConfig({designProcess:{audience:42,pages:["Bad"],layout:"split;display:none",scope:"x".repeat(5000),goal:"",unknown:"ignored"}})'); await wait();
  test('Imported planning validates field types, lengths, arrangement and empty drafts', () => evaluate('state.designProcess.audience===DSStudio.process.defaults().audience && state.designProcess.pages===DSStudio.process.defaults().pages && state.designProcess.layout==="split" && state.designProcess.scope.length===1200 && state.designProcess.goal==="" && !("unknown" in state.designProcess)') && d.getElementById('plan-goal').value==='');
  test('Architecture parsing bounds entries, depth and labels', () => {
    const groups=w.DSStudio.process.hierarchy(Array.from({length:30},(_,i)=>'Group '+i+'x'.repeat(80)+' > Child > Ignored').join('\n'));
    return groups.length===12 && groups.every(([label,children])=>label.length===64 && children.length===1 && children[0]==='Child');
  });
  for (const value of [null,[],42,'invalid']) {
    evaluate('importConfig({designProcess:'+JSON.stringify(value)+'})');
    test('Malformed planning '+JSON.stringify(value)+' uses safe defaults', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  }
  const hostile='<img src=x onerror="window.planExecuted=true"><script>window.planExecuted=true<\/script>';
  input('plan-audience',hostile); input('plan-pages',hostile+' > Child'); input('plan-prototypeNotes',hostile); await wait();
  test('Planning text is escaped in studio lessons, exports and the live sample', () => {
    const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !d.querySelector('[data-process-artifact] img, [data-process-artifact] script') && !exported.querySelector('#design-process img, #design-process script') && !previewDoc().querySelector('#design-process img, #design-process script') && d.querySelector('#process-brief dd').textContent===hostile && exported.querySelector('#brief-lab dd').textContent===hostile && !w.planExecuted;
  });
  reset(); await wait();
  test('Editing planning never mutates the starter defaults; reset restores every field', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults()) && JSON.stringify(DEFAULT.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  d.getElementById('process-prototype').open=true;
  const prototypeNode=d.getElementById('studio-plan-choose'); prototypeNode.querySelector('a').focus();
  input('jAccent','#00badc'); await wait();
  test('Unrelated palette edits preserve planning nodes and prototype focus', () => d.getElementById('studio-plan-choose')===prototypeNode && d.activeElement===prototypeNode.querySelector('a'));
  d.getElementById('process-prototype').open=true;
  d.querySelector('a[href="#studio-plan-choose"]').click(); await wait();
  test('Centre prototype links reach real screen anchors', () => w.location.hash==='#studio-plan-choose' && d.getElementById('process-prototype').open);
  d.querySelector('a[href="#studio-plan-discover"]').click(); await wait();
  test('Centre prototype supports returning to the first screen', () => w.location.hash==='#studio-plan-discover');
  for (const destination of ['choose','review','discover']) {
    const source=destination==='choose'?'discover':destination==='review'?'choose':'review';
    previewDoc().querySelector(`#sample-plan-${source} a[href="#sample-plan-${destination}"]`).click(); await wait();
    test('Live prototype navigates to '+destination+' inside the preview', () => previewDoc().getElementById('sample-plan-'+destination).getBoundingClientRect().top>=-1 && previewDoc().getElementById('sample-plan-'+destination).getBoundingClientRect().top<previewWindow().innerHeight && !w.__reviewErrors.length);
  }
  const processPage=d.createElement('iframe'); processPage.style.cssText='width:1440px;height:1200px;border:0';
  const loadProcessPage=async()=>{
    processPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    await new Promise(resolve=>{processPage.onload=resolve;if(!processPage.isConnected)d.body.append(processPage);});
  };
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('plan-layout','split'); await loadProcessPage();
    for (const width of [320,390,768,1440]) {
      processPage.style.width=width+'px'; app.style.width=width+'px'; await wait();
      const pd=processPage.contentDocument, pw=processPage.contentWindow;
      test(theme+' planning artifacts and controls fit at '+width+'px', () => {
        d.getElementById('expandSections').click();
        const wire=pd.querySelector('.process-wireframe'), style=pw.getComputedStyle(wire);
        return pd.documentElement.scrollWidth<=width+1 && d.documentElement.scrollWidth<=width+1 && style.gridTemplateColumns.split(' ').length===(width<=768?1:2) && [...pd.querySelectorAll('#design-process .process-wireframe > div, #design-process .process-screens > li')].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && el.scrollWidth<=el.clientWidth+1;});
      });
    }
    processPage.style.width='320px'; app.style.width='320px'; await wait();
    for (const step of [0,1,2,3]) {
      d.querySelector(`[data-journey-step="${step}"]`).click(); await wait();
      test(theme+' planning wizard stage '+(step+1)+' fits a 320px studio', () => {
        const controls=[...d.querySelectorAll(`[data-journey-pane="${step}"] textarea, [data-journey-pane="${step}"] select`)];
        if (d.documentElement.scrollWidth<=320 && controls.every(el=>el.scrollWidth<=el.clientWidth+1)) return true;
        throw Error(JSON.stringify({page:d.documentElement.scrollWidth,viewport:w.innerWidth,controls:controls.map(el=>({id:el.id,width:el.clientWidth,scroll:el.scrollWidth}))}));
      });
    }
  }
  processPage.remove(); app.style.width='1440px'; reset(); await wait();
  const standalone=d.createElement('iframe'); standalone.style.cssText='width:1440px;height:1000px;border:0';
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('jProject','Standalone homepage'); input('jBase',18); await wait();
    const files={}; w.download=(name,content,type)=>{files[name]={content,type};};
    d.getElementById('jExportHtml').click(); d.getElementById('jExportCss').click(); w.download=originalDownload;
    const parsed=new w.DOMParser().parseFromString(files['index.html'].content,'text/html');
    test(theme+' standalone pair has a relative CSS link, embedded images and no studio scripts or inline styles', () => parsed.querySelector('link[rel="stylesheet"][href="tokens.css"]') && !parsed.querySelector('script,style') && [...parsed.querySelectorAll('img')].every(img=>img.src.startsWith('data:image/svg+xml')) && parsed.documentElement.dataset.theme===theme);
    const cssUrl=w.URL.createObjectURL(new w.Blob([files['tokens.css'].content],{type:'text/css'}));
    standalone.srcdoc=files['index.html'].content.replace('href="tokens.css"','href="'+cssUrl+'"');
    await new Promise(resolve=>{standalone.onload=resolve;if(!standalone.isConnected)d.body.append(standalone);});
    const pd=standalone.contentDocument, pw=standalone.contentWindow;
    test(theme+' HTML loads its separate complete stylesheet and basic website components', () => pd.querySelector('link[rel="stylesheet"]').sheet && !pd.querySelector('style,script') && pw.getComputedStyle(pd.body).fontSize==='18px' && pd.querySelector('.sample-brand').textContent.includes('Standalone homepage') && ['header nav','main','#home .sample-lead','img','.card','form input[type="email"]','table','details summary','.sample-notice','progress','footer nav'].every(selector=>pd.querySelector(selector)));
    for (const width of [320,768,1440]) {
      standalone.style.width=width+'px'; await wait();
      test(theme+' separately linked website reflows at '+width+'px', () => pd.documentElement.scrollWidth<=width+1 && pw.getComputedStyle(pd.querySelector('.sample-hero')).gridTemplateColumns.split(' ').length===(width<=768?1:12));
    }
    standalone.style.width='320px'; await wait();
    const menu=pd.getElementById('sample-menu'); menu.querySelector('summary').click();
    test(theme+' standalone mobile menu and FAQ work with native HTML', () => {
      const faq=pd.getElementById('getting-started'), wasOpen=faq.open; faq.querySelector('summary').click();
      return menu.open && pd.querySelector('.sample-mobile-navigation').getBoundingClientRect().height>0 && faq.open!==wasOpen && !pd.querySelector('.sample-form').checkValidity();
    });
    w.URL.revokeObjectURL(cssUrl);
  }
  standalone.remove(); reset(); await wait();
  const advancedHtml=evaluate('htmlExport()'), advancedCss=evaluate('cssExport()');
  test('Sample mode defaults to Advanced with a labelled independent tab group', () => evaluate('state.sampleMode')==='advanced' && d.getElementById('dockModeAdvanced').getAttribute('aria-selected')==='true' && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')==='dockModeAdvanced' && d.querySelector('[aria-label="Website sample complexity"]'));
  d.getElementById('dockTabHtml').click(); d.getElementById('dockModeBasic').click(); await wait();
  test('Basic selection synchronizes inspector, preview and central exports while retaining the language tab', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('codeView').textContent===evaluate('codeContent()') && previewDoc().querySelector('.feature-grid') && !previewDoc().querySelector('#design-process'));
  test('Basic exports a compact dedicated CSS file rather than the Advanced gallery styles', () => evaluate('cssExport()').length<advancedCss.length/3 && evaluate('cssExport()').includes('repeat(auto-fit, minmax(') && !evaluate('cssExport()').includes('.sample-grid-demo'));
  const basicDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Basic HTML has exactly three main sections, one heading, logo/nav, hero, three cards, signup and footer', () => basicDoc.querySelectorAll('main > section').length===3 && basicDoc.querySelectorAll('h1').length===1 && basicDoc.querySelector('header .logo[aria-hidden="true"]') && basicDoc.querySelector('header nav[aria-label]') && basicDoc.querySelector('#home .button') && basicDoc.querySelectorAll('.feature-grid article').length===3 && basicDoc.querySelector('#signup form') && basicDoc.querySelector('footer nav[aria-label]') && basicDoc.querySelector('footer a[href="#top"]'));
  test('Basic HTML IDs, fragment destinations and form labels resolve without scripts or inline styles', () => {
    const ids=[...basicDoc.querySelectorAll('[id]')].map(el=>el.id);
    return ids.length===new Set(ids).size && !basicDoc.querySelector('script,style') && basicDoc.querySelector('link[href="tokens.css"]') && [...basicDoc.querySelectorAll('a[href^="#"]')].every(link=>basicDoc.getElementById(link.hash.slice(1))) && [...basicDoc.querySelectorAll('label[for]')].every(label=>basicDoc.getElementById(label.htmlFor));
  });
  for (const [key,id] of [['End','dockModeBasic'],['Home','dockModeAdvanced'],['ArrowRight','dockModeBasic'],['ArrowLeft','dockModeAdvanced']]) {
    const selected=d.querySelector('.studio-dock-modes [aria-selected="true"]');
    selected.dispatchEvent(new w.KeyboardEvent('keydown',{key,bubbles:true})); await wait();
    test('Mode tabs support '+key+' navigation and one tab stop', () => d.activeElement===d.getElementById(id) && d.getElementById(id).getAttribute('aria-selected')==='true' && [...d.querySelectorAll('.studio-dock-modes button')].filter(button=>button.tabIndex===0).length===1 && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')===id);
  }
  test('Returning to Advanced preserves its exact generated page and CSS', () => evaluate('htmlExport()')===advancedHtml && evaluate('cssExport()')===advancedCss);
  d.getElementById('dockModeBasic').click(); await wait(); d.getElementById('jSaveLocal').click();
  const basicProjectId=d.getElementById('jProjects').value, basicProject=evaluate('projectJson()');
  test('Basic selection is saved with the active local project and JSON', () => JSON.parse(basicProject).sampleMode==='basic' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[basicProjectId].data.sampleMode==='basic');
  reset(); evaluate('importConfig('+basicProject+')'); await wait();
  test('Import restores Basic tab selection, preview and export generation', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && previewDoc().querySelector('.signup-form'));
  const basicFiles=[]; w.download=(name,content,type)=>basicFiles.push({name,content,type});
  for (const [index,button] of [...d.querySelectorAll('[data-website-download]')].entries()) {
    button.click(); const html=button.dataset.websiteDownload==='html';
    test('Basic website download '+index+' uses the selected sample and matching file name', () => basicFiles.at(-1).name===(html?'index.html':'tokens.css') && basicFiles.at(-1).content===evaluate(html?'htmlExport()':'cssExport()'));
  }
  let basicCopied=''; Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{basicCopied=text;}}});
  for (const language of ['html','css']) {
    d.getElementById(language==='html'?'dockTabHtml':'dockTabCss').click(); d.getElementById('dockCopy').click(); await wait(); d.getElementById('dockDownload').click();
    test('Basic '+language+' copy and inspector download match the visible code', () => basicCopied===d.getElementById('dockCss').textContent && basicFiles.at(-1).content===basicCopied && basicFiles.at(-1).name===(language==='html'?'index.html':'tokens.css'));
  }
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard}); w.download=originalDownload;
  input('jProject','Harbour learning club'); input('jBase',18); input('jPrimary','#196b63'); input('advGap',32); await wait();
  test('Basic design settings update its HTML, CSS, preview and source descriptions', () => previewDoc().querySelector('.brand').textContent.includes('Harbour learning club') && previewWindow().getComputedStyle(previewDoc().body).fontSize==='18px' && previewWindow().getComputedStyle(previewDoc().querySelector('.feature-grid')).gap==='32px' && d.getElementById('websiteSampleDescription').textContent.startsWith('Basic') && d.getElementById('dockNote').textContent.startsWith('Basic CSS'));
  const basicForm=previewDoc().querySelector('form');
  test('Basic signup has required name/email/consent and native invalid-input checks', () => !basicForm.checkValidity() && ['signup-name','signup-email'].every(id=>previewDoc().getElementById(id).required) && basicForm.querySelector('input[type="checkbox"]').required);
  previewDoc().getElementById('signup-name').value='Taylor'; previewDoc().getElementById('signup-email').value='taylor@example.com'; basicForm.querySelector('input[type="checkbox"]').checked=true;
  const basicBrowsingDoc=previewDoc(); basicForm.requestSubmit(); await wait();
  test('Basic live signup validates and remains a static demonstration without navigating', () => previewDoc()===basicBrowsingDoc && basicForm.checkValidity() && previewDoc().getElementById('basic-signup-note').textContent.includes('No account has been created'));
  input('jRadius',20); await wait();
  test('Basic form values survive live design edits', () => previewDoc().getElementById('signup-name').value==='Taylor' && previewDoc().querySelector('input[type="checkbox"]').checked);
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Switching sample modes resets browsing without leaking Basic form values into Advanced', () => previewDoc().getElementById('contact-name').value==='' && Math.abs(previewWindow().scrollY)<1);
  d.getElementById('dockModeBasic').click(); await wait();
  test('Switching back to Basic begins a fresh browsing session', () => previewDoc().getElementById('signup-name').value==='' && !previewDoc().querySelector('input[type="checkbox"]').checked);
  const basicPage=d.createElement('iframe'); basicPage.style.cssText='width:1440px;height:1000px;border:0';
  for (const theme of ['light','dark']) {
    input('jTheme',theme); await wait();
    const cssUrl=w.URL.createObjectURL(new w.Blob([evaluate('cssExport()')],{type:'text/css'}));
    const htmlUrl=w.URL.createObjectURL(new w.Blob([evaluate('htmlExport()').replace('href="tokens.css"','href="'+cssUrl+'"')],{type:'text/html'}));
    basicPage.src=htmlUrl;
    await new Promise(resolve=>{basicPage.onload=resolve;if(!basicPage.isConnected)d.body.append(basicPage);});
    const pd=basicPage.contentDocument, pw=basicPage.contentWindow;
    for (const width of [320,390,768,1440]) {
      basicPage.style.width=width+'px'; await wait();
      test(theme+' Basic standalone page reflows with its separate stylesheet at '+width+'px', () => {
        const grid=pd.querySelector('.feature-grid'), cards=[...grid.children], first=cards[0].getBoundingClientRect();
        const columns=cards.filter(card=>Math.abs(card.getBoundingClientRect().top-first.top)<1).length;
        return pd.querySelector('link').sheet && !pd.querySelector('style,script') && pd.documentElement.scrollWidth<=width+1 && columns===(width<476?1:3) && pw.getComputedStyle(grid).display==='grid' && pw.getComputedStyle(pd.querySelector('.signup-layout')).gridTemplateColumns.split(' ').length===(width<=768?1:2) && [...pd.querySelectorAll('header nav a, footer nav a, .button')].every(el=>el.getBoundingClientRect().height>=44);
      });
    }
    pd.querySelector('.skip-link').focus();
    test(theme+' Basic skip link and focus outline are visible with keyboard focus', () => pd.activeElement===pd.querySelector('.skip-link') && pd.activeElement.getBoundingClientRect().top>=0 && pw.getComputedStyle(pd.activeElement).outlineStyle==='solid');
    pd.querySelector('.back-to-top').click(); await wait();
    test(theme+' Basic standalone Back to top uses a real native fragment destination', () => pw.location.hash==='#top' && pd.getElementById('top').getBoundingClientRect().top>=-1 && pd.getElementById('top').getBoundingClientRect().top<10);
    w.URL.revokeObjectURL(cssUrl); w.URL.revokeObjectURL(htmlUrl);
  }
  basicPage.remove();
  evaluate('importConfig({sampleMode:"<script>",project:"<img src=x onerror=alert(1)>"})');
  test('Invalid sample mode falls back to Advanced', () => evaluate('state.sampleMode')==='advanced');
  evaluate('importConfig({sampleMode:"basic",project:"<img src=x onerror=alert(1)>"})');
  test('Basic escapes imported project text in its title and brand', () => {
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !page.querySelector('img,script') && page.querySelector('.brand').textContent.includes('<img src=x onerror=alert(1)>');
  });
  evaluate('importConfig({})'); await wait();
  test('Legacy projects without a sample mode retain Advanced', () => evaluate('state.sampleMode')==='advanced' && d.getElementById('dockModeAdvanced').getAttribute('aria-selected')==='true');
  d.getElementById('dockModeBasic').click(); reset(); await wait();
  test('Reset restores Advanced mode and its complete sample', () => evaluate('state.sampleMode')==='advanced' && previewDoc().querySelector('#design-process') && d.getElementById('sampleModeHelp').textContent.startsWith('Advanced'));
  test('No interaction JavaScript errors', () => !w.__reviewErrors.length);
  document.getElementById('results').textContent=JSON.stringify({results, errors:w.__reviewErrors});
};
</script>'''


class Handler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/__font_fixture__':
            query = parse_qs(urlsplit(self.path).query)
            if query.get('mode') == ['error']:
                self.send_error(503, 'Font loading failure fixture')
                return
            rules = []
            for spec in query.get('family', []):
                family = spec.split(':', 1)[0]
                if family not in ['Inter', 'Source Sans 3', 'Literata']:
                    self.send_error(400, 'Unknown font fixture')
                    return
                local = 'local("Times New Roman"), local("Liberation Serif"), local("DejaVu Serif")' if family == 'Literata' else 'local("Arial"), local("Liberation Sans"), local("DejaVu Sans")'
                for style in ['normal', 'italic']:
                    rules.append(f'@font-face {{ font-family: "{family}"; font-style: {style}; font-weight: 100 900; font-display: swap; src: {local}; }}')
            data = '\n'.join(rules).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/css; charset=utf-8')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Length', str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path == '/__review__':
            body = HARNESS
        elif path == '/index.html':
            body = (ROOT / 'index.html').read_text(encoding='utf-8')
            body = body.replace('<head>', '''<head><script>
window.__reviewErrors=[];
addEventListener('error',e=>{
  const resource=e.target.src || e.target.href || '';
  if (!e.message && resource.includes('/__font_fixture__?') && resource.includes('mode=error')) return;
  window.__reviewErrors.push(e.message || 'Failed resource: '+resource);
},true);
addEventListener('unhandledrejection',e=>window.__reviewErrors.push(String(e.reason)));
const reviewConsoleError=console.error.bind(console);
console.error=(...args)=>{ window.__reviewErrors.push(args.map(String).join(' ')); reviewConsoleError(...args); };
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
                                  '--user-data-dir=' + profile, '--virtual-time-budget=45000',
                                  '--dump-dom', f'http://127.0.0.1:{server.server_port}/__review__'],
                                 capture_output=True, encoding='utf-8', errors='replace', timeout=90)
            match = re.search(r'<pre id="results">(.*?)</pre>', run.stdout, re.S)
            if not match or match[1] == 'RUNNING':
                raise SystemExit('Browser review did not complete.\n' + run.stderr[-2000:])
            report = json.loads(unescape(match[1]))
            for item in report['results']:
                print(('PASS' if item['pass'] else 'FAIL') + ': ' + item['name'] +
                      (': ' + item.get('error', '') if not item['pass'] else ''))
            print(f"{sum(item['pass'] for item in report['results'])}/{len(report['results'])} browser checks passed")
            print(json.dumps(report['errors']))
            return int(any(not item['pass'] for item in report['results']))
    finally:
        server.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
