---
title: Workflow lifecycle
type: concept
sources: [S002, S006, S007, S010, S013, S017, S018, S019]
updated: 2026-09-29
---

# Workflow lifecycle

An operator prepares a constitution and approved roadmap, establishes cited wiki context, chooses an eligible feature, and invokes each workflow deliberately. The documented route is start-feature, optional clarify, plan, tasks, analyze-remediate, implement, converge, and closeout. (S002)

Feature 013 used reviewed concrete step-model assignments for bounded Codex subagents. Updated Feature 015 source uses reviewed per-step native agent names instead. Human questions and review gates stay in the main task; completing one workflow does not authorize a later phase. (S002, S019)

Verified Feature 013 keeps the eight workflow phases separate while providing desktop-task execution with a main controller and step subagents; it does not add automatic chaining to the next phase. Direct controller skills use the FlowKit catalog route alongside the Specify bundle. (S018)

Verified Feature 015 assigns a reviewed native Codex agent name to each delegated step. Its supported desktop path shows the intended name in a task label and verifies native selection separately; model and effort appear when Codex exposes them. (S018)

Planning and task generation are separate. Clarification may need another session after the current five-question command limit. Analyze follows task generation or consequential artifact reconciliation; converge follows implementation until identified gaps are resolved. (S002)

Workflows preserve a manual-prompt fallback. Closeout requires a separately approved feature-completion operation and does not create one; completing a workflow does not merge or accept a feature. (S002)

Starting a feature requires unique roadmap eligibility, satisfied dependencies, an exact approved patch, and cited governing context. Partial or missing context blocks a speculative start. (S006)

The five-question clarification cap ends a session, not the ambiguity review; the operator explicitly chooses another session, planning readiness, or deferral. (S007)

Read-only analysis precedes any artifact remediation, and routine corrections return through dependent artifacts before another analysis. Consequential findings stop for a separate decision. (S010)

Closeout requires a separately approved completion operation, an exact roadmap verification patch approved by the operator, curated wiki maintenance, and a separate commit-readiness decision. (S013)

## Related pages

- [Codex workflow controller design](./codex-workflow-controllers.md)
- [Project authority and review gates](./project-authority-and-review-gates.md)
- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Consumer feedback boundary](./consumer-feedback-boundary.md)
- [Installation and release lifecycle](./installation-and-release-lifecycle.md)
- [Feature start contract](./feature-start-contract.md)
- [Preimplementation review gates](./preimplementation-review-gates.md)
- [Artifact flow-back and convergence](./artifact-flow-back-and-convergence.md)
- [Closeout and verification boundary](./closeout-and-verification-boundary.md)
