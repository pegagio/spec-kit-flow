---
title: Preimplementation review gates
type: concept
sources: [S007, S008, S009, S021]
updated: 2026-09-30
---

# Preimplementation review gates

## Earlier feature contracts

The following cited contracts preserve earlier feature intent; Feature 014's prospective refinements are distinguished below. (S021)

Clarification runs one bounded session against the operator-selected active specification. Human answers are incorporated into the specification before the next question; the result distinguishes resolved, outstanding, and deferred ambiguity. The current five-question cap is a session boundary, not proof of planning readiness. (S007)

The operator chooses another clarification session, planning readiness, or deferral. Continuing uses the same feature; deferral stays explicit rather than becoming a product default. Neither an empty question set nor an ended session selects planning automatically. (S007)

Planning requires an operator-identified clarified feature and explicit confirmation that the specification was reviewed. The readiness choices are plan, return to clarification, and defer; unresolved product ambiguity cannot be settled by a technical design assumption. A completed plan leaves plan, research, data model, contracts, and quickstart for review without generating tasks. (S008)

Task generation is a separate step for an operator-selected planned feature. It proposes dependency-ordered work from reviewed design artifacts, reports task coverage and unexpected human actions, and leaves the proposal for review. The operator may choose separate analysis, return to planning, explicit task amendment, or deferral; no route begins implementation directly. (S009)

## Feature 014 core-skill output loops

Clarify begins with the standard skill session, then assesses significant remaining ambiguity and repeats while prior ambiguities are resolved within a finite bound. The five-question limit remains per session and every substantive answer comes from the operator; clarification does not declare planning readiness. (S021)

Plan delegates prerequisites, research, design generation, and constitutional gates to the core skill. Its wrapper checks required/applicable outputs are present and populated, respects justified inapplicability, and feeds exact missing files or placeholders back for correction. This is output verification rather than design review. (S021)

Tasks similarly retries format, section, dependency, and story-coverage gaps while preserving task IDs, completed work, and reviewed design. Unchecked implementation tasks are not generation failures. Material product questions, missing prerequisites, no progress, or the cap stop; Analyze and implementation remain separate invocations. (S021)

**Accepted supersession**: S007–S009 require terminal/readiness/coverage choices in the earlier contracts; S021 removes routine classification gates and uses evidence-driven continuation or blocked recovery. Human answers and consequential authority remain required. (S007, S008, S009, S021)

## Related pages

- [Workflow lifecycle](./workflow-lifecycle.md)
