---
title: Errors
type: reference
sources: [S002, S003]
updated: 2026-10-01
---

# Errors

The local text utility accepts exactly one local file path and writes UTF-8 bytes to stdout. It does not read stdin, change the input, or create an output file. (S002)

Missing paths, directories, and input that cannot be decoded fail with exit status 2. Diagnostics go to stderr, and these failures produce no stdout. (S002)

There is no explicit product size limit. The utility buffers the complete input, so ordinary environmental memory limits can still apply. (S002)

Related decisions: [Normalization](normalization.md).

[Normalize Text Contract](normalize-text-contract.md) records success status and channels, dash-leading path syntax, argument-count validation and other OS read-failure behavior. (S003)
