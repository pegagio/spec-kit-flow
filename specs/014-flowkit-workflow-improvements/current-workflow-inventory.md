# F014 Current Workflow Inventory

**Source boundary**: Working tree inspected on 2026-10-01. Ten active packages and one deprecated definition are recorded below. This is a static source projection, not live-agent or acceptance evidence. Historical review notes remain in [workflow-review-inventory.md](workflow-review-inventory.md).

## Contents

Use the summary for package scope and each workflow section for exact graph terms.

- [Package summary](#package-summary)
- [Complete source graph](#complete-source-graph)
  - [speckit-flow-analyze-remediate](#speckit-flow-analyze-remediate)
  - [speckit-flow-clarify](#speckit-flow-clarify)
  - [speckit-flow-closeout](#speckit-flow-closeout)
  - [speckit-flow-converge](#speckit-flow-converge)
  - [speckit-flow-implement](#speckit-flow-implement)
  - [speckit-flow-plan](#speckit-flow-plan)
  - [speckit-flow-select-feature](#speckit-flow-select-feature)
  - [speckit-flow-specify](#speckit-flow-specify)
  - [speckit-flow-start-feature](#speckit-flow-start-feature)
  - [speckit-flow-tasks](#speckit-flow-tasks)
  - [speckit-flow-wiki-lint-update](#speckit-flow-wiki-lint-update)

## Package summary

Versions, counts, entries, and loops are derived from the current definitions. Empty branch bodies join the next declared step; success still depends on completed evidence.

| Workflow | Version | Delivery | Entry step | Nodes | Branches | Gates | Loops | Delegated |
|---|---|---|---|---|---|---|---|---|
| `speckit-flow-analyze-remediate` | 0.4.5 | Active | `analysis-remediation-loop` | 11 | 6 | 0 | 1 | 5 |
| `speckit-flow-clarify` | 0.4.4 | Active | `clarification-session-loop` | 4 | 0 | 0 | 1 | 2 |
| `speckit-flow-closeout` | 0.6.3 | Active | `assess-closeout-readiness` | 34 | 24 | 1 | 2 | 15 |
| `speckit-flow-converge` | 0.4.7 | Active | `convergence-remediation-loop` | 16 | 12 | 0 | 1 | 8 |
| `speckit-flow-implement` | 0.4.5 | Active | `assess-implementation-state` | 5 | 0 | 0 | 1 | 3 |
| `speckit-flow-plan` | 0.4.5 | Active | `plan-output-loop` | 5 | 0 | 0 | 1 | 2 |
| `speckit-flow-select-feature` | 0.1.1 | Active | `list-roadmap-options` | 11 | 6 | 2 | 0 | 3 |
| `speckit-flow-specify` | 0.1.1 | Active | `inspect-active-feature` | 16 | 11 | 1 | 0 | 6 |
| `speckit-flow-start-feature` | 0.6.0 | Deprecated; stop only | `report-start-feature-deprecation` | 1 | 0 | 0 | 0 | 0 |
| `speckit-flow-tasks` | 0.4.5 | Active | `tasks-output-loop` | 5 | 0 | 0 | 1 | 2 |
| `speckit-flow-wiki-lint-update` | 0.1.2 | Active | `wiki-lint-update-loop` | 7 | 3 | 0 | 1 | 3 |

## Complete source graph

The following tables record every authored node, direct parent/branch, type, explicit delegated assignment, command, switch outcome, human gate, and loop policy. An absent assignment means main-task execution. Only explicit delegation launches a child. Per-step role fit is recorded in [agent-assignment-inventory.md](agent-assignment-inventory.md); native client selection remains unverified; current automated results are recorded in [validation/report.json](validation/report.json). These source tables do not establish live-agent availability.

### speckit-flow-analyze-remediate

Source: [workflow.yml](../../workflows/speckit-flow-analyze-remediate/workflow.yml). Final declared report: `report-analysis-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `analysis-remediation-loop` | Root sequence | do-while | — | — |
| `prepare-analysis-flowback` | `analysis-remediation-loop` / loop-body | prompt | — | — |
| `route-specification-remediation` | `analysis-remediation-loop` / loop-body | switch | — | — |
| `remediate-specification` | `route-specification-remediation` / run | command | Specifier | speckit.specify |
| `route-plan-remediation` | `analysis-remediation-loop` / loop-body | switch | — | — |
| `remediate-plan` | `route-plan-remediation` / run | command | Planner | speckit.plan |
| `route-task-remediation` | `analysis-remediation-loop` / loop-body | switch | — | — |
| `remediate-tasks` | `route-task-remediation` / run | command | Tasker | speckit.tasks |
| `analyze-artifacts` | `analysis-remediation-loop` / loop-body | command | Reviewer | speckit.analyze |
| `assess-analysis` | `analysis-remediation-loop` / loop-body | prompt | Reviewer | — |
| `report-analysis-outcome` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-specification-remediation` | `run` | run | `remediate-specification` |
| `route-specification-remediation` | `skip` | skip | Empty; join next declared step |
| `route-plan-remediation` | `run` | run | `remediate-plan` |
| `route-plan-remediation` | `skip` | skip | Empty; join next declared step |
| `route-task-remediation` | `run` | run | `remediate-tasks` |
| `route-task-remediation` | `skip` | skip | Empty; join next declared step |

Loop `analysis-remediation-loop`: read-only first baseline pass; maximum 6 body passes; condition `{{ steps.assess-analysis.output.state == 'continue' }}`.

### speckit-flow-clarify

Source: [workflow.yml](../../workflows/speckit-flow-clarify/workflow.yml). Final declared report: `clarification-outcome-stop`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `clarification-session-loop` | Root sequence | do-while | — | — |
| `clarify-session` | `clarification-session-loop` / loop-body | command | Specifier | speckit.clarify |
| `assess-clarification-after-session` | `clarification-session-loop` / loop-body | prompt | Reviewer | — |
| `clarification-outcome-stop` | Root sequence | prompt | — | — |

Loop `clarification-session-loop`: core work then assessment; maximum 5 body passes; condition `{{ steps.assess-clarification-after-session.output.state == 'continue' }}`.

### speckit-flow-closeout

Source: [workflow.yml](../../workflows/speckit-flow-closeout/workflow.yml). Final declared report: `report-closeout-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `assess-closeout-readiness` | Root sequence | prompt | Reviewer | — |
| `route-initial-closeout` | Root sequence | switch | — | — |
| `prepare-closeout-status` | `route-initial-closeout` / continue | prompt | — | — |
| `route-closeout-status` | `route-initial-closeout` / continue | switch | — | — |
| `mark-converged-specification-complete` | `route-closeout-status` / run | command | Specifier | speckit.specify |
| `closeout-debrief-loop` | `route-initial-closeout` / continue | do-while | — | — |
| `debrief-roadmap` | `closeout-debrief-loop` / loop-body | command | Reviewer | speckit.flow-roadmap.debrief |
| `assess-closeout-debrief` | `closeout-debrief-loop` / loop-body | prompt | Code Reviewer | — |
| `route-closeout-correction` | `closeout-debrief-loop` / loop-body | switch | — | — |
| `prepare-closeout-flowback` | `route-closeout-correction` / continue | prompt | — | — |
| `route-closeout-specification-remediation` | `route-closeout-correction` / continue | switch | — | — |
| `reconcile-closeout-specification` | `route-closeout-specification-remediation` / run | command | Specifier | speckit.specify |
| `route-closeout-plan-remediation` | `route-closeout-correction` / continue | switch | — | — |
| `reconcile-closeout-plan` | `route-closeout-plan-remediation` / run | command | Planner | speckit.plan |
| `route-closeout-tasks-remediation` | `route-closeout-correction` / continue | switch | — | — |
| `reconcile-closeout-tasks` | `route-closeout-tasks-remediation` / run | command | Tasker | speckit.tasks |
| `analyze-closeout-artifacts` | `route-closeout-correction` / continue | command | Reviewer | speckit.analyze |
| `assess-closeout-task-eligibility` | `route-closeout-correction` / continue | prompt | Reviewer | — |
| `route-closeout-implementation` | `route-closeout-correction` / continue | switch | — | — |
| `implement-closeout-eligible-tasks` | `route-closeout-implementation` / continue | command | Coder | speckit.implement |
| `prepare-roadmap-verification` | Root sequence | prompt | — | — |
| `route-roadmap-verification` | Root sequence | switch | — | — |
| `approve-roadmap-transition` | `route-roadmap-verification` / patch-ready | gate | — | — |
| `route-roadmap-transition` | `route-roadmap-verification` / patch-ready | switch | — | — |
| `apply-approved-roadmap-verification` | `route-roadmap-transition` / approve-patch | command | — | speckit.flow-roadmap.write |
| `prepare-wiki-maintenance` | Root sequence | prompt | Roadmap Agent | — |
| `route-wiki-maintenance` | Root sequence | switch | — | — |
| `wiki-reconciliation-loop` | `route-wiki-maintenance` / ready | do-while | — | — |
| `prepare-wiki-refresh` | `wiki-reconciliation-loop` / loop-body | prompt | — | — |
| `ingest-curated-context` | `wiki-reconciliation-loop` / loop-body | command | Wiki Curator | speckit.flow-wiki.ingest |
| `lint-wiki` | `wiki-reconciliation-loop` / loop-body | command | Reviewer | speckit.flow-wiki.lint |
| `assess-wiki-maintenance` | `wiki-reconciliation-loop` / loop-body | prompt | Reviewer | — |
| `verify-closeout-readiness` | `route-wiki-maintenance` / ready | prompt | Reviewer | — |
| `report-closeout-outcome` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-initial-closeout` | `continue` | continue | `prepare-closeout-status` |
| `route-initial-closeout` | `complete` | complete | Empty; join next declared step |
| `route-initial-closeout` | `blocked` | blocked | Empty; join next declared step |
| `route-closeout-status` | `run` | run | `mark-converged-specification-complete` |
| `route-closeout-status` | `skip` | skip | Empty; join next declared step |
| `route-closeout-correction` | `continue` | continue | `prepare-closeout-flowback` |
| `route-closeout-correction` | `complete` | complete | Empty; join next declared step |
| `route-closeout-correction` | `blocked` | blocked | Empty; join next declared step |
| `route-closeout-specification-remediation` | `run` | run | `reconcile-closeout-specification` |
| `route-closeout-specification-remediation` | `skip` | skip | Empty; join next declared step |
| `route-closeout-plan-remediation` | `run` | run | `reconcile-closeout-plan` |
| `route-closeout-plan-remediation` | `skip` | skip | Empty; join next declared step |
| `route-closeout-tasks-remediation` | `run` | run | `reconcile-closeout-tasks` |
| `route-closeout-tasks-remediation` | `skip` | skip | Empty; join next declared step |
| `route-closeout-implementation` | `continue` | continue | `implement-closeout-eligible-tasks` |
| `route-closeout-implementation` | `complete` | complete | Empty; join next declared step |
| `route-closeout-implementation` | `blocked` | blocked | Empty; join next declared step |
| `route-roadmap-verification` | `patch-ready` | patch-ready | `approve-roadmap-transition` |
| `route-roadmap-verification` | `already-verified` | already-verified | Empty; join next declared step |
| `route-roadmap-verification` | `blocked` | blocked | Empty; join next declared step |
| `route-roadmap-transition` | `approve-patch` | approved | `apply-approved-roadmap-verification` |
| `route-roadmap-transition` | `default` | not-approved | Empty; join next declared step |
| `route-wiki-maintenance` | `ready` | ready | `wiki-reconciliation-loop` |
| `route-wiki-maintenance` | `blocked` | blocked | Empty; join next declared step |

Loop `closeout-debrief-loop`: assessment before correction; maximum 6 body passes; condition `{{ steps.assess-closeout-debrief.output.state == 'continue' }}`.

Human gate `approve-roadmap-transition`: `approve-patch`, `return-to-workflow`, `defer`.

Loop `wiki-reconciliation-loop`: core work then assessment; maximum 5 body passes; condition `{{ steps.assess-wiki-maintenance.output.state == 'continue' }}`.

### speckit-flow-converge

Source: [workflow.yml](../../workflows/speckit-flow-converge/workflow.yml). Final declared report: `report-convergence-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `convergence-remediation-loop` | Root sequence | do-while | — | — |
| `append-task-remediation` | `convergence-remediation-loop` / loop-body | command | Tasker | speckit.converge |
| `assess-convergence` | `convergence-remediation-loop` / loop-body | prompt | Code Reviewer | — |
| `route-convergence-correction` | `convergence-remediation-loop` / loop-body | switch | — | — |
| `prepare-convergence-flowback` | `route-convergence-correction` / continue | prompt | — | — |
| `route-specification-remediation` | `route-convergence-correction` / continue | switch | — | — |
| `reconcile-convergence-specification` | `route-specification-remediation` / run | command | Specifier | speckit.specify |
| `route-plan-remediation` | `route-convergence-correction` / continue | switch | — | — |
| `reconcile-convergence-plan` | `route-plan-remediation` / run | command | Planner | speckit.plan |
| `route-task-remediation` | `route-convergence-correction` / continue | switch | — | — |
| `reconcile-convergence-tasks` | `route-task-remediation` / run | command | Tasker | speckit.tasks |
| `analyze-remediation-tasks` | `route-convergence-correction` / continue | command | Reviewer | speckit.analyze |
| `assess-remediation-eligibility` | `route-convergence-correction` / continue | prompt | Reviewer | — |
| `route-remediation-implementation` | `route-convergence-correction` / continue | switch | — | — |
| `implement-remediation` | `route-remediation-implementation` / continue | command | Coder | speckit.implement |
| `report-convergence-outcome` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-convergence-correction` | `continue` | continue | `prepare-convergence-flowback` |
| `route-convergence-correction` | `complete` | complete | Empty; join next declared step |
| `route-convergence-correction` | `blocked` | blocked | Empty; join next declared step |
| `route-specification-remediation` | `run` | run | `reconcile-convergence-specification` |
| `route-specification-remediation` | `skip` | skip | Empty; join next declared step |
| `route-plan-remediation` | `run` | run | `reconcile-convergence-plan` |
| `route-plan-remediation` | `skip` | skip | Empty; join next declared step |
| `route-task-remediation` | `run` | run | `reconcile-convergence-tasks` |
| `route-task-remediation` | `skip` | skip | Empty; join next declared step |
| `route-remediation-implementation` | `continue` | continue | `implement-remediation` |
| `route-remediation-implementation` | `complete` | complete | Empty; join next declared step |
| `route-remediation-implementation` | `blocked` | blocked | Empty; join next declared step |

Loop `convergence-remediation-loop`: assessment before correction; maximum 6 body passes; condition `{{ steps.assess-convergence.output.state == 'continue' }}`.

### speckit-flow-implement

Source: [workflow.yml](../../workflows/speckit-flow-implement/workflow.yml). Final declared report: `report-implementation-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `assess-implementation-state` | Root sequence | prompt | Reviewer | — |
| `implementation-continuation-loop` | Root sequence | do-while | — | — |
| `implement-eligible-work` | `implementation-continuation-loop` / loop-body | command | Coder | speckit.implement |
| `assess-implementation-after-pass` | `implementation-continuation-loop` / loop-body | prompt | Code Reviewer | — |
| `report-implementation-outcome` | Root sequence | prompt | — | — |

Loop `implementation-continuation-loop`: core work then assessment; maximum 5 body passes; condition `{{ steps.assess-implementation-after-pass.output.state == 'continue' }}`.

### speckit-flow-plan

Source: [workflow.yml](../../workflows/speckit-flow-plan/workflow.yml). Final declared report: `report-plan-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `plan-output-loop` | Root sequence | do-while | — | — |
| `prepare-plan-request` | `plan-output-loop` / loop-body | prompt | — | — |
| `create-plan` | `plan-output-loop` / loop-body | command | Planner | speckit.plan |
| `verify-plan-output` | `plan-output-loop` / loop-body | prompt | Reviewer | — |
| `report-plan-outcome` | Root sequence | prompt | — | — |

Loop `plan-output-loop`: core work then assessment; maximum 5 body passes; condition `{{ steps.verify-plan-output.output.state == 'continue' }}`.

### speckit-flow-select-feature

Source: [workflow.yml](../../workflows/speckit-flow-select-feature/workflow.yml). Final declared report: `report-feature-selection`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `list-roadmap-options` | Root sequence | prompt | Roadmap Agent | — |
| `select-roadmap-feature` | Root sequence | gate | — | — |
| `route-feature-selection` | Root sequence | switch | — | — |
| `prepare-feature-selection` | `route-feature-selection` / default | prompt | Roadmap Agent | — |
| `route-selection-readiness` | `route-feature-selection` / default | switch | — | — |
| `approve-feature-selection` | `route-selection-readiness` / ready | gate | — | — |
| `route-selection-approval` | `route-selection-readiness` / ready | switch | — | — |
| `apply-selected-roadmap-patch` | `route-selection-approval` / approve | command | — | speckit.flow-roadmap.write |
| `activate-selected-feature` | `route-selection-approval` / approve | prompt | — | — |
| `verify-feature-selection` | `route-selection-approval` / approve | prompt | Reviewer | — |
| `report-feature-selection` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-feature-selection` | `defer` | defer | Empty; join next declared step |
| `route-feature-selection` | `default` | selected | `prepare-feature-selection` |
| `route-selection-readiness` | `ready` | ready | `approve-feature-selection` |
| `route-selection-readiness` | `blocked` | blocked | Empty; join next declared step |
| `route-selection-approval` | `approve` | approved | `apply-selected-roadmap-patch` |
| `route-selection-approval` | `default` | not-approved | Empty; join next declared step |

Human gate `select-roadmap-feature`: `{{ steps.list-roadmap-options.output.selection_options }}`.

Human gate `approve-feature-selection`: `approve`, `amend`, `defer`.

### speckit-flow-specify

Source: [workflow.yml](../../workflows/speckit-flow-specify/workflow.yml). Final declared report: `report-specification-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `inspect-active-feature` | Root sequence | prompt | Roadmap Agent | — |
| `route-active-feature` | Root sequence | switch | — | — |
| `retrieve-governing-context` | `route-active-feature` / ready | command | — | speckit.flow-wiki.query |
| `prepare-specification-request` | `route-active-feature` / ready | prompt | Specifier | — |
| `route-specification-readiness` | `route-active-feature` / ready | switch | — | — |
| `draft-specification` | `route-specification-readiness` / ready | command | Specifier | speckit.specify |
| `assess-created-spec-linkage` | `route-specification-readiness` / ready | prompt | Reviewer | — |
| `route-created-spec-linkage` | `route-specification-readiness` / ready | switch | — | — |
| `review-spec-dir-patch` | `route-created-spec-linkage` / repairable | gate | — | — |
| `route-spec-dir-patch-decision` | `route-created-spec-linkage` / repairable | switch | — | — |
| `apply-approved-spec-dir-patch` | `route-spec-dir-patch-decision` / approve-exact-patch | command | — | speckit.flow-roadmap.write |
| `verify-repaired-spec-linkage` | `route-spec-dir-patch-decision` / approve-exact-patch | prompt | Reviewer | — |
| `prepare-specification-outcome` | Root sequence | prompt | — | — |
| `route-specification-outcome` | Root sequence | switch | — | — |
| `brief-against-roadmap` | `route-specification-outcome` / ready-for-brief | command | Reviewer | speckit.flow-roadmap.brief |
| `report-specification-outcome` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-active-feature` | `ready` | ready | `retrieve-governing-context` |
| `route-active-feature` | `blocked` | blocked | Empty; join next declared step |
| `route-specification-readiness` | `ready` | ready | `draft-specification` |
| `route-specification-readiness` | `blocked` | blocked | Empty; join next declared step |
| `route-created-spec-linkage` | `repairable` | repairable | `review-spec-dir-patch` |
| `route-created-spec-linkage` | `linked` | linked | Empty; join next declared step |
| `route-created-spec-linkage` | `blocked` | blocked | Empty; join next declared step |
| `route-spec-dir-patch-decision` | `approve-exact-patch` | approved | `apply-approved-spec-dir-patch` |
| `route-spec-dir-patch-decision` | `default` | not-approved | Empty; join next declared step |
| `route-specification-outcome` | `ready-for-brief` | ready-for-brief | `brief-against-roadmap` |
| `route-specification-outcome` | `blocked` | blocked | Empty; join next declared step |

Human gate `review-spec-dir-patch`: `approve-exact-patch`, `amend`, `defer`.

### speckit-flow-start-feature

Source: [workflow.yml](../../workflows/speckit-flow-start-feature/workflow.yml). Final declared report: `report-start-feature-deprecation`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `report-start-feature-deprecation` | Root sequence | prompt | — | — |

### speckit-flow-tasks

Source: [workflow.yml](../../workflows/speckit-flow-tasks/workflow.yml). Final declared report: `report-task-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `tasks-output-loop` | Root sequence | do-while | — | — |
| `prepare-task-request` | `tasks-output-loop` / loop-body | prompt | — | — |
| `generate-tasks` | `tasks-output-loop` / loop-body | command | Tasker | speckit.tasks |
| `verify-task-output` | `tasks-output-loop` / loop-body | prompt | Reviewer | — |
| `report-task-outcome` | Root sequence | prompt | — | — |

Loop `tasks-output-loop`: core work then assessment; maximum 5 body passes; condition `{{ steps.verify-task-output.output.state == 'continue' }}`.

### speckit-flow-wiki-lint-update

Source: [workflow.yml](../../workflows/speckit-flow-wiki-lint-update/workflow.yml). Final declared report: `report-wiki-update-outcome`. The adjacent diagram is a presentation of this definition.

| Step ID | Parent / branch | Type | Delegated agent | Command |
|---|---|---|---|---|
| `wiki-lint-update-loop` | Root sequence | do-while | — | — |
| `lint-wiki` | `wiki-lint-update-loop` / loop-body | command | Reviewer | speckit.flow-wiki.lint |
| `assess-wiki-findings` | `wiki-lint-update-loop` / loop-body | prompt | Reviewer | — |
| `route-wiki-source-refresh` | `wiki-lint-update-loop` / loop-body | switch | — | — |
| `prepare-stale-source-refresh` | `route-wiki-source-refresh` / continue | prompt | — | — |
| `refresh-stale-source` | `route-wiki-source-refresh` / continue | command | Wiki Curator | speckit.flow-wiki.ingest |
| `report-wiki-update-outcome` | Root sequence | prompt | — | — |

| Switch | Outcome key | Presentation label | Branch entry |
|---|---|---|---|
| `route-wiki-source-refresh` | `continue` | continue | `prepare-stale-source-refresh` |
| `route-wiki-source-refresh` | `complete` | complete | Empty; join next declared step |
| `route-wiki-source-refresh` | `blocked` | blocked | Empty; join next declared step |

Loop `wiki-lint-update-loop`: assessment before correction; maximum 26 body passes; condition `{{ steps.assess-wiki-findings.output.state == 'continue' }}`.
