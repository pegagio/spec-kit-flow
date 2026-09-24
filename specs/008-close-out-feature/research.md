# Research: Close Out Feature

## Decision: Preserve the completion-operation stop

The source checks whether a separately approved completion operation exists. The missing route stops before debrief. No operation is defined here, so a workflow prompt must not pretend to complete the feature.

**Rationale**: A closeout wrapper cannot create lifecycle authority by itself.

## Decision: Add a bounded native route test

The lifecycle suite resolves closeout but does not run it. Add a no-op `operation-missing` route to verify dispatch and stop behavior. Inspect the approved branch in source; the test cannot prove the quality of a future completion operation, debrief, or wiki ingestion.

**Alternative considered**: Execute all branches with a no-op agent. Rejected because mirrored dispatch would imply more coverage than it provides.
