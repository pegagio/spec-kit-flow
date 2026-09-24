# Tasks: Start Eligible Feature

**Input**: Design documents in `specs/001-start-eligible-feature/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [workflow contract](contracts/start-feature.md)

**Tests**: Validate the existing source contract and disposable consumer behavior; no new test framework is required.

## Phase 1: Setup

Confirm the reviewed workflow and bundle coordinates before judging behavior.

- [x] T001 Record current workflow ID/version, bundle pins, CLI version, and source digest in `specs/001-start-eligible-feature/validation.md`

## Phase 2: Foundation

Establish the artifact gate before any source correction.

- [x] T002 Run cross-artifact analysis of `specs/001-start-eligible-feature/spec.md`, `specs/001-start-eligible-feature/plan.md`, and `specs/001-start-eligible-feature/tasks.md`, then reconcile any material inconsistency

## Phase 3: User Story 1 - Start an Eligible Feature (P1)

**Goal**: Verify the approval-gated route from candidate to brief.

**Independent Test**: Inspect the workflow route and run the disposable consumer lifecycle; distinguish native dispatch from live-agent validation.

- [x] T003 [US1] Verify candidate assessment, exact patch approval, approved command order, and final human choice against `workflows/speckit-flow-start-feature/workflow.yml`; correct a concrete mismatch only if found
- [x] T004 [US1] Add and run a no-op deferred start-feature route in the disposable consumer lifecycle check at `tests/test_bundle_lifecycle.py`, then record its observed result and limits in `specs/001-start-eligible-feature/validation.md`

## Phase 4: User Story 2 - Stop When Starting Is Unsafe (P2)

**Goal**: Verify that ambiguous, blocked, deferred, and invalid routes do not authorize an unapproved patch.

**Independent Test**: Trace every non-approval route in the workflow source and confirm the manual fallback remains usable.

- [x] T005 [US2] Verify non-approval and invalid-decision routes against `workflows/speckit-flow-start-feature/workflow.yml`; correct a concrete mismatch only if found
- [x] T006 [US2] Review the manual-prompt path in `workflows/README.md` and record any validation limit in `specs/001-start-eligible-feature/validation.md`

## Phase 5: Polish and Validation

Reconcile the implementation and feature artifacts before human review.

- [x] T007 Run convergence against `specs/001-start-eligible-feature/spec.md`, `specs/001-start-eligible-feature/plan.md`, `specs/001-start-eligible-feature/tasks.md`, and `workflows/speckit-flow-start-feature/workflow.yml`; record unresolved gaps in `specs/001-start-eligible-feature/validation.md`
- [x] T008 Run `git diff --check` and verify no personal name or local username appears in `specs/001-start-eligible-feature/` or changed project source

## Dependencies and Execution Order

T001 precedes T002. Complete T002 before T003 or T005. T004 follows T003; T006 follows T005. Complete both user stories before T007 and T008. Tasks on the same workflow source file are sequential.

## Implementation Strategy

Validate the approved route first, then the stop routes. Change the reviewed YAML only for a demonstrated contract gap. Keep live-agent acceptance as an explicit operator review separate from the no-op lifecycle check.
