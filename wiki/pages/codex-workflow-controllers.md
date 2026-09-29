---
title: Codex workflow controller design
type: concept
sources: [S002, S018, S019, S020]
updated: 2026-09-29
---

# Codex workflow controller design

The roadmap records Feature 013 as verified: direct `flow-kit-*` Codex skills are installed through the FlowKit catalog alongside the Specify bundle, with reviewed step models and a main-task controller. Feature 013 depends on verified Feature 011, not planned Feature 012. Verification remains distinct from publication and feature acceptance. (S018)

The completed Feature 013 specification defines eight direct, explicitly invoked `flow-kit-*` skills with stable FlowKit display names, each bound to one installed workflow in the selected consumer project. Completion of the specification does not by itself establish publication or compatibility outside the recorded validation context. (S019)

The installed workflow remains the authority for prompts, commands, branches, and gates. Controllers cannot copy those decisions into a skill, launch a later phase, select an undeclared fallback, or turn command completion into Git integration, roadmap verification, or feature acceptance. Manual workflow paths remain available. (S019)

Model roles and consumer mappings are outside Feature 013; initial concrete model IDs may be non-portable. (S019)

Verified Feature 015 uses reviewed Codex custom-agent names on explicitly delegated steps, with consumer-owned native agent files and Codex-managed optional model and effort settings. Its [assignment contract](./agent-roles-and-inheritance.md) supersedes the concrete step-model approach for updated workflows without rewriting verified Feature 013 history. (S018, S020)

## Step and interaction rules

Feature 013's earlier controller used concrete models and permitted a one-step model or effort override. In updated Feature 015 source, each delegated step instead names a reviewed Codex custom agent; the controller validates all branches and probes each selected native agent before work. No per-run agent, model, or effort override is available. Main-task steps and human gates remain with the driving agent. (S002, S019)

Clarification questions and review gates appear in the main task. The controller relays an accepted human answer to the same interactive child before continuation. Completing a workflow does not start the next phase. (S019)

## Stop and recovery rules

A failed child preserves partial project edits and stops without automatic rollback or retry. An interrupted main task preserves files and completed-step evidence without built-in resume. A rejected preflight creates no workflow run or recovery record. (S019)

After execution starts, a compact local record keeps workflow identity and version, step statuses, reviewed agent assignments, repository-relative changed files, and the blocker, without full child transcripts. A bundle or skill-package refresh lets an active child finish, then stops before another step and requires a new invocation. (S002, S019)

## Delivery boundary

The FlowKit catalog route installs, refreshes, and removes its direct controller skills alongside pinned Specify workflows while preserving consumer-owned state. Native Specify bundle commands manage only their declared Specify components. Skill-name collisions or locally changed owned files stop unsafe replacement or removal. These are the completed specification's delivery and ownership contracts. (S019)

## Related pages

- [Agent roles and assignment inheritance](./agent-roles-and-inheritance.md)
- [Bundle and workflow model](./bundle-and-workflow-model.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
