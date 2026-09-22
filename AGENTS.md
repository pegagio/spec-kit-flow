# Spec Kit Flow Agent Guidance

Spec Kit Flow is the reusable, human-directed, merge-bounded flow-back workbench for Spec-Driven Development. The `spec-kit-flow` repository and bundle own generic source; reusable workflow and extension IDs use `speckit-flow-<purpose>`. Read [the project status](docs/project-status.md) before assuming a component is released or an installation path is available.

## Authority and scope

- This repository is the source of generic workflow definitions, any separately approved reusable preset, portable consumer feedback capture/report, and maintainer-only feedback intake. Edit reviewed source packages, not installed copies in a consumer's `.specify/` directory.
- A bundle composes versioned components; it is not the source of their behavior. The generic bundle requires compatible roadmap and wiki extensions and initially supports Codex only.
- The Diagram is a consumer, not a runtime prerequisite. Diagram registration, canonical work, projections, adapter feedback, and future orchestration belong to a separately versioned Diagram adapter and its own authority decisions. Do not add them to the generic bundle.
- The human selects tasks and agents. Workflows must not select models, assign or launch agents, schedule work, or turn a successful command into implicit roadmap verification, Git integration, feature acceptance, or Diagram acceptance.
- Preserve the explicit gates for roadmap patches, constitutional amendments, authority or material-scope changes, ambiguous recovery, and other consequential decisions. Routine remediation may flow back through the smallest affected spec, plan, or task artifact only within the operator-issued controller scope.
- Consumer feedback is local evidence. Exported reports are portable handoffs; maintainer intake validates and proposes a disposition. Neither capture nor intake directly edits a workflow, preset, installed component, roadmap, or runtime authority. Approved changes re-enter the normal specification, planning, task, and implementation flow.

## Working conventions

- Keep the eight `workflows/speckit-flow-*/workflow.yml` packages independently reviewable and preserve a manual-prompt fallback. Keep planning and task generation separate.
- Treat the five-question clarification cap as a current command/template behavior. A custom preset and its continuation policy remain unapproved follow-up work; do not imply the existing workflow removes the cap.
- Validate source definitions and bundle behavior in disposable initialized consumers. A no-op Codex executable can test native dispatch, but it does not prove live-agent behavior. Preserve consumer-owned feedback and unrelated components across bundle removal.
- Record component IDs, versions, source digests, and observed results when changing a package or triaging feedback. Keep reports portable: no raw transcripts, secrets, or absolute host paths.
- Do not infer publication, compatibility with stock Spec Kit, or consumer adoption from local test success. Document the tested CLI version and source coordinates explicitly.

The original design rationale and dogfood evidence originated in The Diagram's `specs/027-workflow-prompt-hardening/`. That history is provenance, not a required checkout or a competing authority for generic Spec Kit Flow source. Keep this repository self-contained as its behavior evolves.
