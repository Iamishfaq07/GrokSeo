# GrokSeo — the `/seo` skill for Grok Build

An evidence-first SEO skill for [Grok Build](https://x.ai) (and any Agent Skills-compatible agent). It audits live sites and codebases, diagnoses traffic drops, and **implements fixes in code**, then verifies them — without ranking promises, folklore, or manipulative tactics.

## Features

- **15 workflows** behind one command: audit, page, technical, content, schema, keywords, competitors, ai, local, ecommerce, international, code, fix, launch, diagnose.
- **Evidence over opinion** — findings carry priority (P0–P3), confidence, evidence, fix, and a verification step. Nothing is marked "passed" unless checked.
- **Progressive disclosure** — a small router `SKILL.md` loads only the reference files a task needs.
- **Current-rules discipline** — time-sensitive claims (rich results, AI Overviews, CWV, spam policy) are verified against primary sources.
- **Modern coverage** — technical SEO, structured data, Core Web Vitals, JS rendering, AI-search/GEO/AEO (without myths like required `llms.txt`), local, e-commerce, international/hreflang.
- **Code-native fixes** — framework-aware implementation guidance (metadata APIs, sitemaps, canonicals, schema).
- **Zero-dependency helper scripts** (Python stdlib only).
- **Guardrails** — no cloaking, fake reviews/schema, doorway pages, hidden text, or link schemes.

## Install

From GitHub:

```bash
grok plugin install iamishfaq07/grokseo --trust
```

Locally while developing:

```bash
grok plugin install . --trust
grok inspect      # verify the skill is discovered
```

Skill-only install (no plugin): copy `skills/seo/` to `<project>/.grok/skills/seo/` or `~/.grok/skills/seo/`.

## Usage

```text
/seo audit https://example.com
/seo page https://example.com/pricing
/seo technical https://example.com
/seo schema https://example.com/product/widget
/seo keywords "project management software"
/seo competitors https://example.com
/seo ai https://example.com/guide
/seo code .
/seo fix the technical SEO issues in this project
/seo launch .
/seo diagnose organic traffic dropped 30% after the migration
```

| Mode | Purpose | Reference |
|---|---|---|
| `audit` | Full site/repo audit | `audit.md` |
| `page` | Single page review | `on-page-content.md`, `technical.md` |
| `technical` | Crawl, index, canonical, rendering, CWV | `technical.md` |
| `content` | Intent, helpfulness, trust | `on-page-content.md` |
| `schema` | Structured data | `structured-data.md` |
| `keywords` / `competitors` | Research & gap analysis | `keyword-competitor.md` |
| `ai` | AI Overviews / answer-engine visibility | `ai-search.md` |
| `local` / `ecommerce` / `international` | Specialized SEO | `specialized-seo.md` |
| `code` / `fix` / `launch` | Review, implement, pre-launch gate | `implementation.md` |
| `diagnose` | Traffic/index/ranking drops | `diagnostics.md` |
| templates | Report, launch gate, JSON-LD, robots, redirects | `templates.md` |

## Output format

Audits return an executive summary, findings (priority, confidence, evidence, why it matters, fix, verify), a dependency-ordered action plan, and data gaps. Code work returns changes made, verification, and remaining external actions (e.g. Search Console submission).

## Helper scripts

```bash
python skills/seo/scripts/seo_scan.py https://example.com --json   # single-page HTML/SEO inspection
python skills/seo/scripts/seo_scan.py page.html --file             # same checks on a saved HTML file
python skills/seo/scripts/build_scan.py dist/                      # site-wide checks on built HTML (dupes, missing tags, broken links)
python skills/seo/scripts/site_check.py https://example.com        # robots.txt, sitemaps, HTTP→HTTPS
python skills/seo/scripts/repo_seo_scan.py . --json                # repo pattern scan for SEO risks
```

These are lightweight evidence sources — not a substitute for rendering, Search Console, field CWV data, or a full crawler.

## Repository layout

```text
skills/seo/SKILL.md        router + principles + output contract
skills/seo/references/     focused specialist guidance
skills/seo/scripts/        stdlib-only helpers
scripts/validate_skill.py  structure validator (run in CI)
```

## Development

```bash
python scripts/validate_skill.py
python -m py_compile skills/seo/scripts/*.py
python -m unittest discover -s tests
```

See [CONTRIBUTING.md](CONTRIBUTING.md), [SECURITY.md](SECURITY.md), and [CHANGELOG.md](CHANGELOG.md).

## Marketplace publishing

Grok Build marketplaces can reference this repository as a remote plugin source; pin the full commit SHA for reproducible installs.

## License

MIT
