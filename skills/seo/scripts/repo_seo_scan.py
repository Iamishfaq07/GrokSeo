#!/usr/bin/env python3
"""Lightweight pattern scan for common SEO-related files/configuration.

Usage:
  python repo_seo_scan.py .
  python repo_seo_scan.py . --json

This scanner is intentionally heuristic. Confirm findings by reading the referenced files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", ".cache", "coverage", ".venv", "venv", "vendor"}
TEXT_EXTS = {".html", ".htm", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte", ".astro", ".py", ".php", ".rb", ".mdx", ".json", ".xml", ".txt"}
MAX_FILE = 1_500_000

PATTERNS = {
    "noindex": re.compile(r"noindex", re.I),
    "canonical": re.compile(r"canonical", re.I),
    "robots": re.compile(r"robots\.txt|robots\s*[:=]", re.I),
    "sitemap": re.compile(r"sitemap", re.I),
    "jsonld": re.compile(r"application/ld\+json|@context\s*['\"]?\s*:\s*['\"]https?://schema\.org", re.I),
    "hreflang": re.compile(r"hreflang", re.I),
    "metadata_api": re.compile(r"generateMetadata|export\s+const\s+metadata|useHead\(|<Head>|react-helmet|helmet", re.I),
}


def detect_stack(root: Path):
    stack = []
    pkg = root / "package.json"
    if pkg.exists():
        try:
            data = json.loads(pkg.read_text(errors="ignore"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            for key, label in [
                ("next", "Next.js"), ("nuxt", "Nuxt"), ("astro", "Astro"),
                ("@sveltejs/kit", "SvelteKit"), ("gatsby", "Gatsby"),
                ("@remix-run/react", "Remix"), ("react-router", "React Router"),
                ("react", "React"), ("vue", "Vue")
            ]:
                if key in deps:
                    stack.append(label)
        except Exception:
            pass
    for name, label in [("manage.py", "Django/Python"), ("Gemfile", "Ruby/Rails possible"), ("composer.json", "PHP")]:
        if (root / name).exists():
            stack.append(label)
    return list(dict.fromkeys(stack))


def scan(root: Path):
    findings = {k: [] for k in PATTERNS}
    files_scanned = 0
    suspicious = []
    for base, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for name in files:
            p = Path(base) / name
            if p.suffix.lower() not in TEXT_EXTS and name not in {"robots.txt", "sitemap.xml"}:
                continue
            try:
                if p.stat().st_size > MAX_FILE:
                    continue
                text = p.read_text(errors="ignore")
            except Exception:
                continue
            files_scanned += 1
            rel = str(p.relative_to(root))
            for key, rx in PATTERNS.items():
                if rx.search(text):
                    findings[key].append(rel)
            if re.search(r"noindex", text, re.I) and re.search(r"production|prod", text, re.I):
                suspicious.append({"file": rel, "note": "Contains both noindex and production/prod text; inspect environment logic."})
            if re.search(r"canonical", text, re.I) and re.search(r"localhost|127\.0\.0\.1", text):
                suspicious.append({"file": rel, "note": "Canonical-related code also contains localhost; verify production origin handling."})

    key_files = []
    candidates = [
        "robots.txt", "public/robots.txt", "static/robots.txt", "sitemap.xml", "public/sitemap.xml",
        "next.config.js", "next.config.mjs", "next.config.ts", "nuxt.config.ts", "astro.config.mjs",
        "vite.config.ts", "vite.config.js", "package.json"
    ]
    for c in candidates:
        if (root / c).exists():
            key_files.append(c)

    return {
        "root": str(root.resolve()),
        "stack": detect_stack(root),
        "files_scanned": files_scanned,
        "key_files": key_files,
        "pattern_hits": {k: v[:100] for k, v in findings.items()},
        "notes": suspicious[:100],
        "limitations": [
            "Pattern hits are not automatically errors.",
            "Generated/runtime metadata may not appear in source patterns.",
            "Inspect built/rendered output before declaring an SEO issue fixed."
        ]
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path", nargs="?", default=".")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(args.path)
    result = scan(root)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print("Stack:", ", ".join(result["stack"]) or "unknown")
        print("Files scanned:", result["files_scanned"])
        print("Key files:", ", ".join(result["key_files"]) or "none detected")
        for key, hits in result["pattern_hits"].items():
            print(f"{key}: {len(hits)} file(s)")
        for note in result["notes"]:
            print("NOTE:", note["file"], "-", note["note"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
