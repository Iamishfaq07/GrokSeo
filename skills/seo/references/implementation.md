# SEO implementation in codebases

## Goal

Make framework-native changes that survive future development. Prefer fixing shared templates/components/configuration over hand-editing many generated pages.

## 1. Detect the stack

Inspect project files before editing. Determine:

- framework/runtime (Next.js, Nuxt, SvelteKit, Astro, Remix/React Router, Gatsby, Rails, Django, Laravel, static HTML, CMS theme, etc.);
- router model and route generation;
- SSR/SSG/ISR/CSR behavior;
- metadata/head API;
- sitemap/robots generation;
- image component/CDN behavior;
- localization and content source;
- test/lint/build commands.

Do not impose Next.js patterns on a non-Next project.

## 2. Metadata implementation

Prefer shared typed metadata helpers/templates where the framework supports them.

Ensure route-level output can produce accurate:

- title;
- meta description where useful;
- canonical;
- robots directives;
- Open Graph/social metadata if requested (not a direct SEO substitute);
- locale alternates/hreflang when relevant;
- structured data.

Avoid duplicate head managers or conflicting metadata systems.

## 3. Canonical URL generation

Build canonicals from a trusted production origin, not the current request host when that could be staging/preview/custom-domain dependent. Normalize trailing slash/path rules consistently with routing and redirects.

Do not blindly strip meaningful parameters from pages intended to be distinct.

## 4. Robots and environment safety

Preview/staging environments may use `noindex`, authentication, or restricted access, but production must not inherit those controls accidentally.

Where possible, test environment-specific robots behavior in CI/build output.

## 5. Sitemaps

Generate from the canonical content source/routes rather than crawling the deployed site when the app already knows its URLs. Exclude redirects, errors, private/noindex pages, and infinite parameter combinations.

Keep timestamps meaningful.

## 6. Structured data code

Centralize schemas in small helpers/components. Serialize safely. Ensure dynamic values come from the same source of truth as visible page content.

Never hardcode fake ratings, stock, prices, dates, authors, or addresses.

## 7. Rendering

For important indexable content, prefer SSR/SSG or otherwise ensure robust server-delivered content when the framework permits. Avoid unnecessary client-only rendering for primary copy, navigation, or metadata.

## 8. Internal linking

Use the framework's real link primitive that emits an anchor with `href`. Fix broken/non-canonical targets at the source data or shared component when possible.

## 9. Performance fixes

Prioritize user-centric root causes:

- reduce server latency and blocking dependencies;
- optimize the LCP resource and preload only when justified;
- reduce unnecessary JS/hydration;
- split heavy components;
- size media and stabilize layout;
- avoid loading third-party scripts earlier than needed.

Do not chase Lighthouse 100 at the cost of product behavior.

## 10. Framework notes

### Next.js App Router
Prefer the framework metadata APIs (`metadata` / `generateMetadata`) and route handlers/metadata files for `robots.txt` and sitemap where appropriate. Verify server-rendered output for dynamic routes. Avoid duplicate manual `<head>` injection.

### Next.js Pages Router
Use the framework head mechanism consistently and centralize repeated metadata. Ensure dynamic pages resolve canonical metadata during SSR/SSG when intended.

### Nuxt
Use `useSeoMeta` / `useHead` in shared layouts and per-page composables; set `site.url` (or the SEO module equivalent) so canonicals and sitemaps use the production origin. Verify with `nuxt generate` or a production build, not dev mode.

### SvelteKit
Put per-route `<svelte:head>` data behind `load` results so it renders on the server; generate sitemap/robots via `+server.ts` endpoints; return real `error(404)` for missing params.

### Astro
Centralize `<head>` in a layout component; set `site` in `astro.config` for canonical/sitemap generation; prefer static output and inspect `dist/` (try `build_scan.py dist/`).

### WordPress
Prefer one established SEO plugin over hand-edited theme tags; avoid duplicate title/canonical output from theme plus plugin; check that "discourage search engines" is off in production and that attachment/tag archives follow an intentional indexing policy.

### Shopify
Edit theme Liquid for titles/meta/schema rather than injecting via JS; handle duplicate product URLs via the canonical Shopify emits (collection-scoped product paths); keep variant and filter URLs from creating thin indexable duplicates.

### SPA-only React/Vue/etc.
Assess whether prerendering/SSR is warranted for public search landing pages. If remaining CSR, verify crawler-rendered content, real statuses via server/fallback rules, and crawlable navigation.

### Static-site generators
Prefer compile-time route metadata, sitemap generation, and broken-link checks. Inspect built HTML, not just templates.

## 11. Verification before completion

Run the smallest relevant checks available:

- formatting/lint;
- type checks;
- targeted tests;
- production build for metadata/routing changes;
- inspect built/server HTML for title/canonical/robots/schema;
- run bundled scanners as supplemental checks;
- inspect `git diff` for unintended copy/design changes.

If a check cannot run, state that clearly and do not imply it passed.
