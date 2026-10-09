# Contributing

Contributions should improve correctness, portability, evidence quality, or implementation coverage without turning the root `SKILL.md` into a giant prompt.

## Rules

- Keep the root skill as a router and move specialist detail into focused `references/` files.
- Prefer current primary search-engine documentation for claims that can change.
- Do not add ranking-factor folklore as fact.
- Do not add manipulative SEO tactics, fabricated review/schema data, or mass low-value content patterns.
- Avoid arbitrary hard thresholds unless they come from a stable technical limit or are clearly framed as a heuristic.
- Scripts should remain dependency-light and must clearly state limitations.
- New framework guidance belongs in `references/implementation.md` unless it becomes large enough to justify a dedicated reference.

Run before opening a PR:

```bash
python scripts/validate_skill.py
python -m py_compile skills/seo/scripts/*.py
python -m unittest discover -s tests
python skills/seo/scripts/repo_seo_scan.py . --json
```

For Grok Build users, also run `grok inspect` and exercise `/seo` on at least one representative task.
