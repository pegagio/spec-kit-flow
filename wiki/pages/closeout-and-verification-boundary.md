---
title: Closeout and verification boundary
type: decision
sources: [S013]
updated: 2026-09-24
---

# Closeout and verification boundary

Closeout starts from an operator-identified converged feature, but convergence does not itself complete the feature. A separately approved feature-completion operation must be available; if it is missing, closeout stops before roadmap or wiki changes and does not substitute specification drafting. (S013)

After that operation, roadmap debrief precedes a proposed verification patch. The operator reviews the debrief and exact patch before roadmap write applies only the approved change; return, deferral, or an invalid choice stops the write. (S013)

After an approved roadmap patch, the operator selects durable sources for wiki ingestion and runs wiki lint before commit-readiness review. Unresolved lint findings or blockers stop or return to the affected workflow. A ready-for-explicit-commit disposition does not commit, integrate Git, or accept project work. (S013)

## Related pages

- [Workflow lifecycle](./workflow-lifecycle.md)
