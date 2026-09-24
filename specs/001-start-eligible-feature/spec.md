# Feature Specification: Start Eligible Feature

**Feature Branch**: `feature/time-machine-feature-start`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Guide an operator from an eligible roadmap item through an approved patch, cited context, specification, and brief."

## User Scenarios & Testing

### User Story 1 - Start an Eligible Feature (Priority: P1)

An operator names a roadmap feature that is uniquely eligible to start, reviews the exact proposed roadmap change, and approves it. The operator then receives governing context with citations, a draft specification, and a brief comparing that specification with the roadmap entry. The operator chooses the next state after reviewing the result.

**Why this priority**: This is the primary path for starting work under explicit human control.

**Independent Test**: In an initialized consumer with a uniquely eligible roadmap item and available cited context, run the start-feature workflow and confirm that the roadmap changes only after approval and that the final review does not launch another phase.

**Acceptance Scenarios**:

1. **Given** one uniquely eligible roadmap feature and complete governing context, **when** the operator approves the exact proposed roadmap patch, **then** only that patch is applied before context retrieval, specification drafting, and the roadmap brief.
2. **Given** a completed specification and roadmap brief, **when** the operator selects a next state, **then** the workflow records or reports that choice without starting another agent or workflow phase.

### User Story 2 - Stop When Starting Is Unsafe (Priority: P2)

An operator can defer a feature or address missing prerequisites without a speculative roadmap transition or specification.

**Why this priority**: An ambiguous or unsupported start would create work outside the operator's intended scope.

**Independent Test**: Present ambiguous eligibility, an unmet dependency, incomplete context, and a declined patch in separate runs; confirm each path stops without applying a roadmap patch or drafting the feature specification.

**Acceptance Scenarios**:

1. **Given** multiple plausible roadmap matches, unsatisfied dependencies, or incomplete governing context, **when** the operator requests a start, **then** the workflow stops and reports the blocking condition without changing roadmap or feature state.
2. **Given** a proposed patch, **when** the operator chooses to amend the roadmap, resolve context, or defer, **then** the workflow stops on that path without applying the proposed patch.

### Edge Cases

- A roadmap query finds no eligible feature matching the request.
- Governing context is only partially covered or uncovered; the workflow reports that coverage and does not invent a missing rule.
- A decision value is not recognized; the workflow stops and retains a usable manual prompt path.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST assess one operator-named roadmap feature for unique eligibility, dependencies, and governing context before proposing a state change.
- **FR-002**: The workflow MUST present the exact proposed roadmap patch for human review and MUST NOT apply it before approval.
- **FR-003**: When eligibility is ambiguous, dependencies are unsatisfied, or governing context is incomplete, the workflow MUST stop and report the reason without changing roadmap or feature state.
- **FR-004**: An approved start MUST apply only the reviewed roadmap patch, then retrieve cited governing decisions, constraints, dependencies, and coverage classification.
- **FR-005**: The specification draft MUST preserve the approved feature outcome, scope, dependencies, and governing context; a roadmap brief MUST compare the draft with the approved roadmap entry.
- **FR-006**: The workflow MUST offer the operator explicit choices after the brief and MUST NOT automatically start clarification, planning, agent dispatch, Git integration, or acceptance.
- **FR-007**: If the operator chooses amendment, context resolution, or deferral, the workflow MUST stop with the appropriate next action rather than inventing a replacement feature.
- **FR-008**: The workflow MUST preserve a usable manual prompt path when native dispatch is unavailable or a decision cannot be routed.
- **FR-009**: The workflow MUST operate against compatible roadmap and wiki components identified by the bundle, without requiring The Diagram or its runtime state.

### Key Entities

- **Feature candidate**: The operator-named roadmap item, including its eligibility and dependency evidence.
- **Proposed roadmap patch**: The exact change presented for approval and, if approved, applied without expansion.
- **Governing context**: Cited decisions and constraints with a coverage classification.
- **Feature draft**: The specification and roadmap brief prepared from the approved outcome and governing context.

## Success Criteria

### Measurable Outcomes

- **SC-001**: In every tested eligible start, the roadmap remains unchanged until the operator approves the exact patch.
- **SC-002**: In every tested ambiguous, blocked, or deferred start, no roadmap patch or feature specification is created by this workflow.
- **SC-003**: Every completed eligible start presents a specification, a roadmap brief, and an explicit operator choice for what happens next.
- **SC-004**: Every context lookup reports its coverage classification and citations for supported governing facts; missing coverage is identified rather than filled with invented mechanics.
- **SC-005**: A reviewer can execute the documented manual path when native workflow dispatch is unavailable.

## Assumptions

- The operator has selected a candidate from a governed roadmap and is authorized to review the proposed transition.
- Compatible roadmap and wiki components are available to the consumer; their source remains independently versioned.
- This specification captures the existing generic start-feature workflow and does not add a preset, agent policy, or Diagram adapter.
