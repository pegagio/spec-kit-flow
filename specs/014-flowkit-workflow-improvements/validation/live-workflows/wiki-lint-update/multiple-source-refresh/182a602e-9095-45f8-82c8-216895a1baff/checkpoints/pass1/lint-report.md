# Wiki Lint Report — 2026-10-01

Full pass. Five findings: stale 2, orphans 2, index-drift 1; contradictions 0, links 0, citations 0. One allowlisted index repair applied; four semantic/structural findings remain suggested only. Dates are 30 days old, below the 90-day threshold; source registry dates do not postdate pages. The stale findings below identify substantive divergence from the registered local source contracts.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | pages/errors.md | `Invalid UTF-8 exits 1 and writes a partial result to stdout. (S002)` contradicts registered `docs/error-contract.md`: invalid UTF-8 exits 2 with stderr and no stdout. | Suggested only: ingest `docs/error-contract.md` (S002) and verify the error claim against the approved contract. |
| 2 | stale | semantic | pages/normalization.md | `Normalization collapses interior whitespace and deletes blank lines. (S001)` contradicts registered `docs/normalization-contract.md`: preserve interior whitespace and every logical blank line, including trailing blank lines. | Suggested only: ingest `docs/normalization-contract.md` (S001) and verify whitespace/newline claims against the approved contract. |
| 3 | orphans | structural | pages/errors.md | No other page links to `pages/errors.md`; INDEX links do not count. | Suggested only: decide whether a sourced cross-reference from normalization is useful, then add it during ingestion if justified. |
| 4 | orphans | structural | pages/normalization.md | No other page links to `pages/normalization.md`; INDEX links do not count. | Suggested only: decide whether a sourced cross-reference from errors is useful, then add it during ingestion if justified. |
| 5 | index-drift | mechanical | INDEX.md | Required `INDEX.md` was absent; both valid pages existed only in lowercase `index.md`. | Applied: generated `INDEX.md` from valid frontmatter, grouped by type; preserved lowercase `index.md`. |
