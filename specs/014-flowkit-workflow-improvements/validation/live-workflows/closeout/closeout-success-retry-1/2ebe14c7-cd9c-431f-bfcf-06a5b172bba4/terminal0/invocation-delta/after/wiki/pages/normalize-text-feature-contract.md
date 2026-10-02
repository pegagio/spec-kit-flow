---
title: Normalize Text Feature Contract
type: decision
sources: [S003]
updated: 2026-10-01
---

# Normalize Text Feature Contract

Feature 802 records nine accepted operator answers in its specification. Those answers resolve this feature's behavior while the original normalization and error documents remain pre-clarification sources with open questions; they do not retrospectively rewrite those documents. (S003)

## Normalization decisions

Strict UTF-8 decoding preserves Unicode characters without Unicode normalization. Only ASCII spaces and tabs are removed at line edges; interior whitespace and all blank lines, including trailing blank lines, are preserved. CRLF and bare CR become LF. (S003)

Empty input yields empty output. Originally nonempty input gains a terminating LF only when its normalized result lacks LF. Thus ASCII space followed by tab without a newline yields exactly one LF, while existing trailing LFs remain intact. (S003)

General whitespace stripping and broad Unicode line splitting were rejected because they would remove required characters or lose terminal separators. Literal LF separation and ASCII-only edge trimming preserve the approved distinctions. (S003)

## Input and error decisions

The utility accepts exactly one file path, with no stdin mode, and emits normalized UTF-8 to stdout without modifying input or writing another output file. Missing paths, directories and invalid UTF-8 produce exit status 2, stderr diagnostics and zero stdout. Invalid argument counts and other OS read failures use the same status/channel pattern. (S003)

Whole-file reading and strict decoding precede output, preventing a valid prefix from escaping before a later decoding failure. Buffering requires memory proportional to input size; there is no explicit product size cap, and environmental memory exhaustion remains a limitation. Streaming with equivalent output atomicity would require additional passes or storage and was deferred. (S003)

## Scope and evidence boundaries

The design uses Python 3.11 or later and the standard library for a local deterministic single-file CLI. Batch processing, network services, persistence, packaging and external dependencies remain excluded. Exact-byte transformation and rejection checks, repeated results, idempotence and unchanged input bytes are the specified validation strategy; passing automation does not establish human product or roadmap acceptance. (S003)

Related source questions: [Normalization](./normalization.md) and [Errors](./errors.md).
