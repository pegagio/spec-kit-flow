# Wiki Lint Report — 2026-10-01

Full pass, empty arguments. Configuration: wiki/, citations required, 90-day staleness, index-and-links mechanical repair. Both INDEX.md and index.md exist and identify the same file. All index entries, relative links, source IDs, metadata, and reciprocal links are valid. Page dates are 30 days old; no age finding applies. No mechanical fix is needed.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|---|---|---|---|---|
| 1 | stale | semantic | errors.md | “Invalid UTF-8 exits 1 and writes a partial result to stdout. (S002)” disagrees with registered docs/error-contract.md: invalid UTF-8 exits 2 with stderr and no stdout. | Suggested only: re-ingest docs/error-contract.md (S002); no semantic edit applied by lint. |
| 2 | stale | semantic | normalization.md | “Normalization collapses interior whitespace and deletes blank lines. (S001)” disagrees with registered docs/normalization-contract.md: preserve interior whitespace and every logical blank line including trailing blank lines. | Suggested only: re-ingest docs/normalization-contract.md (S001); no semantic edit applied by lint. |

Counts: index-drift 0; links 0; orphans 0; contradictions 0; stale 2; citations 0. Fixes applied: 0. Suggested actions: 2.

Next action: run speckit-flow-wiki-ingest with docs/error-contract.md to resolve the S002 stale claim.
