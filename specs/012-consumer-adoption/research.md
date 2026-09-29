# Research: Consumer Adoption

The research below resolves the planning alternatives into the documentation-led design the operator reviewed before choosing task generation. Sources are current repository files; no installed payload is treated as editable source. The [specification](spec.md#research-and-review-decisions) records that decision, and the [validation record](validation.md) documents completed implementation and bounded disposable-consumer observations. Real-consumer adoption remains unverified.

## Contents

The sections below provide the planning decisions and review details.

- [Delivery Mechanism](#delivery-mechanism)
- [Review and Conflict Resolution](#review-and-conflict-resolution)
- [Adoption Evidence and Outcomes](#adoption-evidence-and-outcomes)
- [Validation Boundary](#validation-boundary)
- [Review Disposition](#review-disposition)

## Delivery Mechanism

**Decision**: Use a reviewed documentation-led adoption runbook, reusable proposal text, an evidence worksheet, and a copyable manual agent prompt. Expose the runbook immediately after installation and refresh instructions.

**Rationale**: The source checkout is already required by the supported catalog route. The existing catalog installs eight workflow-bound controller skills; a standalone onboarding skill would need new packaging and ownership support. The manual route can inspect project text, present exact patches, and collect evidence without changing the bundle, global templates, or constitutional authority. It is a complete operator-facing procedure, not a passive explanatory page.

| Criterion | Dedicated onboarding skill | Installed preset/template | Reviewed runbook and worksheet |
| --- | --- | --- | --- |
| New install | Convenient explicit skill invocation, but needs delivery support | Can seed text, but installation does not authorize governance | Linked from install instructions; operator invokes procedure |
| Refresh | Skill payload can update independently from project rules after lifecycle support exists | Must distinguish template updates from deliberate local edits | Current runbook compares live state; preserves local text |
| Operator review | Skill can propose exact patches | Requires an additional review process around application | Exact patch and recorded decision are explicit steps |
| Conflict handling | Semantic agent assessment with evidence | Template substitution cannot establish equivalence | Human or instructed agent maps evidence and surfaces conflict |
| Maintainability | Adds standalone skill inventory, provenance, and lifecycle coverage | Adds preset distribution and ownership policy | Reuses reviewed Markdown and existing test tools |
| Manual use | Needs separate fallback maintained in sync | Templates still require manual interpretation | Primary procedure is already manual and reusable by an agent |
| Current support evidence | Controller manifest and catalog restrict skills to eight workflow bindings | Bundle/catalog declare extensions and workflows; no preset delivered | Installation already uses repository docs and source checkout |

**Alternatives considered**: A standalone onboarding skill remains a viable later convenience once its delivery lifecycle is justified. It must not be inserted as a ninth workflow controller with a fabricated workflow binding. A preset or automatically applied template introduces a new delivery surface and cannot decide compatibility of project-owned governance. Plain README snippets alone are insufficient because they do not provide the required review, conflict, and evidence process. An adoption CLI is unnecessary: semantic equivalence still needs review, and no specification requirement calls for automated governance classification.

**Sources**: [installation guide](../../docs/installation.md), [controller manifest](../../controllers/flow-kit/manifest.yml), [catalog implementation](../../tools/catalog.py) (`controller_manifest`, `controller_package_files`, `_owned_target`, `bundle_components`), [bundle manifest](../../bundles/spec-kit-flow/bundle.yml), [catalog tests](../../tests/test_catalog.py).

## Review and Conflict Resolution

**Decision**: Inspect before proposing; map each model rule in both governance and active agent guidance; present minimal exact patches; require an explicit decision for constitutional amendments and material conflicts; recheck the baseline before applying accepted edits. On uncertainty about authority, the integration boundary, or conflicting instructions, ask a concrete question with the affected evidence.

**Rationale**: The specification explicitly accepts equivalent or stricter compatible wording. Text equality and wholesale replacement would both misclassify valid consumer governance. A stronger local rule is compatible only if it still permits the required model behavior; for example, freezing feature artifacts before integration would conflict with the mutable feature unit.

**Alternatives considered**: Exact text matching was rejected by clarification. Automatically weakening a stricter rule or rewriting the entire constitution violates FR-003/FR-004. Invoking the constitution skill without instruction would exceed the operator's chosen scope. A consumer may use its own amendment procedure; record that dependency and leave the result partial or unresolved until that procedure is completed.

**Sources**: [spec clarifications and FR-003–FR-008](spec.md), [constitution principles I, II and IV](../../.specify/memory/constitution.md), [starting proposal](../../docs/merge-bounded-flow-back.md).

## Adoption Evidence and Outcomes

**Decision**: Use a project-owned Markdown review with stable labeled fields, a five-rule evidence matrix, explicit operator decision, project-relative citations, and snapshot digests. Require complete compatible evidence in both active agent guidance and governance plus an established integration boundary for `confirmed`. Capture the guide/template source revision or digest separately from installed component provenance.

**Rationale**: A reviewed worksheet fits the manual interface and keeps evidence inspectable. It separates compatible wording from literal matching, and governance adoption from installation success. Active guidance needs evidence of applicability to the selected project/feature scope, not merely an existing `AGENTS.md` filename. Report limitations if the consumer uses additional nested or conflicting guidance.

**Alternatives considered**: An installation marker or stored boolean cannot establish adoption. A machine-only report schema and validator would add machinery without solving semantic judgment. A README-only result is expressly disallowed by clarification. Full transcripts and host paths are unnecessary and excluded from portable records.

**Sources**: [spec FR-008–FR-012 and SC-004–SC-007](spec.md), [constitution principle V](../../.specify/memory/constitution.md), [catalog lifecycle contract](../013-bundle-workflow-launchers/contracts/lifecycle.md).

## Validation Boundary

**Decision**: Combine structural tests and lifecycle preservation with human-reviewed disposable consumer runs and at least one live-agent sequence covering pre-merge, post-merge, and missing-check behavior. Record actual observed outcomes; do not invent successful adoption from expected fixture results.

**Rationale**: Existing unittest infrastructure and temporary consumer patterns are adequate. Semantic equivalence and whether an agent follows loaded guidance cannot be proven by a no-op process. No new dependency is needed.

**Alternatives considered**: Automated phrase matching alone would not exercise the clarified semantics. Broad compatibility claims exceed the pinned CLI and current Codex integration evidence.

**Sources**: [bundle lifecycle tests](../../tests/test_bundle_lifecycle.py), [mise tool pins](../../mise.toml), [release metadata](../../catalog/release.json), [spec success criteria](spec.md).

## Review Disposition

The three planning questions have reviewed answers: the runbook delivery route, an evidence-first exact-patch conflict procedure, and a project-owned matrix with bounded outcomes. The operator reviewed the documentation-led design and chose to generate tasks for it, as recorded in the specification. There are no unresolved technical placeholders. Any later requested design change flows back through these artifacts. The [validation record](validation.md) documents completed implementation and bounded disposable-consumer and scripted live-agent observations; feature acceptance and real-consumer adoption remain separate. The prior roadmap brief is retained as historical review evidence and is not overwritten by this research.
