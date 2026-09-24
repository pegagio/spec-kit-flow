# Tasks: Plan Implementation

**Input**: Design artifacts in `specs/003-plan-implementation/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [workflow contract](contracts/planning.md)

**Tests**: Verify source routing and one disposable no-op terminal route; plan quality requires separate human review.

## Phase 1: Setup

Capture reviewed source and test coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/003-plan-implementation/validation.md`

## Phase 2: Foundation

Check consistency before implementation.

- [x] T002 Analyze `specs/003-plan-implementation/spec.md`, `specs/003-plan-implementation/plan.md`, and `specs/003-plan-implementation/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Plan a Ready Feature (P1)

**Goal**: Verify that technical planning follows explicit readiness and stops for review.

**Independent Test**: Inspect the gate and command order in source, then confirm the installed workflow resolves in the lifecycle suite.

- [x] T003 [US1] Verify the readiness gate precedes `speckit.plan` and the plan route stops before task generation in `workflows/speckit-flow-plan/workflow.yml`
- [x] T004 [US1] Confirm the installed plan workflow resolves in `tests/test_bundle_lifecycle.py` and record evidence limits in `specs/003-plan-implementation/validation.md`

## Phase 4: User Story 2 - Return or Defer Safely (P2)

**Goal**: Verify return, deferral, and invalid choices do not invoke planning.

**Independent Test**: Exercise the no-op deferred route and inspect every non-plan branch.

- [x] T005 [US2] Verify return-to-clarification, defer, and invalid-decision branches in `workflows/speckit-flow-plan/workflow.yml`
- [x] T006 [US2] Add a no-op `defer` planning route to `tests/test_bundle_lifecycle.py`, run the suite, and record the result in `specs/003-plan-implementation/validation.md`
- [x] T007 [US2] Document the manual planning route in `workflows/README.md` with its readiness and stop boundaries

## Phase 5: Polish and Validation

Close implementation gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/003-plan-implementation/`, `workflows/speckit-flow-plan/workflow.yml`, `workflows/README.md`, and `tests/test_bundle_lifecycle.py`
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before either story. T004 follows T003; T006 and T007 follow T005. Complete both stories before T008 and T009. Changes to the same lifecycle test are sequential.

## Implementation Strategy

Inspect the reviewed package before changing it. Exercise a safe terminal route in a disposable consumer, retain the manual path, and report live planning quality as an acceptance limit.
