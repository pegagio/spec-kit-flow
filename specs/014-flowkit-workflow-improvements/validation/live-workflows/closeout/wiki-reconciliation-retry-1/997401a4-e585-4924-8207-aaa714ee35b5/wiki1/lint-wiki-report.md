# Wiki Lint Report — 2026-10-01

Full unfiltered six-check pass. Semantic findings are report-only.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | stale | semantic | errors.md | The page says "leaves these product decisions open" and lists AMB-INPUT, AMB-OUTPUT, AMB-ERRORS and AMB-SIZE as questions. Current registered S002 docs/error-contract.md explicitly resolves all four: one local path, stdout only/no stdin/input mutation/output file, exit 2 with stderr/no stdout, and no explicit product size limit. Equal updated/ingestion dates do not make these substantive claims current. | Re-ingest docs/error-contract.md through the declared Wiki Curator ingestion step to update the S002 error-policy claims while preserving source identity. Suggested only; no fix applied. |
