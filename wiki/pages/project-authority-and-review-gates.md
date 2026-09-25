---
title: Project authority and review gates
type: decision
sources: [S001, S002, S003]
updated: 2026-09-24
---

# Project authority and review gates

Spec Kit Flow owns generic workflow definitions, approved reusable presets, portable consumer feedback capture and reporting, and maintainer-only feedback intake. Reviewed source packages are the authority for changes; installed copies in a consumer project are not. (S001, S003)

The human chooses tasks and agents. Workflows do not select models, assign or launch agents, schedule work, or turn command success into roadmap verification, Git integration, feature acceptance, or Diagram acceptance. (S001, S002)

Roadmap patches, constitutional amendments, material scope or authority changes, ambiguous recovery, Git integration, and acceptance retain explicit human gates. Routine remediation may flow back through the smallest relevant spec, plan, or task artifact within the operator-issued controller scope. (S001, S002)

Local validation should record tested CLI versions, component IDs, source coordinates, digests, and observed results. Bundle installation or native dispatch with a no-op Codex executable does not establish live-agent behavior, stock Spec Kit compatibility, publication, or consumer adoption. (S001, S002)

## Related pages

- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Consumer feedback boundary](./consumer-feedback-boundary.md)
- [Diagram adapter boundary](./diagram-adapter-boundary.md)
