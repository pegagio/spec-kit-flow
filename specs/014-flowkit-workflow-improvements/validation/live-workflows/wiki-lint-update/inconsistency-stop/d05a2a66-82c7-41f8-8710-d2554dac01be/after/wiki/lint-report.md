# Wiki Lint Report — 2026-10-01

Full configured wiki pass; empty arguments.

| # | Check | Severity | Page | Finding | Suggested fix |
|---|-------|----------|------|---------|---------------|
| 1 | contradictions | semantic | pages/errors.md | > ⚠ conflict: S001 requires exit 1 with partial stdout; S002 requires exit 2 with no stdout. Both are authoritative and no precedence decision exists. | Operator must decide which invalid UTF-8 policy governs S001/S002, then reconcile the approved sources and cited pages; report-only, not applied. |
| 2 | contradictions | semantic | pages/errors.md + pages/normalization.md | Linked normalization.md states invalid UTF-8 exits 1 with partial stdout (S001); errors.md states invalid UTF-8 exits 2 with no stdout (S002). The registered source contracts contain both incompatible equal-authority policies. | Operator must decide which invalid UTF-8 policy governs S001/S002, then reconcile the approved sources and cited pages; report-only, not applied. |

Counts: contradictions 2; index-drift 0; links 0; orphans 0; stale 0; citations 0. Fixes applied: 0. Suggestions: 2. INDEX.md exists and aliases index.md; no index repair is needed.

Next action: operator decides whether invalid UTF-8 must exit 1 with partial stdout (S001) or exit 2 with no stdout (S002), and authorizes reconciliation of the source contracts and cited pages.
