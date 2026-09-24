# Research: Clarify Specification

## Decision: Preserve one-session routing

The reviewed `speckit-flow-clarify` package invokes `speckit.clarify` once, then asks the operator to continue clarification, begin planning, or defer. Each branch stops rather than launching another phase. The current command's five-question cap is a session boundary.

**Rationale**: The existing workflow is independently reviewable and keeps continuation human-directed.

**Alternative considered**: Add an automatic clarification loop or custom preset. Rejected because its continuation policy is unapproved and outside this feature.

## Decision: Bound validation claims

Inspect step ordering and gate choices in source, and exercise one route in a disposable consumer using a no-op Codex executable. Record that this cannot verify question quality or live-agent answer integration.

**Rationale**: Dispatch evidence and user acceptance have different authority.
