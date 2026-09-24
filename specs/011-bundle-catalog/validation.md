# Validation: Bundle Catalog and Lifecycle

**Observed**: 2026-09-24

## Source coordinates

- Bundle: `spec-kit-flow` `0.3.1` at `bundles/spec-kit-flow/bundle.yml`, SHA-256 `ec9eb17af4fbbbe0760b865eb0c470d32e85a3aa9e401259a61119f1c63b2644`; baseline bundle was `0.3.0` at SHA-256 `3308fd1f69ad69d995a7b0a18501ebfabb590936a759372011ec97eaf7a8952f`.
- Roadmap: `flow-roadmap` `0.2.1`, clean annotated tag `v0.2.1`, commit `86b0cc70054b7eca4d715fbccd6448165a85fc1f`.
- Wiki: `flow-wiki` `2.0.1`, clean annotated tag `v2.0.1`, commit `0292ff66758e36849cee4e0f6bcbdac51629e1d0`.
- Consumer feedback: `flow-feedback` `0.2.1`, clean source recorded at commit `4eeddd9be6d16ce726df58acd4508a074d454c5a`; archive SHA-256 `c666b11aa9f10c49ef879191a30a1f06d593d6fe7e404d71a0fc7145d0c75670`.
- Baseline Git commit: `4eeddd9`.
- Tested Specify CLI: `1.0.10.dev0+pegagio.2` on macOS.

## Observed checks

- Prerequisite inspection found the specification, plan, tasks, research, data model, contract, and quickstart. Cross-artifact analysis found no blocking inconsistency.
- `tools/catalog.py build` regenerated local release metadata and the `flow-feedback-0.2.1.zip` runtime archive from committed source. `catalog.verified_release()` passed; release status is `released`, all pins match, the archive checksum matches metadata, and its script bytes match the reviewed source. The older `0.2.0` archive remains unreferenced by this release.
- Four catalog tests, five consumer feedback tests, and eight maintainer intake tests passed. The disposable native bundle lifecycle suite passed both non-skipped tests with local Roadmap and Wiki source checkouts; it installed the `0.2.1` archive, exercised no-op workflow routes and feedback handoff, refreshed, and removed the bundle while retaining unrelated consumer state.
- The checked-in `tools/catalog.py install` and `refresh` commands succeeded against a temporary initialized consumer. Its bundle record identified `spec-kit-flow`, the installed feedback manifest declared `0.2.1`, and refresh reported 11 components refreshed with zero removed.
- The new archive contains four runtime entries and no personal-name, username, or host-home path bytes. Convergence review found no remaining build gap. `git diff --check` passed, and changed project files contain no personal name or local username.

## Evidence limits

The catalog is released locally, not published remotely. The temporary consumer and no-op Codex executable prove native installation, routing, refresh, and removal, not live-agent quality, fresh-machine reproducibility, stock Spec Kit compatibility, or real consumer adoption. Human roadmap verification, Git integration, and feature acceptance remain separate decisions.
