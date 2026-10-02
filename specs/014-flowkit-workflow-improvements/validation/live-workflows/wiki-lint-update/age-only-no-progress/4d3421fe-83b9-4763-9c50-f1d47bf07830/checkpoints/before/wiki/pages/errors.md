---
title: Errors
type: reference
sources: [S002]
updated: 2026-01-01
---

# Errors

Invalid UTF-8, missing files, and directory inputs exit 2 with a concise stderr message and no stdout. (S002)

The tool reads one file path and writes normalized UTF-8 text to stdout. It provides no in-place writes, stdin mode, size limit, or external dependencies. (S002)

Related topic: [Normalization](./normalization.md).
