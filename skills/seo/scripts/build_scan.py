#!/usr/bin/env python3
"""Scan a directory of built/static HTML files for site-wide SEO problems (stdlib only).

Usage:
  python build_scan.py dist/
  python build_scan.py out/ --json

Reports pages missing a title/description/canonical/H1, duplicate titles or descriptions,
noindex pages, and broken internal links that point to files not in the build. Output is
evidence for follow-up, not a verdict; it cannot see client-rendered content, redirects,
or rewrites handled by the server.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from seo_scan import PageParser, meta_value  # noqa: E402

SKIP_DIRS = {"node_modules", ".git", "_next", "assets", "static"}


def page_url(root: Path, f: Path) -> str:
    rel = f.relative_to(root).as_posix()
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "/" + rel


def resolves(root: Path, path: str) -> bool:
    path = urllib.parse.unquote(path).lstrip("/")
    cands = [path, path + ".html", os.path.join(path, "index.html")]
    return any((root / c).is_file() for c in cands if c or c == "")


def scan(root: Path):
    pages = {}
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for name in files:
            if name.endswith((".html", ".htm")):
                f = Path(base) / name
                p = PageParser()
                try:
                    p.feed(f.read_text(encoding="utf-8", errors="replace"))
                except Exception:
                    continue
                pages[page_url(root, f)] = p

    issues = defaultdict(list)
    titles, descs = defaultdict(list), defaultdict(list)
    for url, p in pages.items():
        title = " ".join(p.title.split())
        desc = meta_value(p.meta, name="description")
        robots = meta_value(p.meta, name="robots").lower()
        h1s = [t for t, _ in p.headings if t == "h1"]
        if "noindex" in robots:
            issues["noindex"].append(url)
            continue  # noindex pages are intentionally excluded from the other checks
        if not title:
            issues["missing_title"].append(url)
        else:
            titles[title].append(url)
        if not desc:
            issues["missing_description"].append(url)
        else:
            descs[desc].append(url)
        if not p.canonicals:
            issues["missing_canonical"].append(url)
        if not h1s:
            issues["missing_h1"].append(url)
        for a in p.links:
            href = (a.get("href") or "").strip()
            pu = urllib.parse.urlparse(urllib.parse.urljoin(url, href))
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")) or pu.netloc or pu.scheme:
                continue
            if not resolves(root, pu.path) and pu.path.rsplit("/", 1)[-1].count(".") == 0:
                issues["broken_internal_link"].append(f"{url} -> {pu.path}")
    issues["duplicate_title"] = [f"{t!r}: {u}" for t, u in titles.items() if len(u) > 1]
    issues["duplicate_description"] = [f"{d[:60]!r}: {u}" for d, u in descs.items() if len(u) > 1]
    return {
        "root": str(root),
        "pages": len(pages),
        "issues": {k: v[:200] for k, v in issues.items() if v},
        "limitations": [
            "Static HTML only; client-rendered content and server rewrites are not visible.",
            "Broken-link check ignores links with file extensions and external URLs.",
        ],
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    root = Path(a.path)
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    res = scan(root)
    if a.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Pages scanned: {res['pages']}")
        for k, v in res["issues"].items():
            print(f"{k}: {len(v)}")
            for item in v[:5]:
                print("  -", item)
        if not res["issues"]:
            print("No issues detected by this lightweight check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
