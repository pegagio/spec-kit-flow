# Tasks: FlowKit Workflow Improvements

**Input**: [Specification](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md), [contracts](contracts/), and [quickstart](quickstart.md) for Feature 014.

**Organization**: Tasks are grouped by the seven P1 user stories. Tests are included because FR-017 and FR-024 require branch, gate, loop, manual-path, and disposable-consumer validation. Paths are relative to the repository root. No task authorizes a later FlowKit workflow invocation, a roadmap patch, or a constitutional amendment by itself.

## Contents

Follow the phases in dependency order, then use the dependency and parallel-work sections to coordinate independent changes.

- [Phase 1: Setup](#phase-1-setup)
- [Phase 2: Foundational](#phase-2-foundational)
- [Phase 3: User Story 1](#phase-3-user-story-1--review-every-workflow-end-to-end-p1--mvp)
- [Phase 4: User Story 2](#phase-4-user-story-2--reliable-roadmap-linkage-p1)
- [Phase 5: User Story 3](#phase-5-user-story-3--clarification-and-planning-readiness-p1)
- [Phase 6: User Story 4](#phase-6-user-story-4--generate-and-assess-tasks-p1)
- [Phase 7: User Story 5](#phase-7-user-story-5--converge-through-bounded-remediation-p1)
- [Phase 8: User Story 6](#phase-8-user-story-6--close-out-with-evidence-and-debrief-continuation-p1)
- [Phase 9: User Story 7](#phase-9-user-story-7--usable-agents-for-delegated-steps-p1)
- [Phase 10: Polish and Cross-Cutting Validation](#phase-10-polish-and-cross-cutting-validation)
- [Dependencies and Execution Order](#dependencies-and-execution-order)
- [Parallel Execution Examples](#parallel-execution-examples)
- [Implementation Strategy](#implementation-strategy)

## Phase 1: Setup

**Purpose**: Establish the reviewed roadmap scope and record already approved authority before changing workflow, controller, or agent source.

- [X] T001 Present the exact F014 all-eight-workflow and repository-local-agent scope patch for operator decision, apply it to `.specify/memory/roadmap.md` only if approved, and record the approved, unresolved, or rejected result in `specs/014-flowkit-workflow-improvements/validation/authority-decisions.md`.
- [X] T002 Record approved Constitution 6.0.0 and the F014 Clarify and Close Out clarification decisions in `specs/014-flowkit-workflow-improvements/validation/authority-decisions.md`; verify the current `AGENTS.md` boundary matches them and preserve verified Feature 007/008 history.
- [X] T003 Record the selected Specify CLI version, Git source coordinates, and current component IDs, versions, and digests in `specs/014-flowkit-workflow-improvements/validation/source-baseline.json`, and complete the eight-workflow step, branch, gate, continuation, terminal, resumption, and agent baseline in `specs/014-flowkit-workflow-improvements/workflow-review-inventory.md` before selecting source changes; do not modify checked-in release metadata.

**Checkpoint**: The constitutional and feature-specific authority decisions are recorded; the expanded roadmap scope has an explicit approved or rejected decision. An unresolved or rejected roadmap amendment leaves expanded source work blocked without a fallback design.

## Phase 2: Foundational

**Purpose**: Implement shared loop, evidence, recovery, and validation mechanisms used by the stories. This phase depends on the Phase 1 decisions for any conflicting behavior.

- [X] T004 Add failing controller tests for pre-loop `complete`/`needs-human`/`blocked` routing without a corrective pass, nested `do-while` preflight, unique IDs across loop bodies, one complete supported condition expression, positive `max_iterations`, fresh reassessment, post-loop main-task gate routing, and all-branch named-agent validation in `tests/test_controller.py`.
- [X] T005 Add failing controller tests for the outcome envelope in `tests/test_controller.py`: `state` is exactly `complete`, `continue`, `needs-human`, or `blocked`; `reason_code` is stable; evidence paths are existing project-relative files with observed SHA-256 digests; remaining and resolved IDs do not contradict; `continue` names an in-body next step; completion has no unresolved in-scope work.
- [X] T006 Add failing recovery tests for ordered `(loop_id, iteration)` pass records, distinct repeated step IDs, compact evidence, interruption, and changed-installation safe stops in `tests/test_controller.py`.
- [X] T007 Implement pre-loop assessment and `complete`/`needs-human`/`blocked` routing, built-in Specify `do-while` graph validation, condition evaluation, finite cap handling, nested branch traversal, and all-branch assignment preflight in `controllers/flow-kit/scripts/python/controller.py` without adding a new workflow step type.
- [X] T008 Implement validated assessment-envelope parsing, evidence digest checking, per-workflow progress comparison from the initial and refreshed assessments, and `complete`/`continue`/`needs-human`/`blocked` routing in `controllers/flow-kit/scripts/python/controller.py`; a digest-only change or successful command must not prove progress or completion.
- [X] T009 Implement append-only loop-pass evidence and safe resume/stop state under `.specify/flow-controllers/runs/` in `controllers/flow-kit/scripts/python/recovery.py`, retaining relative paths and excluding raw child transcripts and absolute host paths.
- [X] T010 Update `controllers/flow-kit/controller-protocol.md` to specify initial assessment, the new child per delegated step per pass, same-child relay for that step's questions, main-task consequential gates, progress/cap stops, installation-change handling, and no nested or later FlowKit invocation; increment the changed controller package version and verify pinned CLI compatibility in `controllers/flow-kit/manifest.yml`.
- [X] T011 Create an automated graph and branch-inventory checker in `tools/validate_workflows.py` that reads all eight `workflows/speckit-flow-*/workflow.yml` files and reports initial assessment, success, continuation, human-decision, bounded-stop, and assignment edges without asking the operator to classify routine outcomes.
- [X] T012 Add fixture coverage for clean-before-loop, post-pass gate, supported and rejected loop, outcome, and manual-fallback graph shapes in `tests/consumer-fixtures/controller-workflow.yml` and `tests/test_controller.py`.

**Checkpoint**: The existing controller suite passes, invalid graph/evidence cases stop before work, and repeated-pass recovery is distinct and portable. No workflow package relies on prompt-only loop instructions.

## Phase 3: User Story 1 — Review Every Workflow End to End (P1) 🎯 MVP

**Goal**: Give all eight workflows a machine-checked branch-and-gate inventory and make the common Analyze and Implement return paths reach a defined conclusion or bounded stop.

**Independent Test**: Run the inventory checker against all eight definitions and focused Analyze/Implement fixtures for clean, remediable, blocked, consequential, no-progress, and cap-exhausted paths. Verify that no branch launches a later FlowKit workflow.

### Tests

- [X] T013 [P] [US1] Add Analyze/Implement continuation, artifact-order, fresh-evidence, no-progress, cap, and exact-gate cases to `tests/test_workflow_paths.py`.
- [X] T014 [P] [US1] Add all-eight branch inventory assertions and unexplained-terminal detection to `tests/test_workflow_graph.py`.

### Implementation

- [X] T015 [US1] Compare the machine-checked graph projection with the pre-change eight-workflow inventory in `specs/014-flowkit-workflow-improvements/workflow-review-inventory.md`, resolve unexplained branches, and select only the supported US1 source changes.
- [X] T016 [US1] Replace routine operator classification and one-pass fall-through with initial assessment and evidence-based bounded reassessment in `workflows/speckit-flow-analyze-remediate/workflow.yml`, preserving affected spec→plan→tasks order and consequential gates; increment its workflow version.
- [X] T017 [P] [US1] Complete Implement's in-scope return-to-analysis/specification/plan/tasks paths through initial assessment, dependent reconciliation, analysis, and eligible work or a specific stop in `workflows/speckit-flow-implement/workflow.yml`; keep Converge separately invoked and increment its workflow version.

**Checkpoint**: Analyze and Implement complete their own routine corrective paths, and every workflow has a checkable inventory. This increment does not claim that the other six packages have been updated yet.

## Phase 4: User Story 2 — Reliable Roadmap Linkage (P1)

**Goal**: Start Feature reaches a brief tied to the unique selected roadmap entry or stops with specific missing, stale, or conflicting linkage evidence.

**Independent Test**: Use disposable fixtures with unique, missing, stale, and conflicting `Spec dir` mappings; assert exact patch approval precedes any roadmap edit and the brief resolves the selected specification.

### Tests

- [X] T018 [P] [US2] Add unique/missing/stale/conflicting roadmap-linkage and unapproved-patch cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T019 [US2] Add initial and post-specification linkage assessment, exact roadmap patch gate, approved repair, and refreshed brief routing to `workflows/speckit-flow-start-feature/workflow.yml`; never infer a link from feature number alone and increment its workflow version.
- [X] T020 [US2] Add Start Feature's manual-prompt fallback and changed-linkage fixture assertions to `tests/test_workflow_graph.py`.

**Checkpoint**: The brief uniquely matches the selected spec after any approved repair, or Start Feature stops with recoverable evidence.

## Phase 5: User Story 3 — Clarification and Planning Readiness (P1)

**Goal**: Clarify reassesses significant ambiguity across bounded sessions; separately invoked Plan starts when prerequisites are met without a routine readiness gate.

**Independent Test**: Exercise clean, five-question-limit-with-remaining-ambiguity, no-progress, missing-prerequisite, and material-product-question fixtures. Assert that each substantive answer stays with the operator and Plan is never launched by Clarify.

### Tests

- [X] T021 [P] [US3] Add repeated Clarify-session, five-question-per-session, operator-answer, no-progress, and cap cases to `tests/test_workflow_paths.py`.
- [X] T022 [P] [US3] Add Plan ready, missing-prerequisite, and material-product-ambiguity routing cases to `tests/test_workflow_graph.py`.

### Implementation

- [X] T023 [US3] Add initial and post-session residual-ambiguity assessment and the approved bounded same-invocation Clarify policy to `workflows/speckit-flow-clarify/workflow.yml`, retaining main-task substantive questions and no automatic Plan launch; increment its workflow version.
- [X] T024 [P] [US3] Replace Plan's unconditional readiness gate with initial evidence-based prerequisite routing and safe in-scope re-entry in `workflows/speckit-flow-plan/workflow.yml`; stop for material product decisions and increment its workflow version.

**Checkpoint**: Clarify and Plan each reach their own evidenced conclusion or bounded stop without a redundant routine confirmation.

## Phase 6: User Story 4 — Generate and Assess Tasks (P1)

**Goal**: Tasks generates from reviewed design, checks coverage, and concludes without routine pre- or post-generation operator confirmation.

**Independent Test**: Run complete-design, material-design-gap, incomplete-task-coverage, and corrected-coverage fixtures; assert no implementation or Analyze phase begins.

### Tests

- [X] T025 [P] [US4] Add generation, coverage, in-scope correction, material-gap, and no-extra-gate cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T026 [US4] Replace Tasks' routine pre/post confirmation with initial current-artifact prerequisite and coverage assessment, bounded in-scope correction, and specific stop routes in `workflows/speckit-flow-tasks/workflow.yml`; increment its workflow version.
- [X] T027 [US4] Assert Tasks' manual path and separate Analyze invocation boundary in `tests/test_workflow_graph.py`.

**Checkpoint**: Complete coverage yields Tasks success; a material design gap stops with evidence.

## Phase 7: User Story 5 — Converge Through Bounded Remediation (P1)

**Goal**: Under approved Constitution 6.0.0, Converge reconciles affected artifacts, analyzes changed tasks, implements eligible fixes, and reassesses until clean or a bounded stop.

**Independent Test**: Exercise clean, task-only gap, higher-level behavior gap, blocked prerequisite, consequential decision, repeated gap, no progress, and cap exhaustion. Assert changed tasks are analyzed before implementation and Close Out is never launched.

### Tests

- [X] T028 [P] [US5] Add Converge artifact-order, analyzed-before-implement, refreshed-reassessment, repeated-gap, no-progress, cap, and gate cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T029 [US5] Replace Converge's routine classification gate and single-pass stop with initial clean routing and the approved bounded remediation loop in `workflows/speckit-flow-converge/workflow.yml`; preserve selected feature/task scope, stop reasons, and separate Close Out authority, and increment its workflow version.
- [X] T030 [US5] Assert Converge's manual route and no nested FlowKit workflow invocation in `tests/test_workflow_graph.py`.

**Checkpoint**: Clean evidence ends Converge; remediable evidence is reassessed after ordered correction; unsafe evidence stops with preserved work.

## Phase 8: User Story 6 — Close Out with Evidence and Debrief Continuation (P1)

**Goal**: Close Out recognizes clear completion evidence, repeats routine debrief correction safely, and keeps exact roadmap verification, Git, and acceptance gates.

**Independent Test**: Exercise already-Complete, clear Draft-to-Complete, ambiguous authority, correctable debrief, repeated finding, and rejected exact-patch fixtures. Assert no roadmap edit before exact approval.

### Tests

- [X] T031 [P] [US6] Add Close Out status, debrief-loop, ambiguous-authority, exact-patch rejection, no-progress, and cap cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T032 [US6] Implement the approved evidence-backed in-place Draft-to-Complete route, initial and refreshed debrief assessment, bounded correction loop, and exact-roadmap-patch gate in `workflows/speckit-flow-closeout/workflow.yml`; retain separate Git integration and acceptance authority and increment its workflow version.
- [X] T033 [US6] Assert Close Out's manual path and all terminal routes in `tests/test_workflow_graph.py`.

**Checkpoint**: A clear feature reaches a supported exact patch proposal or approved verification; routine findings are reassessed and unresolved decisions stop.

## Phase 9: User Story 7 — Usable Agents for Delegated Steps (P1)

**Goal**: Every delegated step has a justified exact native name, and this repository has usable configurations for all names retained by the review.

**Independent Test**: Check every branch and loop body, parse every referenced native TOML file, exercise exact-name preflight, and distinguish machine-observed live selection from structural or no-op dispatch evidence.

### Tests

- [ ] T034 [P] [US7] Add exact-agent, missing/malformed/unavailable-name, no-fallback, and main-task gate/switch cases to `tests/test_agent_configs.py`.
- [ ] T035 [P] [US7] Add bundle install/refresh/remove preservation assertions for consumer-owned `.codex/agents/` files to `tests/test_bundle_lifecycle.py`.

### Implementation

- [ ] T036 [US7] Record responsibility and rationale for every delegated step and any proposed fifth name in `specs/014-flowkit-workflow-improvements/agent-assignment-inventory.md`; obtain explicit review before a new name appears in source.
- [ ] T037 [P] [US7] Add usable Architect instructions with native `name`, `description`, and `developer_instructions` in `.codex/agents/architect.toml`, preserving task scope and main-task gates.
- [ ] T038 [P] [US7] Add usable Builder instructions with native `name`, `description`, and `developer_instructions` in `.codex/agents/builder.toml`, preserving task scope and main-task gates.
- [ ] T039 [P] [US7] Replace the temporary launch probe with ordinary Coder responsibilities and native fields in `.codex/agents/coder.toml`, without adding workflow or approval authority.
- [ ] T040 [P] [US7] Add usable Verifier instructions with native `name`, `description`, and `developer_instructions` in `.codex/agents/verifier.toml`, preserving independent assessment and main-task gates.
- [ ] T041 [US7] Apply the approved assignment inventory to delegated nodes in `workflows/speckit-flow-start-feature/workflow.yml`, `workflows/speckit-flow-clarify/workflow.yml`, `workflows/speckit-flow-plan/workflow.yml`, `workflows/speckit-flow-tasks/workflow.yml`, `workflows/speckit-flow-analyze-remediate/workflow.yml`, `workflows/speckit-flow-implement/workflow.yml`, `workflows/speckit-flow-converge/workflow.yml`, and `workflows/speckit-flow-closeout/workflow.yml`, retaining one exact name per child and no assignment on gates, switches, or loop containers.
- [ ] T042 [US7] Extend `tools/validate_workflows.py` to report exact native selection evidence when the Codex client exposes it, otherwise mark live behavior unverified without requiring manual operator verification.

**Checkpoint**: All eight graphs preflight every named branch; this checkout has usable files for each selected name; bundle lifecycle leaves other consumers' agent files alone.

## Phase 10: Polish and Cross-Cutting Validation

**Purpose**: Complete automated end-to-end evidence and documentation without treating a local success as release or acceptance.

- [ ] T043 Increment the source bundle version and align all eight changed workflow version pins with their source definitions in `bundles/spec-kit-flow/bundle.yml` before development-snapshot composition; do not update checked-in release catalog assets.
- [ ] T044 [P] Add scripted initialized-temporary-consumer snapshot install/refresh/remove and preservation assertions, with component IDs, versions, digests, CLI version, source coordinates, results, and explicit limits in `tests/test_snapshot_validation.py`.
- [ ] T045 [P] Update workflow behavior, manual fallback, loop bounds, and agent expectations in `workflows/README.md` and `docs/installation.md` without claiming release or automatic consumer-agent installation.
- [ ] T046 Run the automated scenarios in `specs/014-flowkit-workflow-improvements/quickstart.md` and write their machine-generated branch coverage, observed stops, skipped paths, component provenance, and limitations to `specs/014-flowkit-workflow-improvements/validation/report.json`.
- [ ] T047 Prepare at most two optional final Codex desktop checks—one visible continuation and one named-agent/gate presentation—with exact actions and expected results in `specs/014-flowkit-workflow-improvements/validation/desktop-checks.md`; record any operator observations separately from automated results.
- [ ] T048 Reconcile accepted implementation discoveries across `specs/014-flowkit-workflow-improvements/spec.md`, `specs/014-flowkit-workflow-improvements/plan.md`, and `specs/014-flowkit-workflow-improvements/tasks.md`, then run relevant tests and `git diff --check` before presenting the changed source and residual limits for review.

**Checkpoint**: Automated evidence and documentation cover the delivered source; optional desktop observations are separate. Release, roadmap verification, Git integration, and feature acceptance retain their own explicit decisions.

## Dependencies and Execution Order

### Phase dependencies

1. Phase 1 records the roadmap and prospective authority decisions. Source behavior that conflicts with those decisions cannot proceed while they are unresolved.
2. Phase 2 provides the shared controller, recovery, and graph-checking contract. All seven story phases depend on its completion.
3. Phase 1 records the cross-workflow inventory before source changes. US1 compares it with the machine-checked graph and provides a first implementation increment. US2–US7 can then proceed in separate workflow files, with shared test-file edits coordinated sequentially.
4. Phase 10 follows the delivered story phases. T043 aligns the source bundle pins before snapshot composition. T046 depends on T043–T045; T047 follows the automated report; T048 follows all accepted changes.

### Story completion order

| Story | Depends on | Independently testable result |
|---|---|---|
| US1 | Foundation and pre-change inventory | Checked eight-workflow inventory and Analyze/Implement loops validated with deterministic named-agent fixtures. |
| US2 | Foundation | Start Feature uniquely linked or specifically stopped. |
| US3 | Foundation and approved Clarify policy | Clarify and Plan each reach an evidenced conclusion. |
| US4 | Foundation | Tasks generation and coverage assessment conclude without routine gates. |
| US5 | Foundation and approved Converge authority | Converge reaches clean or a bounded stop after ordered remediation. |
| US6 | Foundation and approved Close Out authority | Completion/debrief reaches an exact proposal or bounded stop. |
| US7 | Foundation and initial inventory | Every delegated branch has a usable exact name in this checkout. |

Shared files `tests/test_workflow_paths.py`, `tests/test_workflow_graph.py`, and `tools/validate_workflows.py` are edited sequentially by the listed tasks; `[P]` marks only work in disjoint files at the point where it is listed. Workflow YAML files and separate native TOML files can be worked on in parallel after their prerequisites. US1–US6 direct-controller path tests use deterministic named-agent fixtures; full native Codex selection evidence and final disposable-consumer validation wait for US7's files and assignment review. A structural or no-op check is not reported as live-agent validation.

## Parallel Execution Examples

- **US1**: T013 in `tests/test_workflow_paths.py` and T014 in `tests/test_workflow_graph.py` can be written together; after T015 records the baseline inventory, T016 and T017 affect different workflow packages.
- **US2**: T018 can be drafted while an independent worker examines the Start Feature YAML for T019; apply source changes after the test cases and approval gates are settled.
- **US3**: T021 and T022 cover different test files; T023 and T024 change separate Clarify and Plan packages after their respective prerequisites.
- **US4**: T025's test fixtures can be prepared alongside a read-only Tasks graph review; T026 and T027 then run in order.
- **US5**: T028 can be prepared while the approved Converge authority is documented; T029 follows the approval and test case definition.
- **US6**: T031 can be prepared while the approved Close Out rule is documented; T032 follows the approval and test case definition.
- **US7**: T034 and T035 affect separate test files; T037–T040 create or edit distinct native agent files after T036's assignment review.

## Implementation Strategy

Start with Phase 1 decisions, source provenance, and the complete eight-workflow inventory before source changes, then build the Phase 2 shared contract. Deliver US1 as the first fixture-tested increment: its checked branch inventory and Analyze/Implement continuation demonstrate that the loop, evidence, and recovery machinery works. Complete the remaining story phases against their own deterministic fixture sets, complete US7's native agent configuration and assignment review, then run the full direct-Codex and disposable-consumer checks. Automated results carry routine verification; at most two final operator checks may confirm the visible Codex desktop experience. Do not treat those observations as approval of a roadmap patch, release, Git integration, or feature acceptance.
