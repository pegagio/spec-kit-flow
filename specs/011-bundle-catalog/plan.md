# Implementation Plan: Bundle Catalog and Lifecycle

**Branch**: `feature/time-machine-bundle-catalog` | **Date**: 2026-09-24 | **Spec**: [spec.md](spec.md)

**Input**: Existing local release catalog and committed `flow-feedback` `0.2.1` source.

## Summary

Bump the bundle to `0.3.1` and its feedback pin to `0.2.1`, then run the existing release builder against clean tagged Roadmap and Wiki checkouts. Update the catalog integrity test and installation/status docs. Verify generated archive contents and metadata, run focused suites, and exercise install and refresh in a disposable consumer.

## Technical Context

**Language/Version**: Bundle YAML schema 1.0; Python 3.11; Specify `1.0.10.dev0+pegagio.2`
**Primary Dependencies**: Clean Roadmap `v0.2.1`, Wiki `v2.0.1`, committed feedback `0.2.1`, Codex integration
**Storage**: `catalog/release.json`, deterministic archives, consumer bundle records
**Testing**: Catalog unit suite, extension suites, disposable lifecycle suite, local install/refresh
**Target Platform**: macOS maintainer checkout and disposable initialized Codex consumer
**Project Type**: Versioned local bundle and catalog
**Performance Goals**: No permanent server or external service
**Constraints**: Source provenance, explicit package pins, no remote publication or implicit acceptance
**Scale/Scope**: One local catalog release and one disposable consumer

## Constitution Check

The bundle composes independently versioned source packages. The Diagram is not a runtime dependency. The local catalog builder records provenance and refuses dirty or mismatched sources. A no-op consumer test proves dispatch only; human review and adoption remain separate. No new framework, service, or model-selection behavior is proposed. Analyze artifacts before implementation and converge afterward.

**Post-design check**: The release contract and validation guide preserve these rules. No exception is required.

## Project Structure

### Documentation (this feature)

```text
specs/011-bundle-catalog/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── contracts/release-lifecycle.md
├── quickstart.md
├── checklists/requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
bundles/spec-kit-flow/bundle.yml
catalog/release.json
catalog/packages/
tools/catalog.py
tests/test_catalog.py
tests/test_bundle_lifecycle.py
docs/installation.md
docs/feedback.md
mise.toml
```

**Structure Decision**: Use the existing release builder; change only the bundle pin, generated release payload, focused integrity test, and source-current docs unless verification finds a concrete defect.
