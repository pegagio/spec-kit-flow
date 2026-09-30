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
          agent: Architect
      - id: assess-cycle
        type: prompt
        flow_kit:
          delegated: true
          agent: Verifier
        prompt: "Assess current evidence and return the required outcome envelope."
```

Each corrective loop has a separate current-evidence assessment and route before the container; only a validated `continue` state enters it. This prevents a clean initial result from executing an unnecessary correction because a `do-while` body runs once before its condition. Each body pass then reassesses. `max_iterations` is a positive integer; F014 uses five body passes unless the reviewed package records a justified smaller cap. A `needs-human` state from either assessment reaches a declared main-task gate, while `blocked` stops with a resumption action. The container has no agent assignment; each delegated executable child names an agent. Main-task gates and switches may be nested in the body but never delegated.

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

`state` is exactly `complete`, `continue`, `needs-human`, or `blocked`. `reason_code` is a stable workflow-specific identifier, never free-form authority. Each evidence path is repository-relative, exists in the selected project when assessed, and has a digest of the observed bytes. A changing digest alone is not progress. `remaining_ids` and `resolved_ids` refer to finding or work identifiers in current feature evidence. `continue` requires an in-scope `next_step_id` in the reviewed loop body; `needs-human` requires a reviewed main-task gate; `blocked` requires a specific resumption action. A `complete` state requires the workflow's defined success evidence and no unresolved in-scope work. The controller rejects unknown states, missing evidence, invalid paths, contradictory IDs, or a route unsupported by the installed graph.

## Progress and termination

After each pass, the controller compares the current outcome with the preceding pass. Progress requires refreshed evidence confirming resolution of at least one prior finding or completion of an eligible task. Repeated unresolved findings without material change, no progress, stale or conflicting evidence, failed prerequisites, and consequential decisions stop at once. When `continue` remains true after the fifth pass, the run stops with a cap-exhausted reason and preserved evidence; it never reports success merely because the loop ended.

The loop outcome and per-pass evidence are recorded in the consumer-local compact run summary. Pass identity is `(loop_id, iteration)`, with step statuses nested under that identity so repeated step IDs do not overwrite earlier passes. Raw child transcripts and absolute machine paths are excluded. A new child handles each delegated step in each pass; an answer to a question from that step returns to the same active child.

## Authority boundary

The controller may execute only nodes declared in the currently invoked workflow. It never invokes another FlowKit workflow or the next phase implicitly. A routine evidence classification is not a human gate. Exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and feature acceptance stay with the operator in the main task. Command success is not a clean assessment.

Constitution 6.0.0 prospectively permits declared, bounded core-command correction and reassessment within one invoked workflow. The operator selected F014's repeated Clarify-session policy and approved the exact broader roadmap scope amendment. These decisions do not change verified historical features.
