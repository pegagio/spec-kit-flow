# Implementation Plan: FlowKit Workflow Improvements

**Branch**: `develop` (feature directory `014-flowkit-workflow-improvements`) | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Clarified F014 specification, approved Constitution 6.0.0, [workflow review baseline](workflow-review-baseline.md), current eight source workflow packages, the operator's five clarification answers, and the operator-approved all-eight-workflow roadmap amendment.

## Contents

The main sections describe the selected runtime approach, authority checks, source layout, and work sequence.

- [Summary](#summary)
- [Technical Context](#technical-context)
- [Loop Entry and Progress](#loop-entry-and-progress)
- [Constitution Check](#constitution-check)
- [Project Structure](#project-structure)
- [Design Sequence](#design-sequence)

## Summary

Review all eight FlowKit workflows branch by branch, then make each invoked workflow reach its own evidenced success, required human decision, or bounded stop. Use the pinned Specify `do-while` step for explicit in-workflow continuation, extend the direct Codex controller to validate and execute that shape with iteration-aware recovery, and replace routine classification gates with a small validated outcome contract. Preserve separate operator invocation of the next workflow, exact approval gates, and manual fallback. Review every delegated step against Feature 015's native agent design and supply usable repository-local configurations for selected names. The recorded F014 Start, Clarify, Plan, Tasks, Converge, and Close Out issues become acceptance cases for this complete-workflow review.

[Research](research.md) resolves the loop representation, progress rule, recovery boundary, and agent-file ownership. [Data model](data-model.md) defines the loop, pass, outcome, progress, gate, assignment, and run evidence. The [continuation contract](contracts/workflow-continuation.md) and [agent contract](contracts/agent-assignment.md) make the runtime interfaces reviewable. The constitutional amendment is approved; this plan does not change workflow source.

## Technical Context

**Language/Version**: Existing Python 3.11 controller and tests; Specify workflow YAML schema 1.0; selected Specify CLI `1.0.10.dev0+pegagio.2`; native Codex custom-agent TOML.

**Primary Dependencies**: Existing Specify workflow loader with built-in `do-while`; FlowKit's shared controller helper/protocol and direct Codex skills; native Codex named-agent selection. No new framework, library, service, or build tool.

**Storage**: Reviewed workflow YAML, repository-local `.codex/agents/*.toml`, and existing compact consumer-local run summaries under `.specify/flow-controllers/runs/`. No database or new bundle-owned agent storage.

**Testing**: Automated controller, catalog, and lifecycle tests; graph, outcome, and manual-fallback fixtures for all eight packages; Specify loader checks; scripted disposable-consumer snapshot install/refresh/remove; and machine-recorded native Codex named-agent selection where the client exposes it. The validation run must report skipped or unobservable checks. After those checks, the operator may perform one or two narrowly specified Codex desktop experience checks to confirm the visible workflow and agent behavior.

**Target Platform**: Codex desktop task in a compatible initialized consumer; this macOS checkout is the source repository and a dogfood consumer. Other clients and native Specify named-agent parity remain unverified until separately tested.

**Project Type**: Versioned workflow packages, shared Codex controller package, local catalog installer, and consumer-owned agent configuration.

**Performance Goals**: Complete static graph, assignment, and compatibility preflight before the first workflow work step. Each correction loop has at most five correction passes per invocation and stops sooner on no progress or a consequential decision. No background processing or unattended retry.

**Constraints**: Human-directed workflow scope and exact consequential gates; no nested FlowKit workflow invocation or automatic next phase; no command-success-as-clean shortcut; five-question Clarify command cap per session; independently reviewable workflow packages and manual fallback; portable evidence without raw transcripts or absolute paths.

**Scale/Scope**: Eight existing workflow IDs, all possible branches and delegated assignments, one selected feature/workflow invocation at a time, and up to five correction passes for each reviewed corrective loop.

## Loop Entry and Progress

A corrective loop may assess before entry or begin with a command that safely checks for work. Analyze and Remediate declares `assessment_only_first_pass: true`: its first body pass skips every correction, runs fresh task analysis, and establishes a read-only baseline through its shared assessment. Later passes enter its shared specification → plan → tasks waterfall, then run the same analyzer and assessment. Six total passes allow one baseline and at most five corrections.

Converge declares `assessment_before_correction: true`. Every pass starts with `speckit.converge`, then one assessment classifies that fresh report and checks progress before a guarded correction branch. The first report establishes the baseline; later reports verify the preceding implementation. Corrections use the shared waterfall, fresh task analysis, eligibility verification, and implementation, then return directly to the source command. Six command/assessment passes permit five corrections and a final confirmation. Intermediate eligibility or implementation blockers stop before another pass. Other reviewed loops retain five body passes.

A `complete` assessment ends successfully. `needs-human` reaches a declared main-task gate when present, otherwise reports the exact required operator decision and stops; `blocked` reports its resumption action. Only validated `continue` permits another pass. Every correction must resolve a prior finding or eligible task against the preceding assessment. No progress, repeated unresolved findings, stale evidence, failed prerequisites, or an untrustworthy outcome stops continuation. A still-`continue` outcome on the final allowed pass is cap exhaustion, never success. Implement records unfinished tasks before the loop and repeats core-skill sessions only while eligible work remains and a prior task was completed.

| Workflow | Initial and refreshed evidence | Confirmed progress within one invocation |
|---|---|---|
| Start Feature | Read-only candidate inventory and dependency chains, explicit operator selection, cited context before approval, exact selected roadmap entry and approved patch, created spec directory, exact `Spec dir` value, and one shared uniquely matched brief result. | An approved linkage correction removes a prior missing/stale mapping finding and a refreshed brief resolves the selected spec uniquely. Exact transition and linkage patch decisions remain main-task gates; deferred, blocked, and ready outcomes use one final report. |
| Clarify | Significant ambiguity IDs tied to current spec passages and the answers incorporated after each bounded session. | At least one prior significant ambiguity ID is resolved in the current spec; a newly discovered question does not turn an unchanged earlier ambiguity into progress. The five-question limit remains per session. |
| Plan | Initial missing file/placeholder section IDs, then current required outputs after each `speckit.plan` pass. | A prior output gap is populated; exact remaining gaps feed the next planning request. The output check does not review design quality and stops on no progress or the five-pass bound. |
| Tasks | Initial task output/coverage gap IDs, then tasks.md and reviewed design after each core-skill pass. | A prior format, section, or coverage gap is filled; exact remaining gaps feed the next task request. Preserve task history and stop on no progress or the five-pass bound. |
| Analyze and Remediate | One shared `speckit.analyze` command and `assess-analysis` step establish the initial read-only baseline and assess every shared-waterfall correction. | Fresh analysis confirms a prior finding resolved after ordered artifact reconciliation; a changed digest alone is insufficient. |
| Implement | Initial unfinished eligible task IDs, then task and validation evidence after each `speckit.implement` session. | A previously unfinished eligible task is completed, and a fresh assessment confirms specific eligible tasks remain for another session; no task progress or the fifth still-incomplete pass causes a bounded stop. |
| Converge | Fresh `speckit.converge` report and shared assessment at the start of every pass; waterfall reconciliation, analysis, eligibility, and implementation follow only when continuation is permitted. | Fresh convergence evidence confirms a prior gap resolved after changed tasks pass analysis and eligible implementation; command success alone is insufficient. |
| Close Out | Completion state, current debrief finding IDs, wiki and roadmap evidence where applicable. | A prior routine debrief finding is resolved in refreshed evidence or the evidenced Draft-to-Complete transition succeeds; exact roadmap verification remains a main-task gate. |

All finding and task IDs are scoped to the selected workflow and feature. When a source command cannot provide stable IDs directly, a reviewed assessment step derives them from inspectable current artifacts; inability to establish a trustworthy comparison stops the loop.

## Constitution Check

**Pre-research gate — authority resolved.** Principle I requires accepted discoveries to flow through F014's spec, plan, tasks, and eventual implementation. Approved Constitution 6.0.0 permits declared, bounded core-command correction and reassessment within the selected workflow and scope, including Converge's analysis and implementation, while forbidding another FlowKit workflow or undeclared later phase. The operator explicitly selected F014's repeated Clarify-session policy and Close Out completion rule in the specification clarification session. Feature 014 changes future behavior without rewriting verified Feature 007/008 history. Substantive answers and consequential decisions remain human gates.

**Roadmap scope gate — resolved.** The operator approved the exact all-eight-workflow and repository-local-agent amendment, which is recorded in `.specify/memory/roadmap.md` and `validation/authority-decisions.md`. F014 implementation may now proceed within that approved scope. Verified feature history remains unchanged.

**Source and validation gates.** Constitution III keeps generic source independent of The Diagram and bundle-owned behavior in reviewed packages. Principle IV requires distinct planning/task phases, installed workflow authority, and manual fallback; the built-in Specify step avoids a new dependency. Principle V requires disposable-consumer evidence with component IDs, versions, digests, tested CLI coordinates, and limits. Automated checks collect that evidence and report coverage and limits. A no-op dispatch or successful loader validation will not be described as live-agent behavior or publication.

**Post-design gate — passed for implementation.** The research and contracts preserve the approved authority boundary, and the exact expanded roadmap amendment is recorded as approved. If the selected Specify runtime or direct controller cannot support the validated loop contract, stop and revise this plan rather than hide continuation in prompt text or silently degrade behavior.

## Project Structure

The design stays in the existing workflow, controller, test, and documentation layout.

### Documentation (this feature)

```text
specs/014-flowkit-workflow-improvements/
├── spec.md
├── checklists/requirements.md
├── workflow-review-baseline.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/
│   ├── workflow-continuation.md
│   └── agent-assignment.md
├── quickstart.md
├── roadmap-reviews/
└── tasks.md
```

### Source Code (repository root)

```text
workflows/speckit-flow-*/workflow.yml          # Eight independently reviewed behavior graphs
bundles/spec-kit-flow/bundle.yml                # Composed versions for changed workflow packages
controllers/flow-kit/controller-protocol.md    # Main-task execution, gates, loops, and stops
controllers/flow-kit/manifest.yml               # Changed controller package version and compatibility
controllers/flow-kit/scripts/python/
├── controller.py                              # Graph/preflight/outcome support
└── recovery.py                                # Iteration-aware portable run evidence
controllers/flow-kit/skills/flow-kit-*/SKILL.md # Thin direct controller entry points
.codex/agents/*.toml                           # This repository's native consumer agents
tests/test_controller.py
tests/test_catalog.py
tests/test_bundle_lifecycle.py
tests/test_workflow_paths.py
tests/test_workflow_graph.py
tests/test_agent_configs.py
tests/test_snapshot_validation.py
tests/consumer-fixtures/
tools/validate_workflows.py
docs/installation.md
workflows/README.md
```

**Structure Decision**: Keep each workflow's prompts, branches, gates, loop condition, and cap in its versioned YAML. Put generic graph validation, outcome-envelope checking, progress comparison, and iteration-aware recovery in the shared controller helper and protocol. Keep native agent instructions in this repository's consumer-owned Codex files, not in the bundle or a FlowKit role map. Increment each changed workflow's own version and the changed controller package version, then update the source bundle version and workflow pins to match; development-snapshot composition rejects a source/pin mismatch. Validate manifest compatibility and source digests. Update user-facing workflow and installation documentation when behavior changes. A release build and checked-in catalog assets remain a separate reviewed step.

## Design Sequence

1. Reconcile the broadened F014 roadmap entry through its exact approval gate. Use approved Constitution 6.0.0 and the F014 clarification decisions as the authority for declared bounded continuation while retaining all consequential gates.
2. Build a machine-checked branch-and-gate inventory for all eight workflows, including every routine result, human decision, terminal state, and delegated agent assignment. Preserve independent package review and map recorded feedback to cases rather than treating it as the full scope.
3. Extend controller validation and the main-task protocol for pre-loop assessment, pinned Specify `do-while`, the outcome envelope, per-workflow semantic progress, five-pass cap, post-loop human-gate routing, and iteration-aware recovery. Retain all-branch named-agent preflight, same-child question relay within a step, and safe interruption/installation-change stops.
4. Update each source workflow in small reviewable groups. Include evidence classification and re-entry after routine correction; keep exact patch and consequential gates; stop at the current workflow's conclusion without starting the next phase. Validate each package's manual path with automated fixtures.
5. Review step responsibilities against the four starting agent names, approve any justified new name before source use, and add usable repository-local native configurations before full direct-Codex story checks. Retire probe-only behavior from ordinary workflow use without changing consumer bundle ownership.
6. Run automated graph, recovery, branch, manual-fallback, and disposable-consumer checks. Capture native agent-selection evidence through the supported client when observable; otherwise mark that claim unverified. Generate a validation report with versions, digests, source coordinates, results, skipped paths, and limitations. Once automated validation is complete, offer at most two concrete Codex desktop experience checks for the operator: one representative continuation and one native-agent/gate presentation check. Record their observations separately from automated results; routine verification must not require operator checks or attestations.
