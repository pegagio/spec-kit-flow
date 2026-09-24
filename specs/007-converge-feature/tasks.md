# Tasks: Converge Feature

**Input**: Design artifacts in `specs/007-converge-feature/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [routing contract](contracts/convergence-routing.md)

**Tests**: Reuse the existing disposable no-op clean-route test; real gap assessment requires human review.

## Phase 1: Setup

Capture reviewed source and tested component coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/007-converge-feature/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/007-converge-feature/spec.md`, `specs/007-converge-feature/plan.md`, and `specs/007-converge-feature/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Assess Implementation Against Intent (P1)

**Goal**: Verify assessment precedes a human clean decision and closeout stays separate.

**Independent Test**: Inspect source and run the existing disposable clean-route lifecycle suite.

- [x] T003 [US1] Verify `speckit.converge`, the result gate, and clean stop in `workflows/speckit-flow-converge/workflow.yml`
- [x] T004 [US1] Run the existing clean-route coverage in `tests/test_bundle_lifecycle.py` and record its limit in `specs/007-converge-feature/validation.md`

## Phase 4: User Story 2 - Route Remaining Work Through Analysis (P2)

**Goal**: Verify remediation returns through analysis and a later convergence run.

**Independent Test**: Trace the remediation commands and stop text.

- [x] T005 [US2] Verify remediation-task analysis and separate implementation handoff in `workflows/speckit-flow-converge/workflow.yml`

## Phase 5: User Story 3 - Preserve a Blocker (P3)

**Goal**: Verify blockers and invalid choices do not claim convergence.

**Independent Test**: Trace both stop routes and follow manual instructions.

- [x] T006 [US3] Verify blocked and invalid-result stops in `workflows/speckit-flow-converge/workflow.yml`
- [x] T007 [US3] Document the manual convergence and remediation path in `workflows/README.md`

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/007-converge-feature/`, `workflows/speckit-flow-converge/workflow.yml`, and `workflows/README.md`
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before the user stories. T004 follows T003. Complete all stories before T008 and T009. The source routes may be inspected independently after T002.

## Implementation Strategy

Use the existing clean-route integration test. Keep the reviewed YAML unless a concrete mismatch is found, document manual fallback, and leave real convergence judgment to human review.
