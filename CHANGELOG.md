# Changelog

## 1.2.0 - 2026-10-03

- `seo_scan.py`: fixed H1 text capturing trailing text, added viewport/lang/hreflang/Open Graph/length checks, and `--file` offline mode.
- Added unit tests (`tests/`) and run them in CI.
- Added `references/templates.md` (report skeleton, launch gate, JSON-LD, robots, redirect map).
- Added AI crawler controls guidance to `references/ai-search.md`.

## 1.1.0 - 2026-10-03

- Added `site_check.py` (robots.txt, sitemap, HTTPS redirect checks).
- Expanded README with modes, examples, helper-script docs, and design principles.

## 1.0.0 - 2026-10-03

- Initial public-ready release.
- Grok Build native frontmatter and `/seo` invocation.
- Open Agent Skills-compatible folder structure.
- Progressive-disclosure references for technical, content, schema, AI search, keyword/competitor, specialized SEO, implementation, and diagnostics.
- Added codebase `fix` and pre-launch workflows.
- Added zero-dependency live-page and repository scanners.
