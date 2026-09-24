# Validation: Start Eligible Feature

**Observed**: 2026-09-24

## Source coordinates

- Workflow: `speckit-flow-start-feature` `0.2.0` at `workflows/speckit-flow-start-feature/workflow.yml`, SHA-256 `e3e6351fe812c4c4093f3ca2311a7de967a14d2700bd52f87bc6b15b10afeb57`.
- Bundle: `spec-kit-flow` `0.3.0`, pinning `flow-roadmap` `0.2.1` and `flow-wiki` `2.0.1`.
- Baseline Git commit: `603e84b` on the feature branch's parent.
- Tested Specify CLI: `1.0.10.dev0+pegagio.2` on macOS.

## Artifact analysis

All nine functional requirements map to the workflow inspection, the bundle check, the manual fallback review, or the disposable consumer test in `tasks.md`. The initial lifecycle test covered native `converge` dispatch but not `start-feature`; T004 was revised to add a deferred start route before implementation. No constitutional conflict or unresolved specification question was found.

## Observed checks

- Source inspection confirms candidate assessment precedes the patch gate; only the approved case invokes `speckit.flow-roadmap.write`; context lookup, specification drafting, and roadmap brief follow approval; and the final gate offers the next human choice without dispatching another phase.
- Source inspection confirms amendment, context resolution, deferral, and an invalid patch decision route to stop prompts rather than the approved command chain.
- The disposable lifecycle suite passed both tests with the pinned local roadmap and wiki source checkouts. Its new no-op deferred start run completed without adding feature files. The first sandbox attempt failed because localhost socket binding was denied; the identical test passed with localhost permission.
- `workflows/README.md` now gives the manual start-feature sequence and its approval boundary.
- Convergence found no remaining source or task gap within the reviewed workflow package. The live-agent approved route remains a separate consumer acceptance decision.
- `git diff --check` passed; the feature artifacts and changed source contain no personal name or local username, and no trailing whitespace was found.

## Evidence limits

The no-op Codex executable establishes native dispatch and deferred-route wiring. It does not judge roadmap eligibility, produce cited context, exercise the approved route with a live agent, or prove the quality of a resulting specification and brief. Those remain human-reviewed consumer acceptance work. This validation does not claim remote publication or compatibility with stock Spec Kit.
