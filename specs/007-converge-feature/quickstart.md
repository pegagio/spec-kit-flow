# Validation Guide: Converge Feature

Use a disposable initialized Codex consumer with the pinned bundle and compatible Specify CLI. Record the CLI version, workflow version and digest, and observed result.

1. Inspect `specify workflow info speckit-flow-converge` and compare inputs and routes with [the contract](contracts/convergence-routing.md).
2. Run the existing `tests/test_bundle_lifecycle.py` suite with its local roadmap and wiki sources. Its no-op `clean` route verifies native dispatch only.
3. Inspect the remediation route in source. Confirm it invokes analysis before a separate implementation run and that the blocked route preserves evidence.
4. In a human-reviewed consumer session, compare real implementation with artifacts and review any appended remediation tasks before accepting a clean result.
