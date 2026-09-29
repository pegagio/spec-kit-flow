# Tasks: Consumer Adoption of Merge-Bounded Flow-Back

**Input**: Design documents from `specs/012-consumer-adoption/`

**Prerequisites**: `plan.md`, `spec.md`, `research.md`, `data-model.md`, `contracts/adoption.md`, `quickstart.md`

**Tests**: Required by FR-011 and the plan. Structural and preservation tests are automated; semantic compatibility and agent behavior need operator-reviewed disposable-consumer scenarios.

**Organization**: Tasks are grouped by the three user stories in `spec.md`.

## Phase 1: Setup

**Purpose**: The repository and existing Python test infrastructure are already initialized. No project setup or new dependency task is needed.

## Phase 2: Foundational

**Purpose**: The design adds no shared runtime component or schema that must block story implementation. Each story can proceed after its own tests and documents are ready.

## Phase 3: User Story 1 - Adopt the Model in a New Consumer (Priority: P1) 🎯 MVP

**Goal**: Let an operator inspect, decide on, and verify adoption in a new consumer without silently changing governance.

**Independent Test**: In a disposable initialized consumer with no conflicting governance, follow the runbook, inspect all proposed changes before acceptance, and verify the resulting active guidance and governance evidence or the unchanged declined state.

### Tests for User Story 1

- [X] T001 [P] [US1] Add document-contract tests for the runbook, proposal wording, and worksheet fields in `tests/test_consumer_adoption.py`, covering M1–M5, evidence in both guidance and governance, explicit decisions, and the four outcomes.

### Implementation for User Story 1

- [X] T002 [P] [US1] Write the operator procedure, copyable manual agent prompt, exact-patch review steps, decision handling, and evidence limits in `docs/consumer-adoption.md`.
- [X] T003 [P] [US1] Create the blank M1–M5 governance and active-guidance evidence matrix with `compatible`, `missing`, `conflicting`, or `uncertain` status, project-relative locator, semantic rationale, and guidance applicability; add proposal and decision fields, snapshot digests, outcomes, and provenance in `docs/templates/adoption-review.md`.
- [X] T004 [US1] Link the new-consumer adoption procedure after installation in `docs/installation.md` and expose it as a project entry point in `README.md`.

**Checkpoint**: A new consumer can follow a manual, reviewable adoption path and record a bounded result without installation claiming adoption.

## Phase 4: User Story 2 - Refresh Without Overwriting Governance (Priority: P2)

**Goal**: Reassess current consumer state after refresh while preserving project-owned rules, local edits, and evidence.

**Independent Test**: In disposable consumers with compatible, missing, conflicting, and locally edited governance, refresh and reassess; verify no project-owned changes occur without a decision and that outcome evidence reflects current state.

### Tests for User Story 2

- [X] T005 [P] [US2] Add disposable-consumer lifecycle tests in `tests/test_consumer_adoption_lifecycle.py` that hash consumer-owned guidance, constitution, review records, and unrelated files before and after bundle installation, refresh, and removal.
- [X] T006 [P] [US2] Define synthetic inputs and expected observable outcomes for compatible, conflicting, declined, deferred, partial, README-only, uncertain-authority, changed-baseline, and nonstandard-boundary cases in `tests/consumer-fixtures/adoption/scenarios.json`.

### Implementation for User Story 2

- [X] T007 [US2] Document refresh reassessment, exact conflict review, baseline recheck, partial and unresolved results, and preservation on removal in `docs/consumer-adoption.md`.
- [X] T008 [US2] Link refresh and removal instructions to reassessment and clarify that neither operation edits nor confirms adoption in `docs/installation.md`.
- [X] T009 [US2] Reconcile the existing disposable installation, refresh, and removal procedures in `specs/012-consumer-adoption/quickstart.md` with implemented commands, fixture coverage, and expected preservation observations.

**Checkpoint**: Refresh starts a new evidence-based review, and removal preserves consumer-owned guidance, governance, history, and adoption records.

## Phase 5: User Story 3 - Use the Model During Feature Work (Priority: P3)

**Goal**: Give agents active project guidance for merge-bounded artifact flow-back, history after integration, and operator-directed consistency checks.

**Independent Test**: In an adopted disposable consumer, review pre-merge change, post-integration change, and missing-check scenarios; verify guidance directs the right artifact treatment and recommendations without invoking workflows independently.

### Tests for User Story 3

- [X] T010 [P] [US3] Add guidance-contract tests in `tests/test_consumer_adoption_guidance.py` that check all five model rules, active-agent applicability instructions, operator-directed workflow recommendations, and the absence of automatic invocation instructions.

### Implementation for User Story 3

- [X] T011 [US3] Refine reusable README, active-agent, and constitution proposal sections to express M1–M5 and operator control in `docs/merge-bounded-flow-back.md`.
- [X] T012 [US3] Add pre-merge, post-integration, and missing-check agent scenarios to `specs/012-consumer-adoption/quickstart.md`, including a manual-path case.
- [X] T013 [US3] Run the manual and live-agent cases in a disposable consumer and record provenance, decisions, actual outcomes, deviations, and limitations in `specs/012-consumer-adoption/validation.md`.

**Checkpoint**: Active guidance is inspectable and directs the expected behavior while leaving workflow invocation with the operator.

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Complete bounded validation and record evidence without overstating semantic or adoption claims.

- [X] T014 Record source coordinates and digests, component identities and versions, tested CLI version, commands, outcomes, skips, and evidence limits for all disposable scenarios in `specs/012-consumer-adoption/validation.md`.
- [X] T015 Run the focused adoption document tests and relevant catalog lifecycle tests, then record exact results in `specs/012-consumer-adoption/validation.md`.
- [X] T016 Review implementation against FR-001–FR-012 and SC-001–SC-007 and record any unmet requirement or remaining operator decision in `specs/012-consumer-adoption/validation.md`.

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No initialization work is required for this repository.
- **Foundational (Phase 2)**: No shared runtime prerequisite is introduced; story work can begin after its own test-first task.
- **User Stories (Phases 3–5)**: Implement in priority order for incremental delivery. US2 and US3 can be developed independently after US1's shared runbook entry point exists, but this task plan sequences them for reviewability.
- **Polish (Phase 6)**: Depends on the desired stories and disposable-consumer scenarios being implemented.

### User Story Dependencies

- **User Story 1 (P1)**: Independent; establishes the new-consumer manual adoption route and MVP evidence worksheet.
- **User Story 2 (P2)**: Depends on the runbook entry point from US1; adds refresh, conflict, and removal lifecycle behavior.
- **User Story 3 (P3)**: Depends on US1's proposal and evidence model; adds operating guidance and live behavior observations.

### Within Each User Story

- Run the story's contract or scenario tests before completing its documentation behavior.
- Keep semantic compatibility judgments and constitutional amendments subject to the consumer operator's explicit decision.
- Record observed results separately from expected results; automated text checks do not establish semantic adoption or live-agent compliance.

### Parallel Opportunities

- T002 and T003 can proceed in parallel after T001 defines the expected document contract.
- T005 and T006 can proceed in parallel because they cover lifecycle preservation and outcome classification in separate files.
- T011 can proceed alongside T010 after the reusable guidance contract is agreed; T012 follows the quickstart additions from US2.
- US2 and US3 can proceed in parallel after US1's runbook and worksheet are reviewed, provided their shared quickstart and validation edits are coordinated.

## Parallel Example: User Story 1

```text
Task: T002 Write docs/consumer-adoption.md after T001 defines its document contract.
Task: T003 Create docs/templates/adoption-review.md after T001 defines its required fields.
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete the US1 document-contract tests.
2. Write and review the runbook and evidence worksheet.
3. Add the new-install entry point.
4. Validate a new disposable consumer for inspect-before-accept, confirmed evidence, and unchanged decline behavior.

### Incremental Delivery

1. Deliver US1 as the manual new-consumer adoption path.
2. Add US2 refresh, conflict, decline, deferral, partial-state, and removal coverage.
3. Add US3 active guidance and manual/live-agent behavior observations.
4. Complete provenance-bearing scenario validation and the requirements review.

## Operator Work and Notes

- The accepted plan selects the documentation-led route. During implementation, operators of each consumer still decide whether to accept constitutional amendments or resolve material conflicts after seeing exact patches.
- Semantic equivalence, applicable nested guidance, and live-agent adherence require evidence-based human review; tasks must report uncertainty instead of inventing a confirmed result.
- The implementation tasks must not invoke a later FlowKit workflow automatically. After task generation or consequential artifact changes, recommend the operator-invoked analysis/remediation workflow.
- `[P]` marks work in separate files with no unfinished-task dependency. `[US#]` labels map tasks to the specification's user stories.

## Phase 7: Convergence

Complete the remaining new-consumer and refresh adoption observations without treating installation preservation as adoption evidence.

- [X] T017 Exercise the documented new-consumer adoption path from missing model rules through exact proposal review, required operator decision, accepted edits, and final M1–M5 evidence; exercise post-refresh reassessment with locally changed compatible and conflicting governance while preserving local text and avoiding reuse of an old confirmed result. Record actual decisions, baseline/final hashes, outcomes, component and CLI provenance, and limitations in `specs/012-consumer-adoption/validation.md`, then update its requirement review per FR-011, SC-001, US1/AC1–AC2, US2/AC1–AC3, plan: Validation and Coverage, and T013–T016 (partial)

## Phase 8: Convergence

Complete the planned decision-safety observations that remain expected outcomes only in the validation record.

- [X] T018 Exercise the remaining quickstart adoption cases in disposable consumers: defer missing-rule additions and a conflict separately, accept only a subset of a proposal, inspect README-only evidence and uncertain nested-guidance applicability, and change a target baseline after proposal review before attempted application. Record observed outcomes, exact decisions (clearly labeling scripted test inputs), unchanged or authorized target hashes, provenance, and limitations in `specs/012-consumer-adoption/validation.md`; verify that stale patches are not applied and incomplete or uncertain evidence never produces confirmed adoption. Reconcile the requirement review and remaining-case inventory per plan: Validation and Coverage, `quickstart.md`: Run the Adoption Cases, T013–T014, and FR-003–FR-005/FR-008 (partial)
