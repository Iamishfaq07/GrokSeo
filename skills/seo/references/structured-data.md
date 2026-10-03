# Structured data

## Core rule

Structured data describes content that actually exists on the page. It does not create eligibility for content or claims that are absent, misleading, private, or fabricated.

Prefer JSON-LD when it fits the stack and current search-engine guidance, but preserve existing valid formats unless there is a reason to migrate.

## Workflow

1. Identify page/entity type.
2. Detect existing markup and duplicate/conflicting entities.
3. Validate JSON syntax and Schema.org vocabulary.
4. Check the current search engine's feature-specific required/recommended properties.
5. Confirm every material property matches visible/current page data.
6. Validate using available official testing tools or validators.
7. Recheck rendered output after implementation.

## Common entities

Use only when applicable, for example:

- `Organization` / suitable subtype;
- `WebSite` for site identity;
- `BreadcrumbList`;
- `Article` / `NewsArticle` / `BlogPosting`;
- `Product`, `Offer`, `AggregateOffer`, `ProductGroup`/variants where appropriate;
- `LocalBusiness` subtype;
- `Event`;
- `JobPosting`;
- `SoftwareApplication`;
- `VideoObject`;
- `Dataset`;
- `ProfilePage` or `QAPage` only for pages that truly match those concepts.

Do not assume every Schema.org type produces a search rich result.

## Entity graph quality

Prefer a coherent graph with stable `@id` identifiers where useful, rather than many disconnected or duplicated blobs.

Keep business identity consistent across organization/local/business entities and visible content. Link related entities semantically only when true.

## High-risk mistakes

Never:

- invent reviews/ratings;
- mark up hidden testimonials as if they are current visible reviews;
- put product prices/availability in schema that disagree with the page;
- use local business data for a location that is not real;
- mark generic pages as articles/products/jobs merely to get a feature;
- copy schema snippets without verifying current eligibility rules.

## Deprecation/freshness

Search appearance features change. Before adding a feature-specific type solely for a Google rich-result benefit, verify current Google documentation. A valid Schema.org type may still have no Google rich-result treatment.
