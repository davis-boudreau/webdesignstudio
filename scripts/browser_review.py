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
  window.addEventListener('unhandledrejection', event => {
    results.push({name:'Browser harness completed without an unhandled exception',pass:false,error:String(event.reason?.stack || event.reason)});
    document.getElementById('results').textContent=JSON.stringify({results,errors:w.__reviewErrors});
  });
  const evaluate = code => w.eval(code);
  const test = (name, fn) => {
    try { if (!fn()) throw Error('Assertion failed'); results.push({name, pass:true}); }
    catch (e) { results.push({name, pass:false, error:String(e)}); }
    document.title='Browser review: '+results.length+' checks; last: '+name;
  };
  // Destination-editor fixtures explicitly reveal its secondary controls.
  const revealDestinationPlan=()=>{const source=d.getElementById('sitemap-source');if(source && source.value!=='custom'){source.value='custom';source.dispatchEvent(new w.Event('change',{bubbles:true}));}d.querySelectorAll('#sitemap-destination-editor, #sitemap-outline-editor, #process-ia .ia-destination-map').forEach(el=>el.open=true);};
  const input = (id, value, type='input') => {
    if(id.startsWith('sitemap-') || id==='plan-pages')revealDestinationPlan();
    const el=d.getElementById(id);
    if(id.startsWith('ia-')){const disclosure=el.closest('.ia-editor-disclosure');if(disclosure)disclosure.open=true;}
    el.value=value;
    el.dispatchEvent(new w.Event(type,{bubbles:true}));
  };
  const revealAll = () => d.querySelectorAll('#main > .studio-section, .step-more').forEach(section => {section.hidden=false;section.open=true;});
  // Most historical feature fixtures exercise the complete Advanced sample.
  // Default/reset behavior is checked separately through resetStudio directly.
  const reset = () => {evaluate('resetStudio()');d.getElementById('dockModeAdvanced').click();};
  const previewDoc = () => d.getElementById('previewPage').contentDocument;
  const previewWindow = () => d.getElementById('previewPage').contentWindow;
  const saved = () => Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects')))[0].data;
  const wait = (ms=100) => new Promise(resolve => setTimeout(resolve,ms));
  test('No startup JavaScript errors', () => !w.__reviewErrors.length);
  test('Fresh startup opens the Brief centre accordion that matches the active builder step',()=>w.DSStudio.activeStage===0 && d.querySelector('[data-journey-step="0"]').getAttribute('aria-current')==='step' && d.getElementById('process-brief').open && !d.getElementById('process-brief').hidden && !d.getElementById('process-ia').open);
  const stepDisclosure=d.querySelector('.journey-step-list');
  test('Choose a step starts expanded with all twelve steps available',()=>stepDisclosure.open && stepDisclosure.querySelectorAll('[data-journey-step]').length===12);
  w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);evaluate('apply()');
  test('Step navigation and rendering keep the step chooser expanded',()=>stepDisclosure.open && w.DSStudio.activeStage===0);
  stepDisclosure.open=false;w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);evaluate('apply()');
  test('A user-collapsed step chooser stays collapsed across navigation and rendering',()=>!stepDisclosure.open);
  stepDisclosure.open=true;w.dssShowWizardStep(1,false);w.dssShowWizardStep(0,false);
  test('A reopened step chooser stays expanded across navigation',()=>stepDisclosure.open);
  test('Startup defaults to OKLCH across state, both method controls and lesson output',()=>evaluate('state.method')==='oklch' && d.getElementById('jRamp').value==='oklch' && d.getElementById('method').value==='oklch' && d.getElementById('rampMethodLabel').textContent==='OKLCH' && d.getElementById('palette-method-status').textContent.includes('OKLCH'));
  test('New projects start with Basic on the left and Advanced on the right',()=>evaluate('state.sampleMode')==='basic' && [...d.querySelectorAll('[aria-label="Website sample complexity"] [role="tab"]')].map(el=>el.id).join(',')==='dockModeBasic,dockModeAdvanced' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && d.getElementById('dockModeBasic').tabIndex===0 && d.getElementById('dockModeAdvanced').tabIndex===-1 && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')==='dockModeBasic');
  d.getElementById('dockModeAdvanced').click();await wait();
  // Studio appearance is a browser preference; project theme and samples are independent.
  const appearanceToggle=d.getElementById('themeToggle');
  const styleSnapshot=element=>{
    const cs=w.getComputedStyle(element);
    return ['color','backgroundColor','fontFamily','fontSize','lineHeight','letterSpacing','borderRadius','borderColor'].map(key=>cs[key]).join('|');
  };
  const chromeSnapshot=()=>[d.body,d.querySelector('.topbar'),d.querySelector('.sidebar .panel'),d.getElementById('journeyTitle'),d.getElementById('inspectorToggle'),d.getElementById('previewTheme')].map(styleSnapshot).join('~');
  test('Studio starts light with a labelled appearance toggle',()=>d.documentElement.dataset.theme==='light' && appearanceToggle.textContent==='Studio: Light' && appearanceToggle.getAttribute('aria-pressed')==='false' && appearanceToggle.getAttribute('aria-label').includes('Studio appearance'));
  for(const studio of ['light','dark']) {
    if(d.documentElement.dataset.theme!==studio)appearanceToggle.click();
    const fixedChrome=chromeSnapshot();
    for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
      d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();
      input('previewTheme',theme,'change');await wait();
      test(studio+' Studio supports '+theme+' '+mode+' page independently',()=>d.documentElement.dataset.theme===studio && previewDoc().documentElement.dataset.theme===theme && d.getElementById('jTheme').value===theme && d.getElementById('dockTheme').value===theme && chromeSnapshot()===fixedChrome);
      test(studio+' Studio keeps '+theme+' '+mode+' design examples in project colours',()=>{
        const sample=w.getComputedStyle(d.getElementById('bdSingle'));
        return sample.getPropertyValue('--text').trim()===evaluate('palette().roles.text') && sample.backgroundColor===evaluate("'rgb('+hexRgb(palette().roles['surface-muted']).join(', ')+')'");
      });
    }
    input('jBase',22);input('jRadius',28);input('jSpacing',8);input('jPrimary','#883366');input('jLeading',1.9);
    input('advColor_success','#661144');d.getElementById('advUnderline').checked=false;d.getElementById('advUnderline').dispatchEvent(new w.Event('change',{bubbles:true}));
    test(studio+' Studio type, controls and surfaces survive project foundation edits',()=>chromeSnapshot()===fixedChrome && w.getComputedStyle(d.body).fontSize==='16px' && w.getComputedStyle(d.getElementById('mobileType').querySelector('.sample')).fontSize!=='16px');
    reset();await wait();
  }
  // Verify preference persistence in a fresh document, never the user's profile.
  const beforeAppearance=evaluate('[projectJson(),htmlExport(),cssExport()]');
  const appearanceDocument=previewDoc(),appearanceCssNode=d.getElementById('dockCss').firstChild;
  appearanceToggle.focus();appearanceToggle.click();await wait(); // Dark -> Light.
  test('Studio changes preserve project, exports, inspector text, focus and preview document',()=>JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'))===JSON.stringify(beforeAppearance) && previewDoc()===appearanceDocument && d.getElementById('dockCss').firstChild===appearanceCssNode && d.activeElement===appearanceToggle);
  appearanceToggle.click();
  const nativePreferenceWrite=w.Storage.prototype.setItem;
  w.Storage.prototype.setItem=function(){throw new w.DOMException('Storage blocked','SecurityError');};
  appearanceToggle.click();
  test('Studio appearance works when preference storage is blocked',()=>d.documentElement.dataset.theme==='light' && !w.__reviewErrors.length);
  appearanceToggle.click();w.Storage.prototype.setItem=nativePreferenceWrite;
  const fresh=d.createElement('iframe');fresh.style.display='none';
  const loadFresh=()=>new Promise(resolve=>{fresh.onload=resolve;fresh.src='/index.html?appearance-review='+Math.random();if(!fresh.isConnected)d.body.append(fresh);});
  await loadFresh();
  test('A fresh document restores dark Studio appearance while its new project stays light',()=>fresh.contentDocument.documentElement.dataset.theme==='dark' && fresh.contentWindow.eval('state.theme')==='light' && fresh.contentDocument.getElementById('themeToggle').getAttribute('aria-pressed')==='true');
  w.localStorage.setItem('dss-studio-appearance','<img src=x onerror=alert(1)>');await loadFresh();
  test('Invalid stored Studio appearance falls back to light without inserting content',()=>fresh.contentDocument.documentElement.dataset.theme==='light' && fresh.contentDocument.getElementById('themeToggle').textContent==='Studio: Light' && !fresh.contentDocument.querySelector('img[onerror]'));
  // Reload real documents, preserving each section fragment and reopening a
  // manually collapsed active lesson. Phase indices differ from display order.
  fresh.style.cssText='position:fixed;inset:0;width:100%;height:100%;border:0;z-index:10000';
  for(const stage of w.DSStudio.orderedStages) {
    const fw=fresh.contentWindow,fd=fresh.contentDocument;
    fw.dssShowWizardStep(stage.index,false);
    fw.history.replaceState(null,'','#'+stage.lesson);
    fd.getElementById(stage.lesson).open=false;
    const priorDoc=fd,priorProject=fw.eval('projectJson()');
    await new Promise(resolve=>{fresh.onload=resolve;fw.location.reload();});await wait();
    const reloaded=fresh.contentWindow,doc=fresh.contentDocument;
    test('Reload opens Step '+(stage.position+1)+' '+stage.label+' and matches the active builder',()=>doc!==priorDoc && reloaded.DSStudio.activeStage===stage.index && doc.querySelector('[data-journey-step="'+stage.index+'"]').getAttribute('aria-current')==='step' && doc.getElementById(stage.lesson).open && !doc.getElementById(stage.lesson).hidden && !doc.querySelector('[data-journey-pane="'+stage.index+'"]').hidden && [...doc.querySelectorAll('#main > .studio-section')].filter(section=>section.id!=='studio-section-4').every(section=>section.open===(section.id===stage.lesson)) && reloaded.eval('projectJson()')===priorProject && !reloaded.__reviewErrors.length);
  }
  fresh.remove();
  if(d.documentElement.dataset.theme!=='light')appearanceToggle.click();
  for(const width of [320,390,1440])for(const studio of ['light','dark']) {
    app.style.width=width+'px';if(d.documentElement.dataset.theme!==studio)appearanceToggle.click();await wait();
    test(studio+' Studio appearance controls fit '+width+'px with visible focus',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && appearanceToggle.getBoundingClientRect().height>=44 && appearanceToggle.getBoundingClientRect().right<=w.innerWidth+1 && w.getComputedStyle(appearanceToggle).outlineStyle!=='none');
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')appearanceToggle.click();reset();await wait();

  test('Startup selects Minor Third 1.2 throughout the typography controls and export', () => evaluate('state.ratio===1.2 && cssExport().includes("--type-ratio: 1.2;")') && ['jScalePreset','clampScalePreset'].every(id=>d.getElementById(id).value==='minor-third') && ['ratio','jRatio','clampRatio'].every(id=>d.getElementById(id).value==='1.2'));
  test('Startup keeps the preview and active Brief expanded with inspector hidden', () => d.querySelector('#main > :first-child').id==='studio-section-4' && [...d.querySelectorAll('#main > .studio-section')].every(section=>!section.hidden && section.open===(section.id==='studio-section-4' || section.id==='process-brief')) && !d.querySelector('.studio-code-dock').open && !d.getElementById('studioInspector').open);
  test('Hidden inspector leaves one quarter for the desktop builder and the rest for the preview', () => Math.abs(d.querySelector('.sidebar').getBoundingClientRect().width-(d.querySelector('.layout').clientWidth-16)/4)<1 && d.getElementById('dockCss').getBoundingClientRect().height===0);
  test('Inspector has a native details/summary disclosure arrow in both states',()=>d.getElementById('studioInspector').tagName==='DETAILS' && d.getElementById('inspectorToggle').tagName==='SUMMARY' && d.getElementById('inspectorToggle').textContent==='Live CSS/HTML Inspector' && w.getComputedStyle(d.getElementById('inspectorToggle')).display==='list-item' && d.getElementById('inspectorToggle').tabIndex===0 && d.getElementById('inspectorToggle').getBoundingClientRect().height>=44);
  test('Competing beginner and centre navigation is removed', () => !d.getElementById('workspaceNav') && !d.getElementById('beginnerStart') && !d.getElementById('beginnerPath') && !d.querySelector('.studio-section-nav') && !d.querySelector('[data-configure-step]'));
  test('Preview initially fills the centre pane in Fluid mode', () => d.getElementById('previewFrame').dataset.width==='fluid' && d.querySelector('button[data-width="fluid"]').getAttribute('aria-pressed')==='true');
  test('Twelve wizard steps connect project planning to fifteen centre lessons and the preview', () => d.querySelectorAll('[data-journey-step]').length===12 && d.querySelectorAll('[data-journey-pane]').length===12 && d.querySelectorAll('#main > .studio-section > .panel > .studio-lesson').length===15 && d.getElementById('jProgress').textContent.includes('of 12'));
  test('Every exported token has a configuration source inside the wizard', () => w.dssReadTokens().length>150 && w.dssReadTokens().every(row=>{
    const source=w.dssTokenSource(row), control=source && d.getElementById(source.control);
    return control && control.closest('[data-journey-pane]')?.dataset.journeyPane===String(source.step);
  }));
  test('Derived token families identify their foundation instead of arbitrary overrides', () => ['--space-6','--primary-700','--text-step-4','--text-h1','--font-ui','--heading-tracking','--button-progress-animation'].every(name=>/Derived|Alias/.test(w.dssTokenSource({name}).mode)));
  test('Font, responsive, layout and interaction settings now live in their wizard steps', () => [['fontSource',5],['clampMinWidth',5],['advWeight',5],['advColumns',9],['advBorder',8],['jSpacing',8],['advState',10],['advReduce',10]].every(([id,step])=>d.getElementById(id).closest('[data-journey-pane]').dataset.journeyPane===String(step)));
  d.getElementById('studio-section-4').open=false;
  d.querySelector('[data-journey-step="5"]').click(); input('jBase',18); await wait();
  const closedPreviewDoc=previewDoc();
  test('Wizard edits update the generated CSS while the responsive section is collapsed', () => !d.getElementById('studio-section-4').open && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('--font-size-base: 18px;'));
  evaluate("dssRevealSection('previewPage',false)"); await wait();
  test('Reopening the collapsed preview keeps the document and current settings', () => d.getElementById('studio-section-4').open && previewDoc()===closedPreviewDoc && parseFloat(previewWindow().getComputedStyle(previewDoc().body).fontSize)===18 && Math.abs(previewWindow().innerWidth-d.getElementById('previewFrame').getBoundingClientRect().width)<2);
  d.getElementById('studio-section-4').open=false;
  reset(); d.querySelector('[data-journey-step="0"]').click(); await wait();
  test('Editing and reopening the preview leaves Colour systems collapsed', () => !d.getElementById('studio-section-1').open && !d.getElementById('studio-section-4').open);
  revealAll(); await wait();
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
  test('Page theme and guided controls synchronize independently of Studio appearance', () => d.documentElement.dataset.projectTheme==='dark' && d.documentElement.dataset.theme==='light' && d.getElementById('jTheme').value==='dark');
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
  w.DSStudio.inspector.show({language:'css',section:'all'});
  d.getElementById('dockTabCss').dispatchEvent(new w.KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}));
  test('Inspector tabs support arrow-key selection and focus', () => d.activeElement.id==='dockTabHtml' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockTabCss').tabIndex===-1);
  test('Inspector code panel is labelled by active tab', () => d.getElementById('dockCss').getAttribute('aria-labelledby')==='dockTabHtml');
  d.getElementById('dockTabCss').click();
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
    test('Three desktop columns keep the builder at 25% and cap the inspector at 25% at '+width+'px', () => Math.abs(left.width-(d.querySelector('.layout').clientWidth-16)/4)<1 && Math.abs(centre.left-left.right-16)<1 && Math.abs(right.left-centre.right-16)<1 && Math.abs(centre.width-right.width*2)<1 && right.width<=(d.querySelector('.layout').clientWidth-16)/4+1 && d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  test('All three columns grow across large and ultrawide screens', () => {
    const first=desktopPanes.find(pane=>pane.width===1440), last=desktopPanes.at(-1);
    return last.left>first.left && last.centre>first.centre && last.right>first.right;
  });
  app.style.width='1280px'; await wait();
  test('Inspector stacks after the centre when three columns would be cramped', () => {
    const left=d.querySelector('.sidebar').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect(), right=d.querySelector('.studio-code-dock').getBoundingClientRect();
    return Math.abs(left.width-(d.querySelector('.layout').clientWidth-16)/4)<1 && Math.abs(centre.left-right.left)<1 && right.top>=centre.bottom && d.documentElement.scrollWidth<=w.innerWidth+1;
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
    return rows.length===(11+44)*2*2 && rows.every(row=>row.status==='candidate');
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
  wizardRepairButton.click(); input('repairHex','#101820');
  const wizardRepairClosed=new Promise(resolve=>d.getElementById('colourRepair').addEventListener('close',resolve,{once:true}));
  d.getElementById('repairApply').click(); await Promise.race([wizardRepairClosed,wait(1000)]); await wait();
  test('Applying a reviewed text fix updates both theme results and returns focus', () => {
    const themes=['light','dark'].map(theme=>reviewCell('secondary','hover',theme).dataset.result), colour=evaluate('state.buttonDesign.overrides.secondary.hoverText');
    if(themes.every(result=>result==='pass') && colour==='#101820' && d.activeElement===wizardRepairButton) return true;
    throw Error(JSON.stringify({themes,colour,active:d.activeElement.outerHTML.slice(0,300),dialogOpen:d.getElementById('colourRepair').open}));
  });
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
  test('Every centre-pane section has a native heading accordion', () => sections.length===16 && sections.every(el=>el.tagName==='DETAILS' && el.querySelector(':scope > summary > h2')));
  const beforeCollapse=evaluate('projectJson()');
  d.getElementById('studio-section-4').open=false;
  d.querySelector('[data-journey-step="5"]').click(); await wait();
  test('Selecting a step opens its lesson without changing design data', () => d.getElementById('studio-section-2').open && !d.getElementById('studio-section-2').hidden && evaluate('projectJson()')===beforeCollapse);
  d.getElementById('dockTabHtml').click();d.getElementById('jViewCss').click(); await wait();
  test('Deliver Inspect CSS selects CSS even after HTML was selected', () => d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.activeElement===d.getElementById('dockCss'));
  d.getElementById('buttonDesignLab').open=false; d.getElementById('bdJump').click(); await wait();
  test('Button laboratory shortcut activates its matching step and opens the detail', () => d.getElementById('buttonDesignLab').open && !d.getElementById('buttonDesignLab').hidden && evaluate('DSStudio.activeStage')===7);
  d.getElementById('studio-section-4').open=false; evaluate("dssRevealSection('previewFrame',false)"); await wait();
  test('Reopening the responsive preview restores its exact width', () => d.getElementById('studio-section-4').open && Math.abs(d.getElementById('previewFrame').getBoundingClientRect().width-1280)<1);
  d.querySelector('[data-journey-step="5"]').click();
  d.querySelector('#studio-section-2 > summary').click();
  test('Individual lesson headings toggle their disclosure', () => !d.getElementById('studio-section-2').open);
  d.querySelector('#studio-section-2 > summary').click(); await wait();
  test('Active lesson headings and typography controls fit a 320px page', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  revealAll();
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
  for (const [id,name] of [['saveBtn','design-system-studio.json'],['cssBtn','tokens.css'],['dockDownload','tokens.css'],['jExportHtml','index.html'],['jExportCss','tokens.css'],['jExportJson','design-system-studio.json'],['bdExport','design-system-buttons.css']]) {
    d.getElementById(id).click();
    test(id+' produces the expected download', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content.length>0);
  }
  for (const [tab,name] of [['viewCss','tokens.css'],['viewJson','design-system-studio.json'],['viewHtml','index.html']]) {
    d.getElementById(tab).click(); d.getElementById('downloadCode').click();
    test(tab+' downloads exactly the displayed code', () => downloadCalls.at(-1).name===name && downloadCalls.at(-1).content===d.getElementById('codeView').textContent);
  }
  test('Responsive preview omits the introductory lesson and duplicate export card', () => !d.querySelector('#studio-section-4 .studio-lesson, #studio-section-4 .website-export, #studio-section-4 [data-website-download], #studio-section-4 [data-website-code]') && d.getElementById('previewPage'));
  const beforeWebsiteDownloads=evaluate('projectJson()');
  for (const [index,button] of [...d.querySelectorAll('[data-website-download]')].entries()) {
    button.click();
    test('Standalone website action '+(index+1)+' downloads the matching live file with its MIME type', () => {
      const html=button.dataset.websiteDownload==='html', file=downloadCalls.at(-1);
      return file.name===(html?'index.html':'tokens.css') && file.type===(html?'text/html':'text/css') && file.content===evaluate(html?'htmlExport()':'cssExport()');
    });
  }
  test('Deliver downloads preserve saved settings', () => evaluate('projectJson()')===beforeWebsiteDownloads);
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
  await importFile(' '.repeat(4000001));
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
      return [...doc.querySelectorAll('.sample-header .sample-nav a')].every(link=>win.getComputedStyle(link).textDecorationLine==='none') && win.getComputedStyle(doc.querySelector('.sample-footer .footer-links a')).textDecorationLine===(underline?'underline':'none');
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
    const checks=[['main','paddingLeft',32],['.sample-hero','paddingTop',80],['.sample-section','paddingTop',64],['.card','paddingTop',24],['.sample-home h1','marginBottom',16],['.sample-lead','marginBottom',24],['.card-grid','columnGap',24],['.sample-home .input','paddingLeft',16],['.sample-home .input','paddingTop',8],['.sample-footer .footer-inner','paddingTop',32]];
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
  test('Export and live preview use Home, About, Resources and Contact footer shortcuts in order', () => {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return [parsed,previewDoc()].every(doc=>JSON.stringify([...doc.querySelectorAll('footer nav[aria-label="Footer navigation"] a')].map(link=>[link.textContent,link.getAttribute('href')]))===JSON.stringify([['Home','#home'],['About','#about'],['Resources','#resources'],['Contact','#contact']]));
  });
  for (const link of [...previewDoc().querySelectorAll('footer nav[aria-label="Footer navigation"] a')]) {
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
  test('Inspector theme selection synchronizes project editors, preview and exported HTML', () => evaluate('state.theme')==='dark' && d.documentElement.dataset.projectTheme==='dark' && d.documentElement.dataset.theme==='light' && d.getElementById('jTheme').value==='dark' && d.getElementById('previewTheme').value==='dark' && previewDoc().documentElement.dataset.theme==='dark' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('previewPage').title.includes('dark'));
  test('Inspector theme is saved to the active project', () => JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='dark');
  test('Theme selection retains a CSS export containing both theme definitions', () => evaluate('cssExport()')===bothThemeCss && evaluate('cssExport()').includes('[data-theme="dark"]'));
  input('previewTheme','light','change'); await wait();
  test('Preview theme control synchronizes the inspector and saved project', () => d.getElementById('dockTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[themedProject].data.theme==='light');
  const savedBeforeStudioToggle=JSON.stringify(saved()), filesBeforeStudioToggle=evaluate('[projectJson(),htmlExport(),cssExport()]');
  d.getElementById('themeToggle').click(); await wait();
  test('Studio appearance leaves the active saved project and exported files unchanged',()=>JSON.stringify(saved())===savedBeforeStudioToggle && JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'))===JSON.stringify(filesBeforeStudioToggle));
  test('Studio appearance toggle leaves page theme controls and preview unchanged', () => d.documentElement.dataset.theme==='dark' && d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light');
  evaluate('importConfig({project:"Imported theme",theme:"light",studioAppearance:"light"})'); await wait();
  test('Imported theme reaches both selectors and the generated preview', () => d.getElementById('dockTheme').value==='light' && d.getElementById('previewTheme').value==='light' && previewDoc().documentElement.dataset.theme==='light' && previewDoc().title.includes('Imported theme'));
  test('Imported project cannot override the local Studio preference',()=>d.documentElement.dataset.theme==='dark' && w.localStorage.getItem('dss-studio-appearance')==='dark');
  d.getElementById('jProjects').value=themedProject;d.getElementById('jLoadLocal').click();await wait();
  test('Loading a saved project preserves Studio appearance and restores its page theme',()=>d.documentElement.dataset.theme==='dark' && evaluate('state.theme')==='light' && d.getElementById('previewTheme').value==='light');
  reset();await wait();
  test('Project reset preserves Studio appearance',()=>d.documentElement.dataset.theme==='dark' && evaluate('state.theme')==='light');
  d.getElementById('themeToggle').click();
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
  test('Brand Colour Palette names its purpose and replaces the whole-project reset with editing', () => d.querySelector('#brandPalette > summary h2').textContent==='Step 4 of 12: Palette' && !d.getElementById('restoreDefaults') && d.getElementById('brandEditPalette').textContent==='Edit Brand Palette');
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
  // Inline state colours edit/reset existing sources, with mirrored defaults.
  reset();app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  const stateColour=(view,key)=>d.querySelector('#interaction-palette-'+view+' [data-state-colour="'+key+'"]');
  input('interaction-palette-controls-component','general','change');
  d.getElementById('jSaveLocal').click();const inlineSavedId=d.getElementById('jProjects').value;
  const hoverColour=stateColour('lesson','hover'),hoverCard=hoverColour.closest('details');hoverCard.open=true;hoverColour.focus();
  const originalDarkHover=evaluate('palette("dark").roles["primary-hover"]');
  hoverColour.value='#00BADC';hoverColour.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Inline semantic state colour keeps focus/disclosure, mirrors controls, autosaves and edits only its theme',()=>d.activeElement===hoverColour && hoverCard.open && stateColour('controls','hover').value==='#00BADC' && evaluate('state.semanticOverrides.light["primary-hover"]')==='#00BADC' && JSON.parse(w.localStorage.getItem('dss-v27-projects'))[inlineSavedId].data.semanticOverrides.light['primary-hover']==='#00BADC' && evaluate('palette("dark").roles["primary-hover"]')===originalDarkHover && d.querySelector('#interaction-palette-lesson [data-interaction-state="hover"] [data-shade="500"]').textContent.includes('#00BADC'));
  input(hoverColour.id,'default','change');await wait();
  test('Inline Default removes a semantic override and restores its generated source colour',()=>!evaluate('state.semanticOverrides.light["primary-hover"]') && stateColour('lesson','hover').value==='default' && stateColour('lesson','hover').options[0].textContent.includes(evaluate('palette().roles["primary-hover"]').toUpperCase()));
  input(stateColour('lesson','invalid').id,'#00BADC','change');input(stateColour('controls','readonly').id,'#CBDB2A','change');await wait();
  test('Invalid and read-only dropdowns update their actual feedback/surface sources',()=>evaluate('state.semanticOverrides.light.danger')==='#00BADC' && evaluate('state.semanticOverrides.light["surface-muted"]')==='#CBDB2A' && d.querySelector('#status-palette-ramp-lessons [data-palette-role="danger"] [data-shade="500"]').textContent.includes('#00BADC'));
  const inlineProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(inlineProject)+')');await wait();
  test('Inline state colour choices survive JSON round-trip using existing saved fields',()=>stateColour('lesson','invalid').value==='#00BADC' && stateColour('controls','readonly').value==='#CBDB2A' && !Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/statePalette/i.test(key)));
  input('interaction-palette-controls-component','primary','change');
  input(stateColour('lesson','hover').id,'#00BADC','change');input(stateColour('controls','active').id,'#CBDB2A','change');await wait();
  test('Button hover and pressed dropdowns update separate real component properties in both themes',()=>['light','dark'].every(theme=>{const data=w.dssGetButtonContrastData().themes[theme].primary;return data.hover==='#00BADC' && data.active==='#CBDB2A';}) && stateColour('controls','hover').value==='#00BADC' && stateColour('lesson','active').value==='#CBDB2A');
  input(stateColour('lesson','hover').id,'default','change');await wait();
  test('Default removes only the selected button property override',()=>!evaluate('state.buttonDesign.overrides.primary.hover') && evaluate('state.buttonDesign.overrides.primary.active')==='#CBDB2A' && stateColour('controls','hover').value==='default');
  input(stateColour('lesson','default').id,'#00BADC','change');await wait();
  test('Shared button base dropdowns synchronize default, disabled and loading and explain the scope',()=>['default','disabled','loading'].every(key=>stateColour('lesson',key).value==='#00BADC') && d.getElementById(stateColour('lesson','default').getAttribute('aria-describedby')).textContent.includes('Disabled, Loading'));
  input(stateColour('controls','focus').id,'#00BADC','change');await wait();
  test('Focus dropdown updates the shared focus/selected source across variants',()=>w.DSStudio.statePalettes.variants.every(variant=>w.DSStudio.statePalettes.entries('light',variant).filter(entry=>['focus','selected'].includes(entry.key)).every(entry=>entry.anchor==='#00BADC')) && stateColour('lesson','selected').value==='#00BADC');
  input(stateColour('lesson','selected').id,'default','change');await wait();
  test('Focus Default restores the button default without changing other properties',()=>evaluate('state.buttonDesign.focus')==='#B86C20' && evaluate('state.buttonDesign.overrides.primary.active')==='#CBDB2A' && stateColour('controls','focus').value==='default');
  input('interaction-palette-lesson-component','outline','change');input(stateColour('lesson','default').id,'#00BADC','change');await wait();
  test('Transparent state dropdown edits its foreground while retaining a transparent background',()=>w.dssGetButtonContrastData().themes.light.outline.bg==='transparent' && w.dssGetButtonContrastData().themes.light.outline.fg==='#00BADC' && stateColour('controls','disabled').value==='#00BADC');
  input(stateColour('controls','default').id,'default','change');await wait();
  test('Transparent state Default removes the foreground override',()=>!evaluate('state.buttonDesign.overrides.outline.text') && stateColour('lesson','default').value==='default');
  const beforeInvalidStateChoice=evaluate('projectJson()');input(stateColour('lesson','hover').id,'not-a-colour','change');await wait();
  test('Inline state dropdown rejects unsupported values without changing project data',()=>evaluate('projectJson()')===beforeInvalidStateChoice);
  // Every general/button interaction state exposes shades from its resolved source.
  reset();w.dssShowWizardStep(4);await wait();
  const interactionGroups=['general','primary','secondary','accent','outline','text'];
  const interactionStates=['default','hover','focus','active','selected','disabled','loading','invalid','success','readonly'];
  for(const method of ['mix','oklch']) for(const theme of ['light','dark']) {
    input('jRamp',method);input('jTheme',theme);await wait();
    const allStateTokens=w.dssReadTokens();
    for(const group of interactionGroups) {
      const beforeStatePaletteView=evaluate('projectJson()');
      input('interaction-palette-controls-component',group,'change');await wait();
      const entries=w.DSStudio.statePalettes.entries(theme,group);
      test(method+' '+theme+' '+group+' has every state, eleven exported shades and a configuration source',()=>entries.length===(group==='general'?10:7) && entries.every(entry=>{
        const expected=evaluate('makeRamp('+JSON.stringify(entry.anchor)+',state.method)');
        return Array.from({length:11},(_,i)=>[50,100,200,300,400,500,600,700,800,900,950][i]).every(step=>{
          const token=allStateTokens.find(token=>token.name===entry.prefix+'-'+step && (token.scope==='Dark')===(theme==='dark'));
          return token && token.value===expected[step] && w.dssTokenSource(token)?.control===entry.control;
        });
      }));
      test(method+' '+theme+' '+group+' mirrored state lessons show actual CSS and preserve project data',()=>['interaction-palette-controls','interaction-palette-lesson'].every(id=>d.getElementById(id+'-component').value===group && [...d.querySelectorAll('#'+id+' [data-interaction-state]')].length===entries.length && entries.every(entry=>{
        const card=d.querySelector('#'+id+' [data-interaction-state="'+entry.key+'"]');
        return card.querySelectorAll('[data-shade]').length===11 && card.querySelector('[data-shade="500"]').textContent.includes(entry.prefix+'-500: '+entry.anchor+';');
      })) && evaluate('projectJson()')===beforeStatePaletteView);
      test(method+' '+theme+' '+group+' gives every state a labelled Default and brand colour dropdown',()=>['controls','lesson'].every(view=>entries.every(entry=>{const select=stateColour(view,entry.key);return select && d.querySelector('label[for="'+select.id+'"]') && d.getElementById(select.getAttribute('aria-describedby')) && select.options[0].value==='default' && [...select.options].some(option=>option.value==='#00BADC');})));
    }
  }
  input('interaction-palette-controls-component','outline','change');await wait();
  test('Transparent variant state ramps explicitly use the foreground source',()=>['default','disabled','loading'].every(key=>{
    const entry=w.DSStudio.statePalettes.entries('dark','outline').find(entry=>entry.key===key);
    return entry.source==='--button-outline-text' && entry.control==='bdText' && entry.cue.includes('transparent') && d.querySelector('#interaction-palette-lesson [data-interaction-state="'+key+'"]').textContent.includes('transparent');
  }));
  evaluate('dssSetButtonContrastColour("outline","bg","#3a5b7c")');await wait();
  test('Button overrides regenerate state ramps and update transparent-source routing without stale views',()=>{
    const entry=w.DSStudio.statePalettes.entries('dark','outline').find(entry=>entry.key==='default');
    return entry.anchor==='#3A5B7C' && entry.source==='--button-outline-bg' && entry.control==='bdDefaultBg' && d.querySelector('#interaction-palette-lesson [data-interaction-state="default"] [data-shade="500"]').textContent.includes('#3A5B7C') && w.dssTokenSource({name:entry.prefix+'-500',scope:'Dark'}).control==='bdDefaultBg';
  });
  d.querySelector('#interaction-palette-lesson [data-interaction-state="default"] button').click();await wait();
  test('Interaction shade inspector contains the complete current stylesheet and preview uses it',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  d.querySelector('#interaction-palette-lesson [data-interaction-state="hover"] button:last-child').click();await wait();
  test('Button state shade configure reaches the correct variant and property',()=>w.DSStudio.activeStage===7 && d.getElementById('bdVariant').value==='outline' && d.activeElement===d.getElementById('bdHover'));
  w.dssShowWizardStep(4);input('interaction-palette-controls-component','general','change');await wait();
  const generalDisclosure=d.querySelector('#interaction-palette-controls [data-interaction-state="readonly"]');generalDisclosure.open=true;
  input('jTheme','light');await wait();
  test('General state theme changes preserve disclosure nodes and include all State Explorer states',()=>generalDisclosure===d.querySelector('#interaction-palette-controls [data-interaction-state="readonly"]') && generalDisclosure.open && [...d.getElementById('advState').options].every(option=>interactionStates.includes(option.value)));
  d.querySelector('#interaction-palette-lesson [data-interaction-state="invalid"] button:last-child').click();await wait();
  test('Invalid state shade configure reaches the current theme Danger semantic colour',()=>w.DSStudio.activeStage===6 && d.getElementById('jSemanticRole').value==='danger' && evaluate('state.theme')==='light');
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    d.querySelectorAll('#interaction-palette-controls details, #interaction-palette-lesson details').forEach(el=>el.open=true);
    test('All expanded interaction state ramps fit '+width+'px with usable component and colour selectors',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['interaction-palette-controls','interaction-palette-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1 && d.getElementById(id+'-component').getBoundingClientRect().height>=44 && [...el.querySelectorAll('[data-state-colour]')].every(select=>select.getBoundingClientRect().height>=44);}));
  }
  const stableCatalogueRow=d.querySelector('#tokenTableBody tr');w.dssUpdateTokenCatalogue();
  test('Unchanged state exports retain catalogue rows instead of rebuilding the large table',()=>d.querySelector('#tokenTableBody tr')===stableCatalogueRow);
  input('tokenSearch','');const stableBrandCatalogueRow=d.querySelector('#tokenTableBody tr');input('jBase',19);await wait();
  test('Editing one foundation token refreshes its catalogue value while reusing unaffected rows',()=>d.querySelector('#tokenTableBody tr')===stableBrandCatalogueRow && d.querySelector('[data-token-name="--font-size-base"]').closest('tr').textContent.includes('19px'));
  // Status ramps reuse resolved theme colours and the exported shade generator.
  reset();w.dssShowWizardStep(4);await wait();
  for(const method of ['mix','oklch']) for(const theme of ['light','dark']) {
    input('jRamp',method);input('jTheme',theme);await wait();
    test(method+' '+theme+' status ramps preserve semantic anchors and match preview/export',()=>evaluate(`
      STATUS_PALETTE_ROLES.every(role=>{
        const anchor=palette('${theme}').roles[role],ramp=makeRamp(anchor,state.method);
        return steps.every(step=>cssExport().includes('--'+role+'-'+step+': '+ramp[step]+';')) && ramp[500]===anchor;
      })`) && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
    test(method+' '+theme+' status teaching reads all eleven theme-specific exported steps',()=>['status-palette-steps','status-palette-ramp-lessons'].every(id=>['success','warning','danger'].every(role=>{
      const rows=[...d.querySelectorAll('#'+id+' [data-palette-role="'+role+'"] [data-shade]')];
      const tokens=w.dssReadTokens().filter(row=>(row.scope==='Dark')===(theme==='dark'));
      return rows.length===11 && rows.every(row=>row.textContent.includes('--'+role+'-'+row.dataset.shade+': '+tokens.find(token=>token.name==='--'+role+'-'+row.dataset.shade).value+';'));
    })) && d.getElementById('status-palette-theme').textContent.includes(theme==='dark'?'Dark':'Light'));
  }
  evaluate('state.semanticOverrides={light:{success:"#246840",warning:"#784500",danger:"#903344"},dark:{success:"#88DDAA",warning:"#EECC77",danger:"#EE8899"}};apply();renderCode()');await wait();
  test('Status overrides regenerate each theme independently and catalogue routes to the semantic source',()=>['light','dark'].every(theme=>['success','warning','danger'].every(role=>{
    const token=w.dssReadTokens().find(row=>row.name==='--'+role+'-500' && (row.scope==='Dark')===(theme==='dark'));
    const source=w.dssTokenSource(token);
    return token.value===evaluate('state.semanticOverrides.'+theme+'.'+role) && token.type==='Colour ramp' && source.step===6 && source.semantic===role && source.control==='jSemanticRole';
  })));
  d.querySelector('#status-palette-steps [data-palette-role="danger"] button').click();await wait();
  test('Status shade inspection opens complete synchronized CSS',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true');
  const statusBeforeConfigure=evaluate('projectJson()');
  d.querySelector('#status-palette-steps [data-palette-role="warning"] .button-row button:last-child').click();await wait();
  test('Status configuration reaches the correct theme role without changing project data',()=>w.DSStudio.activeStage===6 && d.getElementById('jSemanticRole').value==='warning' && evaluate('state.theme')==='dark' && evaluate('projectJson()')===statusBeforeConfigure);
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    d.querySelectorAll('#status-palette-steps details, #status-palette-ramp-lessons details').forEach(el=>el.open=true);
    test('Expanded status steps fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['status-palette-steps-controls','status-palette-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  // Palette process: explicit token names, exported ramps and final Prototype.
  reset();app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  d.getElementById('jBrandEditor').closest('details').open=true;
  const tokenField=()=>d.querySelector('[data-brand-id="blue"] [data-brand-field="id"]');
  const beforeTokenRoles=evaluate('JSON.stringify([state.primary,state.secondary,state.accent])');
  const displayName=d.querySelector('[data-brand-id="blue"] [data-brand-field="name"]');
  displayName.value='Ocean blue';displayName.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Colour display names remain independent of brand token names',()=>tokenField().value==='blue' && evaluate('cssExport()').includes('--brand-blue: #004780'));
  const stableTokenInput=tokenField();stableTokenInput.focus();stableTokenInput.value='ocean-blue';stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
  test('Token rename updates exports, teaching surfaces and catalogue while retaining focus and copied roles',()=>d.activeElement===stableTokenInput && d.querySelector('[data-brand-id="ocean-blue"] [data-brand-field="id"]')===stableTokenInput && evaluate('cssExport()').includes('--brand-ocean-blue: #004780') && !evaluate('cssExport()').includes('--brand-blue:') && d.getElementById('palette-brand-token-list').textContent.includes('--brand-ocean-blue: #004780;') && w.dssReadTokens().some(row=>row.name==='--brand-ocean-blue') && evaluate('JSON.stringify([state.primary,state.secondary,state.accent])')===beforeTokenRoles);
  for(const invalid of ['white','Bad name','x;--evil','']) {
    stableTokenInput.value=invalid;stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));await wait();
    test('Token suffix rejects '+JSON.stringify(invalid)+' without changing saved data',()=>!stableTokenInput.validity.valid && evaluate('state.brandPalette.some(item=>item.id==="ocean-blue")') && evaluate('cssExport()').includes('--brand-ocean-blue: #004780'));
  }
  stableTokenInput.value='ocean-blue';stableTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));
  d.getElementById('jSaveLocal').click();const tokenProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(tokenProject)+')');await wait();
  test('Token suffix survives project JSON import and local storage',()=>d.querySelector('[data-brand-id="ocean-blue"] [data-brand-field="id"]').value==='ocean-blue' && Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>project.data.brandPalette.some(item=>item.id==='ocean-blue')));
  test('Palette sequence puts Main Palette generation before backgrounds, then interaction state steps in both panes',()=>{
    const pairs=[[d.getElementById('jRamp'),d.getElementById('palette-steps-controls')],[d.getElementById('palette-steps-controls'),d.querySelector('.page-background-editor')],[d.getElementById('palette-token-lesson'),d.getElementById('webpage-background-lesson')],[d.querySelector('.page-background-editor'),d.getElementById('interaction-palette-controls')],[d.getElementById('webpage-background-lesson'),d.getElementById('interaction-palette-lesson')]];
    return pairs.every(([before,after])=>Boolean(before.compareDocumentPosition(after)&w.Node.DOCUMENT_POSITION_FOLLOWING));
  });
  for(const method of ['mix','oklch']) for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) {
    for(const [role,hex] of (method==='mix'?[['primary','#004780'],['secondary','#495965'],['accent','#CBDB2A']]:[['primary','#00BADC'],['secondary','#F37327'],['accent','#EF426F']])) input('j'+role[0].toUpperCase()+role.slice(1)+'Brand',hex,'change');
    input('jRamp',method);d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);await wait();
    test(method+' '+mode+' '+theme+' all Main Palette shade steps match exported tokens',()=>evaluate('state.method')===method && ['primary','secondary','accent'].every(role=>{
      const rows=[...d.querySelectorAll('#palette-ramp-lessons [data-palette-role="'+role+'"] [data-shade]')];
      const tokens=w.dssReadTokens();return rows.length===11 && rows.every(row=>row.textContent.includes('--'+role+'-'+row.dataset.shade+': '+tokens.find(token=>token.name==='--'+role+'-'+row.dataset.shade).value+';')) && rows.find(row=>row.dataset.shade==='500').textContent.includes(evaluate('state.'+role).toUpperCase()) && rows.find(row=>row.dataset.shade==='500').dataset.anchor==='true';
    }));
    test(method+' '+mode+' '+theme+' semantic explanation follows both exported themes',()=>['primary','secondary','accent'].every(role=>{
      const text=d.querySelector('#palette-ramp-lessons [data-palette-role="'+role+'"] .palette-token-chain').textContent;
      const tokens=w.dssReadTokens().filter(token=>token.name==='--'+role);return tokens.every(token=>text.includes('--'+role+': '+token.value+';')) && text.includes('generated from --'+role+'-'+(role==='secondary'?700:500)) && text.includes('generated from --'+role+'-300');
    }));
  }
  input('jPrimaryBrand','#004780','change');evaluate('state.semanticOverrides={light:{primary:"#123456"},dark:{}};apply()');await wait();
  test('Palette lesson distinguishes semantic overrides from generated shade values',()=>d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] .palette-token-chain').textContent.includes('--primary: #123456; (custom semantic override)') && d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] [data-shade="500"]').textContent.includes('#004780'));
  d.querySelector('#palette-ramp-lessons [data-palette-role="primary"] button').click();await wait();
  test('Palette shade inspection shows complete current CSS',()=>d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true');
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();d.getElementById('jBrandEditor').closest('details').open=true;d.querySelectorAll('#main-palette-steps details').forEach(el=>el.open=true);
    test('Palette token teaching and expanded ramps fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['palette-steps-controls','palette-token-lesson','jBrandEditor'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();w.dssShowWizardStep(4);await wait();
  const resetTokenInput=d.querySelector('[data-brand-id="blue"] [data-brand-field="id"]');resetTokenInput.focus();resetTokenInput.value='white';resetTokenInput.dispatchEvent(new w.Event('change',{bubbles:true}));reset();await wait();
  test('Reset restores token suffix values and clears stale validation while retaining editor focus',()=>resetTokenInput.value==='blue' && resetTokenInput.validity.valid && d.activeElement===resetTokenInput);
  w.dssShowWizardStep(0,false);await wait();
  const beforeOrderedWalk=evaluate('projectJson()');
  test('Centre lessons follow wizard order immediately after the unchanged preview',()=>[...d.querySelectorAll('#main > .studio-section')].slice(1,13).every((section,position)=>section.id===w.DSStudio.orderedStages[position].lesson));
  for(const [position,index] of w.DSStudio.stageOrder.entries()) {
    if(position)d.getElementById('jNext').click();await wait();
    test('Next follows stage '+(position+1)+' '+w.DSStudio.stages[index].label,()=>w.DSStudio.activeStage===index && d.getElementById('jProgress').textContent.startsWith('Step '+(position+1)+' of 12') && d.querySelector('[data-journey-step="'+index+'"]').getAttribute('aria-current')==='step' && evaluate('projectJson()')===beforeOrderedWalk);
  }
  const finalPrototypeDocument=previewDoc();d.getElementById('reviewFinalPrototype').click();await wait();
  test('Final Prototype reviews the existing live page with native preview focus',()=>d.getElementById('studio-section-4').open && d.activeElement===d.querySelector('#studio-section-4 > summary') && previewDoc()===finalPrototypeDocument && d.getElementById('jNext').hidden);
  d.getElementById('reviewPrototypeExport').click();await wait();
  test('Prototype export route opens existing Deliver without replacing project or preview',()=>w.DSStudio.activeStage===11 && !d.querySelector('[data-journey-pane="11"]').hidden && previewDoc()===finalPrototypeDocument && evaluate('projectJson()')===beforeOrderedWalk);
  // End palette process checks.
  // Neutral palette follows Primary UI without a second editable anchor.
  reset();w.dssShowWizardStep(4);await wait();
  const neutralRows=()=>w.dssReadTokens().filter(row=>/^--neutral-\d+$/.test(row.name));
  for(const method of ['mix','oklch']) for(const primary of ['#004780','#F37327','#008050','#000000','#FFFFFF','#808080']) {
    input('jRamp',method);input('jPrimary',primary);await wait();
    const colours=neutralRows().map(row=>row.value);
    test(method+' '+primary+' produces eleven valid neutral steps ordered light to dark',()=>colours.length===11 && new Set(colours).size===11 && colours.every((hex,i)=>/^#[0-9A-F]{6}$/.test(hex) && (i===0 || evaluate('lum('+JSON.stringify(colours[i-1])+')')>evaluate('lum('+JSON.stringify(hex)+')'))));
    test(method+' '+primary+' neutral midpoint retains hue at low chroma or remains grey',()=>{
      const source=evaluate('rgbToOklch(state.primary)'),mid=evaluate('rgbToOklch(palette().n[500])');
      const delta=Math.abs(Math.atan2(Math.sin(source[2]-mid[2]),Math.cos(source[2]-mid[2])));
      const rgb=evaluate('hexRgb(palette().n[500])');
      return mid[1]<=Math.min(source[1]*.12,.025)+.003 && (source[1]<.005?Math.max(...rgb)-Math.min(...rgb)<=1:delta<.2) && Math.abs(mid[0]-.6)<.005;
    });
    test(method+' '+primary+' neutral lesson reads real tokens and distinguishes its midpoint',()=>['main-palette-steps','palette-ramp-lessons'].every(id=>{
      const rows=[...d.querySelectorAll('#'+id+' [data-palette-role="neutral"] [data-shade]')];
      return rows.length===11 && rows.every(row=>row.textContent.includes('--neutral-'+row.dataset.shade+': '+neutralRows().find(token=>token.name==='--neutral-'+row.dataset.shade).value+';')) && rows.find(row=>row.dataset.shade==='500').textContent.includes('derived midpoint');
    }));
  }
  input('jPrimary','#004780');await wait();const blueNeutrals=JSON.stringify(neutralRows());
  input('jSecondary','#F37327');input('jAccent','#EF426F');await wait();
  test('Supporting and Accent changes do not alter Neutral',()=>JSON.stringify(neutralRows())===blueNeutrals);
  input('jPrimary','#F37327');await wait();
  test('Changing Primary UI hue updates Neutral and all background option groups',()=>JSON.stringify(neutralRows())!==blueNeutrals && ['page','header','main','footer'].every(region=>{
    const options=[...d.getElementById(region+'-background-brand').querySelectorAll('optgroup option')];return options.length===11 && options.every((option,i)=>option.value===neutralRows()[i].value && option.textContent.includes(neutralRows()[i].name));
  }));
  const selectedNeutral=neutralRows().find(row=>row.name==='--neutral-100').value;
  for(const region of ['page','header','main','footer']) input(region+'-background-brand',selectedNeutral,'change');
  await wait();
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const region of ['page','header','main','footer'])input(region+'-background-brand',selectedNeutral,'change');await wait();
    const checkNeutral=(pd,pw)=>['body','header','main','footer'].every(region=>pw.getComputedStyle(pd.querySelector(region==='body'?'body':'body > '+region)).backgroundColor==='rgb('+evaluate('hexRgb('+JSON.stringify(selectedNeutral)+')').join(', ')+')');
    test(mode+' '+theme+' applies a neutral step in all four live backgrounds',()=>checkNeutral(previewDoc(),previewWindow()) && neutralRows().length===11);
    const page=d.createElement('iframe');page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(page);await wait();
    test(mode+' '+theme+' standalone export includes and applies Neutral',()=>checkNeutral(page.contentDocument,page.contentWindow) && page.contentDocument.querySelector('style').textContent.includes('--neutral-100: '+selectedNeutral));page.remove();
  }
  const assignedNeutrals=evaluate('JSON.stringify(state.semanticOverrides)');input('jPrimary','#008050');await wait();
  test('New neutral generation preserves previously copied background choices',()=>evaluate('JSON.stringify(state.semanticOverrides)')===assignedNeutrals && evaluate('palette().roles.background')===selectedNeutral);
  const neutralProject=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();reset();evaluate('importConfig('+JSON.stringify(neutralProject)+')');await wait();
  test('Neutral regenerates from saved Primary and method without storing another anchor',()=>evaluate('state.primary')==='#008050' && neutralRows().length===11 && !Object.hasOwn(JSON.parse(evaluate('projectJson()')),'neutral') && evaluate('JSON.stringify(state.semanticOverrides)')===assignedNeutrals);
  test('Neutral catalogue tokens are classified and configured from Primary UI',()=>neutralRows().every(row=>row.type==='Colour ramp' && w.dssTokenSource(row).control==='jPrimary' && w.dssTokenSource(row).step===4));
  w.dssConfigureToken(neutralRows()[0]);await wait();
  test('Configure Neutral focuses Primary rather than creating an independent colour',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('jPrimary'));
  const neutralCandidates=w.dssGetContrastChecks().filter(row=>/^neutral-\d+ /.test(row.name));
  test('Every neutral step has contrast candidates with valid Primary source targets',()=>neutralCandidates.length===44 && neutralCandidates.every(row=>row.scope==='candidate' && row.targets.some(target=>target.type==='anchor' && target.key==='primary')));
  d.querySelector('#palette-ramp-lessons [data-palette-role="neutral"] button').click();await wait();
  test('Neutral Inspect CSS uses the current complete stylesheet',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--neutral-500:'));
  const neutralBackgroundInspect=d.querySelectorAll('#palette-ramp-lessons [data-palette-role="neutral"] button')[1];neutralBackgroundInspect.click();await wait();
  test('Neutral background inspection targets an existing semantic declaration',()=>neutralBackgroundInspect.textContent==='Inspect background CSS' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--background:') && d.getElementById('dockCss').scrollTop>0);
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);d.querySelector('#main-palette-steps [data-palette-role="neutral"]').open=true;await wait();
    test('Neutral palette fits '+width+'px with expanded steps',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['main-palette-steps','palette-ramp-lessons'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();await wait();
  test('Reset restores the Primary-derived neutral default',()=>JSON.stringify(evaluate('palette().n'))===JSON.stringify(evaluate('makeNeutralRamp(DEFAULT.primary,DEFAULT.method)')));
  input('jRamp','mix');evaluate('resetStudio()');await wait();
  test('Reset restores OKLCH and its neutral output after RGB mix',()=>evaluate('state.method')==='oklch' && d.getElementById('jRamp').value==='oklch' && JSON.stringify(evaluate('palette().n'))===JSON.stringify(evaluate('makeNeutralRamp(state.primary,"oklch")')));
  input('jRamp','mix');d.getElementById('jNewLocal').click();await wait();
  test('New projects restore OKLCH after choosing RGB mix',()=>evaluate('state.method')==='oklch' && d.getElementById('method').value==='oklch');
  for(const method of ['mix','oklch']) {
    evaluate('importConfig({method:'+JSON.stringify(method)+'})');await wait();
    test('Import preserves explicit '+method+' ramp choice',()=>evaluate('state.method')===method && d.getElementById('jRamp').value===method && d.getElementById('method').value===method);
  }
  evaluate('importConfig({method:"invalid"})');await wait();
  test('Invalid imported methods fall back to OKLCH',()=>evaluate('state.method')==='oklch');
  evaluate('importConfig({})');await wait();
  test('Projects without a method inherit OKLCH',()=>evaluate('state.method')==='oklch');
  // End neutral palette checks.
  // Background transparency paints alpha without fading region contents.
  reset();w.dssShowWizardStep(4);await wait();
  const opacityRegions=['body','header','main','footer'];
  const opacityId=region=>(region==='body'?'page':region)+'-background';
  test('Background opacity defaults to fully opaque for existing projects',()=>opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1 && d.getElementById(opacityId(region)+'-opacity').value==='100'));
  const opacityColours={body:'#004780',header:'#F37327',main:'#5FC5BF',footer:'#EF426F'};
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) for(const percent of [0,35,100]) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const region of opacityRegions){input(opacityId(region)+'-hex',opacityColours[region]);input(opacityId(region)+'-opacity',percent);}
    await wait();
    const checkOpacity=(pd,pw)=>opacityRegions.every(region=>{
      const el=pd.querySelector(region==='body'?'body':'body > '+region),style=pw.getComputedStyle(el),rgb=evaluate('hexRgb('+JSON.stringify(opacityColours[region])+')');
      return style.opacity==='1' && style.backgroundColor===(percent===100?'rgb('+rgb.join(', ')+')':'rgba('+rgb.join(', ')+', '+percent/100+')');
    });
    test(mode+' '+theme+' '+percent+'% background paint preserves full content opacity',()=>checkOpacity(previewDoc(),previewWindow()) && previewWindow().getComputedStyle(previewDoc().querySelector('header a')).opacity==='1' && opacityRegions.every(region=>d.getElementById(opacityId(region)+'-opacity-value').textContent===percent+'%' && d.getElementById(region+'-background-opacity-code').textContent==='--'+region+'-background-opacity: '+percent/100+';'));
    const standalone=d.createElement('iframe');standalone.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(standalone);await wait();
    test(mode+' '+theme+' '+percent+'% standalone transparency matches live output',()=>checkOpacity(standalone.contentDocument,standalone.contentWindow) && standalone.contentWindow.getComputedStyle(standalone.contentDocument.documentElement).backgroundColor===evaluate("'rgb('+hexRgb(palette().roles.surface).join(', ')+')'"));standalone.remove();
  }
  input('jTheme','light');input('jSemanticRole','surface','change');evaluate('state.semanticOverrides.light.surface="#FFFFFF";state.semanticOverrides.light.text="#000000";apply()');
  input('page-background-opacity',50);input('header-background-opacity',50);await wait();
  test('Translucent Header contrast uses the actual Body-over-canvas blend',()=>{
    const row=w.dssGetContrastChecks().find(row=>row.theme==='light'&&row.group==='Text and semantic roles'&&row.name==='--text'&&row.location==='--header-background');
    return row.bg==='#B98B73' && d.getElementById('header-background-composite').textContent.includes('#B98B73') && d.getElementById('body-background-composite').textContent.includes('#80A3C0');
  });
  const savedOpacity=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();await wait();
  test('Opacity values autosave with the existing project state',()=>Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>project.data.backgroundOpacity?.light?.header===50));
  reset();evaluate('importConfig('+JSON.stringify(savedOpacity)+')');await wait();
  test('JSON round trip restores both themes and all opacity sliders',()=>evaluate('state.backgroundOpacity.light.header')===50 && evaluate('state.backgroundOpacity.dark.header')===100 && d.getElementById('header-background-opacity').value==='50');
  const previousOpacity=evaluate('state.backgroundOpacity.light.header');input('header-background-brand',evaluate('palette().n[100]'),'change');await wait();
  test('Brand or Neutral background selection preserves its opacity choice',()=>evaluate('state.backgroundOpacity.light.header')===previousOpacity);
  input('jTheme','dark');input('header-background-opacity',25);input('main-background-opacity',35);d.getElementById('header-background-reset').click();await wait();
  test('Background reset clears current-region colour and alpha only',()=>!evaluate('state.backgroundOpacity.dark.header') && !evaluate('state.semanticOverrides.dark["header-background"]') && evaluate('backgroundOpacity("header")')===1 && evaluate('state.backgroundOpacity.dark.main')===35 && evaluate('state.backgroundOpacity.light.header')===50);
  const alphaToken=w.dssReadTokens().find(row=>row.name==='--header-background-opacity'&&row.scope==='Light / base');w.dssConfigureToken(alphaToken);await wait();
  test('Opacity catalogue source selects its theme and focuses its range',()=>evaluate('state.theme')==='light' && w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('header-background-opacity'));
  d.getElementById('header-background-opacity').focus();input('header-background-opacity',64);await wait();
  test('Opacity edits preserve focus and update complete inspector CSS',()=>d.activeElement===d.getElementById('header-background-opacity') && (w.DSStudio.inspector.show({language:'css',section:'all',find:'--header-background-opacity:'}),d.getElementById('dockCss').textContent===evaluate('cssExport()')) && d.getElementById('dockCss').textContent.includes('--header-background-opacity: 0.64;'));
  evaluate('importConfig({backgroundOpacity:{light:{body:-20,header:240,main:33.6,footer:"20",unknown:0},dark:{body:null,header:{bad:1},main:50,footer:0}}})');await wait();
  test('Opacity imports clamp finite numbers, round percentages and reject non-numeric data',()=>evaluate('state.backgroundOpacity.light.body===0 && state.backgroundOpacity.light.header===100 && state.backgroundOpacity.light.main===34 && !("footer" in state.backgroundOpacity.light) && !("unknown" in state.backgroundOpacity.light) && !("body" in state.backgroundOpacity.dark) && !("header" in state.backgroundOpacity.dark) && state.backgroundOpacity.dark.main===50 && state.backgroundOpacity.dark.footer===0'));
  evaluate('importConfig({backgroundOpacity:{light:{body:NaN,header:Infinity,main:-Infinity}}})');await wait();
  test('Non-finite opacity imports remain fully opaque',()=>opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    test('Opacity controls and centre model fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && opacityRegions.every(region=>{const el=d.getElementById(opacityId(region)+'-opacity');return el.getBoundingClientRect().height>=44 && el.getBoundingClientRect().width>0 && el.getAttribute('aria-describedby')==='background-opacity-help';}) && d.getElementById('webpage-background-lesson').scrollWidth<=d.getElementById('webpage-background-lesson').clientWidth+1);
  }
  app.style.width='1440px';input('page-background-opacity',0);evaluate('resetStudio()');await wait();
  test('Reset removes custom opacity data and restores opaque defaults',()=>!evaluate('state.backgroundOpacity') && opacityRegions.every(region=>evaluate('backgroundOpacity('+JSON.stringify(region)+')')===1 && d.getElementById(opacityId(region)+'-opacity').value==='100'));
  // End background transparency checks.
  // Region padding extends the existing layout without replacing content gutters.
  reset();w.dssShowWizardStep(4);await wait();
  const paddingRegions=['header','main','footer'],paddingSides=['top','right','bottom','left'];
  const paddingValues=()=>Object.fromEntries(paddingRegions.map(region=>[region,paddingSides.map(side=>evaluate('regionPadding('+JSON.stringify(region)+','+JSON.stringify(side)+')'))]));
  test('Region padding starts at zero and is available only for Header, Main and Footer',()=>paddingRegions.every(region=>d.getElementById(region+'-padding-controls') && paddingValues()[region].every(value=>value===0)) && !d.getElementById('body-padding-controls'));
  for(const mode of ['basic','advanced']) for(const theme of ['light','dark']) for(const width of [320,1440]) for(const value of [0,64]) {
    app.style.width=width+'px';d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);w.dssShowWizardStep(4);
    for(const region of paddingRegions)for(const side of paddingSides)input(region+'-padding-'+side,value);await wait();
    const checkPadding=(pd,pw)=>paddingRegions.every(region=>{
      const style=pw.getComputedStyle(pd.querySelector('body > '+region));
      const gutter=mode==='advanced'&&region==='main'?parseFloat(pw.getComputedStyle(pd.querySelector('header > .container')).paddingLeft):0;
      return paddingSides.every(side=>Math.abs(parseFloat(style.getPropertyValue('padding-'+side))-value-(['left','right'].includes(side)?gutter:0))<.1);
    });
    test(mode+' '+theme+' '+width+'px region padding '+value+'px matches live output',()=>checkPadding(previewDoc(),previewWindow()) && paddingRegions.every(region=>d.getElementById(region+'-padding-code').textContent.includes('--'+region+'-padding-left: '+value+'px;')));
    const page=d.createElement('iframe');page.style.cssText='width:'+width+'px;height:800px;border:0';page.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(page);await wait();
    test(mode+' '+theme+' '+width+'px region padding '+value+'px exports without overflow',()=>checkPadding(page.contentDocument,page.contentWindow) && page.contentDocument.documentElement.scrollWidth<=width+1);page.remove();
  }
  app.style.width='1440px';w.dssShowWizardStep(4);await wait();
  for(const [index,region] of paddingRegions.entries())for(const [sideIndex,side] of paddingSides.entries())input(region+'-padding-'+side,8+index*16+sideIndex*4);await wait();
  test('All four padding sides are independently saved and shown in the centre',()=>paddingRegions.every((region,index)=>paddingSides.every((side,sideIndex)=>evaluate('regionPadding('+JSON.stringify(region)+','+JSON.stringify(side)+')')===8+index*16+sideIndex*4 && d.getElementById(region+'-padding-'+side+'-value').textContent===(8+index*16+sideIndex*4)+' px')));
  const sharedPadding=evaluate('JSON.stringify(state.regionPadding)');input('jTheme','light');await wait();
  test('Region padding is shared across themes',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding && d.getElementById('header-padding-left').value==='20');
  input('header-background-hex','#123456');input('header-background-opacity',40);d.getElementById('header-background-reset').click();await wait();
  test('Resetting a background preserves its separate padding',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding);
  const paddingProject=JSON.parse(evaluate('projectJson()'));d.getElementById('jSaveLocal').click();await wait();
  test('Region padding autosaves in existing local projects',()=>Object.values(JSON.parse(w.localStorage.getItem('dss-v27-projects'))).some(project=>JSON.stringify(project.data.regionPadding)===sharedPadding));
  reset();evaluate('importConfig('+JSON.stringify(paddingProject)+')');await wait();
  test('Region padding round trips through project JSON',()=>evaluate('JSON.stringify(state.regionPadding)')===sharedPadding && d.getElementById('footer-padding-left').value==='52');
  const nonHeaderPadding=evaluate('JSON.stringify([state.regionPadding.main,state.regionPadding.footer,state.semanticOverrides,state.backgroundOpacity])');d.getElementById('header-padding-reset').click();await wait();
  test('Padding reset restores one region without changing colours, alpha or other regions',()=>paddingValues().header.every(value=>value===0) && evaluate('JSON.stringify([state.regionPadding.main,state.regionPadding.footer,state.semanticOverrides,state.backgroundOpacity])')===nonHeaderPadding);
  const paddingToken=w.dssReadTokens().find(row=>row.name==='--main-padding-left');w.dssConfigureToken(paddingToken);await wait();
  test('Padding catalogue source reveals and focuses the actual slider',()=>w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('main-padding-left') && d.getElementById('main-padding-controls').open);
  input('main-padding-left',17);await wait();
  test('Padding edits preserve focus and update the centre inset',()=>d.activeElement===d.getElementById('main-padding-left') && d.getElementById('main-padding-demo').style.paddingLeft==='17px');
  d.querySelector('#main-padding-demo').parentElement.querySelector('button').click();await wait();
  test('Inspect padding opens complete live CSS at the real padding tokens',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').textContent.includes('--main-padding-left: 17px;') && d.getElementById('dockCss').scrollTop>0);
  evaluate('importConfig({regionPadding:{header:{top:-10,right:500,bottom:13.6,left:"20",unknown:10},main:{top:NaN,right:Infinity,bottom:null,left:32},footer:"bad",body:{top:20}}})');await wait();
  test('Padding imports accept only bounded finite numbers and known regions/sides',()=>evaluate('state.regionPadding.header.top===0 && state.regionPadding.header.right===64 && state.regionPadding.header.bottom===14 && !("left" in state.regionPadding.header) && !("unknown" in state.regionPadding.header) && state.regionPadding.main.left===32 && !("top" in state.regionPadding.main) && !("right" in state.regionPadding.main) && !("bottom" in state.regionPadding.main) && !("body" in state.regionPadding) && !("footer" in state.regionPadding)'));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    paddingRegions.forEach(region=>d.getElementById(region+'-padding-controls').open=true);await wait();
    test('Expanded padding controls and demos fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && paddingRegions.every(region=>{
      const details=d.getElementById(region+'-padding-controls'),demo=d.getElementById(region+'-padding-demo');
      return details.scrollWidth<=details.clientWidth+1 && demo.scrollWidth<=demo.clientWidth+1 && paddingSides.every(side=>d.getElementById(region+'-padding-'+side).getBoundingClientRect().height>=44);
    }));
  }
  app.style.width='1440px';evaluate('resetStudio()');await wait();
  test('Reset clears custom region padding and restores existing spacing defaults',()=>!evaluate('state.regionPadding') && paddingRegions.every(region=>paddingValues()[region].every(value=>value===0) && d.getElementById(region+'-padding-reset').disabled));
  // End region padding checks.
  reset(); await wait(); input('tokenSearch','');
  d.querySelector('[data-journey-step="3"]').click();
  test('Wizard ends at Prototype without implying completed checks', () => !d.querySelector('[data-journey-pane="3"]').hidden && d.getElementById('jNext').hidden && d.getElementById('jProgress').textContent.includes('Step 12 of 12') && !d.querySelector('.journey-steps .is-complete'));
  d.getElementById('jBack').click();
  test('Back from Prototype reaches Deliver',()=>!d.querySelector('[data-journey-pane="11"]').hidden && !d.getElementById('jNext').hidden);
  d.getElementById('jBack').click();
  test('Back navigation reaches accessibility and restores Next', () => !d.querySelector('[data-journey-pane="10"]').hidden && !d.getElementById('jNext').hidden);
  for (const [name,scope,control,step] of [['--space-6','Light / base','jSpacing',8],['--grid-gap','Light / base','advGap',9],['--text-h1','Light / base','clampFactor',5],['--text','Dark','jSemanticRole',6],['--button-secondary-hover-text','Dark','bdHoverText',7],['--brand-blue','Light / base',null,4]]) {
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
    for (const step of [5,8,9,10,11]) {
      d.querySelector(`[data-journey-step="${step}"]`).click();
      d.querySelectorAll(`[data-journey-pane="${step}"] details:not([hidden])`).forEach(details=>details.open=true);
      await wait();
      test(theme+' expanded wizard step '+(step+1)+' fits 320px', () => d.documentElement.scrollWidth<=320 && d.querySelector(`[data-journey-pane="${step}"]`).scrollWidth<=d.querySelector(`[data-journey-pane="${step}"]`).clientWidth+1);
    }
  }
  app.style.width='1440px'; reset(); await wait();
  const teachingProject=evaluate('projectJson()');
  d.querySelector('[data-journey-step="8"]').click();
  test('One selection connects spacing controls and lesson without changing the project', () => !d.querySelector('[data-journey-pane="8"]').hidden && !d.getElementById('studio-section-3').hidden && d.getElementById('studio-section-3').open && evaluate('projectJson()')===teachingProject && d.activeElement===d.querySelector('#studio-section-3 > summary h2'));
  d.documentElement.style.scrollBehavior='auto';
  d.documentElement.style.overflowAnchor='none';
  for (const width of [320,390,768,1280,1440,2560]) {
    app.style.width=width+'px'; await wait();
    d.querySelector('[data-journey-step="6"]').click(); await wait();
    const section=d.getElementById('studio-section-1');
    w.dispatchEvent(new w.Event('resize'));
    section.scrollIntoView({block:'start',behavior:'instant'}); await wait();
    test('Active lesson fits beneath the sticky header at '+width+'px', () => {
      const header=d.querySelector('.topbar').getBoundingClientRect(), summary=section.querySelector('summary').getBoundingClientRect();
      return summary.top>=header.bottom+7 && summary.bottom<=w.innerHeight && d.documentElement.scrollWidth<=w.innerWidth+1;
    });
    test('Inspector stays right on desktop and follows the centre on smaller screens at '+width+'px', () => {
      const code=d.querySelector('.studio-code-dock').getBoundingClientRect(), centre=d.getElementById('main').getBoundingClientRect();
      return (width>1280?code.left>=centre.right:code.top>=centre.bottom) && d.querySelector('#main > :first-child').id==='studio-section-4';
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
  test('Plan leads into Palette and Prototype is the final stage', () => {
    const labels=[...d.querySelectorAll('[data-journey-step]')].map(button=>button.textContent);
    const destinations=w.DSStudio.orderedStages.slice(0,4).map(stage=>'#'+stage.lesson);
    return ['Brief','Architecture','Wireframe','Palette'].every((label,index)=>labels[index].includes(label))
      && labels.at(-1)==='12 · Prototype' && w.DSStudio.orderedStages.filter(stage=>stage.phase==='Plan').length===3
      && JSON.stringify(destinations)===JSON.stringify(['#process-brief','#process-ia','#process-wireframe','#brandPalette']);
  });
  for (const [index,id] of ['brief','ia','wireframe','prototype'].entries()) {
    d.querySelector(`[data-journey-step="${index}"]`).click();
    const before=evaluate('projectJson()');
    await wait();
    test(id+' wizard shortcut opens its centre lesson without changing project data', () => d.getElementById('process-'+id).open && evaluate('projectJson()')===before);
    d.querySelector(`[data-journey-step="${index}"]`).click();
    test(id+' lesson returns to the correct wizard stage and focuses its heading', () => !d.querySelector(`[data-journey-pane="${index}"]`).hidden && d.activeElement===d.querySelector(`#process-${id} > summary h2`));
  }
  // Planning workshops are part of the Advanced sample; New now starts Basic.
  d.getElementById('dockModeAdvanced').click();await wait();
  input('jProject','Community learning hub'); d.getElementById('jSaveLocal').click();
  const planProjectId=d.getElementById('jProjects').value;
  for (const [key,value] of Object.entries({audience:'New community members',goal:'Find a workshop and prepare a question.',scope:'Workshop listings and resources',content:'Organiser supplies workshop copy and photographs.',delivery:'Release in two weeks; organiser approves and maintains content.',success:'Find the right workshop without help.',constraints:'Keyboard and phone access',pages:'Home\nWorkshops > Layout\nWorkshops > Colour\nResources\nContact',layout:'stack',wireframeNotes:'Put workshop choices before supporting resources.',prototypeTask:'Find the layout workshop.',prototypeNotes:'The participant hesitated at the first label.'})) input('plan-'+key,value);
  await wait();
  const processData=evaluate('JSON.stringify(state.designProcess)');
  test('Planning fields autosave with the active local project', () => JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[planProjectId].data.designProcess)===processData);
  test('Brief, architecture, wireframe and prototype artifacts use the edited plan', () => d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent==='New community members' && d.querySelector('#process-ia .process-map').textContent.includes('Workshops') && d.querySelectorAll('#process-ia .process-map > ul > li').length===4 && d.querySelectorAll('#process-ia .process-map ul ul > li').length===2 && d.querySelector('#process-wireframe .process-wireframe--stack') && d.querySelector('#process-prototype').textContent.includes('Find the layout workshop.'));
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
    const groups=w.DSStudio.process.hierarchy(Array.from({length:100},(_,i)=>'Group '+i+'x'.repeat(80)+' > Child > Ignored').join('\n'));
    return groups.length===64 && groups.every(([label,children])=>label.length===64 && children.length===1 && children[0]==='Child');
  });
  for (const value of [null,[],42,'invalid']) {
    evaluate('importConfig({designProcess:'+JSON.stringify(value)+'})');
    test('Malformed planning '+JSON.stringify(value)+' uses safe defaults', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  }
  const hostile='<img src=x onerror="window.planExecuted=true"><script>window.planExecuted=true<\/script>';
  input('plan-audience',hostile); input('plan-pages',hostile+' > Child'); input('plan-prototypeNotes',hostile); await wait();
  test('Planning text is escaped in studio lessons, exports and the live sample', () => {
    const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !d.querySelector('[data-process-artifact] img, [data-process-artifact] script') && !exported.querySelector('#design-process img, #design-process script') && !previewDoc().querySelector('#design-process img, #design-process script') && d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent===hostile && exported.querySelector('#brief-lab [data-brief-field="audience"] dd').textContent===hostile && !w.planExecuted;
  });
  reset(); await wait();
  test('Editing planning never mutates the starter defaults; reset restores every field', () => evaluate('JSON.stringify(state.designProcess)===JSON.stringify(DSStudio.process.defaults()) && JSON.stringify(DEFAULT.designProcess)===JSON.stringify(DSStudio.process.defaults())'));
  d.getElementById('process-prototype').open=true;
  d.querySelector('#process-prototype .step-more').open=true;
  w.dssRevealSection('process-prototype',false);
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
        revealAll();
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
  evaluate('resetStudio()');await wait();
  test('Sample mode resets to Basic with a labelled independent tab group', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockModeBasic').getAttribute('aria-selected')==='true' && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')==='dockModeBasic' && d.querySelector('[aria-label="Website sample complexity"]'));
  d.getElementById('dockTabHtml').click(); d.getElementById('dockModeBasic').click(); await wait();
  test('Basic selection synchronizes inspector, preview and central exports while retaining the language tab', () => evaluate('state.sampleMode')==='basic' && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('codeView').textContent===evaluate('codeContent()') && previewDoc().querySelector('.skill-cards') && !previewDoc().querySelector('#design-process'));
  test('Basic exports shared system foundations without the Advanced gallery styles', () => evaluate('cssExport()').length<advancedCss.length && evaluate('cssExport()').includes('--space-unit:') && evaluate('cssExport()').includes('--button-pad-x:') && evaluate('cssExport()').includes('repeat(auto-fit, minmax(') && !evaluate('cssExport()').includes('.sample-grid-demo'));
  const basicDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
  test('Basic hero embeds the same accessible offline illustration as Advanced and the live inspector', () => {
    const image=basicDoc.querySelector('#home img'), advanced=new w.DOMParser().parseFromString(advancedHtml,'text/html').querySelector('#home img');
    const live=previewDoc().querySelector('#home img');
    return image && image.getAttribute('src')===advanced.getAttribute('src') && image.getAttribute('src').startsWith('data:image/svg+xml;') && image.alt.length>0 && image.width===960 && image.height===720 && live.complete && live.naturalWidth===960 && live.getAttribute('src')===image.getAttribute('src') && d.getElementById('dockCss').textContent===evaluate('htmlExport()');
  });
  test('Basic HTML has exactly four main sections, one heading, logo/nav, hero, three cards, signup and footer', () => basicDoc.querySelectorAll('main > section').length===4 && basicDoc.querySelectorAll('h1').length===1 && basicDoc.querySelector('header .logo[aria-hidden="true"]') && basicDoc.querySelector('header nav[aria-label]') && basicDoc.querySelector('#home .button') && basicDoc.querySelectorAll('.skill-cards article').length===3 && basicDoc.querySelector('#signup form') && basicDoc.querySelector('footer nav[aria-label], footer nav[aria-labelledby]') && basicDoc.querySelector('footer a[href="#top"]'));
  test('Basic is a compact component showcase without long code recipes or exercises', () => basicDoc.querySelector('h1').textContent==='Start with the essentials.' && !basicDoc.querySelector('main pre, main .practice') && !/Try it:|workshop sign-up|HTML \/ Meaning/.test(basicDoc.querySelector('main').textContent) && basicDoc.querySelectorAll('main > section h2').length===3);
  test('Basic showcase keeps one native form, component FAQ and footer disclosure', () => basicDoc.querySelectorAll('details').length===3 && basicDoc.querySelectorAll('main form').length===1 && basicDoc.getElementById('contact-form') && basicDoc.getElementById('basic-faq').closest('#basic-usability') && basicDoc.getElementById('footer-sitemap'));
  test('Basic semantic structure distinguishes sections, independent articles and related aside content', () => basicDoc.querySelectorAll('main').length===1 && basicDoc.querySelectorAll('h1').length===1 && [...basicDoc.querySelectorAll('main section')].every(section=>section.getAttribute('aria-labelledby') && section.contains(basicDoc.getElementById(section.getAttribute('aria-labelledby')))) && basicDoc.querySelector('.layout-example .content-sidebar > article[aria-labelledby="main-content-example-title"] + aside[aria-labelledby="related-links-title"]') && basicDoc.querySelectorAll('.skill-cards > article').length===3 && !basicDoc.querySelector('asside') && basicDoc.querySelector('header nav[aria-label]') && basicDoc.querySelector('footer nav[aria-labelledby="sitemap-title"]') && basicDoc.querySelector('.skip-link').hash==='#main-content');
  test('Basic names header destinations and hero actions after the components they reach', () => [...basicDoc.querySelectorAll('.desktop-navigation a')].map(a=>a.textContent).join(',')==='Home,Components,Layouts,Forms' && [...basicDoc.querySelectorAll('#home .section-actions a')].map(a=>a.hash).join(',')==='#features,#lists');
  test('Basic form groups native radio choices with a legend and one initial choice', () => basicDoc.querySelector('#form-options > legend').textContent==='Learning preference' && basicDoc.querySelectorAll('#form-options input[type="radio"][name="learning"]').length===2 && basicDoc.querySelectorAll('#form-options input:checked').length===1 && [...basicDoc.querySelectorAll('#form-options input')].every(input=>input.closest('label')) && basicDoc.querySelector('#basic-signup-note[role="status"]'));
  test('Basic optional select and textarea start empty with matching labels', () => ['signup-topic','signup-question'].every(id=>basicDoc.getElementById(id).value==='' && !basicDoc.getElementById(id).required && basicDoc.querySelector('label[for="'+id+'"]')) && basicDoc.getElementById('signup-question').defaultValue==='');
  test('Basic footer has main navigation and a four-section eyebrow sitemap', () => basicDoc.querySelectorAll('footer nav').length===2 && basicDoc.querySelector('footer .footer-links') && basicDoc.getElementById('footer-sitemap').tagName==='DETAILS' && !basicDoc.getElementById('footer-sitemap').open && [...basicDoc.querySelectorAll('footer .footer-links a')].map(a=>a.hash).join(',')==='#home,#features,#lists,#signup' && [...basicDoc.querySelectorAll('#sitemap .sitemap-list > li > a')].map(a=>a.textContent).join(',')==='HTML & CSS essentials,Components / Flexbox,Layouts / CSS Grid,Forms / Labels & controls' && basicDoc.querySelectorAll('#sitemap a').length===12 && basicDoc.querySelector('#sitemap a[href="#home"]') && !basicDoc.querySelector('#sitemap a[href="#footer"]'));
  test('Basic gives every main section one primary CTA and one secondary route', () => [...basicDoc.querySelectorAll('main > section')].every(section => {
    const pair=section.querySelector('.section-actions');
    return pair && pair.children.length===2 && pair.children[0].classList.contains('ds-button--primary') && pair.children[1].classList.contains('ds-button--secondary') && !pair.querySelector('[disabled], [aria-busy], [data-preview-state]');
  }));
  test('Basic feature cards offer distinct paths into the practical toolkit', () => [...basicDoc.querySelectorAll('.skill-cards article > a')].map(a=>a.hash).join(',')==='#list-collection,#list-workflow,#list-terms');
  d.querySelector('[data-width="mobile"]').click(); await wait();
  const basicMenuAccent=evaluate('state.accent');
  previewDoc().querySelector('#basic-menu summary').click(); input('jAccent','#3769a8'); await wait();
  test('Basic preview preserves an open hamburger through live palette edits', () => previewDoc().getElementById('basic-menu').open && previewWindow().getComputedStyle(previewDoc().querySelector('.menu-icon')).color==='rgb(55, 105, 168)');
  previewDoc().querySelector('#basic-menu a[href="#lists"]').click(); await wait();
  test('Basic mobile navigation reaches the toolkit inside the preview', () => previewDoc().activeElement===previewDoc().getElementById('lists'));
  previewDoc().getElementById('basic-menu').open=false; input('jAccent',basicMenuAccent);
  d.querySelector('[data-width="fluid"]').click(); await wait();
  const basicActionProject=evaluate('projectJson()');
  for (const link of [...previewDoc().querySelectorAll('.section-actions a, .skill-cards article > a')]) {
    const page=previewDoc(), target=page.getElementById(link.hash.slice(1));
    link.click(); await wait();
    test('Basic action to '+link.getAttribute('href')+' navigates within the preview and focuses its destination', () => previewDoc()===page && page.activeElement===target && evaluate('projectJson()')===basicActionProject);
  }
  const basicActionSettings=evaluate('projectJson()');
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('bdVariant','secondary'); input('bdDefaultBg','#602d54'); input('bdText','#ffffff'); input('bdSize','lg');
    d.getElementById('bdMobileFull').checked=true; d.getElementById('bdMobileFull').dispatchEvent(new w.Event('input',{bubbles:true})); await wait();
    test(theme+' Basic CTAs follow wizard variant colours, size and width settings in the preview and HTML inspector', () => {
      const page=previewDoc(), links=[...page.querySelectorAll('.section-actions .ds-button--secondary')];
      return links.length===4 && links.every(a=>previewWindow().getComputedStyle(a).backgroundColor==='rgb(96, 45, 84)' && a.classList.contains('ds-button--lg') && a.classList.contains('ds-button--mobile-full')) && previewWindow().getComputedStyle(page.querySelector('.section-actions .ds-button--primary')).backgroundColor!=='rgb(96, 45, 84)' && d.getElementById('dockCss').textContent===evaluate('htmlExport()');
    });
    d.querySelector('button[data-width="mobile"]').click(); await wait();
    test(theme+' Basic mobile CTAs use the selected full width and retain visible keyboard focus', () => {
      const page=previewDoc(), pairs=[...page.querySelectorAll('.section-actions')], link=page.querySelector('#features .ds-button--secondary');
      link.focus();
      return pairs.every(pair=>[...pair.children].every(a=>Math.abs(a.getBoundingClientRect().width-pair.getBoundingClientRect().width)<2)) && link.matches(':focus-visible') && previewWindow().getComputedStyle(link).outlineStyle==='solid' && page.documentElement.scrollWidth<=390;
    });
    d.querySelector('button[data-width="fluid"]').click(); await wait();
    d.getElementById('dockTabCss').click();
    test(theme+' Basic CSS inspector and preview share the wizard-generated CTA stylesheet', () => d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && evaluate('cssExport()').includes('#602d54'));
    d.getElementById('dockTabHtml').click();
  }
  evaluate('importConfig('+basicActionSettings+')'); await wait();
  test('Basic HTML IDs, fragment destinations and form labels resolve without scripts or inline styles', () => {
    const ids=[...basicDoc.querySelectorAll('[id]')].map(el=>el.id);
    return ids.length===new Set(ids).size && !basicDoc.querySelector('script,style') && basicDoc.querySelector('link[href="tokens.css"]') && [...basicDoc.querySelectorAll('a[href^="#"]')].every(link=>basicDoc.getElementById(link.hash.slice(1))) && [...basicDoc.querySelectorAll('label[for]')].every(label=>basicDoc.getElementById(label.htmlFor));
  });
  for (const [key,id] of [['End','dockModeAdvanced'],['Home','dockModeBasic'],['ArrowRight','dockModeAdvanced'],['ArrowLeft','dockModeBasic']]) {
    const selected=d.querySelector('.studio-dock-modes [aria-selected="true"]');
    selected.dispatchEvent(new w.KeyboardEvent('keydown',{key,bubbles:true})); await wait();
    test('Mode tabs support '+key+' navigation and one tab stop', () => d.activeElement===d.getElementById(id) && d.getElementById(id).getAttribute('aria-selected')==='true' && [...d.querySelectorAll('.studio-dock-modes button')].filter(button=>button.tabIndex===0).length===1 && d.getElementById('dockSamplePanel').getAttribute('aria-labelledby')===id);
  }
  d.getElementById('dockModeAdvanced').click();await wait();
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
  test('Basic keeps section inspection without a separate exercise guide', () => !d.getElementById('dockLearning').hidden && !d.querySelector('.dock-start') && w.DSStudio.stages[8].task.includes('spacing unit'));
  for (const section of ['basics','header','hero','skills','toolkit','form','footer']) {
    input('dockSection',section,'change');
    for (const language of ['html','css']) {
      d.getElementById(language==='html'?'dockTabHtml':'dockTabCss').click();
      const shown=d.getElementById('dockCss').textContent;
      test('Basic '+section+' '+language+' excerpt isolates its authored section', () => shown.includes('SECTION: '+section) && shown!==evaluate(language==='html'?'htmlExport()':'cssExport()') && (section!=='hero' || !shown.includes('SECTION: toolkit')));
      d.getElementById('dockCopy').click(); await wait(); d.getElementById('dockDownload').click();
      test('Basic '+section+' '+language+' copies excerpt but downloads complete file', () => basicCopied===shown && basicFiles.at(-1).content===evaluate(language==='html'?'htmlExport()':'cssExport()') && basicFiles.at(-1).name===(language==='html'?'index.html':'tokens.css'));
    }
  }
  input('dockSection','hero','change');
  const beforeExercisePadding=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.hero')).paddingTop), beforeExerciseUnit=evaluate('state.spacing');
  input('jSpacing',6); await wait();
  test('Focused CSS follows live spacing changes without changing complete preview styles', () => previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('.hero')).paddingTop)===beforeExercisePadding*6/beforeExerciseUnit && d.getElementById('dockCss').textContent.includes('grid-template-columns'));
  input('dockSection','basics','change');
  test('Page basics shows current spacing token definitions for the live exercise', () => d.getElementById('dockCss').textContent.includes('--space-unit: 6px;') && d.getElementById('dockCss').textContent.includes('--space-4: calc(var(--space-unit) * 4);'));
  input('dockSection','hero','change');
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Advanced hides learning controls and always shows complete code', () => d.getElementById('dockLearning').hidden && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  d.getElementById('dockModeBasic').click(); await wait();
  test('Returning to Basic restores its section filter without saving it in project state', () => d.getElementById('dockSection').value==='hero' && !d.getElementById('dockLearning').hidden && !JSON.parse(evaluate('projectJson()')).dockSection);
  let finishExcerptCopy;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>new Promise(resolve=>{finishExcerptCopy=resolve;})}});
  d.getElementById('dockCopy').click(); input('dockSection','header','change'); finishExcerptCopy(); await wait();
  test('A delayed clipboard result cannot label another section as copied', () => d.getElementById('dockCopy').textContent==='Copy CSS excerpt');
  w.DSStudio.inspector.show();
  for (const theme of ['light','dark']) {
    input('dockTheme',theme,'change');
    for (const width of [320,1440]) {
      app.style.width=width+'px'; await wait();
      test(theme+' Basic learning controls fit at '+width+'px with expanded guide', () => {
        const learning=d.getElementById('dockLearning'), select=d.getElementById('dockSection');
        return learning.scrollWidth<=learning.clientWidth+1 && select.getBoundingClientRect().width<=learning.clientWidth && learning.clientHeight>0 && select.getBoundingClientRect().bottom<=learning.getBoundingClientRect().bottom+1 && select.labels[0].textContent==='Study a section' && select.tabIndex===0;
      });
    }
  }
  input('dockTheme','light','change');
  input('dockSection','all','change'); input('jSpacing',4); await wait();
  test('Complete file restores export parity and formatted labelled markup', () => d.getElementById('dockCss').textContent===evaluate('cssExport()') && /<article[^>]+>\n\s+<p/.test(evaluate('htmlExport()')) && /\.hero-layout \{\n\s+display: grid;/.test(evaluate('cssExport()')));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:originalClipboard}); w.download=originalDownload;
  const initialBasicImage=previewDoc().querySelector('#home img').getAttribute('src');
  input('jProject','Harbour learning club'); input('jBase',18); input('jPrimary','#196b63'); input('advGap',32); await wait();
  test('Basic hero illustration follows live palette edits and HTML exports', () => {
    const live=previewDoc().querySelector('#home img'), exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#home img');
    return live.complete && live.naturalWidth===960 && live.getAttribute('src')!==initialBasicImage && live.getAttribute('src')===exported.getAttribute('src') && decodeURIComponent(live.getAttribute('src')).includes(evaluate('palette().roles.primary'));
  });
  test('Basic design settings update its HTML, CSS, preview and source descriptions', () => previewDoc().querySelector('.brand').textContent.includes('Harbour learning club') && previewWindow().getComputedStyle(previewDoc().body).fontSize==='18px' && previewWindow().getComputedStyle(previewDoc().querySelector('.skill-cards')).gap==='32px' && d.getElementById('dockNote').textContent.startsWith('Basic CSS'));
  const basicForm=previewDoc().querySelector('form');
  test('Basic signup has required name/email/consent and native invalid-input checks', () => !basicForm.checkValidity() && ['signup-name','signup-email'].every(id=>previewDoc().getElementById(id).required) && basicForm.querySelector('input[type="checkbox"]').required);
  previewDoc().getElementById('signup-name').value='Taylor'; previewDoc().getElementById('signup-email').value='taylor@example.com'; basicForm.querySelector('input[type="checkbox"]').checked=true;
  previewDoc().getElementById('signup-topic').value='grid'; previewDoc().getElementById('signup-question').value='How do columns adapt?';
  previewDoc().querySelector('input[name="learning"][value="group"]').checked=true;
  previewDoc().getElementById('basic-faq').open=true;
  const basicBrowsingDoc=previewDoc(); basicForm.requestSubmit(); await wait();
  test('Basic live signup validates and remains a static demonstration without navigating', () => previewDoc()===basicBrowsingDoc && basicForm.checkValidity() && previewDoc().getElementById('basic-signup-note').textContent.includes('No message has been sent'));
  input('jRadius',20); await wait();
  test('Basic optional controls and native FAQ retain state across live edits', () => previewDoc().getElementById('signup-topic').value==='grid' && previewDoc().getElementById('signup-question').value==='How do columns adapt?' && previewDoc().getElementById('basic-faq').open && previewDoc().querySelector('input[name="learning"][value="group"]').checked);
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
    const footerDisclosure=pd.getElementById('footer-sitemap'),footerSummary=pd.getElementById('sitemap-toggle');
    test(theme+' Basic sitemap starts collapsed with a native disclosure and visible heading',()=>!footerDisclosure.open && footerSummary.tagName==='SUMMARY' && pw.getComputedStyle(footerSummary).display==='list-item' && footerSummary.getBoundingClientRect().height>=44 && pd.querySelector('#sitemap a').getBoundingClientRect().height===0);
    footerSummary.click();

    test(theme+' Basic standalone hero loads its current theme illustration without external assets', () => {
      const image=pd.querySelector('#home img');
      return image.complete && image.naturalWidth===960 && image.naturalHeight===720 && image.alt.length>0 && image.getAttribute('src')===evaluate('DSStudio.samples.illustration(palette().roles)');
    });
    for (const width of [320,390,768,1440]) {
      basicPage.style.width=width+'px'; await wait();
      test(theme+' Basic hamburger switches navigation at '+width+'px', () => {
        const menu=pd.getElementById('basic-menu'), desktop=pd.querySelector('.desktop-navigation');
        const links=nav=>[...nav.querySelectorAll('a')].map(link=>link.getAttribute('href')).join(',');
        const mobile=pd.querySelector('.mobile-navigation');
        menu.open=false;
        const narrow=width<=768;
        if (links(desktop)!==links(mobile) || pw.getComputedStyle(menu).display!==(narrow?'block':'none') || pw.getComputedStyle(desktop).display!==(narrow?'none':'block') || mobile.getClientRects().length) return false;
        if (!narrow) return true;
        const summary=menu.querySelector('summary'); summary.focus(); summary.click();
        const opened=menu.open && mobile.getClientRects().length>0 && pw.getComputedStyle(pd.querySelector('.menu-bars')).display==='none' && pw.getComputedStyle(pd.querySelector('.menu-close')).display!=='none' && summary.getBoundingClientRect().height>=44 && pw.getComputedStyle(summary).outlineStyle==='solid' && [...mobile.querySelectorAll('a')].every(link=>link.getBoundingClientRect().height>=44 && link.getBoundingClientRect().right<=width+1);
        summary.click();
        return opened && !menu.open && !mobile.getClientRects().length;
      });
      test(theme+' Basic toolkit is a conventional equal-width CSS Grid at '+width+'px', () => {
        const grid=pd.querySelector('.list-grid'), cards=[...grid.children], sizes=cards.map(card=>card.getBoundingClientRect());
        return pw.getComputedStyle(grid).display==='grid' && sizes.every(box=>Math.abs(box.width-sizes[0].width)<1 && box.right<=width+1) && cards.every(card=>pw.getComputedStyle(card).gridRowEnd==='auto') && (width===1440?sizes.every(box=>Math.abs(box.top-sizes[0].top)<1):true);
      });
      test(theme+' Basic hero image and text reflow at '+width+'px', () => {
        const layout=pd.querySelector('.hero-layout'), text=layout.firstElementChild.getBoundingClientRect(), image=pd.querySelector('#home img').getBoundingClientRect();
        return pw.getComputedStyle(layout).gridTemplateColumns.split(' ').length===(width<=768?1:2) && image.width>0 && Math.abs(image.width/image.height-4/3)<.01 && image.right<=width+1 && (width<=768 ? image.top>=text.bottom : image.left>=text.right);
      });
      test(theme+' Basic sitemap columns have vertically stacked child links at '+width+'px', () => {
        const groups=[...pd.querySelectorAll('#sitemap .sitemap-list > li')], children=[...pd.querySelectorAll('#sitemap .sitemap-list > li > ul')];
        const map=pd.querySelector('#sitemap'), grid=map.querySelector('.sitemap-list'), mapBox=map.getBoundingClientRect(), gridBox=grid.getBoundingClientRect();
        if (pw.getComputedStyle(pd.getElementById('sitemap-title')).textAlign!=='left' || pw.getComputedStyle(grid).justifyItems!=='center' || Math.abs((gridBox.left+gridBox.right)/2-(mapBox.left+mapBox.right)/2)>1) return false;
        return groups.length===4 && children.length===3 && children.every((list,index)=>{
          const style=pw.getComputedStyle(list), bounds=list.getBoundingClientRect(), links=[...list.querySelectorAll('a')], boxes=links.map(link=>link.getBoundingClientRect());
          return style.display==='flex' && style.flexDirection==='column' && pw.getComputedStyle(list.parentElement).textAlign==='center' && links.length===[3,4,1][index] && boxes.every((box,i)=>box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44 && Math.abs((box.left+box.right)/2-(bounds.left+bounds.right)/2)<1 && (!i||box.top>=boxes[i-1].bottom-1));
        }) && (width!==1440||groups.every(group=>Math.abs(group.getBoundingClientRect().top-groups[0].getBoundingClientRect().top)<1)) && pd.documentElement.scrollWidth<=width+1;
      });
      test(theme+' Basic content/sidebar layout and UI components fit at '+width+'px', () => {
        const layout=pd.querySelector('.content-sidebar'), children=[...layout.children], boxes=children.map(el=>el.getBoundingClientRect());
        return pw.getComputedStyle(layout).gridTemplateColumns.split(' ').length===(width<=768?1:2) && (width<=768?boxes[1].top>=boxes[0].bottom:boxes[1].left>=boxes[0].right && boxes[0].width>boxes[1].width) && [...pd.querySelectorAll('.component-demo, .content-sidebar > *, #signup select, #signup textarea, #signup fieldset')].every(el=>el.getBoundingClientRect().right<=width+1 && el.getBoundingClientRect().width>0) && pw.getComputedStyle(pd.querySelector('.media-object')).display==='flex' && pd.querySelector('.avatar[aria-hidden="true"]') && pd.querySelector('.badge').textContent==='Available';
      });
      test(theme+' Basic section actions wrap inside their containers at '+width+'px', () => [...pd.querySelectorAll('.section-actions')].every(pair=>{
        const bounds=pair.getBoundingClientRect();
        return parseFloat(pw.getComputedStyle(pair).gap)>0 && [...pair.children].every(action=>{const box=action.getBoundingClientRect();return box.left>=bounds.left-1 && box.right<=bounds.right+1 && box.height>=44;});
      }));
      test(theme+' Basic sections have distinct responsive compositions at '+width+'px', () => {
        const columns=selector=>pw.getComputedStyle(pd.querySelector(selector)).gridTemplateColumns.split(' ').length;
        const skills=pd.querySelector('.skills-intro').getBoundingClientRect(), lessons=pd.querySelector('.skill-cards').getBoundingClientRect();
        const form=pd.querySelector('.signup-form').getBoundingClientRect(), area=pd.querySelector('.signup-layout').getBoundingClientRect();
        return pw.getComputedStyle(pd.querySelector('.skills-layout')).display==='flex' && pw.getComputedStyle(pd.querySelector('.skills-layout')).flexDirection===(width<=768?'column':'row') && pw.getComputedStyle(pd.querySelector('.skill-cards')).display==='flex' && [...pd.querySelectorAll('#features *')].every(el=>!['grid','inline-grid'].includes(pw.getComputedStyle(el).display)) && columns('.signup-layout')===1 && (width<=768?lessons.top>=skills.bottom:lessons.left>=skills.right) && Math.abs((form.left+form.right)/2-(area.left+area.right)/2)<2 && pw.getComputedStyle(pd.querySelector('.signup-form')).maxWidth!=='none' && pd.querySelector('.hero-image figcaption');
      });
      test(theme+' Basic classic footer keeps its layout inside the open sitemap disclosure at '+width+'px', () => {
        const footer=pd.querySelector('.site-footer'), layout=footer.querySelector('.footer-inner');
        const identity=layout.querySelector('.footer-identity').getBoundingClientRect(), nav=layout.querySelector('nav').getBoundingClientRect(), links=[...layout.querySelectorAll('nav a')];
        return layout.children.length===2 && pw.getComputedStyle(layout).display==='grid' && footer.querySelector('.footer-brand') && !footer.querySelector('.footer-lesson') && footer.querySelectorAll('nav').length===2 && footer.querySelector('#sitemap').tagName==='NAV' && pw.getComputedStyle(footer.querySelector('.sitemap-list')).display==='grid' && (width<=768?nav.top>=identity.bottom:nav.left>=identity.right && Math.abs(nav.top-identity.top)<1) && (width!==1440||links.every(link=>Math.abs(link.getBoundingClientRect().top-links[0].getBoundingClientRect().top)<1)) && footer.querySelector('details').open && [...footer.querySelectorAll('a')].every(link=>link.getBoundingClientRect().height>=44);
      });
      test(theme+' Basic standalone page reflows with its separate stylesheet at '+width+'px', () => {
        const grid=pd.querySelector('.skill-cards'), cards=[...grid.children], first=cards[0].getBoundingClientRect();
        const columns=cards.filter(card=>Math.abs(card.getBoundingClientRect().top-first.top)<1).length;
        return pd.querySelector('link').sheet && !pd.querySelector('style,script') && pd.documentElement.scrollWidth<=width+1 && !pd.querySelector('.lesson-code') && columns===1 && pw.getComputedStyle(grid).display==='flex' && pw.getComputedStyle(pd.querySelector('.signup-layout')).gridTemplateColumns.split(' ').length===1 && [...pd.querySelectorAll('header nav a, footer nav[aria-label="Footer navigation"] a, .button')].filter(el=>el.getClientRects().length).every(el=>el.getBoundingClientRect().height>=44);
      });
    }
    pd.querySelector('#basic-faq summary').focus(); pd.querySelector('#basic-faq summary').click();
    test(theme+' Basic native FAQ opens with a visible focus outline and no scripts', () => pd.getElementById('basic-faq').open && pw.getComputedStyle(pd.querySelector('#basic-faq summary')).outlineStyle==='solid' && !pd.querySelector('script'));
    pd.querySelector('#basic-faq summary').click();
    pd.querySelector('.site-footer .sitemap-list > li > a[href="#features"]').click(); await wait();
    test(theme+' Basic footer Services link reaches its real section', () => pw.location.hash==='#features' && pd.getElementById('features').getBoundingClientRect().top>=-1);
    test(theme+' Basic standalone sitemap expands without scripts and has real destinations', () => pd.getElementById('sitemap').tagName==='NAV' && footerDisclosure.open && [...pd.querySelectorAll('#sitemap a')].every(link=>link.getBoundingClientRect().height>=44 && pd.getElementById(link.hash.slice(1))));
    pd.querySelector('.skip-link').focus();
    test(theme+' Basic skip link and focus outline are visible with keyboard focus', () => pd.activeElement===pd.querySelector('.skip-link') && pd.activeElement.getBoundingClientRect().top>=0 && pw.getComputedStyle(pd.activeElement).outlineStyle==='solid');
    pd.querySelector('.back-to-top').click(); await wait();
    test(theme+' Basic standalone Back to top uses a real native fragment destination', () => pw.location.hash==='#top' && pd.getElementById('top').getBoundingClientRect().top>=-1 && pd.getElementById('top').getBoundingClientRect().top<10);
    w.URL.revokeObjectURL(cssUrl); w.URL.revokeObjectURL(htmlUrl);
  }
  basicPage.remove();
  evaluate('importConfig({sampleMode:"<script>",project:"<img src=x onerror=alert(1)>"})');
  test('Invalid sample mode falls back to Basic', () => evaluate('state.sampleMode')==='basic');
  evaluate('importConfig({sampleMode:"basic",project:"<img src=x onerror=alert(1)>"})');
  test('Basic escapes imported project text in its title and brand', () => {
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return page.querySelectorAll('img').length===1 && page.querySelector('#home img').getAttribute('src').startsWith('data:image/svg+xml;') && !page.querySelector('script,[onerror]') && page.querySelector('.brand').textContent.includes('<img src=x onerror=alert(1)>');
  });
  evaluate('importConfig({})'); await wait();
  test('Legacy projects without a sample mode retain Advanced', () => evaluate('state.sampleMode')==='advanced' && d.getElementById('dockModeAdvanced').getAttribute('aria-selected')==='true');
  d.getElementById('dockModeAdvanced').click(); evaluate('resetStudio()'); await wait();
  test('Reset restores Basic mode and its matching preview and exports', () => evaluate('state.sampleMode')==='basic' && previewDoc().querySelector('.skill-cards') && !previewDoc().querySelector('#design-process') && evaluate('htmlExport()').includes('skill-cards') && d.getElementById('sampleModeHelp').textContent.startsWith('Basic'));
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Brief lesson teaches seven website-project prompts instead of displaying a prefilled project', () => d.querySelectorAll('#process-brief .process-brief-guide > li').length===7 && d.querySelector('#process-brief .process-brief-template').textContent.includes('[audience]') && !d.querySelector('#process-brief .process-brief-draft') && ['goal','audience','scope','content','constraints','delivery','success'].every(key=>d.getElementById('plan-'+key).value===''));
  test('Website brief covers scope, content ownership, requirements, delivery and a concrete example', () => {
    const lesson=d.querySelector('#process-brief'), guide=lesson.querySelector('.process-brief-guide').textContent;
    return ['Purpose:','Audience:','Pages and features:','Content:','Design and requirements:','Delivery:','Success:'].every(label=>guide.includes(label)) && ['out of scope','who will supply','deadline','budget','approves','maintains'].every(term=>guide.includes(term)) && lesson.querySelector('.process-brief-example').textContent.includes('online ordering is out of scope') && lesson.querySelector('.learning-reference a').href==='https://www.smashingmagazine.com/2018/02/comprehensive-website-planning-guide-part1/' && !lesson.querySelector('a[href*="gov.uk"]') && previewDoc().querySelector('#brief-lab .process-brief-example') && evaluate('htmlExport()').includes('Build [website] for [audience]');
  });
  test('Website brief example and wizard labels render cleanly with preserved saved fields', () => d.querySelector('#process-brief .process-brief-example h4').textContent==='Example: a small café website' && d.querySelector('#process-brief .process-brief-example').textContent.includes("today's opening hours") && d.querySelector('label[for="plan-goal"]').textContent==='1. Purpose' && d.querySelector('label[for="plan-constraints"]').textContent==='5. Design and requirements');
  test('Brief wizard has the seven approved lesson questions in the same order with matching labels and prompts', () => {
    const controls=[...d.querySelectorAll('#plan-brief-fields [data-process-field]')], lesson=[...d.querySelectorAll('#process-brief .process-brief-guide li')];
    return JSON.stringify(controls.map(el=>el.dataset.processField))===JSON.stringify(['goal','audience','scope','content','constraints','delivery','success']) && controls.every((el,i)=>d.querySelector('label[for="'+el.id+'"]').textContent===(i+1)+'. '+lesson[i].querySelector('strong').textContent.slice(0,-1) && lesson[i].textContent.trim().endsWith(d.getElementById(el.getAttribute('aria-describedby')).textContent));
  });
  previewDoc().getElementById('working-together').open=true;
  input('plan-audience','Draft audience'); await wait();
  test('Adding the first brief draft preserves the correct preview FAQ and menu state', () => previewDoc().getElementById('working-together').open && !previewDoc().getElementById('sample-menu').open && !previewDoc().querySelector('.process-brief-draft').open);
  reset(); await wait();
  evaluate('importConfig({designProcess:{audience:"Local readers",goal:"Find opening times",scope:"Home and contact",success:"Find an answer",constraints:"Small budget"}})'); await wait();
  test('Existing brief drafts remain available beside the training guide', () => d.querySelector('#process-brief .process-brief-guide') && d.querySelector('#process-brief [data-brief-field="audience"] dd').textContent==='Local readers' && d.getElementById('plan-goal').value==='Find opening times');
  test('Legacy combined brief notes stay intact and new Content/Delivery fields start blank', () => d.getElementById('plan-scope').value==='Home and contact' && d.getElementById('plan-constraints').value==='Small budget' && d.getElementById('plan-content').value==='' && d.getElementById('plan-delivery').value==='');
  input('plan-content','Owner supplies text, logo and photos.'); input('plan-delivery','Two weeks; owner approves and maintains.'); await wait();
  const sevenFieldBrief=evaluate('projectJson()'); reset(); evaluate('importConfig('+sevenFieldBrief+')'); await wait();
  test('Seven-field brief round trips and updates the centre draft and exported website', () => d.getElementById('plan-content').value==='Owner supplies text, logo and photos.' && d.getElementById('plan-delivery').value==='Two weeks; owner approves and maintains.' && d.querySelector('#process-brief [data-brief-field="content"] dd').textContent==='Owner supplies text, logo and photos.' && d.querySelector('#process-brief [data-brief-field="delivery"] dd').textContent==='Two weeks; owner approves and maintains.' && evaluate('htmlExport()').includes('Owner supplies text, logo and photos.') && evaluate('htmlExport()').includes('Two weeks; owner approves and maintains.') && JSON.stringify([...d.querySelectorAll('#process-brief .process-brief dt')].map(el=>el.textContent))===JSON.stringify([...d.querySelectorAll('#process-brief .process-brief-guide strong')].map(el=>el.textContent.slice(0,-1))));
  evaluate('importConfig({designProcess:{content:"x".repeat(5000),delivery:42}})'); await wait();
  test('New brief fields validate imported types and lengths', () => d.getElementById('plan-content').value.length===1200 && d.getElementById('plan-delivery').value==='');
  input('plan-content','<img src=x onerror=alert(1)>'); input('plan-delivery','<script>alert(1)<\/script>'); await wait();
  test('Content and Delivery remain escaped text in centre and exported drafts', () => !d.querySelector('#process-brief .process-brief-draft img, #process-brief .process-brief-draft script') && d.querySelector('#process-brief [data-brief-field="content"] dd').textContent.includes('<img') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#brief-lab .process-brief-draft img, #brief-lab .process-brief-draft script'));
  reset(); await wait();
  test('Reset clears all seven brief editors and saved values', () => ['goal','audience','scope','content','constraints','delivery','success'].every(key=>d.getElementById('plan-'+key).value==='' && evaluate('state.designProcess.'+key)===''));
  d.querySelector('[data-journey-step="9"]').click();
  test('Responsive is a distinct phase between Layout and Accessibility with grid controls and a centre lesson', () => !d.querySelector('[data-journey-pane="9"]').hidden && d.getElementById('advColumns').closest('[data-journey-pane]').dataset.journeyPane==='9' && !d.getElementById('responsiveDesign').hidden && d.getElementById('responsiveDesign').open);
  test('Responsive page tokens are classified as Layout and route to the correct wizard controls', () => w.dssReadTokens().filter(row=>row.name.startsWith('--page-')).every(row=>row.type==='Layout') && [['--page-max-width','responsive-maxWidth'],['--page-gutter','responsive-gutter'],['--page-gutter-wide','responsive-wideGutter']].every(([name,id])=>w.dssTokenSource({name}).step===9 && w.dssTokenSource({name}).control===id));
  evaluate('importConfig({responsiveDesign:{stack:960,wide:1,maxWidth:1e9,gutter:-20,wideGutter:"evil"}})');
  test('Responsive imports bound lengths and keep ordered breakpoints', () => evaluate('state.responsiveDesign.stack===960 && state.responsiveDesign.wide===1120 && state.responsiveDesign.maxWidth===1600 && state.responsiveDesign.gutter===8 && state.responsiveDesign.wideGutter===32'));
  evaluate('importConfig({responsiveDesign:{stack:NaN,wide:Infinity,maxWidth:null,gutter:"48",wideGutter:NaN}})');
  test('Nonfinite or nonnumeric responsive imports use safe defaults', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  for (const value of [null,[],42,'bad']) {
    evaluate('importConfig({responsiveDesign:'+JSON.stringify(value)+'})');
    test('Malformed responsive data '+JSON.stringify(value)+' uses defaults', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  }
  evaluate('importConfig({responsiveDesign:{stack:701,wide:1001,maxWidth:1237,gutter:19,wideGutter:37}})'); await wait();
  test('Valid responsive lengths retain exact imported values in sliders and exports', () => ['stack','wide','maxWidth','gutter','wideGutter'].every(key=>Number(d.getElementById('responsive-'+key).value)===evaluate('state.responsiveDesign.'+key)) && evaluate('state.responsiveDesign.stack===701 && state.responsiveDesign.maxWidth===1237'));
  reset(); d.getElementById('jSaveLocal').click(); const responsiveProjectId=d.getElementById('jProjects').value;
  for (const [key,value] of Object.entries({stack:640,wide:1152,maxWidth:1280,gutter:20,wideGutter:40})) input('responsive-'+key,value);
  await wait();
  const responsiveData=evaluate('JSON.stringify(state.responsiveDesign)'), responsiveJson=evaluate('projectJson()');
  test('Responsive lesson reports the actual preview media-query state', () => {
    const narrow=previewWindow().matchMedia('(max-width: 40rem)').matches;
    return d.getElementById('responsiveLessonViewport').textContent.includes(narrow?'Narrow: main sections stack.':'Main sections can sit side by side.');
  });

  test('Responsive controls update outputs, source recipes, preview and active local save', () => d.getElementById('responsive-stackOut').textContent.includes('40rem') && d.getElementById('responsiveRecipe').textContent.includes('@media (max-width: 40rem)') && d.getElementById('responsiveLessonViewport').textContent.includes('Current preview:') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()') && JSON.stringify(JSON.parse(w.localStorage.getItem('dss-v27-projects'))[responsiveProjectId].data.responsiveDesign)===responsiveData);
  reset(); evaluate('importConfig('+responsiveJson+')'); await wait();
  test('Responsive settings round trip through project JSON and synchronize sliders', () => evaluate('JSON.stringify(state.responsiveDesign)')===responsiveData && d.getElementById('responsive-wide').value==='1152');
  const responsivePage=d.createElement('iframe'); responsivePage.style.cssText='width:1440px;height:1000px;border:0';
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();
    for (const theme of ['light','dark']) {
      input('jTheme',theme); await wait();
      const css=evaluate('cssExport()');
      test(mode+' '+theme+' exports literal breakpoints and shared container values', () => css.includes('@media (max-width: 40rem)') && css.includes('@media (min-width: 72rem)') && css.includes('--page-max-width: 80rem;') && css.includes('--page-gutter: 1.25rem;') && !/@media[^\{]*var\(/.test(css));
      responsivePage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+css+'</style>');
      await new Promise(resolve=>{responsivePage.onload=resolve;if(!responsivePage.isConnected)d.body.append(responsivePage);});
      const pd=responsivePage.contentDocument,pw=responsivePage.contentWindow;
      for (const width of [639,640,641,1151,1152,1153,1440]) {
        responsivePage.style.width=width+'px'; await wait();
        test(mode+' '+theme+' obeys configured cutoffs and gutters at '+width+'px', () => {
          const container=pw.getComputedStyle(pd.querySelector('.container'));
          const composition=pw.getComputedStyle(pd.querySelector(mode==='basic'?'.skills-layout':'.sample-hero'));
          const columns=mode==='basic'?(composition.flexDirection==='column'?1:2):composition.gridTemplateColumns.split(' ').length;
          return pd.documentElement.scrollWidth<=width+1 && container.maxWidth==='1280px' && container.paddingLeft===(width>=1152?'40px':'20px') && columns===(width<=640?1:mode==='basic'?2:12);
        });
      }
      if (mode==='advanced') test('Advanced grid recipe reflects the edited breakpoint', () => pd.querySelector('.sample-code-solution code').textContent.includes('@media (max-width: 40rem)'));
    }
  }
  responsivePage.remove();
  test('Changing sample modes preserves shared responsive decisions', () => evaluate('JSON.stringify(state.responsiveDesign)')===responsiveData);
  reset(); await wait();
  test('Reset restores responsive defaults without mutating the starter object', () => evaluate('JSON.stringify(state.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults()) && JSON.stringify(DEFAULT.responsiveDesign)===JSON.stringify(DSStudio.responsive.defaults())'));
  d.getElementById('dockModeBasic').click(); await wait();
  test('Basic lists lesson contains unordered, ordered and description lists with titles', () => previewDoc().querySelectorAll('#lists .list-grid > article').length===3 && ['ul','ol','dl'].every(selector=>previewDoc().querySelector('#lists .list-grid '+selector)) && [...previewDoc().querySelectorAll('#lists .list-grid > article')].every(card=>card.querySelector('h3')));
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
    test(mode+' sitemap renders its intended depth and preserves the complete Architecture plan', () => {
      const page=previewDoc(), links=[...page.querySelectorAll('#sitemap a')], ids=new Set(links.map(a=>a.hash.slice(1)));
      const expected=w.DSStudio.process.samplePages(mode);
      const fullCount=expected.split('\n').length, topCount=w.DSStudio.process.hierarchy(expected).length;
      return d.getElementById('plan-pages').value===expected && links.length===w.DSStudio.sectionSitemap.nodes().length && !page.querySelector('#sitemap .sitemap-planned') && links.every(a=>page.querySelectorAll('[id="'+a.hash.slice(1)+'"]').length===1) && [...page.querySelectorAll('main > section')].every(el=>el.id && ids.has(el.id)) && d.querySelectorAll('#process-ia .process-map li').length===fullCount && (mode!=='basic'||page.querySelectorAll('#sitemap ul ul a').length===8) && evaluate('htmlExport()').includes('id="sitemap"');
    });
  }
  d.getElementById('process-ia').open=true;
  const planBeforeBasicView=evaluate('state.designProcess.pages');
  for(const theme of ['light','dark']) {
    input('jTheme',theme);
    for(const width of [320,768,1440]) {
      app.style.width=width+'px'; await wait();
      test(theme+' Basic plan aligns parent groups and related children at '+width+'px', () => {
        const map=d.querySelector('#process-ia .process-map--basic'), list=map.querySelector(':scope > ul'), groups=[...list.children];
        const gap=parseFloat(w.getComputedStyle(list).columnGap), bounds=list.getBoundingClientRect(), boxes=groups.map(group=>group.getBoundingClientRect());
        const inline=list.clientWidth>=groups.length*144+(groups.length-1)*gap;
        return groups.map(group=>group.querySelector('strong').textContent).join(',')==='Home,Components,Layouts,Forms,Footer' && w.getComputedStyle(list).display==='flex' && boxes.every(box=>box.left>=bounds.left-1 && box.right<=bounds.right+1) && (!inline||boxes.every(box=>Math.abs(box.top-boxes[0].top)<1)) && groups.every(group=>{
          const children=group.querySelector('ul'), title=group.querySelector('strong').getBoundingClientRect();
          return !children||(children.getBoundingClientRect().top>=title.bottom && Math.abs(children.getBoundingClientRect().left-title.left)<1);
        }) && map.querySelectorAll('ul ul > li').length===w.DSStudio.process.entries().filter(node=>node.depth>1).length && d.documentElement.scrollWidth<=width+1 && evaluate('state.designProcess.pages')===planBeforeBasicView && d.getElementById('plan-pages').value.includes('Forms') && d.getElementById('plan-pages').value.includes('Footer') && previewDoc().querySelector('#signup') && previewDoc().querySelector('footer');
      });
    }
  }
  app.style.width='1440px'; input('jTheme','light');
  input('plan-pages','Home\nSIGN-UP\n footer \nFlexbox > Forms'); await wait();
  test('Basic IA shows Forms/Footer aliases as part of its full model', () => [...d.querySelectorAll('#process-ia .process-map > ul > li > strong')].map(el=>el.textContent).join(',')==='Home,SIGN-UP,footer,Flexbox' && d.querySelector('#process-ia .process-map ul ul li').textContent==='Forms' && evaluate('state.designProcess.pages')==='Home\nSIGN-UP\n footer \nFlexbox > Forms');
  input('plan-pages','Forms\nFooter'); await wait();
  test('Basic IA retains Forms and Footer even when not sitemap destinations', () => d.querySelectorAll('#process-ia .process-map > ul > li').length===2 && d.querySelector('#process-ia .process-map').textContent.includes('sitemap destination outline') && evaluate('state.designProcess.pages')==='Forms\nFooter');
  input('plan-pages',w.DSStudio.process.samplePages('basic')); await wait();
  test('Basic footer contains only Components, Layouts and Forms while the complete plan is preserved', () => {
    const full=new w.DOMParser().parseFromString(evaluate('DSStudio.process.sitemapHtml()'),'text/html');
    return previewDoc().querySelectorAll('#sitemap a').length===14 && full.querySelectorAll('a').length===14 && full.querySelector('ul ul') && [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li > a')].map(a=>a.textContent).join(',')==='Components,Layouts,Forms' && previewDoc().querySelectorAll('#sitemap ul ul a').length===11 && [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].every((group,i)=>Boolean(group.querySelector('ul')));
  });
  input('plan-pages','Home > Forms\nFuture > Flexbox\nGrid & lists'); await wait();
  test('Basic expanded sitemap keeps known children under their parent and never promotes orphan children', () => [...previewDoc().querySelectorAll('#sitemap a')].map(a=>a.hash).join(',')==='#lists' && !previewDoc().querySelector('#sitemap ul ul') && evaluate('state.designProcess.pages')==='Home > Forms\nFuture > Flexbox\nGrid & lists' && d.querySelectorAll('#process-ia .process-map li').length===5);
  input('plan-pages','Flexbox > Semantic HTML\nFlexbox > Unbuilt topic\nGrid & lists > Ordered lists'); await wait();
  test('Basic expanded sitemap includes linked children and safely omits unlinked child labels', () => previewDoc().querySelectorAll('#sitemap a').length===4 && previewDoc().querySelectorAll('#sitemap ul ul a').length===2 && !previewDoc().querySelector('#sitemap .sitemap-planned') && !previewDoc().querySelector('#sitemap').textContent.includes('Unbuilt topic') && evaluate('state.designProcess.pages').includes('Unbuilt topic'));
  input('plan-pages','Home > Enquiry form\nFooter > Common questions\nServices > Website design'); await wait();
  test('Home and Footer groups and their children are omitted from custom footer navigation', () => [...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].every(group=>group.querySelector('a').hash==='#features' && group.querySelector('ul')) && previewDoc().querySelectorAll('#sitemap a').length===2 && evaluate('state.designProcess.pages').includes('Footer > Common questions'));
  const previousMockPlan="Home\nServices\nServices > Website design\nServices > Content planning\nServices > Responsive websites\nResources\nResources > Project checklist\nResources > How we work\nResources > Useful terms\nContact\nContact > Enquiry form\nContact > Common questions\nFooter";
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousMockPlan}})+')'); await wait();
  test('Previous mock-site inventory resolves to the component scope without mutating saved data', () => evaluate('state.designProcess.pages')===previousMockPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===12 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  const previousTutorialPlan='Hero\nFlexbox\nFlexbox > Semantic HTML\nFlexbox > Flexbox layout\nFlexbox > Responsive navigation\nGrid & lists\nGrid & lists > Unordered lists\nGrid & lists > Ordered lists\nGrid & lists > Description lists\nForms\nFooter';
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousTutorialPlan}})+')'); await wait();
  test('The previous complete tutorial plan resolves to the mock inventory without overwriting saved data', () => evaluate('state.designProcess.pages')===previousTutorialPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===12 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  const previousBasicPlan='Home\nWhat you can learn\nWhat you can learn > Give content meaning\nWhat you can learn > Let the layout adapt\nWhat you can learn > Make the basics easy\nLists\nLists > What to include\nLists > A simple workflow\nLists > Useful terms\nSign up\nFooter';
  evaluate('importConfig('+JSON.stringify({sampleMode:'basic',designProcess:{pages:previousBasicPlan}})+')'); await wait();
  test('Old complete Basic inventories resolve to tutorial labels without changing stored planning data', () => evaluate('state.designProcess.pages')===previousBasicPlan && d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && !previewDoc().querySelector('#sitemap .sitemap-planned') && previewDoc().querySelector('#sitemap a[href="#features"]').textContent==='Components / Flexbox');
  input('plan-pages','Home\nWhat you can learn > Give content meaning\nLists > What to include\nSign up'); await wait();
  test('Custom legacy Basic parent and child labels retain real destinations', () => previewDoc().querySelectorAll('#sitemap a').length===5 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  input('plan-pages','Home\nFeatures\nLists\nSign up\nFuture > Account'); await wait();
  test('Basic footer sitemap filters Architecture to linked parent and child entries', () => {
    const map=previewDoc().querySelector('#sitemap .sitemap-list');
    return map.children.length===3 && map.querySelectorAll('a').length===3 && !map.querySelector('ul, span, .sitemap-planned') && d.querySelector('#process-ia .process-map').textContent.includes('Account') && [...map.querySelectorAll('a')].every(a=>previewDoc().getElementById(a.hash.slice(1))) && previewDoc().querySelector('footer #sitemap');
  });
  input('plan-pages','Home\nLearn > Articles\nSign up'); await wait();
  test('Architecture edits update the centre map, Basic footer and downloadable HTML together', () => d.querySelector('#process-ia .process-map').textContent.includes('Learn') && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && !previewDoc().querySelector('#sitemap a[href="#features"]') && !evaluate('htmlExport()').includes('Articles') && evaluate('projectJson()').includes('Articles'));
  const customSitemap=d.getElementById('plan-pages').value, customSitemapExport=evaluate('projectJson()');
  d.getElementById('dockModeAdvanced').click(); await wait();
  test('Custom IA survives mode changes while unlinked sitemap entries remain hidden', () => d.getElementById('plan-pages').value===customSitemap && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && d.querySelector('#process-ia .process-map').textContent.includes('Articles'));
  evaluate('importConfig('+customSitemapExport+')'); await wait();
  test('Custom sitemap survives JSON round trip while Basic omits unlinked entries', () => d.getElementById('plan-pages').value===customSitemap && !previewDoc().querySelector('#sitemap').textContent.includes('Articles') && previewDoc().querySelectorAll('#sitemap a').length===1);
  input('plan-pages','<img src=x onerror=alert(1)> > <script>bad<\/script>'); await wait();
  test('Sitemap labels cannot inject HTML or arbitrary destinations', () => {
    const page=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    return !page.querySelector('#sitemap img, #sitemap script, #sitemap a') && !page.querySelector('#sitemap').textContent.includes('onerror=alert(1)') && page.querySelector('#sitemap').textContent.includes('No sitemap destinations selected') && d.getElementById('plan-pages').validationMessage.includes('three information levels') && !d.querySelector('#process-ia .process-map img, #process-ia .process-map script');
  });
  input('plan-pages',''); await wait();
  test('Empty Architecture has an honest empty sitemap and keeps real footer navigation', () => previewDoc().querySelector('#sitemap').textContent.includes('No sitemap destinations selected') && previewDoc().querySelector('footer .footer-brand[href="#home"]'));
  d.getElementById('plan-use-sample').click(); await wait();
  test('Use complete sitemap restores the full Basic mock-site plan and expanded footer links', () => d.getElementById('plan-pages').value===w.DSStudio.process.samplePages('basic') && previewDoc().querySelectorAll('#sitemap a').length===14 && d.querySelectorAll('#process-ia .process-map li').length===w.DSStudio.process.samplePages('basic').split('\n').length);
  for (const mode of ['advanced','basic']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
    input('plan-pages','Home\nCustom > Future page'); await wait();
    d.getElementById('process-ia').open=false;
    d.getElementById('plan-use-sample').click(); await wait();
    test(mode+' sitemap button restores stored/editor/centre/preview/inspector content and gives visible feedback', () => {
      const expected=w.DSStudio.process.samplePages(mode), parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
      return evaluate('state.designProcess.pages')===expected && d.getElementById('plan-pages').value===expected && d.getElementById('process-ia').open && !d.querySelector('#process-ia .process-map').textContent.includes('Future page') && !previewDoc().querySelector('#sitemap .sitemap-planned') && previewDoc().querySelector('#sitemap').innerHTML===parsed.querySelector('#sitemap').innerHTML && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()') && d.getElementById('plan-sample-status').textContent.includes('destination outline applied:');
    });
    const restored=evaluate('projectJson()');
    d.getElementById('plan-use-sample').click(); await wait();
    test(mode+' repeated sitemap clicks confirm an already complete map without changing data', () => evaluate('projectJson()')===restored && d.getElementById('plan-sample-status').textContent.includes('already complete'));
    input('plan-pages','Home\nMy next page'); await wait();
    test(mode+' editing a restored sitemap clears outdated confirmation', () => d.getElementById('plan-sample-status').textContent==='');
    d.getElementById('plan-use-sample').click(); await wait();
  }
  const listsPage=d.createElement('iframe'); listsPage.style.cssText='width:1440px;height:1000px;border:0';
  listsPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
  await new Promise(resolve=>{listsPage.onload=resolve;d.body.append(listsPage);});
  for (const width of [320,390,1440]) {
    listsPage.style.width=width+'px'; await wait();
    test('Basic list cards and sitemap fit at '+width+'px', () => {
      const pd=listsPage.contentDocument, cards=[...pd.querySelectorAll('#lists .list-grid > article')], boxes=cards.map(card=>card.getBoundingClientRect());
      return pd.documentElement.scrollWidth<=width+1 && boxes.every(box=>box.left>=0 && box.right<=width+1) && (width===1440?(Math.abs(boxes[1].top-boxes[0].top)<1 && boxes[1].left>=boxes[0].right && Math.abs(boxes[2].top-boxes[0].top)<1 && boxes[2].left>=boxes[1].right):(boxes[1].top>=boxes[0].bottom && boxes[2].top>=boxes[1].bottom));
    });
  }
  listsPage.remove();
  for (const mode of ['basic','advanced']) {
    evaluate('importConfig('+JSON.stringify({sampleMode:mode,designProcess:{pages:'Home\nLessons > Layout\nLessons > Typography\nLessons > Colour\nResources\nContact'}})+')'); await wait();
    test(mode+' old starter upgrades to the complete map without planned placeholders', () => d.getElementById('plan-pages').value===w.DSStudio.process.samplePages(mode) && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  }
  reset(); await wait();
  const systemPage=d.createElement('iframe'); systemPage.style.cssText='width:1440px;height:1000px;border:0';
  for (const edited of [false,true]) {
    if (edited) {
      for (const [id,value,type] of [['jSpacing',6],['jBase',20],['jRatio',1.25],['advMeasure',52],['advBorder',2],['advHeight',56],['advShadow','strong','change'],['advOpacity',72],['advAlign','center','change'],['advFocus',5],['bdPaddingX',28],['bdPaddingY',14],['bdRadius',18],['bdMinHeight',60],['bdWeight',600],['bdSize','lg'],['bdVariant','primary'],['bdDefaultBg','#602d54'],['bdText','#ffffff']]) input(id,value,type||'input');
      const editedProject=evaluate('projectJson()'); reset(); evaluate('importConfig('+editedProject+')'); await wait();
    }
    for (const theme of ['light','dark']) {
      input('jTheme',theme); await wait();
      const signatures=[];
      for (const mode of ['advanced','basic']) {
        d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click(); await wait();
        const css=evaluate('cssExport()');
        systemPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+css+'</style>');
        await new Promise(resolve=>{systemPage.onload=resolve;if(!systemPage.isConnected)d.body.append(systemPage);});
        const pd=systemPage.contentDocument,pw=systemPage.contentWindow;
        const style=selector=>pw.getComputedStyle(pd.querySelector(selector));
        const signature={body:style('body').font,h1:style('h1').font,h2:style('main h2').font,h3:style('main h3').font,padding:style('.card').padding,border:style('.card').border,shadow:style('.card').boxShadow,opacity:style('.card').opacity,measure:style('.card p:last-of-type').maxWidth,input:style('.input').minHeight,inputPadding:style('.input').padding,button:style('#home .ds-button').padding,buttonHeight:style('#home .ds-button').minHeight,buttonRadius:style('#home .ds-button').borderRadius,buttonWeight:style('#home .ds-button').fontWeight,buttonBackground:style('#home .ds-button').backgroundColor,buttonText:style('#home .ds-button').color,align:style(mode==='basic'?'.skill-cards':'.card-grid').alignItems,footerPadding:style('.footer-inner').padding,footerLinkWeight:style(mode==='basic'?'.sitemap-list > li > a':'.footer-links a').fontWeight,navFont:style('header nav a').font,navDecoration:style('header nav a').textDecorationLine,background:style('body').backgroundColor};
        signatures.push(signature);
        test(mode+' '+theme+' '+(edited?'edited/imported':'default')+' follows system dimensions in standalone CSS',()=> css.startsWith(w.DSStudio.samples.foundationCss()) && signature.padding===(edited?'36px':'24px') && signature.input===(edited?'56px':'48px') && signature.opacity===(edited?'0.72':'1') && signature.align===(edited?'center':'stretch') && Math.abs(parseFloat(style('h1').fontSize)-evaluate('fluidTypePx(5,1440)'))<.2 && (!edited || (Math.abs(parseFloat(signature.button)-17.08)<.02 && signature.buttonRadius==='18px' && signature.buttonBackground==='rgb(96, 45, 84)' && signature.buttonText==='rgb(255, 255, 255)' && signature.shadow!=='none')));
        if (mode==='basic') test(theme+' Basic sign-up width follows the '+(edited?'edited/imported':'default')+' reading measure',()=>style('.signup-form').maxWidth!=='none' && style('.signup-form').maxWidth===signature.measure);
        const previewStyle=previewWindow().getComputedStyle(previewDoc().querySelector('.card'));
        test(mode+' preview and inspector use the same edited system as downloads',()=>previewStyle.padding===signature.padding && previewStyle.opacity===signature.opacity && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()'));
        const map=pd.getElementById('sitemap');
        const footerDisclosure=pd.getElementById('footer-sitemap'),footerSummary=pd.getElementById('sitemap-toggle');
        test(mode+' '+theme+' sitemap starts collapsed in standalone export',()=>!footerDisclosure.open && footerSummary.tagName==='SUMMARY' && pw.getComputedStyle(footerSummary).display==='list-item' && footerSummary.getBoundingClientRect().height>=44 && map.getBoundingClientRect().height===0);
        footerSummary.click();

        test(mode+' footer presents its sitemap and working return destination',()=> map.tagName==='NAV' && map.closest('details').open && pw.getComputedStyle(pd.getElementById('sitemap-title')).textAlign==='left' && pd.querySelector('.footer-bottom a[href="#top"]') && pd.getElementById('top'));
        test(mode+' footer sitemap works without JavaScript and keeps all destinations valid',()=> map.tagName==='NAV' && [...map.querySelectorAll('a')].every(a=>a.getBoundingClientRect().height>=44 && pd.getElementById(a.hash.slice(1))));
        footerSummary.focus();
        test(mode+' '+theme+' sitemap summary retains the shared visible focus ring',()=>pd.activeElement===footerSummary && pw.getComputedStyle(footerSummary).outlineStyle==='solid' && pw.getComputedStyle(footerSummary).outlineWidth===style(':root').getPropertyValue('--button-focus-width').trim());
        footerSummary.click();
        test(mode+' '+theme+' sitemap heading collapses its content while remaining available',()=>!footerDisclosure.open && map.getBoundingClientRect().height===0 && footerSummary.getBoundingClientRect().height>=44);
        footerSummary.click();

        for (const width of [320,390,1440]) {
          systemPage.style.width=width+'px'; await wait();
          const menu=pd.querySelector('.basic-menu, .sample-menu'); if(menu)menu.open=width<=768;
          const navLink=pd.querySelector(mode==='basic'?(width<=768?'.mobile-navigation a':'.desktop-navigation a'):width<=768?'.sample-mobile-navigation a':'.sample-desktop-navigation a');
          test(mode+' '+theme+' navigation matches Advanced text at '+width+'px '+(edited?'edited':'default'),()=>{
            const ns=pw.getComputedStyle(navLink), live=previewWindow().getComputedStyle(previewDoc().querySelector('header nav a'));
            return ns.fontWeight==='600' && ns.fontFamily===style('body').fontFamily && ns.fontSize===style('body').fontSize && ns.textDecorationLine==='none' && live.fontWeight==='600' && live.textDecorationLine==='none' && navLink.getBoundingClientRect().height>0;
          });
          navLink.focus();
          test(mode+' navigation retains the Advanced focus ring at '+width+'px',()=>pd.activeElement===navLink && pw.getComputedStyle(navLink).outlineStyle==='solid' && pw.getComputedStyle(navLink).outlineWidth===style(':root').getPropertyValue('--button-focus-width').trim());
          test(mode+' '+theme+' footer fits '+width+'px '+(edited?'edited':'default'),()=>pd.documentElement.scrollWidth<=width+1 && [...pd.querySelectorAll('.website-footer a')].every(el=>{const box=el.getBoundingClientRect();return box.left>=0 && box.right<=width+1 && box.height>=44;}) && [...map.querySelectorAll('.sitemap-list > li')].every(group=>pw.getComputedStyle(group).textAlign==='center') && [...map.querySelectorAll('.sitemap-list ul')].every(list=>{const bounds=list.getBoundingClientRect();return pw.getComputedStyle(list).flexDirection==='column' && [...list.querySelectorAll('a')].every(link=>{const box=link.getBoundingClientRect();return Math.abs((box.left+box.right)/2-(bounds.left+bounds.right)/2)<1;});}));
        }
        systemPage.style.width='1440px'; await wait();
      }
      test(theme+' '+(edited?'edited/imported':'default')+' Basic and Advanced share typography, spacing, components and footer styles',()=>JSON.stringify(signatures[0])===JSON.stringify(signatures[1]));
    }
  }
  systemPage.remove(); reset(); await wait();
  d.getElementById('dockModeBasic').click(); await wait();
  w.dssShowWizardStep(1);
  const saveSitemap = async (label,parent='',target='planned') => {
    d.getElementById('sitemap-new').click();
    d.getElementById('sitemap-label').value=label;
    d.getElementById('sitemap-parent').value=parent;
    d.getElementById('sitemap-target').value=target;
    d.getElementById('sitemap-form').requestSubmit(); await wait();
  };
  // Ordinary edits must retain visibility in project data, UI and generated output.
  for (const mode of ['basic','advanced']) for (const visible of [false,true]) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    const destination=w.DSStudio.process.inventory(mode).find(([,id])=>!['home','footer','top'].includes(id))[1];
    evaluate('state.designProcess=DSStudio.process.normalize('+JSON.stringify({
      pages:'Overview\nOverview > Linked entry\nOverview > Second entry\nFuture page',
      pageLinks:{[mode]:{'Overview':destination,'Linked entry':destination,'Second entry':destination,'Future page':''}},
      showPlanned:visible
    })+');apply()');await wait();
    w.dssShowWizardStep(1);
    const initial=evaluate('JSON.stringify(state.designProcess)');
    const visibilityMatches=()=>evaluate('state.designProcess.showPlanned')===visible &&
      d.getElementById('sitemap-planned').checked===visible &&
      JSON.parse(evaluate('projectJson()')).designProcess.showPlanned===visible &&
      Boolean(previewDoc().querySelector('#sitemap .sitemap-planned'))===visible &&
      Boolean(new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap .sitemap-planned'))===visible;
    const undoSitemap=async action=>{
      d.getElementById('sitemap-undo').click();await wait();
      test(mode+' '+visible+' Undo restores '+action+' and visibility',()=>evaluate('JSON.stringify(state.designProcess)')===initial && visibilityMatches() && d.getElementById('sitemap-undo').disabled);
    };
    input('sitemap-items','0:0','change');
    d.getElementById('sitemap-label').value='Renamed entry';d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' '+visible+' rename preserves visibility and destination',()=>visibilityMatches() && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Renamed entry' && a.hash==='#'+destination));
    await undoSitemap('rename');
    await saveSitemap('New planned page');
    test(mode+' '+visible+' creation preserves visibility',()=>visibilityMatches() && evaluate('state.designProcess.pages').includes('New planned page') && previewDoc().querySelector('#sitemap').textContent.includes('New planned page')===visible);
    await undoSitemap('creation');
    input('sitemap-items','0:0','change');d.getElementById('sitemap-delete').click();await wait();
    test(mode+' '+visible+' deletion preserves visibility',()=>visibilityMatches() && !evaluate('state.designProcess.pages').includes('Linked entry') && !previewDoc().querySelector('#sitemap').textContent.includes('Linked entry'));
    await undoSitemap('deletion');
    input('sitemap-items','0:0','change');d.getElementById('sitemap-down').click();await wait();
    test(mode+' '+visible+' reorder preserves visibility and changes order',()=>visibilityMatches() && w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[0][1][1]==='Linked entry');
    await undoSitemap('reorder');
    d.getElementById('sitemap-planned').click();await wait();
    test(mode+' '+visible+' checkbox explicitly changes visibility',()=>evaluate('state.designProcess.showPlanned')===!visible && d.getElementById('sitemap-planned').checked===!visible);
    await undoSitemap('visibility toggle');
  }
  reset();d.getElementById('dockModeBasic').click();await wait();w.dssShowWizardStep(1);
  d.getElementById('sitemap-planned').click();await wait();
  await saveSitemap('Our team');
  test('Sitemap CRUD creates a planned group visible in Basic preview and export',()=>previewDoc().querySelector('#sitemap').textContent.includes('Our team') && previewDoc().querySelector('#sitemap .sitemap-planned') && evaluate('htmlExport()').includes('Our team') && d.querySelector('#process-ia').textContent.includes('Our team'));
  const teamIndex=w.DSStudio.process.hierarchy(evaluate('DSStudio.process.currentPlan().pages')).findIndex(([name])=>name==='Our team');
  await saveSitemap('Meet the mentor',String(teamIndex),'basic-layout');
  test('Sitemap CRUD creates a relationship with a safe existing destination',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(group=>group.textContent.includes('Our team') && group.querySelector('ul a[href="#basic-layout"]')?.textContent==='Meet the mentor'));
  d.getElementById('sitemap-label').value='Meet Alex';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Sitemap CRUD renames labels while preserving destinations and inspector output',()=>previewDoc().querySelector('#sitemap a[href="#basic-layout"]').textContent!=='Meet the mentor' && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Meet Alex'&&a.hash==='#basic-layout') && !evaluate('htmlExport()').includes('Meet the mentor') && d.getElementById('dockCss').textContent===evaluate(d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true'?'htmlExport()':'cssExport()'));
  d.getElementById('sitemap-parent').value='1';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Sitemap CRUD reparents a child under Components',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(group=>group.querySelector(':scope > a')?.textContent==='Components' && [...group.querySelectorAll('ul a')].some(a=>a.textContent==='Meet Alex')));
  d.getElementById('sitemap-up').click();await wait();
  test('Sitemap CRUD reorders children in the rendered footer',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[1][1].at(-2)==='Meet Alex');
  const beforeDelete=evaluate('JSON.stringify(state.designProcess)');
  d.getElementById('sitemap-delete').click();await wait();
  test('Sitemap CRUD deletes an entry',()=>!evaluate('htmlExport()').includes('Meet Alex'));
  d.getElementById('sitemap-undo').click();await wait();
  test('Sitemap CRUD undo restores relationships and destination mapping',()=>evaluate('JSON.stringify(state.designProcess)')===beforeDelete && evaluate('htmlExport()').includes('Meet Alex'));
  const customBuilder=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(customBuilder)+')');await wait();
  test('Sitemap relationships and destination mapping survive JSON round trip',()=>evaluate('htmlExport()').includes('Meet Alex') && previewDoc().querySelector('#sitemap .sitemap-planned') && d.getElementById('sitemap-undo').disabled);
  await saveSitemap('<img src=x onerror=alert(1)>');
  test('Sitemap CRUD rejects relationship delimiters without injecting markup',()=>!previewDoc().querySelector('#sitemap img') && d.getElementById('sitemap-status').textContent.includes('unique label'));
  const maliciousLinks={pageLinks:{basic:{Bad:'javascript:alert(1)',Safe:'basic-layout',Planned:''},advanced:{Bad:'basic-layout'}},showPlanned:true};
  test('Imported sitemap targets accept only fixed IDs for the corresponding mode',()=>{
    const normalized=w.DSStudio.process.normalize(maliciousLinks);return !Object.hasOwn(normalized.pageLinks.basic,'Bad') && normalized.pageLinks.basic.Safe==='basic-layout' && normalized.pageLinks.basic.Planned==='' && !Object.hasOwn(normalized.pageLinks.advanced,'Bad');
  });
  d.getElementById('plan-use-sample').click();await wait();
  test('Complete sitemap restores default labels, link mappings and visibility',()=>!evaluate('state.designProcess.showPlanned') && Object.keys(evaluate('state.designProcess.pageLinks.basic')).length===0 && !previewDoc().querySelector('#sitemap .sitemap-planned'));
  input('sitemap-items','1:1','change');
  d.getElementById('sitemap-label').value='Mentor profile';d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Renaming a child retains its sibling order and existing destination',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages'))[1][1][1]==='Mentor profile' && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Mentor profile'&&a.hash==='#basic-layout'));
  input('plan-pages','Home\nComponents');await wait();
  test('External text edits invalidate sitemap undo instead of restoring stale data',()=>d.getElementById('sitemap-undo').disabled);
  input('plan-pages',Array.from({length:64},(_,i)=>'Planned '+i).join('\n'));await wait();
  await saveSitemap('Too many');await saveSitemap('Still too many');
  test('Sitemap CRUD enforces entry limits and remains usable after repeated rejections',()=>w.DSStudio.process.hierarchy(evaluate('state.designProcess.pages')).length===64 && d.getElementById('sitemap-status').textContent.includes('64 entries'));
  d.getElementById('plan-use-sample').click();await wait();
  d.getElementById('sitemap-planned').click();await wait();
  await saveSitemap('Research <notes');
  test('Sitemap labels render as escaped text without creating page sections',()=>previewDoc().querySelector('#sitemap').textContent.includes('Research <notes') && !previewDoc().querySelector('#sitemap notes') && previewDoc().querySelectorAll('main > section').length===4);
  for (const width of [320,1440]) {
    app.style.width=width+'px';await wait();
    test('Sitemap editor fits the wizard at '+width+'px',()=>[...d.querySelectorAll('#sitemap-editor select, #sitemap-editor input:not([type="checkbox"]), #sitemap-editor button')].every(el=>{const box=el.getBoundingClientRect(),parent=d.getElementById('sitemap-editor').getBoundingClientRect();return box.width>0 && box.left>=parent.left-1 && box.right<=parent.right+1;}));
  }
  d.getElementById('plan-use-sample').click();await wait();
  w.dssShowWizardStep(4);
  const defaultCanvas=evaluate('palette().roles.background');
  input('page-background-hex','#E1E9F0');await wait();
  test('Page background control updates tokens, inspector and Basic preview',()=>evaluate('palette().roles.background')==='#E1E9F0' && previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(225, 233, 240)' && evaluate('cssExport()').includes('--background: #E1E9F0') && d.getElementById('page-background-colour').value==='#e1e9f0');
  for (const [theme,colour,rgb] of [['light','#E1E9F0','rgb(225, 233, 240)'],['dark','#172635','rgb(23, 38, 53)']]) {
    evaluate(`state.theme='${theme}';apply()`);input('page-background-hex',colour);await wait();
    const checkCanvas=(pd,pw)=>pw.getComputedStyle(pd.body).backgroundColor===rgb && [...pd.querySelectorAll('main > section')].length===4 && [...pd.querySelectorAll('main > section')].every(section=>pw.getComputedStyle(section).backgroundColor==='rgba(0, 0, 0, 0)');
    test(theme+' Basic selected background is visible behind every main section',()=>checkCanvas(previewDoc(),previewWindow()));
    const canvasPage=d.createElement('iframe');
    canvasPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');
    d.body.append(canvasPage);await wait();
    test(theme+' Basic exported background is visible behind every main section',()=>checkCanvas(canvasPage.contentDocument,canvasPage.contentWindow));
    canvasPage.remove();
  }
  evaluate("state.theme='light';apply()");await wait();
  input('page-background-hex','bad');await wait();
  test('Page background rejects invalid input without changing state',()=>evaluate('palette().roles.background')==='#E1E9F0');
  const backgroundProject=JSON.parse(evaluate('projectJson()'));reset();evaluate('importConfig('+JSON.stringify(backgroundProject)+')');await wait();
  test('Page background survives project round trip',()=>evaluate('palette().roles.background')==='#E1E9F0');
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Page background applies to Advanced as well as Basic',()=>previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(225, 233, 240)');
  evaluate("state.theme='dark';apply()");await wait();
  input('page-background-colour','#172635');await wait();
  test('Page background is independently editable per theme',()=>evaluate('state.semanticOverrides.dark.background')==='#172635' && evaluate('state.semanticOverrides.light.background')==='#E1E9F0' && previewWindow().getComputedStyle(previewDoc().body).backgroundColor==='rgb(23, 38, 53)');
  d.getElementById('page-background-reset').click();await wait();
  test('Page background reset restores only the current theme',()=>!evaluate('state.semanticOverrides.dark.background') && evaluate('state.semanticOverrides.light.background')==='#E1E9F0');
  evaluate("state.theme='light';apply()");d.getElementById('page-background-reset').click();await wait();
  test('Page background reset restores the default canvas',()=>evaluate('palette().roles.background')===defaultCanvas);
  reset();await wait();
  w.dssShowWizardStep(4);
  const regions=['header','main','footer'];
  test('Background controls follow Brand and Main Palettes, in page order',()=>{
    const pane=d.querySelector('[data-journey-pane="4"]'),editor=d.querySelector('.page-background-editor');
    return Boolean(d.getElementById('jRamp').compareDocumentPosition(editor)&w.Node.DOCUMENT_POSITION_FOLLOWING) &&
      [...editor.querySelectorAll('legend')].map(el=>el.textContent).join('|')==='Body background|Header background|Main background|Footer background' &&
      pane.contains(editor) && d.querySelector('#brandPalette .studio-lesson #webpage-background-lesson');
  });
  test('Body is a visible first-class control and contains the centre page regions',()=>!d.getElementById('body-background-controls').closest('details') && d.getElementById('page-background-colour').getBoundingClientRect().height>=44 && ['header','main','footer'].every(region=>d.getElementById('body-background-value').closest('section').querySelector('.background-contained-regions').contains(d.getElementById(region+'-background-value'))));
  test('Every background selector offers the complete Brand Palette in its saved order',()=>regions.concat('page').every(region=>{
    const values=[...d.getElementById(region+'-background-brand').children].filter(el=>el.tagName==='OPTION').slice(1);
    return values.length===evaluate('state.brandPalette.length') && values.every((option,i)=>option.value===evaluate('state.brandPalette')[i].hex && option.textContent.includes(evaluate('state.brandPalette')[i].name));
  }));
  const regionColours={light:['#004780','#5FC5BF','#F37327'],dark:['#EF426F','#495965','#57B7E7']};
  const bodyColours={light:'#00BADC',dark:'#2B71B9'};
  for (const theme of ['light','dark']) {
    input('jTheme',theme);await wait();
    input('page-background-brand',bodyColours[theme],'change');await wait();
    test(theme+' Body brand choice updates the existing background role and centre model',()=>evaluate('palette().roles.background')===bodyColours[theme] && d.getElementById('body-background-value').textContent==='--background: '+bodyColours[theme]+';' && d.getElementById('body-background-contrast').textContent.includes('Text '));
    for (const [index,region] of regions.entries()) {
      input(region+'-background-brand',regionColours[theme][index],'change');await wait();
      test(theme+' '+region+' background selects a brand value independently',()=>evaluate('palette().roles')[region+'-background']===regionColours[theme][index] && d.getElementById(region+'-background-hex').value===regionColours[theme][index] && d.getElementById(region+'-background-value').textContent.includes(regionColours[theme][index]));
    }
    for (const mode of ['basic','advanced']) {
      d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
      const checkRegions=(pd,pw)=>pw.getComputedStyle(pd.body).backgroundColor==='rgb('+evaluate('hexRgb('+JSON.stringify(bodyColours[theme])+')').join(', ')+')' && regions.every((region,i)=>{
        const rgb=evaluate('hexRgb('+JSON.stringify(regionColours[theme][i])+')');
        return pw.getComputedStyle(pd.querySelector('body > '+region)).backgroundColor==='rgb('+rgb.join(', ')+')';
      });
      test(theme+' '+mode+' preview paints Body and all three regions and preserves card surfaces',()=>checkRegions(previewDoc(),previewWindow()) && previewWindow().getComputedStyle(previewDoc().querySelector('.card')).backgroundColor!==previewWindow().getComputedStyle(previewDoc().querySelector('main')).backgroundColor);
      const exportPage=d.createElement('iframe');exportPage.srcdoc=evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>');d.body.append(exportPage);await wait();
      test(theme+' '+mode+' standalone HTML and CSS paint the same backgrounds',()=>checkRegions(exportPage.contentDocument,exportPage.contentWindow));exportPage.remove();
      for (const region of ['body',...regions]) for (const language of ['css','html']) {
        const row=d.getElementById(region+'-background-value').closest('section');row.querySelector('[data-background-inspect="'+language+'"]').click();await wait();
        test(theme+' '+mode+' '+region+' Inspect '+language+' shows the complete current output',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate(language==='css'?'cssExport()':'htmlExport()') && d.getElementById(language==='css'?'dockTabCss':'dockTabHtml').getAttribute('aria-selected')==='true');
      }
    }
  }
  const regionProject=JSON.parse(evaluate('projectJson()'));input('jProject','Region background test');d.getElementById('jSaveLocal').click();await wait();
  input('header-background-colour','#123456');await wait();
  test('A custom region picker updates the current inspector output',()=>evaluate("palette().roles['header-background']")==='#123456' && d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  d.getElementById('jLoadLocal').click();await wait();
  test('Saved projects restore autosaved per-theme region and Body backgrounds',()=>evaluate('state.semanticOverrides.dark["header-background"]')==='#123456' && evaluate('state.semanticOverrides.light["header-background"]')===regionColours.light[0] && evaluate('state.semanticOverrides.dark.background')===bodyColours.dark && evaluate('state.semanticOverrides.light.background')===bodyColours.light);
  reset();evaluate('importConfig('+JSON.stringify(regionProject)+')');await wait();
  test('Region and Body backgrounds survive project JSON round trip',()=>regions.every((region,i)=>evaluate('state.semanticOverrides.dark')[region+'-background']===regionColours.dark[i] && evaluate('state.semanticOverrides.light')[region+'-background']===regionColours.light[i]) && evaluate('state.semanticOverrides.dark.background')===bodyColours.dark && evaluate('state.semanticOverrides.light.background')===bodyColours.light);
  w.dssConfigureToken({name:'--background',scope:'Light'});await wait();
  test('Body token source routes to the correct theme and visible Body control',()=>evaluate('state.theme')==='light' && w.DSStudio.activeStage===4 && d.activeElement===d.getElementById('page-background-colour'));
  input('jTheme','dark');await wait();
  input('main-background-hex','#123ABC');await wait();
  input('main-background-hex','red;/*');await wait();
  test('Invalid region hex cannot change state or generated output',()=>evaluate('state.semanticOverrides.dark["main-background"]')==='#123ABC' && !evaluate('cssExport()').includes('red;/*') && d.getElementById('main-background-hex').getAttribute('aria-invalid')==='true');
  for (const region of regions) {d.getElementById(region+'-background-reset').click();await wait();}
  test('Region reset restores current-theme defaults and retains other-theme choices',()=>regions.every((region,i)=>!evaluate('state.semanticOverrides.dark')[region+'-background'] && evaluate('state.semanticOverrides.light')[region+'-background']===regionColours.light[i]) && evaluate("palette().roles['main-background']===palette().roles.background && palette().roles['header-background']===palette().roles.surface && palette().roles['footer-background']===palette().roles.surface"));
  input('page-background-hex','#234567');await wait();
  test('Default Main background follows subsequent canvas changes',()=>evaluate("palette().roles['main-background']==='#234567'"));
  d.getElementById('page-background-reset').click();await wait();
  test('Body reset restores only its theme and updates default Main',()=>!evaluate('state.semanticOverrides.dark.background') && evaluate('state.semanticOverrides.light.background')===bodyColours.light && evaluate('palette().roles.background===palette().roles["main-background"]'));
  input('header-background-brand','#FFFFFF','change');await wait();
  evaluate("state.brandPalette=state.brandPalette.map(item=>item.hex==='#FFFFFF'?{...item,name:'<img onerror=alert(1)>',hex:'#EEEEEE'}:item);apply()");await wait();
  test('Brand edits refresh all choices safely while existing assignments retain copied hex',()=>evaluate("palette().roles['header-background']")==='#FFFFFF' && regions.every(region=>[...d.getElementById(region+'-background-brand').options].some(option=>option.value==='#EEEEEE'&&option.textContent.includes('<img onerror=alert(1)>'))) && !d.querySelector('#webpage-region-controls img'));
  evaluate('importConfig({semanticOverrides:{light:{"header-background":"url(javascript:alert(1))","main-background":{},"footer-background":"#abc"},dark:{"header-background":"#abcdef"}}})');await wait();
  test('Imported region overrides validate hex types and lengths',()=>evaluate("!state.semanticOverrides.light['header-background'] && !state.semanticOverrides.light['main-background'] && !state.semanticOverrides.light['footer-background'] && state.semanticOverrides.dark['header-background']==='#ABCDEF'"));
  for (const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    test('Background controls and centre lesson fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['body-background-controls','webpage-region-controls','webpage-background-lesson'].every(id=>{const el=d.getElementById(id);return el.scrollWidth<=el.clientWidth+1;}) && ['page',...regions].every(region=>['brand','colour','hex'].every(kind=>{const el=d.getElementById(region+'-background-'+kind);el.focus();return d.activeElement===el && el.getBoundingClientRect().height>=44;})));
  }
  app.style.width='1440px';reset();await wait();
  test('Reset clears all region overrides and restores selectors',()=>!evaluate('state.semanticOverrides') && regions.every(region=>d.getElementById(region+'-background-reset').disabled));
  reset(); await wait();
  input('jProject','My learning project'); input('jBase',18);
  const beforeLearning=JSON.parse(evaluate('projectJson()'));
  const settleLearningColours=()=>{const style=previewDoc().createElement('style');style.textContent='.ds-button { transition: none !important; }';previewDoc().head.append(style);};
  d.getElementById('dockModeBasic').click();
  d.querySelector('[data-journey-step="7"]').click();
  w.DSStudio.inspector.show({section:'all',language:'css'}); await wait();
  const startedLearning=JSON.parse(evaluate('projectJson()'));
  delete beforeLearning.sampleMode; delete startedLearning.sampleMode;
  test('Unified Buttons step retains design values while showing its task and example',()=>Object.keys(beforeLearning).every(key=>JSON.stringify(beforeLearning[key])===JSON.stringify(startedLearning[key])) && d.getElementById('studyExample').value==='action' && d.querySelector('#buttonDesignLab .step-task').textContent.includes('primary button'));
  test('Teaching state stays outside generated files and project data',()=>!evaluate('htmlExport()').includes('step-task') && !evaluate('cssExport()').includes('journey-phase') && !evaluate('projectJson()').includes('activeStage'));
  d.getElementById('exampleConnections').open=true;
  test('Primary action exposes its exact exported rule and live token values',()=>evaluate('cssExport()').includes(d.getElementById('studyRule').textContent) && d.getElementById('studyRule').textContent.startsWith('.ds-button--primary {') && d.getElementById('studyTokens').textContent.includes('--button-primary-bg:'));
  input('bdDefaultBg','#602d54'); await wait(); settleLearningColours();
  test('A beginner colour change updates the example, connected token and inspector together',()=>previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(96, 45, 84)' && d.getElementById('studyTokens').textContent.toLowerCase().includes('#602d54') && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  d.querySelector('[data-journey-step="8"]').click();
  test('Spacing exercise opens the existing source control',()=>!d.querySelector('[data-journey-pane="8"]').hidden && !d.querySelector('[data-journey-pane="8"]').hidden);
  const beforeLearningPadding=parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('#lists')).paddingTop);
  input('jSpacing',6); await wait();
  test('Spacing connection shows derived values from the current generator',()=>d.getElementById('studyTokens').textContent.includes('--space-unit: 6px') && d.getElementById('studyTokens').textContent.includes('--space-8: calc(var(--space-unit) * 8)') && Math.abs(parseFloat(previewWindow().getComputedStyle(previewDoc().querySelector('#lists')).paddingTop)-beforeLearningPadding*1.5)<.1 && d.getElementById('studyRule').textContent.includes('var(--space-8)') && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  for (const theme of ['light','dark']) {
    input('jTheme',theme); input('studyExample','header','change'); await wait();
    const primary=w.dssReadTokens().filter(row=>row.name==='--primary').find(row=>theme==='dark'?row.scope==='Dark':row.scope!=='Dark');
    test(theme+' connected token reads the correct exported theme scope',()=>d.getElementById('studyTokens').textContent.includes('--primary: '+primary.value));
  }
  for (const option of [...d.getElementById('studyExample').options]) {
    input('studyExample',option.value,'change');
    test('Example '+option.value+' maps to a real generated CSS rule',()=>evaluate('cssExport()').includes(d.getElementById('studyRule').textContent) && !d.getElementById('studyRule').textContent.includes('Inspect its section') && (option.value!=='faq' || d.getElementById('studyTokens').textContent.includes('--heading-weight')) && (option.value!=='footer' || d.getElementById('studyTokens').textContent.includes('--space-8')));
  }
  input('studyExample','profile','change'); d.getElementById('studyPreview').click(); await wait();
  test('Show example focuses its actual preview element',()=>previewDoc().activeElement===previewDoc().getElementById('basic-layout'));
  const beforePicking=evaluate('projectJson()'), pickingDoc=previewDoc();
  d.getElementById('studyPick').click();
  previewDoc().querySelector('#basic-layout a').click(); await wait();
  test('Opt-in selection connects the clicked example without following its link or changing project data',()=>previewDoc()===pickingDoc && d.getElementById('studyExample').value==='profile' && !w.DSStudio.learning.picking && d.activeElement===d.getElementById('studyExample') && evaluate('projectJson()')===beforePicking);
  previewDoc().querySelector('#basic-layout a').click(); await wait();
  test('Normal preview navigation resumes after selecting an example',()=>previewDoc().activeElement===previewDoc().getElementById('list-workflow'));
  d.getElementById('studyPick').click(); previewDoc().dispatchEvent(new w.KeyboardEvent('keydown',{key:'Escape',bubbles:true}));
  test('Escape inside the preview cancels example selection',()=>!w.DSStudio.learning.picking && d.getElementById('studyPick').getAttribute('aria-pressed')==='false');
  d.getElementById('studyPick').click(); previewDoc().querySelector('#home h1').click(); await wait();
  test('Selecting a hero heading connects its layout rather than an unrelated action',()=>d.getElementById('studyExample').value==='hero');
  d.getElementById('studyPick').click(); previewDoc().querySelector('#home .ds-button--primary').click(); await wait();
  test('Selecting a primary action connects its component rule',()=>d.getElementById('studyExample').value==='action' && !w.DSStudio.learning.picking);
  input('dockSection','footer','change');
  test('Existing study-section selection also updates example connections',()=>d.getElementById('studyExample').value==='footer' && d.getElementById('studyRule').textContent.includes('.website-footer .footer-inner'));
  d.getElementById('dockTabHtml').click(); d.getElementById('dockToggle').click();
  w.DSStudio.inspector.show();
  test('Code shortcut retains the selected language and excerpt and expands the inspector',()=>d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='footer' && !d.querySelector('.studio-code-dock').classList.contains('is-collapsed') && d.activeElement===d.getElementById('dockCss') && d.getElementById('dockCss').textContent===w.DSStudio.samples.basicExcerpt(evaluate('htmlExport()'),'html','footer'));
  d.getElementById('studyCode').click();
  test('Find rule selects complete CSS so shared dependencies remain visible',()=>d.getElementById('dockSection').value==='all' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').scrollTop>0 && d.activeElement===d.getElementById('dockCss'));
  d.querySelector('[data-journey-step="9"]').click(); const beforeLearningResponsive=evaluate('JSON.stringify(state.responsiveDesign)');
  d.querySelector('button[data-width="mobile"]').click();d.getElementById('studyPreview').click(); await wait();
  test('Responsive task tests 390px without changing saved breakpoints',()=>Math.abs(previewWindow().innerWidth-390)<1 && evaluate('JSON.stringify(state.responsiveDesign)')===beforeLearningResponsive && previewDoc().activeElement===previewDoc().getElementById('home'));
  const learningFiles=[], beforeLearningDownload=w.download;w.download=(name,content,type)=>learningFiles.push({name,content,type});
  d.querySelector('[data-journey-step="11"]').click();
  test('Export exercise focuses Deliver without downloading automatically',()=>!d.querySelector('[data-journey-pane="11"]').hidden && learningFiles.length===0);
  d.getElementById('jExportHtml').click();d.getElementById('jExportCss').click();
  test('Beginner project exports the complete matching HTML and CSS',()=>learningFiles[0].name==='index.html' && learningFiles[0].content===evaluate('htmlExport()') && learningFiles[1].name==='tokens.css' && learningFiles[1].content===evaluate('cssExport()'));
  w.download=beforeLearningDownload;
  const learningExport=evaluate('projectJson()'); reset();evaluate('importConfig('+learningExport+')'); await wait(); settleLearningColours();
  test('Beginner design survives a project JSON round trip independently of session progress',()=>Object.keys(JSON.parse(learningExport)).every(key=>JSON.stringify(JSON.parse(learningExport)[key])===JSON.stringify(JSON.parse(evaluate('projectJson()'))[key])) && previewWindow().getComputedStyle(previewDoc().querySelector('#home .ds-button--primary')).backgroundColor==='rgb(96, 45, 84)');
  for (const width of [320,390,1280,1440]) {
    app.style.width=width+'px'; await wait();
    w.DSStudio.inspector.show();
    test('Workspace shortcuts and focused code remain usable at '+width+'px',()=>d.documentElement.scrollWidth<=width+1 && [...d.querySelectorAll('.step-output button')].filter(button=>button.getBoundingClientRect().width>0).every(button=>button.getBoundingClientRect().height>=44) && d.activeElement===d.getElementById('dockCss') && d.getElementById('dockCss').getBoundingClientRect().bottom>0 && d.getElementById('dockCss').getBoundingClientRect().top<app.contentWindow.innerHeight);
  }
  app.style.width='1440px';d.querySelector('button[data-width="fluid"]').click();d.getElementById('exampleConnections').open=false;reset();await wait();
  // Regression coverage for the shared journey and confirmed action/scope defects.
  app.style.width='1440px';reset();await wait();
  const wizardProject=evaluate('projectJson()');
  const wizardPreviewDocument=previewDoc();
  for (const stage of w.DSStudio.stages) {
    d.querySelector(`[data-journey-step="${stage.index}"]`).click();
    test('Shared stage '+stage.id+' selects one lesson, controls and focused heading',()=>{
      const active=d.getElementById(stage.lesson);
      return !d.querySelector(`[data-journey-pane="${stage.index}"]`).hidden && !active.hidden && active.open && d.querySelector('#main > :first-child').id==='studio-section-4' && d.activeElement===active.querySelector(':scope > summary h2') && [...d.querySelectorAll('#main > .studio-section')].filter(section=>section.open).length===(d.getElementById('studio-section-4').open?2:1) && evaluate('projectJson()')===wizardProject;
    });
    if(stage.index<4) {
      d.querySelector('#'+stage.lesson+' [data-inspect="json"]').click();
      test(stage.id+' inspects actual planning data in the single inspector',()=>d.getElementById('dockTabJson').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('projectJson()'));
    } else {
      d.querySelector('#'+stage.lesson+' [data-inspect="css"]').click();
      test(stage.id+' inspects complete CSS and a real declaration',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && (!stage.find || evaluate('cssExport()').includes(stage.find)));
    }
  }
  await wait();
  test('Stage navigation preserves the live preview browsing context',()=>previewDoc()===wizardPreviewDocument && previewDoc().getElementById('dssPreviewStyles').textContent===evaluate('cssExport()'));
  d.getElementById('jBack').click();
  test('Previous changes lesson and controls together',()=>evaluate('DSStudio.activeStage')===10 && !d.getElementById('studio-section-5').hidden);
  d.getElementById('jNext').click();
  test('Next changes lesson and controls together',()=>evaluate('DSStudio.activeStage')===11 && !d.getElementById('studio-section-6').hidden);
  for (const width of [320,390,1440]) {
    app.style.width=width+'px';await wait();
    d.querySelector('[data-journey-step="7"]').click();
    const controls=d.querySelector('[data-journey-pane="7"]');
    test('Actual controls join the lesson on narrow screens at '+width+'px',()=>width<=900?controls.closest('.studio-section')?.id==='buttonDesignLab' && controls.previousElementSibling.classList.contains('studio-lesson'):controls.closest('.studio-journey')!==null);
    const row=w.dssReadTokens().find(token=>token.name==='--space-unit');
    w.dssConfigureToken(row);
    test('Token source route selects its lesson and exact control at '+width+'px',()=>evaluate('DSStudio.activeStage')===8 && !d.getElementById('studio-section-3').hidden && d.activeElement===d.getElementById('jSpacing'));
  }
  app.style.width='1440px';await wait();
  w.dssRevealSection('studio-section-8',false);
  d.querySelector('#studio-section-8 > .panel > button').click();
  test('Reference return restores the current step without changing settings',()=>!d.getElementById('studio-section-8').open && !d.getElementById('studio-section-3').hidden && evaluate('projectJson()')===wizardProject);
  const reviewBox=d.querySelector('.readiness-item');
  const acknowledge=()=>{reviewBox.checked=true;reviewBox.dispatchEvent(new w.Event('change',{bubbles:true}));};
  acknowledge();input('jSpacing',5);
  test('Editing the design invalidates readiness acknowledgements',()=>!reviewBox.checked && !d.getElementById('readinessStatus').textContent.startsWith('1 of'));
  acknowledge();reset();
  test('Reset clears readiness even if the same values are restored',()=>!reviewBox.checked);
  acknowledge();evaluate('importConfig(JSON.parse(projectJson()))');d.dispatchEvent(new w.Event('dss:imported'));
  test('Loading a project clears readiness acknowledgements',()=>!reviewBox.checked);
  evaluate("state.designProcess.pageLinks.advanced={'Advanced custom':'about'};state.designProcess.pageLinks.basic={'Basic custom':'features'};apply()");
  d.getElementById('dockModeBasic').click();d.getElementById('plan-use-sample').click();
  test('Restoring Basic sitemap preserves Advanced link mappings',()=>evaluate("state.designProcess.pageLinks.advanced['Advanced custom']") ==='about' && evaluate('Object.keys(state.designProcess.pageLinks.basic).length')===0);
  evaluate("state.designProcess.pageLinks.basic={'Basic custom':'features'};apply()");
  d.getElementById('dockModeAdvanced').click();d.getElementById('plan-use-sample').click();
  test('Restoring Advanced sitemap preserves Basic link mappings',()=>evaluate("state.designProcess.pageLinks.basic['Basic custom']") ==='features' && evaluate('Object.keys(state.designProcess.pageLinks.advanced).length')===0);
  const beforeClampClipboard=w.navigator.clipboard;
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('Clipboard denied'))}});
  d.getElementById('clampCopy').click();await wait();
  test('Rejected clamp clipboard access offers a manual copy fallback',()=>d.getElementById('clampCopyStatus').textContent.includes('copy it manually'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:beforeClampClipboard});
  const unifiedDownloads=[],beforeUnifiedDownload=w.download;
  w.download=(name,content,type)=>unifiedDownloads.push({name,content,type});
  d.getElementById('saveBtn').click();d.getElementById('jExportJson').click();
  test('Project JSON entry points export identical filenames and data',()=>unifiedDownloads.length===2 && unifiedDownloads[0].name===unifiedDownloads[1].name && unifiedDownloads[0].content===unifiedDownloads[1].content);
  w.download=beforeUnifiedDownload;
  // Sitemap disclosure retains its existing grid/navigation and browsing state.
  for (const mode of ['basic','advanced']) {
    app.style.width='1440px';reset();await wait();
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    const footerDocument=previewDoc();
    test(mode+' live sitemap starts collapsed without changing its saved plan',()=>!previewDoc().getElementById('footer-sitemap').open && previewDoc().getElementById('sitemap').tagName==='NAV' && previewDoc().getElementById('sitemap').getAttribute('aria-labelledby')==='sitemap-title');
    previewDoc().getElementById('sitemap-toggle').click();previewDoc().getElementById('sitemap-toggle').focus();
    input('jAccent','#246a68');await wait();
    test(mode+' open sitemap and summary focus survive live palette rendering',()=>previewDoc()===footerDocument && previewDoc().getElementById('footer-sitemap').open && previewDoc().activeElement.id==='sitemap-toggle');
    input('jTheme','dark');await wait();
    test(mode+' sitemap stays open across theme updates',()=>previewDoc().getElementById('footer-sitemap').open);
    previewDoc().getElementById('sitemap-toggle').click();input('jRadius',18);await wait();
    test(mode+' collapsed sitemap stays collapsed after CSS edits',()=>!previewDoc().getElementById('footer-sitemap').open && !evaluate('projectJson()').includes('footer-sitemap'));
    const footerFragment=previewDoc().createElement('a');footerFragment.href='#sitemap';footerFragment.textContent='Review sitemap';previewDoc().body.append(footerFragment);footerFragment.click();await wait();
    test(mode+' preview fragment navigation reveals the collapsed sitemap destination',()=>previewDoc().getElementById('footer-sitemap').open && previewDoc().activeElement===previewDoc().getElementById('sitemap'));
    footerFragment.remove();
    const accordionPage=d.createElement('iframe'),accordionUrl=w.URL.createObjectURL(new w.Blob([evaluate('htmlExport()').replace('<link rel="stylesheet" href="tokens.css">','<style>'+evaluate('cssExport()')+'</style>')],{type:'text/html'}));
    accordionPage.src=accordionUrl;await new Promise(resolve=>{accordionPage.onload=resolve;d.body.append(accordionPage);});
    const fd=accordionPage.contentDocument,fw=accordionPage.contentWindow,disclosure=fd.getElementById('footer-sitemap');
    fw.location.hash='sitemap';await wait();
    test(mode+' standalone native fragment reveals the map without a script',()=>disclosure.open && !fd.querySelector('script') && fw.location.hash==='#sitemap');
    fd.getElementById('sitemap-toggle').click();
    test(mode+' standalone summary can collapse the fragment-revealed map',()=>!disclosure.open && fd.getElementById('sitemap').getBoundingClientRect().height===0);
    accordionPage.remove();w.URL.revokeObjectURL(accordionUrl);
  }
  reset();await wait();
  // A lesson uses the learner's own settings, real output and session comparison.
  for (const mode of ['basic','advanced']) for (const theme of ['light','dark']) {
    app.style.width='1440px';reset();await wait();
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    const beforeSpacingLesson=evaluate('projectJson()');
    d.querySelector('[data-journey-step="8"]').click();await wait();
    const spacingNode=d.querySelector('#studio-section-3 > .panel > .spacing-lesson');
    const exampleId=mode==='basic'?'lists':'services',exampleSelector=mode==='basic'?'.section':'.sample-section';
    test(mode+' '+theme+' spacing lesson connects five teaching parts without replacing the design',()=>spacingNode && [...spacingNode.querySelectorAll(':scope > section:not(#utilityLesson) > h4')].map(heading=>heading.textContent).join('|')==='Understand|Try|Observe|Inspect|Reflect' && evaluate('projectJson()')===beforeSpacingLesson && d.getElementById('spacingPrompt').textContent.includes('4 px to 6 px'));
    test(mode+' '+theme+' lesson starts its comparison from current exported spacing',()=>d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingBefore4').textContent==='16 px' && d.getElementById('spacingBefore8').textContent==='32 px' && d.getElementById('spacingCss').textContent.includes('--space-4: calc(var(--space-unit) * 4);'));
    d.getElementById('spacingEdit').click();
    test(mode+' '+theme+' lesson routes to the actual spacing control',()=>d.activeElement===d.getElementById('jSpacing') && evaluate('DSStudio.activeStage')===8);
    const spacingDocument=previewDoc();
    const beforeLessonPadding=parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart);
    input('jSpacing',6);await wait();
    test(mode+' '+theme+' spacing edit updates explanation, tokens and page without stealing control focus',()=>d.activeElement===d.getElementById('jSpacing') && previewDoc()===spacingDocument && d.getElementById('spacingNowUnit').textContent==='6 px' && d.getElementById('spacingNow4').textContent==='24 px' && d.getElementById('spacingNow8').textContent==='48 px' && d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingObservation').textContent.includes('4 px to 6 px') && parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart)===beforeLessonPadding*1.5);
    test(mode+' '+theme+' lesson shows the current sample HTML and consuming CSS rule',()=>evaluate('htmlExport()').includes(d.getElementById('spacingHtml').textContent) && d.getElementById('spacingHtml').textContent.includes('id="'+exampleId+'"') && d.getElementById('spacingHtml').children.length===0 && d.getElementById('spacingCss').textContent.includes(exampleSelector+' {') && d.getElementById('spacingConnection').textContent.includes('page currently measures '+parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById(exampleId)).paddingBlockStart)+' px'));
    input('spacingReflection','My explanation <scr'+'ipt>window.lessonInjected=true</scr'+'ipt>');input('jAccent','#246a68');await wait();
    test(mode+' '+theme+' unrelated colour edits retain comparison, reflection and lesson nodes',()=>d.querySelector('.spacing-lesson')===spacingNode && d.getElementById('spacingBeforeUnit').textContent==='4 px' && d.getElementById('spacingReflection').value.includes('My explanation') && !w.lessonInjected);
    input('advGap',32);await wait();
    test(mode+' '+theme+' grid gap is explained as a separate live decision',()=>d.getElementById('spacingGapNote').textContent.includes('32px') && d.getElementById('spacingGapNote').textContent.includes('comparison: 24px') && d.getElementById('spacingNow8').textContent==='48 px');
    const beforeCompare=evaluate('projectJson()');d.getElementById('spacingCompare').click();
    test(mode+' '+theme+' new comparison changes only session teaching state',()=>d.getElementById('spacingBeforeUnit').textContent==='6 px' && d.getElementById('spacingBefore8').textContent==='48 px' && evaluate('projectJson()')===beforeCompare);
    d.getElementById('spacingInspectTokens').click();
    test(mode+' '+theme+' Inspect spacing tokens opens complete current CSS',()=>d.getElementById('studioInspector').open && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='all' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingInspectRule').click();
    test(mode+' '+theme+' Inspect section CSS finds a real generated rule',()=>d.getElementById('dockCss').textContent.includes(exampleSelector+' {') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingInspectHtml').click();
    test(mode+' '+theme+' Inspect section HTML selects complete HTML',()=>d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('htmlExport()') && d.getElementById('dockCss').scrollTop>0);
    d.getElementById('spacingExample').click();await wait();
    test(mode+' '+theme+' preview observation opens the real section without changing project values',()=>previewDoc().activeElement===previewDoc().getElementById(exampleId) && d.getElementById('studio-section-4').open && evaluate('projectJson()')===beforeCompare);
    d.getElementById('spacingExample').click();d.getElementById('spacingInspectTokens').click();await wait();
    test(mode+' '+theme+' queued example focus cannot steal a subsequent code selection',()=>d.activeElement===d.getElementById('dockCss'));
    test(mode+' '+theme+' comparison, reflection and tutorial controls stay out of saved/exported data',()=>!evaluate('projectJson()+htmlExport()+cssExport()').includes('My explanation') && !evaluate('projectJson()+htmlExport()+cssExport()').includes('spacingReflection'));
    d.querySelector('[data-journey-step="9"]').click();d.querySelector('[data-journey-step="8"]').click();
    test(mode+' '+theme+' revisiting the lesson retains the session comparison',()=>d.getElementById('spacingBeforeUnit').textContent==='6 px' && d.getElementById('spacingReflection').value.includes('My explanation'));
  }
  d.getElementById('dockModeBasic').click();await wait();
  for (const [preset,token,multiplier] of [['mobile','--space-8',8],['tablet','--space-12',12],['desktop','--space-16',16]]) {
    d.querySelector('button[data-width="'+preset+'"]').click();d.getElementById('previewPage').getBoundingClientRect();await wait();
    test('Basic lesson follows actual responsive section padding at '+preset+' width',()=>{
      const connection=d.getElementById('spacingConnection').textContent,padding=parseFloat(previewWindow().getComputedStyle(previewDoc().getElementById('lists')).paddingBlockStart);
      if(connection.includes('padding-block uses '+token) && connection.includes((6*multiplier)+' px') && padding===6*multiplier && d.getElementById('spacingCss').textContent.includes('var('+token+')')) return true;
      throw Error(JSON.stringify({preset,width:previewWindow().innerWidth,padding,connection,css:d.getElementById('spacingCss').textContent}));
    });
  }
  d.querySelector('button[data-width="fluid"]').click();await wait();
  const beforeLessonResize=evaluate('projectJson()');
  d.getElementById('dockToggle').click();await wait();
  test('Fluid lesson reacts to released inspector width without changing the comparison',()=>{
    const connection=d.getElementById('spacingConnection').textContent;
    if(connection.includes('padding-block uses --space-12') && d.getElementById('spacingBeforeUnit').textContent==='6 px' && evaluate('projectJson()')===beforeLessonResize) return true;
    throw Error(JSON.stringify({width:previewWindow().innerWidth,connection,before:d.getElementById('spacingBeforeUnit').textContent,inspector:d.getElementById('studioInspector').open}));
  });
  d.getElementById('inspectorToggle').click();await wait();
  test('Fluid lesson follows the narrower rule when inspector opens again',()=>d.getElementById('spacingConnection').textContent.includes('padding-block uses --space-8') && evaluate('projectJson()')===beforeLessonResize);
  evaluate('importConfig({spacing:7.25})');await wait();
  test('Imported spacing drives lesson arithmetic from settled generated declarations',()=>d.getElementById('spacingNowUnit').textContent==='7.25 px' && d.getElementById('spacingNow4').textContent==='29 px' && d.getElementById('spacingNow8').textContent==='58 px' && d.getElementById('spacingBeforeUnit').textContent==='7.25 px' && !d.getElementById('spacingReflection').value && d.getElementById('spacingGapNote').textContent.startsWith('Grid gap is 24px.'));
  input('jSpacing',8);d.getElementById('spacingCompare').click();
  test('Spacing experiment stays within the real control limits at the upper bound',()=>d.getElementById('spacingPrompt').textContent.includes('8 px to 6 px'));
  input('spacingReflection','Clear after project reset');reset();await wait();
  test('Reset starts a fresh comparison and clears optional reflection',()=>d.getElementById('spacingBeforeUnit').textContent==='4 px' && !d.getElementById('spacingReflection').value);
  input('jProject','Spacing lesson test');d.getElementById('jSaveLocal').click();input('spacingReflection','Clear after local load');d.getElementById('jLoadLocal').click();await wait();
  test('Loading even identical saved project values starts a fresh tutorial session comparison',()=>!d.getElementById('spacingReflection').value && d.getElementById('spacingBeforeUnit').textContent==='4 px');
  const spacingPracticeWasOpen=d.getElementById('utilityPractice').open;
  for (const theme of ['light','dark']) for (const width of [320,901,1440]) {
    app.style.width=width+'px';input('jTheme',theme);await wait();d.querySelector('[data-journey-step="8"]').click();
    // Measure displayed controls, not cached geometry inside a closed disclosure.
    d.getElementById('utilityPractice').open=true;await wait();
    test(theme+' spacing tutorial stays within its lesson at '+width+'px',()=>{
      const lesson=d.querySelector('.spacing-lesson'),box=lesson.getBoundingClientRect();
      const source=d.getElementById('jSpacing'),inline=source.closest('.spacing-lesson > section');
      const buttons=[...lesson.querySelectorAll('.button-row > button')].map(button=>{const b=button.getBoundingClientRect();return {id:button.id,height:b.height,left:b.left,right:b.right,closedPractice:button.closest('#utilityPractice')?.open===false};});
      const fits=d.documentElement.scrollWidth<=w.innerWidth+1 && lesson.scrollWidth<=lesson.clientWidth+1 && (width>900?source.closest('.studio-journey')!==null:inline?.querySelector('h4').textContent==='Try') && buttons.every(b=>b.height>=44 && b.left>=box.left-1 && b.right<=box.right+1);
      if(!fits)throw Error(JSON.stringify({documentWidth:d.documentElement.scrollWidth,viewport:w.innerWidth,lessonWidth:lesson.clientWidth,lessonScroll:lesson.scrollWidth,left:box.left,right:box.right,inline:inline?.querySelector('h4').textContent,desktop:!!source.closest('.studio-journey'),buttons}));
      return true;
    });
  }
  d.getElementById('utilityPractice').open=spacingPracticeWasOpen;
  app.style.width='1440px';reset();await wait();
  // Collapsing code releases the complete column and safely restores focus.
  d.getElementById('dockModeBasic').click();input('dockSection','footer','change');
  d.querySelector('button[data-width="fluid"]').click();
  w.DSStudio.inspector.show({language:'html',section:'footer'});await wait();
  const collapseProject=evaluate('projectJson()'),collapseDocument=previewDoc();
  for (const width of [320,901,1280,1440,2560]) {
    app.style.width=width+'px';await wait();
    const expandedWidth=d.getElementById('previewFrame').getBoundingClientRect().width;
    d.getElementById('dockCss').focus();d.getElementById('dockToggle').click();await wait();
    test('Collapse releases inspector space and restores opener focus at '+width+'px',()=>{
      const layout=d.querySelector('.layout'),left=d.querySelector('.sidebar').getBoundingClientRect().width;
      const openerBounds=d.getElementById('inspectorToggle').getBoundingClientRect();
      if(openerBounds.top<d.querySelector('.topbar').getBoundingClientRect().bottom || openerBounds.bottom>w.innerHeight) throw Error(JSON.stringify({width,top:openerBounds.top,bottom:openerBounds.bottom,header:d.querySelector('.topbar').getBoundingClientRect().bottom,scroll:w.scrollY,active:d.activeElement.id}));
      return !d.getElementById('studioInspector').open && d.getElementById('inspectorToggle').getBoundingClientRect().width>0 && d.getElementById('dockCss').getBoundingClientRect().height===0 && d.activeElement===d.getElementById('inspectorToggle') && (width<=900 || Math.abs(left-(layout.clientWidth-16)/4)<1) && (width<=1280 || d.getElementById('previewFrame').getBoundingClientRect().width>expandedWidth) && d.documentElement.scrollWidth<=w.innerWidth+1;
    });
    d.getElementById('inspectorToggle').click();await wait();
    test('Native disclosure restores language, excerpt and live document at '+width+'px',()=>d.getElementById('studioInspector').open && d.getElementById('studioInspector').open && d.getElementById('dockTabHtml').getAttribute('aria-selected')==='true' && d.getElementById('dockSection').value==='footer' && d.activeElement===d.getElementById('inspectorToggle') && previewDoc()===collapseDocument && evaluate('projectJson()')===collapseProject && d.documentElement.scrollWidth<=w.innerWidth+1);
  }
  d.getElementById('dockToggle').click();
  test('Pane Collapse returns to its compact bar and releases the inspector column',()=>!d.getElementById('studioInspector').open && d.querySelector('.layout').classList.contains('is-inspector-collapsed'));
  d.querySelector('[data-journey-step="7"]').click();d.querySelector('#buttonDesignLab [data-inspect="css"]').click();
  test('Contextual Inspect CSS reopens the hidden column and selects its promised output',()=>d.getElementById('studioInspector').open && !d.querySelector('.layout').classList.contains('is-inspector-collapsed') && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && previewDoc()===collapseDocument);
  test('Inspector visibility is absent from project JSON',()=>!Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/inspector|collapsed/i.test(key)));
  // Studio section returns never navigate or regenerate the sample website.
  reset();app.style.width='1440px';await wait();
  test('Every studio panel, wizard pane and inspector ends with one native return link',()=>[...d.querySelectorAll('.studio-section > .panel, [data-journey-pane], #studioInspector')].every(container=>{
    const rows=container.querySelectorAll(':scope > .studio-home-return'),link=rows[0]?.querySelector('a');
    return rows.length===1 && container.lastElementChild===rows[0] && link?.getAttribute('href')==='#studio-home' && link.tabIndex===0 && link.textContent.startsWith('Back to top') && link.querySelector('span').getAttribute('aria-hidden')==='true';
  }));
  for(const theme of ['light','dark']) for(const width of [320,901,1440]) {
    input('jTheme',theme);app.style.width=width+'px';w.dssShowWizardStep(4);await wait();
    const controls=d.querySelector('[data-journey-pane="4"]'),panel=d.querySelector('#brandPalette > .panel');
    test(theme+' section return links align right and fit '+width+'px',()=>[controls,panel].every(container=>{
      const row=container.querySelector(':scope > .studio-home-return'),link=row.querySelector('a'),box=link.getBoundingClientRect(),rowBox=row.getBoundingClientRect();
      return box.width>=44 && box.height>=44 && box.width<=container.clientWidth+1 && Math.abs(box.right-(rowBox.right-parseFloat(w.getComputedStyle(row).paddingRight)))<1;
    }) && d.documentElement.scrollWidth<=w.innerWidth+1);
    const beforeHome=evaluate('projectJson()'),beforeStage=w.DSStudio.activeStage,beforeDocument=previewDoc(),beforeLibrary=w.localStorage.getItem('dss-v27-projects');
    const openState=[...d.querySelectorAll('#main > .studio-section')].map(el=>el.open).join(',');
    const link=panel.querySelector(':scope > .studio-home-return a');link.scrollIntoView({block:'center',behavior:'instant'});link.focus();link.click();await wait();
    test(theme+' return reaches the studio top with visible focus at '+width+'px',()=>w.scrollY<=1 && d.activeElement===d.getElementById('studio-home') && w.getComputedStyle(d.getElementById('studio-home')).outlineStyle==='solid' && d.getElementById('studio-home').getBoundingClientRect().top>=-1);
    test(theme+' return preserves the current stage, project, library and preview at '+width+'px',()=>evaluate('projectJson()')===beforeHome && w.DSStudio.activeStage===beforeStage && previewDoc()===beforeDocument && w.localStorage.getItem('dss-v27-projects')===beforeLibrary && [...d.querySelectorAll('#main > .studio-section')].map(el=>el.open).join(',')===openState);
  }
  app.style.width='1440px';w.dssShowWizardStep(8);await wait();
  const nativeReturn=d.querySelector('#studio-section-3 > .panel > .studio-home-return a');
  nativeReturn.scrollIntoView({block:'center',behavior:'instant'});nativeReturn.focus();d.documentElement.style.scrollBehavior='smooth';
  nativeReturn.dispatchEvent(new w.MouseEvent('click',{bubbles:true,cancelable:true,button:0,detail:0}));await wait();
  test('Keyboard-style link activation returns immediately despite smooth page scrolling',()=>w.scrollY<=1 && d.activeElement===d.getElementById('studio-home'));
  d.documentElement.style.removeProperty('scroll-behavior');
  for(const stage of w.DSStudio.orderedStages) {
    w.dssShowWizardStep(stage.index,false);await wait();
    test(stage.label+' retains one return link after stage routing',()=>d.querySelectorAll('#'+stage.lesson+' > .panel > .studio-home-return').length===1 && d.querySelectorAll('[data-journey-pane="'+stage.index+'"] > .studio-home-return').length===1);
  }
  w.DSStudio.inspector.show({language:'css',section:'all'});await wait();
  const homeCode=d.getElementById('dockCss').textContent,homeMode=evaluate('state.sampleMode');
  d.querySelector('#studioInspector > .studio-home-return a').click();await wait();
  test('Inspector return retains its visibility, selected language and exact output',()=>d.getElementById('studioInspector').open && d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===homeCode && evaluate('state.sampleMode')===homeMode && d.activeElement===d.getElementById('studio-home'));
  for(const mode of ['basic','advanced']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();await wait();
    test(mode+' preview and exported files contain no studio return controls',()=>!previewDoc().querySelector('.studio-home-return,.studio-home-link,#studio-home') && !evaluate('htmlExport()').includes('studio-home') && !evaluate('cssExport()').includes('studio-home'));
  }
  // End studio section return checks.

  // Tailwind is an optional source mapping; the website generators remain authoritative.
  reset();await wait();w.dssShowWizardStep(11);await wait();
  const bridgeSource=()=>w.DSStudio.tailwind.source();
  const bridgeSnapshot=()=>JSON.stringify(evaluate('[projectJson(),htmlExport(),cssExport()]'));
  const bridgeCell=source=>d.querySelector('#tailwindMappingRows tr[data-source="'+source+'"] td code');
  test('Deliver presents the Tailwind explanation inside its existing centre lesson',()=>d.getElementById('tailwindBridge').closest('.studio-section').id==='studio-section-6' && d.getElementById('tailwindBridge').closest('.studio-lesson') && w.DSStudio.activeStage===11);
  test('Tailwind example teaches the same four properties without executing its markup',()=>d.getElementById('tailwindCssExample').textContent.includes('padding: var(--space-6)') && ['p-6','bg-surface','text-content','rounded-card'].every(value=>d.getElementById('tailwindHtmlExample').textContent.includes(value)) && !d.getElementById('tailwindHtmlExample').querySelector('article'));
  const bridgeInitial=bridgeSource();
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('previewTheme',theme,'change');await wait();
    test(mode+' '+theme+' mapping follows exported semantic roles independently of Studio appearance',()=>bridgeCell('--surface').textContent===evaluate('palette().roles.surface') && bridgeCell('--text').textContent===evaluate('palette().roles.text') && d.getElementById('tailwindContext').textContent.includes(theme==='dark'?'Dark':'Light'));
    test(mode+' '+theme+' selection leaves the two-theme Tailwind source unchanged',()=>bridgeSource()===bridgeInitial);
  }
  test('Tailwind source maps colour/font/type/radius/spacing without self-references or component CSS',()=>bridgeSource().includes('--color-content: var(--text);') && bridgeSource().includes('--font-display: var(--font-heading);') && bridgeSource().includes('--spacing: var(--space-unit);') && bridgeSource().includes('@theme inline') && !/--([\w-]+): var\(--\1\);/.test(bridgeSource()) && !bridgeSource().includes('.ds-button {') && !bridgeSource().includes('@import'));
  const bridgeRows=[...d.querySelectorAll('#tailwindMappingRows tr')];
  input('jSpacing',8);input('jRadius',26);input('bdRadius',18);input('jBase',20);await wait();
  test('Spacing and independent card/button corners trace current project values',()=>bridgeCell('--space-unit').textContent==='8px' && d.getElementById('tailwindSpacingExample').textContent.includes('48px') && bridgeCell('--radius-base').textContent==='26px' && bridgeCell('--button-radius').textContent==='18px');
  test('Tailwind type mapping reads the exact fluid export declaration',()=>bridgeCell('--text-body').textContent===w.dssReadTokens().find(row=>row.name==='--text-body').value && bridgeSource().includes('--text-body: '+bridgeCell('--text-body').textContent+';'));
  const bridgeFont=d.getElementById('jFont').options[1].value;input('jFont',bridgeFont);await wait();
  test('Font mapping reads the project font stack instead of the Studio font',()=>bridgeCell('--font-body').textContent===w.dssReadTokens().find(row=>row.name==='--font-body').value && bridgeSource().includes('--font-body: '+bridgeCell('--font-body').textContent+';'));
  evaluate("state.semanticOverrides={light:{surface:'#F0E0D0',text:'#332211'},dark:{surface:'#112233',text:'#DDEEFF'}};apply()");await wait();
  input('previewTheme','light','change');await wait();
  test('Light mapping reflects overrides and source preserves both theme values',()=>bridgeCell('--surface').textContent==='#F0E0D0' && bridgeSource().includes('--surface: #F0E0D0;') && bridgeSource().includes('--surface: #112233;') && bridgeSource().includes('@custom-variant dark (&:where([data-theme="dark"], [data-theme="dark"] *))'));
  input('previewTheme','dark','change');await wait();
  test('Dark mapping reflects its own overrides without replacing the light definitions',()=>bridgeCell('--text').textContent==='#DDEEFF' && bridgeSource().includes('--text: #332211;'));
  evaluate('state.responsiveDesign={stack:640,wide:1120,maxWidth:1152,gutter:16,wideGutter:32};apply()');await wait();
  test('Tailwind breakpoints use saved literal lengths outside the inline alias block',()=>bridgeSource().includes('@theme {\n  --breakpoint-page-stack: 40rem;\n  --breakpoint-page-wide: 70rem;') && !bridgeSource().includes('--breakpoint-page-stack: var(') && bridgeCell('Saved stacking cutoff').textContent==='40rem');
  evaluate('renderCode()');await wait();
  test('Mapping rows and unchanged source text survive refreshes',()=>bridgeRows.every((row,index)=>row===d.querySelectorAll('#tailwindMappingRows tr')[index]));
  const bridgeText=d.getElementById('tailwindSource').firstChild;evaluate('renderCode()');await wait();
  test('Unchanged Tailwind source retains its selectable text node',()=>d.getElementById('tailwindSource').firstChild===bridgeText);
  const bridgeBeforeActions=bridgeSnapshot(),bridgePreview=previewDoc();
  const bridgeDownloads=[],bridgeDownload=w.download,bridgeClipboard=w.navigator.clipboard;
  w.download=(name,text,type)=>bridgeDownloads.push({name,text,type});
  let bridgeCopied='';Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:async text=>{bridgeCopied=text;}}});
  d.getElementById('tailwindMappings').open=true;d.getElementById('tailwindSourceDetails').open=true;
  d.getElementById('tailwindCopy').click();await wait();d.getElementById('tailwindDownload').click();
  test('Tailwind copy and download use current source with a distinct filename and MIME type',()=>bridgeCopied===bridgeSource() && bridgeDownloads.length===1 && bridgeDownloads[0].name==='tailwind-theme.css' && bridgeDownloads[0].type==='text/css' && bridgeDownloads[0].text===bridgeSource() && d.getElementById('tailwindStatus').textContent.includes('download requested'));
  test('Bridge interactions preserve exact project JSON, website HTML/CSS and preview document',()=>bridgeSnapshot()===bridgeBeforeActions && previewDoc()===bridgePreview && !evaluate('cssExport()').includes('@theme') && !evaluate('htmlExport()').includes('tailwindBridge'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>Promise.reject(new Error('Clipboard denied'))}});
  d.getElementById('tailwindSourceDetails').open=false;d.getElementById('tailwindCopy').click();await wait();
  test('Denied Tailwind clipboard access opens source and explains manual copying',()=>d.getElementById('tailwindSourceDetails').open && d.getElementById('tailwindStatus').textContent.includes('copy it manually'));
  let bridgeFinishCopy;Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:{writeText:()=>new Promise(resolve=>{bridgeFinishCopy=resolve;})}});
  d.getElementById('tailwindCopy').click();input('jSpacing',3);await wait();bridgeFinishCopy();await wait();
  test('Delayed Tailwind clipboard feedback identifies an older settings snapshot',()=>d.getElementById('tailwindStatus').textContent.includes('earlier theme source'));
  Object.defineProperty(w.navigator,'clipboard',{configurable:true,value:bridgeClipboard});w.download=bridgeDownload;
  d.getElementById('tailwindInspect').click();await wait();
  test('Mapping inspection opens the complete existing website CSS',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate('cssExport()'));
  evaluate('importConfig({project:"<img src=x onerror=alert(1)>",spacing:1e10,radius:-100,font:"Arial; color:red",responsiveDesign:{stack:-1,wide:1e10},semanticOverrides:{light:{surface:"red; color:green"}}})');await wait();
  test('Hostile imports cannot inject mapping markup or executable theme declarations',()=>!d.getElementById('tailwindBridge').querySelector('img,script,style') && !bridgeSource().includes('onerror') && !bridgeSource().includes('color:green') && !bridgeSource().includes('Arial;') && bridgeCell('--space-unit').textContent==='8px' && bridgeSource().includes('--breakpoint-page-stack: 30rem;'));
  reset();await wait();
  test('Project reset refreshes mapping defaults without adding persistence fields',()=>bridgeCell('--space-unit').textContent==='4px' && !Object.keys(JSON.parse(evaluate('projectJson()'))).some(key=>/tailwind/i.test(key)));
  for(const width of [320,390,1440])for(const studio of ['light','dark']) {
    app.style.width=width+'px';if(d.documentElement.dataset.theme!==studio)d.getElementById('themeToggle').click();
    w.dssShowWizardStep(11);d.getElementById('tailwindMappings').open=true;d.getElementById('tailwindSourceDetails').open=true;await wait();
    test(studio+' Tailwind lesson stays readable and scrolls its table locally at '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['tailwindCopy','tailwindDownload','tailwindInspect'].every(id=>{const r=d.getElementById(id).getBoundingClientRect();return r.height>=44 && r.left>=0 && r.right<=w.innerWidth+1;}) && (width>390 || d.querySelector('.tailwind-table-scroll').scrollWidth>d.querySelector('.tailwind-table-scroll').clientWidth));
  }
  app.style.width='1440px';if(d.documentElement.dataset.theme!=='light')d.getElementById('themeToggle').click();reset();await wait();
  // Compare against an otherwise identical document without this optional module.
  const bridgeBaselineHtml=(await (await w.fetch('/index.html')).text()).replace(/<script[^>]+src="src\/js\/tailwind-bridge\.js[^>]*><\/script>/g,'').replace(/<link[^>]+href="src\/css\/tailwind-bridge\.css[^>]*>/g,'');
  const bridgeBaseline=d.createElement('iframe');bridgeBaseline.hidden=true;
  await new Promise(resolve=>{bridgeBaseline.onload=resolve;bridgeBaseline.srcdoc=bridgeBaselineHtml;d.body.append(bridgeBaseline);});
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    const config=JSON.parse(evaluate('projectJson()'));config.sampleMode=mode;config.theme=theme;config.spacing=7;config.radius=20;
    w.importConfig(config);bridgeBaseline.contentWindow.importConfig(config);await wait();
    test(mode+' '+theme+' website exports are byte-identical with and without the Tailwind bridge',()=>!bridgeBaseline.contentWindow.DSStudio.tailwind && evaluate('cssExport()')===bridgeBaseline.contentWindow.cssExport() && evaluate('htmlExport()')===bridgeBaseline.contentWindow.htmlExport() && evaluate('projectJson()')===bridgeBaseline.contentWindow.projectJson());
  }
  bridgeBaseline.remove();reset();await wait();

  // Working plain-CSS utilities retain semantic HTML and component defaults.
  reset();await wait();
  w.dssShowWizardStep(8);await wait();
  test('Local CSS starts with a linked stylesheet and utility practice stays optional',()=>d.getElementById('localCardHtml').textContent.includes('<link rel="stylesheet" href="tokens.css">') && d.getElementById('localCardHtml').textContent.includes('<article class="card">') && !d.getElementById('localCardHtml').querySelector('article,link') && !d.getElementById('utilityPractice').open && !d.getElementById('utilityVocabularyDetails').open && d.getElementById('localCardCss').getBoundingClientRect().height>0);
  test('Optional utility examples are bounded native CSS and excluded from website CSS',()=>w.DSStudio.utilities.definitions.length===20 && new Set(w.DSStudio.utilities.definitions.map(item=>item.name)).size===20 && w.DSStudio.utilities.definitions.every(item=>w.CSS.supports(item.property,item.value) && w.DSStudio.utilities.css().includes(w.DSStudio.utilities.rule(item.name)) && !evaluate('cssExport()').includes(w.DSStudio.utilities.rule(item.name))) && w.DSStudio.utilities.rule('__proto__')==='');
  const utilityParityFrame=d.createElement('iframe');utilityParityFrame.style.cssText='border:0;position:absolute;left:-10000px';d.body.append(utilityParityFrame);
  const utilityNames=new Set(w.DSStudio.utilities.definitions.map(item=>item.name));
  const utilityStyleKeys=['display','flexDirection','flexWrap','alignItems','justifyContent','gap','padding','backgroundColor','color','borderRadius','border','boxShadow','opacity','fontFamily','fontSize','lineHeight','width','height'];
  const utilitySignature=(el,view)=>{const cs=view.getComputedStyle(el);return utilityStyleKeys.map(key=>cs[key]).join('|');};
  const utilityTargets='.card,.media-object,.hero-layout,.skills-layout,.list-grid,.sample-flex-row,.sample-flex-media,.sample-flex-stack';
  async function loadUtilityPractice() {
    const parsed=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    parsed.getElementById(evaluate('state.sampleMode')==='basic'?'basic-structure':'lesson-brief').classList.add('p-6','bg-surface','text-content','rounded-card');
    const utilityBlob=w.URL.createObjectURL(new w.Blob([evaluate('cssExport()')+w.DSStudio.utilities.css()],{type:'text/css'}));
    parsed.querySelector('link[href="tokens.css"]').href=utilityBlob;
    utilityParityFrame.style.width=previewWindow().innerWidth+'px';utilityParityFrame.style.height=previewWindow().innerHeight+'px';
    await new Promise(resolve=>{utilityParityFrame.onload=resolve;utilityParityFrame.srcdoc='<!doctype html>'+parsed.documentElement.outerHTML;});
    w.URL.revokeObjectURL(utilityBlob);
  }
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);
    for(const custom of [false,true]) {
      if(custom){input('jSpacing',8);input('jRadius',26);input('advGap',32);input('advOpacity',75);input('advShadow','medium','change');}
      for(const width of [320,1440]) {
        app.style.width=width+'px';d.querySelector('[data-width="fluid"]').click();await wait();
        await loadUtilityPractice();
        const actual=[...previewDoc().querySelectorAll(utilityTargets)],native=[...utilityParityFrame.contentDocument.querySelectorAll(utilityTargets)];
        test(mode+' '+theme+' '+(custom?'custom':'default')+' separate utility practice matches component appearance at '+width+'px',()=>actual.length>0 && actual.length===native.length && actual.every((el,index)=>utilitySignature(el,previewWindow())===utilitySignature(native[index],utilityParityFrame.contentWindow)));
        const article=previewDoc().getElementById(mode==='basic'?'basic-structure':'lesson-brief');
        test(mode+' '+theme+' '+(custom?'custom':'default')+' website HTML keeps component classes without exercise utilities at '+width+'px',()=>![...previewDoc().querySelectorAll('[class]')].some(el=>[...el.classList].some(name=>utilityNames.has(name))) && !evaluate('cssExport()').includes('OPTIONAL PRACTICE'));
        test(mode+' '+theme+' '+(custom?'custom':'default')+' semantic article uses its shared local card rule at '+width+'px',()=>article.tagName==='ARTICLE' && article.classList.contains('card') && Math.abs(parseFloat(previewWindow().getComputedStyle(article).paddingTop)-evaluate('state.spacing')*6)<.01 && !previewDoc().querySelector('script'));
      }
    }
  }
  app.style.width='1440px';reset();await wait();
  const beforeUtilityExercise=evaluate('htmlExport()+cssExport()+projectJson()'),beforeExerciseDoc=previewDoc();
  await loadUtilityPractice();
  const exerciseWindow=utilityParityFrame.contentWindow;
  const utilityArticle=utilityParityFrame.contentDocument.getElementById('lesson-brief'),utilityOriginalClass=utilityArticle.className;
  utilityArticle.classList.replace('p-6','p-4');
  test('Practice-only p-4 changes padding and retains article meaning and component border',()=>exerciseWindow.getComputedStyle(utilityArticle).paddingTop==='16px' && utilityArticle.tagName==='ARTICLE' && utilityArticle.classList.contains('card') && parseFloat(exerciseWindow.getComputedStyle(utilityArticle).borderTopWidth)>0);
  utilityArticle.className='p-6 p-4 card bg-surface text-content rounded-card';const utilityFirstOrder=exerciseWindow.getComputedStyle(utilityArticle).paddingTop;
  utilityArticle.className='p-4 p-6 card bg-surface text-content rounded-card';
  test('Conflicting practice utilities follow stylesheet order rather than HTML class order',()=>utilityFirstOrder==='24px' && exerciseWindow.getComputedStyle(utilityArticle).paddingTop===utilityFirstOrder);
  utilityArticle.className=utilityOriginalClass;utilityArticle.classList.replace('bg-surface','bg-primary');utilityArticle.classList.replace('text-content','text-on-primary');
  test('Practice colour utilities consume active project theme roles',()=>exerciseWindow.getComputedStyle(utilityArticle).backgroundColor===evaluate("'rgb('+hexRgb(palette().roles.primary).join(', ')+')'") && exerciseWindow.getComputedStyle(utilityArticle).color===evaluate("'rgb('+hexRgb(palette().roles['on-primary']).join(', ')+')'"));
  test('Utility practice leaves website preview and all exports unchanged',()=>previewDoc()===beforeExerciseDoc && evaluate('htmlExport()+cssExport()+projectJson()')===beforeUtilityExercise && previewWindow().getComputedStyle(previewDoc().getElementById('lesson-brief')).paddingTop==='24px');
  utilityParityFrame.remove();
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();input('jTheme',theme);w.dssShowWizardStep(8);await wait();
    const id=mode==='basic'?'basic-structure':'lesson-brief';
    test(mode+' '+theme+' local CSS example reads the exported component rule',()=>evaluate('cssExport()').replace(/\s+/g,'').includes(d.getElementById('localCardCss').textContent.replace(/\s+/g,'')) && d.getElementById('localCardCss').textContent.startsWith('.card {\n  ') && d.getElementById('localCardCss').textContent.includes('padding: var(--space-6)'));
    d.getElementById('utilityPractice').open=true;await wait();
    test(mode+' '+theme+' lesson follows spacing reflection and reads the real article tag',()=>d.getElementById('utilityLesson').closest('.studio-lesson').classList.contains('spacing-lesson') && d.getElementById('utilityLesson').previousElementSibling.querySelector('h4').textContent==='Reflect' && d.getElementById('utilityHtml').textContent.includes('id="'+id+'"') && evaluate('htmlExport()').includes(d.getElementById('utilityHtml').textContent));
    for(const name of ['p-6','p-4','bg-surface','text-content','rounded-card']) {
      input('utilityClass',name,'change');await wait();const definition=w.DSStudio.utilities.definitions.find(item=>item.name===name);
      test(mode+' '+theme+' lesson separates practice '+name+' from actual component output',()=>d.getElementById('utilityRule').textContent===w.DSStudio.utilities.rule(name) && !evaluate('cssExport()').includes(d.getElementById('utilityRule').textContent) && d.getElementById('utilityPracticeHtml').textContent.includes(' '+name+'"') && !evaluate('htmlExport()').includes(d.getElementById('utilityPracticeHtml').textContent) && !d.getElementById('utilityPracticeHtml').children.length && d.getElementById('utilityToken').textContent.includes(definition.token+':') && d.getElementById('utilityMeasured').textContent.includes('component preview measures '+definition.property+': '+previewWindow().getComputedStyle(previewDoc().getElementById(id)).getPropertyValue(definition.property)));
    }
  }
  input('utilityClass','p-6','change');input('jSpacing',7);await wait();
  test('Source edits refresh lesson and page padding',()=>d.getElementById('utilityToken').textContent.includes('--space-unit: 7px') && d.getElementById('utilityMeasured').textContent.includes('42px'));
  d.getElementById('utilityConfigure').click();
  test('Utility configuration focuses the existing spacing control',()=>d.activeElement===d.getElementById('jSpacing') && w.DSStudio.activeStage===8);
  d.getElementById('utilityInspectCss').click();await wait();
  test('Component CSS inspection keeps the complete local stylesheet',()=>d.getElementById('studioInspector').open && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.getElementById('dockNote').textContent.includes('No framework needed') && !d.getElementById('dockCss').textContent.includes('.p-6 {'));
  d.getElementById('dockTabHtml').click();d.getElementById('localInspectCss').click();await wait();
  test('Local-first action opens component CSS from the HTML inspector',()=>d.getElementById('dockTabCss').getAttribute('aria-selected')==='true' && d.getElementById('dockCss').textContent===evaluate('cssExport()') && d.activeElement===d.getElementById('dockCss'));
  d.getElementById('utilityInspectHtml').click();await wait();
  test('Utility HTML inspection keeps the complete semantic page',()=>d.getElementById('dockCss').textContent===evaluate('htmlExport()'));
  const utilityProject=evaluate('projectJson()'),utilityDocument=previewDoc();d.getElementById('utilityPreview').click();await wait();
  test('Showing the utility article retains project and preview document',()=>previewDoc()===utilityDocument && previewDoc().activeElement===previewDoc().getElementById('lesson-brief') && evaluate('projectJson()')===utilityProject);
  test('Showing the utility article brings the preview into view',()=>d.getElementById('previewShell').getBoundingClientRect().top>=0 && d.getElementById('previewShell').getBoundingClientRect().top<w.innerHeight);
  for(const width of [320,390,1440])for(const theme of ['light','dark']) {
    app.style.width=width+'px';input('jTheme',theme);w.dssShowWizardStep(8);d.querySelectorAll('#utilityLesson details').forEach(details=>details.open=true);await wait();
    test(theme+' utility lesson fits '+width+'px with usable controls',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && ['localInspectCss','utilityClass','utilityPreview','utilityInspectHtml','utilityInspectCss','utilityConfigure'].every(id=>{const r=d.getElementById(id).getBoundingClientRect();return r.height>=44 && r.left>=0 && r.right<=w.innerWidth+1;}) && (width>390 || d.querySelector('.utility-table-scroll').scrollWidth>d.querySelector('.utility-table-scroll').clientWidth));
  }
  app.style.width='1440px';reset();await wait();
  w.dssShowWizardStep(8);await wait();
  const beforeLearningPath=evaluate('projectJson()'),learningPathDoc=previewDoc();
  d.getElementById('utilityToTailwind').click();await wait();
  test('Optional next step reaches Tailwind without changing the local website',()=>w.DSStudio.activeStage===11 && !d.getElementById('studio-section-6').hidden && evaluate('projectJson()')===beforeLearningPath && previewDoc()===learningPathDoc && d.getElementById('tailwindBridge').textContent.includes('separate Tailwind v4 practice project'));
  d.querySelector('#tailwindBridge a[href="#utilityLesson"]').click();await wait();
  test('Tailwind exercise links back to the local CSS lesson',()=>w.DSStudio.activeStage===8 && !d.getElementById('studio-section-3').hidden && evaluate('projectJson()')===beforeLearningPath && previewDoc()===learningPathDoc);

  // Full information architecture and independently selected visitor sitemap.
  const iaNodes=()=>{revealDestinationPlan();return w.DSStudio.process.entries();};
  const iaNode=label=>iaNodes().find(node=>node.label===label);
  const iaChoice=label=>[...d.querySelectorAll('#sitemap-choices input')].find(input=>input.dataset.iaId===iaNode(label)?.id);
  const iaSelect=label=>{const option=[...d.getElementById('sitemap-items').options].find(option=>option.textContent.replace(/^\s*—\s*/,'').trim()===label);input('sitemap-items',option.value,'change');};
  const iaFooterHas=label=>[...previewDoc().querySelectorAll('#sitemap a, #sitemap span')].some(el=>el.firstChild?.textContent===label);
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    const parent=mode==='basic'?'Components':'Lessons',child=mode==='basic'?'Content card':'Brief lesson';
    const target=mode==='basic'?'basic-structure':'lesson-brief';
    test(mode+' IA shows every parent and child including sitemap exclusions',()=>d.querySelectorAll('#process-ia .process-map li').length===iaNodes().length && d.querySelector('#process-ia .process-map').textContent.includes('Footer') && d.querySelector('#process-ia .process-map').textContent.includes('Home') && d.querySelectorAll('#sitemap-choices input').length===iaNodes().length);
    test(mode+' lesson distinguishes IA from the visitor sitemap and cites NN/g',()=>d.querySelector('#process-ia .process-ia-guidance a').href==='https://www.nngroup.com/articles/information-architecture-sitemaps/' && d.querySelector('#process-ia .process-ia-guidance').textContent.includes('not remove those hours') && JSON.stringify([...d.querySelectorAll('#process-ia .process-sitemap-preview a')].map(a=>[a.textContent,a.dataset.sitemapTarget]))===JSON.stringify([...previewDoc().querySelectorAll('#sitemap a')].map(a=>[a.textContent,a.hash.slice(1)])));
    const previewLink=d.querySelector('#process-ia .process-sitemap-preview a'),linkedId=previewLink.dataset.sitemapTarget,linkedDoc=previewDoc(),beforePreviewLink=evaluate('projectJson()');
    previewLink.click();await wait();
    test(mode+' visitor sitemap preview links focus the real iframe destination safely',()=>previewLink.hash==='#previewShell' && previewDoc()===linkedDoc && previewDoc().activeElement.id===linkedId && w.DSStudio.activeStage===1 && evaluate('projectJson()')===beforePreviewLink);
    const beforePages=evaluate('DSStudio.process.currentPlan().pages'),beforeCss=evaluate('cssExport()'),beforeBodySections=previewDoc().querySelectorAll('main > section').length;
    const original=iaNode(child),control=iaChoice(child);control.focus();control.click();await wait();
    test(mode+' child exclusion changes only sitemap navigation and retains checkbox focus',()=>!iaFooterHas(child) && iaNode(child).id===original.id && !iaNode(child).includeInSitemap && evaluate('DSStudio.process.currentPlan().pages')===beforePages && evaluate('cssExport()')===beforeCss && previewDoc().getElementById(target) && previewDoc().querySelectorAll('main > section').length===beforeBodySections && d.querySelector('#process-ia .process-map').textContent.includes(child) && d.activeElement===control);
    iaChoice(parent).click();await wait();
    test(mode+' excluded parent suppresses its branch without losing child choices',()=>!iaFooterHas(parent) && iaChoice(child).disabled && !iaChoice(child).checked && iaNodes().filter(node=>node.parentId===iaNode(parent).id).some(node=>node.includeInSitemap));
    iaChoice(parent).click();await wait();
    test(mode+' restoring parent respects individual child exclusions',()=>iaFooterHas(parent) && !iaChoice(child).disabled && !iaFooterHas(child) && !iaChoice(child).checked);
    iaSelect(child);input('sitemap-label','Renamed information');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' renaming excluded information preserves identity and inclusion',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap && !iaFooterHas('Renamed information') && d.querySelector('#process-ia .process-map').textContent.includes('Renamed information'));
    const destinationParent=mode==='basic'?'Layouts':'Layout workshop';
    input('sitemap-parent',String(w.DSStudio.process.hierarchy(w.DSStudio.process.currentPlan().pages).findIndex(([label])=>label===destinationParent)),'change');
    input('sitemap-type','content','change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' reparenting keeps stable identity, type and sitemap choice',()=>iaNode('Renamed information').id===original.id && iaNode('Renamed information').path[0]===destinationParent && iaNode('Renamed information').type==='content' && !iaNode('Renamed information').includeInSitemap);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores the previous relationship and its inclusion',()=>iaNode('Renamed information').id===original.id && iaNode('Renamed information').path[0]===parent && !iaNode('Renamed information').includeInSitemap);
    iaSelect('Renamed information');d.getElementById('sitemap-delete').click();await wait();d.getElementById('sitemap-undo').click();await wait();
    test(mode+' delete and undo restore identity and exclusion',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap);
    const savedIa=evaluate('projectJson()');w.importConfig(JSON.parse(savedIa));await wait();
    test(mode+' IA identities and inclusion survive project JSON round trip',()=>iaNode('Renamed information').id===original.id && !iaNode('Renamed information').includeInSitemap && !iaFooterHas('Renamed information'));
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    iaChoice(parent).click();await wait();
    test(mode+' sitemap inclusion autosaves with the active project',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectId].data.designProcess.iaEntries[mode].some(node=>node.id===iaNode(parent).id && node.includeInSitemap===false));
    const exportDoc=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html');
    test(mode+' standalone HTML and inspector use the same selected sitemap',()=>exportDoc.querySelector('#sitemap').innerHTML===previewDoc().querySelector('#sitemap').innerHTML && ![...exportDoc.querySelectorAll('#sitemap a, #sitemap span')].some(el=>el.firstChild?.textContent===parent));
  }
  reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  iaChoice('Home').click();await wait();
  test('Explicit Home inclusion overrides the former Basic fixed omission',()=>iaFooterHas('Home') && iaNode('Home').includeInSitemap);
  iaChoice('Content card').click();await wait();d.getElementById('dockModeAdvanced').click();await wait();iaChoice('Brief lesson').click();await wait();d.getElementById('dockModeBasic').click();await wait();
  test('Sample switches preserve each sample inclusion choices',()=>!iaChoice('Content card').checked && w.DSStudio.process.currentPlan().iaEntries.advanced.some(node=>node.includeInSitemap===false));
  iaSelect('Components');input('sitemap-label','Teaching group');input('sitemap-type','group','change');d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Group type is a nonlinked heading with selected child destinations',()=>[...previewDoc().querySelectorAll('#sitemap .sitemap-list > li')].some(li=>li.querySelector(':scope > span')?.textContent==='Teaching group' && li.querySelector('ul a')) && iaNode('Teaching group').type==='group');
  const groupId=iaNode('Teaching group').id;iaChoice('Teaching group').click();await wait();iaSelect('Teaching group');input('sitemap-label','Renamed group');d.getElementById('sitemap-form').requestSubmit();await wait();
  test('Parent rename preserves its own identity and descendant exclusions',()=>iaNode('Renamed group').id===groupId && !iaNode('Renamed group').includeInSitemap && !iaNode('Content card').includeInSitemap && iaNode('Content card').path[0]==='Renamed group' && !iaFooterHas('Profile row'));
  for(const width of [320,390,1440]) {
    app.style.width=width+'px';w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    test('IA inclusion controls and both lesson views fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && [...d.querySelectorAll('#sitemap-editor select, #sitemap-editor input:not([type=checkbox]), #process-ia .process-sitemap-preview a')].every(el=>el.getBoundingClientRect().height>=44) && d.getElementById('sitemap-choices').scrollWidth<=d.getElementById('sitemap-choices').clientWidth+1 && [...d.querySelectorAll('#sitemap-choices label')].every(row=>row.getBoundingClientRect().height>=44) && ['.process-map','.process-sitemap-preview'].every(selector=>{const el=d.querySelector('#process-ia '+selector);return el.scrollWidth<=el.clientWidth+1;}));
  }
  app.style.width='1440px';reset();d.getElementById('dockModeBasic').click();
  const bulkIa=Array.from({length:64},(_,i)=>'Group '+i+' > Item '+i).join('\n');
  input('plan-pages',bulkIa);await wait();iaChoice('Item 63').click();await wait();
  test('Inclusion works for bounded legacy outlines without rewriting or truncating their lines',()=>evaluate('state.designProcess.pages')===bulkIa && iaNodes().length===128 && !iaNode('Item 63').includeInSitemap && iaNode('Item 63').path[0]==='Group 63');
  app.style.width='1440px';reset();await wait();
  const invalidIa=w.DSStudio.process.normalize({iaEntries:{basic:[{id:'ia-1',path:['Safe'],type:'<script>',includeInSitemap:false},{id:'ia-1',path:['Duplicate']},{id:'<img>',path:['Bad']},{id:'ia-2',path:['Too','Many','Nested','Levels']},{id:'ia-3',path:[null]}]}});
  test('Imported IA metadata validates identities, paths, types and duplicate IDs',()=>invalidIa.iaEntries.basic.length===1 && invalidIa.iaEntries.basic[0].type==='section' && invalidIa.iaEntries.basic[0].includeInSitemap===false);
  w.importConfig({sampleMode:'basic',designProcess:{pages:'Research <img src=x onerror=alert(1)',showPlanned:true,iaEntries:{basic:[{id:'ia-1',path:['Research <img src=x onerror=alert(1)'],type:'page',includeInSitemap:true}]}}});w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  test('Imported IA labels remain safe text in controls, full IA and sitemap',()=>!d.querySelector('#sitemap-choices img, #process-ia img, #process-ia script') && !previewDoc().querySelector('#sitemap img, #sitemap script') && d.getElementById('sitemap-choices').textContent.includes('<img') && previewDoc().querySelector('#sitemap').textContent.includes('<img'));
  evaluate('resetStudio()');await wait();
  test('Reset clears saved IA metadata and restores default sample inclusion',()=>!evaluate('state.designProcess.iaEntries.basic.length') && !evaluate('state.designProcess.iaEntries.advanced.length') && iaNodes().every(node=>node.includeInSitemap===(node.depth<3 && node.label!=='Home' && node.label!=='Footer')));

  // Three information levels retain a separate visitor sitemap in both samples.
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    const parent=mode==='basic'?'Components':'Design process',branch=mode==='basic'?'Profile row':'Project brief';
    const detail=mode==='basic'?'Availability status':'Purpose and audience';
    const sibling=mode==='basic'?'Name and role':'Scope and delivery';
    const target=mode==='basic'?'basic-layout':'brief-lab';
    const original=iaNodes().filter(node=>node.path.includes(branch)).map(node=>({id:node.id,label:node.label,include:node.includeInSitemap}));
    const sectionCount=previewDoc().querySelectorAll('main > section').length;
    test(mode+' sample includes excluded third-level content planning without invented links',()=>iaNode(detail).depth===3 && iaNode(detail).type==='content' && !iaNode(detail).includeInSitemap && !iaFooterHas(detail) && !d.querySelector('#process-ia .process-map a') && d.querySelector('#process-ia .process-map ul ul ul').textContent.length>0 && d.querySelector('#process-ia a[href="https://www.nngroup.com/articles/flat-vs-deep-hierarchy/"]'));
    iaChoice(detail).click();await wait();
    test(mode+' selected unlinked detail stays out of the visitor sitemap by default',()=>iaNode(detail).includeInSitemap && !iaFooterHas(detail));
    d.getElementById('sitemap-planned').click();await wait();
    test(mode+' planned detail appears at the correct third sitemap level as text',()=>[...previewDoc().querySelectorAll('#sitemap ul ul ul > li > span')].some(el=>el.firstChild.textContent===detail+' ') && ![...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent===detail));
    iaSelect(detail);input('sitemap-target',target,'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    const detailId=iaNode(detail).id;
    test(mode+' third-level destination uses an existing safe anchor in preview and export',()=>[...previewDoc().querySelectorAll('#sitemap ul ul ul a')].some(a=>a.textContent===detail && a.hash==='#'+target) && new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap ul ul ul a[href="#'+target+'"]') && previewDoc().querySelectorAll('main > section').length===sectionCount);
    iaChoice(parent).click();await wait();
    test(mode+' excluded ancestor suppresses third-level links while retaining choices',()=>iaChoice(detail).disabled && iaChoice(detail).checked && !iaFooterHas(detail));
    iaChoice(parent).click();await wait();iaChoice(branch).click();await wait();
    test(mode+' excluded immediate parent also suppresses the third level',()=>iaChoice(detail).disabled && iaChoice(detail).checked && !iaFooterHas(detail));
    iaChoice(branch).click();await wait();
    iaSelect(branch);
    test(mode+' branch parent options exclude descendants and fourth-level moves',()=>[...d.getElementById('sitemap-parent').options].every(option=>!option.textContent.includes(branch) && option.value.split(':').length<2));
    input('sitemap-label','Renamed branch');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' branch rename preserves every descendant identity and inclusion',()=>original.every(old=>iaNode(old.label===branch?'Renamed branch':old.label)?.id===old.id) && iaNode(detail).path[1]==='Renamed branch' && iaNode(detail).includeInSitemap && !iaNode(sibling).includeInSitemap && iaFooterHas(detail));
    const destination=mode==='basic'?'Layouts':'Lessons',dest=iaNode(destination);
    input('sitemap-parent',dest.position.join(':'),'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' moving a two-level branch retains third-level relationships and identities',()=>iaNode(detail).id===detailId && iaNode(detail).path.join(' / ')===destination+' / Renamed branch / '+detail && iaFooterHas(detail));
    iaSelect(detail);input('sitemap-label','Renamed detail');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' detail rename preserves its ID and explicit link mapping',()=>iaNode('Renamed detail').id===detailId && [...previewDoc().querySelectorAll('#sitemap a')].some(a=>a.textContent==='Renamed detail' && a.hash==='#'+target));
    iaSelect('Renamed detail');const orderBefore=iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',');
    d.getElementById(mode==='basic'?'sitemap-up':'sitemap-down').click();await wait();
    test(mode+' detail siblings reorder without losing their identities',()=>iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',')!==orderBefore && iaNode('Renamed detail').id===detailId);
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores third-level sibling order',()=>iaNodes().filter(node=>node.parentId===iaNode('Renamed detail').parentId).map(node=>node.id).join(',')===orderBefore);
    iaSelect('Renamed branch');const beforeDelete=evaluate('projectJson()');d.getElementById('sitemap-delete').click();await wait();
    test(mode+' deleting a branch removes all descendants from the plan',()=>!iaNode('Renamed branch') && !iaNode('Renamed detail') && !iaNode(sibling));
    d.getElementById('sitemap-undo').click();await wait();
    test(mode+' undo restores the complete three-level branch and metadata',()=>evaluate('projectJson()')===beforeDelete && iaNode('Renamed detail').id===detailId);
    const roundTrip=JSON.parse(evaluate('projectJson()'));w.importConfig(roundTrip);await wait();
    test(mode+' third-level identities and choices survive JSON import',()=>iaNode('Renamed detail').id===detailId && iaNode('Renamed detail').includeInSitemap && !iaNode(sibling).includeInSitemap && iaFooterHas('Renamed detail'));
    d.getElementById('jSaveLocal').click();const savedId=d.getElementById('jProjects').value;
    test(mode+' third-level paths and IDs persist in local project storage',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[savedId].data.designProcess.iaEntries[mode].some(node=>node.id===detailId && node.path.length===3));
    iaSelect('Renamed branch');const unchanged=evaluate('projectJson()');
    const forged=new w.Option('Invalid descendant',iaNode('Renamed detail').position.join(':'));d.getElementById('sitemap-parent').add(forged);input('sitemap-parent',forged.value,'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' forged cycle or fourth-level parent is rejected without changing saved data',()=>evaluate('projectJson()')===unchanged && d.getElementById('sitemap-status').textContent.includes('at most three'));
    d.getElementById('sitemap-new').click();input('sitemap-label','New planning detail');const newParent=iaNode(mode==='basic'?'Content card':'Information architecture');input('sitemap-parent',newParent.position.join(':'),'change');d.getElementById('sitemap-form').requestSubmit();await wait();
    test(mode+' adding a third-level item defaults to content excluded from the sitemap',()=>iaNode('New planning detail').depth===3 && iaNode('New planning detail').type==='content' && !iaNode('New planning detail').includeInSitemap);
  }
  reset();d.getElementById('dockModeBasic').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
  const oldTwoLevel=w.DSStudio.process.samplePages('basic').split('\n').filter(line=>line.split('>').length<=2).join('\n');
  w.importConfig({sampleMode:'basic',designProcess:{pages:oldTwoLevel,iaEntries:{basic:[{id:'ia-88',path:['Components','Profile row'],type:'section',includeInSitemap:false}]}}});await wait();
  test('Previous complete two-level samples gain planning details without losing saved IDs or exclusions',()=>iaNode('Profile row').id==='ia-88' && !iaNode('Profile row').includeInSitemap && iaNode('Availability status').depth===3 && iaChoice('Availability status').disabled && evaluate('state.designProcess.pages')===oldTwoLevel);
  const customThree='Services\nServices > Consultation\nServices > Consultation > Duration\nServices > Consultation > Price\nAbout';input('plan-pages',customThree);await wait();
  test('Raw third-level outlines share a single parent tree and remain custom across modes',()=>iaNodes().length===5 && w.DSStudio.process.tree(customThree)[0].children[0].children.length===2 && w.DSStudio.process.hierarchy(customThree)[0][1].length===1);
  d.getElementById('dockModeAdvanced').click();await wait();
  test('Sample switches preserve a custom three-level outline',()=>evaluate('DSStudio.process.currentPlan().pages')===customThree && iaNode('Duration').depth===3);
  input('plan-pages','Root > Branch > Detail > Too deep');await wait();
  test('Raw fourth-level lines are visibly flagged and excluded from rendered IA',()=>!d.getElementById('plan-pages').checkValidity() && d.getElementById('plan-sample-status').textContent.includes('three information levels') && iaNodes().length===0);
  const bulkThree=Array.from({length:64},(_,i)=>'Group '+i+' > Item '+i+' > Detail '+i).join('\n');input('plan-pages',bulkThree);await wait();iaChoice('Detail 63').click();await wait();
  test('Three-level legacy line limits retain all 192 derived entries and choices',()=>iaNodes().length===192 && evaluate('state.designProcess.pages')===bulkThree && iaNode('Detail 63').includeInSitemap && evaluate('state.designProcess.iaEntries.advanced.length')===192 && d.getElementById('plan-pages').checkValidity());
  input('plan-pages','Root > Branch > <img src=x onerror=alert(1)');await wait();
  test('Valid third-level hostile labels remain escaped text in the IA and editor',()=>iaNodes().length===3 && !d.querySelector('#process-ia img, #process-ia script, #sitemap-choices img') && d.querySelector('#process-ia .process-map').textContent.includes('<img src=x onerror=alert(1)') && d.getElementById('sitemap-choices').textContent.includes('<img') && !d.getElementById('plan-pages').validationMessage);
  const bounded=w.DSStudio.process.normalize({iaEntries:{basic:Array.from({length:200},(_,i)=>({id:'ia-'+(i+1),path:['Root '+i,'Branch','Detail'],type:'content',includeInSitemap:false}))}});
  test('Imported third-level metadata retains valid depth and a bounded 192-entry maximum',()=>bounded.iaEntries.basic.length===192 && bounded.iaEntries.basic.every(node=>node.path.length===3 && !node.includeInSitemap));
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(1);revealDestinationPlan();await wait();
    for(const width of [320,390,1440]) {
      app.style.width=width+'px';await wait();
      test(mode+' '+theme+' third-level IA fits '+width+'px with usable controls',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && d.getElementById('sitemap-choices').scrollWidth<=d.getElementById('sitemap-choices').clientWidth+1 && d.getElementById('sitemap-items').scrollWidth<=d.getElementById('sitemap-items').clientWidth+1 && [...d.querySelectorAll('#sitemap-choices .is-grandchild')].every(el=>el.getBoundingClientRect().height>=44) && ['.process-map','.process-sitemap-preview'].every(selector=>{const el=d.querySelector('#process-ia '+selector);return el.scrollWidth<=el.clientWidth+1;}));
    }
  }
  app.style.width='1440px';reset();await wait();

  // Complete content inventory, independent destination references and deep editing.
  {
  await w.DSStudio.ready;
  d.getElementById('sitemap-destination-editor').open=false;
  const model=w.DSStudio.contentArchitecture;
  const contentNodes=()=>model.nodes();
  const contentNode=(label,value)=>contentNodes().find(node=>node.type!=='link' && node.label===label && (value===undefined || node.value===value))||contentNodes().find(node=>node.label===label && (value===undefined || node.value===value));
  const selectContent=id=>{const button=d.querySelector('[data-content-id="'+id+'"]');let ancestor=button.parentElement;while(ancestor){if(ancestor.tagName==='DETAILS')ancestor.open=true;ancestor=ancestor.parentElement;}button.click();};
  const saveContent=async()=>{d.getElementById('ia-form').requestSubmit();await wait();};
  test('Content outline starts without runtime errors',()=>!w.__reviewErrors.length && d.getElementById('ia-content-editor') && !d.getElementById('sitemap-destination-editor').open);
  for(const mode of ['basic','advanced']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
    const nodes=contentNodes(),header=contentNode('Header'),home=contentNode('Home'),hero=nodes.find(node=>node.parentId===home.id && node.label==='Hero');
    test(mode+' inventories actual shared header, hero, footer and deep content',()=>nodes.length>100 && nodes.length<=1000 && header.type==='region' && contentNode('Footer').type==='region' && hero && nodes.some(node=>model.path(nodes,node).length>3));
    test(mode+' inventory contains actual heading, logo, wordmark, image alternative text and CTA wording',()=>contentNode('Wordmark').value===evaluate('state.project') && contentNode('Logo') && nodes.some(node=>node.label==='Heading' && node.value===(mode==='basic'?'Start with the essentials.':'A better web starts with one good decision.')) && contentNode('Alternative text') && nodes.some(node=>node.label==='Primary CTA' && node.value===(mode==='basic'?'Explore components':'Find your first lesson')));
    if(mode==='advanced')test('Numeric progress controls are captured as safe text values',()=>nodes.some(node=>node.type==='field' && node.value==='3' && node.label.includes('Practice checklist')));
    const nav=nodes.find(node=>node.label==='Main navigation' && node.parentId===header.id);
    const homeRef=nodes.find(node=>node.parentId===nav.id && node.label==='Home');
    test(mode+' navigation references canonical destinations without duplicating their content',()=>homeRef.type==='link' && homeRef.target==='home' && homeRef.reference==='#home' && nodes.filter(node=>node.target==='home' && node.type!=='link').length===1 && !nodes.some(node=>node.parentId===homeRef.id));
    test(mode+' every authored sitemap destination has exactly one canonical content entry',()=>w.DSStudio.process.inventory(mode).every(([,id])=>nodes.filter(node=>node.target===id && node.type!=='link').length===1));
    test(mode+' native outline starts collapsed and center/export content roles remain safe text',()=>[...d.querySelectorAll('#ia-outline details')].every(el=>!el.open) && d.querySelectorAll('#process-ia .ia-content-map details').length>10 && !d.querySelector('#process-ia .ia-content-map img, #process-ia .ia-content-map script'));
    input('ia-search','alternative text');await wait();
    test(mode+' search reveals matching deep content and ancestor context',()=>d.getElementById('ia-count').textContent.includes('matching') && [...d.querySelectorAll('#ia-outline details')].some(el=>el.open) && d.getElementById('ia-outline').textContent.includes('Alternative text'));
    input('ia-search','');d.getElementById('ia-collapse').click();
    const heading=nodes.find(node=>node.type==='text' && node.label==='Heading' && model.path(nodes,node).includes('Hero'));
    const beforeBody=previewDoc().getElementById('hero-title').textContent,beforeFooter=previewDoc().querySelector('#sitemap').innerHTML;
    selectContent(heading.id);input('ia-draft','A proposed new heading');input('ia-notes','Confirm with the project owner');input('ia-status','planned','change');await saveContent();
    test(mode+' planned content saves alongside current source content without rewriting the sample',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && contentNodes().find(node=>node.id===heading.id).value===beforeBody && previewDoc().getElementById('hero-title').textContent===beforeBody && previewDoc().querySelector('#sitemap').innerHTML===beforeFooter && d.getElementById('ia-actual').value===beforeBody);
    input('ia-draft','');await saveContent();
    test(mode+' an explicitly empty draft is retained',()=>contentNodes().find(node=>node.id===heading.id).draft==='');
    d.getElementById('ia-undo').click();await wait();
    test(mode+' undo restores planned wording',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading');
    const project=JSON.parse(evaluate('projectJson()'));w.importConfig(project);await wait();
    test(mode+' JSON round trip retains content identities, notes and draft separately from actual content',()=>contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && contentNodes().find(node=>node.id===heading.id).notes==='Confirm with the project owner' && contentNodes().find(node=>node.id===heading.id).value===beforeBody);
    d.getElementById('jSaveLocal').click();const projectId=d.getElementById('jProjects').value;
    test(mode+' local save contains full content planning data',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[projectId].data.designProcess.contentPlan[mode].some(node=>node.id===heading.id && node.draft==='A proposed new heading'));
    const fileJson=evaluate('projectJson()'),fileTransfer=new w.DataTransfer(),fileAlerts=[],previousAlert=w.alert;
    w.alert=message=>fileAlerts.push(message);fileTransfer.items.add(new w.File([fileJson],'content-plan.json',{type:'application/json'}));d.getElementById('loadFile').files=fileTransfer.files;
    // The file contains the current plan: equality alone cannot prove the file read
    // finished. Await import completion before deleting any planning branches.
    let fileImportCompleted=false;
    await new Promise((resolve,reject)=>{
      const imported=()=>{fileImportCompleted=true;w.clearTimeout(timeout);resolve();};
      const timeout=w.setTimeout(()=>{d.removeEventListener('dss:imported',imported);reject(new Error('Content-plan file import did not complete: '+fileAlerts.join('; ')));},3000);
      d.addEventListener('dss:imported',imported,{once:true});
      d.getElementById('loadFile').dispatchEvent(new w.Event('change',{bubbles:true}));
    });await wait();w.alert=previousAlert;
    test(mode+' actual exported JSON file reimports through Load JSON with the complete content plan',()=>fileImportCompleted && !fileAlerts.length && contentNodes().find(node=>node.id===heading.id).draft==='A proposed new heading' && evaluate('projectJson()')===fileJson);
    selectContent(header.id);d.getElementById('ia-delete').click();await wait();
    test(mode+' removing the header planning branch does not remove Home from sitemap or page',()=>!contentNode('Header') && previewDoc().querySelector('#sitemap').innerHTML===beforeFooter && previewDoc().getElementById('home'));
    d.getElementById('ia-undo').click();await wait();
    test(mode+' branch deletion undo restores all descendant identities',()=>contentNode('Header').id===header.id && contentNodes().some(node=>node.id===homeRef.id));
    selectContent(homeRef.id);
    test(mode+' navigation references do not offer separate sitemap membership',()=>d.getElementById('ia-manage-sitemap').disabled && d.getElementById('ia-sitemap-summary').textContent.includes('do not have separate sitemap membership'));
    selectContent(home.id);d.getElementById('ia-manage-sitemap').click();await wait();
    test(mode+' canonical section reaches its matching eyebrow sitemap inclusion control',()=>d.activeElement.dataset.sectionId==='home' && d.getElementById('sitemap-destination-editor').hidden);
    selectContent(hero.id);d.getElementById('ia-add-child').click();input('ia-label','New content group');input('ia-type','group','change');await saveContent();
    const newGroup=contentNode('New content group');
    test(mode+' add child retains the selected container relationship',()=>newGroup.parentId===hero.id && newGroup.status==='planned');
    d.getElementById('ia-add-child').click();input('ia-label','New text');input('ia-draft','Actual planned copy');await saveContent();const child=contentNode('New text');
    selectContent(newGroup.id);input('ia-label','Renamed content group');input('ia-parent',header.id,'change');await saveContent();
    test(mode+' rename and reparent preserve descendant identities and planned copy',()=>contentNode('Renamed content group').id===newGroup.id && contentNode('Renamed content group').parentId===header.id && contentNode('New text').id===child.id && contentNode('New text').parentId===newGroup.id && contentNode('New text').draft==='Actual planned copy');
    const unchanged=evaluate('projectJson()'),forged=new w.Option('Cycle',child.id);d.getElementById('ia-parent').add(forged);input('ia-parent',child.id,'change');await saveContent();
    test(mode+' forged cyclic reparent does not mutate saved content',()=>evaluate('projectJson()')===unchanged && d.getElementById('ia-status-message').textContent.includes('outside this branch'));
    selectContent(child.id);d.getElementById('ia-add-sibling').click();input('ia-label','Second text');await saveContent();
    const siblingsBefore=contentNodes().filter(node=>node.parentId===newGroup.id).map(node=>node.id).join(',');d.getElementById('ia-up').click();await wait();
    test(mode+' sibling reorder preserves the whole branch and changes order',()=>contentNodes().filter(node=>node.parentId===newGroup.id).map(node=>node.id).join(',')!==siblingsBefore && contentNode('New text').id===child.id);
    const footerBeforeRestore=previewDoc().querySelector('#sitemap').innerHTML;d.getElementById('ia-restore').click();await wait();
    test(mode+' restoring sample inventory clears only that sample content edits and retains sitemap',()=>!contentNode('Renamed content group') && previewDoc().querySelector('#sitemap').innerHTML===footerBeforeRestore && evaluate('state.designProcess.contentPlan.'+mode)===null);
    d.getElementById('ia-undo').click();await wait();
    test(mode+' restore can be undone',()=>contentNode('Renamed content group').id===newGroup.id);
    const paragraphs=contentNodes().filter(node=>node.label==='Paragraph');
    selectContent(paragraphs[0].id);input('ia-notes','Repeated role labels use separate identities');await saveContent();
    test(mode+' repeated paragraph role labels remain independently editable',()=>contentNodes().find(node=>node.id===paragraphs[0].id).notes==='Repeated role labels use separate identities' && contentNodes().find(node=>node.id===paragraphs[1].id).notes!== 'Repeated role labels use separate identities');
  }
  reset();d.getElementById('dockModeBasic').click();await wait();
  selectContent(contentNode('Wordmark').id);input('ia-notes','Basic only');await saveContent();d.getElementById('dockModeAdvanced').click();await wait();
  test('Sample switches retain independent content plans',()=>!contentNode('Wordmark').notes);d.getElementById('dockModeBasic').click();await wait();
  test('Switching back restores the saved content plan',()=>contentNode('Wordmark').notes==='Basic only');
  input('jProject','Renamed live project');await wait();
  test('Current content refreshes from authored source while preserving planned notes and IDs',()=>contentNode('Wordmark').value==='Renamed live project' && contentNode('Wordmark').notes==='Basic only');
  reset();await wait();const invalidContentConfig=JSON.parse(evaluate('projectJson()'));invalidContentConfig.advanced.state='invalid';w.importConfig(invalidContentConfig);await wait();
  test('Advanced-only state changes refresh actual source feedback rather than reusing stale cached text',()=>contentNodes().some(node=>node.value==='Enter an email address in the format name@example.com.'));
  w.importConfig({sampleMode:'basic',designProcess:{pages:'Home\nHome > Future content\nFuture destination',iaEntries:{basic:[{id:'ia-77',path:['Home'],type:'section',includeInSitemap:false}]}}});await wait();
  test('Previous custom plans migrate into the content structure without losing destination choices',()=>contentNode('Future content') && contentNode('Future destination') && contentNode('Home').id==='content-legacy-ia-77' && contentNodes().filter(node=>node.target==='home' && node.type!=='link').length===1 && !w.DSStudio.process.entries().find(node=>node.label==='Home').includeInSitemap);
  const deep=Array.from({length:12},(_,i)=>({id:'content-depth-'+i,parentId:i?'content-depth-'+(i-1):null,label:'Level '+(i+1),type:i===11?'text':'group',draft:i===11?'Twelve levels of useful content':null,status:'planned'}));
  w.importConfig({sampleMode:'basic',designProcess:{contentPlan:{basic:deep}}});w.dssShowWizardStep(1);await wait();
  test('Content structures support twelve levels independently from the destination outline',()=>contentNodes().length===12 && model.path(contentNodes(),contentNode('Level 12')).length===12 && d.querySelectorAll('#ia-outline details').length===11);
  selectContent(contentNode('Level 12').id);test('Depth limit disables adding a child at the boundary',()=>d.getElementById('ia-add-child').disabled);
  const unsafe=[{id:'content-safe',parentId:null,label:'<img src=x onerror=alert(1)>',type:'text',draft:'<script>alert(1)<\/script>',notes:'<svg onload=alert(1)>',status:'planned',target:'javascript:alert(1)'},{id:'content-cycle-a',parentId:'content-cycle-b',label:'Cycle A'},{id:'content-cycle-b',parentId:'content-cycle-a',label:'Cycle B'},{id:'content-safe',label:'Duplicate'}];
  const sanitized=model.normalizeNodes(unsafe,'basic');
  test('Content imports validate identities, targets and cycles',()=>sanitized.length===1 && !sanitized[0].target && sanitized[0].label.includes('<img'));
  w.importConfig({sampleMode:'advanced',designProcess:{contentPlan:{advanced:unsafe}}});await wait();
  test('Hostile content labels, drafts and notes stay inert in controls and exported artifacts',()=>!d.querySelector('#ia-content-editor img, #ia-content-editor script, #process-ia .ia-content-map img, #process-ia .ia-content-map svg') && d.getElementById('ia-outline').textContent.includes('<script>') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#ia-lab .ia-content-map img, #ia-lab .ia-content-map script'));
  const oversized=Array.from({length:1010},(_,i)=>({id:'content-bound-'+i,label:'Node '+i,parentId:null,type:'text'}));test('Content imports bound inventory size',()=>model.normalizeNodes(oversized,'basic').length===1000);
  const textHeavy=model.normalizeNodes(Array.from({length:1000},(_,i)=>({id:'content-heavy-'+i,label:'Large '+i,value:'x'.repeat(2400),draft:'y'.repeat(2400),notes:'z'.repeat(1200)})),'basic');
  test('Content imports bound aggregate plan data as well as individual values',()=>textHeavy.length>0 && textHeavy.length<1000 && JSON.stringify(textHeavy).length<=model.MAX_PLAN_CHARS);
  for(const mode of ['basic','advanced'])for(const theme of ['light','dark']) {
    reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();w.dssShowWizardStep(1);await wait();d.getElementById('ia-expand').click();d.querySelectorAll('.ia-editor-disclosure').forEach(el=>el.open=true);
    for(const width of [320,390,1440]) {app.style.width=width+'px';await wait();
      test(mode+' '+theme+' deep outline and content controls fit '+width+'px',()=>d.documentElement.scrollWidth<=w.innerWidth+1 && d.getElementById('ia-outline').scrollWidth<=d.getElementById('ia-outline').clientWidth+1 && [...d.querySelectorAll('#ia-content-editor input:not([type=checkbox]), #ia-content-editor select, #ia-content-editor textarea, #ia-content-editor button')].every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.right<=d.getElementById('ia-content-editor').getBoundingClientRect().right+1;}) && !w.__reviewErrors.length);
    }
  }
  app.style.width='1440px';reset();await wait();
  }

  // Eyebrow sitemap: shared visible labels, real destinations and saved configuration.
  {
    const sectionModel=w.DSStudio.sectionSitemap;
    const changeSource=value=>{const control=d.getElementById('sitemap-source');control.value=value;control.dispatchEvent(new w.Event('change',{bubbles:true}));};
    const chooseSection=(id,checked)=>{const control=[...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===id);control.checked=checked;control.dispatchEvent(new w.Event('change',{bubbles:true}));};
    const mapLinks=()=>[...previewDoc().querySelectorAll('#sitemap a')];
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const rows=sectionModel.nodes(),body=previewDoc(),beforeContent=JSON.stringify(w.DSStudio.contentArchitecture.nodes());
      test(mode+' defaults to page labels and keeps detailed content structure',()=>sectionModel.source()==='sections' && d.getElementById('sitemap-source').value==='sections' && d.getElementById('sitemap-destination-editor').hidden && d.getElementById('sitemap-outline-editor').hidden && w.DSStudio.contentArchitecture.nodes().length>100);
      test(mode+' every sitemap label and destination matches a visible eyebrow or heading',()=>rows.length>10 && rows.every(node=>{const target=body.getElementById(node.id);return target && [...target.querySelectorAll('.eyebrow,.sample-eyebrow,h1,h2,h3,h4,h5,h6,legend'),target].some(el=>el.textContent.replace(/\s+/g,' ').trim()===node.label);}) && mapLinks().map(a=>a.hash.slice(1)).join(',')===rows.map(node=>node.id).join(',') && mapLinks().every((a,i)=>a.textContent===rows[i].label));
      test(mode+' sitemap follows container ancestry and keeps slash labels whole',()=>rows.some(node=>node.id==='home' && !node.parentId) && rows.every(node=>!node.parentId || body.getElementById(node.parentId).contains(body.getElementById(node.id))) && !rows.some(node=>node.id==='footer'));
      test(mode+' preview proxies and exported fragment links share the same labels',()=>{const exported=new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html'),proxies=[...d.querySelectorAll('.process-sitemap-preview a[data-sitemap-target]')];return proxies.length===rows.length && proxies.every((a,i)=>a.hash==='#previewShell' && a.dataset.sitemapTarget===rows[i].id && a.textContent===rows[i].label) && [...exported.querySelectorAll('#sitemap a')].every((a,i)=>a.hash==='#'+rows[i].id && a.textContent===rows[i].label && exported.querySelectorAll('[id="'+rows[i].id+'"]').length===1);});
      if(mode==='basic') {
        test('Basic sitemap root labels match the four section eyebrows',()=>rows.filter(node=>!node.parentId).map(node=>node.label).join('|')==='HTML & CSS essentials|Components / Flexbox|Layouts / CSS Grid|Forms / Labels & controls');
        test('Basic component eyebrows and list heading fallbacks remain correctly nested',()=>rows.find(node=>node.id==='basic-structure').label==='Article / Content card' && rows.find(node=>node.id==='basic-structure').parentId==='features' && rows.find(node=>node.id==='list-collection').label==='Unordered list' && rows.find(node=>node.id==='list-collection').parentId==='lists');
      }
      const parent=mode==='basic'?'features':'components',child=mode==='basic'?'basic-structure':'component-actions';
      chooseSection(child,false);chooseSection(parent,false);await wait();
      test(mode+' excluding a parent suppresses its branch without changing content',()=>!mapLinks().some(a=>a.hash==='#'+parent || a.hash==='#'+child) && [...d.querySelectorAll('#section-sitemap-choices input')].find(el=>el.dataset.sectionId===child).disabled && JSON.stringify(w.DSStudio.contentArchitecture.nodes())===beforeContent);
      const canonical=w.DSStudio.contentArchitecture.nodes().find(node=>node.target===child && node.type!=='link'),select=d.querySelector('[data-content-id="'+canonical.id+'"]');
      for(let ancestor=select.parentElement;ancestor;ancestor=ancestor.parentElement)if(ancestor.tagName==='DETAILS')ancestor.open=true;
      select.click();d.getElementById('ia-manage-sitemap').click();
      test(mode+' configuring an excluded child focuses the parent that must be enabled first',()=>d.activeElement.dataset.sectionId===parent);
      chooseSection(parent,true);await wait();
      test(mode+' re-including a parent retains independent child exclusions',()=>mapLinks().some(a=>a.hash==='#'+parent) && !mapLinks().some(a=>a.hash==='#'+child));
      d.getElementById('jSaveLocal').click();const sectionProjectId=d.getElementById('jProjects').value;
      chooseSection('home',false);await wait();
      test(mode+' section inclusion autosaves to the active project',()=>JSON.parse(w.localStorage.getItem('dss-v27-projects'))[sectionProjectId].data.designProcess.sitemapExcluded[mode].includes('home'));
      chooseSection('home',true);await wait();
      const config=evaluate('projectJson()');evaluate('importConfig('+config+')');await wait();
      test(mode+' section choices round trip through project JSON',()=>evaluate('state.designProcess.sitemapExcluded.'+mode).join(',')===child && !mapLinks().some(a=>a.hash==='#'+child));
      d.getElementById('section-sitemap-restore').click();await wait();
      test(mode+' Include all sections restores the current sample',()=>mapLinks().length===rows.length);
      evaluate('state.designProcess.goal="Keep this unrelated brief edit";apply()');
      d.getElementById('section-sitemap-undo').click();await wait();
      test(mode+' sitemap undo retains later brief changes',()=>evaluate('state.designProcess.goal')==='Keep this unrelated brief edit');
      test(mode+' section configuration undo restores exclusions',()=>!mapLinks().some(a=>a.hash==='#'+child));
      changeSource('custom');await wait();
      test(mode+' custom source reveals compatible destination controls',()=>!d.getElementById('sitemap-destination-editor').hidden && !d.getElementById('sitemap-outline-editor').hidden && d.getElementById('section-sitemap-settings').hidden);
      changeSource('sections');d.getElementById('section-sitemap-restore').click();await wait();
      const proxy=d.querySelector('.process-sitemap-preview [data-sitemap-target="'+parent+'"]');proxy.click();await wait();
      test(mode+' eyebrow sitemap preview link focuses the actual page section',()=>previewDoc().activeElement.id===parent);
      for(const theme of ['light','dark']) {
        if(d.documentElement.dataset.theme!==theme)d.getElementById('themeToggle').click();
        for(const width of [320,390,1440]) {
          app.style.width=width+'px';w.dssShowWizardStep(1);await wait();
          test(mode+' '+theme+' eyebrow sitemap controls fit '+width+'px',()=>{const editor=d.getElementById('section-sitemap-editor'),box=editor.getBoundingClientRect();return d.documentElement.scrollWidth<=w.innerWidth+1 && [...editor.querySelectorAll('select,button,#section-sitemap-choices label')].filter(el=>el.getBoundingClientRect().width>0).every(el=>{const b=el.getBoundingClientRect();return b.height>=44 && b.right<=box.right+1;});});
        }
      }
    }
    app.style.width='1440px';reset();await wait();
    w.importConfig({sampleMode:'basic',designProcess:{sitemapSource:{basic:'sections',advanced:'sections'},sitemapExcluded:{basic:['home','features','lists','signup'],advanced:['about']}}});await wait();
    test('An empty section sitemap explains its selection state and retains website content',()=>!mapLinks().length && previewDoc().querySelector('#sitemap').textContent.includes('No sections selected') && previewDoc().querySelectorAll('main > section').length===4);
    d.getElementById('section-sitemap-restore').click();await wait();
    test('Restoring Basic section choices retains Advanced choices',()=>evaluate('state.designProcess.sitemapExcluded.basic').length===0 && evaluate('state.designProcess.sitemapExcluded.advanced').join(',')==='about');
    d.getElementById('dockModeAdvanced').click();await wait();
    test('Mode switches apply the matching saved section choices',()=>!mapLinks().some(a=>a.hash==='#about') && mapLinks().some(a=>a.hash==='#home'));
    d.getElementById('dockModeBasic').click();await wait();
    test('Returning to Basic restores its complete section sitemap',()=>mapLinks().length===12);
    const fixture='<main><section id="features"><p class="eyebrow">Components / Flexbox</p><article id="basic-structure"><p class="eyebrow">Repeated &amp; safe</p></article><article id="basic-layout"><h3>Repeated &amp; safe</h3></article></section><section id="lists"><article id="list-collection"><p class="eyebrow">Child only</p></article></section></main>';
    const collected=sectionModel.collect(fixture,'basic');
    test('Section collector preserves duplicate label identities and does not borrow child eyebrows',()=>collected.length===4 && collected[1].label===collected[2].label && collected[1].id!==collected[2].id && !collected.some(node=>node.id==='lists') && collected.find(node=>node.id==='list-collection').parentId===null);
    w.importConfig({sampleMode:'basic',designProcess:{sitemapSource:{basic:'malicious'},sitemapExcluded:{basic:['features','features','javascript:alert(1)','missing']}}});await wait();
    test('Imported sitemap source and exclusions use bounded fixed values',()=>evaluate('state.designProcess.sitemapSource.basic')==='auto' && evaluate('state.designProcess.sitemapExcluded.basic').join(',')==='features');
    w.importConfig({sampleMode:'basic',designProcess:{pages:'Home\nCustom > Content card',pageLinks:{basic:{Custom:'features'}}}});await wait();
    test('Older custom outlines retain their navigation until switched explicitly',()=>sectionModel.source()==='custom' && mapLinks().some(a=>a.textContent==='Custom'));
    const customBefore=evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.contentPlan])');changeSource('sections');await wait();
    test('Switching an old plan to page labels preserves its saved plan and content',()=>mapLinks().some(a=>a.textContent==='Components / Flexbox') && evaluate('JSON.stringify([state.designProcess.pages,state.designProcess.pageLinks,state.designProcess.contentPlan])')===customBefore);
    evaluate('state.project="<img src=x onerror=alert(1)> & Safe";state.sampleMode="advanced";state.designProcess.sitemapSource.advanced="sections";apply()');await wait();
    test('Dynamic eyebrow text stays escaped in sitemap controls, preview and exports',()=>mapLinks().some(a=>a.textContent.includes('<img')) && !previewDoc().querySelector('#sitemap img') && !d.querySelector('#section-sitemap-choices img') && !new w.DOMParser().parseFromString(evaluate('htmlExport()'),'text/html').querySelector('#sitemap img'));
    reset();await wait();
  }

  // Student content planning: understand the item, propose content, save and review.
  {
    const model=w.DSStudio.contentArchitecture,rows=()=>model.nodes();
    const select=id=>{const button=d.querySelector('[data-content-id="'+id+'"]');for(let parent=button.parentElement;parent;parent=parent.parentElement)if(parent.tagName==='DETAILS')parent.open=true;button.click();};
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const heading=rows().find(node=>node.label==='Heading'),home=rows().find(node=>node.label==='Home' && node.type!=='link');select(heading.id);
      test(mode+' selected content identifies the item and teaches its properties',()=>d.getElementById('ia-selected-name').textContent===heading.label && d.getElementById('ia-current-path').textContent.startsWith('Location: ') && d.getElementById('ia-origin').textContent==='From the sample website' && d.getElementById('ia-actual-label').textContent==='In the sample (read only)' && d.getElementById('ia-type-help').textContent.includes('words') && d.getElementById('ia-actual').readOnly && d.getElementById('ia-actual').value===heading.value);
      test(mode+' content planning uses three clearly named stages and an explicit sample boundary',()=>d.querySelector('#ia-form legend').textContent==='1. Understand this item' && d.getElementById('ia-plan-heading').textContent==='2. Develop the content plan' && d.getElementById('ia-save-heading').textContent==='3. Save and review' && d.getElementById('ia-plan-boundary').textContent.includes('does not replace') && d.getElementById('ia-draft-label').textContent==='Proposed wording');
      const before=evaluate('projectJson()');input('ia-draft','A clear introduction for our learners');input('ia-notes','Purpose: introduce the course. Owner: course tutor. Next action: review with a beginner.');input('ia-status','needs-content','change');
      test(mode+' content edits stay in the form until saved and are clearly marked',()=>evaluate('projectJson()')===before && d.getElementById('ia-has-draft').checked && d.getElementById('ia-edit-state').textContent.includes('Unsaved edits') && !d.getElementById('ia-discard').disabled);
      d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' save retains the proposed wording, readiness and next action separately from the sample',()=>{const node=rows().find(node=>node.id===heading.id);return node.draft==='A clear introduction for our learners' && node.notes.includes('Owner: course tutor') && node.status==='needs-content' && node.value===heading.value && d.getElementById('ia-actual').value===heading.value && d.getElementById('ia-edit-state').textContent.includes('saved plan') && d.getElementById('ia-discard').disabled && d.activeElement===d.getElementById('ia-save') && d.getElementById('ia-outline').textContent.includes(node.draft) && d.getElementById('ia-outline').textContent.includes('Needs content or revision') && d.querySelector('#process-ia .ia-content-map').textContent.includes('Needs content or revision');});
      const savedPlan=evaluate('projectJson()');input('ia-label','Unsaved name');input('ia-type','image','change');input('ia-draft','Unsaved image brief');
      test(mode+' changing content kind explains the matching planning task',()=>d.getElementById('ia-draft-label').textContent==='Image brief' && d.getElementById('ia-draft-help').textContent.includes('text alternative') && d.getElementById('ia-example').textContent.includes('photograph') && d.getElementById('ia-type-help').textContent.includes('visual asset'));
      d.getElementById('ia-discard').click();
      test(mode+' discarding form edits restores saved properties and proposal without changing the project',()=>evaluate('projectJson()')===savedPlan && d.getElementById('ia-label').value===heading.label && d.getElementById('ia-type').value===heading.type && d.getElementById('ia-draft').value==='A clear introduction for our learners' && d.getElementById('ia-draft-label').textContent==='Proposed wording' && d.getElementById('ia-discard').disabled && d.activeElement===d.getElementById('ia-save'));
      input('ia-draft','');d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' deliberately blank proposals are explained and saved distinctly',()=>rows().find(node=>node.id===heading.id).draft==='' && d.getElementById('ia-proposal-state').textContent.includes('intentionally blank'));
      d.getElementById('ia-has-draft').click();d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' no proposal retains notes and uses the original sample as the starting point',()=>rows().find(node=>node.id===heading.id).draft===null && rows().find(node=>node.id===heading.id).notes.includes('Owner: course tutor') && d.getElementById('ia-proposal-state').textContent.includes('No proposed replacement'));
      for(const [kind,label]of [['image','Image brief'],['link','Proposed link wording'],['field','Proposed label or instructions'],['group','What this area needs']]) {
        const node=rows().find(node=>node.type===kind);select(node.id);
        test(mode+' '+kind+' items show a relevant planning prompt and example',()=>d.getElementById('ia-draft-label').textContent===label && d.getElementById('ia-example').textContent.length>40 && d.getElementById('ia-type-help').textContent.length>40);
      }
      select(home.id);d.getElementById('ia-add-child').click();
      test(mode+' adding inside explains a new planning item and retains the chosen parent',()=>d.getElementById('ia-selected-name').textContent==='New planning item' && d.getElementById('ia-origin').textContent.includes('not added to the sample') && d.getElementById('ia-parent').value===home.id && d.getElementById('ia-edit-state').textContent.includes('New item'));
      input('ia-label','Audience introduction');input('ia-draft','Explain who this course is for.');d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' a new item saves within its chosen container and stays explicitly planned',()=>rows().some(node=>node.label==='Audience introduction' && node.parentId===home.id && node.status==='planned' && node.draft==='Explain who this course is for.') && d.getElementById('ia-origin').textContent.includes('not added to the sample') && d.getElementById('ia-actual-label').textContent==='Recorded content (read only)');
    }
    w.importConfig({sampleMode:'basic',designProcess:{contentPlan:{basic:[{id:'content-unsafe-name',label:'<img src=x onerror=alert(1)>',type:'text',draft:'<svg onload=alert(1)>',notes:'<script>unsafe<\/script>'}]}}});w.dssShowWizardStep(1);await wait();
    test('Student item summaries render imported names and proposals as inert text',()=>d.getElementById('ia-selected-name').textContent.includes('<img') && d.getElementById('ia-draft').value.includes('<svg') && !d.querySelector('#ia-form img, #ia-form svg, #ia-form script'));
    app.style.width='1440px';reset();await wait();
  }

  // Content properties and planning disclosures remain independently collapsible.
  {
    for(const mode of ['basic','advanced']) {
      reset();d.getElementById(mode==='basic'?'dockModeBasic':'dockModeAdvanced').click();w.dssShowWizardStep(1);await wait();
      const properties=d.getElementById('ia-properties'),plan=d.getElementById('ia-content-plan'),summary=properties.querySelector('summary'),planSummary=plan.querySelector('summary');
      test(mode+' content properties and content plan start collapsed with semantic labels',()=>!properties.open && !plan.open && summary.textContent==='Selected content properties' && planSummary.textContent==='2. Develop the content plan' && d.getElementById('ia-selected-name').getBoundingClientRect().height>0);
      const before=evaluate('projectJson()');
      d.querySelector('[data-content-id]').click();
      test(mode+' selecting content keeps disclosures closed and focuses the properties summary',()=>!properties.open && !plan.open && d.activeElement===summary);
      summary.click();
      test(mode+' opening properties leaves the content plan collapsed',()=>properties.open && !plan.open);
      planSummary.click();summary.click();
      test(mode+' opening the plan and closing properties are independent and do not change project data',()=>!properties.open && plan.open && evaluate('projectJson()')===before);
      input('ia-draft','A proposal retained while collapsed');planSummary.click();
      test(mode+' collapsing the plan retains unsaved values and keeps save feedback visible',()=>!plan.open && d.getElementById('ia-draft').value==='A proposal retained while collapsed' && !d.getElementById('ia-discard').disabled && d.getElementById('ia-save').getBoundingClientRect().height>=44 && evaluate('projectJson()')===before);
      d.getElementById('ia-form').requestSubmit();await wait();
      test(mode+' saving from collapsed disclosures retains their state and saves the proposal',()=>!properties.open && !plan.open && w.DSStudio.contentArchitecture.nodes().some(node=>node.draft==='A proposal retained while collapsed'));
      summary.click();d.querySelector('[data-content-id]').click();evaluate('apply()');
      test(mode+' selection and ordinary rendering preserve chosen disclosure states',()=>properties.open && !plan.open);
      summary.click();d.getElementById('ia-add-root').click();
      test(mode+' adding an item opens properties and focuses its required name',()=>properties.open && !plan.open && d.activeElement===d.getElementById('ia-label'));
      summary.click();d.getElementById('ia-form').requestSubmit();
      test(mode+' validation reveals a required field inside collapsed properties',()=>properties.open && !plan.open && d.activeElement===d.getElementById('ia-label') && !d.getElementById('ia-label').validity.valid);
      d.dispatchEvent(new w.Event('dss:imported'));await wait();
      test(mode+' importing returns both content disclosures to collapsed',()=>!properties.open && !plan.open);
      for(const width of [320,390,1440]) {
        app.style.width=width+'px';await wait();
        test(mode+' collapsed content summaries fit and retain touch targets at '+width+'px',()=>[summary,planSummary].every(el=>{const box=el.getBoundingClientRect();return box.height>=44 && box.left>=0 && box.right<=w.innerWidth+1;}) && d.documentElement.scrollWidth<=w.innerWidth+1);
      }
    }
    app.style.width='1440px';reset();await wait();
  }

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
                                  # The content-outline matrix reached 1990 checks at 135s;
                                  # leave bounded headroom for its remaining fixtures.
                                  '--user-data-dir=' + profile, '--virtual-time-budget=150000',
                                  '--dump-dom', f'http://127.0.0.1:{server.server_port}/__review__'],
                                 # The expanded matrix approached five minutes on Windows.
                                 capture_output=True, encoding='utf-8', errors='replace', timeout=360)
            match = re.search(r'<pre id="results">(.*?)</pre>', run.stdout, re.S)
            if not match or match[1] == 'RUNNING':
                progress = re.search(r'<title>(.*?)</title>', run.stdout, re.S)
                raise SystemExit('Browser review did not complete.\n' +
                                 (unescape(progress[1]) + '\n' if progress else '') + run.stderr[-2000:])
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
