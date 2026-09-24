# Research: Analyze and Remediate Artifacts

## Decision: Preserve read-only assessment before routing

The workflow starts with `speckit.analyze` and a human disposition gate. Clean analysis stops. Routine findings select one spec, plan, or task flow-back chain and then reanalyze. Constitutional, authority-or-scope, blocked, and invalid outcomes stop.

**Rationale**: A successful command does not by itself reconcile artifacts or authorize implementation.

**Alternative considered**: Automatically remediate every finding. Rejected because consequential decisions exceed the bounded controller scope.

## Decision: Verify route structure and one terminal dispatch

Inspect all routine and stop paths in reviewed source. Use a disposable no-op clean route to confirm native dispatch. Do not claim that this proves classification quality or actual artifact consistency.

**Rationale**: Live-agent judgment and resulting artifact quality need separate consumer review.
