# Feedback Capture and Transfer

The consumer-side `flow-feedback` extension records workflow, preset, and agent-run observations in the consumer's local `.specify/workflow-feedback/observations.jsonl` journal. It is offline, append-only, and does not require access to the Spec Kit Flow source checkout. Its commands are `speckit.flow-feedback.capture` and `speckit.flow-feedback.report`.

Capture an observation from a JSON file, then export the journal to a portable JSON report and a readable Markdown projection. The extension rejects raw transcripts, secrets, credentials, private keys, and absolute host paths. Before transfer, review the report for any context that should be further generalized.

The bundled `flow-feedback` `0.2.1` rejects absolute host paths embedded after punctuation or written as `file://` URLs while allowing relative evidence references and HTTPS links. The `spec-kit-flow` `0.3.1` local release contains this version in its checksum-pinned archive.

Transfer reports through an explicit human-approved attachment, commit, or handoff. Only the separate `speckit-flow-feedback-maintainer` component can intake them. Consumer capture and reporting never mutate an installed workflow, preset, upstream source package, roadmap, Git state, or agent policy.

The maintainer checkout writes accepted reports and triage proposals under `feedback/inbox/` and `feedback/triage/`. These generated records are local evidence and are ignored by Git. Review an accepted finding and record its scope, provenance, and disposition in a tracked specification or approved roadmap amendment before relying on it as a project change. An explicit, reviewed transfer may still use a separate committed artifact; intake itself does not commit records.

Codex is the only initially supported integration. The execution profile may describe an observed capability label or role, but neither the capture nor report command selects or dispatches an agent.
