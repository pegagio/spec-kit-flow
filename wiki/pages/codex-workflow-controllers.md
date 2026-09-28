---
title: Codex workflow controller design
type: concept
sources: [S018, S019]
updated: 2026-09-28
---

# Codex workflow controller design

The roadmap records Feature 013 as verified: direct `flow-kit-*` Codex skills are installed through the FlowKit catalog alongside the Specify bundle, with reviewed step models and a main-task controller. Feature 013 depends on verified Feature 011, not planned Feature 012. Verification remains distinct from publication and feature acceptance. (S018)

The completed Feature 013 specification defines eight direct, explicitly invoked `flow-kit-*` skills with stable FlowKit display names, each bound to one installed workflow in the selected consumer project. Completion of the specification does not by itself establish publication or compatibility outside the recorded validation context. (S019)

The installed workflow remains the authority for prompts, commands, branches, and gates. Controllers cannot copy those decisions into a skill, launch a later phase, select an undeclared fallback, or turn command completion into Git integration, roadmap verification, or feature acceptance. Manual workflow paths remain available. (S019)

Model roles and consumer mappings are outside Feature 013; initial concrete model IDs may be non-portable. (S019)

## Step and interaction rules

A concrete model on an executable step makes it a bounded child step; unmodeled steps and human gates stay in the main task. FlowKit uses medium reasoning effort for a modeled step unless its reviewed declaration or one named-step operator override selects another supported effort. The controller shows and validates every effective model-effort pair across all branches before work begins and stops for an invalid or unavailable pair without fallback. (S019)

Clarification questions and review gates appear in the main task. The controller relays an accepted human answer to the same interactive child before continuation. Completing a workflow does not start the next phase. (S019)

## Stop and recovery rules

A failed child preserves partial project edits and stops without automatic rollback or retry. An interrupted main task preserves files and completed-step evidence without built-in resume. A rejected preflight creates no workflow run or recovery record. (S019)

After execution starts, a compact local record keeps workflow identity and version, step statuses, effective models and efforts, repository-relative changed files, and the blocker, without full child transcripts. A bundle or skill-package refresh lets an active child finish, then stops before another step and requires a new invocation. (S019)

## Delivery boundary

The FlowKit catalog route installs, refreshes, and removes its direct controller skills alongside pinned Specify workflows while preserving consumer-owned state. Native Specify bundle commands manage only their declared Specify components. Skill-name collisions or locally changed owned files stop unsafe replacement or removal. These are the completed specification's delivery and ownership contracts. (S019)

## Related pages

- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
