# Research: Bundle Catalog and Lifecycle

## Decision: Patch-release the composed bundle

`flow-feedback` source advanced from `0.2.0` to `0.2.1`, while the eight workflow versions and Roadmap/Wiki tags remain unchanged. Bump the bundle from `0.3.0` to `0.3.1` and pin feedback `0.2.1` so release metadata can distinguish changed package bytes.

**Rationale**: The builder rejects changed content under an unchanged released bundle version, and exact pins keep consumer installs reviewable.

## Decision: Regenerate, then verify package bytes

Use `tools/catalog.py build` with the clean tagged external checkouts. Inspect `release.json`, package manifest/script, checksums, source commits, and the diff. Retain the older `0.2.0` archive as historical local artifact; the new release manifest points only to `0.2.1`.

**Alternative considered**: Edit the ZIP or release JSON manually. Rejected because it would bypass deterministic packaging and provenance checks.

## Decision: Test the released path

The disposable lifecycle fixture now extracts the checksum-pinned feedback release archive. Run it after rebuilding, plus `catalog.verified_release()` and a temporary consumer install/refresh through `tools/catalog.py`.

**Rationale**: Source tests, manifest checks, and installed consumer checks establish different parts of the contract.
