# Install and Use Spec Kit Flow

Use the catalog tasks in this repository to install or refresh the bundle. They serve the checked-in release packages on localhost for the duration of each command, so you do not need separate roadmap or wiki source checkouts to install it. The [bundle manifest](../bundles/spec-kit-flow/bundle.yml) and [release metadata](../catalog/release.json) are the sources for current component versions.

The checked-in catalog contains the locally built `0.4.1` release and controller package `0.1.1`. Ordinary catalog install and refresh use these reviewed packages. Development-snapshot mode is reserved for uncommitted source changes in a disposable initialized consumer; the catalog has not been published or pushed.

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

For Codex skill integration, initialize a new disposable consumer with the skills integration enabled. Existing projects need a Codex installation that discovers project skills under `.agents/skills/`:

```sh
specify init --here --force --non-interactive --integration codex --integration-options="--skills"
```

The supported catalog install also installs eight direct FlowKit skills, shared controller files, and `.specify/flow-kit/skills-install.json`. Native `specify bundle install` manages the workflows and extensions, not those direct skills. Use the FlowKit catalog task so both parts are installed and verified together.

To test unreleased controller/workflow changes, initialize an already-created disposable consumer under the system temporary directory, then use the explicit snapshot route:

```sh
consumer_dir="$(mktemp -d)"
specify_bin="$(mise which specify)"
(
  cd "$consumer_dir"
  "$specify_bin" init --here --force --non-interactive --integration codex --integration-options="--skills"
)
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py install "$consumer_dir" --development-snapshot
```

Snapshot mode builds a temporary catalog from current source and the checked-in extension packages. It is restricted to initialized temporary consumers, reports itself as unreleased in the ownership record, and does not change checked-in release metadata. The normal install and refresh routes continue to reject snapshots.

## Dogfood this repository

Use this checkout as a consumer when developing Spec Kit Flow. From the repository root, install the checked-in release if no `spec-kit-flow` bundle is present:

```sh
mise run catalog:install .
```

If `specify bundle list` already shows `spec-kit-flow`, refresh the existing installation instead:

```sh
mise run catalog:refresh .
```

Both catalog commands install or refresh the eight Specify workflows **and** the eight direct FlowKit Codex skills in `.agents/skills/flow-kit-*/`. They also write the separate skill ownership record under `.specify/flow-kit/`. Verify both parts from this checkout:

```sh
mise exec -- specify bundle list
mise exec -- specify workflow list
ls .agents/skills/flow-kit-*/SKILL.md
test -f .specify/flow-kit/skills-install.json
```

The skill picker should then show FlowKit Start Feature, FlowKit Clarify, FlowKit Plan, FlowKit Tasks, FlowKit Analyze, FlowKit Implement, FlowKit Converge, and FlowKit Close Out in a Codex task for this project. If a task was already open before installation, open a fresh task to check discovery. Edit reviewed source under `controllers/`, `workflows/`, and the extension source packages, not the installed copies under `.agents/skills/` or `.specify/`. This repository ignores local installation records and installed payloads.

After installing in this checkout, new local Codex-managed worktrees copy its ignored installation records, FlowKit skill ownership record, extension and workflow payloads, and generated agent files through `.worktreeinclude`. No worktree setup script is needed. Run `mise install` in a worktree if the pinned tools are not already available there.

The copy reflects the source checkout's installed bundle. After changing reviewed release packages, run `mise run catalog:refresh .` in that checkout before creating a worktree. A fresh clone, remote worktree, or plain `git worktree add` does not receive this ignored state; run `mise run catalog:install .` there after preparing the checkout. The workflow registry can contain a temporary localhost catalog URL; use the catalog refresh task to update the bundle.

## Use a workflow

Inspect the workflow before running it in the installed project. For example, start-feature requires an eligible roadmap candidate and governing wiki context:

```sh
specify workflow info speckit-flow-start-feature
specify workflow run speckit-flow-start-feature --input "feature_request=Describe the selected eligible feature"
```

The workflow stops at human review gates. Invoke each later workflow separately. The [workflow guide](../workflows/README.md) gives the route and manual fallback. While editing a workflow in this repository, you can run its source `workflow.yml` by path to test an uninstalled change.

In the Codex app, invoke the corresponding FlowKit skill in a task whose selected project is the consumer. The visible names, skill IDs, and required inputs are:

| Display name | Skill invocation | Required input |
| --- | --- | --- |
| FlowKit Start Feature | `$flow-kit-start-feature` | `feature_request` |
| FlowKit Clarify | `$flow-kit-clarify` | `feature_context` |
| FlowKit Plan | `$flow-kit-plan` | `feature_context` |
| FlowKit Tasks | `$flow-kit-tasks` | `feature_context` |
| FlowKit Analyze | `$flow-kit-analyze-remediate` | `feature_context` |
| FlowKit Implement | `$flow-kit-implement` | `feature_context` |
| FlowKit Converge | `$flow-kit-converge` | `feature_context` |
| FlowKit Close Out | `$flow-kit-closeout` | `feature_context` |

For example, enter `$flow-kit-tasks feature_context=013` in the selected project's Codex task. Optional workflow inputs have defaults and can be supplied in the same `key=value` form. The controller locates the selected compatible Specify executable (preferring the project's mise selection), reads the installed composed workflow without executing native workflow dispatch, and stops before workflow work if runtime, workflow, input, or skill provenance checks fail.

Before the first step, the controller shows every concrete model and effective reasoning effort, including assignments in branches that will not be taken. Omitted effort is Medium. Task generation and implementation use GPT-6 Luna with High effort; the other declared assignments use GPT-6 Sol or GPT-6 Astra with Medium effort as listed in the workflow YAML. Each distinct pair must pass an availability probe in the selected Codex task. A named-step override uses `step_id`, with optional `model` and `reasoning_effort`; it changes only that step. Modeled steps use bounded children, while unmodeled steps and gates stay in the main task. The main task presents child questions as numbered options plus a custom answer when allowed and relays the response to the same child. Native `specify workflow run` ignores FlowKit reasoning-effort metadata and does not provide this controller interaction model.

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

For a supported complete removal of the bundle and its direct FlowKit skills, run the catalog command from the source checkout:

```sh
mise run catalog:remove /path/to/my-project
```

It checks the recorded skill inventory and file digests before calling native bundle removal, then removes only unchanged FlowKit-owned skills and the ownership record. A collision or locally edited owned file stops removal for review. Recovery summaries under `.specify/flow-controllers/runs/`, unrelated skills, feedback, and independently installed components are preserved. The native `specify bundle remove` command alone removes the bundle contents but does not manage direct Codex skills.

## Build release packages

Maintainers need clean checkouts of the independent roadmap and wiki repositories at annotated release tags matching the [bundle manifest](../bundles/spec-kit-flow/bundle.yml). From this repository's root, run:

```sh
mise run catalog:build /path/to/spec-kit-flow-roadmap /path/to/spec-kit-flow-wiki
```

The builder checks source IDs, versions, tags, and cleanliness, then writes deterministic extension archives and source digests to `catalog/`. Review the resulting package contents and diff before committing a release. `--snapshot` is for development packaging; install and refresh reject snapshots. Do not edit archives directly.
