# Feature Specification: Bundle Catalog and Lifecycle

**Feature Branch**: `feature/time-machine-bundle-catalog`

**Created**: 2026-09-24

**Status**: Draft

**Input**: User description: "Package pinned components and guide verified bundle installation, refresh, and removal in consumer projects."

## User Scenarios & Testing

### User Story 1 - Build a Provenance-Bound Bundle (Priority: P1)

A maintainer composes compatible, versioned source packages into a local release catalog. The bundle records exact component versions, while the catalog records source commits, release tags where required, and archive checksums.

**Why this priority**: Consumer installation must resolve reviewed component bytes rather than whichever source tree happens to be nearby.

**Independent Test**: Build the catalog from clean tagged Roadmap and Wiki checkouts plus committed feedback source, then verify release metadata, archive checksums, and payload versions.

**Acceptance Scenarios**:

1. **Given** clean compatible sources, **when** the release builder runs, **then** it creates deterministic archives and release metadata matching the bundle pins.
2. **Given** a changed feedback source at `0.2.1`, **when** bundle `0.3.1` is built, **then** its pinned archive includes the updated validator and its source commit.

### User Story 2 - Install and Refresh in a Disposable Consumer (Priority: P2)

An operator installs the reviewed bundle into a clean non-Diagram Codex consumer, checks component provenance and native dispatch, and refreshes through the current catalog.

**Why this priority**: A valid manifest alone does not prove the complete consumer lifecycle.

**Independent Test**: Run the disposable lifecycle suite and the local catalog install/refresh route against a temporary consumer.

**Acceptance Scenarios**:

1. **Given** a compatible Specify CLI and reviewed catalog, **when** install runs, **then** the consumer receives the pinned extensions and eight workflows with a bundle record.
2. **Given** an installed bundle, **when** refresh runs, **then** the pinned components remain available and unrelated consumer-owned state survives.

### User Story 3 - Remove Without Claiming Adoption (Priority: P3)

An operator removes the bundle from the disposable consumer while preserving an unrelated workflow and consumer-owned feedback evidence. Local success remains bounded evidence, not a publication or live-agent quality claim.

**Why this priority**: Bundle ownership and consumer data have different lifecycles.

**Independent Test**: Verify post-removal state in the disposable lifecycle suite and review installation documentation.

**Acceptance Scenarios**:

1. **Given** a consumer with the bundle and unrelated workflow, **when** removal runs, **then** bundle-owned components are gone and unrelated workflow and feedback journal remain.
2. **Given** local lifecycle success, **when** validation is reported, **then** tested CLI/source coordinates and no-op-agent limits are explicit.

### Edge Cases

- A source version differs from a bundle pin, a source is dirty, or an external release tag is missing; the release builder fails before publishing a new catalog.
- A checksum or workflow source digest differs from release metadata; installation fails before a consumer mutation.
- Refresh encounters a removed bundle-owned component; independently installed components and consumer-owned feedback remain separate.

## Requirements

### Functional Requirements

- **FR-001**: The bundle MUST pin compatible versions of Roadmap, Wiki, consumer feedback, and all eight workflow packages, with Codex as the initial integration.
- **FR-002**: The catalog builder MUST verify source IDs, versions, clean feedback source, and clean annotated external release tags before creating a release.
- **FR-003**: The release catalog MUST record source commits, required tags, archive SHA-256 digests, workflow source digests, and release status.
- **FR-004**: The feedback package in bundle `0.3.1` MUST contain `flow-feedback` `0.2.1` and the corrected portable-path validator.
- **FR-005**: Install and refresh MUST verify catalog status, component checksums, workflow digests, bundle pins, and the tested Specify CLI version.
- **FR-006**: Disposable lifecycle validation MUST cover install, native resolution/dispatch, feedback export and intake handoff, refresh, and removal without deleting unrelated consumer components or feedback evidence.
- **FR-007**: Documentation MUST state the tested coordinates, local catalog command path, compatibility limits, and explicit human handoff for consumer adoption.
- **FR-008**: Local catalog construction and lifecycle tests MUST NOT imply remote publication, stock Spec Kit compatibility, live-agent quality, roadmap verification, Git integration, or feature acceptance.

### Key Entities

- **Bundle manifest**: Versioned composition contract with exact component pins.
- **Release catalog**: Provenance and checksum record for local package assets.
- **Package archive**: Deterministic runtime payload for an extension.
- **Consumer bundle record**: Installed ownership and version evidence.
- **Consumer-owned state**: Feedback journal and unrelated components retained across bundle removal.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Release verification passes and all catalog entries match the new bundle pins and checked-in archive bytes.
- **SC-002**: The disposable lifecycle suite passes install, refresh, and removal with the updated feedback archive.
- **SC-003**: A temporary consumer can use the local catalog install and refresh commands with the tested CLI.
- **SC-004**: Documentation and validation identify current source commits, versions, digests, and evidence limits.

## Assumptions

- Roadmap `v0.2.1` and Wiki `v2.0.1` source checkouts remain clean and at their annotated release tags.
- Feedback `0.2.1` source was committed in the prior Time Machine feature.
- The local catalog may be marked `released` without claiming remote publication.
