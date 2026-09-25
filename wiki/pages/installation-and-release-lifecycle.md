---
title: Installation and release lifecycle
type: howto
sources: [S002, S005, S016]
updated: 2026-09-24
---

# Installation and release lifecycle

The repository's catalog tasks install or refresh the bundle from checked-in release packages. They serve a temporary localhost catalog, check released status, component versions and hashes, and call Specify in the target project; the install task can initialize an empty target project. The documented tested CLI is `1.0.10.dev0+pegagio.2`, while stock Spec Kit compatibility is unverified. (S002, S005)

Prepare the checkout with `mise trust` and `mise install`, then install with `mise run catalog:install <project-directory>` or dogfood locally with `mise run catalog:install .`. Inspect installed bundle, extension, and workflow identities and provenance before use. The repository does not distribute the pinned CLI. (S002, S005)

After a newer reviewed release, run `mise run catalog:refresh <project-directory>` from this checkout; a plain `specify bundle update` cannot reach the temporary catalog after the task exits. A failed refresh may have changed some components, and a new manifest may remove components formerly owned by the bundle. (S002, S005)

Local Codex-managed worktrees copy ignored installed state through `.worktreeinclude`; fresh clones, remote worktrees, and plain Git worktrees need their own installation. Edit reviewed source packages rather than installed `.specify/` copies. (S002, S005)

Maintainers build deterministic release packages from clean roadmap and wiki checkouts at matching annotated tags. Snapshot packages are for development and are rejected by install and refresh. Removing the bundle should leave unrelated components and the consumer feedback journal available. (S005)

The release builder checks source IDs, versions, clean feedback source, and clean annotated external tags before publishing local catalog metadata. Install and refresh verify catalog status, package checksums, workflow digests, bundle pins, and the tested CLI version before accepting the package set. (S016)

Disposable consumer validation covers install, native resolution and dispatch, feedback export and intake handoff, refresh, and removal. Local lifecycle success is bounded evidence; it does not establish remote publication, stock Spec Kit compatibility, live-agent quality, roadmap verification, Git integration, or acceptance. (S016)

## Related pages

- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
