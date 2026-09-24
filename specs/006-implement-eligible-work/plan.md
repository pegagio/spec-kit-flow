# Implementation Plan: Implement Eligible Work

**Branch**: `feature/time-machine-implementation` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Retrospective specification of `speckit-flow-implement`.

## Summary

Verify that the workflow implements only eligible tasks under the selected agent, returns evidence for human review, and routes discoveries or blockers without implicit continuation. Keep the YAML package independently reviewable and add bounded native dispatch and manual-path coverage.

## Technical Context

**Language/Version**: Spec Kit workflow YAML schema 1.0; Python 3 for validation
**Primary Dependencies**: Core `speckit.implement`, `speckit.analyze`, `speckit.specify`, `speckit.plan`, and `speckit.tasks`; Specify `1.0.10.dev0+pegagio.2`; Codex integration
**Storage**: Consumer-owned feature artifacts and implementation
**Testing**: Source route inspection and disposable bundle lifecycle suite
**Target Platform**: Initialized Codex consumer with the pinned bundle
**Project Type**: Versioned workflow source package
**Performance Goals**: No latency target for human-directed implementation
**Constraints**: Current operator-selected agent and task scope; analysis before implementation; explicit convergence and acceptance gates
**Scale/Scope**: One selected feature's remaining eligible tasks per invocation

## Constitution Check

The workflow respects operator task and agent selection, merge-bounded flow-back, and the separation of execution from convergence, Git integration, and acceptance. It does not grant additional scope on failure. Source remains reviewed and has manual fallback. No new framework, preset, or Diagram dependency is proposed. Analyze before implementation and converge afterward.

**Post-design check**: The contract and validation guide preserve these boundaries. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/006-implement-eligible-work/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/implementation-routing.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
workflows/speckit-flow-implement/workflow.yml
workflows/README.md
tests/test_bundle_lifecycle.py
```

**Structure Decision**: Keep execution mechanics in core Spec Kit and review routing in the existing workflow package.
