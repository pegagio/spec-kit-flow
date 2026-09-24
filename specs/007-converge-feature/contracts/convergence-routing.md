# Convergence Routing Contract

`feature_context` identifies the implemented feature. `integration` defaults to `codex`. `convergence_result` is supplied at the human evidence gate.

The workflow invokes `speckit.converge` against specification, plan, and tasks, then offers `clean`, `remediation`, and `blocked`. `clean` stops at Feature Converged with a separate closeout option. `remediation` invokes `speckit.analyze` for the new tasks and stops for separate implementation and later convergence. `blocked` and unrecognized choices stop without a converged claim.

No route integrates Git, accepts the feature, or selects another agent.
