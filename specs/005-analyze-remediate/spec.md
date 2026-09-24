# Feature Specification: Analyze and Remediate Artifacts

**Feature Branch**: `feature/time-machine-artifact-analysis`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Analyze specification, plan, and task consistency and route bounded corrections before implementation."

## User Scenarios & Testing

### User Story 1 - Review a Read-Only Analysis (Priority: P1)

An operator selects a feature after task generation and receives a read-only consistency report across its specification, plan, and tasks. The operator reviews the classification before any remediation or implementation decision.

**Why this priority**: The project requires a clean, reviewable artifact set before implementation begins.

**Independent Test**: Run the workflow in a disposable feature context and confirm analysis precedes the disposition gate and does not modify feature artifacts by itself.

**Acceptance Scenarios**:

1. **Given** a tasked feature, **when** analysis runs, **then** it reports consistency findings without changing files.
2. **Given** a clean report, **when** the operator chooses `clean`, **then** the workflow stops with implementation left to a separate operator instruction.

### User Story 2 - Flow Routine Findings Back (Priority: P2)

When the operator identifies routine findings within the issued controller scope, the workflow routes them through the smallest affected artifact path and repeats read-only analysis.

**Why this priority**: A local correction must propagate to dependent artifacts before implementation.

**Independent Test**: Inspect each routine route and verify that specification changes lead to replanning and retasking, plan changes lead to retasking, and task changes remain task-only before reanalysis.

**Acceptance Scenarios**:

1. **Given** a routine specification finding, **when** that disposition is selected, **then** the workflow updates the specification, replans, regenerates tasks, and reanalyzes.
2. **Given** a routine plan or task finding, **when** the matching disposition is selected, **then** the workflow updates the affected artifact and its dependents before reanalysis.

### User Story 3 - Stop for Consequential Decisions (Priority: P3)

Constitutional, authority, material-scope, ambiguous-recovery, and blocked findings stop for the operator rather than being treated as routine remediation.

**Why this priority**: These decisions exceed the workflow's bounded authority.

**Independent Test**: Inspect all consequential and invalid-disposition routes; confirm none invokes remediation commands.

**Acceptance Scenarios**:

1. **Given** a constitutional finding, **when** the operator selects `constitutional-stop`, **then** the workflow stops and requests a separate approved amendment path.
2. **Given** an authority, material-scope, ambiguous-recovery, or blocker finding, **when** the matching stop route is selected, **then** the workflow preserves evidence and does not claim implementation readiness.

### Edge Cases

- The report mixes routine and consequential findings; consequential work remains outside routine remediation.
- A disposition is unrecognized; the workflow stops with a manual controller fallback.
- Reanalysis still finds gaps; the workflow does not label the feature clean merely because a remediation command ran.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST require an operator-identified feature and its current artifacts.
- **FR-002**: It MUST invoke read-only analysis before presenting a disposition gate.
- **FR-003**: The gate MUST distinguish clean, routine specification, routine plan, routine task, constitutional, authority-or-scope, and blocked outcomes.
- **FR-004**: A clean result MUST stop with implementation available only through a separate operator instruction.
- **FR-005**: Routine specification remediation MUST update the specification, then replan, retask, and reanalyze in that order.
- **FR-006**: Routine plan remediation MUST update the plan, retask, and reanalyze in that order.
- **FR-007**: Routine task remediation MUST update tasks and reanalyze, without silently changing product scope or design.
- **FR-008**: Routine remediation MUST stay within the operator-issued scope and MUST exclude constitutional, authority, ambiguous-recovery, and material-scope changes.
- **FR-009**: Constitutional, authority-or-scope, blocked, and invalid outcomes MUST stop without automatically applying a consequential change.
- **FR-010**: A completed analysis or remediation route MUST NOT launch implementation, choose agents, integrate Git, or accept the feature.
- **FR-011**: A usable manual analysis/remediation controller MUST remain available when native dispatch is unavailable.

### Key Entities

- **Feature artifact set**: The active specification, plan, and tasks under review.
- **Analysis report**: Read-only findings and disposition evidence.
- **Disposition**: The operator-reviewed clean, routine, or stop classification.
- **Remediation path**: The ordered artifact updates and reanalysis for one routine finding class.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every tested analysis route presents a disposition before any remediation command runs.
- **SC-002**: Every routine route ends with a new read-only analysis after its required artifact updates.
- **SC-003**: Every consequential or blocked route invokes zero remediation and implementation commands.
- **SC-004**: A reviewer can follow the documented manual path when native dispatch is unavailable.

## Assumptions

- Core `speckit.analyze` owns read-only consistency analysis; this workflow coordinates bounded disposition and flow-back.
- The operator's issued controller scope defines which routine corrections may proceed without another material decision.
- A remediation command's success does not prove a clean result or authorize implementation.
