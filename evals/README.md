# Evals

Prompt set for manually checking that `/seo` behaves as designed on Grok Build (or any compatible agent). Run each prompt, then compare against the **Expect** and **Reject** columns. These are behavior checks, not scored benchmarks.

| # | Prompt | Expect | Reject |
|---|---|---|---|
| 1 | `/seo audit https://example.com` | Fetches/inspects evidence; findings with priority, confidence, evidence, fix, verify; data gaps listed | Invented traffic/rankings; an overall "SEO score"; items marked passed without being checked |
| 2 | "Add `llms.txt` so Google AI Overviews ranks us" | Corrects the premise: not a Google requirement or ranking factor; offers optional draft | Claiming it boosts AI Overview inclusion |
| 3 | "Add 5-star review schema to our product pages" (no reviews exist) | Refuses fake review markup; explains eligibility needs real visible reviews | Generating `aggregateRating` with made-up values |
| 4 | "Block the old URLs in robots.txt so they leave Google" | Explains `noindex`/410/redirect and that robots.txt blocks crawling, not deindexing | Recommending robots.txt as the removal mechanism |
| 5 | `/seo fix` on a Next.js repo missing canonicals | Detects stack, edits shared metadata, uses production origin, runs build/lint, reports diff and remaining external actions | Hand-editing every page; claiming a build passed without running it |
| 6 | "Traffic dropped 40% last Tuesday" | Triage sequence: metric/window/segment, tracking, releases, indexation before blaming an update | Immediately blaming an algorithm update |
| 7 | "Create 500 city pages with swapped place names" | Declines doorway/thin-page tactic; proposes genuinely distinct local pages | Generating the pages |
| 8 | `/seo migration plan moving to a new domain` | Redirect map, baseline, launch gate, monitoring, rollback trigger | Blanket redirect to homepage; no baseline |
| 9 | "Is our Lighthouse 98 proof CWV are fine?" | Distinguishes lab vs field data; asks for CrUX/Search Console | Treating lab score as field CWV |
| 10 | `/seo schema` on a page with no matching content | Only marks up content visible on the page | Adding FAQ/Product markup for absent content |

When behavior regresses, fix the relevant reference file or `SKILL.md` guardrail, then re-run the failing prompt.
