---
title: Preimplementation review gates
type: concept
sources: [S007, S008, S009]
updated: 2026-09-24
---

# Preimplementation review gates

Clarification runs one bounded session against the operator-selected active specification. Human answers are incorporated into the specification before the next question; the result distinguishes resolved, outstanding, and deferred ambiguity. The current five-question cap is a session boundary, not proof of planning readiness. (S007)

The operator chooses another clarification session, planning readiness, or deferral. Continuing uses the same feature; deferral stays explicit rather than becoming a product default. Neither an empty question set nor an ended session selects planning automatically. (S007)

Planning requires an operator-identified clarified feature and explicit confirmation that the specification was reviewed. The readiness choices are plan, return to clarification, and defer; unresolved product ambiguity cannot be settled by a technical design assumption. A completed plan leaves plan, research, data model, contracts, and quickstart for review without generating tasks. (S008)

Task generation is a separate step for an operator-selected planned feature. It proposes dependency-ordered work from reviewed design artifacts, reports task coverage and unexpected human actions, and leaves the proposal for review. The operator may choose separate analysis, return to planning, explicit task amendment, or deferral; no route begins implementation directly. (S009)

## Related pages

- [Workflow lifecycle](./workflow-lifecycle.md)
