# Data Model: Codex Workflow Controllers

The installed workflow remains the authority for inputs, steps, branches, prompts, and gates. The controller stores only the execution identity and compact recovery evidence needed by Feature 013.

## Controller inventory

| Field | Meaning | Validation |
| --- | --- | --- |
| `skill_name` | Stable Codex invocation name from direct skill source | `flow-kit-{purpose}`, unique across the eight controllers and absent from consumer-owned skill names before installation |
| `display_name` | Human-facing Codex skill picker label | Matches the fixed purpose-to-display-name mapping in the controller contract |
| `workflow_id` | Corresponding installed FlowKit workflow | Exactly one of the eight pinned IDs; no substitute for a missing workflow |
| `controller_version` | Version of the reviewed FlowKit Codex skill package | Matches catalog release metadata and the local FlowKit skill ownership record |

Each inventory entry has one `workflow_id`; every pinned workflow has exactly one controller entry. The FlowKit catalog route owns an installed skill only while its recorded source and installed content match the ownership contract.

## Installed workflow snapshot

| Field | Meaning | Validation |
| --- | --- | --- |
| `workflow_id`, `version` | Identity from the composed installed definition | Match the invoked controller and bundle-compatible installed package |
| `specify_version` | Version of the selected executable used for read-only composition | Match the tested compatible release; missing, ambiguous, or incompatible runtime blocks preflight |
| `source_digest` | Digest of the composed definition used for this invocation | Captured before preflight; compare before each subsequent step and after a running child returns |
| `bundle_record_fingerprint` | Content digest and filesystem device/inode identity of the consumer bundle installation record | Captured after preflight; compare at each step boundary to detect refresh even if workflow bytes are unchanged |
| `skill_record_fingerprint` | Content digest and filesystem device/inode identity of the FlowKit skill ownership record | Captured after preflight; compare at each step boundary to detect skill-only refresh |
| `required_inputs` | Required fields from installed definition | Present and valid before any workflow step |
| `step_graph` | Ordered nested steps and switch branches | Every node and template form supported; all step IDs uniquely addressable |

The controller reads the installed definition once for the current step and retains the starting workflow, bundle-record, and skill-record identities for refresh detection. A change to any of them stops the invocation at the next safe boundary; it never switches to a refreshed graph mid-run. Because the bundle record is shared, an unrelated bundle update may cause a conservative stop.

## Effective step assignment

| Field | Meaning | Validation |
| --- | --- | --- |
| `step_id` | Named executable step, including one in an untaken branch | Unique in the composed graph |
| `declared_model` | Concrete `model` string on a prompt or command step | Nonempty; absent means execute in main task |
| `declared_effort` | FlowKit `reasoning_effort` on a modeled prompt or command step | Optional; absent resolves to `medium`; invalid without a model |
| `override_model`, `override_effort` | Operator's replacements for exactly one named step | Optional; never change other assignments |
| `effective_model`, `effective_effort` | Overrides if present, otherwise model declaration and declared effort or `medium` | Pair must pass live preflight before any workflow step |

Do not use a workflow-level model or effort default in this feature. A model or effort on a gate, switch, or unsupported node is invalid. The main task displays the complete assignment list, including branches that may not execute. Native Specify workflow execution does not apply FlowKit `reasoning_effort` metadata.

## Resolved workflow command

A command node retains its installed YAML `command` ID, rendered `integration`, and rendered arguments. For Codex skills mode, the controller derives the expected skill ID using the pinned Specify invocation rule and resolves it only in the selected consumer's installed `.agents/skills` inventory. The resolved skill's `SKILL.md` name and available source attribution must match the expected command. Missing, ambiguous, mismatched, or inaccessible skills stop the node without substitution. The rendered arguments belong to this one node and are passed unchanged to the main task or modeled child.

## Step result and human interaction

A step result records `step_id`, `kind`, `status` (`pending`, `running`, `waiting_for_human`, `completed`, or `incomplete`), effective model and reasoning effort if any, a compact outcome, and any structured output fields referenced by later template expressions. A modeled child has a stable child identity for the duration of that step. If it asks a question, the main task holds the question text and options, obtains an explicit human answer, and relays it to that same child before marking the step complete. Gate choices are main-task decisions and become step output for the installed switch expression.

Allowed transitions are `pending → running → completed`, `running → waiting_for_human → running`, and `running → incomplete`. A stop leaves unstarted steps pending and never automatically advances or retries an incomplete step.

## Stopped-run record

Initialize one compact JSON record under `.specify/flow-controllers/runs/<run-id>/summary.json` after successful preflight, then update it atomically before child dispatch and after each step or stop. It contains `run_id`, workflow ID/version/digest, starting bundle-record and skill-record fingerprints, controller package version, start/end status, each step's status, effective model, and reasoning effort, repository-relative changed-file paths, and a short stopping blocker or completion outcome. It does not contain child transcripts, secrets, absolute paths, or file contents. An interrupted main task leaves the last persisted step status visible; a `running` step is treated as incomplete evidence on inspection, never as permission to resume. Preserve the record and project edits when a child fails, the main task is interrupted, or a bundle or skill refresh is detected.

The run status moves from `preflight` to `running`, then to `completed` or `stopped`. A failed preflight reports its blocker in the main task without creating a recovery record, native workflow run, or mutated workflow artifact. There is no automatic transition from `stopped` back to `running`; the operator starts a new invocation after reviewing evidence.

## Skill ownership record

The FlowKit catalog route atomically writes `.specify/flow-kit/skills-install.json` with the controller package version, eight skill IDs, workflow bindings, and digests of every installed skill and shared helper file. Refresh replaces the record only after the new inventory is verified. A safe lifecycle check compares recorded digests with installed files before overwrite or deletion. Unknown, conflicting, or locally changed content is an ownership conflict and blocks that lifecycle operation until operator resolution. Successful removal verifies that owned files are gone, then removes this record; separate `.specify/flow-controllers/runs/` recovery summaries remain. Consumer-owned feedback and unrelated components are outside this ownership set. The native Specify bundle record remains separate and authoritative for Specify components.
