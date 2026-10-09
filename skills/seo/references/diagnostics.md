# SEO traffic/indexing diagnosis

Use when the user reports a traffic, ranking, indexing, or impressions drop.

## Do not jump to an algorithm-update conclusion

Start with dates, affected segments, and direct evidence.

## Triage sequence

1. **Define the metric:** clicks, impressions, sessions, conversions, indexed pages, keyword positions, crawl rate, or revenue.
2. **Define the window:** exact start date, comparison period, seasonality, weekday effects.
3. **Segment:** country, device, search type, directory/template, query, branded vs non-branded, new vs returning page, page type.
4. **Check tracking:** analytics/tagging/consent/reporting changes can mimic SEO loss.
5. **Check technical releases:** robots/noindex/canonical/redirect/routing/JS/host/CDN/sitemap changes.
6. **Check indexation:** Search Console Page Indexing/URL Inspection for representative pages when available.
7. **Check demand/SERP change:** query demand, SERP feature changes, new competitors, seasonality, intent shifts.
8. **Check content/site changes:** removals, migrations, redesigns, templates, internal links, product availability.
9. **Check manual/security issues:** manual actions, hacked content, malware, downtime.
10. **Check confirmed search updates:** only after site-specific causes are investigated; verify rollout dates from official sources when possible.

## Pattern clues

- Sitewide sudden drop after deploy -> technical/tracking/deployment first.
- One directory/template -> shared template/indexation/content change.
- Impressions stable, clicks down -> SERP CTR/appearance/intent/competition may be more relevant than indexing.
- Impressions down for one topic -> demand, relevance, competition, or content quality may be involved.
- Indexed count changes without performance impact -> may be normal URL cleanup; evaluate affected canonical pages, not just count.

## Quick decision aid

| Observation | First suspects | First check |
|---|---|---|
| Drop starts the day of a deploy/migration | noindex, robots, canonicals, redirects, rendering | `migration.md`; fetch live HTML and headers for a lost URL |
| Sharp drop on one date, no release | tracking change, outage, manual/security issue, confirmed update | analytics tag audit; Search Console messages; official update dashboards |
| Gradual decline over months | content freshness/quality, competitors, demand, internal-link decay | query-level comparison against SERP leaders |
| Indexing errors rising | soft 404s, duplicate/alternate pages, crawl traps, server errors | Page Indexing report grouped by reason, then sample URLs |
| Crawled but not indexed at scale | low unique value, duplication, weak internal links | compare indexed vs not-indexed page templates |
| Clicks down, impressions flat | SERP features, snippet changes, rank slips, AI answers | position and CTR by query cohort |

## Output

State:

- strongest evidenced causes;
- ruled-out causes;
- remaining hypotheses ranked by confidence, not drama;
- exact checks needed to falsify each hypothesis;
- rollback/fix recommendation when a recent technical change is implicated.
