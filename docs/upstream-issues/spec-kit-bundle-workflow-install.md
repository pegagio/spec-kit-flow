# Spec Kit Bundle Installation Fails for Catalog-Sourced Workflows

## Summary

Spec Kit CLI 1.0.1 cannot install a bundle that includes a workflow resolved by ID from a workflow catalog. Extension components resolve and install successfully, but the first workflow component fails before the bundle record is written.

This blocks the normal clean-consumer installation path for bundles such as `spec-kit-flow`, which deliberately compose independent extension and workflow components instead of embedding copied files.

## Environment

- **Spec Kit CLI**: `1.0.1`
- **Consumer**: a newly initialized non-Diagram project using the Codex integration
- **Bundle source**: a local `bundle.yml` that declares catalog-resolved extensions and workflows
- **Catalog source**: a disposable localhost catalog with checksum-pinned extension archives and workflow YAML URLs

The test catalog is intentionally local and temporary. It proves that the failure is not caused by unavailable remote publication, missing workflow metadata, or the roadmap/wiki extension prerequisites.

## Reproduction

1. Create a clean project with `specify init --here --force --non-interactive --integration codex --integration-options=--skills`.
2. Configure a trusted extension catalog containing `roadmap`, `wiki`, and a generic feedback extension.
3. Configure a workflow catalog containing a workflow ID such as `speckit-flow-start-feature`.
4. Install a bundle that declares those extensions plus `speckit-flow-start-feature` as a workflow component.
5. Run `specify bundle install <bundle.yml>`.

## Actual behavior

The three extension prerequisites install. The first workflow then fails with an error equivalent to:

```text
Error: --dev source must be a workflow YAML file, supported archive, or
directory containing workflow.yml: speckit-flow-start-feature
Error: Failed to install workflow 'speckit-flow-start-feature'.
```

No successful bundle provenance record is written.

## Expected behavior

The bundle installer should resolve `speckit-flow-start-feature` through the configured workflow catalog, install its workflow YAML, continue with the remaining components, and write an installed-bundle record that attributes only the components contributed by the bundle.

## Diagnosis

`specify_cli.bundler.services.primitives._WorkflowKindManager.install()` delegates by directly calling the Typer command handler with only the workflow ID:

```python
workflow_add(component.id)
```

The handler defines `dev` with `typer.Option(False, "--dev", ...)`. When called directly rather than through Typer's command parsing, the omitted argument remains a truthy Typer option object instead of the Boolean `False`. The handler therefore follows its local-development branch and treats the workflow ID as a filesystem path.

## Suggested remediation

The bundler should avoid directly calling the Typer command handler. Prefer a non-CLI workflow-install service that accepts explicit typed arguments. As a targeted compatibility fix, the delegation must pass explicit primitive values, including `dev=False` and `from_url=None`, rather than relying on Typer defaults.

## Acceptance coverage

Add a regression test that creates a clean project with a localhost workflow catalog and installs a bundle containing at least one catalog-sourced workflow. The test should verify:

- the workflow installs from its catalog ID rather than the local `--dev` path;
- the bundle record attributes the installed workflow and extensions;
- `bundle update` refreshes the same workflow successfully; and
- `bundle remove` removes only components attributed to that bundle.

The Spec Kit Flow lifecycle test provides a consumer-level reproduction once this behavior is repaired.
