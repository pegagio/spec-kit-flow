# Research: Generate Implementation Tasks

## Decision: Treat generation as a proposal

The reviewed workflow invokes `speckit.tasks`, then presents a human review gate. `analyze` stops with a separate analysis handoff; `return-to-plan` invokes planning; amendment and deferral stop. None invokes implementation.

**Rationale**: Generated tasks can reveal design gaps or unexpected operator work, so a successful generation command is not implementation authorization.

**Alternative considered**: Automatically run analysis and implementation after generation. Rejected because it would bypass review and separate workflow states.

## Decision: Bound dispatch evidence

Use source inspection and a disposable no-op route to verify native routing. Record that a no-op agent cannot judge task coverage or whether human actions were appropriately surfaced.

**Rationale**: Product and authority decisions remain with the operator.
