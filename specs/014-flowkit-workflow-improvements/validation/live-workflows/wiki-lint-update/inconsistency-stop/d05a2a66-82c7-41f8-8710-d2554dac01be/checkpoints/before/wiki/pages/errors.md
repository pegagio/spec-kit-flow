---
title: Errors
type: reference
sources: [S001, S002]
updated: 2026-10-01
---

# Errors

Invalid UTF-8, missing files, and directory inputs exit 2 with a concise stderr message and no stdout. (S002)

The tool reads one file path and writes normalized UTF-8 text to stdout. It provides no in-place writes, stdin mode, size limit, or external dependencies. (S002)

Related topic: [Normalization](./normalization.md).

The normalization contract also declares invalid UTF-8 exits 1 with partial stdout (S001), conflicting with the error contract exit 2 and no stdout (S002). Authority is unresolved.

> ⚠ conflict: S001 requires exit 1 with partial stdout; S002 requires exit 2 with no stdout. Both are authoritative and no precedence decision exists.
