---
title: Errors
type: reference
sources: [S002, S003]
updated: 2026-10-01
---

# Errors

The current isolated synthetic source leaves these product decisions open. This is controlled test construction, not ingestion evidence. (S002)

- **AMB-INPUT**: Accept exactly one file path, stdin, or both? (S002)
- **AMB-OUTPUT**: Should output go to stdout, update the input in place, or be written to another file? (S002)
- **AMB-ERRORS**: What exit status and output channels apply to missing paths, directories, and undecodable input? (S002)
- **AMB-SIZE**: Should the local utility impose an input size limit? (S002)

Related decisions: [Normalization](normalization.md).

Feature-specific accepted answers appear in [Normalize Text Feature Contract](./normalize-text-feature-contract.md); the original source questions above remain unchanged. (S003)
