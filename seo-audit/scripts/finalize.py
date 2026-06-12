#!/usr/bin/env python3
"""
Torah Lock — finalize step (run AFTER content workflow + new pages exist).
Adds the new secondary pages (Features / FAQ / About) to every footer site-wide,
using root-relative hrefs so the same markup works at any directory depth.
Idempotent.
"""
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXCLUDE_DIRS = {"bennymh", "ilanit", "jonnystorms", "seo-audit"}

INJECT = (
    '<div class="footer-links">\n'
    '      <a href="/features.html">Features</a>\n'
    '      <a href="/faq.html">FAQ</a>\n'
    '      <a href="/about.html">About</a>'
)


def targets():
    files = list(ROOT.glob("*.html")) + list((ROOT / "blog").glob("*.html"))
    for f in files:
        if any(p in EXCLUDE_DIRS for p in f.relative_to(ROOT).parts[:-1]):
            continue
        yield f


def main():
    n = 0
    for f in targets():
        t = f.read_text(encoding="utf-8")
        if '/features.html' in t:        # already injected
            continue
        if '<div class="footer-links">' not in t:
            continue
        t = t.replace('<div class="footer-links">', INJECT, 1)
        f.write_text(t, encoding="utf-8")
        n += 1
    print(f"Footer links injected into {n} files.")


if __name__ == "__main__":
    main()
