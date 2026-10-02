# Data Model: Workflow Continuation

F014 extends the existing reviewed workflow definition and compact controller evidence. It adds no database or durable service. All persisted paths remain relative to the selected consumer project.

## Workflow definition

`WorkflowDefinition` has an ID, version, declared inputs, and ordered steps. Ten active `speckit-flow-*` packages remain separate; one deprecated Start Feature definition is retained as stop-only source and omitted from active bundle and controller bindings. A changed package increments its own version and retains a manual-prompt path. The installed, composed definition remains the behavior authority for the direct Codex controller.

`StepNode` has a globally unique ID and one supported type. Executable `prompt` and `command` nodes may carry `flow_kit.delegated: true` with one exact reviewed `flow_kit.agent`; an undelegated node runs in the main task. `gate` and `switch` nodes remain in the main task. F014 adds support for Specify's existing `do-while` container; the container itself does not carry an agent assignment. Its nested steps retain unique IDs and their own assignments.

## Loop policy and pass

`LoopPolicy` belongs to one `do-while` node and contains its loop ID, body steps, one expression over a validated prior-step outcome, and a positive `max_iterations`. A loop may assess before entry or begin with a safe work-checking command. The optional boolean `assessment_only_first_pass` permits a first read-only baseline pass with all correction stages skipped. Only that first pass, without a previous assessment, may continue without resolved findings; later corrections require the previous assessment and verified progress. Analyze and Remediate uses six total passes for one baseline and at most five corrections; Clarify, Plan, Tasks, Implement, and Close Out wiki maintenance use five body passes. The controller rejects unsupported expressions, unresolved references, invalid caps or baseline flags, and bodies without inspectable assessment. `complete` exits cleanly; `needs-human` reaches a declared main-task gate or stops with the required operator decision; `blocked` stops. A still-`continue` outcome at the cap is a bounded stop.

The mutually exclusive boolean `assessment_before_correction` selects a source command → assessment → guarded correction body. The condition references the assessment directly after the command. Only its continue branch contains corrections. Converge and Close Out debrief use six passes: the first core-command report establishes the baseline, five correction branches may run, and the sixth core-command report confirms the last correction before any additional mutation. Wiki Lint Update uses the same mode with 26 checks for up to 25 source refreshes and final confirmation. Progress and cap checks run after each fresh command assessment and before corrections; an intermediate eligibility or implementation blocker stops immediately.

`LoopPass` is one execution of a loop body. It has a one-based iteration number, the outcome and reason from its assessment, a compact before/after evidence fingerprint, resolved finding or task identifiers, changed repository-relative paths, and per-step statuses. Passes are ordered and append-only in the run summary. A delegated executable step starts a fresh child for each pass; interactive questions within one step resume its current child.

## Assessment outcome

`AssessmentOutcome` is the validated result used for routine routing. Required fields are `state` (`complete`, `continue`, `needs-human`, or `blocked`), a stable `reason_code`, a non-empty array of repository-relative evidence references, and arrays of remaining and resolved finding/work IDs. The generic envelope permits only `state`, `reason_code`, `evidence`, `remaining_ids`, `resolved_ids`, `next_step_id`, `gate_step_id`, and `resume_action`. Workflow-specific affected-layer and exact-patch outputs belong to separate step results; they are not extra envelope fields and never grant authority. Missing, contradictory, stale, or uninspectable evidence produces a blocked result, never an assumed clean result.

The assessment step is a fresh reading of current artifacts and command outputs. A command's exit status, a changed file digest, or a child assertion alone does not prove `complete`. A routine `continue` must identify actual unresolved in-scope work and the next declared action; clean implementation can still leave lifecycle or maintenance work pending. Current routine loop outcomes use `complete`, `continue`, and `blocked`; required input is a blocked reason with the exact question and smallest safe resumption action. Legacy `needs-human` remains supported for declared gates.

For Plan and Tasks, a semantic finding has a stable ID, affected artifact location, violated specification/design constraint, and exact required correction. These fields belong to workflow-specific handoff results, not new generic envelope fields. Reviewer may detect substantive deficiencies in populated artifacts; exact findings return to Planner or Tasker through existing author-owned paths. Only fresh independent assessment confirming prior finding resolution counts as progress. Operator-owned product questions stop or relay to the same active child; review never supplies product answers.

Assessment routing follows the controller schema exactly. A `complete` envelope omits `next_step_id`, `gate_step_id`, and `resume_action`; a `continue` envelope includes only `next_step_id` targeting the declared loop body and requires nonempty `remaining_ids` for actual pending work; a `blocked` envelope includes only a stable `resume_action`. Clean findings do not excuse an invalid terminal envelope. Live verification must record the rejected run, correct ambiguous source guidance, and retry against refreshed source before claiming workflow success.

## Progress snapshot and state transitions

`ProgressSnapshot` records the set of unresolved in-scope finding/work IDs, the set completed in the current pass, and fingerprints of relevant current artifacts. A correction pass counts as progress when refreshed evidence confirms that at least one prior finding was resolved or one eligible task was completed. A digest-only change does not count. Repeated unresolved IDs without material change or absent progress stops immediately. The safety cap stops the loop even when progress continues; it does not convert `continue` into `complete`.

```text
ready → running pass → assess → complete
                       ├→ continue → next pass (progress and cap permit)
                       ├→ needs-human → declared gate (legacy compatibility)
                       └→ blocked → stop

continue + no progress/repeated finding/stale evidence/cap → bounded stop
```

## Human gate and authority

`HumanGate` records the exact question, supported options, the evidence presented, and the operator's decision. It is not an assessment substitute for routine machine-observable states. Exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and acceptance remain human decisions. A gate cannot grant a later workflow invocation implicitly.

## Agent assignment and native configuration

`StepAssignmentIntent` is the existing `(step_id, agent_name)` pair for every possible delegated branch, including loop bodies. The reviewed work-type names are Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator. Authoring and review responsibilities remain separate; existing assessment nodes perform review, with no workflow-node additions. Each selected name has a native Codex TOML file in this repository's `.codex/agents/` for local dogfooding. Codex owns optional model and effort settings. F014 does not install these files into other consumer projects.

Authoring roles complete command-required self-checks, prerequisite checks, and quality checklists. Such checks do not replace independent assessment by the separately assigned Reviewer or Code Reviewer. The prohibition is against acting as the independent reviewer of their own output, not against satisfying the invoked core command. This clarification changes no workflow steps, assignments, or review scope; Specify linkage and roadmap checks remain their existing distinct responsibilities.

## Run evidence

`RunSummary` retains workflow ID/version/digest, installation fingerprints, reviewed assignments, ordered loop passes, step statuses, changed repository-relative paths, terminal state, blocker code, and timestamps. It excludes raw transcripts, secrets, agent TOML contents, and absolute host paths. A preflight failure creates no run record. Interrupted or changed-installation runs stop at a safe boundary and retain completed-pass evidence.

## Active target, source refresh, and diagram metadata

`ActiveFeatureTarget` binds the exact selected roadmap entry to one normalized repository-relative `feature_directory` in `.specify/feature.json`. Selection may reserve the directory without creating it. Specification authoring must preserve that identity; unexpected target creation or pointer drift blocks rather than legitimizing a different target through a roadmap repair.

`WikiRefreshCandidate` binds stable lint finding IDs and affected pages to their cited registered source identity. Multiple pages sharing a source produce one candidate. Each ingestion receives one exact source token; local project sources and explicitly authorized registered URLs define the allowed source set. Conflicting authority, age-only warnings without substantive change, unsupported repair, and unavailable sources remain findings. The report retains both refreshed and pending sources and all non-stale issues.

`TransitionLabel` maps declared switch case keys or `default` to descriptive diagram edge labels. It changes presentation only. Empty branches join the next declared node; completed evidence still controls downstream authorization. `WorkflowDiagram` has one presentation-only Start marker and one node per exact source step ID, with shape derived from node kind and dashed outline only for explicit delegation.
