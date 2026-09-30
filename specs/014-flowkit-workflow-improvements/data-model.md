# Data Model: Workflow Continuation

F014 extends the existing reviewed workflow definition and compact controller evidence. It adds no database or durable service. All persisted paths remain relative to the selected consumer project.

## Workflow definition

`WorkflowDefinition` has an ID, version, declared inputs, and ordered steps. The eight existing `speckit-flow-*` packages remain separate. A changed package increments its own version and retains a manual-prompt path. The installed, composed definition remains the behavior authority for the direct Codex controller.

`StepNode` has a globally unique ID and one supported type. Executable `prompt` and `command` nodes may carry `flow_kit.delegated: true` with one exact reviewed `flow_kit.agent`; an undelegated node runs in the main task. `gate` and `switch` nodes remain in the main task. F014 adds support for Specify's existing `do-while` container; the container itself does not carry an agent assignment. Its nested steps retain unique IDs and their own assignments.

## Loop policy and pass

`LoopPolicy` belongs to one `do-while` node and contains its loop ID, body steps, one expression over a validated prior-step outcome, and a positive `max_iterations`. An initial assessment outside the body is required so `complete`, `needs-human`, and `blocked` can route without a corrective pass; only `continue` enters the body. F014's maximum is five body passes per loop. The controller must reject unsupported expression forms, unresolved references, invalid caps, or a loop whose body has no inspectable reassessment before workflow work. After a body pass, `complete` exits cleanly, `needs-human` reaches a declared main-task gate, and `blocked` stops. A still-`continue` outcome at the cap is a bounded stop.

`LoopPass` is one execution of a loop body. It has a one-based iteration number, the outcome and reason from its assessment, a compact before/after evidence fingerprint, resolved finding or task identifiers, changed repository-relative paths, and per-step statuses. Passes are ordered and append-only in the run summary. A delegated executable step starts a fresh child for each pass; interactive questions within one step resume its current child.

## Assessment outcome

`AssessmentOutcome` is the validated result used for routine routing. Required fields are `state` (`complete`, `continue`, `needs-human`, or `blocked`), a stable `reason_code`, a non-empty array of repository-relative evidence references, and arrays of remaining and resolved finding/work IDs. Workflow-specific fields may describe affected artifact layers or a proposed exact patch, but the generic controller must not infer authorization from them. Missing, contradictory, stale, or uninspectable evidence produces a blocked result, never an assumed clean result.

The assessment step is a fresh reading of current artifacts and command outputs. A command's exit status, a changed file digest, or a child assertion alone does not prove `complete`. A routine `continue` must identify the next in-scope correction. A `needs-human` outcome identifies the consequential decision and reaches a main-task gate. A `blocked` outcome identifies the smallest safe resumption action.

## Progress snapshot and state transitions

`ProgressSnapshot` records the set of unresolved in-scope finding/work IDs, the set completed in the current pass, and fingerprints of relevant current artifacts. A pass counts as progress when refreshed evidence confirms that at least one prior finding was resolved or one eligible task was completed. A digest-only change does not count. Repeated unresolved IDs without material change or absent progress stops immediately. The safety cap stops the loop even when progress continues; it does not convert `continue` into `complete`.

```text
ready → running pass → assess → complete
                       ├→ continue → next pass (progress and cap permit)
                       ├→ needs-human → main-task gate or stop
                       └→ blocked → stop

continue + no progress/repeated finding/stale evidence/cap → bounded stop
```

## Human gate and authority

`HumanGate` records the exact question, supported options, the evidence presented, and the operator's decision. It is not an assessment substitute for routine machine-observable states. Exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and acceptance remain human decisions. A gate cannot grant a later workflow invocation implicitly.

## Agent assignment and native configuration

`StepAssignmentIntent` is the existing `(step_id, agent_name)` pair for every possible delegated branch, including loop bodies. Names start from Architect, Builder, Coder, and Verifier. A new name requires reviewed purpose and approval before source use. Each selected name has a native Codex TOML file in this repository's `.codex/agents/` for local dogfooding. Codex owns optional model and effort settings. F014 does not install these files into other consumer projects.

## Run evidence

`RunSummary` retains workflow ID/version/digest, installation fingerprints, reviewed assignments, ordered loop passes, step statuses, changed repository-relative paths, terminal state, blocker code, and timestamps. It excludes raw transcripts, secrets, agent TOML contents, and absolute host paths. A preflight failure creates no run record. Interrupted or changed-installation runs stop at a safe boundary and retain completed-pass evidence.
