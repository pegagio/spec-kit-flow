# Research: Converge Feature

## Decision: Reuse current clean-route dispatch evidence

The lifecycle suite already installs `speckit-flow-converge` and runs a no-op `clean` route. The reviewed source also defines remediation and blocked routes. Add route inspection and manual guidance rather than another test that repeats the same dispatch.

**Rationale**: Existing integration coverage is sufficient for native clean routing; a duplicated test would add little confidence.

**Alternative considered**: Add another no-op clean-route case. Rejected because it would mirror existing coverage.

## Decision: Keep remediation under normal gates

The remediation branch invokes `speckit.analyze` on newly created tasks and stops for a separate implementation run. A later convergence run reassesses the result. The workflow does not equate task completion with acceptance.

**Rationale**: Newly found work must pass artifact consistency checks and human direction.
