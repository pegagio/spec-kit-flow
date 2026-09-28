---
title: Project authority and review gates
type: decision
sources: [S001, S002, S003, S017]
updated: 2026-09-28
---

# Project authority and review gates

Spec Kit Flow owns generic workflow definitions, approved reusable presets, portable consumer feedback capture and reporting, and maintainer-only feedback intake. Reviewed source packages are the authority for changes; installed copies in a consumer project are not. (S001, S003)

The constitution permits an explicitly invoked Codex controller to use reviewed step models and bounded subagents. The operator controls workflow invocation and task scope; completing one workflow does not launch a later phase or imply roadmap verification, Git integration, feature acceptance, or Diagram acceptance. (S017)

Under constitution 4.0.0, the operator selects the workflow and task scope. A reviewed workflow may declare concrete step models, which invocation authorizes for the run; the operator may override them. A Codex controller shows effective models, stops if an assignment is missing, invalid, or unavailable, and never silently chooses a fallback or starts a later workflow phase. (S017)

The controller keeps clarification questions and consequential gates in the main task and relays an answer to the same step subagent when continuation is needed. (S017)

Roadmap patches, constitutional amendments, material scope or authority changes, ambiguous recovery, Git integration, and acceptance retain explicit human gates. Routine remediation may flow back through the smallest relevant spec, plan, or task artifact within the operator-issued controller scope. (S001, S002)

Local validation should record tested CLI versions, component IDs, source coordinates, digests, and observed results. Bundle installation or native dispatch with a no-op Codex executable does not establish live-agent behavior, stock Spec Kit compatibility, publication, or consumer adoption. (S001, S002)

## Related pages

- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Consumer feedback boundary](./consumer-feedback-boundary.md)
- [Diagram adapter boundary](./diagram-adapter-boundary.md)
