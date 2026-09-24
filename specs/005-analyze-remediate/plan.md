# Implementation Plan: Analyze and Remediate Artifacts

**Branch**: `feature/time-machine-artifact-analysis` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Retrospective specification of `speckit-flow-analyze-remediate`.

## Summary

Verify that analysis is read-only, routine findings follow the smallest artifact flow-back chain and reanalysis, and consequential findings stop for operator authority. Keep the existing YAML package and add focused disposable dispatch coverage plus a manual controller path.

## Technical Context

**Language/Version**: Spec Kit workflow YAML schema 1.0; Python 3 for validation
**Primary Dependencies**: Core `speckit.analyze`, `speckit.specify`, `speckit.plan`, and `speckit.tasks`; Specify `1.0.10.dev0+pegagio.2`; Codex integration
**Storage**: Consumer-owned spec, plan, and tasks
**Testing**: Source route inspection and disposable bundle lifecycle suite
**Target Platform**: Initialized Codex consumer with the pinned bundle
**Project Type**: Versioned workflow source package
**Performance Goals**: No latency target for human-reviewed artifact analysis
**Constraints**: Analysis read-only; routine remediation scoped; constitutional, authority, recovery, and material-scope decisions stop
**Scale/Scope**: One active feature artifact set per invocation

## Constitution Check

The workflow preserves merge-bounded flow-back and keeps consequential decisions with the operator. It reanalyzes after routine correction and never equates analysis with implementation authorization. Source remains independently reviewable with manual fallback. No new framework, preset, or Diagram dependency is proposed. Cross-artifact analysis precedes implementation and convergence follows.

**Post-design check**: The contract and validation guide preserve these boundaries. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/005-analyze-remediate/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/analysis-routing.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
workflows/speckit-flow-analyze-remediate/workflow.yml
workflows/README.md
tests/test_bundle_lifecycle.py
```

**Structure Decision**: Retain one reviewed YAML package for route ordering; core commands own artifact editing and analysis mechanics.
