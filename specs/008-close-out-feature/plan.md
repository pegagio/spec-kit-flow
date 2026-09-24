# Implementation Plan: Close Out Feature

**Branch**: `feature/time-machine-feature-closeout` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Retrospective specification of `speckit-flow-closeout`.

## Summary

Verify the existing closeout workflow's completion-operation gate, exact roadmap-patch approval, wiki maintenance, and terminal commit-readiness boundary. Add a manual path and a focused disposable missing-operation route test. Keep the reviewed YAML unless a concrete mismatch appears.

## Technical Context

**Language/Version**: Spec Kit workflow YAML schema 1.0; Python 3 for validation
**Primary Dependencies**: Roadmap `debrief` and `write`, Wiki `ingest` and `lint`; Specify `1.0.10.dev0+pegagio.2`; Codex integration
**Storage**: Consumer-owned roadmap, wiki, feature artifacts, and Git state
**Testing**: Disposable bundle lifecycle route plus source inspection
**Target Platform**: Initialized Codex consumer with the pinned bundle
**Project Type**: Versioned workflow source package
**Performance Goals**: No latency target for human-reviewed closeout
**Constraints**: No invented completion operation; no implicit roadmap, Git, or project transition
**Scale/Scope**: One converged feature per invocation

## Constitution Check

Completion, roadmap verification, wiki maintenance, and commit readiness remain separate gates. The approved patch is exact, and feedback or workflow success cannot confer authority. Source stays independently reviewable with manual fallback. No new framework, preset, or Diagram dependency is proposed. Analyze artifacts before implementation and converge afterward.

**Post-design check**: The routing contract preserves these rules. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/008-close-out-feature/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/closeout-routing.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
workflows/speckit-flow-closeout/workflow.yml
workflows/README.md
tests/test_bundle_lifecycle.py
```

**Structure Decision**: Keep the YAML package as the source of routing. Use one no-op native test for the missing-operation stop and inspect the remaining branches; a live completion operation needs separate approval.
