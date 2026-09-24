# Validation: Maintainer Feedback Intake

**Observed**: 2026-09-24

## Source coordinates

- Maintainer extension source: `speckit-flow-feedback-maintainer` `0.1.1` at `extensions/speckit-flow-feedback-maintainer/extension.yml`, manifest SHA-256 `0d787c0744c93a074abc557bb8fa5c3f85e758ed176a188f74878aafc20253c3`.
- Updated intake script SHA-256: `eb4cc7528079ddbdc4f6bc8b68c4a789d2dc3f06ea26ecfafe4d6bce8c38e8c6`.
- Baseline Git commit: `f6735c1`.
- Tested Specify CLI: `1.0.10.dev0+pegagio.2` on macOS.

## Observed checks

- Prerequisite inspection found the specification, plan, tasks, research, data model, contract, and quickstart. Cross-artifact analysis found no blocking inconsistency.
- New tests failed against the original source for embedded report paths and unvalidated triage text. Further contract tests exposed rejection of consumer-valid bare component digests and acceptance of incomplete observations. All eight focused maintainer tests passed after aligning path, text, and observation validation.
- The disposable lifecycle suite passed both tests with local roadmap and wiki sources. Its maintainer intake runs from source into a temporary root; the consumer bundle still does not install this component.
- Source inspection confirms digest validation, component provenance, duplicate relationships, and proposal-only next actions. The existing inbox report passed the revised validator read-only; existing `feedback/inbox/` and `feedback/triage/` records were not modified.
- Convergence review found no remaining build gap in this component. `git diff --check` passed, and changed project files contain no personal name or local username.

## Evidence limits

Focused tests cover the new `0.1.1` source and bounded temporary-state intake. They do not approve a proposed source change, prove a human disposition is correct, or publish the maintainer extension. The consumer bundle contains only `flow-feedback`; transfer and maintainer review remain separate human actions.
