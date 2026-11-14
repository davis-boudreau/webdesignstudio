"""Offline review catalogue and local check command; no browser starts on import.

Run all checks: python scripts/review_suites.py
Print CI matrix: python scripts/review_suites.py --matrix
"""
import argparse
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
BROWSER_SUITES = (
    'project_model_review', 'project_library_review', 'navigation_review',
    'planning_review', 'content_tree_review', 'sitemap_review', 'wireframe_review',
    'palette_review', 'contrast_review', 'components_review', 'typography_review',
    'spacing_review', 'responsive_preview_review', 'standalone_exports_review',
    'view_updates_review', 'export_pipeline_review', 'browser_review',
    'button_states_review',
)
OPTIONAL_NETWORK_SUITES = ('font_cdn_review',)
LOCAL_CHECKS = ('check_structure', 'browser_runner_review', *BROWSER_SUITES)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    options = parser.add_mutually_exclusive_group()
    options.add_argument('--matrix', action='store_true', help='Print the offline browser CI matrix as JSON')
    options.add_argument('--list', action='store_true', help='List checks without running them')
    args = parser.parse_args(argv)
    if args.matrix:
        print(json.dumps({'suite': BROWSER_SUITES}))
        return 0
    if args.list:
        print('\n'.join(f'python scripts/{name}.py' for name in LOCAL_CHECKS))
        return 0
    failed = []
    for name in LOCAL_CHECKS:
        print(f'Running scripts/{name}.py', flush=True)
        result = subprocess.run([sys.executable, str(ROOT / 'scripts' / f'{name}.py')], cwd=ROOT)
        if result.returncode:
            failed.append(name)
    print(f'{len(LOCAL_CHECKS) - len(failed)}/{len(LOCAL_CHECKS)} check commands passed', flush=True)
    if failed:
        print('Failed: ' + ', '.join(failed), flush=True)
    return int(bool(failed))


if __name__ == '__main__':
    raise SystemExit(main())
