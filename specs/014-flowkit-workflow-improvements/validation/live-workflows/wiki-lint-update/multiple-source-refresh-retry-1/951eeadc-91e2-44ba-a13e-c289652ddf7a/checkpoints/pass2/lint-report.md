# Wiki Lint Report — 2026-10-01

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | errors.md | The claim “Invalid UTF-8 exits 1 and writes a partial result to stdout. (S002)” disagrees with registered source S002 `docs/error-contract.md`: invalid UTF-8 exits 2 with a concise stderr message and no stdout. | Suggested only: re-ingest `docs/error-contract.md` with `/speckit.flow-wiki.ingest docs/error-contract.md`, then run fresh lint. |
