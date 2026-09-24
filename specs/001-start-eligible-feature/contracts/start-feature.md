# Start-Feature Workflow Contract

## Inputs

`feature_request` is required and names one candidate roadmap feature. `integration` defaults to `codex`. The operator supplies `roadmap_decision` and `final_review_decision` at the respective human gates.

## Ordered route

1. Assess one uniquely eligible candidate and prepare an exact proposed patch without mutation.
2. Ask the operator to approve, amend the roadmap, resolve context, or defer.
3. On approval only, apply the exact patch, retrieve cited context and coverage, draft the specification, and run a roadmap brief.
4. Ask the operator to choose clarification, roadmap amendment, context resolution, planning readiness, or deferral. This choice ends the workflow.

## Stop behavior

Ambiguity, unsatisfied dependencies, or incomplete governing context stop before patch approval. Non-approval decisions route to their named stop actions. An unrecognized decision stops with the manual prompt path. The workflow does not select an agent, launch a follow-on phase, integrate Git, or confer acceptance.

## Component commands

The approved route uses `speckit.flow-roadmap.write`, `speckit.flow-wiki.query`, `speckit.specify`, and `speckit.flow-roadmap.brief`. These commands are provided by compatible independently versioned components and core Spec Kit; this workflow does not own their implementation.
