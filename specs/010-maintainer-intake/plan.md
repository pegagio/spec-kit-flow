# Implementation Plan: Maintainer Feedback Intake

**Branch**: `feature/time-machine-maintainer-intake` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Existing maintainer intake extension and two observed sensitive-content validation gaps.

## Summary

Preserve the existing maintainer-only intake architecture. Align the report path check with consumer `0.2.1`, validate free-text rationale and receipt time before persistence, add focused rejection tests, and increment the maintainer extension source version to `0.1.1`. Verify current inbox and triage records without rewriting them.

## Technical Context

**Language/Version**: Python 3, extension manifest schema 1.0
**Primary Dependencies**: Python standard library; consumer portable report schema 1.0
**Storage**: Source-repository `feedback/inbox/` and `feedback/triage/` JSON files
**Testing**: Maintainer unit suite and disposable bundle lifecycle transfer case
**Target Platform**: Maintainer checkout, not a consumer installation
**Project Type**: Separate maintainer extension
**Performance Goals**: No background activity or network transfer
**Constraints**: Intake only; no source or authority mutation
**Scale/Scope**: One transferred report per invocation

## Constitution Check

Consumer reports remain evidence. Maintainer intake validates, stores, and proposes a disposition without changing workflow source or authority. Any accepted proposal re-enters normal specification flow. No new dependency or framework is required. Analyze artifacts before implementation and converge afterward.

**Post-design check**: The contract and tests preserve these boundaries. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/010-maintainer-intake/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/intake-validation.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
extensions/speckit-flow-feedback-maintainer/extension.yml
extensions/speckit-flow-feedback-maintainer/scripts/python/workflow_feedback_intake.py
extensions/speckit-flow-feedback-maintainer/tests/test_workflow_feedback_intake.py
extensions/speckit-flow-feedback-maintainer/README.md
feedback/inbox/
feedback/triage/
```

**Structure Decision**: Keep the independent maintainer component. Update only its validator, tests, version, and documentation; preserve existing feedback records as evidence.
