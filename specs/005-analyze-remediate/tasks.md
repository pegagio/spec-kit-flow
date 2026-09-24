# Tasks: Analyze and Remediate Artifacts

**Input**: Design artifacts in `specs/005-analyze-remediate/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [routing contract](contracts/analysis-routing.md)

**Tests**: Verify source route structure and a disposable no-op clean route; real classification quality requires human review.

## Phase 1: Setup

Capture reviewed source and tested component coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/005-analyze-remediate/validation.md`

## Phase 2: Foundation

Check consistency before implementation.

- [x] T002 Analyze `specs/005-analyze-remediate/spec.md`, `specs/005-analyze-remediate/plan.md`, and `specs/005-analyze-remediate/tasks.md`, then reconcile material findings

## Phase 3: User Story 1 - Review a Read-Only Analysis (P1)

**Goal**: Confirm analysis precedes disposition and clean results stop before implementation.

**Independent Test**: Inspect the source command order and run a no-op clean route in a disposable consumer.

- [x] T003 [US1] Verify read-only `speckit.analyze` precedes the gate and `clean` stops in `workflows/speckit-flow-analyze-remediate/workflow.yml`
- [x] T004 [US1] Add installed-workflow resolution and a no-op `clean` route to `tests/test_bundle_lifecycle.py`, run the suite, and record limits in `specs/005-analyze-remediate/validation.md`

## Phase 4: User Story 2 - Flow Routine Findings Back (P2)

**Goal**: Verify the smallest artifact update chain and reanalysis for each routine class.

**Independent Test**: Trace the three routine routes against the contract.

- [x] T005 [US2] Verify specification, plan, and task flow-back command order and final reanalysis in `workflows/speckit-flow-analyze-remediate/workflow.yml`

## Phase 5: User Story 3 - Stop for Consequential Decisions (P3)

**Goal**: Verify consequential and invalid outcomes stop without remediation.

**Independent Test**: Trace each stop route and follow the manual controller instructions.

- [x] T006 [US3] Verify constitutional, authority-or-scope, blocked, and invalid stops in `workflows/speckit-flow-analyze-remediate/workflow.yml`
- [x] T007 [US3] Document the manual analysis/remediation controller in `workflows/README.md`

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T008 Run convergence across `specs/005-analyze-remediate/`, `workflows/speckit-flow-analyze-remediate/workflow.yml`, `workflows/README.md`, and `tests/test_bundle_lifecycle.py`
- [x] T009 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before the user stories. T004 follows T003. Complete all three stories before T008 and T009. The routine and consequential routes may be inspected independently after T002.

## Implementation Strategy

Keep the reviewed YAML unless a concrete mismatch is found. Verify safe native routing, document the manual controller, and leave live finding classification and remediation acceptance to the operator.
