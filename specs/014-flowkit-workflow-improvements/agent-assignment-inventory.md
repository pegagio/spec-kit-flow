# F014 Agent Assignment Review

This inventory groups every delegated node in the ten active workflow definitions by the work it performs. The baseline assignment records the prior source name; the applied assignment records the reviewed role now present in workflow source. Each role has its own native definition and may be tuned independently, even when two definitions initially use similar instructions. The inventory reflects the approved assignment direction and the no-new-node constraint.

## Assignment principles for review

- Steps that write or modify application code should use **Coder**. This applies to every `speckit.implement` node, including implementation nested inside Converge or Close Out.
- Repeated instances of the same responsibility should use one reviewed name across workflows.
- Use task-specific names to identify the kind of work at a glance: **Roadmap Agent**, **Specifier**, **Planner**, **Tasker**, **Reviewer**, **Coder**, **Code Reviewer**, and **Wiki Curator**.
- A named agent describes work delegated to that child. Main-task gates, switches, loop control, and operator decisions remain in the main task.
- The Roadmap Agent may read, prepare, or apply exact roadmap changes when a future workflow declares the step. Exact-patch approval remains with the main task; the agent cannot approve or broaden a change.
- Authors complete the invoked command's mandatory self-checks and quality checklists. Those checks do not replace independent review and do not authorize an author to act as its own independent Reviewer.
- A Reviewer must not be the same agent type that authored the specification, plan, task list, or roadmap-aligned artifact it reviews. A Code Reviewer is separate from the higher-level Reviewer and inspects implementation changes.
- Reviewing an artifact means assessing its content against its source requirements and identifying actionable gaps. Existence and non-placeholder checks remain useful evidence, but do not alone establish an independent review.
- Reuse existing assessment nodes for review. Do not add workflow nodes as part of this assignment change; if a current node has no safe correction route for a finding, it returns a specific blocked outcome for operator resumption.

## Responsibility groups

### Read project state and prepare operator decisions

These steps gather roadmap or active-feature context and prepare information for a main-task decision or a later authoring step. Their conclusions do not authorize a gate or change project state by themselves.

| Workflow / step | Baseline agent | Work performed | Applied assignment |
|---|---|---|---|
| Select Feature / `list-roadmap-options` | Architect | Read the roadmap, list available features, and explain dependencies. | **Roadmap Agent** — group with other roadmap operations; this role can also prepare or apply an exact approved patch in a future declared step. The operator selects. |
| Select Feature / `prepare-feature-selection` | Architect | Re-read the selected roadmap entry and prepare its exact identity and dependencies. | **Roadmap Agent** — preserve the exact selection supplied by the operator. |
| Specify / `inspect-active-feature` | Architect | Read the active-feature pointer and roadmap and verify the selected target. | **Roadmap Agent** — read the roadmap consistently while preserving exact target identity. |
| Specify / `prepare-specification-request` | Architect | Prepare the authoring context from the selected entry and existing artifacts. | **Specifier** — this step synthesizes context for specification authoring rather than only reporting source facts. |
| Close Out / `prepare-wiki-maintenance` | Verifier | Re-read the roadmap entry and specification and curate authorized wiki sources. | **Roadmap Agent** — read roadmap context and select sources within the authorized workflow scope. |

### Create or reconcile specification, plan, and task artifacts

These are artifact-authoring commands. They share the same waterfall order when multiple layers need correction, but each command has different judgment and mechanics.

| Workflow / step | Baseline agent | Work performed | Applied assignment |
|---|---|---|---|
| Specify / `draft-specification` | Architect | Create the selected feature specification. | **Specifier** — own feature-level specification decisions. A separate Reviewer must assess the resulting specification. |
| Analyze and Remediate / `remediate-specification` | Architect | Revise the specification from accepted analysis findings. | **Specifier** — same specification-authoring responsibility. |
| Converge / `reconcile-convergence-specification` | Architect | Flow implementation findings into the specification. | **Specifier** — same specification-reconciliation responsibility. |
| Converge / `append-task-remediation` | Architect | Run convergence to identify remaining work and append remediation tasks before the shared artifact waterfall. | **Tasker** — the command records observed gaps as tasks, grouping it with task generation. |
| Close Out / `mark-converged-specification-complete` | Architect | Update the existing specification lifecycle state after evidence supports completion. | **Specifier** — bounded specification-state change from completed evidence. |
| Close Out / `reconcile-closeout-specification` | Architect | Revise the specification from debrief findings. | **Specifier** — same specification-reconciliation responsibility. |
| Plan / `create-plan` | Architect | Generate the technical plan from the reviewed specification. | **Planner** — own plan creation and technical design decisions. A separate Reviewer must assess the resulting plan. |
| Analyze and Remediate / `remediate-plan` | Architect | Revise the plan from accepted analysis findings. | **Planner** — same plan-authoring responsibility. |
| Converge / `reconcile-convergence-plan` | Architect | Flow implementation findings into the plan. | **Planner** — same plan-reconciliation responsibility. |
| Close Out / `reconcile-closeout-plan` | Architect | Revise the plan from debrief findings. | **Planner** — same plan-reconciliation responsibility. |
| Tasks / `generate-tasks` | Architect | Mechanically decompose reviewed specification and plan into ordered tasks. | **Tasker** — mechanical decomposition from approved upstream artifacts. A separate Reviewer must assess the task coverage and dependencies. |
| Analyze and Remediate / `remediate-tasks` | Architect | Revise tasks to match accepted analysis findings and upstream artifacts. | **Tasker** — same task-generation/reconciliation responsibility. |
| Converge / `reconcile-convergence-tasks` | Architect | Record accepted implementation remediation as tasks. | **Tasker** — same task-recording responsibility. |
| Close Out / `reconcile-closeout-tasks` | Architect | Revise tasks from debrief findings. | **Tasker** — same task-generation/reconciliation responsibility. |

### Implement code

The baseline source called these implementation commands through Builder. The applied assignment uses Coder as directed.

| Workflow / step | Baseline agent | Work performed | Applied assignment |
|---|---|---|---|
| Implement / `implement-eligible-work` | Builder | Implement existing eligible tasks. | **Coder** — implement eligible feature tasks; a separate Code Reviewer must inspect the changes. |
| Converge / `implement-remediation` | Builder | Implement eligible remediation tasks after analysis. | **Coder** — same implementation responsibility; a separate Code Reviewer must inspect the changes. |
| Close Out / `implement-closeout-eligible-tasks` | Builder | Implement eligible tasks discovered during closeout remediation. | **Coder** — same implementation responsibility; a separate Code Reviewer must inspect the changes. |

### Assess evidence, analyze artifacts, and verify outcomes

These steps inspect current artifacts or command reports, classify evidence, or verify that a declared condition holds. Their assessment authority stays bounded by the workflow and main-task gates.

| Workflow / step | Baseline agent | Work performed | Applied assignment |
|---|---|---|---|
| Analyze and Remediate / `analyze-artifacts` | Verifier | Run cross-artifact analysis. | **Reviewer** — analyze artifact consistency. |
| Analyze and Remediate / `assess-analysis` | Verifier | Classify the fresh analysis report and current state. | **Reviewer** — assess evidence and progress. |
| Clarify / `assess-clarification-after-session` | Verifier | Determine whether significant ambiguity remains after the core clarify session. | **Reviewer** — assess remaining ambiguity from the updated spec and operator answers. |
| Select Feature / `verify-feature-selection` | Verifier | Verify the exact selected roadmap entry and active pointer agree. | **Reviewer** — verify the approved choice and resulting pointer. |
| Specify / `assess-created-spec-linkage` | Verifier | Check the created specification against the selected roadmap mapping and active pointer. | **Reviewer** — verify exact target and roadmap linkage; broader roadmap alignment is checked by the existing brief step. |
| Specify / `verify-repaired-spec-linkage` | Verifier | Re-check linkage after an approved roadmap repair. | **Reviewer** — same linkage verification responsibility. |
| Specify / `brief-against-roadmap` | Verifier | Run the shared roadmap brief against the authored specification. | **Reviewer** — assess the authored spec against the roadmap while retaining the exact selected target. |
| Plan / `verify-plan-output` | Verifier | Check plan outputs against required artifacts and prior gaps. | **Reviewer** — review plan content against the specification and prior gaps; return exact repairable findings through the existing plan loop. |
| Tasks / `verify-task-output` | Verifier | Check generated tasks against required artifacts and prior gaps. | **Reviewer** — review task coverage and dependencies against the specification and plan; return exact repairable findings through the existing task loop. |
| Implement / `assess-implementation-state` | Verifier | Determine whether eligible planned work remains before implementation. | **Reviewer** — assess current task evidence and eligibility. |
| Implement / `assess-implementation-after-pass` | Verifier | Reassess task progress and evidence after an implementation session. | **Code Reviewer** — review changed code and validation evidence as part of the existing post-pass assessment; route findings through remaining tasks or a specific blocked outcome. |
| Converge / `assess-convergence` | Verifier | Classify the fresh convergence report. | **Code Reviewer** — after each convergence command, inspect implementation changes since the prior pass as well as the report; route findings through the existing waterfall or bounded stop. |
| Converge / `analyze-remediation-tasks` | Verifier | Analyze remediation tasks before implementation. | **Reviewer** — same analysis responsibility as other `speckit.analyze` nodes. |
| Converge / `assess-remediation-eligibility` | Verifier | Check whether analyzed remediation tasks are eligible for implementation. | **Reviewer** — assess evidence and eligibility. |
| Close Out / `assess-closeout-readiness` | Verifier | Assess convergence, completion authority, lifecycle state, and roadmap evidence. | **Reviewer** — assess evidence; consequential roadmap approval stays in the main task. |
| Close Out / `debrief-roadmap` | Verifier | Compare implementation with the roadmap. | **Reviewer** — review implementation against roadmap expectations. |
| Close Out / `assess-closeout-debrief` | Verifier | Classify the fresh debrief report and current state. | **Code Reviewer** — inspect implementation changes alongside the fresh debrief; route findings through the existing correction waterfall or bounded stop. |
| Close Out / `analyze-closeout-artifacts` | Verifier | Analyze artifacts after debrief remediation. | **Reviewer** — same analysis responsibility as other `speckit.analyze` nodes. |
| Close Out / `assess-closeout-task-eligibility` | Verifier | Check whether remediation tasks are eligible for implementation. | **Reviewer** — assess evidence and eligibility. |
| Close Out / `lint-wiki` | Verifier | Run wiki lint and report findings. | **Reviewer** — collect findings and retain their scope. |
| Close Out / `assess-wiki-maintenance` | Verifier | Assess source coverage, ingestion, and fresh lint results. | **Reviewer** — assess source coverage and lint evidence. |
| Close Out / `verify-closeout-readiness` | Verifier | Confirm readiness from completed evidence and controller decisions. | **Reviewer** — verify readiness; commit and acceptance remain outside delegated authority. |
| Wiki Lint Update / `lint-wiki` | Verifier | Run the standalone wiki lint. | **Reviewer** — same lint responsibility as Close Out. |
| Wiki Lint Update / `assess-wiki-findings` | Verifier | Assess fresh findings and permitted source refreshes. | **Reviewer** — assess evidence and permitted remediation. |

### Ingest and update wiki pages

These commands synthesize registered source material into cited wiki pages. Their baseline assignment was Builder; both now use Wiki Curator.

| Workflow / step | Current agent | Work performed | Proposed assignment |
|---|---|---|---|
| Close Out / `ingest-curated-context` | Builder | Ingest selected registered sources into the wiki. | **Wiki Curator** — maintain cited wiki knowledge from selected registered sources. |
| Wiki Lint Update / `refresh-stale-source` | Builder | Re-ingest one authorized registered stale source. | **Wiki Curator** — same source-ingestion responsibility. |

### Clarify feature requirements

| Workflow / step | Baseline agent | Work performed | Applied assignment |
|---|---|---|---|
| Clarify / `clarify-session` | Architect | Run the core clarification skill with the operator. | **Specifier** — keep feature-level clarification with specification work; substantive questions remain in the main task. |

## Applied assignment decisions

1. Apply task-specific labels: Roadmap Agent, Specifier, Planner, Tasker, Reviewer, Coder, Code Reviewer, and Wiki Curator.
2. Use Reviewer for independent specification, plan, task, and roadmap-alignment reviews; use Code Reviewer for implementation review.
3. Use Planner for plan creation and flowback and Tasker for task generation and reconciliation. This separates design planning from mechanical task decomposition.
4. Use Specifier for specification authoring and feature clarification, Roadmap Agent for roadmap operations, Coder for all three implementation commands, and Wiki Curator for ingestion.
5. Reuse existing assessment nodes only: Plan and Tasks verification loops return exact content findings to their respective authoring steps; Implement, Converge, and Close Out assessments inspect implementation changes and route findings through their existing correction paths. No workflow nodes are added. Specify's existing roadmap brief assesses alignment, while exact mapping linkage remains covered by its linkage assessments.

The names identify work types and do not prescribe model or effort settings; each native definition can be tuned independently, and some may begin with similar instructions. This assignment change adds no workflow nodes. Roadmap writing remains subject to its existing main-task approval gates.
