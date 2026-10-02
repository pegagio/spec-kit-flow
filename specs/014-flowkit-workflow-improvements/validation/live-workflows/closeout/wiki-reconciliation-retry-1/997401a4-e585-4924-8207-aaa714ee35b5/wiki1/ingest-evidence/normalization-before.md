---
title: Normalization
type: concept
sources: [S001]
updated: 2026-10-01
---

# Normalization

The current isolated synthetic source leaves these product decisions open. This is controlled test construction, not ingestion evidence. (S001)

- **AMB-ENCODING**: Which decoding and Unicode normalization policy applies? (S001)
- **AMB-EDGE**: Which characters should be removed at line edges? (S001)
- **AMB-BLANKS**: How should interior whitespace and logical blank lines, including trailing blank lines, be handled? (S001)
- **AMB-NEWLINES**: What should happen to CRLF and bare CR line endings? (S001)
- **AMB-FINAL-LF**: What output should empty input produce, and when should a final LF be added? (S001)

Related decisions: [Errors](errors.md).
