# Feature Specification: Generate Implementation Tasks

**Feature Branch**: `feature/time-machine-task-generation`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Generate implementation tasks from an approved plan as a separate workflow step."

## User Scenarios & Testing

### User Story 1 - Produce a Reviewable Task Proposal (Priority: P1)

An operator selects a planned feature and receives dependency-ordered implementation tasks derived from its reviewed design artifacts. Work that unexpectedly requires human action is surfaced for review instead of silently changing the plan.

**Why this priority**: Task generation makes implementation work explicit while preserving the reviewed design as the authority.

**Independent Test**: In a disposable planned feature, invoke task generation and inspect the resulting task proposal for dependencies, coverage, and flagged human actions.

**Acceptance Scenarios**:

1. **Given** reviewed design artifacts for one feature, **when** task generation runs, **then** it proposes dependency-ordered work scoped to that feature.
2. **Given** an unexpected operator action is discovered, **when** tasks are proposed, **then** the workflow surfaces it for human review instead of silently revising the plan.

### User Story 2 - Route the Reviewed Proposal (Priority: P2)

The operator reviews the proposal and chooses analysis, return to planning, explicit task amendment, or deferral. No choice begins implementation directly.

**Why this priority**: A generated task list is not proof that the feature is ready to implement.

**Independent Test**: Inspect each gate route and exercise one terminal route in a disposable consumer; confirm no implementation command runs.

**Acceptance Scenarios**:

1. **Given** an acceptable task proposal, **when** the operator chooses `analyze`, **then** the workflow stops and directs a separate analysis step before implementation.
2. **Given** a material design gap, **when** the operator chooses `return-to-plan`, **then** the workflow invokes planning for the same feature.
3. **Given** a task-level amendment or deferral decision, **when** the operator chooses `amend-tasks` or `defer`, **then** the workflow stops with that concern explicit.

### Edge Cases

- A planned feature or reviewed design artifacts are missing; task generation must not invent them.
- An invalid review choice stops without launching another phase.
- Deferral occurs after a proposal was generated; the proposal remains unaccepted rather than being treated as analysis-ready.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST require an operator-identified planned feature.
- **FR-002**: It MUST invoke task generation from reviewed design artifacts and request dependency-ordered tasks scoped to that feature.
- **FR-003**: It MUST surface surprising human-operator work rather than silently revising the plan.
- **FR-004**: After generation, it MUST present task coverage and human actions for operator review.
- **FR-005**: The review gate MUST offer `analyze`, `return-to-plan`, `amend-tasks`, and `defer`.
- **FR-006**: Choosing `analyze` MUST stop with a separate analysis handoff; it MUST NOT begin implementation.
- **FR-007**: Choosing `return-to-plan` MUST invoke planning for the same feature's material design gap.
- **FR-008**: Choosing amendment, deferral, or an invalid choice MUST stop without treating the proposal as implementation-ready.
- **FR-009**: No route MUST select an agent, integrate Git, accept the feature, or bypass the project's analysis gate.
- **FR-010**: A usable manual task-generation path MUST remain available when native dispatch is unavailable.

### Key Entities

- **Planned feature**: The operator-selected feature and its reviewed design artifacts.
- **Task proposal**: Dependency-ordered implementation work awaiting review.
- **Review decision**: The operator's analysis, replanning, amendment, or deferral choice.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every tested task proposal is presented for human review before an analysis-ready route is chosen.
- **SC-002**: Every tested `analyze` route invokes zero implementation commands and gives a separate analysis handoff.
- **SC-003**: Every tested amendment, deferral, or invalid route leaves the proposal unaccepted for implementation.
- **SC-004**: A reviewer can follow the documented manual path when native dispatch is unavailable.

## Assumptions

- Core `speckit.tasks` owns task-file generation; this workflow owns review and routing.
- Planning is already complete and reviewed before this workflow begins.
- The source workflow generates a proposal before the review gate; deferral does not erase that proposal.
