# Install and Use Spec Kit Flow

Use the catalog tasks in this repository to install or refresh the bundle. They serve the checked-in release packages on localhost for the duration of each command, so you do not need separate roadmap or wiki source checkouts to install it. The [bundle manifest](../bundles/spec-kit-flow/bundle.yml) and [release metadata](../catalog/release.json) are the sources for current component versions.

## Contents

- [Prepare the checkout](#prepare-the-checkout)
- [Install in another project](#install-in-another-project)
- [Dogfood this repository](#dogfood-this-repository)
- [Use a workflow](#use-a-workflow)
- [Refresh or remove the bundle](#refresh-or-remove-the-bundle)
- [Build release packages](#build-release-packages)

## Prepare the checkout

Run these commands from the Spec Kit Flow checkout. You need `mise`, Python 3, and access to the Specify CLI pinned in `mise.toml`. The repository does not distribute that CLI.

```sh
cd /path/to/spec-kit-flow
mise trust
mise install
mise exec -- specify --version
```

If `mise install` cannot obtain the pinned Specify fork, make that CLI available before continuing. The catalog tasks check its exact version and reject development snapshots or mismatched package hashes.

## Install in another project

Choose an existing project directory outside this checkout, or create an empty one. The install task initializes it with Specify if needed.

```sh
mkdir -p /path/to/my-project
mise run catalog:install /path/to/my-project
```

Verify the installation from the project directory:

```sh
cd /path/to/my-project
specify bundle list
specify extension list
specify workflow list
```

The install task starts and stops its own localhost catalog. Do not add Specify's `--offline` flag; the resolver needs to contact that local catalog.

## Dogfood this repository

Install into the checkout itself when developing Spec Kit Flow. Run this from its root:

```sh
mise run catalog:install .
specify bundle list
specify workflow list
```

Edit reviewed workflow and extension source packages, not the installed copies under `.specify/`. This repository ignores the bundle's local installation records, copied default configuration, and installed payloads.

After installing in this checkout, new local Codex-managed worktrees copy its ignored installation records, extension and workflow payloads, and generated agent files through `.worktreeinclude`. No worktree setup script is needed. Run `mise install` in a worktree if the pinned tools are not already available there.

The copy reflects the source checkout's installed bundle. After changing reviewed release packages, run `mise run catalog:refresh .` in that checkout before creating a worktree. A fresh clone, remote worktree, or plain `git worktree add` does not receive this ignored state; run `mise run catalog:install .` there after preparing the checkout. The workflow registry can contain a temporary localhost catalog URL; use the catalog refresh task to update the bundle.

## Use a workflow

Inspect the workflow before running it in the installed project. For example, start-feature requires an eligible roadmap candidate and governing wiki context:

```sh
specify workflow info speckit-flow-start-feature
specify workflow run speckit-flow-start-feature --input "feature_request=Describe the selected eligible feature"
```

The workflow stops at human review gates. Invoke each later workflow separately. The [workflow guide](../workflows/README.md) gives the route and manual fallback. While editing a workflow in this repository, you can run its source `workflow.yml` by path to test an uninstalled change.

## Refresh or remove the bundle

After updating this checkout to a newer reviewed release, return to its root and refresh the target project:

```sh
cd /path/to/spec-kit-flow
mise run catalog:refresh /path/to/my-project
```

For an in-repository installation, use `mise run catalog:refresh .` instead. Use the catalog task because a plain `specify bundle update` cannot reach the temporary catalog after the install task exits. Inspect the result if refresh fails; it may have changed some components before stopping. Refresh can remove components previously owned by the bundle when the new manifest omits them.

To remove the bundle, run this in the installed project:

```sh
specify bundle remove spec-kit-flow
specify bundle list
```

Confirm that unrelated components remain. The consumer's feedback journal is local evidence and should remain available after removal.

## Build release packages

Maintainers need clean checkouts of the independent roadmap and wiki repositories at annotated release tags matching the [bundle manifest](../bundles/spec-kit-flow/bundle.yml). From this repository's root, run:

```sh
mise run catalog:build /path/to/spec-kit-flow-roadmap /path/to/spec-kit-flow-wiki
```

The builder checks source IDs, versions, tags, and cleanliness, then writes deterministic extension archives and source digests to `catalog/`. Review the resulting package contents and diff before committing a release. `--snapshot` is for development packaging; install and refresh reject snapshots. Do not edit archives directly.
