# Feature Specification: Implement Eligible Work

**Feature Branch**: `feature/time-machine-implementation`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Guide implementation of eligible tasks while preserving the operator's scope and artifact consistency gates."

## User Scenarios & Testing

### User Story 1 - Execute Eligible Tasks (Priority: P1)

An operator selects a feature whose artifacts have passed analysis and assigns the current agent to its eligible tasks. The workflow asks that agent to verify prerequisites, execute remaining eligible work, and present evidence for review.

**Why this priority**: Implementation must remain bounded by reviewed tasks and the operator's agent choice.

**Independent Test**: In a disposable feature, inspect that `speckit.implement` is invoked for remaining eligible tasks and its result is reviewed before convergence is offered.

**Acceptance Scenarios**:

1. **Given** clean analysis and eligible tasks, **when** the operator invokes implementation, **then** the selected agent checks prerequisites and executes work within the issued scope.
2. **Given** execution evidence, **when** the operator selects `converge`, **then** the workflow stops and leaves convergence to a separate instruction.

### User Story 2 - Route Discoveries Back to Artifacts (Priority: P2)

When implementation reveals a requirement, design, task, or analysis issue, the operator can route that finding back to the named artifact path before work resumes.

**Why this priority**: Merge-bounded flow-back prevents code and feature artifacts from drifting apart.

**Independent Test**: Inspect all return routes and confirm each invokes the named core command without automatically resuming implementation.

**Acceptance Scenarios**:

1. **Given** a discovery affecting intended behavior, **when** the operator chooses specification flow-back, **then** the workflow invokes specification update for the same feature and stops before implementation resumes.
2. **Given** a design, task, or consistency issue, **when** the matching return route is chosen, **then** the workflow invokes the named plan, tasks, or analysis command.

### User Story 3 - Stop for Blockers (Priority: P3)

A blocker or unrecognized result stops the workflow with evidence and required operator input rather than silently expanding scope.

**Why this priority**: The agent cannot infer new authority from an implementation failure.

**Independent Test**: Inspect blocked and invalid-result routes and verify neither launches another phase or broadens the task set.

**Acceptance Scenarios**:

1. **Given** a blocking issue, **when** the operator chooses `blocked`, **then** the workflow stops and reports the issue and needed operator input.
2. **Given** an invalid result choice, **when** routing occurs, **then** the workflow stops with a manual implementation fallback.

### Edge Cases

- Prerequisites or dependencies are not satisfied; implementation stops rather than skipping them silently.
- A material change is discovered; the workflow does not treat it as routine in-scope work.
- The implementation command succeeds but tasks remain unverified; convergence remains a separate review step.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST require an operator-identified feature with clean analysis and eligible tasks.
- **FR-002**: It MUST invoke implementation only for remaining eligible tasks under the current operator-selected agent boundary.
- **FR-003**: Implementation MUST verify prerequisites and dependencies, report execution evidence, and stop for blockers or merge-bounded artifact flow-back.
- **FR-004**: The result gate MUST offer `converge`, `return-to-analysis`, `return-to-specification`, `return-to-plan`, `return-to-tasks`, and `blocked`.
- **FR-005**: Choosing `converge` MUST stop with a separate convergence handoff; it MUST NOT launch another agent or mark the feature accepted.
- **FR-006**: Each return route MUST invoke its named analysis, specification, plan, or tasks command for the same feature without automatically resuming implementation.
- **FR-007**: A specification, plan, or task change MUST remain subject to the project's dependent-artifact reconciliation and analysis gates before implementation resumes.
- **FR-008**: A blocker or invalid result MUST stop without expanding implementation scope or treating work as complete.
- **FR-009**: A successful command MUST NOT imply roadmap verification, Git integration, publication, or acceptance.
- **FR-010**: A usable manual implementation path MUST remain available when native dispatch is unavailable.

### Key Entities

- **Eligible feature**: The operator-selected feature with analyzed artifacts and remaining tasks.
- **Execution evidence**: Observed task results, blockers, and discoveries for review.
- **Result disposition**: The operator's convergence, return, or blocked decision.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every tested implementation route presents execution evidence for human review before a convergence choice.
- **SC-002**: Every tested return route invokes its named artifact command and launches zero automatic implementation retries.
- **SC-003**: Every tested blocker or invalid route stops without additional task execution.
- **SC-004**: A reviewer can follow the documented manual path when native dispatch is unavailable.

## Assumptions

- Core `speckit.implement` owns task execution mechanics and checklist gates.
- The operator selects the feature, tasks, and agent before invoking this workflow.
- Flow-back may require later dependent-artifact reconciliation; this workflow does not claim a single return command completes that chain.
