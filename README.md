# Spec Kit Flow

Spec Kit Flow is a human-directed, merge-bounded flow-back workbench for Spec-Driven Development. It packages eight reusable Spec Kit workflows, portable consumer feedback, and a version-pinned bundle that composes independently maintained roadmap and wiki extensions.

This repository owns the generic workflow and feedback source. The repository and bundle ID are `spec-kit-flow`; its workflows use `speckit-flow-<purpose>` IDs, and the consumer feedback extension uses `flow-feedback`. The independent `spec-kit-flow-roadmap` and `spec-kit-flow-wiki` repositories publish the extension IDs `flow-roadmap` and `flow-wiki`.

## Contents

- [What the bundle installs](#what-the-bundle-installs)
- [Installation](#installation)
- [Using the workflows](#using-the-workflows)
- [Feedback and project status](#feedback-and-project-status)

## What the bundle installs

The [bundle manifest](bundles/spec-kit-flow/bundle.yml) is version `0.3.1` and targets Codex. It requires Specify `>=1.0.10.dev0` and Python 3. The bundle pins these extensions:

| Extension ID | Version | Purpose |
| --- | --- | --- |
| `flow-roadmap` | `0.2.1` | Governed roadmap changes and feature reviews; source: `spec-kit-flow-roadmap` |
| `flow-wiki` | `2.0.1` | Cited project context, ingestion, and linting; source: `spec-kit-flow-wiki` |
| `flow-feedback` | `0.2.1` | Local observation capture and portable report export; source: this repository |

It also installs the eight workflows in [`workflows/`](workflows/README.md):

| Workflow ID | Version | Role |
| --- | --- | --- |
| `speckit-flow-start-feature` | `0.2.0` | Assess an eligible roadmap feature, obtain approval for its exact patch, query context, specify, and brief |
| `speckit-flow-clarify` | `0.1.0` | Run one bounded clarification session |
| `speckit-flow-plan` | `0.1.0` | Review readiness and create the technical plan |
| `speckit-flow-tasks` | `0.1.0` | Generate implementation tasks separately from planning |
| `speckit-flow-analyze-remediate` | `0.1.0` | Analyze artifact consistency and route bounded remediation |
| `speckit-flow-implement` | `0.1.0` | Implement eligible tasks within the selected agent's scope |
| `speckit-flow-converge` | `0.1.0` | Compare implementation with the feature artifacts and close gaps |
| `speckit-flow-closeout` | `0.2.0` | Review completion, roadmap verification, wiki maintenance, and commit readiness through explicit gates |

The bundle does not include a preset or `speckit-flow-feedback-maintainer`. Maintainer intake belongs in this source environment, not a consumer project.

## Installation

This repository contains a local released catalog package set for Roadmap `v0.2.1` and Wiki `v2.0.1`. A compatible Specify CLI must already be available; `mise.toml` records the tested fork version but this checkout does not distribute the CLI. From the Spec Kit Flow checkout, point the mise task at an existing consumer project directory:

```sh
git clone https://github.com/pegagio/spec-kit-flow.git
cd spec-kit-flow
mise trust
mkdir -p /path/to/my-project
mise run catalog:install /path/to/my-project
```

The task first requires a catalog marked `released`. It then checks the packaged component versions and checksums, serves the checked-in packages and workflow source on localhost for the duration of the install, and calls `specify bundle install` in the consumer directory. Specify initializes a new project when needed. The tested CLI is `1.0.10.dev0+pegagio.2`; compatibility with stock Spec Kit remains unverified. `mise install` can activate the pinned CLI only when that fork is obtainable in your environment. Inspect installed component IDs and provenance before use.

To dogfood the workflows while developing this repository, run `mise run catalog:install .` from its root. New local Codex-managed worktrees copy the ignored installed state through `.worktreeinclude`. Edit the reviewed source packages; local installation state is ignored. Use `mise run catalog:refresh .` after a newer reviewed release. See the [installation guide](docs/installation.md) for worktree and fresh-clone steps.

After pulling a newer reviewed release of this repository, refresh the bundle with:

```sh
mise run catalog:refresh /path/to/my-project
```

The same task must provide the temporary catalogs during refresh, and it also rejects snapshots. Maintainers build release packages from clean checkouts at matching annotated tags with `mise run catalog:build <roadmap-checkout> <wiki-checkout>`. The `--snapshot` build option is for development packages only; those packages cannot be installed through the consumer tasks. Review `catalog/release.json` and the packages before committing them. See [installation and lifecycle details](docs/installation.md) for provenance, removal, and release requirements.

## Using the workflows

Prepare a project constitution, use `speckit.flow-roadmap.write` for an approved roadmap, then use `speckit.flow-wiki.init` and `speckit.flow-wiki.ingest` to establish cited project context. The operator chooses an eligible feature and invokes each workflow deliberately. A typical route is:

```text
start-feature → clarify (as needed) → plan → tasks → analyze-remediate
              → implement → converge → closeout
```

Inspect an installed workflow and supply its required context when running it. For example, after reviewing the roadmap and its eligibility:

```sh
specify workflow info speckit-flow-start-feature
specify workflow run speckit-flow-start-feature --input "feature_request=Describe the chosen roadmap feature"
```

The workflows preserve a manual-prompt fallback. Clarification may need another session after the current command's five-question cap. Analyze after task generation or consequential artifact reconciliation before implementation; converge after implementation until gaps are resolved. Planning and task generation remain separate. The closeout workflow requires a separately approved feature-completion operation and does not create one.

Human review controls roadmap patches, material scope and authority changes, ambiguous recovery, Git integration, and acceptance. A completed workflow does not select or launch another agent or imply that a feature was merged or accepted. See the [workflow command map](workflows/README.md) and [project constitution](.specify/memory/constitution.md) for the governing contracts.

## Feedback and project status

Consumers may use `flow-feedback` to capture local observations and export a portable report. Its commands are `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`. Capture and export do not change workflow source or project authority; maintainer intake is a separate step. See [feedback guidance](docs/feedback.md).

The [project status](docs/project-status.md) records tested versions, source coordinates, validation evidence, and remaining publication limits. The disposable lifecycle test proves bundle installation and native dispatch with a no-op Codex executable; it does not prove live-agent behavior or general consumer compatibility.
