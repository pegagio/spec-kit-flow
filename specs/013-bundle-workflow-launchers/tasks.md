# Tasks: FlowKit Codex Workflow Controllers

**Input**: `specs/013-bundle-workflow-launchers/spec.md`, `plan.md`, `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`

**Prerequisites**: Constitution 4.0.0; pinned Specify CLI `1.0.10.dev0+pegagio.2`; reviewed Feature 011 bundle and catalog foundation

**Tests**: Required by FR-013 and the story acceptance scenarios. Write each story's focused tests before its implementation tasks; preserve separate live desktop evidence because a stub cannot prove child-task behavior.

**Organization**: User stories are P1 controller execution, P2 human interaction and recovery, and P3 bundle lifecycle. Tasks use repository-relative file paths. A release gate remains open until model access, skill ownership, and selected-project interaction are proven in disposable consumers.

## Phase 1: Setup

**Purpose**: Prepare small, reusable fixtures and record the tested integration coordinates without changing released packages.

- [X] T001 Create `tests/consumer-fixtures/controller-workflow.yml` with ordered prompt, command, gate, and nested switch/default steps, modeled and unmodeled executable nodes, and an untaken-branch model for controller tests.
- [X] T002 [P] Create `tests/consumer-fixtures/controller-local-skill/SKILL.md` as an unrelated consumer-owned Codex skill fixture for install, refresh, and removal preservation checks.
- [X] T003 Record the pinned `specify --version`, `codex --version`, source coordinates, step-model capability probe, skill-tools versus Specify Python import behavior, and supported Codex `SKILL.md` plus `agents/openai.yaml` shape in `specs/013-bundle-workflow-launchers/validation.md`; confirm that Specify bundle manifests do not install direct skills, and distinguish schema acceptance from model entitlement and native CLI dispatch from desktop children.

## Phase 2: Foundational

**Purpose**: Establish a no-dispatch way to inspect the installed workflow. This blocks all three user stories.

- [X] T004 Add failing tests in `tests/test_controller.py` for locating the selected compatible Specify runtime through mise and ordinary executable paths, rejecting missing, ambiguous, or mismatched runtimes before state changes, loading the composed installed workflow in the selected project, preserving version, source digest, bundle-record and FlowKit skill-record content/device/inode fingerprints, and never calling native `WorkflowEngine.execute` or `specify workflow run`.
- [X] T005 Implement the portable Specify runtime locator and version check in `controllers/flow-kit/scripts/bootstrap.sh` and the bounded read-only installed-definition loader and immutable workflow, bundle-record, and skill-record snapshot in `controllers/flow-kit/scripts/python/controller.py`; use the selected compatible Specify composition API without requiring a consumer skill-tools environment, return only graph and provenance to the main task, and reject an unsupported step or template form before execution.

**Checkpoint**: The controller can inspect, identify, and validate an installed workflow without creating native workflow run state.

## Phase 3: User Story 1 — Run Installed Workflows in a Codex Task (P1) 🎯 MVP

**Goal**: Eight discoverable skills execute their installed workflow definitions in the selected desktop task, with reviewed per-step models and full preflight.

**Independent test**: In a disposable Codex consumer, install through the development-snapshot FlowKit catalog route, find all eight skills and a verified ownership record, invoke one with valid inputs, observe its installed graph and modeled child assignment, and verify a missing runtime, missing input, or invalid model stops before any workflow step.

### Tests

- [X] T006 [US1] Add failing tests in `tests/test_controller.py` for every switch branch, required inputs, unique step IDs, one named-step model and/or effort override, unmodeled main-task steps, installed Codex command-skill resolution and provenance, rejection of a missing, mismatched, or inaccessible skill without fallback, medium effort when omitted on a modeled step, high effort when declared, invalid model-effort pairs, and the rule that models and effort belong only on modeled prompt or command steps, never gates, switches, or workflow defaults.
- [X] T007 [P] [US1] Add failing Codex consumer tests in `tests/test_bundle_lifecycle.py` for eight stable `flow-kit-{purpose}` skill IDs, the eight exact FlowKit display names in `contracts/controller.md`, one-to-one workflow mapping, a complete initial `.specify/flow-kit/skills-install.json` record, selected project context, and a clear stop for a missing installed workflow; assert no controller extension command is installed.
- [X] T008 [P] [US1] Add failing source and catalog tests in `tests/test_catalog.py` for the direct Codex skill package manifest, eight source skill directories, the exact model-effort assignment matrix in `plan.md`, changed workflow versions and digests, release source digest, explicit disposable `--development-snapshot` install and refresh paths that retain ordinary snapshot rejection, and rejection of an unchanged catalog release version when package content changes.

### Implementation

- [X] T009 [US1] Implement recursive all-branch enumeration, required-input checks, unique step identity, and exact one-step model and/or effort override in `controllers/flow-kit/scripts/python/controller.py`; require a nonempty model for each child, resolve omitted effort to `medium`, reject effort without a model or model/effort on gates and switches, and stop on a negative or inconclusive model-effort availability result without mutating workflow artifacts.
- [X] T010 [US1] Implement ordered prompt/command execution, selected-project Codex command-skill resolution using the pinned Specify invocation rule with name and available provenance checks, rendered argument pass-through, main-task gate verdict output, exact switch-case/default routing, supported `{{ inputs.* }}` and `{{ steps.*.output.* }}` rendering, and stop-on-unknown semantics in `controllers/flow-kit/scripts/python/controller.py`; follow installed YAML rather than copy its prompts or gates.
- [X] T011 [US1] Write `controllers/flow-kit/controller-protocol.md` for the main task to display every effective model-effort pair, probe each distinct pair with a no-project-work child before workflow execution, invoke each resolved installed command skill with its rendered YAML arguments in the main task or bounded modeled child using that pair, and stop on an inconclusive probe, missing command skill, or dispatch failure without fallback.
- [X] T012 [US1] Create `controllers/flow-kit/manifest.yml` with a reviewed package version, compatible Specify CLI coordinate, Codex compatibility, and eight `flow-kit-{purpose}` skill IDs, display names, and one-to-one workflow bindings; validate the manifest against the eight direct skill directories without introducing Specify controller commands.
- [X] T013 [P] [US1] Create thin `controllers/flow-kit/skills/flow-kit-start-feature/`, `flow-kit-clarify/`, `flow-kit-plan/`, and `flow-kit-tasks/` skill directories with `SKILL.md` and `agents/openai.yaml`, each binding only its workflow ID and using the installed shared protocol.
- [X] T014 [P] [US1] Create thin `controllers/flow-kit/skills/flow-kit-analyze-remediate/`, `flow-kit-implement/`, `flow-kit-converge/`, and `flow-kit-closeout/` skill directories with `SKILL.md` and `agents/openai.yaml` and the same ID-only contract.
- [X] T015 [P] [US1] Update `workflows/speckit-flow-start-feature/workflow.yml`: assign `gpt-6-sol` to `assess-eligibility`, `draft-specification`, and `brief-against-roadmap`; leave the approval-gated roadmap write and other steps unmodeled, omit `workflow.model`, and bump the workflow version.
- [X] T016 [P] [US1] Update `workflows/speckit-flow-clarify/workflow.yml`: assign `gpt-6-sol` only to `clarify-specification`, leave gate/switch/stop prompts unmodeled, omit `workflow.model`, and bump the workflow version.
- [X] T017 [P] [US1] Update `workflows/speckit-flow-plan/workflow.yml`: assign `gpt-6-astra` to `create-plan` and `gpt-6-sol` to `return-to-clarification`, leave the readiness gate and stop prompts unmodeled, omit `workflow.model`, and bump the workflow version.
- [X] T018 [P] [US1] Update `workflows/speckit-flow-tasks/workflow.yml`: assign `gpt-6-luna` with `reasoning_effort: high` to `generate-tasks` and `gpt-6-sol` with implicit medium effort to `return-to-plan`; leave the task-review gate and stop prompts unmodeled, omit workflow-level model and effort defaults, and bump the workflow version.
- [X] T019 [P] [US1] Update `workflows/speckit-flow-analyze-remediate/workflow.yml`: assign `gpt-6-astra` to `analyze-artifacts`, every `reanalyze-*` command, and every `replan-*` command; assign `gpt-6-sol` to the `remediate-*` and `retask-*` commands; leave gates/switches/stop prompts unmodeled, omit `workflow.model`, and bump the workflow version.
- [X] T020 [P] [US1] Update `workflows/speckit-flow-implement/workflow.yml`: assign `gpt-6-luna` with `reasoning_effort: high` to `implement-eligible-work` and `gpt-6-sol` with implicit medium effort to all `return-to-*` commands; leave gates/switches/stop prompts unmodeled, omit workflow-level model and effort defaults, and bump the workflow version.
- [X] T021 [P] [US1] Update `workflows/speckit-flow-converge/workflow.yml`: assign `gpt-6-astra` with implicit medium effort to `assess-convergence` and `gpt-6-sol` with implicit medium effort to `return-remediation-to-analysis`; leave gates/switches/stop prompts unmodeled, omit workflow-level model and effort defaults, and bump the workflow version.
- [X] T022 [P] [US1] Update `workflows/speckit-flow-closeout/workflow.yml`: assign `gpt-6-sol` to `debrief-roadmap`, `ingest-curated-context`, and `lint-wiki`; leave the approved completion operation, roadmap write, gates, switches, and stop prompts unmodeled; omit `workflow.model` and bump the workflow version.
- [X] T023 [US1] Pin the eight bumped workflow versions in `bundles/spec-kit-flow/bundle.yml`, preserving the independent roadmap/wiki extension pins and manual workflow packages; validate that `controllers/flow-kit/manifest.yml` binds exactly those eight workflow IDs.
- [X] T024 [US1] Extend `tools/catalog.py` to package the reviewed direct skill source and shared helper, record their package version and digest alongside the eight workflow source digests in `catalog/release.json`, and install or refresh the skill package through the supported catalog route with ownership preflight, verified inventory, and atomic initial or replacement `.specify/flow-kit/skills-install.json` records before any skill can run; add explicit `--development-snapshot` install and refresh modes limited to disposable initialized consumers and snapshot build provenance for uncommitted source digests plus dirty status, while ordinary install/refresh keep rejecting snapshots and release builds retain clean-source gates.
- [X] T025 [US1] Validate the P1 path in a disposable initialized consumer through the development-snapshot catalog route in `tests/test_bundle_lifecycle.py`, plus `tests/test_controller.py` and `tests/test_catalog.py`; record skill invocation names, source and installed display metadata, installed workflow attribution, Specify runtime selection, effective model-effort pairs, selected project, and preflight blockers in `specs/013-bundle-workflow-launchers/validation.md` without claiming a released catalog or live child behavior from a stub.
- [X] T026 [US1] Run the live `flow-kit-tasks` scenario in the selected disposable Codex task from `specs/013-bundle-workflow-launchers/quickstart.md`; confirm the compatible Specify loader, all eight exact display names in the Codex skill picker, the modeled child's invocation of the selected project's installed `speckit-tasks` skill with YAML-rendered arguments, its actual Luna/high assignment, named-step model and effort overrides, main-task gate, visible result and workspace diff, and missing-runtime, missing-command, rejected-input, or unavailable-model-effort stops before any workflow step or recovery record in `specs/013-bundle-workflow-launchers/validation.md`.

**Checkpoint**: A controller can run one installed workflow in the chosen task, with model preflight, while all eight names are discoverable. Do not claim full acceptance until the live and lifecycle gates below pass.

## Phase 4: User Story 2 — Keep Human Decisions in the Main Task (P2)

**Goal**: An interactive child pauses for a human answer in the main task, continues as the same child, and leaves bounded recovery evidence on failure, interruption, or refresh.

**Independent test**: Invoke an interactive clarification and a gate in a disposable consumer; answer in the main task, verify continuation in the same child, then exercise failure, interruption, and refresh without rollback, retry, or later-phase launch.

### Tests

- [X] T027 [US2] Add failing tests in `tests/test_controller.py` for structured child questions with options and custom answers, same-child continuation, an explicit main-task gate verdict, invalid or missing human answers, and no advancement to another workflow phase.
- [X] T028 [US2] Add failing record and stop tests in `tests/test_controller.py` for atomic updates before child dispatch and after each step, preserved partial edits, `pending/running/waiting_for_human/completed/incomplete` statuses, recorded effective model-effort pairs, a running step treated as incomplete after interruption, relative changed-file paths, no transcripts/secrets/absolute paths, and a stop after an active child finishes when the workflow digest, Specify bundle-record fingerprint, or FlowKit skill-record fingerprint changes, including a skill-only refresh with unchanged workflow YAML.

### Implementation

- [X] T029 [US2] Extend `controllers/flow-kit/controller-protocol.md` with main-task multiple-choice or custom-answer presentation, explicit gate decisions, answer relay to the same child identity, and a stop if relay or continuation fails.
- [X] T030 [US2] Implement atomic `.specify/flow-controllers/runs/<run-id>/summary.json` updates in `controllers/flow-kit/scripts/python/recovery.py` after successful preflight and at each step boundary; include workflow ID/version/digest, starting bundle-record and skill-record fingerprints, effective models and reasoning efforts, statuses, repository-relative changed files, and blocker, excluding full child transcripts, secrets, absolute paths, and file contents, and create no record for a rejected preflight.
- [X] T031 [US2] Extend `controllers/flow-kit/scripts/python/controller.py` to preserve child edits on failure, reject automatic retry or resume, and compare the installed workflow digest plus both record content/device/inode fingerprints before each next step and after an active child completes; stop under any changed installation record without executing another step.
- [X] T032 [US2] Run the live selected-project clarification and human-gate scenario from `specs/013-bundle-workflow-launchers/quickstart.md` in a disposable consumer; use `tools/catalog.py refresh <consumer> --development-snapshot` for the skill-only mid-run refresh and record child identity, effective model, answer relay, main-task diffs, failed-step edits, interruption evidence, and refresh stop despite unchanged workflow YAML in `specs/013-bundle-workflow-launchers/validation.md`.

**Checkpoint**: Same-child interaction and operator-guided recovery have live evidence. Failure or interruption leaves files and a compact record, and no phase advances automatically.

## Phase 5: User Story 3 — Maintain Controllers Through the FlowKit Catalog (P3)

**Goal**: Install, refresh, and removal align controller skills with pinned workflows while preserving consumer-owned content.

**Independent test**: In disposable Codex consumers, install, refresh, and remove through the FlowKit catalog route; check controller inventory and workflow alignment, then repeat with a same-name skill and a locally edited FlowKit file and verify conflicts are reported without silent replacement or deletion.

### Tests

- [X] T033 [US3] Add failing catalog lifecycle cases in `tests/test_bundle_lifecycle.py` for fresh install, refresh, removal of owned files and the skill ownership record with recovery summaries preserved, a same-name consumer skill, a locally edited owned skill or helper, incomplete operations, unrelated skills, feedback evidence, and independently installed Specify components.
- [X] T034 [P] [US3] Add failing release-integrity cases in `tests/test_catalog.py` for the direct skill package archive, manifest ID/version, eight skill directories and display metadata, changed workflow digests, and safe refusal when controller inventory differs from the released workflow set.

### Implementation

- [X] T035 [US3] Extend `tools/catalog.py` with full refresh and removal ownership checks and postcondition inventory checks for the directly installed skills and shared helper; compare source and installed-file digests, report conflicts or partial operations, preserve locally modified or consumer-owned files, atomically replace `.specify/flow-kit/skills-install.json` only after a verified refresh, and remove it only after verified removal while preserving `.specify/flow-controllers/runs/` recovery summaries.
- [X] T036 [US3] Add the reviewed `catalog:remove` task in `mise.toml` and its `tools/catalog.py` command path, using the same ownership preflight and preserving feedback, unrelated skills, and non-bundle components.
- [X] T037 [US3] Complete direct skill package packaging and release-version alignment in `tools/catalog.py`, `controllers/flow-kit/manifest.yml`, and `bundles/spec-kit-flow/bundle.yml`; prepare `catalog/release.json` only from reviewed source coordinates and changed versions, without treating a development snapshot as a released catalog release.
- [X] T038 [US3] Exercise fresh catalog install, refresh, collision handling, edited-file protection, partial-failure reporting, and removal through the supported route in `tests/test_bundle_lifecycle.py`; record actual skill package and workflow IDs, versions, source digests, tested CLI, and preservation results in `specs/013-bundle-workflow-launchers/validation.md`. Verify documentation does not claim native Specify bundle commands install the controller skills.

**Checkpoint**: Supported lifecycle operations preserve consumer-owned state and match the pinned controller/workflow inventory. Unresolved native-path safety or project-context failures block release.

## Final Phase: Polish and Cross-Cutting Validation

**Purpose**: Make the new operator path understandable and verify the whole feature against its authority boundaries.

- [X] T039 Update `docs/installation.md`, `README.md`, and `workflows/README.md` with the eight FlowKit display names and corresponding `flow-kit-*` invocations, required workflow inputs, compatible Specify runtime preflight, concrete models, medium effort default, Luna/high overrides, named-step overrides, skills-mode setup, supported catalog install/refresh/remove route, clearly labeled disposable development-snapshot mode, native Specify bundle scope and its ignored effort metadata, manual fallback, and evidence limits.
- [X] T040 Compare `docs/installation.md`, `README.md`, and `workflows/README.md` against `controllers/flow-kit/manifest.yml` and the eight workflow input declarations; verify each document maps every workflow to the correct display name, `flow-kit-*` invocation, and required input, and verify `workflows/README.md` has one manual fallback for each; record the audit and any mismatches in `specs/013-bundle-workflow-launchers/validation.md` for SC-009.
- [X] T041 Run the focused controller, catalog, and lifecycle suites plus `specs/013-bundle-workflow-launchers/quickstart.md`, including live `gpt-6-luna`/high task-generation and implementation dispatch; review all eight manual-prompt paths in `workflows/README.md` for executable inputs, gates, and stop points, execute at least one path through a gate in a disposable consumer without native workflow dispatch, and record commands, versions, source coordinates, digests, observed results, and unrun checks in `specs/013-bundle-workflow-launchers/validation.md`.
- [X] T042 Compare the final `specs/013-bundle-workflow-launchers/spec.md`, `plan.md`, and `tasks.md` with the implementation and controller/lifecycle contracts; record any routine flow-back or unresolved authority, model-access, project-context, or ownership gate in `specs/013-bundle-workflow-launchers/validation.md` before claiming readiness.
- [X] T043 Review changed source and installation diffs with `git diff --check`, ensure no raw transcripts, secrets, or absolute host paths enter `controllers/flow-kit/`, `catalog/release.json`, or `specs/013-bundle-workflow-launchers/validation.md`, and prepare the release evidence for a separate operator publication decision.

## Dependencies and Execution Order

### Phase dependencies

1. Complete Setup T001–T003, then Foundational T004–T005.
2. US1 T006–T026 supplies the installed-definition runner and discoverable controllers needed by US2 and US3, then verifies live dispatch in the selected task.
3. US2 T027–T032 and US3 T033–T038 may proceed independently after US1. Each story's tests precede its implementation, and each has a separate consumer checkpoint.
4. Final validation T039–T043 follows the selected story increments. A failed model-access, human-interaction, or skill-ownership gate stops release under FR-015.

### Parallel opportunities

- T001 and T002 touch different fixture files and can proceed in parallel; T003 can inspect pinned tools independently.
- After T005, US1's tests T007 and T008 touch separate files, and the eight workflow-source edits T015–T022 touch separate packages. Finish the shared protocol and package manifest before testing direct skill behavior.
- After US1, US2's controller interaction work and US3's catalog/lifecycle work use different primary files; coordinate shared `tests/test_bundle_lifecycle.py` changes before merging them.
- T033 and T034 target separate test files; T039 documentation can proceed while focused implementation checks run, then be reconciled against actual behavior.

### Parallel example: User Story 1

After T009–T012 establish the shared contract, one implementer can edit `workflows/speckit-flow-clarify/workflow.yml` (T016) while another edits `workflows/speckit-flow-plan/workflow.yml` (T017). Separately, T013 and T014 create disjoint Codex skill directories. Review the package manifest and workflow pins in T023 before catalog work.

### Parallel example: User Story 2

After tests T027–T028, one implementer can update `controllers/flow-kit/controller-protocol.md` (T029) while another implements `controllers/flow-kit/scripts/python/recovery.py` (T030). Integrate both in `controller.py` at T031 before the live task scenario T032.

### Parallel example: User Story 3

T033 can specify lifecycle behavior in `tests/test_bundle_lifecycle.py` while T034 specifies release integrity in `tests/test_catalog.py`. Implement the shared ownership guard in T035, then the removal route T036; run T038 only after both paths are available.

## Implementation Strategy

**MVP**: Complete Setup, Foundation, and US1. Validate one controller in a disposable selected project and all eight installed names before advancing. This is a functional increment, not full Feature 013 acceptance: same-child interaction and safe lifecycle still require US2 and US3.

**Incremental delivery**: Add US2 to prove the desktop human interaction and recovery contract. Add US3 to align install, refresh, and removal with consumer ownership. Run final validation, preserve manual prompt paths, and present any unresolved release gate for an explicit operator decision. Do not commit, publish, launch another workflow phase, or infer roadmap or feature acceptance from checked tasks or passing automation.

## Phase 6: Convergence

- [X] T044 Reject empty or whitespace-only values for required workflow inputs before creating workflow state; add focused preflight tests for `feature_context=` and equivalent blank values per FR-004 (partial).
- [X] T045 Validate supported template expression forms throughout every possible workflow branch before starting any step, while retaining runtime resolution of prior-step output values; add a later-step unsupported-template regression test per plan: preflight and T005 (partial).
- [X] T046 Validate every path in the FlowKit skill ownership record as an expected, repository-contained package path before install, refresh, or removal can read, replace, or delete it; add a traversal regression test that preserves an outside consumer file per FR-012 (partial).
- [X] T047 Restrict persisted recovery blockers to bounded, non-sensitive codes or sanitized summaries and test that child transcript text and secret-bearing strings cannot enter `summary.json` per FR-019 (partial).
- [X] T048 Require clean, attributable source for the bundle manifest and all eight workflow definitions in a released catalog build, alongside the existing controller-source check; add a dirty-workflow and dirty-bundle regression test per plan: release gates and T037 (partial).
