# Feature Specification: Consumer Adoption of Merge-Bounded Flow-Back

**Feature Branch**: `develop` (no feature branch created by this specification)

**Created**: 2026-09-28

**Status**: Complete

**Input**: User description: "Create the specification for the approved roadmap feature: Start the next eligible roadmap feature: 012 Consumer Adoption of Merge-Bounded Flow-Back. Preserve the approved outcome, scope, dependencies, and cited governing context."

## Clarifications

### Session 2026-09-28

- Q: If a consumer’s existing constitution uses different wording or adds stricter rules while still allowing the merge-bounded model, should the adoption path treat it as compatible without a constitutional amendment? → A: Yes. Equivalent or stricter rules count as compatible when inspectable project-state evidence satisfies each required model rule.
- Q: For confirmed adoption, must the model’s operating rules appear in guidance that agents actually read during feature work, or is a project document such as a README sufficient? → A: Require operating rules in active agent guidance and compatible project governance.

## User Scenarios & Testing

### User Story 1 - Adopt the Model in a New Consumer (Priority: P1)

A project operator installing FlowKit can review how the Merge-Bounded Flow-Back Spec Persistence Model would appear in the project's guidance and governance, decide whether to adopt it, and verify the resulting project state.

**Why this priority**: Installing a bundle alone does not establish a project's rules. The operator needs a deliberate adoption path before using the model as project authority.

**Independent Test**: In a disposable initialized consumer with no conflicting governance, follow the documented new-install path, inspect the proposed and resulting project guidance, and verify that adoption is reported only after project state reflects the operator's decision.

**Acceptance Scenarios**:

1. **Given** a new consumer with no model guidance, **when** the operator starts the adoption path, **then** the operator can review proposed guidance and governance changes before accepting them.
2. **Given** the operator accepts adoption, **when** the path completes, **then** project guidance and governance express the accepted model consistently and the result identifies project-state evidence for adoption.
3. **Given** the operator declines adoption, **when** the path ends, **then** project governance remains unchanged and the result does not report adoption.

### User Story 2 - Refresh Without Overwriting Governance (Priority: P2)

An operator refreshing an existing consumer can compare current project rules with model guidance and resolve differences explicitly while preserving project-owned decisions.

**Why this priority**: A refresh must not silently change the project's constitution or mistake installed component state for governance acceptance.

**Independent Test**: In disposable consumers with matching, absent, and conflicting governance, refresh FlowKit and follow the adoption path; verify that each outcome is accurately reported and existing rules remain intact until an authorized change is accepted.

**Acceptance Scenarios**:

1. **Given** existing governance already expresses the model, **when** the operator checks adoption after refresh, **then** the result identifies the matching project state without duplicating or silently rewriting governance.
2. **Given** existing governance differs in wording or adds stricter compatible rules, **when** the operator checks adoption after refresh, **then** the result identifies evidence for each required model rule without requiring a constitutional amendment.
3. **Given** existing governance conflicts with proposed model language, **when** the operator refreshes, **then** the conflict and affected project text are presented for an explicit decision before any governance change.
4. **Given** the operator leaves a conflict unresolved, **when** the path ends, **then** the project is reported as unresolved or incomplete rather than adopted.

### User Story 3 - Use the Model During Feature Work (Priority: P3)

An agent working in a consumer project follows adopted guidance: it reconciles accepted discoveries through the current feature artifacts before merge, treats merged feature artifacts as history, and points the operator to appropriate consistency workflows when checks are missing.

**Why this priority**: Adoption has practical value only when project guidance leads to consistent, operator-directed feature work.

**Independent Test**: In a disposable adopted consumer, present pre-merge and post-merge changes plus a missing consistency check; inspect whether guidance directs the expected artifact treatment and recommendation without launching a workflow independently.

**Acceptance Scenarios**:

1. **Given** an unmerged feature has an accepted behavior change, **when** an agent follows adopted guidance, **then** it updates the current feature's intended behavior and reconciles dependent planning, tasks, and implementation before proceeding from the changed direction.
2. **Given** a feature has entered the designated integration branch, **when** a later behavioral change is proposed, **then** guidance directs it to a new feature and preserves the merged feature's meaning.
3. **Given** an applicable consistency check has not run, **when** an agent reports its work, **then** it flags the missing check and recommends the relevant operator-invoked FlowKit workflow without launching that workflow or its underlying command.

### Edge Cases

- A constitution uses different terminology or stricter rules; the path recognizes compatible rules when each required model rule has inspectable evidence and surfaces any material conflict without declaring the existing rule invalid on its own.
- A consumer has only README guidance, only constitutional language, or wording that partially matches; adoption remains partial unless active agent guidance and compatible project governance both contain the required rules.
- The operator accepts only some changes or defers a constitutional amendment; the result identifies what remains incomplete.
- A refresh changes recommended wording after deliberate local edits; local text remains until the operator resolves the difference.
- A project's designated integration branch differs from a typical branch name; guidance refers to the project's actual boundary.
- Bundle removal preserves project-owned governance and feature history.

## Requirements

### Functional Requirements

- **FR-001**: The feature MUST compare an onboarding skill, a preset or template approach, and any other materially viable supported candidate before selecting a delivery mechanism. The comparison MUST cover new installation, refresh, operator review, conflict handling, maintainability, and manual use.
- **FR-002**: The selected mechanism MUST provide a documented, reviewable path for new and refreshed consumers to consider the model in project guidance and governance.
- **FR-003**: The path MUST present proposed changes to project-owned guidance and governance for operator review and MUST require an explicit decision before applying a constitutional amendment or resolving a material conflict.
- **FR-004**: The path MUST NOT silently replace, weaken, or reinterpret existing project governance. An unresolved conflict MUST prevent a confirmed-adoption result.
- **FR-005**: The operator MUST be able to decline or defer adoption without changing project governance, and the result MUST distinguish that outcome from confirmed adoption.
- **FR-006**: Proposed guidance MUST express pre-merge reconciliation of `spec.md`, `plan.md`, `tasks.md`, and implementation; the designated integration merge boundary; and new-feature treatment for later behavioral change. The starting proposal in `docs/merge-bounded-flow-back.md` MAY be refined.
- **FR-007**: Proposed agent guidance MUST direct agents to flag missing checks and unresolved divergence, recommend applicable FlowKit consistency workflows, and leave invocation of those workflows and underlying commands to the operator.
- **FR-008**: The path MUST determine and report adoption from inspectable project state, distinguishing confirmed, partial, declined, and unresolved outcomes. Existing constitutional wording that is equivalent to or stricter than the model MUST count as compatible when project-state evidence satisfies each required model rule; exact proposed wording MUST NOT be required. Confirmed adoption MUST require the operating rules in active agent guidance and compatible project governance; a README alone MUST NOT suffice as agent guidance. Bundle installation or command success alone MUST NOT count as confirmed adoption.
- **FR-009**: The path MUST preserve merged feature history, project-owned guidance, unrelated components, and consumer-owned evidence during installation, refresh, and removal.
- **FR-010**: The mechanism MUST remain generic to FlowKit consumers, use reviewed source, and preserve a usable manual path.
- **FR-011**: Validation MUST exercise new installation, refresh, existing governance conflicts, decline or deferral, partial state, and confirmed adoption in disposable initialized consumers, recording component and tested CLI provenance and observed outcomes.
- **FR-012**: Documentation MUST explain the supported adoption route, decision points, conflict outcomes, project-state confirmation, evidence limits, and the distinction between installing FlowKit and adopting project governance.

### Key Entities

- **Consumer project**: An initialized project with its own guidance, constitution, feature history, and installed FlowKit components.
- **Adoption proposal**: Reviewable model guidance and governance changes offered to the operator; wording may be refined from the starting proposal.
- **Governance conflict**: A material difference between proposed model rules and an existing project rule requiring an explicit operator decision.
- **Adoption outcome**: The reported state of confirmed, partial, declined, or unresolved adoption together with inspectable project-state evidence.

## Success Criteria

### Measurable Outcomes

- **SC-001**: In disposable new and refreshed consumers, the operator can inspect all proposed project guidance and governance changes before accepting any constitutional amendment.
- **SC-002**: In each tested consumer with conflicting governance, zero conflicting constitutional changes occur without an explicit operator decision, and the conflict remains visible until resolved.
- **SC-003**: In each tested declined, deferred, or partial adoption, the result does not claim confirmed adoption and identifies the remaining or rejected decision.
- **SC-004**: In each tested confirmed adoption, a reviewer can identify project-state evidence for both active agent guidance and compatible governance and distinguish it from bundle installation evidence.
- **SC-005**: In pre-merge, post-merge, and missing-check scenarios, adopted guidance yields the expected artifact treatment or operator recommendation without an agent independently invoking a FlowKit workflow.
- **SC-006**: A reviewer can compare at least the onboarding skill and preset or template candidates against the same documented criteria and trace the selected mechanism to a recorded decision before implementation.
- **SC-007**: Disposable-consumer validation records tested component identities, versions, source digests, CLI version, source coordinates, and observed outcomes, without claiming remote publication or adoption outside those consumers.

## Assumptions

- Feature 012 depends on verified Feature 011. Feature 013 was delivered independently and does not settle Feature 012's adoption mechanism.
- Governing decisions are C-01 through C-05 in the roadmap and constitution: merge-bounded persistence, human-directed authority, generic component boundaries, reviewable source and fallback, and bounded validation.
- `docs/merge-bounded-flow-back.md` is a starting proposal, not text consumers must adopt verbatim.
- Adoption is a project-governance decision separate from bundle installation, workflow invocation, roadmap verification, Git integration, and feature acceptance.
- This feature does not establish a separate scope-creep policy, change Specify's global base template, add Diagram-specific behavior, or rewrite merged feature history.

## Research and Review Decisions

The three roadmap questions were resolved in the [research](research.md), [plan](plan.md), and [adoption contract](contracts/adoption.md). After reviewing the proposed documentation-led design, the operator chose to generate tasks for it. That decision accepts the design direction for task generation; it does not establish that implementation or disposable-consumer and live-agent validation have occurred.

1. **Delivery mechanism**: Use a reviewed adoption runbook, reusable proposal text, an evidence worksheet, and a copyable manual agent prompt, linked from installation and refresh instructions. The [delivery comparison](research.md#delivery-mechanism) explains why this route was selected over a dedicated onboarding skill or installed preset/template.
2. **Review and conflict resolution**: Inspect existing guidance and governance first, map each model rule to evidence, present minimal exact patches, and require an explicit operator decision for constitutional amendments or material conflicts. Recheck the baseline before applying accepted edits. The [research decision](research.md#review-and-conflict-resolution) and [review contract](contracts/adoption.md#review-and-mutation-contract) define the boundary.
3. **Adoption evidence and outcomes**: Use a project-owned review with evidence for every rule in both active agent guidance and compatible governance, an established integration boundary, project-relative citations, and a separate operator decision. Report confirmed, partial, declined, or unresolved state according to the observed evidence. The [research decision](research.md#adoption-evidence-and-outcomes) and [output contract](contracts/adoption.md#output-contract) describe the proposed record; the result must be established during validation, not inferred from task generation.

## Governing Context and Coverage

- [Roadmap Feature 012](../../.specify/memory/roadmap.md) defines the approved outcome, scope, exclusions, dependency on Feature 011, and open questions.
- [Artifact flow-back and convergence](../../wiki/pages/artifact-flow-back-and-convergence.md) (S010–S012, S017) supports pre-merge reconciliation, post-merge historical treatment, and operator-invoked consistency checks.
- [Project authority and review gates](../../wiki/pages/project-authority-and-review-gates.md) (S001–S003, S017) supports operator control of workflow and scope, constitutional gates, and bounded evidence claims.
- [Bundle and workflow model](../../wiki/pages/bundle-and-workflow-model.md) (S001, S002, S016–S019) supports generic component boundaries and the existing bundle and controller delivery split.
- [Feature start contract](../../wiki/pages/feature-start-contract.md) (S006) requires the approved outcome and scope to survive specification drafting.

Wiki coverage for Feature 012 is **Partial**. The wiki sources did not settle the adoption mechanism, conflict-resolution path, or adoption-evidence format. The linked Feature 012 research and contract document those decisions, and the [validation record](validation.md) documents completed implementation and bounded disposable-consumer observations. Real-consumer adoption and feature acceptance remain separate.
