# Consumer Feedback Portability Contract

`speckit.flow-feedback.capture` reads one JSON observation, validates its schema and sensitive content, and appends one canonical JSON line to the consumer-owned journal. Duplicate IDs and malformed existing journals stop without an append.

`speckit.flow-feedback.report` revalidates the journal, emits deterministic JSON with an integrity digest, and writes a Markdown projection from the same report. Both commands reject raw transcripts, sensitive keys and values, and absolute host paths in any string field. A host path after punctuation must be rejected; relative evidence references and HTTPS URLs remain valid.

Neither command contacts a source authority, edits an installed component, or applies a disposition. Export requires an explicit human transfer before maintainer intake.
