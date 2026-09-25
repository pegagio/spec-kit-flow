---
title: Bundle and workflow model
type: concept
sources: [S001, S002, S016]
updated: 2026-09-24
---

# Bundle and workflow model

The `spec-kit-flow` repository and bundle own generic workflow and feedback source. A bundle composes versioned components; each workflow remains an independently reviewable source package, and extensions retain their reviewed manifest IDs. (S001, S002)

The documented bundle is version `0.3.1`, targets Codex, and requires Specify `>=1.0.10.dev0` and Python 3. It pins `flow-roadmap` `0.2.1`, `flow-wiki` `2.0.1`, and the consumer `flow-feedback` extension `0.2.1`; roadmap and wiki are maintained in separate repositories. (S002)

The bundle includes eight workflows: `speckit-flow-start-feature`, `speckit-flow-clarify`, `speckit-flow-plan`, `speckit-flow-tasks`, `speckit-flow-analyze-remediate`, `speckit-flow-implement`, `speckit-flow-converge`, and `speckit-flow-closeout`. It does not include a preset or the maintainer feedback intake component. (S001, S002)

Generic source has no Diagram executable, database, registration command, canonical-state mutation, or runtime service dependency. (S001)

The bundle manifest pins compatible component versions; the local release catalog binds packages to source commits, required release tags, archive SHA-256 digests, workflow source digests, and release status. Codex is the initial integration. (S016)

## Related pages

- [Project authority and review gates](./project-authority-and-review-gates.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Installation and release lifecycle](./installation-and-release-lifecycle.md)
- [Diagram adapter boundary](./diagram-adapter-boundary.md)
