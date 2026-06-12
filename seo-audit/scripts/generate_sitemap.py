#!/usr/bin/env python3
"""
Torah Lock — sitemap generator.
Scans the repo for indexable HTML pages and writes sitemap.xml.
Excludes: noindex attribution redirects (bennymh/ilanit/jonnystorms), 404.html,
and anything marked <meta name="robots" content="noindex">.
Run from anywhere: python3 seo-audit/scripts/generate_sitemap.py [YYYY-MM-DD]
"""
import sys, re, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "https://torahlock.app"
TODAY = sys.argv[1] if len(sys.argv) > 1 else datetime.date.today().isoformat()

EXCLUDE_DIRS = {"bennymh", "ilanit", "jonnystorms", "seo-audit"}
EXCLUDE_FILES = {"404.html"}


def loc_for(path: pathlib.Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return BASE + "/"
    return f"{BASE}/{rel}"


def indexable(path: pathlib.Path) -> bool:
    if path.name in EXCLUDE_FILES:
        return False
    if any(part in EXCLUDE_DIRS for part in path.relative_to(ROOT).parts[:-1]):
        return False
    txt = path.read_text(encoding="utf-8", errors="ignore")
    if re.search(r'<meta[^>]+name="robots"[^>]+noindex', txt, re.I):
        return False
    return True


def main():
    pages = []
    # root-level html
    for p in sorted(ROOT.glob("*.html")):
        if indexable(p):
            pages.append(p)
    # blog posts
    for p in sorted((ROOT / "blog").glob("*.html")):
        if indexable(p):
            pages.append(p)

    # order: homepage first, then root pages, then blog
    def sort_key(p):
        rel = p.relative_to(ROOT).as_posix()
        if rel == "index.html":
            return (0, rel)
        if "/" not in rel:
            return (1, rel)
        return (2, rel)

    pages.sort(key=sort_key)

    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in pages:
        lines += ["  <url>",
                  f"    <loc>{loc_for(p)}</loc>",
                  f"    <lastmod>{TODAY}</lastmod>",
                  "  </url>"]
    lines.append("</urlset>")
    (ROOT / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote sitemap.xml with {len(pages)} URLs (lastmod {TODAY}).")


if __name__ == "__main__":
    main()
