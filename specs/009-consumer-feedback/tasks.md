# Tasks: Consumer Feedback

**Input**: Design artifacts in `specs/009-consumer-feedback/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [portability contract](contracts/feedback-portability.md)

**Tests**: Focused validation regression plus existing capture and report coverage.

## Phase 1: Setup

Capture source and release coordinates.

- [x] T001 Record source extension ID/version/digest, pinned bundle version, CLI version, and baseline commit in `specs/009-consumer-feedback/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/009-consumer-feedback/spec.md`, `specs/009-consumer-feedback/plan.md`, and `specs/009-consumer-feedback/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Capture Local Evidence (P1)

**Goal**: Preserve validated append-only capture and duplicate rejection.

**Independent Test**: Run focused capture tests.

- [x] T003 [US1] Verify observation validation, append-only journal writes, and duplicate rejection in `extensions/flow-feedback/scripts/python/workflow_feedback.py`

## Phase 4: User Story 2 - Preserve Portability (P2)

**Goal**: Reject embedded absolute host paths while allowing relative references and HTTPS URLs.

**Independent Test**: Focused positive and negative validator tests.

- [x] T004 [US2] Add embedded-path and allowed-reference tests in `extensions/flow-feedback/tests/test_workflow_feedback.py`
- [x] T005 [US2] Tighten path detection in `extensions/flow-feedback/scripts/python/workflow_feedback.py` and increment `extensions/flow-feedback/extension.yml` to `0.2.1`
- [x] T006 [US2] Run the focused unit suite and record its result in `specs/009-consumer-feedback/validation.md`

## Phase 5: User Story 3 - Keep Feedback as Evidence (P3)

**Goal**: Preserve local-only export and explicit transfer.

**Independent Test**: Inspect source and run the disposable lifecycle suite for the pinned archive.

- [x] T007 [US3] Verify report integrity, Markdown projection, and no source or authority mutation in extension commands and script
- [x] T008 [US3] Document source-versus-pinned-archive coordinates in `docs/feedback.md`, use the pinned release archive in `tests/test_bundle_lifecycle.py`, and run the disposable suite

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T009 Run convergence across `specs/009-consumer-feedback/`, extension source, tests, and docs
- [x] T010 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before story work. T004 precedes T005 and T006. Complete stories before T009 and T010.

## Implementation Strategy

Preserve the existing extension architecture, fix one proven privacy gap with focused tests, and carry the source version into the later catalog rebuild. Keep installed-package evidence separate from the new source behavior.
