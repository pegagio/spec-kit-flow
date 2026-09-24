# Clarification Workflow Contract

`feature_context` is required and identifies the active feature. `integration` defaults to `codex`. `clarification_decision` is supplied at the human review gate.

The workflow invokes `speckit.clarify` for one session. It then presents resolved, outstanding, and deferred ambiguity and offers exactly three choices: `continue-clarification`, `begin-planning`, and `defer`. Each route terminates this invocation. An unrecognized choice terminates with a manual prompt fallback.

The command's current five-question cap does not imply readiness. A continuation requires another operator invocation on the same active feature. Planning requires a separate operator invocation. A deferral stays explicit and does not become an automatic product default.
