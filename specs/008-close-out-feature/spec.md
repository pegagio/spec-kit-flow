# Feature Specification: Close Out Feature

**Feature Branch**: `feature/time-machine-feature-closeout`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Guide explicit completion review, roadmap verification, wiki maintenance, and commit readiness."

## User Scenarios & Testing

### User Story 1 - Confirm Completion Authority (Priority: P1)

After convergence, an operator checks whether a separately approved feature-completion operation exists. If it does not, closeout stops without claiming a lifecycle transition.

**Why this priority**: Convergence cannot silently substitute for feature completion.

**Independent Test**: Run the missing-operation route in a disposable consumer and inspect the available-operation route in source.

**Acceptance Scenarios**:

1. **Given** no approved completion operation, **when** the operator selects `operation-missing`, **then** closeout stops before roadmap debrief or mutation.
2. **Given** an approved operation, **when** the operator selects `operation-available`, **then** the workflow prompts for that operation before debrief; it does not invent a substitute.

### User Story 2 - Review Roadmap Verification (Priority: P2)

The operator reviews the debrief and exact proposed verification patch before any roadmap write. Deferral or flow-back stops closeout.

**Why this priority**: Roadmap state is a separate authority decision.

**Independent Test**: Inspect the debrief, approval gate, and three decision routes.

**Acceptance Scenarios**:

1. **Given** an approved completion operation and supporting evidence, **when** debrief proposes a patch, **then** the operator can approve only that exact patch before `speckit.flow-roadmap.write` runs.
2. **Given** deferral, flow-back, or an invalid choice, **when** routing occurs, **then** no roadmap write, wiki ingest, or acceptance follows.

### User Story 3 - Maintain Context and Review Commit Readiness (Priority: P3)

After an approved roadmap patch, the operator selects durable sources for wiki ingestion. Wiki lint and Git change review precede a commit-readiness decision; the workflow does not commit.

**Why this priority**: Searchable context and a clean working tree need their own evidence before an explicit commit.

**Independent Test**: Inspect the approved route and manual fallback, then exercise one no-op native route.

**Acceptance Scenarios**:

1. **Given** an approved roadmap patch, **when** wiki maintenance runs, **then** curated sources are ingested and linted before commit readiness is offered.
2. **Given** commit readiness, **when** the operator selects `ready-for-explicit-commit`, **then** the workflow stops without committing, integrating Git, or accepting project work.

### Edge Cases

- A completion operation is unavailable; stop without using `speckit.specify` as a substitute.
- Wiki lint reports unresolved findings; stop or return to the affected workflow before a commit.
- A completion, roadmap, or commit-readiness result is unrecognized; stop without a state transition.

## Requirements

### Functional Requirements

- **FR-001**: The workflow MUST require an operator-identified converged feature.
- **FR-002**: It MUST gate closeout on a separately approved feature-completion operation and stop if that operation is missing or the result is invalid.
- **FR-003**: It MUST NOT infer completion from convergence or use specification drafting as a completion substitute.
- **FR-004**: After operation availability, it MUST request the approved operation and invoke `speckit.flow-roadmap.debrief` before proposing verification.
- **FR-005**: It MUST require human review of the debrief and exact proposed patch before `speckit.flow-roadmap.write` applies only the approved patch.
- **FR-006**: Return, defer, or invalid roadmap decisions MUST stop without applying a roadmap patch.
- **FR-007**: After an approved patch, it MUST invoke `speckit.flow-wiki.ingest` for operator-selected durable sources and `speckit.flow-wiki.lint` before commit-readiness review.
- **FR-008**: The commit-readiness gate MUST NOT itself commit, integrate Git, or accept project work.
- **FR-009**: Unresolved lint findings, blockers, and invalid gate choices MUST stop or return to the relevant workflow without a false success claim.
- **FR-010**: A manual closeout path MUST remain available when native dispatch is unavailable.

### Key Entities

- **Converged feature**: Operator-selected feature with reviewed convergence evidence.
- **Completion operation**: Separately approved lifecycle operation, outside this workflow's definition.
- **Roadmap verification patch**: Exact proposed change reviewed by the operator.
- **Curated context set**: Durable source documents selected for wiki ingestion.
- **Commit-readiness disposition**: Human decision after wiki lint and Git review, distinct from a commit.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Every tested missing-operation route stops before roadmap or wiki commands.
- **SC-002**: Every tested roadmap write route passes an explicit exact-patch approval gate.
- **SC-003**: Every tested commit-ready route passes wiki ingestion and lint first and performs zero Git commits.
- **SC-004**: A reviewer can follow the documented manual path when native dispatch is unavailable.

## Assumptions

- The completion operation must be defined and approved separately; this feature cannot make it available.
- The operator controls roadmap verification, source curation, commit, and project acceptance independently.
