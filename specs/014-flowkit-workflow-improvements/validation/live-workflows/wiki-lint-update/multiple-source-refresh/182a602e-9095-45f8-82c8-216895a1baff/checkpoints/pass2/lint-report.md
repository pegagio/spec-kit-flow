# Wiki Lint Report — 2026-10-01

Full pass, pass 2. Three findings: stale 1, orphans 2; contradictions 0, links 0, index-drift 0, citations 0. No fixes applied; all three findings are suggested only. Configuration uses the validated defaults with the installed configuration overlay; no environment overrides are present. Both pages are younger than the 90-day age threshold and neither source was re-ingested after its page update. The remaining stale finding is substantive source divergence. The normalization page now agrees with S001. `INDEX.md` resolves to the existing lowercase `index.md` on this case-insensitive filesystem; its entries exactly match valid page metadata, so no repair is needed.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | pages/errors.md | `Invalid UTF-8 exits 1 and writes a partial result to stdout. (S002)` contradicts registered `docs/error-contract.md`: invalid UTF-8 exits 2 with a concise stderr message and no stdout. | Suggested only: ingest `docs/error-contract.md` (S002), then verify the error claim against the approved contract. |
| 2 | orphans | structural | pages/errors.md | No other page links to `pages/errors.md`; INDEX links do not count. | Suggested only: decide whether a sourced cross-reference from normalization is useful, then add it during ingestion if justified. |
| 3 | orphans | structural | pages/normalization.md | No other page links to `pages/normalization.md`; INDEX links do not count. | Suggested only: decide whether a sourced cross-reference from errors is useful, then add it during ingestion if justified. |
