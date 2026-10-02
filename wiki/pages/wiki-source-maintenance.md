---
title: Wiki source maintenance
type: concept
sources: [S021]
updated: 2026-10-02
---

# Wiki source maintenance

The separately invoked Wiki Lint Update design starts with fresh lint and requires no active feature. An optional scope narrows the check; stale page citations identify registered source identities, not pages to ingest. Shared sources are deduplicated and one authorized source is refreshed per pass before re-linting. Registered remote URLs require explicit operator authorization. (S021)

All lint findings remain visible. Safe independent stale-source refreshes may proceed while unrelated inconsistencies or structural issues remain, but authority-conflicted claims cannot be silently overwritten. Unavailable or unauthorized sources, unsupported repairs, and age-only timestamp changes remain reported for resolution. (S021)

Progress requires substantive prior-finding resolution and a finite bound. No progress or exhausted capacity preserves pending sources, partial changes, every remaining issue, suggested actions, and the smallest safe resumption action. Clean requires a successful fresh lint with no unresolved findings, not ingestion success. Feature artifacts, roadmap state, Git actions, and other workflow invocation are outside this design's scope. (S021)

## Related pages

- [Workflow lifecycle](./workflow-lifecycle.md)
