# Task Generation Workflow Contract

`feature_context` is required and identifies the planned feature. `integration` defaults to `codex`. `task_review_decision` is supplied at the human review gate.

The workflow first invokes `speckit.tasks` with instructions to produce dependency-ordered work from reviewed design artifacts and surface surprising human actions. It then offers `analyze`, `return-to-plan`, `amend-tasks`, and `defer`.

`analyze` stops with a separate `speckit-flow-analyze-remediate` handoff. `return-to-plan` invokes `speckit.plan` for the same feature's design gap. Amendment, deferral, and invalid choices stop without beginning implementation. No route selects an agent, integrates Git, or accepts the feature.
