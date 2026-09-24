# Project Status and Handoff

**Snapshot**: 2026-09-24. Recheck Git, installed CLI, component sources, and tests before treating this snapshot as current.

## Contents

- [Purpose and settled decisions](#purpose-and-settled-decisions)
- [Current validation and limits](#current-validation-and-limits)
- [Reproduce the focused checks](#reproduce-the-focused-checks)
- [Next decisions](#next-decisions)

## Purpose and settled decisions

Spec Kit Flow packages the author's human-directed, merge-bounded flow-back process as reusable Spec Kit components. The generic source and release boundary is this repository, not The Diagram. The repository and bundle ID are `spec-kit-flow`; workflow and extension IDs owned here use `speckit-flow-<purpose>`. Independently versioned extensions retain their manifest IDs. The Diagram is the first dogfood consumer and may later add a separately versioned control-plane adapter. Agent/model selection and dispatch, Diagram canonical-state behavior, and a custom clarification preset are not part of this generic bundle.

Eight workflow source packages are present under `workflows/`: start-feature, clarify, plan, tasks, analyze-remediate, implement, converge, and closeout. Plan and tasks are independently adoptable. Source packages remain the review surface; native installation creates operational copies. The versioned bundle manifest is `bundles/spec-kit-flow/bundle.yml` version `0.2.0`. It pins `flow-roadmap` `0.2.0`, `flow-wiki` `2.0.0`, portable feedback `0.1.0`, start-feature and closeout workflows `0.2.0`, and the six other workflows `0.1.0`, with Codex as the initial supported integration. The extension repositories are named `spec-kit-flow-roadmap` and `spec-kit-flow-wiki`; the workflows call `speckit.flow-roadmap.*` and `speckit.flow-wiki.*`. No preset is accepted or bundled.

Consumer-side `speckit-flow-feedback` captures local observations and exports JSON plus a Markdown projection without source connectivity. The separate `speckit-flow-feedback-maintainer` component validates transferred reports and records proposed dispositions under `feedback/inbox/` and `feedback/triage/`; it is not installed by the consumer bundle. The first inbox/triage pair records the Diagram `diagram-converge` terminal-prompt observation. Its proposed source refinement must be reviewed and, if accepted, specified, planned, tasked, and implemented here through normal flow-back—not applied by intake.

## Current validation and limits

The disposable lifecycle test in `tests/test_bundle_lifecycle.py` passed on 2026-09-24 with the locally forked Specify CLI `1.0.10.dev0+pegagio.2` and the local `flow-roadmap` and `flow-wiki` source checkouts. It installs the bundle into a clean non-Diagram Codex project through a private localhost catalog, checks component provenance, command availability in installed extension manifests, and native workflow resolution, runs a bounded clean route with a no-op Codex executable, exports feedback, tests maintainer acceptance and malformed-report rejection, refreshes, and removes the bundle without deleting an unrelated consumer workflow. A separate case rejects a `flow-wiki` version mismatch. The feedback and maintainer extensions also have focused Python unit tests. The no-op run proves workflow-engine dispatch, not live-agent quality.

The bundle is not published to a vetted catalog or release source. A local manifest resolves component IDs from installed components or configured catalogs; it does not embed them. The lifecycle test currently requires compatible `flow-roadmap` and `flow-wiki` source directories supplied by the caller. The 2026-09-24 run used independent local checkouts, not The Diagram. This is a test-harness availability gap for a fresh machine, not a generic bundle runtime dependency. Before claiming independent reproducibility or broad consumer compatibility, vet independently obtainable, version-pinned sources and rerun the fixture from them. Stock Spec Kit compatibility is also unverified; the local fork includes a fix for catalog-sourced workflow installation during bundle install. See `docs/upstream-issues/spec-kit-bundle-workflow-install.md`.

The tested `flow-roadmap` source was commit `6e29a26` (extension manifest SHA-256 `8f454d97d8b36a15008da81a61876c0dc7864d5a7955f14e6f2c77f9e6b8b083`); `flow-wiki` was commit `a2fd927` (extension manifest SHA-256 `9e9d196220990e8c67dcfbc0c074f8a025e7afb9a30ce1636eeee9b8995c1f8e`). The changed start-feature and closeout workflow source SHA-256 digests were `e3e6351fe812c4c4093f3ca2311a7de967a14d2700bd52f87bc6b15b10afeb57` and `c5ee89e3ab4eede96b0a147fdbcb1af280815f81e184fd661530a1f900db7515`, respectively. These identify local source evidence, not published package artifacts.

## Reproduce the focused checks

Use a compatible `specify` executable and Python 3. Set `SPECIFY_BIN` if the executable is not on `PATH`. Use the local skill-tools Python only if that environment exists and has the required packages; otherwise an ordinary Python 3 suffices for these standard-library tests.

```sh
python3 -m unittest discover -s extensions/speckit-flow-feedback/tests -p 'test_*.py'
python3 -m unittest discover -s extensions/speckit-flow-feedback-maintainer/tests -p 'test_*.py'

SPECIFY_BIN=/path/to/compatible/specify \
SPEC_KIT_FLOW_TEST_ROADMAP_SOURCE=/path/to/roadmap-extension \
SPEC_KIT_FLOW_TEST_WIKI_SOURCE=/path/to/wiki-extension \
python3 -m unittest discover -s tests -p test_bundle_lifecycle.py
```

The lifecycle test starts a temporary loopback catalog and cleans up its disposable consumer. If required source inputs are absent, it skips rather than proving bundle compatibility. `tests/consumer-fixtures/README.md` documents the sanitized observation and optional portable-report export inputs. `docs/installation.md` distinguishes local validation from a future published installation path.

## Next decisions

1. Vet independently obtainable sources for the pinned `flow-roadmap`, `flow-wiki`, feedback, and workflow components, then define the catalog or release artifact and repeat clean-consumer installation on a fresh machine.
2. Decide when to run a live Codex consumer workflow and review its output, gates, stop behavior, and manual fallback. The current fixture does not replace that adoption decision.
3. Triage the existing terminal-prompt feedback as a possible bounded workflow-source refinement. Do not assume intake approved the change or directly edit an installed copy.
4. Consider the clarification-cap preset and any Diagram adapter only through their separate design and approval paths; do not let either delay generic bundle validation by default.

The originating planning and dogfood record is The Diagram's Feature 027 (`specs/027-workflow-prompt-hardening/`, including its spec, plan, contracts, tasks, and validation). It explains why these boundaries were chosen. Future work in this repository should carry its own current specifications and decisions so it does not depend on access to that project or its conversation history.
