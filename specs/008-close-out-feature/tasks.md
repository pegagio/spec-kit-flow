# Tasks: Close Out Feature

**Input**: Design artifacts in `specs/008-close-out-feature/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [routing contract](contracts/closeout-routing.md)

**Tests**: Add one disposable no-op missing-operation route test; review the other human decisions in source.

## Phase 1: Setup

Capture reviewed source and tested component coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/008-close-out-feature/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/008-close-out-feature/spec.md`, `specs/008-close-out-feature/plan.md`, and `specs/008-close-out-feature/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Confirm Completion Authority (P1)

**Goal**: Verify missing-operation stops before debrief and approved operations stay separate.

**Independent Test**: Inspect source and run a disposable missing-operation route.

- [x] T003 [US1] Verify completion-operation gate and missing/invalid stops in `workflows/speckit-flow-closeout/workflow.yml`
- [x] T004 [US1] Add and run the no-op missing-operation native route in `tests/test_bundle_lifecycle.py`

## Phase 4: User Story 2 - Review Roadmap Verification (P2)

**Goal**: Verify exact-patch approval precedes roadmap write.

**Independent Test**: Trace the debrief, approval gate, approved route, and stop routes.

- [x] T005 [US2] Verify debrief and exact-patch approval routing in `workflows/speckit-flow-closeout/workflow.yml`

## Phase 5: User Story 3 - Maintain Context and Review Commit Readiness (P3)

**Goal**: Verify wiki maintenance and commit readiness remain separate from a commit.

**Independent Test**: Trace the approved source route and manual fallback.

- [x] T006 [US3] Verify wiki ingest, lint, and commit-readiness gate in `workflows/speckit-flow-closeout/workflow.yml`
- [x] T007 [US3] Document the manual closeout path in `workflows/README.md`

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/008-close-out-feature/`, `workflows/speckit-flow-closeout/workflow.yml`, `workflows/README.md`, and the focused test
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before the user stories. T004 follows T003. Complete all stories before T008 and T009. Source routes may be inspected independently after T002.

## Implementation Strategy

Use the existing package, test the missing-operation stop, and document manual fallback. Preserve the reviewed YAML unless a concrete mismatch appears. A real completion operation remains outside this feature.
