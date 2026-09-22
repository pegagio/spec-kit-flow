# Spec Kit Flow Constitution

## Core Principles

### I. Spec Evolution and Merge-Bounded Persistence

The project MUST use the Merge-Bounded Flow-Back Spec Persistence Model.

- **One mutable change set**: Before a feature is merged, its `spec.md`, `plan.md`, `tasks.md`, and implementation MUST be treated as one mutable, reviewable unit.
- **Changes flow back**: Accepted discoveries MAY originate in any artifact, but their consequences MUST be applied throughout the artifact set before work proceeds from the changed direction. A change to intended behavior MUST be reflected in `spec.md`; a change to technical approach MUST be reflected in `plan.md`; and a change to the required work MUST be reflected in `tasks.md`. Lower-level artifacts and implementation MUST NOT silently contradict higher-level intent.
- **Scope requires acceptance**: Flow-back MUST NOT be used to introduce material scope without review. Independently valuable behavior, substantial scope expansion, or work requiring separate acceptance MUST be captured as a separate feature.
- **Consistency gates implementation and merge**: After tasking or consequential artifact reconciliation, the agent MUST run `/speckit.analyze` before starting or resuming implementation. After implementation, the agent MUST use `/speckit.converge` until no gaps remain. Known divergence MUST block implementation or merge until it is reconciled or explicitly removed from scope.
- **Merge freezes history**: Acceptance into the project's designated integration branch is the persistence boundary. After that merge, the feature directory MUST be treated as a semantically immutable historical record. Editorial corrections MAY improve presentation only when they do not alter meaning.
- **Later changes flow forward**: A later requirement or behavioral change MUST be expressed in a new feature directory. The new feature MUST reference any earlier feature that it amends, replaces, or depends on when that relationship is material, and MUST NOT rewrite the earlier feature to describe the new outcome retroactively.

**Rationale:** This model permits requirements and implementation knowledge to converge while a feature is being developed, makes the merged feature a coherent unit of review, and preserves an auditable sequence of accepted changes without rewriting project history.

### II. Human-Directed Authority

The human operator MUST select tasks and agents. Workflows MUST NOT select models, assign or launch agents, or schedule work. Successful commands MUST NOT implicitly verify a roadmap item, integrate Git changes, accept a feature, or grant acceptance in The Diagram. Roadmap patches, constitutional amendments, authority changes, material scope changes, and ambiguous recovery MUST pass an explicit human decision gate. Routine remediation MAY flow back only within the operator-issued controller scope.

**Rationale:** Automation can prepare evidence and bounded changes, but it cannot inherit decisions the operator has not made.

### III. Generic Source and Component Boundaries

This repository MUST own generic workflow source, any separately approved reusable preset, portable consumer feedback capture and reporting, and maintainer-only feedback intake. The `spec-kit-flow` repository and bundle MUST retain that identity; reusable workflow and extension IDs MUST use `speckit-flow-<purpose>`. A bundle MUST compose versioned components and MUST NOT become a second source of their behavior. The Diagram MUST remain a consumer rather than a runtime prerequisite; its registration, canonical work, projections, adapter feedback, and orchestration MUST stay in a separately versioned adapter under its own authority.

**Rationale:** These boundaries keep the generic workbench reusable and each component's behavior traceable to one reviewed source.

### IV. Reviewable Source and Manual Fallback

Changes MUST target reviewed source packages rather than installed copies in a consumer's `.specify/` directory. Workflow packages MUST remain independently reviewable, and planning and task generation MUST remain separate. Every workflow MUST preserve a usable manual-prompt path when native dispatch is unavailable. A new framework, dependency, or build tool MUST have a documented need and explicit approval before adoption.

**Rationale:** Independent review and a manual path let operators inspect and run the process without relying on one dispatch mechanism.

### V. Evidence-Based Validation and Feedback

Changed source definitions and bundle behavior MUST be validated in disposable initialized consumers where applicable. Validation records MUST identify component IDs, versions, source digests, tested CLI version, source coordinates, and observed results. A no-op agent run MUST be described as dispatch evidence, not live-agent validation. Local tests MUST NOT be presented as proof of publication, stock Spec Kit compatibility, or consumer adoption. Consumer feedback MUST remain local evidence; exported reports MUST omit raw transcripts, secrets, and absolute host paths. Maintainer intake MUST validate reports and propose dispositions; neither capture nor intake MAY directly change workflow source, presets, installed components, roadmaps, or runtime authority.

**Rationale:** Provenance and bounded claims make results reproducible while keeping feedback separate from governance and implementation.

## Component and Consumer Constraints

The generic bundle MUST require compatible roadmap and wiki extensions and MUST identify Codex as its initial supported integration until other integrations are validated and accepted. Consumer-owned feedback and unrelated components MUST survive bundle removal. A custom clarification preset or continuation policy MUST require its own approval; the current five-question clarification cap MUST NOT be described as removed by the existing workflows. Diagram-specific behavior MUST NOT enter the generic bundle through a consumer fixture or feedback report.

## Development and Review Gates

Before changing behavior, maintainers MUST reconcile the relevant specification, plan, and tasks under Principle I. Reviews MUST check operator authority, component boundaries, manual fallback, provenance, and the evidence supporting compatibility claims. After changes, maintainers MUST run relevant tests and checks, report any checks that could not run, and document changed user-facing workflows or installation requirements. Consumer feedback accepted for source change MUST re-enter specification, planning, tasking, and implementation through the normal feature flow. Publication and consumer acceptance require their own explicit decisions.

## Governance

This constitution governs project decisions when lower-level guidance conflicts with it. `AGENTS.md` provides operational agent guidance and MUST remain consistent with this constitution. Amendments MUST document the proposed rule change, its rationale, affected workflows or artifacts, and any migration needed for active work; they require explicit human review before acceptance. An amendment MUST NOT retroactively rewrite a merged feature's meaning.

Constitution versions use semantic versioning: MAJOR for incompatible governance changes or principle removal/redefinition, MINOR for a new principle or material expansion, and PATCH for non-semantic clarification. The first ratified constitution is version 1.0.0. Every amendment MUST update the version and last-amended date, and its review MUST verify compliance with the principles and identify any unresolved exceptions. Exceptions MUST be explicit, scoped, and approved by the human operator; an exception does not silently amend this constitution.

**Version**: 1.0.0 | **Ratified**: 2026-09-22 | **Last Amended**: 2026-09-22
