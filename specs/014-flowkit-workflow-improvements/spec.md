# Feature Specification: FlowKit Workflow Improvements

**Feature Branch**: `develop` (no feature branch created)

**Created**: 2026-09-29

**Status**: Draft

**Input**: Review all eight FlowKit workflows so each has the right gates, automation, continuation paths, and bounded stops to reach a sound conclusion; incorporate Feature 015's named-agent design, build usable agent configurations, and address the recorded workflow issues as symptoms of incomplete continuation.

## Clarifications

### Session 2026-09-29

- Q: Should an invoked workflow run its own reviewed corrective steps and reassess until success, a required human decision, or a bounded stop, without invoking another FlowKit workflow? → A: Yes; continue through steps defined in the current workflow.
- Q: If a five-question Clarify session ends but significant ambiguity remains, should the already-invoked Clarify workflow start another bounded session without a new invocation? → A: Yes; continue within the current invocation while each substantive answer remains human-provided.
- Q: Where should F014 deliver the new Codex agent configurations needed by the reviewed workflows? → A: Add usable agent files to this repository only; leave consumer bundle installation for a possible later feature.
- Q: When Close Out finds a cleanly converged feature whose specification is still Draft, should its invocation authorize changing the specification to Complete before debrief? → A: Yes, when completion evidence is clear; stop on ambiguity and keep roadmap verification separately approved.
- Q: When a workflow repeats a corrective pass, what should determine when it stops trying within the current invocation? → A: Continue while each pass makes measurable progress, stop on repeated findings or no progress, and enforce a finite safety cap.

## User Scenarios & Testing

The operator invokes each workflow separately. The primary delivery is a step-by-step review of all eight workflows as complete control loops. Routine evidence-backed work should continue within an invoked workflow until its defined success, human decision, or genuine blocker, subject to reviewed authority.

### User Story 1 - Review Every Workflow End to End (Priority: P1)

A maintainer can trace each of the eight FlowKit workflows from invocation to every possible terminal result. Each routine outcome has evidence-based routing and a bounded continuation when further in-scope work is needed. A human gate appears where the operator must decide, and a stop explains what input or authority is missing.

**Independent Test**: For each workflow, enumerate all branch outcomes and run representative successful, remediable, blocked, and consequential-decision cases against its manual and direct Codex paths.

**Acceptance Scenarios**:

1. **Given** an operator-invoked workflow with routine in-scope work remaining, **when** a step produces a remediable result, **then** the workflow continues or loops using current evidence until its defined conclusion or bounded stop.
2. **Given** a consequential operator decision, **when** the workflow reaches it, **then** the main task presents the exact decision and waits instead of inferring approval.
3. **Given** a genuine blocker, repeated finding, stale evidence, or lack of progress, **when** continuation cannot be trusted, **then** the workflow stops with a specific reason, preserved work, and a resumption point.
4. **Given** a successful terminal result, **when** the workflow finishes, **then** it reports that workflow's conclusion without launching the next phase or implying acceptance, roadmap verification, or Git integration.

### User Story 2 - Start with Reliable Roadmap Linkage (Priority: P1)

The former Start Feature is split into Select Feature and Specify. Selection lists candidates, dependency chains, immediate unlocks, and downstream dependents; the human discusses and chooses one exact feature. Exact approval authorizes its roadmap delta and active `.specify/feature.json` pointer. It never creates a feature directory or writes a specification, and preserves existing spec bytes. Specify is separately invoked, consumes that pointer and unique roadmap mapping, retrieves context, authors the exact target, verifies linkage, and runs the shared brief. The combined workflow is deprecated and excluded from active bundle/controller bindings.

**Independent Test**: Start a feature in a disposable project with a unique eligible entry, then repeat with absent, stale, and conflicting specification-directory mappings.

**Acceptance Scenarios**:

1. **Given** an eligible entry and approved start patch, **when** the specification directory is known, **then** the brief resolves that specification to the intended entry.
2. **Given** a missing mapping, **when** linkage is proposed, **then** the operator sees an exact roadmap patch and no mapping changes before approval.
3. **Given** stale or conflicting mappings, **when** a unique link cannot be established, **then** the workflow stops with the evidence and a recoverable next action.
4. **Given** several candidates or no eligible candidate, **when** Start begins, **then** it shows dependency readiness and downstream impact and waits for an exact human selection or deferral without choosing or changing roadmap state.

### User Story 3 - Assess Clarification and Planning Readiness (Priority: P1)

After clarification, the operator receives an evidence-backed assessment of remaining significant ambiguity. A separate planning invocation delegates to the existing planning skill, which owns prerequisite checks, research, design generation, and constitutional gates.

**Independent Test**: Exercise clarified, materially ambiguous, and missing-prerequisite specifications through separate Clarify and Plan runs.

**Acceptance Scenarios**:

1. **Given** a clarification session reaches its five-question limit, **when** significant ambiguity remains, **then** the workflow assesses the remaining questions and starts another bounded session within the current invocation; each substantive answer still comes from the operator.
2. **Given** a reviewed specification without material product ambiguity, **when** the operator invokes Plan, **then** planning proceeds without a routine readiness confirmation.
3. **Given** a missing prerequisite or material product ambiguity, **when** the core planning skill encounters it, **then** the workflow reports the exact blocker or operator question without choosing a product answer.

### User Story 4 - Generate and Assess Tasks (Priority: P1)

The operator invokes Tasks for a reviewed plan. The workflow invokes the core task skill, verifies generation output, and retries exact output or coverage gaps while progress is verified. The operator may review it and separately invoke Analyze.

**Independent Test**: Run Tasks with complete design artifacts and with a material design gap; inspect generation, coverage, and the resulting stop or success.

**Acceptance Scenarios**:

1. **Given** reviewed design without a material gap, **when** the operator invokes Tasks, **then** generation begins without an extra routine pre-generation question.
2. **Given** complete generated coverage, **when** the agent assesses tasks, **then** the workflow exits successfully without a routine post-generation human gate.
3. **Given** missing coverage or a material design gap, **when** tasks are assessed, **then** the workflow reports the exact gap without beginning implementation.

### User Story 5 - Converge Through Bounded Remediation (Priority: P1)

The operator invokes Converge for one selected feature. Every pass invokes `speckit.converge` and classifies its fresh report before entering a shared specification → plan → tasks correction waterfall, fresh task analysis, one eligibility check, and eligible implementation. Implementation returns directly to the core convergence command. Loop control checks progress before further correction and permits a final convergence check after the fifth correction. Task history is preserved; analysis or implementation blockers and required operator decisions stop immediately and propagate to the final report. Constitution 6.0.0 permits these declared, bounded steps within the selected scope without authorizing another FlowKit workflow.

**Independent Test**: Exercise clean, task-only gap, changed-behavior gap, blocked, and repeated-gap cases, including analysis before implementation and reassessment after changes.

**Acceptance Scenarios**:

1. **Given** a clean assessment, **when** Converge runs, **then** it reports clean and stops for separately invoked Close Out.
2. **Given** an in-scope gap, **when** remediation changes tasks or higher-level intent, **then** affected artifacts are reconciled and changed tasks pass analysis before implementation resumes.
3. **Given** eligible analyzed fixes, **when** they are implemented, **then** Converge reassesses current artifacts and implementation within the same invocation.
4. **Given** a consequential decision, stale evidence, repeated finding, or lack of progress, **when** continuation is unsafe, **then** it stops with the exact reason and preserves work.

### User Story 6 - Close Out with Evidence and Debrief Continuation (Priority: P1)

The operator invokes Close Out for a converged feature. Clear completion evidence avoids a redundant availability question. Routine correctable debrief findings are reconciled and reassessed within the invocation; the exact roadmap verification patch still requires approval.

**Independent Test**: Exercise already-complete and authorized in-place completion states, ambiguous authority, a correctable debrief finding, and a repeated finding.

**Acceptance Scenarios**:

1. **Given** inspectable completion evidence, **when** Close Out checks the feature, **then** it continues without asking the operator to classify operation availability.
2. **Given** a cleanly converged feature whose specification is still Draft, **when** completion evidence is clear, **then** Close Out changes the existing specification to Complete and debriefs the refreshed feature state without a separate status-edit approval.
3. **Given** a routine correctable finding, **when** it is reconciled in scope, **then** Close Out refreshes evidence and repeats debrief before proposing a patch.
4. **Given** a material decision, untrustworthy delta, repeated finding, or no progress, **when** continuation is unsafe, **then** it stops without applying a roadmap patch.
5. **Given** current trusted evidence of existing roadmap verification, **when** Close Out runs, **then** it skips the verification write but still maintains curated wiki context and checks lint before commit-readiness reporting.
6. **Given** blocked task eligibility or an unresolved implementation question, **when** correction cannot safely continue, **then** the shared report preserves the question and recovery action without another debrief.
7. **Given** an initial stop or already-verified shortcut, **when** outcome preparation runs, **then** it uses completed evidence without referencing a skipped loop output.

### User Story 7 - Assign Usable Agents to Delegated Steps (Priority: P1)

The operator can inspect the agent selected for every delegated step and use each reviewed name in this repository's own Codex checkout. Assignments reflect the step's responsibility, while gates and main-task steps remain with the controller. The four Feature 015 names are the starting set; an additional name is proposed only when the review shows a distinct role that the four cannot express clearly.

**Independent Test**: Inventory all delegated steps and native agent files, review each assignment against its step purpose, then probe every distinct name used by every workflow branch in a disposable consumer and this source checkout.

**Acceptance Scenarios**:

1. **Given** a delegated step, **when** its workflow is reviewed, **then** the step has one justified, exact reviewed agent name and can be dispatched without a fallback.
2. **Given** a gate or main-task step, **when** assignments are reviewed, **then** it remains in the main task and receives no child assignment.
3. **Given** a name beyond Architect, Builder, Coder, and Verifier is proposed, **when** it is reviewed, **then** its distinct purpose and configuration are approved before the name appears in workflow source.
4. **Given** this repository's Codex checkout, **when** each used agent is probed, **then** its native configuration is usable; temporary probe instructions are not mistaken for production behavior.

### Edge Cases

- A correct active feature pointer exists but the roadmap lacks `Spec dir`; conflicting candidates must not be hidden by a number match.
- Clarify ends with no questions while the specification still contains a significant unresolved product choice.
- A task-generation child asks for a new design choice; invocation does not supply that answer.
- A Converge command succeeds while the current assessment remains blocked; command success does not prove clean convergence.
- A discovery changes intended behavior or technical approach; dependent artifacts and analysis must be refreshed before implementation resumes.
- A Close Out debrief uses a stale snapshot after artifact correction; it must be rerun against current evidence.
- An Analyze return branch performs one corrective step but leaves fresh findings or downstream artifacts unresolved; Analyze must route from the new evidence rather than report premature success. Implement may stop after a core-skill session while eligible tasks remain; the wrapper checks task and validation evidence and repeats the core skill while progress is verified.
- A delegated name exists in workflow source but has no usable native agent configuration in the current checkout; preflight must stop specifically, and the feature review must supply or revise that configuration through its own reviewed change.
- An agent name is technically available but poorly matched to a step's responsibility; availability alone does not make the assignment correct.

## Requirements

Constitution 6.0.0 prospectively permits declared, bounded correction and reassessment inside an operator-invoked workflow while preserving separate FlowKit workflow invocation. Feature 014 changes future behavior without rewriting verified Feature 007 or 008 history. The operator's F014 clarification answers select the repeated Clarify-session policy and evidence-backed Close Out completion rule; exact roadmap patches and other consequential decisions retain their own gates.

### Functional Requirements

- **FR-001**: Feature 014 MUST preserve separate operator invocation of workflow phases and usable manual paths. Completing one workflow MUST NOT silently launch a later workflow.
- **FR-002**: Select Feature MUST present candidates and dependency impact, allow discussion before an explicit human choice, and activate only the exactly approved unique roadmap target through `.specify/feature.json` without creating or modifying a specification. Specify MUST consume that active target, pass `SPECIFY_FEATURE_DIRECTORY` explicitly, author or revise only its specification, and establish a uniquely matched roadmap brief or report a specific linkage blocker. Mapping and lifecycle changes require exact roadmap patch approval. The combined Start Feature MUST be deprecated and perform no work.
- **FR-003**: Clarify MUST assess remaining significant ambiguity from current specification evidence after each bounded session, explain its findings, and continue with another bounded session in the same invocation when specific significant questions remain. The five-question command cap remains per session, substantive answers remain operator-provided, and the workflow MUST stop on a reviewed safety bound, lack of progress, or a consequential decision rather than equating the cap or an empty question set with readiness.
- **FR-004**: Clarify MUST keep substantive operator questions and routing in the main task and MUST NOT launch Plan.
- **FR-005**: Plan MUST invoke `speckit.plan` for the selected reviewed specification and present the resulting design artifacts or exact blocker. The core skill owns prerequisite checks, research, design generation, and constitutional gates. The wrapper MUST check that required and applicable output artifacts are present and populated, then feed exact missing files or placeholder sections back into the core skill while output gaps are being resolved. It MUST preserve completed design, accept justified not-applicable sections, and stop for operator input, blockers, no progress, or the reviewed safety bound. This is output verification, not design review. Substantive product decisions remain operator-provided and Tasks remains separately invoked.
- **FR-006**: Tasks MUST treat invocation as authorization to generate from reviewed design without a routine pre-generation confirmation; a material design gap MUST cause a specific stop.
- **FR-007**: Tasks MUST wrap `speckit.tasks` in a bounded output-verification loop: prepare exact gaps, invoke the core skill, verify tasks.md is populated with required format, sections, and story/dependency coverage, then retry remaining gaps while progress is verified. Retries MUST preserve existing task IDs, completion markers, completed work, and reviewed design. Unchecked implementation tasks MUST NOT count as incomplete generation. Operator input, material design gaps, missing prerequisites, no progress, or the reviewed cap cause a specific stop. Task review, Analyze, and implementation remain separate operator actions.
- **FR-008**: Converge MUST classify clean, remediable, and blocked outcomes from inspectable current evidence without asking the operator to classify routine results.
- **FR-009**: An invoked Converge run MUST stay within selected feature and task scope, append bounded remediation tasks, reconcile accepted changes through affected spec, plan, and task artifacts, analyze changed tasks, implement eligible fixes, and reassess until clean or a bounded stop.
- **FR-010**: Converge MUST stop on consequential decisions, ambiguous recovery, failed prerequisites, repeated findings, lack of progress, or an exhausted reviewed iteration bound; preserve partial work and explain the blocker. Successful commands alone MUST NOT establish a clean result.
- **FR-011**: A clean Converge result MUST NOT start Close Out, change roadmap status, integrate Git, or accept the feature.
- **FR-012**: The Converge correction, analysis, implementation, and reassessment steps MUST be declared in the installed workflow definition, bounded to the operator-selected feature and tasks, and preserve every consequential human gate. They MUST NOT invoke another FlowKit workflow, expand material scope, or change verified Feature 007 history.
- **FR-013**: A Close Out invocation MUST assess the selected feature's convergence and completion state from inspectable evidence. When the feature is cleanly converged and its existing specification is Draft, Close Out MUST update that specification in place to Complete and debrief the refreshed state without a separate status-edit or operation-availability gate. It MUST recognize an already Complete specification, stop specifically when completion authority or evidence is ambiguous, and MUST NOT substitute feature creation for completion. This prospective Feature 014 rule replaces the prior operation-availability route without rewriting verified Feature 008 history.
- **FR-014**: Within reviewed Close Out scope, the workflow MUST reconcile routine correctable debrief findings, refresh evidence, and repeat debrief until an exact patch proposal is supported or a bounded stop occurs.
- **FR-015**: Close Out MUST retain explicit approval of the exact roadmap verification patch and separate authority for Git integration and acceptance. Both approved fresh verification and current trusted existing verification MUST reach shared curated wiki ingestion, lint, and coverage checks before the commit-readiness report. Required operator decisions MUST stop as blocked questions with recovery actions rather than stop-only defer/abort gates. Wiki maintenance MUST reconcile specific source-backed findings through a five-pass single-source ingestion, lint, and assessment loop, repeating only with substantive prior-gap resolution inside the authorized source set. It MUST preserve conflicting claims and block for required authority decisions, unavailable sources, age-only stale warnings without substantive update evidence, unsupported repairs, scope expansion, stale evidence, no progress, or cap exhaustion. The workflow MUST use one final report and preserve partial approved changes when later maintenance fails.
- **FR-016**: Changed workflow definitions MUST preserve reviewed named-agent assignments, main-task human gates, source-package authority, and bounded recovery. Independent extension behavior requires separate review.
- **FR-017**: Validation MUST cover success and stop paths, human gates, evidence classification, artifact order, loop termination, and manual and direct Codex paths in disposable consumers. Records MUST identify component IDs, versions, digests, tested CLI version, source coordinates, and observed limits.
- **FR-018**: The feature MUST review the original eight source workflows and the separately invoked Select Feature and Specify replacements—Start Feature, Clarify, Plan, Tasks, Analyze and Remediate, Implement, Converge, and Close Out—step by step. For each, it MUST record the intended success result, branch outcomes, human gates, routine automation, continuation or loop edges, termination rules, and resumption evidence before selecting source changes.
- **FR-019**: Analyze and Remediate MUST explicitly invoke fresh `speckit.analyze` in its initial read-only loop pass and after every shared specification → plan → tasks correction, using one analyzer and one assessment step. It MUST use the latest completed analyzer report as the authoritative finding source for correction decisions; missing, failed, or stale analysis MUST cause a specific stop. Each invoked workflow MUST use inspectable, current evidence to classify routine outcomes and continue through its own reviewed, bounded work until a defined success, required human decision, or bounded stop. Implement MUST run `speckit.implement` against the existing eligible task plan, reassess the task checklist after each session, and repeat while eligible work remains and progress is verified. Its wrapper MUST NOT re-specify, re-plan, re-task, or re-analyze. No workflow may invoke another FlowKit workflow, ask the operator to classify a routine machine-observable result, exit after one session while known in-scope work remains eligible, or infer success from command completion alone.
- **FR-020**: Every loop MUST use a reviewed, inspectable progress measure and continue while each correction pass makes measurable progress within a finite safety cap. An explicitly declared first baseline assessment may establish prior finding IDs without claiming a finding resolved; it counts toward the total loop cap. It MUST stop immediately for repeated findings without material change, no progress, stale evidence, failed prerequisites, or an exhausted cap. A stop MUST identify the smallest safe resumption action and preserve completed work. Planning MUST set the cap and progress evidence for each loop.
- **FR-021**: Human gates MUST remain at exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and acceptance. Routine evidence-based routing MUST not add a redundant confirmation gate. Completing one workflow MUST not invoke the next workflow without distinct authority.
- **FR-022**: The feature MUST inventory every delegated step across all eight workflows, review whether its exact agent name fits the step's purpose, and keep gates and undelegated steps in the main task. The starting reviewed names are Architect, Builder, Coder, and Verifier; any additional name MUST have a distinct reviewed purpose and approval before use in source.
- **FR-023**: This repository, as a FlowKit consumer, MUST have usable native Codex configurations for every name its reviewed workflows require. F014 MUST deliver those files only in this repository; the existing Coder launch-probe configuration MUST be replaced or explicitly retired from ordinary workflow use, and missing agents MUST not receive a silent fallback. Bundle installation, refresh, and removal MUST continue to leave consumer-owned agent files untouched. A later feature MAY separately propose installing agent files into consumer projects.
- **FR-024**: Validation MUST exercise every reviewed branch or demonstrate why a branch cannot be safely executed, check all used names in full-graph preflight, and compare manual and direct Codex paths. Evidence MUST distinguish structural checks, no-op dispatch, and live named-agent behavior.

### Key Entities

- **Feature linkage**: The unique relation between a roadmap entry and its specification directory, subject to exact patch approval when changed.
- **Readiness assessment**: An evidence-backed explanation of whether the current specification or task proposal can proceed within the invoked phase.
- **Remediation cycle**: One bounded pass from a convergence finding through artifact reconciliation, analysis, eligible implementation, and reassessment.
- **Debrief cycle**: One Close Out review, optional in-scope correction, refreshed evidence, and repeated review.
- **Workflow conclusion**: A defined success or bounded stop for one explicitly invoked workflow, distinct from the next workflow phase or feature acceptance.
- **Agent assignment**: One reviewed native Codex name attached to a delegated step because its responsibilities match that step; the name carries no approval authority.

## Success Criteria

These outcomes are measured in disposable initialized consumers and reviewed workflow runs; they do not imply publication or real-consumer adoption.

### Measurable Outcomes

- **SC-001**: Every tested missing, stale, and conflicting linkage case produces a uniquely matched brief after exact patch approval or stops with a specific recoverable reason; no unapproved mapping changes.
- **SC-002**: Every tested Clarify and Plan case states significant ambiguity or missing prerequisites with evidence, or proceeds without a routine readiness gate when ready.
- **SC-003**: Every tested Tasks case with complete reviewed design finishes generation and coverage assessment without routine pre- or post-generation confirmation; each material gap receives a specific stop.
- **SC-004**: Every tested remediable Converge case analyzes changed tasks before eligible implementation and reassesses current state until clean or a documented bounded stop; no clean result is inferred from command success alone.
- **SC-005**: Every tested Close Out case with clear completion evidence avoids a redundant availability question; routine correctable findings are reassessed against refreshed evidence before a patch proposal.
- **SC-006**: All tested consequential decisions, untrustworthy evidence, repeated findings, and nonprogress cases stop without silent roadmap mutation, Git integration, acceptance, or launching a later workflow.
- **SC-007**: Each changed workflow has a usable manual path and validation record with component version, digest, CLI version, source coordinates, and observed outcome.
- **SC-008**: All eight workflows have a reviewed branch-and-gate inventory with explicit success, continuation, human-decision, and stop routes; no reviewed branch has an unexplained terminal state or unbounded retry.
- **SC-009**: Every tested routine remediable outcome continues from fresh evidence while measurable progress occurs, reaches a defined conclusion or bounded stop, and stops on repeated findings or no progress; every tested consequential decision waits for the operator in the main task.
- **SC-010**: Every delegated step in all eight workflows has a justified reviewed agent name, and every distinct name used in the source checkout has a working native Codex configuration and full-graph preflight evidence; no probe-only instruction is used for normal workflow work.

## Assumptions

- Roadmap Feature 014 defines the authorized scope for this draft; dependencies 001, 002, 003, 004, 007, 008, and 013 are verified. Feature 012 is not a dependency.
- Starting F014 permits this draft and the requested lifecycle transition, but does not authorize an exact `Spec dir` patch, workflow source change, implementation, or acceptance. The separately approved Constitution 6.0.0 amendment is now part of F014's governing context.
- The existing five-question clarification limit remains a per-session command boundary. The operator explicitly selected bounded repeated sessions within one Clarify invocation for F014; a reusable custom preset, if later proposed, still needs its own review and approval.
- Accepted feedback is evidence for prospective design, not direct source-change authority. Additional feedback requires a roadmap amendment.
- The operator selected progress-based continuation with a finite safety cap for corrective loops. Planning must define each loop's observable progress measure and exact cap; repeated findings without material change and no progress stop immediately.
- The operator chose Feature 015's Architect, Builder, Coder, and Verifier as the initial assignment vocabulary. More names may be proposed by the F014 review only when a distinct responsibility warrants them, with explicit review before workflow source uses them.
- The source checkout is also a FlowKit consumer. Its tracked `.codex/agents/coder.toml` is currently a temporary launch probe, and no Architect, Builder, or Verifier file is present here. The operator selected repository-local configurations for F014; consumer bundle installation of agent files remains a possible later feature, not part of this delivery.
- The operator selected evidence-backed in-place Draft-to-Complete editing within an invoked Close Out run; F014 must prospectively reconcile this with verified Feature 008 and retain a separate exact roadmap verification patch gate.
