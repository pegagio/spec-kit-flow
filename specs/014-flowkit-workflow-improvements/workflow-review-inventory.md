# F014 Current Workflow Review Inventory

**Evidence boundary**: Read-only inventory of the eight source `workflow.yml` files before F014 source edits. It records current behavior, not the approved target design.

**Source baseline**: [source-baseline.json](validation/source-baseline.json). The existing controller records workflow ID/version/digest, assignments, per-step status, changed relative paths, blocker, and timestamps in `.specify/flow-controllers/runs/<run-id>/summary.json`; repeated step IDs overwrite prior records, and summaries have no loop/iteration or safe-resumption-point field.

## Review summary

| Workflow | Current success result | Routine automation and continuation | Human gates | Stops and resumption evidence |
|---|---|---|---|---|
| `speckit-flow-start-feature` | Success is gated review of the drafted specification and roadmap brief | initial eligibility assessment followed by approved roadmap write, wiki query, spec creation, and brief; there is no post-spec linkage repair or re-brief loop. | See route details. | A completed start handoff; exact patch or context blockers; final reviewer-selected next action. |
| `speckit-flow-clarify` | Success is a human-selected planning-ready or deferred result after one clarification session | one `speckit.clarify` command. The continue branch stops and requires a separate invocation; no in-run loop or residual-ambiguity assessment. |  classify continue/planning/defer | One clarification session; explicit continue, planning-review, or deferral stop. |
| `speckit-flow-plan` | Success is planning artifacts after the operator confirms readiness | plan command, then stop for plan review. Return-to-clarification invokes one clarify command and ends without refreshed readiness or plan. |  unconditional plan/return/defer choice | Plan review, explicit defer, or end after one clarification return. |
| `speckit-flow-tasks` | Success is generated task proposal routed to Analyze after a human review | one tasks command. Return-to-plan invokes one plan command and ends; no regenerated tasks or coverage reassessment. |  task coverage/route | Analyze handoff, task amendment stop, defer, or end after one plan return. |
| `speckit-flow-analyze-remediate` | Success is clean analysis and stop for separately invoked Implement | Success is clean analysis and stop for separately invoked Implement. Routine routes classify analysis through a human gate, perform one minimal spec/plan/tasks correction sequence, then reanalyze once and terminate regardless of fresh result. Consequential/constitutional/scope/blocker routes stop explicitly. No loop or progress bound. Resumption evidence: core artifacts and controller summary; no repeated-pass state. | See route details. | Clean-analysis stop, one correction/reanalysis pass, or explicit constitutional/authority/blocker stop. |
| `speckit-flow-implement` | Success is implementation executed and stop for separately invoked Converge | Success is implementation executed and stop for separately invoked Converge. Routine results are classified by a human gate. Return branches run one Analyze/Specify/Plan/Tasks command and end without reconciliation or resumed implementation. No loop. Resumption evidence: changed artifacts, command evidence, and controller summary; no branch continuation marker. | See route details. | Converge handoff, one corrective command then end, or implementation blocker. |
| `speckit-flow-converge` | Success is a human-classified clean result and stop for separate Close Out. Remediation runs one Analyze command then stops for separate implementation and later Converge. No same-invocation analysis/implementation/reassessment loop. Human gate: clean/remediation/blocked classification. Resumption evidence: convergence output, tasks, controller summary; no loop progress record. | Success is a human-classified clean result and stop for separate Close Out. Remediation runs one Analyze command then stops for separate implementation and later Converge. No same-invocation analysis/implementation/reassessment loop. Human gate: clean/remediation/blocked classification. Resumption evidence: convergence output, tasks, controller summary; no loop progress record. |  clean/remediation/blocked classification | Clean stop, remediation stop after analysis, or blocker. |
| `speckit-flow-closeout` | Success is a current supported roadmap verification patch or evidence that the entry is already verified, reached after completion assessment and bounded debrief correction. Exact patch, wiki/lint, and commit-readiness decisions remain explicit. | Initial evidence assessment routes clean Draft-to-Complete, already-Complete debrief, ambiguous authority, and blockers; a five-pass loop refreshes findings, performs ordered corrections and debrief, and reassesses. | Two consequential gates, exact roadmap patch, and commit readiness. | Already verified; exact patch approved and follow-up wiki/lint/readiness; or specific authority, blocker, no-progress, repeated-finding, and cap stops. |

## Complete node and branch inventory

Each source step is listed in declaration order in its source package. Gate options, switch cases, bounded loops, and nested terminal routes are shown explicitly. The machine-checked projection below records each current package's complete graph counts.

### speckit-flow-analyze-remediate

**Version**: `0.3.0`. Run read-only analysis, route routine findings through the smallest artifact flow-back path, and stop for consequential decisions.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `analysis_disposition` (string; required=False)

**Steps and branches**:
- `analyze-artifacts` (command): command `speckit.analyze`; delegated to `Verifier`
- `classify-analysis-result` (gate): human gate: clean, routine-spec-flowback, routine-plan-flowback, routine-task-flowback, constitutional-stop, authority-or-scope-stop, blocked; Review the analysis report. Routine in-scope flow-back is automatic only through the named artifact path. Constitutional, authority, ambiguous-recovery, material-scope, and blocked results stop for the operator.
- `route-analysis-result` (switch): routes clean, routine-spec-flowback, routine-plan-flowback, routine-task-flowback, constitutional-stop, authority-or-scope-stop, blocked
  - Case `clean`:
    - `stop-analysis-clean` (prompt): main-task stop/prompt; Stop at Tasks Analyzed. The operator may invoke speckit-flow-implement for eligible work.
  - Case `routine-spec-flowback`:
    - `remediate-specification` (command): command `speckit.specify`; delegated to `Architect`
    - `replan-after-specification` (command): command `speckit.plan`; delegated to `Architect`
    - `retask-after-specification` (command): command `speckit.tasks`; delegated to `Architect`
    - `reanalyze-after-specification` (command): command `speckit.analyze`; delegated to `Verifier`
  - Case `routine-plan-flowback`:
    - `remediate-plan` (command): command `speckit.plan`; delegated to `Architect`
    - `retask-after-plan` (command): command `speckit.tasks`; delegated to `Architect`
    - `reanalyze-after-plan` (command): command `speckit.analyze`; delegated to `Verifier`
  - Case `routine-task-flowback`:
    - `remediate-tasks` (command): command `speckit.tasks`; delegated to `Architect`
    - `reanalyze-after-tasks` (command): command `speckit.analyze`; delegated to `Verifier`
  - Case `constitutional-stop`:
    - `stop-for-constitutional-approval` (prompt): main-task stop/prompt; Stop before changing the constitution. Report the finding, impact, and proposed amendment; obtain explicit approval through the separate constitutional workflow.
  - Case `authority-or-scope-stop`:
    - `stop-for-authority-or-scope-decision` (prompt): main-task stop/prompt; Stop before expanding authority or material scope, or resolving an ambiguous recovery case. Ask for the smallest explicit operator decision needed to continue.
  - Case `blocked`:
    - `stop-with-analysis-blocker` (prompt): main-task stop/prompt; Stop with the reported blocker and preserve the analysis evidence. Do not claim that implementation is ready.

**Observed terminal/continuation behavior**: Success is clean analysis and stop for separately invoked Implement. Routine routes classify analysis through a human gate, perform one minimal spec/plan/tasks correction sequence, then reanalyze once and terminate regardless of fresh result. Consequential/constitutional/scope/blocker routes stop explicitly. No loop or progress bound. Resumption evidence: core artifacts and controller summary; no repeated-pass state.


### speckit-flow-clarify

**Version**: `0.3.0`. Run one interactive clarification session, preserve incremental edits, and return an explicit continuation, planning, or deferral result.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `clarification_decision` (string; required=False)

**Steps and branches**:
- `clarify-specification` (command): command `speckit.clarify`; delegated to `Architect`
- `choose-clarification-result` (gate): human gate: continue-clarification, begin-planning, defer; Review resolved, outstanding, and deferred ambiguity. Continue another clarification session, accept planning readiness, or defer a bounded concern.
- `route-clarification-result` (switch): routes continue-clarification, begin-planning, defer
  - Case `continue-clarification`:
    - `stop-for-next-clarification-session` (prompt): main-task stop/prompt; Stop at the clarification loop-back. Start another speckit-flow-clarify run with the same active feature; do not claim that the specification is clarified merely because one session ended.
  - Case `begin-planning`:
    - `stop-for-human-planning-review` (prompt): main-task stop/prompt; Stop at Spec Clarified. The operator must re-read the specification and choose whether to invoke speckit-flow-plan.
  - Case `defer`:
    - `stop-with-explicit-deferral` (prompt): main-task stop/prompt; Stop after recording the bounded deferred ambiguity. Do not convert a deferred product decision into an automatic default.

**Observed terminal/continuation behavior**: Success is a human-selected planning-ready or deferred result after one clarification session. Routine work: one `speckit.clarify` command. The continue branch stops and requires a separate invocation; no in-run loop or residual-ambiguity assessment. Human gate: classify continue/planning/defer. Resumption evidence: updated spec and controller step summary; no session-count/progress evidence.


### speckit-flow-closeout

**Version**: `0.5.0`. Assess completion evidence, reconcile bounded debrief findings, and keep feature completion, roadmap verification, wiki maintenance, Git integration, and project acceptance distinct.

**Declared inputs**: `feature_context` (string; required=True; exact repository-relative spec directory), `integration` (string; required=False), `closeout_decision` (string; required=False), `roadmap_transition_decision` (string; required=False), `commit_readiness_decision` (string; required=False)

**Steps and branches**:
- `assess-closeout-readiness` (Verifier assessment): inspect current convergence, lifecycle status, and prior debrief evidence. A clearly clean Draft spec enters the bounded status-completion/debrief route; an already Complete spec proceeds to debrief without an availability gate; ambiguous authority reaches the initial consequential gate; untrusted or non-clean evidence stops.
- `route-initial-closeout` (switch): `continue` enters `closeout-debrief-loop`; `needs-human` reaches `closeout-initial-consequential-gate` (`defer`, `abort`); `blocked` reaches a specific stop. A current `already-verified` result can stop without a roadmap write.
- `closeout-debrief-loop` (`do-while`, maximum 5): `assess-closeout-before-pass` refreshes feature and debrief evidence and selects `mark-spec-complete`, `debrief-current-spec`, `reconcile-specification`, `reconcile-plan`, `reconcile-tasks`, or `implement-eligible`. The status route updates only the existing Draft spec in place, then runs a fresh debrief. Artifact correction follows spec→plan→tasks or plan→tasks order, analyzes changed tasks, verifies eligibility before implementation, and reruns debrief. Every pass ends with `assess-closeout-after-pass` against refreshed evidence.
- `route-final-closeout` (switch): a complete assessment with `patch-ready` reaches `approve-roadmap-transition`; `already-verified` stops cleanly; `needs-human` reaches `closeout-final-consequential-gate`; `blocked` and cap-exhausted continuation stop with a reason and resumption action.
- `approve-roadmap-transition` (gate): `approve-patch`, `return-to-workflow`, or `defer`. Only `approve-patch` invokes `speckit.flow-roadmap.write` with the exact approved proposal, then runs curated `speckit.flow-wiki.ingest`, `speckit.flow-wiki.lint`, and `confirm-commit-readiness` (`ready-for-explicit-commit`, `return-to-workflow`, `blocked`). Deferral and flow-back do not write the roadmap. The workflow does not commit or accept the feature.

**Observed terminal/continuation behavior**: Current supported debrief evidence reaches the exact roadmap patch gate; already verified evidence stops without a write. Routine correctable findings repeat only after measurable progress. Consequential ambiguity, stale/untrusted evidence, non-clean convergence, repeated findings, no progress, and the five-pass cap produce bounded stops. A roadmap write is possible only after exact patch approval; Git integration and acceptance remain separate.

## US1 Machine-Checked Projection and Comparison

The checker at [`tools/validate_workflows.py`](../../tools/validate_workflows.py) reads all eight source YAML packages, enumerates switch branches and nested loop bodies, records delegated assignments and human gates, and classifies terminal paths. Its projection is generated from current source; counts below are evidence from the current checkout, while the preceding inventory remains the pre-change behavior record.

| Workflow | Entry / first assessment | Nodes | Switch branches | Human gates | Continuation loops | Assignments | Bounded stops | Unexplained terminal paths |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `speckit-flow-start-feature` | `assess-eligibility` | 31 | 19 | 4 | 0 | 6 | 14 | 0 |
| `speckit-flow-clarify` | `assess-clarification-state` | 20 | 15 | 2 | 1 | 4 | 8 | 0 |
| `speckit-flow-plan` | `assess-plan-readiness` | 22 | 17 | 2 | 1 | 4 | 6 | 0 |
| `speckit-flow-tasks` | `assess-task-readiness` | 22 | 17 | 2 | 1 | 4 | 8 | 0 |
| `speckit-flow-analyze-remediate` | `assess-analysis` | 29 | 19 | 2 | 1 | 12 | 6 | 0 |
| `speckit-flow-implement` | `assess-implementation` | 35 | 21 | 2 | 1 | 18 | 7 | 0 |
| `speckit-flow-converge` | `assess-convergence` | 52 | 41 | 2 | 1 | 26 | 6 | 0 |
| `speckit-flow-closeout` | `assess-closeout-readiness` | 67 | 50 | 4 | 1 | 28 | 9 | 0 |

Start Feature now verifies the created spec directory against the exact selected roadmap entry after `speckit.specify`, before briefing. A unique exact mapping proceeds directly to the brief; a unique missing or stale mapping shows the exact patch for approval, writes only that patch, rechecks the mapping, and refreshes the brief. Conflicting or ambiguous ownership stops with evidence, and amend/defer branches do not write. The brief receives explicit `SPEC_TARGET` and `ROADMAP_ENTRY` constraints.

Tasks now assesses reviewed design and current task coverage before generating, without a routine confirmation. Its five-pass loop reassesses coverage, repeats only after a prior coverage gap is resolved, succeeds on complete current coverage, and stops specifically for a material design gap, substantive question, stale evidence, no progress, or the cap. Task review and Analyze remain separate operator actions. Converge now assesses before correction and runs a five-pass loop with distinct paths for task-only, task-artifact, plan, and specification gaps, plus already-analyzed implementation work. Changed higher-level artifacts flow through dependent plan and task reconciliation; changed tasks are analyzed before implementation, and implementation must have fresh eligibility evidence. A final convergence assessment continues only after a prior gap is resolved, otherwise it ends cleanly or stops with the exact decision or blocker. Neither workflow launches another FlowKit workflow.

The old Analyze and Implement classifiers and single-pass correction branches were replaced with initial evidence assessments, five-pass loop containers, fresh final assessments, and separate complete, consequential-gate, blocker, invalid-state, and loop-bound routes. Analyze preserves specification→plan→tasks→analysis ordering and changes no implementation. Implement preserves dependency reconciliation, requires fresh analysis before resumed implementation, and stops at its own success; Converge remains a separately invoked workflow. All assignments are checked across both switch alternatives and loop bodies.

Plan's `return-to-clarification` and Tasks' `return-to-plan` leaves in the pre-change inventory are classified as bounded return stops. The current Plan and Tasks loops supersede those baseline routes. New terminal paths still fail classification unless they declare a recognizable success, stop, gate, or explicitly gated return command. The checker reports Close Out and Plan's gate as entry points rather than fabricating assessment nodes; the baseline inventory records their pre-change behavior.


### speckit-flow-converge — Pre-Change Definition

**Version**: `0.3.0`. Assess implementation against the current feature artifacts, route bounded remediation through analysis, and stop cleanly or with a blocker.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `convergence_result` (string; required=False)

**Steps and branches**:
- `assess-convergence` (command): command `speckit.converge`; delegated to `Verifier`
- `classify-convergence-result` (gate): human gate: clean, remediation, blocked; Review convergence evidence. A clean result exits converged. New remediation Tasks return through ordinary task analysis and implementation before convergence resumes.
- `route-convergence-result` (switch): routes clean, remediation, blocked
  - Case `clean`:
    - `stop-converged` (prompt): main-task stop/prompt; Stop at Feature Converged. The operator may invoke speckit-flow-closeout; convergence is not Git integration or project acceptance.
  - Case `remediation`:
    - `return-remediation-to-analysis` (command): command `speckit.analyze`; delegated to `Architect`
    - `stop-for-remediation` (prompt): main-task stop/prompt; Pause convergence after analysis. Return to the implementation workflow for eligible remediation Tasks, then resume speckit-flow-converge.
  - Case `blocked`:
    - `stop-with-convergence-blocker` (prompt): main-task stop/prompt; Stop with the convergence blocker and preserve evidence.

**Observed terminal/continuation behavior**: Success is a human-classified clean result and stop for separate Close Out. Remediation runs one Analyze command then stops for separate implementation and later Converge. No same-invocation analysis/implementation/reassessment loop. Human gate: clean/remediation/blocked classification. Resumption evidence: convergence output, tasks, controller summary; no loop progress record.


### speckit-flow-implement

**Version**: `0.3.0`. Implement remaining eligible tasks under the current human-selected agent and return execution, flow-back, or blocker evidence.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `implementation_result` (string; required=False)

**Steps and branches**:
- `implement-eligible-work` (command): command `speckit.implement`; delegated to `Builder`
- `classify-implementation-result` (gate): human gate: converge, return-to-analysis, return-to-specification, return-to-plan, return-to-tasks, blocked; Review implementation evidence. Continue to convergence only when eligible work is executed; otherwise return through the named flow-back path or stop with the blocker.
- `route-implementation-result` (switch): routes converge, return-to-analysis, return-to-specification, return-to-plan, return-to-tasks, blocked
  - Case `converge`:
    - `stop-for-convergence` (prompt): main-task stop/prompt; Stop at Implementation Executed. The operator may invoke speckit-flow-converge; this workflow does not select or launch a follow-on agent.
  - Case `return-to-analysis`:
    - `return-to-analysis` (command): command `speckit.analyze`; delegated to `Architect`
  - Case `return-to-specification`:
    - `return-to-specification` (command): command `speckit.specify`; delegated to `Architect`
  - Case `return-to-plan`:
    - `return-to-plan` (command): command `speckit.plan`; delegated to `Architect`
  - Case `return-to-tasks`:
    - `return-to-tasks` (command): command `speckit.tasks`; delegated to `Architect`
  - Case `blocked`:
    - `stop-with-implementation-blocker` (prompt): main-task stop/prompt; Stop with the blocking issue and required operator input. Do not expand implementation scope silently.

**Observed terminal/continuation behavior**: Success is implementation executed and stop for separately invoked Converge. Routine results are classified by a human gate. Return branches run one Analyze/Specify/Plan/Tasks command and end without reconciliation or resumed implementation. No loop. Resumption evidence: changed artifacts, command evidence, and controller summary; no branch continuation marker.


### speckit-flow-plan

**Version**: `0.3.0`. Create implementation design artifacts only after human confirmation that the clarified specification is ready for planning.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `plan_review_decision` (string; required=False)

**Steps and branches**:
- `confirm-planning-readiness` (gate): human gate: plan, return-to-clarification, defer; Confirm that the specification was reviewed after clarification and is ready for technical planning. Return to clarification for missing prerequisites or material product ambiguity.
- `route-planning-readiness` (switch): routes plan, return-to-clarification, defer
  - Case `plan`:
    - `create-plan` (command): command `speckit.plan`; delegated to `Architect`
    - `stop-for-plan-review` (prompt): main-task stop/prompt; Stop at Design Planned. The operator reviews plan, research, data model, contracts, and quickstart before choosing speckit-flow-tasks.
  - Case `return-to-clarification`:
    - `return-to-clarification` (command): command `speckit.clarify`; delegated to `Architect`
  - Case `defer`:
    - `stop-with-deferred-plan` (prompt): main-task stop/prompt; Stop without creating planning artifacts. Record the deferred planning decision and retain the manual prompt as fallback.

**Observed terminal/continuation behavior**: Success is planning artifacts after the operator confirms readiness. Routine work: plan command, then stop for plan review. Return-to-clarification invokes one clarify command and ends without refreshed readiness or plan. Human gate: unconditional plan/return/defer choice. Resumption evidence: current artifacts and controller summary; no re-entry marker.


### speckit-flow-start-feature

**Version**: `0.4.0`. Prepare one uniquely eligible roadmap feature through an approval-gated roadmap transition, cited context, specification, and roadmap brief.

**Declared inputs**: `feature_request` (string; required=True), `integration` (string; required=False), `roadmap_decision` (string; required=False), `final_review_decision` (string; required=False)

**Steps and branches**:
- `assess-eligibility` (prompt): main-task stop/prompt; delegated to `Architect`; Assess the roadmap for one uniquely eligible feature matching: {{ inputs.feature_request }}. Read dependencies and governing context. Prepare an exact proposed status patch only; do not mutate the roadmap. Stop if eligibility is ambiguous, dependencies are unsatisfied, or governing context is incomplete.
- `approve-roadmap-patch` (gate): human gate: approve, amend-roadmap, resolve-context, defer; Review the exact roadmap patch and context coverage. Approve only a uniquely eligible, exact patch; otherwise amend the roadmap, resolve context, or defer.
- `route-roadmap-decision` (switch): routes approve, amend-roadmap, resolve-context, defer
  - Case `approve`:
    - `apply-approved-roadmap-patch` (command): command `speckit.flow-roadmap.write`
    - `retrieve-governing-context` (command): command `speckit.flow-wiki.query`
    - `draft-specification` (command): command `speckit.specify`; delegated to `Architect`
    - `brief-against-roadmap` (command): command `speckit.flow-roadmap.brief`; delegated to `Verifier`
    - `review-specification-and-brief` (gate): human gate: clarify, amend-roadmap, resolve-context, begin-planning, defer; Review the specification and roadmap brief. Choose the next human-directed state; this workflow does not start it automatically.
  - Case `amend-roadmap`:
    - `stop-for-roadmap-amendment` (prompt): main-task stop/prompt; Stop the start-feature workflow. Prepare a new exact approval-gated roadmap amendment; do not invent a replacement feature.
  - Case `resolve-context`:
    - `stop-for-context-resolution` (prompt): main-task stop/prompt; Stop the start-feature workflow. Report the missing or partial wiki coverage and the smallest evidence or human decision needed to continue.
  - Case `defer`:
    - `stop-with-deferred-feature` (prompt): main-task stop/prompt; Stop the start-feature workflow without changing roadmap, feature, branch, or specification state. Record that the operator deferred the candidate.

**Observed terminal/continuation behavior**: Success is gated review of the drafted specification and roadmap brief. Routine automation: initial eligibility assessment followed by approved roadmap write, wiki query, spec creation, and brief; there is no post-spec linkage repair or re-brief loop. Human gates: exact initial roadmap patch and final spec/brief routing. Stops: amend roadmap, resolve context, defer, or invalid choice. Resumption evidence: current controller run summary and roadmap/spec artifacts; no workflow-specific resumption contract.


### speckit-flow-tasks — Pre-Change Definition

**Version**: `0.3.0`. Generate tasks from reviewed design artifacts, surface surprising human work, and route readiness to analysis rather than implicit edits.

**Declared inputs**: `feature_context` (string; required=True), `integration` (string; required=False), `task_review_decision` (string; required=False)

**Steps and branches**:
- `generate-tasks` (command): command `speckit.tasks`; delegated to `Architect`
- `review-task-proposal` (gate): human gate: analyze, return-to-plan, amend-tasks, defer; Review task coverage and any surprising human-operator actions. Send an acceptable proposal to analysis, return design gaps to planning, or defer.
- `route-task-review` (switch): routes analyze, return-to-plan, amend-tasks, defer
  - Case `analyze`:
    - `stop-for-analysis` (prompt): main-task stop/prompt; Stop at Tasks Proposed. Invoke speckit-flow-analyze-remediate next; do not begin implementation directly.
  - Case `return-to-plan`:
    - `return-to-plan` (command): command `speckit.plan`; delegated to `Architect`
  - Case `amend-tasks`:
    - `stop-for-task-amendment` (prompt): main-task stop/prompt; Stop for an explicit task amendment. Do not silently change the plan or bypass the normal analysis path.
  - Case `defer`:
    - `stop-with-deferred-tasks` (prompt): main-task stop/prompt; Stop without treating the task proposal as analysis-ready.

**Observed terminal/continuation behavior**: Success is generated task proposal routed to Analyze after a human review. Routine work: one tasks command. Return-to-plan invokes one plan command and ends; no regenerated tasks or coverage reassessment. Human gate: task coverage/route. Resumption evidence: tasks/plan artifacts and controller summary; no loop state.

## Pre-Change Cross-Workflow Findings

- At the pre-change baseline, all eight packages were ordered prompt/command/gate/switch graphs with no explicit loop. Routine result classification was performed by gates in Analyze, Clarify, Tasks, Converge, Implement, and Close Out; Plan also had an unconditional readiness gate.
- Corrective branches generally ran one command or one short ordered artifact sequence and then terminated. Only Analyze ran a fresh analysis once, with no route from that result back into the graph.
- No pre-change branch automatically invoked another FlowKit workflow; command steps could invoke core Specify commands within the current workflow.
- The pre-change direct controller preflighted graph syntax and named assignments, started one child for each delegated command, routed explicit gates in the main task, and persisted step-boundary summaries. Recovery had no iteration-aware record or artifact-based progress test.
- Pre-change named assignments were: Architect for design/correction commands; Builder for implementation and Close Out wiki ingestion; Verifier for assessment and lint; no workflow delegated to Coder. The Implement return-to-analysis step used Architect while Analyze commands used Verifier; Close Out wiki ingestion used Builder.

## Pre-Change Assignment Baseline

| Workflow | Delegated step IDs and current names |
|---|---|
| `speckit-flow-analyze-remediate` | `analyze-artifacts`: Verifier; `remediate-specification`: Architect; `replan-after-specification`: Architect; `retask-after-specification`: Architect; `reanalyze-after-specification`: Verifier; `remediate-plan`: Architect; `retask-after-plan`: Architect; `reanalyze-after-plan`: Verifier; `remediate-tasks`: Architect; `reanalyze-after-tasks`: Verifier
| `speckit-flow-clarify` | `clarify-specification`: Architect
| `speckit-flow-closeout` | `debrief-roadmap`: Verifier; `ingest-curated-context`: Builder; `lint-wiki`: Verifier
| `speckit-flow-converge` | `assess-convergence`: Verifier; `return-remediation-to-analysis`: Architect
| `speckit-flow-implement` | `implement-eligible-work`: Builder; `return-to-analysis`: Architect; `return-to-specification`: Architect; `return-to-plan`: Architect; `return-to-tasks`: Architect
| `speckit-flow-plan` | `create-plan`: Architect; `return-to-clarification`: Architect
| `speckit-flow-start-feature` | `assess-eligibility`: Architect; `draft-specification`: Architect; `brief-against-roadmap`: Verifier
| `speckit-flow-tasks` | `generate-tasks`: Architect; `return-to-plan`: Architect

**Validation limit**: This inventory is a static source-graph review. It does not demonstrate live native-agent selection, successful workflow execution, or consumer behavior. Those require the planned tests and disposable-consumer checks after the roadmap scope gate is resolved.
