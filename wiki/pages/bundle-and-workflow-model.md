---
title: Bundle and workflow model
type: concept
sources: [S001, S002, S016, S017, S018, S019]
updated: 2026-09-28
---

# Bundle and workflow model

The `spec-kit-flow` repository and bundle own generic workflow and feedback source. A bundle composes versioned components; each workflow remains an independently reviewable source package, and extensions retain their reviewed manifest IDs. (S001, S002)

The documented bundle is version `0.4.1`, targets Codex, and requires Specify `>=1.0.10.dev0` and Python 3. It pins `flow-roadmap` `0.2.1`, `flow-wiki` `2.0.1`, and the consumer `flow-feedback` extension `0.2.1`; roadmap and wiki are maintained in separate repositories. (S002)

The bundle includes eight workflows: `speckit-flow-start-feature`, `speckit-flow-clarify`, `speckit-flow-plan`, `speckit-flow-tasks`, `speckit-flow-analyze-remediate`, `speckit-flow-implement`, `speckit-flow-converge`, and `speckit-flow-closeout`. It does not include a preset or the maintainer feedback intake component. (S001, S002)

The local FlowKit catalog release adds eight direct Codex controller skills alongside the Specify bundle. Native bundle commands manage the declared workflows and extensions, while FlowKit catalog install, refresh, and removal manage the direct skills as a separate owned package. (S002)

Generic source has no Diagram executable, database, registration command, canonical-state mutation, or runtime service dependency. (S001)

The bundle manifest pins compatible component versions; the local release catalog binds packages to source commits, required release tags, archive SHA-256 digests, workflow source digests, and release status. Codex is the initial integration. (S016)

The amended constitution permits Codex controllers to dispatch bounded step subagents, but requires them to follow the installed, versioned workflow definition instead of copying its prompts, gates, or decision rules into a skill. Every workflow keeps a manual-prompt path when native dispatch is unavailable. (S017)

Verified Feature 013 defines direct `flow-kit-*` Codex controller skills installed through the FlowKit catalog route alongside the Specify bundle. Its roadmap records bounded consumer validation of concrete step models and desktop interaction, without claiming publication or broader compatibility. (S018)

The completed Feature 013 specification requires the FlowKit catalog route to manage the direct skills; native Specify bundle commands manage only their declared Specify components. (S019)

## Related pages

- [Codex workflow controller design](./codex-workflow-controllers.md)
- [Project authority and review gates](./project-authority-and-review-gates.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Installation and release lifecycle](./installation-and-release-lifecycle.md)
- [Diagram adapter boundary](./diagram-adapter-boundary.md)
