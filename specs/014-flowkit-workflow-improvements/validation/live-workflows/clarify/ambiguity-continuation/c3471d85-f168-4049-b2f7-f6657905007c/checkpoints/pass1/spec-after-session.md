# Feature Specification: Normalize Text

**Feature Identity**: Roadmap entry 802 — Normalize Text; specs/802-normalize-text/.

**Status**: Synthetic clarification variant; product behavior pending decisions.

**Created**: 2026-10-01

## Clarifications

Accepted product answers are recorded incrementally for this bounded session.

### Session 2026-10-01

- Q: How should the utility receive the text to normalize? → A: Accept exactly one file path; do not support stdin.

- Q: Where should the normalized text be written? → A: Write normalized text to stdout; do not modify files.

- Q: What status and output should missing paths, directories, and undecodable input produce? → A: All three fail with exit status 2, diagnostics on stderr, and no stdout.

- Q: How should input bytes be decoded, and should Unicode characters be normalized? → A: Decode strictly as UTF-8 and preserve Unicode characters without Unicode normalization.

- Q: Which characters should be removed from the beginning and end of each line? → A: Remove only ASCII spaces and tabs at each line edge.

## User Scenarios & Testing *(mandatory)*

A local text-tool user requests normalized text or a deterministic explanation of rejected input. The input is exactly one file path. Output is stdout without file modification. UTF-8 decoding, Unicode preservation, line-edge trimming, and rejection behavior are specified below. Interior whitespace, blank lines, newline forms, final LF, and size policy remain undecided.

### User Story 1 - Normalize local text (Priority: P1)

The user obtains normalized text while retaining the information required by the eventual accepted whitespace and Unicode policies.

**Independent Test**: The accepted input, transformation and destination decisions must determine exact examples before implementation.

**Acceptance Scenarios**: Given a UTF-8 file containing a line with edge ASCII spaces or tabs, those edge characters are removed while other Unicode characters remain unchanged; the result is written to stdout without modifying the file. Exact blank-line, newline, and final-LF expectations still depend on the remaining decisions.

### User Story 2 - Understand rejected input (Priority: P2)

The user receives deterministic observable rejection behavior for inputs that cannot be processed.

**Independent Test**: A missing path, directory, or undecodable input must each yield status 2, stderr diagnostics, and empty stdout.

### Edge Cases

Empty input, whitespace-only lines, trailing blank lines, mixed newline forms, non-ASCII whitespace, decomposed Unicode, invalid encodings, missing paths, directories and large inputs require the decisions below. No default is chosen here.

## Requirements *(mandatory)*

The current synthetic [normalization source](../../docs/normalization-contract.md) and [input/error source](../../docs/error-contract.md) leave these same choices open; cited wiki pages mirror that state.

### Functional Requirements

- **FR-001**: The utility MUST accept exactly one file path and MUST NOT support stdin.
- **FR-002**: The utility MUST decode input strictly as UTF-8 and preserve Unicode characters without Unicode normalization. Invalid UTF-8 MUST follow FR-008.
- **FR-003**: The utility MUST remove only ASCII space and ASCII tab characters from the beginning and end of each line, preserving other characters.
- **FR-004 (AMB-BLANKS)**: [NEEDS CLARIFICATION: How should interior whitespace and logical blank lines, including trailing blank lines, be handled?]
- **FR-005 (AMB-NEWLINES)**: [NEEDS CLARIFICATION: What should happen to CRLF and bare CR line endings?]
- **FR-006 (AMB-FINAL-LF)**: [NEEDS CLARIFICATION: What output should empty input produce, and when should a final LF be added?]
- **FR-007**: The utility MUST write normalized text to stdout and MUST NOT modify the input or write another output file.
- **FR-008**: Missing paths, directories, and undecodable input MUST each fail with exit status 2, diagnostic text on stderr, and no stdout.
- **FR-009 (AMB-SIZE)**: [NEEDS CLARIFICATION: Should the local utility impose an input size limit?]

### Key Entities

- **Input text**: Local content submitted through exactly one file path.
- **Normalized result**: Text written to stdout whose exact transformations are pending.
- **Input rejection**: A failure with status 2, stderr diagnostics, and no stdout for the specified input failures.

## Success Criteria *(mandatory)*

User-visible acceptance depends on explicit choices rather than inferred defaults.

### Measurable Outcomes

- **SC-001**: Accepted examples yield exact expected text for every selected whitespace, newline and Unicode rule.
- **SC-002**: Each selected rejected-input category yields its exact selected status and output-channel behavior.
- **SC-003**: Repeating an accepted example yields identical behavior.

## Assumptions

Entry 802 uniquely owns this target; roadmap dependency 801 is verified. This controlled variant changes no identity, lifecycle or dependency. The constitution retains Python standard library only, local deterministic behavior and unit-test validation. Batch processing, network services, packaging and external dependencies remain excluded. Four product choices above remain open in current spec/source/wiki evidence. Clarification does not authorize a roadmap amendment, implementation, Git integration or acceptance.
