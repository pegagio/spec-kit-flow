# Implementation Plan: Consumer Feedback

**Branch**: `feature/time-machine-consumer-feedback` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Existing consumer feedback extension and a confirmed absolute-path validation gap.

## Summary

Keep the existing local capture and report architecture. Tighten path detection for absolute host paths embedded after punctuation, add focused positive and negative tests, and increment the source extension version to `0.2.1`. Validate source behavior now; rebuild the pinned catalog package in the later bundle-catalog feature.

## Technical Context

**Language/Version**: Python 3, extension manifest schema 1.0
**Primary Dependencies**: Python standard library; Specify `1.0.10.dev0+pegagio.2` for bundle validation
**Storage**: Consumer-owned JSONL journal and explicit report files
**Testing**: Focused extension unit tests and disposable bundle lifecycle suite
**Target Platform**: Initialized Codex consumer
**Project Type**: Versioned extension source package
**Performance Goals**: No new network or background activity
**Constraints**: Portable output, append-only capture, no authority mutation
**Scale/Scope**: One observation per capture; one journal per export

## Constitution Check

Consumer feedback remains local evidence and export remains an explicit handoff. Source validation does not confer maintainer approval. The source package is independently versioned, and the current released archive remains distinct until catalog repackaging. No new dependency or framework is needed. Analyze artifacts before implementation and converge afterward.

**Post-design check**: The contract preserves the evidence and authority boundary. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/009-consumer-feedback/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/feedback-portability.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
extensions/flow-feedback/extension.yml
extensions/flow-feedback/scripts/python/workflow_feedback.py
extensions/flow-feedback/tests/test_workflow_feedback.py
docs/feedback.md
```

**Structure Decision**: Keep validation in the extension's existing module and tests beside it. The bundle-catalog feature will repackage the incremented source.
