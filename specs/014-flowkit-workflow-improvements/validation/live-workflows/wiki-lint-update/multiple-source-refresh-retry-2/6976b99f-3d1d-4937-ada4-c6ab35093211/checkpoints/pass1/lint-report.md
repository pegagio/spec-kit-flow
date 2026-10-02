# Wiki Lint Report — 2026-10-01

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | pages/errors.md | Claim "Invalid UTF-8 exits 1 and writes a partial result to stdout. (S002)" disagrees with registered docs/error-contract.md: exit 2 with stderr and no stdout. | Re-ingest docs/error-contract.md (S002) and reassess pages/errors.md. Report-only; no fix applied. |
| 2 | stale | semantic | pages/normalization.md | Claim "Normalization collapses interior whitespace and deletes blank lines. (S001)" disagrees with registered docs/normalization-contract.md: preserve interior whitespace and every logical blank line including trailing blank lines. | Re-ingest docs/normalization-contract.md (S001) and reassess pages/normalization.md. Report-only; no fix applied. |
