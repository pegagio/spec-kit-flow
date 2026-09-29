# Data Model: Named Agents for Delegated Steps

This model separates reviewed workflow selection from consumer-owned Codex configuration. FlowKit stores no role-to-model map.

## Reviewed step intent

`StepAssignmentIntent` belongs to each executable `prompt` or `command` node. `flow_kit.delegated: true` marks a bounded child and requires exactly one `flow_kit.agent` from Architect, Builder, Coder, or Verifier. Each delegated step has a unique step ID and its own agent name. A concrete `model` field on a delegated step is legacy source and fails preflight. A missing or unknown agent name also fails. Workflow-level agent defaults are unsupported.

`MainTaskStep` is an executable step without delegation metadata, or a gate or switch. It runs in the driving agent's main task and has no child agent selection. An agent name on a nondelegated step and delegation on a gate or switch are invalid.

## Native consumer agent

`CodexCustomAgent` is Codex's native TOML configuration layer in `.codex/agents/` or `~/.codex/agents/`. Its `name` field is the identity; its filename is not. Codex requires `name`, `description`, and `developer_instructions`; `model` and `model_reasoning_effort` are optional. Codex owns loading and assignment precedence. FlowKit does not package, write, copy, remove, or implement a second parser for these files.

## Dispatch selection and evidence

`StepAssignmentIntent` is one preflight row for every delegated step in every possible branch: `step_id` and `agent_name`. There is no workflow default or per-run override. Preflight checks that each selected native agent can launch a bounded child. The controller does not require model or effort introspection to select the agent.

Codex's native subagent activity provides launch visibility through a controller-supplied task label containing the intended agent name; the pane may also show model and effort. The label does not independently prove native selection, which relies on the exact `agent_type` request and successful probe. `RunAssignmentEvidence` retains compact step IDs and selected agent names with existing recovery evidence after preflight; it excludes TOML contents, raw child transcripts, secrets, and local absolute paths. A preflight rejection creates no run record.

One workflow has many steps; delegated steps may choose different named agents, while main-task steps have no child selection. The lifecycle is `loaded → validated and probed → dispatched`. An absent or unavailable agent stops before workflow work; a later dispatch failure preserves completed-step evidence. Human gates remain in the main task.
