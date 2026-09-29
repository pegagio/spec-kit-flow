# Implementation Plan: Consumer Adoption of Merge-Bounded Flow-Back

**Branch**: `develop` (active feature identity: `012-consumer-adoption`) | **Date**: 2026-09-28 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/012-consumer-adoption/spec.md`.

## Contents

The sections below provide the planning decisions and review details.

- [Summary](#summary)
- [Technical Context](#technical-context)
- [Constitution Check](#constitution-check)
- [Project Structure](#project-structure)
- [Implementation Approach](#implementation-approach)
- [Validation and Coverage](#validation-and-coverage)
- [Complexity Tracking](#complexity-tracking)

## Summary

Provide a reviewed adoption runbook, reusable proposal text, and an evidence worksheet for new and refreshed consumers. Link the runbook from installation and refresh instructions. An operator or explicitly instructed agent inspects the consumer, proposes exact changes, obtains the required decisions, applies only accepted changes, and checks the resulting active agent guidance and governance against every model rule. No installation operation declares adoption.

The operator reviewed the documentation-led onboarding design with a copyable manual agent prompt and chose to generate tasks for it. [Research](research.md) compares this selected route with a dedicated onboarding skill and a preset/template installation approach. The [specification's recorded decisions](spec.md#research-and-review-decisions) establish the reviewed direction; the [validation record](validation.md) documents completed implementation and bounded disposable-consumer observations. The existing roadmap brief records the earlier open questions and remains historical review evidence.

## Technical Context

**Language/Version**: Markdown artifacts; existing Python 3.11 test infrastructure for document contract and disposable-consumer checks.

**Primary Dependencies**: Existing catalog tools and Specify CLI pinned by `mise.toml` (`1.0.10.dev0+pegagio.2` at planning); no new dependencies, framework, preset, or workflow.

**Storage**: Reviewed source documents in this repository; consumer-owned guidance, constitution, and a project-relative Markdown adoption review selected by the operator. Adoption records are outside package ownership.

**Testing**: Python `unittest` for structural/document coverage and lifecycle preservation; controlled manual and live-agent scenarios for semantic equivalence, conflict decisions, and agent behavior. Automated text matching cannot establish semantic adoption.

**Target Platform**: Current Codex consumer integration and the existing pinned Specify fork; manual review remains usable without native workflow dispatch. Stock Spec Kit compatibility remains unverified.

**Project Type**: Documentation and governance onboarding capability within the existing workbench.

**Performance Goals**: One bounded review of the selected consumer's governing files; no background scanning or performance SLA.

**Constraints**: Exact proposed patches before constitutional decisions; no changes on decline or deferral; inspect both active guidance and governance; preserve local edits across refresh/removal; no absolute host paths in portable evidence; no automatic workflow invocation.

**Scale/Scope**: One selected consumer per review, new-install and refresh entry points, five stable model-rule groups, four adoption states plus a separate operator decision field.

## Constitution Check

The pre-research gate passes: the design remains inside FR-001–FR-012, adds no new authority or dependency, and retains explicit decisions. The post-design gate also passes for the operator-reviewed design and this consistency remediation.

| Principle | Design evidence and constraint |
| --- | --- |
| I. Merge-bounded persistence | Proposal text covers the mutable feature unit, flow-back, consistency checks, integration boundary, and later-feature history. Changes remain in Feature 012; earlier feature records stay intact. |
| II. Human-directed authority | Runbook invocation authorizes inspection and proposal drafting. Constitutional amendment and material conflict resolution require a recorded decision on the exact patch; uncertain project rules return a substantive question. No subsequent workflow is launched. |
| III. Generic boundaries | Generic documentation and templates remain in this repository. No Diagram dependency, bundle runtime authority, new extension, or ninth controller workflow is introduced. |
| IV. Reviewable source and fallback | Edit source documentation, not installed payloads. The manual procedure is the primary interface; a copyable agent prompt follows the same contract. Planning and task generation stay separate. |
| V. Bounded evidence | Fixture records identify versions, digests, CLI, source coordinates, decisions, and observed outcomes. Structural tests, semantic review, live agent behavior, publication, and adoption outside fixtures are distinct claims. |

No constitutional exception is required. The operator reviewed the design direction for task generation, and the [validation record](validation.md) documents completed implementation and bounded disposable-consumer observations. Feature acceptance and real-consumer adoption remain separate.

## Project Structure

The feature artifacts describe the selected design and its validation boundary.

```text
specs/012-consumer-adoption/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/adoption.md
├── quickstart.md
└── validation.md                 # Implementation evidence, created later
```

The implementation should use the existing documentation and test layout.

```text
docs/
├── consumer-adoption.md          # New runbook and copyable agent prompt
├── templates/adoption-review.md  # New evidence worksheet
├── merge-bounded-flow-back.md    # Refined reusable README, agent, governance text
└── installation.md               # Install/refresh links to explicit adoption route
README.md                        # Adoption entry point and bounded claims
tests/
├── test_consumer_adoption.py     # New document/fixture contract checks
├── test_consumer_adoption_lifecycle.py # New refresh/removal preservation checks
├── test_consumer_adoption_guidance.py  # New guidance contract checks
├── consumer-fixtures/adoption/   # New synthetic governance/guidance variants
└── test_catalog.py              # Preservation regression where applicable
```

**Structure Decision**: Keep procedure, proposal language, and report template reviewable as source documents. Consumers obtain them through the same source checkout required by catalog installation. Refresh points to the current reviewed runbook but never copies it over consumer-owned rules. Catalog package contents and the eight controller bindings need no change for this design.

## Implementation Approach

Implementation has three increments: create the runbook and evidence contract with reusable model guidance; link installation/refresh/removal documentation and add synthetic scenario fixtures; execute automated preservation checks and manual/live-agent consumer validation, recording provenance and limitations. Task generation is a separate invocation.

The runbook first establishes the actual designated integration branch, governing document locations, and which agent guidance is loaded for the selected project and feature scope. Missing or conflicting evidence stays visible. It builds the rule-by-rule matrix in [the data model](data-model.md), accepts semantically equivalent or stricter compatible rules, and produces minimal exact patches for missing rules. README text may explain the model but cannot satisfy active agent guidance evidence by itself.

The operator reviews constitutional changes and material conflicts before mutation. A changed baseline invalidates the proposed patch and requires renewed review of the changed proposal. After accepted edits, reread the affected files and rebuild the evidence matrix. Report the observed adoption state with a separate decision value, so a deferred decision and incomplete state are represented without inventing a fifth adoption status.

Every report includes source-relative evidence and review limitations. A prior report is a record of its observed snapshot; refresh requires current inspection and cannot carry forward a previous `confirmed` result merely because the earlier report exists. Removal preserves the project-owned result and adopted rules.

## Validation and Coverage

The [quickstart](quickstart.md) defines executable setup and validation cases. Automated tests validate required sections/rules, fixture completeness, and byte preservation across catalog refresh/removal. Semantic equivalence and live behavior require observed review; passing structural checks never promotes a fixture to confirmed adoption.

| Requirements | Planned evidence |
| --- | --- |
| FR-001, SC-006 | Candidate comparison and reviewed delivery decision in research/plan |
| FR-002, FR-010, FR-012 | New-install/refresh entry points, usable manual prompt, documented outcome and evidence limits |
| FR-003–FR-005, SC-001–SC-003 | Exact-patch approval, conflict, decline, deferral, and baseline-change cases |
| FR-006–FR-008, SC-004–SC-005 | Five-rule matrix in active guidance and governance; equivalent/stricter, partial, and live behavior cases |
| FR-009 | Preservation hashes before/after install, refresh, and removal |
| FR-011, SC-007 | Disposable initialized consumers and provenance-bearing validation records |

## Complexity Tracking

No constitutional violations or new runtime abstraction are proposed. The operator-reviewed design accepts the tradeoff of manual discovery and semantic review rather than skill-picker convenience. No new design decision is introduced by this remediation.
