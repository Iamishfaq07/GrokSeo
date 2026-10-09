# Changelog

## 1.3.0 - 2026-10-09

- Added `migration` mode and `references/migration.md` (classification, baseline, launch, monitoring, failure patterns).
- Added a symptom→suspect decision table to `references/diagnostics.md`.
- Added publisher/news and SaaS/B2B sections to `references/specialized-seo.md`.
- Added example outputs in `examples/`.

## 1.2.0 - 2026-10-03

- `seo_scan.py`: fixed H1 text capturing trailing text, added viewport/lang/hreflang/Open Graph/length checks, and `--file` offline mode.
- Added `build_scan.py` for site-wide checks on built/static HTML output.
- Added Nuxt, SvelteKit, Astro, WordPress, and Shopify notes to `references/implementation.md`.
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
