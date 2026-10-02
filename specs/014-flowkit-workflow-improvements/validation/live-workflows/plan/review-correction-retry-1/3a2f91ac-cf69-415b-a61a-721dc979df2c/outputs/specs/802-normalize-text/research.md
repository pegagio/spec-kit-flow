# Research: Normalize Text

The specification and constitution answer all product questions. This bounded design research uses the accepted contract and standard-library behavior; no external dependency or uncertain external API requires a separate research delegate.

## Transformation and Byte Channels

**Decision**: Read bytes, strictly decode UTF-8, transform strings with explicit CRLF/CR replacements and LF splitting, then encode UTF-8 to binary stdout.

**Rationale**: Text-mode universal newline/output translation and `splitlines()` can silently broaden the recognized separators. Explicit LF splitting preserves trailing empty segments and non-ASCII characters. Trim with exactly ASCII space and tab rather than general Unicode whitespace. CRLF replacement must precede bare CR replacement.

**Alternatives considered**: General `strip()` violates the accepted character policy; `splitlines()` recognizes more separators and obscures trailing blank lines; Unicode normalization violates FR-002.

## Input, Errors and Size

**Decision**: Use one positional file path with standard-library argument parsing. Complete read/decode before stdout. Missing paths, directories and undecodable inputs fail with status 2, stderr diagnostics and no stdout. Handle other read errors through the same adapter convention.

**Rationale**: This directly implements the accepted channels and avoids partial successful output on known input failures. Binary stdout avoids host newline translation.

**Alternatives considered**: Stdin, in-place updates, separate output files and explicit limits conflict with accepted answers. Whole-file processing is simple and linear but requires proportional memory; streaming is a future technical optimization only if justified, with identical semantics and no product cap.

## Empty Input and Final LF

**Decision**: Preserve original emptiness separately from normalized emptiness. Empty input yields empty output. Nonempty input receives a final LF only when needed; existing trailing LFs remain.

**Rationale**: A space/tab-only file normalizes to an empty string before finalization but must yield one LF. Checking only normalized emptiness would violate the exact accepted example.

**Alternatives considered**: Always append LF duplicates trailing separators; discard empty segments loses blank lines.

## Validation

**Decision**: Use `unittest` for the pure function and subprocess adapter checks, with byte-exact comparisons and unchanged-file assertions.

**Rationale**: The constitution requires unit tests and prohibits external dependencies. Repeatability checks cover deterministic behavior. No benchmark or new performance threshold is required.

**Alternatives considered**: External test frameworks introduce an unnecessary dependency. All technical unknowns are resolved; no NEEDS CLARIFICATION remains.
