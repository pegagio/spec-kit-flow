# Feature 014 Research: Workflow Continuation and Agent Assignments

The initial decisions were based on the original eight source workflow definitions, the F014 specification and clarifications, approved Constitution 6.0.0, the direct Codex controller, and the selected Specify CLI `1.0.10.dev0+pegagio.2`. They guide planning; they do not authorize workflow source or roadmap changes.

## Decision: Review all eight workflows as bounded control loops

Each workflow needs an explicit success condition, evidence-based routine routing, human decision points, continuation edge, and safe stop. A workflow may perform its own reviewed corrective steps and reassess within one invocation; it does not call another FlowKit workflow or start the next phase. The historical [baseline](workflow-review-baseline.md) shows one-pass fall-through or stop paths in every workflow. The operator approved the exact all-eight-workflow scope amendment; source changes may proceed within that scope.

**Rationale**: The recorded F014 issues share a control-flow cause: a corrective command or review runs once, then the graph ends without evaluating fresh evidence. **Alternatives considered**: Keep separate invocations after every routine correction; the operator rejected this as premature termination. Hide continuation in a child prompt; that would make control flow difficult to review and validate.

## Decision: Use Specify's existing `do-while` step for reviewed cycles

The selected Specify runtime accepts `type: do-while` with nested `steps`, one complete `{{ ... }}` condition expression, and `max_iterations` of at least one. A minimal five-iteration graph validated under the selected runtime. The body runs once before the condition is checked. The approved implementations use either a core-skill-first output loop, an explicitly read-only first baseline pass, or source-command assessment before a guarded correction. Entry behavior is defined per workflow, rather than requiring a separate initial wrapper assessment. After the initial declared pass, only validated continuation with the required progress permits further work. F014 should use this existing step type only where an in-scope routine result requires repetition. The original five-body-pass starting bound was refined to the exact per-workflow caps in the plan, including six-check correction modes and the 26-check wiki-source loop. When the condition still requests work at the cap, report a bounded stop, not success; preserve the latest evidence and a safe resumption point.

At the pre-change baseline, the FlowKit controller validated only `prompt`, `command`, `gate`, and `switch`, and its template checker does not accept a comparison expression. F014 extended controller graph validation, rendering, branch processing, and protocol instructions to understand the built-in `do-while` shape and the narrow condition grammar actually used. The installed Specify definition remains the source of steps, gates, and loop bounds. Native Specify loader acceptance is structural evidence; direct Codex behavior needs its own validation.

**Rationale**: Reusing the pinned workflow format avoids a new language or dependency and keeps loop policy visible in reviewed YAML. **Alternatives considered**: A new `loop` or `repeat` step type is unsupported by the pinned registry. Duplicating five copies of each branch would obscure maintenance and evidence. An unmodeled main-task retry would make installed YAML cease to be the behavior authority.

## Decision: Classify outcomes through a small, validated evidence contract

For routine routing, an assessment step should produce a machine-checkable outcome with `complete`, `continue`, `needs-human`, or `blocked`; a reason code; repository-relative evidence references; and the remaining finding or work identifiers. Workflow-specific step outputs may carry additional data outside the strict generic envelope, but a command exit code or changed file alone cannot declare success. The controller validates the envelope before selecting a branch. If the source command emits prose, a reviewed assessment step may translate current artifacts into the envelope; it must cite inspectable evidence and stop on an untrustworthy or contradictory result. Consequential decisions remain main-task gates.

**Rationale**: Current YAML often asks the operator to classify routine results, and current controller output references have no cross-workflow outcome type. A small envelope makes routing testable without copying workflow prompts into the controller. **Alternatives considered**: Parse arbitrary prose for keywords; too fragile for authority decisions. Treat command success as completion; contradicted by observed one-pass failures and the constitution.

## Decision: Continue on semantic progress, with a finite safety bound

Each loop defines the artifact set and finding/work identifiers it is trying to improve. [The plan](plan.md#loop-entry-and-progress) specifies the evidence and progress signal for each workflow. A pass makes progress only when it resolves at least one prior in-scope finding or completes an eligible task and the refreshed evidence confirms that change. A file digest changing by itself is insufficient. Repeated unresolved findings without material change, no progress, stale snapshots, failed prerequisites, or an untrustworthy delta stop immediately. The per-workflow finite cap remains an independent safety bound even while progress continues. A later operator invocation may resume from preserved evidence after a bounded stop; there is no unattended retry.

**Rationale**: This matches the operator's progress-based choice while preventing endless retries and false success. **Alternatives considered**: A fixed small retry count as the only rule can interrupt useful progress; an uncapped progress rule can run indefinitely.

## Decision: Make repeated-pass recovery iteration-aware

The pre-change recovery summary stored `steps` by step ID, so a second pass would overwrite the first. The F014 design records each pass under a loop ID and iteration number, with step IDs, statuses, outcome/reason codes, relevant evidence fingerprints, and changed repository-relative paths. It must remain compact, local, and transcript-free. A new child is launched for each delegated executable step in each pass; an interactive question and answer stay with that step's active child. Interruption or installation refresh still stops at the next safe boundary and preserves the record.

**Rationale**: A bounded loop is reviewable only if the operator can see what changed between passes and why it stopped. **Alternatives considered**: Overwrite `steps[step_id]`; loses history. Store raw child transcripts; violates the existing recovery boundary.

## Decision: Keep agent configuration local to this repository for F014

The operator selected task-specific work labels: Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator. The current workflow source uses Architect, Builder, and Verifier across delegated branches; the only tracked local agent file is a temporary Coder launch probe. F014 reviews every assignment by responsibility, supplies usable native Codex files for the selected names, and replaces probe-only instructions. Existing all-branch preflight and exact native selection remain. Catalog install, refresh, and removal do not own or alter consumer agent files; the operator left that possibility to a later feature. Independent review uses existing assessment nodes; this role reassignment adds no workflow nodes.

**Rationale**: It enables the source checkout to dogfood its workflows without changing Feature 015's consumer ownership contract. **Alternatives considered**: Automatically install agent files with the bundle; outside F014 and contrary to the current ownership boundary. A FlowKit role map; previously rejected as duplicate configuration.

## Decision: Apply approved authority and preserve remaining gates

Approved Constitution 6.0.0 permits declared, bounded core-command analysis, implementation, and reassessment within an operator-invoked workflow; another FlowKit workflow remains separately invoked. The operator explicitly selected F014's repeated Clarify-session policy and evidence-backed Close Out Draft-to-Complete rule. These are prospective changes to future source, not edits to verified Feature 007/008 history. The operator approved the all-eight-workflow scope amendment before expanded source changes.

**Rationale**: The constitutional change was separately approved and the F014 clarification answers settle the feature-specific continuation choices. Exact roadmap patches, material scope, substantive answers, Git integration, and acceptance remain human gates. **Alternatives considered**: Treat the F014 draft or passing tests as authority to override the prior constitution; that would bypass explicit human gates.

## Accepted refinements from workflow review

Core skills already own prerequisite discovery and their substantive questions. Clarify starts with its session, Plan and Tasks combine structural checks with independent Reviewer semantic assessment and return exact located findings to Planner/Tasker through existing author-owned correction paths, and Implement repeats existing eligible work without adding re-specification, re-planning, re-tasking, analysis, or a Codex goal. A goal is not required for continuity when the reviewed graph and controller enforce continuation and bounded stops.

Analyze and Remediate shares one waterfall with different entry points and one analyzer/assessment. Converge records remediation tasks on every permitted correction, then enters the same layer ordering before task analysis, eligibility, implementation, and fresh convergence. Close Out uses that ordering for debrief corrections and a separate bounded wiki loop. Duplicate routing states and stop-only human gates are replaced by completed-evidence joins and blocked recovery questions where no consequential approval is needed.

Selection and specification authoring have distinct intent and are separately invoked. Read-only dependency discussion and exact selection/activation precede any authoring. Start Feature is retained only to report deprecation. Wiki Lint Update is a separately invoked wiki-scope loop; all findings remain visible while registered authorized sources are refreshed individually. A project-owned rendering skill makes graph structure inspectable with exact source terms.

**Semantic-review tradeoff**: Reuse the existing assessment nodes and bounded author correction paths instead of adding review nodes or a blanket operator review gate. This preserves topology and independent responsibility while requiring findings to identify actual semantic deficiencies, including populated artifacts. Structural-only success misses contradictory designs or tasks; unrestricted reviewer rewriting weakens author ownership. Fresh confirmation of prior finding resolution, finite caps, and operator-owned product answers constrain this approach. Validation must exercise exact finding handoff, successful repair, repeated/no-progress findings, cap exhaustion, and unanswered product questions; current static and snapshot evidence does not itself prove those scenarios.

These refinements supersede the original entry/gate assumptions. Baseline source digests remain historical; current provenance, implementation coverage, and unresolved delivery are recorded in the reconciliation record and current inventory.
