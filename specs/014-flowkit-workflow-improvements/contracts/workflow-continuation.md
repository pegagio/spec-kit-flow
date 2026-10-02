# Contract: Bounded Workflow Continuation

This contract describes the direct FlowKit Codex controller's interpretation of reviewed workflow loops. It uses the pinned Specify `do-while` step type; it does not claim that native `specify workflow run` performs identical named-agent dispatch or recovery.

## Definition shape

The installed workflow definition owns every loop body, condition, cap, command, assignment, and human gate. The controller must reject unsupported nodes or expressions before workflow work. The example shows the shape, not a complete F014 workflow:

```yaml
steps:
  - id: review-loop
    type: do-while
    condition: "{{ steps.assess-cycle.output.state == 'continue' }}"
    max_iterations: 5
    steps:
      - id: correct-cycle
        type: command
        command: speckit.tasks
        flow_kit:
          delegated: true
          agent: Tasker
      - id: assess-cycle
        type: prompt
        flow_kit:
          delegated: true
          agent: Reviewer
        prompt: "Assess current evidence and return the required outcome envelope."
```

A corrective loop may assess before entry or begin with a safe work-checking command. Analyze and Remediate instead declares the boolean `assessment_only_first_pass: true` on its `do-while` node: its first pass skips all mutation and establishes a read-only analysis baseline through the same read-only assessment used after corrections. The controller passes `--assessment-only-first-pass` to `route-loop`; only iteration 1 without a previous assessment may continue without resolved findings. Later passes must supply that baseline or the preceding assessment and demonstrate progress. Six total passes allow one baseline and at most five corrections; Clarify, Plan, Tasks, Implement, and Close Out wiki maintenance use five body passes. `max_iterations` is a positive integer. `needs-human` reaches a declared main-task gate when one exists, otherwise stops with the required operator decision and a resumption action; `blocked` stops with a resumption action. The container has no agent assignment; each delegated executable child names an agent. Main-task gates and switches may be nested in the body but never delegated.

Converge, Close Out debrief, and Wiki Lint Update use the mutually exclusive `assessment_before_correction: true` mode. Each body contains its source command, the report assessment, and a switch on that assessment's state with corrections only in continue. Validate and call `route-loop --assessment-before-correction` immediately after the assessment, before entering the correction branch. Iteration 1 establishes the gap baseline; later iterations compare the fresh report with the preceding assessment. Converge and Close Out debrief use six checks for five corrections and final confirmation. Wiki Lint Update uses 26 checks for 25 source refreshes and final confirmation. Complete, required human input, blocked, no progress, or cap exhaustion exits before further correction. Intermediate task eligibility or implementation blockers stop immediately and are reported, rather than starting another source command. Successful implementation returns directly to the core convergence command for its next report.

## Assessment envelope

The controller accepts one validated outcome from the reviewed assessment step before evaluating the loop condition. Its minimal portable form is:

```json
{
  "state": "continue",
  "reason_code": "routine-task-gap",
  "evidence": [
    {"path": "specs/014-flowkit-workflow-improvements/tasks.md", "sha256": "<64 lowercase hex digits>"}
  ],
  "remaining_ids": ["T021"],
  "resolved_ids": ["T019"],
  "next_step_id": "correct-cycle"
}
```

Current routine loop `state` is `complete`, `continue`, or `blocked`. Required operator input is a blocked reason with its exact question and recovery action. The controller also accepts legacy `needs-human` for declared human gates. `reason_code` and `resume_action` are stable identifiers matching `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`: lowercase letters and digits joined by single hyphens, without spaces or underscores. Assessment prompts that may return either field state this syntax explicitly. These are machine-readable routing labels, never free-form authority or prose. Each evidence path is repository-relative, exists in the selected project when assessed, and has a digest of the observed bytes. A changing digest alone is not progress. `remaining_ids` and `resolved_ids` refer to finding or work identifiers in current feature evidence. `continue` requires an in-scope `next_step_id` in the reviewed loop body; `needs-human` requires a reviewed main-task gate or, when none is declared, a stable resumption action; `blocked` requires a specific resumption action. A `complete` state requires the workflow's defined success evidence and no unresolved in-scope work. The controller rejects unknown states, missing evidence, invalid paths, contradictory IDs, or a route unsupported by the installed graph.

Assessment routing follows the controller schema exactly. A `complete` envelope omits `next_step_id`, `gate_step_id`, and `resume_action`; a `continue` envelope includes only `next_step_id` targeting the declared loop body; a `blocked` envelope includes only a stable `resume_action`. Clean findings do not excuse an invalid terminal envelope. Live verification must record the rejected run, correct ambiguous source guidance, and retry against refreshed source before claiming workflow success.

## Progress and termination

After each correction pass, the controller compares the current outcome with the preceding pass. Progress requires refreshed evidence confirming resolution of at least one prior finding or completion of an eligible task. Repeated unresolved findings without material change, no progress, stale or conflicting evidence, failed prerequisites, and consequential decisions stop at once. When `continue` remains true after the final allowed pass, the run stops with a cap-exhausted reason and preserved evidence; it never reports success merely because the loop ended.

Close Out wiki coverage uses stable claim-level findings established before correction. Whole-source coverage is a grouping only: resolving a prior loop-limit claim counts while a separate partial-activation claim remains. The preparation output supplies an exact source/page/section correction checklist to the ingestion child without changing its single-token command arguments. Initial curation includes feature-relevant registered local supporting sources within operator-issued project scope. Routine date-only freshness revalidation may update metadata after every claim and citation is verified against current authorized sources, recording before/after source and page digests; it needs no extra permission and supplies zero substantive progress credit. Conflicting authority, access outside the frozen scope, and actual missing knowledge retain their explicit stops. Existing envelope fields, prior-ID comparison, five-pass cap, and consequential gates are unchanged.

The loop outcome and per-pass evidence are recorded in the consumer-local compact run summary. Pass identity is `(loop_id, iteration)`, with step statuses nested under that identity so repeated step IDs do not overwrite earlier passes. Raw child transcripts and absolute machine paths are excluded. A new child handles each delegated step in each pass; an answer to a question from that step returns to the same active child.

Plan and Tasks combine structural required-output checks with independent Reviewer semantic assessment against the approved spec and reviewed design. A populated but inconsistent artifact remains deficient. The workflow-specific result returns exact findings (stable ID, artifact location, violated constraint, required correction) to Planner or Tasker through the existing correction path; it does not extend the generic envelope. Fresh reassessment must confirm a prior structural or semantic finding resolved. Repeated findings, no progress, stale evidence, unanswered substantive product questions, and five-pass cap exhaustion preserve remaining IDs and a recovery action. Reviewer assesses; the author corrects; the operator supplies substantive answers. This contract adds no nodes or topology changes.

Authoring roles complete command-required self-checks, prerequisite checks, and quality checklists. Such checks do not replace independent assessment by the separately assigned Reviewer or Code Reviewer. The prohibition is against acting as the independent reviewer of their own output, not against satisfying the invoked core command. This clarification changes no workflow steps, assignments, or review scope; Specify linkage and roadmap checks remain their existing distinct responsibilities.

## Authority boundary

The controller may execute only nodes declared in the currently invoked workflow. It never invokes another FlowKit workflow or the next phase implicitly. A routine evidence classification is not a human gate. Exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and feature acceptance stay with the operator in the main task. Command success is not a clean assessment.

Constitution 6.0.0 prospectively permits declared, bounded core-command correction and reassessment within one invoked workflow. The operator selected F014's repeated Clarify-session policy and approved the exact broader roadmap scope amendment. These decisions do not change verified historical features.

## Joined transitions and retained evidence

Different case keys may have empty bodies and join the same next node when that node evaluates completed outputs before choosing further work. A shared edge does not authorize a brief, correction, write, or implementation. Success prerequisites remain checked explicitly; deferred or amended gate choices remain reported and never count as approval. Optional `transition_labels` names displayed paths without changing case keys or selected choices.

The current graph's explicit gates are feature choice and exact activation patch in Select Feature, exact linkage repair in Specify, and exact verification patch in Close Out. Substantive questions within core skills still require operator answers through the same active child. Blocked reports preserve those questions; they are not implicit approvals or automatically added workflow gates.
