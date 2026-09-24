# Tasks: Clarify Specification

**Input**: Design artifacts in `specs/002-clarify-specification/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [workflow contract](contracts/clarification.md)

**Tests**: Validate source routing and one disposable no-op route; live-agent answer quality remains a separate review.

## Phase 1: Setup

Capture the reviewed source and test coordinates.

- [x] T001 Record workflow ID/version, bundle version, CLI version, and source digest in `specs/002-clarify-specification/validation.md`

## Phase 2: Foundation

Check artifact consistency before implementation.

- [x] T002 Analyze `specs/002-clarify-specification/spec.md`, `specs/002-clarify-specification/plan.md`, and `specs/002-clarify-specification/tasks.md`, then reconcile any material finding

## Phase 3: User Story 1 - Resolve Ambiguity With the Operator (P1)

**Goal**: Confirm the workflow delegates one bounded interactive session and preserves its result for review.

**Independent Test**: Inspect the source command and run a disposable no-op clarification route without claiming live answer quality.

- [x] T003 [US1] Verify one `speckit.clarify` invocation and the five-question session-boundary wording in `workflows/speckit-flow-clarify/workflow.yml`
- [x] T004 [US1] Add a no-op `begin-planning` clarification route to `tests/test_bundle_lifecycle.py`, run the lifecycle suite, and record evidence limits in `specs/002-clarify-specification/validation.md`

## Phase 4: User Story 2 - Choose the Next Human-Directed State (P2)

**Goal**: Confirm explicit continuation, planning readiness, and deferral routes stop without automatic phase dispatch.

**Independent Test**: Trace every gate branch and follow the documented manual path.

- [x] T005 [US2] Verify all three gate choices and the invalid-decision stop against `workflows/speckit-flow-clarify/workflow.yml`
- [x] T006 [US2] Document the manual clarification sequence in `workflows/README.md` and record its validation boundary in `specs/002-clarify-specification/validation.md`

## Phase 5: Polish and Validation

Close remaining implementation gaps and check the changed scope.

- [x] T007 Run convergence across `specs/002-clarify-specification/`, `workflows/speckit-flow-clarify/workflow.yml`, `workflows/README.md`, and `tests/test_bundle_lifecycle.py`
- [x] T008 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before T003 or T005. T004 follows T003; T006 follows T005. Complete both user stories before T007 and T008. The test and README changes are independent, but this queue processes them sequentially.

## Implementation Strategy

Validate the reviewed source first, then add one native route and manual instructions. Correct workflow YAML only for a demonstrated mismatch. Report live-agent validation as an acceptance limit, not as a test pass.
