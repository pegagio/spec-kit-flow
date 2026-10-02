# Implementation Plan: Normalize Text

**Branch**: `802-normalize-text` | **Date**: 2026-10-01 | **Spec**: [spec.md](spec.md)

**Input**: `specs/802-normalize-text/spec.md`, including all nine accepted clarification answers.

## Summary

Provide a local Python CLI that reads exactly one UTF-8 file and emits normalized UTF-8 bytes to stdout without modifying files. Separate a pure normalization function from path reading, argument validation and output channels. Preserve the approved product rules in [the CLI contract](contracts/cli.md). This document authorizes design only; implementation and acceptance remain separate decisions.

## Technical Context

**Language/Version**: Python 3.11 or later, using the consumer's compatible Python runtime.

**Primary Dependencies**: Python standard library only (`argparse`, `pathlib`, `sys`, `unittest`).

**Storage**: Read-only local input file; no persisted results or database.

**Testing**: Standard-library `unittest` for transformation, plus subprocess CLI checks with temporary files and exact byte assertions.

**Target Platform**: Local environments with Python and binary stdout/stderr; no network service.

**Project Type**: Single CLI module with a reusable pure transform.

**Performance Goals**: Linear work in input length; no numeric latency target is specified.

**Constraints**: Strict UTF-8, deterministic output, no Unicode normalization, no product size limit, no filesystem writes. Decode the complete input before stdout emission to guarantee empty stdout on invalid encoding.

**Scale/Scope**: Exactly one file per invocation. Full buffering uses memory proportional to file size; runtime resource exhaustion remains an environmental limitation, not an invented product size threshold.

## Constitution Check

Both design gates pass; no exceptions are needed.

| Principle | Before research | After design |
|---|---|---|
| Standard library only | PASS: no external dependency proposed | PASS: all selected modules ship with Python |
| Local and deterministic | PASS: file input and explicit byte rules | PASS: no network, locale-dependent decoding or Unicode normalization |
| Explicit human decisions | PASS: nine answers govern design | PASS: FR-001–FR-009 map to contract and validation; roadmap unchanged |
| No integration or another consumer change | PASS: planning scope only | PASS: only five planning documents created |
| Unit-test behavior validation | PASS: unittest strategy selected | PASS: transform and CLI cases specified in quickstart |

## Project Structure

The design adds a small module rather than a package or service hierarchy.

```text
specs/802-normalize-text/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
└── contracts/cli.md

normalize_text.py          # proposed CLI and pure transform
tests/test_normalize_text.py # proposed standard-library tests
```

The source paths are proposed, not created by planning. Keep `normalize(text)` pure and `main(argv)` responsible for input/output. No persistent domain objects are necessary.

## Requirement Coverage and Validation

Every requirement has an observable check rather than relying on implementation structure.

| Requirement | Design responsibility | Validation |
|---|---|---|
| FR-001 | CLI accepts one positional path, no stdin mode | zero/two argument rejection and one-path success |
| FR-002 | read bytes and strict UTF-8 decode; no normalization | invalid bytes, decomposed Unicode and non-ASCII whitespace |
| FR-003 | trim only ASCII space/tab at each LF-delimited line edge | leading/trailing ASCII trim and retained non-ASCII edge characters |
| FR-004 | split on literal LF preserving empty segments | interior whitespace and trailing blank line exact bytes |
| FR-005 | replace CRLF first, then bare CR with LF | mixed newline fixtures |
| FR-006 | test original input emptiness; conditionally append LF | empty, whitespace-only, terminated and unterminated fixtures |
| FR-007 | On successful normalization, replace the input file contents with the normalized UTF-8 bytes; do not emit successful output to stdout | normalized bytes persisted in the input path |
| FR-008 | catch read/decode failures before output | missing/directory/invalid UTF-8: status 2, stderr and empty stdout |
| FR-009 | no input length check | large finite fixture, inspection for product limit |

SC-001 follows exact byte comparisons; SC-002 follows rejection channel/status assertions; SC-003 repeats fixtures and compares bytes/status. CLI usage errors use argparse's standard status 2; additional OS read failures receive the same diagnostic treatment for a coherent local CLI, without changing the three required rejection cases.

## Complexity Tracking

No constitutional violations or additional frameworks are proposed. Full buffering is deliberately simpler than streaming and protects the no-partial-output contract. It can consume substantial memory for large files; streaming with guaranteed empty stdout on late decoding failure would require a second pass or temporary storage and is deferred.
