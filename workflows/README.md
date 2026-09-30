# Spec Kit Flow Workflows

These are the reviewed, versioned source packages for the human-directed Spec Kit Flow super-states. Install a package only from its reviewed directory, validate native list, information, resolution, registry attribution, and source-copy equality, and never edit an installed copy. The FlowKit catalog also installs a direct Codex skill for each workflow; these controller skills follow the installed YAML and keep its prompts, commands, gates, and branches authoritative.

Each packaged workflow preserves its manual-prompt fallback and explicit human gates. Delegated executable steps name a reviewed Codex custom agent in `flow_kit.agent`; Codex loads that agent's consumer-owned configuration. FlowKit does not map roles to models or parse custom-agent TOML. Executable steps without delegation metadata, gates, branch decisions, and questions remain in the main Codex task.

Use the selected consumer project in the Codex task and invoke one skill at a time. Required inputs come from the installed workflow definition:

| Workflow | Codex skill and display name | Required input | Delegated step agents |
| --- | --- | --- | --- |
| `speckit-flow-start-feature` | `$flow-kit-start-feature` — FlowKit Start Feature | `feature_request` | `assess-eligibility`, `draft-specification`: Architect; `assess-created-spec-linkage`, `verify-repaired-spec-linkage`, both brief steps: Verifier |
| `speckit-flow-clarify` | `$flow-kit-clarify` — FlowKit Clarify | `feature_context` | `clarify-session`: Architect; ambiguity assessments: Verifier |
| `speckit-flow-plan` | `$flow-kit-plan` — FlowKit Plan | `feature_context` | `create-plan`: Architect; `verify-plan-output`: Verifier |
| `speckit-flow-tasks` | `$flow-kit-tasks` — FlowKit Tasks | `feature_context` | `generate-tasks`: Architect; `verify-task-output`: Verifier |
| `speckit-flow-analyze-remediate` | `$flow-kit-analyze-remediate` — FlowKit Analyze | `feature_context` | `analyze-artifacts`, `assess-analysis`: Verifier; `remediate-specification`, `remediate-plan`, `remediate-tasks`: Architect |
| `speckit-flow-implement` | `$flow-kit-implement` — FlowKit Implement | `feature_context` | task assessments: Verifier; `implement-eligible-work`: Builder |
| `speckit-flow-converge` | `$flow-kit-converge` — FlowKit Converge | `feature_context` | task recording and shared waterfall stages: Architect; analysis, eligibility, and convergence assessment: Verifier; `implement-remediation`: Builder |
| `speckit-flow-closeout` | `$flow-kit-closeout` — FlowKit Close Out | `feature_context` (exact repository-relative spec directory) | assessment, analysis, debrief, and lint: Verifier; spec/plan/tasks correction: Architect; eligible implementation and wiki ingest: Builder |

For example: `$flow-kit-clarify feature_context=013`. The controller checks the selected compatible Specify runtime and installed workflow, then validates every named assignment across possible branches. It requests each native child with the exact reviewed `agent_type`. Codex's subagent activity shows each launch: probe labels include the agent name, and work-child labels include the agent name and step ID. Model and effort appear when Codex exposes them. The label provides launch visibility; the exact `agent_type` request establishes native selection. No run-time assignment override is available. Codex custom-agent configuration belongs to the consumer and is loaded by Codex itself. Clarification questions and review gates appear in the main task. A child question is answered there and relayed to the same child. The main task reports results and visible workspace diffs. Use the manual paths below if named-agent dispatch is unavailable.

For a project-scoped agent, create a file such as `.codex/agents/architect.toml` in the consumer project:

```toml
name = "Architect"
description = "Plans and reviews workflow changes."
developer_instructions = "Follow the task scope and return a concise result to the parent."
```

A delegated workflow step names the matching native agent directly:

```yaml
- id: analyze-artifacts
  flow_kit:
    delegated: true
    agent: Verifier
  command: "speckit.analyze"
  integration: "{{ inputs.integration }}"
```

Codex owns optional `model` and `model_reasoning_effort` fields and their inheritance behavior. FlowKit does not read or change `.codex/agents/` files. Each delegated workflow step must use one of the reviewed names: Architect, Builder, Coder, or Verifier.

| Workflow | Core or extension commands |
| --- | --- |
| `speckit-flow-start-feature` | `speckit.flow-roadmap.write`, `speckit.flow-wiki.query`, `speckit.specify`, `speckit.flow-roadmap.brief` |
| `speckit-flow-clarify` | `speckit.clarify` |
| `speckit-flow-plan` | `speckit.plan`, `speckit.clarify` |
| `speckit-flow-tasks` | `speckit.tasks` |
| `speckit-flow-analyze-remediate` | `speckit.analyze`, `speckit.specify`, `speckit.plan`, `speckit.tasks` |
| `speckit-flow-implement` | `speckit.implement` |
| `speckit-flow-converge` | `speckit.converge`, `speckit.specify`, `speckit.plan`, `speckit.tasks`, `speckit.analyze`, `speckit.implement` |
| `speckit-flow-closeout` | `speckit.specify`, `speckit.plan`, `speckit.tasks`, `speckit.analyze`, `speckit.implement`, `speckit.flow-roadmap.debrief`, `speckit.flow-roadmap.write`, `speckit.flow-wiki.ingest`, `speckit.flow-wiki.lint` |

## Manual start-feature path

When native workflow dispatch is unavailable, the operator can follow the reviewed `speckit-flow-start-feature` source manually:

1. Select one roadmap candidate and record its exact roadmap entry identifier, eligibility, dependencies, and governing context. Prepare the exact proposed status patch without applying it. Never infer the entry from its feature number alone. Stop if the candidate or entry identifier is ambiguous, blocked, or lacks governing context.
2. Review the proposed patch with the human operator. Apply only the approved patch with `speckit.flow-roadmap.write`; amendment, context resolution, or deferral ends this attempt without applying it.
3. Query cited governing context and its coverage with `speckit.flow-wiki.query`, then use `speckit.specify` to draft the approved feature.
4. Read the actual created spec directory from `.specify/feature.json` and the files on disk. Compare its exact repository-relative directory with the `Spec dir` mapping on the exact selected roadmap entry and check that no other entry claims that directory. Write the path inside backticks with a trailing slash and no punctuation before the closing backtick. If the mapping is unique and exact, run `speckit.flow-roadmap.brief` with both explicit `SPEC_TARGET` and `ROADMAP_ENTRY` constraints.
5. If the selected entry is uniquely identified and its mapping is missing or stale, with no competing owner for the actual spec directory, prepare the minimal exact `Spec dir` patch and show it to the operator. Apply only that exact approved patch with `speckit.flow-roadmap.write`, reread the roadmap, verify the unique exact mapping, and refresh the brief with both explicit constraints. Amendment or deferral makes no roadmap change. If entry identity, directory ownership, or the repaired mapping is conflicting or ambiguous, stop with the evidence and smallest safe operator action.
6. Present the specification and uniquely matched brief for human review. The operator chooses clarification, roadmap amendment, context resolution, planning readiness, or deferral. Start any next workflow only on a separate operator instruction.

## Manual clarification path

When native clarification dispatch is unavailable, run `speckit.clarify` on the operator-selected active specification one session at a time within the same invocation. The command checks for significant ambiguity and may finish without questions. The five-question cap applies per session. Present every substantive question in the main task, wait for the operator's answer, and apply only that answer to the current session. After each session, assess the current specification and confirm that the session resolved a significant ambiguity before continuing. On later sessions, compare against the previous assessment's remaining question IDs.

Stop as clarified when no significant unresolved ambiguity remains, without invoking Plan or treating that result as automatic planning approval. Stop with a specific decision when the question is outside Clarify's authority, on no measurable progress, after five sessions, or on a genuine blocker. Preserve accepted answers and report remaining question IDs with the smallest safe resumption action.

## Manual planning path

When native planning dispatch is unavailable, record the missing required planning files or placeholder sections for the operator-selected reviewed specification, then invoke `speckit.plan`. Let the core skill perform research, constitutional gates, and design generation; keep technical work within the feature scope and ask the operator for substantive product decisions.

Check that required and applicable outputs exist and contain substantive content, accepting justified not-applicable sections. This checks deliverable production, not design quality. If gaps remain and a prior output gap was filled, feed the exact missing files or sections back into `speckit.plan`, preserving completed design. Stop when outputs are populated, an operator answer or blocker prevents continuation, no progress occurs, or the five-pass safety limit is reached. Present artifacts and the exact outcome for review; task generation requires a separate operator instruction.

## Manual task-generation path

When native task workflow dispatch is unavailable, record exact missing task output or coverage gaps from the reviewed specification and design, then invoke `speckit.tasks` without a routine pre-generation question. Check that tasks.md is populated with correctly formatted tasks, applicable story phases, dependency coverage, independent test criteria, and the core skill's supporting sections. Unchecked implementation tasks are expected; completion here means generation is finished.

If gaps remain and a prior gap was filled, feed the exact remaining gaps back into `speckit.tasks`, preserving task IDs, completion markers, approved decisions, and completed work. Stop with the exact material design gap, missing prerequisite, operator question, no-progress result, or five-pass safety limit. Present the task plan for review; the operator may separately invoke Analyze. Task generation does not change reviewed design or begin implementation.

## Manual analysis and remediation path

When native analysis dispatch is unavailable, use the same evidence-based continuation contract manually. Run fresh `speckit.analyze` on the active specification, plan, and tasks without modifying them, then classify that report from its findings and current artifacts; missing, failed, or stale analysis is a blocker. Every correction decision uses the latest completed analyzer report; do not ask the operator to classify a routine result. Clean analysis ends successfully, while consequential decisions and genuine blockers stop with the evidence and required operator action.

Use one shared specification → plan → tasks waterfall, entering at the highest affected artifact. The first loop pass skips all corrections and establishes the read-only analysis baseline. For routine findings within the issued scope, enter the waterfall and then run the same analyzer and assessment again: specification changes require `speckit.specify` → `speckit.plan` → `speckit.tasks` → `speckit.analyze`; plan changes require plan → tasks → analyze; task changes require tasks → analyze. Continue while each pass resolves tracked findings. Stop on repeated findings, no measurable progress, stale evidence, an exhausted five-pass safety cap for corrections (six total passes including the baseline), or a blocker. Preserve completed work and report the smallest safe resumption action. Constitutional amendments, authority or material-scope changes, and ambiguous recovery require an explicit operator decision.

## Manual implementation path

When native implementation dispatch is unavailable, first record unfinished eligible task IDs from the operator-selected feature's existing task plan. If none remain, verify completion and stop. Otherwise invoke `speckit.implement` for all remaining eligible tasks. After each session, inspect current task and validation evidence against the prior task list. If eligible tasks remain and the session completed a previously unfinished task, run another implementation session. Continue until complete, a concrete blocker or required operator input, no progress, or the five-pass safety cap. The FlowKit wrapper does not invoke Specify, Plan, Tasks, Analyze, or another FlowKit workflow.

Report completed and remaining task IDs, validation results, changed paths, and the exact blocker or operator question when work stops. Confirm completion from the task checklist and validation evidence, not merely command success. Treat no progress or cap exhaustion as a bounded stop, preserve completed work, and identify a safe resumption point. Leave Converge, roadmap verification, Git integration, and acceptance for separate operator action.

## Manual convergence path

When native convergence dispatch is unavailable, run `speckit.converge` for the operator-selected implemented feature on every pass. Classify its fresh findings, appended remediation tasks, prerequisite errors, and validation evidence. The command owns gap detection and task recording; the wrapper assessment owns routing and loop control. A clean result stops at Feature Converged; Close Out requires a separate operator instruction.

For routine in-scope findings, enter the shared specification → plan → tasks waterfall at the highest affected artifact; implementation-only gaps skip all three stages. Preserve existing task IDs, completion markers, and convergence work. Analyze changed tasks before implementation; check fresh analysis and exact task eligibility before invoking `speckit.implement`. Already recorded work also receives fresh analysis. An analysis blocker or required operator decision prevents implementation and stops with the exact required action.

After implementation, return directly to `speckit.converge` within the same invocation. Compare its next report against the prior gap baseline before authorizing another correction. A prior gap must be resolved in current behavior and validation; appended tasks, checkbox claims, and changed bytes alone do not demonstrate progress. Five correction passes are followed by a final convergence check, using six total loop passes. Stop before further correction on no progress, repeated findings, stale evidence, failed prerequisites, or cap exhaustion. Substantive product, constitutional, authority, material-scope, and ambiguous-recovery decisions require operator input without taking the consequential action. One main-task report handles every final outcome, preserving completed work and the exact resumption action. Convergence does not integrate Git, update the roadmap, accept the feature, or invoke Close Out.

## Manual closeout path

When native closeout dispatch is unavailable, identify the feature by its exact repository-relative specification directory and inspect current convergence and completion evidence. Clear evidence authorizes an in-place Draft-to-Complete update to that existing specification; do not create a feature or change its requirements. Pass the explicit `SPEC_TARGET` to every debrief and approved roadmap-write command. Run `speckit.flow-roadmap.debrief` on refreshed evidence. For a routine, in-scope finding, correct the smallest affected artifact, reconcile dependent plan and task artifacts, analyze changed tasks, implement only eligible work, and rerun debrief. Continue only when fresh evidence shows measurable progress, with a five-pass maximum; stop for ambiguity, consequential decisions, stale evidence, repeated findings, no progress, missing prerequisites, or exhausted passes. Present the exact roadmap verification patch for approval before running `speckit.flow-roadmap.write`. After approval, curate durable wiki context, run wiki lint, and present commit readiness separately; closeout does not commit, integrate Git, or accept the feature.
