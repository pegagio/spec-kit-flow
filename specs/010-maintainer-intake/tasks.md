# Tasks: Maintainer Feedback Intake

**Input**: Design artifacts in `specs/010-maintainer-intake/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [validation contract](contracts/intake-validation.md)

**Tests**: Focused intake validation regressions and the existing disposable handoff test.

## Phase 1: Setup

Capture reviewed source and tested component coordinates.

- [x] T001 Record maintainer extension ID/version/digest, CLI version, and baseline commit in `specs/010-maintainer-intake/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/010-maintainer-intake/spec.md`, `specs/010-maintainer-intake/plan.md`, and `specs/010-maintainer-intake/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Validate Transferred Evidence (P1)

**Goal**: Reject nonportable reports before writing maintainer records.

**Independent Test**: Valid, tampered, and embedded-path report tests.

- [x] T003 [US1] Add recomputed-digest embedded-path, missing-field, and digest-spelling tests in `extensions/speckit-flow-feedback-maintainer/tests/test_workflow_feedback_intake.py`
- [x] T004 [US1] Align report path and observation-schema validation in `extensions/speckit-flow-feedback-maintainer/scripts/python/workflow_feedback_intake.py` with consumer source

## Phase 4: User Story 2 - Record a Safe Proposal (P2)

**Goal**: Reject sensitive operator text before writing triage.

**Independent Test**: Rationale and receipt-time validation tests with no created records.

- [x] T005 [US2] Add nonportable-rationale and receipt-time tests in `extensions/speckit-flow-feedback-maintainer/tests/test_workflow_feedback_intake.py`
- [x] T006 [US2] Validate rationale and receipt time before persistence, increment `extensions/speckit-flow-feedback-maintainer/extension.yml` to `0.1.1`, and document the behavior in its `README.md`

## Phase 5: User Story 3 - Preserve Duplicate Relationships (P3)

**Goal**: Keep repeat reports as linked evidence, not new proposals.

**Independent Test**: Existing duplicate test and read-only record inspection.

- [x] T007 [US3] Verify duplicate relationship and proposal-only behavior in the maintainer script and existing `feedback/` records
- [x] T008 [US3] Run the maintainer unit suite and disposable lifecycle suite; record evidence limits in `specs/010-maintainer-intake/validation.md`

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T009 Run convergence across `specs/010-maintainer-intake/`, maintainer source, tests, docs, and feedback records
- [x] T010 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before story work. T003 precedes T004; T005 precedes T006. Complete stories before T009 and T010.

## Implementation Strategy

Keep the maintainer-only architecture and record format. Tighten validation at its trust boundary and leave the existing inbox and triage evidence untouched.
