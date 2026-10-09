# Site migrations, redesigns, and replatforming

Most catastrophic organic losses come from migrations. Treat the plan as a gate, not an afterthought.

## Classify the change

| Type | Main risks |
|---|---|
| URL/path restructure | lost redirects, chains, changed internal links |
| Domain / subdomain / protocol change | signals reset, missed host variants, mixed content |
| Replatform / CMS / framework | template metadata loss, rendering changes, status-code differences |
| Redesign (same URLs) | removed content, changed headings/links, slower pages, JS-only content |
| Consolidation / pruning | removing pages that earn traffic or links without a successor |
| International restructure | hreflang breakage, wrong locale redirects |

## Pre-migration (baseline)

1. Crawl the old site and export all indexable URLs with status, title, description, canonical, H1, internal-link counts.
2. Export Search Console performance by page and query, plus top linked pages if backlink data exists.
3. Record CWV and rendering baseline for key templates.
4. Build the **redirect map** (old → closest equivalent; see `templates.md`). Map by content equivalence, not blanket redirect to the homepage.
5. Decide per section: keep, merge, redirect, or remove (410 only when no substitute exists).
6. Stage with `noindex`/auth, then **confirm that control is removed at launch** (see launch gate in `templates.md`).

## Launch day

- Redirects live as permanent server-side redirects; test a sample of every URL pattern, not just a handful.
- Old URLs → one hop to the final canonical (no chains/loops); host/protocol/trailing-slash variants normalized.
- New robots.txt and sitemap are the production versions; sitemap lists only new canonical URLs.
- Canonicals, hreflang, internal links, and structured data point to the new URLs.
- Keep the old sitemap reachable briefly if it helps discovery of redirects; submit the new sitemap.
- For domain moves, use the engine's change-of-address tooling where available and keep old-domain redirects long-term.

## Post-migration monitoring (first weeks)

- Re-crawl new site: status codes, canonicals, noindex, orphaned pages, redirect chains.
- Compare indexed/crawled counts and clicks/impressions per section against baseline, by segment.
- Watch server logs or crawl stats for 404/5xx spikes and unexpected crawl-rate drops.
- Fix high-value 404s with redirects to true equivalents; do not mass-redirect to unrelated pages (treated as soft 404s).
- Expect temporary fluctuation; escalate on sustained loss concentrated in a section/template (see `diagnostics.md`).

## Common failure patterns

- Staging `noindex` or `Disallow: /` shipped to production.
- Redirect map built from a partial URL list; parameter and paginated URLs forgotten.
- Titles/descriptions/canonicals dropped by the new template.
- Content moved behind client-only rendering.
- Internal links still pointing to redirecting URLs.
- Pruned pages that had links or traffic.

## Output when asked for a migration plan

Provide: scope and risk classification, redirect strategy, URL inventory source, template-parity checklist, launch gate, monitoring metrics with owners and dates, and a rollback trigger (for example, "sitewide 5xx or noindex detected → revert").
