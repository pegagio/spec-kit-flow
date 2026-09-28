# Controller Invocation Contract

This contract describes the proposed Codex-facing behavior. The installed workflow YAML remains authoritative for its prompts, commands, gates, branches, declared models, and FlowKit reasoning-effort overrides.

## Skill identity and invocation

The reviewed Codex skill package provides `flow-kit-{purpose}` skills directly, where `{purpose}` is `start-feature`, `clarify`, `plan`, `tasks`, `analyze-remediate`, `implement`, `converge`, or `closeout`. Each skill binds exactly the corresponding installed `speckit-flow-{purpose}` workflow ID. The skills are not Specify extension commands. The operator invokes one skill in the selected consumer project task and supplies the inputs named by that workflow; the skill must not choose another workflow or project.

| Workflow purpose | Codex display name | Stable invocation name |
| --- | --- | --- |
| `start-feature` | FlowKit Start Feature | `flow-kit-start-feature` |
| `clarify` | FlowKit Clarify | `flow-kit-clarify` |
| `plan` | FlowKit Plan | `flow-kit-plan` |
| `tasks` | FlowKit Tasks | `flow-kit-tasks` |
| `analyze-remediate` | FlowKit Analyze | `flow-kit-analyze-remediate` |
| `implement` | FlowKit Implement | `flow-kit-implement` |
| `converge` | FlowKit Converge | `flow-kit-converge` |
| `closeout` | FlowKit Close Out | `flow-kit-closeout` |

The skill ID appears in the installed directory and `SKILL.md` frontmatter; the display name is Codex UI metadata in `agents/openai.yaml` under `interface.display_name`. The source package and supported FlowKit catalog route must preserve both exactly during installation and refresh. Ownership and removal checks use the explicit skill ID and installed-file digests. No Specify extension command or generated skill name is part of this identity.

Example invocation: `$flow-kit-clarify feature_context=013-bundle-workflow-launchers`. The controller shows missing required inputs and stops before execution. An operator may override `model=<concrete-id>` and/or `reasoning_effort=<supported-level>` for one `step_id=<named-step>` only; neither override changes another step.

## Workflow source and execution

The installed skill's portable shell bootstrap locates the selected consumer's compatible Specify executable and runs the controller with that runtime. The controller loads the composed installed workflow without dispatch, validates its ID and version, and reads required inputs and the complete step graph. The consumer does not need the maintainer's skill-tools Python environment. A missing executable, ambiguous runtime, incompatible version, or failed loader stops before any workflow step or recovery record. A step-level `model` and optional `reasoning_effort` are valid only for a `prompt` or `command` node; effort without a model is invalid. Example reviewed source:

```yaml
steps:
  - id: clarify-specification
    command: "speckit.clarify"
    model: "gpt-6-sol"
    integration: "{{ inputs.integration }}"
    input:
      args: "Clarify the active specification for {{ inputs.feature_context }}."
```

The example is a contract shape, not an already released assignment; its omitted effort means `medium` in FlowKit. A reviewed Luna step adds `reasoning_effort: high`. The controller executes unmodeled prompt and command nodes in the main task; it dispatches modeled nodes as bounded children using their effective model and effort. For each command node, it resolves the rendered Codex integration and command ID to a skill in the selected project's installed inventory, checks the skill's declared name and available provenance, and passes the rendered YAML arguments to that installed skill. The modeled child executes only that command node and returns its result; it does not bootstrap FlowKit, create a second run summary, own the workflow gate, or dispatch another child to re-run the node. A missing, ambiguous, mismatched, or inaccessible skill stops the node; the controller never substitutes an unchecked global skill or a copied command prompt. The helper may compose and inspect the workflow, render supported template references, and record results, but it must not call native `WorkflowEngine.execute` or `specify workflow run`. The controller supports ordered prompt/command execution, gate verdicts, and exact switch-case/default routing for the current eight graphs. It rejects an unknown node type or unresolved expression before proceeding. Native Specify execution ignores `reasoning_effort`; this field has an effect only through the FlowKit controller.

## Preflight and assignments

Before the first workflow step, the controller must:

1. Verify a compatible Specify loader, the corresponding installed workflow, and all required inputs in the selected project.
2. Traverse every possible branch and reject an empty, malformed, misplaced, or ambiguous step model or effort declaration. Omitted effort on a modeled step resolves to `medium`.
3. Apply operator model and/or effort overrides to one uniquely named step, if supplied; show all effective pairs, including untaken branches.
4. Prove each distinct effective model-effort pair can spawn a bounded child in this task with a no-project-work probe. A rejected or inconclusive probe stops the run. A successful probe is current evidence, not a guarantee of later access. Each modeled workflow node uses a new child; a probe child is never continued with workflow work.
5. Retain the starting workflow version and digest plus the consumer Specify bundle-record and FlowKit skill-record fingerprints in memory. Do not execute a workflow step, create a recovery record, or write native workflow run state when preflight fails.

The controller cannot silently replace a model or effort. If a later modeled dispatch fails despite preflight, stop with the original assignment and blocker.

## Human question and gate protocol

A modeled child returns a structured request such as:

```json
{
  "step_id": "clarify-specification",
  "kind": "question",
  "question": "Should the dashboard show one workflow or multiple workflows?",
  "options": ["One workflow", "Multiple workflows"],
  "allow_custom_answer": true
}
```

The main task presents those options to the human and accepts a selected or custom answer. It sends the answer to the same child identity, then waits for that child's continuation. A child never invents an answer or advances a review gate. The main task presents gate options directly from installed YAML, records the explicit verdict in the step result, and follows only the selected installed branch. If a question cannot be relayed or the same child cannot continue, stop with preserved edits and evidence.

The installed controller helper validates structured child questions, explicit answers and same-child targets, installed gate options, and one selected switch branch before the main task continues. Child options may be short strings or objects with `id` and `description`; the latter display their descriptions while answer selection resolves to their IDs. It accepts `allow_custom`, `custom_allowed`, or `allow_custom_answer` from a child and normalizes to `allow_custom_answer`; conflicting flags stop the step. These checks do not choose an answer or launch a workflow phase.

## Completion and stop behavior

The main task displays step progress, child results, and workspace diffs available in the selected project. It preserves an active child's partial edits on failure. It compares the installed workflow digest and both installation-record fingerprints before starting another step and after an active child returns; any change stops the run before another step. It leaves a compact local summary as defined in [data-model.md](../data-model.md). It does not auto-resume after main-task interruption, launch the next workflow phase, integrate Git, mark roadmap verification, or accept a feature.
