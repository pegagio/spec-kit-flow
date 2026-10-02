# Implementation Plan: Normalize Text

**Branch**: `802-normalize-text` | **Date**: 2026-10-01 | **Spec**: [spec.md](spec.md)

## Summary

Build a local Python standard-library CLI that accepts exactly one file path, strictly decodes UTF-8, normalizes line boundaries and ASCII line-edge whitespace, and emits UTF-8 to stdout without file mutation. The operator's nine accepted choices govern this design; open synthetic source/wiki variants do not override them.

## Technical Context

**Language/Version**: Python 3.11 or newer, compatible standard-library subset; no dependency installation.
**Primary Dependencies**: `argparse`, `pathlib`, and `sys`; tests use `unittest`, `tempfile`, and `subprocess`.
**Storage**: Read-only local input file; no persistent result or database.
**Testing**: Pure transformation unit tests plus subprocess CLI tests for exact bytes, statuses, channels, and unchanged input.
**Target Platform**: Local operating systems with Python and binary stdout.
**Project Type**: Single CLI module, no packaging deliverable.
**Performance Goals**: Deterministic output; no invented throughput target.
**Constraints**: No network, external dependencies, Unicode normalization, file writes, stdin support, or explicit product size limit.
**Scale/Scope**: One file per invocation. Whole-file buffering costs O(n) memory and permits complete validation before emitting output; very large files may exhaust host resources.

## Constitution Check

Both pre-research and post-design gates pass. Only Python standard-library components are planned; execution is local and deterministic. All nine explicit product policies remain intact. Roadmap ownership and verified dependency 801 remain unchanged. Validation uses unit tests. No Git integration, publication, implementation, or changes to another consumer are authorized by this plan. No exceptions are required.

## Project Structure

The five planning outputs are `plan.md`, `research.md`, `data-model.md`, `contracts/cli.md`, and `quickstart.md` in this feature directory. The proposed implementation is `normalize_text.py` at the consumer root, with `tests/test_normalize_text.py`; these files are future implementation work, not created here. A single pure normalization function and a thin CLI entry point suffice; no shared framework is needed.

## Design and Requirement Coverage

| Requirement | Design responsibility | Validation |
|---|---|---|
| FR-001 | Argument parser requires exactly one path and never reads stdin | Zero/two argument subprocess cases |
| FR-002 | Read bytes and strict UTF-8 decode; encode output as UTF-8 without Unicode normalization | Invalid UTF-8, decomposed Unicode, non-ASCII whitespace |
| FR-003 | Apply `strip(" \t")` to each LF-separated segment | Edge ASCII versus interior/Unicode whitespace |
| FR-004 | Split/join with literal LF so empty and trailing segments survive | Interior and trailing blank lines |
| FR-005 | Replace CRLF first, then remaining CR with LF | Mixed newline and bare CR examples |
| FR-006 | Test original input emptiness; append LF for nonempty input only when result lacks LF | Empty and whitespace-only input |
| FR-007 | Emit validated bytes through binary stdout; never open any file for writing | Exact stdout and input byte comparison |
| FR-008 | Catch read/decode rejection before output, status 2 and stderr | Missing path, directory, malformed UTF-8 |
| FR-009 | No length guard; document host-resource limitation | Representative large-file test, static review |

SC-001 is covered by exact acceptance bytes, SC-002 by rejection channel/status assertions, and SC-003 by repeated invocations. Research resolves design choices in [research.md](research.md); [CLI contract](contracts/cli.md) defines observable behavior and [quickstart](quickstart.md) provides validation steps.

## Risks and Complexity Tracking

Whole-file buffering is deliberate: partial stdout cannot escape before decode validation. It may exhaust available memory for unusually large inputs; an arbitrary product size cap would violate FR-009. A future streaming design must retain rejection/output guarantees and is not required here. Diagnostics should be concise and deterministic in meaning; their exact prose is not a product constraint. No constitution violations or unresolved product decisions remain.
