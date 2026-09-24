# Implementation Routing Contract

`feature_context` identifies the analyzed feature with eligible tasks. `integration` defaults to `codex`. `implementation_result` is supplied at the human evidence gate.

The workflow invokes `speckit.implement` once, requesting prerequisite checks, bounded task execution, and evidence. The gate then offers `converge`, `return-to-analysis`, `return-to-specification`, `return-to-plan`, `return-to-tasks`, and `blocked`.

`converge` stops with a separate convergence handoff. Each return choice invokes only its named core command for the same feature. `blocked` and unrecognized choices stop. No route selects another agent, retries implementation automatically, integrates Git, or accepts the feature.
