# Tasks: Generate Implementation Tasks

**Input**: Design artifacts in `specs/004-generate-tasks/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [workflow contract](contracts/task-generation.md)

**Tests**: Verify source routing and one disposable no-op route; generated task quality requires human review.

## Phase 1: Setup

Capture the reviewed source and tested component coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/004-generate-tasks/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/004-generate-tasks/spec.md`, `specs/004-generate-tasks/plan.md`, and `specs/004-generate-tasks/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Produce a Reviewable Task Proposal (P1)

**Goal**: Verify proposal generation from reviewed design and explicit human-work surfacing.

**Independent Test**: Inspect command arguments and confirm the installed workflow resolves in a disposable consumer.

- [x] T003 [US1] Verify `speckit.tasks` invocation and surprising-human-work wording in `workflows/speckit-flow-tasks/workflow.yml`
- [x] T004 [US1] Confirm installed task workflow resolution in `tests/test_bundle_lifecycle.py` and record its evidence limit in `specs/004-generate-tasks/validation.md`

## Phase 4: User Story 2 - Route the Reviewed Proposal (P2)

**Goal**: Confirm the review choices cannot start implementation directly.

**Independent Test**: Exercise a no-op deferred route and inspect every other branch.

- [x] T005 [US2] Verify analysis, replanning, amendment, deferral, and invalid routes in `workflows/speckit-flow-tasks/workflow.yml`
- [x] T006 [US2] Add a no-op `defer` task-review route to `tests/test_bundle_lifecycle.py`, run the suite, and record the result in `specs/004-generate-tasks/validation.md`
- [x] T007 [US2] Document the manual task-generation and review path in `workflows/README.md`

## Phase 5: Polish and Validation

Close remaining build gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/004-generate-tasks/`, `workflows/speckit-flow-tasks/workflow.yml`, `workflows/README.md`, and `tests/test_bundle_lifecycle.py`
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before the user stories. T004 follows T003; T006 and T007 follow T005. Complete both stories before T008 and T009. Edits to the lifecycle test remain sequential.

## Implementation Strategy

Keep the reviewed workflow source unless a concrete mismatch is found. Validate native routing, explain the manual fallback, and leave task proposal acceptance under human control.
