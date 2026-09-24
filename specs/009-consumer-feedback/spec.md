# Feature Specification: Consumer Feedback

**Feature Branch**: `feature/time-machine-consumer-feedback`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Capture local workflow observations and export portable reports without changing source or authority."

## User Scenarios & Testing

### User Story 1 - Capture Local Evidence (Priority: P1)

An operator records a structured observation with component identity, version, digest, execution context, expected and observed behavior, safety response, and evidence references. The extension validates it before appending to consumer-owned state.

**Why this priority**: Reproducible feedback needs provenance and a local record without changing source.

**Independent Test**: Capture a valid observation, reject a duplicate ID, and confirm the journal is append-only.

**Acceptance Scenarios**:

1. **Given** a valid observation, **when** capture runs, **then** one canonical JSON line is appended to the consumer journal.
2. **Given** a duplicate ID or malformed observation, **when** capture runs, **then** the journal is not extended.

### User Story 2 - Preserve Portability (Priority: P2)

The operator can export a JSON report and Markdown projection whose contents omit raw transcripts, secrets, and absolute host paths, including paths embedded after punctuation in prose.

**Why this priority**: Transferable evidence must not disclose local host details.

**Independent Test**: Reject an embedded absolute path while allowing a relative evidence reference and an HTTPS source link.

**Acceptance Scenarios**:

1. **Given** an absolute host path in a string field, **when** capture or export validates it, **then** validation rejects the record before writing output.
2. **Given** valid local evidence, **when** report runs, **then** it emits deterministic JSON with an integrity digest and a Markdown projection from the same observations.

### User Story 3 - Keep Feedback as Evidence (Priority: P3)

An exported report is a handoff for separate maintainer review. Capture and report never edit workflows, presets, roadmap state, Git state, or agent policy.

**Why this priority**: A consumer observation is not a source decision.

**Independent Test**: Inspect command and implementation scope; exercise the installed extension in a disposable consumer.

**Acceptance Scenarios**:

1. **Given** a completed export, **when** the operator reviews it, **then** transfer remains an explicit human action.
2. **Given** a report, **when** capture or export completes, **then** no source or authority file is changed.

### Edge Cases

- A corrupted or duplicate-ID journal rejects a new capture or report.
- A field contains a path after a colon or opening parenthesis; portability validation rejects it.
- A relative evidence reference or HTTPS URL remains valid.

## Requirements

### Functional Requirements

- **FR-001**: The extension MUST expose `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`.
- **FR-002**: Capture MUST validate required provenance fields, component digest, and disposition before appending one canonical JSON line to consumer-owned state.
- **FR-003**: Duplicate observation IDs and malformed journals MUST be rejected without modifying the journal.
- **FR-004**: Capture and export MUST reject sensitive keys, known secret values, raw transcripts, and absolute host paths, including paths embedded after punctuation in prose.
- **FR-005**: Portability checks MUST continue to allow relative evidence references and HTTPS URLs.
- **FR-006**: Report MUST revalidate observations and emit deterministic JSON with an integrity digest and a Markdown projection from the same content.
- **FR-007**: Capture and export MUST be offline and MUST NOT mutate installed components, workflow or preset source, roadmap state, Git state, or agent policy.
- **FR-008**: Transfer and maintainer disposition MUST remain separate human-directed actions.

### Key Entities

- **Observation**: Structured, sanitized consumer evidence with provenance and behavior fields.
- **Journal**: Consumer-owned append-only JSONL observations.
- **Portable report**: Revalidated JSON export with integrity digest.
- **Markdown projection**: Readable view of the same report data.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Valid capture and report tests produce one journal entry, a digest-bearing JSON report, and a matching Markdown projection.
- **SC-002**: Duplicate, malformed, or sensitive inputs create no new journal or report output.
- **SC-003**: Tests reject embedded absolute paths after punctuation while accepting relative references and HTTPS URLs.
- **SC-004**: Disposable consumer validation confirms the installed command names and local export path.

## Assumptions

- The current source is `flow-feedback` version `0.2.0`; a behavior correction requires a source version increment and later catalog repackaging.
- Source review and consumer handoff are distinct from maintainer acceptance.
