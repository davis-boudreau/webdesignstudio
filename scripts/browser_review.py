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
    return evaluate('state.base===22 && state.ratio===1.125 && state.font===DEFAULT.font && !htmlExport().includes("<img")');
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
    const ranks={review:0,pass:1,exempt:2,candidate:3};const values=[...body.rows].map(row=>ranks[row.dataset.status]);
    return values.every((value,i)=>!i||value>=values[i-1]);
  }));
  app.style.width='320px';
  d.querySelector('#contrastChecks .contrast-group summary').click(); await wait();
  test('Expanded contrast table scrolls within a 320px page', () => d.documentElement.scrollWidth<=w.innerWidth+1);
  test('Contrast report ratios are finite and between 1 and 21', () => report().every(row=>Number.isFinite(row.ratio) && row.ratio>=1 && row.ratio<=21));
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
            print(json.dumps(report['errors']))
            return int(any(not item['pass'] for item in report['results']))
    finally:
        server.shutdown()


if __name__ == '__main__':
    raise SystemExit(main())
