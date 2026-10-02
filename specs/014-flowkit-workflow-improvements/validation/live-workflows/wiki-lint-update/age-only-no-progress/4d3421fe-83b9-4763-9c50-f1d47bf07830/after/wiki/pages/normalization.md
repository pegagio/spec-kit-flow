---
title: Normalization
type: concept
sources: [S001]
updated: 2026-01-01
---

# Normalization

Normalization strips ASCII spaces and tabs from each line edge while preserving interior whitespace and every logical blank line, including trailing blank lines. (S001)

CRLF and bare CR become LF. Empty input produces empty output. For nonempty input, a terminating LF is added only when the normalized output does not already end in LF; existing trailing LF characters are preserved. (S001)

Unicode is preserved without normalization. (S001)

Related topic: [Errors](./errors.md).
