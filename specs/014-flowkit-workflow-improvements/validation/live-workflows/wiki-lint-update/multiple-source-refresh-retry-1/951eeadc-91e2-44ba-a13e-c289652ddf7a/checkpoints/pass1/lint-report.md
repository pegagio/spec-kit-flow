# Wiki Lint Report — 2026-10-01

Full pass; configuration validated. `wiki/INDEX.md` exists and aliases `wiki/index.md` on this filesystem. Both indexed pages exist, have valid metadata and registered citations, and link reciprocally. Page ages are 30 days, below the 90-day threshold; registry ingestion dates equal page update dates. The findings below identify substantive claims superseded by their approved registered source contracts, rather than timestamp staleness. No conflicting page pair or conflict marker was found.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | pages/errors.md | S002 page claim “Invalid UTF-8 exits 1 and writes a partial result to stdout.” conflicts with approved `docs/error-contract.md`: invalid UTF-8 exits 2 with stderr and no stdout. | Suggested only: run `/speckit.flow-wiki.ingest docs/error-contract.md`, then independently lint the refreshed claim. |
| 2 | stale | semantic | pages/normalization.md | S001 page claim “Normalization collapses interior whitespace and deletes blank lines.” conflicts with approved `docs/normalization-contract.md`: preserve interior whitespace and every logical blank line, including trailing blank lines. | Suggested only: run `/speckit.flow-wiki.ingest docs/normalization-contract.md`, then independently lint the refreshed claim. |

Counts: index-drift 0; links 0; orphans 0; contradictions 0; stale 2; citations 0. Mechanical fixes applied: 0. Semantic refresh suggestions: 2. No index regeneration or link replacement is needed.

Next action: `/speckit.flow-wiki.ingest docs/error-contract.md` to resolve the S002 stale claim.
