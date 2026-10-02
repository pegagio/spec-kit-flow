---
title: Normalization
type: concept
sources: [S001]
updated: 2026-10-01
---

# Normalization

Normalization strips ASCII spaces and tabs from each line edge while preserving interior whitespace and every logical blank line, including trailing blank lines. (S001)

CRLF and bare CR become LF. Empty input produces empty output. Nonempty input receives a terminating LF only when its normalized output lacks one; existing trailing LF characters remain intact. Unicode is preserved without normalization. (S001)

Related contract: [Errors](errors.md).
