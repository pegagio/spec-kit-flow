---
title: Workflow diagram conventions
type: howto
sources: [S021]
updated: 2026-09-30
---

# Workflow diagram conventions

The project-owned rendering skill derives a diagram from the operator-selected source workflow. A single Start marker points to its first declared step and every source step has exactly one node. Branches, joins, guarded corrections, loop conditions, and iteration bounds preserve definition semantics without invented steps or approvals. (S021)

Visible node content uses the exact ID, an assigned agent in parentheses when present, and a nonblank command. Shapes convey step types and delegated outlines convey child execution, so redundant id, agent, type, and delegated labels and absent-field placeholders are omitted. Descriptive declared transition labels make paths readable without changing outcome keys or recorded human choices. (S021)

Shared paths may simplify the picture only where completed evidence still controls downstream authorization. Exact human choices and verified prerequisites remain distinct even when branches join. The diagram is an inspection aid, not an alternate workflow authority or an invocation. (S021)

## Related pages

- [Codex workflow controller design](./codex-workflow-controllers.md)
