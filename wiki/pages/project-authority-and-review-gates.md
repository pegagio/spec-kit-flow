---
title: Project authority and review gates
type: decision
sources: [S001, S002, S003, S017, S019, S020]
updated: 2026-09-29
---

# Project authority and review gates

Spec Kit Flow owns generic workflow definitions, approved reusable presets, portable consumer feedback capture and reporting, and maintainer-only feedback intake. Reviewed source packages are the authority for changes; installed copies in a consumer project are not. (S001, S003)

The operator controls workflow invocation and task scope. Every explicitly delegated step names a reviewed Codex agent, and the controller may launch bounded children using those names. Completing one workflow does not launch a later phase or imply roadmap verification, Git integration, feature acceptance, or Diagram acceptance. (S001)

Feature 013's earlier concrete-model arrangement allowed a named-step override. Feature 015's current assignment rule supersedes that approach: invocation authorizes the workflow's reviewed agent names without a per-run agent, model, or effort override, and a missing or unavailable assignment stops without fallback. (S001, S019, S020)

Feature 015's reviewed-agent constitution amendment was approved before workflow or controller source changes. Every delegated step names its own agent, and invocation provides no per-run agent, model, or effort override. (S020)

The controller keeps clarification questions and consequential gates in the main task and relays an answer to the same step subagent when continuation is needed. (S017)

Roadmap patches, constitutional amendments, material scope or authority changes, ambiguous recovery, Git integration, and acceptance retain explicit human gates. Routine remediation may flow back through the smallest relevant spec, plan, or task artifact within the operator-issued controller scope. (S001, S002)

Local validation should record tested CLI versions, component IDs, source coordinates, digests, and observed results. Bundle installation or native dispatch with a no-op Codex executable does not establish live-agent behavior, stock Spec Kit compatibility, publication, or consumer adoption. (S001, S002)

## Related pages

- [Agent roles and assignment inheritance](./agent-roles-and-inheritance.md)
- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Consumer feedback boundary](./consumer-feedback-boundary.md)
- [Diagram adapter boundary](./diagram-adapter-boundary.md)
