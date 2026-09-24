# Feedback Capture and Transfer

The consumer-side `flow-feedback` extension records workflow, preset, and agent-run observations in the consumer's local `.specify/workflow-feedback/observations.jsonl` journal. It is offline, append-only, and does not require access to the Spec Kit Flow source checkout. Its commands are `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`.

Capture an observation from a JSON file, then export the journal to a portable JSON report and a readable Markdown projection. The extension rejects raw transcripts, secrets, credentials, private keys, and absolute host paths. Before transfer, review the report for any context that should be further generalized.

The `flow-feedback` `0.2.1` source also rejects absolute host paths embedded after punctuation or written as `file://` URLs while allowing relative evidence references and HTTPS links. The bundle remains pinned to the released `0.2.0` archive until a reviewed catalog rebuild includes this source version.

Transfer reports through an explicit human-approved attachment, commit, or handoff. Only the separate `speckit-flow-feedback-maintainer` component can intake them. Consumer capture and reporting never mutate an installed workflow, preset, upstream source package, roadmap, Git state, or agent policy.

Codex is the only initially supported integration. The execution profile may describe an observed capability label or role, but neither the capture nor report command selects or dispatches an agent.
