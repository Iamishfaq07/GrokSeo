# Full SEO audit workflow

Use for broad site/repository audits and pre-launch reviews. Do not blindly execute every check on tiny sites; adapt to the site's type and scale.

## 1. Establish scope and site type

Infer from evidence: SaaS, local service, e-commerce, publisher/content, marketplace/UGC, documentation, app/tool, enterprise/lead-gen, or mixed.

Capture:

- primary conversion/user goal;
- important page templates;
- target countries/languages if evident;
- rendering/framework/deployment architecture when a repo exists;
- whether the task is live-site only, repo only, or both.

Do not stall on missing business context. Audit what can be verified and mark assumptions.

## 2. Discovery and crawlability

Check material URLs for:

- DNS/TLS/HTTPS accessibility;
- meaningful HTTP status codes;
- redirect chains/loops and HTTP->HTTPS / host normalization;
- crawlable `<a href>` navigation for important paths;
- robots.txt syntax and accidental disallows;
- meta robots / X-Robots-Tag conflicts;
- orphaned important pages;
- crawl traps from parameters, calendars, internal search, or faceted navigation where applicable.

Remember: robots.txt controls crawling, not guaranteed de-indexing. A page blocked from crawling may not expose its `noindex` directive to a crawler.

## 3. Indexability and canonicalization

Check:

- self-referential canonicals on canonical HTML pages when appropriate;
- canonical target returns a usable status and is indexable;
- no contradictory canonical, redirect, hreflang, sitemap, and internal-link signals;
- duplicate URLs from query parameters, trailing slash, host/protocol variants, print pages, filters, sort URLs, session IDs;
- soft-404 behavior;
- staging/dev pages accidentally indexable;
- sitemap contains preferred canonical indexable URLs, not redirects/404/noindex URLs.

Do not claim actual Google index state without Search Console/URL Inspection/SERP evidence.

## 4. Rendering and JavaScript

Compare initial HTML with rendered content if possible. Important page meaning, links, metadata, structured data, and status semantics should remain discoverable and stable.

Flag:

- blank/app-shell initial HTML for critical content when avoidable;
- client-only metadata that is missing or unstable;
- JS-generated canonicals that conflict with source HTML;
- soft-404 SPAs returning `200` for missing routes;
- blocked JS/CSS required for rendering;
- links implemented only as click handlers without crawlable hrefs;
- hydration/runtime errors that remove main content.

## 5. Site architecture and internal links

Assess whether important content is reachable through logical navigation and contextual links.

Look for:

- excessive click depth for high-value pages;
- orphan pages;
- generic or misleading anchors;
- broken internal links;
- dead-end pages;
- internal links pointing through redirects or to non-canonicals;
- taxonomy that creates duplicate/near-duplicate archives;
- hub/pillar/category opportunities grounded in user intent, not arbitrary keyword clustering.

## 6. On-page and content

Read `on-page-content.md`.

At minimum inspect titles, primary heading, descriptive snippet candidates, main content, intent match, originality/information gain, trust/source signals, duplication, media usefulness, author/company context where relevant, and conversion/user journey.

## 7. Structured data

Read `structured-data.md`.

Only recommend types that accurately match visible page content and current feature eligibility. Validate syntax and required/recommended properties using current engine docs.

## 8. Performance and page experience

Separate field and lab data.

Current baseline Core Web Vitals targets when still confirmed by primary docs:

- LCP <= 2.5 s
- INP <= 200 ms
- CLS <= 0.1

Evaluate at the 75th percentile when using field data and consider mobile/desktop separately. Diagnose actual causes rather than optimizing a score for its own sake.

Also inspect mobile usability, intrusive overlays, broken interactions, layout instability, accessibility problems that impede users/crawlers, and excessive JS/rendering cost.

## 9. Specialized modules

Load only when applicable:

- local / e-commerce / international: `specialized-seo.md`
- AI search: `ai-search.md`
- keyword/competitor/content architecture: `keyword-competitor.md`
- code implementation: `implementation.md`

## 10. Measurement readiness

When available, review:

- Google Search Console performance/indexing/sitemap/CWV data;
- analytics organic landing pages and conversions;
- server logs for crawler behavior on large/complex sites;
- Bing Webmaster Tools if Bing matters;
- rank tracking only as a directional supplement, not the sole success metric.

Check annotation/change dates before attributing traffic movement to an SEO change.

## 11. Synthesize, don't dump

Group duplicates into root causes. A useful audit should usually identify a small number of systems/templates producing many symptoms.

Prioritize using:

- business/user importance of affected pages;
- scope (# of URLs/templates affected);
- severity (crawl/index/relevance/UX);
- confidence in causality;
- effort and dependencies;
- reversibility/risk.

Every P0/P1 should have a verification step.
