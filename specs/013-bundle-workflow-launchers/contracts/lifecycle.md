# Controller Catalog Lifecycle Contract

The supported FlowKit catalog route composes the existing Specify bundle with one reviewed, directly authored Codex skill package. The Specify bundle keeps its eight workflow and independent extension pins; the skill package owns eight `flow-kit-*` skills and a shared controller helper. The skill package manifest and release metadata record its version, inventory, source digest, and alignment with the released bundle version. A changed skill package or workflow requires a new FlowKit catalog release version. Native `specify bundle` operations manage only the Specify components declared in `bundle.yml`; they do not install, refresh, or remove the Codex controller skills.

| Operation | Required result | Conflict behavior |
| --- | --- | --- |
| Install | `mise run catalog:install <consumer>` installs the Specify bundle and all eight direct Codex skills with their specified IDs and display names. | A consumer-owned same-name skill or shared-helper path is reported before changes; it is not replaced. |
| Refresh | `mise run catalog:refresh <consumer>` aligns the installed skill package and Specify workflows with the reviewed catalog release. | A locally edited owned file or an unexpected owner blocks replacement and remains available for review. |
| Remove | `mise run catalog:remove <consumer>` removes FlowKit-owned skills and shared helper alongside the Specify bundle; unrelated skills, feedback, and components remain. | A locally edited owned file is preserved and the unresolved ownership conflict is reported. |

Preflight the full skill and helper inventory before a lifecycle operation. Initial installation must verify the installed files and atomically write `.specify/flow-kit/skills-install.json` before a skill can run; refresh and removal apply the same ownership check before replacing or deleting files. The record holds the package version, workflow bindings, and installed-file digests. Refresh atomically replaces it after verifying the new inventory. Successful removal verifies that owned files are gone, then removes the record; it preserves separate `.specify/flow-controllers/runs/` recovery summaries. A failed or partial operation must report its actual state and must not claim a complete installation. The explicit `--development-snapshot` catalog mode applies to install and refresh only in disposable initialized consumers, uses the same lifecycle checks, and labels the result unreleased; ordinary install and refresh continue to reject snapshots. Only the supported catalog route is advertised as installing the combined FlowKit experience. The direct native Specify bundle commands remain available for their declared components and are documented with that narrower scope.

## Installed-state example

```json
{
  "package": "flow-kit-controllers",
  "version": "<reviewed-version>",
  "bundle": "spec-kit-flow",
  "controllers": [
    {"skill": "flow-kit-clarify", "display_name": "FlowKit Clarify", "workflow": "speckit-flow-clarify"}
  ]
}
```

This is an abbreviated shape of the FlowKit ownership record, not a second workflow registry. The installed Specify bundle record remains authoritative for workflows and extensions.

## Validation boundary

Test catalog install, refresh, removal, naming collisions, locally edited skill or helper files, incomplete operations, and unrelated consumer data in disposable initialized consumers. Check package and workflow versions, source and installed-file digests, tested Specify CLI version, observed Codex skill paths, and all eight skill picker display names. A no-op Codex executable proves CLI routing only. At least one live desktop run must demonstrate selected-project context, effective model dispatch, same-child clarification, a main-task gate, visible results, and stopped-run evidence before claiming the controller UX works.
