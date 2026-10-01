# Feature Specification: FlowKit Workflow Improvements

**Feature Branch**: `develop` (no feature branch created)

**Created**: 2026-09-29

**Status**: Draft

**Input**: Review the original eight FlowKit workflows so each has the right gates, automation, continuation paths, and bounded stops to reach a sound conclusion; incorporate Feature 015's named-agent design, build usable agent configurations, and address the recorded workflow issues as symptoms of incomplete continuation.

## Contents

This specification records accepted workflow intent and the requirements for completion.

- [Clarifications](#clarifications)
- [User Scenarios and Testing](#user-scenarios--testing)
- [Requirements](#requirements)
- [Success Criteria](#success-criteria)
- [Assumptions](#assumptions)

## Clarifications

The initial session established the continuation and authority boundaries retained by subsequent reviews.

### Session 2026-09-29

- Q: Should an invoked workflow run its own reviewed corrective steps and reassess until success, a required human decision, or a bounded stop, without invoking another FlowKit workflow? → A: Yes; continue through steps defined in the current workflow.
- Q: If a five-question Clarify session ends but significant ambiguity remains, should the already-invoked Clarify workflow start another bounded session without a new invocation? → A: Yes; continue within the current invocation while each substantive answer remains human-provided.
- Q: Where should F014 deliver the new Codex agent configurations needed by the reviewed workflows? → A: Add usable agent files to this repository only; leave consumer bundle installation for a possible later feature.
- Q: When Close Out finds a cleanly converged feature whose specification is still Draft, should its invocation authorize changing the specification to Complete before debrief? → A: Yes, when completion evidence is clear; stop on ambiguity and keep roadmap verification separately approved.
- Q: When a workflow repeats a corrective pass, what should determine when it stops trying within the current invocation? → A: Continue while each pass makes measurable progress, stop on repeated findings or no progress, and enforce a finite safety cap.

## User Scenarios & Testing

The operator invokes each workflow separately. The delivered source has ten active workflows: Select Feature, Specify, Clarify, Plan, Tasks, Analyze and Remediate, Implement, Converge, Close Out, and Wiki Lint Update. Start Feature remains a stop-only deprecated source, excluded from active bundle and launcher bindings. The review began with eight workflows and incorporated the operator-approved replacements and additions. Routine evidence-backed work should continue within an invoked workflow until its defined success, human decision, or genuine blocker, subject to reviewed authority.

### User Story 1 - Review Every Workflow End to End (Priority: P1)

A maintainer can trace each of the ten active FlowKit workflows from invocation to every possible terminal result. Each routine outcome has evidence-based routing and a bounded continuation when further in-scope work is needed. A human gate appears where the operator must decide, and a stop explains what input or authority is missing.

**Independent Test**: For each workflow, enumerate all branch outcomes and run representative successful, remediable, blocked, and consequential-decision cases against its manual and direct Codex paths.

**Acceptance Scenarios**:

1. **Given** an operator-invoked workflow with routine in-scope work remaining, **when** a step produces a remediable result, **then** the workflow continues or loops using current evidence until its defined conclusion or bounded stop.
2. **Given** a consequential operator decision, **when** the workflow reaches it, **then** the main task presents the exact decision and waits instead of inferring approval.
3. **Given** a genuine blocker, repeated finding, stale evidence, or lack of progress, **when** continuation cannot be trusted, **then** the workflow stops with a specific reason, preserved work, and a resumption point.
4. **Given** a successful terminal result, **when** the workflow finishes, **then** it reports that workflow's conclusion without launching the next phase or implying acceptance, roadmap verification, or Git integration.

### User Story 2 - Start with Reliable Roadmap Linkage (Priority: P1)

The former Start Feature is split into Select Feature and Specify. Selection lists candidates, dependency chains, immediate unlocks, and downstream dependents; the human discusses and chooses one exact feature. Exact approval authorizes its roadmap delta and active `.specify/feature.json` pointer. It never creates a feature directory or writes a specification, and preserves existing spec bytes. Specify is separately invoked, consumes that pointer and unique roadmap mapping, retrieves context, authors the exact target, verifies linkage, and runs the shared brief. The combined workflow is deprecated and excluded from active bundle/controller bindings.

**Independent Test**: Exercise selection and specification authoring separately in a disposable project with unique, absent, stale, and conflicting specification-directory mappings; verify selection never writes a specification.

**Acceptance Scenarios**:

1. **Given** a selected eligible entry and exactly approved activation patch, **when** Select Feature completes, **then** the roadmap and active pointer identify that unique target while existing specification bytes remain unchanged and no directory is created.
2. **Given** that active pointer, **when** Specify is separately invoked, **then** it retrieves cited context, authors only the active target, verifies exact linkage, and runs its uniquely matched brief.
3. **Given** a missing mapping, **when** linkage is proposed, **then** the operator sees an exact roadmap patch and no mapping changes before approval.
4. **Given** stale or conflicting mappings, **when** a unique link cannot be established, **then** the workflow stops with the evidence and a recoverable next action.
5. **Given** several candidates or no eligible candidate, **when** Select Feature begins, **then** it shows dependency readiness and downstream impact and waits for an exact human selection or deferral without choosing or changing roadmap state.

### User Story 3 - Assess Clarification and Planning Readiness (Priority: P1)

After clarification, the operator receives an evidence-backed assessment of remaining significant ambiguity. A separate planning invocation delegates to the existing planning skill, which owns prerequisite checks, research, design generation, and constitutional gates.

**Independent Test**: Exercise clarified, materially ambiguous, and missing-prerequisite specifications through separate Clarify and Plan runs; include populated planning artifacts with semantic deficiencies, exact independent findings returned to Planner, and bounded correction or stop.

**Acceptance Scenarios**:

1. **Given** a clarification session reaches its five-question limit, **when** significant ambiguity remains, **then** the workflow assesses the remaining questions and starts another bounded session within the current invocation; each substantive answer still comes from the operator.
2. **Given** a reviewed specification without material product ambiguity, **when** the operator invokes Plan, **then** planning proceeds without a routine readiness confirmation.
3. **Given** a missing prerequisite or material product ambiguity, **when** the core planning skill encounters it, **then** the workflow reports the exact blocker or operator question without choosing a product answer.
4. **Given** populated planning artifacts with a contradiction or missing requirement coverage, **when** the existing independent assessment identifies the semantic deficiency, **then** its exact findings return to Planner through the existing correction path; fresh assessment confirms substantive resolution or reports a bounded stop.

### User Story 4 - Generate and Assess Tasks (Priority: P1)

The operator invokes Tasks for a reviewed plan. The workflow invokes the core task skill, checks generation structure, independently assesses semantic coverage and consistency, and returns exact findings to Tasker while progress permits correction. The operator may review it and separately invoke Analyze.

**Independent Test**: Run Tasks with complete design artifacts and with a material design gap; inspect generation, coverage, and the resulting stop or success.

**Acceptance Scenarios**:

1. **Given** reviewed design without a material gap, **when** the operator invokes Tasks, **then** generation begins without an extra routine pre-generation question.
2. **Given** complete generated coverage, **when** the agent assesses tasks, **then** the workflow exits successfully without a routine post-generation human gate.
3. **Given** incomplete generated coverage that can be repaired within reviewed design, **when** Tasks assesses it, **then** exact gaps feed another core-skill pass while semantic progress and the cap permit.
4. **Given** a material design gap or required product answer, **when** generation cannot safely proceed, **then** Tasks reports the exact blocker without beginning implementation.

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

The operator can inspect the agent selected for every delegated step and use each reviewed name in this repository's own Codex checkout. Agent names identify the kind of work delegated, so each role can be tuned without changing unrelated step types. A work author and its reviewer are different agent types. Roadmap work uses a Roadmap Agent that can read or write when a workflow declares the task, while existing approval gates remain in the main task. Code review uses a separate Code Reviewer rather than the higher-level Reviewer used for specifications, plans, tasks, and roadmap alignment.

**Independent Test**: Inventory all delegated steps and native agent files, review each assignment against its step purpose, verify that authoring and review use different agent types, then probe every distinct name used by every workflow branch in a disposable consumer and this source checkout.

**Acceptance Scenarios**:

1. **Given** a delegated step, **when** its workflow is reviewed, **then** the step has one justified, exact reviewed agent name and can be dispatched without a fallback.
2. **Given** a gate or main-task step, **when** assignments are reviewed, **then** it remains in the main task and receives no child assignment.
3. **Given** a specification, plan, or task list is authored, **when** an existing workflow assessment reviews its output, **then** the review uses a different agent type; Plan and Tasks return actionable findings through their existing repair loops.
4. **Given** implementation code is produced, **when** an existing post-implementation assessment reviews it, **then** a Code Reviewer distinct from Coder checks the changes and routes findings through the existing correction path or reports a bounded stop.
5. **Given** a workflow delegates roadmap work, **when** it reads or prepares roadmap changes, **then** it uses the Roadmap Agent and preserves every exact human approval gate before a consequential write.
6. **Given** this repository's Codex checkout, **when** each used agent is probed, **then** its native configuration is usable; temporary probe instructions are not mistaken for production behavior.

### User Story 8 - Refresh Wiki Sources and Report Every Finding (Priority: P1)

The operator invokes Wiki Lint Update with a full or narrowed lint scope. It starts with lint, maps source-backed stale findings through citations to registered sources, refreshes one authorized source at a time, and re-lints. Independent safe refreshes proceed while other findings remain visible. Source authority conflicts and unsupported repairs are reported for operator resolution.

**Independent Test**: Exercise multiple stale pages sharing a source, multiple independent stale sources, non-stale findings, unauthorized URLs, no progress, and capacity exhaustion without requiring an active feature.

**Acceptance Scenarios**:

1. **Given** stale pages with registered citations, **when** lint identifies them, **then** shared sources are deduplicated and each selected ingestion receives exactly one source token before fresh lint.
2. **Given** contradictions or other findings alongside safely refreshable sources, **when** refresh proceeds, **then** every finding remains recorded and conflicted authority is not silently resolved.
3. **Given** unavailable or unauthorized sources, no progress, or the 25-refresh bound, **when** updates stop, **then** the report preserves pending sources and the smallest safe resumption action.
4. **Given** the final successful lint has no unresolved findings, **when** the workflow concludes, **then** it reports clean without changing feature artifacts, roadmap state, or Git.

### User Story 9 - Inspect Workflow Diagrams (Priority: P2)

The operator can render a selected source workflow into a project-local flowchart whose nodes and transitions can be reconciled directly with the definition.

**Independent Test**: Render a selected definition and compare all declared step IDs, branches, types, delegation, and the entry edge with the source.

**Acceptance Scenarios**:

1. **Given** a selected workflow, **when** the project rendering skill runs, **then** its adjacent diagram has one Start marker connected to the first declared step and every source step appears exactly once.
2. **Given** a node, **when** the operator reads it, **then** its exact ID, parenthesized agent when present, and nonblank command are visible; type and delegation use shapes and outlines without redundant labels or placeholders.
3. **Given** collapsed paths or loop guards, **when** the diagram is rendered, **then** descriptive declared transition labels and the actual branches, joins, conditions, and bounds preserve source semantics.

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
- **FR-005**: Plan MUST invoke `speckit.plan` for the selected reviewed specification and present the resulting design artifacts or exact blocker. The core skill owns prerequisite checks, research, design generation, and constitutional gates. The wrapper MUST check that required and applicable output artifacts are present and populated, then feed exact missing files or placeholder sections back into the core skill while output gaps are being resolved. It MUST preserve completed design, accept justified not-applicable sections, and stop for operator input, blockers, no progress, or the reviewed safety bound. Structural output checks MUST be accompanied by independent semantic assessment in the existing assessment step, as required by FR-028. Exact actionable findings MUST return to Planner through the existing bounded correction path; populated artifacts alone MUST NOT establish satisfactory output. Substantive product decisions remain operator-provided and Tasks remains separately invoked.
- **FR-006**: Tasks MUST treat invocation as authorization to generate from reviewed design without a routine pre-generation confirmation; a material design gap MUST cause a specific stop.
- **FR-007**: Tasks MUST wrap `speckit.tasks` in a bounded output-verification loop: prepare exact gaps, invoke the core skill, verify tasks.md is populated with required format, sections, and story/dependency coverage, then independently assess semantic consistency and coverage and return exact actionable findings to Tasker through the existing bounded correction path while progress is verified. Retries MUST preserve existing task IDs, completion markers, completed work, and reviewed design. Unchecked implementation tasks MUST NOT count as incomplete generation. Operator input, material design gaps, missing prerequisites, no progress, or the reviewed cap cause a specific stop. Additional operator review, Analyze, and implementation remain separate operator actions.
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
- **FR-018**: The feature MUST review all ten active source workflows step by step and retain the original eight-workflow baseline as historical evidence. Start Feature MUST remain a stop-only deprecated definition excluded from active delivery. For each, it MUST record the intended success result, branch outcomes, human gates, routine automation, continuation or loop edges, termination rules, and resumption evidence before selecting source changes.
- **FR-019**: Analyze and Remediate MUST explicitly invoke fresh `speckit.analyze` in its initial read-only loop pass and after every shared specification → plan → tasks correction, using one analyzer and one assessment step. It MUST use the latest completed analyzer report as the authoritative finding source for correction decisions; missing, failed, or stale analysis MUST cause a specific stop. Each invoked workflow MUST use inspectable, current evidence to classify routine outcomes and continue through its own reviewed, bounded work until a defined success, required human decision, or bounded stop. Implement MUST run `speckit.implement` against the existing eligible task plan, reassess the task checklist after each session, and repeat while eligible work remains and progress is verified. Its wrapper MUST NOT re-specify, re-plan, re-task, or re-analyze. No workflow may invoke another FlowKit workflow, ask the operator to classify a routine machine-observable result, exit after one session while known in-scope work remains eligible, or infer success from command completion alone.
- **FR-020**: Every loop MUST use a reviewed, inspectable progress measure and continue while each correction pass makes measurable progress within a finite safety cap. An explicitly declared first baseline assessment may establish prior finding IDs without claiming a finding resolved; it counts toward the total loop cap. It MUST stop immediately for repeated findings without material change, no progress, stale evidence, failed prerequisites, or an exhausted cap. A stop MUST identify the smallest safe resumption action and preserve completed work. Planning MUST set the cap and progress evidence for each loop.
- **FR-021**: Human gates MUST remain at exact roadmap patches, constitutional or authority changes, material scope, ambiguous recovery, substantive product answers, Git integration, and acceptance. Routine evidence-based routing MUST not add a redundant confirmation gate. Completing one workflow MUST not invoke the next workflow without distinct authority.
- **FR-022**: The feature MUST inventory every delegated step across all ten active workflows, assign a task-specific reviewed name, and keep gates and undelegated steps in the main task. The role set MUST distinguish Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator. A Roadmap Agent MAY read or prepare roadmap writes in a workflow; exact roadmap approval and mutation authority MUST remain with the main task. Existing artifact-assessment steps MUST independently review the outputs they are assigned to assess, using Reviewer for specifications, plans, tasks, and roadmap alignment. Existing post-implementation assessment steps MUST inspect implementation changes using Code Reviewer before the workflow reports completion. Findings MUST use the workflow's existing correction route or produce a specific bounded stop. Code Reviewer MUST remain distinct from Reviewer. This agent-assignment change MUST NOT add workflow steps.
- **FR-023**: This repository, as a FlowKit consumer, MUST have usable native Codex configurations for every role required by its reviewed workflows. F014 MUST deliver those files only in this repository; the existing Coder launch-probe configuration MUST be replaced with ordinary Coder responsibilities, and missing agents MUST not receive a silent fallback. Bundle installation, refresh, and removal MUST continue to leave consumer-owned agent files untouched. A later feature MAY separately propose installing agent files into consumer projects.
- **FR-024**: Validation MUST exercise every reviewed branch or demonstrate why a branch cannot be safely executed, check all used names in full-graph preflight, verify author/reviewer separation and code-review routing, and compare manual and direct Codex paths. Evidence MUST distinguish structural checks, no-op dispatch, and live named-agent behavior.
- **FR-025**: The separately invoked Wiki Lint Update workflow MUST start with fresh lint, map all source-backed stale findings to registered source identities, refresh them individually with bounded progress checks, and retain every other unresolved lint finding in its report. Safe independent refreshes MAY continue while unrelated semantic or structural findings remain; authority-conflicted claims, unavailable sources, age-only timestamp updates, and unsupported repairs MUST remain reported for resolution. Exact URL refresh authorization MUST come from operator input. This workflow MUST NOT invoke another workflow or change feature artifacts, roadmap state, or Git.

- **FR-026**: A project-owned workflow rendering skill MUST derive diagrams from the selected source definition, include an entry marker, exact step IDs, assigned agents and nonblank commands, distinct type shapes, and delegated outlines. It MUST preserve all branches, joins, loop conditions and caps, and declared descriptive transition labels without inventing steps or printing absent-field placeholders.
- **FR-027**: Routine outcomes requiring operator input MUST use `blocked` with the exact question and resumption action. Distinct outcome keys MAY share a path only when completed evidence still determines all downstream authorization. Collapsing paths MUST NOT collapse exact human choices or permit an unverified success path. Legacy `needs-human` remains controller compatibility for explicitly declared gates.
- **FR-028**: Plan and Tasks output-verification loops MUST independently review the content produced by Planner and Tasker, respectively, and return exact actionable findings to the corresponding authoring step. Required-file and placeholder checks alone MUST NOT count as review. Specify MUST retain its existing independent roadmap brief after specification authoring; that brief verifies roadmap alignment and MUST NOT be described as a general content-review loop. Reviewers MUST NOT edit the artifacts they review; corrections remain with the authoring agent through an existing bounded path when available. Semantic assessment MUST check applicable accepted requirements, internal and cross-artifact consistency, and required coverage even when every required file and section is populated. Findings MUST identify the affected artifact or section, the applicable requirement or accepted decision, the observed deficiency, and the correction needed within approved scope. Across fresh assessments, stable finding identities and evidence of substantive resolution MUST establish progress; changed wording, populated placeholders, or renamed findings alone MUST NOT establish progress. The first assessment establishes a baseline under FR-020, and subsequent correction passes MUST resolve prior deficiencies without leaving new blocking findings unreported. Repeated findings without material change, no substantive resolution, stale evidence, or the reviewed cap MUST cause a specific bounded stop. If a finding requires a substantive product answer or material scope decision, the workflow MUST present the exact question to the operator instead of allowing Reviewer or author to infer an answer. This contract uses existing assessment and correction steps and adds no workflow nodes.

- **FR-029**: Assessment `reason_code` values and any `resume_action` values MUST match the controller grammar `^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$`: lowercase letters and digits joined by single hyphens, with no spaces or underscores. Assessment prompts that may return either field MUST state this syntax explicitly. The controller MUST reject malformed values before routing.

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
- **SC-008**: All ten active workflows and the deprecated source have a current branch-and-gate inventory with explicit success, continuation, human-decision, and stop routes; no reviewed branch has an unexplained terminal state or unbounded retry.
- **SC-009**: Every tested routine remediable outcome continues from fresh evidence while measurable progress occurs, reaches a defined conclusion or bounded stop, and stops on repeated findings or no progress; every tested consequential decision waits for the operator in the main task.
- **SC-010**: Every delegated step in all ten active workflows has a justified task-specific agent name and working native configuration; existing assessment steps review author outputs independently and review implementation changes using a distinct Code Reviewer before reporting completion, without adding workflow nodes.

- **SC-011**: Every tested wiki refresh uses a registered authorized source, retains all unresolved findings, and completes only from a fresh finding-free lint report; no timestamp-only update proves progress.
- **SC-012**: Diagrams cover every source step exactly once with an explicit Start edge, matching labels, shapes, delegation, and transition semantics.
- **SC-013**: Every tested independent review either accepts the artifact against its applicable requirements or returns exact findings through an existing correction path; populated but semantically deficient Plan and Tasks artifacts receive independent findings returned to Planner and Tasker, respectively, and fresh assessments demonstrate substantive finding resolution or a specific progress/cap stop; code-review findings use the current workflow's existing task or implementation correction path, or produce a specific bounded stop. Review assignments never authorize roadmap writes, Git integration, or feature acceptance. The reviewed change adds no workflow nodes.

## Assumptions

- Roadmap Feature 014 defines the authorized scope for this draft; dependencies 001, 002, 003, 004, 007, 008, and 013 are verified. Feature 012 is not a dependency.
- The initial F014 invocation authorized the draft and requested lifecycle transition. Subsequent operator approvals authorize the documented source changes; exact roadmap patches and acceptance retain their separate decision requirements. The separately approved Constitution 6.0.0 amendment is now part of F014's governing context.
- The existing five-question clarification limit remains a per-session command boundary. The operator explicitly selected bounded repeated sessions within one Clarify invocation for F014; a reusable custom preset, if later proposed, still needs its own review and approval.
- Accepted feedback is evidence for prospective design, not direct source-change authority. Additional feedback outside the approved change set requires a roadmap amendment. The approved replacement workflows, wiki maintenance workflow, and rendering skill are recorded in this specification; the exact F014 roadmap reconciliation patch was approved and applied on 2026-09-30.
- The operator selected progress-based continuation with a finite safety cap for corrective loops. Planning must define each loop's observable progress measure and exact cap; repeated findings without material change and no progress stop immediately.
- Agent names identify task responsibilities: Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator. Use existing assessment nodes for review and add no workflow nodes as part of this assignment change.
- The source checkout is also a FlowKit consumer. F014 supplies repository-local agent configurations for dogfooding; consumer bundle installation of agent files remains a possible later feature.
- The operator selected evidence-backed in-place Draft-to-Complete editing within an invoked Close Out run; F014 must prospectively reconcile this with verified Feature 008 and retain a separate exact roadmap verification patch gate.
