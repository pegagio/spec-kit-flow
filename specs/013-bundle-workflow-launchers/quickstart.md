# Quickstart: Validate Codex Workflow Controllers

This is the maintainer run guide for the implemented Feature 013 release. Run it against the reviewed bundle and Specify CLI versions recorded in the release metadata. Use disposable initialized consumers; do not treat a stub CLI dispatch as proof of desktop child-task behavior.

## Prerequisites

From the Spec Kit Flow source checkout, verify `mise trust`, `mise install`, `specify --version`, and `codex --version`. The tested Specify coordinate for this plan is `1.0.10.dev0+pegagio.2`; record the actual versions used. Ensure the reviewed release catalog or explicitly marked development snapshot includes the direct Codex skill package and updated workflow digests. Use the configured skill-tools Python for maintainer tests; if it is absent or lacks a dependency, report that issue before changing the environment. The disposable consumer must work without the maintainer's skill-tools environment by using its selected compatible Specify runtime.

## Install and inspect a disposable consumer

For pre-release validation, first build a development snapshot from reviewed roadmap and wiki source checkouts with `python3 tools/catalog.py build <roadmap-checkout> <wiki-checkout> --snapshot`. The snapshot must record exact digests and dirty status for uncommitted controller or workflow source. The install below uses the planned `--development-snapshot` mode; it must accept only disposable initialized consumers and visibly identify the result as unreleased. For a released catalog, use `mise run catalog:install "$consumer_dir"` instead.

```sh
consumer_dir="$(mktemp -d)"
(
  cd "$consumer_dir"
  specify init --here --force --non-interactive --integration codex --integration-options="--skills"
)
python3 tools/catalog.py install "$consumer_dir" --development-snapshot
find "$consumer_dir/.agents/skills" -maxdepth 1 -type d -name 'flow-kit-*' -print
```

Expect eight distinct controller skill directories and a verified `.specify/flow-kit/skills-install.json` record before invoking a skill. Check that each direct skill's `SKILL.md` name and `agents/openai.yaml` display name match [controller.md](contracts/controller.md), and confirm those labels appear in the desktop skill picker. Inspect the FlowKit skill ownership record and installed Specify bundle record, then use `specify workflow resolve speckit-flow-clarify` from the consumer to confirm workflow attribution. Check each skill maps to its corresponding installed workflow, and compare package and workflow versions and digests with `catalog/release.json`. A missing workflow or a pre-existing same-name local skill must produce a clear blocker, not a substitute or silent skip.

From the selected Codex task, verify the controller bootstrap locates the compatible `specify` executable and reads the composed workflow without native dispatch. Repeat with a normal installed executable and with a mise-selected executable. A missing or mismatched runtime must stop before any workflow step or recovery record.

## Exercise the P1 desktop dispatch

Prepare a planned feature in the disposable consumer from the reviewed Feature 013 artifacts, then select that consumer as the Codex project task:

```sh
mkdir -p "$consumer_dir/specs/999-controller-probe"
cp specs/013-bundle-workflow-launchers/spec.md specs/013-bundle-workflow-launchers/plan.md specs/013-bundle-workflow-launchers/research.md specs/013-bundle-workflow-launchers/data-model.md "$consumer_dir/specs/999-controller-probe/"
cp -R specs/013-bundle-workflow-launchers/contracts "$consumer_dir/specs/999-controller-probe/"
printf '{"feature_directory":"specs/999-controller-probe"}\n' > "$consumer_dir/.specify/feature.json"
```

Invoke `$flow-kit-tasks feature_context=999-controller-probe` in that desktop task. Confirm the main task shows the installed workflow's effective model-effort pairs, resolves `speckit.tasks` to the selected project's installed `$speckit-tasks`, dispatches `generate-tasks` in a `gpt-6-luna`/high child with YAML-rendered arguments, keeps the review gate in the main task, and reports the result and workspace diff without starting analysis. Repeat with a named-step model and/or effort override and verify only that step changes. Reject a missing input or an unavailable model-effort pair in an untaken branch before any workflow step or run record is created. Remove the disposable consumer's `speckit-tasks` skill and verify the controller stops at that node without invoking a global substitute. Record observed child identity, effective model and effort, selected skill source, project, and result; the ephemeral catalog test alone cannot establish these facts.

## Exercise same-child clarification

Invoke `$flow-kit-clarify` with `feature_context=999-controller-probe`. Expect the main task to display all effective modeled-step assignments, including implicit medium effort, before workflow work. An invalid or unavailable model-effort pair in any possible branch must block before the first workflow step; a model-catalog listing alone does not count as availability evidence.

For a valid pair, confirm that a modeled step uses a child with the effective model and medium effort, while unmodeled steps and gates stay in the main task. When the child asks a multiple-choice clarification question, answer in the main task and verify the same child continues. Verify the gate waits for a human choice, reports results and workspace diffs in the selected task, and does not launch `speckit-flow-plan`. Record the visible child identity, effective model, and effort as live evidence; do not rely on a no-op executable for this claim.

## Exercise Luna implementation dispatch

Prepare a minimal, analysis-ready implementation task in the disposable consumer and invoke `$flow-kit-implement` for that feature. Confirm `implement-eligible-work` runs in a child whose effective assignment is `gpt-6-luna`/high, while the main task retains the workflow decisions and shows the resulting diff. Record the observed model, effort, and child identity. If that pair is unavailable to the selected account, record the preflight stop and treat live dispatch as unverified; do not substitute Sol or claim this release gate passed.

## Exercise stop and lifecycle boundaries

In disposable fixtures, test a child failure after a file edit, an interrupted main task, and a catalog refresh while a child is active. Include a skill-only refresh that changes the Codex package while leaving the current workflow YAML unchanged: build the changed development snapshot, then run `python3 tools/catalog.py refresh "$consumer_dir" --development-snapshot` while the child is active. The active child may finish, but no next step may run after the workflow digest, Specify bundle-record fingerprint, or FlowKit skill-record fingerprint changes. In each case, inspect `.specify/flow-controllers/runs/<run-id>/summary.json`: it should contain workflow version, step statuses, effective models and efforts, repository-relative changed files, and blocker, without full child transcripts or absolute paths. Confirm edits remain for operator review and no automatic retry or resume occurs.

Run install/refresh/remove with an unrelated local skill and feedback record present. Repeat with a same-name skill and with a locally edited FlowKit skill or shared helper; expect a reported ownership conflict and preserved local content. After resolving only the fixture conflict, run the supported removal route:

```sh
mise run catalog:remove "$consumer_dir"
```

Expect FlowKit-owned controller skills, shared helper, and `.specify/flow-kit/skills-install.json` to disappear while `.specify/flow-controllers/runs/` summaries, unrelated skills, feedback, and independently installed Specify components remain. Confirm the documentation explains that native `specify bundle` commands do not manage these direct Codex skills.

## Check documentation findability

Compare `docs/installation.md`, `README.md`, and `workflows/README.md` with `controllers/flow-kit/manifest.yml` and the required inputs in the eight workflow definitions. For each workflow, verify that all three documents give the same display name, `flow-kit-*` invocation, and required input. Verify that `workflows/README.md` has a manual fallback for each workflow. Record the mapping audit and any mismatches in `validation.md`; this is a documentation consistency check, not a timed operator study.

## Verify manual fallback

Review all eight manual paths in `workflows/README.md` against their installed workflow inputs, human gates, and stop points. With native workflow dispatch unavailable in a disposable consumer, follow at least one path through a gate using the underlying installed command skills and record its observed result. Native `specify workflow run` ignores FlowKit's `reasoning_effort` metadata; do not claim it ran a modeled step at high effort without separate evidence. Report any path whose instructions no longer permit a human-directed run after model fields and controller skills are added.

## Focused checks and evidence

```sh
~/.codex/venvs/skill-tools/bin/python -m unittest tests.test_controller tests.test_catalog tests.test_bundle_lifecycle
git diff --check
```

Capture tested CLI and Codex versions, bundle and component IDs, source commits or coordinates, source digests, the consumer scenario results, and any limits. Use [controller.md](contracts/controller.md) for task behavior and [lifecycle.md](contracts/lifecycle.md) for ownership expectations. Local success does not imply publication, stock Spec Kit compatibility beyond the tested coordinates, Git integration, roadmap verification, or feature acceptance.
