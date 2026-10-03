# AI search / answer-engine visibility

## Baseline

Do not treat “GEO/AEO” as a separate magic layer. For Google AI features, current primary guidance states that foundational SEO still applies and there are no special additional technical requirements beyond being indexable/eligible to appear with a snippet.

Optimize for usefulness, accessibility, clarity, evidence, and entity understanding rather than tricks.

## What to audit

### Access and eligibility

- Is the page crawlable/indexable by the target engine?
- Can the engine access the content without login or blocked rendering resources?
- Are snippet controls intentionally configured?
- Does the canonical page expose the core answer/content clearly?

### Citability and information quality

Prefer content that is easy to verify and cite:

- original facts, first-party data, examples, or methodology;
- clear definitions and direct answers near the relevant section;
- descriptive headings and stable section anchors where useful;
- explicit units, dates, scope, and assumptions;
- trustworthy external citations for claims that need them;
- author/company provenance when materially relevant;
- structured data that accurately describes entities.

Do not mechanically rewrite every paragraph into Q&A format.

### Entity and brand clarity

Ensure the site clearly communicates who/what it is, what it offers, and how key entities relate. Organization/site-name/business/profile structured data can support machine understanding when accurate.

### Multimodal content

Useful original images, charts, video, transcripts, and demonstrations can improve user value and give search systems richer material. Optimize them for accessibility and discovery rather than adding decorative media.

## `llms.txt` and similar files

Treat as optional/experimental unless the target platform explicitly documents support. Do not call it a Google ranking factor or requirement for AI Overviews/AI Mode.

If the user wants one, make it concise, factual, maintainable, and secondary to normal crawl/index/content quality.

## Measuring AI visibility

Do not fabricate “AI visibility scores.” Depending on available data, use:

- referral/analytics segments from AI assistants where identifiable;
- Search Console data for Google Search overall;
- repeatable manual/automated query sampling with dated evidence;
- brand/entity citation tracking from a clearly defined query set;
- conversion/engagement outcomes from those visits.

AI answer outputs can vary by user, time, model, and query formulation. Treat sampled presence as observational, not guaranteed coverage.

## AI crawler controls

Distinguish crawlers by purpose, and verify current user-agent tokens in each vendor's own documentation before editing robots.txt:

- **Search/answer retrieval** crawlers (appear in AI answers with citations) — blocking them removes eligibility to be cited.
- **Model-training** crawlers/tokens — blocking is a content-licensing choice, not an SEO fix.
- **User-initiated fetchers** — often do not follow robots.txt the same way; check vendor docs.

Present this as a business trade-off with the user. Do not copy-paste long "block all AI bots" lists from the web, and never claim a robots.txt rule enforces access control.
