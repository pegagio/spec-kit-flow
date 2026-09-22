# Installation and Lifecycle

## Current local-development path

This repository has a GitHub remote but no published release artifact or catalog entry yet. During local development, validate each workflow with `specify workflow add --dev workflows/<workflow-id>` and validate each extension with `specify extension add --dev extensions/<extension-id>`. Use a disposable initialized consumer project and inspect installed provenance before running any workflow.

`bundles/spec-kit-flow/bundle.yml` is a version-pinned composition contract. Spec Kit bundles resolve component IDs through installed components or configured catalogs; a local bundle manifest does not embed its component payloads. The disposable localhost catalog in `tests/test_bundle_lifecycle.py` proves clean-consumer installation, local-source refresh, removal, and feedback export with the compatible Specify fork. General installation still needs a vetted published source for the pinned components.

## Future bundle lifecycle

After the owner creates a vetted install source, a consumer will inspect and install the bundle with:

```text
specify bundle validate --path <bundle-directory>
specify bundle info spec-kit-flow
specify bundle install <bundle-source>
```

The consumer must resolve compatible `roadmap`, `wiki`, and Codex prerequisites. Missing or incompatible prerequisites are failures, not substitutions. Inspect installed bundle and component provenance after installation.

For a released local-source revision, refresh with `specify bundle install <bundle-source> --refresh`. For a catalog source, use `specify bundle update spec-kit-flow`. Refresh may remove components previously owned by the bundle but omitted from the revised manifest; independently installed components remain untouched. If refresh fails, inspect the result because Spec Kit does not promise rollback of every already-modified installed component.

Remove the bundle with `specify bundle remove spec-kit-flow`. Confirm that unrelated independently installed components remain and that the local feedback journal is retained as consumer-owned evidence. A consumer must not install `speckit-flow-feedback-maintainer`; maintainer intake belongs only in the Spec Kit Flow source environment.
