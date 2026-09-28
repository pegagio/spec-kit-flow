# Feature Specification: FlowKit Codex Workflow Controllers

**Feature Branch**: `013-bundle-workflow-launchers`

**Created**: 2026-09-26

**Status**: Complete

**Input**: User description: "Start feature 013. Preserve the approved outcome, scope, dependencies, and cited governing context."

## Clarifications

### Session 2026-09-26

- Q: When you override a model declared by the workflow, should your override affect one agent step, every agent step in that run, or should both choices be available? → A: Override one named agent step.
- Q: If a step subagent fails after changing project files, what should the controller do with those partial edits? → A: Preserve the edits and stop for operator review.
- Q: Which workflow steps should launch a subagent? → A: Only steps with a declared model launch subagents.
- Q: Should an unavailable model in a workflow branch that is never taken stop the run? → A: Yes. Check every possible modeled step before the workflow starts.
- Q: If the main Codex task is interrupted between workflow steps, what recovery should the first controller release provide? → A: Stop with evidence; the operator handles recovery without built-in resume.
- Q: If the FlowKit bundle is refreshed while a workflow is running, which workflow version should finish that run? → A: Stop the run and require a new invocation.
- Q: If the bundle refreshes while a subagent is partway through a step, should that step finish before the workflow stops? → A: Finish the active step, then stop the run.
- Q: When a workflow stops after completing some steps, what recovery record should it leave? → A: Keep a compact local step and file summary.

## User Scenarios & Testing

### User Story 1 - Run Installed Workflows in a Codex Task (Priority: P1)

A consumer-project operator can see a stable, named Codex skill for each installed FlowKit workflow and explicitly run the desired workflow inside the selected project's Codex task. The main task shows progress and diffs while bounded step subagents use concrete models declared in the installed workflow.

**Why this priority**: The operator needs the desktop task experience and per-step model choices without manually selecting a model for each step or moving the workflow into separate CLI sessions.

**Independent Test**: Install through the supported FlowKit catalog route in a disposable consumer, confirm all eight workflow controller skills are discoverable, and invoke one skill with valid inputs and a declared model.

**Acceptance Scenarios**:

1. **Given** a compatible consumer project installed through the FlowKit catalog route, **when** the operator inspects available Codex skills, **then** one stable controller skill is visible for each of the eight FlowKit workflows under its specified FlowKit display name.
2. **Given** the operator invokes a controller skill with valid inputs, **when** an executable step in its installed workflow declares an available model, **then** the main task shows the effective model and reasoning effort, launches that step in a subagent with those assignments or a one-step operator override, and reports the workflow result in the selected project.
3. **Given** required workflow inputs are missing or any possible branch contains a modeled step with an invalid or unavailable effective model-effort pair, **when** the controller checks readiness, **then** it reports the blocker and does not start the workflow or silently choose a fallback assignment.

### User Story 2 - Keep Human Decisions in the Main Task (Priority: P2)

An operator can answer clarification questions and review gates in the main Codex task while an interactive step continues in the same subagent after its answer is relayed.

**Why this priority**: A child task has no direct human composer in the tested desktop experience, so the controller must preserve the workflow's human decisions in the main task.

**Independent Test**: Invoke a workflow with an interactive clarification and a review gate in a disposable consumer; verify the main task presents each question and relays accepted answers to the same step subagent before continuation.

**Acceptance Scenarios**:

1. **Given** a step subagent asks for clarification, **when** the controller receives its question, **then** it presents the question in the main task and relays the operator's answer to that same subagent.
2. **Given** a workflow contains a human review gate, **when** the controller reaches it, **then** the operator makes the required decision in the main task before continuation or a state change.
3. **Given** a workflow completes, **when** the controller reports its result, **then** no later workflow phase starts without a separate operator instruction; Git integration, roadmap verification, and feature acceptance retain their own decisions.

### User Story 3 - Maintain Controllers Through the FlowKit Catalog (Priority: P3)

A maintainer can package Codex controller skills alongside the FlowKit bundle through the supported FlowKit catalog route so new installs, refreshes, and removals keep skills aligned with the versioned workflows and do not disturb consumer-owned state.

**Why this priority**: Consumer projects need controller availability to follow the same lifecycle guarantees as the workflows they run.

**Independent Test**: Run FlowKit catalog lifecycle validation in disposable consumers covering fresh installation, refresh, and removal while checking controller presence, version alignment, and removal behavior.

**Acceptance Scenarios**:

1. **Given** a fresh compatible consumer project, **when** the supported FlowKit catalog install completes, **then** the controller skills are installed alongside the pinned Specify workflow components.
2. **Given** an installed release is refreshed through the FlowKit catalog route, **when** controller skills or workflow pins change, **then** the consumer receives the reviewed controller set aligned with the refreshed workflows.
3. **Given** the FlowKit catalog release is removed, **when** removal completes, **then** FlowKit-owned controller skills are removed while unrelated consumer-owned evidence and components survive.

### Edge Cases

- The consumer project has only some FlowKit workflows installed; controllers for missing workflows report the missing installation state and do not substitute another workflow.
- The controller cannot access a compatible Specify workflow loader in the selected consumer; it reports the missing runtime and stops before a workflow step or recovery record is created.
- A workflow input, model, or reasoning-effort declaration changes during refresh; the corresponding controller follows the installed definition and does not rely on stale invocation guidance.
- The Specify bundle or FlowKit skill package refreshes during a workflow run; the controller lets an active subagent step finish, then stops before another step, preserves project files and completed-step evidence, and requires a new invocation instead of switching to refreshed source.
- A step has a model declaration but its value or effective reasoning effort is invalid or unavailable; the controller stops for operator resolution and never silently selects another assignment.
- A model is unavailable only in a branch that will not be taken; the controller still blocks the run during full preflight before any step starts.
- Required inputs or model preflight fail before any workflow step starts; the controller reports the blocker in the main task without creating workflow run state or a recovery record.
- The operator overrides the model and/or effort of a named agent step; the controller applies those overrides only to that step and retains every other declared assignment.
- A workflow step has no model declaration; the controller handles it in the main task and does not launch a subagent for that step.
- A child question cannot be relayed or its answer cannot be returned to the same step subagent; the controller stops without inventing an answer or advancing the workflow gate.
- A step subagent fails after editing project files; the controller preserves those edits, reports the incomplete step, and stops for operator review without automatically reverting or retrying.
- The main Codex task is interrupted between workflow steps; the controller preserves project files and completed-step evidence, does not automatically resume or repeat a step, and leaves recovery to the operator.
- A workflow stops after execution has started; the operator can inspect a compact local record of the workflow version, step results, effective models and reasoning efforts, changed files, and blocker without requiring full child transcripts.
- A supported skill delivery mechanism cannot preserve interactive gates or selected project context; the feature stops for a documented resolution rather than shipping a degraded controller.
- A consumer already has a locally owned skill with a conflicting name; FlowKit catalog installation or refresh reports the conflict and avoids silent replacement.
- FlowKit catalog removal encounters controller artifacts that were modified locally; removal reports the ownership conflict and preserves consumer-owned evidence unless the operator explicitly resolves it.

## Requirements

### Functional Requirements

- **FR-001**: The supported FlowKit catalog installation MUST provide one explicit Codex controller skill for each of the eight installed FlowKit workflows. These controllers are Codex skill source, not Specify extension commands.
- **FR-002**: Each controller skill MUST have a stable, unambiguous `flow-kit-{purpose}` invocation name and MUST appear in the Codex skill picker under its specified FlowKit display name. The eight display names are FlowKit Start Feature, FlowKit Clarify, FlowKit Plan, FlowKit Tasks, FlowKit Analyze, FlowKit Implement, FlowKit Converge, and FlowKit Close Out, in the corresponding workflow order. Skill names MUST NOT change workflow bindings.
- **FR-003**: Each controller MUST verify that a compatible workflow loader is available and its corresponding workflow is installed in the selected consumer project before attempting to run it. If either check fails, it MUST report the blocker without starting a workflow step or creating a recovery record.
- **FR-004**: Each controller MUST identify required workflow inputs before dispatch and report missing inputs without mutating workflow state.
- **FR-005**: Each controller MUST follow the installed, versioned workflow definition rather than duplicating its prompts, gates, or decision rules in the skill.
- **FR-006**: An executable workflow step with a concrete model declaration in workflow YAML MUST run in a subagent; a step without a model declaration MUST remain in the main task. A modeled step MUST use medium reasoning effort unless its reviewed step declaration or an operator override specifies another supported effort. Before dispatch, the controller MUST show each effective model and effort, use the declared values unless the operator overrides one named step, and leave all other assignments unchanged.
- **FR-007**: Before any workflow step starts, the controller MUST validate the effective concrete model and reasoning effort for every possible modeled step, including steps in branches that may not be taken. If any model or model-effort pair is empty where required, invalid, unsupported, or unavailable, it MUST stop for operator resolution without changing workflow state or silently selecting a fallback assignment.
- **FR-008**: The controller MUST run bounded modeled steps as subagents in the selected Codex task, keep unmodeled steps and gates in the main task, and keep workflow progress, results, and workspace diffs visible there.
- **FR-009**: The controller MUST present clarification questions and human review gates in the main task, relay an accepted answer to the same interactive step subagent, and prevent continuation until required decisions are received.
- **FR-010**: Controller execution MUST preserve each workflow's manual-prompt fallback and separate phase boundaries; it MUST NOT implicitly launch another workflow, schedule work, integrate Git changes, verify a roadmap item, or accept a feature.
- **FR-011**: The supported FlowKit catalog install and refresh commands MUST install or update the reviewed Codex skill package alongside the pinned Specify workflow set, using one documented operator command for each lifecycle operation.
- **FR-012**: Supported FlowKit catalog removal MUST remove FlowKit-owned controller skills without deleting unrelated consumer-owned state, feedback evidence, or non-bundle components.
- **FR-013**: Validation MUST cover fresh installation, refresh, removal, selected project context, concrete step model and reasoning-effort dispatch, same-child clarification, at least one human review gate, and workflow results in disposable consumers.
- **FR-014**: Documentation MUST describe controller invocation, workflow inputs, declared models and effort, named-step overrides, the supported FlowKit catalog lifecycle, native Specify bundle scope and its effort limitation, manual fallback, and evidence limits.
- **FR-015**: If the Specify workflow schema rejects concrete model or FlowKit reasoning-effort metadata, the supported FlowKit catalog route cannot safely deliver the direct Codex skills, or controller execution cannot preserve project context or interactive gates, the feature MUST stop for an explicit operator decision rather than silently move policy elsewhere or ship degraded behavior.
- **FR-016**: If a step subagent fails after editing project files, the controller MUST preserve the partial edits, report the incomplete step, and stop for operator review without automatically reverting or retrying.
- **FR-017**: If the main Codex task is interrupted between workflow steps, the initial controller release MUST preserve project files and completed-step evidence and MUST NOT automatically resume or repeat work. Built-in checkpoint resume is out of scope; the operator directs recovery.
- **FR-018**: If the Specify bundle or FlowKit skill package refreshes during a workflow run, the controller MUST let an active subagent step finish under the current definition, then stop before another step, preserve project files and completed-step evidence, and require a new invocation. If no subagent step is active, it MUST stop before the next step. It MUST NOT use refreshed source to continue the current run.
- **FR-019**: Once a workflow step has started, the controller MUST maintain a compact local recovery record so a stopped run retains the workflow ID and version, starting Specify bundle and FlowKit skill package fingerprints, completed and incomplete step statuses, effective step models and reasoning efforts, repository-relative changed-file paths, and the stopping blocker. The record MUST NOT contain full child chat transcripts. A preflight rejection before the first step reports its blocker in the main task without creating a recovery record or workflow run state.

### Key Entities

- **Workflow controller skill**: A Codex-facing entry point that checks one installed FlowKit workflow, gathers required inputs, coordinates its steps and human gates in the selected task, and reports the outcome.
- **Installed FlowKit workflow**: One of the eight versioned workflow packages installed into a consumer project by the FlowKit bundle.
- **Step model and effort declaration**: A concrete model recorded for an executable step in a reviewed workflow definition directs the controller to use a subagent. The controller uses medium reasoning effort unless that step declares a FlowKit effort override; the operator may override one named step without changing other assignments.
- **Step subagent**: A bounded Codex child task that executes one modeled workflow step and can continue after the main task relays a human answer.
- **Controller inventory**: The complete set of controller skills expected for the installed FlowKit catalog release, including invocation names, display names, and workflow associations.
- **Consumer project context**: The project state selected by the operator where installed workflows, feature artifacts, and local evidence reside.
- **FlowKit skill ownership record**: The consumer-visible evidence of direct Codex skill package ownership, version, refresh, and removal behavior, separate from the Specify bundle record.
- **Workflow recovery record**: A local summary of workflow identity and version, step results and models, changed files, and the blocker for operator-guided recovery after a stopped run.

## Success Criteria

### Measurable Outcomes

- **SC-001**: In a fresh disposable consumer, all eight FlowKit controller skills are discoverable after supported catalog installation with the specified display names and stable invocation names.
- **SC-002**: A controller invoked with valid inputs follows the installed workflow and reports its result in the selected Codex task with visible progress and workspace diffs.
- **SC-003**: Before the first modeled step, the main task shows each effective model and reasoning effort; a one-step operator override changes only the named step, each modeled step uses a child task with its effective model and effort, and unmodeled steps do not launch child tasks.
- **SC-004**: Missing inputs or an unavailable effective model-effort pair in any possible branch are reported before the first workflow step, with no workflow state change or silent substitution.
- **SC-005**: An interactive clarification is answered in the main task and relayed to the same child task; a human gate requires an explicit decision before continuation.
- **SC-006**: Completing one workflow does not start a later workflow without a separate operator instruction.
- **SC-007**: Catalog refresh validation shows controller inventory and workflow pins remain aligned for the refreshed release.
- **SC-008**: Catalog removal validation shows FlowKit-owned controllers are removed while unrelated consumer-owned evidence and components remain present.
- **SC-009**: `README.md`, `docs/installation.md`, and `workflows/README.md` each identify the matching display name, skill invocation, and required input for all eight workflows; `workflows/README.md` also provides a manual fallback for each.
- **SC-010**: A failed step that edited project files leaves those edits available for operator review and does not automatically revert, retry, or start the next step.
- **SC-011**: After an interrupted main task, the operator can inspect preserved files and completed-step evidence; the controller neither resumes nor repeats a step automatically.
- **SC-012**: A Specify bundle or FlowKit skill package refresh during an active subagent step allows that step to finish, then stops the run with files and completed-step evidence preserved; no further step uses refreshed source without a new invocation.
- **SC-013**: After a run stops following its first started step, a local record identifies the workflow version, each completed or incomplete step, effective models and reasoning efforts, changed files, and blocker without storing full child transcripts; a preflight rejection leaves no recovery record.

## Assumptions

- Feature 013 depends on the verified bundle catalog and lifecycle foundation from Feature 011 and has no dependency on planned Feature 012.
- The approved outcome is explicit-invocation Codex controllers installed by the FlowKit catalog route alongside the Specify bundle; the earlier thin CLI launcher and Specify extension-command delivery designs are superseded for this path.
- The initial workflow step models may be non-portable. Model roles and consumer model mappings are deferred to a later feature.
- The initial controller does not provide built-in checkpoint resume after a main-task interruption; operator-guided recovery uses preserved files and completed-step evidence.
- The governing context is C-02 Human-directed authority, C-03 Generic component boundaries, C-04 Reviewable source and manual fallback, and C-05 Evidence-based validation and feedback from the project roadmap and constitution.
- The eight target workflows are the current FlowKit workflow set: start feature, clarify, plan, tasks, analyze and remediate, implement, converge, and closeout.
- Consumer validation uses disposable initialized projects and records bounded evidence; the prior subagent probes alone do not establish full Specify integration, YAML model metadata support, remote publication, stock Spec Kit compatibility beyond tested coordinates, roadmap verification, Git integration, or feature acceptance.
