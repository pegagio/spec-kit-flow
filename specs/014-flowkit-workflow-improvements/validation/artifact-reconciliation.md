# F014 Artifact Reconciliation

On 2026-09-30 the operator directed flow-back of the accepted workflow review changes into the durable feature artifacts. This record reconciles source revision `c34ea2a` with Feature 014 intent. Some incremental flow-back already existed, but older scenarios, counts, loop bounds, gate assumptions, and quickstart commands conflicted with delivered source.

## Contents

The record separates accepted intent, source evidence, remaining delivery, and approval requirements.

- [Persistence boundary and authority](#persistence-boundary-and-authority)
- [Accepted change traceability](#accepted-change-traceability)
- [Delivered source and remaining work](#delivered-source-and-remaining-work)
- [Validation and limits](#validation-and-limits)
- [Required next decisions](#required-next-decisions)

## Persistence boundary and authority

The constitution requires accepted discoveries to flow through spec, plan, tasks, and implementation before proceeding. Source increments were committed directly to `develop` while Feature 014 remained Draft/in-progress and its artifacts were incompletely reconciled. That was a sequencing divergence. The operator explicitly directed this retrospective repair; it is recorded as a scoped resolution for F014, not a new acceptance boundary or an amendment of the constitution. Verified earlier feature directories and released catalog history remain untouched. Future changes to an accepted feature must flow forward through a new feature directory.

The [authority record](authority-decisions.md) preserves prior decisions and this repair. The exact [roadmap scope patch](roadmap-reconciliation.patch) was approved and applied verbatim on 2026-09-30 under Constitution II. The F014 roadmap scope now records the accepted refinements; lifecycle remains in-progress and no acceptance transition was made.

## Accepted change traceability

The current [spec](../spec.md), [plan](../plan.md), [tasks](../tasks.md), [data model](../data-model.md), [research](../research.md), and [contracts](../contracts/workflow-continuation.md) now describe the accepted behavior. Original task IDs and baseline evidence remain review provenance; superseding tasks identify which designs were replaced.

| Accepted intent | Requirements | Work records | Source evidence |
|---|---|---|---|
| Clarify starts with the core session, assesses afterward, repeats only with semantic progress, and has no terminal decision gate | FR-003, FR-004, FR-020, FR-027 | T021–T023, T057 | `c2b62f5`, `ed0c38c`; Clarify 0.4.2 |
| Plan and Tasks invoke the core skill, verify required outputs, and retry exact gaps without wrapper readiness/review gates | FR-005–FR-007, FR-020 | T050–T051 | `1439f39`, `990158a`; Plan/Tasks 0.4.2 |
| Implement continues existing eligible tasks until complete or blocked, with progress/cap checks and no goal dependency or artifact waterfall | FR-019, FR-020 | T049 supersedes T017 | `aa226d5`; Implement 0.4.2 |
| Analyze and Remediate uses one analyzer/assessment and a shared waterfall with spec, plan, and task entry points | FR-019, FR-020 | T052 | `6faa1b6`; Analyze 0.4.2 |
| Converge starts each pass with the core command, records remediation tasks on corrections, shares the waterfall, analyzes and verifies eligibility before implementation | FR-008–FR-012, FR-020 | T053 | `2fe2f0c`; Converge 0.4.2 |
| Human selection includes candidates and dependency discussion; selection/activation and specification authoring are separately invoked; combined Start Feature is deprecated | FR-001, FR-002, FR-018 | T054–T056 supersede combined Start Feature delivery | `09bac9d`, `9170430`; Select/Specify 0.1.0, deprecated Start Feature 0.6.0 |
| Equivalent paths join completed-evidence evaluation; required input is blocked, descriptive labels do not change choices or downstream authorization | FR-021, FR-027 | T056–T058 | `9170430`, `ed0c38c`; current graph and controller 0.5.0 |
| Close Out shares debrief correction stages, retains exact verification approval, reports readiness automatically, and reconciles wiki sources through its sibling loop | FR-013–FR-015, FR-020 | T058–T059 | `2b236d7`; Close Out 0.6.0 |
| Standalone wiki maintenance starts with lint, refreshes one registered authorized stale source per pass, and retains every other issue | FR-025 | T060, US8 | `c34ea2a`; Wiki Lint Update 0.1.0 |
| Project-owned diagrams use exact source terms, type shapes, delegation outlines, one Start marker, and declared descriptive edge labels | FR-026, SC-012 | T061, US9 | `90f6edf`; `skills/flowkit-render-workflow/SKILL.md` and adjacent diagrams |
| Reconcile artifacts, source inventory, evidence, and open delivery without declaring acceptance | FR-017, FR-018, FR-022–FR-024 | T048, T062–T065 | This record and [machine evidence](artifact-reconciliation.json) |

## Delivered source and remaining work

The source bundle 0.13.0 pins ten active workflows and the controller 0.5.0 exposes ten thin launchers. One deprecated definition remains stop-only source with no active binding. The [current inventory](../current-workflow-inventory.md) records every source node, command, agent, branch, gate, and loop. Historical review notes and baseline digests are labeled as historical rather than rewritten into evidence of current execution.

The three core-skill-first output/session loops and Implement have five body passes. Analyze uses one read-only baseline and five correction passes. Converge and Close Out debrief use six source-command checks permitting five corrections and final confirmation. Close Out wiki maintenance uses five ingest/lint passes. Wiki Lint Update uses 26 lint checks permitting 25 source refreshes and final confirmation. All remain subject to earlier blocked, no-progress, stale-evidence, and command-failure stops.

T043 package-pin alignment and T045 user documentation are delivered. T034–T042 remain open: native configurations and per-step role rationale are not complete, only the temporary Coder probe exists locally, and structural assignments do not prove native availability. T044 and T046–T047 retain final disposable-consumer, consolidated report, and optional desktop evidence work. T064 is complete with exact roadmap patch approval and application; T065 records subsequent operator-invoked analysis/convergence and any further artifact repair. The feature remains Draft/in-progress.

## Validation and limits

Current checks passed: 111 unit tests with one external lifecycle suite skipped, eleven pinned Specify definition schema validations, static graph projection with zero unexplained terminals, bundle/source version and active-launcher agreement, source-current inventory coverage, local artifact links, and whitespace checks. [Machine evidence](artifact-reconciliation.json) records source coordinates, component versions/digests, current artifact digests, and observed limitations.

The external lifecycle suite lacks configured independent roadmap/wiki source paths. No live agent execution, final consumer lifecycle acceptance, release, install, publication, or feature acceptance is established by this repair. The rendering skill and source diagrams are recorded as delivered artifacts; no renderer visual review was performed during this reconciliation.

## Required next decisions

The exact roadmap scope repair is applied. Separately invoke Analyze and Remediate for consequential artifact reconciliation and Converge for implementation coverage; Constitution I recommends those checks and reserves their invocation to the operator. Complete outstanding agent and consumer validation tasks, then review the artifact and implementation diffs jointly before acceptance. This repair does not invoke those workflows or commit changes.
