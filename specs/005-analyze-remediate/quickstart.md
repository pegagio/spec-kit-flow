# Validation Guide: Analyze and Remediate Artifacts

Use a disposable initialized Codex consumer with the pinned bundle and compatible Specify CLI. Record the CLI version, workflow version and digest, and observed result.

1. Inspect `specify workflow info speckit-flow-analyze-remediate` and compare gate options and route commands with [the contract](contracts/analysis-routing.md).
2. Run a no-op `clean` route. Confirm native completion and no implementation dispatch; this does not prove the artifacts are actually consistent.
3. Inspect each routine path in source and verify its artifact-update order and reanalysis. Inspect all consequential and invalid stop paths for absence of remediation commands.
4. Review real analysis and resulting artifact changes in a separate human-reviewed consumer session before accepting a clean implementation handoff.
