# Tasks: Named Agents for Delegated Steps

**Input**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [data-model.md](data-model.md), [assignment contract](contracts/assignment.md), and [quickstart.md](quickstart.md)

**Tests**: Required by FR-012. Write behavior tests before changing the behavior they cover and confirm the expected failure. Ownership regression tests may already pass; preserve those results as a baseline.

**Scope**: Feature 015 depends on Feature 013, not Feature 014. The constitution, Feature 015 roadmap amendment, and separately approved roadmap vision/C-02 corrections are applied. Codex desktop named-agent selection is observed; source migration and controller protocol are implemented, while live integrated dispatch validation remains. No task authorizes a later workflow phase, roadmap transition, Git integration, or feature acceptance.

**Eight workflow files**: `workflows/speckit-flow-analyze-remediate/workflow.yml`, `workflows/speckit-flow-clarify/workflow.yml`, `workflows/speckit-flow-closeout/workflow.yml`, `workflows/speckit-flow-converge/workflow.yml`, `workflows/speckit-flow-implement/workflow.yml`, `workflows/speckit-flow-plan/workflow.yml`, `workflows/speckit-flow-start-feature/workflow.yml`, and `workflows/speckit-flow-tasks/workflow.yml`.

**Eight controller skills**: `controllers/flow-kit/skills/flow-kit-analyze-remediate/SKILL.md`, `controllers/flow-kit/skills/flow-kit-clarify/SKILL.md`, `controllers/flow-kit/skills/flow-kit-closeout/SKILL.md`, `controllers/flow-kit/skills/flow-kit-converge/SKILL.md`, `controllers/flow-kit/skills/flow-kit-implement/SKILL.md`, `controllers/flow-kit/skills/flow-kit-plan/SKILL.md`, `controllers/flow-kit/skills/flow-kit-start-feature/SKILL.md`, and `controllers/flow-kit/skills/flow-kit-tasks/SKILL.md`.

## Phase 1: Setup

**Purpose**: Establish a reproducible Feature 013 baseline and validation record without changing source behavior.

- [X] T001 Verify the approved constitution 5.0.0 amendment in `.specify/memory/constitution.md` against `specs/015-agent-roles-assignment-inheritance/contracts/constitution-amendment.md`, then record that FR-013 gate, eight workflow package versions and source digests, controller/catalog digests, Codex version, Specify version, and baseline focused test results in `specs/015-agent-roles-assignment-inheritance/validation.md`; exclude absolute host paths and secrets.
- [X] T002 [P] Add disposable-consumer native-agent fixtures for Coder, Verifier, and Architect under `tests/consumer-fixtures/named-agents/consumer-a/.codex/agents/` and `consumer-b/.codex/agents/`; use distinct benign instructions across consumers and omit optional model/effort in at least one file.

## Phase 2: Foundational Prerequisites

**Purpose**: Resolve governance and prove exact native dispatch before modifying workflow or controller source.

**Checkpoint**: Do not begin User Story source changes until T003–T005 are complete. A generic child named after an agent does not satisfy T004.

- [X] T003 Present the exact replacement in `specs/015-agent-roles-assignment-inheritance/contracts/roadmap-amendment.md` for operator review; after explicit approval and operator-directed roadmap workflow invocation, reconcile `.specify/memory/roadmap.md` while preserving Feature 014 and verified history. Stop source work if approval is deferred.
- [X] T004 Demonstrate that the supported Codex desktop can launch a bounded child by exact native custom-agent `name` with its distinctive instructions loaded; record the operator-provided screenshots, observed results, and limits in `specs/015-agent-roles-assignment-inheritance/validation.md`. The operator accepted the desktop screenshots as sufficient evidence; desktop version and exact launch action were not captured. A separate in-session tool probe returned `NOT_CONFIRMED` and remains a limitation of that tool path.
- [X] T005 Define the native named-dispatch request, bounded no-work probe, and native subagent visibility procedure in `controllers/flow-kit/controller-protocol.md`, grounded in the accepted Codex desktop evidence; do not implement a TOML parser, FlowKit role map, generic-child substitute, or per-run override.

## Phase 3: User Story 1 — Use a Named Agent for Each Delegated Step (P1) 🎯 MVP

**Goal**: Every delegated executable step carries its own reviewed Codex agent name and launches that exact native agent.

**Independent Test**: Install identical reviewed workflow bytes in two disposable consumers with different native agent configurations. Confirm the Analyze and Remediate workflow's Architect and Verifier assignments, verify Verifier's delegated work child loads the consumer's instructions, and inspect Codex's native subagent visibility and optional model/effort display. The separate T004 desktop probe covers Coder.

### Tests

- [X] T006 [P] [US1] Add controller tests in `tests/test_controller.py` for exact per-step `Coder`/`Verifier` selection, distinct child identities, and no per-run agent/model/effort override. Verify native subagent visibility and optional model/effort display in the live T012 scenario instead of mirroring Codex UI behavior in a controller unit test.
- [X] T007 [P] [US1] Add failing loader checks in `tests/test_catalog.py` for preserved `flow_kit.delegated: true` and exact `flow_kit.agent` metadata, fixed Architect/Builder/Coder/Verifier names, and migrated versions across the eight workflow files listed above.

### Implementation

- [X] T008 [US1] Implement `StepAssignmentIntent` selection in `controllers/flow-kit/scripts/python/controller.py`: each delegated `prompt` or `command` uses its own reviewed `flow_kit.agent`; remove concrete step-model dispatch and reject invocation-level agent/model/effort overrides.
- [X] T009 [US1] Specify exact named-agent no-work probe and bounded work-child dispatch in `controllers/flow-kit/controller-protocol.md`, using the verified T004 surface and preserving same-child interactive continuation; update the eight controller skills listed above only for bootstrap and protocol references, without copying workflow prompts or gates into them.
- [X] T010 [US1] Document native Codex subagent activity and child-pane identity in `controllers/flow-kit/controller-protocol.md` as the launch visibility surface; require no separate FlowKit message or approval gate.
- [X] T011 [US1] Replace delegated concrete `model` fields with explicit `flow_kit.delegated: true` and reviewed per-step `flow_kit.agent` in the eight workflow files listed above; preserve IDs, prompts, branches, gates, and separate phases, and bump changed package versions and `bundles/spec-kit-flow/bundle.yml` pins, starting with `workflows/speckit-flow-tasks/workflow.yml`.
- [X] T012 [US1] Run the two-consumer named-agent and native UI visibility scenario from `specs/015-agent-roles-assignment-inheritance/quickstart.md`; record workflow digests, component versions, native instruction evidence, optional setting behavior, and limits in `specs/015-agent-roles-assignment-inheritance/validation.md`. Consumer A and B showed named probes and work children; the marker-only Verifier fixtures stopped at `step-failed` as designed.

## Phase 4: User Story 2 — Keep Main-Task Work in the Main Task (P2)

**Goal**: An agent name selects a child only when the executable step explicitly declares delegation; main-task work, gates, and switches stay with the driving agent.

**Independent Test**: Run a main-task prompt, two delegated prompts with different names, and a human gate. Confirm only delegated prompts launch children, while the main task handles the prompt, switch, gate, and answers to an interactive child.

### Tests

- [X] T013 [US2] Add boundary and continuation tests in `tests/test_controller.py` for main-task executable steps, nondelegated agent placement, gate/switch delegation rejection, answers returned to the same active child, and no child launch for main-task work.

### Implementation

- [X] T014 [US2] Separate explicit delegation from main-task execution in `controllers/flow-kit/scripts/python/controller.py`; reject an agent on a nondelegated step and delegation on a gate or switch, without inferring child dispatch from an agent name alone.
- [X] T015 [US2] Update `controllers/flow-kit/controller-protocol.md` and the eight controller skills listed above, starting with `controllers/flow-kit/skills/flow-kit-tasks/SKILL.md`, to keep main-task prompts, switches, questions, review gates, recovery decisions, and later-phase invocation with the driving agent; keep workflow prompts and gate text in installed YAML.
- [X] T016 [US2] Run the mixed main-task/delegated/gate scenario and interactive continuation in a disposable consumer; record child count and main-task ownership in `specs/015-agent-roles-assignment-inheritance/validation.md`.

## Phase 5: User Story 3 — Diagnose Agent Availability (P3)

**Goal**: Validate every possible delegated branch and stop before workflow work when a named agent cannot launch, without substitution or a preflight recovery record.

**Independent Test**: In disposable consumers, make a delegated agent absent, misspelled, malformed, or unavailable on taken and untaken branches. Each case identifies step ID, agent name, and reason before work; refresh/removal leaves consumer files unchanged.

### Tests

- [X] T017 [P] [US3] Add failing all-branch preflight tests in `tests/test_controller.py` for missing name, unknown reviewed name, case mismatch, workflow-level default, delegated legacy concrete `model`, malformed metadata, and invalid untaken branch; assert no workflow state, recovery record, or fallback. Native agent unavailability is checked by the dispatch probe.
- [X] T018 [P] [US3] Add ownership regression tests in `tests/test_bundle_lifecycle.py` for install, refresh, and remove with consumer `.codex/agents/` files present and byte-for-byte unchanged; record whether the existing catalog already passes.

### Implementation

- [X] T019 [US3] Validate full installed graph and `StepAssignmentIntent` rows before work in `controllers/flow-kit/scripts/python/controller.py`: unique IDs, metadata placement, explicit agent on every delegated executable, exact reviewed names, no workflow default, and specific migration error for delegated legacy `model`.
- [X] T020 [US3] Implement every-selected-agent bounded preflight and dispatch-time unavailable-agent handling in `controllers/flow-kit/controller-protocol.md` and `controllers/flow-kit/scripts/python/controller.py`; preflight failures create no run/recovery record, while later failures preserve completed-step evidence through `controllers/flow-kit/scripts/python/recovery.py`.
- [X] T021 [US3] Verify `tools/catalog.py` leaves consumer Codex agent files untouched during install, refresh, and remove, correcting only a proven violation; run `tests/test_bundle_lifecycle.py` and record byte-level results in `specs/015-agent-roles-assignment-inheritance/validation.md`. The four-test lifecycle suite passed.
- [X] T022 [US3] Run missing, malformed, unavailable, case-mismatched, untaken-branch, legacy-model, and changed-during-run scenarios from `specs/015-agent-roles-assignment-inheritance/quickstart.md`; record Codex edit behavior and stop boundaries in `specs/015-agent-roles-assignment-inheritance/validation.md` without adding a watcher.

## Phase 6: Polish and Cross-Cutting Validation

**Purpose**: Document supported behavior and verify the complete feature boundary.

- [X] T023 Validate all eight updated workflows through the supported Specify loader and separately run native `specify workflow run` in a disposable initialized consumer; record exact Specify/Codex versions, observed differences, and limits in `specs/015-agent-roles-assignment-inheritance/validation.md`. The native attempt reached a Codex stop prompt but failed on the disposable checkout trust check before a delegated step.
- [X] T024 Update `docs/installation.md` and `workflows/README.md` with custom-agent TOML and per-step YAML examples, consumer ownership, manual-prompt path, main-task boundary, and the T023 observed native `specify workflow run` differences; do not claim parity from loader acceptance.
- [X] T025 Run focused controller, catalog, and bundle-lifecycle tests plus the repository's relevant validation command; record commands, results, source digests, and limits in `specs/015-agent-roles-assignment-inheritance/validation.md` and compare outcomes with FR-001–FR-013 and SC-001–SC-007 in `specs/015-agent-roles-assignment-inheritance/spec.md`.

## Dependencies and Execution Order

```text
T001–T002 → T003 roadmap gate → T004 desktop dispatch proof → T005 procedure
           → US1 (T006–T012) → US2 (T013–T016) → US3 (T017–T022) → T023–T025
```

T004–T005, T012, and the C-02 roadmap correction are complete. Within each story, write behavior tests first and confirm expected failures before implementation; an already passing ownership regression establishes a baseline. US2 and US3 can start after T005 if contributors avoid simultaneous edits to shared controller, test, and protocol files; the preferred single-contributor order is US1 → US2 → US3. T016 and T022 remain independent story checkpoints, not operator acceptance.

## Parallel Examples

These pairs touch different files and have no dependency on each other after their phase prerequisites:

- **Setup**: T001 writes `validation.md` while T002 creates `tests/consumer-fixtures/named-agents/`.
- **US1**: T006 writes `tests/test_controller.py` while T007 writes `tests/test_catalog.py`.
- **US2**: T013–T016 share controller/protocol files, so execute them in order.
- **US3**: T017 writes `tests/test_controller.py` while T018 writes `tests/test_bundle_lifecycle.py`.

## Implementation Strategy

Complete Setup and Foundational gates, then deliver US1 as a demonstrable MVP slice and run its two-consumer independent test. It is not release-ready until US2, US3, and cross-cutting validation pass. Add the main-task boundary in US2, then all-branch diagnostics and lifecycle protection in US3. Finish with documentation, native Specify comparison, and full recorded validation. If exact native named-agent dispatch is unavailable, record the evidence and stop for an operator runtime or scope decision; a generic child is not an implementation of Feature 015.

## Phase 7: Convergence

- [X] T026 CRITICAL Reconcile the current controller-protocol source digest, final T016/T022 outcomes, and remaining validation limits in `specs/015-agent-roles-assignment-inheritance/validation.md` and `plan.md` per Constitution V and FR-012 (partial).
- [X] T027 Require the reviewed agent name in each probe and workflow-child activity label in `controllers/flow-kit/controller-protocol.md`, update the operator documentation, and verify the visible naming without treating the label as proof of native selection per FR-007 and SC-002 (partial).

## Phase 8: Convergence

- [X] T028 CRITICAL Bump the changed controller package and bundle source versions in `controllers/flow-kit/manifest.yml` and `bundles/spec-kit-flow/bundle.yml`, then reconcile source-versus-checked-in-release wording and final provenance without rewriting the historical `catalog/release.json` per Constitution III and plan: versioned components (partial).

## Phase 9: Convergence

- [X] T029 HIGH Refresh the malformed-agent and unsupported-model disposable consumers from current source, rerun their native preflight failures, and record whether each final diagnostic names the affected step ID and observed reason without workflow work or a run record per FR-006 and SC-004 (partial).
