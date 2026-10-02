# Contract: Agent Assignment Review

F014 reviews the agent on every delegated executable step in all ten active source workflows, including branches that are not taken in a particular run and steps inside future `do-while` bodies. The reviewed work-type names are Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator. Author and reviewer roles remain distinct. This assignment change reuses existing workflow assessment nodes and MUST NOT add nodes.

## Assignment record

The step inventory records one row per executable node:

| Field | Meaning |
|---|---|
| `workflow_id` | One of the ten active reviewed `speckit-flow-*` IDs. |
| `step_id` | Globally unique ID within the workflow definition. |
| `step_type` | `prompt` or `command`; gates, switches, and loop containers remain in the main task. |
| `responsibility` | Concrete work and output expected from this step. |
| `delegated` | Explicit reviewed child marker; false means main-task execution. |
| `agent_name` | Exact native Codex name when delegated; absent otherwise. |
| `rationale` | Why this agent's instructions fit the responsibility. |
| `validation` | Structural preflight and native behavior evidence or an explicit remaining limit. |

An assignment is valid only when `flow_kit.delegated: true` and `flow_kit.agent` appear together on an executable child node, the name is reviewed, and full-graph preflight can launch that native agent. A name alone does not delegate. No workflow-level default, per-run agent/model/effort override, or fallback is allowed. Human gates, switches, and loop containers remain in the main task.

## Reviewed role responsibilities

Use the following as a review starting point, not as an automatic rewrite:

| Responsibility | Name | Review boundary |
|---|---|---|
| Read or perform roadmap operations | Roadmap Agent | May apply only an exact change supplied by a declared workflow after the main task records required operator approval; the agent never approves or broadens it. |
| Author or clarify feature specifications | Specifier | Completes command-required author self-checks; independent specification assessment belongs to a different assigned role. |
| Create or reconcile technical plans | Planner | Completes command-required author self-checks; independent plan assessment belongs to Reviewer. |
| Decompose or reconcile implementation tasks | Tasker | Completes command-required author self-checks; independent task assessment belongs to Reviewer. |
| Review specifications, plans, tasks, and roadmap alignment | Reviewer | Existing assessments return findings through their current correction path or report a precise bounded stop. |
| Implement code | Coder | Implementation progress is reviewed by a separate Code Reviewer assignment at the existing assessment point. |
| Review implementation changes | Code Reviewer | Distinct from Coder and from the higher-level Reviewer. Uses only an existing workflow assessment node. |
| Ingest and maintain cited wiki pages | Wiki Curator | Remains within selected and authorized source scope. |

Exact source assignments and current correction routes appear in the agent-assignment inventory. A report-only or linkage node must not be described as a retry loop; it returns material findings as blocked with a resumption action when no existing correction route is available.

## Repository-local native files

F014 adds usable `.codex/agents/*.toml` files in this source checkout for every selected name and replaces or retires the temporary Coder probe instructions. Each file has Codex-required `name`, `description`, and `developer_instructions`; optional model and reasoning effort remain Codex-owned and should be omitted unless a reviewed need is demonstrated. Instructions state role responsibilities and preserve task scope, main-task human gates, and stop behavior. They must not contain personal host paths, secrets, a FlowKit role map, or authority to invoke another workflow.

The source checkout is a consumer. These files do not become bundle payloads, and catalog installation, refresh, and removal continue to preserve consumer-owned agent files. A later feature may separately propose an opt-in or bundled consumer installation mechanism.

## Validation

Automated static validation checks all possible branches and loop bodies, exact names, and no delegation on main-task nodes. A scripted probe requests each distinct selected native name through the supported Codex client and captures machine-readable readiness and instruction-loading evidence when exposed. A task label is a launch cue, not proof of exact native selection; the report separates observed native selection from dispatch-only evidence and marks unavailable observations unverified. Record model/effort only when Codex exposes them. Missing, malformed, or unavailable names stop before workflow work without substitution. A no-op executable establishes dispatch structure only, not live-agent behavior. A final operator desktop check may confirm the visible experience, but automated validation does not depend on operator inspection.
