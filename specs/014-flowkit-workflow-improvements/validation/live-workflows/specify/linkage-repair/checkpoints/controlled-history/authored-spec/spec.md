# Feature Specification: Normalize Text

**Feature Identity**: `802 — specs/802-normalize-text/`

**Created**: 2026-10-01

**Status**: Draft

**Input**: Normalize one local text file according to the approved synthetic fixture decisions.

## User Scenarios & Testing *(mandatory)*

The user receives predictable normalized text without losing meaningful whitespace or changing the source file.

### User Story 1 - Normalize a local file (Priority: P1)

A user supplies one local file path and receives normalized text on standard output for use in a subsequent local operation.

**Why this priority**: The primary value is reliable normalization with preserved content and an unchanged source.

**Independent Test**: Supply representative valid files, compare standard output with the expected text, and compare source bytes before and after each operation.

**Acceptance Scenarios**:

1. **Given** text ` a  b \r\n\r\n`, **When** the user normalizes it, **Then** output is `a  b\n\n`, retaining interior spaces and the trailing blank line.
2. **Given** text `a\rb`, **When** normalized, **Then** output is `a\nb\n`.
3. **Given** an empty input file, **When** normalized, **Then** output is empty.
4. **Given** nonempty input containing only an ASCII space and tab (` \t`), **When** normalized, **Then** output is one LF (`\n`).
5. **Given** text with existing trailing LF characters, **When** normalized, **Then** all trailing LF characters remain and no extra LF is added.
6. **Given** Unicode characters, including nonbreaking spaces and decomposed characters, **When** normalized, **Then** those characters retain their exact identity; only the specified ASCII edge whitespace and line endings change.

### User Story 2 - Reject invalid input safely (Priority: P2)

A user receives a concise error instead of misleading partial output when the supplied file cannot be used.

**Why this priority**: Predictable failure protects downstream operations from incomplete text.

**Independent Test**: Supply each invalid-input category and verify status, diagnostic stream, empty standard output, and unchanged existing files.

**Acceptance Scenarios**:

1. **Given** a missing path, **When** normalization is requested, **Then** the operation exits with status 2, reports a concise diagnostic on standard error, and emits no standard output.
2. **Given** a directory path, **When** normalization is requested, **Then** the operation exits with status 2, reports a concise diagnostic on standard error, and emits no standard output.
3. **Given** invalid UTF-8 anywhere in a file, including after a valid prefix, **When** normalization is requested, **Then** the operation exits with status 2, reports a concise diagnostic on standard error, and emits no standard output.

### Edge Cases

The acceptance cases include empty input, nonempty whitespace-only input, mixed CRLF/bare CR/LF endings, files without a final newline, repeated blank lines, trailing blank lines, preserved interior tabs/spaces, and Unicode whitespace that is not ASCII space or tab. Invalid UTF-8 after valid content must still produce no output. Input takes exactly one path and has no standard-input mode.

## Requirements *(mandatory)*

These requirements describe observable behavior; the approved fixture packet governs where historical wiki claims disagree.

### Functional Requirements

- **FR-001**: The operation MUST accept exactly one local file path and MUST NOT accept standard input as an alternate input mode.
- **FR-002**: Input MUST be decoded as strict UTF-8, preserving Unicode characters without Unicode normalization.
- **FR-003**: Normalization MUST trim only ASCII space and tab at each line edge, preserving every other character.
- **FR-004**: Normalization MUST preserve interior whitespace and every logical blank line, including all trailing blank lines.
- **FR-005**: Normalization MUST convert CRLF and bare CR line endings to LF.
- **FR-006**: Empty original input MUST produce empty output. For any nonempty original input, a terminating LF MUST be added if and only if the normalized result does not already end in LF. Every existing trailing LF MUST be preserved. Nonempty whitespace-only input trimmed to empty content MUST therefore produce one LF.
- **FR-007**: Successful normalized output MUST go only to standard output. The operation MUST NOT modify the input file or write another output file.
- **FR-008**: Missing files, directory paths, and invalid UTF-8 MUST each produce exit status 2, a concise standard-error diagnostic, and zero standard output, including when undecodable content follows a valid prefix.
- **FR-009**: The feature MUST NOT impose an explicit input-size limit.

### Key Entities

- **Input text**: Original file content whose emptiness, Unicode characters, whitespace, and logical lines govern normalization.
- **Normalized text**: The output resulting only from the specified edge trimming and line-ending rules.
- **Input rejection**: An unusable file request reported without normalized output or file mutation.

## Success Criteria *(mandatory)*

Users can verify outcomes directly from output, diagnostics, status, and unchanged source bytes.

### Measurable Outcomes

- **SC-001**: 100% of valid-input acceptance cases produce exactly the required output, including all whitespace, Unicode, empty-input, and final-LF boundaries.
- **SC-002**: 100% of the three specified rejection categories exit with status 2, emit a concise diagnostic, and emit zero standard output.
- **SC-003**: Source bytes remain unchanged in 100% of success and rejection cases involving existing files, and no output file is created.
- **SC-004**: Acceptance validation covers each of FR-001 through FR-009 and each error category with repeatable checks.

## Assumptions

The verified prerequisite is Feature 801. The approved packet and its direct-human approval record govern this synthetic feature; contradictory historical wiki claims about deleting blank lines, collapsing interior whitespace, exit status 1, or partial output do not govern it. The scope is one local file and a reusable normalization operation. Batch processing, network access, persistence, packaging, and external dependencies are excluded. No performance target or new product policy is inferred. There is no explicit size cap; available local resources remain an environmental constraint.
