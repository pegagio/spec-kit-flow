# Spec Kit Flow Workflows

These are the reviewed, versioned source packages for the human-directed Spec Kit Flow super-states. Install a package only from its reviewed directory, validate native list, information, resolution, registry attribution, and source-copy equality, and never edit an installed copy.

Each workflow preserves its manual prompt fallback and explicit human gates. None selects, ranks, assigns, launches, schedules, supervises, or terminates an agent; provider and model policy remain outside this bundle.

| Workflow | Core or extension commands |
| --- | --- |
| `speckit-flow-start-feature` | `speckit.flow-roadmap.write`, `speckit.flow-wiki.query`, `speckit.specify`, `speckit.flow-roadmap.brief` |
| `speckit-flow-clarify` | `speckit.clarify` |
| `speckit-flow-plan` | `speckit.plan`, `speckit.clarify` |
| `speckit-flow-tasks` | `speckit.tasks`, `speckit.plan` |
| `speckit-flow-analyze-remediate` | `speckit.analyze`, `speckit.specify`, `speckit.plan`, `speckit.tasks` |
| `speckit-flow-implement` | `speckit.implement`, `speckit.analyze`, `speckit.specify`, `speckit.plan`, `speckit.tasks` |
| `speckit-flow-converge` | `speckit.converge`, `speckit.analyze` |
| `speckit-flow-closeout` | `speckit.flow-roadmap.debrief`, `speckit.flow-roadmap.write`, `speckit.flow-wiki.ingest`, `speckit.flow-wiki.lint` |

## Manual start-feature path

When native workflow dispatch is unavailable, the operator can follow the reviewed `speckit-flow-start-feature` source manually:

1. Select one roadmap candidate and assess its eligibility, dependencies, and governing context. Prepare the exact proposed status patch without applying it. Stop if the candidate is ambiguous, blocked, or lacks governing context.
2. Review the proposed patch with the human operator. Apply only the approved patch with `speckit.flow-roadmap.write`; amendment, context resolution, or deferral ends this attempt without applying it.
3. Query cited governing context and its coverage with `speckit.flow-wiki.query`. Use `speckit.specify` to draft the approved feature, then `speckit.flow-roadmap.brief` to compare it with the roadmap entry.
4. Present the specification and brief for human review. The operator chooses clarification, roadmap amendment, context resolution, planning readiness, or deferral. Start any next workflow only on a separate operator instruction.

## Manual clarification path

When native clarification dispatch is unavailable, run `speckit.clarify` for the operator-selected active feature. Present one question at a time, obtain the operator's answer, and update the specification after each accepted answer. Treat the command's current five-question cap as the end of one session; report resolved, outstanding, and deferred ambiguity without assuming readiness.

After reviewing that result, the operator may request another `speckit-flow-clarify` session on the same feature, choose to begin planning, or defer a bounded concern. Record the choice and stop. Planning and another clarification session each require a separate operator instruction.

## Manual planning path

When native planning dispatch is unavailable, ask the operator to review the clarified specification and explicitly confirm planning readiness. If a prerequisite or material product decision is missing, return to `speckit.clarify` for the same feature; if planning is deferred, stop without creating design artifacts.

Only after the operator confirms readiness, run `speckit.plan` for the selected feature. Present the plan, research, data model, contracts, and quickstart for review, then stop. Task generation requires a separate operator instruction.

## Manual task-generation path

When native task workflow dispatch is unavailable, run `speckit.tasks` for the operator-selected planned feature using its reviewed design artifacts. Review the dependency order, coverage, and any surprising human actions with the operator. Do not silently revise the plan to accommodate a new product decision.

If the proposal is acceptable, stop and ask the operator to invoke `speckit-flow-analyze-remediate` separately. If review finds a material design gap, return to `speckit.plan` for the same feature. An explicit task amendment or deferral ends this attempt without marking the proposal ready for implementation.

## Manual analysis and remediation path

When native analysis dispatch is unavailable, run `speckit.analyze` on the active specification, plan, and tasks without modifying them. Present the findings and ask the operator to classify the result. A clean result stops with implementation available only on a separate operator instruction.

For routine findings within the issued scope, update the smallest affected artifact path, then reanalyze: specification changes require `speckit.specify` → `speckit.plan` → `speckit.tasks` → `speckit.analyze`; plan changes require plan → tasks → analyze; task changes require tasks → analyze. Stop for constitutional amendments, authority or material-scope changes, ambiguous recovery, blockers, and unrecognized decisions. Preserve the report and obtain the relevant explicit operator decision before those changes.

## Manual implementation path

When native implementation dispatch is unavailable, use `speckit.implement` only for the operator-selected feature, current agent, and remaining eligible tasks after clean analysis. Verify prerequisites and dependencies, execute within scope, and present task results, tests, discoveries, and blockers for human review.

If work is complete, stop and let the operator invoke `speckit-flow-converge` separately. For a discovery, return to the smallest affected specification, plan, task, or analysis path; reconcile dependent artifacts and reanalyze before resuming implementation. For a blocker or unrecognized result, stop with the issue and required operator input. Do not infer roadmap verification, Git integration, or acceptance from execution.

## Manual convergence path

When native convergence dispatch is unavailable, run `speckit.converge` for the operator-selected implemented feature and review its assessment against the current specification, plan, and tasks. A clean result stops at Feature Converged; closeout requires a separate operator instruction.

If convergence appends bounded remediation tasks, run `speckit.analyze` on the updated artifacts. Resolve its findings before the operator separately invokes implementation for eligible tasks, then run convergence again. For a blocker or unrecognized result, stop and preserve the evidence. Convergence does not integrate Git or accept the feature.

## Manual closeout path

When native closeout dispatch is unavailable, first confirm that a separately approved feature-completion operation exists for the operator-selected converged feature. If it is missing, stop without inferring completion or substituting `speckit.specify`. If available, perform that approved operation, then run `speckit.flow-roadmap.debrief` and present its evidence and exact proposed verification patch.

Apply only a patch the operator explicitly approves with `speckit.flow-roadmap.write`; return to the relevant workflow or stop on deferral or an unrecognized decision. After an approved patch, ingest operator-selected durable sources with `speckit.flow-wiki.ingest`, then run `speckit.flow-wiki.lint`. Resolve lint findings before reviewing Git changes and commit readiness. A ready decision does not itself commit, integrate Git, or accept project work.
