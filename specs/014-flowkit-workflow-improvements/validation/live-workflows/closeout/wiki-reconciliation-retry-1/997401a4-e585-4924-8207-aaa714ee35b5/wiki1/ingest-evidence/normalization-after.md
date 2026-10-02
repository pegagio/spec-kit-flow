---
title: Normalization
type: concept
sources: [S001]
updated: 2026-10-01
---

# Normalization

The normalization contract records the operator-approved policies for the disposable Feature 802 fixture. (S001)

- **Encoding**: Decode strictly as UTF-8 and preserve Unicode code points without Unicode normalization. (S001)
- **Line edges**: Trim only ASCII spaces and tabs at each line edge. (S001)
- **Whitespace and blank lines**: Preserve interior whitespace, every logical blank line, and all trailing blank lines. (S001)
- **Line endings**: Convert CRLF and bare CR to LF. (S001)
- **Final LF**: Original empty input produces empty output. For originally nonempty input, add one final LF only when the normalized result lacks one; whitespace-only nonempty input therefore produces LF. (S001)

Related decisions: [Errors](errors.md).
