# Implementation Plan: Named Agents for Delegated Steps

**Branch**: `develop` (feature directory `015-agent-roles-assignment-inheritance`) | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Revised Feature 015 draft, constitution 5.0.0, and the approved [roadmap amendment](contracts/roadmap-amendment.md).

## Summary

Every delegated workflow step explicitly names one Codex custom agent. A workflow-level default is not used. Main-task steps have no agent selection, and gates and switches stay in the main task. Codex's native agent files own instructions and optional model and reasoning settings; FlowKit has no role map. The controller validates every branch before work, and the supported Codex client shows launched children under task labels containing the intended agent name. Exact native agent requests and readiness probes establish selection separately from those labels. No run-time assignment override or additional approval gate is introduced.

[Research](research.md) confirms Specify preserves the proposed step metadata. Operator-provided Codex desktop screenshots demonstrate native `Coder` selection, instruction loading, inherited settings, and configured model/effort. Current Codex documentation supports direct app requests to spawn subagents and resolves native custom-agent identity from the TOML `name`; the controller procedure now uses that app orchestration path and stops if the native identity is not confirmed. CLI and generic child-tool probes did not load the selected custom agent; see [validation.md](validation.md). The [constitution amendment](contracts/constitution-amendment.md) and Feature 015 roadmap amendment are applied.

## Technical Context

**Language/Version**: Python 3.11.16 for existing controller source; workflow YAML schema 1.0; Specify CLI `1.0.10.dev0+pegagio.2`; Codex CLI 0.157.1 on the validation host

**Primary Dependencies**: Existing Specify loader and FlowKit controller; Codex native custom-agent discovery and exact named child dispatch; no new library or FlowKit assignment format

**Storage**: Reviewed workflow YAML; consumer-owned Codex custom-agent TOML in `.codex/agents/` or `~/.codex/agents/`; existing compact recovery summary. The catalog owns no Codex agent file.

**Testing**: Focused controller and lifecycle tests, Specify loader validation, and disposable-consumer probes for distinct named agents, main-task steps, native subagent visibility, human gates, and native-runner differences

**Target Platform**: Selected Codex desktop task in a compatible initialized consumer; macOS is the current validation host

**Constraints**: Four reviewed agent names; every delegated step names one; no workflow-level agent default, FlowKit role map, per-run assignment override, or silent fallback; all-branch preflight; main-task review gates

**Scale/Scope**: Eight existing workflow packages, four reviewed agent names, all possible delegated branches in one invocation

## Constitution Check

**Governance, source migration, and the planned live boundaries have been validated.** Constitution II requires a reviewed Codex agent name on every explicitly delegated step and bars per-run assignment overrides. The approved Feature 015 roadmap entry uses native Codex UI visibility. The controller preflight, workflow metadata, launch procedure, and lifecycle boundaries are implemented. The two-consumer dispatch, same-child continuation, and native availability stops are recorded in [validation.md](validation.md).

Constitution III keeps generic source independent of The Diagram. Constitution IV requires reviewed workflow YAML, separate planning and task generation, and manual fallback. Constitution V requires disposable-consumer evidence with exact component and runtime coordinates. Specify loader acceptance is not proof that the controller can select a Codex custom agent.

**Post-design gate.** The controller validates the reviewed names and documents Codex's native named-agent request while preserving main-task boundaries. The supported Codex desktop evidence verifies `Coder` selection, and the two-consumer runs verify Architect and Verifier selection with native UI visibility. The exposed controller child tool and CLI did not confirm exact custom-agent selection; those limits remain documented in [validation.md](validation.md).

## Project Structure

The design stays within the existing workflow and controller architecture.

```text
specs/015-agent-roles-assignment-inheritance/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── assignment.md
│   ├── constitution-amendment.md
│   └── roadmap-amendment.md
├── quickstart.md
└── tasks.md                 # Created only by the later tasks phase
```

Implementation targets, after governance approval, are the eight `workflows/speckit-flow-*/workflow.yml` packages, `controllers/flow-kit/controller-protocol.md`, the controller helper and skill instructions, focused tests, and user documentation. The catalog needs only a regression check that it does not own or alter Codex agent files.

## Complexity Tracking

An explicit delegation marker remains necessary because Feature 013's concrete `model` field previously meant both “choose a model” and “launch a child.” An agent name alone must not turn a main-task node or human gate into a child. Native custom agents remove the proposed JSON role map and its schema, parser, ownership, and drift costs. Two-consumer native selection, same-child continuation, and negative preflight behavior are recorded in [validation.md](validation.md).
