# F014 Authority Decisions

This record captures decisions already made for Feature 014. It does not amend the roadmap or authorize a new workflow scope by itself.

| Decision | State | Evidence |
|---|---|---|
| Constitution II in-workflow bounded correction and reassessment | Approved; Constitution 6.0.0 is the current authority. | Operator approved the exact amendment during the F014 analyze remediation turn on 2026-09-29. |
| Clarify repeated bounded sessions within one invocation | Approved for F014; each substantive answer remains operator-provided and the five-question cap remains per session. | Operator selected clarification answer A on 2026-09-29. |
| Close Out evidence-backed in-place Draft-to-Complete | Approved for F014 when completion evidence is clear; exact roadmap verification remains separately gated. | Operator selected clarification answer A on 2026-09-29. |
| Codex agent configurations | Repository-local files only for F014; any consumer bundle installation mechanism is deferred to a later feature. | Operator selected answer A with later-feature caveat on 2026-09-29. |
| F014 all-eight-workflow review and US1 source scope | Approved; exact roadmap amendment applied. | Operator approved the exact `roadmap-scope-proposal.patch` on 2026-09-29; applied to `.specify/memory/roadmap.md`. |

Verified Feature 007 and Feature 008 history remains unchanged. The accepted authority changes apply prospectively through F014.

## Workflow review and retrospective reconciliation

The operator approved the subsequent workflow source refinements and commits culminating in `c34ea2a`: core-skill continuation/output loops, shared remediation waterfalls, explicit entry diagrams and a project-owned rendering skill, descriptive collapsed transitions, separate Select Feature and Specify with stop-only Start Feature deprecation, simplified Close Out with bounded wiki reconciliation, and standalone Wiki Lint Update.

On 2026-09-30 the operator explicitly directed retrospective reconciliation of these accepted changes across the artifact set. Source work was committed directly to `develop` before complete artifact reconciliation. This repair records that sequencing divergence and the operator-directed resolution; it does not redefine the constitution's integration/acceptance boundary or rewrite verified feature history. F014 remains Draft/in-progress with unfinished delivery. Later behavioral changes to accepted features must use a new feature directory.

The operator approved the exact F014 [roadmap scope repair](roadmap-reconciliation.patch) on 2026-09-30 and directed its application. The patch was applied verbatim to `.specify/memory/roadmap.md`; only the F014 scope record changed, with status remaining in-progress and no acceptance transition.
