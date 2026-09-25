# Tasks: Bundle Catalog and Lifecycle

**Input**: Design artifacts in `specs/011-bundle-catalog/`

**Prerequisites**: [spec.md](spec.md), [plan.md](plan.md), [research.md](research.md), [release contract](contracts/release-lifecycle.md)

**Tests**: Catalog integrity, focused extensions, disposable lifecycle, and local released-catalog consumer path.

## Phase 1: Setup

Capture current source and tool coordinates.

- [x] T001 Record current bundle version/digest, CLI version, external source tags/commits, feedback source commit, and baseline Git commit in `specs/011-bundle-catalog/validation.md`

## Phase 2: Foundation

Check artifact consistency and source cleanliness before build.

- [x] T002 Analyze `specs/011-bundle-catalog/spec.md`, `specs/011-bundle-catalog/plan.md`, and `specs/011-bundle-catalog/tasks.md`, then reconcile material findings
- [x] T003 Verify clean Roadmap and Wiki tagged checkouts and committed feedback source

## Phase 3: User Story 1 - Build a Provenance-Bound Bundle (P1)

**Goal**: Produce a versioned local release whose package bytes match reviewed source.

**Independent Test**: Verify catalog release and inspect archive manifest/script.

- [x] T004 [US1] Bump `bundles/spec-kit-flow/bundle.yml` to `0.3.1` and pin `flow-feedback` `0.2.1`
- [x] T005 [US1] Run `tools/catalog.py build` with clean tagged external checkouts to regenerate `catalog/release.json` and `catalog/packages/flow-feedback-0.2.1.zip`
- [x] T006 [US1] Update the feedback package integrity case in `tests/test_catalog.py` and verify all catalog coordinates and hashes

## Phase 4: User Story 2 - Install and Refresh in a Disposable Consumer (P2)

**Goal**: Verify bundle-native install and refresh with the updated feedback package.

**Independent Test**: Run focused suites and a temporary released-catalog consumer.

- [x] T007 [US2] Run catalog, consumer feedback, and maintainer intake unit suites plus `tests/test_bundle_lifecycle.py`
- [x] T008 [US2] Run `tools/catalog.py install` and `refresh` against a temporary consumer with the tested CLI; inspect bundle and feedback version

## Phase 5: User Story 3 - Remove Without Claiming Adoption (P3)

**Goal**: Preserve consumer-owned state and report local evidence limits.

**Independent Test**: Inspect disposable lifecycle removal assertions and temporary consumer results.

- [x] T009 [US3] Verify removal retains unrelated workflow and feedback journal in `tests/test_bundle_lifecycle.py`
- [x] T010 [US3] Update `docs/installation.md` and `docs/feedback.md` with current coordinates and limits

## Phase 6: Polish and Validation

Close build gaps and inspect changed scope.

- [x] T011 Run convergence across `specs/011-bundle-catalog/`, bundle, catalog, tests, and docs
- [x] T012 Run `git diff --check` and verify changed project files contain no personal name or local username

## Dependencies and Execution Order

T001 precedes T002 and T003. T004 follows T002 and T003. T005 follows T004; T006 follows T005. Complete the release before consumer checks and documentation. T011 and T012 close the feature.

## Implementation Strategy

Keep the existing builder and deterministic package format. Regenerate the release from committed sources, test the released path in a disposable consumer, and report the limits of local validation.
