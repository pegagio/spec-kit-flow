# Feature Specification: Maintainer Feedback Intake

**Feature Branch**: `feature/time-machine-maintainer-intake`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Validate transferred feedback reports and record proposed dispositions for maintainer review."

## User Scenarios & Testing

### User Story 1 - Validate Transferred Evidence (Priority: P1)

A maintainer receives a portable consumer report and checks its schema, integrity digest, component provenance, and redaction before creating a record.

**Why this priority**: Intake must not trust a transferred file simply because it came from a consumer workflow.

**Independent Test**: Accept a valid report, reject tampering and an embedded host path, and verify rejected reports create no inbox or triage files.

**Acceptance Scenarios**:

1. **Given** a valid digest-bearing report, **when** intake runs, **then** it creates one inbox copy and one bounded triage proposal.
2. **Given** a tampered or nonportable report, **when** intake runs, **then** it rejects before writing records.

### User Story 2 - Record a Safe Proposal (Priority: P2)

The maintainer chooses a disposition and rationale. Intake validates that free-text rationale before writing it and records the next action as a proposal through ordinary specification flow.

**Why this priority**: The triage record is project-owned data and must not become a path or secret leak.

**Independent Test**: Reject a rationale with an embedded absolute path or secret-shaped value and confirm no files are created.

**Acceptance Scenarios**:

1. **Given** a supported disposition and portable rationale, **when** intake succeeds, **then** the triage record names the proposed disposition and next action without editing source.
2. **Given** sensitive rationale text, **when** intake runs, **then** it rejects before creating inbox or triage files.

### User Story 3 - Preserve Duplicate Relationships (Priority: P3)

When the same report arrives again, intake records its relationship to the original triage without creating a second source proposal or inbox copy.

**Why this priority**: Repeated transfer should not multiply work or imply repeated approvals.

**Independent Test**: Intake the same report twice and verify distinct triage IDs, one inbox copy, and a `duplicate_of` reference.

**Acceptance Scenarios**:

1. **Given** a previously triaged report digest, **when** intake runs again, **then** it records a duplicate relationship and no second inbox copy.
2. **Given** any accepted proposal, **when** intake finishes, **then** it has not edited workflows, presets, bundle, roadmap, installed components, Git state, or agent policy.

### Edge Cases

- The report has a valid recomputed digest but embeds an absolute path after punctuation; reject it.
- A supported disposition has a nonportable rationale; reject before writing files.
- An existing triage record is malformed JSON; stop duplicate detection rather than guessing.

## Requirements

### Functional Requirements

- **FR-001**: Maintainer intake MUST remain a separate component outside the consumer bundle.
- **FR-002**: It MUST validate report schema, integrity digest, every required consumer observation field, component provenance, unique observation IDs, and nonempty evidence references before writing. It MUST accept the consumer's prefixed or bare SHA-256 component digest form.
- **FR-003**: It MUST reject sensitive keys and values, raw transcripts, and absolute host paths in reports, including paths embedded after punctuation or written as `file://` URLs.
- **FR-004**: It MUST validate the disposition and reject sensitive or nonportable rationale and receipt-time text before writing a triage record.
- **FR-005**: A valid first intake MUST create a canonical inbox copy and a triage proposal with component coordinates, rationale, status, and next action.
- **FR-006**: An identical report digest MUST create a duplicate triage relationship without a second inbox copy or source proposal.
- **FR-007**: Rejected input MUST create no inbox or triage record.
- **FR-008**: Intake MUST NOT directly edit a workflow, preset, bundle, roadmap, installed component, Git state, or agent policy; proposed changes must re-enter ordinary specification, planning, task, and implementation flow.

### Key Entities

- **Transferred report**: Consumer-generated portable JSON with integrity digest.
- **Inbox copy**: Canonical accepted report held in maintainer state.
- **Triage proposal**: Maintainer disposition and rationale for review.
- **Duplicate relationship**: Link from a repeat intake to the original triage record.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Valid intake creates exactly one inbox and one triage record.
- **SC-002**: Tampered, malformed, or sensitive inputs create zero new records.
- **SC-003**: A second intake of the same digest creates one duplicate triage record and no second inbox copy.
- **SC-004**: The disposable lifecycle test accepts a valid report and rejects a tampered report in maintainer-owned temporary state.

## Assumptions

- This component is maintainer-only and is not packaged into the consumer bundle.
- A triage disposition is a proposal, not an approval to modify source.
