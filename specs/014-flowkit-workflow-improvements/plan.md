# Implementation Plan: FlowKit Workflow Improvements

**Branch**: `develop` (feature directory `014-flowkit-workflow-improvements`) | **Date**: 2026-09-29 | **Spec**: [spec.md](spec.md)

**Input**: Clarified F014 specification, approved Constitution 6.0.0, [workflow review baseline](workflow-review-baseline.md), ten active source workflow packages and the deprecated Start Feature definition, the operator's five clarification answers, and the operator-approved all-eight-workflow roadmap amendment.

## Contents

The main sections describe the selected runtime approach, authority checks, source layout, and work sequence.

- [Summary](#summary)
- [Technical Context](#technical-context)
- [Loop Entry and Progress](#loop-entry-and-progress)
- [Constitution Check](#constitution-check)
- [Project Structure](#project-structure)
- [Design Sequence](#design-sequence)
- [Selection and authoring split](#selection-and-authoring-split)
- [Reconciliation and remaining delivery](#reconciliation-and-remaining-delivery)
- [Incorporated source validation](#incorporated-source-validation)
- [Live workflow verification](#live-workflow-verification)

## Summary

Review all ten active FlowKit workflows branch by branch, then make each invoked workflow reach its own evidenced success, required human decision, or bounded stop. Use the pinned Specify `do-while` step for explicit in-workflow continuation, extend the direct Codex controller to validate and execute that shape with iteration-aware recovery, and replace routine classification gates with a small validated outcome contract. Preserve separate operator invocation of the next workflow, exact approval gates, and manual fallback. Review every delegated step against Feature 015's native agent design and supply usable repository-local configurations for selected names. The recorded F014 Start, Clarify, Plan, Tasks, Converge, and Close Out issues become acceptance cases for this complete-workflow review.

[Research](research.md) resolves the loop representation, progress rule, recovery boundary, and agent-file ownership. [Data model](data-model.md) defines the loop, pass, outcome, progress, gate, assignment, and run evidence. The [continuation contract](contracts/workflow-continuation.md) and [agent contract](contracts/agent-assignment.md) make the runtime interfaces reviewable. The constitutional amendment is approved; this plan records the accepted technical approach and current delivery.

## Technical Context

**Language/Version**: Existing Python 3.11 controller and tests; Specify workflow YAML schema 1.0; selected Specify CLI `1.0.10.dev0+pegagio.2`; native Codex custom-agent TOML.

**Primary Dependencies**: Existing Specify workflow loader with built-in `do-while`; FlowKit's shared controller helper/protocol and direct Codex skills; native Codex named-agent selection. No new framework, library, service, or build tool.

**Storage**: Reviewed workflow YAML, repository-local `.codex/agents/*.toml`, and existing compact consumer-local run summaries under `.specify/flow-controllers/runs/`. No database or new bundle-owned agent storage.

**Testing**: Automated controller, catalog, and lifecycle tests; graph, outcome, and manual-fallback fixtures for all eight packages; Specify loader checks; scripted disposable-consumer snapshot install/refresh/remove; and machine-recorded native Codex named-agent selection where the client exposes it. The validation run must report skipped or unobservable checks. After those checks, the operator may perform one or two narrowly specified Codex desktop experience checks to confirm the visible workflow and agent behavior.

**Target Platform**: Codex desktop task in a compatible initialized consumer; this macOS checkout is the source repository and a dogfood consumer. Other clients and native Specify named-agent parity remain unverified until separately tested.

**Project Type**: Versioned workflow packages, shared Codex controller package, local catalog installer, and consumer-owned agent configuration.

**Performance Goals**: Complete static graph, assignment, and compatibility preflight before the first workflow work step. Feature correction loops permit at most five correction passes per invocation; Wiki Lint Update permits at most 25 source refreshes and stops sooner on no progress or a consequential decision. No background processing or unattended retry.

**Constraints**: Human-directed workflow scope and exact consequential gates; no nested FlowKit workflow invocation or automatic next phase; no command-success-as-clean shortcut; five-question Clarify command cap per session; independently reviewable workflow packages and manual fallback; portable evidence without raw transcripts or absolute paths.

**Scale/Scope**: Ten active workflow IDs plus the deprecated Start Feature source, all possible branches and delegated assignments, one selected feature/workflow invocation at a time, five correction passes for feature loops, and up to 25 source refreshes for Wiki Lint Update.

## Loop Entry and Progress

A corrective loop may assess before entry or begin with a command that safely checks for work. Analyze and Remediate declares `assessment_only_first_pass: true`: its first body pass skips every correction, runs fresh task analysis, and establishes a read-only baseline through its shared assessment. Later passes enter its shared specification → plan → tasks waterfall, then run the same analyzer and assessment. Six total passes allow one baseline and at most five corrections.

Converge declares `assessment_before_correction: true`. Every pass starts with `speckit.converge`, then one assessment classifies that fresh report and checks progress before a guarded correction branch. The first report establishes the baseline; later reports verify the preceding implementation. Corrections use the shared waterfall, fresh task analysis, eligibility verification, and implementation, then return directly to the source command. Six command/assessment passes permit five corrections and a final confirmation. Intermediate eligibility or implementation blockers stop before another pass. Close Out uses the same six-check debrief mode plus a separate five-pass wiki ingest/lint loop. Wiki Lint Update uses 26 lint/assessment passes for at most 25 source refreshes and final confirmation. Clarify, Plan, Tasks, and Implement use five body passes.

A `complete` assessment ends successfully. Current routine loops use `blocked` for prerequisites and required operator input, retaining the exact question and resumption action. Legacy `needs-human` remains compatible with declared gates; it does not add a gate to current graphs. Only validated `continue` permits another pass. Every correction must resolve a prior finding or eligible task against the preceding assessment. No progress, repeated unresolved findings, stale evidence, failed prerequisites, or an untrustworthy outcome stops continuation. A still-`continue` outcome on the final allowed pass is cap exhaustion, never success. Implement records unfinished tasks before the loop and repeats core-skill sessions only while eligible work remains and a prior task was completed.

| Workflow | Initial and refreshed evidence | Confirmed progress within one invocation |
|---|---|---|
| Select Feature | Candidate and dependency inventory, exact operator choice, unique target, exact approved roadmap patch, and active pointer. | A non-looping selection/activation handoff; no specification write or directory creation. Partial writes and deferral are reported. |
| Specify | Active pointer, cited context, exact authored directory, unique roadmap mapping, and one shared brief. | A non-looping authoring handoff; any linkage repair requires exact approval and fresh verification before the brief. |
| Clarify | Significant ambiguity IDs tied to current spec passages and the answers incorporated after each bounded session. | At least one prior significant ambiguity ID is resolved in the current spec; a newly discovered question does not turn an unchanged earlier ambiguity into progress. The five-question limit remains per session. |
| Plan | Required file/placeholder checks plus independent Reviewer semantic assessment of current design against the approved spec and constitution after each `speckit.plan` pass, including populated but deficient artifacts. | Fresh assessment confirms resolution of a prior structural or semantic finding; exact remaining findings return to Planner through the existing planning correction path. Preserve decisions; stop on no progress, unresolved operator-owned product answers, or the five-pass bound. |
| Tasks | Required task structure/coverage checks plus independent Reviewer semantic assessment against the approved spec and plan after each core-skill pass, including populated but deficient task artifacts. | Fresh assessment confirms resolution of a prior structural or semantic finding; exact remaining findings return to Tasker through the existing task correction path. Preserve task history; stop on no progress, unresolved operator-owned product answers, or the five-pass bound. |
| Analyze and Remediate | One shared `speckit.analyze` command and `assess-analysis` step establish the initial read-only baseline and assess every shared-waterfall correction. | Fresh analysis confirms a prior finding resolved after ordered artifact reconciliation; a changed digest alone is insufficient. |
| Implement | Initial unfinished eligible task IDs, then task and validation evidence after each `speckit.implement` session. | A previously unfinished eligible task is completed, and a fresh assessment confirms specific eligible tasks remain for another session; no task progress or the fifth still-incomplete pass causes a bounded stop. |
| Converge | Fresh `speckit.converge` report and shared assessment at the start of every pass; waterfall reconciliation, analysis, eligibility, and implementation follow only when continuation is permitted. | Fresh convergence evidence confirms a prior gap resolved after changed tasks pass analysis and eligible implementation; command success alone is insufficient. |
| Close Out | Completion state, current debrief finding IDs, wiki source coverage, lint and roadmap evidence. | Six debrief checks allow five corrections; a sibling five-pass single-source wiki loop requires prior-gap resolution. Only the exact roadmap patch has a human gate; commit readiness is reported automatically. |
| Wiki Lint Update | Fresh lint, stable finding IDs, cited registered source identities, authorized URLs, and prior resolved findings. | Each refresh resolves a prior finding, followed by fresh lint. Twenty-six checks allow at most 25 refreshes; all other unresolved findings remain reported. |

Plan and Tasks assessments carry exact findings with stable IDs, affected artifact locations, the violated requirement or design constraint, and the required correction in their workflow-specific handoff, separate from the strict outcome envelope. Reviewer assesses independently; Planner and Tasker retain author-owned correction. Populated files and changed wording alone cannot establish success. Reassessment must confirm a prior finding resolved; repeated unresolved findings, stale evidence, and a still-incomplete final pass stop with remaining IDs and a recovery action. A substantive product question returns to the operator through the same active child, without inventing an answer or adding a workflow node. Existing assessment/correction topology and the five-pass bound remain unchanged.

All finding and task IDs are scoped to the selected workflow and its feature or wiki scope. When a source command cannot provide stable IDs directly, a reviewed assessment step derives them from inspectable current artifacts; inability to establish a trustworthy comparison stops the loop.

Assessment routing follows the controller schema exactly. A `complete` envelope omits `next_step_id`, `gate_step_id`, and `resume_action`; a `continue` envelope includes only `next_step_id` targeting the declared loop body; a `blocked` envelope includes only a stable `resume_action`. Clean findings do not excuse an invalid terminal envelope. Live verification must record the rejected run, correct ambiguous source guidance, and retry against refreshed source before claiming workflow success.

Authoring roles complete command-required self-checks, prerequisite checks, and quality checklists. Such checks do not replace independent assessment by the separately assigned Reviewer or Code Reviewer. The prohibition is against acting as the independent reviewer of their own output, not against satisfying the invoked core command. This clarification changes no workflow steps, assignments, or review scope; Specify linkage and roadmap checks remain their existing distinct responsibilities.

## Constitution Check

**Pre-research gate — authority resolved.** Principle I requires accepted discoveries to flow through F014's spec, plan, tasks, and eventual implementation. Approved Constitution 6.0.0 permits declared, bounded core-command correction and reassessment within the selected workflow and scope, including Converge's analysis and implementation, while forbidding another FlowKit workflow or undeclared later phase. The operator explicitly selected F014's repeated Clarify-session policy and Close Out completion rule in the specification clarification session. Feature 014 changes future behavior without rewriting verified Feature 007/008 history. Substantive answers and consequential decisions remain human gates.

**Roadmap scope gates — resolved.** The operator approved the exact all-eight-workflow and repository-local-agent amendment, which is recorded in `.specify/memory/roadmap.md` and `validation/authority-decisions.md`. The original source work was authorized by that approval. The subsequent replacement/addition scope is recorded here; its exact roadmap reconciliation patch was approved and applied on 2026-09-30. Verified feature history remains unchanged.

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
workflows/speckit-flow-*/workflow.yml          # Ten active behavior graphs plus one deprecated stop-only source
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
tests/test_agent_configs.py                    # Native definition and assignment checks
tests/test_snapshot_validation.py              # Delivered; pinned snapshot lifecycle evidence recorded
tests/consumer-fixtures/
tools/validate_workflows.py
docs/installation.md
workflows/README.md
```

**Structure Decision**: Keep each workflow's prompts, branches, gates, loop condition, and cap in its versioned YAML. Put generic graph validation, outcome-envelope checking, progress comparison, and iteration-aware recovery in the shared controller helper and protocol. Keep native agent instructions in this repository's consumer-owned Codex files, not in the bundle or a FlowKit role map. Increment each changed workflow's own version and the changed controller package version, then update the source bundle version and workflow pins to match; development-snapshot composition rejects a source/pin mismatch. Validate manifest compatibility and source digests. Update user-facing workflow and installation documentation when behavior changes. A release build and checked-in catalog assets remain a separate reviewed step.

## Design Sequence

1. Reconcile the broadened F014 roadmap entry through its exact approval gate. Use approved Constitution 6.0.0 and the F014 clarification decisions as the authority for declared bounded continuation while retaining all consequential gates.
2. Build a machine-checked branch-and-gate inventory for all ten active workflows and the deprecated source, including every routine result, human decision, terminal state, and delegated agent assignment. Preserve independent package review and map recorded feedback to cases rather than treating it as the full scope.
3. Extend controller validation and the main-task protocol for pre-loop assessment, pinned Specify `do-while`, the outcome envelope, per-workflow semantic progress and explicit finite caps, post-loop human-gate routing, and iteration-aware recovery. Retain all-branch named-agent preflight, same-child question relay within a step, and safe interruption/installation-change stops.
4. Update each source workflow in small reviewable groups. Include evidence classification and re-entry after routine correction; keep exact patch and consequential gates; stop at the current workflow's conclusion without starting the next phase. Validate each package's manual path with automated fixtures.
5. Apply the operator-reviewed task-specific role names to every delegated step, add usable repository-local native configurations, and replace the probe-only Coder instructions. Reuse existing assessment steps for independent artifact and implementation review; do not add workflow nodes or change their topology.
6. Run automated graph, recovery, branch, manual-fallback, and disposable-consumer checks. Capture native agent-selection evidence through the supported client when observable; otherwise mark that claim unverified. Generate a validation report with versions, digests, source coordinates, results, skipped paths, and limitations. Once automated validation is complete, offer at most two concrete Codex desktop experience checks for the operator: one representative continuation and one native-agent/gate presentation check. Record their observations separately from automated results; routine verification must not require operator checks or attestations.


## Selection and authoring split

The operator-approved split replaces Start Feature with `speckit-flow-select-feature` and `speckit-flow-specify`. Selection owns inventory, dependency discussion, exact selection approval, roadmap mutation, and active-pointer verification, without writing spec files or creating target directories. The main-task pointer step uses the shared atomic `activate-feature` helper. Specify consumes the pointer, keeps `SPECIFY_FEATURE_DIRECTORY` explicit, authors or revises only that target, verifies linkage, and runs the brief. Existing spec contents survive selection. A reserved directory is valid until authoring. Failed pointer activation after a roadmap write is reported as partial state. Deprecation is stop-only source plus retirement from the active bundle and controller inventory; historical catalog evidence is preserved. Tests cover pointer-only writes, shared brief paths, package inventory, and retirement of unchanged owned launcher files; locally modified retired files block refresh.

The two replacement workflows use `blocked` for unmet prerequisites, required operator input, conflicts, ambiguity, and unapproved or deferred changes, with the cause and recovery action retained in output. Readiness and brief switches use explicit success and `blocked` cases. Linkage uses `repairable`, `linked`, and `blocked` outcomes. Empty success and stop paths join outcome preparation, which reads only completed evidence and permits the brief only for verified linkage; shared paths do not imply identical authorization. Human gate choices remain explicit and are preserved for reporting; optional `transition_labels` metadata labels their shared approval paths `approved` and `not-approved` without changing runtime choices. The validated feature-selection fallback is labeled `selected`.

The six previously reviewed loop workflows collapse ungated `needs-human` into `blocked`, preserving operator questions and stable resumption actions. Completion, continuation, waterfall actions, and artifact entry points remain distinct. Converge uses explicit `continue`, `complete`, and `blocked` branches for correction and task eligibility. Shared controller validation accepts this three-state correction switch and the compatible legacy four-state form; Closeout is subsequently simplified as described below.

Closeout now has one shared correction waterfall, analyzer, eligibility check, implementation command, and fresh debrief. Its six assessment-before-correction checks allow five corrections and final confirmation. Required human decisions use blocked questions and recovery actions, replacing stop-only defer/abort gates. Exact roadmap-patch approval remains the sole human gate; commit readiness is assessed and reported without granting commit authority. Outcome preparation uses only completed initial or loop evidence, so initial stops never reference a skipped loop. Blocked eligibility stops before another debrief. Both approved fresh verification and existing verification enter shared wiki maintenance; ingestion, lint, coverage, and Git-change evidence must be checked before commit-readiness reporting. One report preserves partial state and original gate choices without committing or implying acceptance.

Wiki maintenance uses a sibling five-pass ingest/lint/assessment loop. Each pass selects exactly one source within the authorized curated set, preserving the core ingestion contract. Prepared baseline IDs identify individual missing durable contracts and stale claims rather than whole-source completion. The ingestion child receives all exact source-backed corrections for its selected source as completed preparation context alongside the single-token arguments. This allows a corrected prior claim to establish progress while other claims from the same source remain. Initial curation includes feature-relevant registered local supporting sources inside the operator-issued project scope. The main-task preparation step may directly revalidate date-only warnings and update freshness metadata only after proving every claim and citation supported by current authorized sources; it records source/page before-and-after digests and earns no substantive progress credit. Neither routine source selection nor this verified revalidation requires another operator confirmation. Conflicts requiring authority decisions, unavailable or unauthorized sources, unverified date-only warnings, unsupported repairs, scope expansion, stale evidence, no progress, and the cap stop as blocked. Only a validated complete latest assessment permits the final commit-readiness recommendation.

The independent `speckit-flow-wiki-lint-update` package starts each pass with lint and assesses the complete findings before one registered-source refresh. It preserves non-stale findings while independent safe stale refreshes proceed, then reports blocked recovery actions for any unresolved issues. Twenty-six checks allow up to 25 individual source refreshes and final confirmation; no-progress and capacity stops preserve pending source identities. Optional lint scope and explicit registered URL authorization remain separate from source evidence. The workflow has its own launcher, graph, and bundle contribution.

## Reconciliation and remaining delivery

The [reconciliation record](validation/artifact-reconciliation.md) maps approved source changes to requirements, design, tasks, and current source evidence. The [current inventory](current-workflow-inventory.md) replaces baseline observations as the source-current graph and assignment reference. Original baseline records remain historical evidence. At that earlier reconciliation milestone, source bundle 0.13.5 pinned ten active definitions and controller 0.5.1 carried ten thin launchers. The current tested source is bundle 0.13.7/controller 0.5.2, recorded in the final live audit. The deprecated definition has no active binding. Checked-in release catalog assets remain unchanged.

The project rendering skill lives in `skills/flowkit-render-workflow/`, with a project-discoverable installed copy. It renders `flowchart.md` adjacent to a selected definition. Prompt, command, switch, loop, and gate shapes plus delegated outlines convey metadata; labels contain the exact ID, optional `(AgentName)`, and optional command. A presentation-only Start node anchors entry. `transition_labels` is presentation metadata validated against declared branches; runtime outcomes and gate choices remain intact.

The responsibility inventory, eight native configuration files, source assignments, and existing assessment-prompt reviews are implemented and pass static tests. The attributable [validation report](validation/report.json), recorded against source revision `c34ea2aa2fa23e131d796be39343064f0a93a652` with working-tree changes, reports 116 automated tests, zero failures/errors, and a skipped external-working-tree lifecycle suite. T044 is delivered: the initialized-consumer snapshot install/refresh/remove passed against checksum-pinned release packages, preserving consumer-owned files and an unrelated workflow. T046 has delivered the consolidated automated report. Earlier skipped/pending observations in reconciliation evidence remain historical, not current T044/T046 blockers. The distinct lifecycle suite using external roadmap/wiki working trees remains skipped unless their source settings are configured; it is supplementary to T044. Exact live Codex native-agent selection is unverified by this report, whose static validator cannot observe it; optional desktop checks are prepared and not run. Static branch projections are not runtime branch execution. T066–T069 delivered the accepted semantic-review contracts, with 41 focused deterministic checks (26 path, 11 graph, and four agent checks) and the source validator passing as recorded in `semantic_review_follow_up` in the validation report. This evidence covers scripted independent-agent handoffs, routing, prompt contracts, and topology; that follow-up did not verify live semantic reasoning or native-agent selection, and lifecycle suites were not rerun for it. Later live observations have separate evidence boundaries. T070/T072/T074 delivered the shared assessment-identifier grammar correction across 13 assessment prompts in eight source workflows, with 50 controller tests, 12 graph tests, and the workflow validator passing as recorded in `identifier_grammar_follow_up` in the validation report. The shared T065/T071/T073/T075/T076/T077 source-current evidence reconciliation was delivered and independently confirmed by Converge run `0a87d86f-bb0a-4189-b692-b0367e434624`, whose validated final outcome resolved F014-G002 with no remaining findings. Historical tests remain prior observations; incorporation into this checkout receives separate fresh validation in the report. The exact roadmap scope patch is approved and applied; roadmap lifecycle and feature Draft status are unchanged. This artifact repair authorizes no release or acceptance.

## Incorporated source validation

After incorporation and T078/T079 corrections, the full suite ran 126 tests with zero failures or errors; the optional external-working-tree lifecycle suite was skipped. The checksum-pinned consumer snapshot install/refresh/remove and all eleven workflow definitions passed. All eight source-identical native role configurations passed exact-name readiness probes. Current results and source digests are recorded in `final_source_validation` and `native_role_availability` in [the validation report](validation/report.json). Native identity/model introspection, general live semantic correctness and optional desktop observations remain outside that evidence. Feature acceptance, roadmap verification, release and Git integration remain separately controlled.

## Live workflow verification

T080–T089 extend validation to real installed-skill scenarios for Select Feature, Specify, Clarify, Plan, Tasks, Closeout, and Wiki Lint Update. The operator-issued Codex goal coordinates separate invocations in isolated synthetic consumers, collects controller and artifact evidence, corrects reviewed source, refreshes installed snapshots, and retries affected scenarios. This coordination does not change in-workflow topology, bounds, authority, or phase separation. Follow the [live verification runbook](validation/live-workflows/runbook.md); collect attributable initial fixture decisions and exact approvals before dependent success scenarios. Existing 126-test, consumer lifecycle, role readiness, and three live workflow observations remain historical evidence within their recorded scope, not proof that the seven remaining workflows have run live. Required scenarios remain open until independently verified against final source.

Current live evidence records all 23 required scenarios passing, with T080–T089 delivered. Exact fixture decisions and patches were directly approved; actual gates relayed only matching approvals after current evidence. The driver exercised separate native invocations, evidence collection, command-local corrections, source repairs and refreshes, strict rejection/retry, completed-child cleanup and compaction recovery. [The final audit](validation/live-workflows/completion-audit.json) binds all passing records to current source, preserves 12 failed required attempts and distinguishes unavailable model/effort identity, four missing per-run Wiki role snapshots and excluded accidental dispatches. All ten active workflows have defined live case or prerequisite evidence; this is not exhaustive branch or command coverage.

A static compatibility check found that Closeout supplied prose to the core wiki lint scope parser. Closeout 0.6.5 now passes an empty scope for full lint, with bundle 0.13.7 pinning it. The new path assertion failed on the old input and passes after correction; the final available 127-test suite and eleven-workflow validator pass, with only the optional external working-tree lifecycle skipped. The prerequisite consumer was refreshed after its completed clean Analyze run. At that static-correction milestone, Closeout live scenarios were pending; that record supplies no live completion claim. Later live execution is recorded separately in the coverage matrix.
