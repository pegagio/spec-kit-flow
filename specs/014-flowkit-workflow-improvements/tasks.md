# Tasks: FlowKit Workflow Improvements

**Input**: [Specification](spec.md), [plan](plan.md), [research](research.md), [data model](data-model.md), [contracts](contracts/), and [quickstart](quickstart.md) for Feature 014.

**Organization**: Tasks retain the original seven P1 story phases and add the approved wiki maintenance and rendering work under cross-cutting delivery. Completed superseded tasks are historical work records, not requests to restore removed behavior. Tests are included because FR-017 and FR-024 require branch, gate, loop, manual-path, and disposable-consumer validation. Paths are relative to the repository root. No task authorizes a later FlowKit workflow invocation, a roadmap patch, or a constitutional amendment by itself.

## Current delivery status

T001–T079 are delivered within their recorded validation limits. T080–T089 are delivered: all 23 defined live scenarios passed independent audits against current workflow source and controller 0.5.2. Separately invoked Analyze, Implement and Converge prerequisites also passed. The available 127-test suite, eleven-workflow validator and checksum-pinned snapshot lifecycle passed; one optional external-working-tree lifecycle suite was skipped. [The final live audit](validation/live-workflows/completion-audit.json) records exact source continuity, retained failed attempts and coverage limits. Static checks alone did not satisfy the live tasks. Feature status remains Draft and roadmap status remains in-progress.

T049–T060 supersede the earlier wrapper designs and add the approved replacements and wiki workflow. Ten active workflows and one deprecated source are delivered. T034–T048 and T061–T064 are complete, including the reviewed agent assignments, snapshot lifecycle evidence, static report, and optional desktop-check instructions. T044 uses checksum-pinned roadmap and wiki release artifacts, so independent working-tree checkouts are not required. The recorded `validation/report.json` reports 116 tests with zero failures/errors and successful pinned snapshot install/refresh/remove. The distinct external-working-tree lifecycle suite remains skipped because its source settings were unset; all eight roles passed exact-name readiness probes; native identity introspection remains unverified; optional desktop checks are prepared and not run. These limits do not reopen completed T044/T046. The shared T065/T071/T073/T075/T076/T077 evidence reconciliation is delivered once after separately invoked Analyze and Remediate and Converge follow-up; independent Converge run `0a87d86f-bb0a-4189-b692-b0367e434624` confirmed the correction with no remaining findings; T066–T069 are complete for deterministic semantic-review handoff, routing, and source-contract validation; that deterministic milestone did not verify live reasoning. Later live execution has separate evidence. Feature status remains Draft and roadmap status remains in-progress.

## Contents

Follow the phases in dependency order, then use the dependency and parallel-work sections to coordinate independent changes.

- [Current delivery status](#current-delivery-status)
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
- [Shared evidence reconciliation](#shared-evidence-reconciliation)
- [Phase 11: Convergence](#phase-11-convergence)
- [Phase 12: Convergence](#phase-12-convergence)
- [Phase 13: Convergence](#phase-13-convergence)
- [Phase 14: Convergence](#phase-14-convergence)
- [Phase 15: Convergence](#phase-15-convergence)
- [Phase 16: Convergence](#phase-16-convergence)
- [Phase 17: Live Workflow Verification](#phase-17-live-workflow-verification)

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

**Goal**: Give all active workflows and the deprecated source a machine-checked branch-and-gate inventory. Analyze completes its corrective routes; Implement repeats the core skill while eligible task progress is verified.

**Independent Test**: Run the inventory checker against all eleven source definitions, Analyze's corrective fixtures, and Implement's core-skill continuation contract. Verify that no branch launches a later FlowKit workflow.

### Tests

- [X] T013 [P] [US1] Add Analyze/Implement continuation, artifact-order, fresh-evidence, no-progress, cap, and exact-gate cases to `tests/test_workflow_paths.py`.
- [X] T014 [P] [US1] Add all-eight branch inventory assertions and unexplained-terminal detection to `tests/test_workflow_graph.py`.

### Implementation

- [X] T015 [US1] Compare the machine-checked graph projection with the pre-change eight-workflow inventory in `specs/014-flowkit-workflow-improvements/workflow-review-inventory.md`, resolve unexplained branches, and select only the supported US1 source changes.
- [X] T016 [US1] Replace routine operator classification and one-pass fall-through with initial assessment and evidence-based bounded reassessment in `workflows/speckit-flow-analyze-remediate/workflow.yml`, preserving affected spec→plan→tasks order and consequential gates; increment its workflow version.
- [X] T017 [P] [US1] Complete Implement's in-scope return-to-analysis/specification/plan/tasks paths through initial assessment, dependent reconciliation, analysis, and eligible work or a specific stop in `workflows/speckit-flow-implement/workflow.yml`; keep Converge separately invoked and increment its workflow version.

**Checkpoint**: Analyze completes its corrective paths, Implement delegates each eligible-work session to the core skill and reassesses progress, and every workflow has a checkable inventory. This increment does not claim that the other six packages have been updated yet.

## Phase 4: User Story 2 — Reliable Roadmap Linkage (P1)

**Goal**: Select Feature presents candidates and dependencies and activates the exactly approved unique target without specification writes; separately invoked Specify authors that same target and reaches a uniquely linked brief. T056 supersedes the combined Start Feature implementation below.

**Independent Test**: Use disposable fixtures with unique, missing, stale, and conflicting `Spec dir` mappings; assert exact patch approval precedes any roadmap edit and the brief resolves the selected specification.

### Tests

- [X] T018 [P] [US2] Add unique/missing/stale/conflicting roadmap-linkage and unapproved-patch cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T019 [US2] Add initial and post-specification linkage assessment, exact roadmap patch gate, approved repair, and refreshed brief routing to `workflows/speckit-flow-start-feature/workflow.yml`; never infer a link from feature number alone and increment its workflow version.
- [X] T020 [US2] Add Start Feature's manual-prompt fallback and changed-linkage fixture assertions to `tests/test_workflow_graph.py`.

**Checkpoint**: Selection preserves existing spec bytes and authoring preserves active target identity; linkage is verified before the shared brief. Deprecated Start Feature stops without work.

## Phase 5: User Story 3 — Clarification and Planning Readiness (P1)

**Goal**: Clarify reassesses significant ambiguity across bounded sessions; separately invoked Plan delegates to the existing core skill and presents its artifacts or blocker.

**Independent Test**: Exercise clean, five-question-limit-with-remaining-ambiguity, no-progress, missing-prerequisite, and material-product-question fixtures. Assert that each substantive answer stays with the operator and Plan is never launched by Clarify.

### Tests

- [X] T021 [P] [US3] Add repeated Clarify-session, five-question-per-session, operator-answer, no-progress, and cap cases to `tests/test_workflow_paths.py`.
- [X] T022 [P] [US3] Add Plan ready, missing-prerequisite, and material-product-ambiguity routing cases to `tests/test_workflow_graph.py`.

### Implementation

- [X] T023 [US3] Add post-session residual-ambiguity assessment without a redundant initial wrapper assessment and the approved bounded same-invocation Clarify policy to `workflows/speckit-flow-clarify/workflow.yml`, retaining main-task substantive questions and no automatic Plan launch; increment its workflow version.
- [X] T024 [P] [US3] Replace Plan's unconditional readiness gate with the core-skill output-verification loop and exact-gap feedback in `workflows/speckit-flow-plan/workflow.yml`; stop for material product decisions and increment its workflow version.

**Checkpoint**: Clarify and Plan each reach their own evidenced conclusion or bounded stop without a redundant routine confirmation.

## Phase 6: User Story 4 — Generate and Assess Tasks (P1)

**Goal**: Tasks generates from reviewed design, checks coverage, and concludes without routine pre- or post-generation operator confirmation.

**Independent Test**: Run complete-design, material-design-gap, incomplete-task-coverage, and corrected-coverage fixtures; assert no implementation or Analyze phase begins.

### Tests

- [X] T025 [P] [US4] Add generation, coverage, in-scope correction, material-gap, and no-extra-gate cases to `tests/test_workflow_paths.py`.

### Implementation

- [X] T026 [US4] Replace Tasks' routine pre/post confirmation with a core-skill output-verification loop, preserved task history, exact-gap retries, and specific blocked reports in `workflows/speckit-flow-tasks/workflow.yml`; increment its workflow version.
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

- [X] T034 [P] [US7] Add exact-agent, missing/malformed/unavailable-name, no-fallback, and main-task gate/switch cases to `tests/test_agent_configs.py`.
- [X] T035 [P] [US7] Add bundle install/refresh/remove preservation assertions for consumer-owned `.codex/agents/` files to `tests/test_bundle_lifecycle.py`; snapshot lifecycle validation uses pinned component release artifacts when working-tree sources are unavailable.

### Implementation

- [X] T036 [US7] Record responsibility and rationale for every delegated step in `specs/014-flowkit-workflow-improvements/agent-assignment-inventory.md`; apply the operator-reviewed role set without adding workflow nodes.
- [X] T037 [P] [US7] Add usable Roadmap Agent and Specifier instructions with native `name`, `description`, and `developer_instructions` in their repository-local TOML files, preserving exact target scope and main-task approval gates.
- [X] T038 [P] [US7] Add usable Planner and Tasker instructions in their repository-local TOML files; preserve the reviewed specification and plan as upstream constraints and defer independent review to Reviewer.
- [X] T039 [P] [US7] Replace the temporary launch probe with ordinary Coder responsibilities and add the distinct Code Reviewer configuration; use the Code Reviewer only on existing assessment nodes, without adding workflow nodes or granting implementation authority.
- [X] T040 [P] [US7] Add usable Reviewer and Wiki Curator instructions in their repository-local TOML files, preserving author/reviewer separation, source citations, task scope, and main-task gates.
- [X] T041 [US7] Apply the reviewed assignment inventory and required assessment-prompt changes to delegated nodes in the ten active workflow definitions, retaining one exact name per child and no assignment on gates, switches, or loop containers; reuse existing assessment nodes for independent review and add no nodes.
- [X] T042 [US7] Extend `tools/validate_workflows.py` to report exact native selection evidence when the Codex client exposes it, otherwise mark live behavior unverified without requiring manual operator verification. This static validator records native selection as unverified because it does not launch Codex subagents.

**Checkpoint**: Completion requires all active graphs to preflight every named branch and this checkout to have usable files for each selected name; bundle lifecycle leaves other consumers' agent files alone.

## Phase 10: Polish and Cross-Cutting Validation

**Purpose**: Complete automated end-to-end evidence and documentation without treating a local success as release or acceptance.

- [X] T043 Increment the source bundle version and align all ten active workflow version pins with their source definitions in `bundles/spec-kit-flow/bundle.yml` before development-snapshot composition; do not update checked-in release catalog assets.
- [X] T044 [P] Add scripted initialized-temporary-consumer snapshot install/refresh/remove and preservation assertions, with component IDs, versions, digests, CLI version, source coordinates, results, and explicit limits in `tests/test_snapshot_validation.py`. The test uses checksum-pinned roadmap and wiki release packages and needs no external project checkout.
- [X] T045 [P] Update workflow behavior, manual fallback, loop bounds, and agent expectations in `workflows/README.md` and `docs/installation.md` without claiming release or automatic consumer-agent installation.
- [X] T046 Run the automated scenarios in `specs/014-flowkit-workflow-improvements/quickstart.md` and write their machine-generated branch coverage, observed stops, skipped paths, component provenance, and limitations to `specs/014-flowkit-workflow-improvements/validation/report.json`. Historical independent-source lifecycle validation was skipped. The current report records T044's checksum-pinned snapshot lifecycle as passed and the consolidated report as delivered; the separate external-working-tree lifecycle suite remains skipped, not an open T044 requirement.
- [X] T047 Prepare at most two optional final Codex desktop checks—one visible continuation and one named-agent/gate presentation—with exact actions and expected results in `specs/014-flowkit-workflow-improvements/validation/desktop-checks.md`; record any operator observations separately from automated results. The optional checks are prepared but not run.
- [X] T048 Reconcile accepted implementation discoveries across `specs/014-flowkit-workflow-improvements/spec.md`, `specs/014-flowkit-workflow-improvements/plan.md`, and `specs/014-flowkit-workflow-improvements/tasks.md`, then run relevant tests and `git diff --check` before presenting the changed source and residual limits for review. Historical repair is recorded by T062–T063. T044's snapshot consumer lifecycle and T046's consolidated report are delivered; the separate external-working-tree lifecycle suite remains skipped, native agent selection remains unverified, and optional desktop checks remain not run. No new completion marker follows from this reconciliation.
- [X] T049 [US1] Simplify `workflows/speckit-flow-implement/workflow.yml` to a bounded `speckit.implement` continuation loop with evidence-based task assessment and outcome report; align its diagram, manual path, versions, and focused tests. This supersedes T017's artifact flowback design for Implement without changing the separate Converge workflow.
- [X] T050 [US3] Simplify Plan to an Architect `speckit.plan` command with required-output verification and exact-gap retry feedback, followed by a main-task outcome report; update the diagram, manual path, feature requirements, version pins, and focused tests. This supersedes T022/T024's wrapper readiness routing and broad design reassessment. The Architect name and output-only review describe historical work; the accepted current role is Planner, and FR-005/FR-028 require independent structural plus semantic Reviewer assessment through the existing correction path. T066–T068 validate and reconcile that current contract without restoring old wrapper nodes.
- [X] T051 [US4] Simplify Tasks to the Plan-style core-skill output loop with exact-gap retry feedback and preserved task history; update source, diagram, manual path, requirements, versions, and focused tests. This supersedes T026's readiness routing and separate stop gates.
- [X] T052 [US1] Simplify Analyze and Remediate to one shared specification → plan → tasks waterfall, one analyzer, and one assessment; support an explicit first read-only baseline pass followed by at most five progress-checked corrections, and update diagram, controller, docs, versions, and focused tests.

- [X] T053 [US5] Simplify Converge to one shared task-recording and specification → plan → tasks waterfall, one task analyzer and eligibility check, one implementation command, and one convergence assessment; run speckit.converge on every pass with assessment before a guarded correction branch, allow five corrections plus final confirmation, preserve task history and stop propagation, and refresh diagram, manual path, versions, and focused tests.

- [X] T054 [US2] Simplify Start Feature with cited context before approval, explicit exact-patch and feature-context handoffs, one shared brief for verified linkage paths, and one final report; retain exact roadmap approval and post-repair verification, remove terminal choice gates, and refresh diagram, manual path, versions, and focused tests.

- [X] T055 [US2] Begin Start Feature with a read-only candidate and dependency inventory and an explicit human feature-selection gate; distinguish immediate unlocks from downstream dependents, support validated dynamic gate option lists, make the feature request optional, preserve exact selected identity through later handoffs, and update diagram, manual path, controller protocol/version, and tests.

- [X] T056 [US2] Split Start Feature into separately invoked Select Feature and Specify workflows; activate a uniquely mapped target through exact approval and pointer-only updates without spec writes, author that same target with context and brief, deprecate the combined source, and update launchers, package lifecycle, diagrams, contracts, and tests.
- [X] T057 Collapse ungated needs-human outcomes into blocked across Clarify, Plan, Tasks, Implement, Analyze and Remediate, and Converge; preserve questions, recovery actions, completion/continuation distinctions, Closeout gates, and legacy controller compatibility; refresh diagrams, version pins, documentation, and focused tests.
- [X] T058 [US6] Simplify Closeout to a shared bounded debrief/correction waterfall and one outcome report; remove stop-only gates, fix skipped-output and blocked-eligibility routing, verify exact approved roadmap patches, maintain wiki context for already-verified features, check lint before readiness review, and refresh diagram, docs, versions, and tests.
- [X] T059 [US6] Add bounded single-source wiki refresh, lint, and evidence-assessment continuation in Closeout; preserve source authority and conflicts, reject timestamp-only progress, stop on unsupported remediation or no progress, and refresh diagrams, tests, and documentation.
- [X] T060 Add independent Wiki Lint Update workflow, launcher, and chart; lint before refresh, map stale pages to registered sources, retain all other issues, support explicit URL authorization, enforce bounded progress, and update inventory and source packaging.

- [X] T061 [US9] Add the project-owned FlowKit Render Workflow skill with exact IDs, optional parenthesized agents and nonblank commands, type shapes, delegated outlines, one Start marker, descriptive declared edge labels, and source-faithful adjacent diagrams.
- [X] T062 Reconcile the approved ten-workflow delivery and deprecated Start Feature across spec, plan, tasks, research, data model, contracts, quickstart, and checklist; preserve baseline evidence and explicitly record pending validation and agent work.
- [X] T063 Generate the source-current node, branch, gate, loop, assignment, and version inventory and provenance record from revision c34ea2a; run available schema, graph, unit, and diff checks without claiming live execution or acceptance.
- [X] T064 Present and apply only the exactly approved F014 roadmap reconciliation patch in `validation/roadmap-reconciliation.patch`; keep lifecycle unchanged and record the operator decision.
- [X] T065 After separately operator-invoked Analyze and Remediate and Converge, reconcile additional accepted findings in `specs/014-flowkit-workflow-improvements/tasks.md` and their attributable results in `specs/014-flowkit-workflow-improvements/validation/report.json`; incorporate T066–T069 validation when delivered. Preserve successful T044 snapshot lifecycle and T046 reporting, record the supplementary external-working-tree lifecycle suite as skipped unless its sources are supplied, native agent selection as unverified unless the client exposes attributable evidence, and optional desktop checks as not run unless separately observed. Report exact remaining checks and recovery actions without treating static/snapshot results or this reconciliation as live-agent evidence, completion, or acceptance.

### Accepted semantic-review follow-up

These tasks implement and validate FR-022/FR-028 and SC-010/SC-013 against the reconciled design. They preserve the existing workflow topology, bounds, role separation, task history, and operator-owned product answers. Existing populated-output tests do not demonstrate semantic-defect detection. Deterministic fixtures establish routing and handoff evidence; live reasoning claims require separately attributable observations.

- [X] T066 [US3] Add populated but semantically deficient Plan fixtures in `tests/consumer-fixtures/plan-semantic-review/` and executable cases in `tests/test_workflow_paths.py`: a design contradicting an accepted spec requirement and a missing required design coverage case despite populated sections. Assert independent Reviewer findings carry stable ID, artifact location, violated requirement/accepted decision, observed deficiency, and exact correction separately from the strict envelope; the existing `verify-plan-output` → `prepare-plan-request` → `create-plan` path returns those exact findings to Planner, and fresh assessment confirms substantive resolution while reporting new blocking findings. Exercise digest/wording-only change, renamed/repeated findings, stale evidence, no resolution, fifth-pass continuation, and operator-owned product-question relay or blocked recovery; none grants success or an inferred answer. Preserve the five-pass cap, node IDs/edges, and separately invoked Tasks boundary. Depends on completed T024/T041/T050; run `python3 -m unittest discover -s tests -p test_workflow_paths.py`.
- [X] T067 [US4] After T066's shared test-file edits, add populated but semantically deficient Tasks fixtures in `tests/consumer-fixtures/tasks-semantic-review/` and executable cases in `tests/test_workflow_paths.py`: omitted accepted requirement coverage and dependencies contradicting the approved plan despite valid checklist structure. Assert the same exact finding contract returns through `verify-task-output` → `prepare-task-request` → `generate-tasks` to Tasker, existing IDs/check markers/completed history survive correction, and fresh assessment confirms prior deficiency resolution while retaining new blocking findings. Cover digest/wording-only change, renamed/repeated findings, stale evidence, no progress, fifth-pass continuation, and unresolved substantive product questions with exact operator relay or blocked recovery; preserve five-pass bounds, graph topology, and separate Analyze/implementation authority. Depends on T066 and completed T026/T041/T051; run `python3 -m unittest discover -s tests -p test_workflow_paths.py`.
- [X] T068 Reconcile only source gaps exposed by T066–T067 in `workflows/speckit-flow-plan/workflow.yml` and `workflows/speckit-flow-tasks/workflow.yml`: make existing Reviewer assessment and request preparation preserve exact semantic findings for author-owned correction, structural checks, finding-resolution progress, operator questions, and specific bounded stops. Keep existing nodes/edges, five-pass bounds, Planner/Tasker roles, and strict outcome-envelope fields; update affected manual paths, adjacent `flowchart.md`, `workflows/README.md`, and changed package versions/source bundle pins in `bundles/spec-kit-flow/bundle.yml` only where source changes require them. Extend `tests/test_workflow_graph.py` to compare exact topology and bounds with the reviewed baseline; run workflow path and graph suites plus `python3 tools/validate_workflows.py`, and record observed results/limits in `specs/014-flowkit-workflow-improvements/validation/report.json`. Depends on T066–T067; no installed-copy or release-catalog edits.
- [X] T069 Add executable Code Reviewer correction-or-stop cases in `tests/test_workflow_paths.py` and assignment assertions in `tests/test_agent_configs.py` for existing post-implementation assessment nodes in Implement, Converge, and Closeout. Supply an attributable implementation delta with an exact review finding; assert a distinct Code Reviewer returns it through the current workflow's eligible task/implementation correction path and fresh assessment confirms resolution, or a workflow lacking a safe eligible route produces a specific bounded stop and resumption action. Reject successful-command-only completion, unresolved review findings, inferred product answers, extra nodes, later workflow invocation, roadmap writes, Git integration, and acceptance. Reconcile only demonstrated prompt gaps in the affected source `workflows/speckit-flow-implement/workflow.yml`, `workflows/speckit-flow-converge/workflow.yml`, and `workflows/speckit-flow-closeout/workflow.yml`, with corresponding versions/pins/manual paths/diagrams if changed; run workflow path, graph, and agent suites and record deterministic versus live evidence separately in `specs/014-flowkit-workflow-improvements/validation/report.json`. Depends on T068 to serialize shared test-file edits and completed T039/T041; retain existing correction bounds and topology.

**Checkpoint**: Current static evidence and documentation cover the delivered source; optional desktop observations are separate. Release, roadmap verification, Git integration, and feature acceptance retain their own explicit decisions.

## Dependencies and Execution Order

### Phase dependencies

1. Phase 1 records the roadmap and prospective authority decisions. Source behavior that conflicts with those decisions cannot proceed while they are unresolved.
2. Phase 2 provides the shared controller, recovery, and graph-checking contract. All seven story phases depend on its completion.
3. Phase 1 records the cross-workflow inventory before source changes. US1 compares it with the machine-checked graph and provides a first implementation increment. US2–US7 can then proceed in separate workflow files, with shared test-file edits coordinated sequentially.
4. Phase 10 follows the delivered story phases. T043 aligns the source bundle pins before snapshot composition. T046 depends on T043–T045; T047 follows the automated report; T048 follows all accepted changes.

### Story completion order

| Story | Depends on | Independently testable result |
|---|---|---|
| US1 | Foundation and pre-change inventory | Checked active/deprecated inventory, Analyze's corrective loop, and Implement's core-skill continuation loop. |
| US2 | Foundation | Separate selection/activation and same-target specification/brief; deprecated source performs no work. |
| US3 | Foundation and approved Clarify policy | Clarify and Plan each reach an evidenced conclusion. |
| US4 | Foundation | Tasks generation and coverage assessment conclude without routine gates. |
| US5 | Foundation and approved Converge authority | Converge reaches clean or a bounded stop after ordered remediation. |
| US6 | Foundation and approved Close Out authority | Completion/debrief reaches an exact proposal or bounded stop. |
| US7 | Foundation and initial inventory | Every delegated branch has a usable exact name in this checkout. |
| US8 | Controller loop support and reviewed source authorization | Wiki refresh begins with lint, refreshes authorized registered sources individually, and reports all findings. |
| US9 | Reviewed workflow definitions | Project-owned diagrams expose exact source IDs, entry, type, delegation, and branch semantics. |

Shared files `tests/test_workflow_paths.py`, `tests/test_workflow_graph.py`, and `tools/validate_workflows.py` are edited sequentially by the listed tasks; `[P]` marks only work in disjoint files at the point where it is listed. Workflow YAML files and separate native TOML files can be worked on in parallel after their prerequisites. US1–US6 direct-controller path tests use deterministic named-agent fixtures; full native Codex selection evidence and final disposable-consumer validation wait for US7's files and assignment review. A structural or no-op check is not reported as live-agent validation. The accepted follow-up runs T066 → T067 → T068 → T069 sequentially because the tasks share test and workflow source files; T065 incorporates their attributable results after separately selected workflow follow-up. No new task has a parallel marker or a completed prerequisite that authorizes the next workflow.

## Parallel Execution Examples

- **US1**: T013 in `tests/test_workflow_paths.py` and T014 in `tests/test_workflow_graph.py` can be written together; after T015 records the baseline inventory, T016 and T017 affect different workflow packages.
- **US2**: T018 can be drafted while an independent worker examines the Start Feature YAML for T019; apply source changes after the test cases and approval gates are settled.
- **US3**: T021 and T022 cover different test files; T023 and T024 change separate Clarify and Plan packages after their respective prerequisites.
- **US4**: T025's test fixtures can be prepared alongside a read-only Tasks graph review; T026 and T027 then run in order.
- **US5**: T028 can be prepared while the approved Converge authority is documented; T029 follows the approval and test case definition.
- **US6**: T031 can be prepared while the approved Close Out rule is documented; T032 follows the approval and test case definition.
- **US7**: T034 and T035 affect separate test files; T037–T040 create or edit distinct native agent files after T036's assignment review.

## Implementation Strategy

Preserve Phase 1 decisions and the original eight-workflow baseline. The current inventory and reconciliation record describe accepted source delivery. T066–T069 are delivered against that source; The shared T065/T071/T073/T075/T076/T077 evidence reconciliation is delivered in `validation/report.json#source_current_reconciliation`; independent Converge run `0a87d86f-bb0a-4189-b692-b0367e434624` confirmed resolution with no remaining findings. Preserve the delivered pinned snapshot evidence; report the skipped external-working-tree lifecycle suite, unverified native selection, and optional unrun desktop checks separately. Deliver US1 as the first fixture-tested increment: its checked branch inventory, Analyze correction loop, and Implement core-skill continuation demonstrate the loop, evidence, and recovery machinery. Complete the remaining story phases against their own deterministic fixture sets, complete US7's native agent configuration and assignment review, then run the full direct-Codex and disposable-consumer checks. Automated results carry routine verification; at most two final operator checks may confirm the visible Codex desktop experience. Do not treat those observations as approval of a roadmap patch, release, Git integration, or feature acceptance.


## Phase 11: Convergence

This pass records current implementation gaps against the approved specification and remaining T065 evidence work. Complete the identifier-contract correction before reconciling final source-current evidence; retain all historical validation results and their limits.

- [X] T070 State the explicit `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` grammar for both `reason_code` and `resume_action` in every assessment prompt returning either field in `workflows/speckit-flow-analyze-remediate/workflow.yml`, `workflows/speckit-flow-clarify/workflow.yml`, `workflows/speckit-flow-closeout/workflow.yml`, `workflows/speckit-flow-implement/workflow.yml`, `workflows/speckit-flow-plan/workflow.yml`, `workflows/speckit-flow-tasks/workflow.yml`, and `workflows/speckit-flow-wiki-lint-update/workflow.yml`; preserve existing nodes, edges, roles, bounds, and envelope fields. Add assessment-prompt contract coverage in `tests/test_workflow_graph.py` and explicit underscore/space rejection coverage for both fields in `tests/test_controller.py`; reconcile affected manual paths, adjacent diagrams, source package versions, and `bundles/spec-kit-flow/bundle.yml` pins only where changed source requires it. Run controller and workflow graph suites plus `tools/validate_workflows.py`; record observed results and limits in `specs/014-flowkit-workflow-improvements/validation/report.json` per FR-029, FR-017, and SC-007 (partial).
- [X] T071 After T070 and fresh analysis of the resulting task/artifact changes, finish T065's attributable evidence reconciliation in `specs/014-flowkit-workflow-improvements/validation/report.json` and `specs/014-flowkit-workflow-improvements/tasks.md`: record this separately operator-invoked Converge's findings and their implementation/reassessment results, identify current component versions and source digests without relabeling historical 116-test or pinned snapshot observations as current reruns, and incorporate the delivered T066–T069 focused validation and T070 results. Verify recorded digests and versions against their source files and report exact remaining checks/recovery actions. Preserve T044/T046 successful historical evidence, supplementary external-working-tree lifecycle as skipped unless actually run, native selection as unverified unless attributable client evidence exists, optional desktop checks as not run unless observed, and Draft/in-progress plus separate release/Git/acceptance authority. Reconcile completion markers only from attributable delivered results per T065, FR-017, FR-024, and Constitution V (partial).


## Phase 12: Convergence

This fresh pass retains the unresolved findings already recorded by Phase 11. T072 overlaps T070, and T073 overlaps T071 and T065; one attributable implementation and validation of each shared obligation can support those task chains together. Preserve all prior IDs and completion markers, and analyze the appended tasks before implementation.

- [X] T072 Complete the still-unmet T070 identifier-contract correction in every assessment prompt returning `reason_code` or `resume_action` across `workflows/speckit-flow-*/workflow.yml`, explicitly stating `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` for both fields; retain the verified Converge 0.4.6 syntax correction and preserve topology, assignments, bounds, and envelope fields. Verify coverage in `tests/test_workflow_graph.py` and underscore/space rejection for both fields in `tests/test_controller.py`; reconcile only affected manual paths, adjacent diagrams, package versions, and `bundles/spec-kit-flow/bundle.yml` pins. Run controller and workflow graph suites and `tools/validate_workflows.py`, and record attributable results and limits in `specs/014-flowkit-workflow-improvements/validation/report.json` per FR-029, FR-017, and SC-007 (partial).
- [X] T073 After T070/T072 delivery and fresh artifact/task analysis, complete the shared T065/T071 evidence obligation in `specs/014-flowkit-workflow-improvements/validation/report.json` and reconcile its supported completion markers in `specs/014-flowkit-workflow-improvements/tasks.md`: record this Converge pass, the verified post-Implement Converge boundary and exact intervening syntax fix, current component versions/digests, T066–T069 focused validation, and T070/T072 correction and reassessment results. Verify current versions/digests against source files; keep the historical 116-test and pinned snapshot observations distinct from actual new runs, preserve supplementary lifecycle skips, unverified native selection, and optional unrun desktop checks unless new attributable evidence exists, and report remaining checks/recovery actions. Preserve Draft/in-progress and separate release/Git/acceptance authority per T065, FR-017, FR-024, and Constitution V (partial).


## Phase 13: Convergence

This pass retains F014-G001 and F014-G002 after the analyzed plan-status correction. T074 shares the T070/T072 obligation, and T075 shares T065/T071/T073; deliver each shared correction once, preserve all earlier task IDs and markers, and analyze the changed task list before eligible implementation.

- [X] T074 Complete the shared T070/T072 assessment-identifier correction in every assessment prompt returning `reason_code` or `resume_action` across `workflows/speckit-flow-*/workflow.yml`, explicitly stating `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$` for both fields; preserve the verified Converge 0.4.6 correction, topology, assignments, bounds, and outcome fields. Add prompt-coverage assertions in `tests/test_workflow_graph.py` and underscore/space rejection checks for both fields in `tests/test_controller.py`; reconcile only affected manual paths, adjacent diagrams, source package versions, and `bundles/spec-kit-flow/bundle.yml` pins. Run controller and graph suites plus `tools/validate_workflows.py` and record attributable results and limits in `specs/014-flowkit-workflow-improvements/validation/report.json` per FR-029, FR-017, and SC-007 (partial).
- [X] T075 After T070/T072/T074 delivery and fresh artifact/task analysis, complete the shared T065/T071/T073 evidence reconciliation in `specs/014-flowkit-workflow-improvements/validation/report.json` and reconcile only supported completion markers in `specs/014-flowkit-workflow-improvements/tasks.md`: record this Converge pass, verified post-Implement boundary and intervening syntax fix, source-current versions/digests, delivered T066–T069 validation, identifier correction, and fresh reassessment results. Verify versions/digests against current source; distinguish historical 116-test and pinned snapshot observations from actual new runs, preserve supplementary lifecycle skips, unverified live/native behavior, and optional unrun desktop checks unless attributable new evidence exists, and report remaining checks/recovery actions. Preserve Draft/in-progress and separate release/Git/acceptance authority per T065, FR-017, FR-024, and Constitution V (partial).


## Phase 14: Convergence

This fresh pass resolves F014-G001 through substantive source and test evidence and retains F014-G002. T076 shares the existing T065/T071/T073/T075 evidence obligation; reconcile it once after fresh analysis, preserving all historical task IDs, completion markers, observations, and evidence limits.

- [X] T076 After delivered T070/T072/T074 and fresh artifact/task analysis, complete the shared T065/T071/T073/T075 evidence reconciliation in `specs/014-flowkit-workflow-improvements/validation/report.json` and reconcile only attributable supported completion markers in `specs/014-flowkit-workflow-improvements/tasks.md`: record this fresh Converge reassessment, F014-G001 resolution and remaining F014-G002, verified post-Implement boundary, current source versions/digests, delivered semantic-review validation and identifier correction. Verify recorded source digests and versions against current files and preserve historical 116-test and pinned snapshot observations separately from the newly observed 50 controller tests, 12 graph tests, and workflow validator. Preserve supplementary lifecycle skips, unverified live/native behavior, optional unrun desktop checks, Draft/in-progress status, and separate release/Git/acceptance authority; state exact remaining checks and recovery actions per T065, FR-017, FR-024, and Constitution V (partial).


## Phase 15: Convergence

This fresh pass confirms F014-G001 remains resolved and retains F014-G002 after clean artifact analysis. T077 shares T065/T071/T073/T075/T076; deliver the evidence reconciliation once and preserve every historical task ID, marker, observation, and validation limit.

- [X] T077 After delivered T070/T072/T074 and fresh analysis of this appended task list, complete the shared T065/T071/T073/T075/T076 evidence obligation in `specs/014-flowkit-workflow-improvements/validation/report.json` and reconcile only supported completion markers in `specs/014-flowkit-workflow-improvements/tasks.md`: record this Converge pass, F014-G001 resolution and F014-G002 correction/reassessment, the verified post-Implement boundary and intervening syntax fix, current component IDs/versions/source digests, source coordinates, CLI evidence, and delivered semantic-review and identifier-grammar validation. Validate recorded versions and digests against current source and distinguish historical 116-test and pinned snapshot observations from the recorded 41 semantic-review checks and 50 controller/12 graph checks; require fresh reassessment to confirm reconciliation, without claiming those historical tests were rerun. Preserve supplementary lifecycle skips, unverified live/native behavior, optional unrun desktop checks, Draft/in-progress status, separate release/Git/acceptance authority, and exact remaining checks/recovery actions per T065, FR-017, FR-024, and Constitution V (partial).


## Shared evidence reconciliation

T065/T071/T073/T075/T076/T077 are completed by one source-current evidence correction in [the report](validation/report.json). Original 116-test and pinned snapshot observations, 41 semantic-review checks, and 50 controller/12 graph checks remain historical and were not rerun in this evidence pass. Current component versions, digests, and active bundle pins were verified; the workflow validator passed for eleven definitions. The prior independently verified post-Implement syntax-fix boundary and grammar reassessment remain attributable. Independent Converge run `0a87d86f-bb0a-4189-b692-b0367e434624` confirmed F014-G002 resolution with a validated complete outcome and no remaining findings. Supplementary lifecycle remains skipped, live semantic reasoning and native identity introspection remain unverified, optional desktop checks remain not run, and Draft/in-progress, release, Git, and acceptance authority remain unchanged.


## Phase 16: Convergence

This pass records F014-D001: eight undelegated loop nodes in seven diagrams display agent names absent from their source nodes. Correct presentation only, preserving workflow topology, delegated-node labels, and completed task history.

- [X] T078 Remove phantom parenthesized agent labels from the undelegated do-while nodes in `workflows/speckit-flow-analyze-remediate/flowchart.md`, `workflows/speckit-flow-implement/flowchart.md`, `workflows/speckit-flow-plan/flowchart.md`, `workflows/speckit-flow-tasks/flowchart.md`, `workflows/speckit-flow-converge/flowchart.md`, `workflows/speckit-flow-closeout/flowchart.md` (both loops), and `workflows/speckit-flow-wiki-lint-update/flowchart.md` per FR-026, SC-012, and US9/AC2 (contradicts). Preserve exact source step IDs, conditions, caps, entry edges, shapes, outlines, topology, and all genuinely assigned delegated-node labels. Add a source-to-diagram assertion in `tests/test_workflow_graph.py` rejecting agent labels on unassigned nodes and retaining exact assigned labels; run the graph suite and `tools/validate_workflows.py --fail-on-unexplained`, then reconcile only changed diagram validation coordinates in `specs/014-flowkit-workflow-improvements/validation/report.json` without relabeling historical evidence. Depends on completed T068/T069/T074 and fresh analysis of this appended task before eligible implementation.

- [X] T079 Correct the manual Plan and Tasks guidance in `workflows/README.md` to require independent structural and semantic assessment, exact located findings returned to Planner or Tasker, fresh substantive resolution before retry/completion, operator-owned product answers, task/design preservation and the existing five-pass bounds. Remove the manual Plan statement excluding design-quality review; required-file production alone must not establish completion. Add focused manual/direct contract parity assertions in `tests/test_workflow_graph.py`, run graph/path tests and the source validator, and record attributable evidence in `specs/014-flowkit-workflow-improvements/validation/report.json`. This resolves F014-M001 under FR-001/FR-005/FR-007/FR-028 and SC-007/SC-013 without new nodes or authority. Implement after prerequisites and checklist verification; preserve all historical tasks and feature/roadmap status.

T078/T079 are delivered with 15 graph tests (including all eleven diagrams and ten negative mutations), 26 workflow path tests and independent code review passing. Fresh full-suite incorporation validation ran 126 tests with no failures or errors, plus a passing pinned consumer lifecycle; the supplementary external-working-tree suite was skipped. The original 79 tasks are complete; current source evidence is in `final_source_validation` in [the report](validation/report.json). T080–T089 below add the remaining live verification work.

## Phase 17: Live Workflow Verification

The operator requested agent-driven live testing, evidence collection, source remediation, and retries under one Codex goal. This phase verifies the seven active workflows without live end-to-end evidence from the previous verification cycle. Preserve completed task history and distinguish real installed-skill execution from static graph projection, mocked dispatch, readiness probes, and earlier observations. Scope is disposable local consumers and this repository's reviewed source; each workflow remains a separately invoked phase, with its existing steps, agent assignments, bounds, prerequisites, and human gates intact.

**Execution contract**: Once this phase is invoked, start a Codex goal to complete T080–T089. The coordinating task may explicitly invoke the listed workflows in the disposable Codex task, observe completion, make in-scope source corrections, refresh the consumer, and separately invoke retries. An individual workflow must never invoke another workflow. Continue while measurable progress is possible; a recoverable test failure is work to remediate, not completion or an automatic reason to return control to the operator. Stop for genuinely missing access, unavailable exact agent assignments, an unresolved authority or material product decision, or repeated failure without a supported correction. Preserve checkpoints and exact recovery actions. Do not mark the goal complete while a required scenario remains failed, skipped, or unverified.

**Human inputs**: Prepare concrete fixture choices, specification answers, curated local wiki sources, and exact roadmap patches during setup. Reuse only attributable operator decisions that match the current question and exact patch bytes; do not impersonate the operator, manufacture gate approval, relax a gate for testing, or treat a simulated approval as a live gate result. Request genuinely missing setup decisions together before dependent scenarios. If a later correction invalidates an approval, checkpoint that scenario, continue independent scenarios, and request the changed exact decision. No task authorizes a commit, push, release, real-project roadmap verification, or feature acceptance.

**Evidence and completion**: Every required scenario must invoke the real installed FlowKit skill with its core/extension command skills and exact named agents, reach its expected complete outcome or intentionally tested bounded stop, and pass independent assertions on durable artifacts and prohibited side effects. A blocker in a success scenario is a failed scenario, even if controller validation passes. Record step/run IDs, validated outcomes, loop passes, source and installed component versions/digests, before/after artifact digests, findings, corrections, and retest links in portable `validation/live-workflows/` records. Use repository-relative or fixture-relative paths, sanitized summaries, and no raw transcripts or personal host paths. Keep an explicit matrix of required scenarios, observed results, and remaining untested branches; selected scenario coverage is not proof of every possible live branch or every extension command.

- [x] T080 Prepare an initialized disposable consumer and a reusable scenario plan in `specs/014-flowkit-workflow-improvements/validation/live-workflows/setup.md`. Prefer reusing the existing disposable Codex task after inspecting its current state; establish native-agent launch support, required core skills and ownership manifests, compatible roadmap/wiki integrations, all ten active workflow installations, exact role configurations, and source/installed digests. Prepare an isolated small synthetic feature with a roadmap dependency chain, constitution, local wiki sources, and a tiny implementable scope. Define pristine fixture checkpoints and scenario-specific copies so prior changes cannot hide defects; preserve historical run evidence before resets. Present any required one-time operator setup and concrete gate/answer packet, including exact proposed roadmap patches, before dependent runs. Record the attributable approved inputs and their validity conditions. Do not require another project's roadmap or wiki. Depends on delivered T079.

- [x] T081 Establish the goal-driven test coordination and recovery procedure in `specs/014-flowkit-workflow-improvements/validation/live-workflows/runbook.md`, and use it for T082–T089. Invoke installed skills by messaging the authorized disposable Codex task, wait for run completion, collect controller summaries and independently inspect artifact changes, and maintain a durable scenario/finding ledger across context changes. Record exact prompts and prerequisites using portable fixture identities. For each discovered defect, identify its smallest affected source package, add a meaningful regression check, correct reviewed source rather than installed copies, reconcile affected spec/plan/task intent, versions, bundle pins, manual guidance and diagrams, run relevant checks, then refresh the consumer using the supported installation path and verify the installed digests before retry. Retain attributable before/after boundaries required by debrief or Converge; do not overwrite historical failed runs. Reuse stable finding IDs and existing remediation tasks rather than appending duplicates on every retry. Keep the outer goal active until all required scenarios pass or an actionable external blocker is established. Depends on T080; this task remains open until the procedure has actually coordinated the verification phase.

- [x] T082 Run `$flow-kit-select-feature` live against the synthetic roadmap. Verify that candidates and dependency relationships are presented before selection, the recorded operator choice selects the exact feature, and only the approved exact roadmap patch and `.specify/feature.json` activation occur. Assert existing specification bytes are preserved and no new specification is authored. Separately exercise a rejected selection/patch and a conflicting or unresolved mapping, verifying the intended stop and no unauthorized writes. Collect evidence under `validation/live-workflows/select-feature/`, remediate defects through T081, and retry the affected scenarios until their independent assertions pass. Depends on T080 and the T081 coordination procedure.

- [x] T083 Run `$flow-kit-specify` live for the selected synthetic feature with an attributable authoring request. Verify governing context, actual core specification authoring, exact active-target preservation, uniquely resolved roadmap linkage, and the resulting roadmap brief. Exercise an approved exact linkage repair when required and an unresolved/conflicting linkage stop without unauthorized roadmap edits. Assert no implicit Plan invocation or target substitution. Store results under `validation/live-workflows/specify/`; remediate and retry through T081. Depends on T082's successful selection scenario, or a separately verified equivalent pristine target fixture.

- [x] T084 Run `$flow-kit-clarify` live on a synthetic specification with explicit ambiguities and setup-approved product answers. Verify questions are presented and recorded, each session respects the core five-question cap, significant remaining ambiguity causes a real subsequent session, and fresh assessment concludes only after substantive resolution. Also run a clean/no-significant-ambiguity case and an intentionally unresolved answer/no-progress case with an evidenced bounded stop. Do not invent answers or automatically start Plan. Store results under `validation/live-workflows/clarify/`; remediate and retry through T081. Depends on T083's successful authoring scenario, with isolated fixtures for the additional cases.

- [x] T085 Run `$flow-kit-plan` live on the clarified synthetic feature. Verify the actual core Plan skill produces every required planning deliverable and an independent Reviewer performs structural and semantic assessment. Run a controlled scenario with a known missing deliverable or material inconsistency visible at the assessment boundary; verify exact located findings return to Planner, a real corrective invocation occurs, and fresh review proves resolution before completion. Record how the defect is introduced without editing installed workflow definitions or falsifying outcomes. Exercise a material product decision stop with the exact unresolved question. Store results under `validation/live-workflows/plan/`; remediate and retry through T081. Depends on T084's successful clarification scenario.

- [x] T086 Run `$flow-kit-tasks` live on the reviewed synthetic plan and specification. Independently verify actual core task generation, requirement/design coverage, dependency ordering, and preservation of existing task history. Run a controlled missing-coverage or semantic-inconsistency scenario at the assessment boundary; verify the Reviewer hands exact findings to Tasker, the correction actually runs, and fresh review proves substantive resolution. Exercise a material design-gap stop and assert no implicit Analyze or Implement invocation. Store results under `validation/live-workflows/tasks/`; remediate and retry through T081. Depends on T085's successful planning scenario.

- [x] T087 Run `$flow-kit-closeout` live on the small synthetic feature after separately invoking Analyze and Remediate, Implement, and Converge as needed to establish trustworthy current-task implementation and completion evidence. These prerequisite invocations are coordinated outside Closeout and do not close the real Feature 014. Verify the actual debrief, evidence-backed specification status, exact approved roadmap verification, wiki ingestion/lint, and final readiness report without Git integration or feature acceptance. Include one routine debrief correction and one substantive stale-source wiki reconciliation requiring a real refresh and fresh lint; also exercise a rejected exact roadmap patch and verify partial-state preservation and the intended stop. Use the setup-approved patch only when its bytes still match. Store results under `validation/live-workflows/closeout/`; remediate and retry through T081. Depends on T086's successful task-generation scenario and separately established prerequisite evidence.

- [x] T088 Run the installed Wiki Lint Update launcher for `speckit-flow-wiki-lint-update` live on an isolated local wiki fixture. Verify lint runs first, at least two concretely stale registered sources are mapped through their cited source identities and refreshed through real ingestion passes, and fresh lint plus substantive claim/citation checks establish resolution. Also exercise an already-clean case and a conflicting or unsupported inconsistency case that remains visible and stops without invented authority; assert age-only timestamp changes do not count as progress. Record non-staleness findings rather than silently dropping them. Store results under `validation/live-workflows/wiki-lint-update/`; remediate and retry through T081. Depends on T080 and the T081 coordination procedure; may run independently of T082–T087.

- [x] T089 Independently reconcile the seven workflow scenario records and all defect/retest chains into `specs/014-flowkit-workflow-improvements/validation/live-workflows/coverage.md` and `validation/report.json`. Require successful live terminal outcomes and artifact assertions for every required success scenario, correct observable stops and side-effect assertions for every required negative scenario, and no unresolved defects. Re-run the relevant automated regression suites, full available suite, workflow validator, installation checks affected by corrections, and whitespace checks against final source; refresh and rerun affected live scenarios whenever their installed package or shared controller changes. Preserve historical evidence and explicitly name untested branches, unexecuted skill commands, unavailable client introspection, and unrelated optional checks. Reconcile changed intent across this feature's spec, plan, tasks, quickstart, and validation audit without implying release, Git integration, roadmap acceptance, or exhaustive universal live coverage. Mark T080–T089 and the Codex goal complete only when their attributable completion criteria are satisfied. Depends on T081–T088.

T088 completion evidence and T081 ongoing coordination evidence are recorded in [live coverage](validation/live-workflows/coverage.md) and [the ledger](validation/live-workflows/ledger.json). All four Wiki scenarios passed on final workflow 0.1.3/controller 0.5.2, with independent terminal validation and artifact checks. Routine corrections clarified all 13 assessment prompts and the shared protocol without changing graph topology or runtime validation. Focused 86-test and full 126-test suites passed; one optional external lifecycle check was skipped. At that Wiki milestone, T080–T087 and T089 remained open; it did not complete the live verification goal.

T084 completion evidence is recorded in the live ledger and three independent Clarify audits: two actual sessions with five and four attributable answers; an already-clean session with zero questions and no mutation; and a real unanswered question stopped with `human-input-missing`, preserving its original child for explicit resumption. At that Clarify milestone, ten of 23 required scenarios passed and T080–T083, T085–T087 and T089 remained open.

T085 completion evidence is recorded in three independent Plan audits: actual substantive generation, exact-finding correction and fresh review, and an actual valid unanswered product question with a bounded stop. At that Plan milestone, thirteen of 23 required scenarios passed and T080–T083, T086–T087, and T089 remained open. Historical failed trials are retained.

T086 completion is supported by independent audits of task generation/history preservation, exact-finding correction with fresh review, and a real unanswered question for a material plan/spec contradiction. At that Tasks milestone, sixteen of 23 required scenarios passed and T080–T083, T087, and T089 remained open; failed trials and their bounded corrections remain recorded.

T080 setup is delivered after the corrected live selection retry verified the actual writer prerequisite and protected artifact invariants. Its independent audit and directly approved supplemental decisions are linked in [setup](validation/live-workflows/setup.md). Scenario verification remains incomplete at seventeen of 23 required passes.

T082 is delivered: exact approved selection/activation, attributable defer with protected files and Git refs unchanged, and unsafe mapping exclusion all passed independent live audits. Eighteen of 23 required scenarios pass; Specify linkage repair and four Closeout cases remain.

T083 is delivered: actual authoring with mandatory checks and clean brief, exact-gated missing-link repair with fresh verification, and competing-linkage stop passed independent audits. Nineteen of 23 required scenarios pass; four Closeout cases remain.

T087 is delivered across all four actual Closeout cases. The final stale-source case completed three individual ingestions, three fresh six-check lints, independent substantive coverage assessments and the terminal readiness report. Its audit records 54 native assertions, 33 coordinator checks and 15 typed execution children. All 23 required scenarios now pass. T081 coordination and T089 final reconciliation are complete within the recorded limits; no Git integration or acceptance is inferred.
