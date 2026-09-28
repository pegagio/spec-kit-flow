# Implementation Plan: FlowKit Codex Workflow Controllers

**Branch**: `013-bundle-workflow-launchers` (feature identifier; current checkout is `develop`) | **Date**: 2026-09-26 | **Spec**: [spec.md](spec.md)

**Input**: Clarified Feature 013 specification and constitution 4.0.0.

## Summary

Package eight explicit Codex controller skills as reviewed FlowKit source. The supported FlowKit catalog route installs them alongside the Specify workflow bundle. Each has a stable `flow-kit-{purpose}` invocation name and the fixed skill picker display name in the [controller contract](contracts/controller.md). Each thin skill names one workflow and uses a shared controller protocol to load the installed, composed workflow definition. The main Codex task handles unmodeled steps, questions, gates, progress, and recovery evidence; concrete step-level `model` declarations dispatch bounded child tasks with an effective reasoning effort. The controller validates all possible modeled steps and inputs before execution, then interprets the four step types used by the current workflows without invoking native `specify workflow run`, whose Codex integration creates separate CLI sessions.

## Technical Context

**Language/Version**: Python 3.11; YAML workflow schema 1.0; pinned Specify CLI `1.0.10.dev0+pegagio.2`; Codex skills mode

**Primary Dependencies**: Existing Specify bundle and workflow composition paths; an accessible compatible Specify runtime in the consumer; current Codex skill format and desktop child-task tools; FlowKit catalog

**Storage**: Versioned workflow YAML and direct Codex skill source; existing bundle and release records plus a FlowKit skill ownership record; compact consumer-local stopped-run record without child transcripts

**Testing**: Focused controller and catalog tests, Specify schema validation, disposable initialized Codex consumers, live US1 desktop model-effort dispatch and same-child clarification, and a source-to-documentation audit of all eight controller names, invocations, required inputs, and manual fallbacks

**Target Platform**: Selected Codex desktop project task in a compatible initialized consumer; macOS is the current validation host

**Project Type**: Versioned workflow bundle plus a Codex skill package and local controller helper

**Performance Goals**: Show assignments and finish preflight before the first workflow step; no background scheduler or service

**Constraints**: No silent model or effort fallback or cross-phase launch; no duplicated workflow prompts or gates in skills; preserve manual fallback and consumer-owned files; stop on a missing compatible Specify runtime, unsupported step type, uncertain model-effort access, changed installation record, or unsafe skill ownership state

**Scale/Scope**: Eight fixed workflow IDs and their current `prompt`, `command`, `gate`, and `switch` nodes; one operator-selected consumer project and one workflow invocation at a time

## Constitution Check

**Pre-research gate — pass for planning.** The operator chooses the workflow and scope. Reviewed workflow YAML, not a skill copy, owns prompts, step models, FlowKit effort overrides, branches, and gates. The controller presents assignments, questions, and consequential decisions in the main task; it never grants roadmap, Git, or feature acceptance. Direct Codex skills are versioned FlowKit source delivered by the supported catalog route alongside the Specify bundle; no Specify extension commands are added. The existing eight manual paths remain usable. Validation must identify tested Specify and Codex coordinates and distinguish stub routing from live interaction. No new framework, dependency, or build tool is proposed.

**Release gates.** Specify currently accepts step-level model strings but does not reject empty strings or verify account availability. Its bundle manifest has no direct skill component, so native `specify bundle` commands alone cannot deliver these controllers. The supported FlowKit catalog route must install the reviewed skill package, preserve its `flow-kit-*` IDs and `interface.display_name` values, report ownership conflicts, and preserve modified local skills. The controller must prove access to the compatible Specify workflow loader in the selected consumer before any workflow step. Model-effort preflight must fail closed. If the catalog route or runtime bridge cannot deliver those guarantees or selected-project interaction, stop for operator resolution under FR-015; do not ship a degraded controller or claim native bundle commands install the skills.

**Post-design gate — pass with release gates retained.** The [research](research.md), [data model](data-model.md), [controller contract](contracts/controller.md), [lifecycle contract](contracts/lifecycle.md), and [quickstart](quickstart.md) keep workflow semantics in installed YAML, make stop states explicit, and require end-to-end consumer evidence before compatibility claims. No constitutional exception is proposed.

## Reviewed Step Model Assignments

These are the initial concrete, potentially non-portable assignments to write into individual executable steps. The FlowKit controller uses `medium` reasoning effort for each modeled step unless the step declares `reasoning_effort` or the operator overrides that named step. The two Luna steps declare `high`; all Sol and Astra steps use `medium`. This is FlowKit controller metadata: the tested Specify loader preserves it, but native `specify workflow run` does not apply it. The selected consumer task must probe every effective model-effort pair before any workflow step, including assignments in branches that will not run. All unlisted prompt and command steps remain in the main task; gate and switch nodes never declare a model or effort. Do not set a workflow-level model or effort default or substitute model-role labels in Feature 013.

| Workflow | `gpt-6-sol` / medium step IDs | `gpt-6-luna` / high step IDs | `gpt-6-astra` / medium step IDs |
| --- | --- | --- | --- |
| start-feature | `assess-eligibility`, `draft-specification`, `brief-against-roadmap` | — | — |
| clarify | `clarify-specification` | — | — |
| plan | `return-to-clarification` | — | `create-plan` |
| tasks | `return-to-plan` | `generate-tasks` | — |
| analyze-remediate | all `remediate-*` and `retask-*` commands | — | `analyze-artifacts`, all `reanalyze-*` and `replan-*` commands |
| implement | all `return-to-*` commands | `implement-eligible-work` | — |
| converge | `return-remediation-to-analysis` | — | `assess-convergence` |
| closeout | `debrief-roadmap`, `ingest-curated-context`, `lint-wiki` | — | — |

Review the complete eight-workflow diff and its version bumps before release. A model or effort rejected by the selected account stops the run for operator resolution; the assignment is not silently changed.

## Refresh Boundary

Capture the composed workflow digest and fingerprints of both `.specify/bundle-records.json` and the FlowKit catalog skill ownership record when preflight succeeds. Fingerprints include content digest and filesystem device/inode identity. The Specify bundle record detects workflow bundle changes; the FlowKit record detects a skill-only catalog refresh even when workflow bytes remain the same. Compare all three before each new step and after an active child returns. Any change causes a conservative stop at that boundary, including a change made by another bundle. Preserve the original workflow version, effective assignments, project edits, and completed-step evidence in the local summary. A preflight rejection creates no run record.

## Runtime and Development Installation

Maintainer skill validation uses the configured skill-tools Python. A consumer does not need that private development environment: a portable shell bootstrap in the installed controller package must locate the selected `specify` executable, identify its compatible Python runtime without a hard-coded host path, verify its version against the installed FlowKit release, and use that runtime for the controller's bounded read-only `WorkflowEngine(project_root).load_workflow(id)` call. Only the composed definition and provenance return to the main task. Missing or ambiguous executables, version mismatch, loader failure, or an unsafe runtime stop before workflow work or recovery-record creation. Exercise both a mise-selected executable and an ordinary installed executable in disposable consumers; do not add Specify's dependencies to the skill-tools environment.

For a workflow `command` node, resolve its rendered `integration` and command ID through the selected consumer's installed Codex skill inventory using the pinned Specify command-to-skill naming rule. Verify the skill directory, `SKILL.md` name, and installed command provenance where available before passing the node's rendered arguments to that skill. An unmodeled command is invoked in the main task; a modeled command is invoked by the bounded child in the same selected project. A missing, ambiguous, mismatched, or inaccessible command skill stops at that node with preserved evidence. Live validation must prove that a child can invoke the installed command skill and that the controller does not substitute a copied command prompt or `specify workflow run`.

The existing catalog installer rejects snapshot releases. For live pre-release validation, add an explicit development-snapshot mode for both install and refresh through the same catalog route, restricted to disposable initialized consumers and visibly labeled as a snapshot. Snapshot build may package the current uncommitted controller and workflow source, but must record source digests and dirty working-tree status rather than misrepresent it as a release commit. Both operations must exercise the same package, ownership preflight, and postconditions as released installation without publishing or claiming a release. The normal install and refresh commands must continue to reject snapshots and keep their clean-source release gates.

## Project Structure

### Documentation (this feature)

```text
specs/013-bundle-workflow-launchers/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── controller.md
│   └── lifecycle.md
├── quickstart.md
└── validation.md        # Implementation evidence, created during task execution
```

`tasks.md` belongs to the separate task-generation phase.

### Source Code (repository root)

```text
workflows/speckit-flow-*/workflow.yml       # Reviewed concrete per-step model and effort declarations
controllers/flow-kit/manifest.yml             # Version and eight skill-to-workflow bindings
controllers/flow-kit/skills/flow-kit-*/        # Thin Codex SKILL.md and agents/openai.yaml files
controllers/flow-kit/scripts/bootstrap.sh       # Locate selected Specify runtime without a private skill-tools dependency
controllers/flow-kit/scripts/python/           # Shared installed-definition inspection and record support
bundles/spec-kit-flow/bundle.yml               # Existing Specify workflow and extension pins
tools/catalog.py                               # Catalog skill packaging, install, refresh, remove, ownership checks
catalog/release.json                          # Generated release provenance after source review
mise.toml                                     # Supported removal task beside install/refresh
tests/test_catalog.py
tests/test_bundle_lifecycle.py
tests/test_controller.py                     # Focused graph and record behavior
docs/installation.md
workflows/README.md
```

**Structure Decision**: Keep the eight Codex skills as direct, reviewed source and use the FlowKit catalog route to install them alongside the Specify bundle. A controller package manifest pins the eight skill IDs, display names, and workflow bindings; release metadata records its version and source digest. The catalog route owns skill installation, refresh, removal, and ownership checks, while Specify continues to own the workflow bundle. At initial installation, write and verify the skill ownership record before a skill can run; refresh atomically replaces it after verifying new files. Successful removal verifies that owned skills and shared helper are gone, then removes the ownership record, while preserving separate workflow recovery summaries. Install the shared helper and protocol at `.specify/flow-kit/` and have each thin skill invoke that project-relative location. Put shared graph inspection, preflight, and record formatting in one controller helper. The desktop main task owns child-task orchestration; the helper must not invoke `specify workflow run` or copy YAML prompts into skill instructions. Reject any step type or template form the controller cannot faithfully execute. Native Specify bundle commands remain workflow and extension operations and are not advertised as a complete controller installation path.

## Complexity Tracking

No constitutional violation is planned. The current Specify bundle manifest has no direct skill component type. The supported FlowKit catalog route will version and install the direct Codex package alongside that bundle, keeping the Specify workflow IDs and extension namespace intact.
