---
title: Normalize Text Feature Contract
type: decision
sources: [S003]
updated: 2026-10-01
---

# Normalize Text Feature Contract

The nine operator answers in `specs/802-normalize-text/spec.md` define the feature-specific contract. The original normalization and error documents retain their pre-clarification questions; the specification explicitly distinguishes their open state from these accepted answers. (S003)

## Input and output

Accept exactly one local file path, with no stdin mode. Emit normalized UTF-8 bytes to stdout without modifying input or creating an output file. Successful processing returns status 0 with empty stderr; dash-prefixed paths use `--`. (S003)

Missing paths, directory paths and undecodable input each return status 2, a category diagnostic on stderr and no stdout. Invalid argument count and other OS read failures use the same status/channel pattern. Diagnostic wording need not be fixed. Complete reading and strict UTF-8 decoding before output ensures late invalid bytes cannot emit a prefix. (S003)

## Normalization and edge cases

Decode strictly as UTF-8 and preserve Unicode without normalization. Convert CRLF to LF before converting remaining CR. Trim only ASCII spaces and tabs at each line edge; preserve interior whitespace, other Unicode characters and all blank lines, including trailing blank lines. (S003)

Empty original input stays empty. Nonempty original input gains a terminating LF only when the normalized result lacks one; existing trailing LFs remain intact. Thus `" \t"` becomes `"\n"`, `"a\rb"` becomes `"a\nb\n"`, and `" a  b \r\n\r\n"` becomes `"a  b\n\n"`. Non-ASCII edge whitespace and decomposed Unicode remain unchanged apart from a needed final LF. (S003)

## Design decisions and limits

The reviewed design separates a pure transform from argument validation, reading and output. Python 3.11 or later and the standard library support a local deterministic CLI; transient values require no persistence. Exact byte comparisons and subprocess channel/status checks are the selected validation approach. These are design choices, not a claim of project acceptance. (S003)

Literal LF splitting preserves trailing segments and avoids the extra Unicode separator behavior of `splitlines()`. General whitespace stripping, fallback decoding and file mutation conflict with the accepted contract. Full buffering protects empty stdout on decoding failure and takes memory proportional to input size; streaming with that guarantee would require additional passes or storage. No explicit product size threshold applies, while environmental memory exhaustion remains possible. (S003)

Original question context: [Normalization](./normalization.md) and [Errors](./errors.md). (S003)
