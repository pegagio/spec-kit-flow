# Quickstart: Validate F014 Workflow Improvements

The source contains ten active workflows and one deprecated stop-only definition. Use this guide for current static and fixture validation. The recorded snapshot-consumer and consolidated automated checks are complete for their tested source; live native-agent selection remains unverified. T066–T069 add deterministic semantic-review correction coverage recorded separately in the validation report.

## Run available checks

Use the prescribed skill-tools Python environment from the source checkout:

```sh
~/.codex/venvs/skill-tools/bin/python -m unittest discover -s tests
~/.codex/venvs/skill-tools/bin/python tools/validate_workflows.py --fail-on-unexplained
~/.codex/venvs/skill-tools/bin/python tools/validate_workflows.py --json
git diff --check
```

The source inventory checks all eleven definitions; active bundle and launcher bindings include only ten. Fixture suites test routing, progress and cap stops, exact human choices, task history, active target identity, joined branches, and selected-source wiki ingestion. A passing projection is structural evidence, not live controller or named-agent execution.

## Check the delivered workflow contracts

Use [the current inventory](current-workflow-inventory.md) and [continuation contract](contracts/workflow-continuation.md) to compare declared IDs, assignments, branches, gates, and loops with the YAML and adjacent diagrams.

| Workflow group | Required fixture evidence |
|---|---|
| Select Feature and Specify | Candidate/dependency presentation, explicit choice, exact patch approval, pointer-only activation, unchanged existing spec bytes, same-target authoring, verified linkage and shared brief. |
| Deprecated Start Feature | Stops without mutation, dispatch, or automatic replacement invocation; excluded from active packaging. |
| Clarify | Core session first, operator-provided answers, five questions per session, fresh residual ambiguity assessment, progress and five-session bound. |
| Plan and Tasks | Structural checks plus independent Reviewer semantic assessment of populated but deficient artifacts; exact located findings handed to Planner/Tasker through existing author-owned correction paths; fresh confirmation of prior finding resolution, preserved design/task history, no-progress and cap stops, operator-owned product answers, unchanged topology and five-pass bound. |
| Implement | Repeated core implementation of existing eligible tasks, checklist progress, complete or blocked stop, no wrapper re-spec/plan/task/analyze or goal dependency. |
| Analyze and Remediate | Read-only baseline, shared waterfall and analyzer, five corrections plus final assessment, no-progress and blocked stop. |
| Converge | Fresh core command every pass, mandatory task recording on correction, shared waterfall, analysis and eligibility before implementation, five corrections plus final confirmation. |
| Close Out | Evidence-backed existing-spec completion, shared debrief waterfall, exact verification gate, sibling five-pass wiki loop, fresh lint before automatic readiness report. |
| Wiki Lint Update | Initial lint, cited registered-source deduplication, single-source refresh, all findings retained, exact URL authorization, 25 refreshes plus final lint confirmation. |
| Rendering skill | Exact source IDs, one Start edge, node kind shapes, delegated outlines, optional labels without placeholders, declared branches and loop guards. |

## Distinguish recorded consumer checks and remaining agent evidence

The current [validation report](validation/report.json) records 116 automated tests with zero failures/errors and snapshot install/refresh/remove passing for source revision `c34ea2aa2fa23e131d796be39343064f0a93a652` with working-tree changes under Specify `1.0.10.dev0+pegagio.2`. This is attributable recorded evidence, not a rerun after artifact correction. T044 and the T046 consolidated report are delivered within those limits.

`tests/test_snapshot_validation.py` initializes a temporary consumer and installs, refreshes, and removes the local bundle snapshot. It uses checksum-pinned roadmap, wiki, and feedback release packages from `catalog/packages`, recording their versions, digests, source coordinates, the Specify CLI version, result, and test limits. No live checkouts of other projects are required. The distinct source-checkout lifecycle suite in `tests/test_bundle_lifecycle.py` remains skipped unless its roadmap and wiki source paths are configured. Source bundle 0.13.5 and controller 0.5.1 differ from the published catalog; no release claim follows from these checks.

The snapshot lifecycle test verifies consumer-owned files and an unrelated workflow survive install, refresh, and removal. The source-checkout lifecycle test additionally exercises current external component working trees; it can be enabled with `SPEC_KIT_FLOW_TEST_ROADMAP_SOURCE` and `SPEC_KIT_FLOW_TEST_WIKI_SOURCE`, but is not required for T044. `tests/test_agent_configs.py` parses all eight repository-local agent definitions and checks all 49 active assignments. These checks do not prove live Codex agent selection. `tools/validate_workflows.py` reports native selection as unverified because it does not launch Codex subagents.

## Record outcomes and review

The [reconciliation record](validation/artifact-reconciliation.md), [machine evidence](validation/artifact-reconciliation.json), and [current validation report](validation/report.json) identify the scope, provenance, observed checks, and remaining work. [Optional desktop checks](validation/desktop-checks.md) are prepared but not run. Historical baseline and per-increment records retain their original evidence boundaries. The independent-source consumer lifecycle suite is a separate skipped check, not an open T044 requirement; earlier skipped observations remain historical. Native-agent selection remains unverified in the recorded automated report, optional desktop observations remain not run, and T066–T069 now cover the semantic-review correction scenarios above through deterministic scripted-agent fixtures, source prompt assertions, and exact topology checks; live reasoning remains unverified. Recommend separately invoking Analyze and Remediate after artifact reconciliation and Converge after implementation; this guide does not invoke them. Roadmap patch approval, release, Git integration, and feature acceptance remain separate operator decisions.

## Semantic-review follow-up evidence

The `semantic_review_follow_up` entry in [validation/report.json](validation/report.json) records 26 path tests, 11 graph tests, 4 agent tests, source validation, exact changed-source digests, and limits for T066–T069. The source versions are Plan and Tasks 0.4.4, Implement 0.4.4, Converge 0.4.5, Closeout 0.6.2, and bundle 0.13.3. Earlier snapshot provenance remains historical; this follow-up did not refresh installed copies or rerun the lifecycle suites. The shared T065/T071/T073/T075/T076/T077 evidence obligation is now delivered once in `source_current_reconciliation`; independent Converge run `0a87d86f-bb0a-4189-b692-b0367e434624` confirmed the correction.


## Source-current evidence reconciliation

The `source_current_reconciliation` entry in [the validation report](validation/report.json) records bundle 0.13.5, controller 0.5.1, all eleven source workflow versions and digests, active bundle pin verification, the independently verified post-Implement syntax-fix boundary, and clean analysis before the shared evidence correction. Historical 116-test/snapshot, 41 semantic-review, and 50 controller/12 graph results remain separate observations; this evidence-only pass reran the static workflow validator, which passed eleven definitions with zero unexplained terminals. Fresh independent Converge run `0a87d86f-bb0a-4189-b692-b0367e434624` confirmed resolution with no remaining findings. External-working-tree lifecycle remains skipped, live reasoning/native selection unverified, optional desktop checks unrun, and feature Draft/roadmap in-progress with release, Git, and acceptance authority separate.

## Incorporated source validation

After incorporation and T078/T079 corrections, the full suite ran 126 tests with zero failures or errors; the optional external-working-tree lifecycle suite was skipped. The checksum-pinned consumer snapshot install/refresh/remove and all eleven workflow definitions passed. All eight source-identical native role configurations passed exact-name readiness probes. Current results and source digests are recorded in `final_source_validation` and `native_role_availability` in [the validation report](validation/report.json). Native identity/model introspection, general live semantic correctness and optional desktop observations remain outside that evidence. Feature acceptance, roadmap verification, release and Git integration remain separately controlled.
