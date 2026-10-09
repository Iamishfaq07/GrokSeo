#!/usr/bin/env python3
"""Draft an llms.txt from a built/static HTML directory (stdlib only).

Usage:
  python llms_txt.py dist/ --base-url https://example.com --name "Example Co" \
      --summary "One-sentence description." > llms.txt

llms.txt is an optional, experimental convention. It is NOT a Google ranking factor or a
requirement for AI Overviews/AI Mode (see references/ai-search.md). Review and edit the draft
by hand: it only lists indexable pages (no noindex) using their <title> and meta description.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_scan import SKIP_DIRS, page_url  # noqa: E402
from seo_scan import PageParser, meta_value  # noqa: E402


def collect(root: Path):
    pages = []
    for base, dirs, files in os.walk(root):
        dirs[:] = sorted(d for d in dirs if d not in SKIP_DIRS)
        for name in sorted(files):
            if not name.endswith((".html", ".htm")):
                continue
            f = Path(base) / name
            p = PageParser()
            p.feed(f.read_text(encoding="utf-8", errors="replace"))
            if "noindex" in meta_value(p.meta, name="robots").lower():
                continue
            title = " ".join(p.title.split())
            if title:
                pages.append((page_url(root, f), title, meta_value(p.meta, name="description")))
    return sorted(pages)


def render(pages, base_url, name, summary):
    lines = [f"# {name}", ""]
    if summary:
        lines += [f"> {summary}", ""]
    lines += ["## Pages", ""]
    for url, title, desc in pages:
        entry = f"- [{title}]({base_url.rstrip('/')}{url})"
        lines.append(entry + (f": {desc}" if desc else ""))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("path")
    ap.add_argument("--base-url", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--summary", default="")
    a = ap.parse_args()
    root = Path(a.path)
    if not root.is_dir():
        print(f"Not a directory: {root}", file=sys.stderr)
        return 2
    sys.stdout.write(render(collect(root), a.base_url, a.name, a.summary))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
