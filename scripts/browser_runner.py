"""Shared isolated Chrome runner for independently authored HTML review suites.

No feature harness is imported here. Each run owns its server and temporary
profile; callers supply HTML and optional Chrome flags without patching globals.
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


class ReviewServer(ThreadingHTTPServer):
    # Chrome requests the deferred local assets in a burst. Keep the Windows
    # listener queue large enough to avoid intermittent unchanged-asset failures.
    request_queue_size = 128


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, harness, **kwargs):
        self.harness = harness
        super().__init__(*args, **kwargs)

    def log_message(self, *_args):
        pass

    def do_GET(self):
        path = self.path.split('?', 1)[0]
        if path == '/__review_tick__':
            # Test-only real-time synchronization for browser File.text().
            threading.Event().wait(0.02)
            self.send_response(204)
            self.send_header('Cache-Control', 'no-store')
            self.end_headers()
            return
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
            body = self.harness
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


def run_review(harness, *, chrome_flags=(), virtual_time_budget=225000, timeout=660):
    """Print suite results and return nonzero for failed checks or captured errors.

    Chrome flags apply only to this run. Defaults preserve the full integration
    suite's virtual-time and wall-clock budgets. No normal user profile is used.
    """
    browser = os.environ.get('CHROME_BIN') or shutil.which('google-chrome') or shutil.which('chromium')
    if not browser:
        for location in ['C:/Program Files/Google/Chrome/Application/chrome.exe',
                         'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe']:
            if Path(location).is_file():
                browser = location
                break
    if not browser:
        raise SystemExit('Chrome/Chromium not found. Set CHROME_BIN to its executable.')
    server = ReviewServer(('127.0.0.1', 0), partial(Handler, harness=harness, directory=str(ROOT)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        with tempfile.TemporaryDirectory(prefix='studio-review-') as profile:
            run = subprocess.run([browser, *chrome_flags, '--headless', '--disable-gpu', '--no-first-run',
                                  '--no-default-browser-check', '--disable-background-networking',
                                  # Real file reads can complete after Chrome advances virtual timers;
                                  # allow the content/file and sitemap matrices to finish.
                                  '--user-data-dir=' + profile, f'--virtual-time-budget={virtual_time_budget}',
                                  '--dump-dom', f'http://127.0.0.1:{server.server_port}/__review__'],
                                 # Allow the expanded matrix to finish on Windows.
                                 capture_output=True, encoding='utf-8', errors='replace', timeout=timeout)
            return report_result(run)
    finally:
        server.shutdown()
        server.server_close()



def report_result(run):
    """Decode Chrome's dumped DOM, print diagnostics and fail closed."""
    match = re.search(r'<pre id="results">(.*?)</pre>', run.stdout, re.S)
    if not match or match[1] == 'RUNNING':
        progress = re.search(r'<title>(.*?)</title>', run.stdout, re.S)
        raise SystemExit('Browser review did not complete.\n' +
                         (unescape(progress[1]) + '\n' if progress else '') + run.stderr[-2000:])
    try:
        report = json.loads(unescape(match[1]))
        results, errors = report['results'], report['errors']
        if (not isinstance(results, list) or not results or
                not isinstance(errors, list) or
                any(not isinstance(item, dict) or
                    not isinstance(item.get('name'), str) or
                    not isinstance(item.get('pass'), bool) for item in results)):
            raise ValueError('Expected nonempty checks and an errors list')
    except (ValueError, KeyError, TypeError) as error:
        raise SystemExit(f'Invalid browser review report: {error}') from error
    for item in results:
        print(('PASS' if item['pass'] else 'FAIL') + ': ' + item['name'] +
              (': ' + str(item.get('error', '')) if not item['pass'] else ''))
    print(f"{sum(item['pass'] for item in results)}/{len(results)} browser checks passed")
    print(json.dumps(errors))
    if run.returncode:
        print(f'Chrome exited with status {run.returncode}: ' + run.stderr[-2000:])
    return int(bool(run.returncode or errors or any(not item['pass'] for item in results)))
