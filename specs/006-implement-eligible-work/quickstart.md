# Validation Guide: Implement Eligible Work

Use a disposable initialized Codex consumer with the pinned bundle and compatible Specify CLI. Record CLI and workflow versions, source digest, and observed result.

1. Inspect `specify workflow info speckit-flow-implement` and compare inputs and routes with [the contract](contracts/implementation-routing.md).
2. Run a no-op `blocked` route. Confirm native completion and no follow-on convergence or implementation dispatch. This does not execute real tasks.
3. Inspect each return route in the reviewed source. Confirm it invokes the named artifact command for the same feature and does not automatically resume implementation.
4. Review a real implementation and its task evidence in a separate human-directed consumer session before accepting completeness or convergence readiness.
