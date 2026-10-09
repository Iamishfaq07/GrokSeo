---
name: seo
description: Audit, plan, implement, and verify SEO for websites and web codebases. Use for technical SEO, on-page/content SEO, structured data, Core Web Vitals, crawl/indexing, internal linking, sitemaps, international/local/e-commerce SEO, AI-search visibility, launch checks, traffic-drop diagnosis, or SEO fixes in code.
when-to-use: SEO audit, technical SEO, on-page SEO, schema, sitemap, robots.txt, canonical, hreflang, Core Web Vitals, AI search, GEO, AEO, local SEO, ecommerce SEO, search visibility, indexing, ranking drop, SEO fix, pre-launch SEO
argument-hint: "[audit|page|technical|content|schema|keywords|competitors|ai|local|ecommerce|international|code|fix|launch|diagnose] [URL|path|topic]"
user-invocable: true
license: MIT
compatibility: Agent Skills open format; optimized for Grok Build and portable to compatible agents.
metadata:
  author: community
  version: "1.2.0"
  category: seo
  short-description: Evidence-first SEO auditing and implementation
---

# SEO

Use this skill to move from evidence -> diagnosis -> prioritized action -> implementation -> verification.

## Operating principles

1. **Inspect before advising.** Prefer the live site, rendered output, source code, Search Console/analytics data, or other direct evidence. Never invent page content, rankings, traffic, backlinks, or index status.
2. **Separate fact from hypothesis.** Label claims as `Observed`, `Verified`, `Likely`, or `Needs data` when uncertainty matters.
3. **Prefer primary sources for changing rules.** For Google-specific behavior, verify against current Google Search Central/web.dev documentation when web access exists. For Bing indexing, prefer Bing/IndexNow docs. For Schema.org semantics, prefer Schema.org.
4. **Do not promise rankings.** SEO changes improve eligibility, discoverability, relevance, experience, or crawl efficiency; they do not guarantee position or traffic.
5. **People-first, not keyword-first.** Do not recommend keyword stuffing, doorway pages, fake reviews, hidden text, link schemes, mass low-value pages, or other manipulative tactics.
6. **Progressive disclosure.** Read only the reference file(s) relevant to the task. Do not load all references by default.
7. **Implement when asked.** In a codebase, make safe, framework-native fixes, run relevant tests/build checks, inspect the diff, and verify the changed SEO output before declaring completion.
8. **Do not create pseudo-precision.** Do not invent an overall “SEO score” unless the user explicitly asks for one and the scoring rubric is shown. Prioritize findings by impact, confidence, and effort instead.

## Route the request

Choose the smallest workflow that satisfies the request:

| Mode | Use for | Read |
|---|---|---|
| `audit` | Full site or full repo audit | `references/audit.md` plus relevant specialist refs |
| `page` | One URL/page | `references/on-page-content.md`, `references/technical.md` |
| `technical` | Crawl/index/canonical/robots/rendering/CWV | `references/technical.md` |
| `content` | Helpful content, intent, information gain, trust | `references/on-page-content.md` |
| `schema` | Structured data audit/generation | `references/structured-data.md` |
| `keywords` | Query research, intent, clustering, content gaps | `references/keyword-competitor.md` |
| `competitors` | SERP/content/architecture comparison | `references/keyword-competitor.md` |
| `ai` | AI Overviews/AI Mode/answer-engine visibility | `references/ai-search.md` |
| `local` | Local business visibility | `references/specialized-seo.md` |
| `ecommerce` | Products, variants, facets, merchant SEO | `references/specialized-seo.md` |
| `international` | hreflang, locale architecture | `references/specialized-seo.md` |
| `code` | Source-code SEO review | `references/implementation.md`, `references/technical.md` |
| `fix` | Apply SEO changes to code | `references/implementation.md` + the relevant specialist ref |
| `launch` | Pre-launch SEO gate | `references/audit.md`, `references/implementation.md` |
| `diagnose` | Traffic/index/ranking drop | `references/diagnostics.md` |
| any | Report skeleton, launch checklist, JSON-LD/robots/redirect templates | `references/templates.md` |

If no mode is named, infer it from the request. A broad “check my SEO” is `audit`; a concrete code change request is `fix`.

## Grok Build tool use

On Grok Build, prefer the native tools when available:

- `web_search` for current SEO rules, SERPs, and primary-source discovery; constrain to official domains when validating engine-specific rules.
- `web_fetch` for a known documentation/page URL when enabled. If it is unavailable, do not pretend it was fetched.
- `list_dir`, `grep`, and `read_file` to inspect a repository before editing.
- `search_replace` for precise code changes.
- `run_terminal_command` for builds, tests, curl-based checks, or the bundled scripts when permitted.
- `search_tool` / `use_tool` to discover and use connected data sources such as analytics, Search Console, crawlers, or SEO APIs when the user has them available.
- `spawn_subagent` may parallelize independent parts of a broad audit, but only when available and useful; the parent must reconcile duplicated/conflicting findings and verify the final claims.

On other Agent Skills-compatible clients, use the equivalent tools. The workflow must degrade gracefully when a tool is unavailable.

## Evidence collection

Use the best evidence available, roughly in this order:

1. User-provided analytics/Search Console/exported data.
2. Live URL plus rendered page/source, HTTP status/headers, robots.txt, sitemap(s), structured data, and internal links.
3. Repository source and build output.
4. Search-engine result pages and official documentation, when web/search tools are available.
5. User-provided screenshots or reports.

For live websites, inspect both what users see and what crawlers receive when possible. JavaScript sites require special attention to server HTML versus rendered HTML.

If shell/network access is available, the bundled `scripts/seo_scan.py` can perform a lightweight deterministic page check. Treat it as one evidence source, not a substitute for browser rendering, field CWV, Search Console, or a full crawler.

## Freshness rule

SEO guidance changes. Before stating a time-sensitive rule as current, verify it from a primary source when web access is available. This includes supported rich-result types, crawler behavior, AI-search guidance, Core Web Vitals, Search spam policies, and search-engine submission APIs.

Read `references/source-policy.md` for source hierarchy and claims discipline.

## Full audit behavior

For a full audit, follow `references/audit.md`. At minimum cover:

- discovery, crawlability, indexability, status codes, redirects;
- robots directives, canonicals, sitemaps, pagination/facets where relevant;
- rendering and JavaScript discoverability;
- titles, headings, snippets, content intent/quality, duplication;
- site architecture and internal linking;
- structured data validity and eligibility;
- image/video discoverability when relevant;
- mobile/page experience and Core Web Vitals evidence;
- international/local/e-commerce specifics when detected;
- AI-search eligibility and citability without unsupported “GEO hacks”;
- security/HTTPS and obvious search-impacting deployment mistakes;
- measurement setup and post-change verification.

Do not mark an item “passed” unless it was actually checked.

## Implementation behavior

When the user asks to fix or optimize a repository:

1. Identify framework, routing model, rendering mode, metadata system, and deployment assumptions.
2. Read `references/implementation.md` and only the specialist references needed.
3. Inspect existing conventions before editing.
4. Fix root causes, not just surface tags.
5. Preserve existing behavior and visual design unless SEO requires a visible change.
6. Do not fabricate business claims, author credentials, ratings, reviews, prices, availability, addresses, or legal/compliance statements for SEO.
7. Run the narrowest relevant lint/type/test/build checks available.
8. Inspect generated/rendered metadata when feasible.
9. Summarize changed files, verification performed, remaining risks, and any external actions the user must take (for example Search Console submission).

## Output contract

For audits and diagnoses, default to this structure:

### Executive summary
2-6 sentences: biggest blockers/opportunities, evidence quality, and what matters first.

### Findings
For each material finding include:

- **Priority:** P0 blocker / P1 high / P2 medium / P3 low
- **Confidence:** High / Medium / Low
- **Evidence:** URL, file, selector, header, report, or observed behavior
- **Why it matters:** user/search impact, without claiming guaranteed ranking effects
- **Fix:** concrete action
- **Verify:** how to confirm the fix worked

### Action plan
Sequence fixes by dependency. Prefer a few high-leverage actions over a giant generic checklist.

### Data gaps
List only missing data that materially limits the conclusion.

For code implementation, replace the generic action plan with `Changes made`, `Verification`, and `Remaining external actions`.

## Priority definitions

- **P0 — Blocker:** prevents crawling/indexing, serves wrong status/redirect/canonical at scale, exposes a severe spam-policy risk, or breaks a critical launch path.
- **P1 — High:** likely affects important templates, discoverability, relevance, rich-result eligibility, internal link flow, or major user experience.
- **P2 — Medium:** meaningful optimization with narrower scope or weaker evidence.
- **P3 — Low:** cleanup, polish, or experiment with limited expected impact.

Priority is not the same as certainty. A potentially high-impact hypothesis with weak evidence should have lower confidence, not be presented as fact.

## Non-negotiable guardrails

- Never recommend cloaking, deceptive redirects, hidden text/links, doorway pages, purchased/manipulative links, review markup for reviews that do not exist, or scaled low-value content.
- Do not treat E-E-A-T as a single measurable ranking factor. Use it as a quality/trust evaluation framework.
- Do not treat `llms.txt`, special “GEO schema,” or a specific writing pattern as required for Google AI features unless current primary-source documentation says so.
- Do not equate lab Lighthouse scores with field Core Web Vitals.
- Do not assume a URL is indexed because it returns `200`, appears in a sitemap, or has a canonical.
- Do not block a URL in robots.txt merely to remove it from an index; crawlers generally must access a page to see `noindex`.
- Do not use canonicalization as a substitute for fixing fundamentally different or low-value pages.

## Bundled helpers

- `scripts/seo_scan.py` — lightweight URL/HTML SEO inspection with no third-party Python dependencies.
- `scripts/repo_seo_scan.py` — lightweight repository pattern scan for common web SEO risks.
- `scripts/seo_scan.py --file page.html` analyzes a saved HTML file offline.
- `scripts/build_scan.py <dir>` scans built/static HTML for missing or duplicate titles/descriptions, missing canonicals/H1s, noindex pages, and broken internal links.
- `scripts/site_check.py` — robots.txt, sitemap, and HTTP→HTTPS redirect check.

Use helper output as evidence, then inspect important findings directly before changing code.
