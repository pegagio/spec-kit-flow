# Contract: Agent Assignment Review

F014 reviews the agent on every delegated executable step in all eight source workflows, including branches that are not taken in a particular run and steps inside future `do-while` bodies. The four reviewed starting names are Architect, Builder, Coder, and Verifier. A new name is a proposal until its distinct responsibility and configuration are reviewed; no workflow source may use it early.

## Assignment record

The step inventory records one row per executable node:

| Field | Meaning |
|---|---|
| `workflow_id` | One of the eight reviewed `speckit-flow-*` IDs. |
| `step_id` | Globally unique ID within the workflow definition. |
| `step_type` | `prompt` or `command`; gates, switches, and loop containers remain in the main task. |
| `responsibility` | Concrete work and output expected from this step. |
| `delegated` | Explicit reviewed child marker; false means main-task execution. |
| `agent_name` | Exact native Codex name when delegated; absent otherwise. |
| `rationale` | Why this agent's instructions fit the responsibility. |
| `validation` | Structural preflight and native behavior evidence or an explicit remaining limit. |

An assignment is valid only when `flow_kit.delegated: true` and `flow_kit.agent` appear together on an executable child node, the name is reviewed, and full-graph preflight can launch that native agent. A name alone does not delegate. No workflow-level default, per-run agent/model/effort override, or fallback is allowed. Human gates, switches, and loop containers remain in the main task.

## Initial role heuristic

Use the following as a review starting point, not as an automatic rewrite:

| Responsibility | Starting name | Review concern |
|---|---|---|
| Specification, design, task decomposition, bounded artifact reconciliation | Architect | Check that work is design or artifact synthesis rather than verification. |
| Eligible implementation and code correction | Builder or Coder | Define a distinct purpose if both remain; do not assign by name alone. |
| Independent analysis, convergence assessment, roadmap brief/debrief, wiki lint | Verifier | Keep the assessor separate from the correction where practical. |
| Curated wiki ingestion and other specialized work | Review against the four names | Propose a fifth name only if none has a clear, maintainable responsibility fit. |

The current source has one `speckit.analyze` return step named Architect while other analysis steps use Verifier. Close Out's wiki ingest uses Builder. Those are review candidates, not preapproved changes.

## Repository-local native files

F014 adds usable `.codex/agents/*.toml` files in this source checkout for every selected name and replaces or retires the temporary Coder probe instructions. Each file has Codex-required `name`, `description`, and `developer_instructions`; optional model and reasoning effort remain Codex-owned and should be omitted unless a reviewed need is demonstrated. Instructions state role responsibilities and preserve task scope, main-task human gates, and stop behavior. They must not contain personal host paths, secrets, a FlowKit role map, or authority to invoke another workflow.

The source checkout is a consumer. These files do not become bundle payloads, and catalog installation, refresh, and removal continue to preserve consumer-owned agent files. A later feature may separately propose an opt-in or bundled consumer installation mechanism.

## Validation

Automated static validation checks all possible branches and loop bodies, exact names, and no delegation on main-task nodes. A scripted probe requests each distinct selected native name through the supported Codex client and captures machine-readable readiness and instruction-loading evidence when exposed. A task label is a launch cue, not proof of exact native selection; the report separates observed native selection from dispatch-only evidence and marks unavailable observations unverified. Record model/effort only when Codex exposes them. Missing, malformed, or unavailable names stop before workflow work without substitution. A no-op executable establishes dispatch structure only, not live-agent behavior. A final operator desktop check may confirm the visible experience, but automated validation does not depend on operator inspection.
