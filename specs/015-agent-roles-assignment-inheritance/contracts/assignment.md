# Contract: Named Codex Agent Selection

This is the proposed direct Codex controller contract for Feature 015. It depends on live proof that the supported Codex client can select a native custom agent by exact name. Specify loader acceptance of `flow_kit` metadata alone does not prove execution behavior.

## Reviewed workflow metadata

```yaml
workflow:
  id: example
  name: Example named-agent workflow
  version: 1.0.0
steps:
  - id: focused-change
    type: prompt
    flow_kit:
      delegated: true
      agent: Coder
    prompt: Make the reviewed change.
  - id: design-check
    type: prompt
    flow_kit:
      delegated: true
      agent: Architect
    prompt: Check the design.
  - id: parent-summary
    type: prompt
    prompt: Summarize the child results in the main task.
  - id: human-review
    type: gate
    message: Review the result.
    options: [approve, reject]
```

`focused-change` launches Coder; `design-check` launches Architect. `parent-summary` and `human-review` stay in the driving agent's main task. Every delegated step has its own agent name. There is no workflow-level agent default or delegated step without an agent name. An agent name alone never delegates. Reject unsupported placement and legacy concrete step models before work. Preserve existing prompts, branches, and gates during source migration.

## Native consumer agent files

Codex loads one custom agent from each standalone TOML file under `.codex/agents/` or `~/.codex/agents/`. The filename is conventional; the `name` field is authoritative. A consumer could provide `.codex/agents/coder.toml` with:

```toml
name = "Coder"
description = "Focused code changes within a reviewed workflow step."
model = "gpt-6-sol"
model_reasoning_effort = "high"
developer_instructions = "Complete only the delegated step and return its result to the controller."
```

Codex requires `name`, `description`, and `developer_instructions`; model and effort are optional native settings. The example model is illustrative and must be available to the consumer. FlowKit has no role-map file, does not own these agent files, and does not calculate their effective model or effort independently.

## Preflight and dispatch

1. Validate installed workflow identity, unique step IDs, metadata placement, explicit delegation, every switch branch, and the fixed reviewed agent names. Reject a delegated step without `flow_kit.agent`, a workflow-level agent default, or a delegated concrete `model` as legacy or unsupported source.
2. Resolve each delegated step directly to its own native Codex custom agent. There is no workflow default or per-run agent, model, or effort override.
3. Confirm that every selected agent can start a bounded, no-work preflight child by passing the exact reviewed name as the native `agent_type`. A successful exact-type spawn and the expected readiness token establish availability; the tool reply need not repeat the selected type. A generic child with the same task label or model is not proof that the named agent's instructions loaded.
4. Dispatch each workflow child with `agent_type` set to its reviewed agent name. Label every probe with that agent name and every work child with the agent name and step ID so Codex's native activity identifies what launched. The label is for operator visibility; the exact `agent_type` request establishes native selection. Model and effort appear when Codex exposes them. Missing setting details do not block launch.
5. Dispatch the reviewed steps. Agent-file edits during the run follow Codex's native behavior; the controller adds no watcher. Keep human questions and gates in the main task and relay answers to the same active child.

A missing name, malformed native definition, unsupported configured value, or child launch failure stops at the smallest safe boundary. Preflight rejection creates no workflow state or recovery record. A later dispatch failure retains completed-step evidence under the existing recovery contract.

Native `specify workflow run` does not interpret this contract in the tested CLI. The manual-prompt path remains usable with operator-directed agent selection and without claims of equivalent preflight guarantees.
