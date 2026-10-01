---
title: Closeout and verification boundary
type: decision
sources: [S013, S021]
updated: 2026-09-30
---

# Closeout and verification boundary

## Earlier feature contracts

The following cited contracts preserve earlier feature intent; Feature 014's prospective refinements are distinguished below. (S021)

Closeout starts from an operator-identified converged feature, but convergence does not itself complete the feature. A separately approved feature-completion operation must be available; if it is missing, closeout stops before roadmap or wiki changes and does not substitute specification drafting. (S013)

After that operation, roadmap debrief precedes a proposed verification patch. The operator reviews the debrief and exact patch before roadmap write applies only the approved change; return, deferral, or an invalid choice stops the write. (S013)

After an approved roadmap patch, the operator selects durable sources for wiki ingestion and runs wiki lint before commit-readiness review. Unresolved lint findings or blockers stop or return to the affected workflow. A ready-for-explicit-commit disposition does not commit, integrate Git, or accept project work. (S013)

## Feature 014 completion and maintenance

Close Out assesses selected-feature convergence and completion evidence. A clearly converged existing Draft specification may be changed in place to Complete and debriefed without a redundant operation-availability or status-edit gate; ambiguous evidence or authority blocks. Routine debrief corrections flow through affected artifact layers and fresh reassessment until an exact patch is supported or a bounded stop occurs. (S021)

The exact roadmap verification patch still needs explicit approval. Newly approved and already verified entries both receive curated single-source wiki ingestion, lint, and coverage checks before automatic commit-readiness reporting. Source-backed wiki findings may trigger another bounded pass only when prior gaps are substantively resolved within the authorized source set; conflicts, unsupported repair, unavailable sources, age-only warnings, no progress, or exhausted capacity block. (S021)

One final report preserves completed evidence, questions, original gate choices, and partial changes. Readiness does not commit, integrate Git, or accept the feature. (S021)

**Accepted supersession**: S013 requires a separately approved completion operation and a human commit-readiness decision; S021 authorizes evidence-backed in-place completion and automated readiness reporting while retaining exact roadmap approval and separate Git/acceptance authority. S013 remains historical feature evidence. (S013, S021)

## Related pages

- [Workflow lifecycle](./workflow-lifecycle.md)
