# Research: Normalize Text

All significant product decisions are already approved in [spec.md](spec.md). This phase resolves implementation choices against those requirements and the constitution; no external integration or unresolved technology research is required.

## Transformation and Unicode

**Decision**: Strictly decode UTF-8 bytes, replace CRLF then bare CR with LF, split on literal LF, trim only ASCII space/tab from each segment, and join with LF. Preserve Unicode code points without normalization.

**Rationale**: Literal separators retain all blank and trailing segments; explicit trimming avoids Python's broader Unicode whitespace semantics. CRLF must be replaced before CR to avoid doubling boundaries.

**Alternatives considered**: Generic whitespace stripping and `splitlines()` lose distinctions required by FR-002–FR-005. Unicode normalization is explicitly excluded.

## Empty Input and Final Newline

**Decision**: Base emptiness on the original input, not the normalized result. Empty input yields empty output; nonempty input gets a terminating LF only when absent after transformation.

**Rationale**: A space followed by a tab is nonempty input and must yield exactly one LF even though trimming removes its content. Existing trailing LF characters are preserved.

**Alternatives considered**: Checking transformed emptiness would incorrectly emit nothing for whitespace-only input; always appending would add unwanted trailing blank lines.

## CLI, I/O, and Failure Atomicity

**Decision**: One local script with an argument parser, read-only binary input, strict decoding, pure transformation, and binary UTF-8 stdout. Prepare the complete output before writing. Invalid argument counts, missing paths, directories, undecodable input, and other read failures return status 2 with stderr diagnostics and empty stdout.

**Rationale**: Standard-library-only code meets the constitution and avoids platform newline/encoding translation. Handling other read failures the same way is a conservative technical error policy, not a new product capability.

**Alternatives considered**: In-place editing, stdin, and output-file options contradict approved scope. Streaming adds complexity to no-partial-output guarantees; whole-file buffering is acceptable without a promised resource ceiling.

## Resource and Validation Strategy

**Decision**: Impose no product size limit. Use standard-library unit tests and subprocess checks with temporary files, including representative large input and repeated runs.

**Rationale**: FR-009 permits natural host resource limits without inventing a cap. Exact byte assertions catch newline, Unicode, channel, and blank-line regressions.

**Alternatives considered**: External test frameworks and benchmarks add dependencies or unsupported targets. No NEEDS CLARIFICATION items remain. Both constitution gates pass without exceptions.
