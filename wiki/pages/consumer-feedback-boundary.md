---
title: Consumer feedback boundary
type: concept
sources: [S001, S002, S004, S014, S015]
updated: 2026-09-30
---

# Consumer feedback boundary

Consumer feedback is local evidence. Capture and export produce portable reports; maintainer intake validates them and proposes a disposition. None of these steps directly changes workflows, presets, installed components, roadmaps, Git state, or agent policy. Approved changes return to the ordinary specification, planning, task, and implementation flow. (S001, S002, S004)

The consumer-side `flow-feedback` extension records workflow, preset, and agent-run observations in an offline, append-only `.specify/workflow-feedback/observations.jsonl` journal. Its commands are `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`; it exports portable JSON and readable Markdown. (S004)

Reports are transferred through an explicit human-approved attachment, commit, or handoff. Only the separate `speckit-flow-feedback-maintainer` component performs maintainer intake. Reports should exclude raw transcripts, secrets, credentials, private keys, and absolute host paths, and should be reviewed for context that needs generalization before transfer. (S001, S004)

Codex is the initially supported integration. An execution profile may record an observed capability label or role, but feedback capture and reporting do not select or dispatch agents. (S001, S004)

An observation records component identity, version, digest, execution context, expected and observed behavior, safety response, and evidence references. Capture rejects duplicate IDs and malformed journals before append; export revalidates observations and produces deterministic JSON with an integrity digest and a Markdown projection. (S014)

Portability validation rejects raw transcripts, sensitive values, and absolute host paths even when embedded after punctuation, while retaining relative evidence references and HTTPS links. (S014)

Maintainer intake is a separate component outside the consumer bundle. It checks report schema, digest, observation IDs, component provenance, evidence references, and redaction before recording a canonical inbox copy and bounded triage proposal. Invalid or nonportable reports create no records. (S015)

A repeated report digest creates a duplicate triage relationship without another inbox copy or source proposal. A disposition and rationale remain a proposal for review, not approval to change source. (S015)

Maintainer triage and package-change evidence must retain component IDs, versions, source digests, and observed results. Portable reports exclude raw transcripts, secrets, and absolute host paths. A local test result alone cannot establish publication, stock compatibility, or consumer adoption. (S001)

## Related pages

- [Project authority and review gates](./project-authority-and-review-gates.md)
- [Workflow lifecycle](./workflow-lifecycle.md)
