"""Dependency-free runner contract tests. Run: python scripts/browser_runner_review.py."""
from contextlib import redirect_stdout
from html import escape
import importlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
from urllib.request import urlopen

import browser_runner as runner
import review_suites


def completed(report=None, *, returncode=0):
    if report is None:
        report = {'results': [{'name': 'Example', 'pass': True}], 'errors': []}
    return subprocess.CompletedProcess([], returncode,
        '<pre id="results">' + escape(json.dumps(report)) + '</pre>', 'browser diagnostic')


class RunnerContracts(unittest.TestCase):
    def report(self, result):
        with redirect_stdout(io.StringIO()):
            return runner.report_result(result)

    def test_success(self):
        self.assertEqual(self.report(completed()), 0)

    def test_failed_assertion(self):
        self.assertEqual(self.report(completed({'results': [
            {'name': 'Failure', 'pass': False, 'error': '<detail>&'}], 'errors': []})), 1)

    def test_captured_errors_fail_even_with_passing_assertions(self):
        self.assertEqual(self.report(completed({'results': [
            {'name': 'Example', 'pass': True}], 'errors': ['Late exception']})), 1)

    def test_browser_exit_code_fails_even_with_passing_assertions(self):
        self.assertEqual(self.report(completed(returncode=9)), 1)

    def test_incomplete_has_progress_and_browser_diagnostics(self):
        for dom in ['', '<title>Last check &amp; progress</title><pre id="results">RUNNING</pre>']:
            with self.subTest(dom=dom), self.assertRaises(SystemExit) as caught:
                self.report(subprocess.CompletedProcess([], 0, dom, 'browser diagnostic'))
            self.assertIn('did not complete', str(caught.exception))
            self.assertIn('browser diagnostic', str(caught.exception))
            if dom:
                self.assertIn('Last check & progress', str(caught.exception))

    def test_malformed_or_empty_reports_fail(self):
        for report in [None, [], {}, {'results': [], 'errors': []},
                       {'results': [{'name': 'Example', 'pass': 'false'}], 'errors': []},
                       {'results': [{'pass': True}], 'errors': []},
                       {'results': [{'name': 'Example', 'pass': True}], 'errors': 'oops'}]:
            result = completed(report) if report is not None else subprocess.CompletedProcess(
                [], 0, '<pre id="results">invalid json</pre>', '')
            with self.subTest(report=report), self.assertRaises(SystemExit):
                self.report(result)

    def test_suite_imports_do_not_import_integration_or_launch_browser(self):
        with patch.object(runner, 'run_review', side_effect=AssertionError('Ran on import')):
            for name in (*review_suites.BROWSER_SUITES, *review_suites.OPTIONAL_NETWORK_SUITES):
                if name == 'browser_review':
                    continue
                importlib.import_module(name)
        self.assertNotIn('browser_review', sys.modules)

    def test_catalogue_accounts_for_every_review_file(self):
        registered = ('browser_runner_review', *review_suites.BROWSER_SUITES,
                      *review_suites.OPTIONAL_NETWORK_SUITES)
        discovered = {path.stem for path in Path(__file__).parent.glob('*_review.py')}
        self.assertEqual(len(registered), len(set(registered)))
        self.assertEqual(set(registered), discovered)

    def test_ci_matrix_does_not_launch_checks_or_include_live_network_suite(self):
        output = io.StringIO()
        with patch.object(review_suites.subprocess, 'run', side_effect=AssertionError('Launched check')), \
                redirect_stdout(output):
            self.assertEqual(review_suites.main(['--matrix']), 0)
        matrix = json.loads(output.getvalue())
        self.assertEqual(matrix, {'suite': list(review_suites.BROWSER_SUITES)})
        self.assertIn('button_states_review', matrix['suite'])
        self.assertFalse(set(matrix['suite']) & set(review_suites.OPTIONAL_NETWORK_SUITES))

    def test_local_checks_continue_and_propagate_failure(self):
        for failed in [False, True]:
            def launch(command, **kwargs):
                return subprocess.CompletedProcess(command, int(failed and command[-1].endswith('check_structure.py')))
            with self.subTest(failed=failed), patch.object(review_suites.subprocess, 'run', side_effect=launch) as run, \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(review_suites.main([]), int(failed))
            self.assertEqual(run.call_count, len(review_suites.LOCAL_CHECKS))
            self.assertEqual([Path(call.args[0][-1]).stem for call in run.call_args_list], list(review_suites.LOCAL_CHECKS))
            self.assertTrue(all(call.args[0][0] == sys.executable and call.kwargs['cwd'] == review_suites.ROOT
                                for call in run.call_args_list))

    def test_independent_runs_serve_their_own_harness_and_clean_profiles(self):
        profiles = []
        for harness, flags in [('first suite', ('--force-high-contrast',)), ('second suite', ())]:
            def launch(command, **kwargs):
                self.assertEqual(command[0], 'test-chrome')
                self.assertEqual('--force-high-contrast' in command, bool(flags))
                self.assertIn('--virtual-time-budget=1234', command)
                self.assertEqual(kwargs['timeout'], 7)
                profile = Path(next(arg.split('=', 1)[1] for arg in command
                                    if arg.startswith('--user-data-dir=')))
                self.assertTrue(profile.is_dir())
                profiles.append(profile)
                base = command[-1].rsplit('/', 1)[0]
                with urlopen(command[-1]) as response:
                    self.assertEqual(response.read().decode(), harness)
                with urlopen(base + '/index.html') as response:
                    self.assertIn('window.__reviewErrors=[]', response.read().decode())
                with urlopen(base + '/__font_fixture__?family=Inter') as response:
                    self.assertIn('@font-face', response.read().decode())
                with urlopen(base + '/__review_tick__') as response:
                    self.assertEqual(response.status, 204)
                return completed()
            with patch.dict('os.environ', {'CHROME_BIN': 'test-chrome'}), \
                    patch.object(runner.subprocess, 'run', side_effect=launch), \
                    redirect_stdout(io.StringIO()):
                self.assertEqual(runner.run_review(harness, chrome_flags=flags,
                                                  virtual_time_budget=1234, timeout=7), 0)
            self.assertFalse(profiles[-1].exists())
        self.assertNotEqual(profiles[0], profiles[1])

    def test_timeout_closes_server_and_removes_profile(self):
        profiles, servers = [], []
        original_server = runner.ReviewServer

        def server(*args, **kwargs):
            instance = original_server(*args, **kwargs)
            servers.append(instance)
            return instance

        def launch(command, **kwargs):
            profiles.append(Path(next(arg.split('=', 1)[1] for arg in command
                                     if arg.startswith('--user-data-dir='))))
            raise subprocess.TimeoutExpired(command, kwargs['timeout'])

        with patch.dict('os.environ', {'CHROME_BIN': 'test-chrome'}), \
                patch.object(runner, 'ReviewServer', side_effect=server), \
                patch.object(runner.subprocess, 'run', side_effect=launch), \
                self.assertRaises(subprocess.TimeoutExpired):
            runner.run_review('timeout suite')
        self.assertFalse(profiles[0].exists())
        self.assertEqual(servers[0].socket.fileno(), -1)


if __name__ == '__main__':
    unittest.main()
