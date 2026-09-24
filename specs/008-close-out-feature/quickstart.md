# Validation Guide: Close Out Feature

Use a disposable initialized Codex consumer with the pinned bundle and compatible Specify CLI. Record CLI, workflow version and digest, and observed result.

1. Inspect `specify workflow info speckit-flow-closeout` and compare its inputs with [the routing contract](contracts/closeout-routing.md).
2. Run the focused `tests/test_bundle_lifecycle.py` suite with its local roadmap and wiki sources. The no-op missing-operation route checks native dispatch and an early stop only.
3. Inspect the approved, deferred, flow-back, and invalid routes in source. Confirm the exact-patch gate precedes roadmap write, wiki lint precedes commit-readiness review, and no route commits.
4. In a separately approved human-reviewed consumer session, exercise the actual completion operation, debrief, patch review, wiki curation, and lint before judging commit readiness.
