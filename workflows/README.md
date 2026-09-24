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
