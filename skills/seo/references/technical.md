# Technical SEO reference

## HTTP and redirects

- Important canonical pages should normally return `200`.
- Missing content should return a meaningful `404`/`410`, not a soft-404 `200` page.
- Permanent moves should use an appropriate server-side permanent redirect; avoid long chains and loops.
- Normalize protocol/host/path variants consistently.
- Preserve useful query parameters only when they represent intentional distinct content.

## robots.txt vs noindex

- `robots.txt` controls crawler access; it is not a reliable removal mechanism for already-known URLs.
- `noindex` is a page/header indexing directive and usually must be crawlable to be observed.
- Do not block CSS/JS required for rendering important content without a reason.
- Keep private content behind authentication; search directives are not access control.

## Canonicals

Canonical signals should agree across:

- redirect destination;
- `<link rel="canonical">`;
- sitemap URL;
- internal links;
- hreflang annotations.

Use canonicals for duplicate or substantially similar representations, not as a universal patch for weak pages. Avoid canonicalizing distinct localized pages to another language/region version.

## Sitemaps

Sitemaps should contain canonical URLs intended for search, generally excluding redirects, errors, and `noindex` URLs. Split large sitemaps according to protocol/engine limits and use sitemap indexes when needed.

`lastmod` should reflect meaningful content changes when used; do not churn dates merely to look fresh.

## JavaScript SEO

For JS frameworks:

- prefer server-rendered/static-rendered critical content where practical;
- verify initial HTML and rendered HTML;
- ensure crawlable anchors use real `href` values;
- avoid source-vs-rendered canonical contradictions;
- return real error status semantics for missing routes;
- do not rely on user interaction to expose essential content or links;
- test hydration/runtime failures.

Search engines differ in rendering capability. Server-rendering improves robustness beyond any one engine.

## Internal links

A strong internal link should be:

- crawlable;
- contextually useful to a person;
- pointed at the canonical destination;
- descriptively anchored without stuffing;
- placed where it supports navigation or understanding.

Do not manufacture sitewide exact-match links solely for keywords.

## Pagination, filters, faceted navigation

On e-commerce/catalog/search sites:

- decide which facets deserve indexable landing pages based on durable user demand and unique value;
- keep combinatorial filter explosions from creating endless crawlable URLs;
- use consistent canonicals and internal links;
- avoid blanket rules that accidentally hide valuable categories/products;
- test sorting/filter parameters and crawler paths at scale.

## Core Web Vitals

Use field data when possible. Distinguish:

- LCP: loading of the main visible content;
- INP: interaction responsiveness;
- CLS: unexpected layout movement.

Baseline good thresholds (re-verify if current rules matter): LCP <=2.5s, INP <=200ms, CLS <=0.1 at the 75th percentile.

Common root causes:

- LCP: slow TTFB, render-blocking resources, oversized hero media, client rendering, poor caching/CDN configuration;
- INP: long main-thread tasks, heavy hydration, large JS bundles, expensive event handlers;
- CLS: unsized media/ads/embeds, late font/layout swaps, injected content above existing content.

## Images and media

- meaningful images need useful alt text; decorative images should not receive spammy descriptions;
- provide dimensions/aspect ratio to reduce layout shifts;
- use modern formats/compression where compatible;
- responsive images should match display needs;
- lazy-load below-the-fold media, not the primary LCP asset by default;
- use image/video structured data only when it matches the page and current eligibility.

## Security and deployment

Check for search-impacting operational issues:

- mixed-content or HTTPS problems;
- accidental basic-auth removal or staging exposure;
- environment-specific `noindex` leaking to production;
- production robots.txt copied from staging;
- CDN/cache serving stale metadata;
- edge redirects changing canonical/locale behavior.
