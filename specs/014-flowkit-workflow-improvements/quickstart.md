# Quickstart: Validate F014 Workflow Continuation

Use this guide after implementation artifacts exist. The operator-approved roadmap amendment authorizes the all-eight-workflow review, and Constitution 6.0.0 supplies the approved in-workflow authority. Validation is executed by tests and disposable-consumer scripts, with a generated evidence report. Consequential workflow decisions still use the prescribed human gates. At the end, the operator may check one or two visible Codex desktop behaviors; routine validation does not depend on those checks.

## Prepare the source checkout

From this repository, install its pinned tools explicitly and record the selected Specify version. The current source differs from the checked-in release catalog, so use a disposable development snapshot for consumer validation.

```sh
mise trust
mise install
mise exec -- specify --version
git diff --check
```

The validation script records the Git revision, each changed workflow and controller component ID/version/source digest, the Specify CLI version, and the source coordinates used for the run. It reports these with test results; a successful local run does not imply release or consumer adoption.

## Validate definitions and controller behavior

Automated graph checks must cover all eight installed workflow definitions: unique step IDs, supported expressions, positive finite loop caps, a fresh assessment in each loop, explicit terminal states, and exact agent names on every delegated executable branch. Preflight must fail before workflow work when an assignment, route, condition, or native agent is missing or invalid.

After implementation, run the existing and new suites with the prescribed skill-validation Python environment:

```sh
~/.codex/venvs/skill-tools/bin/python -m unittest tests.test_controller tests.test_catalog tests.test_bundle_lifecycle tests.test_workflow_paths tests.test_workflow_graph tests.test_agent_configs tests.test_snapshot_validation
```

Focused fixtures must demonstrate the following for each of the eight workflows:

| Evidence path | Expected result |
|---|---|
| Clean initial assessment | Route before entering any corrective `do-while` body and reach that workflow's evidenced conclusion without an unnecessary correction. |
| Routine correctable finding | Execute the reviewed correction, reassess current evidence, and continue within the same invocation while progress is confirmed. |
| Finding resolved after a later pass | Report success only after refreshed evidence proves the workflow's success condition. |
| Repeated finding, no progress, stale or contradictory evidence | Stop promptly with a specific reason and preserved resumption evidence. |
| Continued progress at the fifth body pass | Stop at the safety cap with `continue` evidence, never a clean verdict. |
| Consequential decision or substantive question | Stop at the reviewed main-task gate and use the operator's answer; do not infer approval. |
| Interruption or changed installation | Stop at the next safe boundary with distinct records for completed loop passes. |

The test matrix exercises the recorded Start Feature, Clarify, Plan, Tasks, Analyze, Implement, Converge, and Close Out return paths. Clarify must preserve the command's five-question cap per session while allowing another bounded session only under its approved continuation rule. Close Out may update an evidenced clean Draft spec to Complete only under its approved authority rule; roadmap verification remains a separate exact human decision. Gate fixtures inject explicit decisions or assert that execution pauses for one; they never treat fixture answers as live approval.

## Validate the disposable consumer

Automate the [installation guide's development-snapshot procedure](../../docs/installation.md#install-in-another-project) in an initialized temporary consumer. The script verifies installed workflow definitions and direct FlowKit skills, executes selected branches through native Specify loading and the direct Codex controller, and checks each package's manual prompt path using fixtures. A no-op Codex dispatch check validates structure only; capture live named-agent execution separately when the supported client exposes machine-readable evidence.

For every selected native agent name, automated checks parse the repository-local `.codex/agents/<name>.toml` file and verify exact Codex selection when observable. Disposable-consumer tests assert that bundle install, refresh, and removal preserve consumer agent files and unrelated components. If the client does not expose selection evidence, the report marks live selection unverified. F014 does not install agent files into other projects.

## Final Codex desktop check

After the automated report is complete, offer the operator no more than two short, concrete checks in a prepared disposable consumer: confirm that one representative workflow visibly continues after a routine correction, and confirm that a named agent and a consequential gate appear as intended in the Codex desktop task. Supply the exact action and expected visible result for each check. Record the operator's observation as desktop experience evidence, separate from automated test results. These checks do not replace branch coverage, component provenance, or an explicit approval decision.

## Validation report

The generated report identifies each workflow and branch tested, observed terminal state, passes completed, remaining findings, fixture gate decisions, agent assignment evidence, and any untested path. Automated assertions compare results with [the continuation contract](contracts/workflow-continuation.md) and [the assignment contract](contracts/agent-assignment.md). The report distinguishes passing checks from unverified claims, records any final desktop observations separately, and identifies the governing decisions needed for source changes. Feature acceptance remains a separate operator decision.
