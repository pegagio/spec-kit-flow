---
title: Errors
type: reference
sources: [S002]
updated: 2026-10-01
---

# Errors

The command reads exactly one file path and writes normalized UTF-8 text to stdout. (S002)

Invalid UTF-8, missing files, and directories exit 2 with a concise stderr message and no stdout. (S002)

The contract excludes in-place writes, stdin mode, size limits, and external dependencies. (S002)
