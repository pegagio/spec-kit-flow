# Research: Normalize Text

This phase resolves technical choices from the approved specification and constitution. No significant product unknowns remain and no external dependency or integration requires external research. No research agent or network lookup was needed.

## Transformation and Newlines

**Decision**: Replace CRLF with LF before replacing remaining CR. Split on literal LF, trim each segment using only ASCII space/tab, and join with LF. For nonempty original input append LF only if the result lacks one.

**Rationale**: Literal LF splitting preserves trailing empty segments and avoids treating other Unicode separators as newline characters. Testing original input emptiness preserves the required `" \t"` → `"\n"` case.

**Alternatives considered**: `splitlines()` recognizes extra Unicode separators and can lose terminal separators. General whitespace stripping removes characters FR-003 requires preserving. Neither fits the contract.

## Encoding and Output Atomicity

**Decision**: Read raw bytes, decode with strict UTF-8, normalize, encode UTF-8 and then emit binary stdout. Do not normalize Unicode. Complete reading/decoding before emission.

**Rationale**: Explicit encoding avoids locale dependence; buffering ensures undecodable input produces no stdout even if invalid bytes occur late.

**Alternatives considered**: Text-mode universal newline handling obscures precise transformation order. Streaming emits partial output before late failures unless backed by a second pass or temporary output, adding complexity and file writes.

## Interfaces and Error Handling

**Decision**: A thin `normalize_text.py` CLI accepts exactly one positional path. Missing input, directory input and decoding failure report a concise category diagnostic to stderr and exit 2. Standard argument parsing rejects invalid arity. Use ordinary OS read failures in the same diagnostic path.

**Rationale**: This preserves all approved observable choices without stdin, output-file, batch or network interfaces.

**Alternatives considered**: File mutation and separate output paths contradict FR-007; fallback decoding contradicts FR-002. An explicit size cap contradicts FR-009.

## Validation and Delivery Boundary

**Decision**: Standard-library unittest covers a pure transform and subprocess CLI behavior, using temporary fixtures and exact bytes.

**Rationale**: Constitution requires unit tests and no external dependencies. Subprocess checks expose status/channel errors that pure function tests cannot detect.

**Alternatives considered**: Third-party test tools or packaging introduce unnecessary dependencies. This phase creates documents only; tests and implementation remain future work.
