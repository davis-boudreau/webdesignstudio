"""Dependency-free structure check: every asset referenced by index.html exists,
and every file in src/ is referenced. Run: python scripts/check_structure.py"""
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parent.parent
html = (root / "index.html").read_text(encoding="utf-8")
refs = set(re.findall(r'(?:href|src)="(src/[^"]+)"', html))
errors = [f"missing file: {r}" for r in sorted(refs) if not (root / r).is_file()]
on_disk = {p.relative_to(root).as_posix() for p in (root / "src").rglob("*") if p.is_file()}
errors += [f"unreferenced file: {p}" for p in sorted(on_disk - refs)]
if re.search(r"<style>|<script>", html):
    errors.append("index.html contains inline <style>/<script>; move it into src/")

print("\n".join(errors) or f"OK: {len(refs)} assets verified")
sys.exit(1 if errors else 0)
