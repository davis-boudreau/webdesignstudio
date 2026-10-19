"""Dependency-free structure check: every asset referenced by index.html exists,
and every file in src/ is referenced. Run: python scripts/check_structure.py"""
import pathlib
import re
import sys
from collections import Counter
from html.parser import HTMLParser

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
refs = {ref.split('?', 1)[0] for ref in re.findall(r'(?:href|src)="(src/[^"]+)"', html)}
errors = [f"missing file: {r}" for r in sorted(refs) if not (root / r).is_file()]
on_disk = {p.relative_to(root).as_posix() for p in (root / "src").rglob("*") if p.is_file()}
errors += [f"unreferenced file: {p}" for p in sorted(on_disk - refs)]


class PageReferences(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.anchors = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('href', '').startswith('#'):
            self.anchors.append(attrs['href'][1:])


page = PageReferences()
page.feed(html)
errors += [f"duplicate HTML id: {name}" for name, count in Counter(page.ids).items() if count > 1]
errors += [f"missing anchor target: #{name}" for name in page.anchors if name not in page.ids]
for path in [root / 'index.html', *sorted((root / 'src').rglob('*'))]:
    if path.is_file() and re.search(r'nscc', path.read_text(encoding='utf-8'), re.I):
        errors.append(f"institution-specific reference: {path.relative_to(root)}")
if re.search(r"<style>|<script>", html):
    errors.append("index.html contains inline <style>/<script>; move it into src/")

print("\n".join(errors) or f"OK: {len(refs)} assets verified")
sys.exit(1 if errors else 0)
