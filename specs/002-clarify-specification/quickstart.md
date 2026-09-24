# Validation Guide: Clarify Specification

Use an initialized disposable Codex consumer with the pinned bundle and a compatible Specify CLI. Record the CLI version, workflow version and source digest, and observed result.

1. Inspect `specify workflow info speckit-flow-clarify` and compare its input and gate options with [the contract](contracts/clarification.md).
2. Run one native workflow route with a no-op Codex executable and `clarification_decision=begin-planning`. Confirm completion without a follow-on planning run. This checks dispatch only.
3. Review the source route for `continue-clarification`, `defer`, and invalid decisions. Confirm each stops and that the manual route is documented.
4. In a separate human-reviewed consumer session, verify that real questions are answered by the operator and integrated incrementally. A no-op executable cannot validate that behavior.
