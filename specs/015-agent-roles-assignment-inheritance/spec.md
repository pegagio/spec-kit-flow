# Feature Specification: Named Agents for Delegated Steps

**Feature Branch**: `develop` (no feature branch created)

**Created**: 2026-09-29

**Status**: Complete

**Input**: Start Feature 015 before Feature 014, then revise its assignment design to use Codex native custom agents without a FlowKit role map.

## Clarifications

The later decisions below supersede the earlier role-map and step → workflow → unnamed-child proposals. The current contract is an explicit Codex agent name on every delegated step.

### Session 2026-09-29

- The exact constitutional amendment was approved and applied as version 5.0.0 before workflow or controller source changes.
- The reviewed agent names are Architect, Builder, Coder, and Verifier; new names require a later reviewed change.
- Consumers configure those agents in Codex's native custom-agent TOML files. FlowKit has no role-to-model map and does not require model or effort fields beyond Codex's own file rules.
- Each delegated step names its own agent. There is no workflow-level agent default, unnamed delegated step, or temporary per-run agent/model/effort override.
- Codex's native subagent activity provides launch visibility. The controller supplies a task label containing the reviewed agent name; the pane may also show model and reasoning effort. The label is an operator cue, while the exact native agent request and successful probe establish selection. FlowKit does not require a separate launch message or a dedicated native-agent-name field in the pane.
- Agent-file edits during a run follow Codex's native behavior; Feature 015 adds no watcher or special stop rule.

## User Scenarios & Testing

These scenarios cover explicit agent selection, the main-task boundary, and safe dispatch in the supported Codex path.

### User Story 1 - Use a Named Agent for Each Delegated Step (Priority: P1)

A FlowKit maintainer can name the Codex custom agent required by each delegated workflow step. A consumer configures those names using Codex's native agent files. Different steps can use different agents without a FlowKit map or concrete model declarations in the workflow.

**Independent Test**: Install the same reviewed workflow in two disposable consumers with different native configurations for the same agent names. Confirm that each delegated step launches its named agent and that the reviewed workflow does not change.

**Acceptance Scenarios**:

1. **Given** a delegated step with `flow_kit.agent: Coder`, **when** it launches, **then** Codex shows a Coder child using the consumer's Coder configuration.
2. **Given** another delegated step with `flow_kit.agent: Verifier`, **when** it launches, **then** Codex shows a separate Verifier child using the consumer's Verifier configuration.
3. **Given** Codex exposes the selected child's model and reasoning effort, **when** the operator inspects the child pane, **then** those values are visible; unavailable setting details do not block launch.

### User Story 2 - Keep Main-Task Work in the Main Task (Priority: P2)

The main agent drives the workflow. An executable step without explicit delegation runs in that main task, while gates and switches always remain there. An agent name never turns a main-task step into a child.

**Independent Test**: Run a workflow with a main-task prompt, two delegated prompts using different names, and a human gate. Confirm only the delegated prompts launch children and the gate stays with the operator.

**Acceptance Scenarios**:

1. **Given** an executable step without `flow_kit.delegated: true`, **when** it runs, **then** it remains in the main task and launches no child.
2. **Given** a human gate or switch, **when** the workflow reaches it, **then** the main task handles it without launching a child.
3. **Given** a step with an agent name but no delegation marker, **when** preflight runs, **then** it rejects the unsupported placement before workflow work.

### User Story 3 - Diagnose Agent Availability (Priority: P3)

An operator can see why a named agent cannot be used before workflow work begins. FlowKit checks every branch, including branches that may not run, and never substitutes another agent.

**Independent Test**: In disposable consumers, test absent, misspelled, malformed, and unavailable agents, including in an untaken branch. Confirm specific preflight failures with no workflow work or recovery record.

**Acceptance Scenarios**:

1. **Given** a delegated step with no agent name, **when** preflight runs, **then** it identifies the step and stops.
2. **Given** a step naming an unavailable or invalid custom agent, **when** preflight runs, **then** it identifies the name and step and stops without a fallback.
3. **Given** an invalid agent on any possible branch, **when** preflight runs, **then** it stops before the first workflow step.
4. **Given** FlowKit is refreshed or removed, **when** the consumer has Codex agent files, **then** those files remain consumer-owned and unchanged.

### Edge Cases

- A delegated step still declares a concrete model from Feature 013; preflight stops with a specific migration reason.
- A custom-agent file omits model or effort; Codex applies its native configuration precedence, including parent and `[agents]` defaults.
- An agent name differs only in case or spelling from its Codex `name`; preflight must not select another agent accidentally.
- A custom-agent file changes during an active run; document Codex's observed behavior without adding a watcher.
- A named agent becomes unavailable after preflight; stop at dispatch and preserve completed-step evidence.
- Native `specify workflow run` may not support these names; document observed behavior rather than claiming parity from YAML acceptance.

## Requirements

These requirements keep assignment selection in reviewed workflow steps and consumer configuration in Codex.

### Functional Requirements

- **FR-001**: FlowKit MUST use a fixed, reviewed set of agent names: Architect, Builder, Coder, and Verifier. Names MUST match native Codex custom-agent `name` values exactly. A workflow MUST NOT introduce another name without a later reviewed change; a named agent confers no approval authority.
- **FR-002**: Each delegated `prompt` or `command` step MUST explicitly declare `flow_kit.delegated: true` and one `flow_kit.agent` from the reviewed set. A delegated step without an agent name MUST fail preflight. A workflow-level agent default MUST NOT substitute for a missing step name.
- **FR-003**: Main-task executable steps MUST remain in the main task and MUST NOT declare a child agent. Gates and switches MUST remain in the main task and MUST NOT be delegated. An agent name alone MUST NOT launch a child.
- **FR-004**: The selected name MUST launch the matching Codex custom agent using its native configuration. Codex owns optional model and reasoning settings and their precedence; FlowKit MUST NOT maintain a role map, copy those settings into another configuration source, or choose a fallback agent.
- **FR-005**: A workflow invocation MUST use the reviewed agent name on each delegated step. The controller MUST NOT accept a per-run agent, model, or effort override for a step.
- **FR-006**: Before workflow work, preflight MUST validate the full installed graph, including all switch branches, and confirm that every selected named agent can start a bounded child. A missing, malformed, unsupported, or unavailable agent MUST stop preflight with its step ID and reason, without workflow state or a recovery record.
- **FR-007**: The supported Codex client MUST show each launched probe and workflow child in native subagent activity. FlowKit MUST give every probe a visible task label containing its reviewed agent name and every workflow child a label containing its agent name and step ID. The label is a launch cue, not proof of native selection; the exact native agent request and successful probe establish that selection. Model and reasoning effort MAY appear in the child pane when Codex exposes them; missing setting details MUST NOT block an otherwise valid launch. FlowKit MUST NOT require a separate parent-authored launch message, dedicated native-agent-name field, or approval gate.
- **FR-008**: Feature 015 MUST preserve bounded child execution, main-task questions and gates, same-child interactive continuation, manual-prompt paths, compact recovery, and separate workflow phases from Feature 013.
- **FR-009**: FlowKit installation, refresh, and removal MUST NOT own, overwrite, or delete consumer Codex agent files. Agent-file edits during a run require documentation of native behavior, not a FlowKit watcher.
- **FR-010**: Updated workflows MUST replace concrete step-model declarations with explicit delegation and agent names. The controller MUST reject a delegated legacy model declaration with a migration reason; previously installed Feature 013 versions remain historical.
- **FR-011**: The feature MUST validate workflow metadata against the supported Specify loader and test native `specify workflow run` separately. Documentation MUST state the verified differences from direct Codex controller execution.
- **FR-012**: Validation MUST cover different named agents across steps, main-task steps, human gates, every-branch preflight, unavailable agents, native subagent visibility and optional model/effort display, consumer ownership, and native Specify behavior in disposable initialized consumers. Record component versions, source digests, Codex version, Specify version, and observed limits.
- **FR-013**: Before workflow or controller source uses named agents, maintainers MUST present an exact constitution amendment for operator review and acceptance. The roadmap and this specification alone do not grant that authority.

### Key Entities

- **Delegated step**: An executable workflow step explicitly marked for bounded child execution and carrying one reviewed Codex agent name.
- **Main-task step**: A workflow step handled by the driving agent; it has no child agent selection.
- **Codex custom agent**: A consumer-owned native TOML definition identified by its `name` field, with model and effort resolved by Codex.
- **Native subagent visibility**: Codex activity shows a child launch under a controller-supplied label containing the intended agent name; Codex may also show model and effort. The label does not independently prove native selection.

## Success Criteria

These outcomes are verified through observed controller and child behavior.

### Measurable Outcomes

- **SC-001**: The same reviewed workflow launches its named agents in two disposable consumers with different native agent configurations and no FlowKit role map.
- **SC-002**: In the supported Codex client, every tested probe and workflow child appears in native subagent activity with a task label containing its reviewed agent name, plus the step ID for a workflow child; model and effort are checked when Codex displays them. Exact native selection is verified separately from the label.
- **SC-003**: Every delegated step has a reviewed agent name, and different steps can use different names; no main-task step or human gate launches a child.
- **SC-004**: Every tested missing, malformed, or unavailable agent in any possible branch stops preflight before workflow work, with a specific step and reason and no silent substitution.
- **SC-005**: A per-run agent, model, or effort override is rejected; a legacy delegated concrete model reports a migration stop.
- **SC-006**: FlowKit install, refresh, and removal leave consumer Codex agent files unchanged.
- **SC-007**: Documentation includes workflow and custom-agent examples, the main-task boundary, and observed native Specify differences.

## Assumptions

- Feature 013 supplies the verified direct controller and catalog foundation. Feature 014 is independent.
- Codex's native agent files may omit model and effort; Codex resolves those settings through its own precedence. FlowKit selects only the agent name.
- The supported Codex child-dispatch surface must be shown to select an exact native agent name before Feature 015 can be called implemented. The currently exposed task tool has no named-agent parameter.
- Updated Feature 015 workflows do not silently reinterpret previously installed Feature 013 concrete-model declarations.
- Out of scope are implicit child dispatch, workflow-level agent defaults, per-run assignment overrides, a FlowKit role map, Feature 014 changes, retroactive Feature 013 edits, and unverified native Specify parity.
