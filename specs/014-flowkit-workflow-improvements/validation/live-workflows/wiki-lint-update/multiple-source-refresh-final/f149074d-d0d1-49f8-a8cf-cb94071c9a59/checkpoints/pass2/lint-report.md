# Wiki Lint Report — 2026-10-01

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | errors.md | STALE-S002-ERRORS: “Invalid UTF-8 exits 1 and writes a partial result to stdout.” contradicts registered S002 docs/error-contract.md: invalid UTF-8 exits 2 with concise stderr and no stdout. | Suggested only: ingest docs/error-contract.md (S002), then run a fresh full lint pass. |
