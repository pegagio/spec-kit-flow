# Feature Specification: Normalize Text

**Feature Identity**: Roadmap entry 802 — Normalize Text; specs/802-normalize-text/.

**Status**: Draft

**Created**: 2026-10-01

## Clarifications

Accepted product answers are recorded incrementally for this bounded session.

### Session 2026-10-01

- Q: How should the utility receive the text to normalize? → A: Accept exactly one file path; do not support stdin.

- Q: Where should the normalized text be written? → A: Write normalized text to stdout; do not modify files.

- Q: What status and output should missing paths, directories, and undecodable input produce? → A: All three fail with exit status 2, diagnostics on stderr, and no stdout.

- Q: How should input bytes be decoded, and should Unicode characters be normalized? → A: Decode strictly as UTF-8 and preserve Unicode characters without Unicode normalization.

- Q: Which characters should be removed from the beginning and end of each line? → A: Remove only ASCII spaces and tabs at each line edge.

- Q: How should interior whitespace and blank lines, including trailing blank lines, be handled? → A: Preserve interior whitespace and all blank lines, including trailing blank lines.

- Q: How should CRLF and bare CR line endings be represented in normalized output? → A: Convert both CRLF and bare CR to LF.

- Q: What should empty input produce, and when should a terminating LF be added? → A: Empty input stays empty; for nonempty input add LF only if normalized output does not already end with LF, preserving existing trailing LFs.

- Q: Should the utility impose an explicit input-size limit? → A: Do not impose an explicit product input-size limit.

## User Scenarios & Testing *(mandatory)*

A local text-tool user requests normalized text or a deterministic explanation of rejected input. The input is exactly one file path. Output is stdout without file modification. UTF-8 decoding, Unicode preservation, line-edge trimming, and rejection behavior are specified below. Interior whitespace and all blank lines are preserved. CRLF and bare CR become LF. Empty input remains empty; nonempty input receives a terminating LF only when needed. No explicit product input-size limit applies.

### User Story 1 - Normalize local text (Priority: P1)

The user obtains normalized text while retaining the information required by the eventual accepted whitespace and Unicode policies.

**Independent Test**: Compare exact stdout for UTF-8 files with edge spaces/tabs, interior whitespace, blank lines, mixed line endings, Unicode, and empty or unterminated input; verify the input file is unchanged.

**Acceptance Scenarios**: Given a UTF-8 file containing a line with edge ASCII spaces or tabs, those edge characters are removed while other Unicode characters remain unchanged; the result is written to stdout without modifying the file. Interior whitespace and all blank lines are preserved; CRLF and bare CR become LF; nonempty input gains a final LF only if needed, while empty input stays empty.

**Additional Exact Acceptance Examples**: `" a  b \r\n\r\n"` yields `"a  b\n\n"`; `"a\rb"` yields `"a\nb\n"`; empty input yields empty output; `" \t"` yields exactly `"\n"`; existing trailing LF characters remain present.

### User Story 2 - Understand rejected input (Priority: P2)

The user receives deterministic observable rejection behavior for inputs that cannot be processed.

**Independent Test**: A missing path, directory, or undecodable input must each yield status 2, stderr diagnostics, and empty stdout.

### Edge Cases

Empty input, whitespace-only lines, trailing blank lines, mixed newline forms, non-ASCII whitespace, decomposed Unicode, invalid encodings, missing paths, directories and large inputs follow the requirements below. Empty input yields empty output; ASCII space followed by ASCII tab with no newline yields exactly one LF. Existing trailing blank lines remain present. No explicit product input-size limit applies.

## Requirements *(mandatory)*

The synthetic [normalization source](../../docs/normalization-contract.md) and [input/error source](../../docs/error-contract.md) leave these choices open; cited wiki pages mirror that state. The operator answers recorded above resolve them for this specification.

### Functional Requirements

- **FR-001**: The utility MUST accept exactly one file path and MUST NOT support stdin.
- **FR-002**: The utility MUST decode input strictly as UTF-8 and preserve Unicode characters without Unicode normalization. Invalid UTF-8 MUST follow FR-008.
- **FR-003**: The utility MUST remove only ASCII space and ASCII tab characters from the beginning and end of each line, preserving other characters.
- **FR-004**: The utility MUST preserve interior whitespace and all logical blank lines, including trailing blank lines.
- **FR-005**: The utility MUST convert CRLF and bare CR line endings to LF.
- **FR-006**: Empty input MUST produce empty output. For nonempty input the utility MUST add a terminating LF only if normalized output does not already end with LF, preserving existing trailing LF characters.
- **FR-007**: The utility MUST write normalized text to stdout and MUST NOT modify the input or write another output file.
- **FR-008**: Missing paths, directories, and undecodable input MUST each fail with exit status 2, diagnostic text on stderr, and no stdout.
- **FR-009**: The utility MUST NOT impose an explicit product input-size limit.

### Key Entities

- **Input text**: Local content submitted through exactly one file path.
- **Normalized result**: Text written to stdout using FR-002–FR-006 transformations.
- **Input rejection**: A failure with status 2, stderr diagnostics, and no stdout for the specified input failures.

## Success Criteria *(mandatory)*

User-visible acceptance depends on explicit choices rather than inferred defaults.

### Measurable Outcomes

- **SC-001**: Accepted examples yield exact expected text for every selected whitespace, newline and Unicode rule.
- **SC-002**: Each selected rejected-input category yields its exact selected status and output-channel behavior.
- **SC-003**: Repeating an accepted example yields identical behavior.

## Assumptions

Entry 802 uniquely owns this target; roadmap dependency 801 is verified. This controlled variant changes no identity, lifecycle or dependency. The constitution retains Python standard library only, local deterministic behavior and unit-test validation. Batch processing, network services, packaging and external dependencies remain excluded. All product choices in this specification have now been answered by the operator; synthetic source/wiki pages retain their pre-clarification open state. Clarification does not authorize a roadmap amendment, implementation, Git integration or acceptance.
