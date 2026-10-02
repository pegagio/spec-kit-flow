# Data Model: Normalize Text

This feature has transient values only; no database, stored result, or schema migration is required. The [CLI contract](contracts/cli.md) governs observable outcomes.

## Input File and Decoded Text

**Fields**: Exactly one path string, original byte sequence, and strictly decoded UTF-8 text. The path references a readable local file; a directory, missing path, or decoding failure produces rejection before stdout is written. Original byte/text emptiness is retained for the final-LF decision. Unicode code points remain unchanged except the specified ASCII edge and newline transformations.

## Normalized Result

**Fields**: LF-separated trimmed text and its UTF-8 byte encoding. Its derivation replaces CRLF then CR, trims only ASCII space/tab at segment edges, preserves interior whitespace and all empty segments, then adds one LF only for nonempty original input whose result lacks a final LF. Empty original input produces zero bytes. Existing trailing LF characters are never collapsed.

## Rejection

**Fields**: Failure category, stderr diagnostic, exit status 2, and empty stdout. Categories include missing path, directory, invalid UTF-8, invalid argument count, and other read errors. Diagnostics do not include input contents or raw tracebacks. Success has status 0 and empty stderr.

## Lifecycle and Relationships

An invocation moves from argument validation to read/decode, normalization, and output. Any validation/read/decode rejection terminates before output. Exactly one input produces exactly one result or rejection; no file is mutated. Repeated invocations on unchanged input yield identical result bytes and status. Values are discarded after exit; memory grows linearly with input size and no explicit product limit is enforced.
