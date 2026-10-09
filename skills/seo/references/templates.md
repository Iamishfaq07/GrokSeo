# Templates

Starting points only. Fill every value from real, visible page data; never ship placeholder values.

## Audit report skeleton

```markdown
## Executive summary
<2-6 sentences: biggest blockers/opportunities, evidence quality, what first>

## Findings
### [P1] <short title>  (Confidence: High)
- **Evidence:** <URL / file:line / header / report>
- **Why it matters:** <user/search impact, no ranking promises>
- **Fix:** <concrete action>
- **Verify:** <how to confirm>

## Action plan
1. <dependency-ordered step>

## Data gaps
- <only what materially limits conclusions>
```

## Pre-launch gate (tick only what was actually checked)

- [ ] Production is not `noindex` / `Disallow: /` / staging-auth
- [ ] robots.txt and sitemap are production versions; sitemap URLs return 200 and are canonical
- [ ] Redirect map covers old URLs (301/308, no chains); http→https and host variants normalized
- [ ] Unique title + description + canonical per indexable template
- [ ] Server HTML contains primary content and crawlable `<a href>` links
- [ ] Real 404/410 for missing pages (no soft-404)
- [ ] Structured data valid and matches visible content
- [ ] Analytics + Search Console verified; sitemap submitted
- [ ] Field/lab CWV baseline recorded

## JSON-LD templates

Organization + WebSite graph (use real values; add `sameAs` only for real profiles):

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {"@type": "Organization", "@id": "https://example.com/#org", "name": "Example Co",
     "url": "https://example.com/", "logo": "https://example.com/logo.png"},
    {"@type": "WebSite", "@id": "https://example.com/#website", "url": "https://example.com/",
     "name": "Example Co", "publisher": {"@id": "https://example.com/#org"}}
  ]
}
```

BreadcrumbList:

```json
{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
  {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://example.com/"},
  {"@type": "ListItem", "position": 2, "name": "Guides", "item": "https://example.com/guides/"}
]}
```

Article (author/dates must be real and visible on the page):

```json
{"@context": "https://schema.org", "@type": "Article", "headline": "<page headline>",
 "datePublished": "<ISO 8601>", "dateModified": "<ISO 8601>",
 "author": {"@type": "Person", "name": "<real author>"},
 "image": ["<absolute image URL>"], "mainEntityOfPage": "<canonical URL>"}
```

Product with offer (price/availability must match the page; omit ratings unless real, visible reviews exist):

```json
{"@context": "https://schema.org", "@type": "Product", "name": "<name>", "image": ["<url>"],
 "sku": "<sku>", "offers": {"@type": "Offer", "price": "<number>", "priceCurrency": "<ISO 4217>",
 "availability": "https://schema.org/InStock", "url": "<canonical URL>"}}
```

## Redirect map CSV

```csv
old_url,new_url,status,notes
/old-page,/new-page,301,content merged
```

## robots.txt baseline

```text
User-agent: *
Disallow: /cart/
Disallow: /internal-search/

Sitemap: https://example.com/sitemap.xml
```

Block only low-value crawl traps; never block CSS/JS needed for rendering, and never rely on robots.txt to deindex.
