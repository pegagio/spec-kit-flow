<!--
SYNC IMPACT REPORT
==================
Version change: 1.0.0 → 1.1.0
Bump rationale: MINOR — add one planned feature for consumer adoption of the Merge-Bounded Flow-Back Spec Persistence Model.

Changes this revision:
  - Added spec 012 as planned without changing verified entries 001–011.
  - Replaced the no-planned-features statement with the current planned feature and recorded its research questions.

Specs affected: 012
Open questions added/resolved: added mechanism selection, existing-governance handling, and adoption evidence; none resolved.

Notes: The operator approved the feature amendment on 2026-09-26 and clarified that proposed guidance may be refined. The operator then specified that agents should recommend the FlowKit consistency workflows and flag skipped checks, not invoke workflows or core commands independently. The proposal document is docs/merge-bounded-flow-back.md; it does not choose a delivery mechanism. The earlier verification decision for 001–011 remains intact.
-->

# Spec Kit Flow — Spec Roadmap

This living roadmap records the project's completed specifications and leaves room for future features. It is not a commitment to new scope or sequence. The [constitution](constitution.md) governs this ledger; each entry points to its feature specification. The operator designated every current spec as verified on 2026-09-26.

## Contents

- [Vision and end states](#vision-and-end-states)
- [Constraints and decisions](#constraints-and-decisions)
- [Planned specs](#planned-specs)
- [Open questions](#open-questions)
- [Cross-cutting notes](#cross-cutting-notes)

Status legend: **undecided** · **needs-info** · **planned** · **specced** · **in-progress** · **implemented** · **verified** · **deferred** · **abandoned**.

## Vision and end states

The constitution establishes the durable project direction; the completed specs define the current delivery boundary.

- Provide a reusable, human-directed Spec-Driven Development workbench whose feature artifacts stay consistent through merge-bounded flow-back and explicit review gates.
- Keep generic workflows, independently versioned extensions, portable consumer feedback, maintainer intake, and the bundle catalog traceable to reviewed source and bounded validation evidence.
- Preserve manual workflow paths and human control over agent selection, material scope, roadmap verification, Git integration, publication, and acceptance.
- Treat additional features as future roadmap amendments. Feature 012 is the sole current planned feature.

## Constraints and decisions

These cross-cutting constraints come from the [constitution](constitution.md); they do not create new feature scope.

- **C-01 — Merge-bounded persistence**: Before merge, accepted discoveries flow through the current spec, plan, tasks, and implementation; after merge, behavioral changes move into a new feature directory. This keeps reviewable intent and historical records coherent.
- **C-02 — Human-directed authority**: The operator chooses tasks and agents and explicitly approves consequential roadmap, scope, integration, and acceptance decisions. Command success cannot confer those decisions.
- **C-03 — Generic component boundaries**: This repository owns generic workflow and feedback source; the bundle composes versioned components. The Diagram remains a consumer, with adapter behavior governed separately.
- **C-04 — Reviewable source and fallback**: Changes target source packages, planning and task generation remain distinct, and each workflow retains a manual-prompt path. New build tools or dependencies require a documented need and approval.
- **C-05 — Bounded validation and feedback**: Disposable consumer tests record component and CLI provenance without claiming publication, stock compatibility, or live-agent quality. Feedback capture and intake provide evidence and proposals, not direct source or authority changes.

## Planned Specs

Entries 001–011 record all current feature directories as verified history. Feature 012 is planned and has no spec directory yet. Dependencies describe delivery prerequisites between these specs, not the order in which an operator must run workflow phases.

### 001 — Start Eligible Feature  [status: verified]

- **Description**: Guide an operator from an eligible roadmap item through an approved patch, cited context, a specification draft, and roadmap brief.
- **Outcome**: An eligible start produces a reviewed feature draft and explicit next choice; ambiguous eligibility, dependencies, or context stop without a state change.
- **Scope (in)**: Eligibility and dependency checks, exact patch approval, governing-context coverage, specification drafting, brief, and manual fallback.
- **Scope (out)**: Automatic clarification, planning, agent dispatch, Git integration, acceptance, or Diagram runtime behavior.
- **Depends on**: none.
- **Governed by**: C-02, C-03, C-04.
- **Spec dir**: `specs/001-start-eligible-feature/`.

### 002 — Clarify Specification  [status: verified]

- **Description**: Run one bounded clarification session for an operator-selected active specification and route its result.
- **Outcome**: Accepted answers enter the spec incrementally, unresolved ambiguity remains visible, and the operator chooses continuation, planning readiness, or deferral.
- **Scope (in)**: One session, the current five-question boundary, result review, explicit routing, and manual fallback.
- **Scope (out)**: Automatically declaring readiness, launching planning, or introducing an unapproved continuation preset.
- **Depends on**: none.
- **Governed by**: C-02, C-04.
- **Spec dir**: `specs/002-clarify-specification/`.

### 003 — Plan Implementation  [status: verified]

- **Description**: Check planning readiness and create reviewable technical artifacts for a clarified feature.
- **Outcome**: A plan, research, data model, contracts, and quickstart are offered for review only after an explicit readiness decision.
- **Scope (in)**: Reviewed-spec confirmation, plan/return/defer gate, technical planning, and manual fallback.
- **Scope (out)**: Resolving product ambiguity through design assumptions or automatically generating tasks.
- **Depends on**: none.
- **Governed by**: C-02, C-04.
- **Spec dir**: `specs/003-plan-implementation/`.

### 004 — Generate Implementation Tasks  [status: verified]

- **Description**: Generate dependency-ordered tasks from reviewed design artifacts as a separate workflow phase.
- **Outcome**: The operator reviews task coverage and unexpected human work before choosing analysis, replanning, amendment, or deferral.
- **Scope (in)**: Task proposal generation, coverage review, explicit routing, and manual fallback.
- **Scope (out)**: Automatic implementation, agent selection, Git integration, or bypassing analysis.
- **Depends on**: none.
- **Governed by**: C-02, C-04.
- **Spec dir**: `specs/004-generate-tasks/`.

### 005 — Analyze and Remediate Artifacts  [status: verified]

- **Description**: Analyze spec, plan, and task consistency before implementation and route bounded corrections through affected artifacts.
- **Outcome**: Routine findings receive dependent-artifact reconciliation and another read-only analysis; consequential or blocked outcomes stop for a separate decision.
- **Scope (in)**: Analysis disposition, scoped spec/plan/task remediation, reanalysis, and manual fallback.
- **Scope (out)**: Unapproved constitutional, authority, material-scope, or ambiguous-recovery changes and automatic implementation.
- **Depends on**: none.
- **Governed by**: C-01, C-02, C-04.
- **Spec dir**: `specs/005-analyze-remediate/`.

### 006 — Implement Eligible Work  [status: verified]

- **Description**: Implement analyzed, eligible tasks within the operator-selected feature, task, and agent boundary.
- **Outcome**: Execution evidence is reviewed, discoveries return through the relevant artifacts and analysis, and blockers stop without expanding scope.
- **Scope (in)**: Eligible task execution, prerequisite checks, return routes, blocker handling, and manual fallback.
- **Scope (out)**: Automatic agent launch, implementation retries after artifact changes, roadmap verification, publication, or acceptance.
- **Depends on**: none.
- **Governed by**: C-01, C-02, C-04.
- **Spec dir**: `specs/006-implement-eligible-work/`.

### 007 — Converge Feature  [status: verified]

- **Description**: Compare implementation with current feature artifacts and route bounded remaining work to resolution.
- **Outcome**: Clean convergence stops for separate closeout; remediation tasks pass analysis before another implementation and convergence run.
- **Scope (in)**: Gap assessment, clean/remediation/blocked disposition, task analysis, and manual fallback.
- **Scope (out)**: Automatic closeout, Git integration, publication, or acceptance.
- **Depends on**: none.
- **Governed by**: C-01, C-02, C-04.
- **Spec dir**: `specs/007-converge-feature/`.

### 008 — Close Out Feature  [status: verified]

- **Description**: Guide explicit feature-completion review, roadmap verification, curated wiki maintenance, and commit-readiness review.
- **Outcome**: A separately approved completion operation and exact roadmap patch precede wiki ingestion and lint; commit readiness remains an operator decision.
- **Scope (in)**: Completion gate, roadmap debrief and patch review, selected wiki sources, lint, and manual fallback.
- **Scope (out)**: Inventing a completion operation, automatic commit or Git integration, or implied project acceptance.
- **Depends on**: none.
- **Governed by**: C-01, C-02, C-05.
- **Spec dir**: `specs/008-close-out-feature/`.

### 009 — Consumer Feedback  [status: verified]

- **Description**: Capture local workflow observations and export portable reports without changing source or authority.
- **Outcome**: Valid observations become append-only local evidence and deterministic digest-bearing JSON and Markdown reports; malformed or sensitive input is rejected.
- **Scope (in)**: Provenance validation, duplicate rejection, portability checks, offline capture and export.
- **Scope (out)**: Automatic report transfer, maintainer disposition, source changes, or roadmap mutation.
- **Depends on**: none.
- **Governed by**: C-02, C-03, C-05.
- **Spec dir**: `specs/009-consumer-feedback/`.

### 010 — Maintainer Feedback Intake  [status: verified]

- **Description**: Validate transferred consumer reports and record bounded maintainer disposition proposals.
- **Outcome**: Valid reports create a canonical inbox copy and triage proposal; duplicates link to earlier intake, while invalid input creates no record.
- **Scope (in)**: Schema, digest, provenance, evidence, and redaction checks; safe triage and duplicate handling.
- **Scope (out)**: Packaging intake into the consumer bundle or directly editing workflows, roadmaps, installed components, Git state, or agent policy.
- **Depends on**: 009.
- **Governed by**: C-02, C-03, C-05.
- **Spec dir**: `specs/010-maintainer-intake/`.

### 011 — Bundle Catalog and Lifecycle  [status: verified]

- **Description**: Package pinned workflow and extension components and guide verified installation, refresh, and removal in consumer projects.
- **Outcome**: The local catalog records reviewed provenance and checksums, and disposable lifecycle validation covers installation through removal without deleting consumer-owned evidence.
- **Scope (in)**: Bundle pins, deterministic release assets, catalog verification, tested CLI coordinates, lifecycle tests, and installation documentation.
- **Scope (out)**: Remote publication, stock Spec Kit compatibility claims, live-agent quality claims, or automatic consumer adoption.
- **Depends on**: 001, 002, 003, 004, 005, 006, 007, 008, 009, 010.
- **Governed by**: C-02, C-03, C-04, C-05.
- **Spec dir**: `specs/011-bundle-catalog/`.

### 012 — Consumer Adoption of Merge-Bounded Flow-Back  [status: planned]

- **Description**: Investigate how the FlowKit bundle should bring the Merge-Bounded Flow-Back Spec Persistence Model into consumer projects, then implement the selected mechanism.
- **Outcome**: New and refreshed bundle consumers have a validated, reviewable path to use the model in project guidance and governance; adoption is confirmed from project state rather than assumed from installation.
- **Scope (in)**: Compare an onboarding skill, a preset or template approach, and other supported mechanisms; review and refine the proposed README and constitution language as needed; implement the chosen path, conflict handling, and disposable-consumer validation.
- **Scope (out)**: Silent replacement of existing project governance, retroactive edits to merged feature history, a separate scope-creep policy, Diagram-specific behavior, and changes to Specify's global base template.
- **Depends on**: 011.
- **Governed by**: C-01, C-02, C-03, C-04, C-05.
- **Notes**: The operator set the adoption goal and requested investigation followed by implementation. Agents should recommend the operator-invoked FlowKit consistency workflows and flag missing checks rather than independently launch those workflows or their core commands. `docs/merge-bounded-flow-back.md` is a starting proposal, not required verbatim text; the delivery mechanism remains subject to research and review.

## Open Questions

Feature 012 must answer these questions before its implementation path is settled:

- Which supported mechanism should deliver and maintain the guidance: an onboarding skill, a preset or template approach, or another reviewed option?
- How should new installations and refreshes handle an existing or conflicting project constitution without silently replacing governance?
- What project-state evidence confirms that the model was adopted, and how should a declined or incomplete adoption be reported?

## Cross-Cutting Notes

The workflow run order is start-feature, optional clarification, planning, task generation, analysis, implementation, convergence, and closeout. That operational route is distinct from the delivery dependencies recorded above. The maintainer intake component remains outside the consumer bundle.

The operator designated all eleven entries verified on 2026-09-26. Their `spec.md` headers still say `Draft`; this roadmap records the operator's lifecycle decision without rewriting historical feature artifacts. No configured ADR or PRD evidence was available for this creation.

**Version**: 1.1.0 | **Ratified**: 2026-09-26 | **Last Amended**: 2026-09-26
