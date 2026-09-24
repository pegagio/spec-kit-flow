# Tasks: Implement Eligible Work

**Input**: Design artifacts in `specs/006-implement-eligible-work/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [routing contract](contracts/implementation-routing.md)

**Tests**: Verify source routing and a disposable no-op blocked route; real task execution requires human review.

## Phase 1: Setup

Capture reviewed source and tested component coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/006-implement-eligible-work/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/006-implement-eligible-work/spec.md`, `specs/006-implement-eligible-work/plan.md`, and `specs/006-implement-eligible-work/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Execute Eligible Tasks (P1)

**Goal**: Verify selected-agent, prerequisite, and evidence boundaries.

**Independent Test**: Inspect the implementation command and confirm the installed workflow resolves.

- [x] T003 [US1] Verify bounded `speckit.implement` arguments and the result gate in `workflows/speckit-flow-implement/workflow.yml`
- [x] T004 [US1] Confirm installed implementation workflow resolution in `tests/test_bundle_lifecycle.py` and record its evidence limit in `specs/006-implement-eligible-work/validation.md`

## Phase 4: User Story 2 - Route Discoveries Back to Artifacts (P2)

**Goal**: Verify each named return path stops implementation.

**Independent Test**: Trace the four return commands and confirm no route restarts implementation.

- [x] T005 [US2] Verify analysis, specification, plan, and task return routes in `workflows/speckit-flow-implement/workflow.yml`

## Phase 5: User Story 3 - Stop for Blockers (P3)

**Goal**: Verify blocker and invalid results stop without scope expansion.

**Independent Test**: Exercise a no-op blocked route and follow the manual fallback.

- [x] T006 [US3] Add a no-op `blocked` implementation route to `tests/test_bundle_lifecycle.py`, run the suite, and record the result in `specs/006-implement-eligible-work/validation.md`
- [x] T007 [US3] Document the manual implementation and flow-back path in `workflows/README.md`

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/006-implement-eligible-work/`, `workflows/speckit-flow-implement/workflow.yml`, `workflows/README.md`, and `tests/test_bundle_lifecycle.py`
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before the user stories. T004 follows T003; T006 and T007 follow T005. Complete all stories before T008 and T009. The return routes can be inspected independently after T002.

## Implementation Strategy

Keep reviewed source unless a concrete mismatch is found. Exercise a safe terminal route in a disposable consumer, document manual fallback, and leave live task results and acceptance to the operator.
