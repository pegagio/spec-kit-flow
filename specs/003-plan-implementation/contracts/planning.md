# Planning Workflow Contract

`feature_context` is required and identifies the clarified feature. `integration` defaults to `codex`. The human supplies `plan_review_decision` at the readiness gate.

The gate offers `plan`, `return-to-clarification`, and `defer`. The `plan` route invokes `speckit.plan` and then stops for operator review of plan, research, data model, contracts, and quickstart. The return route invokes `speckit.clarify` for the same feature. Deferral and invalid decisions stop without invoking planning.

The workflow never invokes task generation or implementation. Completion of the planning command does not imply feature acceptance, Git integration, or agent selection.
