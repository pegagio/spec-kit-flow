# Feature Specification: Converge Feature

**Feature Branch**: `feature/time-machine-convergence`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Compare implementation with feature artifacts and route remaining gaps to resolution."

## User Scenarios & Testing

### User Story 1 - Assess Implementation Against Intent (Priority: P1)

An operator selects an implemented feature and receives an assessment against its current specification, plan, and tasks. A clean result stops at a converged state for separate human closeout review.

**Why this priority**: Task completion alone does not prove the implementation matches intended behavior.

**Independent Test**: In a disposable feature, invoke convergence and confirm the workflow reviews the result before declaring a clean route.

**Acceptance Scenarios**:

1. **Given** implemented work and current feature artifacts, **when** convergence runs, **then** it assesses the implementation against specification, plan, and tasks.
2. **Given** a clean result, **when** the operator selects `clean`, **then** the workflow stops without integrating Git, accepting the feature, or starting closeout.

### User Story 2 - Route Remaining Work Through Analysis (Priority: P2)

If convergence identifies bounded remaining work, it records remediation tasks and returns them through ordinary analysis and implementation before convergence resumes.

**Why this priority**: Newly found work must pass the same artifact consistency gate as the original tasks.

**Independent Test**: Inspect the remediation route and confirm it invokes analysis before asking the operator to resume implementation.

**Acceptance Scenarios**:

1. **Given** bounded implementation gaps, **when** the operator selects `remediation`, **then** the workflow analyzes the new tasks and stops for implementation to be invoked separately.
2. **Given** remediation implementation later completes, **when** the operator resumes convergence, **then** a fresh assessment determines whether gaps remain.

### User Story 3 - Preserve a Blocker (Priority: P3)

A blocked or unrecognized result stops with evidence and a manual path rather than claiming convergence.

**Why this priority**: Incomplete evidence cannot confer a clean outcome.

**Independent Test**: Inspect blocked and invalid routes and confirm neither begins closeout or marks acceptance.

**Acceptance Scenarios**:

1. **Given** a convergence blocker, **when** the operator selects `blocked`, **then** the workflow stops and preserves the blocker evidence.
2. **Given** an invalid result choice, **when** routing occurs, **then** the workflow stops with a manual convergence fallback.

### Edge Cases

- Convergence appends tasks but analysis finds a specification or plan inconsistency; implementation remains gated until reconciled.
- A prior clean result becomes stale after implementation or artifact changes; the operator must run convergence again.
- No gaps are found; no empty remediation phase is added by the core convergence command.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST require an operator-identified implemented feature and its current artifacts.
- **FR-002**: It MUST invoke `speckit.converge` to assess implementation against specification, plan, and tasks.
- **FR-003**: Any bounded remediation tasks created by convergence MUST be reported and routed through ordinary task analysis before implementation resumes.
- **FR-004**: The result gate MUST offer `clean`, `remediation`, and `blocked`.
- **FR-005**: A clean route MUST stop at Feature Converged without automatically invoking closeout, Git integration, or acceptance.
- **FR-006**: A remediation route MUST invoke analysis of the new tasks and stop for separate implementation, followed by a later convergence run.
- **FR-007**: A blocked or invalid route MUST stop without claiming convergence.
- **FR-008**: The workflow MUST NOT choose or launch another agent, broaden material scope, or treat task completion as publication or acceptance.
- **FR-009**: A usable manual convergence path MUST remain available when native dispatch is unavailable.

### Key Entities

- **Feature artifact set**: Current specification, plan, and tasks.
- **Convergence assessment**: Evidence comparing implementation with the artifact set.
- **Remediation tasks**: Bounded remaining work added by the core convergence command.
- **Result disposition**: The operator-reviewed clean, remediation, or blocked outcome.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every tested clean route stops without invoking closeout or acceptance commands.
- **SC-002**: Every tested remediation route invokes analysis before implementation can resume.
- **SC-003**: Every tested blocked or invalid route reports a stop rather than a converged outcome.
- **SC-004**: A reviewer can follow the documented manual path when native dispatch is unavailable.

## Assumptions

- Core `speckit.converge` owns gap assessment and append-only remediation tasks.
- The operator decides when implementation is ready for convergence and when a later clean result is acceptable for closeout review.
- Convergence is distinct from Git integration, roadmap verification, publication, and feature acceptance.
