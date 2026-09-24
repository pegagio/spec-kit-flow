# Installation and Lifecycle

## Local catalog installation

The checkout contains bundle `0.3.1`, `catalog/release.json`, and checksum-pinned archives for `flow-roadmap` 0.2.1, `flow-wiki` 2.0.1, and `flow-feedback` 0.2.1. The catalog is marked `released` and records the Roadmap `v0.2.1` and Wiki `v2.0.1` annotated tags. The eight workflows are served from their reviewed source files. No external component checkouts or public catalog service are needed by a consumer. The compatible Specify CLI is a separate prerequisite: `mise.toml` pins the tested local fork but this checkout does not distribute it, and `mise install` succeeds only when that fork is obtainable in your environment.

For a released catalog, run `mise run catalog:install /path/to/consumer-project` from this repository's root. The consumer directory must exist and be outside this checkout; Specify initializes it if needed. The task verifies release status, package checksums, workflow hashes, bundle pins, and the exact tested Specify version, then starts a temporary loopback catalog and invokes native bundle installation. The server stops when the command finishes. Do not pass Specify's `--offline` flag: its component resolver treats the temporary loopback catalog as a network source, although no external catalog service is contacted.

The local `bundle.yml` remains a composition contract and does not embed component payloads. `mise run catalog:refresh /path/to/consumer-project` supplies a fresh temporary catalog and runs native bundle refresh from that manifest. Use this task for updates; a plain `specify bundle update` has no active catalog after the temporary server stops. Existing installed bundle records may contain the former loopback URL, which is transient; the release manifest in this checkout records durable source commits and package digests.

`flow-feedback` replaces the consumer extension ID `speckit-flow-feedback` and exposes `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`; the former command names are not aliases. In an existing consumer, retain its local feedback journal, install and verify the new extension, then remove or disable the former installation according to its ownership. A bundle refresh may remove an old bundle-owned component omitted from the new manifest; an independently installed old extension remains a separate installation.

## Release build and lifecycle

The release builder needs clean local checkouts of the independently maintained roadmap and wiki extensions at annotated tags matching the bundle's extension versions. The source repositories document their own release gates in `RELEASE.md`. From this repository's root, run:

```sh
mise run catalog:build /path/to/spec-kit-flow-roadmap /path/to/spec-kit-flow-wiki
```

The default builder checks source IDs and versions against `bundles/spec-kit-flow/bundle.yml`, refuses uncommitted extension source, verifies that each external checkout is at its matching annotated release tag, creates deterministic runtime archives, and records the source repository, tag, commit, version, and archive hash in `catalog/release.json`. Workflow hashes are recorded from source. For development packaging only, pass `--snapshot`; this marks the catalog as a snapshot that consumer install and refresh tasks reject. Review the generated package contents and diff before committing a release. Do not edit archives directly. Repository names are `spec-kit-flow-roadmap` and `spec-kit-flow-wiki`; their extension IDs are `flow-roadmap` and `flow-wiki`. The consumer still needs compatible Specify, Python 3, and Codex prerequisites. Missing or incompatible prerequisites are failures, not substitutions.

Refresh may remove components previously owned by the bundle but omitted from the revised manifest; independently installed components remain untouched. If refresh fails, inspect the result because Spec Kit does not promise rollback of every already-modified installed component.

Remove the bundle with `specify bundle remove spec-kit-flow`. Confirm that unrelated independently installed components remain and that the local feedback journal is retained as consumer-owned evidence. A consumer must not install `speckit-flow-feedback-maintainer`; maintainer intake belongs only in the Spec Kit Flow source environment.
