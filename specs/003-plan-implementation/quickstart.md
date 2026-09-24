# Validation Guide: Plan Implementation

Use a disposable initialized Codex consumer with the pinned bundle and a compatible Specify CLI. Record the CLI version, workflow source version and digest, and observed result.

1. Inspect `specify workflow info speckit-flow-plan` and compare gate options and commands with [the contract](contracts/planning.md).
2. Run the `defer` route with a no-op Codex executable; confirm completion without new planning artifacts. This proves terminal routing only.
3. Inspect the `plan`, `return-to-clarification`, and invalid-decision routes in the reviewed YAML. Verify that only the explicit `plan` choice can invoke `speckit.plan` and that no route launches task generation.
4. Review an actual plan and its artifacts in a separate live consumer session before accepting planning quality.
