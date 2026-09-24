# Validation: Consumer Feedback

**Observed**: 2026-09-24

## Source coordinates

- Extension source: `flow-feedback` `0.2.1` at `extensions/flow-feedback/extension.yml`, manifest SHA-256 `a0fbcb23b65d20840f963f90fa023117b3789446c87dae69abb4deb9777f48d1`.
- Updated source script SHA-256: `b2ed233a85919f06f701bc910cf2aaa299aa1ee5f758b8c028f15acb4e1ea7be`.
- Pinned bundle: `spec-kit-flow` `0.3.0` with `flow-feedback` `0.2.0`; released archive `flow-feedback-0.2.0.zip`.
- Baseline Git commit: `104fae4`.
- Tested Specify CLI: `1.0.10.dev0+pegagio.2` on macOS.

## Observed checks

- Prerequisite inspection found the specification, plan, tasks, research, data model, contract, and quickstart. Cross-artifact analysis found no blocking inconsistency.
- The new embedded-path test failed against the original source for colon, parenthesis, and `file://` forms, then all five focused extension tests passed after the validator change. Relative evidence references and HTTPS URLs remain accepted.
- Source inspection confirms validated canonical JSONL capture, duplicate rejection, report revalidation and integrity digest, Markdown projection, and no network or source-authority mutation.
- The lifecycle fixture now extracts the checksum-pinned released feedback archive for bundle tests. Both disposable lifecycle tests passed with the pinned local roadmap and wiki source checkouts. Four catalog tests passed.
- Convergence review found no remaining source or test gap in this feature. `git diff --check` passed, and changed project files contain no personal name or local username.

## Evidence limits

The focused tests validate `0.2.1` source. The disposable lifecycle test validates the currently released `0.2.0` archive, not the new validator. The later bundle-catalog feature must repackage and pin `0.2.1` before claiming installed consumer availability. Export still requires human review and transfer; neither capture nor export approves a source change.
