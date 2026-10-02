# Implementation Plan: Normalize Text

**Branch**: `802-normalize-text` | **Date**: 2026-10-01 | **Spec**: [spec.md](spec.md)

## Summary

Design a deterministic Python standard-library CLI that reads exactly one file, strictly decodes UTF-8, applies the nine accepted policies, and emits UTF-8 bytes to stdout without modifying files. The current specification's accepted operator answers govern over the synthetic source/wiki pages that still describe open choices.

## Technical Context

**Language/Version**: Python 3; use the consumer's compatible interpreter, with no new runtime pin or dependency introduced.

**Primary Dependencies**: Standard library `argparse`, `pathlib`, `sys`, and `unittest`.

**Storage**: Read-only local input; no persistent state or output files.

**Testing**: Standard-library unit tests for the transformation and subprocess CLI checks for exit codes, byte channels and file preservation.

**Target Platform**: Local environments with Python 3 and filesystem/stdout access.

**Project Type**: Single local CLI.

**Performance Goals**: Linear transformation in input length; no invented numerical latency target.

**Constraints**: Strict UTF-8, exact LF bytes, no Unicode normalization, no stdin, no file mutation, no explicit product size cap, no network or external dependencies.

**Scale/Scope**: One file per invocation. Whole-file decoding and transformation use memory proportional to input; exceptionally large inputs remain subject to host resources. Streaming adds complexity and is deferred unless actual usage justifies it, without adding a product limit.

## Constitution Check

The pre-research gate passes: standard-library-only, local deterministic behavior, preserved human product/roadmap decisions, and unit-test validation. Planning authorizes no Git operation or consumer mutation beyond these requested design artifacts. The post-design gate also passes: the pure transformation and CLI adapter require no services, frameworks, persistence, packaging or external dependencies. No exception or constitutional amendment is needed.

## Research and Design

[Research](research.md) resolves technical choices without changing product scope. [Data model](data-model.md) defines the ephemeral values and pipeline. [CLI contract](contracts/cli.md) binds the external invocation and byte/error behavior. [Quickstart](quickstart.md) provides implementation-time validation commands; these commands have not run against an implementation in this planning session.

Read input bytes completely before publishing output. Strictly decode UTF-8, replace CRLF with LF before replacing remaining CR, split only on LF, trim only ASCII space/tab at each segment edge and rejoin with LF. Preserve empty segments so blank lines and existing trailing LF characters survive. Use original input emptiness to decide the final-LF rule: empty input stays empty; nonempty input adds one LF only if the normalized string lacks it. Encode to UTF-8 and write through binary stdout to avoid platform newline translation.

Separate the pure transformation from the argument/file/channel adapter. Normalize neither Unicode characters nor interior whitespace. Missing paths, directories and undecodable bytes must produce status 2, stderr diagnostics and no stdout. Define other read failures consistently as status 2 with no stdout as a technical error handling convention, without introducing another product feature. Diagnostics should identify the failure category without exposing input content.

## Requirement and Validation Coverage

| Requirement | Design and validation |
| --- | --- |
| FR-001 | Exactly one positional path, no stdin; reject zero/multiple arguments with status 2. |
| FR-002 | Strict UTF-8 decode/encode; compare composed/decomposed Unicode and non-ASCII whitespace bytes. |
| FR-003 | Trim only space/tab edges; retain other Unicode whitespace. |
| FR-004 | Preserve interior spacing and every empty segment, including trailing blank lines. |
| FR-005 | Replace CRLF then CR; compare mixed newline examples exactly. |
| FR-006 | Track original emptiness; test empty input and space/tab-only nonempty input separately. |
| FR-007 | Binary stdout only; compare input bytes before and after. |
| FR-008 | Read/decode before output; assert status 2, stderr and empty stdout for all three specified failures. |
| FR-009 | No cap; exercise a reasonably large fixture without treating its size as a product maximum. |

SC-001 uses exact acceptance vectors; SC-002 verifies each rejected category; SC-003 repeats invocations to compare byte-identical results. Full implementation validation remains future work.

## Project Structure

The documentation consists of `plan.md`, `research.md`, `data-model.md`, `contracts/cli.md` and `quickstart.md` in this feature directory. Proposed future source layout is `normalize_text.py` at the consumer root and `tests/test_normalize_text.py`. Neither exists as a result of this planning command. One small module with a pure normalization function and CLI entry adapter avoids unnecessary packages or abstractions.

## Complexity Tracking

There are no constitution violations or unresolved technical decisions. Whole-file memory usage is the material implementation tradeoff, not a new product size limit. This plan stops at design and does not generate tasks or claim acceptance.
