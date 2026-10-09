# Example: `/seo page https://example.com/pricing` (illustrative output)

> Illustrative format only; not a real site.

## Executive summary
The pricing page is indexable and returns 200, but its canonical points to the homepage, which likely prevents the page from being indexed under its own URL. The title and H1 are generic. Evidence is from the fetched HTML only; no Search Console data was available.

## Findings

### [P0] Canonical points to the homepage  (Confidence: High)
- **Evidence:** `<link rel="canonical" href="https://example.com/">` in server HTML of `/pricing`
- **Why it matters:** Signals that `/pricing` is a duplicate of `/`, so it may not be indexed or shown for pricing queries.
- **Fix:** Emit a self-referencing canonical from the shared layout using the production origin plus the route path.
- **Verify:** Re-fetch the page; run `seo_scan.py https://example.com/pricing` and confirm one canonical equal to the final URL; check URL Inspection.

### [P2] Generic title  (Confidence: Medium)
- **Evidence:** `<title>Home | Example</title>` on `/pricing`
- **Why it matters:** Reduces relevance clarity and click appeal for pricing intent.
- **Fix:** Use a page-specific title that matches the page's purpose and visible H1.
- **Verify:** Re-scan and inspect the rendered title.

## Action plan
1. Fix canonical generation in the shared layout (affects all routes).
2. Add per-route title/description defaults.
3. Re-run `build_scan.py` on the build output to catch the same issue elsewhere.

## Data gaps
- Search Console indexing status for `/pricing`.
