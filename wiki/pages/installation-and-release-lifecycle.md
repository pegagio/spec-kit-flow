---
title: Installation and release lifecycle
type: howto
sources: [S002, S005, S016]
updated: 2026-09-29
---

# Installation and release lifecycle

The repository's catalog tasks install or refresh the bundle and eight direct FlowKit Codex skills from checked-in release packages. They serve a temporary localhost catalog, check released status, component versions and hashes, and call Specify in the target project; the install task can initialize an empty target project. The documented tested CLI is `1.0.10.dev0+pegagio.2`, while stock Spec Kit compatibility is unverified. (S005)

Prepare a checkout that matches the checked-in release with `mise trust` and `mise install`, then install with `mise run catalog:install <project-directory>` or dogfood locally with `mise run catalog:install .`. The current unreleased source checkout rejects those ordinary commands because its source differs from the catalog; validate it only through a disposable initialized consumer with development-snapshot mode. Inspect installed bundle, extension, and workflow identities and provenance before use. The repository does not distribute the pinned CLI. (S002, S005)

After a newer reviewed release, run `mise run catalog:refresh <project-directory>` from this checkout; a plain `specify bundle update` cannot reach the temporary catalog after the task exits or manage the direct skills. A failed refresh may have changed some components, and a new manifest may remove components formerly owned by the bundle. (S005)

Local Codex-managed worktrees copy ignored installed state through `.worktreeinclude`; fresh clones, remote worktrees, and plain Git worktrees need their own installation. Edit reviewed source packages rather than installed `.specify/` copies. (S002, S005)

Maintainers build deterministic release packages from clean roadmap and wiki checkouts at matching annotated tags. The checked-in `0.4.1` catalog is a local release and has not been published or pushed; current source bundle `0.5.0` and controller `0.2.0` are unreleased. Ordinary install and refresh require a checkout matching that release, while development snapshots are limited to initialized disposable consumers. Complete removal through the FlowKit catalog route checks skill ownership and preserves locally edited or unrelated skills, recovery summaries, independently installed components, and feedback evidence. Native `specify bundle remove` alone does not remove the direct skills. (S002, S005)

The release builder checks source IDs, versions, clean feedback source, and clean annotated external tags before publishing local catalog metadata. Install and refresh verify catalog status, package checksums, workflow digests, bundle pins, and the tested CLI version before accepting the package set. (S016)

Disposable consumer validation covers install, native resolution and dispatch, feedback export and intake handoff, refresh, and removal. Local lifecycle success is bounded evidence; it does not establish remote publication, stock Spec Kit compatibility, roadmap verification, Git integration, or acceptance. (S016, S005)

In the direct Codex skill path, delegated steps use exact native agent names from consumer-owned `.codex/agents/` files. The controller probes selected agents before work, while Codex owns optional model and effort settings. See [named agents for delegated steps](./agent-roles-and-inheritance.md). (S005)

## Related pages

- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Codex workflow controller design](./codex-workflow-controllers.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
- [Named agents for delegated steps](./agent-roles-and-inheritance.md)
