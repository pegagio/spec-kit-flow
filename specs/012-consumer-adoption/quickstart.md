# Quickstart: Validate Consumer Adoption

Use this guide to validate the operator-reviewed adoption route. The scenario file contains synthetic inputs and expected results only; it does not claim that the cases were observed or that any consumer adopted the model.

## Contents

The sections below provide the planning decisions and review details.

- [Prerequisites](#prerequisites)
- [Prepare a Disposable Consumer](#prepare-a-disposable-consumer)
- [Run the Adoption Cases](#run-the-adoption-cases)
- [Validate Agent Behavior](#validate-agent-behavior)
- [Automated Checks](#automated-checks)
- [Review the Evidence](#review-the-evidence)

## Prerequisites

Use a source checkout containing the implemented documentation, the pinned Specify CLI from `mise.toml`, Python 3.11, and Codex for live behavior checks. Run `mise trust` and `mise install` explicitly as documented in the installation guide. Keep every consumer under the system temporary directory and use synthetic project names and content. Record guide/template source coordinates or digests and actual CLI version before testing.

## Prepare a Disposable Consumer

From the repository root, create an isolated consumer and initialize its Codex skills integration:

```sh
consumer_dir="$(mktemp -d)"
specify_bin="$(mise which specify)"
(
  cd "$consumer_dir"
  "$specify_bin" init --here --force --non-interactive --integration codex --integration-options="--skills"
)
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py install "$consumer_dir" --development-snapshot
"$specify_bin" --version
```

Record installed component identities, versions, and digests from the consumer's Specify records and `.specify/flow-kit/skills-install.json`; label snapshot packages unreleased. Record source coordinates and digests for the adoption documents separately because the runbook is consumed from the source checkout rather than installed in the controller package. Establish a synthetic integration branch and record it as the fixture's designated boundary.

## Run the Adoption Cases

For each row, create a fresh consumer or restore a documented synthetic baseline. Open the consumer as the selected Codex project for live checks. Use the implemented runbook's copyable prompt and worksheet; for the manual case, a human follows the same steps. Save sanitized observations and exact decisions in the feature validation record. The [contract](contracts/adoption.md) and [data model](data-model.md) define the required report fields. `tests/consumer-fixtures/adoption/scenarios.json` records expected classifications, not observations or operator decisions.

| Case | Action | Expected observable result |
| --- | --- | --- |
| New consumer | Inspect missing rules, review exact proposal, accept | Changes occur after decision; every rule has final evidence in both columns; confirmed result |
| Already compatible | Use equivalent or stricter compatible wording in both locations | No constitutional amendment or duplicated guidance; citations justify each rule |
| Governance conflict | Existing rule forbids updating unmerged specs | Conflict is cited; no change before decision; unresolved until settled |
| Decline | Decline a complete proposed patch | Governance/guidance hashes unchanged; declined result |
| Defer | Defer missing-rule additions, then separately defer a conflict | No change; partial for missing evidence, unresolved for conflict; decision is defer |
| Partial acceptance | Accept only governance changes | Agent guidance gaps remain visible; partial result |
| README only | Put matching text only in README | Active guidance column remains missing; cannot confirm |
| Uncertain applicability | Use nested or conflicting agent instructions | Applicability is investigated; unresolved while authority remains uncertain |
| Nonstandard boundary | Designate `integration` as merge branch | Guidance/report use the actual boundary without assuming a conventional name |
| Stale proposal | Edit a target after proposal review but before application | Patch is not applied against changed baseline; reinspect and seek decision on revised proposal |
| Refresh with local edits | Refresh components, then reassess changed compatible/conflicting wording | Local text is byte-preserved; result derives from current state |
| Removal | Remove installed components after adoption | Adopted guidance, governance, history, review record, unrelated files and feedback remain |

Exercise the refresh and removal rows with the existing catalog interface, retaining before/after hashes of consumer-owned files:

```sh
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py refresh "$consumer_dir" --development-snapshot
PATH="$(dirname "$specify_bin"):$PATH" python3 tools/catalog.py remove "$consumer_dir"
```

Do not run removal against a real project as part of this validation. If a lifecycle operation fails, record the actual component state and failure; do not claim the full scenario passed.

## Validate Agent Behavior

In an adopted disposable consumer, supply an accepted pre-merge behavioral discovery and inspect whether spec, plan, tasks, and implementation consequences are reconciled before continued work. Then present a post-integration behavioral change and verify that guidance directs it to a new feature while preserving merged meaning. Finally, present a missing consistency check and inspect whether the agent flags it and recommends the relevant workflow without invoking that workflow or its underlying command.

Record actual observations and a concise sanitized explanation of any deviation. A no-op executable or prompt text inspection cannot substitute for these live cases. Retain a separate manual review case proving the procedure works without a direct skill or native workflow dispatch.

## Automated Checks

After implementation, run focused document/fixture and preservation tests followed by the native disposable bundle lifecycle test. The native lifecycle test uses the checked-out extension sources and pinned Specify CLI:

```sh
mise exec -- python3 -m unittest discover -s tests -p 'test_consumer_adoption*.py' -v
mise exec -- python3 -m unittest discover -s tests -p 'test_catalog.py' -v
SPEC_KIT_FLOW_TEST_ROADMAP_SOURCE="$(pwd)/.specify/extensions/flow-roadmap" SPEC_KIT_FLOW_TEST_WIKI_SOURCE="$(pwd)/.specify/extensions/flow-wiki" mise exec -- python3 -m unittest discover -s tests -p 'test_bundle_lifecycle.py' -v
```

For tests specifically validating Codex skills, use the project-required skill-tools Python environment; if that interpreter lacks dependencies, report it before changing the environment. The planned adoption tests validate source documents and lifecycle preservation, not skill generation.

The adoption discovery pattern includes `test_consumer_adoption.py`, `test_consumer_adoption_lifecycle.py`, and `test_consumer_adoption_guidance.py`. Together these tests check rule coverage, worksheet evidence fields, scenario shape and expected outcomes, and preservation of synthetic consumer-owned files through controller skill install/refresh/removal. The native bundle lifecycle test also hashes consumer guidance, constitution, adoption review records, and unrelated files across bundle install/refresh/removal. Semantic outcomes must remain separately observed evidence. Record exact commands, results, skips, and reasons in `validation.md`; a skipped live case prevents claims that agent behavior was validated.

## Review the Evidence

Verify SC-001–SC-007 against recorded outcomes, including zero unapproved constitutional changes and no false confirmed results. Inspect the combined feature and implementation diff before declaring readiness for any later gate. Recommend operator-invoked analysis/remediation after tasks, convergence after implementation, and applicable validation before merge. Do not invoke a later workflow automatically.
