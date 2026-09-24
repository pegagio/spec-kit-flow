# Research: Implement Eligible Work

## Decision: Preserve the selected agent boundary

The workflow invokes `speckit.implement` for remaining eligible tasks and asks it to verify prerequisites, retain the operator-selected agent boundary, and report evidence. It does not choose, launch, or schedule another agent.

**Rationale**: The project constitution reserves task and agent selection for the human operator.

**Alternative considered**: Automatically dispatch work to a new agent. Rejected because it would grant authority the workflow does not own.

## Decision: Route discoveries without implied completion

The result gate offers convergence, return to analysis/specification/plan/tasks, and blocked. Convergence is a separate operator invocation. Artifact return commands do not by themselves complete the dependent reconciliation chain.

**Rationale**: Merge-bounded artifacts must be reconciled and analyzed before implementation resumes.
